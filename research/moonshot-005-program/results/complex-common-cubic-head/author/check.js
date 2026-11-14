
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

function verifyCommonCubic() {
 const g=makeHeadGroup(),r=makeRing(g,4),need=(x,m)=>{if(!x)throw Error(m)};
 const pow=(x,n)=>{if(n<0){x=g.inv[x];n=-n}let z=g.id;for(let k=0;k<n;k++)z=g.mul[z][x];return z};
 const equal=(a,b)=>a.every((row,i)=>row.every((x,j)=>x.size===b[i][j].size&&[...x].every(([k,v])=>b[i][j].get(k)===v)));
 const clone=m=>m.map(row=>row.map(x=>new Map(x)));
 const rank=el=>{const u=g.elements[el].u,bb=(u[2]-u[0]-u[1])/2,a=u[0]%2,d=u[1]%2,b=(bb%2+2)%2;if(!a&&!b&&!d)return 0;if((a*d-b*b)%2)return 2;return 1;};
 const raw=r.eye();
 r.left(raw,3,r.mono(g.qa));
 r.rowop(raw,2,3,r.mono(g.id,-1));
 r.left(raw,1,r.mono(g.qa));
 r.rowop(raw,1,0,r.mono(g.id));
 r.left(raw,0,r.mono(g.qb));
 r.left(raw,2,r.mono(g.qb));
 const canonical=r.eye();canonical[0][0]=r.mono(g.qb);canonical[1][0]=r.mono(g.id);canonical[1][1]=r.mono(g.qa);canonical[2][2]=r.mono(g.qb);canonical[2][3]=r.mono(g.mul[g.qa][g.qb],-1);canonical[3][3]=r.mono(g.qa);
 need(equal(raw,canonical),"literal eight-event head map");
 const pre=r.eye();pre[1][1]=r.mono(g.inv[g.P]);pre[3][3]=r.mono(g.inv[g.P]);
 let actual=r.mm(raw,pre),withoutPost=clone(actual);r.left(actual,0,r.mono(g.inv[g.P]));r.left(actual,2,r.mono(g.inv[g.P]));
 const expected=r.eye();for(let i=0;i<4;i++)expected[i][i]=r.mono(g.inv[g.A]);expected[1][0]=r.mono(g.id);expected[2][3]=r.mono(pow(g.A,-2),-1);
 need(equal(actual,expected),"common cubic source");
 need(!equal(withoutPost,expected),"postpermutation negative control");
 const inverse=r.eye();for(let i=0;i<4;i++)inverse[i][i]=r.mono(g.A);inverse[1][0]=r.mono(pow(g.A,2),-1);inverse[2][3]=r.mono(g.id);
 need(equal(r.mm(actual,inverse),r.eye())&&equal(r.mm(inverse,actual),r.eye()),"literal inverse interface");
 const S=r.eye();S[1][1]=r.mono(g.id,-1);S[2][2]=r.mono(g.id,-1);const positiveInverse=r.mm(r.mm(S,inverse),S);
 const opposite=r.eye();for(let i=0;i<4;i++)opposite[i][i]=r.mono(g.A);opposite[1][0]=r.mono(pow(g.A,2));opposite[2][3]=r.mono(g.id,-1);
 need(equal(positiveInverse,opposite),"opposite baseline same couplings");
 const oldZ=g.mul[g.mul[g.inv[g.qa]][g.inv[g.qb]]][g.inv[g.qc]];
 need(pow(g.A,3)===oldZ&&pow(g.A,6)===g.id,"cubic and sixth power");
 const ranks=Array.from({length:6},(_,k)=>rank(pow(g.A,k)));
 need(ranks.join(",")==="0,1,2,2,2,1","all power ranks");
 need(rank(g.U)===1&&g.mul[g.mul[g.U][pow(g.P,2)]][g.inv[g.U]]===pow(g.A,2),"Hilbert 90 square");
 need(g.mul[g.mul[g.U][g.mul[g.Z][g.P]]][g.inv[g.U]]===g.A,"Hilbert 90 first power");
 need(g.mul[g.mul[g.qc][pow(g.P,2)]][g.inv[g.qc]]!==pow(g.A,2),"missing translation negative control");
 const swap=g.elements.findIndex(x=>x.u.every(y=>y===0)&&g.perms[x.p].join(",")==="1,0,2");
 need(pow(g.mul[g.inv[g.qb]][swap],3)!==g.Z,"swap is not cubic cycle");
 const scale=10n**30n,cache={};function root(n){if(cache[n])return cache[n];const target=BigInt(n)**199n*scale**200n;let lo=0n,hi=BigInt(n)*scale+1n;while(hi-lo>1n){let m=(lo+hi)/2n;if(m**200n<=target)lo=m;else hi=m}need(lo**200n<=target&&hi**200n>target,"power enclosure");return cache[n]=[lo,hi]}
 const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,n)=>[a[0]*BigInt(n),a[1]*BigInt(n)],sub=(a,b)=>[a[0]-b[1],a[1]-b[0]];
 const hs=add(add(root(1),root(7)),root(8)),paid=add(mul(hs,3),mul(root(7),6)),target=mul(root(23),4),margin=sub(target,paid),one=sub(margin,root(1)),two=sub(margin,root(2));
 need(one[0]>0n&&two[1]<0n,"one rank-one query fits; one rank-two query does not");
 return{status:"PASS_EXACT_COMMON_CUBIC_CONTROL",source:{commit:"83f65d544b43608eade0658083048ce0b615a933",path:"research/moonshot-005-program/results/quadratic-sign-query-gate/author/PROOF.md",git_blob:"8cddb0aff69b91ae648422f2cd5e77a12883ebe7",section:1},group:{size:192,ordinary_permutation_translation_subgroup:24,representation:"D_u P with u in (Z/4)^3 of even coordinate sum; permutation of three nonzero two-bit Walsh frequencies",A:g.elements[g.A],P:g.elements[g.P],Z:g.elements[g.Z],U:g.elements[g.U]},literal_source:{events:8,moves:6,adds:2,owners:0,move_profile:{"1":2,"7":2,"8":2},new_ordinary_permutations:4},common_source:"F A^-1 diag(L(A),U(-A^-1))",inverse_positive_body:"F A diag(L(A),U(-A^-1)) after literal inversion, ordinary F^2, and two destination sign conjugations",A_power_gaussian_ranks:ranks,hilbert90:"A^2=U P^2 U^-1; A=U (Z P) U^-1; U=Q_b^2 Q_c is a PAID rank-one Gaussian up to an ordinary translation",controls:{raw_four_column_identity:true,common_coupling:true,both_inverse_compositions:true,missing_post_permutation_rejected:true,wrong_order_two_permutation_rejected:true,missing_Hilbert90_translation_rejected:true},conditional_four_role_invoice:{native_halves:3,rank7_idles:6,desired_targets:{"23":4},unconstructed:true,scale:String(scale),native_half_interval:hs.map(String),room_before_queries:margin.map(String),room_after_one_rank1:one.map(String),room_after_one_rank2:two.map(String)},full120_linkage:"Not asserted or needed: this theorem starts from the committed canonical eight-event control.",complete_caller:false,new_kappa:false};
}

if(typeof module!=="undefined"){
 module.exports={verifyCommonCubic};
 if(require.main===module){
  const fs=require("fs"),crypto=require("crypto");
  if(process.argv.length!==3)throw Error("usage: node check.js PATH_TO_PINNED_SOURCE_PROOF_MD");
  const raw=fs.readFileSync(process.argv[2]),head=Buffer.from("blob "+raw.length+"\0");
  const sha=crypto.createHash("sha1").update(head).update(raw).digest("hex");
  if(sha!=="8cddb0aff69b91ae648422f2cd5e77a12883ebe7")throw Error("source Git blob mismatch");
  process.stdout.write(JSON.stringify(verifyCommonCubic(),null,2)+"\n");
 }
}
