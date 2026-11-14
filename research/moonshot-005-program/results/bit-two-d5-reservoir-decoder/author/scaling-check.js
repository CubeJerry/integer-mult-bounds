function checkOneDirectionRestriction(geometry,word) {
 const R=geometry.native_roots,mask=ids=>ids.reduce((v,i)=>v^(1n<<BigInt(i)),0n),dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0);
 function rank(A){const p=new Map();for(let x of A){while(x){const k=x.toString(2).length;if(p.has(k))x^=p.get(k);else{p.set(k,x);break;}}}return p.size;}
 const K=R.map((r,i)=>mask(R.map((s,j)=>i===j||dot(r,s)===0?j:-1).filter(j=>j>=0))),P=word.source_partition,d=mask(P.a)^mask(P.b),A=mask([72,...P.foreign]),rows=[];
 if(rank(K)!==9||rank([...K,d])!==10||rank(K.filter((_,i)=>i!==72))!==9)throw Error("global ranks");
 for(let i=0;i<111;i++){const Z=mask(R.map((r,j)=>i!==j&&dot(r,R[i])!==0?j:-1).filter(j=>j>=0)),rC=rank(K.map(v=>v&Z)),rS=rank([...K,d].map(v=>v&Z));if(rC!==8||rS!==(i===72?8:9))throw Error("restriction rank "+i);if(i===72&&(A&Z))throw Error("A noncontact");rows.push({receiver:i,canonical_restriction_rank:rC,enlarged_restriction_rank:rS});}
 if(!(A&(1n<<72n))||A===K[72]||(A&K[72])!==A||rank([...K,A])!==10)throw Error("exceptional kernel basis");
 return {status:"PASS",coefficient_characteristic:2,global_ranks:[9,10],canonical_without72_rank:9,restriction_rows:rows,exceptional_receiver:72,exceptional_kernel_basis:[K[72].toString(16),A.toString(16)],exceptional_target_is_subset:true,scope:"All-field and arbitrary block-width normal form follows from the binary restriction-rank certificate; no universal physical lower bound."};
}
