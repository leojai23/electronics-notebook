require('./lab_engine.js'); require('./robot_engine.js');
const {runRobotCheck,makeSim}=globalThis.ERobot, R=require('./robots.json');
let bad=0;
for(const r of R){ if(!r.code) continue; const t=Date.now(), o=runRobotCheck(r.n,r.code); const f=o.results.filter(x=>!x.ok);
 console.log(String(r.n).padStart(2),r.title.padEnd(34),f.length?'FAIL':'pass',o.results.length,'checks',(Date.now()-t)+'ms',o.warns.length?'warns: '+o.warns.map(w=>w.msg.slice(0,60)).join(' | '):'');
 o.results.forEach(x=>{ if(!x.ok){bad++;console.log('    X',x.say);} else if(/this run|furthest/.test(x.say)) console.log('    .',x.say);});
}
console.log(bad?`FAILED ${bad}`:'ALL ROBOT CHECKS PASS');
