function checkTwoD5NegativeControls(base,geometry) {
 const tests=[
 ["omit first local correction",w=>{w.operations=w.operations.filter(o=>JSON.stringify(o)!==JSON.stringify(["ADD","A","P"]));}],
 ["omit second local correction",w=>{w.operations=w.operations.filter(o=>JSON.stringify(o)!==JSON.stringify(["ADD","B","Q"]));}],
 ["omit canonical cancellation",w=>{w.operations=w.operations.filter(o=>JSON.stringify(o)!==JSON.stringify(["ADD","Q","P"]));}],
 ["omit foreign decoder",w=>{w.operations=w.operations.filter(o=>JSON.stringify(o)!==JSON.stringify(["ADD","F","Y72"]));}],
 ["visit incomparable source charts",w=>{const k=w.operations.findIndex(o=>o[0]==="MOVE"&&o[1]==="X72");w.operations.splice(k,0,["MOVE","X72","D1"],["MOVE","X72","D2"]);}],
 ["remove retained source copy",w=>{w.operations=w.operations.filter(o=>!((o[0]==="INIT"&&o[1]==="R1")||(o[0]==="ADD"&&o[2]==="R1")));}],
 ["omit own canonical coefficient",w=>{const k=w.operations.findIndex(o=>o[0]==="ADD"&&o[1]==="X72"&&o[2]==="Q");w.operations.splice(k,1);}]
 ];const results=[];
 for(const [name,mutate] of tests){const w=JSON.parse(JSON.stringify(base));mutate(w);let rejected=false;try{checkPayloadFork(w,geometry);}catch(e){rejected=true;results.push({name,status:"REJECT",reason:String(e.message)});}if(!rejected)throw Error("negative control passed: "+name);}
 return results;
}
