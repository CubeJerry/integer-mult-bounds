export function checkD5LocalHistory(g) {
  const R=g.native_roots;
  const fail=m=>{throw Error(m)};
  const assert=(p,m)=>{if(!p)fail(m)};
  assert(Array.isArray(R)&&R.length===111,"111 native roots");
  const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
  const brank=arr=>{const B=new Map();let n=0;for(let x of arr){while(x){const p=x.toString(2).length-1;if(B.has(p))x^=B.get(p);else{B.set(p,x);n++;break}}}return n};
  const par=x=>{let t=0;while(x){t^=x&1;x>>=1}return t};
  const p=103, inv=a=>{let t=1;for(let i=0;i<p-2;i++)t=t*a%p;return t};
  const prank=rows=>{const M=rows.map(a=>a.map(x=>(x%p+p)%p));let k=0;for(let c=0;c<(M[0]?.length||0)&&k<M.length;c++){let a=k;while(a<M.length&&!M[a][c])a++;if(a===M.length)continue;[M[k],M[a]]=[M[a],M[k]];let z=inv(M[k][c]);M[k]=M[k].map(x=>x*z%p);for(let i=k+1;i<M.length;i++){z=M[i][c];if(z)M[i]=M[i].map((x,j)=>(x-z*M[k][j]%p+p)%p)}k++}return k};
  const F=[0,1,2,4,8,14,30,59];
  const G=F.map(i=>F.reduce((m,j,k)=>m|((((dot(R[i],R[j])/2)%2+2)%2)<<k),0));
  assert(brank(G.map(BigInt))===8,"binary polar basis");
  const X=R.map(r=>{const v=F.map(j=>((dot(r,R[j])/2)%2+2)%2);const a=[];for(let x=0;x<256;x++)if(G.every((s,k)=>par(x&s)===v[k]))a.push(x);assert(a.length===1,"unique binary coordinate");return a[0]});
  assert(new Set(X).size===111,"distinct binary points");
  const D=R.flatMap((r,i)=>[92,54,38].every(j=>dot(r,R[j])===0)?[i]:[]);
  const expectedD=[1,10,11,18,23,27,31,35,41,49,57,61,65,72,73,80,89,110];
  assert(JSON.stringify(D)===JSON.stringify(expectedD),"D source support");
  const axes=[[1,0,1,0,1,-2,-1,0],[1,0,1,0,-1,0,1,-2],[1,0,-1,-2,-1,0,-1,0],[1,2,-1,0,1,0,1,0],[1,-2,-1,0,1,0,1,0]];
  assert(axes.every((a,i)=>axes.every((b,j)=>dot(a,b)===(i===j?8:0))),"D5 orthogonal axes");
  const edges=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)edges.push([a,b]);
  const mapD=D.map(i=>{const c=axes.map(a=>dot(R[i],a)/4);assert(c.filter(x=>x!==0).length===2&&c.every(x=>[-1,0,1].includes(x)),"signed D5 edge");const e=c.flatMap((x,k)=>x?[k]:[]);return edges.findIndex(x=>x[0]===e[0]&&x[1]===e[1])});
  const words=[];for(let m=0;m<1024;m++){let wt=0,d=[0,0,0,0,0];for(let e=0;e<10;e++)if(m>>e&1){wt++;for(let k of edges[e])d[k]^=1}if(!(wt%2)&&d.every(x=>x===0))words.push(D.reduce((x,i,k)=>m>>mapD[k]&1?x|1n<<BigInt(i):x,0n))}
  assert(words.length===32,"even Eulerian words");
  const Z=[];for(let z of words)if(brank(Z.concat(z))>Z.length)Z.push(z);
  assert(Z.length===5,"punctured even Eulerian rank");
  const mons=[];for(let m=0;m<256;m++)if(m.toString(2).replaceAll("0","").length<=3)mons.push(m);
  const poly=ms=>ms.map(m=>X.reduce((y,x,i)=>(x&m)===m?y|1n<<BigInt(i):y,0n));
  const Q3=poly(mons),Q2=poly(mons.filter(m=>m.toString(2).replaceAll("0","").length<=2));
  const ALL=(1n<<111n)-1n, DM=D.reduce((x,i)=>x|1n<<BigInt(i),0n);
  assert(brank(Q3)===84&&brank(Q3.map(x=>x&(ALL^DM)))===79,"native cubic shortening dimension");
  assert(Z.every(z=>brank(Q3.concat(z))===84),"Eulerian code contained in cubic code");
  assert(brank(Q2)===36&&brank(Q2.map(x=>x&(ALL^DM)))===36,"no quadratic shortening");
  const C=poly([0,1,2,4,8,16,32,64,128]);
  const local=[],cert=[];
  for(let i=0;i<111;i++){
    const outsideZero=R.flatMap((r,j)=>j!==i&&!(DM>>BigInt(j)&1n)&&dot(R[i],r)!==0?[j]:[]);
    const outsideForeign=R.flatMap((r,j)=>j!==i&&!(DM>>BigInt(j)&1n)&&dot(R[i],r)===0?[j]:[]);
    assert(brank(outsideZero.map(j=>BigInt(256|X[j])))===8,"outside-D canonical zero restriction");
    const qrows=outsideForeign.map(j=>{const a=[];for(let s=0;s<8;s++)for(let t=s;t<8;t++)a.push(R[j][s]*R[j][t]);return a});
    assert(prank(qrows)===28,"outside-D foreign quadratic rank");
    const zeroMask=R.reduce((x,r,j)=>j!==i&&dot(R[i],r)!==0?x|1n<<BigInt(j):x,0n);
    const c=C.map(x=>x&zeroMask),cr=brank(c),ids=[];
    for(let m=0;m<32;m++){let z=0n;for(let k=0;k<5;k++)if(m>>k&1)z^=Z[k];if(brank(c.concat(z&zeroMask))===cr)ids.push(m)}
    if(D.includes(i))assert(ids.length===1,"no own fitting in D-local code");
    local.push({role:i,dimension:Math.log2(ids.length),members:ids});
    cert.push({role:i,outside_noncontact_rank:8,outside_foreign_count:outsideForeign.length,outside_foreign_quadratic_rank:28});
  }
  const hist={};for(let x of local)hist[x.dimension]=(hist[x.dimension]||0)+1;
  assert(JSON.stringify(hist)===JSON.stringify({0:77,2:28,5:6}),"local dimension histogram");
  const carrier=Z.every(z=>Number(z>>1n&1n)===Number(z>>18n&1n));
  assert(carrier,"equal carrier coefficients");
  const planes=[...new Map(local.filter(x=>x.dimension===2).map(x=>[x.members.join(","),x.members])).values()];
  assert(planes.length===5&&new Set(planes.flat().filter(x=>x)).size===15,"five disjoint local planes");
  return {status:"PASS_D5_CUBIC_LOCAL_HISTORY_SCREEN",source_recovery_blob:"8eba43d142c819c206dce5df87ea4571aaead287",source_qualification:"Derived native roots; no fresh gzip replay",binary_frame:F,binary_polar_rows:G,D,axes,edge_roles:edges.map((e,k)=>({edge:e,roles:D.filter((_,l)=>mapD[l]===k)})),code_basis:Z.map(z=>D.filter(i=>z>>BigInt(i)&1n)),cubic_rank:84,outside_cubic_rank:79,quadratic_shortening_dimension:0,local_dimension_histogram:hist,local_planes:planes,local_receiver_data:local,canonical_outside_certificates:cert,all_outside_foreign_quadratic_rank:28,carrier_coefficients_equal:carrier,negative_controls:{single_native_unit_in_D_is_not_in_code:!words.includes(1n<<1n),single_edge_pair_is_not_even_Eulerian:!words.includes((1n<<1n)|(1n<<18n))},classification:"Source-bound universal linear algebra; local injection does not supply a global fitting",new_complete_kappa:false};
}
export function validateD5LocalHistory(g) {
  const out=checkD5LocalHistory(g);
  const tests=[["missing_native_role",x=>x.native_roots.pop()],["duplicated_carrier",x=>x.native_roots[18]=x.native_roots[1].slice()]];
  out.negative_controls.source_mutations=tests.map(([name,mutate])=>{
    const x=JSON.parse(JSON.stringify(g));mutate(x);
    try{checkD5LocalHistory(x);return {name,rejected:false};}
    catch(e){return {name,rejected:true,reason:String(e.message)};}
  });
  if(out.negative_controls.source_mutations.some(x=>!x.rejected))throw Error("A mutation control did not reject");
  return out;
}
if (typeof process!=="undefined" && process.argv[1] && import.meta.url===new URL("file://"+process.argv[1]).href) {
  const {readFileSync}=await import("node:fs");
  const {createHash}=await import("node:crypto");
  const path=process.argv[2]; if(!path)throw Error("Usage: node check.mjs RECOVERED-NATIVE-ROOTS.json");
  const raw=readFileSync(path), sha=createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
  if(sha!=="8eba43d142c819c206dce5df87ea4571aaead287")throw Error("Source Git blob mismatch");
  process.stdout.write(JSON.stringify(validateD5LocalHistory(JSON.parse(raw.toString("utf8"))),null,2)+"\n");
}
