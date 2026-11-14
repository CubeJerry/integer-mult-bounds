export function checkSingularSplit(g) {
 const R=g.native_roots,assert=(x,m)=>{if(!x)throw Error(m)},dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0);
 assert(R.length===111,"native source length");
 const rank=rows=>{const B=new Map();let n=0;for(let x of rows){while(x){const k=x.toString(2).length-1;if(B.has(k))x^=B.get(k);else{B.set(k,x);n++;break}}}return n};
 const par=x=>{let z=0;while(x){z^=x&1;x>>=1}return z};
 const p=103,inv=a=>{let x=1;for(let j=0;j<101;j++)x=x*a%p;return x};
 const rr=rows=>{const M=rows.map(a=>a.map(x=>(x%p+p)%p));let k=0;for(let c=0;c<(M[0]?.length||0)&&k<M.length;c++){let j=k;while(j<M.length&&!M[j][c])j++;if(j===M.length)continue;[M[k],M[j]]=[M[j],M[k]];let z=inv(M[k][c]);M[k]=M[k].map(x=>x*z%p);for(let i=k+1;i<M.length;i++){z=M[i][c];if(z)M[i]=M[i].map((x,j)=>(x-z*M[k][j]%p+p)%p)}k++}return k};
 const frame=[0,1,2,4,8,14,30,59],G=frame.map(i=>frame.reduce((x,j,k)=>x|((((dot(R[i],R[j])/2)%2+2)%2)<<k),0));
 assert(rank(G.map(BigInt))===8,"binary polar frame");
 const coord=r=>{const v=frame.map(j=>((dot(r,R[j])/2)%2+2)%2);let a=[];for(let x=0;x<256;x++)if(G.every((z,k)=>par(z&x)===v[k]))a.push(x);assert(a.length===1,"binary root coordinate");return a[0]};
 const q=x=>{let a=0;for(let i=0;i<8;i++)if(x>>i&1){a^=1;for(let j=i+1;j<8;j++)if((x>>j&1)&&(G[i]>>j&1))a^=1}return a};
 const polar=(x,y)=>G.reduce((z,row,i)=>z^((x>>i&1)*par(row&y)),0);
 const masks=[...new Set(R.filter(r=>r.filter(x=>x!==0).length===4).map(r=>r.reduce((m,x,i)=>x?m|(1<<i):m,0)))].sort((a,b)=>a-b);
 assert(masks.length===14,"four-coordinate supports");
 const full=Array.from({length:8},(_,i)=>Array.from({length:8},(_,j)=>i===j?2:0));
 for(let m of masks){let pos=Array.from({length:8},(_,i)=>i).filter(i=>m>>i&1);for(let signs=0;signs<8;signs++){let r=Array(8).fill(0);r[pos[0]]=1;for(let j=1;j<4;j++)r[pos[j]]=signs>>(j-1)&1?-1:1;full.push(r)}}
 const X=R.map(coord),Y=full.map(coord);assert(new Set(Y).size===120&&Y.every(x=>q(x)===1),"full anisotropic quadric");
 assert(R.every(r=>full.some(t=>r.every((x,i)=>x===t[i]))),"native puncture");
 const s=38,hvals=X.map(x=>polar(s,x));
 assert(q(s)===0&&s!==0,"nonzero singular pivot");
 assert(G.reduce((m,g,k)=>m|(par(s&g)<<k),0)===189,"pivot linear mask");
 const bitset=S=>S.reduce((m,i)=>m|1n<<BigInt(i),0n),support=w=>R.flatMap((_,i)=>w>>BigInt(i)&1n?[i]:[]);
 const K=R.map((r,i)=>R.reduce((m,t,j)=>i===j||dot(r,t)===0?m|1n<<BigInt(j):m,0n));
 const h=bitset(hvals.flatMap((x,i)=>x?[i]:[])),ALL=(1n<<111n)-1n;
 const A=K.map((w,i)=>w&(hvals[i]?h:ALL^h));
 const fullK=full.map((r,i)=>full.reduce((m,t,j)=>i===j||dot(r,t)===0?m|1n<<BigInt(j):m,0n));
 const fullMasks=[0,1].map(t=>Y.reduce((m,x,i)=>polar(s,x)===t?m|1n<<BigInt(i):m,0n));
 assert([0,1].every(t=>rank(fullK.filter((_,i)=>polar(s,Y[i])===t).map(w=>w&fullMasks[t]))===7+t),"full block ranks7 and8");
 assert([0,1].every(t=>rank(A.filter((_,i)=>hvals[i]===t))===7+t),"native block ranks7 and8");
 assert(A.every((w,i)=>(w>>BigInt(i)&1n)&&R.every((r,j)=>i===j||dot(r,R[i])===0||!(w>>BigInt(j)&1n))),"complete fitting");
 const C=[ALL,...Array.from({length:8},(_,k)=>bitset(X.flatMap((x,i)=>x>>k&1?[i]:[])))];
 const Cs=K.filter((_,i)=>!hvals[i]),hC=C.map(w=>w&h),hCs=Cs.map(w=>w&h);
 assert(rank(C)===9&&rank(Cs)===8&&rank(hC)===8&&rank(hCs)===7,"seed and filtered-code dimensions");
 assert(rank(A)===15&&rank(A.concat(C))===16&&rank(A.concat(Cs,hC))===15,"global code identity");
 assert(rank(Cs.concat(hCs))===14,"six proper innovations");
 const a=R[72],b=[0,0,1,1,0,0,1,-1];
 assert(dot(a,b)===0&&(coord(a)^coord(b))===s,"orthogonal root decomposition of pivot");
 assert(!R.some(r=>r.every((x,i)=>x===b[i])||r.every((x,i)=>x===-b[i])),"omitted normal has no input");
 const covers=[],hist={};
 for(let i=0;i<111;i++){
  const S=support(A[i]).filter(j=>j!==i),foreignRank=rr(S.map(j=>R[j]));
  let parts,partner=null,normal=null;
  if(!hvals[i]){
   const lab=X[i]^s,fi=Y.indexOf(lab);assert(fi>=0,"anisotropic partner");normal=full[fi];
   assert(dot(normal,R[i])===0,"real-orthogonal partner");
   partner=X.indexOf(lab);parts=[S.filter(j=>j===partner),S.filter(j=>j!==partner)];
   assert(parts[1].every(j=>dot(R[j],normal)===0),"common-facet cover");
  }else{
   parts=[S.filter(j=>dot(R[j],a)===0),S.filter(j=>dot(R[j],a)!==0)];
   assert(parts[1].every(j=>dot(R[j],b)===0),"fixed two-facet cover");
  }
  const partRanks=parts.map(P=>rr(P.map(j=>R[j])));assert(partRanks.every(r=>r<=6),"proper chart ranks");
  assert(foreignRank===(partner===-1?6:7),"exact foreign ranks");
  const chi=foreignRank<=6?0:1;hist[chi]=(hist[chi]||0)+1;covers.push({receiver:i,class:hvals[i],partner,partner_normal:normal,foreign_support:S,foreign_rank:foreignRank,parts,part_ranks:partRanks,charge:chi});
 }
 assert(hist[0]===4&&hist[1]===107,"charge107");
 const seeds=[1,3,5,10,30,61],modes=seeds.map(i=>K[i]&h);
 assert(seeds.every(i=>hvals[i]===0)&&rank(Cs.concat(modes))===14,"explicit six directions");
 const supports=modes.map(support);
 supports.forEach((S,k)=>assert(S.every(j=>dot(R[j],R[seeds[k]])===0)&&rr(S.map(j=>R[j]))===7,"actual rank7 facet-local mode"));
 assert(hvals[0]===1&&rank(Cs.concat(modes,K[0]&h))===15&&rr(support(K[0]&h).map(j=>R[j]))===8,"one nonlocal direction");
 const overlap=R.flatMap((_,j)=>{const banks=supports.flatMap((S,k)=>S.includes(j)?[k]:[]);return banks.length?[{source:j,banks}]:[]});
 assert(overlap.filter(x=>x.banks.length>=2).length===53,"direct shared-source conflict");
 const Kb=bitset(R.flatMap((r,i)=>dot(r,b)===0?[i]:[])),nativeSeeds=[1,3,5,10,11,15,30],seed8=nativeSeeds.map(i=>K[i]).concat(K[0]&h);
 assert(rank(seed8)===8&&rr(support(Kb).map(i=>R[i]))===7&&rank(seed8.concat(Kb,modes))===15,"eight seeds and seven proper additions");
 const normalize=v=>v.find(x=>x!==0)<0?v.map(x=>-x):v,axes=new Map();
 for(let i=0;i<120;i++)if(polar(s,Y[i])===0){let j=Y.indexOf(Y[i]^s);if(j>i)for(let sign of[1,-1]){let v=normalize(full[i].map((x,k)=>x+sign*full[j][k]));axes.set(v.join(","),v)}}
 const axes2=[...axes.values()];assert(axes2.length===8&&axes2.every((a,i)=>axes2.every((b,j)=>dot(a,b)===(i===j?8:0))),"D8 doubled axes");
 for(let i=0;i<120;i++){const c=axes2.map(a=>dot(a,full[i])/4);if(polar(s,Y[i])===0)assert(c.filter(x=>x!==0).length===2&&c.every(x=>[-1,0,1].includes(x)),"D8 edge root");else assert(c.every(x=>Math.abs(x)===0.5)&&c.reduce((a,x)=>a*Math.sign(x),1)===1,"even half-spinor root")}
 assert(69n**200n<7n**199n*10n**200n&&79n**200n<8n**199n*10n**200n,"exact endpoint lower prices");
 return {status:"PASS_SINGULAR_PIVOT_SPLIT",source_recovery_blob:"8eba43d142c819c206dce5df87ea4571aaead287",binary_frame:frame,binary_polar_rows:G,pivot:s,pivot_linear_mask:189,full_class_sizes:[56,64],native_class_sizes:[hvals.filter(x=>!x).length,hvals.filter(x=>x).length],doubled_D8_axes:axes2,fitting_rank:15,canonical_joint_rank:16,canonical_intersection_dimension:8,canonical_quotient_dimension:7,charge_histogram:hist,charge:107,zero_charge_receivers:covers.filter(x=>x.charge===0).map(x=>x.receiver),seed_space_dimension:8,filtered_canonical_dimension:8,filtered_seed_dimension:7,seed_filtered_intersection_dimension:1,proper_direction_receivers:seeds,proper_direction_supports:supports,nonlocal_direction_receiver:0,six_plus_one_joint_dimension:15,shared_source_conflict_count:53,shared_source_incidence:overlap,alternative_eight_seeds:{canonical_native_rows:nativeSeeds,filtered_row:0},alternative_seven_proper_modes:{omitted_normal:b,filtered_rows:seeds},covers,negative_controls:{anisotropic_pivot92_is_not_covered_by_the_singular_hypothesis:q(X[92])===1,four_omitted_partners_are_geometric_normals_not_inputs:true},independent_route_budget_lower_bound:"8*7.9+7*6.9=111.5>83",actual_source_word:false,new_complete_kappa:false};
}
if(typeof process!=="undefined"&&process.argv[1]&&import.meta.url===new URL("file://"+process.argv[1]).href){
 const {readFileSync}=await import("node:fs"),{createHash}=await import("node:crypto");
 if(!process.argv[2])throw Error("Usage: node check.mjs RECOVERED-NATIVE-ROOTS.json");
 const raw=readFileSync(process.argv[2]),sha=createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
 if(sha!=="8eba43d142c819c206dce5df87ea4571aaead287")throw Error("Source Git blob mismatch");
 process.stdout.write(JSON.stringify(checkSingularSplit(JSON.parse(raw.toString("utf8"))),null,2)+"\n");
}
