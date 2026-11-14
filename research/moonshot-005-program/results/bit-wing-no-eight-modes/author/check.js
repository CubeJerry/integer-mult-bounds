function checkWingStrict(g){
const need=(b,m)=>{if(!b)throw Error(m);},R=g.native_roots,dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0);
need(g.native_source_sha256==="51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78","source provenance");
need(R.length===111&&R.every(r=>r.length===8&&r.every(Number.isInteger)&&dot(r,r)===4),"normalized roots");
const axes=[92,15,106],W=R.map((_,i)=>i).filter(i=>!axes.includes(i)&&axes.filter(a=>dot(R[a],R[i])===0).length===1),F=[0,14,30,31,60,69,70];need(W.length===76&&F.every(i=>W.includes(i)),"wing frame");
for(let i=0;i<7;i++)for(let j=0;j<i;j++)need(dot(R[F[i]],R[F[j]])!==0,"noncontact frame");
const E=W.filter(i=>!F.includes(i)).map(i=>({role:i,endpoints:F.map((j,k)=>dot(R[i],R[j])===0?k:-1).filter(k=>k>=0)})).filter(e=>e.endpoints.length===2),degree=Array(7).fill(0),pairs=new Set();need(E.length===19,"edge count");
for(const e of E){e.endpoints.forEach(a=>degree[a]++);pairs.add(e.endpoints.join(","));}need(pairs.size===19&&degree.every(x=>x>=5),"saturated star");
const missing=[];for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)if(!pairs.has([a,b].join(",")))missing.push([a,b]);need(JSON.stringify(missing)==="[[0,3],[4,6]]","missing edges");
for(let i=0;i<E.length;i++)for(let j=0;j<i;j++){const share=E[i].endpoints.some(a=>E[j].endpoints.includes(a));need((dot(R[E[i].role],R[E[j].role])!==0)===share,"actual star mask");}
const roles=F.concat(E.map(e=>e.role)),vectors=F.map((_,a)=>1<<a).concat(E.map(e=>(1<<e.endpoints[0])^(1<<e.endpoints[1])^128)),witness=[60,69,70,59,63,78,93],rows=witness.map(i=>vectors[roles.indexOf(i)]);
const rank=A=>{const p=new Map();for(let x of A){while(x){const k=31-Math.clz32(x);if(p.has(k))x^=p.get(k);else{p.set(k,x);break;}}}return p.size;},parity=x=>{let s=0;while(x){s^=1;x&=x-1;}return s;};
need(W.includes(3)&&!roles.includes(3)&&witness.every(i=>roles.includes(i)&&dot(R[3],R[i])!==0),"actual role3 zeros");need(rank(rows)===7&&rows.every(r=>parity(r&15)===0)&&parity(15)===0,"isotropic annihilator");
const K=W.map(i=>W.reduce((m,j,k)=>m|((i===j||dot(R[i],R[j])===0)?1n<<BigInt(k):0n),0n)),rankBig=A=>{const p=new Map();for(let x of A){while(x){const k=x.toString(2).length-1;if(p.has(k))x^=p.get(k);else{p.set(k,x);break;}}}return p.size;};need(rankBig(K)===9,"canonical rank9");
need(rank(rows.slice(1))===6&&dot(R[3],R[F[0]])===0,"negative controls");
const loops=[{role:77,point:0},{role:107,point:3}];for(const z of loops){need(W.includes(z.role),"loop inwings");need(F.every((f,i)=>(dot(R[z.role],R[f])===0)===(i===z.point)),"loop singleton");need(E.filter(e=>e.endpoints.includes(z.point)).every(e=>dot(R[z.role],R[e.role])!==0),"loop zero allincidentedges");}
return {status:"PASS_NATIVE_76_WING_NO_EIGHT_MODE_CERTIFICATE",source_provenance:g.native_source_sha256,recovered_geometry_blob:"8eba43d142c819c206dce5df87ea4571aaead287",recovery_certificate_sha256:g.certificate_sha256,wing_roles:W,frame:F,edges:E,degree,missing_edges:missing,seed_roles:roles,canonical_star_vectors_8bit:vectors,extra_role:3,noncontact_witness_roles:witness,witness_vectors_8bit:rows,witness_rank:7,isotropic_annihilator_8bit:15,annihilator_weight:4,canonical_wing_rank:9,augmented_star_loop_roles:loops,negative_controls:{deleted_anchor_rank:6,substituted_frame0_is_contact:true},theorem:"All characteristic-two fields and V>=1: fitting rank>8V. Scalar minimum9. No all-width9V lower bound asserted.",scope:"Derived authenticated certificate geometry, not fresh native gzip replay. No physical supplier or new kappa."};
}
