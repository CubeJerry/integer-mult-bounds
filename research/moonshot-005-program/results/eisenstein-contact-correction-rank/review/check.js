
function reviewCorrection(sym,rec){
 const need=(v,m)=>{if(!v)throw Error(m)},dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
 const pc=v=>{let n=0;while(v){v&=v-1;n++}return n};
 const rho=v=>{if(pc(v)===3)return Array.from({length:9},(_,i)=>(v>>i&1)?2:-1);const missing=Array.from({length:9},(_,i)=>i).filter(i=>!(v>>i&1));need(missing.length===2,"root model");return Array.from({length:9},(_,i)=>3*(+(i===missing[0])-+(i===missing[1])));};
 const Z=[7,25,42,52,76,82,97,127].map(rho),P=sym.cycles.map(c=>Z.map(z=>dot(z,rho(c[0]))/9));
 const frac=s=>{const a=s.split("/").map(Number);return a[0]/(a[1]||1)};
 const S=sym.real_matrix.map((r,i)=>r.map((s,j)=>2*frac(s)+ +(i===j)));
 const A=P.map(x=>P.map(y=>dot(x,y))),C=P.map(x=>P.map(y=>dot(x,S.map(r=>dot(r,y)))));
 need(JSON.stringify(A)===JSON.stringify(rec.A40)&&JSON.stringify(C)===JSON.stringify(rec.C40),"reconstructed canonical coordinates");
 const orth=(i,j)=>i!==j&&A[i][j]===0&&C[i][j]===0;
 const pencils=new Set(rec.pencils.map(q=>q.classes.join(",")));need(pencils.size===90,"pencil premise");
 let duals=0;
 for(let i=0;i<40;i++)for(let j=i+1;j<40;j++)if(!orth(i,j)){
   const common=Array.from({length:40},(_,k)=>k).filter(k=>orth(i,k)&&orth(j,k));need(common.length===4&&pencils.has(common.join(",")),"dual pencil");duals++;
 }
 need(duals===540,"complete dual census");
 const selected=[3,8,14,18,20,25],N=selected.map(i=>selected.map(j=>C[i][j]/4));
 need(selected.every((i,a)=>selected.every((j,b)=>a===b||A[i][j]===0)),"six forced real zeros");
 function det(M){const a=M.map(r=>r.map(BigInt)),n=a.length;let old=1n,sign=1n;
  for(let k=0;k<n-1;k++){let q=k;while(q<n&&!a[q][k])q++;if(q===n)return 0n;if(q!==k){[a[q],a[k]]=[a[k],a[q]];sign=-sign}
   const pivot=a[k][k];for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++){const z=a[i][j]*pivot-a[i][k]*a[k][j];need(z%old===0n,"exact Bareiss division");a[i][j]=z/old;}for(let i=k+1;i<n;i++)a[i][k]=0n;old=pivot;
  }return sign*a[n-1][n-1];
 }
 need(det(N)===9n,"six-minor determinant9");

 function rank(M,p=103){const a=M.map(r=>r.map(x=>(x%p+p)%p));let n=0;const inv=x=>{let z=1;for(let k=0;k<p-2;k++)z=z*x%p;return z};
  for(let c=0;c<a[0].length&&n<a.length;c++){let i=n;while(i<a.length&&!a[i][c])i++;if(i===a.length)continue;[a[i],a[n]]=[a[n],a[i]];const d=inv(a[n][c]);a[n]=a[n].map(x=>x*d%p);for(let j=n+1;j<a.length;j++){const v=a[j][c];a[j]=a[j].map((x,k)=>(x-v*a[n][k]%p+p)%p)}n++;}return n;
 }
 const constraints=[];
 for(let i=0;i<40;i++)for(let j=0;j<40;j++)if(i===j||orth(i,j))constraints.push(P[i].flatMap(x=>P[j].map(y=>x*y)));
 const sf=S.flat();need(constraints.length===520&&constraints.every(r=>dot(r,sf)===0),"exact S kernel");
 need(rank(constraints)===63,"independent rank63 modulo103");need(rank(C)===8,"correction rank8 lower witness");
 const wrong=sf.map((x,i)=>x+ +(Math.floor(i/8)===i%8));need(constraints.some(r=>dot(r,wrong)!==0),"S+I forbidden by diagonal");
 const singular=N.map((r,i)=>i===0?r.map(()=>0):r);need(det(singular)===0n,"six-minor zero-row control");
 const I=selected.map(i=>sym.cycles[i][0]);need(JSON.stringify(I)==="[19,38,74,84,97,127]","source normals");
 return{status:"PASS_INDEPENDENT_CORRECTION_RANK_REVIEW",dual_pairs_checked:duals,universal_block_rank_lower:"4V",canonical_six_indices:selected,canonical_six_normals:I,C_over4_determinant:"9",forced_correction_minor_determinant:"-1/3",canonical_block_rank_lower:"6V",ambient_constraints:520,ambient_constraint_rank_mod103:63,exact_kernel:"span(S)",canonical_ambient_correction_rank:"8V",negative_controls:{S_plus_I_rejected:true,zero_row_minor_determinant:"0"},independent_method:"separate dual-neighbor reconstruction, BigInt determinant and prime103 constraint elimination",no_movement_lower_bound:true,no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewCorrection};
 if(require.main===module){
  const fs=require("fs"),crypto=require("crypto"),expected=["ffe061f5986a5982a18fca2ff479447db06cf22b5a8db6bd305c8de3c11315cf","3576da5c2c7254cf38beb551bec076d625cbede9a463f92f00fed57852df856e"];
  if(process.argv.length!==expected.length+2)throw Error("supply the authenticated input JSON paths in documented order");
  const raws=process.argv.slice(2).map(p=>fs.readFileSync(p));
  raws.forEach((b,i)=>{if(crypto.createHash("sha256").update(b).digest("hex")!==expected[i])throw Error("input SHA-256 mismatch "+i)});
  process.stdout.write(JSON.stringify(reviewCorrection(...raws.map(b=>JSON.parse(b))),null,2)+"\n");
 }
}
