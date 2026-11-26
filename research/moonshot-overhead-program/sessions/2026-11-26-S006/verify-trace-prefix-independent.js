// Independent byte-array and field oracles for the trace coefficient prefix and grouped CRT.
// Run with node verify-trace-prefix-independent.js. The verifier uses dense arithmetic.

function pRem(x,y) {
  const d=31-Math.clz32(y);
  while(x&&31-Math.clz32(x)>=d)x^=y<<(31-Math.clz32(x)-d);
  return x;
}
function pGcd(x,y){while(y)[x,y]=[y,pRem(x,y)];return x;}
function field(b) {
  const q=2**b; let h=q+1;
  const checks=new Set(); let degree=b;
  for(let p=2;p<=degree;p++)if(degree%p===0){checks.add(b/p);while(degree%p===0)degree/=p;}
  function raw(a,v) {
    let x=0;
    while(v){if(v&1)x^=a;v>>>=1;a<<=1;if(a&q)a^=h;}
    return x;
  }
  for(;h<2*q;h+=2) {
    let x=2,pass=true;
    for(let k=1;k<=b;++k) {
      x=raw(x,x);
      if(checks.has(k)&&pGcd(x^2,h)!==1){pass=false;break;}
    }
    if(pass&&x===2)break;
  }
  if(h>=2*q)throw Error("field construction");
  let mul=raw;
  if(b<=9) {
    const table=Array.from({length:q},(_,a)=>Uint32Array.from({length:q},(_,v)=>raw(a,v)));
    mul=(a,v)=>table[a][v];
  }
  function sq(x){return mul(x,x);}
  function frob(x,j){while(j--)x=sq(x);return x;}
  function pow(x,e) {
    let z=1;
    while(e){if(e&1)z=mul(z,x);e>>>=1;x=sq(x);}
    return z;
  }
  function inv(x){if(!x)throw Error("zero inverse");return pow(x,q-2);}
  return {b,q,h,mul,sq,frob,pow,inv};
}

function must(ok,s){if(!ok)throw Error(s);}
function same(a,b){return a.length===b.length&&a.every((x,i)=>x===b[i]);}
function terms(c,i) {
  const support=new Set();
  for(const e of [1,2**c,2**(2*c)])for(const t of [e,2*e]) {
    if(support.has(t))support.delete(t);else support.add(t);
  }
  return [...support].map(t=>t*2**i).sort((a,b)=>a-b);
}
function longDiv(bits,exps) {
  const h=exps.at(-1), a=bits.slice(), q=new Uint8Array(h);
  must(a.length===2*h,"parent width");
  for(let i=2*h-1;i>=h;--i)if(a[i]) {
    q[i-h]=1;for(const e of exps)a[i-h+e]^=1;
  }
  must(a.slice(h).every(x=>x===0),"uncancelled high term");
  return [a.slice(0,h),q];
}
function dMap(x,exps) {
  const h=x.length,z=new Uint8Array(h);
  for(const e of exps)for(let i=0;i<e;++i)z[i]^=x[h-e+i];
  return z;
}
function lowMap(x,exps) {
  const h=x.length,z=new Uint8Array(h);
  for(const e of exps)for(let i=e;i<h;++i)z[i]^=x[i-e];
  return z;
}
function xor(x,y){return Uint8Array.from(x,(e,i)=>e^y[i]);}
function split(bits,exps) {
  const h=bits.length/2,E=exps.slice(0,-1),A=bits.slice(0,h),B=bits.slice(h);
  const D=dMap(B,E),Q=xor(B,D),R=xor(A,lowMap(Q,E));
  must(D.slice(h/2).every(x=>x===0)&&dMap(D,E).every(x=>x===0),"degree gap");
  return [R,Q];
}
function combine(R,Q,exps) {
  const E=exps.slice(0,-1), h=Q.length,z=new Uint8Array(2*h);
  z.set(xor(R,lowMap(Q,E)),0);z.set(xor(Q,dMap(Q,E)),h);return z;
}
function prefix(input,c,r,counts) {
  let parents=[input];
  for(let i=c-2;i>=c-1-r;--i) {
    const exps=terms(c,i), next=[];
    for(const p of parents) {
      const got=split(p,exps),div=longDiv(p,exps);
      must(same(got[0],div[0])&&same(got[1],div[1]),"ordinary long division");
      must(same(combine(got[0],got[1],exps),p),"local round trip");
      next.push(...got);counts.divisions++;
    }
    parents=next;
  }
  return parents;
}
function inverse(digits,c,r) {
  let nodes=digits.slice();
  for(let i=c-1-r;i<c-1;++i) {
    const next=[], exps=terms(c,i);
    for(let j=0;j<nodes.length;j+=2)next.push(combine(nodes[j],nodes[j+1],exps));
    nodes=next;
  }
  return nodes[0];
}
function directHorner(digits,c,r) {
  const exps=terms(c,c-1-r),d=digits[0].length;
  let z=digits.at(-1).slice();
  for(let j=digits.length-2;j>=0;--j) {
    const w=new Uint8Array(z.length+d);
    for(const e of exps)for(let i=0;i<z.length;i++)w[i+e]^=z[i];
    for(let i=0;i<d;i++)w[i]^=digits[j][i];
    z=w;
  }
  return z;
}
function fixture(n,seed) {
  let a=seed>>>0;
  return Uint8Array.from({length:n},()=>{a=(Math.imul(a,1664525)+1013904223)>>>0;return a>>>31;});
}

function localCheck(b) {
  const c=b/3,q=2**b,m=c-1,counts={b,forward:0,inverseFirst:0,divisions:0,flatIdentities:0};
  for(let r=0;r<=m;r++) {
    const inputs=[];
    if(b===3)for(let mask=0;mask<256;mask++)inputs.push(Uint8Array.from({length:q},(_,i)=>(mask>>i)&1));
    if(b===6||b===9)for(let i=0;i<q;i++){const p=new Uint8Array(q);p[i]=1;inputs.push(p);}
    for(let t=0;t<6;t++)inputs.push(fixture(q,314+t+47*r));
    for(const p of inputs) {
      const digits=prefix(p,c,r,counts);
      must(same(inverse(digits,c,r),p)&&same(directHorner(digits,c,r),p),"prefix reconstruction");
      counts.forward++;counts.flatIdentities++;
    }
    const n=2**r,d=q/n,targets=[];
    for(let t=0;t<9;t++)targets.push(Array.from({length:n},(_,j)=>fixture(d,98233+17*j+391*t+r)));
    if(b===6||b===9)for(let k=0;k<q;++k) {
      const a=Array.from({length:n},()=>new Uint8Array(d));a[Math.floor(k/d)][k%d]=1;targets.push(a);
    }
    for(const target of targets) {
      const p=inverse(target,c,r);
      must(same(p,directHorner(target,c,r)),"inverse-first dense Horner");
      const digits=prefix(p,c,r,counts);
      must(digits.every((v,j)=>same(v,target[j])),"arbitrary tuple round trip");
      counts.inverseFirst++;counts.flatIdentities++;
    }
  }
  return counts;
}

function sparseConvolve(f,exps){
 const z=new Uint8Array(f.length+exps.at(-1));
 for(const e of exps)for(let i=0;i<f.length;i++)z[i+e]^=f[i];return z;
}
function expsOf(p){const e=[];p.forEach((v,i)=>{if(v)e.push(i);});return e;}
function descend(f,div,field=null) {
 const t=div.length-1,rem=field?Uint32Array.from(f):Uint8Array.from(f),nonzero=[];
 for(let i=0;i<=t;i++)if(div[i])nonzero.push([i,div[i]]);
 for(let i=f.length-1;i>=t;--i)if(rem[i]) {
   const x=rem[i];for(const [e,y]of nonzero)rem[i-t+e]^=field&&y!==1?field.mul(x,y):x;
 }
 return rem.slice(0,t);
}
function minPoly(F,s) {
 const roots=[];let x=s;
 do {roots.push(x);x=F.sq(x);}while(x!==s);
 let p=[1];for(const y of roots) {
  const z=Array(p.length+1).fill(0);p.forEach((v,j)=>{z[j]^=F.mul(v,y);z[j+1]^=v;});p=z;
 }
 must(p.every(x=>x===0||x===1),"nonbinary minimal polynomial");return {roots,p:Uint8Array.from(p)};
}
function evalp(F,p,x){let v=0;for(let i=p.length-1;i>=0;--i)v=F.mul(v,x)^p[i];return v;}
function hbase(digits,exps){
 let z=digits.at(-1).slice();for(let i=digits.length-2;i>=0;--i){
  z=sparseConvolve(z,exps);digits[i].forEach((x,k)=>{z[k]^=x;});
 }return z;
}
function groupedTest(b) {
 const F=field(b),c=b/3,q=F.q,m=c-1,M=2**m,v=q/M,E=terms(c,0),
  groups=new Map(),mp=new Map(),fieldAll=b<=12,checks={b,points:0,cosets:0,orbits:0,
  irreducibles:0,factorProductIdentities:0,cosetRemainders:0,
  cosetWordComparisons:0,groupedRemainders:0,coordinateTables:0};
 function tr(z){return z^F.frob(z,c)^F.frob(z,2*c);}
 function S(z){const t=tr(z);return t^F.sq(t);}
 const simple=new Uint8Array(v+1);for(const e of E)simple[e]=1;
 for(let x=0;x<q;x++){
  const s=S(x);
  if(fieldAll)must(s===E.reduce((a,e)=>a^F.pow(x,e),0),"relative trace vs actual polynomial");
  if(!groups.has(s))groups.set(s,[]);groups.get(s).push(x);checks.points++;
 }
 must(groups.size===M&&[...groups.values()].every(x=>x.length===v),"actual fibres");
 const covered=new Set();
 for(const s of [...groups.keys()].sort((a,b)=>a-b))if(!covered.has(s)) {
  const o=minPoly(F,s);o.roots.forEach(t=>covered.add(t));
  let composite=Uint8Array.of(1);for(let j=o.p.length-2;j>=0;--j){
    composite=sparseConvolve(composite,E);composite[0]^=o.p[j];}
  mp.set(s,{...o,composite});checks.orbits++;
 }
 if(fieldAll){
  const seen=new Set();
  for(const [s,{roots,composite}] of mp) {
   let product=Uint8Array.of(1);
   for(const t of roots)for(const x of groups.get(t))if(!seen.has(x)){
    const g=minPoly(F,x);g.roots.forEach(z=>seen.add(z));
    must(g.roots.every(z=>roots.includes(S(z))),"irreducible straddles classes");
    product=sparseConvolve(product,expsOf(g.p));checks.irreducibles++;
   }
   must(same(product,composite),"wrong grouped irreducible product");checks.factorProductIdentities++;
  }
  must(seen.size===q,"unclassified factor roots");
 }
 checks.cosets=groups.size;
 const order=[...mp.values()],seenTuples=new Set();
 for(let n=0;n<2**M;n++){
  const g=Uint8Array.from({length:M},(_,k)=>(n>>>k)&1);
  let pack=0,j=0;
  for(const {p} of order){const rem=descend(g,p);for(const bit of rem)pack|=bit<<j++;}
  must(j===M&&!seenTuples.has(pack),"rank deficiency in grouped coordinates");seenTuples.add(pack);
 }
 checks.coordinateTables=seenTuples.size;
 if(fieldAll)for(let trial=0;trial<6;trial++){
  const f=fixture(q,947+trial*319);
  let digits=[f];
  for(let i=m-1;i>=0;i--)digits=digits.flatMap(p=>longDiv(p,terms(c,i)));
  const g=Array.from({length:v},(_,k)=>Uint8Array.from(digits,p=>p[k]));
  for(const [s,points] of groups) {
   const div=Uint32Array.from(simple);div[0]^=s;
   const literal=descend(f,div,F),pred=Uint32Array.from(g,p=>evalp(F,p,s));
   must(same(literal,pred),"actual coset polynomial remainder");
   const x=points[trial%points.length];
   must(evalp(F,literal,x)===evalp(F,f,x),"remainder on actual root");
   checks.cosetRemainders++;checks.cosetWordComparisons+=v;
  }
  for(const {p,composite}of order){
   const r=p.length-1,coordinates=g.map(a=>descend(a,p));
   const mixed=Array.from({length:r},(_,j)=>Uint8Array.from(coordinates,a=>a[j]));
   must(same(hbase(mixed,E),descend(f,composite)),"actual grouped polynomial remainder");
   checks.groupedRemainders++;
  }
 }
 return checks;
}
const counts={coefficientPrefix:[3,6,9,12,15,18].map(localCheck),groupedOrbit:[3,6,9,12,15].map(groupedTest)};
console.log(JSON.stringify(counts,null,2));
