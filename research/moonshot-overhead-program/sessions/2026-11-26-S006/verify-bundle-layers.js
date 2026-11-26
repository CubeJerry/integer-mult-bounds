// Independent finite controls for consecutive additive layers on representative bundles.
// Run with: node verify-bundle-layers.js
// Dense matrices below are test oracles, outside the proposed tape algorithm.
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
function orderedBasis(inputs,n) {
  const pivots=Array(n).fill(0), basis=[];
  for(const x of inputs) {
    let y=x;for(let j=n-1;y&&j>=0;--j) {
      if(!(y&(1<<j)))continue;
      if(pivots[j])y^=pivots[j];
      else {pivots[j]=y;basis.push(x);break;}
    }
  }
  return basis;
}
function span(basis) {
  let arr=[0];
  for(const z of basis)arr=arr.concat(arr.map(x=>x^z));
  return arr;
}
function setup(F,top) {
  const c=F.b/3, eg=[],lg=[];
  for(let j=0;j<F.b;++j) {
    const x=2**j, y=F.frob(x,c);
    eg.push(x^y); lg.push(x^y^F.frob(y,c));
  }
  const orbit=x=>Array.from({length:F.b},(_,i)=>F.frob(x,i));
  // Deterministic pseudorandom test fixtures. The uniform algorithm can use
  // the standing deterministic small-field normal-basis construction.
  let seed=1729,alpha=0;
  for(let i=0;i<5000&&!alpha;++i) {
    seed=(Math.imul(1664525,seed)+1013904223)>>>0;
    const x=seed%F.q;
    if(orderedBasis(orbit(x),F.b).length===F.b)alpha=x;
  }
  if(!alpha)throw Error("missing normal test fixture");
  const eta=alpha^F.frob(alpha,c), etaOrbit=orbit(eta);
  if(new Set(etaOrbit).size!==F.b||orderedBasis(etaOrbit,F.b).length!==2*c)
    throw Error("normal-pair degree or rank");
  const V=orderedBasis([1,eta,...eg],F.b);
  const lBasis=orderedBasis([1,...lg],F.b);
  const T=span(lBasis.slice(1)).sort((a,b)=>a-b);
  if(V.length!==2*c+1||lBasis.length!==c||T.length!==2**(c-1))
    throw Error("wrong trace split");
  const section=new Map();
  for(const t of T){section.set(t,t);section.set(t^1,t);}
  const seen=new Set(),reps=[],stab=[],fixed=[];
  let offsetBundles=0;
  for(const t of T)if(!seen.has(t)) {
    reps.push(t);let z=t,n=0;
    do {if(seen.has(z))throw Error("quotient orbit collision");
      seen.add(z);z=section.get(F.sq(z));++n;}while(z!==t);
    const epsilon=F.frob(t,n)^t;
    if(epsilon>1)throw Error("quotient period");
    stab.push([n,epsilon]);offsetBundles+=epsilon;
  }
  for(let i=0;i<c;++i) {
    const actual=T.filter(t=>section.get(F.frob(t,i))===t).length;
    let a=c,g=i;while(g)[a,g]=[g,a%g];
    const formula=2**(a-1)*(1+Number((c/a)%2===0));
    if(actual!==formula)throw Error("quotient Burnside fixed-space count");
    fixed.push(actual);
  }
  if(fixed.reduce((a,x)=>a+x,0)!==c*reps.length)throw Error("Burnside quotient count");
  if(c===2&&offsetBundles===0)throw Error("missing nonsplit even-c control");
  const S=[[1]],gammas=[],direct=[];
  function linearEval(s,x) {
    let ans=0;
    for(const c of s){ans^=F.mul(c,x);x=F.sq(x);}
    return ans;
  }
  function horner(poly,x){let v=0;for(let i=poly.length-1;i>=0;--i)v=F.mul(v,x)^poly[i];return v;}
  for(let j=0;j<=top;++j) {
    let p=[1];for(const u of span(V.slice(0,j))) {
      const next=Array(p.length+1).fill(0);
      p.forEach((w,i)=>{next[i]^=F.mul(w,u);next[i+1]^=w;});p=next;
    }
    direct.push(p);
    const dense=Array(2**j+1).fill(0);S[j].forEach((w,i)=>{dense[2**i]=w;});
    if(p.some((x,i)=>x!==dense[i]))throw Error("subspace polynomial mismatch");
    if(j===top)break;
    const gamma=linearEval(S[j],V[j]);if(!gamma)throw Error("zero gamma");
    gammas.push(gamma);
    const next=Array(S[j].length+1).fill(0);
    S[j].forEach((w,i)=>{next[i]^=F.mul(gamma,w);next[i+1]^=F.sq(w);});
    S.push(next);
  }
  const basisPolys=[[1]];
  for(let h=1;h<2**top;++h) {
    const j=31-Math.clz32(h), rest=h-2**j, p=Array(h+1).fill(0);
    // This dense oracle is built from direct products over the actual subspaces.
    for(let k=0;k<direct[j].length;++k)if(direct[j][k])
      for(let z=0;z<basisPolys[rest].length;++z)p[k+z]^=F.mul(direct[j][k],basisPolys[rest][z]);
    if(p[h]!==1)throw Error("nonmonic graded basis");
    basisPolys.push(p);
  }
  return {c,V,reps,stab,fixed,offsetBundles,eta,S,gammas,basisPolys,linearEval,horner};
}
function makePiece(anchor,top,P,F) {
  const points=span(P.V.slice(0,top)).map(x=>x^anchor);
  const kernels=[],plans=[];
  for(let j=0;j<=top;++j) {
    const m=2**j, local=[];
    for(let i0=0;i0<points.length;i0+=m) {
      const A=points.slice(i0,i0+m);
      let van=[1]; for(const z of A) {
        const next=Array(van.length+1).fill(0);
        van.forEach((c,i)=>{next[i]^=F.mul(c,z);next[i+1]^=c;});van=next;
      }
      const columns=[];
      for(const z of A) {
        const denominator=A.reduce((v,w)=>w===z?v:F.mul(v,w^z),1), factor=F.inv(denominator);
        const rem=Array(m);rem[m-1]=van[m];
        for(let k=m-1;k>0;--k)rem[k-1]=van[k]^F.mul(z,rem[k]);
        for(let k=0;k<m;++k)rem[k]=F.mul(rem[k],factor);
        // Change this delta polynomial from global monomials by monic triangular elimination.
        const coord=Array(m).fill(0);
        for(let h=m-1;h>=0;--h){
          coord[h]=rem[h];if(!coord[h])continue;
          P.basisPolys[h].forEach((w,i)=>{rem[i]^=F.mul(coord[h],w);});
        }
        if(rem.some(Boolean))throw Error("incomplete independent interpolation");
        columns.push(coord);
      }
      local.push(columns);
    }
    kernels.push(local);
    if(j===top)break;
    const count=points.length/(2*m), w=[];
    let tw=P.linearEval(P.S[j],anchor), pref=0;
    const increments=P.V.slice(j+1,top).map(e=>{pref^=P.linearEval(P.S[j],e);return pref;});
    for(let i=0;i<count;++i) {
      w.push(tw);
      if(tw!==P.linearEval(P.S[j],points[2*m*i]))throw Error("twiddle order");
      if(i+1===count)break;
      let k=0;while((i>>k)&1)++k;tw^=increments[k];
    }
    plans.push({w,gamma:P.gammas[j],invertGamma:F.inv(P.gammas[j])});
  }
  function expected(y,j) {
    const m=2**j,out=[];
    kernels[j].forEach((columns,ix)=>{
      const p=Array(m).fill(0);
      columns.forEach((col,h)=>{const val=y[ix*m+h];col.forEach((w,i)=>{p[i]^=F.mul(val,w);});});
      out.push(...p);
    });
    return out;
  }
  function layer(input,j,reverse=false,normalized=false,adverse="") {
    const m=2**j, out=Array(points.length), {w,gamma,invertGamma}=plans[j];
    for(let p=0;p<w.length;++p){
      const k=p*2*m, t=adverse==="offset"?w[0]:w[p];
      const weight=normalized?F.mul(t,invertGamma):t;
      const gap=(normalized||adverse==="unit")?1:gamma;
      for(let h=0;h<m;++h){
        const a=input[k+h],b=input[k+m+h];
        let low,high;
        if(reverse) {
          high=F.mul(a^b,normalized?1:invertGamma);
          low=a^F.mul(weight,high);
        } else {
          low=a^F.mul(weight,b);high=low^F.mul(gap,b);
        }
        if(adverse==="order"){out[k+2*h]=low;out[k+2*h+1]=high;}
        else {out[k+h]=low;out[k+m+h]=high;}
      }
    }
    return out;
  }
  return {points,expected,layer,top};
}
function run(b) {
  const F=field(b), top=b<=9?2*(b/3)+1:6, P=setup(F,top);
  const full=top===P.V.length;
  const slices=full?P.reps.map(t=>[t,0]):[
    [P.reps[0],0],[P.reps[1],3],[P.reps[P.reps.length-1],2**(P.V.length-top)-1]
  ];
  const pieces=slices.map(([t,mask])=>{
    let a=t;
    P.V.slice(top).forEach((v,j)=>{if((mask>>>j)&1)a^=v;});
    return makePiece(a,top,P,F);
  });
  const rejected={unit:false,offset:false,order:false,unconvertedNormalization:false};
  const choices=[
    Array(top).fill(false),Array(top).fill(true),
    Array.from({length:top},(_,j)=>j%2===0),
    Array.from({length:top},(_,j)=>j%2===1)
  ];
  const convention=choices.map(normalize=>{
    const scales=[1];
    for(let h=1;h<2**top;++h) {
      const j=31-Math.clz32(h);
      scales.push(F.mul(scales[h-2**j],normalize[j]?P.gammas[j]:1));
    }
    return {normalize,scales};
  });
  let inputs=0,chains=0,comparisons=0;
  function same(a,b){return a.length===b.length&&a.every((v,i)=>v===b[i]);}
  function check(p,y) {
    const raw=Array.from({length:top+1},(_,j)=>p.expected(y,j));
    if(!same(raw[0],y))throw Error("terminal point order");
    for(const {normalize,scales} of convention) {
      const levels=raw.map((arr,j)=>
        arr.map((z,h)=>F.mul(z,scales[h%(2**j)])));
      let work=levels[top];
      for(let j=top-1;j>=0;--j) {
        work=p.layer(work,j,false,normalize[j]);++comparisons;
        if(!same(work,levels[j]))throw Error("forward mismatch at "+j);
      }
      for(let j=0;j<top;++j) {
        work=p.layer(work,j,true,normalize[j]);++comparisons;
        if(!same(work,levels[j+1]))throw Error("reverse mismatch at "+j);
      }
      ++chains;
    }
    for(const tag of Object.keys(rejected))if(!rejected[tag])
      for(let j=top-1;j>=0;--j)
        if(!same(p.layer(raw[j+1],j,false,tag==="unconvertedNormalization",tag),raw[j])){
          rejected[tag]=true;break;
        }
  }
  if(full) {
    const y=pieces.map(p=>p.points.map(()=>1));
    for(let d=0;d<F.q;++d) {
      pieces.forEach((p,i)=>{
        check(p,y[i]);p.points.forEach((z,h)=>{y[i][h]=F.mul(y[i][h],z);});
      });
      ++inputs;
    }
  }
  for(let seed=1;seed<=8;++seed) {
    let rng=seed;const f=Array.from({length:Math.min(F.q,3*2**top+2)},()=>{
      rng=(Math.imul(1664525,rng)+1013904223)>>>0;return rng>>>31;
    });
    pieces.forEach(p=>check(p,p.points.map(z=>P.horner(f,z))));++inputs;
  }
  for(let seed=0;seed<4;++seed) {
    let rng=seed+31415;
    pieces.forEach(p=>check(p,p.points.map(()=>{
      rng=(Math.imul(rng,1103515245)+12345)>>>0;return rng%F.q;
    })));++inputs;
  }
  if(!Object.values(rejected).every(Boolean))throw Error("missing adverse control");
  let expandedPoints=0,untwistedRejected=0;
  for(let ix=0;ix<P.reps.length;++ix) {
    const [h,epsilon]=P.stab[ix], t=P.reps[ix];
    if(!epsilon)continue;
    // y(X)=X. The proposed relation without the affine offset fails on v=0.
    const correct=P.horner([0,1],t^epsilon), wrong=P.horner([0,1],t);
    if(F.frob(P.horner([0,1],t),h)!==correct||correct===wrong)
      throw Error("incorrect untwisted fixed-point control");
    ++untwistedRejected;
  }
  if(full) {
    // Independent binary polynomial, a fixed-point relation, and recovery of
    // all point values from the actually stored bundles (test only).
    const f=Array.from({length:29},(_,k)=>Number((k*k+2*k+5)%13<6));
    const recovered=new Map();
    for(let ix=0;ix<P.reps.length;++ix) {
      const t=P.reps[ix], [h,epsilon]=P.stab[ix], p=pieces[ix];
      for(const a of p.points) {
        const v=t^a;
        const target=t^F.frob(v,h)^epsilon;
        if(F.frob(P.horner(f,a),h)!==P.horner(f,target))throw Error("affine stabilizer");
        let u=a,value=P.horner(f,a);
        for(let i=0;i<F.b;i++) {
          if(recovered.has(u)&&recovered.get(u)!==value)throw Error("inconsistent expansion");
          recovered.set(u,value);u=F.sq(u);value=F.sq(value);
        }
      }
    }
    if(recovered.size!==F.q||[...recovered].some(([x,z])=>P.horner(f,x)!==z))
      throw Error("representative reconstruction");
    expandedPoints=recovered.size;
  }
  return {degree:b,modulus:F.h,eta:P.eta,bundleDimension:P.V.length,
    quotientFixed:P.fixed,representatives:P.reps.length,offsetBundles:P.offsetBundles,
    pieces:pieces.length,sliceDimension:top,inputs,chains,comparisons,expandedPoints,untwistedRejected,rejected};
}
console.log(JSON.stringify([3,6,9,12,15,18,27].map(run),null,2));
