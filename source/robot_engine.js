/* Robot simulator: runs the exercise sketches on a virtual 2-wheel robot. Units are cm and seconds. No DOM here. */
(function (root) {
  'use strict';
  const { Sim } = root.ELab;
  const W = 320, H = 210, VMAX = 52, TRACK = 14, BODY_R = 11, SONAR_F = 13, EYE_F = 10, EYE_S = 4;
  const PIN = { L1: 5, L2: 6, R1: 3, R2: 11, TRIG: 7, ECHO: 8, HEAD: 9, BTN: 2, RED: 12, GREEN: 13, BUZZ: 4, EYE_L: 14, EYE_R: 15 };
  const rad = d => d * Math.PI / 180, deg = r => r * 180 / Math.PI;

  function stadium() {
    const pts = [], r = 45, x1 = 90, x2 = 230, y1 = 60, y2 = 150, cy = (y1 + y2) / 2;
    for (let x = x1; x <= x2; x += 5) pts.push([x, y2]);
    for (let a = 90; a >= -90; a -= 6) pts.push([x2 + r * Math.cos(rad(a)), cy + r * Math.sin(rad(a))]);
    for (let x = x2; x >= x1; x -= 5) pts.push([x, y1]);
    for (let a = -90; a >= -270; a -= 6) pts.push([x1 + r * Math.cos(rad(a)), cy + r * Math.sin(rad(a))]);
    pts.push(pts[0]);
    return pts;
  }
  function circle(cx, cy, r) { const p = []; for (let a = 0; a <= 360; a += 5) p.push([cx + r * Math.cos(rad(a)), cy + r * Math.sin(rad(a))]); return p; }

  const MAPS = {
    open: { name: 'Open floor', walls: [], lines: [] },
    wall: { name: 'Wall ahead', walls: [{ x: 300, y: 15, w: 12, h: 180 }], lines: [] },
    target: { name: 'Moving target', walls: [{ id: 'target', x: 200, y: 75, w: 14, h: 60, soft: true }], lines: [] },
    boxes: { name: 'Obstacle course', walls: [{ x: 110, y: 12, w: 40, h: 40 }, { x: 235, y: 15, w: 40, h: 40 }, { x: 100, y: 160, w: 44, h: 38 }, { x: 235, y: 155, w: 40, h: 40 }, { x: 180, y: 80, w: 36, h: 50 }], lines: [] },
    corner: { name: 'Wall with a choice', walls: [{ x: 250, y: 20, w: 14, h: 105 }, { x: 120, y: 42, w: 130, h: 13 }], lines: [] },
    strip: { name: 'Straight line', walls: [], lines: [{ w: 4, pts: [[10, 105], [310, 105]] }] },
    oval: { name: 'Line track', walls: [], lines: [{ w: 4, pts: stadium() }] },
    ring: { name: 'Ring', walls: [], lines: [{ w: 5, pts: circle(160, 105, 90) }], ring: { x: 160, y: 105, r: 90 } },
    mission: { name: 'Mission track', walls: [{ id: 'box', x: 150, y: 48, w: 22, h: 24 }], lines: [{ w: 4, pts: stadium() }] },
  };

  function rayRect(ox, oy, dx, dy, r) {
    let t0 = 0, t1 = Infinity;
    for (const [o, d, a, b] of [[ox, dx, r.x, r.x + r.w], [oy, dy, r.y, r.y + r.h]]) {
      if (Math.abs(d) < 1e-9) { if (o < a || o > b) return Infinity; continue; }
      let p = (a - o) / d, q = (b - o) / d;
      if (p > q) { const s = p; p = q; q = s; }
      t0 = Math.max(t0, p); t1 = Math.min(t1, q);
      if (t0 > t1) return Infinity;
    }
    return t0;
  }

  class RobotSim extends Sim {
    constructor(mapId, start, code, opts) {
      super({ parts: [], wires: [] }, code, opts);
      opts = opts || {};
      const m = MAPS[mapId] || MAPS.open;
      this.mapId = mapId;
      this.walls = JSON.parse(JSON.stringify(m.walls)).concat([{ x: -10, y: -10, w: W + 20, h: 10, border: true }, { x: -10, y: H, w: W + 20, h: 10, border: true }, { x: -10, y: 0, w: 10, h: H, border: true }, { x: W, y: 0, w: 10, h: H, border: true }]);
      this.lines = m.lines;
      this.x = start.x; this.y = start.y; this.th = rad(start.deg || 0); this.startPose = { x: start.x, y: start.y };
      this.vL = 0; this.vR = 0; this.head = 90; this.headTarget = 90;
      this.lifted = !!opts.lifted; this.mismatch = opts.mismatch || 0; this.press = 0;
      this.crashes = 0; this.travelled = 0; this.turned = 0; this.ready = false; this.trail = [[this.x, this.y]]; this.lastPing = -1e9; this.headSeen = [];
    }
    recalc() { this.dirty = false; } // no circuit to solve here
    drv(p) { const q = this.pins[p]; if (q.mode !== 1) return 0; return q.duty !== null ? q.duty : q.level; }
    cmd(a, b) {
      const c = this.drv(a) - this.drv(b), m = Math.abs(c);
      return m < 0.3 ? 0 : Math.sign(c) * (m - 0.3) / 0.7 * VMAX;
    }
    hits(x, y) {
      for (const w of this.walls) {
        if (w.gone) continue;
        const nx = Math.max(w.x, Math.min(x, w.x + w.w)), ny = Math.max(w.y, Math.min(y, w.y + w.h));
        if ((nx - x) * (nx - x) + (ny - y) * (ny - y) < BODY_R * BODY_R) return w;
      }
      return null;
    }
    physics(h) {
      const tau = 0.08, k = 1 - Math.exp(-h / tau);
      const tL = this.cmd(PIN.L1, PIN.L2) * (1 - this.mismatch), tR = this.cmd(PIN.R1, PIN.R2);
      this.vL += (tL - this.vL) * k; this.vR += (tR - this.vR) * k;
      const dh = 600 * h;
      this.head += Math.max(-dh, Math.min(dh, this.headTarget - this.head));
      if (this.lifted) return;
      const v = (this.vL + this.vR) / 2, dth = (this.vL - this.vR) / TRACK * h;
      this.th += dth; this.turned += dth;
      const nx = this.x + v * Math.cos(this.th) * h, ny = this.y + v * Math.sin(this.th) * h, hit = this.hits(nx, ny);
      if (hit) {
        const was = this.hits(this.x, this.y);
        const fresh = this.simT - (this.lastCrash === undefined ? -1e9 : this.lastCrash) > 1000000; this.lastCrash = this.simT;
        if (fresh && Math.abs(v) > 1) { this.crashes++; this.warn('crash', 'bad', 'The robot crashed. On a real robot, this could stall the motors or damage the parts.'); }
        if (!was) return;
      }
      this.travelled += Math.abs(v) * h;
      this.x = nx; this.y = ny;
      const last = this.trail[this.trail.length - 1];
      if (Math.hypot(nx - last[0], ny - last[1]) > 1.5) { this.trail.push([nx, ny]); if (this.trail.length > 2500) this.trail.shift(); }
    }
    advance(t) {
      let cur = this.ct;
      while (cur < t) { const h = Math.min(t - cur, 5000); this.physics(h / 1e6); cur += h; }
      super.advance(t);
    }
    sonarPos() { return [this.x + SONAR_F * Math.cos(this.th), this.y + SONAR_F * Math.sin(this.th)]; }
    distance() {
      const [ox, oy] = this.sonarPos(), a = this.th - rad(this.head - 90);
      let best = Infinity;
      for (const off of [-7.5, 0, 7.5]) {
        const d = a + rad(off), dx = Math.cos(d), dy = Math.sin(d);
        for (const w of this.walls) { if (!w.gone) best = Math.min(best, rayRect(ox, oy, dx, dy, w)); }
      }
      return best;
    }
    eyePos(side) {
      const s = side === 'L' ? 1 : -1;
      return [this.x + EYE_F * Math.cos(this.th) + s * EYE_S * Math.sin(this.th), this.y + EYE_F * Math.sin(this.th) - s * EYE_S * Math.cos(this.th)];
    }
    onLine(p) {
      for (const l of this.lines) {
        for (let i = 1; i < l.pts.length; i++) {
          const [ax, ay] = l.pts[i - 1], [bx, by] = l.pts[i], dx = bx - ax, dy = by - ay;
          const u = Math.max(0, Math.min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / (dx * dx + dy * dy || 1)));
          if (Math.hypot(p[0] - ax - u * dx, p[1] - ay - u * dy) <= l.w / 2) return true;
        }
      }
      return false;
    }
    eye(side) { return this.onLine(this.eyePos(side)) ? 1 : 0; }
    builtin(name, a, line) {
      const vm = this.vm;
      if (name === 'digitalRead') {
        const pin = a[0]; this.checkPin(pin, line); this.advance(vm.time); vm.time += 5;
        if (pin === PIN.EYE_L) return this.eye('L');
        if (pin === PIN.EYE_R) return this.eye('R');
        const q = this.pins[pin];
        if (pin === PIN.BTN) {
          if (this.press) return 0;
          if (q.mode === 2) return 1;
          this.warn('btnfloat', 'warn', 'Use INPUT_PULLUP for the button on pin 2, or its reading will float.');
          return Math.random() < 0.5 ? 0 : 1;
        }
        return q.mode === 1 ? q.level : 0;
      }
      if (name === 'analogRead') {
        const pin = a[0] < 6 ? a[0] + 14 : a[0]; this.advance(vm.time); vm.time += 100;
        if (pin === PIN.EYE_L) return this.eye('L') ? 900 : 60;
        if (pin === PIN.EYE_R) return this.eye('R') ? 900 : 60;
        return 0;
      }
      if (name === 'pulseIn' && a[0] === PIN.ECHO) {
        this.advance(vm.time);
        const timeout = a[2] === undefined ? 1000000 : a[2];
        if (!this.ready) { this.warn('notrig', 'warn', 'Set TRIG HIGH for 10 microseconds before pulseIn, or the sensor never sends its sound.'); vm.time += Math.min(timeout, 1000000); return 0; }
        this.ready = false; this.lastPing = this.simT;
        const d = this.distance();
        if (d < 2 || d > 400) { vm.time += Math.min(timeout, 38000); return 0; }
        const dur = Math.round(d * 2 / 0.0343);
        if (dur > timeout) { vm.time += timeout; return 0; }
        vm.time += dur + 400; return dur;
      }
      if (name === 'digitalWrite' && a[0] === PIN.TRIG && this.pins[PIN.TRIG].level === 1 && !a[1]) this.ready = true;
      return super.builtin(name, a, line);
    }
    servo(obj, m, a, line) {
      const r = super.servo(obj, m, a, line);
      if (m === 'write' && obj.pin === PIN.HEAD) this.headTarget = Math.max(0, Math.min(180, a[0]));
      return r;
    }
    setTargetGap(gap) {
      const w = this.walls.find(x => x.id === 'target'); if (!w) return;
      w.x = Math.max(this.sonarPos()[0] + gap, this.x + BODY_R + 0.5); w.y = this.y - w.h / 2;
    }
    removeBox(flag) { const w = this.walls.find(x => x.id === 'box'); if (w) w.gone = flag; }
    moved() { return Math.hypot(this.x - this.startPose.x, this.y - this.startPose.y); }
    headingDeg() { return deg(this.th); }
  }

  // Which parts each exercise has fitted, and where it starts.
  const BASE = { x: 60, y: 105, deg: 0 };
  const SCEN = {
    5: { map: 'open', lifted: true, intro: 'The robot is on a box, so the wheels spin in the air.' }, 6: { map: 'open' }, 7: { map: 'open', start: { x: 110, y: 105, deg: 0 } }, 8: { map: 'open', start: { x: 160, y: 105, deg: 0 } }, 9: { map: 'open', start: { x: 40, y: 105, deg: 0 } }, 10: { map: 'open', start: { x: 120, y: 105, deg: 0 } }, 11: { map: 'open', start: { x: 110, y: 60, deg: 0 } }, 12: { map: 'open', start: { x: 120, y: 105, deg: 0 } },
    13: { map: 'open', fit: ['button'] }, 14: { map: 'open', fit: ['leds'] }, 15: { map: 'open', fit: ['buzzer'] },
    16: { map: 'target', fit: ['sonar'], gap: 50 }, 17: { map: 'wall', fit: ['sonar'] }, 18: { map: 'target', fit: ['sonar'], gap: 40 }, 19: { map: 'boxes', fit: ['sonar'], start: { x: 40, y: 105, deg: 0 }, intro: 'Let it run for a few minutes. It can eventually clip a box beside its narrow beam and get stuck, just as a real robot can. The next exercises help with that' }, 20: { map: 'open', fit: ['sonar', 'servo'], start: { x: 160, y: 105, deg: 0 } }, 21: { map: 'corner', fit: ['sonar', 'servo'] },
    22: { map: 'strip', fit: ['line'], start: { x: 100, y: 109, deg: 0 } }, 23: { map: 'oval', fit: ['line'], start: { x: 110, y: 150, deg: 0 } }, 24: { map: 'ring', fit: ['line'], start: { x: 160, y: 105, deg: 20 } }, 25: { map: 'mission', fit: ['line', 'sonar', 'leds', 'button'], start: { x: 110, y: 150, deg: 0 } },
  };

  const CHECKS = {
    5(h) { h.run(1000); h.say(h.s.vL > 10 && Math.abs(h.s.vR) < 1, 'The left wheel spins forward first.'); h.run(1500); h.say(h.s.vR > 10 && Math.abs(h.s.vL) < 1, 'Then the right wheel spins forward.'); },
    6(h) { h.run(2200); h.say(h.s.moved() > 50, 'The robot drives forward for about 2 seconds.'); h.run(1300); h.say(Math.abs(h.s.vL) + Math.abs(h.s.vR) < 2, 'Then it stops.'); },
    7(h) { h.run(1600); const d = h.s.moved(); h.say(d > 30, 'The robot drives forward.'); h.run(2400); h.say(h.s.moved() < 15, 'It reverses and finishes close to the start.'); },
    8(h) { h.run(1000); const a = Math.abs(h.s.headingDeg()); h.say(a > 60 && a < 120, `It turns about 90 degrees (this run: ${Math.round(a)}).`); h.say(h.s.moved() < 5, 'It turns on the spot.'); },
    9(h) { h.run(1900); const a = h.s.vL; h.run(2000); const b = h.s.vL; h.run(2000); const c = h.s.vL; h.say(a > 0 && b > a && c > b, 'The robot speeds up in three steps.'); },
    10(h) { h.run(1200); h.say(h.s.moved() > 15, 'forward() moves the robot forward.'); h.run(500); h.say(Math.abs(h.s.headingDeg()) > 40, 'spinLeft() turns the robot.'); h.run(3000); h.say(h.s.crashes === 0, 'It finishes the routine without crashing.'); },
    11(h) { h.run(8700); h.say(h.s.moved() < 30, `The robot finishes near its start (this run: ${Math.round(h.s.moved())} cm away).`); h.say(Math.abs(h.s.turned) > rad(280), 'It makes four turns.'); h.say(h.s.crashes === 0, 'It doesn\'t crash.'); },
    12(h) { h.run(5000); h.say(h.s.travelled > 30, 'The robot performs its moves.'); h.say(h.s.crashes === 0, 'It doesn\'t crash.'); },
    13(h) { h.run(1000); h.say(h.s.moved() < 1, 'Nothing moves until you press the button.'); h.s.press = 1; h.run(200); h.s.press = 0; h.run(1500); h.say(h.s.moved() > 20, 'After a press, the robot drives.'); h.run(1300); h.say(Math.abs(h.s.vL) < 2, 'Then it stops and waits.'); },
    14(h) { h.run(1000); h.say(h.s.pins[13].level === 1 && h.s.pins[12].level === 0 && h.s.vL > 5, 'Green is on while driving.'); h.run(1500); h.say(h.s.pins[12].level === 1 && h.s.pins[13].level === 0 && Math.abs(h.s.vL) < 2, 'Red is on while stopped.'); },
    15(h) { h.run(100); h.say(h.s.pins[4].level === 1 && h.s.moved() < 1, 'It beeps before it moves.'); h.run(1400); h.say(h.s.moved() > 10, 'Then it drives.'); },
    16(h) { h.run(800); h.say(/(4[7-9]|5[0-3])\.\d\d/.test(h.s.serial), 'With a target 50 cm away, the reading is about 50 cm.'); },
    17(h) { h.run(14000); const g = h.s.distance(); h.say(h.s.crashes === 0, 'The robot doesn\'t touch the wall.'); h.say(g > 8 && g < 28 && Math.abs(h.s.vL) < 2, `It stops about 20 cm away (this run: ${Math.round(g)} cm).`); },
    18(h) { h.run(5000); let g = h.s.distance(); h.say(g > 13 && g < 28, `It closes in to about 20 cm (this run: ${Math.round(g)} cm).`); h.s.setTargetGap(8); h.run(2500); g = h.s.distance(); h.say(g > 12, 'It backs away when the target gets too close.'); h.say(h.s.crashes === 0, 'It doesn\'t crash.'); },
    19(h) { h.run(30000); h.say(h.s.crashes === 0, `It drives for 30 seconds without crashing (this run: ${h.s.crashes} crashes).`); h.say(h.s.travelled > 200, `It keeps moving (this run: ${Math.round(h.s.travelled)} cm).`); },
    20(h) { h.run(3600); [150, 90, 30].forEach(a => h.say(h.seen.some(x => Math.abs(x - a) < 5), `The head turns to ${a} degrees.`)); },
    21(h) { h.run(14000); h.say(h.maxHeading > 40 && h.minHeading > -10, 'At the wall, it turns to the side with more room.'); h.say(h.s.crashes === 0, 'It doesn\'t crash.'); },
    22(h) { h.run(600); h.say(/Left: 1\s+Right: 0/.test(h.s.serial), 'With the left sensor over the tape, it reads Left: 1, Right: 0.'); },
    23(h) { h.run(40000, true); h.say(h.lap, 'The robot completes a full lap.'); h.say(h.maxOff < 16, `It stays close to the line (furthest: ${Math.round(h.maxOff)} cm).`); h.say(h.s.crashes === 0, 'It doesn\'t crash.'); },
    24(h) { h.run(60000); h.say(h.maxRing < 92, 'The robot stays inside the ring for a minute.'); h.say(h.s.travelled > 150, `It keeps moving (this run: ${Math.round(h.s.travelled)} cm).`); },
    25(h) {
      h.run(1000); h.say(h.s.moved() < 1 && h.s.pins[12].level === 1, 'It waits, showing red, until you press the button.');
      h.s.press = 1; h.run(200); h.s.press = 0; h.run(35000);
      h.say(Math.abs(h.s.vL) + Math.abs(h.s.vR) < 3 && h.s.pins[12].level === 1 && h.s.crashes === 0, 'It follows the line, then stops at the box with red showing.');
      const d = h.s.travelled; h.s.removeBox(true); h.run(4000);
      h.say(h.s.travelled > d + 20 && h.s.pins[13].level === 1, 'When the box is removed, it carries on with green showing.');
    },
  };

  function makeSim(n, code, opts) {
    const sc = SCEN[n] || { map: 'open' }, st = sc.start || BASE;
    const sim = new RobotSim((opts && opts.map) || sc.map, (opts && opts.start) || st, code, { lifted: sc.lifted && !(opts && opts.map), mismatch: opts && opts.mismatch });
    if (sc.gap && !(opts && opts.map && opts.map !== sc.map)) sim.setTargetGap(sc.gap);
    return sim;
  }

  function runRobotCheck(n, code, opts) {
    const s = makeSim(n, code, opts), results = [];
    if (s.err) return { results: [{ ok: false, say: `Line ${s.err.line}: ${s.err.msg}` }], compileError: s.err, warns: [] };
    const h = {
      s, seen: [], maxHeading: 0, minHeading: 0, maxRing: 0, maxOff: 0, lap: false, cp: 0,
      say(ok, say) { results.push({ ok: !!ok, say }); },
      run(ms, track) {
        for (let t = 0; t < ms; t += 10) {
          s.step(10);
          this.seen.push(s.head);
          const a = s.headingDeg(); this.maxHeading = Math.max(this.maxHeading, a); this.minHeading = Math.min(this.minHeading, a);
          const m = MAPS[s.mapId];
          if (m.ring) this.maxRing = Math.max(this.maxRing, Math.hypot(s.x - m.ring.x, s.y - m.ring.y));
          if (track) {
            let best = Infinity; const pts = m.lines[0].pts;
            for (let i = 0; i < pts.length; i += 2) best = Math.min(best, Math.hypot(s.x - pts[i][0], s.y - pts[i][1]));
            this.maxOff = Math.max(this.maxOff, best);
            const cps = [[275, 105], [160, 60], [45, 105], [110, 150]], c = cps[this.cp];
            if (c && Math.hypot(s.x - c[0], s.y - c[1]) < 18) { this.cp++; if (this.cp === cps.length) this.lap = true; }
          }
          if (s.err) return;
        }
      },
    };
    (CHECKS[n] || (() => {})).call(null, h);
    if (s.err) results.push({ ok: false, say: `Line ${s.err.line}: ${s.err.msg}` });
    return { results, warns: Array.from(s.warns.values()) };
  }

  root.ERobot = { RobotSim, MAPS, SCEN, makeSim, runRobotCheck, W, H, BODY_R, EYE_F, EYE_S, SONAR_F, PIN };
})(typeof window !== 'undefined' ? window : globalThis);
