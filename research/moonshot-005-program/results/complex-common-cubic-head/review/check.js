
function reviewCommonA(){
 const need=(p,m)=>{if(!p)throw Error(m)},id={p:[0,1,2,3],q:[0,0,0,0]},key=g=>g.p.join("")+":"+g.q.join(""),same=(a,b)=>key(a)===key(b),prod=(a,b)=>({p:b.p.map(i=>a.p[i]),q:b.q.map((v,j)=>(v+a.q[b.p[j]])%4)}),power=(g,n)=>{let x=id;for(let j=0;j<(n%24+24)%24;j++)x=prod(g,x);return x},inv=g=>power(g,23),pc=v=>{let n=0;while(v){n^=1;v&=v-1}return n};
 const Q=v=>({p:[0,1,2,3],q:[0,1,2,3].map(k=>pc(v&k))}),a=Q(1),b=Q(2),c=Q(3),P={p:[0,3,1,2],q:[0,0,0,0]},Pi=power(P,2),A=prod(power(b,3),P),Ai=power(A,5);
 need(same(prod(prod(P,a),Pi),b)&&same(prod(prod(P,b),Pi),c),"actual dual-frequency three-cycle");
 need(same(power(A,6),id),"order6");const Z=prod(prod(power(a,3),power(b,3)),power(c,3));need(same(power(A,3),Z)&&same(power(Z,2),id),"cubic norm");
 const U=prod(power(b,2),c),Ui=power(U,3);need(same(prod(prod(U,power(P,2)),Ui),power(A,2)),"cyclic conjugacy");need(same(prod(prod(prod(U,Z),P),Ui),A),"full conjugacy");
 need(!same(prod(prod(c,power(P,2)),power(c,3)),power(A,2)),"translation omission control");
 const elt=(g,z=1)=>new Map([[key(g),{g,z}]]),zero=()=>new Map(),plus=(a,b,t=1)=>{const o=new Map(a);for(const[k,v]of b){const z=(o.get(k)?.z||0)+t*v.z;if(z)o.set(k,{g:v.g,z});else o.delete(k)}return o},left=(g,a)=>{const o=new Map();for(const v of a.values()){const h=prod(g,v.g),k=key(h),z=(o.get(k)?.z||0)+v.z;if(z)o.set(k,{g:h,z});else o.delete(k)}return o};
 const identity=()=>Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>i===j?elt(id):zero()));
 const ops=[["M",1,Pi],["M",3,Pi],["M",3,a],["ADD",3,2,-1],["M",2,b],["M",1,a],["ADD",0,1,1],["M",0,b],["M",0,Pi],["M",2,Pi]];
 const execute=(ops,start=identity())=>{const rows=start.map(r=>r.map(x=>new Map(x)));for(const op of ops){if(op[0]==="M")rows[op[1]]=rows[op[1]].map(x=>left(op[2],x));else rows[op[2]]=rows[op[2]].map((x,j)=>plus(x,rows[op[1]][j],op[3]));}return rows};
 const canonical=M=>M.map(r=>r.map(e=>[...e].map(([k,v])=>[k,v.z]).sort((x,y)=>x[0].localeCompare(y[0])))),equal=(a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));
 const expected=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>i===j?elt(Ai):i===1&&j===0?elt(id):i===2&&j===3?elt(power(A,4),-1):zero())),native=execute(ops);
 need(equal(native,expected),"literal all-column common interface");
 const rev=ops.slice().reverse().map(op=>op[0]==="ADD"?["ADD",op[1],op[2],-op[3]]:["M",op[1],inv(op[2])]);
 need(equal(execute(rev,native),identity())&&equal(execute(ops,execute(rev)),identity()),"both inverse compositions");

 const sign=[1,-1,-1,1],opposite=execute(rev).map((r,i)=>r.map((e,j)=>new Map([...e].map(([k,v])=>[k,{g:v.g,z:v.z*sign[i]*sign[j]}]))));
 const expOpp=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>i===j?elt(A):i===1&&j===0?elt(power(A,2)):i===2&&j===3?elt(id,-1):zero()));need(equal(opposite,expOpp),"opposite baseline");
 need(!equal(execute(ops.slice(1)),expected),"omitted boundary permutation control");
 const swap={p:[0,2,1,3],q:[0,0,0,0]};need(!same(power(prod(power(b,3),swap),3),Z),"involution is not three-cycle");
 const group=new Map([[key(id),id]]),queue=[id];for(let i=0;i<queue.length;i++)for(const g of[a,b,c,P,swap]){const h=prod(g,queue[i]);if(!group.has(key(h))){group.set(key(h),h);queue.push(h)}}need(group.size===192,"actual monomial head group");
 const phase=[[1,0],[0,1],[-1,0],[0,-1]],ranks=[];
 for(let k=0;k<6;k++){const g=power(A,k),M=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>{const z=[0,0];for(let v=0;v<4;v++){const s=pc(i&g.p[v])^pc(j&v)?-1:1;z[0]+=s*phase[g.q[v]][0];z[1]+=s*phase[g.q[v]][1]}return z}));
 const sizes=M.map(r=>r.filter(z=>z[0]||z[1]).length);need(sizes.every(s=>s===sizes[0]),"uniform support");const rank=Math.log2(sizes[0]);need(Number.isInteger(rank),"Gaussian support power");
 for(const r of M)for(const z of r)if(z[0]||z[1])need((z[0]*z[0]+z[1]*z[1])*sizes[0]===16,"Gaussian normalization");
 ranks.push(rank);}
 need(JSON.stringify(ranks)==="[0,1,2,2,2,1]","power ranks");
 const scale=10n**24n,roots={};for(const n of[2,7,8,23]){const N=BigInt(n)**199n*scale**200n;let lo=0n,hi=BigInt(n)*scale;while(hi-lo>1n){const mid=(lo+hi)/2n;if(mid**200n<=N)lo=mid;else hi=mid}need(lo**200n<=N&&hi**200n>N,"root bracket");roots[n]=[lo,hi];}
 const [l7,u7]=roots[7],[l8,u8]=roots[8],[l23,u23]=roots[23],[l2,u2]=roots[2],allow=[4n*l23-3n*scale-9n*u7-3n*u8,4n*u23-3n*scale-9n*l7-3n*l8],one=allow.map(x=>x-scale),two=[allow[0]-u2,allow[1]-l2];
 need(one[0]>0n&&two[1]<0n,"query budget signs");
 return{status:"PASS_INDEPENDENT_COMMON_CUBIC_INTERFACE",operator_model:"actual four-frequency permutation/phase monomials; symbolic group algebra retains all field sums",group_order:group.size,literal_public_columns:4,inverse_compositions:2,common_baseline_orientations:2,cubic_norm:"A^3=Z, A^6=I",Hilbert90_conjugacy:true,head_power_ranks:ranks,price:{t:"199/200",denominator:scale.toString(),allowance:allow.map(String),one_rank1_remaining:one.map(String),one_rank2_remaining:two.map(String),literal_profile:"4[1]+9[7]+3[8] ->4[23]",conditional_on_head_synthesis:true},negative_controls:{omitted_boundary_rejected:true,involution_cycle_rejected:true,omitted_translation_rejected:true},full120_linkage:false,head_circuit_constructed:false,no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewCommonA};
 if(require.main===module){
  const fs=require("node:fs"),crypto=require("node:crypto"),pins=["1bc214b889a5d9ecee6fa887966dd828a4aeee95b5584379e5d249d9ceddea01"];
  if(process.argv.length!==pins.length+2)throw Error("supply the authenticated input paths in README order");
  const raws=process.argv.slice(2).map(x=>fs.readFileSync(x));
  raws.forEach((b,i)=>{if(crypto.createHash("sha256").update(b).digest("hex")!==pins[i])throw Error("input SHA256 mismatch "+i)});
  process.stdout.write(JSON.stringify(reviewCommonA(),null,2)+"\n");
 }
}
