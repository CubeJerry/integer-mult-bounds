
function checkThreeCarrier(flat){
 const need=(v,m)=>{if(!v)throw Error(m)},dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
 const full=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 const native=Array.from({length:111},(_,i)=>flat.independent_generators.map(w=>+w.native_difference.includes(i)).join(""));
 need(new Set(full).size===120&&new Set(native).size===111,"signature uniqueness");
 const map=native.map(s=>full.indexOf(s));need(map.every(i=>i>=0),"signature match");const R=map.map(i=>flat.full_roots[i]);
 const B=(i,j)=>{let v=dot(R[i],R[j]);need(v%2===0,"integral lattice pairing");return (v/2%2+2)%2};
 const ab=R.map((_,i)=>[B(i,15),B(i,92)]),cl=ab.map(([a,b])=>a+2*b),axes=[92,15,106];
 const K=R.map((_,i)=>R.map((_,j)=>1^B(i,j)));
 const D=R.map((_,i)=>R.map((_,j)=>B(i,j)^(ab[i][0]&ab[j][1])^(ab[i][1]&ab[j][0])));
 const T=[1,2,3].map(k=>cl.map(c=>+(c===0||c===k)));
 for(let a=0;a<3;a++)for(let j=0;j<111;j++)need(T[a][j]===K[axes[a]][j],"carrier totals");
 for(let i=0;i<111;i++)for(let j=0;j<111;j++)need(K[i][j]===(D[i][j]^(cl[i]===0?T[0][j]^T[1][j]^T[2][j]:T[cl[i]-1][j])),"nine-mode factorization");
 const A=K.map((r,i)=>r.map((x,j)=>x*+(ab[i][1]===ab[j][1])));
 const C=A.map((r,i)=>r.map((x,j)=>axes.includes(i)||axes.includes(j)?+(i===j):x));
 const bitrows=M=>M.map(r=>r.reduce((n,x,i)=>n|(BigInt(x)<<BigInt(i)),0n));
 function rank2(rows){const p=new Map();for(const v of rows){let x=v;while(x){let k=x.toString(2).length-1;if(p.has(k))x^=p.get(k);else{p.set(k,x);break}}}return {rank:p.size,echelon:[...p].sort((a,b)=>b[0]-a[0]).map(([pivot,row])=>({pivot,row_hex:row.toString(16)}))};}
 function rank103(M){if(!M.length)return 0;const p=103,a=M.map(r=>r.map(x=>(x%p+p)%p));let k=0;const inv=x=>{let z=1;for(let i=0;i<101;i++)z=z*x%p;return z};
  for(let c=0;c<8&&k<a.length;c++){let h=k;while(h<a.length&&!a[h][c])h++;if(h===a.length)continue;[a[k],a[h]]=[a[h],a[k]];const d=inv(a[k][c]);a[k]=a[k].map(x=>x*d%p);for(let i=k+1;i<a.length;i++){const d=a[i][c];a[i]=a[i].map((x,j)=>(x-d*a[k][j]%p+p)%p)}k++;}return k;
 }
 const rank=M=>rank2(bitrows(M)).rank;
 need(rank(K)===9&&rank(D)===6&&rank(T)===3,"factor ranks");
 need(rank2([...bitrows(D),...bitrows(T)]).rank===9,"independent factor spaces");
 need(rank(A)===15&&rank2([...bitrows(K),...bitrows(A)]).rank===16,"pivot ranks");
 need(rank(C)===18&&rank2([...bitrows(K),...bitrows(C)]).rank===19,"three-coordinate fitting ranks");
 need(C.every((r,i)=>r[i]===1&&r.every((x,j)=>!x||!B(i,j))),"valid fitting");
 need(R[92].every((x,i)=>x===R[15][i]-R[106][i]),"real carrier relation");
 const rowCover=[],hist={};
 for(let i=0;i<111;i++){
  const support=C[i].flatMap((x,j)=>x&&j!==i?[j]:[]),normal=axes.includes(i)?[]:ab[i][1]?[15,106]:[92];
  need(support.every(j=>dot(R[i],R[j])===0&&normal.some(k=>dot(R[k],R[j])===0)),"explicit carrier cover");
  need(normal.every(k=>rank103([R[i],R[k]])===2),"proper intersections");
  const lower=rank103(support.map(j=>R[j])),m=axes.includes(i)?0:ab[i][1]?2:1;
  need(lower===(m===0?0:m===1?6:7),"sharp support lower rank");
  hist[m]=(hist[m]||0)+1;rowCover.push({receiver:i,foreign_support:support,foreign_real_rank:lower,carrier_normals:normal,minimum_proper_cover:m});
 }
 need(hist[0]===3&&hist[1]===57&&hist[2]===51,"charge histogram");
 const negative=[];
 for(const unpaid of [15,106]){
  const witness=R.findIndex((_,i)=>!axes.includes(i)&&ab[i][1]&&A[i][unpaid]===1);
  need(witness>=0&&dot(R[unpaid],R[15])!==0&&dot(R[unpaid],R[106])!==0,"unpaid-axis cover failure");
  negative.push({unpaid_axis:unpaid,receiver:witness,uncovered_foreign_source:unpaid});
 }
 const result={
 status:"PASS_THREE_CARRIER_PUNCTURE_AND_SIX_MOMENT_BRIDGE",
 native_sha256:"51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78",
 source_qualification:"derived from authenticated admitted flat-cubic certificate; not fresh compressed-native replay",
 axes,partition_including_axes:[0,1,2,3].map(k=>cl.filter(c=>c===k).length),
 canonical_rank:9,E6_moment_rank:6,carrier_total_rank:3,pivot_filter_rank:15,pivot_canonical_joint_rank:16,
 completed_three_coordinate_rank:18,completed_canonical_joint_rank:19,cover_histogram:hist,chi:51,
 block_sizes:[0,1].map(k=>ab.filter(a=>a[1]===k).length),
 block_ranks:[0,1].map(k=>rank(A.filter((_,i)=>ab[i][1]===k).map(r=>r.filter((_,j)=>ab[j][1]===k)))),
 fitting_basis_certificate:rank2(bitrows(C)),row_cover:rowCover,negative_controls:negative,
 no_actual_source_extension_emitted:true,no_complete_invoice:true,no_new_kappa:true};
 return result;
}

if(typeof module!=="undefined"){
 module.exports={checkThreeCarrier};
 if(require.main===module){
  const fs=require("fs"),crypto=require("crypto");
  if(process.argv.length!==3)throw Error("usage: node check.js flat_RESULT.json");
  const b=fs.readFileSync(process.argv[2]);
  if(crypto.createHash("sha256").update(b).digest("hex")!=="4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc")throw Error("input SHA-256 mismatch");
  process.stdout.write(JSON.stringify(checkThreeCarrier(JSON.parse(b)),null,2)+"\n");
 }
}
