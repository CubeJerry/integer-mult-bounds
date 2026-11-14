
function reviewWing(flat,receipt){
 const need=(b,m)=>{if(!b)throw Error(m)},dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
 const fSig=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 const nSig=Array.from({length:111},(_,i)=>flat.independent_generators.map(w=>+w.native_difference.includes(i)).join(""));
 need(new Set(fSig).size===120,"full signatures");const mapping=nSig.map(s=>fSig.indexOf(s));need(mapping.every(i=>i>=0)&&new Set(mapping).size===111,"native recovery");
 const R=mapping.map(i=>flat.full_roots[i]),ax=[92,15,106],W=R.flatMap((r,i)=>!ax.includes(i)&&ax.filter(j=>dot(r,R[j])===0).length===1?[i]:[]);
 need(W.length===76&&JSON.stringify(W)===JSON.stringify(receipt.wing_roles),"wing set");
 const F=receipt.frame;need(F.length===7&&F.every(i=>W.includes(i)),"frame");
 for(let a=0;a<7;a++)for(let b=0;b<a;b++)need(dot(R[F[a]],R[F[b]])!==0,"independent point blocks");
 const E=receipt.edges,deg=Array(7).fill(0),pairs=new Set();
 for(const e of E){need(W.includes(e.role)&&!F.includes(e.role),"edge role");
 const contacts=F.flatMap((f,a)=>dot(R[e.role],R[f])===0?[a]:[]);need(JSON.stringify(contacts)===JSON.stringify(e.endpoints),"actual point-edge mask");
 const key=contacts.join(",");need(contacts.length===2&&!pairs.has(key),"simple edge graph");pairs.add(key);contacts.forEach(a=>deg[a]++);}
 need(E.length===19&&deg.every(d=>d>4)&&JSON.stringify(deg)===JSON.stringify(receipt.degree),"high-degree seed");
 for(let i=0;i<E.length;i++)for(let j=0;j<i;j++){const shared=E[i].endpoints.some(a=>E[j].endpoints.includes(a));need((dot(R[E[i].role],R[E[j].role])!==0)===shared,"star contact mask");}
 const vectors=new Map(F.map((r,a)=>[r,1<<a]));E.forEach(e=>vectors.set(e.role,128|(1<<e.endpoints[0])|(1<<e.endpoints[1])));
 const anchor=receipt.noncontact_witness_roles.map(r=>vectors.get(r));need(anchor.length===7&&anchor.every(Number.isInteger),"anchor labels");
 const parity=x=>{let n=0;for(;x;x&=x-1)n^=1;return n};
 const annihilator=Array.from({length:255},(_,i)=>i+1).filter(x=>anchor.every(a=>parity(a&x)===0));need(annihilator.length===1&&annihilator[0]===15&&parity(15)===0,"unique isotropic annihilator");
 need(receipt.extra_role===3&&W.includes(3)&&receipt.noncontact_witness_roles.every(r=>dot(R[3],R[r])!==0),"actual extra-role zeros");

 const rankBig=rows=>{const pivot=new Map();let rank=0;for(let x of rows){for(let i=0;x&&i<111;i++)if(x>>BigInt(i)&1n){if(pivot.has(i))x^=pivot.get(i);else{pivot.set(i,x);rank++;break}}}return rank};
 const rows=W.map(i=>W.reduce((v,j,k)=>v|((i===j||dot(R[i],R[j])===0)?1n<<BigInt(k):0n),0n));need(rankBig(rows)===9,"canonical rank9");
 const loops=receipt.augmented_star_loop_roles;
 for(const z of loops){need(W.includes(z.role),"loop in wing");need(F.every((f,a)=>(dot(R[z.role],R[f])===0)===(a===z.point)),"singleton point contact");need(E.filter(e=>e.endpoints.includes(z.point)).every(e=>dot(R[z.role],R[e.role])!==0),"loop zero blocks");}
 need(dot(R[3],R[F[0]])===0,"wrong anchor is not prescribed zero");
 const deleted=Array.from({length:256},(_,i)=>i).filter(x=>anchor.slice(1).every(a=>parity(a&x)===0));need(deleted.length===4,"deleting anchor enlarges annihilator");
 return{status:"PASS_INDEPENDENT_WING_SEED_AND_ISOTROPIC_REVIEW",derived_source:"admitted84 flat witnesses, no fresh gzip",seed_roles:26,strict_obstruction_roles:27,quantitative_augmented_seed_roles:28,frame:F,degree:deg,anchor_rank:7,annihilator:15,canonical_rank:9,source_loop_roles:loops,negative_controls:{deleted_anchor_nullity:2,frame0_not_zero_constraint:true},universal_statement:"characteristic2, every V>=1: rank>8V via admitted saturated-star normalization and isotropic extension",no_universal_9V_claim:true,no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewWing};
 if(require.main===module){
  const fs=require("fs"),crypto=require("crypto"),expected=["4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc","342550e3df984e7a4e08a84f11e44739c7b6e5d6802aee17291f5378bb0ecd7c"];
  if(process.argv.length!==expected.length+2)throw Error("supply the authenticated input JSON paths in documented order");
  const raws=process.argv.slice(2).map(p=>fs.readFileSync(p));
  raws.forEach((b,i)=>{if(crypto.createHash("sha256").update(b).digest("hex")!==expected[i])throw Error("input SHA-256 mismatch "+i)});
  process.stdout.write(JSON.stringify(reviewWing(...raws.map(b=>JSON.parse(b))),null,2)+"\n");
 }
}
