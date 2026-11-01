require('./lab_engine.js');
const {Sim,compileSketch}=globalThis.ELab, R=require('./robots.json');
let bad=0;
for(const r of R){ if(!r.code) continue;
  try{ compileSketch(r.code);}catch(e){bad++;console.log('COMPILE',r.n,r.title,'line',e.line,e.message);console.log(r.code.split('\n')[e.line-1]);continue;}
  const s=new Sim({parts:[],wires:[]},r.code); s.step(3000);
  if(s.err){bad++;console.log('RUN',r.n,r.title,s.err);} 
  const w=[...s.warns.values()].filter(x=>!/floating|wanders|never triggered|no power/.test(x.msg)); if(w.length) console.log(' note',r.n,w.map(x=>x.msg.slice(0,70)));
}
console.log(bad?`BAD ${bad}`:'all robot sketches compile and run');
