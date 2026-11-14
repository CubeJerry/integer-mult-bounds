// Root general theorem; independent Worker C matrix controls.
function checkOrdinaryKernelIdentities(){
  const p=137,D=3,R=4,n=D*R;
  const need=(b,s)=>{if(!b)throw Error(s);},mod=x=>((x%p)+p)%p;
  const zero=(r,c=r)=>Array.from({length:r},()=>Array(c).fill(0));
  const eye=r=>{const M=zero(r);for(let i=0;i<r;i++)M[i][i]=1;return M;};
  const add=(A,B)=>A.map((row,i)=>row.map((x,j)=>mod(x+B[i][j])));
  const sub=(A,B)=>A.map((row,i)=>row.map((x,j)=>mod(x-B[i][j])));
  const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((v,x,k)=>mod(v+x*B[k][j]),0)));
  const equal=(A,B)=>JSON.stringify(A)===JSON.stringify(B);
  const powmod=(x,k)=>{let v=1;for(;k;k=Math.floor(k/2),x=x*x%p)if(k%2)v=v*x%p;return v;};
  const rank=M=>{
    if(!M.length)return 0;M=M.map(row=>row.map(mod));let r=0;
    for(let j=0;j<M[0].length&&r<M.length;j++){
      let i=r;while(i<M.length&&!M[i][j])i++;if(i===M.length)continue;
      [M[i],M[r]]=[M[r],M[i]];const q=powmod(M[r][j],p-2);
      for(let k=j;k<M[r].length;k++)M[r][k]=M[r][k]*q%p;
      for(let a=r+1;a<M.length;a++)if(M[a][j]){const q=M[a][j];for(let k=j;k<M[a].length;k++)M[a][k]=mod(M[a][k]-q*M[r][k]);}r++;
    }return r;
  };
  const rowEqual=(A,B)=>rank(A)===rank(B)&&rank([...A,...B])===rank(A);
  const block=(M,r,c,B,scale=1)=>{for(let i=0;i<D;i++)for(let j=0;j<D;j++)M[r*D+i][c*D+j]=mod(scale*B[i][j]);};
  const A=[[0,0,p-1],[1,0,0],[0,1,0]],Id=eye(D);
  const powers=[Id];for(let j=1;j<=6;j++)powers.push(mul(powers[j-1],A));
  need(equal(powers[6],Id)&&equal(powers[3],Id.map(row=>row.map(x=>mod(-x)))),"order-six head");
  function native(a,b,sigma,epsilon,c){
    const F=eye(n),theta=eye(n),B=powers[(sigma+6)%6],C=powers[(sigma+epsilon+6)%6];
    block(F,a,a,B);block(F,b,b,B);block(F,a,b,C,c);
    block(theta,a,a,B,-1);block(theta,b,b,B,-1);block(theta,a,b,C,c);
    return {F,theta,roles:[a,b],kind:"native",expected:2*D};
  }
  function query(dest,source,type){
    const F=eye(n),theta=eye(n),g=type==="Z"?Id.map(row=>row.map(x=>mod(-x))):[[p-1,0,0],[0,1,0],[0,0,1]];
    if(dest===source){block(F,dest,source,g);block(theta,dest,source,g,-1);}
    else{block(F,dest,source,g);block(theta,dest,source,g,-1);}
    return {F,theta,roles:[source],kind:dest===source?"inplace":"shear",expected:D};
  }
  const perms=[[0,1,2],[1,2,0],[2,0,1],[1,0,2],[0,2,1],[2,1,0]];
  const records=[];
  for(let seed=0;seed<40;seed++){
    let state=seed+731;const rand=k=>{state=(state*1664525+1013904223)>>>0;return state%k;};
    const protectedCase=seed===0;
    const gates=[
      native(0,1,seed%2?1:-1,(seed>>1)%2?1:-1,(seed>>2)%2?1:-1),
      query(protectedCase?0:2,protectedCase?0:2,"Z"),
      query(1,protectedCase?0:3,"rank1"),
      native(1,protectedCase?0:2,(seed>>3)%2?1:-1,(seed>>4)%2?1:-1,1)
    ];
    const ordinary=Array.from({length:gates.length+1},()=>{
      let O=eye(n);
      for(let t=0;t<4;t++){
        const lim=protectedCase?2:R,a=rand(lim),b=(a+1+rand(lim-1))%lim,pi=perms[rand(6)],H=zero(D);
        for(let k=0;k<D;k++)H[pi[k]][k]=1;
        const E=eye(n);block(E,a,b,H,rand(2)?1:-1);O=mul(E,O);
      }return O;
    });
    const prefix=[ordinary[0]];
    for(let j=0;j<gates.length;j++)prefix.push(mul(mul(ordinary[j+1],gates[j].F),prefix[j]));
    const M=prefix[gates.length],terms=Array(gates.length);let suffix=eye(n);
    for(let j=gates.length-1;j>=0;j--){
      terms[j]=mul(mul(mul(suffix,ordinary[j+1]),sub(gates[j].F,gates[j].theta)),prefix[j]);
      suffix=mul(mul(suffix,ordinary[j+1]),gates[j].theta);
    }
    const thetaM=mul(suffix,ordinary[0]),delta=sub(M,thetaM),total=terms.reduce(add,zero(n));
    need(equal(total,delta),"actual-prefix theta-suffix telescope");
    let U=ordinary[0],constraints=[];
    for(let j=0;j<gates.length;j++){
      for(const role of gates[j].roles)for(let k=0;k<D;k++)constraints.push(U[role*D+k]);
      const difference=sub(gates[j].F,gates[j].theta);
      need(rank(difference)===gates[j].expected&&rank(terms[j])===gates[j].expected,"gate term rank");
      const inactive=Array.from({length:n},(_,i)=>i).filter(i=>!gates[j].roles.includes(Math.floor(i/D)));
      for(const G of [gates[j].F,gates[j].theta])for(const col of inactive)for(let row=0;row<n;row++)need(G[row][col]===(row===col?1:0),"identity on coordinate kernel");
      U=mul(ordinary[j+1],U);
    }
    const stacked=terms.flat(),replaced=[...delta,...terms.slice(1).flat()];
    need(rowEqual(stacked,constraints),"ordinary-prefix kernel equality");
    need(rowEqual(stacked,replaced),"deleted-native kernel equality");
    const codim=rank(stacked),kernel=n-codim;
    if(protectedCase)need(kernel>=2*D,"nonzero protected ordinary kernel control");
    records.push({seed,term_ranks:terms.map(rank),kernel_dimension:kernel,endpoint_parity_difference_rank:rank(delta)});
  }
  // An even Gaussian is nonidentity on the full kernel of its zero parity difference.
  const even=eye(n);block(even,0,0,[[p-1,0,0],[0,p-1,0],[0,0,1]]);
  const evenDifference=sub(even,even);
  need(rank(evenDifference)===0&&rank(sub(even,eye(n)))===2,"even-query negative control");
  // An ordinary endpoint permits a common idle subspace: a native and its inverse.
  const F=native(0,1,1,1,1).F;
  const inverseNative=native(0,1,-1,1,-1).F;
  need(equal(mul(inverseNative,F),eye(n)),"ordinary endpoint cancellation");
  need(2*D<n,"ordinary endpoint retains idle kernel");
  return {status:"PASS_ORDINARY_KERNEL_TELESCOPE",prime:p,head_dimension:D,public_roles:R,cases:records,checks:["actual prefixes and theta suffixes","noncommuting ordinary role/head permutation shears","coordinate identity-on-kernel","ordinary-prefix constraint rowspace equality","deleted-native replacement rowspace equality"],negative_controls:{theta_even_nonidentity_query_rejected:true,ordinary_endpoint_does_not_force_zero_kernel:true},qualification:"Finite exact matrix controls authenticate the elementary telescope/kernel lemmas. The universal complex star-algebra projection and pure-E2 contradiction are proved in PROOF.md, not inferred from these finite tests.",new_kappa:false};
}
export {checkOrdinaryKernelIdentities};
if(typeof process!=="undefined"&&process.argv[1]&&import.meta.url.endsWith(process.argv[1])) console.log(JSON.stringify(checkOrdinaryKernelIdentities(),null,2));
