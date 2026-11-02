/* Live Tools: calculators that update as you type. The sums sit apart from the screen code, so they can be tested. */
(function (root) {
  'use strict';

  // ---------- colour codes ----------
  const NAMES = ['black', 'brown', 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'grey', 'white'];
  const LABEL = n => n.charAt(0).toUpperCase() + n.slice(1);
  const MULT = { silver: -2, gold: -1 };
  NAMES.forEach((n, i) => { MULT[n] = i; });
  const TOL = { brown: 1, red: 2, green: 0.5, blue: 0.25, violet: 0.1, grey: 0.05, gold: 5, silver: 10 };

  // ---------- number formats ----------
  const sig = (x, n = 3) => String(+Number(x).toPrecision(n));
  const PREFIX = [[1e9, 'G'], [1e6, 'M'], [1e3, 'k'], [1, ''], [1e-3, 'm'], [1e-6, 'µ'], [1e-9, 'n'], [1e-12, 'p']];
  function si(x, unit, n = 3) {
    if (x === 0) return `0 ${unit}`;
    // "159 mHz" and "70 mΩ" are too easy to misread as MHz and MΩ.
    if ((unit === 'Ω' || unit === 'Hz') && Math.abs(x) < 1) return `${sig(x, n)} ${unit}`;
    const a = Math.abs(x) * (1 + 1e-12), p = PREFIX.find(q => a >= q[0]) || PREFIX[PREFIX.length - 1];
    return `${sig(x / p[0], n)} ${p[1]}${unit}`;
  }
  function span(raw) {
    const sec = +raw.toPrecision(6), say = (v, w) => `${sig(v)} ${w}${+sig(v) === 1 ? '' : 's'}`;
    if (sec < 1) return si(sec, 's');
    if (sec < 90) return say(sec, 'second');
    if (sec < 5400) return say(sec / 60, 'minute');
    if (sec < 172800) return say(sec / 3600, 'hour');
    return say(sec / 86400, 'day');
  }

  // ---------- standard resistor values ----------
  const E12 = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2];
  function stdUp(x) {
    let d = Math.pow(10, Math.floor(Math.log10(x)));
    for (let k = 0; k < 2; k++, d *= 10) for (const m of E12) if (m * d >= x * (1 - 1e-9)) return +(m * d).toPrecision(3);
    return x;
  }
  function stdDown(x) {
    let d = Math.pow(10, Math.floor(Math.log10(x)));
    for (let k = 0; k < 2; k++, d /= 10) for (let i = E12.length - 1; i >= 0; i--) if (E12[i] * d <= x * (1 + 1e-9)) return +(E12[i] * d).toPrecision(3);
    return x;
  }

  // Reads 220, 4.7k, 4k7, 1M, 1M5 or 220R. Returns ohms, or null.
  function parseOhm(text) {
    const s = String(text).trim().replace(/\s*(ohms?|Ω)$/i, '').replace(/\s+/g, '');
    let m = /^(\d+)([rRkKmMgG])(\d+)$/.exec(s);
    if (m) { const v = parseFloat(`${m[1]}.${m[3]}`) * ({ r: 1, k: 1e3, m: 1e6, g: 1e9 })[m[2].toLowerCase()]; return v > 0 ? v : null; }
    m = /^(\d*\.?\d+)([rRkKmMgG]?)$/.exec(s);
    if (!m) return null;
    const v = parseFloat(m[1]) * ({ '': 1, r: 1, k: 1e3, m: 1e6, g: 1e9 })[m[2].toLowerCase()];
    return v > 0 ? v : null;
  }

  function decodeResistor(b) {
    const digits = b.slice(0, b.length - 2).map(n => NAMES.indexOf(n)), mult = b[b.length - 2], tol = TOL[b[b.length - 1]];
    const value = digits.reduce((a, d) => a * 10 + d, 0), ohm = +(value * Math.pow(10, MULT[mult])).toPrecision(6);
    return { ohm, tol, min: ohm * (1 - tol / 100), max: ohm * (1 + tol / 100), backwards: digits[0] === 0 };
  }
  // The bands for a value. `exact` is false when this many bands can only get close.
  function encodeResistor(ohm, count, tolName) {
    const n = count - 2;
    let e = Math.floor(Math.log10(ohm) + 1e-12) - n + 1, mant = Math.round(ohm / Math.pow(10, e));
    if (mant >= Math.pow(10, n)) { mant = Math.round(mant / 10); e += 1; }
    if (e < -2 || e > 9) return null;
    const digits = String(mant).padStart(n, '0').split('').map(d => NAMES[+d]), mult = e === -2 ? 'silver' : e === -1 ? 'gold' : NAMES[e];
    const made = mant * Math.pow(10, e);
    return { bands: [...digits, mult, tolName], made: +made.toPrecision(6), exact: Math.abs(made - ohm) / ohm < 1e-6 };
  }

  // ---------- diodes ----------
  const DIODES = {
    '1N34': 'Germanium signal diode', '1N914': 'Fast signal diode, about 100 V', '1N4148': 'Fast signal diode, about 100 V and 200 mA',
    '1N4001': 'Power diode, 50 V, 1 A', '1N4002': 'Power diode, 100 V, 1 A', '1N4003': 'Power diode, 200 V, 1 A', '1N4004': 'Power diode, 400 V, 1 A', '1N4005': 'Power diode, 600 V, 1 A', '1N4006': 'Power diode, 800 V, 1 A', '1N4007': 'Power diode, 1000 V, 1 A',
    '1N4728': 'Zener diode, 3.3 V', '1N4733': 'Zener diode, 5.1 V', '1N4742': 'Zener diode, 12 V',
    '1N5400': 'Power diode, 50 V, 3 A', '1N5408': 'Power diode, 1000 V, 3 A',
    '1N5817': 'Schottky diode, 20 V, 1 A', '1N5818': 'Schottky diode, 30 V, 1 A', '1N5819': 'Schottky diode, 40 V, 1 A',
  };
  function decodeDiode(bands) {
    const digits = bands.filter(Boolean).map(n => NAMES.indexOf(n)).join(''), part = '1N' + digits;
    return { part, known: DIODES[part] || null };
  }
  function encodeDiode(text) {
    const m = /^\s*1?n?\s*(\d{1,4})[a-z]*\s*$/i.exec(String(text));
    if (!m) return null;
    return m[1].split('').map(d => NAMES[+d]);
  }

  // ---------- capacitor codes ----------
  const CAP_TOL = { f: '±1%', g: '±2%', j: '±5%', k: '±10%', m: '±20%', z: '+80% / −20%' };
  function parseCap(text) {
    const s = String(text).trim().toLowerCase().replace(/µ/g, 'u');
    const PF = { p: 1, n: 1e3, u: 1e6 };
    let m = /^(\d+)([pnu])(\d*)$/.exec(s);
    if (m) return { pf: parseFloat(`${m[1]}.${m[3] || 0}`) * PF[m[2]], tol: null };
    m = /^(\d*\.\d+|\d+)\s*([pnu])f?$/.exec(s);
    if (m) return { pf: parseFloat(m[1]) * PF[m[2]], tol: null };
    m = /^(\d)(\d)(\d)\s*([fgjkmz])?$/.exec(s);
    if (m) {
      const third = +m[3], mult = third === 8 ? 0.01 : third === 9 ? 0.1 : Math.pow(10, third);
      return { pf: +((+m[1] * 10 + +m[2]) * mult).toPrecision(6), tol: m[4] ? CAP_TOL[m[4]] : null };
    }
    m = /^(\d{1,2})\s*([fgjkmz])?$/.exec(s);
    if (m && +m[1] > 0) return { pf: +m[1], tol: m[2] ? CAP_TOL[m[2]] : null };
    return null;
  }
  function encodeCap(pf) {
    if (pf < 10 || pf >= 1e10) return null;
    const e = Math.floor(Math.log10(pf) + 1e-12) - 1, mant = Math.round(pf / Math.pow(10, e));
    return mant >= 100 ? null : `${mant}${e}`;
  }

  const num = x => typeof x === 'number' && isFinite(x);
  const need = (v, keys) => keys.every(k => num(v[k]) && v[k] > 0);
  const ASK = { err: 'Type a number above 0 in each box.' };

  // ---------- one function per tool: values in, results out ----------
  const CALC = {
    led(v) {
      if (!need(v, ['v', 'vf', 'ma', 'n'])) return ASK;
      const drop = v.n * v.vf;
      if (v.v <= drop) return { err: `${sig(v.n)} LED${v.n > 1 ? 's' : ''} in a row need${v.n > 1 ? '' : 's'} more than ${sig(drop)} V. Raise the supply, or use fewer LEDs.` };
      const left = v.v - drop, exact = left / (v.ma / 1000), up = stdUp(exact), amps = left / up, watts = amps * amps * up;
      const warn = [];
      if (v.ma > 20) warn.push('Most small LEDs and Arduino pins should stay at 20 mA or less.');
      if (watts > 0.25) warn.push(`This resistor would heat up by ${si(watts, 'W')}, more than a common 1/4 W part can take. Use a bigger one.`);
      if (left < 0.5) warn.push('Very little voltage is left for the resistor, so brightness will change a lot with the supply.');
      const enc = encodeResistor(up, 4, 'gold');
      return { big: ['Use this resistor', si(up, 'Ω')], rows: [['Exact sum', si(exact, 'Ω')], ['Voltage across the resistor', `${sig(left)} V`], ['Current with this resistor', si(amps, 'A')], ['Heat in the resistor', si(watts, 'W')], ['Its colour bands', enc.bands.map(LABEL).join(', ')]], warn, up, bands: enc.bands, ok: warn.length ? null : 'Good: this is the next standard value above the exact sum, so the current stays a little under your target.' };
    },
    ohm(v) {
      const f = v.find, keys = ['v', 'i', 'r'].filter(k => k !== f);
      if (!need(v, keys)) return ASK;
      let V = v.v, A = v.i / 1000, R = v.r;
      if (f === 'v') V = A * R; if (f === 'i') A = V / R; if (f === 'r') R = V / A;
      const P = V * A, warn = [];
      if (P > 0.25) warn.push(`That's ${si(P, 'W')} of heat. A common 1/4 W resistor would overheat.`);
      if (A > 0.02) warn.push('That current is more than an Arduino pin should supply directly (20 mA is a safe limit).');
      const big = { v: ['Voltage', `${sig(V)} V`], i: ['Current', si(A, 'A')], r: ['Resistance', si(R, 'Ω')] }[f];
      return { big, rows: [['Voltage', `${sig(V)} V`], ['Current', si(A, 'A')], ['Resistance', si(R, 'Ω')], ['Power (heat)', si(P, 'W')]], warn, V, A, R, P };
    },
    divider(v) {
      if (!need(v, ['vin', 'r1', 'r2'])) return ASK;
      const out = v.vin * v.r2 / (v.r1 + v.r2), A = v.vin / (v.r1 + v.r2), src = v.r1 * v.r2 / (v.r1 + v.r2), warn = [];
      if (out > 5) warn.push('That is above 5 V. It could damage an Arduino pin. Make R1 bigger or R2 smaller.');
      if (src > 10000) warn.push(`An Arduino reads best when this source is 10 kΩ or less. Yours is about ${si(src, 'Ω')}, so readings may drift. Use smaller resistors.`);
      if (A > 0.02) warn.push('This divider wastes a lot of current. Use bigger resistors.');
      const rows = [['Current through both', si(A, 'A')], ['Fraction of the input', `${sig(out / v.vin * 100)}%`]];
      if (out <= 5) rows.push(['analogRead on a 5 V Arduino', String(Math.round(out / 5 * 1023))]);
      return { big: ['Voltage out', `${sig(out)} V`], rows, warn, out };
    },
    combine(v) {
      const parts = String(v.list || '').split(/[,;]+/).map(s => s.trim()).filter(Boolean), vals = parts.map(parseOhm);
      if (!vals.length) return { err: 'Type two or more values, such as 220, 330, 1k.' };
      const bad = parts.find((p, i) => vals[i] === null);
      if (bad) return { err: `“${bad}” isn't a resistor value. Try forms such as 220, 4.7k or 1M.` };
      const series = vals.reduce((a, b) => a + b, 0), parallel = 1 / vals.reduce((a, b) => a + 1 / b, 0);
      return { big: ['In a row (series)', si(series, 'Ω', 4)], rows: [['Side by side (parallel)', si(parallel, 'Ω', 4)], ['How many resistors', String(vals.length)]], series, parallel };
    },
    capcode(v) {
      const c = parseCap(v.code);
      if (!c) return { err: 'Type a code such as 104, 473J, 22, 4n7 or 100n.' };
      const code = encodeCap(c.pf), F = c.pf * 1e-12;
      const rows = [['In picofarads', `${sig(c.pf, 4)} pF`], ['In nanofarads', `${sig(c.pf / 1e3, 4)} nF`], ['In microfarads', `${sig(c.pf / 1e6, 4)} µF`]];
      if (code) rows.push(['Three-digit code', code]);
      if (c.tol) rows.push(['Tolerance', c.tol]);
      return { big: ['This capacitor is', si(F, 'F', 4)], rows, pf: c.pf };
    },
    rc(v) {
      if (!need(v, ['r', 'c'])) return ASK;
      const tau = v.r * v.c, fc = 1 / (2 * Math.PI * tau);
      return { big: ['One time constant', span(tau)], rows: [['Charged to 63% after', span(tau)], ['Almost full (99%) after', span(5 * tau)], ['Filter cut-off frequency', si(fc, 'Hz')]], tau, fc, curve: true };
    },
    base(v) {
      const parts = { tip120: { vbe: 2.5, gain: 250, max: 5000, name: 'TIP120' }, bc547: { vbe: 0.7, gain: 10, max: 100, name: 'BC547' }, p2222: { vbe: 0.7, gain: 10, max: 600, name: 'PN2222' } }, p = parts[v.part] || parts.tip120;
      if (!need(v, ['vc', 'ma'])) return ASK;
      if (v.vc <= p.vbe) return { err: `The ${p.name}'s base needs more than ${p.vbe} V to turn on.` };
      const ib = v.ma / 1000 / p.gain, exact = (v.vc - p.vbe) / ib, down = stdDown(exact), real = (v.vc - p.vbe) / down, warn = [];
      if (v.ma > p.max) warn.push(`${sig(v.ma)} mA is above the ${p.name}'s ${p.max} mA limit. Choose a bigger transistor.`);
      if (real > 0.02) warn.push(`The pin would have to supply ${si(real, 'A')}, above the 20 mA limit. Use a transistor with more gain.`);
      return { big: ['Base resistor', si(down, 'Ω')], rows: [['Base current needed', si(ib, 'A')], ['Exact sum', si(exact, 'Ω')], ['Current from the pin', si(real, 'A')]], warn, down, ib };
    },
    adc(v) {
      if (!num(v.read) || !num(v.pwm) || v.read < 0 || v.pwm < 0) return { err: 'Type numbers of 0 or more.' };
      const warn = [];
      if (v.read > 1023) warn.push('analogRead only gives 0 to 1023.');
      if (v.pwm > 255) warn.push('analogWrite only takes 0 to 255.');
      const read = Math.min(v.read, 1023), pwm = Math.min(v.pwm, 255), volts = read / 1023 * v.ref, duty = pwm / 255, avg = duty * v.ref;
      return { big: [`analogRead(${sig(read, 4)}) means`, `${sig(volts)} V`], rows: [['analogWrite on-time', `${sig(duty * 100)}%`], ['Average output', `${sig(avg)} V`], ['Times per second', 'About 490 (976 on pins 5, 6)']], warn, volts, duty, avg };
    },
    sonar(v) {
      if (!need(v, ['us']) || !num(v.temp)) return ASK;
      const speed = 331.3 + 0.606 * v.temp, cm = v.us * speed / 10000 / 2, warn = [];
      if (cm < 2 || cm > 400) warn.push('An HC-SR04 can only measure from about 2 cm to 400 cm, so this reading may not be real.');
      return { big: ['Distance', `${sig(cm)} cm`], rows: [['Speed of sound', `${sig(speed, 4)} m/s`], ['Sound travelled there and back', `${sig(cm * 2)} cm`], ['Sum to use in code', `duration * ${sig(speed / 10000, 3)} / 2`]], warn, cm, speed };
    },
    battery(v) {
      if (!need(v, ['mah', 'ma'])) return ASK;
      const sec = v.mah * 0.7 / v.ma * 3600, warn = [];
      if (v.ma > v.mah / 2) warn.push('This is a heavy draw for this battery. It will run out sooner than this, and may feel warm.');
      return { big: ['Should last about', span(sec)], rows: [['Label capacity', `${sig(v.mah, 4)} mAh`], ['Usable (about 70%)', `${sig(v.mah * 0.7, 4)} mAh`], ['Your circuit draws', `${sig(v.ma, 4)} mA`]], warn, hours: sec / 3600 };
    },
    robot(v) {
      if (!need(v, ['mm', 'rpm', 'track', 'dist'])) return ASK;
      const around = Math.PI * v.mm / 10, speed = v.rpm / 60 * around, turn = Math.PI * v.track / 4, go = v.dist / speed, spin = turn / speed;
      return { big: ['Top speed', `${sig(speed)} cm/s`], rows: [['One wheel turn travels', `${sig(around)} cm`], [`Time to go ${sig(v.dist)} cm`, `${Math.round(go * 1000)} ms`], ['Time for a 90° turn on the spot', `${Math.round(spin * 1000)} ms`]], warn: [], speed, go, spin };
    },
    regulator(v) {
      if (!need(v, ['vin', 'vout', 'ma'])) return ASK;
      if (v.vin <= v.vout) return { err: 'The input must be higher than the output.' };
      const drop = v.vin - v.vout, W = drop * v.ma / 1000, warn = [], eff = v.vout / v.vin;
      if (drop < 2) warn.push('A 7805-type regulator needs about 2 V extra at its input. The output may sag.');
      if (v.vin > 25) warn.push('That is above the 25 V recommended for an LM7805.');
      if (v.ma > 1500) warn.push('That is above the LM7805\'s 1.5 A limit.');
      if (W > 1) warn.push(`${si(W, 'W')} is too much heat for a bare regulator. Fit a heat sink, lower the input voltage, or use a switching regulator.`);
      return { big: ['Heat to get rid of', si(W, 'W')], rows: [['Voltage dropped', `${sig(drop)} V`], ['Power reaching your circuit', si(v.vout * v.ma / 1000, 'W')], ['Efficiency', `${sig(eff * 100)}%`]], warn, W, eff, ok: W <= 1 && !warn.length ? 'A bare regulator can handle this, though it may still feel warm.' : null };
    },
  };

  root.EToolsCalc = { CALC, decodeResistor, encodeResistor, decodeDiode, encodeDiode, parseOhm, parseCap, encodeCap, stdUp, stdDown, si, sig, span };
  if (typeof document === 'undefined') return;

  // ---------- drawings, redrawn on every change ----------
  const swatch = n => `var(--c-${n})`;
  function resistorSvg(bands) {
    const n = bands.length, x0 = 120, gap = 26, marks = bands.map((b, i) => {
      const x = i === n - 1 ? 244 : x0 + i * gap;
      return `<rect x="${x}" y="17" width="13" height="46" fill="${swatch(b)}"/>`;
    }).join('');
    return `<svg class="tool-art" viewBox="0 0 400 80" role="img" aria-label="Resistor with bands: ${bands.join(', ')}"><path d="M0 40H90M310 40H400" stroke="var(--silver-d)" stroke-width="5"/><rect x="90" y="17" width="220" height="46" rx="20" fill="var(--tan)" stroke="var(--tan-d)" stroke-width="2"/>${marks}</svg>`;
  }
  function diodeSvg(bands) {
    const list = bands.filter(Boolean), marks = list.map((b, i) => {
      const x = i === 0 ? 112 : 132 + i * 24, w = i === 0 ? 28 : 13;
      return `<rect x="${x}" y="22" width="${w}" height="36" fill="${swatch(b)}"/>`;
    }).join('');
    return `<svg class="tool-art" viewBox="0 0 400 96" role="img" aria-label="Glass diode with bands: ${list.join(', ')}. The wide band marks the cathode."><path d="M0 40H100M300 40H400" stroke="var(--silver-d)" stroke-width="5"/><rect x="100" y="22" width="200" height="36" rx="10" fill="var(--c-glass)" stroke="var(--silver-d)" stroke-width="2"/>${marks}<text x="50" y="88" text-anchor="middle" font-size="13" fill="var(--text)" font-weight="700">Cathode (−)</text><text x="350" y="88" text-anchor="middle" font-size="13" fill="var(--text)" font-weight="700">Anode (+)</text></svg>`;
  }
  function rcSvg(res) {
    const pts = []; for (let i = 0; i <= 50; i++) { const t = i / 10; pts.push(`${(44 + t * 66).toFixed(1)},${(130 - (1 - Math.exp(-t)) * 110).toFixed(1)}`); }
    const label = t => (t === 0 ? '0' : t === 1 || t === 5 ? span(t * res.tau) : '');
    const ticks = [0, 1, 2, 3, 4, 5].map(t => `<path d="M${44 + t * 66} 130v5" stroke="var(--soft)"/><text x="${44 + t * 66}" y="150" text-anchor="${t === 5 ? 'end' : 'middle'}" font-size="12" fill="var(--soft)">${label(t)}</text>`).join('');
    const y63 = 130 - 0.632 * 110;
    return `<svg class="tool-art" viewBox="0 0 400 158" role="img" aria-label="Charging curve. It reaches 63 percent after ${span(res.tau)}, and almost full after ${span(5 * res.tau)}."><path d="M44 20V130H374" fill="none" stroke="var(--soft)"/><path d="M44 ${y63}H110V130" fill="none" stroke="var(--border)" stroke-dasharray="4 4"/><text x="38" y="${y63 + 4}" text-anchor="end" font-size="12" fill="var(--soft)">63%</text><text x="38" y="24" text-anchor="end" font-size="12" fill="var(--soft)">100%</text><polyline points="${pts.join(' ')}" fill="none" stroke="var(--accent)" stroke-width="3"/>${ticks}</svg>`;
  }
  function pwmSvg(res) {
    const d = res.duty, cycle = 80; let p = 'M20 70';
    for (let i = 0; i < 4; i++) { const x = 20 + i * cycle; p += ` L${x} ${d > 0 ? 20 : 70} L${x + d * cycle} ${d > 0 ? 20 : 70} L${x + d * cycle} 70 L${x + cycle} 70`; }
    const ya = 70 - d * 50;
    return `<svg class="tool-art" viewBox="0 0 360 92" role="img" aria-label="Pin signal, on for ${sig(d * 100)} percent of the time."><path d="M20 70H340" stroke="var(--border)"/><path d="${p}" fill="none" stroke="var(--accent)" stroke-width="3"/><path d="M20 ${ya}H340" stroke="var(--warn)" stroke-dasharray="5 4" stroke-width="2"/><text x="340" y="88" text-anchor="end" font-size="12" fill="var(--warn)">Dashed line: the average</text></svg>`;
  }

  function outHtml(res, art) {
    if (res.err) return `<div class="msg">${res.err}</div>`;
    const rows = (res.rows || []).map(r => `<tr><th scope="row">${r[0]}</th><td>${r[1]}</td></tr>`).join('');
    return (res.big ? `<div class="tool-big"><span>${res.big[0]}</span><b>${res.big[1]}</b></div>` : '') + (art || '') + (rows ? `<div class="tw"><table class="tool-rows">${rows}</table></div>` : '') + (res.warn || []).map(w => `<div class="msg">${w}</div>`).join('') + (res.ok ? `<div class="msg good">${res.ok}</div>` : '');
  }

  // ---------- ordinary calculators ----------
  function wire(form) {
    const name = form.getAttribute('data-tool'), out = form.parentElement.querySelector('.tool-out');
    const read = () => {
      const v = {};
      form.querySelectorAll('[data-f]').forEach(i => {
        const k = i.getAttribute('data-f'), u = form.querySelector(`[data-u="${k}"]`);
        v[k] = i.value.trim() === '' ? NaN : parseFloat(i.value) * (u ? parseFloat(u.value) : 1);
      });
      form.querySelectorAll('[data-t]').forEach(i => { v[i.getAttribute('data-t')] = i.value; });
      form.querySelectorAll('[data-c]').forEach(i => { const raw = i.value; v[i.getAttribute('data-c')] = raw !== '' && !isNaN(+raw) ? +raw : raw; });
      return v;
    };
    const update = () => {
      form.querySelectorAll('[data-hide-if]').forEach(el => { const [k, val] = el.getAttribute('data-hide-if').split('='), sel = form.querySelector(`[data-c="${k}"]`); el.hidden = sel.value === val; });
      const res = CALC[name](read());
      let art = '';
      if (!res.err) {
        if (res.bands) art = resistorSvg(res.bands);
        if (res.curve) art = rcSvg(res);
        if (name === 'adc') art = pwmSvg(res);
      }
      out.innerHTML = outHtml(res, art);
    };
    form.addEventListener('submit', e => e.preventDefault());
    form.addEventListener('input', e => {
      const t = e.target;
      if (t.hasAttribute('data-s')) { form.querySelector(`[data-f="${t.getAttribute('data-s')}"]`).value = t.value; }
      if (t.hasAttribute('data-f')) {
        const k = t.getAttribute('data-f'), s = form.querySelector(`[data-s="${k}"]`); if (s) s.value = t.value;
        const filler = form.querySelector(`[data-fills="${k}"]`);
        if (filler) { const hit = Array.from(filler.options).find(o => o.value !== '' && +o.value === +t.value); filler.value = hit ? hit.value : ''; }
      }
      if (t.hasAttribute('data-fills') && t.value !== '') { const f = form.querySelector(`[data-f="${t.getAttribute('data-fills')}"]`); f.value = t.value; }
      update();
    });
    update();
  }

  // ---------- colour-chip pickers ----------
  function chipColumn(group, legend, list, value, sub) {
    return `<fieldset class="band"><legend>${legend}</legend>` + list.map(n => `<label class="chip"><input type="radio" name="${group}" value="${n}"${n === value ? ' checked' : ''}><i style="background:${n ? swatch(n) : 'transparent'}"></i><span>${n ? LABEL(n) : 'None'}${sub && n ? `<small>${sub(n)}</small>` : ''}</span></label>`).join('') + '</fieldset>';
  }
  const pick = (box, name) => { const c = box.querySelector(`input[name="${name}"]:checked`); return c ? c.value : ''; };

  function wireResistor(box) {
    const grid = box.querySelector('.bands'), countSel = box.querySelector('[data-count]'), typed = box.querySelector('[data-typed]'), out = box.parentElement.querySelector('.tool-out'), note = box.querySelector('[data-typed-note]');
    const DIGITS = NAMES, MULTS = [...NAMES, 'gold', 'silver'], TOLS = Object.keys(TOL);
    const multSub = n => { const e = MULT[n]; return e >= 0 ? `×${si(Math.pow(10, e), '').trim()}` : `×${e === -1 ? '0.1' : '0.01'}`; };
    function build(bands) {
      const n = bands.length;
      grid.style.setProperty('--n', n);
      grid.innerHTML = bands.map((b, i) => {
        if (i === n - 1) return chipColumn('rb' + i, 'Tolerance', TOLS, b, c => `±${TOL[c]}%`);
        if (i === n - 2) return chipColumn('rb' + i, 'Multiply', MULTS, b, multSub);
        return chipColumn('rb' + i, `Digit ${i + 1}`, DIGITS, b, c => NAMES.indexOf(c));
      }).join('');
    }
    function paint() {
      const n = +countSel.value, bands = []; for (let i = 0; i < n; i++) bands.push(pick(grid, 'rb' + i));
      const r = decodeResistor(bands), warn = [];
      if (r.backwards) warn.push('The first band is almost never black. You may be reading this resistor from the wrong end. Start from the end furthest from the gold or silver band.');
      if (r.ohm === 0) { out.innerHTML = `<div class="msg">All the digit bands are black, which gives 0 Ω. Choose other colours.</div>`; return bands; }
      out.innerHTML = outHtml({ big: ['This resistor is', `${si(r.ohm, 'Ω', 4)} ±${r.tol}%`], rows: [['Could really be as low as', si(r.min, 'Ω', 4)], ['Could really be as high as', si(r.max, 'Ω', 4)], ['Colours', bands.map(LABEL).join(', ')]], warn }, resistorSvg(bands));
      return bands;
    }
    grid.addEventListener('change', () => { const b = paint(); const r = decodeResistor(b); typed.value = r.ohm >= 1 ? si(r.ohm, '', 4).replace(/\s+/g, '') : r.ohm ? String(r.ohm) : ''; note.textContent = ''; });
    countSel.addEventListener('change', () => { const n = +countSel.value, v = parseOhm(typed.value) || 220, e = encodeResistor(v, n, n === 4 ? 'gold' : 'brown'); build(e.bands); paint(); });
    typed.addEventListener('input', () => {
      const v = parseOhm(typed.value), n = +countSel.value;
      if (v === null) { note.textContent = typed.value.trim() ? 'Try a form such as 220, 4.7k or 1M.' : ''; return; }
      const tol = pick(grid, 'rb' + (n - 1)) || 'gold', e = encodeResistor(v, n, tol);
      if (!e) { note.textContent = 'That value is outside what colour bands can show.'; return; }
      note.textContent = e.exact ? '' : `${n} bands can't show that exactly. This is the closest: ${si(e.made, 'Ω', 4)}.`;
      build(e.bands); paint();
    });
    typed.value = '220';
    build(encodeResistor(220, 4, 'gold').bands); paint();
  }

  function wireDiode(box) {
    const grid = box.querySelector('.bands'), typed = box.querySelector('[data-typed]'), out = box.parentElement.querySelector('.tool-out'), note = box.querySelector('[data-typed-note]');
    function build(bands) {
      grid.style.setProperty('--n', 4);
      grid.innerHTML = [0, 1, 2, 3].map(i => chipColumn('db' + i, i === 0 ? 'Wide band' : `Band ${i + 1}`, i < 2 ? NAMES : ['', ...NAMES], bands[i] || '', c => NAMES.indexOf(c))).join('');
    }
    function paint() {
      const bands = [0, 1, 2, 3].map(i => pick(grid, 'db' + i)), r = decodeDiode(bands), warn = [];
      if (r.part.length > 2 && r.part[2] === '0') warn.push('Part numbers don\'t start with 0, so the first band is probably a different colour. Check it in good light.');
      if (!bands[2] && bands[3]) warn.push('Band 3 is empty but band 4 isn\'t, so the digits may be out of order.');
      out.innerHTML = outHtml({ big: ['This diode is', r.part], rows: [['What it is', r.known || 'Not in this short list. Look up the number.'], ['Colours', bands.filter(Boolean).map(LABEL).join(', ')]], warn }, diodeSvg(bands));
      return r;
    }
    grid.addEventListener('change', () => { const r = paint(); typed.value = r.part; note.textContent = ''; });
    typed.addEventListener('input', () => {
      const b = encodeDiode(typed.value);
      if (!b || b.length < 2) { note.textContent = typed.value.trim() ? 'Try a form such as 1N4148.' : ''; return; }
      note.textContent = ''; build(b); paint();
    });
    typed.value = '1N4148';
    build(encodeDiode('1N4148')); paint();
  }

  root.ETools = {
    init() {
      document.querySelectorAll('form[data-tool]').forEach(wire);
      document.querySelectorAll('[data-chips="resistor"]').forEach(wireResistor);
      document.querySelectorAll('[data-chips="diode"]').forEach(wireDiode);
    },
  };
})(typeof window !== 'undefined' ? window : globalThis);
