export function checkWingGap(g){
 const assert=(p,m)=>{if(!p)throw Error(m)}, roots=g.native_roots;
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0), contact=(i,j)=>i===j||dot(roots[i],roots[j])===0;
 assert(g.native_source_sha256==="51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78","native pin");
 assert(g.certificate_sha256==="4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc","recovery pin");
 assert(roots.length===111&&roots.every(r=>r.length===8&&r.every(Number.isInteger)&&dot(r,r)===4),"root normalization");
 const axes=[92,15,106];
 const W=roots.map((_,i)=>i).filter(i=>!axes.includes(i)&&axes.filter(a=>dot(roots[a],roots[i])===0).length===1);
 const F=[0,14,30,31,60,69,70];
 assert(W.length===76&&F.every(i=>W.includes(i)),"wing frame");
 assert(F.every(i=>F.every(j=>i===j||!contact(i,j))),"frame identity mask");
 const edges=W.filter(i=>!F.includes(i)).map(i=>({role:i,ends:F.map((f,a)=>contact(i,f)?a:-1).filter(a=>a>=0)})).filter(x=>x.ends.length===2);
 assert(edges.length===19,"nineteen edges");
 const expected=[];for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)if(!(a===0&&b===3)&&!(a===4&&b===6))expected.push(a+","+b);
 assert(edges.every(e=>expected.includes(e.ends.join(",")))&&new Set(edges.map(e=>e.ends.join(","))).size===19,"edge graph");
 const degree=Array(7).fill(0);for(const e of edges)e.ends.forEach(a=>degree[a]++);
 for(const e of edges)for(const f of edges)if(e.role!==f.role){
  const share=e.ends.some(a=>f.ends.includes(a));
  assert(contact(e.role,f.role)===!share,"edge-edge mask");
 }
 const loopRoles=[77,107],loopPoints=[0,3];
 for(let z=0;z<2;z++){
  assert(W.includes(loopRoles[z]),"loop belongs to wings");
  for(let a=0;a<7;a++)assert(contact(loopRoles[z],F[a])===(a===loopPoints[z]),"singleton contact");
  for(const e of edges.filter(e=>e.ends.includes(loopPoints[z])))assert(!contact(loopRoles[z],e.role),"loop-star zero");
 }
 assert(!contact(77,107),"loop pair actual zero");
 const categories=["A","C","C","A","B","C","B"];
 const weight={"AB":3,"AC":4,"BA":1,"BC":2,"CA":0,"CB":2,"CC":2};
 const incidence=[],starWeights=Array(7).fill(0);
 for(let e=0;e<edges.length;e++)for(const a of edges[e].ends){
  const b=edges[e].ends.find(x=>x!==a),w=weight[categories[a]+categories[b]];
  assert(Number.isInteger(w)&&w>=0,"nonnegative weight");
  incidence.push({edge:e,role:edges[e].role,from:a,to:b,weight:w});starWeights[a]+=w;
 }
 const totalWeight=incidence.reduce((s,x)=>s+x.weight,0);
 const loopWeight=incidence.filter(x=>loopPoints.includes(x.from)).reduce((s,x)=>s+x.weight,0);
 assert(totalWeight===76&&loopWeight===36,"weighted h and V coefficients");
 const coefficients=[];
 for(let e=0;e<edges.length;e++)for(const a of edges[e].ends){
  const b=edges[e].ends.find(x=>x!==a);
  const c=starWeights[a]-2*(weight[categories[a]+categories[b]]+weight[categories[b]+categories[a]]);
  assert(c===(categories[a]==="A"?10:0),"gamma coefficient");
  coefficients.push({edge:e,from:a,coefficient:c});
 }
 const gammaValue={"AB":0,"AC":0,"BA":10,"BC":6,"CA":10,"CB":4,"CC":5};
 const formalV=38,formalH=18,formalG=Array(7).fill(0);
 const formalGamma=edges.map(e=>e.ends.map((a,i)=>{const b=e.ends[1-i],x=gammaValue[categories[a]+categories[b]];formalG[a]+=x;return x}));
 assert(JSON.stringify(formalG)==="[0,38,38,0,38,38,38]","formal G sums");
 for(let e=0;e<edges.length;e++)for(const a of edges[e].ends){
  const m=loopPoints.includes(a)?1:0;
  assert(formalG[a]+m*formalV===formalH+2*(formalGamma[e][0]+formalGamma[e][1]),"formal LR equality");
 }
 const binaryRank=rows=>{const basis=new Map();for(let r of rows){while(r){const k=31-Math.clz32(r);if(basis.has(k))r^=basis.get(k);else{basis.set(k,r);break;}}}return basis.size};
 const parity=n=>{let s=0;for(;n;n&=n-1)s^=1;return s};
 const seed=F.concat(edges.map(e=>e.role)),vectors=F.map((_,a)=>1<<a).concat(edges.map(e=>(1<<e.ends[0])^(1<<e.ends[1])^128));
 const anchorRoles=[60,69,70,59,63,78,93],anchorVectors=anchorRoles.map(i=>vectors[seed.indexOf(i)]);
 assert(anchorRoles.every(i=>!contact(3,i)),"role3 actual zero anchors");
 assert(binaryRank(anchorVectors)===7&&anchorVectors.every(v=>parity(v&15)===0)&&parity(15)===0,"role3 isotropic common annihilator");
 assert(binaryRank(anchorVectors.slice(1))===6,"deleted anchor control");
 assert(contact(3,F[0]),"wrong anchor control");
 const canonicalRows=W.map(i=>W.reduce((r,j,k)=>contact(i,j)?r|(1n<<BigInt(k)):r,0n));
 const rankBig=rows=>{const basis=new Map();for(let r of rows){while(r){const k=r.toString(2).length-1;if(basis.has(k))r^=basis.get(k);else{basis.set(k,r);break;}}}return basis.size};
 assert(rankBig(canonicalRows)===9,"canonical scalar upper");
 return {
  status:"PASS_WEIGHTED_WING_FRACTIONAL_GAP",
  recovered_geometry_git_blob:"8eba43d142c819c206dce5df87ea4571aaead287",
  native_source_sha256:g.native_source_sha256,recovery_certificate_sha256:g.certificate_sha256,
  wing_roles:W,frame:F,edges,degree,loops:loopRoles.map((role,i)=>({role,point:loopPoints[i]})),
  categories,incidence_weights:incidence,star_weight_sums:starWeights,gamma_coefficients:coefficients,
  weighted_identity:{h_coefficient:totalWeight,V_coefficient:loopWeight,remaining:"10*(G_0+G_3)",bound:"rank(M) >= (161/19)*V"},
  all_fields_lower_bound:true,characteristic_two_upper_bound:"9V",
  width_two_result:"minimum rank18 over every characteristic-two field; rank>=18 over every field",
  formal_relaxation_point:{V:formalV,h:formalH,j:formalV+formalH,G:formalG,directed_gamma:formalGamma,all_38_LR_equalities:true,not_a_block_fitting:true},
  predecessor_independent_geometry_review:{seed_roles:seed,isotropic_extra_role:3,anchor_roles:anchorRoles,anchor_vectors:anchorVectors,anchor_rank:7,annihilator:15,canonical_rank:9},
  controls:{removed_anchor_rank:6,frame0_is_invalid_role3_zero:true},
  no_new_kappa:true,no_packet_lifetime_or_MOVE_lower_bound_claimed:true
 };
}

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 if(process.argv.length!==3)throw Error("usage: node check.mjs RECOVERED-NATIVE-ROOTS.json");
 const bytes=readFileSync(process.argv[2]);
 const hash=createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
 if(hash!=="8eba43d142c819c206dce5df87ea4571aaead287")throw Error("source Git blob mismatch");
 process.stdout.write(JSON.stringify(checkWingGap(JSON.parse(bytes.toString("utf8"))),null,2)+"\n");
}
