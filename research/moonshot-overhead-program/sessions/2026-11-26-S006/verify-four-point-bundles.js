// Exact finite checks for the whole-block Frobenius coarsening theorem.
// Run with: node verify-four-point-bundles.js
function gcd(a,b) {
  while (b) [a,b]=[b,a%b];
  return a;
}
function binaryBasis(vectors,n) {
  const pivots=new Uint32Array(n);
  let rank=0;
  for (let v of vectors) {
    for (let j=n-1;v&&j>=0;--j) {
      if (!(v&(1<<j))) continue;
      if (pivots[j]) v^=pivots[j];
      else {pivots[j]=v; ++rank; break;}
    }
  }
  function reduce(v) {
    for (let j=n-1;j>=0;--j) if (v&(1<<j)) v^=pivots[j];
    return v;
  }
  return {rank,reduce};
}
function order2(e) {
  let residue=2%e, order=1;
  while (residue!==1) {residue=2*residue%e; ++order;}
  return order;
}
function formula(n) {
  let a=0,m=n;
  while(m%2===0){m/=2;++a;}
  const best=new Map([[1,0]]);
  for(let e=3;e<=m;e+=2) {
    if(m%e) continue;
    const cost=order2(e);
    for(const [existing,oldCost] of [...best]) {
      const lcm=existing*e/gcd(existing,e);
      best.set(lcm,Math.min(best.get(lcm)??Infinity,oldCost+cost));
    }
  }
  return 1+(a===0?0:2**(a-1))+best.get(m);
}
function polynomialRemainder(p,d) {
  const h=31-Math.clz32(d);
  while (p&&(31-Math.clz32(p))>=h) p^=d<<(31-Math.clz32(p)-h);
  return p;
}
function field(n) {
  const q=2**n;
  let modulus=q+1;
  for (;modulus<2*q;modulus+=2) {
    let irreducible=true;
    for(let deg=1;deg<=Math.floor(n/2)&&irreducible;++deg) {
      for(let d=2**deg+1;d<2**(deg+1);d+=2) {
        if(polynomialRemainder(modulus,d)===0){irreducible=false;break;}
      }
    }
    if(irreducible)break;
  }
  if(modulus>=2*q) throw Error("field construction");
  function mul(a,b) {
    let r=0;
    while(b) {
      if(b&1)r^=a;
      a<<=1; if(a&q)a^=modulus;
      b>>>=1;
    }
    return r;
  }
  function power(a,e) {
    let r=1;
    while(e){if(e&1)r=mul(r,a); e>>>=1;a=mul(a,a);}
    return r;
  }
  const square=Array.from({length:q},(_,i)=>mul(i,i));
  return {n,q,square,mul,power,modulus};
}
function orbit(x,op) {
  const values=[];let y=x;
  do{values.push(y);y=op(y);}while(y!==x);
  return values;
}
function directField(n) {
  const F=field(n), records=new Map();
  let min=n+1, full=0;
  for(let eta=2;eta<F.q;++eta) {
    const values=orbit(eta,z=>F.square[z]);
    const V=binaryBasis([1,...values],n);
    if(values.length===n){++full;min=Math.min(min,V.rank);}
    if(n<=9){
      const key=values.length+"/"+V.rank;
      if(!records.has(key)) records.set(key,{eta,d:values.length,dim:V.rank});
      checkCoarsening(eta,V,F);
    }
  }
  if(min!==formula(n)) throw Error("polynomial-basis minimum");
  if(n<=9)for(const rec of records.values())checkInterpolation(rec.eta,F);
  return {n,full,min,groupedPlanes:n<=9?F.q-2:0,interpolationFamilies:records.size};
}
// Compute the least invariant partition by repeated equivalence-class merges,
// without using the span formula. Compare to that formula only after convergence.
function checkCoarsening(eta,V,F) {
  const parent=Uint32Array.from({length:F.q},(_,i)=>i);
  function root(x) {
    while(x!==parent[x]) {parent[x]=parent[parent[x]];x=parent[x];}
    return x;
  }
  function join(x,y) {
    const a=root(x),b=root(y);
    if(a===b)return false;
    parent[b]=a;return true;
  }
  for(let x=0;x<F.q;++x){join(x,x^1);join(x,x^eta);}
  let steps=0;
  while(true) {
    const snapshot=Array.from({length:F.q},(_,i)=>root(i));
    let changed=false;
    for(let x=0;x<F.q;++x) {
      if(join(F.square[x],F.square[snapshot[x]]))changed=true;
    }
    if(!changed)break;
    if(++steps>F.n)throw Error("failed to stabilize partitions");
  }
  const quotientToClass=new Map(), classToQuotient=new Map();
  for(let x=0;x<F.q;++x) {
    const repr=V.reduce(x), label=root(x);
    if(quotientToClass.has(repr)&&quotientToClass.get(repr)!==label)throw Error("split span coset");
    if(classToQuotient.has(label)&&classToQuotient.get(label)!==repr)throw Error("overmerged partition");
    quotientToClass.set(repr,label);classToQuotient.set(label,repr);
  }
  if(classToQuotient.size!==2**(F.n-V.rank))throw Error("wrong partition size");
}
function inverse(m,F) {
  const n=m.length;
  const rows=m.map((r,i)=>[...r,...Array.from({length:n},(_,j)=>Number(i===j))]);
  for(let j=0;j<n;++j){
    const h=rows.findIndex((r,i)=>i>=j&&r[j]!==0);
    if(h<0)throw Error("lost row subspace");
    [rows[j],rows[h]]=[rows[h],rows[j]];
    const scale=F.power(rows[j][j],F.q-2);
    for(let k=j;k<2*n;++k)rows[j][k]=F.mul(rows[j][k],scale);
    for(let i=0;i<n;++i)if(i!==j&&rows[i][j]) {
      const c=rows[i][j];for(let k=j;k<2*n;++k)rows[i][k]^=F.mul(c,rows[j][k]);
    }
  }
  return rows.map(r=>r.slice(n));
}
function checkInterpolation(eta,F) {
  const seen=new Set();
  for(let a=0;a<F.q;++a) {
    if(seen.has(a))continue;
    const A=[a,a^1,a^eta,a^1^eta];A.forEach(z=>seen.add(z));
    const evaluation=A.map(z=>{const s=F.square[z]^z;return [1,z,s,F.mul(z,s)];});
    const rows=inverse(evaluation,F);
    // Elementary invertible row mixings preserve the local full support subspace.
    for(let j=0;j<4;++j)for(let k=0;k<4;++k)if(k!==j) {
      const c=A[k]^1;
      for(let t=0;t<4;++t)rows[j][t]^=F.mul(c,rows[k][t]);
    }
    inverse(rows,F);
  }
}
// Enumerate necklaces in a normal basis. Every primitive necklace contributes n field elements.
function cyclicMinimum(n) {
  const N=2**n, all=N-1, seen=new Uint8Array(N);
  let min=n+1, full=0, minimizers=0;
  function rotate(x){return ((x<<1)&all)|(x>>>(n-1));}
  for(let x=1;x<all;++x)if(!seen[x]) {
    const values=orbit(x,rotate);values.forEach(y=>{seen[y]=1;});
    if(values.length!==n)continue;
    full+=n;
    const rank=binaryBasis([all,...values],n).rank;
    if(rank<min){min=rank;minimizers=0;}
    if(rank===min)minimizers+=n;
  }
  if(min!==formula(n))throw Error("cyclic-basis minimum");
  return {n,full,min,minimizers};
}
function sharpTriple(t) {
  const n=3**t, h=n/3, one=(1n<<BigInt(n))-1n;
  function rotate(x){return ((x<<1n)&one)|(x>>BigInt(n-1));}
  const eta=1n|(1n<<BigInt(h)), a=orbit(eta,rotate), basis=Array(n).fill(0n);
  let rank=0;
  for(let val of [one,...a])for(let j=n-1;val&&j>=0;--j) {
    if(!(val&(1n<<BigInt(j))))continue;
    if(basis[j])val^=basis[j];else{basis[j]=val;++rank;break;}
  }
  if(a.length!==n||rank!==2*h+1)throw Error("sharp 3-power witness");
  return {b:n,orbit:a.length,dimension:rank};
}
const degrees=Array.from({length:11},(_,i)=>i+2);
const fieldResults=degrees.map(directField);
const cyclicResults=[...degrees,15,21].map(cyclicMinimum);
for(let i=0;i<degrees.length;++i)if(fieldResults[i].full!==cyclicResults[i].full)
  throw Error("incompatible basis counts");
if(formula(15)!==5||formula(21)!==6)throw Error("odd LCM cover adverse cases");
console.log(JSON.stringify({fieldResults,cyclicResults,triple:[1,2,3,4,5].map(sharpTriple)},null,2));
