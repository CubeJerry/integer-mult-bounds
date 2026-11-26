// Independent finite scalar and actual predictor/repair controls for modular Walsh lifting.
// Run with: node verify-modular-walsh-review.js
// BigInt operations and dense Lagrange inverses are finite proof controls.
function exactControls() {
  function mod(x,m) { return (x % m + m) % m; }
  function inv(x,m) {
    let a=m,b=mod(x,m),u=0n,v=1n;
    while(b) {
      const h=a/b; [a,b]=[b,a-h*b]; [u,v]=[v,u-h*v];
    }
    if(a!==1n) throw Error("nonunit");
    return mod(u,m);
  }
  function divide(z,b,M) {
    if(b===1n) return z;
    const r=mod(-mod(z,b)*inv(mod(M,b),b),b), n=z+r*M;
    if(n%b) throw Error("division remainder");
    const x=n/b;
    if(x<0n||x>=M||mod(b*x,M)!==z) throw Error("division");
    return x;
  }
  function parity(x) {
    let p=0;while(x){p^=1;x&=x-1;}return p;
  }
  function spec(m,c) {
    const radius=Math.ceil(2*Math.sqrt(m)), u=Math.floor(m/2-radius);
    const d=Math.ceil(m/2+radius)-u;
    let bin=1n, step=1n, p=1n;
    for(let j=1;j<=d;j++) {
      bin=bin*BigInt(c-u-j+1)/BigInt(j); step*=-2n; p+=bin*step;
    }
    return {u,d,p};
  }
  function sign(x) { return (x&1)?-1n:1n; }
  function abs(x) { return x<0n?-x:x; }
  function one(m,mode) {
    const W=2**Math.ceil(Math.log2(m+1)), {u,d}=spec(m,0);
    const vals=Array.from({length:m+1},(_,c)=>spec(m,c).p);
    const gaps=new Set();
    for(const v of vals)for(const a of [-1n,1n])for(const z of [-1n,1n]) {
      if(a*v!==z)gaps.add(abs(a*v-z));
    }
    let U=2n;
    for(let i=2;i<=W+d;i++) U*=BigInt(i);
    for(const g of gaps) U*=g;
    const M=1n+(U<<80n);
    const input=Array.from({length:m},(_,i)=>mode===0?0:
      mode===1?Number((i+1)%2===1&&(i+1)<=(m+1)/2):parity((i+1)&3));
    const z=sign(input.reduce((a,b)=>a+b,0));
    const pred=Array.from({length:W},(_,t)=>{
      const beta=input.map((_,j)=>parity((j+1)&t));
      return sign(u-beta.reduce((a,b)=>a+b,0))*vals[input.reduce((s,v,j)=>s+(v^beta[j]),0)];
    });
    const J=Array.from({length:W},(_,i)=>i).filter(i=>pred[i]!==z);
    if(J.length>W/16) throw Error("Chebyshev");
    if(!J.length) return {m,mode,j:0,modulusBits:M.toString(2).length,checks:0};
    const nodes=Array.from({length:W},(_,i)=>divide(BigInt(i),BigInt(W),M));
    const X=nodes.map((_,i)=>mod(BigInt((i+1)*(i+2)*1234567-634535),M));
    const powers=nodes.map(x=>{
      let p=1n;return J.map(()=>{const old=p;p=mod(p*x,M);return old;});
    });
    const Vinv=J.map(i=>{
      let coeff=[1n],scale=1n;
      for(const j of J)if(i!==j) {
        const next=Array(coeff.length+1).fill(0n);
        coeff.forEach((v,h)=>{next[h]=mod(next[h]-v*nodes[j],M);next[h+1]=mod(next[h+1]+v,M);});
        coeff=next; scale=mod(scale*(nodes[i]-nodes[j]),M);
      }
      return coeff.map(v=>mod(v*inv(scale,M),M));
    });
    const He=J.map((_,h)=>X.reduce((acc,x,i)=>mod(acc+powers[i][h]*(pred[i]-z)*x,M),0n));
    const recovered=J.map((i,t)=>{
      const e=Vinv[t].reduce((a,v,h)=>mod(a+v*He[h],M),0n), g=pred[i]-z;
      return mod((g<0n?-1n:1n)*divide(e,abs(g),M),M);
    });
    const a=J.map((_,h)=>recovered.reduce((s,x,t)=>mod(s+x*Vinv[t][h],M),0n));
    for(let i=0;i<W;i++){
      const Z=powers[i].reduce((s,p,h)=>mod(s+p*a[h],M),0n);
      if(mod(pred[i]*X[i]-pred[i]*Z+z*Z,M)!==mod(z*X[i],M))throw Error("failed correction");
    }
    return {m,mode,j:J.length,modulusBits:M.toString(2).length,checks:W};
  }
  let divides=0;
  for(const M of [9n,25n,35n,221n])for(let b=1n;b<=70n;b++){
    let ok=true;try{if(b!==1n)inv(b,M);}catch{ok=false;}
    if(!ok)continue;
    for(let z=0n;z<M;z++){divide(z,b,M);++divides;}
  }
  const adverse=-spec(63,0).p-1n;
  if(adverse%73n!==0n||adverse!==-4510048854467219030016n)throw Error("gap control");
  let rejected=false;try{divide(1n,-adverse,73n**5n);}catch{rejected=true;}
  if(!rejected)throw Error("invalid gap accepted");
  return {divisionCases:divides,repairs:[31,63,127].flatMap(m=>[0,1,2].map(mode=>one(m,mode))),adverseGap:adverse.toString(),rejected};
}

console.log(JSON.stringify(exactControls(),null,2));
