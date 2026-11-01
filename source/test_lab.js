// Runs all 25 examples through the automatic check, plus fault-injection tests of the engine.
require('./lab_engine.js'); require('./lab_examples.js');
const { Sim, runCheck, compileSketch } = globalThis.ELab, EX = globalThis.ELAB_EXAMPLES;
let fail = 0;
const ok = (c, s) => { if (!c) { fail++; console.log('  FAIL ' + s); } };
for (const e of EX) {
  const t0 = Date.now(), r = runCheck(e, e.c, e.code, 'R3');
  const bad = r.results.filter(x => !x.ok), hard = r.warns.filter(w => w.sev === 'bad');
  console.log(`${String(e.n).padStart(2)} ${e.title.padEnd(36)} ${bad.length ? 'FAIL' : 'pass'} ${r.results.length} checks ${Date.now() - t0}ms` + (r.warns.length ? '  warns: ' + r.warns.map(w => w.msg.slice(0, 70)).join(' | ') : ''));
  bad.forEach(b => { fail++; console.log('   X ' + b.say); });
  if (hard.length) { fail++; console.log('   hard warnings on a preset'); }
}
console.log('--- engine behaviour');
const ex2 = EX[1];
// 1. LED with no resistor burns and warns.
{ const c = { parts: [{ id: 'L', type: 'led', color: 'red', legs: { a: 'c5', k: 'c6' } }], wires: [['5V', 'a5'], ['a6', 'GND']] };
  const s = new Sim(c, 'void setup(){} void loop(){}'); s.step(50);
  ok(s.part('L').st.burned, 'LED with no resistor should burn'); console.log('  no resistor:', [...s.warns.values()].map(w => w.msg.slice(0, 60))); }
// 2. Short circuit.
{ const s = new Sim({ parts: [], wires: [['5V', 'GND']] }, 'void setup(){} void loop(){}'); s.step(20); ok(s.warns.has('short5'), 'short should warn'); }
// 3. LED backwards stays dark.
{ const c = JSON.parse(JSON.stringify(ex2.c)); const l = c.parts.find(p => p.type === 'led'); [l.legs.a, l.legs.k] = [l.legs.k, l.legs.a];
  const r = runCheck(ex2, c, ex2.code, 'R3'); ok(!r.results[0].ok, 'reversed LED should fail the check'); }
// 4. R4 pin limit warns on 220 ohm.
{ const r = runCheck(ex2, ex2.c, ex2.code, 'R4'); ok(r.warns.some(w => /R4/.test(w.msg)), 'R4 should warn at 14 mA'); console.log('  R4:', r.warns.map(w => w.msg.slice(0, 80))); }
// 5. Currents are right: 3 V across 220+25+12 ohm.
{ const s = new Sim(ex2.c, 'void setup(){pinMode(8,OUTPUT);digitalWrite(8,HIGH);} void loop(){}'); s.step(50); const i = s.part('LED1').st.i * 1000; console.log('  LED current mA', i.toFixed(2)); ok(Math.abs(i - 11.67) < 0.6, 'LED current expected near 11.7 mA'); }
// 6. Motor straight on a pin warns.
{ const c = { parts: [{ id: 'M', type: 'motor', legs: { a: 'c5', b: 'c6' } }], wires: [['D5', 'a5'], ['a6', 'GND']] };
  const s = new Sim(c, 'void setup(){pinMode(5,OUTPUT);digitalWrite(5,HIGH);} void loop(){}'); s.step(30); ok(s.warns.has('pin5'), 'motor on pin should overload'); }
// 7. Reversed flyback diode shorts the battery when on.
{ const e = EX[15], c = JSON.parse(JSON.stringify(e.c)); const d = c.parts.find(p => p.type === 'diode'); [d.legs.a, d.legs.k] = [d.legs.k, d.legs.a];
  const r = runCheck(e, c, e.code, 'R3'); console.log('  reversed diode:', r.warns.map(w => w.msg.slice(0, 70))); ok(r.warns.some(w => /Short|rated/.test(w.msg)), 'reversed diode should warn'); }
// 8. Missing diode warns.
{ const e = EX[15], c = JSON.parse(JSON.stringify(e.c)); c.parts = c.parts.filter(p => p.type !== 'diode'); const r = runCheck(e, c, e.code, 'R3'); ok(r.warns.some(w => /flyback/.test(w.msg)), 'no diode should warn'); }
// 9. Capacitor backwards warns.
{ const e = EX[13], c = JSON.parse(JSON.stringify(e.c)); const d = c.parts.find(p => p.type === 'cap'); [d.legs.p, d.legs.n] = [d.legs.n, d.legs.p]; const r = runCheck(e, c, e.code, 'R3'); ok(r.warns.some(w => /backwards/.test(w.msg)), 'reversed cap should warn'); }
// 10. Compile errors are friendly.
for (const [src, want] of [
  ['void setup(){ pinMode(8, OUTPUT) }\nvoid loop(){}', /semicolon/], ['void setup(){ digitalRite(8, HIGH); }\nvoid loop(){}', /digitalWrite/],
  ['void setup(){ x = 3; }\nvoid loop(){}', /variable "x"/], ['void loop(){}', /setup/], ['void setup(){ Serial.println("a); }\nvoid loop(){}', /closing/],
  ['void setup(){ serial.begin(9600); }\nvoid loop(){}', /Serial/],
]) { let m = ''; try { compileSketch(src); } catch (e) { m = `line ${e.line}: ${e.message}`; } console.log('  ' + m); ok(want.test(m), 'error for: ' + src); }
// 11. Language: integer division, floats, arrays, functions, ++, ternary, strings.
{ const s = new Sim({ parts: [], wires: [] }, `int a[] = {1,2,3};
long sq(int v){ return (long)v*v; }
void setup(){ Serial.begin(9600); int x=7; Serial.println(x/2); float f=7/2.0; Serial.println(f); Serial.println(sq(300));
 a[1]+=5; Serial.println(a[1]); int y=x++; Serial.println(y); Serial.println(x>3?10:20); String t="v="; t+=4; Serial.println(t);
 byte b=255; b++; Serial.println(b); int o=32767; o++; Serial.println(o); char c='A'; Serial.println(c); for(int i=0;i<5;i++){ if(i==2) continue; if(i==4) break; Serial.print(i);} Serial.println(""); }
void loop(){}`);
  s.step(20); console.log('  ' + JSON.stringify(s.serial), s.err || ''); ok(s.serial === '3\n3.50\n90000\n7\n7\n10\nv=4\n0\n-32768\nA\n013\n', 'language semantics'); }
// 12. Infinite loop doesn't hang.
{ const s = new Sim({ parts: [], wires: [] }, 'void setup(){ while(true){} } void loop(){}'); const t = Date.now(); s.step(100); ok(Date.now() - t < 1500, 'busy loop should stay bounded'); }
console.log(fail ? `FAILED ${fail}` : 'ALL PASSED');
