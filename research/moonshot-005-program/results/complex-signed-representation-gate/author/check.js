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

function verifySignedPermutationGate(){
 const g=makeHeadGroup(),need=(x,m)=>{if(!x)throw Error(m)},swap=[1,0,2];
 const data=g.elements.map(e=>{const parity=(e.u[0]+e.u[1]+e.u[2])/2%2,bits=[(parity+e.u[1])%2,(parity+e.u[0])%2,(parity+e.u[0]+e.u[1])%2],tau=swap.map(j=>swap[g.perms[e.p][j]]);return{bits,tau};});
 const mul=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,x,k)=>s+x*B[k][j],0)));
 const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j)));
 const rep=(e,signed)=>{const d=data[e];return Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>+(i===d.tau[j])*(signed&&d.bits[i]?-1:1)));};
 const reps0=g.elements.map((_,i)=>rep(i,false)),reps1=g.elements.map((_,i)=>rep(i,true)),eq=(A,B)=>A.every((row,i)=>row.every((v,j)=>v===B[i][j]));
 let homomorphisms=0;
 for(let a=0;a<192;a++)for(let b=0;b<192;b++){const c=g.mul[a][b];need(eq(mul(reps0[a],reps0[b]),reps0[c])&&eq(mul(reps1[a],reps1[b]),reps1[c]),"two exact representations");homomorphisms+=2;}
 for(const h of g.H)need(eq(reps0[h],reps1[h]),"ordinary agreement");
 const rank=e=>{const u=g.elements[e].u,a=u[0]%2,d=u[1]%2,b=((u[2]-u[0]-u[1])/2%2+2)%2;return!a&&!b&&!d?0:(a*d-b*b)%2?2:1;};
 const census={};for(let e=0;e<192;e++){const delta=data[e].bits.reduce((a,b)=>a+b,0),key=rank(e)+","+delta;census[key]=(census[key]||0)+1;}
 need(JSON.stringify(census)==='{"0,0":24,"2,3":24,"1,1":72,"2,2":72}'||Object.keys(census).length===4&&census["0,0"]===24&&census["1,1"]===72&&census["2,2"]===72&&census["2,3"]===24,"rank-difference census");
 const pow=(e,n)=>{if(n<0){e=g.inv[e];n=-n}let z=g.id;for(let k=0;k<n;k++)z=g.mul[z][e];return z;};
 const sub=(A,B)=>A.map((row,i)=>row.map((v,j)=>v-B[i][j]));
 const block=(D,O)=>Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>i<3?(j<3?D[i][j]:O[i][j-3]):j<3?0:D[i-3][j-3]));
 const zero=Array.from({length:3},()=>Array(3).fill(0));
 const nativeControls=[];
 for(const s of[-1,1])for(const eps of[-1,1])for(const c of[-1,1]){
  const B0=reps0[pow(g.A,s)],B1=reps1[pow(g.A,s)],X=sub(B1,B0),D=sub(block(B1,reps1[pow(g.A,s+eps)].map(row=>row.map(v=>c*v))),block(B0,reps0[pow(g.A,s+eps)].map(row=>row.map(v=>c*v))));
  const target=block(X,zero);let actual=D;
  if(s===eps){
   const L=eye(6),R=eye(6);for(let i=0;i<3;i++)for(let j=0;j<3;j++){L[i][j+3]=-c*B0[i][j];R[i][j+3]=-c*B1[i][j];}
   actual=mul(mul(L,D),R);
  }
  need(eq(actual,target),"native triangular difference reduction");need(data[pow(g.A,s)].bits.reduce((a,b)=>a+b,0)===1,"native diagonal difference rank one");nativeControls.push({sigma:s,epsilon:eps,coupling:c,difference_rank:2});
 }
 const qControls=[];
 for(let e=0;e<192;e++)if(rank(e)===1){const X=sub(reps1[e],reps0[e]);need(data[e].bits.reduce((a,b)=>a+b,0)===1,"all rank-one query differences");qControls.push(e);}
 const lambdaChecks=[];for(const q of[g.qa,g.qb,g.qc]){const h=g.mul[q][q];need(g.H.includes(h)&&eq(reps0[h],eye(3))&&eq(reps1[h],eye(3)),"lambda square translation collapses equally");lambdaChecks.push(h);}
 return{status:"PASS_SIGNED_PERMUTATION_CALLER_GATE",source_group:192,ordinary_subgroup:24,quotient:"C2^3 semidirect S3, after the four ordinary translations",exact_representation_multiplication_checks:homomorphisms,census_gaussian_rank_and_difference_rank:census,native_controls:nativeControls,rank1_query_types_checked:qControls.length,query_modes:["in-place","distinct-bank shear"],ordinary_lambda_translation_controls:lambdaChecks,universal_inequality:"h1 + 2*h2_nonalt + 3*h2_Z <= 2*m + q1 + 2*q2_nonalt + 3*q2_Z",closed_targets:[{halves:3,rank1_queries:1,head_targets:[2,2,2,2],minimum_difference_rank:8,available:7},{halves:3,rank1_queries:0,head_targets:[2,2,2,1],minimum_difference_rank:7,available:6}],surviving_changed_query_target:{halves:1,rank1_queries:1,rank2_Z_queries:1,head_targets:["rank2_nonalt","rank2_nonalt","rank2_nonalt"],required_difference_rank:6,available_difference_rank:6,caller_unconstructed:true},scope:"Fixed collective tensor G192 with ordinary matrix coefficients in C[H24]; exact phases retained. No claim for larger ordinary quadratic-phase Clifford operators, column-specific encodings, approximate degeneration, changed native/body source, or all algorithms.",new_kappa:false};
}

function verifyChangedQueryBudget(){
 const scale=10n**30n,cache={},need=(x,m)=>{if(!x)throw Error(m)};
 function root(n){if(cache[n])return cache[n];let lo=0n,hi=BigInt(n)*scale+1n,target=BigInt(n)**199n*scale**200n;while(hi-lo>1n){const m=(lo+hi)/2n;if(m**200n<=target)lo=m;else hi=m;}need(lo**200n<=target&&hi**200n>target,"root");return cache[n]=[lo,hi];}
 const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,k)=>[a[0]*BigInt(k),a[1]*BigInt(k)],sub=(a,b)=>[a[0]-b[1],a[1]-b[0]];
 const paid=add(add(mul(root(1),2),mul(root(7),2)),add(root(8),root(2))),margin=sub(mul(root(9),3),paid);
 need(margin[0]>0n,"changed-query raw room");
 return{t:"199/200",scale:String(scale),native_halves:1,rank7_idles:1,rank2_Z_queries:1,rank1_queries:1,target_gaussian_ranks:[9,9,9],paid_interval:paid.map(String),raw_margin_interval:margin.map(String),head_circuit:"OPEN: raw price and representation inequality only"};
}
function verifyLambdaButterfly(){
 const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],times=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],z=[0,0],one=[1,0];
 const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,a,k)=>add(s,times(a,B[k][j])),[0,0]))),eq=(A,B)=>A.every((row,i)=>row.every((x,j)=>x[0]===B[i][j][0]&&x[1]===B[i][j][1]));
 const sub=[[one,[-1,0]],[z,one]],scaleBeta=[[[1,-1],z],[z,[2,0]]],addIntoV=[[one,z],[one,one]],scaleGamma=[[[-1,1],z],[z,one]],addIntoU=[[one,one],[z,one]];
 const numerator=mm(mm(mm(mm(addIntoU,scaleGamma),addIntoV),scaleBeta),sub),expected=[[[1,1],[1,-1]],[[1,-1],[1,1]]];
 if(!eq(numerator,expected))throw Error("five-operation butterfly numerator");
 const square=mm(numerator,numerator),fourSwap=[[z,[4,0]],[[4,0],z]];
 if(!eq(square,fourSwap))throw Error("lambda squared translation");
 const adj=expected[0].map((_,i)=>expected.map(row=>[row[i][0],-row[i][1]])),unitarity=mm(adj,numerator),fourI=[[[4,0],z],[z,[4,0]]];
 if(!eq(unitarity,fourI))throw Error("lambda unitary");
 return{status:"PASS_EXACT_FIVE_OPERATION_LAMBDA",pair_algorithm:["u <- u-v","u <- ((1-i)/2)u","v <- v+u","u <- (-1+i)u","u <- u+v"],scalar_adds_per_pair:3,scalar_scales_per_pair:2,extra_scalar_or_field_storage:0,restoration:"No helper is acquired; inverse is the reversed five-step word with inverse scales.",denominator_per_service:2,source_normalization_services_per_half:4,scalar_adds_per_half_per_field_dimension:"6D",scalar_scales_per_half_per_field_dimension:"4D",layout:"If translation-paired coordinates are not directly accessible, charge one explicit ordinary pairing permutation and its inverse per lambda; at most8 such layout permutations per half, plus the2 head-swap gauge permutations. Their bit/tape implementation remains an inherited ordinary compiler obligation.",gaussian_rank_moves_added:0,compiler_status:"Fixed finite Gaussian-dyadic coefficients and bounded local prefixes; no precision-dependent degeneration. Full finite compiler constants must include these services."};
}

function verifyLiteralLambdaSource(){
 const g=makeHeadGroup(),need=(x,m)=>{if(!x)throw Error(m)},ca=(x,y)=>[x[0]+y[0],x[1]+y[1]],cm=(x,y)=>[x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]],mono=(e,c=[1,0])=>new Map([[e,c]]);
 const sum=(A,B)=>{const C=new Map(A);for(const[e,b]of B){const c=ca(C.get(e)||[0,0],b);if(c[0]||c[1])C.set(e,c);else C.delete(e);}return C;};
 const prod=(A,B)=>{let C=new Map();for(const[e,a]of A)for(const[f,b]of B)C=sum(C,mono(g.mul[e][f],cm(a,b)));return C;},scale=(A,n)=>new Map([...A].map(([e,c])=>[e,[n*c[0],n*c[1]]]));
 const eye=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>i===j?mono(g.id):new Map())),mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>sum(s,prod(v,B[k][j])),new Map())));
 const eqe=(A,B)=>A.size===B.size&&[...A].every(([e,c])=>{const d=B.get(e);return d&&c[0]===d[0]&&c[1]===d[1];}),eq=(A,B)=>A.every((row,i)=>row.every((v,j)=>eqe(v,B[i][j])));
 const lambda=q=>sum(mono(g.id,[1,1]),mono(g.mul[q][q],[1,-1])),lambdainv=q=>sum(mono(g.id,[1,-1]),mono(g.mul[q][q],[1,1]));
 const La=lambda(g.qa),Lb=lambda(g.qb),Lai=lambdainv(g.qa),Lbi=lambdainv(g.qb),Sa=prod(La,mono(g.inv[g.qa])),Sb=prod(Lb,mono(g.inv[g.qb]));
 const raw=eye();raw[0][0]=mono(g.qb);raw[1][0]=mono(g.id);raw[1][1]=mono(g.qa);raw[2][2]=mono(g.qb);raw[2][3]=mono(g.mul[g.qa][g.qb],[-1,0]);raw[3][3]=mono(g.qa);
 const pre=eye().map(row=>row.map(v=>scale(v,2)));pre[0][0]=La;pre[2][2]=La;
 const post=eye();post[0][0]=prod(Lai,Lbi);post[2][2]=prod(Lai,Lbi);post[1][1]=scale(Lai,2);post[3][3]=scale(Lai,2);
 const actual=mm(mm(post,raw),pre),target=eye();target[0][0]=scale(Sb,4);target[1][1]=scale(Sa,4);target[1][0]=mono(g.id,[8,0]);target[2][2]=scale(Sb,4);target[2][3]=scale(prod(Sa,Sb),-2);target[3][3]=scale(Sa,4);
 need(eq(actual,target),"all four literal normalized source columns, common denominator8");
 const P=g.elements.findIndex(e=>e.u.every(x=>x===0)&&g.perms[e.p].join(",")==="1,0,2"),A=prod(Sb,mono(P)),Ai=prod(mono(P),Sb);
 need(eqe(prod(A,Ai),mono(g.id,[4,0])),"normalized A inverse");
 need(eqe(prod(A,A),prod(Sa,Sb)),"normalized A squared");
 need(eqe(prod(prod(A,A),prod(A,A)),mono(g.id,[16,0])),"normalized A fourth power");
 const pg=eye(),qg=eye();pg[1][1]=mono(P);pg[3][3]=mono(P);qg[0][0]=mono(P);qg[2][2]=mono(P);const common=mm(mm(qg,target),pg),want=eye();for(let i=0;i<4;i++)want[i][i]=scale(Ai,4);want[1][0]=mono(g.id,[8,0]);want[2][3]=scale(prod(A,A),-2);need(eq(common,want),"ordinary swap common source, all four columns");
 return{status:"PASS_LITERAL_LAMBDA_NORMALIZED_SOURCE",normalization:"pre lambda_a on X,U; post lambda_a^-1 lambda_b^-1 on X,U and lambda_a^-1 on Y,V",exact_source_matrix_denominator:8,arbitrary_input_columns_checked:4,normalized_head:"A=S_b P, P swaps a,b; A^2=S_a S_b; A^4=I",all_gaussian_input_coefficients_retained:true,common_source_verified:true,not_a_caller:true};
}

console.log(JSON.stringify({gate:verifySignedPermutationGate(),changed_query_budget:verifyChangedQueryBudget(),lambda:verifyLambdaButterfly(),literal_normalization:verifyLiteralLambdaSource()},null,2));
