function reviewSingularSplit(flat){
 const fail=m=>{throw Error(m)},need=(b,m)=>{if(!b)fail(m)},dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),par=n=>{let a=0;while(n){a^=n&1;n>>=1}return a};
 const br=rows=>{const B=new Map();for(let x of rows){while(x){const j=x.toString(2).length-1;if(B.has(j))x^=B.get(j);else{B.set(j,x);break}}}return B.size};
 const sig=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 const map=Array.from({length:111},(_,i)=>sig.indexOf(flat.independent_generators.map(w=>+w.native_difference.includes(i)).join("")));need(new Set(map).size===111&&map.every(x=>x>=0),"authenticated84-signature source");
 const F=flat.full_roots,R=map.map(i=>F[i]),frame=[0,1,2,4,8,14,30,59],G=frame.map(i=>frame.reduce((a,j,k)=>a|((((dot(R[i],R[j])/2)%2+2)%2)<<k),0));
 const labels=new Map();for(let x=0;x<256;x++){const s=G.map(a=>par(a&x)).join("");need(!labels.has(s),"nondegenerate polar frame");labels.set(s,x)}
 const coords=F.map(r=>labels.get(frame.map(j=>((dot(r,R[j])/2)%2+2)%2).join(""))),X=map.map(i=>coords[i]);
 const q=x=>{let z=par(x);for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)z^=((x>>i)&(x>>j)&(G[i]>>j)&1);return z};
 const B=(x,y)=>G.reduce((z,a,i)=>z^((x>>i&1)*par(a&y)),0),s=38,h=x=>B(s,x);need(q(s)===0&&s!==0,"singular pivot");need(coords.every(x=>q(x)===1)&&new Set(coords).size===120,"full quadric");
 const bit=i=>1n<<BigInt(i),mask=ids=>ids.reduce((a,i)=>a|bit(i),0n),K=R.map((r,i)=>mask(R.map((v,j)=>j===i||dot(r,v)===0?j:-1).filter(j=>j>=0))),hm=mask(X.map((x,i)=>h(x)?i:-1).filter(i=>i>=0)),all=(1n<<111n)-1n;
 const A=K.map((k,i)=>k&(h(X[i])?hm:all^hm)),C0=K.filter((_,i)=>!h(X[i])),hC=K.map(k=>k&hm),hC0=C0.map(k=>k&hm);
 need(br(K)===9&&br(A)===15&&br([...K,...A])===16,"global ranks");need(br(C0)===8&&br(hC)===8&&br([...C0,...hC])===15,"code identity dimensions");need(br([...C0,...hC,...A])===15,"complete code equality");need(br(hC0)===7&&br([...C0,...hC0])===14,"proper quotient dimension");

 const p=107,inv=x=>{let y=1;for(let j=0;j<p-2;j++)y=y*x%p;return y},rr=rows=>{const a=rows.map(r=>r.map(x=>(x%p+p)%p));let k=0;for(let j=0;j<(a[0]?.length||0)&&k<a.length;j++){let t=k;while(t<a.length&&!a[t][j])t++;if(t===a.length)continue;[a[t],a[k]]=[a[k],a[t]];const u=inv(a[k][j]);a[k]=a[k].map(x=>x*u%p);for(let l=k+1;l<a.length;l++){const c=a[l][j];a[l]=a[l].map((x,z)=>(x-c*a[k][z]%p+p)%p)}k++}return k};
 const ids=m=>Array.from({length:111},(_,i)=>i).filter(i=>m&bit(i)),seeds=[1,3,5,10,30,61],modes=seeds.map(i=>K[i]&hm),ns=[1,3,5,10,11,15,30],omitted=[0,0,1,1,0,0,1,-1];
 need(br([...C0,...modes])===14&&br([...C0,...modes,K[0]&hm])===15,"six plus one");
 need(seeds.every(i=>!h(X[i])&&!(modes[seeds.indexOf(i)]&bit(i))),"local own zero");
 for(let j=0;j<6;j++)need(ids(modes[j]).every(i=>dot(R[i],R[seeds[j]])===0)&&rr(ids(modes[j]).map(i=>R[i]))===7,"actual facet mode");
 const kb=mask(R.map((r,i)=>dot(r,omitted)===0?i:-1).filter(i=>i>=0)),start=ns.map(i=>K[i]).concat([K[0]&hm]);
 need(br(start)===8&&br([...start,kb,...modes])===15,"eight seeds seven proper additions");need(rr(ids(kb).map(i=>R[i]))===7,"omitted normal facet");
 let chi=0;const one=[],covers=[];for(let i=0;i<111;i++){const supp=ids(A[i]^bit(i));need(A[i]&bit(i),"own coefficient");need(supp.every(j=>dot(R[i],R[j])===0),"fitting zeros");
 let parts,normal;if(!h(X[i])){const t=coords.indexOf(X[i]^s);need(t>=0&&dot(F[t],R[i])===0,"singular partner orthogonal");normal=F[t];parts=[supp.filter(j=>dot(R[j],normal)===0),supp.filter(j=>dot(R[j],normal)!==0)];need(parts[1].length<=1&&parts[1].every(j=>map[j]===t),"only partner exception")}
 else{normal=R[72];parts=[supp.filter(j=>dot(R[j],normal)===0),supp.filter(j=>dot(R[j],normal)!==0)];need(parts[1].every(j=>dot(R[j],omitted)===0),"second carrier cover")}
 const rank=rr(supp.map(j=>R[j]));need(rank===6||rank===7,"foreign support rank");need(parts.every(part=>rr(part.map(j=>R[j]))<=6),"proper cover ranks");if(rank===6)one.push(i);else chi++;
 covers.push({receiver:i,foreign: supp.length,rank,parts:parts.map(x=>x.length)});
 }
 need(chi===107&&one.join(",")==="26,35,72,77","exact proper cover charge");

 const can=r=>{const z=r.find(x=>x);return z<0?r.map(x=>-x):r},axesMap=new Map();for(let i=0;i<120;i++)if(!h(coords[i])){const j=coords.indexOf(coords[i]^s);for(const sign of[1,-1]){const a=can(F[i].map((x,k)=>x+sign*F[j][k]));axesMap.set(a.join(","),a)}}
 const axes=[...axesMap.values()];need(axes.length===8&&axes.every((a,i)=>axes.every((b,j)=>dot(a,b)===(i===j?8:0))),"D8 double axes");
 const ds=[],sp=[],parities=new Set();for(let i=0;i<120;i++){const v=axes.map(a=>dot(F[i],a));if(!h(coords[i])){need(v.filter(x=>x).length===2&&v.every(x=>x===0||Math.abs(x)===4),"D8 root coordinates");ds.push(v)}else{need(v.every(x=>Math.abs(x)===2),"half-spinor coordinates");parities.add(v.filter(x=>x<0).length%2);sp.push(v)}}
 need(ds.length===56&&sp.length===64&&parities.size===1,"full split line counts");const hist={};for(let i=0;i<111;i++){const c=modes.filter(m=>m&bit(i)).length;if(c)hist[c]=(hist[c]||0)+1}need(Object.entries(hist).filter(([k])=>+k>=2).reduce((a,[_,n])=>a+n,0)===53,"actual overlap53");
 need(BigInt(8)**199n*10n**200n>79n**200n&&BigInt(7)**199n*10n**200n>69n**200n,"exact endpoint price lower comparisons");
 const bad=K.map((k,i)=>k&(h(X[i])?all^hm:hm));need(bad.every((x,i)=>!(x&bit(i))),"cross-class negative control");
 return{status:"PASS_INDEPENDENT_SINGULAR_SPLIT",source:"84-signature native recovery, no author import",prime:p,global_rank:15,canonical_enlargement:16,code_dimensions:{Cs:8,hC:8,intersection:1,hCs:7,Cs_plus_hCs:14},native_class_sizes:[X.filter(x=>!h(x)).length,X.filter(h).length],global_charge:chi,one_chart_receivers:one,six_proper_modes:seeds,mode_supports:modes.map(x=>ids(x).length),shared_source_histogram:hist,alternative_seed_dimension:8,final_dimension:15,axes,full_block_line_counts:[ds.length,sp.length],halfspinor_sign_parity:[...parities][0],covers,negative_controls:{cross_class_own_blocks_all_zero:true,anisotropic_pivot92_excluded:q(X[92])===1},all_characteristic_two_fields_and_widths:"By binary rank stability, explicit fitting identity and tensoring; no complete source",new_kappa:false};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
 const read=(p,pin)=>{const raw=fs.readFileSync(p);if(crypto.createHash("sha256").update(raw).digest("hex")!==pin)throw Error("Source SHA256 mismatch: "+p);return JSON.parse(raw.toString("utf8"))};
 if(process.argv.length!==4)throw Error("Usage: node check.js FLAT-CUBIC-RESULT.json SOURCE-RECOVERY.json");
 const flat=read(process.argv[2],"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc"),geo=read(process.argv[3],"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e");
 console.log(JSON.stringify(reviewSingularSplit(flat),null,2));
}
