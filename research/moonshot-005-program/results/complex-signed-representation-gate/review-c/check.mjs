// Independent Worker C reconstruction. No author checker imports.
function checkSignedIndependently() {
  const fail = s => { throw new Error(s); }, need = (b,s) => { if(!b) fail(s); };
  const perms = [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
  const elements=[];
  for(let a=0;a<4;a++) for(let b=0;b<4;b++) for(let c=0;c<4;c++)
    if((a+b+c)%2===0) for(const p of perms) elements.push({u:[a,b,c],p});
  const key = g => g.u.join("")+"|"+g.p.join("");
  const lookup = new Map(elements.map((g,i)=>[key(g),i]));
  const compose = (g,h) => ({u:g.u.map((x,j)=>(x+h.u[g.p.indexOf(j)])%4),p:h.p.map(j=>g.p[j])});
  const mult = elements.map(g=>elements.map(h=>lookup.get(key(compose(g,h)))));
  const id=lookup.get("000|012"), inverse=mult.map(row=>row.indexOf(id));
  const find=(u,p=[0,1,2])=>lookup.get(key({u,p}));
  const qa=find([1,0,1]),qb=find([0,1,1]),qc=find([1,1,0]);
  const q=[qa,qb,qc], T=[id,...q.map(g=>mult[g][g])];
  const cosetReps=Array.from({length:8},(_,x)=>q.reduce((g,v,k)=>(x>>k)&1?mult[g][v]:g,id));
  const signs=elements.map(g=>{
    const phase=find(g.u);
    const matches=cosetReps.map((v,x)=>T.some(t=>mult[t][v]===phase)?x:-1).filter(x=>x>=0);
    need(matches.length===1,"unique sign coset"); return matches[0];
  });
  for(let g=0;g<192;g++){
    const [a,b,c]=elements[g].u,e=((a+b+c)/2)%2;
    const formula=((e+b)%2)+2*((e+a)%2)+4*((e+a+b)%2);
    need(formula===signs[g],"published sign formula matches independently reconstructed coset");
  }
  const action=perms.map(p=>q.map(g=>{
    const pg=find([0,0,0],p), conjugate=mult[mult[pg][g]][inverse[pg]];
    const x=signs[conjugate]; need([1,2,4].includes(x),"generator permutation");
    return Math.log2(x);
  }));
  const zero=n=>Array.from({length:n},()=>Array(n).fill(0));
  const product=(a,b)=>a.map(row=>b[0].map((_,j)=>row.reduce((v,x,k)=>v+x*b[k][j],0)));
  const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const rho=(g,signed)=>{
    const M=zero(3), tau=action[perms.findIndex(p=>p.join("")===elements[g].p.join(""))];
    for(let k=0;k<3;k++)M[tau[k]][k]=signed&&((signs[g]>>tau[k])&1)?-1:1;
    return M;
  };
  const R0=elements.map((_,g)=>rho(g,false)),R1=elements.map((_,g)=>rho(g,true));
  let hom=0;
  for(let g=0;g<192;g++)for(let h=0;h<192;h++){
    need(equal(product(R0[g],R0[h]),R0[mult[g][h]]),"rho0 homomorphism");
    need(equal(product(R1[g],R1[h]),R1[mult[g][h]]),"rho1 homomorphism");hom+=2;
  }
  const H=elements.map((_,g)=>g).filter(g=>signs[g]===0);
  need(H.length===24&&H.every(g=>equal(R0[g],R1[g])),"ordinary agreement");
  // Compute Gaussian rank from actual one-column Fourier-conjugated matrices.
  const W=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]];
  const ipow=[[1,0],[0,1],[-1,0],[0,-1]];
  const physical=elements.map(g=>{
    const p=[0,...g.p.map(x=>x+1)],ph=[[1,0],...g.u.map(x=>ipow[x])],M=[];
    for(let i=0;i<4;i++){M[i]=[];for(let j=0;j<4;j++){
      let re=0,im=0;for(let k=0;k<4;k++){const c=W[i][p[k]]*W[k][j];re+=c*ph[p[k]][0];im+=c*ph[p[k]][1];}
      M[i][j]=[re,im];
    }}
    const counts=Array.from({length:4},(_,j)=>M.reduce((n,row)=>n+(row[j][0]!==0||row[j][1]!==0),0));
    need(counts.every(x=>x===counts[0])&&[1,2,4].includes(counts[0]),"Gaussian support");
    return Math.log2(counts[0]);
  });
  const wt=x=>x.toString(2).split("").filter(x=>x==="1").length,census={};
  for(let g=0;g<192;g++){const k=physical[g]+","+wt(signs[g]);census[k]=(census[k]||0)+1;}
  need(equal(census,{"0,0":24,"2,3":24,"1,1":72,"2,2":72}),"rank census");
  const A=mult[inverse[qb]][find([0,0,0],[2,0,1])];
  const power=(g,n)=>{let h=id;if(n<0){g=inverse[g];n=-n;}for(let k=0;k<n;k++)h=mult[h][g];return h;};
  need(power(A,6)===id&&wt(signs[A])===1&&wt(signs[power(A,3)])===3,"cubic head");
  const mod=(x,p)=>((x%p)+p)%p;
  const powmod=(x,n,p)=>{let v=1;for(;n;n=Math.floor(n/2),x=x*x%p)if(n%2)v=v*x%p;return v;};
  const rankdet=(M,p)=>{
    M=M.map(row=>row.map(x=>mod(x,p)));let rank=0,det=1;
    for(let j=0;j<M[0].length&&rank<M.length;j++){
      let r=rank;while(r<M.length&&!M[r][j])r++;if(r===M.length)continue;
      if(r!==rank){[M[r],M[rank]]=[M[rank],M[r]];det=mod(-det,p);}
      const pivot=M[rank][j];det=det*pivot%p;const iv=powmod(pivot,p-2,p);
      for(let k=j;k<M[rank].length;k++)M[rank][k]=M[rank][k]*iv%p;
      for(let i=rank+1;i<M.length;i++)if(M[i][j]){const c=M[i][j];for(let k=j;k<M[i].length;k++)M[i][k]=mod(M[i][k]-c*M[rank][k],p);}
      rank++;
    } return {rank,det:rank===M.length?det:0};
  };
  const native=[];
  for(const sigma of [-1,1])for(const epsilon of [-1,1])for(const c of [-1,1]){
    const b0=R0[power(A,sigma)],b1=R1[power(A,sigma)],X=b1.map((row,i)=>row.map((x,j)=>x-b0[i][j]));
    const off0=R0[power(A,sigma+epsilon)],off1=R1[power(A,sigma+epsilon)];
    const M=zero(6);for(let i=0;i<3;i++)for(let j=0;j<3;j++){M[i][j]=M[i+3][j+3]=X[i][j];M[i][j+3]=c*(off1[i][j]-off0[i][j]);}
    const L=zero(6),R=zero(6);for(let i=0;i<6;i++)L[i][i]=R[i][i]=1;
    if(epsilon===sigma)for(let i=0;i<3;i++)for(let j=0;j<3;j++){L[i][j+3]=-c*b0[i][j];R[i][j+3]=-c*b1[i][j];}
    const reduced=product(product(L,M),R);
    const target=zero(6);for(let i=0;i<3;i++)for(let j=0;j<3;j++)target[i][j]=target[i+3][j+3]=X[i][j];
    need(equal(reduced,target),"native exact elimination");
    need(rankdet(M,137).rank===2,"native rank lower witness");
    native.push({sigma,epsilon,c,rank:2});
  }
  // Different prime from both author and root tensor witnesses.
  const prime=137,imag=37;need(imag*imag%prime===prime-1,"Gaussian prime");
  const trace=elements.map(g=>{
    let v=1;for(let k=0;k<3;k++)if(g.p[k]===k)v+=powmod(imag,g.u[k],prime);return mod(v,prime);
  });
  const Gram=mult.map((_,g)=>elements.map((_,h)=>powmod(trace[mult[inverse[g]][h]],6,prime)));
  const gram=rankdet(Gram,prime);need(gram.rank===192,"V6 tensor independence");
  // Exact floor brackets for the optimistic changed-query invoice.
  const scale=10n**25n;
  function bracket(r){const rhs=BigInt(r)**199n*scale**200n;let lo=0n,hi=BigInt(r)*scale+1n;
    while(hi-lo>1n){const mid=(lo+hi)/2n;if(mid**200n<=rhs)lo=mid;else hi=mid;}return [lo,hi];}
  const b2=bracket(2),b7=bracket(7),b8=bracket(8),b9=bracket(9);
  const lower=3n*b9[0]-2n*scale-2n*b7[1]-b8[1]-b2[1];
  const upper=3n*b9[1]-2n*scale-2n*b7[0]-b8[0]-b2[0];
  need(lower>0n,"strict optimistic invoice");
  return {status:"PASS_INDEPENDENT_SIGNED_CALLER_REVIEW",group:192,ordinary:24,coset_reconstruction:"Eight products of Qa,Qb,Qc modulo actual four translations; no author sign formula imported",homomorphism_checks:hom,rank_census_from_Fourier_support:census,native_cases:native,tensor_independence:{width:6,prime,imaginary:imag,...gram},raw_invoice:{scale:scale.toString(),margin:[lower.toString(),upper.toString()]},scope:"Fixed collective G192/H24; all V>=6 by tensor independence. No caller and no new kappa."};
}
function checkLambdaIndependently(){
  const need=(b,s)=>{if(!b)throw Error(s);};
  const norm=([a,b,d])=>{if(a===0&&b===0)return [0,0,0];while(d&&a%2===0&&b%2===0){a/=2;b/=2;d--;}return [a,b,d];};
  const add=(a,b)=>{const d=Math.max(a[2],b[2]);return norm([a[0]*2**(d-a[2])+b[0]*2**(d-b[2]),a[1]*2**(d-a[2])+b[1]*2**(d-b[2]),d]);};
  const neg=a=>[-a[0],-a[1],a[2]];
  const mul=(a,b)=>norm([a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0],a[2]+b[2]]);
  const one=[1,0,0],alpha=[1,1,1],beta=[1,-1,1];
  const mono=(u,c=one)=>new Map([[u.join(""),c]]);
  const sum=(A,B)=>{const C=new Map(A);for(const [u,c]of B){const n=add(C.get(u)||[0,0,0],c);if(n[0]||n[1])C.set(u,n);else C.delete(u);}return C;};
  const scale=(A,c)=>new Map([...A].map(([u,x])=>[u,mul(c,x)]).filter(([,x])=>x[0]||x[1]));
  const prod=(A,B)=>{let C=new Map();for(const [u,c]of A)for(const [v,d]of B){const w=[0,1,2].map(i=>(Number(u[i])+Number(v[i]))%4);C=sum(C,mono(w,mul(c,d)));}return C;};
  const equal=(A,B)=>{const C=sum(A,scale(B,[-1,0,0]));return C.size===0;};
  const I=mono([0,0,0]),Qa=mono([1,0,1]),Qb=mono([0,1,1]),Qai=mono([3,0,3]),Qbi=mono([0,3,3]);
  const Ta=prod(Qa,Qa),Tb=prod(Qb,Qb);
  const la=sum(scale(I,alpha),scale(Ta,beta)),lb=sum(scale(I,alpha),scale(Tb,beta));
  const lai=sum(scale(I,beta),scale(Ta,alpha)),lbi=sum(scale(I,beta),scale(Tb,alpha));
  const Sa=prod(la,Qai),Sb=prod(lb,Qbi);
  for(const [l,li,T,S,Q]of [[la,lai,Ta,Sa,Qa],[lb,lbi,Tb,Sb,Qb]]){
    need(equal(prod(l,l),T),"lambda square translation");
    need(equal(prod(l,li),I),"lambda inverse");
    need(equal(prod(S,S),I),"normalized involution");
    need(equal(prod(l,S),Q),"Q=lambda*S");
  }
  const original=Array.from({length:4},()=>Array.from({length:4},()=>new Map()));
  original[0][0]=Qb;original[1][0]=I;original[1][1]=Qa;original[2][2]=Qb;original[2][3]=scale(prod(Qa,Qb),[-1,0,0]);original[3][3]=Qa;
  const pre=[la,I,la,I],post=[prod(lai,lbi),lai,prod(lai,lbi),lai];
  const actual=original.map((row,i)=>row.map((a,j)=>prod(prod(post[i],a),pre[j])));
  const expected=Array.from({length:4},()=>Array.from({length:4},()=>new Map()));
  expected[0][0]=Sb;expected[1][0]=I;expected[1][1]=Sa;expected[2][2]=Sb;expected[2][3]=scale(prod(Sa,Sb),[-1,0,0]);expected[3][3]=Sa;
  for(let i=0;i<4;i++)for(let j=0;j<4;j++)need(equal(actual[i][j],expected[i][j]),"literal independent source column");
  // Exact five in-place operations on two arbitrary scalar inputs.
  let u=[one,[0,0,0]],v=[[0,0,0],one];
  const plus=(a,b)=>a.map((x,i)=>add(x,b[i]));
  const times=(a,c)=>a.map(x=>mul(x,c));
  u=plus(u,times(v,[-1,0,0]));u=times(u,beta);v=plus(v,u);u=times(u,[-1,1,0]);u=plus(u,v);
  need(JSON.stringify([u,v])===JSON.stringify([[alpha,beta],[beta,alpha]]),"five-operation butterfly");
  // A forbidden one-column expansion does fail after tensor lifting.
  const tensorEigenvalue=mul([0,1,0],[0,1,0]),falseCollective=add(alpha,beta);
  need(JSON.stringify(tensorEigenvalue)!==JSON.stringify(falseCollective),"collective versus tensor-power negative control");
  return {status:"PASS_INDEPENDENT_LAMBDA_SOURCE_REVIEW",algebra:"Exact Gaussian-dyadic coefficients in the abstract commuting phase group; collective identities hold at every tensor width",literal_source_entries_checked:16,arbitrary_inputs:4,lambda_identities_checked:8,butterfly_operations:5,ordinary_services:{full_source:8,per_half:4,per_pair_add:3,per_pair_scale:2,helper_storage:0},scope:"No new Gaussian MOVE; layout and finite precision/scalar costs remain paid. This is not a caller."};
}
export { checkSignedIndependently, checkLambdaIndependently };
if (typeof process!=="undefined" && process.argv[1] && import.meta.url.endsWith(process.argv[1])) console.log(JSON.stringify({signed:checkSignedIndependently(),lambda:checkLambdaIndependently()},null,2));
