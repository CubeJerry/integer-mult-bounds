function checkTwoD5Geometry(geometry,word) {
 const R=geometry.native_roots,n=111,P=word.source_partition,{a,b,foreign:L,canonical_c:c,canonical_background:g}=P;
 const gcd=(x,y)=>{x=x<0n?-x:x;y=y<0n?-y:y;while(y){const t=x%y;x=y;y=t;}return x;};
 function rank(A){A=A.map(r=>r.map(BigInt));let s=0;for(let j=0;j<8&&s<A.length;j++){let p=s;while(p<A.length&&!A[p][j])p++;if(p===A.length)continue;[A[p],A[s]]=[A[s],A[p]];for(let i=s+1;i<A.length;i++)if(A[i][j]){const x=A[s][j],y=A[i][j];for(let k=j;k<8;k++)A[i][k]=x*A[i][k]-y*A[s][k];let d=0n;for(const z of A[i])d=gcd(d,z);if(d>1n)A[i]=A[i].map(z=>z/d);}s++;}return s;}
 const dot=(x,y)=>x.reduce((s,z,k)=>s+BigInt(z)*BigInt(y[k]),0n),mask=ids=>ids.reduce((v,i)=>v^(1n<<BigInt(i)),0n),eq=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
 function rank2(A){const p=new Map();for(let x of A){while(x){const k=x.toString(2).length;if(p.has(k))x^=p.get(k);else{p.set(k,x);break;}}}return p.size;}
 const K=R.map((r,i)=>mask(R.map((s,j)=>i===j||dot(r,s)===0n?j:-1).filter(j=>j>=0)));
 const fullD1=R.map((r,i)=>[92,54,38].every(j=>dot(r,R[j])===0n)?i:-1).filter(i=>i>=0),fullD2=R.map((r,i)=>[1,18,31].every(j=>dot(r,R[j])===0n)?i:-1).filter(i=>i>=0);
 if(!eq(fullD1.filter(i=>i!==72),a)||!eq(fullD2.filter(i=>i!==72),b))throw Error("D5 source set mismatch");
 if(new Set([...a,...b,...L,72]).size!==52||a.some(i=>b.includes(i)||L.includes(i))||b.some(i=>L.includes(i))||[...a,...b,...L].includes(72))throw Error("source partition overlap");
 if(mask(c)!==(mask(a)^mask(b)^mask(L)^(1n<<72n)))throw Error("fitting identity");
 if(rank2(K)!==9||rank2([...K,mask(c)])!==9||mask(g)!==K[92])throw Error("canonical preloads");
 if(L.some(i=>dot(R[i],R[72])!==0n))throw Error("foreign noncontact");
 const q=[0,0,1,1,0,0,1,-1];
 if(dot(q,q)!==4n||dot(q,R[72])!==0n||rank([R[72],q])!==2||L.some(i=>dot(q,R[i])!==0n)||rank(L.map(i=>R[i]))!==6)throw Error("proper foreign chart");
 if(R.some(r=>eq(r,q)||eq(r,q.map(x=>-x))))throw Error("q must be omitted");
 const dimensions={D1:8-rank([92,54,38].map(i=>R[i])),D2:8-rank([1,18,31].map(i=>R[i])),I:8-rank([92,54,38,1,18,31].map(i=>R[i])),E:8-rank([R[72],q])};
 if(!eq(dimensions,{D1:5,D2:5,I:2,E:6})||rank(a.map(i=>R[i]))!==5||rank(b.map(i=>R[i]))!==5)throw Error("chart dimensions");
 const mA=mask(a),mB=mask(b),mC=mask(c),mG=mask(g),fitting=mC^mA^mB;
 const ranks={canonical:rank2(K),initial_pair:rank2([mC^mG,mG]),carried_history:rank2([mC,mG,mA,mB]),final_pair:rank2([fitting,mG^mB]),canonical_plus_sum:rank2([...K,mA^mB]),canonical_plus_separate_modes:rank2([...K,mA,mB]),full_fitting:rank2([...K.filter((_,i)=>i!==72),fitting])};
 if(!eq(ranks,{canonical:9,initial_pair:2,carried_history:4,final_pair:2,canonical_plus_sum:10,canonical_plus_separate_modes:11,full_fitting:10}))throw Error("code rank certificate");
 return {status:"PASS",native_roles:n,dimensions,source_counts:{a:a.length,b:b.length,foreign:L.length,canonical_c:c.length,canonical_g:g.length,moved:P.all_moved.length,retained_points:P.retained_point_copies.length},ranks,own_fitting_coefficient:1,foreign_support:L,foreign_real_rank:6,proper_cover_chi_for_row72:0,omitted_normal:q,source_qualification:geometry.qualification};
}
