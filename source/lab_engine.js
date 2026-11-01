/* Electronics lab engine: an Arduino-subset compiler and VM, plus a DC circuit solver. No DOM in this file. */
(function (root) {
  'use strict';

  // ---------- language: tokenizer ----------
  class CodeError extends Error { constructor(line, msg) { super(msg); this.line = line; } }
  const TYPE_WORDS = new Set(['void', 'int', 'long', 'short', 'unsigned', 'signed', 'byte', 'char', 'float', 'double', 'bool', 'boolean', 'String', 'uint8_t', 'int8_t', 'uint16_t', 'int16_t', 'uint32_t', 'int32_t', 'size_t', 'word', 'Servo']);
  const MODS = new Set(['const', 'static', 'volatile']);
  const OPS3 = ['<<=', '>>='];
  const OPS2 = ['==', '!=', '<=', '>=', '&&', '||', '++', '--', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<', '>>'];

  function tokenize(src) {
    const out = [], defines = {};
    let i = 0, line = 1;
    const n = src.length;
    function lexLine(text, ln) { return lexInner(text, ln); }
    function lexInner(text, ln) {
      const saved = [i, line]; const toks = scan(text, ln); i = saved[0]; line = saved[1]; return toks;
    }
    function scan(s, ln) {
      const res = []; let p = 0;
      while (p < s.length) {
        const c = s[p];
        if (c === '\n') { ln++; p++; continue; }
        if (c === ' ' || c === '\t' || c === '\r') { p++; continue; }
        if (c === '/' && s[p + 1] === '/') { while (p < s.length && s[p] !== '\n') p++; continue; }
        if (c === '/' && s[p + 1] === '*') {
          p += 2;
          while (p < s.length && !(s[p] === '*' && s[p + 1] === '/')) { if (s[p] === '\n') ln++; p++; }
          p += 2; continue;
        }
        if (c === '#') {
          let e = p; while (e < s.length && s[e] !== '\n') e++;
          const d = s.slice(p, e).match(/^#\s*define\s+([A-Za-z_]\w*)\s*(.*)$/);
          if (d) defines[d[1]] = scan(d[2].replace(/\/\/.*$/, ''), ln);
          p = e; continue;
        }
        if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(s[p + 1] || ''))) {
          let e = p, isF = false;
          if (c === '0' && /[xX]/.test(s[p + 1] || '')) { e += 2; while (/[0-9a-fA-F]/.test(s[e] || '')) e++; }
          else { while (/[0-9.]/.test(s[e] || '')) { if (s[e] === '.') isF = true; e++; }
            if (/[eE]/.test(s[e] || '') && /[0-9+-]/.test(s[e + 1] || '')) { isF = true; e += 2; while (/[0-9]/.test(s[e] || '')) e++; } }
          const v = Number(s.slice(p, e));
          while (/[uUlLfF]/.test(s[e] || '')) { if (/[fF]/.test(s[e])) isF = true; e++; }
          res.push({ t: 'num', v, f: isF, line: ln }); p = e; continue;
        }
        if (/[A-Za-z_]/.test(c)) {
          let e = p; while (/\w/.test(s[e] || '')) e++;
          const w = s.slice(p, e);
          if (defines[w]) res.push(...defines[w].map(x => Object.assign({}, x, { line: ln })));
          else res.push({ t: 'id', v: w, line: ln });
          p = e; continue;
        }
        if (c === '"') {
          let e = p + 1, v = '';
          while (e < s.length && s[e] !== '"' && s[e] !== '\n') {
            if (s[e] === '\\') { e++; const m = { n: '\n', t: '\t', '"': '"', '\\': '\\' }; v += m[s[e]] !== undefined ? m[s[e]] : s[e]; } else v += s[e];
            e++;
          }
          if (s[e] !== '"') throw new CodeError(ln, 'This text is missing its closing " mark.');
          res.push({ t: 'str', v, line: ln }); p = e + 1; continue;
        }
        if (c === "'") {
          let v = s[p + 1], e = p + 2;
          if (v === '\\') { v = { n: '\n', t: '\t' }[s[p + 2]] || s[p + 2]; e = p + 3; }
          if (s[e] !== "'") throw new CodeError(ln, "A character needs a closing ' mark.");
          res.push({ t: 'chr', v: v.charCodeAt(0), line: ln }); p = e + 1; continue;
        }
        const a = s.substr(p, 3), b = s.substr(p, 2);
        if (OPS3.includes(a)) { res.push({ t: 'op', v: a, line: ln }); p += 3; continue; }
        if (OPS2.includes(b)) { res.push({ t: 'op', v: b, line: ln }); p += 2; continue; }
        if ('+-*/%=<>!&|^~?:;,.(){}[]'.includes(c)) { res.push({ t: 'op', v: c, line: ln }); p++; continue; }
        throw new CodeError(ln, 'I don\'t understand the character "' + c + '" here.');
      }
      return res;
    }
    void lexLine; void n;
    const toks = scan(src, 1);
    const last = toks.length ? toks[toks.length - 1].line : 1;
    toks.push({ t: 'eof', v: 'end of the code', line: last });
    return out.concat(toks);
  }

  // ---------- language: parser ----------
  const PREC = { '||': 1, '&&': 2, '|': 3, '^': 4, '&': 5, '==': 6, '!=': 6, '<': 7, '<=': 7, '>': 7, '>=': 7, '<<': 8, '>>': 8, '+': 9, '-': 9, '*': 10, '/': 10, '%': 10 };
  const ASSIGN = new Set(['=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=']);

  class Parser {
    constructor(toks) { this.toks = toks; this.p = 0; }
    get cur() { return this.toks[this.p]; }
    next() { return this.toks[this.p++]; }
    is(v) { const c = this.cur; return (c.t === 'op' || c.t === 'id') && c.v === v; }
    accept(v) { if (this.is(v)) { this.p++; return true; } return false; }
    expect(v, why) {
      if (this.accept(v)) return;
      const c = this.cur, prev = this.toks[this.p - 1];
      const at = v === ';' && prev ? prev.line : c.line;
      throw new CodeError(at, why || `Expected "${v}" before "${c.v}".` + (v === ';' ? ' Most lines end with a semicolon.' : ''));
    }
    ident(why) { const c = this.cur; if (c.t !== 'id') throw new CodeError(c.line, why || `Expected a name, found "${c.v}".`); this.p++; return c.v; }
    isType(k = 0) { const c = this.toks[this.p + k]; return c && c.t === 'id' && (TYPE_WORDS.has(c.v) || MODS.has(c.v)); }

    type() {
      while (this.cur.t === 'id' && MODS.has(this.cur.v)) this.p++;
      let unsigned = false, word = null, extra = null;
      while (this.cur.t === 'id' && TYPE_WORDS.has(this.cur.v)) {
        const w = this.next().v;
        if (w === 'unsigned') unsigned = true;
        else if (w === 'signed') unsigned = false;
        else if (!word) word = w; else extra = w;
      }
      void extra;
      if (!word && !unsigned) throw new CodeError(this.cur.line, `Expected a type such as int, found "${this.cur.v}".`);
      const map = { void: 'void', int: unsigned ? 'u16' : 'i16', short: 'i16', long: unsigned ? 'u32' : 'i32', byte: 'u8', char: unsigned ? 'u8' : 'chr', float: 'f', double: 'f', bool: 'bool', boolean: 'bool', String: 'str', uint8_t: 'u8', int8_t: 'i8', uint16_t: 'u16', int16_t: 'i16', uint32_t: 'u32', int32_t: 'i32', size_t: 'u32', word: 'u16', Servo: 'servo' };
      return word ? map[word] : 'u16';
    }

    program() {
      const items = [];
      while (this.cur.t !== 'eof') {
        const line = this.cur.line;
        if (!this.isType()) throw new CodeError(line, `Code outside a function must start with a type, such as "int" or "void". Found "${this.cur.v}".`);
        const ty = this.type(), name = this.ident();
        if (this.accept('(')) {
          const params = [];
          if (this.is('void') && this.toks[this.p + 1].v === ')') this.p++;
          while (!this.is(')')) {
            const pt = this.type(), pn = this.cur.t === 'id' ? this.next().v : null;
            let arr = false; if (this.accept('[')) { this.expect(']'); arr = true; }
            params.push({ ty: pt, name: pn, arr });
            if (!this.accept(',')) break;
          }
          this.expect(')');
          if (this.accept(';')) continue;
          if (!this.is('{')) throw new CodeError(this.cur.line, 'A function needs its code inside { and }.');
          items.push({ k: 'fn', ty, name, params, body: this.block(), line });
        } else {
          items.push(...this.declRest(ty, name, line));
          this.expect(';');
        }
      }
      return items;
    }

    declRest(ty, name, line) {
      const out = [];
      for (;;) {
        const d = { k: 'decl', ty, name, line, arr: false, size: null, init: null, list: null };
        if (this.accept('[')) { d.arr = true; if (!this.is(']')) d.size = this.expr(); this.expect(']'); }
        if (this.accept('=')) {
          if (this.accept('{')) {
            d.list = [];
            while (!this.is('}')) { d.list.push(this.expr()); if (!this.accept(',')) break; }
            this.expect('}');
          } else d.init = this.expr();
        }
        out.push(d);
        if (!this.accept(',')) break;
        name = this.ident();
      }
      return out;
    }

    block() {
      const line = this.cur.line; this.expect('{');
      const body = [];
      while (!this.is('}')) {
        if (this.cur.t === 'eof') throw new CodeError(line, 'This { never gets its closing }.');
        body.push(...this.stmt());
      }
      this.next();
      return { k: 'block', body, line };
    }

    one() { const s = this.stmt(); return s.length === 1 ? s[0] : { k: 'block', body: s, line: this.cur.line }; }

    stmt() {
      const c = this.cur, line = c.line;
      if (this.is('{')) return [this.block()];
      if (this.accept(';')) return [];
      if (this.accept('if')) {
        this.expect('('); const cond = this.expr(); this.expect(')');
        const a = this.one(); let b = null;
        if (this.accept('else')) b = this.one();
        return [{ k: 'if', cond, a, b, line }];
      }
      if (this.accept('while')) { this.expect('('); const cond = this.expr(); this.expect(')'); return [{ k: 'while', cond, body: this.one(), line }]; }
      if (this.accept('do')) {
        const body = this.one(); this.expect('while'); this.expect('('); const cond = this.expr(); this.expect(')'); this.expect(';');
        return [{ k: 'do', cond, body, line }];
      }
      if (this.accept('for')) {
        this.expect('('); let init = [];
        if (!this.is(';')) {
          if (this.isType()) { const ty = this.type(), n = this.ident(); init = this.declRest(ty, n, line); }
          else init = [{ k: 'expr', e: this.expr(), line }];
        }
        this.expect(';');
        const cond = this.is(';') ? null : this.expr(); this.expect(';');
        const step = this.is(')') ? null : this.expr(); this.expect(')');
        return [{ k: 'for', init, cond, step, body: this.one(), line }];
      }
      if (this.accept('return')) { const e = this.is(';') ? null : this.expr(); this.expect(';'); return [{ k: 'ret', e, line }]; }
      if (this.accept('break')) { this.expect(';'); return [{ k: 'brk', line }]; }
      if (this.accept('continue')) { this.expect(';'); return [{ k: 'cont', line }]; }
      if (this.is('switch')) throw new CodeError(line, 'This simulator doesn\'t run "switch" yet. Use if and else if instead.');
      if (this.isType() && !(this.toks[this.p + 1].v === '(' && !MODS.has(c.v))) {
        const ty = this.type(), name = this.ident();
        const d = this.declRest(ty, name, line); this.expect(';');
        return d;
      }
      const e = this.expr(); this.expect(';');
      return [{ k: 'expr', e, line }];
    }

    expr() {
      const l = this.ternary();
      if (this.cur.t === 'op' && ASSIGN.has(this.cur.v)) {
        const t = this.next();
        if (l.k !== 'var' && l.k !== 'idx') throw new CodeError(t.line, 'You can only assign to a variable.');
        return { k: 'assign', op: t.v, lhs: l, r: this.expr(), line: t.line };
      }
      return l;
    }
    ternary() {
      const c = this.bin(1);
      if (this.accept('?')) { const a = this.expr(); this.expect(':'); return { k: 'tern', c, a, b: this.ternary(), line: c.line }; }
      return c;
    }
    bin(min) {
      let l = this.unary();
      for (;;) {
        const t = this.cur, pr = t.t === 'op' ? PREC[t.v] : undefined;
        if (pr === undefined || pr < min) return l;
        this.p++;
        l = { k: 'bin', op: t.v, l, r: this.bin(pr + 1), line: t.line };
      }
    }
    unary() {
      const t = this.cur;
      if (t.t === 'op') {
        if (t.v === '-' || t.v === '!' || t.v === '~' || t.v === '+') { this.p++; return { k: 'un', op: t.v, e: this.unary(), line: t.line }; }
        if (t.v === '++' || t.v === '--') { this.p++; return { k: 'inc', op: t.v, pre: true, lhs: this.unary(), line: t.line }; }
        if (t.v === '(' && this.isType(1) && !MODS.has(this.toks[this.p + 1].v)) {
          this.p++; const ty = this.type(); this.expect(')');
          return { k: 'cast', ty, e: this.unary(), line: t.line };
        }
      }
      return this.postfix();
    }
    postfix() {
      let e = this.primary();
      for (;;) {
        const t = this.cur;
        if (t.t !== 'op') return e;
        if (t.v === '[') { this.p++; const i = this.expr(); this.expect(']'); e = { k: 'idx', a: e, i, line: t.line }; continue; }
        if (t.v === '++' || t.v === '--') { this.p++; e = { k: 'inc', op: t.v, pre: false, lhs: e, line: t.line }; continue; }
        if (t.v === '.') {
          this.p++; const m = this.ident(); this.expect('(');
          e = { k: 'mcall', obj: e, m, args: this.args(), line: t.line }; continue;
        }
        return e;
      }
    }
    args() {
      const a = [];
      while (!this.is(')')) { a.push(this.expr()); if (!this.accept(',')) break; }
      this.expect(')');
      return a;
    }
    primary() {
      const t = this.next();
      if (t.t === 'num') return { k: 'num', v: t.v, f: t.f, line: t.line };
      if (t.t === 'str') return { k: 'str', v: t.v, line: t.line };
      if (t.t === 'chr') return { k: 'chr', v: t.v, line: t.line };
      if (t.t === 'op' && t.v === '(') { const e = this.expr(); this.expect(')'); return e; }
      if (t.t === 'id') {
        if (this.is('(')) {
          this.p++;
          if (TYPE_WORDS.has(t.v)) {
            const a = this.args(); const m = { int: 'i16', long: 'i32', float: 'f', double: 'f', byte: 'u8', char: 'chr', word: 'u16', bool: 'bool', String: 'str' }[t.v];
            return { k: 'cast', ty: m || 'i16', e: a[0] || { k: 'str', v: '' }, line: t.line };
          }
          return { k: 'call', name: t.v, args: this.args(), line: t.line };
        }
        return { k: 'var', name: t.v, line: t.line };
      }
      throw new CodeError(t.line, `I didn't expect "${t.v}" here.`);
    }
  }

  // ---------- language: compiler to bytecode ----------
  const O = {}; ['PUSH', 'POP', 'DUP', 'DUP2', 'LG', 'SG', 'LL', 'SL', 'LI', 'SI', 'BIN', 'DIVI', 'MODI', 'UN', 'JMP', 'JZ', 'JNZ', 'CALL', 'BI', 'MC', 'RET', 'CONV', 'MKARR', 'NEWARR', 'NEWSERVO', 'FMT'].forEach((k, i) => { O[k] = i; });

  // name: [min args, max args, return type]
  const BUILTINS = {
    pinMode: [2, 2, 'v'], digitalWrite: [2, 2, 'v'], digitalRead: [1, 1, 'i'], analogWrite: [2, 2, 'v'], analogRead: [1, 1, 'i'],
    delay: [1, 1, 'v'], delayMicroseconds: [1, 1, 'v'], millis: [0, 0, 'i'], micros: [0, 0, 'i'], pulseIn: [2, 3, 'i'],
    tone: [2, 3, 'v'], noTone: [1, 1, 'v'], map: [5, 5, 'i'], constrain: [3, 3, '?'], min: [2, 2, '?'], max: [2, 2, '?'], abs: [1, 1, '?'],
    random: [1, 2, 'i'], randomSeed: [1, 1, 'v'], sqrt: [1, 1, 'f'], pow: [2, 2, 'f'], sin: [1, 1, 'f'], cos: [1, 1, 'f'], floor: [1, 1, 'f'], ceil: [1, 1, 'f'], round: [1, 1, 'f'],
  };
  const CONSTS = { HIGH: 1, LOW: 0, INPUT: 0, OUTPUT: 1, INPUT_PULLUP: 2, true: 1, false: 0, A0: 14, A1: 15, A2: 16, A3: 17, A4: 18, A5: 19, LED_BUILTIN: 13, PI: 3.141592653589793 };
  const cls = ty => (ty === 'f' ? 'f' : ty === 'str' ? 's' : ty === 'chr' ? 'c' : ty === 'servo' ? 'o' : ty === 'void' ? 'v' : 'i');

  function suggest(name, list) {
    const low = name.toLowerCase();
    const hit = list.find(x => x.toLowerCase() === low);
    if (hit) return ` Did you mean "${hit}"? Capital letters matter.`;
    const close = list.find(x => dist(x.toLowerCase(), low) <= 2);
    return close ? ` Did you mean "${close}"?` : '';
  }
  function dist(a, b) {
    const d = Array.from({ length: a.length + 1 }, (_, i) => [i]);
    for (let j = 1; j <= b.length; j++) d[0][j] = j;
    for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    return d[a.length][b.length];
  }

  class Compiler {
    constructor(items) { this.items = items; this.fns = {}; this.fnList = []; this.globals = {}; this.nglobals = 0; this.cur = null; this.scopes = []; this.loops = []; }
    run() {
      for (const it of this.items) if (it.k === 'fn') {
        if (this.fns[it.name]) throw new CodeError(it.line, `The function "${it.name}" is written twice.`);
        const f = { name: it.name, ty: it.ty, params: it.params, code: [], nlocals: 0, idx: this.fnList.length, node: it };
        this.fns[it.name] = f; this.fnList.push(f);
      }
      if (!this.fns.setup) throw new CodeError(1, 'Every sketch needs a "void setup()" function, even an empty one.');
      if (!this.fns.loop) throw new CodeError(1, 'Every sketch needs a "void loop()" function, even an empty one.');
      const init = { name: '__init', ty: 'void', params: [], code: [], nlocals: 0, idx: this.fnList.length };
      this.fnList.push(init); this.cur = init; this.scopes = [{}];
      for (const it of this.items) if (it.k === 'decl') {
        if (this.globals[it.name]) throw new CodeError(it.line, `The variable "${it.name}" is declared twice.`);
        const slot = this.nglobals++;
        this.globals[it.name] = { slot, ty: it.ty, arr: it.arr, g: true };
        this.declInit(it, this.globals[it.name]);
      }
      this.emit(O.PUSH, 0, 0); this.emit(O.RET, 0, 0);
      for (const f of this.fnList) if (f.node) this.fn(f);
      return { fns: this.fnList, init: init.idx, setup: this.fns.setup.idx, loop: this.fns.loop.idx, nglobals: this.nglobals };
    }
    emit(o, a, line) { this.cur.code.push({ o, a, l: line }); return this.cur.code.length - 1; }
    fn(f) {
      this.cur = f; f.nlocals = 0; this.scopes = [{}]; this.loops = [];
      for (const p of f.params) { const s = f.nlocals++; if (p.name) this.scopes[0][p.name] = { slot: s, ty: p.ty, arr: p.arr, g: false }; }
      this.stmt(f.node.body);
      this.emit(O.PUSH, 0, f.node.line); this.emit(O.RET, 0, f.node.line);
    }
    find(name) {
      for (let i = this.scopes.length - 1; i >= 0; i--) if (this.scopes[i][name]) return this.scopes[i][name];
      return this.globals[name];
    }
    declInit(d, v) {
      const L = d.line;
      if (d.ty === 'servo') { this.emit(O.NEWSERVO, 0, L); this.store(v, L); this.emit(O.POP, 0, L); return; }
      if (d.arr) {
        if (d.list) { for (const e of d.list) { this.expr(e); this.emit(O.CONV, d.ty, L); } this.emit(O.MKARR, [d.list.length, d.size ? 0 : d.list.length], L); }
        else { if (!d.size) throw new CodeError(L, `The array "${d.name}" needs a size or a list of values.`); this.expr(d.size); this.emit(O.NEWARR, d.ty, L); }
        this.store(v, L); this.emit(O.POP, 0, L); return;
      }
      if (d.init) { this.expr(d.init); this.emit(O.CONV, d.ty, L); }
      else this.emit(O.PUSH, d.ty === 'str' ? '' : 0, L);
      this.store(v, L); this.emit(O.POP, 0, L);
    }
    store(v, L) { this.emit(O.DUP, 0, L); this.emit(v.g ? O.SG : O.SL, v.slot, L); }
    stmt(s) {
      const L = s.line;
      switch (s.k) {
        case 'block': this.scopes.push({}); s.body.forEach(x => this.stmt(x)); this.scopes.pop(); return;
        case 'decl': {
          const sc = this.scopes[this.scopes.length - 1];
          if (sc[s.name]) throw new CodeError(L, `The variable "${s.name}" is already declared here.`);
          const v = { slot: this.cur.nlocals++, ty: s.ty, arr: s.arr, g: false };
          sc[s.name] = v; this.declInit(s, v); return;
        }
        case 'expr': this.expr(s.e); this.emit(O.POP, 0, L); return;
        case 'if': {
          this.expr(s.cond); const j = this.emit(O.JZ, 0, L); this.stmt(s.a);
          if (s.b) { const k = this.emit(O.JMP, 0, L); this.cur.code[j].a = this.cur.code.length; this.stmt(s.b); this.cur.code[k].a = this.cur.code.length; }
          else this.cur.code[j].a = this.cur.code.length;
          return;
        }
        case 'while': case 'do': case 'for': return this.loop(s);
        case 'ret':
          if (s.e) { this.expr(s.e); this.emit(O.CONV, this.cur.ty === 'void' ? 'i32' : this.cur.ty, L); } else this.emit(O.PUSH, 0, L);
          this.emit(O.RET, 0, L); return;
        case 'brk': if (!this.loops.length) throw new CodeError(L, '"break" only works inside a loop.'); this.loops[this.loops.length - 1].brk.push(this.emit(O.JMP, 0, L)); return;
        case 'cont': if (!this.loops.length) throw new CodeError(L, '"continue" only works inside a loop.'); this.loops[this.loops.length - 1].cont.push(this.emit(O.JMP, 0, L)); return;
        default: throw new CodeError(L, 'I can\'t run this line.');
      }
    }
    loop(s) {
      const L = s.line, code = this.cur.code, info = { brk: [], cont: [] };
      this.scopes.push({});
      if (s.k === 'for') s.init.forEach(x => this.stmt(x));
      const top = code.length; let jz = null;
      if (s.k !== 'do' && s.cond) { this.expr(s.cond); jz = this.emit(O.JZ, 0, L); }
      this.loops.push(info); this.stmt(s.body); this.loops.pop();
      const contAt = code.length;
      if (s.k === 'for' && s.step) { this.expr(s.step); this.emit(O.POP, 0, L); }
      if (s.k === 'do') { this.expr(s.cond); this.emit(O.JNZ, top, L); } else this.emit(O.JMP, top, L);
      const end = code.length;
      if (jz !== null) code[jz].a = end;
      info.brk.forEach(i => { code[i].a = end; }); info.cont.forEach(i => { code[i].a = contAt; });
      this.scopes.pop();
    }
    lvalType(n) {
      if (n.k === 'var') { const v = this.find(n.name); if (!v) throw new CodeError(n.line, `I don't know the variable "${n.name}". Did you declare it?`); return v.ty; }
      if (n.k === 'idx') return this.lvalType(n.a);
      throw new CodeError(n.line, 'You can only change a variable.');
    }
    expr(n) {
      const L = n.line;
      switch (n.k) {
        case 'num': this.emit(O.PUSH, n.v, L); return n.f ? 'f' : (Number.isInteger(n.v) ? 'i' : 'f');
        case 'str': this.emit(O.PUSH, n.v, L); return 's';
        case 'chr': this.emit(O.PUSH, n.v, L); return 'c';
        case 'var': {
          const v = this.find(n.name);
          if (v) { this.emit(v.g ? O.LG : O.LL, v.slot, L); return v.arr ? 'a' : cls(v.ty); }
          if (n.name in CONSTS) { this.emit(O.PUSH, CONSTS[n.name], L); return n.name === 'PI' ? 'f' : 'i'; }
          const names = Object.keys(this.globals).concat(Object.keys(CONSTS)); for (const sc of this.scopes) names.push(...Object.keys(sc));
          throw new CodeError(L, `I don't know "${n.name}". Did you declare it?` + suggest(n.name, names));
        }
        case 'idx': { const ty = this.lvalType(n.a); this.expr(n.a); this.expr(n.i); this.emit(O.LI, 0, L); return cls(ty); }
        case 'cast': { const t = this.expr(n.e); if (n.ty === 'str') { if (t === 'f') this.emit(O.FMT, 2, L); else if (t === 'c') this.emit(O.FMT, 'c', L); else this.emit(O.FMT, 's', L); return 's'; } this.emit(O.CONV, n.ty, L); return cls(n.ty); }
        case 'un': { const t = this.expr(n.e); this.emit(O.UN, n.op, L); return n.op === '!' ? 'i' : t; }
        case 'tern': {
          this.expr(n.c); const j = this.emit(O.JZ, 0, L); const a = this.expr(n.a); const k = this.emit(O.JMP, 0, L);
          this.cur.code[j].a = this.cur.code.length; const b = this.expr(n.b); this.cur.code[k].a = this.cur.code.length;
          return a === 'f' || b === 'f' ? 'f' : a;
        }
        case 'bin': return this.bin(n);
        case 'assign': return this.assign(n);
        case 'inc': return this.inc(n);
        case 'call': return this.call(n);
        case 'mcall': return this.mcall(n);
        default: throw new CodeError(L, 'I can\'t work this out.');
      }
    }
    bin(n) {
      const L = n.line;
      if (n.op === '&&' || n.op === '||') {
        this.expr(n.l); this.emit(O.UN, '!!', L); this.emit(O.DUP, 0, L);
        const j = this.emit(n.op === '&&' ? O.JZ : O.JNZ, 0, L);
        this.emit(O.POP, 0, L); this.expr(n.r); this.emit(O.UN, '!!', L);
        this.cur.code[j].a = this.cur.code.length; return 'i';
      }
      const a = this.expr(n.l), b = this.expr(n.r);
      const anyF = a === 'f' || b === 'f', anyS = a === 's' || b === 's';
      if (anyS && n.op === '+') { this.emit(O.BIN, a === 'f' || b === 'f' ? 'S+f' : 'S+', L); return 's'; }
      if (n.op === '/' && !anyF) { this.emit(O.DIVI, 0, L); return 'i'; }
      if (n.op === '%') { this.emit(O.MODI, 0, L); return 'i'; }
      this.emit(O.BIN, n.op, L);
      if (['==', '!=', '<', '<=', '>', '>='].includes(n.op)) return 'i';
      return anyF ? 'f' : 'i';
    }
    loadL(lhs) {
      const L = lhs.line;
      if (lhs.k === 'var') { const v = this.find(lhs.name); this.lvalType(lhs); this.emit(v.g ? O.LG : O.LL, v.slot, L); }
      else { this.lvalType(lhs); this.expr(lhs.a); this.expr(lhs.i); this.emit(O.DUP2, 0, L); this.emit(O.LI, 0, L); }
    }
    assign(n) {
      const L = n.line, ty = this.lvalType(n.lhs), lhs = n.lhs, isArr = lhs.k === 'idx';
      if (lhs.k === 'var' && lhs.name in CONSTS && !this.find(lhs.name)) throw new CodeError(L, `"${lhs.name}" is a fixed value and can't be changed.`);
      if (n.op === '=') {
        if (isArr) { this.expr(lhs.a); this.expr(lhs.i); }
        this.expr(n.r);
      } else {
        this.loadL(lhs);
        const rt = this.expr(n.r), op = n.op.slice(0, -1);
        const isF = cls(ty) === 'f' || rt === 'f';
        if (op === '/' && !isF) this.emit(O.DIVI, 0, L);
        else if (op === '%') this.emit(O.MODI, 0, L);
        else this.emit(O.BIN, cls(ty) === 's' && op === '+' ? (rt === 'f' ? 'S+f' : 'S+') : op, L);
      }
      this.emit(O.CONV, ty, L);
      if (isArr) this.emit(O.SI, 0, L);
      else { const v = this.find(lhs.name); this.emit(O.DUP, 0, L); this.emit(v.g ? O.SG : O.SL, v.slot, L); }
      return cls(ty);
    }
    inc(n) {
      const L = n.line, ty = this.lvalType(n.lhs), d = n.op === '++' ? 1 : -1;
      if (n.lhs.k === 'var') {
        const v = this.find(n.lhs.name);
        this.emit(v.g ? O.LG : O.LL, v.slot, L);
        if (!n.pre) this.emit(O.DUP, 0, L);
        this.emit(O.PUSH, d, L); this.emit(O.BIN, '+', L); this.emit(O.CONV, ty, L);
        if (n.pre) this.emit(O.DUP, 0, L);
        this.emit(v.g ? O.SG : O.SL, v.slot, L);
      } else {
        this.loadL(n.lhs); this.emit(O.PUSH, d, L); this.emit(O.BIN, '+', L); this.emit(O.CONV, ty, L); this.emit(O.SI, 0, L);
        if (!n.pre) { this.emit(O.PUSH, -d, L); this.emit(O.BIN, '+', L); }
      }
      return cls(ty);
    }
    call(n) {
      const L = n.line, f = this.fns[n.name];
      if (f) {
        if (n.args.length !== f.params.length) throw new CodeError(L, `"${n.name}" needs ${f.params.length} value(s), but got ${n.args.length}.`);
        n.args.forEach((a, i) => { this.expr(a); if (!f.params[i].arr) this.emit(O.CONV, f.params[i].ty, L); });
        this.emit(O.CALL, f.idx, L);
        return cls(f.ty);
      }
      const b = BUILTINS[n.name];
      if (!b) throw new CodeError(L, `I don't know the function "${n.name}".` + suggest(n.name, Object.keys(BUILTINS).concat(Object.keys(this.fns))));
      if (n.args.length < b[0] || n.args.length > b[1]) throw new CodeError(L, `"${n.name}" needs ${b[0] === b[1] ? b[0] : b[0] + ' to ' + b[1]} value(s), but got ${n.args.length}.`);
      let anyF = false;
      n.args.forEach(a => { if (this.expr(a) === 'f') anyF = true; });
      this.emit(O.BI, [n.name, n.args.length], L);
      return b[2] === '?' ? (anyF ? 'f' : 'i') : b[2] === 'v' ? 'i' : b[2];
    }
    mcall(n) {
      const L = n.line;
      if (n.obj.k === 'var' && n.obj.name === 'Serial') {
        if (['print', 'println'].includes(n.m)) {
          if (n.args.length > 2) throw new CodeError(L, `Serial.${n.m} takes one value at a time.`);
          if (n.args.length) {
            const t = this.expr(n.args[0]);
            if (t === 'f') { if (n.args[1]) this.expr(n.args[1]); else this.emit(O.PUSH, 2, L); this.emit(O.FMT, 'dyn', L); }
            else this.emit(O.FMT, t === 'c' ? 'c' : 's', L);
          } else this.emit(O.PUSH, '', L);
          this.emit(O.BI, ['Serial.' + n.m, 1], L); return 'v';
        }
        if (n.m === 'begin' || n.m === 'flush' || n.m === 'end') { n.args.forEach(a => { this.expr(a); this.emit(O.POP, 0, L); }); this.emit(O.PUSH, 0, L); return 'i'; }
        if (n.m === 'available') { this.emit(O.PUSH, 0, L); return 'i'; }
        throw new CodeError(L, `This simulator doesn't run Serial.${n.m}().` + suggest(n.m, ['print', 'println', 'begin']));
      }
      if (n.obj.k === 'var') {
        const v = this.find(n.obj.name);
        if (!v) throw new CodeError(L, `I don't know "${n.obj.name}".` + (n.obj.name === 'serial' ? ' Did you mean "Serial"? Capital letters matter.' : ''));
        if (v.ty === 'servo') {
          if (!['attach', 'write', 'read', 'detach', 'attached', 'writeMicroseconds'].includes(n.m)) throw new CodeError(L, `A Servo doesn't have "${n.m}".` + suggest(n.m, ['attach', 'write', 'read', 'detach']));
          this.expr(n.obj); n.args.forEach(a => this.expr(a)); this.emit(O.MC, [n.m, n.args.length], L); return 'i';
        }
      }
      throw new CodeError(L, `"${n.m}" can't be used here.`);
    }
  }

  function compileSketch(src) { return new Compiler(new Parser(tokenize(src)).program()).run(); }

  const WRAP = { i8: [8, true], u8: [8, false], chr: [8, true], i16: [16, true], u16: [16, false], i32: [32, true], u32: [32, false] };
  function conv(v, ty) {
    if (typeof v === 'string' || typeof v === 'object') return v;
    if (ty === 'f' || ty === 'str' || ty === 'void' || ty === 'servo') return v;
    if (ty === 'bool') return v ? 1 : 0;
    const w = WRAP[ty]; if (!w) return v;
    v = Math.trunc(v); if (!isFinite(v)) return 0;
    const m = Math.pow(2, w[0]);
    v = ((v % m) + m) % m;
    return w[1] && v >= m / 2 ? v - m : v;
  }

  class VM {
    constructor(prog, host) { this.prog = prog; this.host = host; this.time = 0; this.g = new Array(prog.nglobals).fill(0); this.stack = []; this.frames = []; this.halted = false; this.err = null; this.stage = 0; this.line = 0; this.enter(prog.init, []); }
    enter(idx, args) {
      const f = this.prog.fns[idx], locals = new Array(f.nlocals).fill(0);
      for (let i = 0; i < args.length; i++) locals[i] = args[i];
      this.frames.push({ f, pc: 0, l: locals });
      if (this.frames.length > 60) throw new CodeError(this.line, 'A function keeps calling itself and has run out of memory.');
    }
    fail(line, msg) { this.err = { line, msg }; this.halted = true; }
    run(until) {
      let budget = 400000;
      try {
        while (this.time < until && !this.halted && budget-- > 0) this.stepOp();
      } catch (e) {
        if (e instanceof CodeError) this.fail(e.line || this.line, e.message); else this.fail(this.line, 'Something went wrong while running: ' + e.message);
      }
      return budget > 0;
    }
    stepOp() {
      const fr = this.frames[this.frames.length - 1], s = this.stack, op = fr.f.code[fr.pc++];
      this.time += 1; this.line = op.l;
      let a, b;
      switch (op.o) {
        case O.PUSH: s.push(op.a); break;
        case O.POP: s.pop(); break;
        case O.DUP: s.push(s[s.length - 1]); break;
        case O.DUP2: s.push(s[s.length - 2], s[s.length - 1]); break;
        case O.LG: s.push(this.g[op.a]); break;
        case O.SG: this.g[op.a] = s.pop(); break;
        case O.LL: s.push(fr.l[op.a]); break;
        case O.SL: fr.l[op.a] = s.pop(); break;
        case O.LI: b = s.pop(); a = s.pop();
          if (!Array.isArray(a)) throw new CodeError(op.l, 'This isn\'t an array, so [ ] won\'t work.');
          if (b < 0 || b >= a.length) { s.push(0); this.host.warnOnce('bounds', `Line ${op.l}: reading position ${b} of an array that has ${a.length} items.`); } else s.push(a[b]);
          break;
        case O.SI: { const v = s.pop(); b = s.pop(); a = s.pop();
          if (!Array.isArray(a)) throw new CodeError(op.l, 'This isn\'t an array, so [ ] won\'t work.');
          if (b < 0 || b >= a.length) this.host.warnOnce('bounds', `Line ${op.l}: writing position ${b} of an array that has ${a.length} items.`); else a[b] = v;
          s.push(v); break; }
        case O.BIN: b = s.pop(); a = s.pop(); s.push(binop(op.a, a, b)); break;
        case O.DIVI: b = s.pop(); a = s.pop(); if (b === 0) { this.host.warnOnce('div0', `Line ${op.l}: dividing by zero.`); s.push(0); } else s.push(Math.trunc(a / b)); break;
        case O.MODI: b = s.pop(); a = s.pop(); if (b === 0) { this.host.warnOnce('div0', `Line ${op.l}: dividing by zero.`); s.push(0); } else s.push(Math.trunc(a) % Math.trunc(b)); break;
        case O.UN: a = s.pop(); s.push(op.a === '-' ? -a : op.a === '!' ? (a ? 0 : 1) : op.a === '!!' ? (a ? 1 : 0) : op.a === '~' ? ~a : a); break;
        case O.JMP: fr.pc = op.a; break;
        case O.JZ: if (!s.pop()) fr.pc = op.a; break;
        case O.JNZ: if (s.pop()) fr.pc = op.a; break;
        case O.CALL: { const f = this.prog.fns[op.a], n = f.params.length, args = n ? s.splice(s.length - n, n) : []; this.enter(op.a, args); break; }
        case O.BI: { const n = op.a[1], args = n ? s.splice(s.length - n, n) : []; s.push(this.host.builtin(op.a[0], args, op.l)); break; }
        case O.MC: { const n = op.a[1], args = n ? s.splice(s.length - n, n) : []; const obj = s.pop(); s.push(this.host.servo(obj, op.a[0], args, op.l)); break; }
        case O.RET: {
          const v = s.pop(); this.frames.pop();
          if (this.frames.length) { s.push(v); break; }
          this.time += 5; s.length = 0;
          if (this.stage === 0) { this.stage = 1; this.enter(this.prog.setup, []); }
          else { this.stage = 2; this.enter(this.prog.loop, []); }
          break;
        }
        case O.CONV: s.push(conv(s.pop(), op.a)); break;
        case O.MKARR: { const n = op.a[0], arr = n ? s.splice(s.length - n, n) : []; s.push(arr); break; }
        case O.NEWARR: a = s.pop(); if (a < 0 || a > 2000) throw new CodeError(op.l, 'That array is too big for an Uno.'); s.push(new Array(a).fill(op.a === 'str' ? '' : 0)); break;
        case O.NEWSERVO: s.push({ servo: true, pin: null, angle: 90 }); break;
        case O.FMT:
          if (op.a === 'dyn') { b = s.pop(); a = s.pop(); s.push(Number(a).toFixed(Math.max(0, Math.min(8, b)))); }
          else if (op.a === 'c') { a = s.pop(); s.push(typeof a === 'string' ? a : String.fromCharCode(a)); }
          else if (op.a === 2) { s.push(Number(s.pop()).toFixed(2)); }
          else s.push(String(s.pop()));
          break;
        default: throw new CodeError(op.l, 'Unknown instruction.');
      }
    }
  }
  function binop(op, a, b) {
    switch (op) {
      case '+': return a + b; case '-': return a - b; case '*': return a * b; case '/': return b === 0 ? 0 : a / b;
      case '==': return a === b || a == b ? 1 : 0; case '!=': return a == b ? 0 : 1; // eslint-disable-line eqeqeq
      case '<': return a < b ? 1 : 0; case '<=': return a <= b ? 1 : 0; case '>': return a > b ? 1 : 0; case '>=': return a >= b ? 1 : 0;
      case '&': return a & b; case '|': return a | b; case '^': return a ^ b; case '<<': return a << b; case '>>': return a >> b;
      case 'S+': return String(a) + String(b);
      case 'S+f': return (typeof a === 'number' ? a.toFixed(2) : a) + (typeof b === 'number' ? b.toFixed(2) : b);
      default: throw new CodeError(0, 'Unknown operator ' + op);
    }
  }

  // ---------- circuit: nodes ----------
  const PWM_PINS = [3, 5, 6, 9, 10, 11];
  function netKey(n) {
    let m = /^([a-j])(\d+)$/.exec(n);
    if (m) return ('abcde'.includes(m[1]) ? 'T' : 'B') + m[2];
    m = /^(TP|TN|BP|BN)\d+$/.exec(n);
    if (m) return m[1];
    if (/^GND\d?$/.test(n)) return 'GND';
    return n;
  }
  function pinNode(n) { return n >= 14 ? 'A' + (n - 14) : 'D' + n; }
  function pinNumber(node) { const m = /^D(\d+)$/.exec(node); if (m) return +m[1]; const a = /^A(\d)$/.exec(node); return a ? 14 + +a[1] : null; }

  // Types: leg names, then default values.
  const PART_TYPES = {
    resistor: { legs: ['a', 'b'], names: ['one leg', 'the other leg'], label: 'Resistor', def: { ohm: 220 } },
    led: { legs: ['a', 'k'], names: ['the + leg (long)', 'the &#8722; leg (short)'], label: 'LED', def: { color: 'red' } },
    button: { legs: ['a', 'b'], names: ['one leg', 'the diagonally opposite leg'], label: 'Push button', def: {} },
    pot: { legs: ['a', 'w', 'b'], names: ['the left leg', 'the middle leg', 'the right leg'], label: 'Potentiometer', def: { ohm: 10000 } },
    ldr: { legs: ['a', 'b'], names: ['one leg', 'the other leg'], label: 'Light sensor (LDR)', def: {} },
    cap: { legs: ['p', 'n'], names: ['the + leg (long)', 'the &#8722; leg (stripe)'], label: 'Capacitor', def: { uf: 470, rating: 16 } },
    diode: { legs: ['a', 'k'], names: ['the plain end', 'the striped end'], label: 'Diode (1N4001)', def: {} },
    npn: { legs: ['b', 'c', 'e'], names: ['the base leg', 'the collector leg', 'the emitter leg'], label: 'Transistor', def: { model: 'TIP120' } },
    motor: { legs: ['a', 'b'], names: ['one wire', 'the other wire'], label: 'DC motor', def: {} },
    buzzer: { legs: ['p', 'n'], names: ['the + leg', 'the &#8722; leg'], label: 'Piezo buzzer', def: {} },
    servo: { legs: ['g', 'v', 's'], names: ['the brown wire (ground)', 'the red wire (power)', 'the orange wire (signal)'], label: 'Servo motor', def: {} },
    sonar: { legs: ['vcc', 'trig', 'echo', 'gnd'], names: ['the VCC pin', 'the TRIG pin', 'the ECHO pin', 'the GND pin'], label: 'Ultrasonic sensor', def: {} },
    lm35: { legs: ['v', 'o', 'g'], names: ['the +Vs leg', 'the Vout leg', 'the GND leg'], label: 'Temperature sensor (LM35)', def: { tempC: 25 } },
    soil: { legs: ['v', 'o', 'g'], names: ['the VCC pin', 'the AOUT pin', 'the GND pin'], label: 'Soil moisture sensor', def: { moist: 50 } },
    irmod: { legs: ['v', 'g', 'o'], names: ['the VCC pin', 'the GND pin', 'the OUT pin'], label: 'IR obstacle module', def: { cm: 100 } },
    battery: { legs: ['p', 'n'], names: ['the red wire (+)', 'the black wire (&#8722;)'], label: '4 &#215; AA battery pack', def: { volts: 6 } },
  };
  const NPN = { TIP120: { vbe: 1.4, vsat: 1.0, beta: 1000, imax: 5 }, '2N2222': { vbe: 0.7, vsat: 0.2, beta: 100, imax: 0.6 } };
  const LED_VF = { red: 2.0, yellow: 2.1, green: 2.2, blue: 3.0, white: 3.0 };

  // Output voltage of the powered sensor modules.
  function sensorOut(p) {
    if (p.type === 'lm35') return p.tempC * 0.01;
    if (p.type === 'soil') return 3.0 - 1.8 * p.moist / 100; // drier soil, higher voltage
    return p.cm <= 20 ? 0 : 5; // IR module: LOW when something is close
  }

  // ---------- simulator ----------
  class Sim {
    constructor(circuit, code, opts) {
      this.board = (opts && opts.board) || 'R3';
      this.parts = JSON.parse(JSON.stringify(circuit.parts));
      this.wires = JSON.parse(JSON.stringify(circuit.wires));
      this.code = code; this.err = null; this.vm = null;
      this.serial = ''; this.warns = new Map();
      this.pins = {}; for (let i = 0; i < 20; i++) this.pins[i] = { mode: 0, level: 0, duty: null, tone: null, toneEnd: null };
      this.ct = 0; this.simT = 0; this.dirty = true; this.m = {}; this.V = [];
      this.parts.forEach(p => {
        p.st = { i: 0, peak: 0, v: 0, burned: false, speed: 0, angle: 90, target: 90, sound: 0, freq: 0, vc: 0, on: false, ready: false, press: 0 };
        if (p.type === 'pot' && p.x === undefined) p.x = 0.5;
        if (p.type === 'ldr' && p.light === undefined) p.light = 0.5;
        if (p.type === 'sonar' && p.cm === undefined) p.cm = 100;
        if (p.type === 'lm35' && p.tempC === undefined) p.tempC = 25;
        if (p.type === 'soil' && p.moist === undefined) p.moist = 50;
        if (p.type === 'irmod' && p.cm === undefined) p.cm = 100;
      });
      this.prepare();
      try { this.prog = compileSketch(code); this.vm = new VM(this.prog, this); }
      catch (e) { if (e instanceof CodeError) this.err = { line: e.line, msg: e.message }; else throw e; }
      this.recalc();
    }
    warn(code, sev, msg) { if (!this.warns.has(code)) this.warns.set(code, { sev, msg }); }
    warnOnce(code, msg) { this.warn(code, 'warn', msg); }
    part(id) { return this.parts.find(p => p.id === id); }
    net(node) { return this.netIdx[this.find(netKey(node))]; }

    prepare() {
      const par = {};
      this.find = k => { if (par[k] === undefined) par[k] = k; while (par[k] !== k) { par[k] = par[par[k]]; k = par[k]; } return k; };
      const union = (a, b) => { par[this.find(netKey(a))] = this.find(netKey(b)); };
      this.find('GND');
      ['5V', '3V3', 'VIN'].forEach(k => this.find(k));
      this.wires.forEach(w => union(w[0], w[1]));
      const used = new Set(['GND', '5V', '3V3', 'VIN']);
      this.wires.forEach(w => { used.add(netKey(w[0])); used.add(netKey(w[1])); });
      this.parts.forEach(p => Object.values(p.legs).forEach(n => used.add(netKey(n))));
      for (let i = 0; i < 20; i++) used.add(netKey(pinNode(i)));
      this.netIdx = {}; let N = 1;
      const g = this.find('GND'); this.netIdx[g] = 0;
      used.forEach(k => { const r = this.find(k); if (this.netIdx[r] === undefined) this.netIdx[r] = N++; });
      this.N = N;
      this.pinNet = {}; for (let i = 0; i < 20; i++) this.pinNet[i] = this.net(pinNode(i));
      this.sup5 = this.net('5V'); this.sup3 = this.net('3V3');
      // Only pins with something attached need solving.
      const count = {}; const bump = n => { const r = this.netIdx[this.find(netKey(n))]; count[r] = (count[r] || 0) + 1; };
      this.wires.forEach(w => { bump(w[0]); bump(w[1]); }); this.parts.forEach(p => Object.values(p.legs).forEach(bump));
      this.pinUsed = {}; for (let i = 0; i < 20; i++) this.pinUsed[i] = !!count[this.pinNet[i]];
      this.parts.forEach(p => {
        p.n = {}; Object.keys(p.legs).forEach(k => { p.n[k] = this.net(p.legs[k]); });
        p.s = { d: false, be: false, ce: 0, ib: 0, ic: 0 };
      });
      this.hasCaps = this.parts.some(p => p.type === 'cap');
      this.parts.filter(p => p.type === 'motor').forEach(m => {
        const drv = this.parts.some(t => t.type === 'npn' && (t.n.c === m.n.a || t.n.c === m.n.b));
        if (!drv) return;
        const fly = this.parts.some(d => d.type === 'diode' && ((d.n.a === m.n.a && d.n.k === m.n.b) || (d.n.a === m.n.b && d.n.k === m.n.a)));
        if (!fly) this.warn('flyback', 'warn', 'The motor has no flyback diode. Real motors kick back a voltage spike that can damage the transistor.');
      });
      this.parts.filter(p => p.type === 'servo').forEach(s => { if (s.n.g !== 0) this.warn('sgnd', 'bad', 'The servo\'s ground isn\'t joined to Arduino GND. In real life it would jitter or ignore the signal.'); });
    }

    // One DC solve at one PWM phase. Levels maps pin number to 0 or 1 volts-high.
    solve(levels, dt) {
      const N = this.N, sz = N - 1;
      const G = this._g && this._g.length === sz ? this._g : (this._g = Array.from({ length: sz }, () => new Float64Array(sz + 1)));
      let V = new Float64Array(N);
      const sg = (a, b, g) => {
        if (a) G[a - 1][a - 1] += g;
        if (b) G[b - 1][b - 1] += g;
        if (a && b) { G[a - 1][b - 1] -= g; G[b - 1][a - 1] -= g; }
      };
      const si = (a, b, i) => { if (a) G[a - 1][sz] += i; if (b) G[b - 1][sz] -= i; }; // current i into a, out of b
      const src = (n, v, r) => { const g = 1 / r; sg(n, 0, g); si(n, 0, v * g); };
      const parts = this.parts;
      for (let iter = 0; iter < 40; iter++) {
        for (let r = 0; r < sz; r++) { G[r].fill(0); G[r][r] = 1e-9; }
        src(this.sup5, 5, 0.2); src(this.sup3, 3.3, 1);
        for (let i = 0; i < 20; i++) {
          if (!this.pinUsed[i]) continue;
          const pin = this.pins[i];
          if (pin.mode === 1) src(this.pinNet[i], levels[i] ? 5 : 0, 25);
          else if (pin.mode === 2) src(this.pinNet[i], 5, 35000);
        }
        for (const p of parts) {
          const n = p.n, s = p.s, st = p.st;
          switch (p.type) {
            case 'resistor': sg(n.a, n.b, 1 / p.ohm); break;
            case 'button': sg(n.a, n.b, st.press ? 20 : 1e-9); break;
            case 'pot': sg(n.a, n.w, 1 / (p.ohm * p.x + 1)); sg(n.w, n.b, 1 / (p.ohm * (1 - p.x) + 1)); break;
            case 'ldr': sg(n.a, n.b, 1 / (200 * Math.pow(100, 1 - p.light))); break;
            case 'motor': sg(n.a, n.b, 1 / 20); break;
            case 'buzzer': sg(n.p, n.n, 1 / 2000); break;
            case 'servo': sg(n.v, n.g, st.moving ? 1 / 30 : 1 / 500); break;
            case 'sonar': sg(n.vcc, n.gnd, 1 / 333); break;
            case 'lm35': case 'soil': case 'irmod': {
              sg(n.v, n.g, 1 / 20000);
              if (s.d) { const vo = sensorOut(p); sg(n.o, n.g, 1 / 100); si(n.o, n.g, vo / 100); } else sg(n.o, n.g, 1e-9);
              break;
            }
            case 'battery': { const g = 2; sg(n.p, n.n, g); si(n.p, n.n, p.volts * g); break; }
            case 'cap': { const g = (p.uf * 1e-6) / (dt || 0.002); sg(n.p, n.n, g); si(n.p, n.n, g * st.vc); break; }
            case 'led': case 'diode': {
              const vf = p.type === 'led' ? (LED_VF[p.color] || 2) : 0.7, rs = p.type === 'led' ? 12 : 0.5;
              if (s.d && !st.burned) { sg(n.a, n.k, 1 / rs); si(n.a, n.k, vf / rs); } else sg(n.a, n.k, 1e-9);
              break;
            }
            case 'npn': {
              const m = NPN[p.model] || NPN.TIP120;
              if (s.be) { sg(n.b, n.e, 1 / 5); si(n.b, n.e, m.vbe / 5); } else sg(n.b, n.e, 1e-9);
              if (s.ce === 1) { sg(n.c, n.e, 1 / 0.2); si(n.c, n.e, m.vsat / 0.2); }
              else if (s.ce === 2) { sg(n.c, n.e, 1e-6); si(n.e, n.c, m.beta * s.ib); }
              else sg(n.c, n.e, 1e-9);
              break;
            }
            default:
          }
        }
        const x = gauss(G, sz);
        V = new Float64Array(N); for (let k = 1; k < N; k++) V[k] = x[k - 1];
        let changed = false;
        for (const p of parts) {
          const n = p.n, s = p.s;
          if (p.type === 'lm35' || p.type === 'soil' || p.type === 'irmod') {
            const on = V[n.v] - V[n.g] > 3;
            if (on !== s.d) { s.d = on; changed = true; }
          } else if (p.type === 'led' || p.type === 'diode') {
            const vf = p.type === 'led' ? (LED_VF[p.color] || 2) : 0.7, vd = V[n.a] - V[n.k];
            const on = s.d ? ((vd - vf) > -1e-6) : vd > vf;
            if (on !== s.d) { s.d = on; changed = true; }
          } else if (p.type === 'npn') {
            const m = NPN[p.model] || NPN.TIP120, vbe = V[n.b] - V[n.e], vce = V[n.c] - V[n.e];
            const be = s.be ? (vbe - m.vbe) > -1e-6 : vbe > m.vbe;
            if (be !== s.be) { s.be = be; changed = true; }
            const ib = be ? Math.max(0, (vbe - m.vbe) * 5) : 0;
            let ce = 0;
            if (be && ib > 1e-7) {
              const icSat = s.ce === 1 ? (vce - m.vsat) / 0.2 : Infinity;
              if (s.ce === 1) ce = icSat > m.beta * ib ? 2 : (vce > m.vsat - 1e-6 || icSat > -1e-3 ? 1 : 0);
              else if (s.ce === 2) ce = vce < m.vsat ? 1 : 2;
              else ce = vce > m.vsat ? 1 : 0;
            }
            if (ce !== s.ce) { s.ce = ce; changed = true; }
            if (Math.abs(ib - s.ib) > 1e-6) { if (s.ce === 2) changed = true; s.ib = ib; }
          }
        }
        if (!changed) break;
      }
      return V;
    }

    // Averages over PWM phases, then updates every part's readings and warnings.
    recalc(dt) {
      const P = this.pins, pwm = [];
      for (let i = 0; i < 20; i++) if (P[i].mode === 1 && this.pinUsed[i]) {
        if (P[i].tone) pwm.push([i, 0.5]);
        else if (P[i].duty !== null && P[i].duty > 0 && P[i].duty < 1) pwm.push([i, P[i].duty]);
      }
      const phases = pwm.length ? 16 : 1, levels = {};
      const acc = new Float64Array(this.N);
      const pc = {}; this.parts.forEach(p => { pc[p.id] = { i: 0, peak: 0, v: 0, c: 0, ic: 0 }; });
      const pinI = {}; let i5 = 0, ibat = 0, r = 0;
      for (let k = 0; k < phases; k++) {
        for (let i = 0; i < 20; i++) {
          const q = P[i]; levels[i] = q.duty !== null ? (q.duty >= 1 ? 1 : 0) : q.level;
        }
        pwm.forEach(([i, d]) => { levels[i] = (k + 0.5) / phases < d ? 1 : 0; });
        const V = this.solve(levels, dt);
        let capI = 0, batI = 0;
        for (let n = 0; n < this.N; n++) acc[n] += V[n] / phases;
        for (let i = 0; i < 20; i++) if (P[i].mode === 1 && this.pinUsed[i]) {
          const c = Math.abs((levels[i] ? 5 : 0) - V[this.pinNet[i]]) / 25;
          pinI[i] = Math.max(pinI[i] || 0, c);
        }
        for (const p of this.parts) {
          const n = p.n, c = pc[p.id];
          let cur = 0, vp = 0;
          switch (p.type) {
            case 'resistor': vp = V[n.a] - V[n.b]; cur = vp / p.ohm; break;
            case 'led': case 'diode': {
              const vf = p.type === 'led' ? (LED_VF[p.color] || 2) : 0.7, rs = p.type === 'led' ? 12 : 0.5;
              vp = V[n.a] - V[n.k]; cur = p.s.d && !p.st.burned ? (vp - vf) / rs : 0; break;
            }
            case 'motor': vp = V[n.a] - V[n.b]; cur = vp / 20; break;
            case 'buzzer': vp = V[n.p] - V[n.n]; cur = vp / 2000; break;
            case 'button': vp = V[n.a] - V[n.b]; cur = p.st.press ? vp * 20 : 0; break;
            case 'npn': vp = V[n.c] - V[n.e]; cur = p.s.ce === 1 ? (vp - (NPN[p.model] || NPN.TIP120).vsat) / 0.2 : p.s.ce === 2 ? (NPN[p.model] || NPN.TIP120).beta * p.s.ib : 0; break;
            case 'battery': vp = V[n.p] - V[n.n]; cur = Math.max(0, (p.volts - vp) * 2); break;
            case 'cap': vp = V[n.p] - V[n.n]; cur = (vp - p.st.vc) * (p.uf * 1e-6) / (dt || 0.002); break;
            case 'servo': vp = V[n.v] - V[n.g]; cur = vp * (p.st.moving ? 1 / 30 : 1 / 500); break;
            case 'sonar': vp = V[n.vcc] - V[n.gnd]; cur = vp / 333; break;
            case 'lm35': case 'soil': case 'irmod': vp = V[n.o] - V[n.g]; cur = (V[n.v] - V[n.g]) / 20000; if (V[n.v] - V[n.g] < -1) this.warn('prev-' + p.id, 'bad', `${p.id} has its power connected backwards. That can destroy a real sensor. Check VCC and GND.`); break;
            case 'pot': vp = V[n.w] - V[n.a]; break;
            case 'ldr': vp = V[n.a] - V[n.b]; cur = vp / (200 * Math.pow(100, 1 - p.light)); break;
            default:
          }
          c.i += cur / phases; c.v += vp / phases; c.peak = Math.max(c.peak, Math.abs(cur));
          if (p.type === 'npn') c.ic = Math.max(c.ic, Math.abs(cur));
          if (p.type === 'cap') capI += Math.abs(cur);
          if (p.type === 'battery') batI = Math.max(batI, cur);
        }
        i5 = Math.max(i5, Math.abs(5 - V[this.sup5]) / 0.2 - capI);
        ibat = Math.max(ibat, batI - capI);
      }
      this.V = acc;
      let reburn = false;
      for (const p of this.parts) {
        const c = pc[p.id], st = p.st;
        st.i = c.i; st.v = c.v; st.peak = c.peak;
        if (p.type === 'led') {
          if (c.peak > 0.05 && !st.burned) { st.burned = true; reburn = true; this.warn('burn-' + p.id, 'bad', `${p.id}: too much current burned out this LED. Add a resistor in series, then select Stop and Start to try again.`); }
          else if (c.peak > 0.025) this.warn('hot-' + p.id, 'warn', `${p.id}: ${(c.peak * 1000).toFixed(0)} mA is more than an LED should take. Use a bigger resistor.`);
          if (c.v < -1) this.warn('rev-' + p.id, 'warn', `${p.id} has voltage across it the wrong way. It looks backwards: swap its legs.`);
        } else if (p.type === 'resistor') {
          if (Math.abs(c.i * c.v) > 0.25) this.warn('rp-' + p.id, 'warn', `${p.id} is getting hot: it's over its ¼ watt limit.`);
        } else if (p.type === 'cap') {
          if (c.v < -0.5) this.warn('crev-' + p.id, 'bad', `${p.id} is connected backwards. A real electrolytic capacitor can overheat or burst. Put its stripe on the negative side.`);
          if (Math.abs(c.v) > p.rating) this.warn('cov-' + p.id, 'bad', `${p.id} is above its ${p.rating} V rating.`);
        } else if (p.type === 'npn') {
          const m = NPN[p.model] || NPN.TIP120;
          if (c.ic > m.imax) this.warn('ic-' + p.id, 'bad', `${p.id} is carrying more current than a ${p.model} is rated for.`);
        } else if (p.type === 'motor') {
          st.speed = Math.max(-1.2, Math.min(1.2, c.v / 6));
        } else if (p.type === 'sonar') {
          if (c.v < -1) this.warn('srev-' + p.id, 'bad', 'VCC and GND on the distance sensor are swapped. That can destroy a real sensor.');
        }
      }
      const limit = this.board === 'R4' ? 0.008 : 0.02, hard = this.board === 'R4' ? 0.008 : 0.04;
      for (const i in pinI) {
        if (pinI[i] > hard) this.warn('pin' + i, 'bad', `Pin ${i < 14 ? i : 'A' + (i - 14)} is carrying ${(pinI[i] * 1000).toFixed(0)} mA, over the Uno ${this.board} limit of ${(hard * 1000).toFixed(0)} mA. This can damage a real board. Add a resistor, or use a transistor for motors.`);
        else if (pinI[i] > limit) this.warn('pin' + i, 'warn', `Pin ${i < 14 ? i : 'A' + (i - 14)} is carrying ${(pinI[i] * 1000).toFixed(0)} mA, above the ${(limit * 1000).toFixed(0)} mA guideline.`);
      }
      if (i5 > 1.5) this.warn('short5', 'bad', 'Short circuit on the 5V pin: it has an almost direct path to GND. Check your wires.');
      else if (i5 > 0.5) this.warn('usb', 'bad', `The 5V pin is supplying ${(i5 * 1000).toFixed(0)} mA, more than USB can give. Motors need their own battery.`);
      if (ibat > 2.5) this.warn('shortb', 'bad', 'Short circuit on the battery. Check the diode\'s direction and the wiring around it.');
      this.parts.forEach(p => {
        if (p.type !== 'servo') return;
        if (p.n.v === this.sup5 && !this.warns.has('sfive')) this.warn('sfive', 'warn', 'The servo is powered from the Arduino. A battery pack is safer, because servos draw sudden gulps of current.');
      });
      // Buzzer sound comes from a tone on any pin wired to it.
      for (const p of this.parts) if (p.type === 'buzzer') {
        let f = 0;
        for (let i = 0; i < 20; i++) if (P[i].tone && P[i].mode === 1 && (this.pinNet[i] === p.n.p || this.pinNet[i] === p.n.n)) f = P[i].tone;
        const dv = Math.abs(p.st.v);
        p.st.freq = f; p.st.sound = f && dv > 0.5 ? 1 : 0;
      }
      this.dirty = false;
      if (reburn) { r = 1; this.recalc(dt); }
      return r;
    }

    // Moves circuit time forward to t (microseconds).
    advance(t) {
      const dt = t - this.ct;
      if (dt <= 0) { if (this.dirty) this.recalc(); return; }
      for (let i = 0; i < 20; i++) { const q = this.pins[i]; if (q.tone && q.toneEnd !== null && t >= q.toneEnd) { q.tone = null; q.toneEnd = null; this.dirty = true; } }
      for (const p of this.parts) if (p.type === 'servo') {
        const st = p.st, pw = this.V[p.n.v] - this.V[p.n.g];
        const powered = pw > 3.5 && pw < 7.5, moving = powered && Math.abs(st.angle - st.target) > 0.5;
        if (moving) {
          const d = 0.0006 * dt; // about 60 degrees per 0.1 s
          st.angle += Math.max(-d, Math.min(d, st.target - st.angle));
        }
        if (moving !== !!st.moving) { st.moving = moving; this.dirty = true; }
        if (p.n.g !== 0 && powered) st.jitter = Math.sin(t / 30000) * 4; else st.jitter = 0;
      }
      if (this.hasCaps) {
        const n = Math.max(1, Math.min(250, Math.ceil(dt / 2000))), h = dt / n / 1e6;
        for (let k = 0; k < n; k++) {
          this.recalc(h);
          for (const p of this.parts) if (p.type === 'cap') p.st.vc = this.V[p.n.p] - this.V[p.n.n];
        }
      } else if (this.dirty) this.recalc();
      this.ct = t;
    }

    step(ms) {
      const target = this.simT + ms * 1000;
      if (this.vm && !this.vm.halted) {
        while (this.vm.time < target && !this.vm.halted) {
          if (!this.vm.run(target)) break;
        }
        if (this.vm.err) this.err = this.vm.err;
      }
      this.advance(target);
      this.simT = target;
    }

    setInput(id, v) {
      const p = this.part(id); if (!p) return;
      if (p.type === 'button') p.st.press = v ? 1 : 0;
      else if (p.type === 'lm35') p.tempC = v;
      else if (p.type === 'soil') p.moist = v;
      else if (p.type === 'irmod') p.cm = v;
      else if (p.type === 'pot') p.x = v;
      else if (p.type === 'ldr') p.light = v;
      else if (p.type === 'sonar') p.cm = v;
      this.dirty = true;
    }

    isFloating(net) {
      if (net === 0) return false;
      const seen = new Set([net]), todo = [net];
      const anchored = new Set([0, this.sup5, this.sup3]);
      for (let i = 0; i < 20; i++) if (this.pinUsed[i] && this.pins[i].mode) anchored.add(this.pinNet[i]);
      for (const p of this.parts) if ((p.type === 'lm35' || p.type === 'soil' || p.type === 'irmod') && p.s.d) anchored.add(p.n.o);
      const links = [];
      for (const p of this.parts) {
        const n = p.n;
        if (p.type === 'resistor' || p.type === 'ldr' || p.type === 'motor' || p.type === 'buzzer') links.push(Object.values(n));
        else if (p.type === 'button' && p.st.press) links.push([n.a, n.b]);
        else if (p.type === 'pot') { links.push([n.a, n.w]); links.push([n.w, n.b]); }
        else if (p.type === 'battery') links.push([n.p, n.n]);
        else if ((p.type === 'led' || p.type === 'diode') && p.s.d) links.push([n.a, n.k]);
      }
      while (todo.length) {
        const c = todo.pop();
        if (anchored.has(c)) return false;
        for (const l of links) if (l.includes(c)) for (const o of l) if (!seen.has(o)) { seen.add(o); todo.push(o); }
      }
      return true;
    }

    // ---------- Arduino functions ----------
    checkPin(pin, line) {
      if (!Number.isInteger(pin) || pin < 0 || pin > 19) throw new CodeError(line, `Pin ${pin} doesn't exist on an Uno. Use 0 to 13, or A0 to A5.`);
      return this.pins[pin];
    }
    readV(pin) {
      this.advance(this.vm.time);
      if (this.dirty) this.recalc();
      return this.V[this.pinNet[pin]] || 0;
    }
    builtin(name, a, line) {
      const vm = this.vm;
      switch (name) {
        case 'pinMode': { const q = this.checkPin(a[0], line); this.advance(vm.time); q.mode = a[1] === 1 ? 1 : a[1] === 2 ? 2 : 0; this.dirty = true; vm.time += 5; return 0; }
        case 'digitalWrite': {
          const q = this.checkPin(a[0], line); this.advance(vm.time);
          const high = a[1] ? 1 : 0;
          if (q.mode === 0) { this.warnOnce('nomode' + a[0], `Line ${line}: pin ${a[0]} is written to but was never set as an OUTPUT. Add pinMode(${a[0]}, OUTPUT); in setup().`); }
          if (q.level === 1 && !high) this.parts.forEach(p => { if (p.type === 'sonar' && p.n.trig === this.pinNet[a[0]]) p.st.ready = true; });
          q.level = high; q.duty = null; this.dirty = true; vm.time += 5; return 0;
        }
        case 'digitalRead': {
          const q = this.checkPin(a[0], line); vm.time += 5;
          if (q.mode === 1) return q.level;
          const v = this.readV(a[0]);
          if (q.mode === 0 && this.isFloating(this.pinNet[a[0]])) {
            this.warnOnce('float' + a[0], `Pin ${a[0]} is floating, so it reads random values. Use INPUT_PULLUP, or a resistor to GND or 5V.`);
            return Math.random() < 0.5 ? 0 : 1;
          }
          return v > 2.5 ? 1 : 0;
        }
        case 'analogWrite': {
          const q = this.checkPin(a[0], line); this.advance(vm.time);
          const val = Math.max(0, Math.min(255, Math.round(a[1])));
          if (q.mode !== 1) q.mode = 1;
          const canPwm = PWM_PINS.includes(a[0]) && !(this.servoLib && (a[0] === 9 || a[0] === 10));
          if (!canPwm) {
            if (this.servoLib && (a[0] === 9 || a[0] === 10)) this.warnOnce('sv910', `Line ${line}: the Servo library turns off analogWrite on pins 9 and 10.`);
            else this.warnOnce('nopwm' + a[0], `Line ${line}: pin ${a[0]} can't do analogWrite. Use pin 3, 5, 6, 9, 10 or 11.`);
            q.duty = null; q.level = val >= 128 ? 1 : 0;
          } else { q.duty = val / 255; q.level = val > 0 ? 1 : 0; }
          this.dirty = true; vm.time += 5; return 0;
        }
        case 'analogRead': {
          let pin = a[0]; if (pin < 6) pin += 14;
          if (pin < 14 || pin > 19) throw new CodeError(line, 'analogRead only works on pins A0 to A5.');
          vm.time += 100;
          const v = this.readV(pin);
          if (this.isFloating(this.pinNet[pin])) { this.warnOnce('afloat' + pin, `A${pin - 14} isn't connected to anything, so its reading wanders.`); return Math.floor(Math.random() * 1024); }
          return Math.max(0, Math.min(1023, Math.round(v / 5 * 1023)));
        }
        case 'delay': vm.time += Math.max(0, a[0]) * 1000; return 0;
        case 'delayMicroseconds': vm.time += Math.max(0, a[0]); return 0;
        case 'millis': return Math.floor(vm.time / 1000);
        case 'micros': return Math.floor(vm.time);
        case 'pulseIn': {
          this.checkPin(a[0], line); this.advance(vm.time); if (this.dirty) this.recalc();
          const timeout = a[2] === undefined ? 1000000 : a[2], net = this.pinNet[a[0]];
          const s = this.parts.find(p => p.type === 'sonar' && p.n.echo === net);
          if (s) {
            const pw = this.V[s.n.vcc] - this.V[s.n.gnd];
            if (pw < 4) this.warn('snop', 'warn', 'The distance sensor has no power. Check VCC and GND.');
            else if (s.st.ready && !s.soft && s.cm >= 2 && s.cm <= 400) {
              const dur = Math.round(s.cm * 2 / 0.0343);
              s.st.ready = false; s.st.ping = this.simT;
              if (dur <= timeout) { vm.time += dur + 400; return dur; }
            } else if (!s.st.ready) this.warn('notrig', 'warn', 'The sensor was never triggered. Set TRIG HIGH for 10 microseconds before pulseIn.');
          }
          vm.time += Math.min(timeout, 1000000); return 0;
        }
        case 'tone': { const q = this.checkPin(a[0], line); this.advance(vm.time); q.mode = 1; q.tone = a[1]; q.duty = null; q.toneEnd = a[2] !== undefined ? vm.time + a[2] * 1000 : null; this.dirty = true; vm.time += 10; return 0; }
        case 'noTone': { const q = this.checkPin(a[0], line); this.advance(vm.time); q.tone = null; q.toneEnd = null; q.level = 0; this.dirty = true; vm.time += 5; return 0; }
        case 'map': { const [x, b, c, d, e] = a; if (c === b) return d; return Math.trunc((x - b) * (e - d) / (c - b)) + d; }
        case 'constrain': return Math.min(a[2], Math.max(a[1], a[0]));
        case 'min': return Math.min(a[0], a[1]);
        case 'max': return Math.max(a[0], a[1]);
        case 'abs': return Math.abs(a[0]);
        case 'random': return a.length === 1 ? Math.floor(Math.random() * a[0]) : a[0] + Math.floor(Math.random() * (a[1] - a[0]));
        case 'randomSeed': return 0;
        case 'sqrt': return Math.sqrt(a[0]); case 'pow': return Math.pow(a[0], a[1]); case 'sin': return Math.sin(a[0]); case 'cos': return Math.cos(a[0]);
        case 'floor': return Math.floor(a[0]); case 'ceil': return Math.ceil(a[0]); case 'round': return Math.round(a[0]);
        case 'Serial.print': this.serial += a[0]; this.trimSerial(); vm.time += 50; return 0;
        case 'Serial.println': this.serial += a[0] + '\n'; this.trimSerial(); vm.time += 50; return 0;
        default: throw new CodeError(line, `I can't run "${name}".`);
      }
    }
    trimSerial() { if (this.serial.length > 12000) this.serial = this.serial.slice(-9000); }
    servo(obj, m, a, line) {
      const vm = this.vm;
      if (!obj || !obj.servo) throw new CodeError(line, 'This isn\'t a Servo.');
      if (m === 'attach') {
        this.checkPin(a[0], line); obj.pin = a[0]; this.servoLib = true; this.advance(vm.time);
        this.pins[a[0]].mode = 1; this.dirty = true; return 1;
      }
      if (m === 'detach') { obj.pin = null; return 0; }
      if (m === 'attached') return obj.pin !== null ? 1 : 0;
      if (m === 'read') return Math.round(obj.angle);
      if (m === 'write' || m === 'writeMicroseconds') {
        let ang = a[0];
        if (m === 'writeMicroseconds') ang = (a[0] - 544) * 180 / (2400 - 544);
        ang = Math.max(0, Math.min(180, ang));
        if (obj.pin === null) { this.warnOnce('noattach', `Line ${line}: call attach() before write().`); return 0; }
        this.advance(vm.time); obj.angle = ang;
        const net = this.pinNet[obj.pin];
        this.parts.forEach(p => { if (p.type === 'servo' && p.n.s === net) p.st.target = ang; });
        vm.time += 20; return 0;
      }
      return 0;
    }

    measure(p) {
      switch (p.type) {
        case 'led': return p.st.burned ? 0 : Math.max(0, p.st.i) * 1000;
        case 'motor': return Math.abs(p.st.speed);
        case 'buzzer': return p.st.sound;
        case 'servo': return p.st.angle;
        default: return p.st.i * 1000;
      }
    }
  }

  function gauss(A, n) {
    for (let c = 0; c < n; c++) {
      let piv = c, best = Math.abs(A[c][c]);
      for (let r = c + 1; r < n; r++) { const v = Math.abs(A[r][c]); if (v > best) { best = v; piv = r; } }
      if (piv !== c) { const t = A[c]; A[c] = A[piv]; A[piv] = t; }
      const d = A[c][c] || 1e-12;
      for (let r = c + 1; r < n; r++) {
        const f = A[r][c] / d;
        if (f === 0) continue;
        const Ar = A[r], Ac = A[c];
        for (let k = c; k <= n; k++) Ar[k] -= f * Ac[k];
      }
    }
    const x = new Float64Array(n);
    for (let r = n - 1; r >= 0; r--) {
      let s = A[r][n];
      for (let k = r + 1; k < n; k++) s -= A[r][k] * x[k];
      x[r] = s / (A[r][r] || 1e-12);
    }
    return x;
  }

  // ---------- automatic checking ----------
  function runCheck(ex, circuit, code, board) {
    const sim = new Sim(circuit, code, { board }), res = [];
    if (sim.err) return { compileError: sim.err, results: [{ ok: false, say: `Line ${sim.err.line}: ${sim.err.msg}` }], warns: [] };
    const thr = { led: 0.4, motor: 0.05, buzzer: 0.5 };
    for (const st of ex.test) {
      if (st.set) Object.keys(st.set).forEach(k => sim.setInput(k, st.set[k]));
      const startSerial = sim.serial.length, run = st.run || 500, settle = st.settle === undefined ? Math.min(150, run / 3) : st.settle;
      const data = {}; sim.parts.forEach(p => { data[p.id] = { min: Infinity, max: -Infinity, last: 0, sum: 0, c: 0, seen: [] }; });
      for (let t = 0; t < run; t += 5) {
        sim.step(5);
        if (t < settle) continue;
        sim.parts.forEach(p => {
          const d = data[p.id], v = sim.measure(p);
          if (v < d.min) d.min = v; if (v > d.max) d.max = v; d.last = v; d.sum += v; d.c++;
          if (p.type === 'servo') d.seen.push(v);
        });
      }
      if (sim.err) { res.push({ ok: false, say: `Line ${sim.err.line}: ${sim.err.msg}` }); break; }
      const text = sim.serial.slice(startSerial);
      let ok = true;
      for (const c of st.see || []) {
        if (c.serial !== undefined) { if (!(new RegExp(c.serial)).test(text)) ok = false; continue; }
        const p = sim.part(c.p), d = data[c.p];
        if (!p) { ok = false; continue; }
        const th = thr[p.type] === undefined ? 0.5 : thr[p.type];
        if (c.is === 'on' && !(d.min > th)) ok = false;
        if (c.is === 'off' && !(d.max <= th)) ok = false;
        if (c.is === 'blink' && !(d.max > th && d.min <= th)) ok = false;
        if (c.is === 'changes' && !(d.max - d.min > (c.by || 0.2))) ok = false;
        if (c.angle !== undefined && Math.abs(d.last - c.angle) > 6) ok = false;
        if (c.visits && !c.visits.every(a => d.seen.some(v => Math.abs(v - a) < 6))) ok = false;
        if (c.brighter && !(d.sum / d.c > (data[c.brighter].sum / data[c.brighter].c) * 1.3)) ok = false;
        if (c.above !== undefined && !(d.sum / d.c > c.above)) ok = false;
        if (c.below !== undefined && !(d.sum / d.c < c.below)) ok = false;
      }
      res.push({ ok, say: st.say });
    }
    const warns = Array.from(sim.warns.values());
    return { results: res, warns };
  }

  root.ELab = { Sim, runCheck, compileSketch, PART_TYPES, CodeError, netKey, pinNumber };
})(typeof window !== 'undefined' ? window : globalThis);
