require('./lab_engine.js');
const {Sim,compileSketch}=globalThis.ELab,S=require('./sensors.json');let bad=0;
for(const r of S){ if(!r.code) continue; try{compileSketch(r.code);}catch(e){bad++;console.log('COMPILE',r.title,'line',e.line,e.message);continue;}
 const s=new Sim({parts:[],wires:[]},r.code);s.step(2000);if(s.err){bad++;console.log('RUN',r.title,s.err);} }
console.log(bad?'BAD '+bad:'all sensor sketches compile and run');
