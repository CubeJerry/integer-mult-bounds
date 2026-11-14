export function checkCorrection(sym,rec) {
 const fail=m=>{throw Error(m)}, assert=(p,m)=>{if(!p)fail(m)};
 const weight=v=>{let n=0;for(;v;v&=v-1)n++;return n};
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 const rho=v=>{if(weight(v)===3)return Array.from({length:9},(_,i)=>(v>>i)&1?2:-1);const missing=Array.from({length:9},(_,i)=>i).filter(i=>!((v>>i)&1));assert(missing.length===2,"root weight");return Array.from({length:9},(_,i)=>i===missing[0]?3:i===missing[1]?-3:0)};
 const frame=[7,25,42,52,76,82,97,127].map(rho);
 const p=v=>frame.map(z=>dot(rho(v),z)/9);
 const E2=sym.real_matrix.map(r=>r.map(x=>x==="0"?0:x==="1/2"?1:x==="-1/2"?-1:NaN));
 assert(E2.length===8&&E2.every(r=>r.length===8&&r.every(Number.isInteger)),"E matrix");
 const S=E2.map((r,i)=>r.map((x,j)=>x+(i===j?1:0)));
 const matv=(M,v)=>M.map(r=>dot(r,v));
 const P=sym.cycles.map(c=>c.map(p));
 assert(P.length===40&&P.every(c=>c.length===3&&c.every(p=>p.every(Number.isInteger)&&dot(p,p)===4)),"cycle coordinates");
 const A=P.map(x=>P.map(y=>dot(x[0],y[0]))), C=P.map(x=>P.map(y=>dot(x[0],matv(S,y[0]))));
 assert(JSON.stringify(A)===JSON.stringify(rec.A40),"A reconstruction"); assert(JSON.stringify(C)===JSON.stringify(rec.C40),"C reconstruction");
 for(let i=0;i<8;i++)for(let j=0;j<8;j++){assert(S[i][j]===-S[j][i],"S skew");assert(dot(S[i],S.map(r=>r[j]))===(i===j?-3:0),"S square");}
 const orth=(i,j)=>i!==j&&A[i][j]===0&&C[i][j]===0;
 const gains=Array.from({length:40},()=>Array(40).fill(null));
 let badPhasePairs=0;
 assert(rec.nonorthogonal_pair_gains.length===540,"gain count");
 for (const [i,j,k] of rec.nonorthogonal_pair_gains){
  assert(i<j&&!orth(i,j)&&gains[i][j]===null,"gain key");
  gains[i][j]=k;gains[j][i]=(3-k)%3;
  for(let a=0;a<3;a++)for(let b=0;b<3;b++){
   const ac=dot(P[i][a],P[j][b]),cc=dot(P[i][a],matv(S,P[j][b]));
   assert((ac===0)===((b-a-k+6)%3===0),"phase gain");
   assert(3*ac*ac+cc*cc===16,"nonorthogonal modulus");
   if(ac===0){assert(Math.abs(cc)===4,"bad-contact numerator");badPhasePairs++;}
  }
 }
 assert(rec.pencils.length===90,"pencil count");
 const pencilSets=new Map(rec.pencils.map((p,i)=>[p.classes.join(","),i]));
 assert(pencilSets.size===90,"distinct pencils");
 const covered=new Map();
 for(const pencil of rec.pencils){
  assert(pencil.classes.length===4,"pencil size");
  const phases=Object.fromEntries(pencil.phase_witness);
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
   const i=pencil.classes[a],j=pencil.classes[b];assert(i<j&&!orth(i,j),"pencil edge");
   assert(dot(P[i][phases[i]],P[j][phases[j]])===0,"pencil real witness");
   const k=i+","+j;covered.set(k,(covered.get(k)||0)+1);
  }
 }
 assert(covered.size===540&&[...covered.values()].every(x=>x===1),"pencil partition");
 const dual=[];
 for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!orth(i,j)){
  const L=Array.from({length:40},(_,k)=>k).filter(k=>orth(i,k)&&orth(j,k));
  assert(L.length===4&&pencilSets.has(L.join(",")),"dual pencil");
  dual.push({pair:[i,j],pencil_index:pencilSets.get(L.join(",")),classes:L});
 }
 let localCases=0;
 for(const pencil of rec.pencils)for(let code=0;code<81;code++){
  const ph=Array.from({length:4},(_,i)=>Math.floor(code/3**i)%3);let bad=0;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){
   const i=pencil.classes[a],j=pencil.classes[b];
   if((ph[b]-ph[a]-gains[i][j]+6)%3===0)bad++;
  }
  assert(bad>=1,"local pencil bad pair"); localCases++;
 }
 const canonicalBad=dual.filter(x=>A[x.pair[0]][x.pair[1]]===0);
 const witnesses=canonicalBad.map(x=>{
  const L=x.classes;let pair;
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)if(A[L[a]][L[b]]===0)pair=[L[a],L[b]];
  assert(!!pair,"canonical second bad pair");
  return {pair1:x.pair,pair2:pair,C_numerators:[C[x.pair[0]][x.pair[1]],C[pair[0]][pair[1]]]};
 });
 function determinant(M){
  M=M.map(r=>r.map(BigInt));let previous=1n,sign=1n;
  for(let k=0;k<M.length-1;k++){
   let r=k;while(r<M.length&&M[r][k]===0n)r++;if(r===M.length)return 0n;
   if(r!==k){[M[r],M[k]]=[M[k],M[r]];sign=-sign;}
   const pivot=M[k][k];
   for(let i=k+1;i<M.length;i++)for(let j=k+1;j<M.length;j++){
    const numerator=M[i][j]*pivot-M[i][k]*M[k][j];assert(numerator%previous===0n,"exact determinant division");M[i][j]=numerator/previous;
   }
   for(let i=k+1;i<M.length;i++)M[i][k]=0n;previous=pivot;
  }
  return sign*M[M.length-1][M.length-1];
 }
 const canonicalSix=[3,8,14,18,20,25];
 assert(canonicalSix.every(i=>canonicalSix.every(j=>i===j||A[i][j]===0)),"canonical orthogonal six");
 const sixC=canonicalSix.map(i=>canonicalSix.map(j=>C[i][j]));
 assert(determinant(sixC)===36864n,"canonical rank-six determinant");
 function rankMod(M,prime=101){
  M=M.map(r=>r.map(x=>(x%prime+prime)%prime));let rank=0;
  const inverse=x=>{let a=x,b=prime,u=1,v=0;while(b){const q=Math.floor(a/b);[a,b]=[b,a-q*b];[u,v]=[v,u-q*v];}return(u%prime+prime)%prime};
  for(let c=0;c<M[0].length&&rank<M.length;c++){
   let k=rank;while(k<M.length&&!M[k][c])k++;if(k===M.length)continue;
   [M[k],M[rank]]=[M[rank],M[k]];const inv=inverse(M[rank][c]);
   for(let j=c;j<M[0].length;j++)M[rank][j]=M[rank][j]*inv%prime;
   for(let i=rank+1;i<M.length;i++)if(M[i][c]){const a=M[i][c];for(let j=c;j<M[0].length;j++)M[i][j]=(M[i][j]-a*M[rank][j]%prime+prime)%prime;}
   rank++;
  }
  return rank;
 }
 const ambient=[];
 for(let i=0;i<40;i++)for(let j=0;j<40;j++)if(i===j||orth(i,j)){
  const row=P[i][0].flatMap(x=>P[j][0].map(y=>x*y));assert(dot(row,S.flat())===0,"ambient S kernel");ambient.push(row);
 }
 assert(ambient.length===520&&rankMod(ambient)===63,"canonical ambient rank");
 assert(rankMod(C)===8&&rankMod(A)===8,"canonical rank-eight controls");
 return {
  status:"PASS_DUAL_PENCIL_CORRECTION_RANK",
  source_symmetry_git_blob:"8b0fc7779990f0a3ad15494af97f082be3592944",
  source_receipt_git_blob:"599d23ddbc300c78665d8e8079a13cb273bf868a",
  reconstruction:{cycles:40,nonorthogonal_pairs:540,pencils:90,phase_pairs_checked:4860,bad_phase_pairs:badPhasePairs,local_pencil_assignments_checked:localCases},
  dual_pencils:dual,
  canonical_witnesses:witnesses,
  universal_result:{unchanged_base:"H",own_blocks:"I_V",correction_rank_lower:"4V",forced_scalar_minor_determinant:"1/9",field:"Q(sqrt(-3)) or C"},
  canonical_result:{classes:canonicalSix,C_minor:sixC,C_determinant:"36864",forced_correction_determinant:"-1/3",correction_rank_lower:"6V"},
  canonical_ambient_result:{coefficient_unknowns:64,homogeneous_constraints:520,rank_mod_101:63,kernel:"span(S)",required_correction:"-theta*C/12",rank:8,scope:"R_ij = p_i^T T p_j in the canonical phase section"},
  upper_controls:{unchanged_H_to_real_Gram:"(bar(H)-H)/2",canonical_rank:8,rescaled_base:"H/2",added_component:"bar(H)/2",added_rank:4,canonical_result_rank:8},
  no_movement_lower_bound_claimed:true,no_new_kappa:true
 };
}

export function runChecks(sym,rec) {
 const out=checkCorrection(sym,rec), negative=[];
 for(const type of ["delete_pencil","change_gain","alter_E"]) {
  const s=JSON.parse(JSON.stringify(sym)), r=JSON.parse(JSON.stringify(rec));
  if(type==="delete_pencil")r.pencils.pop();
  if(type==="change_gain")r.nonorthogonal_pair_gains[0][2]=(r.nonorthogonal_pair_gains[0][2]+1)%3;
  if(type==="alter_E")s.real_matrix[0][0]="1/2";
  let error="";try{checkCorrection(s,r)}catch(e){error=String(e.message)}
  if(!error)throw Error("negative control escaped: "+type);
  negative.push({type,rejected_at:error});
 }
 out.negative_controls=negative;
 return out;
}

import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 if(process.argv.length!==4)throw Error("usage: node check.mjs SYMMETRY.json predecessor_RESULT.json");
 const paths=process.argv.slice(2);
 const expected=["8b0fc7779990f0a3ad15494af97f082be3592944","599d23ddbc300c78665d8e8079a13cb273bf868a"];
 const inputs=paths.map((path,i)=>{
  const bytes=readFileSync(path);
  const hash=createHash("sha1").update(Buffer.from("blob "+bytes.length+"\0")).update(bytes).digest("hex");
  if(hash!==expected[i])throw Error("source Git blob mismatch: "+path);
  return JSON.parse(bytes.toString("utf8"));
 });
 process.stdout.write(JSON.stringify(runChecks(...inputs),null,2)+"\n");
}
