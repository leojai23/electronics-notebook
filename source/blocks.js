/* Block coding for both simulators. Blocks generate plain Arduino code, which the student can read and edit. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const SRC = () => window.BLOCKLY_SRC || 'https://unpkg.com/blockly@10.4.3/blockly.min.js';
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* the page still works */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* the page still works */ } },
  };
  const pinOpts = list => list.map(p => [String(p), String(p)]);
  const DIG = pinOpts([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]), PWM = pinOpts([3, 5, 6, 9, 10, 11]), ANA = [['A0', 'A0'], ['A1', 'A1'], ['A2', 'A2'], ['A3', 'A3'], ['A4', 'A4'], ['A5', 'A5']];
  const stmt = (type, msg, args, colour, extra) => Object.assign({ type, message0: msg, args0: args, previousStatement: null, nextStatement: null, colour }, extra || {});
  const val = (type, msg, args, colour, out, extra) => Object.assign({ type, message0: msg, args0: args, output: out || null, colour }, extra || {});
  const num = n => ({ type: 'input_value', name: n, check: 'Number' });
  const any = n => ({ type: 'input_value', name: n });
  const bool = n => ({ type: 'input_value', name: n, check: 'Boolean' });
  const dd = (n, o) => ({ type: 'field_dropdown', name: n, options: o });
  const C = { pin: 200, time: 40, logic: 210, loop: 120, math: 230, vars: 330, text: 160, part: 20, move: 290, sense: 60 };

  const DEFS = [
    { type: 'ar_setup', message0: 'when the Arduino starts %1 %2', args0: [{ type: 'input_dummy' }, { type: 'input_statement', name: 'DO' }], colour: 65, deletable: false },
    { type: 'ar_loop', message0: 'repeat forever %1 %2', args0: [{ type: 'input_dummy' }, { type: 'input_statement', name: 'DO' }], colour: 65, deletable: false },
    stmt('ar_pin', 'set pin %1 to %2', [dd('P', DIG), dd('V', [['HIGH (on)', 'HIGH'], ['LOW (off)', 'LOW']])], C.pin),
    stmt('ar_pwm', 'set pin %1 level to %2', [dd('P', PWM), num('V')], C.pin, { tooltip: 'Fast pulsing (PWM). The level runs from 0 to 255.' }),
    val('ar_btn', 'button on pin %1 is pressed', [dd('P', DIG)], C.pin, 'Boolean'),
    val('ar_dread', 'pin %1 reading (0 or 1)', [dd('P', DIG)], C.pin, 'Number'),
    val('ar_an', 'analog reading of %1', [dd('P', ANA)], C.pin, 'Number', { tooltip: 'A number from 0 to 1023.' }),
    stmt('ar_wait', 'wait %1 milliseconds', [num('V')], C.time),
    stmt('ar_if', 'if %1 then %2 %3', [bool('C'), { type: 'input_dummy' }, { type: 'input_statement', name: 'T' }], C.logic),
    stmt('ar_ifelse', 'if %1 then %2 %3 otherwise %4 %5', [bool('C'), { type: 'input_dummy' }, { type: 'input_statement', name: 'T' }, { type: 'input_dummy' }, { type: 'input_statement', name: 'E' }], C.logic),
    val('ar_cmp', '%1 %2 %3', [num('A'), dd('O', [['<', '<'], ['>', '>'], ['=', '=='], ['≠', '!='], ['≤', '<='], ['≥', '>=']]), num('B')], C.logic, 'Boolean', { inputsInline: true }),
    val('ar_both', '%1 %2 %3', [bool('A'), dd('O', [['and', '&&'], ['or', '||']]), bool('B')], C.logic, 'Boolean', { inputsInline: true }),
    val('ar_not', 'not %1', [bool('A')], C.logic, 'Boolean'),
    stmt('ar_repeat', 'repeat %1 times %2 %3', [num('N'), { type: 'input_dummy' }, { type: 'input_statement', name: 'DO' }], C.loop),
    stmt('ar_while', 'while %1 do %2 %3', [bool('C'), { type: 'input_dummy' }, { type: 'input_statement', name: 'DO' }], C.loop),
    val('ar_num', '%1', [{ type: 'field_number', name: 'N', value: 0 }], C.math, 'Number'),
    val('ar_arith', '%1 %2 %3', [num('A'), dd('O', [['+', '+'], ['−', '-'], ['×', '*'], ['÷', '/']]), num('B')], C.math, 'Number', { inputsInline: true }),
    val('ar_map', 'scale %1 from 0–1023 to 0–%2', [num('A'), num('B')], C.math, 'Number', { inputsInline: true }),
    stmt('ar_set', 'set %1 to %2', [{ type: 'field_input', name: 'N', text: 'count' }, num('V')], C.vars),
    stmt('ar_chg', 'change %1 by %2', [{ type: 'field_input', name: 'N', text: 'count' }, num('V')], C.vars),
    val('ar_get', '%1', [{ type: 'field_input', name: 'N', text: 'count' }], C.vars, 'Number'),
    stmt('ar_print', 'print %1 %2', [any('V'), dd('L', [['then new line', 'NL'], ['stay on this line', 'SAME']])], C.text),
    val('ar_txt', '" %1 "', [{ type: 'field_input', name: 'T', text: 'hello' }], C.text, 'String'),
    val('ar_dist', 'distance in cm', [], C.sense, 'Number'),
    stmt('ar_servo', 'turn servo to %1 degrees', [num('V')], C.part),
    stmt('ar_tone', 'play note %1 Hz on pin %2', [num('F'), dd('P', DIG)], C.part),
    stmt('ar_notone', 'stop the note on pin %1', [dd('P', DIG)], C.part),
    stmt('rb_move', '%1 at speed %2', [dd('K', [['drive forward', 'F'], ['drive backward', 'B'], ['spin left', 'L'], ['spin right', 'R']]), num('V')], C.move),
    stmt('rb_stop', 'stop the wheels', [], C.move),
    stmt('rb_wheels', 'left wheel %1 right wheel %2', [num('L'), num('R')], C.move, { inputsInline: true, tooltip: 'Each wheel speed runs from -255 to 255.' }),
    val('rb_line', '%1 line sensor sees black', [dd('S', [['left', 'A0'], ['right', 'A1']])], C.sense, 'Boolean'),
    val('rb_eye', '%1 line sensor reading', [dd('S', [['left', 'A0'], ['right', 'A1']])], C.sense, 'Number'),
    val('rb_btn', 'start button is pressed', [], C.sense, 'Boolean'),
    stmt('rb_light', 'turn %1 light %2', [dd('C', [['red', '12'], ['green', '13']]), dd('V', [['on', 'HIGH'], ['off', 'LOW']])], C.part),
    stmt('rb_beep', 'turn buzzer %1', [dd('V', [['on', 'HIGH'], ['off', 'LOW']])], C.part),
  ];

  // ---------- turning blocks into Arduino code ----------
  const safeName = s => { const n = String(s || 'x').replace(/[^A-Za-z0-9_]/g, '_'); return /^[A-Za-z_]/.test(n) ? n : 'v_' + n; };
  const DRIVE = `const int L1 = 5, L2 = 6;   // left motor
const int R1 = 3, R2 = 11;  // right motor

void setMotor(int a, int b, int speed) {
  if (speed >= 0) {
    analogWrite(a, speed);
    analogWrite(b, 0);
  } else {
    analogWrite(a, 0);
    analogWrite(b, -speed);
  }
}

void drive(int left, int right) {
  setMotor(L1, L2, left);
  setMotor(R1, R2, right);
}
`;
  function generate(ws, kind) {
    const c = { out: new Set(), input: new Set(), pull: new Set(), serial: false, servo: false, dist: false, vars: new Set(), drive: false };
    const inp = (b, n) => { const k = b.getInputTargetBlock(n); return k ? ex(k) : '0'; };
    const cond = (b, n) => { const k = b.getInputTargetBlock(n); return k ? ex(k) : 'false'; };
    function ex(b) {
      const f = n => b.getFieldValue(n);
      switch (b.type) {
        case 'ar_num': return String(f('N'));
        case 'ar_arith': return `(${inp(b, 'A')} ${f('O')} ${inp(b, 'B')})`;
        case 'ar_map': return `map(${inp(b, 'A')}, 0, 1023, 0, ${inp(b, 'B')})`;
        case 'ar_cmp': return `${inp(b, 'A')} ${f('O')} ${inp(b, 'B')}`;
        case 'ar_both': return `(${cond(b, 'A')}) ${f('O')} (${cond(b, 'B')})`;
        case 'ar_not': return `!(${cond(b, 'A')})`;
        case 'ar_btn': c.pull.add(f('P')); return `digitalRead(${f('P')}) == LOW`;
        case 'ar_dread': c.input.add(f('P')); return `digitalRead(${f('P')})`;
        case 'ar_an': return `analogRead(${f('P')})`;
        case 'ar_get': { const n = safeName(f('N')); c.vars.add(n); return n; }
        case 'ar_txt': return JSON.stringify(String(f('T')));
        case 'ar_dist': c.dist = true; return 'readDistanceCm()';
        case 'rb_line': c.input.add(f('S')); return `digitalRead(${f('S')}) == 1`;
        case 'rb_eye': c.input.add(f('S')); return `digitalRead(${f('S')})`;
        case 'rb_btn': c.pull.add('2'); return 'digitalRead(2) == LOW';
        default: return '0';
      }
    }
    const body = (b, n, pad) => { const k = b.getInputTargetBlock(n); return k ? seq(k, pad) : ''; };
    function seq(b, pad) {
      let out = '';
      for (let k = b; k; k = k.getNextBlock()) out += one(k, pad);
      return out;
    }
    function one(b, p) {
      const f = n => b.getFieldValue(n), q = p + '  ';
      switch (b.type) {
        case 'ar_pin': c.out.add(f('P')); return `${p}digitalWrite(${f('P')}, ${f('V')});\n`;
        case 'ar_pwm': c.out.add(f('P')); return `${p}analogWrite(${f('P')}, ${inp(b, 'V')});\n`;
        case 'ar_wait': return `${p}delay(${inp(b, 'V')});\n`;
        case 'ar_if': return `${p}if (${cond(b, 'C')}) {\n${body(b, 'T', q)}${p}}\n`;
        case 'ar_ifelse': return `${p}if (${cond(b, 'C')}) {\n${body(b, 'T', q)}${p}} else {\n${body(b, 'E', q)}${p}}\n`;
        case 'ar_repeat': return `${p}for (int i${p.length} = 0; i${p.length} < ${inp(b, 'N')}; i${p.length}++) {\n${body(b, 'DO', q)}${p}}\n`;
        case 'ar_while': return `${p}while (${cond(b, 'C')}) {\n${body(b, 'DO', q)}${p}}\n`;
        case 'ar_set': { const n = safeName(f('N')); c.vars.add(n); return `${p}${n} = ${inp(b, 'V')};\n`; }
        case 'ar_chg': { const n = safeName(f('N')); c.vars.add(n); return `${p}${n} = ${n} + ${inp(b, 'V')};\n`; }
        case 'ar_print': c.serial = true; return `${p}Serial.${f('L') === 'NL' ? 'println' : 'print'}(${inp(b, 'V')});\n`;
        case 'ar_servo': c.servo = true; return `${p}myServo.write(${inp(b, 'V')});\n`;
        case 'ar_tone': return `${p}tone(${f('P')}, ${inp(b, 'F')});\n`;
        case 'ar_notone': return `${p}noTone(${f('P')});\n`;
        case 'rb_move': {
          c.drive = true; const s = inp(b, 'V'), k = f('K');
          const a = { F: [s, s], B: ['-' + s, '-' + s], L: ['-' + s, s], R: [s, '-' + s] }[k];
          return `${p}drive(${a[0]}, ${a[1]});\n`;
        }
        case 'rb_stop': c.drive = true; return `${p}drive(0, 0);\n`;
        case 'rb_wheels': c.drive = true; return `${p}drive(${inp(b, 'L')}, ${inp(b, 'R')});\n`;
        case 'rb_light': c.out.add(f('C')); return `${p}digitalWrite(${f('C')}, ${f('V')});\n`;
        case 'rb_beep': c.out.add('4'); return `${p}digitalWrite(4, ${f('V')});\n`;
        default: return '';
      }
    }
    const tops = ws.getTopBlocks(false), setupB = tops.find(b => b.type === 'ar_setup'), loopB = tops.find(b => b.type === 'ar_loop');
    const setupBody = setupB ? body(setupB, 'DO', '  ') : '', loopBody = loopB ? body(loopB, 'DO', '  ') : '';
    const robot = kind === 'robot', TRIG = 7, ECHO = robot ? 8 : 6;
    let head = '// Written by your blocks. Open the Code tab to edit it by hand.\n';
    if (c.servo) head += '#include <Servo.h>\nServo myServo;\n';
    if (c.dist) head += `const int TRIG = ${TRIG}, ECHO = ${ECHO};\n`;
    c.vars.forEach(n => { head += `int ${n} = 0;\n`; });
    if (c.drive) head += '\n' + DRIVE;
    if (c.dist) {
      head += `\nfloat readDistanceCm() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long echoTime = pulseIn(ECHO, HIGH, 30000);
  if (echoTime == 0) return 400;   // no echo: treat the way as clear
  return echoTime * 0.0343 / 2;
}
`;
    }
    let s = '';
    if (c.drive) s += '  pinMode(L1, OUTPUT);\n  pinMode(L2, OUTPUT);\n  pinMode(R1, OUTPUT);\n  pinMode(R2, OUTPUT);\n';
    if (c.dist) s += '  pinMode(TRIG, OUTPUT);\n  pinMode(ECHO, INPUT);\n';
    c.out.forEach(p => { s += `  pinMode(${p}, OUTPUT);\n`; });
    c.input.forEach(p => { s += `  pinMode(${p}, INPUT);\n`; });
    c.pull.forEach(p => { s += `  pinMode(${p}, INPUT_PULLUP);\n`; });
    if (c.serial) s += '  Serial.begin(9600);\n';
    if (c.servo) s += '  myServo.attach(9);\n';
    return `${head}\nvoid setup() {\n${s}${setupBody}}\n\nvoid loop() {\n${loopBody}}\n`;
  }

  // ---------- ready-made programs ----------
  const n = v => ({ type: 'ar_num', fields: { N: v } }), txt = s => ({ type: 'ar_txt', fields: { T: s } }), an = p => ({ type: 'ar_an', fields: { P: p || 'A0' } });
  const inV = (type, fields, inputs) => { const o = { type }; if (fields) o.fields = fields; if (inputs) { o.inputs = {}; Object.keys(inputs).forEach(k => { o.inputs[k] = { block: inputs[k] }; }); } return o; };
  const num0 = v => (typeof v === 'number' ? n(v) : v);
  const get = name => inV('ar_get', { N: name }), dist = () => inV('ar_dist');
  const cmp = (a, o, b) => inV('ar_cmp', { O: o }, { A: num0(a), B: num0(b) }), both = (a, o, b) => inV('ar_both', { O: o }, { A: a, B: b }), not = a => inV('ar_not', null, { A: a });
  const mapTo = (a, b) => inV('ar_map', null, { A: a, B: num0(b) }), mul = (a, b) => inV('ar_arith', { O: '*' }, { A: num0(a), B: num0(b) });
  const btn = p => inV('ar_btn', { P: String(p) }), dread = p => inV('ar_dread', { P: String(p) });
  const pin = (p, v) => inV('ar_pin', { P: String(p), V: v ? 'HIGH' : 'LOW' }), pwm = (p, v) => inV('ar_pwm', { P: String(p) }, { V: num0(v) }), wait = v => inV('ar_wait', null, { V: num0(v) });
  const print = (v, nl) => inV('ar_print', { L: nl ? 'NL' : 'SAME' }, { V: typeof v === 'string' ? txt(v) : v });
  const set = (name, v) => inV('ar_set', { N: name }, { V: num0(v) }), chg = (name, v) => inV('ar_chg', { N: name }, { V: num0(v) });
  const servo = v => inV('ar_servo', null, { V: num0(v) }), tone = (f, p) => inV('ar_tone', { P: String(p) }, { F: n(f) }), noTone = p => inV('ar_notone', { P: String(p) });
  const chain = list => { const c = list.flat().filter(Boolean); for (let i = 0; i < c.length - 1; i++) c[i] = Object.assign({}, c[i]); for (let i = c.length - 2; i >= 0; i--) c[i].next = { block: c[i + 1] }; return c[0]; };
  const iff = (c, t, e) => { const o = inV(e ? 'ar_ifelse' : 'ar_if', null, { C: c }); o.inputs.T = { block: chain(t) }; if (e) o.inputs.E = { block: chain(e) }; return o; };
  const rep = (v, b) => { const o = inV('ar_repeat', null, { N: num0(v) }); o.inputs.DO = { block: chain(b) }; return o; }, wh = (c, b) => { const o = inV('ar_while', null, { C: c }); o.inputs.DO = { block: chain(b) }; return o; };
  const mv = (k, s) => inV('rb_move', { K: k }, { V: n(s) }), halt = () => inV('rb_stop'), wheels = (l, r) => inV('rb_wheels', null, { L: n(l), R: n(r) });
  const line = s => inV('rb_line', { S: s === 'L' ? 'A0' : 'A1' }), eye = s => inV('rb_eye', { S: s === 'L' ? 'A0' : 'A1' }), rbtn = () => inV('rb_btn');
  const light = (c, on) => inV('rb_light', { C: c === 'red' ? '12' : '13', V: on ? 'HIGH' : 'LOW' }), beep = on => inV('rb_beep', { V: on ? 'HIGH' : 'LOW' });
  const prog = (s, l) => {
    const top = (type, y, list) => { const o = { type, x: 16, y, deletable: false }; const c = chain(list); if (c) o.inputs = { DO: { block: c } }; return o; };
    return { blocks: { languageVersion: 0, blocks: [top('ar_setup', 16, s), top('ar_loop', 120, l)] } };
  };
  const follow = () => iff(both(line('L'), '&&', not(line('R'))), [wheels(0, 170)], [iff(both(line('R'), '&&', not(line('L'))), [wheels(170, 0)], [mv('F', 140)])]);
  const PRESET = {
    lab: {
      1: () => prog([], []), 2: () => prog([], [pin(8, 1), wait(1000), pin(8, 0), wait(1000)]), 3: () => prog([], [pin(8, 1), pin(9, 0), wait(500), pin(8, 0), pin(9, 1), wait(500)]),
      4: () => prog([], [pin(10, 1), wait(3000), pin(10, 0), pin(9, 1), wait(1000), pin(9, 0), pin(8, 1), wait(3000), pin(8, 0)]),
      5: () => prog([], [8, 9, 10, 11].flatMap(p => [pin(p, 1), wait(150), pin(p, 0)])), 6: () => prog([pin(8, 1), pin(9, 1)], []),
      7: () => prog([], [set('level', 0), rep(51, [pwm(9, get('level')), chg('level', 5), wait(20)]), rep(51, [pwm(9, get('level')), chg('level', -5), wait(20)])]),
      8: () => prog([], [iff(btn(2), [pin(8, 1)], [pin(8, 0)])]),
      9: () => prog([], [iff(btn(2), [set('pressed', 1)], [set('pressed', 0)]), iff(both(cmp(get('pressed'), '==', 1), '&&', cmp(get('wasPressed'), '==', 0)), [iff(cmp(get('ledOn'), '==', 0), [set('ledOn', 1), pin(8, 1)], [set('ledOn', 0), pin(8, 0)]), wait(50)]), set('wasPressed', get('pressed'))]),
      10: () => prog([], [print('A0 reading: '), print(an(), true), wait(200)]), 11: () => prog([], [pwm(9, mapTo(an(), 255)), wait(10)]),
      12: () => prog([], [iff(cmp(an(), '<', 500), [pin(8, 1)], [pin(8, 0)]), wait(100)]),
      13: () => prog([], [tone(262, 4), wait(300), noTone(4), wait(50), tone(330, 4), wait(300), noTone(4), wait(50), tone(392, 4), wait(300), noTone(4), wait(650)]),
      14: () => prog([], []), 15: () => prog([], [pin(5, 1), wait(800), pin(5, 0), wait(800)]), 16: () => prog([], [pin(5, 1), wait(2000), pin(5, 0), wait(2000)]),
      17: () => prog([], [pwm(5, 80), wait(1500), pwm(5, 160), wait(1500), pwm(5, 255), wait(1500)]), 18: () => prog([], [pwm(5, mapTo(an(), 255)), wait(20)]),
      19: () => prog([], [servo(0), wait(1000), servo(90), wait(1000), servo(180), wait(1000)]),
      20: () => prog([], [set('angle', 0), rep(91, [servo(get('angle')), chg('angle', 2), wait(15)]), rep(91, [chg('angle', -2), servo(get('angle')), wait(15)])]), 21: () => prog([], [servo(mapTo(an(), 180)), wait(15)]),
      22: () => prog([], [print('Distance: '), print(dist()), print(' cm', true), wait(200)]),
      23: () => prog([], [set('cm', dist()), iff(cmp(get('cm'), '<', 60), [pin(8, 1)], [pin(8, 0)]), iff(cmp(get('cm'), '<', 30), [pin(9, 1)], [pin(9, 0)]), iff(cmp(get('cm'), '<', 15), [pin(10, 1), tone(880, 4)], [pin(10, 0), noTone(4)]), wait(100)]),
      24: () => prog([], [iff(cmp(dist(), '<', 20), [pin(8, 1), servo(90)], [pin(8, 0), servo(0)]), wait(100)]), 25: () => prog([], [iff(cmp(dist(), '<', 20), [pin(5, 0), pin(8, 1)], [pin(5, 1), pin(8, 0)]), wait(100)]),
      26: () => prog([], [print('Temperature: '), print(mul(an(), 0.489), true), iff(cmp(mul(an(), 0.489), '>', 30), [pin(8, 1)], [pin(8, 0)]), wait(500)]),
      27: () => prog([], [print(an(), true), iff(cmp(an(), '>', 500), [pin(8, 1)], [pin(8, 0)]), wait(500)]), 28: () => prog([], [iff(cmp(dread(2), '==', 0), [pin(8, 1)], [pin(8, 0)]), wait(50)]),
    },
    robot: {
      5: () => prog([], [wheels(255, 0), wait(1500), wheels(0, 0), wait(500), wheels(0, 255), wait(1500), wheels(0, 0), wait(1500)]), 6: () => prog([], [mv('F', 200), wait(2000), halt(), wait(2000)]),
      7: () => prog([], [mv('F', 200), wait(1500), halt(), wait(500), mv('B', 200), wait(1500), halt(), wait(2000)]), 8: () => prog([], [mv('R', 170), wait(400), halt(), wait(2000)]),
      9: () => prog([], [mv('F', 120), wait(2000), mv('F', 180), wait(2000), mv('F', 255), wait(2000), halt(), wait(3000)]),
      10: () => prog([], [mv('F', 180), wait(1000), halt(), mv('L', 180), wait(400), halt(), mv('F', 180), wait(1000), halt(), mv('R', 180), wait(400), halt(), mv('B', 180), wait(1000), halt(), wait(2000)]),
      11: () => prog([], [rep(4, [mv('F', 180), wait(1200), halt(), wait(300), mv('R', 170), wait(400), halt(), wait(300)]), wait(5000)]),
      12: () => prog([], [mv('F', 200), wait(600), halt(), wait(150), mv('L', 170), wait(300), halt(), wait(150), mv('R', 170), wait(600), halt(), wait(150), mv('L', 170), wait(300), halt(), wait(150), mv('B', 200), wait(600), halt(), wait(150), wheels(120, 255), wait(900), halt(), wait(3000)]),
      13: () => prog([], [iff(rbtn(), [wait(500), mv('F', 200), wait(2000), halt()])]), 14: () => prog([], [light('green', 1), light('red', 0), mv('F', 180), wait(1500), light('green', 0), light('red', 1), halt(), wait(1500)]),
      15: () => prog([], [beep(1), wait(150), beep(0), wait(150), beep(1), wait(150), beep(0), wait(300), mv('F', 180), wait(1500), halt(), wait(3000)]), 16: () => prog([], [print(dist(), true), wait(200)]),
      17: () => prog([], [iff(cmp(dist(), '<', 20), [halt()], [mv('F', 170)]), wait(60)]),
      18: () => prog([], [set('cm', dist()), iff(cmp(get('cm'), '<', 15), [mv('B', 150)], [iff(both(cmp(get('cm'), '>', 25), '&&', cmp(get('cm'), '<', 80)), [mv('F', 150)], [halt()])]), wait(60)]),
      19: () => prog([], [iff(cmp(dist(), '<', 25), [halt(), wait(200), mv('B', 170), wait(400), mv('R', 170), wait(350), halt(), wait(100)], [mv('F', 170)]), wait(60)]),
      20: () => prog([], [servo(150), wait(800), servo(90), wait(800), servo(30), wait(800), servo(90), wait(800)]),
      21: () => prog([servo(90), wait(500)], [iff(cmp(dist(), '<', 25), [halt(), servo(150), wait(400), set('leftCm', dist()), servo(30), wait(400), set('rightCm', dist()), servo(90), wait(300), iff(cmp(get('leftCm'), '>', get('rightCm')), [mv('L', 170)], [mv('R', 170)]), wait(350), halt()], [mv('F', 170)]), wait(60)]),
      22: () => prog([], [print('Left: '), print(eye('L')), print('  Right: '), print(eye('R'), true), wait(200)]), 23: () => prog([], [follow()]),
      24: () => prog([], [iff(both(line('L'), '||', line('R')), [mv('B', 170), wait(400), iff(line('L'), [mv('R', 170)], [mv('L', 170)]), wait(350)], [mv('F', 160)])]),
      25: () => prog([light('red', 1), wh(not(rbtn()), [wait(10)]), wait(500)], [iff(cmp(dist(), '<', 15), [halt(), light('green', 0), light('red', 1), wait(100)], [light('red', 0), light('green', 1), follow()])]),
    },
  };

  // ---------- toolboxes ----------
  const shadowNum = v => ({ shadow: { type: 'ar_num', fields: { N: v } } });
  const T = {
    pin: { kind: 'category', name: 'Pins', colour: C.pin, contents: [{ kind: 'block', type: 'ar_pin' }, { kind: 'block', type: 'ar_pwm', inputs: { V: shadowNum(128) } }, { kind: 'block', type: 'ar_btn' }, { kind: 'block', type: 'ar_dread' }, { kind: 'block', type: 'ar_an' }] },
    time: { kind: 'category', name: 'Time', colour: C.time, contents: [{ kind: 'block', type: 'ar_wait', inputs: { V: shadowNum(1000) } }] },
    logic: { kind: 'category', name: 'Decisions', colour: C.logic, contents: [{ kind: 'block', type: 'ar_if' }, { kind: 'block', type: 'ar_ifelse' }, { kind: 'block', type: 'ar_cmp', inputs: { A: shadowNum(0), B: shadowNum(0) } }, { kind: 'block', type: 'ar_both' }, { kind: 'block', type: 'ar_not' }] },
    loop: { kind: 'category', name: 'Loops', colour: C.loop, contents: [{ kind: 'block', type: 'ar_repeat', inputs: { N: shadowNum(4) } }, { kind: 'block', type: 'ar_while' }] },
    math: { kind: 'category', name: 'Numbers', colour: C.math, contents: [{ kind: 'block', type: 'ar_num' }, { kind: 'block', type: 'ar_arith', inputs: { A: shadowNum(1), B: shadowNum(1) } }, { kind: 'block', type: 'ar_map', inputs: { B: shadowNum(255) } }] },
    vars: { kind: 'category', name: 'Variables', colour: C.vars, contents: [{ kind: 'block', type: 'ar_set', inputs: { V: shadowNum(0) } }, { kind: 'block', type: 'ar_chg', inputs: { V: shadowNum(1) } }, { kind: 'block', type: 'ar_get' }] },
    text: { kind: 'category', name: 'Serial Monitor', colour: C.text, contents: [{ kind: 'block', type: 'ar_print', inputs: { V: { shadow: { type: 'ar_txt' } } } }, { kind: 'block', type: 'ar_txt' }] },
    parts: { kind: 'category', name: 'Parts', colour: C.part, contents: [{ kind: 'block', type: 'ar_dist' }, { kind: 'block', type: 'ar_servo', inputs: { V: shadowNum(90) } }, { kind: 'block', type: 'ar_tone', inputs: { F: shadowNum(440) } }, { kind: 'block', type: 'ar_notone' }] },
    drive: { kind: 'category', name: 'Drive', colour: C.move, contents: [{ kind: 'block', type: 'rb_move', inputs: { V: shadowNum(180) } }, { kind: 'block', type: 'rb_stop' }, { kind: 'block', type: 'rb_wheels', inputs: { L: shadowNum(170), R: shadowNum(170) } }] },
    sense: { kind: 'category', name: 'Sensors', colour: C.sense, contents: [{ kind: 'block', type: 'ar_dist' }, { kind: 'block', type: 'rb_line' }, { kind: 'block', type: 'rb_eye' }, { kind: 'block', type: 'rb_btn' }] },
    extras: { kind: 'category', name: 'Lights and sound', colour: C.part, contents: [{ kind: 'block', type: 'rb_light' }, { kind: 'block', type: 'rb_beep' }, { kind: 'block', type: 'ar_servo', inputs: { V: shadowNum(90) } }] },
  };
  const toolbox = kind => ({ kind: 'categoryToolbox', contents: kind === 'robot' ? [T.drive, T.sense, T.extras, T.time, T.logic, T.loop, T.math, T.vars, T.text] : [T.pin, T.time, T.logic, T.loop, T.parts, T.math, T.vars, T.text] });

  // ---------- loading ----------
  let loading = null;
  function ensure() {
    if (window.Blockly && window.Blockly.__ready) return Promise.resolve();
    if (loading) return loading;
    loading = new Promise((res, rej) => {
      const go = () => { try { window.Blockly.defineBlocksWithJsonArray(DEFS); window.Blockly.__ready = true; res(); } catch (e) { rej(e); } };
      if (window.Blockly) { go(); return; }
      const s = document.createElement('script'); s.src = SRC(); s.onload = go; s.onerror = () => { loading = null; rej(new Error('load')); };
      document.head.appendChild(s);
    });
    return loading;
  }
  function theme() {
    const css = getComputedStyle(document.documentElement), col = n => css.getPropertyValue(n).trim();
    return window.Blockly.Theme.defineTheme('notebook' + Date.now(), { base: window.Blockly.Themes.Classic, componentStyles: { workspaceBackgroundColour: col('--bg'), toolboxBackgroundColour: col('--panel'), toolboxForegroundColour: col('--text'), flyoutBackgroundColour: col('--accent-soft'), flyoutForegroundColour: col('--text'), scrollbarColour: col('--soft'), insertionMarkerColour: col('--text') } });
  }

  // ---------- one panel per simulator ----------
  const hosts = {};
  addEventListener('nb-reading', () => { Object.keys(hosts).forEach(p => { if (hosts[p].ws) hosts[p].ws.setTheme(theme()); }); });
  function attach(p, kind, host) {
    const h = hosts[p] = { p, kind, host, mode: 'code', ws: null, id: null, quiet: false };
    const tabs = $(p + '-tabs');
    tabs.innerHTML = '<button type="button" class="alt on" data-m="code" role="tab" aria-selected="true">Code</button><button type="button" class="alt" data-m="blocks" role="tab" aria-selected="false">Blocks</button>';
    tabs.addEventListener('click', e => { const b = e.target.closest('[data-m]'); if (b) request(h, b.getAttribute('data-m')); });
    const saved = store.get('eblocks-mode');
    h.want = saved === 'blocks' ? 'blocks' : 'code';
  }
  function paint(h) {
    const blocks = h.mode === 'blocks', tabs = $(h.p + '-tabs');
    tabs.querySelectorAll('[data-m]').forEach(b => { const on = b.getAttribute('data-m') === h.mode; b.classList.toggle('on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
    $(h.p + '-blockbox').hidden = !blocks;
    const ta = $(h.p + '-code'); ta.readOnly = blocks; ta.closest('.code-box').classList.toggle('short', blocks);
    ta.closest('.sim-grid').classList.toggle('blocks-on', blocks);
    $(h.p + '-codelabel').textContent = blocks ? 'The code your blocks wrote' : 'Arduino code';
    if (blocks && h.ws) setTimeout(() => { window.Blockly.svgResize(h.ws); }, 0);
  }
  function msg(h, html) { $(h.p + '-blockmsg').innerHTML = html; }
  function request(h, mode) {
    msg(h, '');
    if (mode === 'code') { h.mode = 'code'; store.set('eblocks-mode', 'code'); h.want = 'code'; paint(h); return; }
    if (h.mode === 'blocks') return;
    const saved = store.get(`eblocks-${h.p}-${h.id}`);
    const edited = h.host.isEdited() && !(saved && saved.gen === h.host.getCode());
    if (edited) {
      msg(h, `<div class="confirm"><span>Blocks will replace the code you typed for this example.</span><button type="button" id="${h.p}-bk-yes">Use blocks</button><button type="button" class="alt" id="${h.p}-bk-no">Keep my code</button></div>`);
      $(`${h.p}-bk-yes`).addEventListener('click', () => { msg(h, ''); enter(h); });
      $(`${h.p}-bk-no`).addEventListener('click', () => msg(h, ''));
      return;
    }
    enter(h);
  }
  function enter(h) {
    msg(h, '<p class="marks">Loading blocks&#8230;</p>');
    ensure().then(() => {
      msg(h, '');
      h.mode = 'blocks'; h.want = 'blocks'; store.set('eblocks-mode', 'blocks');
      paint(h);
      if (!h.ws) {
        h.ws = window.Blockly.inject($(h.p + '-blockbox'), { toolbox: toolbox(h.kind), renderer: 'zelos', sounds: false, trashcan: false, theme: theme(), move: { scrollbars: true, drag: true, wheel: true }, zoom: { controls: false, wheel: false, startScale: 0.72 } });
        h.ws.addChangeListener(ev => {
          if (h.quiet || ev.isUiEvent || h.mode !== 'blocks') return;
          push(h);
        });
      }
      load(h);
    }).catch(() => {
      h.mode = 'code'; h.want = 'code'; paint(h);
      msg(h, '<div class="msg">Blocks couldn\'t load. They need an internet connection the first time. The Code tab still works.</div>');
    });
  }
  function push(h) {
    const code = generate(h.ws, h.kind);
    store.set(`eblocks-${h.p}-${h.id}`, { ws: window.Blockly.serialization.workspaces.save(h.ws), gen: code });
    h.host.setBlocksCode(code);
  }
  function load(h) {
    const saved = store.get(`eblocks-${h.p}-${h.id}`);
    const preset = PRESET[h.kind] && PRESET[h.kind][h.host.number()];
    const state = saved ? saved.ws : (preset ? preset() : prog([], []));
    h.quiet = true;
    window.Blockly.Events.disable();
    try { window.Blockly.serialization.workspaces.load(state, h.ws); h.ws.cleanUp(); } finally { window.Blockly.Events.enable(); }
    h.quiet = false;
    window.Blockly.svgResize(h.ws);
    h.ws.scroll(16, 16);
    push(h);
  }

  window.EBlocks = {
    attach,
    onOpen(p, id) {
      const h = hosts[p]; if (!h) return;
      h.id = id; msg(h, '');
      if (h.want === 'blocks') { if (h.mode === 'blocks' && h.ws) { load(h); paint(h); } else enter(h); } else { h.mode = 'code'; paint(h); }
    },
    reset(p, id) { store.del(`eblocks-${p}-${id}`); },
    // Used by tests: the code a ready-made program generates.
    presetCode(kind, number) {
      return ensure().then(() => {
        const ws = new window.Blockly.Workspace();
        window.Blockly.Events.disable();
        window.Blockly.serialization.workspaces.load(PRESET[kind][number](), ws);
        window.Blockly.Events.enable();
        const code = generate(ws, kind); ws.dispose(); return code;
      });
    },
    presets() { return { lab: Object.keys(PRESET.lab).map(Number), robot: Object.keys(PRESET.robot).map(Number) }; },
  };
})();
