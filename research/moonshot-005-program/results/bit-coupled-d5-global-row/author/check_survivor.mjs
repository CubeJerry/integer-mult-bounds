export function checkD5Survivor(g){
 const R=g.native_roots,assert=(x,m)=>{if(!x)throw Error(m)},dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0),rk=rows=>{const B=new Map();let n=0;for(let x of rows){while(x){let p=x.toString(2).length-1;if(B.has(p))x^=B.get(p);else{B.set(p,x);n++;break}}}return n};
 assert(R.length===111,"source length");
 const K=R.map((r,i)=>R.reduce((m,s,j)=>i===j||dot(r,s)===0?m|1n<<BigInt(j):m,0n)),E=R.flatMap((r,i)=>[1,18,31].every(j=>dot(r,R[j])===0)?[i]:[]),S=E.filter(i=>i!==72),b=S.reduce((m,i)=>m|1n<<BigInt(i),0n);
 let C=[];for(let row of K)if(rk(C.concat(row))>C.length)C.push(row);assert(C.length===9,"canonical rank");
 const p=103,inv=x=>{let a=1;for(let i=0;i<101;i++)a=a*x%p;return a},rr=A=>{let M=A.map(a=>a.map(x=>(x%p+p)%p)),k=0;for(let c=0;c<(M[0]?.length||0)&&k<M.length;c++){let j=k;while(j<M.length&&!M[j][c])j++;if(j===M.length)continue;[M[k],M[j]]=[M[j],M[k]];let z=inv(M[k][c]);M[k]=M[k].map(x=>x*z%p);for(let i=k+1;i<M.length;i++){z=M[i][c];if(z)M[i]=M[i].map((x,j)=>(x-z*M[k][j]%p+p)%p)}k++}return k};
 assert(rr(S.map(i=>R[i]))===5,"helper spans its chart");
 const valid=[],zeroRanks=[];
 for(let i=0;i<111;i++){
  const mask=R.reduce((m,r,j)=>j!==i&&!E.includes(j)&&dot(r,R[i])!==0?m|1n<<BigInt(j):m,0n);
  assert(rk(C.map(w=>w&mask))===8,"outside-chart canonical kernel");
  zeroRanks.push(8);
  const own=1n<<BigInt(i),Z=R.reduce((m,r,j)=>j!==i&&dot(r,R[i])!==0?m|1n<<BigInt(j):m,0n);
  for(let bits=0;bits<512;bits++){let canonical=0n;for(let j=0;j<9;j++)if(bits>>j&1)canonical^=C[j];const Q=canonical^b;if((Q&own)&&!(Q&Z)){assert(canonical===K[i],"unique canonical choice");const foreign=R.flatMap((_,j)=>j!==i&&(Q>>BigInt(j)&1n)?[j]:[]),quad=foreign.map(j=>{let a=[];for(let s=0;s<8;s++)for(let t=s;t<8;t++)a.push(R[j][s]*R[j][t]);return a});assert(rr(foreign.map(j=>R[j]))===7&&rr(quad)===28,"no two proper covers");valid.push({receiver:i,canonical_native_row:i,foreign_support:foreign,foreign_rank:7,quadratic_rank:28,charge:2})}}
 }
 assert(JSON.stringify(valid.map(x=>x.receiver))==="[1,18,31,35,49]","exact survivor choices");
 assert(E.every(i=>S.some(j=>i!==j&&dot(R[i],R[j])!==0)),"no inside-chart own fitting");
 return{status:"PASS_D5_SURVIVING_PACKET_GATE",source_recovery_blob:"8eba43d142c819c206dce5df87ea4571aaead287",helper_support:S,helper_chart_normals:[1,18,31],outside_canonical_restriction_ranks:zeroRanks,valid_receivers:valid,canonical_choices_exhausted:512,scope:"Every characteristic-two field and block width for unchanged Q=G+bI with G canonical",new_complete_kappa:false};
}
if(typeof process!=="undefined"&&process.argv[1]&&import.meta.url===new URL("file://"+process.argv[1]).href){
 const {readFileSync}=await import("node:fs"),{createHash}=await import("node:crypto");
 if(!process.argv[2])throw Error("Usage: node check_survivor.mjs RECOVERED-NATIVE-ROOTS.json");
 const raw=readFileSync(process.argv[2]),sha=createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
 if(sha!=="8eba43d142c819c206dce5df87ea4571aaead287")throw Error("Source Git blob mismatch");
 process.stdout.write(JSON.stringify(checkD5Survivor(JSON.parse(raw.toString("utf8"))),null,2)+"\n");
}
