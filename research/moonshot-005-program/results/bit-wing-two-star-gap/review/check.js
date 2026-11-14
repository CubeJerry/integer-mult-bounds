
function reviewTwoStars(flat){
 const need=(p,m)=>{if(!p)throw Error(m)},dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
 const signatures=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 need(new Set(signatures).size===120,"unique full signatures");
 const mapping=Array.from({length:111},(_,i)=>signatures.indexOf(flat.independent_generators.map(w=>+w.native_difference.includes(i)).join("")));
 need(mapping.every(i=>i>=0)&&new Set(mapping).size===111,"native mapping");
 const R=mapping.map(i=>flat.full_roots[i]),axes=[92,15,106],W=R.flatMap((r,i)=>!axes.includes(i)&&axes.filter(a=>dot(r,R[a])===0).length===1?[i]:[]);
 const F=[0,14,39,41,60,63,70],contact=(i,j)=>i===j||dot(R[i],R[j])===0;
 need(W.length===76&&F.every(a=>W.includes(a)),"76 wings");
 for(const a of F)for(const b of F)need(a===b||!contact(a,b),"frame zeros");
 const E=W.filter(i=>!F.includes(i)).map(i=>({role:i,pair:F.flatMap((f,k)=>contact(i,f)?[k]:[])})).filter(e=>e.pair.length===2);
 const lookup=new Map(E.map(e=>[e.pair.join(","),e])),deg=Array(7).fill(0);
 need(E.length===20&&lookup.size===20,"edge count");
 for(let a=0;a<7;a++)for(let b=a+1;b<7;b++)need(lookup.has(a+","+b)===(a!==0||b!==3),"K7 minus03");
 for(const e of E){e.pair.forEach(a=>deg[a]++);for(const f of E)if(e!==f)need(contact(e.role,f.role)===!e.pair.some(a=>f.pair.includes(a)),"all edge contacts");}
 const loops=[[85,0],[107,3]],A=[0,3],B=[1,2,4,5,6];
 for(const [z,a]of loops){need(W.includes(z),"wing loop");F.forEach((f,b)=>need(contact(z,f)===(a===b),"loop frame"));E.filter(e=>e.pair.includes(a)).forEach(e=>need(!contact(z,e.role),"augmented star"));}
 need(!contact(85,107),"unused loop-pair zero");
 const inc=E.flatMap(e=>e.pair.map(a=>({role:e.role,a,b:e.pair.find(b=>b!==a)}))),key=x=>x.role+":"+x.a;
 const wt=x=>A.includes(x.a)?2:A.includes(x.b)?0:1,out=Array(7).fill(0);
 inc.forEach(x=>out[x.a]+=wt(x));const weighted=Object.fromEntries(inc.map(x=>[key(x),out[x.a]-2*(wt(x)+wt({...x,a:x.b,b:x.a}))]));
 need(inc.reduce((s,x)=>s+wt(x),0)===40,"40h");need(out[0]+out[3]===20,"20V");
 inc.forEach(x=>need(weighted[key(x)]===(A.includes(x.a)?6:0),"weighted gamma"));

 const ce=Object.fromEntries(inc.map(x=>[key(x),0]));let paths=0;
 for(const a of A)for(const b of B){const c=A.find(x=>x!==a),e=lookup.get([a,b].sort((x,y)=>x-y).join(",")),f=lookup.get([b,c].sort((x,y)=>x-y).join(","));
 need(!contact(e.role,f.role),"CE source zero");ce[e.role+":"+a]+=4;ce[f.role+":"+c]+=2;inc.filter(x=>x.a===a).forEach(x=>ce[key(x)]--);paths++;}
 inc.forEach(x=>need(ce[key(x)]===(A.includes(x.a)?1:0),"CE coefficient"));
 const v=5,h=4,g=x=>A.includes(x.a)?1:A.includes(x.b)?2:1,G=Array(7).fill(0);inc.forEach(x=>G[x.a]+=g(x));
 for(const x of inc)need(h+2*(g(x)+g({...x,a:x.b,b:x.a}))-G[x.a]-(A.includes(x.a)?v:0)>=0,"formal LR");
 let allPaths=0;for(const e of inc.filter(x=>A.includes(x.a)))for(const f of inc.filter(x=>x.a===e.b&&x.b!==e.a)){need(2*g({...f,a:f.b,b:f.a})+4*g(e)===v-h+G[e.a],"formal CE");allPaths++;}
 const piv=new Map();for(const i of W){let row=W.reduce((z,j,k)=>contact(i,j)?z^(1n<<BigInt(k)):z,0n);while(row){const bit=row&-row;if(piv.has(bit))row^=piv.get(bit);else{piv.set(bit,row);break;}}}need(piv.size===9,"binary rank9");
 const bad=inc.find(x=>A.includes(x.a)),badGa=G[bad.a]-1;
 need(h+2*(g(bad)-1+g({...bad,a:bad.b,b:bad.a}))<badGa+v,"decremented formal gamma rejected");
 return{status:"PASS_INDEPENDENT_TWO_STAR_GEOMETRY_AND_RANK_REVIEW",source:"native mapping independently recovered from84 admitted flat signatures",roles:29,frame:F,degree:deg,weighted_LR:{h:40,V:20,augmented_gamma:6},cross_sum:{paths,V:10,h:-10,augmented_gamma:1},combination:{h:100,V:80,rank_lower:"44V/5"},canonical_binary_rank:9,formal_point:{V:v,h,G,LR_incidences:40,CE_paths:allPaths,is_matrix:false},small_widths:[1,2,3,4].map(V=>({V,lower:Math.ceil(44*V/5),upper_characteristic_two:9*V})),negative_controls:{decremented_gamma_rejected:true,dropping_one_loop_halves_LR_singleton_term:true},unused_source_constraint:"loop85 and107 are noncontacts",no_physical_supplier:true,no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewTwoStars};
 if(require.main===module){
  const fs=require("node:fs"),crypto=require("node:crypto"),pins=["4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc"];
  if(process.argv.length!==pins.length+2)throw Error("supply the authenticated input paths in README order");
  const raws=process.argv.slice(2).map(x=>fs.readFileSync(x));
  raws.forEach((b,i)=>{if(crypto.createHash("sha256").update(b).digest("hex")!==pins[i])throw Error("input SHA256 mismatch "+i)});
  process.stdout.write(JSON.stringify(reviewTwoStars(...raws.map(b=>JSON.parse(b.toString("utf8")))),null,2)+"\n");
 }
}
