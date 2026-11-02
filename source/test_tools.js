// Checks the Live Tools sums against answers worked out by hand. Run: node test_tools.js
require('./tools.js');
const T = globalThis.EToolsCalc, C = T.CALC;
let bad = 0, n = 0;
function eq(name, got, want) { n++; const ok = JSON.stringify(got) === JSON.stringify(want); if (!ok) { bad++; console.log('FAIL', name, 'got', got, 'want', want); } }
function near(name, got, want, tol = 0.005) { n++; if (Math.abs(got - want) > Math.abs(want) * tol) { bad++; console.log('FAIL', name, 'got', got, 'want', want); } }
const row = (r, label) => { const f = r.rows.find(x => x[0].includes(label)); return f ? f[1] : undefined; };

// Resistors, both ways
eq('red red brown gold', T.decodeResistor(['red', 'red', 'brown', 'gold']).ohm, 220);
eq('yellow violet brown', T.decodeResistor(['yellow', 'violet', 'brown', 'gold']).ohm, 470);
eq('green blue red gold', T.decodeResistor(['green', 'blue', 'red', 'gold']).ohm, 5600);
eq('5 band 4.7k', T.decodeResistor(['yellow', 'violet', 'black', 'brown', 'brown']).ohm, 4700);
eq('gold multiplier', T.decodeResistor(['yellow', 'violet', 'gold', 'gold']).ohm, 4.7);
eq('silver multiplier', T.decodeResistor(['yellow', 'violet', 'silver', 'gold']).ohm, 0.47);
eq('tolerance', T.decodeResistor(['red', 'red', 'brown', 'gold']).tol, 5);
eq('backwards hint', T.decodeResistor(['black', 'red', 'brown', 'gold']).backwards, true);
eq('encode 220', T.encodeResistor(220, 4, 'gold').bands, ['red', 'red', 'brown', 'gold']);
eq('encode 10k', T.encodeResistor(10000, 4, 'gold').bands, ['brown', 'black', 'orange', 'gold']);
eq('encode 4.7', T.encodeResistor(4.7, 4, 'gold').bands, ['yellow', 'violet', 'gold', 'gold']);
eq('encode 0.47', T.encodeResistor(0.47, 4, 'gold').bands, ['yellow', 'violet', 'silver', 'gold']);
eq('encode 5-band', T.encodeResistor(4700, 5, 'brown').bands, ['yellow', 'violet', 'black', 'brown', 'brown']);
eq('inexact', T.encodeResistor(4750, 4, 'gold').exact, false);
eq('exact on 5 band', T.encodeResistor(4750, 5, 'brown').exact, true);
eq('round up a decade', T.encodeResistor(9990, 4, 'gold').made, 10000);
for (const v of [1, 2.2, 10, 47, 100, 220, 1000, 4700, 33000, 1e6, 8.2e6]) eq('round trip ' + v, T.decodeResistor(T.encodeResistor(v, 4, 'gold').bands).ohm, v);

// Reading typed values
for (const [s, v] of [['220', 220], ['4.7k', 4700], ['4k7', 4700], ['1M', 1e6], ['1M5', 1.5e6], ['220R', 220], ['4R7', 4.7], ['10 k', 10000], ['1k ohm', 1000], ['abc', null], ['0', null]]) eq('parse ' + s, T.parseOhm(s), v);

// Standard values
eq('stdUp 300', T.stdUp(300), 330); eq('stdUp 150', T.stdUp(150), 150); eq('stdUp 830', T.stdUp(830), 1000); eq('stdUp 90', T.stdUp(90), 100);
eq('stdDown 625', T.stdDown(625), 560); eq('stdDown 1250', T.stdDown(1250), 1200); eq('stdDown 100', T.stdDown(100), 100); eq('stdDown 99', T.stdDown(99), 82);

// Diodes
eq('1N4148', T.decodeDiode(['yellow', 'brown', 'yellow', 'grey']).part, '1N4148');
eq('1N914', T.decodeDiode(['white', 'brown', 'yellow', '']).part, '1N914');
eq('known', !!T.decodeDiode(['yellow', 'black', 'black', 'violet']).known, true);
eq('encode 1N4148', T.encodeDiode('1n4148'), ['yellow', 'brown', 'yellow', 'grey']);
eq('encode with suffix', T.encodeDiode('1N4733A'), ['yellow', 'violet', 'orange', 'orange']);
eq('encode junk', T.encodeDiode('hello'), null);

// Capacitor codes
for (const [s, pf] of [['104', 100000], ['102', 1000], ['473', 47000], ['473J', 47000], ['101', 100], ['22', 22], ['4n7', 4700], ['100n', 100000], ['1u0', 1e6], ['0.1u', 100000], ['229', 2.2], ['108', 0.1]]) near('cap ' + s, T.parseCap(s).pf, pf, 1e-6);
eq('cap tol', T.parseCap('473J').tol, '±5%'); eq('cap junk', T.parseCap('xyz'), null);
eq('code for 100 nF', T.encodeCap(100000), '104'); eq('code for 47 nF', T.encodeCap(47000), '473');

// LED resistor
let r = C.led({ v: 5, vf: 2, ma: 10, n: 1 });
eq('LED 5 V red 10 mA', r.up, 330); near('LED exact', parseFloat(row(r, 'Exact')), 300);
r = C.led({ v: 9, vf: 3, ma: 20, n: 1 }); eq('LED 9 V blue 20 mA', r.up, 330);
r = C.led({ v: 5, vf: 2, ma: 20, n: 1 }); eq('LED exact 150', r.up, 150); eq('no warning at 20 mA', r.warn.length, 0);
eq('LED too many', !!C.led({ v: 5, vf: 2, ma: 10, n: 3 }).err, true);
eq('LED empty', !!C.led({ v: NaN, vf: 2, ma: 10, n: 1 }).err, true);
eq('LED high current warns', C.led({ v: 5, vf: 2, ma: 30, n: 1 }).warn.length > 0, true);
eq('LED hot resistor warns', C.led({ v: 24, vf: 2, ma: 20, n: 1 }).warn.some(w => w.includes('1/4 W')), true);

// Ohm's law
r = C.ohm({ find: 'i', v: 5, r: 1000 }); near('I', r.A, 0.005);
r = C.ohm({ find: 'v', i: 20, r: 220 }); near('V', r.V, 4.4);
r = C.ohm({ find: 'r', v: 5, i: 20 }); near('R', r.R, 250); near('P', r.P, 0.1);
eq('Ohm ignores the found box', C.ohm({ find: 'i', v: 5, r: 100, i: NaN }).err, undefined);

// Divider
r = C.divider({ vin: 9, r1: 10000, r2: 10000 }); near('half', r.out, 4.5); eq('no warnings', r.warn.length, 0);
eq('over 5 V warns', C.divider({ vin: 12, r1: 1000, r2: 10000 }).warn.some(w => w.includes('above 5 V')), true);
eq('high source warns', C.divider({ vin: 9, r1: 100000, r2: 100000 }).warn.some(w => w.includes('10 kΩ')), true);

// Series and parallel
r = C.combine({ list: '220, 220' }); eq('series', r.series, 440); near('parallel', r.parallel, 110);
r = C.combine({ list: '1k, 4k7' }); eq('series k', r.series, 5700);
eq('bad item', !!C.combine({ list: '220, cat' }).err, true); eq('empty list', !!C.combine({ list: '' }).err, true);

// RC
r = C.rc({ r: 10000, c: 100e-6 }); near('tau', r.tau, 1); near('cut-off', r.fc, 0.159);

// Base resistor
r = C.base({ part: 'tip120', vc: 5, ma: 1000 }); near('TIP120 Ib', r.ib, 0.004); eq('TIP120 Rb', r.down, 560);
r = C.base({ part: 'bc547', vc: 5, ma: 50 }); near('BC547 Ib', r.ib, 0.005); eq('BC547 Rb', r.down, 820);
eq('over limit warns', C.base({ part: 'bc547', vc: 5, ma: 200 }).warn.length > 0, true);

// Analog and PWM
r = C.adc({ ref: 5, read: 512, pwm: 128 }); near('volts', r.volts, 2.502); near('duty', r.duty, 0.502); near('avg', r.avg, 2.51);
near('full scale', C.adc({ ref: 5, read: 1023, pwm: 255 }).volts, 5); eq('zero allowed', C.adc({ ref: 5, read: 0, pwm: 0 }).volts, 0);
eq('over range warns', C.adc({ ref: 5, read: 2000, pwm: 10 }).warn.length, 1);

// Ultrasonic
r = C.sonar({ us: 1000, temp: 20 }); near('17 cm', r.cm, 17.17); near('speed', r.speed, 343.4);
eq('0 °C is allowed', C.sonar({ us: 1000, temp: 0 }).err, undefined);
eq('out of range warns', C.sonar({ us: 100, temp: 20 }).warn.length, 1);

// Battery
near('7 hours', C.battery({ mah: 2000, ma: 200 }).hours, 7);

// Robot
r = C.robot({ mm: 65, rpm: 200, track: 13, dist: 50 }); near('speed', r.speed, 68.07); near('turn', r.spin, 0.15); near('go', r.go, 0.7345);

// Regulator
r = C.regulator({ vin: 9, vout: 5, ma: 500 }); near('2 W', r.W, 2); eq('heat warns', r.warn.some(w => w.includes('heat sink')), true);
r = C.regulator({ vin: 9, vout: 5, ma: 200 }); near('0.8 W', r.W, 0.8); eq('OK message', !!r.ok, true);
eq('low headroom warns', C.regulator({ vin: 6, vout: 5, ma: 100 }).warn.some(w => w.includes('2 V')), true);

// Number display
eq('kilo', T.si(1500, 'Ω'), '1.5 kΩ'); eq('milli', T.si(0.0182, 'A'), '18.2 mA'); eq('nano', T.si(1e-7, 'F'), '100 nF'); eq('exact kilo', T.si(1000, 'Ω'), '1 kΩ'); eq('small hertz', T.si(0.159, 'Hz'), '0.159 Hz'); eq('small ohms', T.si(0.07, 'Ω'), '0.07 Ω');
eq('one second', T.span(10000 * 100e-6), '1 second'); eq('seconds', T.span(5), '5 seconds'); eq('minutes', T.span(600), '10 minutes'); eq('hours', T.span(25200), '7 hours');

console.log(`${n - bad} of ${n} checks passed`);
process.exit(bad ? 1 : 0);
