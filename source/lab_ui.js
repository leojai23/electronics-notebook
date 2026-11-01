/* Electronics lab workspace: draws the bench, handles editing, and runs the simulation. */
(function () {
  'use strict';
  const { Sim, runCheck, PART_TYPES, netKey } = window.ELab, EX = window.ELAB_EXAMPLES;
  const $ = id => document.getElementById(id);
  const W = 716, H = 700, BX = 40, BY = 120, AX = 170, AY = 456, AH = 210;
  const rowsTop = 'abcde', rowsBot = 'fghij';
  const colX = c => BX + 28 + (c - 1) * 20;
  const TOP_PINS = ['SCL', 'SDA', 'AREF', 'GND', 'D13', 'D12', 'D11', 'D10', 'D9', 'D8', '', 'D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1', 'D0'];
  const BOT_PINS = ['IOREF', 'RESET', '3V3', '5V', 'GND2', 'GND3', 'VIN', '', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5'];
  const pinPos = {};
  TOP_PINS.forEach((n, i) => { if (n) pinPos[n] = { x: AX + 92 + i * 15, y: AY + 14 }; });
  BOT_PINS.forEach((n, i) => { if (n) pinPos[n] = { x: AX + 164 + i * 15, y: AY + AH - 14 }; });
  const DECOR = new Set(['SCL', 'SDA', 'AREF', 'IOREF', 'RESET']);

  function pos(n) {
    if (pinPos[n]) return pinPos[n];
    let m = /^([a-e])(\d+)$/.exec(n);
    if (m) return { x: colX(+m[2]), y: BY + 62 + rowsTop.indexOf(m[1]) * 18 };
    m = /^([f-j])(\d+)$/.exec(n);
    if (m) return { x: colX(+m[2]), y: BY + 170 + rowsBot.indexOf(m[1]) * 18 };
    m = /^(TP|TN|BP|BN)(\d+)$/.exec(n);
    if (m) return { x: colX(+m[2]), y: BY + { TP: 16, TN: 34, BP: 270, BN: 288 }[m[1]] };
    return { x: 0, y: 0 };
  }
  const isBottomPin = n => pinPos[n] && pinPos[n].y > AY + 40;
  const pretty = n => {
    let m;
    if ((m = /^D(\d+)$/.exec(n))) return 'Arduino pin ' + m[1];
    if (/^A\d$/.test(n)) return 'Arduino ' + n;
    if (/^GND\d?$/.test(n)) return 'Arduino GND';
    if (n === '5V' || n === '3V3' || n === 'VIN') return 'Arduino ' + n;
    if ((m = /^(TP|TN|BP|BN)(\d+)$/.exec(n))) return `the ${{ TP: 'top + rail', TN: 'top &#8722; rail', BP: 'bottom + rail', BN: 'bottom &#8722; rail' }[m[1]]} (column ${m[2]})`;
    return 'hole ' + n;
  };
  const clone = o => JSON.parse(JSON.stringify(o));
  const store = {
    get(k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* the page still works */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* the page still works */ } },
  };
  const LEDC = { red: 'var(--red)', green: 'var(--led-green)', yellow: 'var(--led-yellow)', blue: 'var(--led-blue)', white: 'var(--white)' };
  const BAND = ['#1b1b1b', '#7a4a26', '#d23b35', '#e67e22', '#e9c22d', '#2fae4f', '#2f7fe0', '#7b4fc0', '#9aa0a6', '#ffffff'];
  const ohms = v => (v >= 1000 ? (v / 1000) + ' k&#937;' : v + ' &#937;');

  function bands(v) {
    const e = Math.floor(Math.log10(v)) - 1, d = Math.round(v / Math.pow(10, e));
    return [Math.floor(d / 10), d % 10, Math.max(0, e)].map(i => BAND[i] || BAND[0]);
  }
  const line = (a, b, c, w) => `<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${c}" stroke-width="${w || 2.5}" stroke-linecap="round"/>`;
  const curve = (a, b, c, w) => `<path d="M${a.x} ${a.y} C${a.x} ${a.y + 34} ${b.x} ${b.y - 44} ${b.x} ${b.y}" fill="none" stroke="${c}" stroke-width="${w || 3}" stroke-linecap="round"/>`;
  const mid = (a, b) => ({ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 });
  const lbl = (x, y, s, size, fill, anchor) => `<text x="${x}" y="${y}" font-size="${size || 10}" font-weight="700" fill="${fill || 'var(--lab)'}" text-anchor="${anchor || 'middle'}">${s}</text>`;
  const SILVER = 'var(--silver)';

  // Each part draws itself between its leg holes. Motors, servos, sensors and batteries sit above the board.
  const DRAW = {
    resistor(p) {
      const a = pos(p.legs.a), b = pos(p.legs.b), c = mid(a, b), ang = Math.atan2(b.y - a.y, b.x - a.x) * 180 / Math.PI, cols = bands(p.ohm);
      return line(a, b, SILVER) + `<g transform="translate(${c.x} ${c.y}) rotate(${ang})"><rect x="-17" y="-6.5" width="34" height="13" rx="5" fill="var(--tan)" stroke="var(--tan-d)"/>` +
        `<rect x="-12" y="-6.5" width="4" height="13" fill="${cols[0]}"/><rect x="-5" y="-6.5" width="4" height="13" fill="${cols[1]}"/><rect x="2" y="-6.5" width="4" height="13" fill="${cols[2]}"/><rect x="10" y="-6.5" width="3" height="13" fill="var(--gold)"/></g>`;
    },
    led(p) {
      const a = pos(p.legs.a), k = pos(p.legs.k), c = mid(a, k), col = LEDC[p.color] || LEDC.red, top = { x: c.x, y: c.y - 14 };
      return line(a, top, SILVER, 2) + line(k, top, SILVER, 2) +
        `<circle data-glow cx="${top.x}" cy="${top.y}" r="24" fill="${col}" opacity="0"/>` +
        `<circle data-dome cx="${top.x}" cy="${top.y}" r="10" fill="${col}" fill-opacity=".55" stroke="${col}" stroke-width="2"/>` +
        `<path d="M${top.x - 5} ${top.y - 3} q1 -4 4 -4" fill="none" stroke="var(--white)" stroke-opacity=".7" stroke-width="1.5"/>` +
        `<g data-burn opacity="0"><path d="M${top.x - 6} ${top.y - 6}l12 12M${top.x + 6} ${top.y - 6}l-12 12" stroke="var(--black)" stroke-width="3"/></g>` + lbl(a.x, a.y + 16, '+', 12, 'var(--hole)');
    },
    button(p) {
      const a = pos(p.legs.a), b = pos(p.legs.b), c = mid(a, b);
      return line(a, b, SILVER) + `<rect x="${c.x - 15}" y="${c.y - 15}" width="30" height="30" rx="3" fill="var(--black)" stroke="var(--black-l)"/><circle data-cap cx="${c.x}" cy="${c.y}" r="9" fill="var(--silver-d)" stroke="var(--silver)"/>`;
    },
    pot(p) {
      const a = pos(p.legs.a), w = pos(p.legs.w), b = pos(p.legs.b), c = { x: w.x, y: w.y + 26 };
      return line(a, c, SILVER) + line(w, c, SILVER) + line(b, c, SILVER) + `<circle cx="${c.x}" cy="${c.y}" r="21" fill="var(--blue)" stroke="var(--blue-d)" stroke-width="2"/><g data-knob transform="rotate(0 ${c.x} ${c.y})" data-cx="${c.x}" data-cy="${c.y}"><circle cx="${c.x}" cy="${c.y}" r="12" fill="var(--board)"/><rect x="${c.x - 1.5}" y="${c.y - 12}" width="3" height="9" fill="var(--black)"/></g>`;
    },
    ldr(p) {
      const a = pos(p.legs.a), b = pos(p.legs.b), c = mid(a, b);
      return line(a, b, SILVER) + `<circle cx="${c.x}" cy="${c.y}" r="11" fill="var(--ceramic)" stroke="var(--ceramic-d)"/><path d="M${c.x - 7} ${c.y - 3}h12l-10 3h10l-10 3h12" fill="none" stroke="var(--black)" stroke-width="1.5"/>`;
    },
    cap(p) {
      const a = pos(p.legs.p), b = pos(p.legs.n), c = mid(a, b);
      if (p.uf < 1) return line(a, b, SILVER) + `<circle cx="${c.x}" cy="${c.y}" r="9" fill="var(--ceramic)" stroke="var(--ceramic-d)"/>`;
      const dir = b.x >= a.x ? 1 : -1;
      return line(a, c, SILVER) + line(b, c, SILVER) + `<circle cx="${c.x}" cy="${c.y}" r="13" fill="var(--cap)" stroke="var(--cap-d)"/><path d="M${c.x + dir * 4} ${c.y - 12.3} A13 13 0 0 ${dir > 0 ? 1 : 0} ${c.x + dir * 4} ${c.y + 12.3} Z" fill="var(--stripe)"/>` + lbl(c.x - dir * 4, c.y + 4, '+', 12, 'var(--white)');
    },
    diode(p) {
      const a = pos(p.legs.a), k = pos(p.legs.k), c = mid(a, k), ang = Math.atan2(k.y - a.y, k.x - a.x) * 180 / Math.PI;
      return line(a, k, SILVER) + `<g transform="translate(${c.x} ${c.y}) rotate(${ang})"><rect x="-13" y="-6" width="26" height="12" rx="2" fill="var(--black)" stroke="var(--black-l)"/><rect x="6" y="-6" width="4" height="12" fill="var(--silver)"/></g>`;
    },
    npn(p) {
      const b = pos(p.legs.b), c = pos(p.legs.c), e = pos(p.legs.e), m = { x: c.x, y: c.y + 30 };
      const big = p.model !== '2N2222';
      return line(b, { x: m.x - 12, y: m.y }, SILVER, 3) + line(c, m, SILVER, 3) + line(e, { x: m.x + 12, y: m.y }, SILVER, 3) +
        (big ? `<rect x="${m.x - 26}" y="${m.y - 4}" width="52" height="14" fill="var(--silver)" stroke="var(--silver-d)"/><rect x="${m.x - 26}" y="${m.y + 6}" width="52" height="24" rx="2" fill="var(--black)" stroke="var(--black-l)"/>` + lbl(m.x, m.y + 22, 'TIP120', 10)
          : `<path d="M${m.x - 22} ${m.y + 22} v-14 a22 14 0 0 1 44 0 v14 z" fill="var(--black)" stroke="var(--black-l)"/>` + lbl(m.x, m.y + 15, '2N2222', 8.5)) +
        lbl(b.x - 8, b.y - 7, 'B', 9.5, 'var(--hole)') + lbl(c.x, c.y - 7, 'C', 9.5, 'var(--hole)') + lbl(e.x + 8, e.y - 7, 'E', 9.5, 'var(--hole)');
    },
    buzzer(p) {
      const a = pos(p.legs.p), b = pos(p.legs.n), c = mid(a, b);
      return line(a, b, SILVER) + `<circle cx="${c.x}" cy="${c.y}" r="17" fill="var(--black)" stroke="var(--black-l)"/><circle cx="${c.x}" cy="${c.y}" r="4" fill="var(--silver-d)"/>` + lbl(c.x - 9, c.y - 5, '+', 11) +
        `<g data-wave opacity="0" fill="none" stroke="var(--pt)" stroke-width="2.5"><path d="M${c.x + 21} ${c.y - 8}q6 8 0 16"/><path d="M${c.x + 27} ${c.y - 12}q9 12 0 24"/></g>`;
    },
    motor(p) {
      const x = bodyX(p), y = 38;
      return curve({ x: x - 24, y: y + 16 }, pos(p.legs.a), 'var(--red)') + curve({ x: x - 8, y: y + 16 }, pos(p.legs.b), 'var(--black)') +
        `<rect x="${x - 38}" y="${y - 16}" width="12" height="32" rx="2" fill="var(--brass)"/><rect x="${x - 26}" y="${y - 20}" width="58" height="40" rx="4" fill="var(--silver)" stroke="var(--silver-d)"/><rect x="${x + 32}" y="${y - 3}" width="16" height="6" fill="var(--silver-d)"/>` +
        `<g data-rot data-cx="${x + 64}" data-cy="${y}" transform="rotate(0 ${x + 64} ${y})"><circle cx="${x + 64}" cy="${y}" r="20" fill="var(--black)" stroke="var(--black-l)" stroke-width="3"/><path d="M${x + 64} ${y - 17}V${y + 17}M${x + 47} ${y}H${x + 81}" stroke="var(--yellow-w)" stroke-width="5"/></g>`;
    },
    servo(p) {
      const x = bodyX(p), y = 58, s = pos(p.legs.s), v = pos(p.legs.v), g = pos(p.legs.g);
      return curve({ x: x - 12, y: y + 22 }, g, 'var(--brown)') + curve({ x: x, y: y + 22 }, v, 'var(--red)') + curve({ x: x + 12, y: y + 22 }, s, 'var(--orange)') +
        `<rect x="${x - 44}" y="${y - 14}" width="88" height="10" rx="2" fill="var(--blue-d)"/><rect x="${x - 32}" y="${y - 22}" width="64" height="44" rx="3" fill="var(--blue)" stroke="var(--blue-d)"/>` + lbl(x, y + 12, 'SG90', 11, 'var(--white)') +
        `<g data-horn data-cx="${x}" data-cy="${y - 24}" transform="rotate(0 ${x} ${y - 24})"><rect x="${x - 5}" y="${y - 62}" width="10" height="42" rx="5" fill="var(--white)" stroke="var(--board-d)"/></g><circle cx="${x}" cy="${y - 24}" r="6" fill="var(--silver)" stroke="var(--silver-d)"/>`;
    },
    sonar(p) {
      const x = bodyX(p), y = 46, keys = ['vcc', 'trig', 'echo', 'gnd'], cols = ['var(--red)', 'var(--w1)', 'var(--w2)', 'var(--black)'];
      let leads = ''; keys.forEach((k, i) => { leads += curve({ x: x - 18 + i * 12, y: y + 24 }, pos(p.legs[k]), cols[i], 2.5); });
      return leads + `<rect x="${x - 56}" y="${y - 24}" width="112" height="48" rx="4" fill="var(--blue)" stroke="var(--blue-d)"/><circle cx="${x - 30}" cy="${y}" r="20" fill="var(--silver)" stroke="var(--silver-d)"/><circle cx="${x - 30}" cy="${y}" r="13" fill="var(--mesh)"/><circle cx="${x + 30}" cy="${y}" r="20" fill="var(--silver)" stroke="var(--silver-d)"/><circle cx="${x + 30}" cy="${y}" r="13" fill="var(--mesh)"/>` +
        `<g data-ping opacity="0" fill="none" stroke="var(--pt)" stroke-width="2.5"><path d="M${x + 60} ${y - 12}q8 12 0 24"/><path d="M${x + 67} ${y - 17}q11 17 0 34"/></g><text data-cm x="${x}" y="${y - 30}" font-size="11" font-weight="700" fill="var(--lab)" text-anchor="middle"></text>`;
    },
    lm35(p) {
      const a = pos(p.legs.v), b = pos(p.legs.o), c = pos(p.legs.g), m = { x: b.x, y: b.y + 28 };
      return line(a, { x: m.x - 9, y: m.y }, SILVER) + line(b, m, SILVER) + line(c, { x: m.x + 9, y: m.y }, SILVER) + `<path d="M${m.x - 18} ${m.y + 16} v-12 a18 13 0 0 1 36 0 v12 z" fill="var(--black)" stroke="var(--black-l)"/>` + lbl(m.x, m.y + 11, 'LM35', 9.5) + `<text data-val x="${m.x}" y="${m.y + 30}" font-size="11" font-weight="700" fill="var(--hole)" text-anchor="middle"></text>`;
    },
    soil(p) {
      const a = pos(p.legs.v), b = pos(p.legs.o), c = pos(p.legs.g), m = { x: b.x, y: b.y + 34 };
      return line(a, { x: m.x - 8, y: m.y }, SILVER) + line(b, m, SILVER) + line(c, { x: m.x + 8, y: m.y }, SILVER) + `<path d="M${m.x - 20} ${m.y} h40 v44 l-20 22 l-20 -22 z" fill="var(--black)" stroke="var(--black-l)"/>` + lbl(m.x, m.y + 24, 'SOIL', 9.5) + `<text data-val x="${m.x}" y="${m.y + 42}" font-size="10" font-weight="700" fill="var(--lab)" text-anchor="middle"></text>`;
    },
    irmod(p) {
      const x = bodyX(p), y = 52;
      return curve({ x: x - 12, y: y + 22 }, pos(p.legs.v), 'var(--red)', 2.5) + curve({ x: x, y: y + 22 }, pos(p.legs.g), 'var(--black)', 2.5) + curve({ x: x + 12, y: y + 22 }, pos(p.legs.o), 'var(--w1)', 2.5) +
        `<rect x="${x - 42}" y="${y - 22}" width="84" height="44" rx="4" fill="var(--blue-d)" stroke="var(--black-l)"/><circle cx="${x + 26}" cy="${y - 8}" r="8" fill="var(--board)" stroke="var(--silver)"/><circle cx="${x + 26}" cy="${y + 10}" r="8" fill="var(--black)" stroke="var(--black-l)"/>` + lbl(x - 12, y + 4, 'IR', 13) +
        `<g data-ping opacity="0" fill="none" stroke="var(--red)" stroke-width="2.5"><path d="M${x + 38} ${y - 12}q7 12 0 24"/><path d="M${x + 46} ${y - 17}q10 17 0 34"/></g><text data-val x="${x}" y="${y - 28}" font-size="11" font-weight="700" fill="var(--lab)" text-anchor="middle"></text>`;
    },
    battery(p) {
      const x = bodyX(p), y = 44;
      let cells = ''; for (let i = 0; i < 4; i++) cells += `<rect x="${x - 47 + i * 24}" y="${y - 17}" width="22" height="34" rx="2" fill="var(--gold)" stroke="var(--brass-d)"/>`;
      return curve({ x: x - 14, y: y + 24 }, pos(p.legs.p), 'var(--red)') + curve({ x: x + 14, y: y + 24 }, pos(p.legs.n), 'var(--black)') +
        `<rect x="${x - 52}" y="${y - 24}" width="104" height="48" rx="4" fill="var(--black)" stroke="var(--black-l)"/>${cells}` + lbl(x, y - 28, '4 &#215; AA, 6 V', 10.5);
    },
  };
  function bodyX(p) {
    if (p.x !== undefined) return p.x;
    const xs = Object.values(p.legs).map(n => pos(n).x);
    return Math.max(70, Math.min(W - 80, xs.reduce((a, b) => a + b, 0) / xs.length));
  }

  // ---------- static bench ----------
  function benchSvg() {
    let h = '';
    h += `<rect x="${BX}" y="${BY}" width="636" height="304" rx="8" fill="var(--board)" stroke="var(--board-d)" stroke-width="1.5"/>`;
    h += `<rect x="${BX + 6}" y="${BY + 143}" width="624" height="18" rx="3" fill="var(--board-d)"/>`;
    [[BY + 7, 'var(--red)'], [BY + 44, 'var(--blue)'], [BY + 260, 'var(--red)'], [BY + 298, 'var(--blue)']].forEach(([y, c]) => { h += `<line x1="${BX + 16}" x2="${BX + 620}" y1="${y}" y2="${y}" stroke="${c}" stroke-width="1.5"/>`; });
    for (const [s, y] of [['+', BY + 20], ['&#8722;', BY + 38], ['+', BY + 274], ['&#8722;', BY + 292]]) { h += `<text x="${BX + 12}" y="${y}" font-size="13" font-weight="700" text-anchor="middle" fill="var(--hole)">${s}</text>`; h += `<text x="${BX + 626}" y="${y}" font-size="13" font-weight="700" text-anchor="middle" fill="var(--hole)">${s}</text>`; }
    const nodes = [];
    for (let c = 1; c <= 30; c++) {
      if (c % 5 === 0 || c === 1) { h += `<text x="${colX(c)}" y="${BY + 53}" font-size="8.5" text-anchor="middle" fill="var(--hole)">${c}</text><text x="${colX(c)}" y="${BY + 258}" font-size="8.5" text-anchor="middle" fill="var(--hole)">${c}</text>`; }
      ['TP', 'TN', 'BP', 'BN'].forEach(r => nodes.push(r + c));
      for (const r of rowsTop + rowsBot) nodes.push(r + c);
    }
    (rowsTop + rowsBot).split('').forEach(r => { const y = pos(r + '1').y + 3; h += `<text x="${BX + 12}" y="${y}" font-size="9" text-anchor="middle" fill="var(--hole)">${r}</text>`; });
    nodes.forEach(n => { const q = pos(n); h += `<g class="node" data-n="${n}"><circle cx="${q.x}" cy="${q.y}" r="8.5" fill="transparent"/><rect class="hole" x="${q.x - 3}" y="${q.y - 3}" width="6" height="6" rx="1" fill="var(--hole)"/></g>`; });
    // Arduino board
    h += `<path d="M${AX} ${AY} H${AX + 400} L${AX + 420} ${AY + 18} V${AY + 70} L${AX + 400} ${AY + 90} V${AY + AH - 18} L${AX + 384} ${AY + AH} H${AX} Z" fill="var(--teal)" stroke="var(--teal-d)" stroke-width="2"/>`;
    h += `<rect x="${AX - 26}" y="${AY + 26}" width="70" height="56" rx="3" fill="var(--silver)" stroke="var(--silver-d)"/><rect x="${AX - 20}" y="${AY + 34}" width="42" height="40" fill="var(--silver-d)"/>`;
    h += `<rect x="${AX - 20}" y="${AY + 146}" width="60" height="46" rx="3" fill="var(--black)" stroke="var(--black-l)"/><circle cx="${AX - 2}" cy="${AY + 169}" r="10" fill="var(--silver-d)"/>`;
    h += `<rect x="${AX + 170}" y="${AY + 108}" width="190" height="44" rx="4" fill="var(--black)" stroke="var(--black-l)"/>` + lbl(AX + 265, AY + 135, 'ATmega328P', 12);
    h += lbl(AX + 110, AY + 76, 'Arduino Uno', 14, 'var(--white)');
    h += `<circle data-onboard cx="${AX + 76}" cy="${AY + 42}" r="4.5" fill="var(--black)" stroke="var(--pt)"/>` + lbl(AX + 76, AY + 60, 'L', 9, 'var(--white)');
    h += `<rect x="${AX + 84}" y="${AY + 6}" width="${19 * 15}" height="16" rx="2" fill="var(--black)"/><rect x="${AX + 156}" y="${AY + AH - 22}" width="${14 * 15}" height="16" rx="2" fill="var(--black)"/>`;
    for (const n in pinPos) {
      const q = pinPos[n], bot = isBottomPin(n), name = n.replace(/^D(\d+)$/, '$1').replace(/^GND\d$/, 'GND');
      h += `<text transform="translate(${q.x + 3} ${bot ? q.y - 13 : q.y + 13}) rotate(-90)" font-size="8.5" font-weight="700" text-anchor="${bot ? 'start' : 'end'}" fill="var(--white)">${name}</text>`;
      if (DECOR.has(n)) h += `<rect x="${q.x - 3}" y="${q.y - 3}" width="6" height="6" rx="1" fill="var(--hole)"/>`;
      else h += `<g class="node" data-n="${n}"><circle cx="${q.x}" cy="${q.y}" r="8" fill="transparent"/><rect class="hole" x="${q.x - 3}" y="${q.y - 3}" width="6" height="6" rx="1" fill="var(--silver)"/></g>`;
    }
    return h;
  }

  // ---------- the lab ----------
  const Lab = {
    id: null, ex: null, c: null, code: '', sim: null, tool: 'select', pending: [], addType: null, selected: null, undo: [], raf: 0, last: 0, audio: null, osc: null, lastSerial: -1,

    init() {
      const svg = $('sim-svg');
      svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      svg.innerHTML = `<rect width="${W}" height="${H}" fill="var(--mat)"/><rect width="${W}" height="${H}" fill="url(#matgrid)"/>` + benchSvg() + '<g id="sim-wires"></g><g id="sim-parts"></g><path id="sim-rubber" fill="none" stroke="var(--pt)" stroke-width="3" stroke-dasharray="5 5" pointer-events="none"/>';
      this.nodeEls = {}; svg.querySelectorAll('.node').forEach(g => { this.nodeEls[g.getAttribute('data-n')] = g; });
      svg.addEventListener('click', e => this.onClick(e));
      svg.addEventListener('mouseover', e => this.onHover(e));
      svg.addEventListener('mouseleave', () => this.highlight(null));
      svg.addEventListener('pointermove', e => this.onMove(e));
      svg.addEventListener('pointerdown', e => this.pressPart(e, 1));
      addEventListener('pointerup', () => this.releaseAll());
      $('sim-start').addEventListener('click', () => (this.sim ? this.stop() : this.start()));
      $('sim-check').addEventListener('click', () => this.check());
      $('tool-select').addEventListener('click', () => this.setTool('select'));
      $('tool-wire').addEventListener('click', () => this.setTool('wire'));
      $('tool-delete').addEventListener('click', () => this.deleteSelected());
      $('tool-undo').addEventListener('click', () => this.doUndo());
      $('tool-restore').addEventListener('click', () => this.askRestore());
      $('restore-yes').addEventListener('click', () => this.restore());
      $('restore-no').addEventListener('click', () => { $('restore-confirm').hidden = true; });
      $('tool-add').addEventListener('change', e => { const v = e.target.value; e.target.value = ''; if (v) this.startAdd(v); });
      $('sim-board').addEventListener('change', () => { this.stop(); this.status(`Board set to Uno ${$('sim-board').value}.`); });
      const ta = $('sim-code');
      ta.addEventListener('input', () => { this.code = ta.value; this.gutter(); this.save(); if (this.sim) this.stop(); this.markLine(null); });
      ta.addEventListener('scroll', () => { $('sim-gutter').scrollTop = ta.scrollTop; });
      ta.addEventListener('keydown', e => {
        if (e.key === 'Tab' && !e.shiftKey) { e.preventDefault(); const s = ta.selectionStart; ta.setRangeText('  ', s, ta.selectionEnd, 'end'); ta.dispatchEvent(new Event('input')); }
      });
      addEventListener('keydown', e => {
        if (e.key === 'Escape') this.setTool('select');
        if ((e.key === 'Delete' || e.key === 'Backspace') && this.selected && !e.target.matches('input,select,textarea')) { e.preventDefault(); this.deleteSelected(); }
      });
      let opts = '<option value="">Add a part&#8230;</option>';
      Object.keys(PART_TYPES).forEach(k => { opts += `<option value="${k}">${PART_TYPES[k].label}</option>`; });
      $('tool-add').innerHTML = opts;
      this.renderIndex();
    },

    renderIndex() {
      const done = store.get('elab-done') || {};
      const groups = [['LEDs and resistors', 1, 7], ['Buttons, dials and sensors', 8, 13], ['Capacitors and transistors', 14, 15], ['DC motors', 16, 18], ['Servo motors', 19, 21], ['Distance sensor projects', 22, 25], ['More sensors', 26, 28]];
      $('lab-index').innerHTML = groups.map(([g, a, b]) => `<h2>${g}</h2><ol class="ex-list" start="${a}">` + EX.slice(a - 1, b).map(e => `<li><a href="#ex-${e.n}">${e.title}</a>${done[e.n] ? ' <span class="done">&#10003; checked</span>' : ''}<span class="marks">${e.goal}</span></li>`).join('') + '</ol>').join('');
      document.querySelectorAll('[data-ex-topic]').forEach(ol => {
        const t = ol.getAttribute('data-ex-topic');
        ol.innerHTML = EX.filter(e => e.topics.includes(t)).map(e => `<li><a href="#ex-${e.n}">Example ${e.n}: ${e.title}</a></li>`).join('');
      });
    },

    open(id) {
      this.stop();
      this.id = id;
      this.ex = id === 'sandbox' ? null : EX[+id.slice(3) - 1] || EX[0];
      const saved = store.get('elab-' + id);
      this.c = saved ? saved.c : (this.ex ? clone(this.ex.c) : { parts: [], wires: [] });
      this.code = saved ? saved.code : (this.ex ? this.ex.code : '// Build your own circuit, then write its code here.\nvoid setup() {\n}\n\nvoid loop() {\n}\n');
      this.undo = []; this.selected = null; this.pending = []; this.setTool('select');
      $('sim-code').value = this.code; this.gutter(); this.markLine(null);
      $('sim-serial').textContent = ''; $('sim-results').innerHTML = ''; $('restore-confirm').hidden = true;
      this.msgKey = null; this.renderNotes(); this.draw(); this.renderControls(); this.renderMsgs();
      $('sim-check').hidden = !this.ex;
      this.status(this.ex ? 'Select Start Simulation to run this circuit.' : 'Add parts and wires, write your code, then select Start Simulation.');
    },
    close() { this.stop(); },

    renderNotes() {
      const ex = this.ex;
      $('sim-title').innerHTML = ex ? `Example ${ex.n}: ${ex.title}` : 'Free build';
      $('sim-goal').innerHTML = ex ? ex.goal : 'A blank bench for trying your own circuits and code.';
      const box = $('sim-notes');
      if (!ex) { box.innerHTML = '<p>Select <strong>Add a part</strong>, then select the holes for each leg. Use <strong>Wire</strong> to join any two points. Your build stays saved in this browser.</p>'; $('sim-pn').innerHTML = '<a href="#lab">&larr; All examples</a>'; return; }
      const counts = {};
      ex.c.parts.forEach(p => {
        const n = p.type === 'resistor' ? `${ohms(p.ohm)} resistor` : p.type === 'led' ? `${p.color} LED` : p.type === 'cap' ? `${p.uf} &#181;F capacitor` : p.type === 'npn' ? `${p.model} transistor` : PART_TYPES[p.type].label;
        counts[n] = (counts[n] || 0) + 1;
      });
      const parts = ['Arduino Uno and USB cable', 'Breadboard and jumper wires'].concat(Object.keys(counts).map(k => `${counts[k]} &#215; ${k}`));
      const steps = [];
      ex.c.parts.forEach(p => {
        const t = PART_TYPES[p.type];
        steps.push(`<strong>${p.id}</strong> (${t.label}): ` + t.legs.map((l, i) => `${t.names[i]} to ${pretty(p.legs[l])}`).join(', ') + '.');
      });
      ex.c.wires.forEach(w => steps.push(`Wire: ${pretty(w[0])} to ${pretty(w[1])}.`));
      const prev = ex.n > 1 ? `<a href="#ex-${ex.n - 1}">&larr; Example ${ex.n - 1}</a>` : '<a href="#lab">&larr; All examples</a>';
      const next = ex.n < EX.length ? `<a href="#ex-${ex.n + 1}">Example ${ex.n + 1} &rarr;</a>` : '<a href="#robots">Robot exercises &rarr;</a>';
      box.innerHTML = `<h2>What should happen</h2><p>${ex.happen}</p>` + (ex.inputs ? `<p><strong>Your turn:</strong> ${ex.inputs}</p>` : '') +
        `<h2>Parts you need</h2><ul class="tight">${parts.map(x => `<li>${x}</li>`).join('')}</ul>` +
        `<h2>Build it step by step</h2><p class="sub">Unplug the power first. These are the same holes you see on the bench, so you can copy them onto a real breadboard.</p><ol class="q">${steps.map(s => `<li>${s}</li>`).join('')}</ol>` +
        `<h2>Try this</h2><p>${ex.tryit}</p>`;
      $('sim-pn').innerHTML = prev + next;
    },

    renderControls() {
      const box = $('sim-controls'); let h = '';
      this.c.parts.forEach(p => {
        if (p.type === 'button') h += `<div class="ctl"><span class="ctl-l">${p.id}</span><button type="button" class="alt hold" data-hold="${p.id}">Hold to press</button></div>`;
        if (p.type === 'pot') h += `<div class="ctl"><label class="ctl-l" for="ctl-${p.id}">${p.id} dial</label><input type="range" id="ctl-${p.id}" data-in="${p.id}" min="0" max="100" value="${Math.round((p.x === undefined ? 0.5 : p.x) * 100)}"><output id="out-${p.id}"></output></div>`;
        if (p.type === 'ldr') h += `<div class="ctl"><label class="ctl-l" for="ctl-${p.id}">Room light</label><input type="range" id="ctl-${p.id}" data-in="${p.id}" min="0" max="100" value="${Math.round((p.light === undefined ? 0.5 : p.light) * 100)}"><output id="out-${p.id}"></output></div>`;
        if (p.type === 'sonar') h += `<div class="ctl"><label class="ctl-l" for="ctl-${p.id}">Distance to wall</label><input type="range" id="ctl-${p.id}" data-in="${p.id}" min="2" max="300" value="${p.cm === undefined ? 100 : p.cm}"><output id="out-${p.id}"></output></div><div class="ctl"><label class="ctl-chk"><input type="checkbox" id="soft-${p.id}" data-soft="${p.id}"${p.soft ? ' checked' : ''}> Soft curtain (absorbs the sound)</label></div>`;
      });
      this.c.parts.forEach(p => {
        if (p.type === 'lm35') h += `<div class="ctl"><label class="ctl-l" for="ctl-${p.id}">Temperature</label><input type="range" id="ctl-${p.id}" data-in="${p.id}" min="0" max="100" value="${p.tempC === undefined ? 25 : p.tempC}"><output id="out-${p.id}"></output></div>`;
        if (p.type === 'soil') h += `<div class="ctl"><label class="ctl-l" for="ctl-${p.id}">Soil moisture</label><input type="range" id="ctl-${p.id}" data-in="${p.id}" min="0" max="100" value="${p.moist === undefined ? 50 : p.moist}"><output id="out-${p.id}"></output></div>`;
        if (p.type === 'irmod') h += `<div class="ctl"><label class="ctl-l" for="ctl-${p.id}">Object distance</label><input type="range" id="ctl-${p.id}" data-in="${p.id}" min="2" max="100" value="${p.cm === undefined ? 100 : p.cm}"><output id="out-${p.id}"></output></div>`;
      });
      if (this.c.parts.some(p => p.type === 'buzzer')) h += '<div class="ctl"><label class="ctl-chk"><input type="checkbox" id="sim-sound" checked> Sound</label></div>';
      box.innerHTML = h; box.hidden = !h;
      box.querySelectorAll('[data-in]').forEach(el => { el.addEventListener('input', () => this.onInput(el)); this.showOut(el); });
      box.querySelectorAll('[data-soft]').forEach(el => el.addEventListener('change', () => {
        const id = el.getAttribute('data-soft'), p = this.part(id); p.soft = el.checked;
        if (this.sim) { this.sim.part(id).soft = el.checked; } this.save();
      }));
      box.querySelectorAll('[data-hold]').forEach(el => {
        const id = el.getAttribute('data-hold');
        const set = v => { if (this.sim) this.sim.setInput(id, v); el.classList.toggle('on', !!v); };
        el.addEventListener('pointerdown', () => set(1));
        ['pointerup', 'pointerleave', 'pointercancel', 'blur'].forEach(ev => el.addEventListener(ev, () => set(0)));
        el.addEventListener('keydown', e => { if ((e.key === ' ' || e.key === 'Enter') && !e.repeat) { e.preventDefault(); set(1); } });
        el.addEventListener('keyup', e => { if (e.key === ' ' || e.key === 'Enter') set(0); });
      });
    },
    showOut(el) {
      const id = el.getAttribute('data-in'), p = this.part(id), o = $('out-' + id); if (!o || !p) return;
      o.textContent = p.type === 'sonar' || p.type === 'irmod' ? `${el.value} cm` : p.type === 'lm35' ? `${el.value}\u00b0C` : `${el.value}%`;
    },
    onInput(el) {
      const id = el.getAttribute('data-in'), p = this.part(id), v = +el.value;
      if (p.type === 'pot') p.x = v / 100; else if (p.type === 'ldr') p.light = v / 100; else if (p.type === 'sonar' || p.type === 'irmod') p.cm = v; else if (p.type === 'lm35') p.tempC = v; else if (p.type === 'soil') p.moist = v;
      if (this.sim) this.sim.setInput(id, ['sonar', 'irmod', 'lm35', 'soil'].includes(p.type) ? v : v / 100);
      this.showOut(el); this.save(); this.live();
    },

    part(id) { return this.c.parts.find(p => p.id === id); },
    save() { store.set('elab-' + this.id, { c: this.c, code: this.code }); },
    push() { this.undo.push(JSON.stringify(this.c)); if (this.undo.length > 40) this.undo.shift(); },
    doUndo() {
      if (!this.undo.length) { this.status('Nothing to undo.'); return; }
      this.stop(); this.c = JSON.parse(this.undo.pop()); this.selected = null; this.draw(); this.renderControls(); this.save(); this.status('Undid your last change.');
    },
    askRestore() { if (this.ex) $('restore-confirm').hidden = false; else this.restore(); },
    restore() {
      this.stop(); store.del('elab-' + this.id); $('restore-confirm').hidden = true;
      this.open(this.id); this.status(this.ex ? 'Example restored to its original circuit and code.' : 'Bench cleared.');
    },

    // ---------- drawing ----------
    wireColor(w, i) {
      const k = [netKey(w[0]), netKey(w[1])];
      if (k.some(x => x === 'GND' || x === 'TN' || x === 'BN')) return 'var(--black)';
      if (k.some(x => x === '5V' || x === 'TP' || x === 'BP')) return 'var(--red)';
      return `var(--w${(i % 5) + 1})`;
    },
    wirePath(a, b, i) {
      const pa = pos(a), pb = pos(b);
      if (isBottomPin(a) || isBottomPin(b)) {
        const [from, to] = isBottomPin(a) ? [pa, pb] : [pb, pa];
        const k = i % 6, yb = AY + AH + 8 + k * 3, xr = AX + 428 + k * 5;
        return `M${from.x} ${from.y} V${yb} H${xr} V${BY + 318} C${xr} ${BY + 290} ${to.x} ${to.y + 70} ${to.x} ${to.y}`;
      }
      const dy = Math.abs(pa.y - pb.y), dx = Math.abs(pa.x - pb.x);
      if (dy > 60) { const h = Math.min(90, dy / 2); const s = pa.y > pb.y ? 1 : -1; return `M${pa.x} ${pa.y} C${pa.x} ${pa.y - s * h} ${pb.x} ${pb.y + s * h} ${pb.x} ${pb.y}`; }
      const h = Math.min(30, 8 + (dx + dy) / 4);
      return `M${pa.x} ${pa.y} C${pa.x} ${pa.y - h} ${pb.x} ${pb.y - h} ${pb.x} ${pb.y}`;
    },
    draw() {
      $('sim-wires').innerHTML = this.c.wires.map((w, i) => {
        const d = this.wirePath(w[0], w[1], i), sel = this.selected === 'w' + i;
        return `<g data-wire="${i}" class="wire${sel ? ' sel' : ''}"><path d="${d}" fill="none" stroke="var(--wire-halo)" stroke-width="5" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${this.wireColor(w, i)}" stroke-width="3" stroke-linecap="round"/><path d="${d}" fill="none" stroke="transparent" stroke-width="12"/></g>`;
      }).join('');
      $('sim-parts').innerHTML = this.c.parts.map(p => `<g data-part="${p.id}" class="part${this.selected === p.id ? ' sel' : ''}">${DRAW[p.type](p)}</g>`).join('');
      this.liveEls = {};
      this.c.parts.forEach(p => { this.liveEls[p.id] = document.querySelector(`#sim-parts [data-part="${CSS.escape(p.id)}"]`); });
      this.renderProps(); this.live();
    },
    renderProps() {
      const box = $('sim-props'), sel = this.selected; let h = '';
      const p = sel && sel[0] !== 'w' ? this.part(sel) : null;
      if (p) {
        h = `<strong>${p.id}</strong> ${PART_TYPES[p.type].label}`;
        if (p.type === 'resistor') h += ` <label>Value <select id="prop-ohm">${[100, 220, 330, 470, 1000, 2200, 4700, 10000].map(v => `<option value="${v}"${v === p.ohm ? ' selected' : ''}>${ohms(v)}</option>`).join('')}</select></label>`;
        if (p.type === 'led') h += ` <label>Colour <select id="prop-color">${Object.keys(LEDC).map(v => `<option${v === p.color ? ' selected' : ''}>${v}</option>`).join('')}</select></label>`;
        if (p.type === 'cap') h += ` <label>Value <select id="prop-uf">${[0.1, 10, 100, 470, 1000].map(v => `<option value="${v}"${v === p.uf ? ' selected' : ''}>${v} &#181;F</option>`).join('')}</select></label>`;
        if (p.type === 'npn') h += ` <label>Model <select id="prop-model"><option${p.model === 'TIP120' ? ' selected' : ''}>TIP120</option><option${p.model === '2N2222' ? ' selected' : ''}>2N2222</option></select></label>`;
        h += ' <span id="sim-read" class="marks"></span>';
      } else if (sel) h = 'Wire selected. Select Delete to remove it.';
      box.innerHTML = h; box.hidden = !h;
      const wire = (id, fn) => { const el = $(id); if (el) el.addEventListener('change', () => { this.push(); this.stop(); fn(el.value); this.draw(); this.save(); }); };
      wire('prop-ohm', v => { p.ohm = +v; }); wire('prop-color', v => { p.color = v; }); wire('prop-uf', v => { p.uf = +v; }); wire('prop-model', v => { p.model = v; });
    },

    // ---------- editing ----------
    setTool(t) {
      this.tool = t; this.pending = []; this.addType = t === 'part' ? this.addType : null;
      $('tool-select').classList.toggle('on', t === 'select'); $('tool-wire').classList.toggle('on', t === 'wire');
      $('sim-svg').classList.toggle('placing', t !== 'select');
      $('sim-rubber').setAttribute('d', '');
      if (t === 'wire') this.status('Wire: select the first point, then the second. Press Esc when you\'re done.');
      else if (t === 'select' && this.id) this.status('Select a part to read its current, or to change or delete it.');
    },
    startAdd(type) { this.stop(); this.setTool('part'); this.addType = type; this.promptLeg(); },
    promptLeg() { const t = PART_TYPES[this.addType]; this.status(`${t.label}: select a hole for ${t.names[this.pending.length]}.`); },
    onClick(e) {
      const nodeEl = e.target.closest('[data-n]'), partEl = e.target.closest('[data-part]'), wireEl = e.target.closest('[data-wire]');
      if (this.tool === 'wire') {
        if (!nodeEl) return;
        const n = nodeEl.getAttribute('data-n');
        if (!this.pending.length) { this.pending = [n]; this.status(`Wire from ${pretty(n)}: now select the other end.`); return; }
        if (this.pending[0] !== n) { this.stop(); this.push(); this.c.wires.push([this.pending[0], n]); this.draw(); this.save(); this.status(`Wire added. Select another start point, or press Esc.`); }
        this.pending = []; $('sim-rubber').setAttribute('d', ''); return;
      }
      if (this.tool === 'part') {
        if (!nodeEl) return;
        this.pending.push(nodeEl.getAttribute('data-n'));
        const t = PART_TYPES[this.addType];
        if (this.pending.length < t.legs.length) { this.promptLeg(); return; }
        const legs = {}; t.legs.forEach((l, i) => { legs[l] = this.pending[i]; });
        const pre = { lm35: 'T', soil: 'SM', irmod: 'IR', resistor: 'R', led: 'LED', button: 'BTN', pot: 'POT', ldr: 'LDR', cap: 'C', diode: 'D', npn: 'Q', motor: 'M', buzzer: 'BZ', servo: 'SV', sonar: 'S', battery: 'B' }[this.addType];
        let k = 1; while (this.part(pre + k)) k++;
        this.stop(); this.push();
        this.c.parts.push(Object.assign({ id: pre + k, type: this.addType, legs }, clone(t.def)));
        this.selected = pre + k; this.setTool('select'); this.draw(); this.renderControls(); this.save();
        this.status(`${t.label} added as ${pre + k}.`); return;
      }
      if (partEl) { this.selected = partEl.getAttribute('data-part'); this.draw(); return; }
      if (wireEl) { this.selected = 'w' + wireEl.getAttribute('data-wire'); this.draw(); return; }
      if (this.selected) { this.selected = null; this.draw(); }
    },
    deleteSelected() {
      if (!this.selected) { this.status('Select a part or wire first.'); return; }
      this.stop(); this.push();
      if (this.selected[0] === 'w' && /^w\d+$/.test(this.selected)) this.c.wires.splice(+this.selected.slice(1), 1);
      else this.c.parts = this.c.parts.filter(p => p.id !== this.selected);
      this.selected = null; this.draw(); this.renderControls(); this.save(); this.status('Deleted. Select Undo to bring it back.');
    },
    onHover(e) { const el = e.target.closest('[data-n]'); this.highlight(el ? el.getAttribute('data-n') : null); },
    highlight(n) {
      if (this.hi) this.hi.forEach(g => g.classList.remove('hi'));
      this.hi = [];
      const label = $('sim-hole');
      if (!n) { label.textContent = ''; return; }
      const k = netKey(n);
      for (const m in this.nodeEls) if (netKey(m) === k) { this.nodeEls[m].classList.add('hi'); this.hi.push(this.nodeEls[m]); }
      label.innerHTML = pretty(n) + (this.hi.length > 1 ? ` &middot; ${this.hi.length} joined points` : '');
    },
    onMove(e) {
      if (this.tool !== 'wire' || !this.pending.length) return;
      const svg = $('sim-svg'), m = svg.getScreenCTM(); if (!m) return;
      const x = (e.clientX - m.e) / m.a, y = (e.clientY - m.f) / m.d, a = pos(this.pending[0]);
      $('sim-rubber').setAttribute('d', `M${a.x} ${a.y} L${x} ${y}`);
    },
    pressPart(e, v) {
      if (!this.sim || this.tool !== 'select') return;
      const g = e.target.closest('[data-part]'); if (!g) return;
      const p = this.part(g.getAttribute('data-part'));
      if (p && p.type === 'button') { this.sim.setInput(p.id, v); this.pressed = p.id; }
    },
    releaseAll() { if (this.pressed && this.sim) { this.sim.setInput(this.pressed, 0); } this.pressed = null; },

    // ---------- running ----------
    start() {
      this.setTool('select');
      const sim = new Sim(this.c, this.code, { board: $('sim-board').value });
      $('sim-results').innerHTML = '';
      if (sim.err) { this.showError(sim.err); return; }
      this.markLine(null); this.sim = sim; this.lastSerial = -1; $('sim-serial').textContent = '';
      const b = $('sim-start'); b.textContent = 'Stop Simulation'; b.classList.add('stop');
      this.status('Simulation running.'); this.renderMsgs(); this.last = performance.now();
      const tick = now => {
        if (!this.sim) return;
        const dt = Math.min(50, now - this.last); this.last = now;
        this.sim.step(dt);
        if (this.sim.err) { const er = this.sim.err; this.stop(); this.showError(er); return; }
        this.live();
        this.raf = requestAnimationFrame(tick);
      };
      this.raf = requestAnimationFrame(tick);
    },
    stop() {
      if (this.raf) cancelAnimationFrame(this.raf);
      this.raf = 0; const was = !!this.sim; this.sim = null;
      const b = $('sim-start'); if (b) { b.textContent = 'Start Simulation'; b.classList.remove('stop'); }
      this.sound(0);
      if (was) { this.live(); this.status('Simulation stopped.'); }
    },
    showError(err) {
      this.markLine(err.line); this.msgKey = null;
      $('sim-msgs').innerHTML = `<div class="msg bad"><strong>Code problem on line ${err.line}.</strong> ${err.msg}</div>`;
      this.status(`Code problem on line ${err.line}.`);
    },
    check() {
      this.stop();
      const r = runCheck(this.ex, this.c, this.code, $('sim-board').value), all = r.results.every(x => x.ok);
      if (r.compileError) this.markLine(r.compileError.line);
      const bad = r.warns.filter(w => w.sev === 'bad');
      const pass = all && !bad.length;
      let h = `<div class="check-head ${pass ? 'ok' : 'no'}">${pass ? 'Your build passes every check.' : all ? 'It behaves correctly, but something would be unsafe on a real board.' : 'Not there yet. Look at the items marked below.'}</div><ul class="check-list">`;
      h += r.results.map(x => `<li class="${x.ok ? 'ok' : 'no'}"><span aria-hidden="true">${x.ok ? '&#10003;' : '&#10007;'}</span> ${x.say}</li>`).join('') + '</ul>';
      h += r.warns.map(w => `<div class="msg ${w.sev}">${w.msg}</div>`).join('');
      $('sim-results').innerHTML = h;
      if (pass) { const d = store.get('elab-done') || {}; d[this.ex.n] = 1; store.set('elab-done', d); this.renderIndex(); }
      this.status(pass ? 'All checks passed.' : 'Some checks need another look.');
    },
    status(s) { $('sim-status').innerHTML = s; },
    gutter() {
      const n = this.code.split('\n').length; let h = '';
      for (let i = 1; i <= n; i++) h += `<span data-l="${i}">${i}</span>`;
      $('sim-gutter').innerHTML = h; $('sim-gutter').scrollTop = $('sim-code').scrollTop;
    },
    markLine(l) {
      document.querySelectorAll('#sim-gutter .err').forEach(x => x.classList.remove('err'));
      if (l) { const el = document.querySelector(`#sim-gutter [data-l="${l}"]`); if (el) el.classList.add('err'); }
    },
    renderMsgs() {
      const s = this.sim, box = $('sim-msgs');
      const list = s ? Array.from(s.warns.values()) : [];
      const key = (s ? 'run:' : 'idle:') + list.map(w => w.msg).join('|');
      if (key === this.msgKey) return;
      this.msgKey = key;
      box.innerHTML = list.length ? list.map(w => `<div class="msg ${w.sev}">${w.msg}</div>`).join('') : (s ? '<div class="msg good">No problems so far.</div>' : '');
    },
    sound(f) {
      try {
        const on = f && $('sim-sound') && $('sim-sound').checked;
        if (on && !this.audio) {
          const Ctx = window.AudioContext || window.webkitAudioContext; if (!Ctx) return;
          this.audio = new Ctx(); this.osc = this.audio.createOscillator(); this.gain = this.audio.createGain();
          this.osc.type = 'square'; this.gain.gain.value = 0; this.osc.connect(this.gain); this.gain.connect(this.audio.destination); this.osc.start();
        }
        if (!this.audio) return;
        if (on) this.osc.frequency.value = f;
        this.gain.gain.value = on ? 0.03 : 0;
      } catch (e) { /* no sound available */ }
    },

    // Updates what moves or glows without redrawing the bench.
    live() {
      const s = this.sim, get = id => (s ? s.part(id) : null);
      let tone = 0;
      this.c.parts.forEach(p => {
        const el = this.liveEls && this.liveEls[p.id]; if (!el) return;
        const q = get(p.id), st = q ? q.st : null;
        if (p.type === 'led') {
          const mA = st && !st.burned ? Math.max(0, st.i) * 1000 : 0, b = Math.min(1, Math.sqrt(mA / 14));
          el.querySelector('[data-glow]').setAttribute('opacity', (b * 0.55).toFixed(2));
          el.querySelector('[data-dome]').setAttribute('fill-opacity', (0.45 + b * 0.55).toFixed(2));
          el.querySelector('[data-burn]').setAttribute('opacity', st && st.burned ? 1 : 0);
        } else if (p.type === 'pot') {
          const k = el.querySelector('[data-knob]'), v = q ? q.x : (p.x === undefined ? 0.5 : p.x);
          k.setAttribute('transform', `rotate(${(v - 0.5) * 270} ${k.getAttribute('data-cx')} ${k.getAttribute('data-cy')})`);
        } else if (p.type === 'button') {
          el.querySelector('[data-cap]').setAttribute('fill', st && st.press ? 'var(--pt)' : 'var(--silver-d)');
        } else if (p.type === 'motor') {
          const r = el.querySelector('[data-rot]'); this.rot = this.rot || {};
          this.rot[p.id] = ((this.rot[p.id] || 0) + (st ? st.speed : 0) * 18) % 360;
          r.setAttribute('transform', `rotate(${this.rot[p.id].toFixed(1)} ${r.getAttribute('data-cx')} ${r.getAttribute('data-cy')})`);
        } else if (p.type === 'servo') {
          const h = el.querySelector('[data-horn]'), ang = st ? st.angle + (st.jitter || 0) : 90;
          h.setAttribute('transform', `rotate(${(ang - 90).toFixed(1)} ${h.getAttribute('data-cx')} ${h.getAttribute('data-cy')})`);
        } else if (p.type === 'buzzer') {
          el.querySelector('[data-wave]').setAttribute('opacity', st && st.sound ? 1 : 0);
          if (st && st.sound) tone = st.freq;
        } else if (p.type === 'lm35' || p.type === 'soil' || p.type === 'irmod') {
          const src = q || p, val = el.querySelector('[data-val]');
          if (val) val.textContent = p.type === 'lm35' ? `${src.tempC === undefined ? 25 : src.tempC}\u00b0C` : p.type === 'soil' ? `${src.moist === undefined ? 50 : src.moist}%` : `${src.cm === undefined ? 100 : src.cm} cm`;
          const ping = el.querySelector('[data-ping]'); if (ping) ping.setAttribute('opacity', s && q.s.d ? 1 : 0);
        } else if (p.type === 'sonar') {
          const cm = q ? q.cm : (p.cm === undefined ? 100 : p.cm);
          el.querySelector('[data-cm]').textContent = `${cm} cm`;
          el.querySelector('[data-ping]').setAttribute('opacity', s && st.ping !== undefined && s.simT - st.ping < 90000 ? 1 : 0);
        }
      });
      const ob = document.querySelector('[data-onboard]');
      if (ob) ob.setAttribute('fill', s && s.pins[13].level && s.pins[13].mode === 1 ? 'var(--pt)' : 'var(--black)');
      if (!s) { this.sound(0); return; }
      this.sound(tone);
      if (s.serial.length !== this.lastSerial) { const box = $('sim-serial'); box.textContent = s.serial.slice(-4000); box.scrollTop = box.scrollHeight; this.lastSerial = s.serial.length; }
      this.renderMsgs();
      const read = $('sim-read'), sel = this.selected;
      if (read && sel && sel[0] !== 'w') {
        const q = get(sel);
        if (q) {
          const ma = (Math.abs(q.st.i) * 1000).toFixed(1), v = Math.abs(q.st.v).toFixed(2);
          read.textContent = q.type === 'motor' ? `${v} V, ${ma} mA, speed ${Math.round(Math.abs(q.st.speed) * 100)}%` : q.type === 'servo' ? `angle ${Math.round(q.st.angle)}°, ${v} V` : q.type === 'sonar' ? `${v} V, ${ma} mA` : `${v} V, ${ma} mA`;
        }
      } else if (read) read.textContent = '';
    },
  };
  window.ELabUI = Lab;
})();
