export function checkTwoStarGap(g){
 const assert=(p,m)=>{if(!p)throw Error(m)},R=g.native_roots,dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),contact=(i,j)=>i===j||dot(R[i],R[j])===0;
 assert(g.native_source_sha256==="51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78","native source pin");
 assert(g.certificate_sha256==="4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc","recovery certificate pin");
 assert(R.length===111&&R.every(r=>r.length===8&&r.every(Number.isInteger)&&dot(r,r)===4),"normalized roots");
 const W=R.map((_,i)=>i).filter(i=>![92,15,106].includes(i)&&[92,15,106].filter(a=>dot(R[i],R[a])===0).length===1),F=[0,14,39,41,60,63,70];
 assert(W.length===76&&F.every(i=>W.includes(i)),"native wing frame");assert(F.every(i=>F.every(j=>i===j||!contact(i,j))),"identity frame");
 const E=W.filter(i=>!F.includes(i)).map(i=>({role:i,ends:F.map((j,a)=>contact(i,j)?a:-1).filter(a=>a>=0)})).filter(e=>e.ends.length===2);
 assert(E.length===20,"twenty edges");const expected=[];for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)if(a!==0||b!==3)expected.push(a+","+b);
 assert(E.every(e=>expected.includes(e.ends.join(",")))&&new Set(E.map(e=>e.ends.join(","))).size===20,"complete graph minus missing edge");
 const degree=Array(7).fill(0);for(const e of E)e.ends.forEach(a=>degree[a]++);
 for(const e of E)for(const f of E)if(e.role!==f.role)assert(contact(e.role,f.role)===!e.ends.some(a=>f.ends.includes(a)),"edge pair mask");
 const A=[0,3],B=[1,2,4,5,6],loops=[{role:85,point:0},{role:107,point:3}];
 for(const z of loops){assert(W.includes(z.role),"loop in wings");assert(F.every((f,a)=>contact(z.role,f)===(a===z.point)),"singleton");assert(E.filter(e=>e.ends.includes(z.point)).every(e=>!contact(z.role,e.role)),"augmented star zero");}
 assert(!contact(85,107),"loop-loop source zero");
 const weights=[],s=Array(7).fill(0);
 for(let e=0;e<E.length;e++)for(const a of E[e].ends){const b=E[e].ends.find(x=>x!==a),w=A.includes(a)?2:A.includes(b)?0:1;weights.push({edge:e,from:a,to:b,weight:w});s[a]+=w;}
 assert(weights.reduce((z,x)=>z+x.weight,0)===40&&weights.filter(x=>A.includes(x.from)).reduce((z,x)=>z+x.weight,0)===20,"weighted coefficients");
 const coefficients=weights.map(x=>{const reverse=weights.find(y=>y.edge===x.edge&&y.from===x.to);const c=s[x.from]-2*(x.weight+reverse.weight);assert(c===(A.includes(x.from)?6:0),"remaining gamma coefficient");return {edge:x.edge,from:x.from,coefficient:c};});
 const paths=[];
 for(const a of A){const c=A.find(x=>x!==a);for(const b of B){const e=E.findIndex(x=>x.ends.includes(a)&&x.ends.includes(b)),f=E.findIndex(x=>x.ends.includes(c)&&x.ends.includes(b));assert(e>=0&&f>=0&&!contact(E[e].role,E[f].role),"two-star path zero");paths.push({a,b,c,first_edge:e,second_edge:f,first_role:E[e].role,second_role:E[f].role});}}
 const formalV=5,formalH=4,gamma=E.map(e=>e.ends.map((a,i)=>A.includes(a)?1:A.includes(e.ends[1-i])?2:1)),G=Array(7).fill(0);
 E.forEach((e,i)=>e.ends.forEach((a,j)=>G[a]+=gamma[i][j]));
 assert(JSON.stringify(G)==="[5,8,8,5,8,8,8]","formal G");
 const lrSlacks=[];
 for(let e=0;e<E.length;e++)for(const a of E[e].ends){const slack=formalH+2*(gamma[e][0]+gamma[e][1])-G[a]-(A.includes(a)?formalV:0);assert(slack>=0,"formal LR");lrSlacks.push(slack);}
 let crossCount=0;
 for(const a of A)for(let e=0;e<E.length;e++)if(E[e].ends.includes(a)){
  const b=E[e].ends.find(x=>x!==a),ge=gamma[e][E[e].ends.indexOf(a)];
  for(let f=0;f<E.length;f++)if(f!==e&&E[f].ends.includes(b)){const c=E[f].ends.find(x=>x!==b),gf=gamma[f][E[f].ends.indexOf(c)];assert(2*gf+4*ge===formalV-formalH+G[a],"formal cross equality");crossCount++;}
 }
 const rows=W.map(i=>W.reduce((r,j,k)=>contact(i,j)?r|(1n<<BigInt(k)):r,0n)),basis=new Map();for(let x of rows){while(x){const k=x.toString(2).length-1;if(basis.has(k))x^=basis.get(k);else{basis.set(k,x);break;}}}assert(basis.size===9,"canonical rank nine");
 return {status:"PASS_TWO_AUGMENTED_STARS_WING_GAP",source_geometry_git_blob:"8eba43d142c819c206dce5df87ea4571aaead287",native_source_sha256:g.native_source_sha256,recovery_certificate_sha256:g.certificate_sha256,wing_roles:W,frame:F,edges:E,degree,loops,classes:{A,B},weights,star_weight_sums:s,weighted_gamma_coefficients:coefficients,cross_paths:paths,
 theorem:{all_fields:true,all_positive_widths:true,rank_lower:"44V/5",characteristic_two_upper:"9V",exact_minimum_at_widths:[1,2,3,4],minimum_at_these_widths:"9V",first_unexcluded_fractional_candidate:"V=5, rank44"},
 inequalities:["40h >= 20V+6(G_0+G_3)","G_0+G_3 >= 10(V-h)","100h >= 80V"],
 formal_relaxation_point:{V:formalV,h:formalH,j:formalV+formalH,G,directed_gamma:gamma,LR_slacks:lrSlacks,cross_inequalities_checked:crossCount,all_cross_equalities:true,not_an_actual_fitting:true},
 no_packet_lifetime_or_MOVE_bound:true,no_new_kappa:true};
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
 process.stdout.write(JSON.stringify(checkTwoStarGap(JSON.parse(bytes.toString("utf8"))),null,2)+"\n");
}
