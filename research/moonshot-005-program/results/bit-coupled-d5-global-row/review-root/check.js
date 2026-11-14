
function reviewD5Pair(flat){
 const need=(b,m)=>{if(!b)throw Error(m)},gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r}return a},
 Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return[n/g,d/g]},
 add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]),div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]),zero=()=>Q(0);
 function rref(input){const A=input.map(r=>r.map(x=>Array.isArray(x)?Q(x[0],x[1]):Q(x))),piv=[];let r=0;for(let c=0;c<8&&r<A.length;c++){let s=r;while(s<A.length&&!A[s][c][0])s++;if(s===A.length)continue;[A[r],A[s]]=[A[s],A[r]];const z=A[r][c];A[r]=A[r].map(x=>div(x,z));for(let i=0;i<A.length;i++)if(i!==r&&A[i][c][0]){const w=A[i][c];A[i]=A[i].map((x,j)=>add(x,neg(mul(w,A[r][j]))));}piv.push(c);r++;}return{rows:A.slice(0,r),piv};}
 const nullspace=input=>{const a=rref(input);return Array.from({length:8},(_,j)=>j).filter(j=>!a.piv.includes(j)).map(j=>{const v=Array.from({length:8},zero);v[j]=Q(1);a.piv.forEach((p,k)=>v[p]=neg(a.rows[k][j]));return v})};
 const canon=input=>rref(input).rows,serialize=B=>JSON.stringify(B.map(r=>r.map(x=>x[0]+"/"+x[1]))),signatures=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 need(new Set(signatures).size===120,"root signatures");const mapping=Array.from({length:111},(_,i)=>signatures.indexOf(flat.independent_generators.map(w=>+w.native_difference.includes(i)).join("")));need(mapping.every(x=>x>=0)&&new Set(mapping).size===111,"native mapping");const R=mapping.map(i=>flat.full_roots[i]);

 const dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),bit=i=>1n<<BigInt(i),rank2=rows=>{const b=new Map();for(let x of rows)while(x){const k=x&-x;if(b.has(k))x^=b.get(k);else{b.set(k,x);break;}}return b.size;},set=S=>S.reduce((x,i)=>x|bit(i),0n);
 const n1=[92,54,38],n2=[1,18,31],D=R.flatMap((r,i)=>n1.every(j=>dot(r,R[j])===0)?[i]:[]),E=R.flatMap((r,i)=>n2.every(j=>dot(r,R[j])===0)?[i]:[]);
 need(D.length===18&&E.length===19&&D.filter(i=>E.includes(i)).join(",")==="72","exact source cohorts");
 need(canon(n1.concat(n2).map(i=>R[i])).length===6,"meet rank2");
 const q=[0,0,1,1,0,0,1,-1];need(dot(q,q)===4&&dot(q,R[72])===0,"omitted normal");
 const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b)||JSON.stringify(a.map(x=>-x))===JSON.stringify(b);
 need(flat.full_roots.some(r=>same(r,q))&&!R.some(r=>same(r,q)),"actual omitted root");
 const K=R.map((r,i)=>R.reduce((x,t,j)=>i===j||dot(r,t)===0?x|bit(j):x,0n)),z=set(D),zz=set(E),a=z^bit(72),b=zz^bit(72);
 need(z===(K[92]&K[54]&K[38])&&zz===(K[1]&K[18]&K[31]),"cubic product identities");

 const frame=[0,1,2,4,8,14,30,59],G=frame.map(i=>frame.reduce((m,j,k)=>m|((((dot(R[i],R[j])/2)%2+2)%2)<<k),0)),par=x=>{let y=0;while(x){y^=x&1;x>>=1;}return y;};
 const dual=new Map();for(let x=0;x<256;x++){const y=G.reduce((s,g,k)=>s|(par(g&x)<<k),0);need(!dual.has(y),"nondegenerate frame");dual.set(y,x);}
 const X=R.map(r=>dual.get(frame.reduce((s,j,k)=>s|((((dot(r,R[j])/2)%2+2)%2)<<k),0)));
 const c=set(X.flatMap((x,i)=>par(189&x)===0?[i]:[])),target=c^a^b,L=R.flatMap((_,i)=>i!==72&&(target&bit(i))?[i]:[]);
 need(rank2(K)===9&&rank2(K.concat(c))===9,"canonical c");
 need(L.length===16&&(target&bit(72))!==0n&&!(target&~K[72]),"valid proper row");
 need(L.every(i=>dot(R[i],q)===0)&&canon(L.map(i=>R[i])).length===6,"rank6 correction chart");
 const M=K.slice();M[72]=target;
 need(rank2(M)===10&&rank2(M.concat(K))===10,"actual fitting and quotient");
 need(rank2(K.concat(z,zz))===11&&rank2(K.concat(a,b))===11,"separate histories");
 const pop=x=>x.toString(2).split("1").length-1,Q3=Array.from({length:256},(_,m)=>m).filter(m=>pop(m)<=3).map(m=>set(X.flatMap((x,i)=>(x&m)===m?[i]:[])));
 need(rank2(Q3)===84&&rank2(Q3.concat(a))===85&&rank2(Q3.concat(b))===85&&rank2(Q3.concat(a^b))===84,"punctured/cubic distinction");
 const s=38;let qvalue=par(s);for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)qvalue^=((s>>i)&1)&((s>>j)&1)&((G[i]>>j)&1);
 need(qvalue===0&&X.every((x,i)=>Number(c>>BigInt(i)&1n)===(1^par(G.reduce((v,row,k)=>v|((par(row&s))<<k),0)&x))),"singular canonical form");
 need((a&b)===0n&&!(set(L)&(a|b)),"disjoint raw acquisition");
 const g=K[92],moved=R.flatMap((_,i)=>(c|g)&bit(i)?[i]:[]);
 need(moved.length===81&&rank2([c,g,a,b])===4,"actual initial supports/history");
 const bad=c^z^b;need(!(bad&bit(72)),"one-sided separator control");
 return{status:"PASS_ROOT_COUPLED_D5_ROW",source:"Independent84-signature root recovery",D1:D,D2:E,common_input:72,meet_rank:2,omitted_normal:q,foreign_support:L,foreign_real_rank:6,canonical_support:R.flatMap((_,i)=>c&bit(i)?[i]:[]),moved_sources:moved,unchanged_sources:111-moved.length,raw_mode_sizes:[D.length-1,E.length-1],canonical_rank:9,fitting_rank:10,fitting_quotient:1,separate_history_rank:11,separate_history_quotient:2,actual_carried_history_rank:4,charge:220,cubic_rank:84,punctured_mode_extensions:[85,85],sum_cubic:true,one_sided_separator_rejected:true,new_complete_kappa:false};
}

function reviewCoupledDirection(geo) {
 const R=geo.native_roots,need=(x,m)=>{if(!x)throw Error(m)},bit=i=>1n<<BigInt(i),dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0);
 const rk=rows=>{const b=new Map();for(let x of rows)while(x){const t=x&-x;if(b.has(t))x^=b.get(t);else{b.set(t,x);break;}}return b.size;};
 const K=R.map((r,i)=>R.reduce((x,s,j)=>i===j||dot(r,s)===0?x|bit(j):x,0n)),all=(1n<<111n)-1n;
 const z=K[92]&K[54]&K[38],zz=K[1]&K[18]&K[31],d=z^zz,cert=[];
 need(rk(K)===9&&rk(K.filter((_,i)=>i!==72))===9&&rk(K.concat(d))===10,"canonical ranks");
 for(let i=0;i<111;i++){const mask=all^K[i],c=K.map(x=>x&mask),r=rk(c),j=rk(c.concat(d&mask));
 need(r===8&&j===(i===72?8:9),"local quotient restriction "+i);
 cert.push({receiver:i,canonical_restriction_rank:r,extended_restriction_rank:j});}
 const L=[5,12,15,22,26,30,34,40,47,50,58,64,76,77,93,106],target=L.reduce((x,i)=>x|bit(i),bit(72)),H=K[72]^target;
 need(!(H&bit(72))&&!(H&~K[72])&&rk(K.concat(H,d))===10,"normalized local innovation");
 const tests=[];for(let mask=0;mask<16;mask++){const Z=[[mask&1,(mask>>1)&1],[(mask>>2)&1,(mask>>3)&1]],isI=mask===9,rankZ=rk(Z.map(r=>BigInt(r[0]|r[1]<<1)));let surviving=0;
 for(let j=0;j<111;j++)if(j!==72&&(K[72]&bit(j))){const h=Number(H>>BigInt(j)&1n);const M=Z.map((row,a)=>row.map((v,b)=>(+(a===b))^(h&v)));if(M.some(row=>row.some(Boolean)))surviving++;}
 need((surviving===16)===isI,"partial block deletion control");tests.push({mask,rank_Z:rankZ,total_fitting_rank:18+rankZ,receiver72_foreign_blocks:surviving,charge:isI?220:222});}
 return{status:"PASS_ROOT_COUPLED_DIRECTION_CLASSIFICATION",canonical_rank_without_receiver72:9,restriction_certificates:cert,only_noncanonical_receiver:72,all_field_block_family:"A_i=K_i tensor I for i!=72; A_72=K_72 tensor I+(K_72+target_72) tensor Z",rank_formula:"9V+rank(Z)",charge_dichotomy:"220 if Z=I;222 otherwise",width2_F2_controls:tests,new_complete_kappa:false};
}
function reviewD5Survivor(g){
 const R=g.native_roots,N=111,all=(1n<<111n)-1n,bit=i=>1n<<BigInt(i),dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),need=(x,s)=>{if(!x)throw Error(s)};
 function basis(rows){const m=new Map();for(let x of rows){while(x){const k=x.toString(2).length-1;if(m.has(k))x^=m.get(k);else{m.set(k,x);break}}}return[...m.values()]}
 function kernel(rows,mask){const m=new Map(),out=[];for(let row of rows){let x=row&mask,y=row;while(x){const k=x.toString(2).length-1;if(m.has(k)){const [u,v]=m.get(k);x^=u;y^=v}else{m.set(k,[x,y]);break}}if(!x&&y)out.push(y)}return basis(out)}
 const ids=x=>Array.from({length:N},(_,i)=>i).filter(i=>x&bit(i)),mask=xs=>xs.reduce((a,i)=>a|bit(i),0n);
 const K=R.map((r,i)=>mask(R.map((v,j)=>i===j||dot(r,v)===0?j:-1).filter(j=>j>=0))),C=basis(K),products=[];
 for(let i=0;i<C.length;i++)for(let j=i;j<C.length;j++)for(let k=j;k<C.length;k++)products.push(C[i]&C[j]&C[k]);const Q=basis(products);need(C.length===9&&Q.length===84,"canonical and cubic codes");
 const p=107,inv=x=>{let z=1;for(let i=0;i<p-2;i++)z=z*x%p;return z},rr=rows=>{const a=rows.map(r=>r.map(x=>(x%p+p)%p));let k=0;for(let j=0;j<(a[0]?.length||0)&&k<a.length;j++){let t=k;while(t<a.length&&!a[t][j])t++;if(t===a.length)continue;[a[k],a[t]]=[a[t],a[k]];const u=inv(a[k][j]);a[k]=a[k].map(x=>x*u%p);for(let l=k+1;l<a.length;l++){const c=a[l][j];if(c)a[l]=a[l].map((x,z)=>(x-c*a[k][z]%p+p)%p)}k++}return k};

 const D=R.map((r,i)=>[1,18,31].every(j=>dot(r,R[j])===0)?i:-1).filter(i=>i>=0),dm=mask(D),b=dm^bit(72);need(D.length===19&&rr(ids(b).map(i=>R[i]))===5,"second bank full support");
 const restrictions=[],fits=[];for(let i=0;i<N;i++){const forbidden=mask(R.map((r,j)=>j!==i&&dot(r,R[i])!==0&&!D.includes(j)?j:-1).filter(j=>j>=0));const rank=basis(C.map(x=>x&forbidden)).length;need(rank===8,"outside-D canonical restriction rank8");restrictions.push(rank);
 const row=(b&bit(i))?b:K[i]^b;let valid=!!(row&bit(i));for(const j of ids(row^bit(i)))if(dot(R[i],R[j])!==0)valid=false;if(valid)fits.push(i);
 }
 need(fits.join(",")==="1,18,31,35,49","only five fitting receivers");
 const proofs=[];for(const i of fits){const rows=ids((K[i]^b)^bit(i)).map(j=>R[j]),quad=rows.map(r=>{const a=[];for(let j=0;j<8;j++)for(let k=j;k<8;k++)a.push(r[j]*r[k]);return a});need(rr(rows)===7&&rr(quad)===28,"two-chart obstruction");proofs.push({receiver:i,foreign_sources:rows.length,linear_rank:7,quadratic_rank:28,charge:2})}
 return{status:"PASS_ROOT_SURVIVING_PACKET_GATE",prime:107,canonical_restriction_ranks:restrictions,possible_receivers:fits,forced_canonical:"G=K_i tensor I_V",proofs,scope:"Unchanged Q=G+bI_V only, every characteristic-two field and width, no noncommutativity restriction",new_kappa:false};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
 const read=(p,pin)=>{const raw=fs.readFileSync(p);if(crypto.createHash("sha256").update(raw).digest("hex")!==pin)throw Error("Source SHA256 mismatch: "+p);return JSON.parse(raw.toString("utf8"))};
 if(process.argv.length!==4)throw Error("Usage: node check.js FLAT-CUBIC-RESULT.json SOURCE-RECOVERY.json");
 const flat=read(process.argv[2],"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc"),geo=read(process.argv[3],"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e");
 console.log(JSON.stringify({geometry:reviewD5Pair(flat),direction:reviewCoupledDirection(geo),survivor:reviewD5Survivor(geo)},null,2));
}
