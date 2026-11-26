// Finite support, rank and semilinear transport controls for C001-CRT4.
// Run with: node verify-four-point.js
// The small dense matrix operations below are test oracles.
function proofControls() {
  // Binary polynomials for irreducible fields F_(2^b).
  const moduli = {3:0xb, 4:0x13, 5:0x25, 7:0x83, 11:0x805};
  function field(b) {
    const q=2**b, modulus=moduli[b];
    function mul(a,d) {
      let v=0;
      while(d) { if(d&1)v^=a; d>>>=1; a<<=1; if(a&q)a^=modulus; }
      return v;
    }
    function pow(a,e) {
      let v=1;
      while(e) { if(e&1)v=mul(v,a); e>>>=1; a=mul(a,a); }
      return v;
    }
    const sq = Array.from({length:q},(_,i)=>mul(i,i));
    // A cyclic multiplicative group: injectivity and roots of all field elements.
    if(new Set(sq).size!==q || Array.from({length:q-1},(_,i)=>pow(i+1,q-1)).some(x=>x!==1))throw Error("invalid modulus");
    return {b,q,mul,pow,sq};
  }
  const key = x => [...x].sort((a,b)=>a-b).join(",");
  const squareSet=(x,F)=>x.map(a=>F.sq[a]);
  function partition(U,F) {
    const seen=new Set(), out=[];
    for(let a=0;a<F.q;a++)if(!seen.has(a)) {
      const A=U.map(u=>a^u); A.forEach(z=>seen.add(z)); out.push(A);
    }
    return out;
  }
  function localTopRow(A,F) {
    return A.map(a=>F.pow(A.filter(z=>z!==a).reduce((s,z)=>F.mul(s,a^z),1),F.q-2));
  }
  function rank(vectors,b) {
    const basis=Array(b).fill(0);
    for(let v of vectors)for(let k=b-1;v&&k>=0;k--) {
      if(!(v&(1<<k)))continue;
      if(basis[k])v^=basis[k];else{basis[k]=v;break;}
    }
    return basis.filter(x=>x!==0).length;
  }
  function examine(b) {
    const F=field(b), U=[0,1,2,3], groups=partition(U,F);
    const cosets=new Set(groups.map(key));
    let good=0, fullRank=0, nontrivialProjectiveTopImages=0;
    for(const A of groups) {
      let cur=[...A], orbitSet=new Set(cur), clean=true;
      for(let j=1;j<b;j++) {
        cur=squareSet(cur,F);
        if(cosets.has(key(cur)))nontrivialProjectiveTopImages++;
        if(cur.some(z=>orbitSet.has(z)))clean=false;
        cur.forEach(z=>orbitSet.add(z));
      }
      if(clean)good++;
      const weights=localTopRow(A,F);
      const powers=A.map(()=>1), cols=[];
      // F2-rank of the actual leading coefficient as a map on binary
      // monomial inputs. Once it is full, remaining columns cannot increase it.
      for(let j=0;j<F.q;j++) {
        cols.push(powers.reduce((s,x,i)=>s^F.mul(x,weights[i]),0));
        powers.forEach((x,i)=>{powers[i]=F.mul(x,A[i]);});
        if(j%16===15 && rank(cols,b)===b)break;
      }
      const topRank=rank(cols,b); if(topRank===b)fullRank++;
      if(clean&&topRank!==b)throw Error("rank contradicts good-coset proof");
    }
    if(nontrivialProjectiveTopImages!==0) throw Error("unexpected stable four-point coset");
    if(good<groups.length-8*(b-1))throw Error("exception bound");
    return {b,cosets:groups.length,good,fullRank,nontrivialProjectiveTopImages};
  }
  function testMatrix(b,U,expectMonomial,graded=false) {
    const F=field(b), n=F.q, m=U.length, groups=partition(U,F), cm=[];
    for(const A of groups) {
      let modulus=[1];
      for(const a of A) {
        const v=Array(modulus.length+1).fill(0);
        modulus.forEach((c,i)=>{v[i]^=F.mul(c,a); v[i+1]^=c;}); modulus=v;
      }
      const rows=Array.from({length:m},()=>[]), p=Array(m).fill(0); p[0]=1;
      for(let j=0;j<n;j++) {
        const c=graded ? [p[0],p[1]^p[2]^p[3],p[2]^p[3],p[3]] : p;
        c.forEach((v,i)=>rows[i].push(v));
        const z=p[m-1]; for(let i=m-1;i>=0;i--)p[i]=(i?p[i-1]:0)^F.mul(z,modulus[i]);
      }
      cm.push(...rows);
    }
    // Unique semilinear matrix from M C^(2) = C using elementary linear solves.
    const augmented=Array.from({length:n},(_,j)=>[...cm.map(row=>F.sq[row[j]]),...cm.map(row=>row[j])]);
    for(let k=0;k<n;k++) {
      const h=augmented.findIndex((r,i)=>i>=k&&r[k]); if(h<0)throw Error("singular");
      [augmented[k],augmented[h]]=[augmented[h],augmented[k]];
      const u=F.pow(augmented[k][k],n-2);
      for(let j=k;j<2*n;j++)augmented[k][j]=F.mul(augmented[k][j],u);
      for(let i=0;i<n;i++)if(i!==k&&augmented[i][k]) {
        const c=augmented[i][k]; for(let j=k;j<2*n;j++)augmented[i][j]^=F.mul(c,augmented[k][j]);
      }
    }
    const counts=Array.from({length:n},(_,j)=>augmented.reduce((s,r)=>s+Number(r[n+j]!==0),0));
    const mono=counts.every(x=>x===1); if(mono!==expectMonomial)throw Error("monomial comparator failed");
    return {b,U,graded,monomial:mono,nonzerosPerRow:[...new Set(counts)].sort((a,b)=>a-b),nonmonomialRows:counts.filter(x=>x>1).length};
  }
  const U3=Array.from({length:8},(_,i)=>i).filter(a=>{const f=field(3);return (a^f.sq[a]^f.sq[f.sq[a]])===0;});
  return {
    prime: [5,7,11].map(examine),
    matrices:[testMatrix(5,[0,1],true),testMatrix(5,[0,1,2,3],false),testMatrix(5,[0,1,2,3],false,true),testMatrix(3,U3,true)]
  };
}

console.log(JSON.stringify(proofControls(),null,2));
