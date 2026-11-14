
function reviewRankFour(s, receipt) {
 const need=(ok,m)=>{if(!ok)throw Error(m)},dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
 const wt=v=>{let c=0;while(v){v&=v-1;c++}return c};
 const rho=v=>wt(v)===3?Array.from({length:9},(_,i)=>(v>>>i&1)?2:-1):Array.from({length:9},(_,i)=>{const off=Array.from({length:9},(_,k)=>k).filter(k=>!(v>>>k&1));need(off.length===2,"weight");return 3*(+(i===off[0])-+(i===off[1]));});
 const normals=Array.from({length:512},(_,i)=>i).filter(v=>[3,7].includes(wt(v)));
 const real=new Map(normals.map(v=>[v,rho(v)]));
 const reflect=(x,a)=>{const t=dot(x,a);need(t%9===0,"integral reflection on roots");return x.map((v,i)=>v-t/9*a[i]);};
 const E=(x,reverse=false)=>s.A2_planes.reduce((v,p)=>{const q=reverse?[...p].reverse():p;for(const n of q)v=reflect(v,real.get(n));return v},x);
 const cycles=s.cycles;need(cycles.length===40&&new Set(cycles.flat()).size===120,"cycle partition");
 const same=(a,b)=>a.every((v,i)=>v===b[i]);
 const orientations=[];
 for(const rev of [false,true]){
   let ok=true;
   for(const cycle of cycles)for(let i=0;i<3;i++){
      const v=cycle[i],n=cycle[(i+1)%3],sgn=s.canonical_root_signs[String(v)];
      if(!same(E(real.get(v),rev),real.get(n).map(x=>x*sgn)))ok=false;
   }
   if(ok)orientations.push(rev);
 }
 need(orientations.length===1,"reflection orientation unique");
 const rev=orientations[0], Z=[7,25,42,52,76,82,97,127],zr=Z.map(v=>real.get(v));
 for(let i=0;i<8;i++)for(let j=0;j<8;j++)need(dot(zr[i],zr[j])===18*+(i===j),"orthogonal frame");
 const Etwice=zr.map(a=>zr.map(b=>dot(a,E(b,rev))/9));
 const parse=x=>{const a=x.split("/").map(Number);return a[0]/(a[1]||1)};
 need(Etwice.every((row,i)=>row.every((x,j)=>x===2*parse(s.real_matrix[i][j]))),"reflection matrix agrees source");
 const S=Etwice.map((r,i)=>r.map((x,j)=>x+ +(i===j)));
 for(let i=0;i<8;i++)for(let j=0;j<8;j++){
  need(S[i][j]===-S[j][i],"skew");
  need(S[i].reduce((a,x,k)=>a+x*S[k][j],0)===-3*+(i===j),"complex structure");
 }
 const p=new Map(normals.map(v=>[v,zr.map(z=>dot(z,real.get(v))/9)]));
 for(const q of p.values())need(q.every(Number.isInteger)&&dot(q,q)===4,"normalized coordinates");
 const rdot=(v,w)=>dot(real.get(v),real.get(w));
 const ca=(v,w)=>dot(p.get(v),p.get(w));
 const cc=(v,w)=>dot(p.get(v),S.map(row=>dot(row,p.get(w))));
 let binaryContactPairs=0;
 for(let i=0;i<normals.length;i++)for(let j=i+1;j<normals.length;j++){
  need((rdot(normals[i],normals[j])===0)===(wt(normals[i]&normals[j])%2===1),"binary contact convention");binaryContactPairs++;
 }
 const reps=cycles.map(c=>c[0]),A=reps.map(v=>reps.map(w=>ca(v,w))),C=reps.map(v=>reps.map(w=>cc(v,w)));
 need(JSON.stringify(A)===JSON.stringify(receipt.A40)&&JSON.stringify(C)===JSON.stringify(receipt.C40),"independent matrices");
 function rank(M,prime=103){
   const m=M.map(r=>r.map(x=>(x%prime+prime)%prime));let k=0;
   const pow=(a,n)=>{let b=1;while(n){if(n&1)b=b*a%prime;a=a*a%prime;n>>=1}return b};
   for(let c=0;c<m[0].length&&k<m.length;c++){
    let q=k;while(q<m.length&&!m[q][c])q++;if(q===m.length)continue;
    [m[q],m[k]]=[m[k],m[q]];const inv=pow(m[k][c],prime-2);for(let j=c;j<m[k].length;j++)m[k][j]=m[k][j]*inv%prime;
    for(let i=k+1;i<m.length;i++){const h=m[i][c];for(let j=c;j<m[i].length;j++)m[i][j]=(m[i][j]-h*m[k][j]%prime+prime)%prime}k++;
   }return k;
 }
 const rankH=rank(A.map((r,i)=>r.map((a,j)=>3*a+10*C[i][j])));need(rankH===4&&rank(A)===8&&rank(C)===8,"independent prime rank witnesses");
 let forbidden=0;const gains=[],adj=Array.from({length:40},()=>Array(40).fill(0));
 for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){
    const zero=A[i][j]===0&&C[i][j]===0;
    adj[i][j]=adj[j][i]=+zero;
    if(zero)continue;
    const ks=[0,1,2].filter(k=>rdot(reps[i],cycles[j][k])===0);
    need(ks.length===1,"unique contact phase");const k=ks[0];
    for(let a=0;a<3;a++)for(let b=0;b<3;b++)need((rdot(cycles[i][a],cycles[j][b])===0)===((b-a+3)%3===k),"phase gain");
    gains.push([i,j,k]);if(k===0)forbidden++;
 }
 need(gains.length===540&&forbidden===176,"contact counts");
 const classes=new Map(cycles.flatMap((c,i)=>c.map(v=>[v,i]))),covered=new Set();
 need(receipt.pencils.length===90,"ninety witnesses");
 function addPencil(q,set){
  const vs=q.root_witness,cl=vs.map(v=>classes.get(v));need(new Set(cl).size===4,"distinct cycles");
  for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){
   const ci=cl[i],cj=cl[j];need(rdot(vs[i],vs[j])===0,"real contact");
   need(!(ca(vs[i],vs[j])===0&&cc(vs[i],vs[j])===0),"complex nonorthogonal");
   const key=[ci,cj].sort((a,b)=>a-b).join(",");need(!set.has(key),"duplicate edge");set.add(key);
  }
 }
 for(const q of receipt.pencils)addPencil(q,covered);
 need(covered.size===540&&gains.every(([i,j])=>covered.has([i,j].join(","))),"complete edge partition");
 let rejected=false;try{addPencil(receipt.pencils[0],covered)}catch(e){rejected=e.message==="duplicate edge"}need(rejected,"negative duplicate-pencil control");
 for(let i=0;i<40;i++)for(let j=0;j<40;j++){
  const b2=adj[i].reduce((z,x,k)=>z+x*adj[k][j],0);
  need(b2===8*+(i===j)-2*adj[i][j]+4,"orthogonality adjacency identity");
 }
 const dualRank=rank(adj.map((r,i)=>r.map((x,j)=>2*+(i===j)-x)));need(dualRank===16,"dual rank");
 const wrongCoefficientRank=rank(A.map((r,i)=>r.map((a,j)=>3*a+20*C[i][j])));
 need(wrongCoefficientRank===8,"wrong Hermitian coefficient control");
 // Matrix projector rank upper bound, without the author's 40 by 40 tight-frame identity.
 const projector12=S.map((r,i)=>r.map((x,j)=>3*+(i===j)+10*x));
 const projectorRank=rank(projector12);need(projectorRank===4,"complex projector rank");
 return {
 status:"PASS_INDEPENDENT_REFLECTION_AND_PENCIL_REVIEW",
 source_sha256:"ffe061f5986a5982a18fca2ff479447db06cf22b5a8db6bd305c8de3c11315cf",
 real_root_model:"nine dimensional integer sum-zero roots", reflection_application_order:rev?"reverse within each source A2 pair":"listed order within each source A2 pair",
 binary_contact_pairs_checked:binaryContactPairs,prime:103,square_root_of_minus_three:10,rank_H_mod103:rankH,
 rank_real_parts_mod103:[rank(A),rank(C)],projector_rank_mod103:projectorRank,
 forbidden_nonzero_contacts_canonical:forbidden,edge_disjoint_pencils:90,edge_partition_size:covered.size,
 universal_bad_contacts_at_least:90,complementary_fitting_rank:dualRank,
 negative_controls:{duplicate_pencil_rejected:rejected,wrong_coefficient_rank:wrongCoefficientRank},
 independent_method:"Rebuilt E from real A2 reflections; independently checked supplied witnesses without author's clique enumerator or matrix multiplication identity",
 no_new_kappa:true
 };
}

if(typeof module!=="undefined"){
 module.exports={reviewRankFour};
 if(require.main===module){
  const fs=require("fs"),crypto=require("crypto");
  if(process.argv.length!==4)throw Error("usage: node check.js SYMMETRY.json author_RESULT.json");
  const s=fs.readFileSync(process.argv[2]),r=fs.readFileSync(process.argv[3]);
  const hash=b=>crypto.createHash("sha256").update(b).digest("hex");
  if(hash(s)!=="ffe061f5986a5982a18fca2ff479447db06cf22b5a8db6bd305c8de3c11315cf"||hash(r)!=="3576da5c2c7254cf38beb551bec076d625cbede9a463f92f00fed57852df856e")throw Error("source or receipt SHA-256 mismatch");
  process.stdout.write(JSON.stringify(reviewRankFour(JSON.parse(s),JSON.parse(r)),null,2)+"\n");
 }
}
