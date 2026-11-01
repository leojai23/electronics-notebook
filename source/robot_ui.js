/* Robot simulator screen, plus the Build Log for recording real-world tests. */
(function () {
  'use strict';
  const R = window.ERobot, CODE = window.ROBOT_CODE, EX = window.ELAB_EXAMPLES;
  const $ = id => document.getElementById(id);
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* the page still works */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* the page still works */ } },
  };
  const NO_DRIVE = new Set([5]);
  const UI = {
    n: null, sim: null, raf: 0, last: 0, code: '', map: 'open', start: null, wheelL: 0, wheelR: 0,
    init() {
      const sel = $('rs-map');
      sel.innerHTML = Object.keys(R.MAPS).map(k => `<option value="${k}">${R.MAPS[k].name}</option>`).join('');
      sel.addEventListener('change', () => { this.stop(); this.map = sel.value; this.applyStart(true); this.draw(); this.status(`Floor set to ${R.MAPS[this.map].name}. Drag the robot to where you want it to start.`); });
      $('rs-start').addEventListener('click', () => (this.sim ? this.stop() : this.begin()));
      $('rs-reset').addEventListener('click', () => { this.stop(); this.applyStart(true); this.draw(); this.status('Robot back at its starting point.'); });
      $('rs-check').addEventListener('click', () => this.check());
      $('rs-restore').addEventListener('click', () => { if (this.n) $('rs-confirm').hidden = false; });
      $('rs-yes').addEventListener('click', () => { store.del('erobot-' + this.n); if (window.EBlocks) window.EBlocks.reset('rs', this.n); $('rs-confirm').hidden = true; this.open(this.n); this.status('Original code restored.'); });
      $('rs-no').addEventListener('click', () => { $('rs-confirm').hidden = true; });
      $('rs-left').addEventListener('click', () => this.turn(-15));
      $('rs-right').addEventListener('click', () => this.turn(15));
      $('rs-mis').addEventListener('change', () => { if (this.sim) this.stop(); this.status($('rs-mis').checked ? 'Now the left motor is 4% weaker, like many real motors.' : 'Both motors now match perfectly.'); });
      const ta = $('rs-code');
      ta.addEventListener('input', () => { this.code = ta.value; this.gutter(); if (this.sim) this.stop(); this.mark(null); store.set('erobot-' + this.n, this.code); });
      ta.addEventListener('scroll', () => { $('rs-gutter').scrollTop = ta.scrollTop; });
      ta.addEventListener('keydown', e => { if (e.key === 'Tab' && !e.shiftKey) { e.preventDefault(); ta.setRangeText('  ', ta.selectionStart, ta.selectionEnd, 'end'); ta.dispatchEvent(new Event('input')); } });
      const hold = $('rs-btn'), set = v => { if (this.sim) this.sim.press = v; hold.classList.toggle('on', !!v); };
      hold.addEventListener('pointerdown', () => set(1));
      ['pointerup', 'pointerleave', 'pointercancel', 'blur'].forEach(ev => hold.addEventListener(ev, () => set(0)));
      hold.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); set(1); } });
      hold.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') set(0); });
      $('rs-gap').addEventListener('input', () => { $('rs-gap-out').textContent = $('rs-gap').value + ' cm'; if (this.sim) { this.sim.setTargetGap(+$('rs-gap').value); this.draw(); } });
      $('rs-box').addEventListener('change', () => { this.boxGone = $('rs-box').checked; if (this.sim) this.sim.removeBox(this.boxGone); this.draw(); });
      const cv = $('rs-canvas');
      cv.addEventListener('pointerdown', e => { if (this.sim) return; const p = this.toWorld(e); if (Math.hypot(p.x - this.start.x, p.y - this.start.y) < 26) { this.drag = true; cv.setPointerCapture(e.pointerId); } });
      cv.addEventListener('pointermove', e => { if (!this.drag) return; const p = this.toWorld(e); this.start.x = Math.max(12, Math.min(R.W - 12, p.x)); this.start.y = Math.max(12, Math.min(R.H - 12, p.y)); this.draw(); });
      cv.addEventListener('pointerup', () => { this.drag = false; });
      addEventListener('resize', () => { if (this.n !== null && !$('page-rsim').hidden) this.draw(); });
    },
    toWorld(e) { const r = $('rs-canvas').getBoundingClientRect(); return { x: (e.clientX - r.left) / r.width * R.W, y: (e.clientY - r.top) / r.height * R.H }; },
    turn(d) { if (this.sim) return; this.start.deg = (this.start.deg + d + 360) % 360; this.draw(); },
    applyStart(force) {
      const sc = R.SCEN[this.n] || {}, st = sc.start && (!this.map || this.map === sc.map) ? sc.start : { x: 60, y: 105, deg: 0 };
      if (force || !this.start) this.start = Object.assign({}, st);
    },
    open(n) {
      this.stop();
      n = R.SCEN[n] ? n : 6;
      this.n = n; const sc = R.SCEN[n];
      this.map = sc.map; this.boxGone = false; $('rs-box').checked = false; $('rs-map').value = sc.map; this.applyStart(true);
      const saved = store.get('erobot-' + n); this.code = typeof saved === 'string' ? saved : CODE[n].code;
      $('rs-code').value = this.code; this.gutter(); this.mark(null);
      $('rs-title').textContent = `Robot Simulator: Exercise ${n}`; $('rs-sub').textContent = CODE[n].title + (sc.intro ? `. ${sc.intro}` : '');
      $('rs-back').setAttribute('href', `#robot-${n}`); $('rs-serial').textContent = ''; $('rs-results').innerHTML = ''; $('rs-msgs').innerHTML = ''; $('rs-confirm').hidden = true;
      const fit = sc.fit || [];
      $('rs-ctl-btn').hidden = !fit.includes('button'); $('rs-ctl-gap').hidden = sc.map !== 'target'; $('rs-ctl-box').hidden = sc.map !== 'mission';
      if (sc.gap) { $('rs-gap').value = sc.gap; $('rs-gap-out').textContent = sc.gap + ' cm'; }
      const prev = n > 5 ? `<a href="#rsim-${n - 1}">&larr; Exercise ${n - 1}</a>` : '<a href="#robots">&larr; All exercises</a>';
      const next = n < 25 ? `<a href="#rsim-${n + 1}">Exercise ${n + 1} &rarr;</a>` : '<a href="#robots">All exercises &rarr;</a>';
      $('rs-pn').innerHTML = prev + next;
      this.draw(); this.read();
      if (window.EBlocks) window.EBlocks.onOpen('rs', n);
      this.status('Select Start to run this code. When stopped, you can drag the robot to a new starting point.');
    },
    close() { this.stop(); },
    blockHost() {
      const U = this;
      return {
        number() { return U.n; },
        getCode() { return U.code; },
        isEdited() { return U.code !== CODE[U.n].code; },
        setBlocksCode(code) { const was = !!U.sim; U.code = code; $('rs-code').value = code; U.gutter(); U.mark(null); store.set('erobot-' + U.n, code); if (was) U.stop(); },
      };
    },
    opts() { return { map: this.map, start: Object.assign({}, this.start), mismatch: $('rs-mis').checked ? 0.04 : 0 }; },
    begin() {
      const s = R.makeSim(this.n, this.code, this.opts());
      $('rs-results').innerHTML = '';
      if (s.err) { this.showErr(s.err); return; }
      if (this.map === 'target') s.setTargetGap(+$('rs-gap').value);
      if (this.boxGone) s.removeBox(true);
      this.mark(null); this.sim = s; this.lastSerial = -1; this.msgKey = null; $('rs-serial').textContent = '';
      const b = $('rs-start'); b.textContent = 'Stop'; b.classList.add('stop');
      this.status('Robot running.'); this.last = performance.now();
      const tick = now => {
        if (!this.sim) return;
        const dt = Math.min(50, now - this.last); this.last = now;
        this.sim.step(dt);
        if (this.sim.err) { const e = this.sim.err; this.stop(); this.showErr(e); return; }
        this.draw(); this.read();
        this.raf = requestAnimationFrame(tick);
      };
      this.raf = requestAnimationFrame(tick);
    },
    stop() {
      if (this.raf) cancelAnimationFrame(this.raf);
      this.raf = 0; const was = !!this.sim; this.sim = null;
      const b = $('rs-start'); if (b) { b.textContent = 'Start'; b.classList.remove('stop'); }
      if (was) { this.keep = this.lastPose; this.status('Robot stopped. Select Reset to go back to the start.'); }
    },
    showErr(e) { this.mark(e.line); $('rs-msgs').innerHTML = `<div class="msg bad"><strong>Code problem on line ${e.line}.</strong> ${e.msg}</div>`; this.status(`Code problem on line ${e.line}.`); },
    check() {
      this.stop();
      const usingDefaultFloor = this.map === R.SCEN[this.n].map;
      const r = R.runRobotCheck(this.n, this.code, { mismatch: 0 });
      if (r.compileError) this.mark(r.compileError.line);
      const all = r.results.every(x => x.ok);
      let h = `<div class="check-head ${all ? 'ok' : 'no'}">${all ? 'Your code passes every check.' : 'Not there yet. Look at the items marked below.'}</div><ul class="check-list">`;
      h += r.results.map(x => `<li class="${x.ok ? 'ok' : 'no'}"><span aria-hidden="true">${x.ok ? '&#10003;' : '&#10007;'}</span> ${x.say}</li>`).join('') + '</ul>';
      h += r.warns.filter(w => w.sev !== 'bad' || !all).map(w => `<div class="msg ${w.sev}">${w.msg}</div>`).join('');
      if (!usingDefaultFloor) h += '<div class="msg">Checks always use this exercise\'s own floor and starting point.</div>';
      $('rs-results').innerHTML = h;
      this.status(all ? 'All checks passed.' : 'Some checks need another look.');
    },
    status(s) { $('rs-status').textContent = s; },
    gutter() { const n = this.code.split('\n').length; let h = ''; for (let i = 1; i <= n; i++) h += `<span data-l="${i}">${i}</span>`; $('rs-gutter').innerHTML = h; $('rs-gutter').scrollTop = $('rs-code').scrollTop; },
    mark(l) { document.querySelectorAll('#rs-gutter .err').forEach(x => x.classList.remove('err')); if (l) { const el = document.querySelector(`#rs-gutter [data-l="${l}"]`); if (el) el.classList.add('err'); } },
    read() {
      const s = this.sim, pct = v => `${Math.round(v / 52 * 100)}%`;
      if (!s) { $('rs-read').innerHTML = '<span><b>Left wheel</b> 0%</span><span><b>Right wheel</b> 0%</span><span><b>Crashes</b> 0</span><span><b>Time</b> 0.0 s</span>'; return; }
      const d = s.distance();
      $('rs-read').innerHTML = `<span><b>Left wheel</b> ${pct(s.vL)}</span><span><b>Right wheel</b> ${pct(s.vR)}</span><span><b>Sensor sees</b> ${d > 400 ? 'nothing' : Math.round(d) + ' cm'}</span><span><b>Line</b> L ${s.eye('L')}, R ${s.eye('R')}</span><span><b>Crashes</b> ${s.crashes}</span><span><b>Time</b> ${(s.simT / 1e6).toFixed(1)} s</span>`;
      if (s.serial.length !== this.lastSerial) { const box = $('rs-serial'); box.textContent = s.serial.slice(-3000); box.scrollTop = box.scrollHeight; this.lastSerial = s.serial.length; }
      const list = Array.from(s.warns.values()), key = list.map(w => w.msg).join('|');
      if (key !== this.msgKey) { this.msgKey = key; $('rs-msgs').innerHTML = list.map(w => `<div class="msg ${w.sev}">${w.msg}</div>`).join(''); }
    },
    draw() {
      const cv = $('rs-canvas'), box = cv.getBoundingClientRect(); if (!box.width) return;
      const dpr = window.devicePixelRatio || 1, pw = Math.round(box.width * dpr), ph = Math.round(box.width * R.H / R.W * dpr);
      if (cv.width !== pw || cv.height !== ph) { cv.width = pw; cv.height = ph; }
      const css = getComputedStyle(document.documentElement), col = n => css.getPropertyValue(n).trim();
      const c = cv.getContext('2d'), S = pw / R.W;
      c.setTransform(S, 0, 0, S, 0, 0);
      c.fillStyle = col('--card'); c.fillRect(0, 0, R.W, R.H);
      c.strokeStyle = col('--acrylic'); c.lineWidth = 0.25; c.beginPath();
      for (let x = 20; x < R.W; x += 20) { c.moveTo(x, 0); c.lineTo(x, R.H); }
      for (let y = 20; y < R.H; y += 20) { c.moveTo(0, y); c.lineTo(R.W, y); }
      c.stroke();
      const s = this.sim, map = R.MAPS[this.map];
      c.lineCap = 'round'; c.lineJoin = 'round';
      c.strokeStyle = col('--black');
      map.lines.forEach(l => { c.lineWidth = l.w; c.beginPath(); l.pts.forEach((p, i) => (i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]))); c.stroke(); });
      const walls = s ? s.walls.filter(w => !w.border && !w.gone) : map.walls.filter(w => !(w.id === 'box' && this.boxGone)).map(w => (w.id === 'target' ? Object.assign({}, w, { x: this.start.x + 13 + +$('rs-gap').value, y: this.start.y - w.h / 2 }) : w));
      walls.forEach(w => { c.fillStyle = w.id === 'target' ? col('--tan') : col('--silver-d'); c.fillRect(w.x, w.y, w.w, w.h); c.strokeStyle = col('--black-l'); c.lineWidth = 0.6; c.strokeRect(w.x, w.y, w.w, w.h); });
      if (s) { c.strokeStyle = col('--pt'); c.lineWidth = 1; c.beginPath(); s.trail.forEach((p, i) => (i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1]))); c.stroke(); }
      const sc = R.SCEN[this.n] || {}, fit = sc.fit || [], x = s ? s.x : this.start.x, y = s ? s.y : this.start.y, th = s ? s.th : this.start.deg * Math.PI / 180, head = s ? s.head : 90;
      if (fit.includes('sonar') && s) {
        const [ox, oy] = s.sonarPos(), d = Math.min(s.distance(), 400), a = th - (head - 90) * Math.PI / 180, ping = s.simT - s.lastPing < 120000;
        c.fillStyle = col('--pt'); c.globalAlpha = ping ? 0.28 : 0.1; c.beginPath(); c.moveTo(ox, oy);
        c.lineTo(ox + d * Math.cos(a - 0.13), oy + d * Math.sin(a - 0.13)); c.lineTo(ox + d * Math.cos(a + 0.13), oy + d * Math.sin(a + 0.13)); c.closePath(); c.fill(); c.globalAlpha = 1;
      }
      c.save(); c.translate(x, y); c.rotate(th);
      this.wheelL = (this.wheelL + (s ? s.vL : 0) * 0.05) % 4; this.wheelR = (this.wheelR + (s ? s.vR : 0) * 0.05) % 4;
      const wheel = (wy, off) => { c.fillStyle = col('--black'); c.fillRect(-7, wy - 1.5, 13, 3); c.strokeStyle = col('--black-l'); c.lineWidth = 0.5; for (let i = -7 + (off + 4) % 4; i < 6; i += 4) { c.beginPath(); c.moveTo(i, wy - 1.5); c.lineTo(i, wy + 1.5); c.stroke(); } };
      wheel(-10.5, this.wheelL); wheel(10.5, this.wheelR);
      c.fillStyle = col('--acrylic'); c.strokeStyle = col('--acrylic-d'); c.lineWidth = 0.6; c.beginPath(); c.roundRect(-10, -9, 21, 18, 3); c.fill(); c.stroke();
      c.fillStyle = col('--teal'); c.fillRect(-3, -5.5, 10, 11);
      c.fillStyle = col('--black'); c.fillRect(-9, -5, 4, 10);
      const on = p => s && s.pins[p].mode === 1 && s.pins[p].level;
      if (fit.includes('leds')) { c.fillStyle = on(12) ? col('--red') : col('--black-l'); c.beginPath(); c.arc(3, -7, 1.3, 0, 7); c.fill(); c.fillStyle = on(13) ? col('--led-green') : col('--black-l'); c.beginPath(); c.arc(3, 7, 1.3, 0, 7); c.fill(); }
      if (fit.includes('line')) ['L', 'R'].forEach(k => { const w = k === 'L' ? -R.EYE_S : R.EYE_S, seen = s && s.eye(k); c.fillStyle = seen ? col('--pt') : col('--blue'); c.beginPath(); c.arc(R.EYE_F, w, 1.5, 0, 7); c.fill(); });
      if (fit.includes('sonar')) { c.save(); c.translate(11, 0); c.rotate(-(head - 90) * Math.PI / 180); c.fillStyle = col('--blue'); c.fillRect(0, -5, 3, 10); c.fillStyle = col('--silver'); c.beginPath(); c.arc(3, -2.6, 1.3, 0, 7); c.arc(3, 2.6, 1.3, 0, 7); c.fill(); c.restore(); }
      if (fit.includes('buzzer') && on(4)) { c.strokeStyle = col('--pt'); c.lineWidth = 0.8; c.beginPath(); c.arc(0, 0, 15, 0, 7); c.stroke(); }
      c.fillStyle = col('--white'); c.beginPath(); c.moveTo(9, 0); c.lineTo(5.5, -2.4); c.lineTo(5.5, 2.4); c.closePath(); c.fill();
      c.restore();
      if (sc.lifted && this.map === sc.map) { c.setTransform(S, 0, 0, S, 0, 0); c.fillStyle = col('--card-ink'); c.font = '600 6px sans-serif'; c.fillText('On a box: wheels spin in the air', x - 40, y + 26); }
    },
  };
  window.ERobotUI = UI;

  // ---------- Build Log ----------
  const LOG_KEY = 'build-log';
  const Log = {
    data: {},
    rows() {
      const a = EX.map(e => ({ id: 'ex' + e.n, name: `Example ${e.n}: ${e.title}`, href: '#ex-' + e.n }));
      const b = Object.keys(window.ROBOT_TITLES).map(n => ({ id: 'r' + n, name: `Exercise ${n}: ${window.ROBOT_TITLES[n]}`, href: '#robot-' + n }));
      return { a, b };
    },
    init() {
      this.data = store.get(LOG_KEY) || {};
      const { a, b } = this.rows();
      const row = r => {
        const d = this.data[r.id] || {};
        const opts = ['Not tried', 'Worked', 'Worked after a fix', 'Problem'].map(o => `<option${d.s === o ? ' selected' : ''}>${o}</option>`).join('');
        return `<tr><td><a href="${r.href}">${r.name}</a></td><td><select id="log-s-${r.id}" data-log="${r.id}" aria-label="Result for ${r.name}">${opts}</select></td><td><input type="text" id="log-n-${r.id}" data-logn="${r.id}" value="${(d.n || '').replace(/"/g, '&quot;')}" aria-label="Notes for ${r.name}" placeholder="What did you notice?"></td></tr>`;
      };
      const head = '<tr><th>Build</th><th>Result</th><th>Notes</th></tr>';
      $('log-a').innerHTML = head + a.map(row).join(''); $('log-b').innerHTML = head + b.map(row).join('');
      document.querySelectorAll('[data-log]').forEach(el => el.addEventListener('change', () => { this.set(el.getAttribute('data-log'), 's', el.value); }));
      document.querySelectorAll('[data-logn]').forEach(el => el.addEventListener('input', () => { this.set(el.getAttribute('data-logn'), 'n', el.value); }));
      $('log-copy').addEventListener('click', () => this.copy());
      this.paint();
    },
    set(id, k, v) { this.data[id] = this.data[id] || {}; this.data[id][k] = v; store.set(LOG_KEY, this.data); this.paint(); },
    paint() {
      const { a, b } = this.rows(), all = a.concat(b); let ok = 0, bad = 0;
      all.forEach(r => { const s = (this.data[r.id] || {}).s; if (s === 'Worked' || s === 'Worked after a fix') ok++; if (s === 'Problem') bad++; });
      $('log-sum').textContent = `${ok} of ${all.length} builds confirmed on real parts, ${bad} with problems.`;
    },
    copy() {
      const { a, b } = this.rows(), lines = [];
      a.concat(b).forEach(r => { const d = this.data[r.id] || {}; if (d.s && d.s !== 'Not tried') lines.push(`${r.name}: ${d.s}${d.n ? ' (' + d.n + ')' : ''}`); });
      const text = lines.length ? lines.join('\n') : 'No builds recorded yet.', btn = $('log-copy');
      const done = m => { btn.textContent = m; setTimeout(() => { btn.textContent = 'Copy my results'; }, 1800); };
      const out = $('log-out');
      const fallback = () => { out.hidden = false; out.value = text; out.focus(); out.select(); done('Selected: press Ctrl+C'); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(() => done('Copied'), fallback); else fallback();
    },
  };
  window.EBuildLog = Log;
})();
