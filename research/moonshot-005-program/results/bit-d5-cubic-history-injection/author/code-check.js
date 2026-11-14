function checkD5CubicCode(geometry) {
 const R=geometry.native_roots,n=111,dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0),key=v=>{const t=v.find(x=>x!==0);return(t<0?v.map(x=>-x):v).join(",");};
 const axes=[[1,0,1,0,1,-2,-1,0],[1,0,1,0,-1,0,1,-2],[1,0,-1,-2,-1,0,-1,0],[1,2,-1,0,1,0,1,0],[1,-2,-1,0,1,0,1,0]],lookup=new Map(R.map((r,i)=>[key(r),i])),D=R.map((_,i)=>i).filter(i=>[92,54,38].every(j=>dot(R[i],R[j])===0));
 for(let i=0;i<5;i++)for(let j=0;j<5;j++)if(dot(axes[i],axes[j])!==(i===j?8:0))throw Error("D5 axes");
 const edges=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){const roots=[1,-1].map(s=>axes[i].map((x,k)=>(x+s*axes[j][k])/2));edges.push({edge:[i,j],root_vectors:roots,native_roles:roots.map(r=>lookup.get(key(r))??null)});}
 const found=edges.flatMap(e=>e.native_roles.filter(x=>x!==null)).sort((a,b)=>a-b);if(JSON.stringify(found)!==JSON.stringify(D)||D.length!==18)throw Error("D5 native section");
 const basis=rows=>{const p=new Map(),b=[];for(let v of rows){let x=v;while(x){const k=x.toString(2).length-1;if(p.has(k))x^=p.get(k);else{p.set(k,x);b.push(x);break;}}}return b;};
 const K=R.map((a,i)=>R.reduce((v,b,j)=>v|((i===j||dot(a,b)===0)?1n<<BigInt(j):0n),0n)),C=basis(K),pairs=[],triples=[];for(let i=0;i<C.length;i++)for(let j=i;j<C.length;j++){pairs.push(C[i]&C[j]);for(let k=j;k<C.length;k++)triples.push(C[i]&C[j]&C[k]);}
 const Q2=basis(pairs),Q3=basis(triples),dmask=D.reduce((x,i)=>x|(1n<<BigInt(i)),0n),outside=((1n<<111n)-1n)^dmask,projected=basis(Q3.map(x=>x&outside));
 const words=[];for(let m=0;m<1024;m++){const deg=Array(5).fill(0);let w=0,z=0n;for(let k=0;k<10;k++)if((m>>k)&1){w++;for(const v of edges[k].edge)deg[v]^=1;for(const i of edges[k].native_roles)if(i!==null)z|=1n<<BigInt(i);}if(w%2===0&&deg.every(v=>v===0)){const support=D.filter(i=>(z>>BigInt(i))&1n);words.push({edge_mask:m,edge_count:w,hex:z.toString(16),support,weight:support.length,carrier_coefficient:Number((z>>1n)&1n),outside_base_inputs:support.filter(i=>![92,36,54,38,55,23,1,18].includes(i))});}}
 const local=basis(words.map(w=>BigInt("0x"+w.hex))),s={canonical_rank:C.length,quadratic_rank:Q2.length,cubic_rank:Q3.length,outside_D_cubic_rank:projected.length,local_rank:local.length,quadratic_plus_local_rank:basis([...Q2,...local]).length};
 if(JSON.stringify(s)!==JSON.stringify({canonical_rank:9,quadratic_rank:36,cubic_rank:84,outside_D_cubic_rank:79,local_rank:5,quadratic_plus_local_rank:41}))throw Error("code ranks");
 if(words.length!==32||basis([...Q3,...local]).length!==84||words.some(w=>((BigInt("0x"+w.hex)>>1n)&1n)!==((BigInt("0x"+w.hex)>>18n)&1n)))throw Error("code equality/carrier");
 const nonzero=words.filter(w=>w.edge_mask),weight_histogram={};for(const w of nonzero)weight_histogram[w.weight]=(weight_histogram[w.weight]||0)+1;
 return{status:"PASS",section:"D=F92 intersect F54 intersect F38",native_source_roles:D,double_axes:axes,edge_map:edges,punctured_sign_edges:edges.filter(e=>e.native_roles.includes(null)).map(e=>e.edge),rank_certificate:s,canonical_basis_hex:C.map(x=>x.toString(16)),quadratic_basis_hex:Q2.map(x=>x.toString(16)),cubic_basis_hex:Q3.map(x=>x.toString(16)),outside_D_echelon_hex:projected.map(x=>x.toString(16)),local_basis_hex:local.map(x=>x.toString(16)),all_even_Eulerian_words:words,nonzero_weight_histogram:weight_histogram,carrier_pair:[1,18],carrier_edge:[3,4]};
}

if(typeof module!=="undefined")module.exports={checkD5CubicCode};
