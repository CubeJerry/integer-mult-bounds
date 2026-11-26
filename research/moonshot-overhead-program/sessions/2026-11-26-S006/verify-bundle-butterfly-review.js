// Run with: node verify-bundle-butterfly-review.js
function gcd(a,b) {
  while (b) [a,b]=[b,a%b];
  return a;
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

// Finite controls for one compressed U/W stage at b=3c, c a power of 3.
// Dense interpolation and full expansion below are correctness oracles.
function prepare(n) {
  const F=field(n), c=n/3, universe=Array.from({length:F.q},(_,i)=>i);
  function frob(x,j){while(j--)x=F.square[x];return x;}
  function traceL(x){let z=0;for(let i=0;i<c;++i){z^=x;x=F.square[x];}return z;}
  const E=universe.filter(z=>(z^frob(z,c)^frob(z,2*c))===0);
  const T=universe.filter(z=>frob(z,c)===z&&traceL(z)===0);
  const V=[...E,...E.map(z=>z^1)],eta=E.find(x=>x!==0);
  const trans=new Set();for(const t of T)for(const v of V)trans.add(t^v);
  if(trans.size!==F.q||V.length*T.length!==F.q)throw Error("bad complement");
  const orbits=new Set(),reps=[];
  for(const t of T)if(!orbits.has(t)){
    reps.push(t);
    let y=t;do{orbits.add(y);y=F.square[y];}while(y!==t);
  }
  let burnside=0;
  for(let i=0;i<c;++i)burnside+=2**(gcd(i,c)-1);
  if(reps.length*c!==burnside)throw Error("bad orbit count");
  const delta=F.square[eta]^eta, deltaInv=F.power(delta,F.q-2), circuits=[];
  for(const t of reps) {
    const seen=new Set();
    for(const v of V) {
      const a=t^v;
      if(seen.has(a))continue;
      const points=[a,a^1,a^eta,a^eta^1];points.forEach(z=>seen.add(z));
      const evalU=points.map(z=>{const h=F.square[z]^z;return [1,z,h,F.mul(z,h)];});
      circuits.push({a,points,evalU,interpU:inverse(evalU,F)});
    }
  }
  function apply(m,x){return m.map(r=>r.reduce((s,v,j)=>s^F.mul(v,x[j]),0));}
  function forward(p,a) {
    const h=F.square[a]^a;
    const q0=[p[0]^F.mul(h,p[2]),p[1]^F.mul(h,p[3])];
    return [...q0,q0[0]^F.mul(delta,p[2]),q0[1]^F.mul(delta,p[3])];
  }
  function reverse(q,a) {
    const h=F.square[a]^a, v=[F.mul(q[0]^q[2],deltaInv),F.mul(q[1]^q[3],deltaInv)];
    return [q[0]^F.mul(h,v[0]),q[1]^F.mul(h,v[1]),...v];
  }
  function expand(storedPoints) {
    const table=Array(F.q).fill(-1);
    for(const [arg,value] of storedPoints) {
      let z=arg,y=value;
      for(let j=0;j<n;++j) {
        if(table[z]!==-1&&table[z]!==y)throw Error("stabilizer inconsistency");
        table[z]=y;z=F.square[z];y=F.square[y];
      }
    }
    if(table.some(y=>y<0))throw Error("missing field point");
    return table;
  }
  function test(y) {
    const up=[],down=[];
    for(const {a,points,evalU,interpU} of circuits){
      const v=points.map(z=>y[z]);
      const p=apply(interpU,v),q=forward(p,a),back=reverse(q,a);
      const low=v[0]^v[1], high=v[2]^v[3];
      const direct=[v[0]^F.mul(a,low),low,v[2]^F.mul(a^eta,high),high];
      if(q.some((v,i)=>v!==direct[i])||back.some((v,i)=>v!==p[i]))throw Error("wrong butterfly");
      const recoveredU=apply(evalU,back);
      const recoveredW=points.map((z,i)=>q[2*(i>>1)]^F.mul(q[2*(i>>1)+1],z));
      points.forEach((z,i)=>{up.push([z,recoveredU[i]]);down.push([z,recoveredW[i]]);});
    }
    if(expand(up).some((v,i)=>v!==y[i])||expand(down).some((v,i)=>v!==y[i]))throw Error("wrong full table");
  }
  function negativeControl() {
    const carried=circuits.flatMap(({points})=>points.map(z=>[z,z===0?eta:0]));
    let rejected=false;
    try{expand(carried);}catch(e){rejected=e.message==="stabilizer inconsistency";}
    if(!rejected)throw Error("bad root point was accepted");
  }
  return {F,c,eta,reps:reps.length,VSize:V.length,quartets:circuits.length,test,negativeControl};
}
function denseCase(F,seed) {
  let x=seed;
  const coeff=Array.from({length:F.q},()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x>>>31;});
  return Array.from({length:F.q},(_,z)=>{
    let v=0;for(let j=coeff.length-1;j>=0;--j)v=F.mul(v,z)^coeff[j];return v;
  });
}
function run(b) {
  const s=prepare(b),F=s.F;let cases=0;
  if(b===3) {
    for(let mask=0;mask<2**F.q;++mask) {
      const y=Array.from({length:F.q},(_,z)=>{
        let v=0;for(let j=F.q-1;j>=0;--j)v=F.mul(v,z)^((mask>>>j)&1);return v;
      });
      s.test(y);++cases;
    }
  } else {
    const columns=Array(F.q).fill(1);
    for(let j=0;j<F.q;++j) {
      s.test(columns);++cases;
      for(let z=0;z<F.q;++z)columns[z]=F.mul(columns[z],z);
    }
    for(const seed of [1,2,3,4,5,17,511,65537]){s.test(denseCase(F,seed));++cases;}
  }
  s.negativeControl();
  return {b,eta:s.eta,representatives:s.reps,VSize:s.VSize,storedQuartets:s.quartets,
    bits:b*s.reps*s.VSize,cases,quartetRoundTrips:s.quartets*cases,badStabilizerRejected:true};
}
console.log(JSON.stringify([3,9].map(run),null,2));
