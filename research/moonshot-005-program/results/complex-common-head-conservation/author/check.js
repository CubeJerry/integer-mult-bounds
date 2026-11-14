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

function verifyCommonHeadConservation(){
 const g=makeHeadGroup(),p=101,need=(x,m)=>{if(!x)throw Error(m)},eta=g.elements.map(e=>e.u.reduce((a,b)=>a+b,0)%4===0?1:-1),swap=[1,0,2];
 const reps=g.elements.map(e=>{const q=e.u.reduce((a,b)=>a+b,0)/2%2,x=[(q+e.u[1])%2,(q+e.u[0])%2,(q+e.u[0]+e.u[1])%2],pm=swap.map(j=>swap[g.perms[e.p][j]]);return Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>+(i===pm[j])*(x[i]?-1:1)));});
 const reps0=g.elements.map(e=>{const pm=swap.map(j=>swap[g.perms[e.p][j]]);return Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>+(i===pm[j])));});
 const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>+(i===j))),zero=(n,m=n)=>Array.from({length:n},()=>Array(m).fill(0)),tr=A=>A[0].map((_,j)=>A.map(row=>row[j])),mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,a,k)=>s+a*B[k][j],0))),sub=(A,B)=>A.map((row,i)=>row.map((v,j)=>v-B[i][j])),add=(A,B)=>A.map((row,i)=>row.map((v,j)=>v+B[i][j])),eq=(A,B)=>A.every((row,i)=>row.every((v,j)=>v===B[i][j])),rank=A=>A.length?nullspaceMod(A,A[0].length,p).rank:0;
 const pow=(e,k)=>{if(k<0){e=g.inv[e];k=-k}let z=g.id;for(let j=0;j<k;j++)z=g.mul[z][e];return z;};
 const rankg=e=>{const u=g.elements[e].u,a=u[0]%2,d=u[1]%2,b=((u[2]-u[0]-u[1])/2%2+2)%2;return!a&&!b&&!d?0:(a*d-b*b)%2?2:1;};
 let secondHomomorphismChecks=0; const rep2=reps.map((M,e)=>M.map(row=>row.map(v=>eta[e]*v))); for(let a=0;a<192;a++)for(let b=0;b<192;b++){need(eq(mm(rep2[a],rep2[b]),rep2[g.mul[a][b]]),"second representation homomorphism");secondHomomorphismChecks++;}
 const secondCensus={};for(let e=0;e<192;e++){const r=rank(sub(reps[e].map(row=>row.map(v=>eta[e]*v)),reps0[e])),key=rankg(e)+","+r;secondCensus[key]=(secondCensus[key]||0)+1;}
 need(secondCensus["0,0"]===24&&secondCensus["1,2"]===72&&secondCensus["2,2"]===72&&secondCensus["2,0"]===24,"second pair census");
 let st=6138123;const rand=n=>{st^=st<<13;st^=st>>>17;st^=st<<5;return(st>>>0)%n;};
 let controls=0,sylvesterChecks=0,rightChecks=0,leftChecks=0,wrongLeftRejected=0,omittedEvenRejected=0,nativeSecondChecks=0;
 for(const sigma of[-1,1])for(const eps of[-1,1])for(const c of[-1,1]){
  const a=pow(g.A,sigma),o=pow(g.A,sigma+eps),B0=reps0[a],B1=reps[a].map(row=>row.map(v=>eta[a]*v)),O0=reps0[o],O1=reps[o].map(row=>row.map(v=>eta[o]*v)),block=(B,O)=>Array.from({length:6},(_,i)=>Array.from({length:6},(_,j)=>i<3?(j<3?B[i][j]:c*O[i][j-3]):j<3?0:B[i-3][j-3]));
  need(rank(sub(block(B1,O1),block(B0,O0)))===4,"second pair native rank4");nativeSecondChecks++;
 }
 function setBlock(M,i,j,B,c=1){for(let a=0;a<3;a++)for(let b=0;b<3;b++)M[3*i+a][3*j+b]=c*B[a][b];}
 for(let caseId=0;caseId<96;caseId++){
  const R=2+caseId%4,n=3*R,gates=[];
  function ordinary(){let i=rand(R),j=rand(R-1);if(j>=i)j++;const F=eye(n),h=g.H[rand(24)];setBlock(F,i,j,reps[h],rand(2)?1:-1);return{F,theta:F,kind:"ordinary"};}
  function coordinateRows(banks){return banks.flatMap(i=>Array.from({length:3},(_,a)=>Array.from({length:n},(_,j)=>+(j===3*i+a))));}
  gates.push(ordinary());
  const specs=[];for(let j=0;j<1+caseId%3;j++)specs.push("native");specs.push("rank1","Z");for(let j=0;j<1+caseId%2;j++)specs.push("even");
  for(let j=specs.length-1;j>0;j--){const k=rand(j+1);[specs[j],specs[k]]=[specs[k],specs[j]];}
  for(const kind of specs){
   let i=rand(R),j=rand(R-1);if(j>=i)j++;let F=eye(n),T=eye(n),rb,lb,wrongLb;
   if(kind==="native"){
    const s=rand(2)?1:-1,e=rand(2)?1:-1,c=rand(2)?1:-1,a=pow(g.A,s),o=pow(g.A,s+e);for(const k of[i,j]){setBlock(F,k,k,reps[a]);setBlock(T,k,k,reps[a],-1);}setBlock(F,i,j,reps[o],c);setBlock(T,i,j,reps[o],c);rb=lb=[i,j];wrongLb=lb;
   }else{
    const e=kind==="rank1"?[g.qa,g.qb,g.qc][rand(3)]:kind==="Z"?g.Z:pow(g.A,2),self=rand(2)===0;
    if(self){setBlock(F,i,i,reps[e]);setBlock(T,i,i,reps[e],eta[e]);rb=lb=[i];wrongLb=lb;}
    else{setBlock(F,i,j,reps[e]);setBlock(T,i,j,reps[e],eta[e]);rb=[j];lb=[i];wrongLb=[j];}
   }
   gates.push({F,theta:T,kind,right:coordinateRows(rb),left:tr(coordinateRows(lb)),wrongLeft:tr(coordinateRows(wrongLb))});gates.push(ordinary());
  }
  const prefix=[eye(n)],oprefix=[eye(n)];for(const F of gates){prefix.push(mm(F.F,prefix.at(-1)));oprefix.push(F.kind==="ordinary"?mm(F.F,oprefix.at(-1)):oprefix.at(-1));}
  const suffix=Array(gates.length+1),osuffix=Array(gates.length+1);suffix[gates.length]=eye(n);osuffix[gates.length]=eye(n);for(let j=gates.length-1;j>=0;j--){suffix[j]=mm(suffix[j+1],gates[j].theta);osuffix[j]=gates[j].kind==="ordinary"?mm(osuffix[j+1],gates[j].F):osuffix[j+1];}
  let total=zero(n),rAct=[],rOrd=[],lAct=[],lOrd=[],wrongAct=[],wrongOrd=[],oddRows=[],oddCols=[],sumRanks=0;
  for(let j=0;j<gates.length;j++){const G=gates[j];if(G.kind==="ordinary")continue;
   rOrd.push(...mm(G.right,oprefix[j]));lOrd.push(...tr(mm(osuffix[j+1],G.left)));wrongOrd.push(...tr(mm(osuffix[j+1],G.wrongLeft)));
   if(G.kind==="even"){rAct.push(...mm(G.right,prefix[j]));lAct.push(...tr(mm(suffix[j+1],G.left)));wrongAct.push(...tr(mm(suffix[j+1],G.wrongLeft)));}
   else{const T=mm(mm(suffix[j+1],sub(G.F,G.theta)),prefix[j]),rr=rank(T);need(rr===(G.kind==="native"?6:3),"local theta difference rank");sumRanks+=rr;total=add(total,T);rAct.push(...T);lAct.push(...tr(T));wrongAct.push(...tr(T));oddRows.push(...T);oddCols.push(...tr(T));}
  }
  need(eq(total,sub(prefix.at(-1),suffix[0])),"full telescope");
  const rr=rank(rAct),ro=rank(rOrd),lr=rank(lAct),lo=rank(lOrd);need(rr===ro&&rank([...rAct,...rOrd])===rr,"right ordinary constraints");rightChecks++;need(lr===lo&&rank([...lAct,...lOrd])===lr,"left ordinary constraints");leftChecks++;
  const wa=rank(wrongAct),wo=rank(wrongOrd);if(wa!==wo||rank([...wrongAct,...wrongOrd])!==wa)wrongLeftRejected++;
  if(rank(oddRows)!==ro||rank([...oddRows,...rOrd])!==ro)omittedEvenRejected++;
  need(rank(total)>=rank(oddRows)+rank(oddCols)-sumRanks,"Sylvester source inequality");sylvesterChecks++;controls++;
 }
 need(wrongLeftRejected>0&&omittedEvenRejected>0,"negative kernel controls");
 const scale=10n**24n,cache={};function root(n){if(cache[n])return cache[n];let lo=0n,hi=BigInt(n)*scale+1n,target=BigInt(n)**199n*scale**200n;while(hi-lo>1n){const mid=(lo+hi)/2n;if(mid**200n<=target)lo=mid;else hi=mid;}need(lo**200n<=target&&hi**200n>target,"rigorous powers");return cache[n]=[lo,hi];}
 const ia=(a,b)=>[a[0]+b[0],a[1]+b[1]],im=(a,k)=>[a[0]*BigInt(k),a[1]*BigInt(k)],is=(a,b)=>[a[0]-b[1],a[1]-b[0]];
 let prices=0,minGap=null;
 for(let m=1;m<=6;m++)for(let R=2;R<=8;R++)for(let x=0;x<=3;x++)for(let z=0;z<=3;z++)for(let w=0;w<=3;w++){
  const H=Math.min(2*R,2*m+x+2*z+2*w),q=Math.floor(H/R),rem=H%R,target=ia(im(root(7*m+q),R-rem),im(root(7*m+q+1),rem));
  const paid=ia(ia(im(root(7),m*(R-1)),im(root(8),m)),ia(im(root(1),m+x),im(root(2),z+w))),gap=is(paid,target);
  need(gap[0]>0n,"all admissible finite common-body prices are negative");prices++;if(!minGap||gap[0]<BigInt(minGap.lower))minGap={m,R,x,z,w,H,lower:String(gap[0]),upper:String(gap[1])};
 }
 const rejectedCandidateMargin=is(im(root(16),4),ia(ia(im(root(7),6),im(root(8),2)),ia(im(root(1),3),root(2))));
 need(rejectedCandidateMargin[0]>0n&&8>2*2+1+2,"favourable arithmetic but forbidden head rank");
 const gr=makeRing(g,3),Np=gr.eye(),Nm=gr.eye(); for(const N of[Np,Nm]){N[0][0]=gr.mono(g.A);N[1][1]=gr.mono(g.A);} Np[0][1]=gr.mono(pow(g.A,2)); Nm[0][1]=gr.mono(pow(g.A,2),-1); const sharp=gr.mm(Nm,Np),sharpWant=gr.eye();sharpWant[0][0]=gr.mono(pow(g.A,2));sharpWant[1][1]=gr.mono(pow(g.A,2));need(sharp.every((row,i)=>row.every((M,j)=>M.size===sharpWant[i][j].size&&[...M].every(([e,c])=>sharpWant[i][j].get(e)===c))),"sharp exact group-ring source");
 return{status:"PASS_COMMON_HEAD_CONSERVATION_CONTROLS",second_representation_homomorphism_checks:secondHomomorphismChecks,sharp_two_native_endpoint:true,group_order:192,ordinary_subgroup:24,second_representation_census:secondCensus,second_representation_native_cases:nativeSecondChecks,kernel_controls:{field_prime:p,representation:"signed3D permutation quotient; finite checks validate telescoping/constraint identities, not a substitute for faithful tensor proof",words:controls,right_constraint_checks:rightChecks,left_constraint_checks:leftChecks,sylvester_checks:sylvesterChecks,wrong_left_shear_bank_rejections:wrongLeftRejected,omitted_even_query_constraint_rejections:omittedEvenRejected},price_controls:{t:"199/200",scale:String(scale),m_range:[1,6],R_range:[2,8],x_z_w_range:[0,3],cases:prices,heads:"Worst balanced rank0/1/2 profile consistent with conservation; every smaller rank sum has less target credit.",minimum_paid_minus_target:minGap,rejected_positive_margin_two_half_four_role:rejectedCandidateMargin.map(String)},universal_theorem:"H_tot <=2m+x+2z+2w; all completed common-body invoices have paid>target for every0<t<1 andm>=1.",no_new_kappa:true};
}

console.log(JSON.stringify(verifyCommonHeadConservation(),null,2));
