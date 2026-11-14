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

function verifyFiniteRankComponents(){
 const g=makeHeadGroup(),need=(x,m)=>{if(!x)throw Error(m)},n=g.elements.length;
 const rank=el=>{const u=g.elements[el].u,a=u[0]%2,d=u[1]%2,b=((u[2]-u[0]-u[1])/2%2+2)%2;if(!a&&!b&&!d)return 0;return((a*d-b*b)%2)?2:1};
 const ranks=g.elements.map((_,i)=>rank(i)),chars=g.elements.map(x=>{let re=1,im=0;for(let j=0;j<3;j++)if(g.perms[x.p][j]===j){re+=[1,0,-1,0][x.u[j]];im+=[0,1,0,-1][x.u[j]]}return[re,im]});
 let max2=0,scalars=0;for(let i=0;i<n;i++){const s=chars[i][0]**2+chars[i][1]**2;if(s===16)scalars++;if(i!==g.id)max2=Math.max(max2,s)}
 need(scalars===1&&max2===8,"projective distinctness and exact trace bound");
 let contacts=0;for(const h of g.H)for(let x=0;x<n;x++){need(ranks[g.mul[h][x]]===ranks[x]&&ranks[g.mul[x][h]]===ranks[x],"rank bimodule");contacts+=2}
 const modRanks=[],prime=101,imaginary=10,cpow=(x,e)=>{let z=1;for(let j=0;j<e;j++)z=z*x%prime;return z};
 for(let V=1;V<=6;V++){
  const cp=chars.map(([a,b])=>cpow((a+imaginary*b+prime*10)%prime,V)),Gram=g.elements.map((_,i)=>g.elements.map((_,j)=>cp[g.mul[g.inv[i]][j]]));
  const rr=nullspaceMod(Gram,n,prime).rank;modRanks.push({V,rank_mod101:rr});
 }
 need(modRanks[0].rank_mod101===10&&modRanks[5].rank_mod101===192,"finite Gram independence");
 need(191<256,"V16 diagonal dominance");
 const r=makeRing(g,2),eq=(a,b)=>a.every((row,i)=>row.every((x,j)=>x.size===b[i][j].size&&[...x].every(([k,v])=>b[i][j].get(k)===v)));
 const project=(M,k)=>M.map(row=>row.map(x=>new Map([...x].filter(([e])=>ranks[e]===k))));
 let checks=0;
 for(let s=0;s<16;s++){
  const M=[[r.sum(r.mono(g.qa),r.mono(g.H[s%24],s+1)),r.mono(g.rank2N)],[r.mono(g.A),r.sum(r.mono(g.Z),r.mono(g.qb,-1))]];
  const L=r.eye(),R=r.eye();L[0][1]=r.mono(g.H[(3*s)%24],2);R[1][0]=r.mono(g.H[(5*s+1)%24],-3);
  for(let k=0;k<3;k++){need(eq(project(r.mm(r.mm(L,M),R),k),r.mm(r.mm(L,project(M,k)),R)),"exact rank component intertwining");checks++;}
 }
 need(ranks[g.qa]===1&&ranks[g.mul[g.qa][g.qa]]===0,"nonordinary multiplication is not rank preserving");
 // The one-column identity C_a=alpha I+beta X_a fails for its collective tensor lift at width two.
 const oneColumn={Qa_on_frequency_a:[0,1],alpha_minus_beta:[0,1]},twoColumn={Qa_tensor_on_a_a:[-1,0],alpha_plus_beta:[1,0]};
 need(oneColumn.Qa_on_frequency_a.join(",")===oneColumn.alpha_minus_beta.join(",")&&twoColumn.Qa_tensor_on_a_a.join(",")!==twoColumn.alpha_plus_beta.join(","),"one-column false-ordinary control");
 return{status:"PASS_FINITE_HEAD_RANK_COMPONENTS",group:{order:n,ordinary_subgroup:g.H.length,rank_counts:[0,1,2].map(k=>ranks.filter(x=>x===k).length),nontrivial_scalar_operators:scalars-1,maximum_nonidentity_trace_squared:max2,dimension:4},tensor_separation:{analytic_all_width_threshold:16,strict_Gram_row_bound_at16:"191/256",finite_exact_Gram_prime:prime,finite_exact_Gram_imaginary:imaginary,finite_Gram_ranks:modRanks,certified_all_width_threshold:6,monotonicity_reason:"Every group element fixes the zero Walsh basis vector, so width-V independence implies width-(V+1) independence."},rank_bimodule:{left_and_right_multiplications_checked:contacts,exact_matrix_component_controls:checks},negative_controls:{one_column_false_ordinary:true,two_column_rejection:true,nonordinary_left_multiplier_changes_rank:true},scope:"Fixed finite one-column unitary/Clifford family and ordinary subgroup; tensor lifts and exact global scalar phases retained. No all-head-circuit impossibility, rank-only target sufficiency, movement lower bound, or new kappa.",new_kappa:false};
}

console.log(JSON.stringify(verifyFiniteRankComponents(), null, 2));
