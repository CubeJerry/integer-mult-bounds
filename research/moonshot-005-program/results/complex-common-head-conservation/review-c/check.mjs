// Independent Worker C review controls; no author imports.
function checkTwoSidedIndependently(){
  const p=137,D=3,R=5,n=D*R;
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
    return {F,theta,roles:[a,b],leftRoles:[a,b],kind:"native",expected:2*D};
  }
  function query(dest,source,type){
    const F=eye(n),theta=eye(n);
    const g=type==="Z"?Id.map(row=>row.map(x=>mod(-x))):type==="even"?[[p-1,0,0],[0,p-1,0],[0,0,1]]:[[p-1,0,0],[0,1,0],[0,0,1]];
    block(F,dest,source,g);block(theta,dest,source,g,type==="even"?1:-1);
    return {F,theta,roles:[source],leftRoles:[dest],kind:type==="even"?"even":dest===source?"inplace":"shear",expected:type==="even"?0:D};
  }
  const perms=[[0,1,2],[1,2,0],[2,0,1],[1,0,2],[0,2,1],[2,1,0]];
  const tr=M=>M[0].map((_,j)=>M.map(row=>row[j]));
  const select=(M,roles)=>roles.flatMap(role=>Array.from({length:D},(_,k)=>M[role*D+k]));
  const records=[];let wrongLeftRejected=0,omittedEvenRejected=0;
  for(let seed=0;seed<40;seed++){
    let state=seed+731;const rand=k=>{state=(state*1664525+1013904223)>>>0;return state%k;};
    const protectedCase=seed===0;
    const gates=[
      native(0,1,seed%2?1:-1,(seed>>1)%2?1:-1,(seed>>2)%2?1:-1),
      query(protectedCase?1:3,protectedCase?0:(seed%2?3:2),"even"),
      query(protectedCase?1:4,protectedCase?0:(seed%3?1:4),seed%2?"Z":"rank1")
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
    const M=prefix[gates.length],terms=Array(gates.length),thetaLeft=Array(gates.length),ordinaryLeft=Array(gates.length);let suffix=eye(n),ordinarySuffix=eye(n);
    for(let j=gates.length-1;j>=0;j--){
      thetaLeft[j]=mul(suffix,ordinary[j+1]);ordinaryLeft[j]=mul(ordinarySuffix,ordinary[j+1]);
      terms[j]=mul(mul(thetaLeft[j],sub(gates[j].F,gates[j].theta)),prefix[j]);
      suffix=mul(thetaLeft[j],gates[j].theta);ordinarySuffix=ordinaryLeft[j];
    }
    const thetaM=mul(suffix,ordinary[0]),delta=sub(M,thetaM),total=terms.reduce(add,zero(n));
    need(equal(total,delta),"actual-prefix theta-suffix telescope");
    let U=ordinary[0],rightOrdinary=[],leftOrdinary=[],rightActual=[],leftActual=[],wrongLeftOrdinary=[],wrongLeftActual=[],oddRows=[],oddCols=[],sumRanks=0;
    for(let j=0;j<gates.length;j++){
      const G=gates[j],difference=sub(G.F,G.theta),r=rank(terms[j]);
      need(rank(difference)===G.expected&&r===G.expected,"gate term rank");
      rightOrdinary.push(...select(U,G.roles));
      leftOrdinary.push(...select(tr(ordinaryLeft[j]),G.leftRoles));
      wrongLeftOrdinary.push(...select(tr(ordinaryLeft[j]),G.roles));
      if(G.kind==="even"){
        rightActual.push(...select(prefix[j],G.roles));
        leftActual.push(...select(tr(thetaLeft[j]),G.leftRoles));
        wrongLeftActual.push(...select(tr(thetaLeft[j]),G.roles));
      }else{
        rightActual.push(...terms[j]);leftActual.push(...tr(terms[j]));wrongLeftActual.push(...tr(terms[j]));
        oddRows.push(...terms[j]);oddCols.push(...tr(terms[j]));sumRanks+=r;
      }
      for(const [F,roles]of [[G.F,G.roles],[G.theta,G.roles],[tr(G.F),G.leftRoles],[tr(G.theta),G.leftRoles]]){
        const inactive=Array.from({length:n},(_,i)=>i).filter(i=>!roles.includes(Math.floor(i/D)));
        for(const col of inactive)for(let row=0;row<n;row++)need(F[row][col]===(row===col?1:0),"right/left identity on coordinate kernel");
      }
      U=mul(ordinary[j+1],U);
    }
    need(rowEqual(rightActual,rightOrdinary),"right augmented ordinary-prefix kernel");
    need(rowEqual(leftActual,leftOrdinary),"left augmented ordinary-suffix kernel");
    if(!rowEqual(wrongLeftActual,wrongLeftOrdinary))wrongLeftRejected++;
    if(!rowEqual(oddRows,rightOrdinary))omittedEvenRejected++;
    need(rank(rightActual)-rank(oddRows)<=D&&rank(leftActual)-rank(oddCols)<=D,"one even-query rank allowance");
    need(rank(delta)>=rank(oddRows)+rank(oddCols)-sumRanks,"two-sided Sylvester control");
    records.push({seed,right_odd_codimension:rank(oddRows),left_odd_codimension:rank(oddCols),right_augmented_codimension:rank(rightActual),left_augmented_codimension:rank(leftActual),parity_difference_rank:rank(delta),odd_inner_dimension:sumRanks});
  }
  need(wrongLeftRejected>0&&omittedEvenRejected>0,"active negative controls");
  // An even Gaussian is nonidentity on the full kernel of its zero parity difference.
  const even=eye(n);block(even,0,0,[[p-1,0,0],[0,p-1,0],[0,0,1]]);
  const evenDifference=sub(even,even);
  need(rank(evenDifference)===0&&rank(sub(even,eye(n)))===2,"even-query negative control");
  // An ordinary endpoint permits a common idle subspace: a native and its inverse.
  const F=native(0,1,1,1,1).F;
  const inverseNative=native(0,1,-1,1,-1).F;
  need(equal(mul(inverseNative,F),eye(n)),"ordinary endpoint cancellation");
  need(2*D<n,"ordinary endpoint retains idle kernel");
  return {status:"PASS_INDEPENDENT_TWO_SIDED_KERNEL_REVIEW",prime:p,head_dimension:D,public_roles:R,cases:records,wrong_left_shear_bank_rejections:wrongLeftRejected,omitted_even_query_rejections:omittedEvenRejected,controls:["actual-prefix/theta-suffix telescope","right ordinary-prefix equivalence","left reverse-theta ordinary-suffix equivalence","adjoint native and shear coordinate kernels","even-query rank allowance","Sylvester factor dimension inequality"],qualification:"Finite controls support the elementary identities only. The universal mixed-endpoint projection proof and all-t concavity theorem are independently reviewed in REVIEW.md.",new_kappa:false};
}
export {checkTwoSidedIndependently};
if(typeof process!=="undefined"&&process.argv[1]&&import.meta.url.endsWith(process.argv[1]))console.log(JSON.stringify(checkTwoSidedIndependently(),null,2));
