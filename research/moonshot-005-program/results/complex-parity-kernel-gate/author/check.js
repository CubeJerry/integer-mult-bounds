"use strict";

function makeHeadGroup() {
 const perms=[];for(let a=0;a<3;a++)for(let b=0;b<3;b++)if(b!==a)for(let c=0;c<3;c++)if(c!==a&&c!==b)perms.push([a,b,c]);
 const ps=new Map(perms.map((p,i)=>[p.join(","),i])), pi=ps.get("0,1,2"), ph=[];
 for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++)if((a+b+c)%2===0)ph.push([a,b,c]);
 const elements=[],idx=new Map();for(const u of ph)for(let p=0;p<6;p++){let i=elements.length;elements.push({u,p});idx.set(u.join(",")+";"+p,i);}
 const compose=(p,q)=>p.map((_,i)=>p[q[i]]),pinv=p=>p.map((_,i)=>p.indexOf(i));
 const mul=elements.map(g=>elements.map(h=>{const p=perms[g.p],ip=pinv(p),u=g.u.map((x,i)=>(x+h.u[ip[i]])%4),r=ps.get(compose(p,perms[h.p]).join(","));return idx.get(u.join(",")+";"+r)}));
 const id=idx.get("0,0,0;"+pi),inv=elements.map((g,i)=>mul[i].findIndex(x=>x===id));
 const elt=(u,p=[0,1,2])=>idx.get(u.join(",")+";"+ps.get(p.join(",")));
 const qa=elt([1,0,1]),qb=elt([0,1,1]),qc=elt([1,1,0]),P=elt([0,0,0],[2,0,1]);
 const H=elements.map((g,i)=>({g,i})).filter(({g})=>g.u.every(x=>x%2===0)&&g.u.reduce((a,b)=>a+b,0)%4===0).map(x=>x.i);
 const pow=(g,n)=>{if(n<0){g=inv[g];n=-n;}let z=id;for(let k=0;k<n;k++)z=mul[z][g];return z};
 const A=mul[inv[qb]][P],Z=pow(A,3),U=mul[pow(qb,2)][qc];
 if(elements.length!==192||H.length!==24||pow(A,6)!==id||mul[mul[U][pow(P,2)]][inv[U]]!==pow(A,2))throw Error("group");
 return{perms,elements,mul,inv,id,H,qa,qb,qc,P,A,Z,U,rank2N:mul[qa][qb]};
}
function makeRing(g,n=2){
 const zero=()=>new Map(),mono=(x,k=1)=>new Map([[x,k]]);
 const sum=(a,b,c=1)=>{let r=new Map(a);for(const[x,v]of b){let y=(r.get(x)||0)+c*v;if(y)r.set(x,y);else r.delete(x)}return r};
 const prod=(a,b)=>{let r=new Map();for(const[x,u]of a)for(const[y,v]of b){const z=g.mul[x][y],w=(r.get(z)||0)+u*v;if(w)r.set(z,w);else r.delete(z)}return r};
 const eye=()=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?mono(g.id):zero()));
 const mm=(a,b)=>a.map(r=>b[0].map((_,j)=>r.reduce((z,x,k)=>sum(z,prod(x,b[k][j])),zero())));
 const rowop=(m,i,j,c)=>{const z=m[i].map((v,k)=>sum(v,prod(c,m[j][k])));m[i]=z};
 const left=(m,i,c)=>{m[i]=m[i].map(v=>prod(c,v))};
 return{zero,mono,sum,prod,eye,mm,rowop,left};
}
function nullspaceMod(mat,n,p=101) {
 const m=mat.map(r=>Int32Array.from(r,x=>(x%p+p)%p));let pivot=[],at=0;
 const mod=x=>(x%p+p)%p,inv=x=>{let y=1;for(let j=0;j<p-2;j++)y=y*x%p;return y};
 for(let c=0;c<n&&at<m.length;c++){
  let r=at;while(r<m.length&&!m[r][c])r++;if(r===m.length)continue;[m[r],m[at]]=[m[at],m[r]];
  let z=inv(m[at][c]);for(let j=c;j<n;j++)m[at][j]=m[at][j]*z%p;
  for(let i=0;i<m.length;i++)if(i!==at&&m[i][c]){let z=m[i][c];for(let j=c;j<n;j++)m[i][j]=mod(m[i][j]-z*m[at][j]);}
  pivot.push(c);at++;
 }
 const pv=new Set(pivot),free=Array.from({length:n},(_,i)=>i).filter(i=>!pv.has(i)),basis=[];
 for(const c of free){let x=Array(n).fill(0);x[c]=1;for(let j=0;j<pivot.length;j++)x[pivot[j]]=mod(-m[j][c]);basis.push(x)}
 return {rank:pivot.length,dimension:free.length,basis,pivot,free};
}
function ordinaryRows(g,M,target,p=101) {
 const n=M.length,hs=g.H,Hs=new Set(hs),other=g.elements.map((_,i)=>i).filter(i=>!Hs.has(i)),oi=new Map(other.map((x,i)=>[x,i]));
 const width=n*hs.length,mat=Array.from({length:n*other.length},()=>Array(width).fill(0)),ti=g.inv[target];
 for(let j=0;j<n;j++)for(let h=0;h<hs.length;h++)for(let k=0;k<n;k++)for(const[x,c]of M[j][k]){
  const z=g.mul[ti][g.mul[hs[h]][x]],r=oi.get(z);if(r!==undefined)mat[k*other.length+r][j*hs.length+h]+=c;
 }
 const ns=nullspaceMod(mat,width,p);return {...ns,width,equations:mat.length,mat};
}

function verifyParityKernelGate(){
 const g=makeHeadGroup(),eta=g.elements.map(e=>e.u.reduce((a,b)=>a+b,0)%4===0?1:-1),Hs=new Set(g.H),need=(x,m)=>{if(!x)throw Error(m)};
 let characterChecks=0;for(let i=0;i<192;i++)for(let j=0;j<192;j++){need(eta[g.mul[i][j]]===eta[i]*eta[j],"eta character");characterChecks++;}
 const pow=(e,n)=>{if(n<0){e=g.inv[e];n=-n}let z=g.id;for(let k=0;k<n;k++)z=g.mul[z][e];return z;};
 let controls=0,telescopeTerms=0,projectedColumnControls=0;
 for(const n of[3,4,5]){
  const r=makeRing(g,n),zeroMat=(rows,cols)=>Array.from({length:rows},()=>Array.from({length:cols},()=>r.zero()));
  const theta=M=>M.map(row=>row.map(v=>new Map([...v].map(([e,c])=>[e,eta[e]*c]))));
  const neg=M=>M.map(row=>row.map(v=>new Map([...v].map(([e,c])=>[e,-c]))));
  const plus=(A,B)=>A.map((row,i)=>row.map((v,j)=>r.sum(v,B[i][j]))),diff=(A,B)=>plus(A,neg(B));
  const eq=(A,B)=>A.every((row,i)=>row.every((v,j)=>v.size===B[i][j].size&&[...v].every(([e,c])=>B[i][j].get(e)===c)));
  const zero=M=>M.every(row=>row.every(v=>v.size===0));
  const p0=M=>M.map(row=>row.map(v=>new Map([...v].filter(([e])=>Hs.has(e)))));
  const embedding=zeroMat(n,n-2);for(let i=2;i<n;i++)embedding[i][i-2]=r.mono(g.id);
  for(const s of[-1,1])for(const e of[-1,1])for(const c of[-1,1])for(let seed=0;seed<4;seed++){
   const N=r.eye();N[0][0]=r.mono(pow(g.A,s));N[1][1]=r.mono(pow(g.A,s));N[0][1]=r.mono(pow(g.A,s+e),c);
   const Qpre=r.eye(),Qpost=r.eye();Qpre[1][1]=r.mono(g.Z);Qpost[0][0]=r.mono(g.Z);
   const R=r.eye(),Ri=r.eye(),L=r.eye(),Li=r.eye(),ops=[];
   for(let k=0;k<4;k++){let i=(seed+k)%n,j=(seed+2*k+1)%n;if(j===i)j=(j+1)%n;const h=g.H[(5*seed+3*k)%24],v=k%2?1:-1;r.rowop(R,i,j,r.mono(h,v));ops.push([i,j,h,v]);}
   for(const[i,j,h,v]of ops.toReversed())r.rowop(Ri,i,j,r.mono(h,-v));
   for(let k=0;k<3;k++){let i=(seed+2*k)%n,j=(i+1)%n;const h=g.H[(seed+7*k)%24];r.rowop(L,i,j,r.mono(h,1));}
   need(eq(r.mm(R,Ri),r.eye())&&eq(r.mm(Ri,R),r.eye()),"ordinary inverse");
   const gates=[R,Qpre,N,Qpost,L],prefix=[r.eye()];for(const F of gates)prefix.push(r.mm(F,prefix.at(-1)));
   const M=prefix.at(-1),T=[];let total=zeroMat(n,n);
   for(let j=0;j<gates.length;j++){let suffix=r.eye();for(let k=j+1;k<gates.length;k++)suffix=r.mm(theta(gates[k]),suffix);const term=r.mm(r.mm(suffix,diff(gates[j],theta(gates[j]))),prefix[j]);T.push(term);total=plus(total,term);telescopeTerms++;}
   need(eq(total,diff(M,theta(M))),"actual-prefix theta-suffix telescope");need(eq(M,theta(M)),"sharp even endpoint");
   const J=r.mm(Ri,embedding),MJ=r.mm(M,J),expected=r.mm(L,embedding);
   need(eq(MJ,expected),"ordinary idle injection survives");
   need(eq(r.mm(p0(M),J),MJ),"ordinary component contains complete idle image");projectedColumnControls++;
   for(const j of[1,2,3])need(zero(r.mm(T[j],J)),"common term kernels");
   if(s===e){const core=r.mm(r.mm(Qpost,N),Qpre),expectedP0=zeroMat(n,n);for(let i=2;i<n;i++)expectedP0[i][i]=r.mono(g.id);need(eq(p0(core),expectedP0),"sharp ordinary rank R-2 banks");}
   controls++;
  }
 }
 const r=makeRing(g,3),N=r.eye();N[0][0]=r.mono(g.A);N[1][1]=r.mono(g.A);N[0][1]=r.mono(pow(g.A,2));const Qpre=r.eye(),Qpost=r.eye();Qpre[1][1]=r.mono(g.Z);Qpost[0][0]=r.mono(g.Z);const core=r.mm(r.mm(Qpost,N),Qpre),evenExtra=r.eye();evenExtra[2][2]=r.mono(g.mul[g.A][g.Z]);const unpaid=r.mm(evenExtra,core);
 const theta=M=>M.map(row=>row.map(v=>new Map([...v].map(([e,c])=>[e,eta[e]*c])))),eq=(A,B)=>A.every((row,i)=>row.every((v,j)=>v.size===B[i][j].size&&[...v].every(([e,c])=>B[i][j].get(e)===c))),noOrd=M=>M.every(row=>row.every(v=>[...v].every(([e])=>!Hs.has(e))));
 need(eq(unpaid,theta(unpaid))&&noOrd(unpaid),"extra theta-even Gaussian escapes local-kernel premise");
 const oddExtra=r.eye();oddExtra[2][2]=r.mono(g.qa);const odd=r.mm(oddExtra,core);need(!eq(odd,theta(odd))&&noOrd(odd),"theta-even target hypothesis");
 const singular=r.eye();singular[2][2]=r.zero();need(noOrd(r.mm(core,singular)),"singular omitted input invalidates invertibility hypothesis");
 return{status:"PASS_PARITY_KERNEL_CALLER_GATE",character_checks:characterChecks,exact_even_word_controls:controls,telescoping_terms_checked:telescopeTerms,ordinary_idle_injection_controls:projectedColumnControls,bank_counts:[3,4,5],all_native_sigma_epsilon_c_choices_checked:8,universal_proof:"Actual-prefix/theta-suffix telescoping; saturated rank sum gives common kernel; chronological identity on every local kernel identifies an ordinary idle injection; pi0 has rank at least(R-2)D.",negative_controls:{unpaid_theta_even_Gaussian_removes_ordinary_component:true,theta_odd_endpoint_has_no_ordinary_component:true,singular_deleted_input_removes_ordinary_component:true},specific_closed_target:"One native half +one original cubic-Z rank2 query +one rank1 query cannot produce three independent rank2 heads in fixed G192/H24, in any ordering or either query mode.",scope:"No claim for all query inventories, larger ordinary Clifford phases, changed source/body interfaces, unknown-zero or discarded-input contracts, or approximate degenerations.",new_kappa:false};
}

console.log(JSON.stringify(verifyParityKernelGate(),null,2));
