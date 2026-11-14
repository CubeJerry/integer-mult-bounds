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

function verifyTwoHalfGate(){
 const g=makeHeadGroup(),r=makeRing(g,3),need=(x,m)=>{if(!x)throw Error(m)};
 const rank=e=>{const u=g.elements[e].u,a=u[0]%2,d=u[1]%2,b=((u[2]-u[0]-u[1])/2%2+2)%2;return!a&&!b&&!d?0:(a*d-b*b)%2?2:1;};
 const pow=(e,n)=>{if(n<0){e=g.inv[e];n=-n}let z=g.id;for(let k=0;k<n;k++)z=g.mul[z][e];return z;};
 const eqentry=(a,b)=>a.size===b.size&&[...a].every(([e,v])=>b.get(e)===v);
 const eq=(a,b)=>a.every((row,i)=>row.every((v,j)=>eqentry(v,b[i][j])));
 const project=(M,k)=>M.map(row=>row.map(v=>new Map([...v].filter(([e])=>rank(e)===k))));
 const native=(s,e,c=1)=>{let N=r.eye();N[0][0]=r.mono(pow(g.A,s));N[1][1]=r.mono(pow(g.A,s));N[0][1]=r.mono(pow(g.A,s+e),c);return N;};
 const choices=[];for(const s of[-1,1])for(const e of[-1,1])choices.push([s,e]);
 let cases=0,fullColumnWitness=0,fullRowWitness=0;
 for(let k=0;k<8;k++){
  const L=r.eye(),Li=r.eye(),R=r.eye(),Ri=r.eye(),h=g.H[3*k%24],j=g.H[(5*k+1)%24];
  L[1][0]=r.mono(h,2);Li[1][0]=r.mono(h,-2);R[0][1]=r.mono(j,-3);Ri[0][1]=r.mono(j,3);
  const S=r.eye();S[0][0]=r.zero();S[2][2]=r.zero();S[0][2]=r.mono(g.id);S[2][0]=r.mono(g.id);
  const C=r.mm(r.mm(L,S),R),Ci=r.mm(r.mm(Ri,S),Li);need(eq(r.mm(C,Ci),r.eye())&&eq(r.mm(Ci,C),r.eye()),"ordinary C inverse");
  need(C[2][2].size===0,"zero idle-idle C");
  for(const x of choices)for(const y of choices){
   const N1=native(...x),N2=native(...y),M=r.mm(r.mm(N2,C),N1),P1=project(M,1);
   const X=[r.prod(r.mono(pow(g.A,y[0])),C[0][2]),r.prod(r.mono(pow(g.A,y[0])),C[1][2])];
   const Y=[r.prod(C[2][0],r.mono(pow(g.A,x[0]))),r.prod(C[2][1],r.mono(pow(g.A,x[0])))];
   for(let a=0;a<2;a++){need(eqentry(P1[a][2],X[a]),"exact rank1 cross column");need(eqentry(P1[2][a],Y[a]),"exact rank1 cross row");}
   need(P1[2][2].size===0,"rank1 zero corner");
   // C_active,idle=(I,2h)^T and C_idle,active=(I,-3j); the first components give explicit inverses.
   need(eqentry(r.prod(r.mono(pow(g.A,-y[0])),X[0]),r.mono(g.id)),"injective cross-column witness");fullColumnWitness++;
   need(eqentry(r.prod(Y[0],r.mono(pow(g.A,-x[0]))),r.mono(g.id)),"surjective cross-row witness");fullRowWitness++;cases++;
  }
 }
 const N=native(1,1),Nminus=native(1,1,-1),Cnonordinary=r.eye();Cnonordinary[2][2]=r.mono(g.qa);
 const paid=r.mm(r.mm(Nminus,Cnonordinary),N),paidExpected=r.eye();paidExpected[0][0]=r.mono(pow(g.A,2));paidExpected[1][1]=r.mono(pow(g.A,2));paidExpected[2][2]=r.mono(g.qa);
 need(eq(paid,paidExpected),"paid one-query sharpness control");
 const p0=project(r.mm(N,N),0);need(eqentry(p0[2][2],r.mono(g.id)),"nonzero ordinary corner control");
 const singular=r.eye();singular[1][1]=r.zero();singular[2][2]=r.zero();const singP1=project(r.mm(r.mm(Nminus,singular),N),1);
 need(singP1.every(row=>row.every(e=>e.size===0)),"invertibility premise control");
 const scale=10n**30n,cache={};function root(n){if(cache[n])return cache[n];if(n===0)return[0n,0n];let target=BigInt(n)**199n*scale**200n,lo=0n,hi=BigInt(n)*scale+1n;while(hi-lo>1n){const m=(lo+hi)/2n;if(m**200n<=target)lo=m;else hi=m}need(lo**200n<=target&&hi**200n>target,"power enclosure");return cache[n]=[lo,hi]}
 const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,k)=>[a[0]*BigInt(k),a[1]*BigInt(k)],sub=(a,b)=>[a[0]-b[1],a[1]-b[0]];
 const half=add(add(root(1),root(7)),root(8)),m2paid=add(mul(half,2),mul(root(7),2)),m2target=add(mul(root(16),2),root(15)),m2margin=sub(m2target,m2paid),m2query=sub(m2margin,root(1));
 const m3paid=add(mul(half,3),mul(root(7),6)),m3target=add(mul(root(23),3),root(22)),m3margin=sub(m3target,m3paid),m3query=sub(m3margin,root(1));
 need(m2margin[0]>0n&&m2query[1]<0n&&m3margin[0]>0n&&m3query[1]<0n,"mixed target budgets");
 const bodyAllocation=[];
 for(let idle=0;idle<=6;idle++){
  let best=null,profile=null,count=0;
  for(let a=0;a<=3;a++)for(let b=0;b<=3;b++)for(let c=0;c<=3;c++)for(let d=0;d<=3;d++)if(a+b+c+d===6+idle){
   const ranks=[7*a+2,7*b+2,7*c+2,7*d+1],target=ranks.map(root).reduce(add,[0n,0n]),paid=add(add(mul(half,3),mul(root(7),idle)),root(1)),margin=sub(target,paid);
   count++;need(margin[1]<0n,"all optimistic one-query mixed-head allocations fail");
   if(!best||margin[1]>best[1]){best=margin;profile=ranks;}
  }
  bodyAllocation.push({rank7_idles:idle,profiles_checked:count,maximizing_profile:profile,maximum_margin_interval:best.map(String)});
 }
 return{status:"PASS_TWO_HALF_THREE_ROLE_COMPONENT_GATE",model:"Fixed finite tensor Clifford algebra with exact phases and ordinary rank-preserving subgroup; all three input fields arbitrary; no extra owner, discarded field or nonordinary interstage service.",group_order:g.elements.length,finite_component_controls:{cases,full_column_inverse_witnesses:fullColumnWitness,full_row_inverse_witnesses:fullRowWitness},universal_proof:"If pi0(N2 C N1)=0 and C is invertible ordinary then C_idle,idle=0; the rank1 component has an injective cross column and a surjective cross row, hence rank at least two bank dimensions. A(2,2,1) target has only one.",negative_controls:{nonordinary_paid_query_evades_component_obstruction:true,nonzero_idle_corner_detected:true,singular_middle_invalidates_rank_bound:true},exact_budget:{t:"199/200",scale:String(scale),two_half_three_role_no_query:m2margin.map(String),two_half_three_role_one_rank1:m2query.map(String),three_half_four_role_no_query:m3margin.map(String),three_half_four_role_one_rank1:m3query.map(String),optimistic_one_query_three_full_one_partial:bodyAllocation},status_of_three_half_four_role:"Both one-query(2,2,2,2) and no-query(2,2,2,1) sufficient head-synthesis alternatives remain open.",complete_supplier:false,new_kappa:false};
}

console.log(JSON.stringify(verifyTwoHalfGate(),null,2));
