// Finite controls on the actual graded interpolation rows for composite field degrees.
// Run with: node verify-four-point-all-degrees.js
function field(b) {
  const h={4:0x13,6:0x43,8:0x11b,9:0x211}[b], q=2**b;
  function mul(a,v) {
    let out=0;
    while(v){if(v&1)out^=a;v>>>=1;a<<=1;if(a&q)a^=h;}
    return out;
  }
  function pow(a,e) {
    let out=1;
    while(e){if(e&1)out=mul(out,a);e>>>=1;a=mul(a,a);}
    return out;
  }
  const sq=Array.from({length:q},(_,x)=>mul(x,x));
  const inv=Array.from({length:q},(_,x)=>x?pow(x,q-2):0);
  for(let x=1;x<q;++x)if(mul(x,inv[x])!==1)throw Error("bad field modulus");
  return {b,q,mul,pow,sq,inv};
}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
function key(a){return [...a].sort((x,y)=>x-y).join(",");}
function partition(U,F) {
  const result=[],seen=new Set();
  for(let a=0;a<F.q;++a)if(!seen.has(a)){
    const A=U.map(z=>a^z);A.forEach(z=>seen.add(z));result.push(A);
  }
  return result;
}
function parameters(eta,F) {
  const U=[0,1,eta,eta^1], H=[], conj=[];
  let z=eta, d=0;
  for(let i=0;i<F.b;++i) {
    conj.push(z);
    if(z===eta||z===(eta^1))H.push(i);
    z=F.sq[z];if(!d&&z===eta)d=i+1;
  }
  const predicted=d%2===0&&conj[d/2]===(eta^1)?d/2:d;
  const r=F.b/H.length;
  if(r!==predicted||((r===1)!==(d===2)))throw Error("wrong stabilizer formula");
  return {U,d,r,H};
}
// Coefficients of the four delta polynomials in 1,X,s,Xs for s=X^2+X.
function interpolationRows(A,F) {
  const rows=[[],[],[],[]];
  for(const z of A) {
    let denom=1, poly=[1];
    for(const w of A)if(w!==z){
      denom=F.mul(denom,z^w);
      const next=Array(poly.length+1).fill(0);
      poly.forEach((c,j)=>{next[j]^=F.mul(c,w);next[j+1]^=c;});poly=next;
    }
    const c=poly.map(x=>F.mul(x,F.inv[denom]));
    [c[0],c[1]^c[2]^c[3],c[2]^c[3],c[3]].forEach((v,h)=>{if(v)rows[h].push([z,v]);});
  }
  return rows;
}
function rowKey(row,F) {
  const sorted=[...row].sort(([x],[y])=>x-y), inverse=F.inv[sorted[0][1]];
  return sorted.map(([z,c])=>z+"="+F.mul(c,inverse)).join(",");
}
function conjugate(row,F) {return row.map(([z,c])=>[F.sq[z],F.sq[c]]);}
function binaryRank(values,b) {
  const pivots=Array(b).fill(0);
  for(let x of values)for(let i=b-1;x&&i>=0;--i) {
    if(!(x&(1<<i)))continue;
    if(pivots[i])x^=pivots[i];else{pivots[i]=x;break;}
  }
  return pivots.filter(Boolean).length;
}
function checkLayout(eta,F) {
  const {d,r,H,U}=parameters(eta,F), blocks=partition(U,F);
  const rows=blocks.map(A=>interpolationRows(A,F));
  const allRows=new Set(rows.flat().map(row=>rowKey(row,F)));
  if(allRows.size!==F.q)throw Error("dependent rows");
  const mono=rows.flat().every(row=>allRows.has(rowKey(conjugate(row,F),F)));
  if(mono!==(d===2))throw Error("four-point monomial criterion");
  let good=0;const topClasses=new Set();
  for(let ia=0;ia<blocks.length;++ia) {
    const A=blocks[ia],seen=new Set(A);
    let S=[...A],disjoint=true,top=rows[ia][3],conjKey=rowKey(top,F);
    for(let i=1;i<F.b;++i) {
      top=conjugate(top,F);const signature=rowKey(top,F);
      if(signature<conjKey)conjKey=signature;
      S=S.map(z=>F.sq[z]);
      if(S.some(z=>seen.has(z)))disjoint=false;
      S.forEach(z=>seen.add(z));
    }
    if(!disjoint)continue; ++good;topClasses.add(conjKey);
    const weighted=rows[ia][3], powers=A.map(()=>1),cols=[];
    for(let j=0;j<F.q;++j) {
      cols.push(weighted.reduce((s,[,w],i)=>s^F.mul(w,powers[i]),0));
      A.forEach((z,i)=>{powers[i]=F.mul(z,powers[i]);});
      if(j%16===15&&binaryRank(cols,F.b)===F.b)break;
    }
    if(binaryRank(cols,F.b)!==F.b)throw Error("small-range good row");
  }
  let sum=0;for(let i=1;i<F.b;++i)sum+=2**gcd(i,F.b);
  if(good<blocks.length-2*sum||topClasses.size*H.length!==good)throw Error("orbit count");
  return {d,r,eta,stable:mono,good,goodTopClasses:topClasses.size};
}
function run(b) {
  const F=field(b), summaries=new Map(), counts=new Map();
  for(let eta=2;eta<F.q;++eta) {
    const {d,r}=parameters(eta,F), id=d+"/"+r;
    if(!summaries.has(id))summaries.set(id,checkLayout(eta,F));
    counts.set(id,(counts.get(id)||0)+1);
  }
  const families=[...summaries.entries()].map(([id,x])=>({...x,etaCount:counts.get(id)}))
    .sort((x,y)=>x.d-y.d||x.r-y.r);
  if(b%2===0&&!families.some(x=>x.d===2&&x.stable))throw Error("missing F4 control");
  if(b%2===1&&families.some(x=>x.stable))throw Error("odd stable flag");
  if(b===9) {
    const traceZeroF8=Array.from({length:F.q},(_,x)=>x).filter(x=>
      F.pow(x,8)===x && (x^F.sq[x]^F.sq[F.sq[x]])===0);
    if(traceZeroF8.length!==4||traceZeroF8.includes(1)||key(traceZeroF8)!==key(traceZeroF8.map(x=>F.sq[x])))
      throw Error("odd composite stable plane outside scope");
  }
  return {b,fieldElementsExamined:F.q-2,families};
}
console.log(JSON.stringify([4,6,8,9].map(run),null,2));
