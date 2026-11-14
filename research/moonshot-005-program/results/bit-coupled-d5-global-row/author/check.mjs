export function checkCoupledD5(g) {
 const R=g.native_roots,assert=(x,m)=>{if(!x)throw Error(m)},dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0);
 assert(R.length===111,"native source length");
 const rank=rows=>{const B=new Map();let n=0;for(let x of rows){while(x){const k=x.toString(2).length-1;if(B.has(k))x^=B.get(k);else{B.set(k,x);n++;break}}}return n};
 const par=x=>{let z=0;while(x){z^=x&1;x>>=1}return z};
 const p=103,inv=a=>{let x=1;for(let i=0;i<101;i++)x=x*a%p;return x};
 const rr=rows=>{const M=rows.map(r=>r.map(x=>(x%p+p)%p));let k=0;for(let j=0;j<(M[0]?.length||0)&&k<M.length;j++){let a=k;while(a<M.length&&!M[a][j])a++;if(a===M.length)continue;[M[a],M[k]]=[M[k],M[a]];let u=inv(M[k][j]);M[k]=M[k].map(x=>x*u%p);for(let i=k+1;i<M.length;i++){u=M[i][j];if(u)M[i]=M[i].map((x,l)=>(x-u*M[k][l]%p+p)%p)}k++}return k};
 const F=[0,1,2,4,8,14,30,59],G=F.map(i=>F.reduce((x,j,k)=>x|((((dot(R[i],R[j])/2)%2+2)%2)<<k),0));
 assert(rank(G.map(BigInt))===8,"binary frame");
 const X=R.map(r=>{const t=F.map(j=>((dot(r,R[j])/2)%2+2)%2),a=[];for(let x=0;x<256;x++)if(G.every((v,k)=>par(v&x)===t[k]))a.push(x);assert(a.length===1,"binary point");return a[0]});
 const bitset=S=>S.reduce((x,i)=>x|1n<<BigInt(i),0n),support=x=>R.flatMap((_,i)=>x>>BigInt(i)&1n?[i]:[]);
 const D=R.flatMap((r,i)=>[92,54,38].every(j=>dot(r,R[j])===0)?[i]:[]),E=R.flatMap((r,i)=>[1,18,31].every(j=>dot(r,R[j])===0)?[i]:[]);
 const expectedD=[1,10,11,18,23,27,31,35,41,49,57,61,65,72,73,80,89,110],expectedE=[3,7,16,21,38,39,53,54,67,68,71,72,81,84,85,88,92,104,108],L=[5,12,15,22,26,30,34,40,47,50,58,64,76,77,93,106];
 assert(JSON.stringify(D)===JSON.stringify(expectedD)&&JSON.stringify(E)===JSON.stringify(expectedE),"D5 supports");
 assert(JSON.stringify(D.filter(i=>E.includes(i)))==="[72]","shared native input");
 const q=[0,0,1,1,0,0,1,-1];
 assert(dot(q,q)===4&&dot(q,R[72])===0,"orthogonal virtual root");
 assert(R.every(r=>r.some((x,i)=>x!==q[i])&&r.some((x,i)=>x!==-q[i])),"virtual root is omitted");
 assert([92,54,38,1,18,31].every(i=>dot(q,R[i])===0),"shared two-dimensional chart");
 assert(rr([92,54,38,1,18,31].map(i=>R[i]))===6,"D intersection dimension2");
 assert(rr(D.filter(i=>i!==72).map(i=>R[i]))===5&&rr(E.filter(i=>i!==72).map(i=>R[i]))===5,"proper source ranks");
 assert(L.every(i=>dot(R[i],R[72])===0&&dot(R[i],q)===0)&&rr(L.map(i=>R[i]))===6,"foreign correction chart");
 const K=R.map((r,i)=>R.reduce((x,s,j)=>i===j||dot(r,s)===0?x|1n<<BigInt(j):x,0n));
 const z=bitset(D),w=bitset(E),unit=1n<<72n,a=z^unit,b=w^unit,l=bitset(L);
 assert(z===(K[92]&K[54]&K[38])&&w===(K[1]&K[18]&K[31]),"cubic D5 indicators");
 const C=[(1n<<111n)-1n,...Array.from({length:8},(_,j)=>X.reduce((x,u,i)=>u>>j&1?x|1n<<BigInt(i):x,0n))];
 const s=38;let qs=0;for(let i=0;i<8;i++)if(s>>i&1){qs^=1;for(let j=i+1;j<8;j++)if((s>>j&1)&&(G[i]>>j&1))qs^=1}
 assert(qs===0&&G.reduce((m,g,k)=>m|(par(g&s)<<k),0)===189,"canonical singular label");
 const c=X.reduce((x,u,i)=>(1^par(u&189))?x|1n<<BigInt(i):x,0n);
 assert(c===(a^b^unit^l),"exact global row identity");
 assert((a&b)===0n&&(a&l)===0n&&(b&l)===0n&&((a|b|l)&unit)===0n,"disjoint acquisition cohorts");
 const row=c^z^w;
 assert(row===(unit|l),"fitting row support");
 const M=K.slice();M[72]=row;
 assert(M.every((m,i)=>(m>>BigInt(i)&1n)&&R.every((r,j)=>i===j||dot(R[i],r)===0||!(m>>BigInt(j)&1n))),"all native fitting obligations");
 assert(rank(M)===10&&rank(M.concat(C))===10,"actual fitting rank and canonical containment");
 assert(rank(C.concat(z,w))===11&&rank(C.concat(a,b))===11,"two different history spaces");
 const Q3=[];for(let m=0;m<256;m++)if(m.toString(2).replaceAll("0","").length<=3)Q3.push(X.reduce((x,u,i)=>(u&m)===m?x|1n<<BigInt(i):x,0n));
 assert(rank(Q3)===84&&rank(Q3.concat(a))===85&&rank(Q3.concat(b))===85&&rank(Q3.concat(a^b))===84,"punctured modes leave cubic code separately");
 const bad=c^z^b;
 assert((bad>>72n&1n)===0n,"one-sided separator deletion must fail own block");
 const gram=A=>A.map(i=>A.map(j=>dot(R[i],R[j])));
 return {status:"PASS_COUPLED_D5_GLOBAL_ROW",source_recovery_blob:"8eba43d142c819c206dce5df87ea4571aaead287",binary_frame:F,binary_polar_rows:G,D,E,D_normals:[92,54,38],E_normals:[1,18,31],D_gram:gram([92,54,38]),E_gram:gram([1,18,31]),shared_native_input:72,shared_chart_real_rank:2,source_chart_join_real_rank:8,omitted_shared_root:q,receiver:72,foreign_correction_support:L,foreign_correction_rank:6,raw_mode_a:support(a),raw_mode_b:support(b),raw_source_ranks:[5,5],canonical_coefficient_mask:379,canonical_linear_mask:189,canonical_singular_label:38,canonical_support:support(c),canonical_support_size:support(c).length,cubic_modes:[D,E],whole_fitting_rank:10,whole_fitting_canonical_joint_rank:10,actual_fitting_quotient_dimension:1,separate_mode_history_rank:11,separate_mode_history_quotient_dimension:2,displayed_fitting_charge:220,punctured_a_is_cubic:false,punctured_b_is_cubic:false,sum_is_cubic:true,negative_controls:{delete_separator_on_only_one_side_breaks_own_block:true},chronological_word_in_this_package:false,complete_supplier:false,new_complete_kappa:false};
}
if(typeof process!=="undefined"&&process.argv[1]&&import.meta.url===new URL("file://"+process.argv[1]).href){
 const {readFileSync}=await import("node:fs"),{createHash}=await import("node:crypto");
 if(!process.argv[2])throw Error("Usage: node check.mjs RECOVERED-NATIVE-ROOTS.json");
 const raw=readFileSync(process.argv[2]),sha=createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
 if(sha!=="8eba43d142c819c206dce5df87ea4571aaead287")throw Error("Source Git blob mismatch");
 process.stdout.write(JSON.stringify(checkCoupledD5(JSON.parse(raw.toString("utf8"))),null,2)+"\n");
}
