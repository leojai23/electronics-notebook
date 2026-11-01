/* Coding course runner: runs a lesson's code on a virtual board, and checks the tasks. */
(function (root) {
  'use strict';
  const { Sim } = root.ELab;

  // A board with no circuit: a button on pin 2, a dial on A0, and pins you can watch.
  class LessonSim extends Sim {
    constructor(code) {
      super({ parts: [], wires: [] }, code, {});
      this.press = 0; this.dial = 0.5; this.log = {};
    }
    recalc() { this.dirty = false; }
    builtin(name, a, line) {
      const vm = this.vm;
      if (name === 'digitalRead') {
        const pin = a[0]; this.checkPin(pin, line); vm.time += 5;
        const q = this.pins[pin];
        if (q.mode === 1) return q.level;
        if (pin === 2) { if (this.press) return 0; if (q.mode === 2) return 1; this.warnOnce('float2', 'The button on pin 2 needs INPUT_PULLUP, or its reading will float.'); return Math.random() < 0.5 ? 0 : 1; }
        return 0;
      }
      if (name === 'analogRead') {
        vm.time += 100;
        const pin = a[0] < 6 ? a[0] + 14 : a[0];
        return pin === 14 ? Math.round(this.dial * 1023) : 0;
      }
      if (name === 'digitalWrite') {
        this.checkPin(a[0], line);
        const was = this.pins[a[0]].level, r = super.builtin(name, a, line), now = this.pins[a[0]].level;
        if (was !== now) (this.log[a[0]] = this.log[a[0]] || []).push(this.vm.time / 1000);
        return r;
      }
      return super.builtin(name, a, line);
    }
  }

  // Runs a task's code and compares it with what the task expects.
  function checkTask(task, code) {
    const s = new LessonSim(code), results = [];
    if (s.err) return { results: [{ ok: false, say: `Line ${s.err.line}: ${s.err.msg}` }], err: s.err };
    const press = (task.press || []).slice(), at = {};
    (task.expect || []).forEach(e => { if (e.t !== undefined) at[e.t] = true; });
    const levels = {};
    for (let t = 0; t < (task.run || 1000); t += 10) {
      while (press.length && press[0][0] <= t) s.press = press.shift()[1];
      s.step(10);
      if (s.err) break;
      if (at[t]) levels[t] = Object.assign({}, ...Object.keys(s.pins).map(k => ({ [k]: s.pins[k].mode === 1 ? s.pins[k].level : 0 })));
    }
    if (s.err) return { results: [{ ok: false, say: `Line ${s.err.line}: ${s.err.msg}` }], err: s.err };
    for (const e of task.expect || []) {
      let ok = true;
      if (e.serial !== undefined) ok = new RegExp(e.serial, 'm').test(s.serial);
      if (e.notSerial !== undefined) ok = !new RegExp(e.notSerial, 'm').test(s.serial);
      if (e.toggles !== undefined) ok = ((s.log[e.toggles] || []).length >= e.atLeast);
      if (e.noCode !== undefined) ok = !new RegExp(e.noCode).test(code.replace(/\/\/.*$/gm, ''));
      if (e.highAt !== undefined) ok = !!(levels[e.t] && levels[e.t][e.highAt] === 1);
      if (e.lowAt !== undefined) ok = !!(levels[e.t] && levels[e.t][e.lowAt] === 0);
      results.push({ ok, say: e.say });
    }
    return { results, serial: s.serial };
  }
  root.ECourseRun = { LessonSim, checkTask };

  if (typeof document === 'undefined') return;

  // ---------- screen ----------
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* the page still works */ } },
  };
  const active = new Set();
  function esc(s) { return String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }
  function wireRunner(box) {
    const ta = box.querySelector('textarea'), out = box.querySelector('.run-out'), runBtn = box.querySelector('[data-run]'), key = box.getAttribute('data-key'), original = ta.value;
    const saved = store.get(key); if (typeof saved === 'string') ta.value = saved;
    ta.addEventListener('input', () => store.set(key, ta.value));
    ta.addEventListener('keydown', e => { if (e.key === 'Tab' && !e.shiftKey) { e.preventDefault(); ta.setRangeText('  ', ta.selectionStart, ta.selectionEnd, 'end'); store.set(key, ta.value); } });
    const state = { sim: null, raf: 0, last: 0 };
    const led = box.querySelector('[data-led]'), hold = box.querySelector('[data-hold]'), dial = box.querySelector('[data-dial]');
    function paint() { if (led) { const q = state.sim && state.sim.pins[13]; led.classList.toggle('lit', !!(q && q.mode === 1 && q.level)); } }
    function stop() {
      if (state.raf) cancelAnimationFrame(state.raf);
      state.raf = 0; state.sim = null; runBtn.textContent = 'Run'; runBtn.classList.remove('stop'); active.delete(stop); paint();
    }
    function start() {
      const s = new LessonSim(ta.value);
      if (s.err) { out.textContent = `Line ${s.err.line}: ${s.err.msg}`; out.classList.add('bad'); return; }
      out.classList.remove('bad'); out.textContent = ''; state.sim = s; if (dial) s.dial = +dial.value / 100;
      runBtn.textContent = 'Stop'; runBtn.classList.add('stop'); active.add(stop); state.last = performance.now();
      let lastLen = -1;
      const tick = now => {
        if (!state.sim) return;
        s.step(Math.min(50, now - state.last)); state.last = now;
        if (s.err) { out.textContent = `Line ${s.err.line}: ${s.err.msg}`; out.classList.add('bad'); stop(); return; }
        if (s.serial.length !== lastLen) { out.textContent = s.serial.slice(-2000); out.scrollTop = out.scrollHeight; lastLen = s.serial.length; }
        paint(); state.raf = requestAnimationFrame(tick);
      };
      state.raf = requestAnimationFrame(tick);
    }
    runBtn.addEventListener('click', () => (state.sim ? stop() : start()));
    box.querySelector('[data-reset]').addEventListener('click', () => { stop(); ta.value = original; store.set(key, original); out.textContent = ''; out.classList.remove('bad'); const r = box.querySelector('.task-res'); if (r) r.innerHTML = ''; });
    if (hold) {
      const set = v => { if (state.sim) state.sim.press = v; hold.classList.toggle('on', !!v); };
      hold.addEventListener('pointerdown', () => set(1));
      ['pointerup', 'pointerleave', 'pointercancel', 'blur'].forEach(ev => hold.addEventListener(ev, () => set(0)));
      hold.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); set(1); } });
      hold.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') set(0); });
    }
    if (dial) dial.addEventListener('input', () => { if (state.sim) state.sim.dial = +dial.value / 100; });
    const chk = box.querySelector('[data-check]');
    if (chk) chk.addEventListener('click', () => {
      stop();
      const r = checkTask(root.COURSE_TASKS[box.getAttribute('data-task')], ta.value), all = r.results.every(x => x.ok);
      box.querySelector('.task-res').innerHTML = `<div class="check-head ${all ? 'ok' : 'no'}">${all ? 'Well done. That works.' : 'Not there yet.'}</div><ul class="check-list">` + r.results.map(x => `<li class="${x.ok ? 'ok' : 'no'}"><span aria-hidden="true">${x.ok ? '&#10003;' : '&#10007;'}</span> ${esc(x.say)}</li>`).join('') + '</ul>';
      if (r.serial !== undefined) out.textContent = r.serial.slice(-1500);
      if (all) { const d = store.get('course-done') || {}; d[box.getAttribute('data-task')] = 1; store.set('course-done', d); paintDone(); }
    });
  }
  function paintDone() {
    const d = store.get('course-done') || {}, boxes = document.querySelectorAll('[data-done-for]');
    boxes.forEach(el => { el.textContent = d[el.getAttribute('data-done-for')] ? ' ✓ done' : ''; });
    const sum = document.getElementById('course-sum');
    if (sum) sum.textContent = `${Object.keys(d).length} of ${Object.keys(root.COURSE_TASKS).length} tasks completed in this browser.`;
  }
  root.EParts = {
    init() {
      const key = 'parts-have', have = store.get(key) || {}, boxes = document.querySelectorAll('[data-part]');
      const paint = () => { let n = 0; boxes.forEach(b => { if (b.checked) n++; }); document.getElementById('parts-sum').textContent = `You have ${n} of ${boxes.length} items, in this browser.`; };
      boxes.forEach(b => { b.checked = !!have[b.getAttribute('data-part')]; b.addEventListener('change', () => { have[b.getAttribute('data-part')] = b.checked; store.set(key, have); paint(); }); });
      paint();
      const btn = document.getElementById('parts-copy'), out = document.getElementById('parts-out');
      btn.addEventListener('click', () => {
        const dec = document.createElement('textarea'), lines = [];
        boxes.forEach(b => { if (!b.checked) { dec.innerHTML = b.getAttribute('data-name'); lines.push(dec.value); } });
        const text = lines.length ? lines.join('\n') : 'You have everything on the list.';
        const done = m => { btn.textContent = m; setTimeout(() => { btn.textContent = 'Copy what I still need'; }, 1800); };
        const fallback = () => { out.hidden = false; out.value = text; out.focus(); out.select(); done('Selected: press Ctrl+C'); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(() => done('Copied'), fallback); else fallback();
      });
    },
  };
  root.ECourse = {
    init() { document.querySelectorAll('[data-key]').forEach(wireRunner); paintDone(); },
    stopAll() { active.forEach(f => f()); },
  };
})(typeof window !== 'undefined' ? window : globalThis);
