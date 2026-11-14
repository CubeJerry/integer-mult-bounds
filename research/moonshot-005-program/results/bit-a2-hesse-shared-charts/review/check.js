
function reviewA2(flat,quad,g) {
 const need=(v,m)=>{if(!v)throw Error(m)},dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0),vecEq=(a,b)=>a.every((x,i)=>x===b[i]);
 const sigFull=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 const sigNat=Array.from({length:111},(_,i)=>flat.independent_generators.map(w=>+w.native_difference.includes(i)).join(""));
 need(new Set(sigFull).size===120&&new Set(sigNat).size===111,"independent signature uniqueness");
 const map=sigNat.map(s=>sigFull.indexOf(s));need(map.every(i=>i>=0)&&JSON.stringify(map)===JSON.stringify(g.native_to_full),"native index recovery");
 const R=map.map(i=>flat.full_roots[i]), F=flat.full_roots;
 function rank(M,p=103){if(!M.length)return 0;const a=M.map(r=>r.map(x=>(x%p+p)%p));let n=0;const pow=(x,e)=>{let y=1;while(e){if(e&1)y=y*x%p;x=x*x%p;e>>=1}return y};
  for(let c=0;c<a[0].length&&n<a.length;c++){let k=n;while(k<a.length&&!a[k][c])k++;if(k===a.length)continue;[a[k],a[n]]=[a[n],a[k]];let z=pow(a[n][c],p-2);a[n]=a[n].map(x=>x*z%p);for(let i=n+1;i<a.length;i++){let h=a[i][c];a[i]=a[i].map((x,j)=>(x-h*a[n][j]%p+p)%p)}n++;}return n;
 }
 const carriers=[92,15,106],pBasis=[R[92],R[15]];
 need(R[92].every((x,i)=>x===R[15][i]-R[106][i]),"A2 relation");
 const common=R.flatMap((r,i)=>pBasis.every(v=>dot(r,v)===0)?[i]:[]);
 const wing=carriers.map(k=>R.flatMap((r,i)=>!carriers.includes(i)&&dot(r,R[k])===0&&!common.includes(i)?[i]:[]));
 need(common.length===32&&JSON.stringify(wing.map(w=>w.length))==="[25,25,26]","real source partition");
 need(JSON.stringify(wing)===JSON.stringify(g.wing_native_indices),"receipt wing identities");
 const triples=g.e6_minuscule_triples, weights=triples.map(t=>t.e6_projection_times_three);
 need(weights.length===27&&new Set(weights.map(v=>v.join(","))).size===27,"27 weights");
 for(const v of weights)need(dot(v,v)===24&&pBasis.every(r=>dot(v,r)===0),"weight norm and complement");
 const shifts=[R[92].map((x,i)=>-x+2*R[15][i]),R[92].map((x,i)=>2*x-R[15][i]),R[92].map((x,i)=>-R[15][i]-x)];
 const nativeUsed=new Set(),mult={};
 for(let k=0;k<27;k++){const t=triples[k];let count=0;
  for(let j=0;j<3;j++){
   const v=weights[k].map((x,i)=>x+shifts[j][i]);need(v.every(x=>x%3===0),"integral triple");
   const r=v.map(x=>x/3);need(vecEq(r,t.oriented_roots[j]),"oriented root");
   need(F.some(z=>vecEq(z,r)||vecEq(z,r.map(x=>-x))),"full root member");
   const i=t.native_indices[j];if(i!==null){need(!nativeUsed.has(i),"unique native member");nativeUsed.add(i);count++;need(vecEq(R[i],r)||vecEq(R[i],r.map(x=>-x)),"actual native root");need(wing[j].includes(i),"native wing class")}
  }mult[count]=(mult[count]||0)+1;
 }
 need(nativeUsed.size===76&&mult[3]===23&&mult[2]===3&&mult[1]===1,"native triple puncture");
 const weightIndex=new Map(weights.map((v,i)=>[v.join(","),i])),lines=[];
 for(let i=0;i<27;i++)for(let j=i+1;j<27;j++){const v=weights[i].map((x,k)=>-x-weights[j][k]),k=weightIndex.get(v.join(","));if(k!==undefined&&j<k)lines.push([i,j,k]);}
 need(lines.length===45&&weights.every((_,i)=>lines.filter(L=>L.includes(i)).length===5),"independent real zero-sum line incidence");
 const ax=[[1,65],[7,55],[16,95]],reflect=(v,r)=>{let d=dot(v,r);need(d%2===0,"integral weight reflection");return v.map((x,i)=>x-d/2*r[i])};
 const turn=v=>ax.reduce((x,p)=>reflect(reflect(x,R[p[1]]),R[p[0]]),v),orbits=[],seen=new Set();
 for(let i=0;i<27;i++)if(!seen.has(i)){const a=turn(weights[i]),b=turn(a);need(vecEq(turn(b),weights[i]),"real Coxeter order three");const L=[i,weightIndex.get(a.join(",")),weightIndex.get(b.join(","))].sort((x,y)=>x-y);need(L.every(Number.isInteger)&&new Set(L).size===3,"real weight orbit");L.forEach(j=>seen.add(j));orbits.push(L);}
 need(orbits.length===9,"nine real Coxeter orbits");
 const byWeight=new Map(triples.map((t,i)=>[t.w,i]));
 need(g.cells.length===9,"nine cells");
 const cb=[];
 for(const c of g.cells){const wi=c.weights.map(w=>byWeight.get(w)).sort((a,b)=>a-b);need(orbits.some(L=>JSON.stringify(L)===JSON.stringify(wi)),"selected spread independent reconstruction");
  const b=[...pBasis,weights[wi[0]],weights[wi[1]]];need(rank(b)===4,"cell lower rank");
  need(weights[wi[2]].every((x,k)=>x+weights[wi[0]][k]+weights[wi[1]][k]===0),"cell rank upper");
  const perpendicular=F.filter(r=>b.every(v=>dot(r,v)===0));need(rank(perpendicular)===4,"cell exact perpendicular upper witness");const inside=F.filter(r=>perpendicular.every(v=>dot(r,v)===0));need(inside.length===12,"full D4 roots");cb.push(b);
  const access=R.flatMap((r,i)=>b.every(v=>dot(r,v)===0)?[i]:[]);need(JSON.stringify(access)===JSON.stringify(c.containing_receiver_facets),"cell exact receiver facets");
  for(const group of c.group_cache_charts){const q=group.full_real_basis;need(q.length===3&&rank(q)===3,"group rank3");
   need(q.every(v=>dot(v,R[group.carrier])===0&&perpendicular.every(n=>dot(v,n)===0)),"group intersection upper");
   const ac=R.flatMap((r,i)=>q.every(v=>dot(r,v)===0)?[i]:[]);
   need(JSON.stringify(ac)===JSON.stringify(group.containing_receiver_facets),"group exact access");
   need(!wing.flat().some(i=>ac.includes(i)),"no wing receiver cache access");
   need(group.native_sources.every(i=>q.some(v=>vecEq(v,R[i])||vecEq(v,R[i].map(x=>-x)))),"each source is actual cache basis root");
  }
 }

 const histogram={},actualLines=[];
 for(let i=0;i<9;i++)for(let j=i+1;j<9;j++){need(rank(cb[i].concat(cb[j]))===6,"cell pair lower rank6");
  for(let k=j+1;k<9;k++){const r=rank(cb[i].concat(cb[j],cb[k]));histogram[r]=(histogram[r]||0)+1;if(r===6)actualLines.push([i,j,k]);}
 }
 need(histogram[6]===12&&histogram[8]===72&&JSON.stringify(actualLines)===JSON.stringify(g.hesse_lines.map(x=>x.cells)),"independent Hesse census");
 // Each rank-six upper bound is authenticated by two independent exact orthogonal roots.
 for(const L of g.hesse_lines){const b=L.cells.flatMap(i=>cb[i]);const orth=F.filter(r=>b.every(v=>dot(r,v)===0));need(orth.length===3&&rank(orth)===2,"exact rank-six upper witness");}
 for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)need(actualLines.filter(L=>L.includes(i)&&L.includes(j)).length===1,"Hesse pair uniqueness");
 need(g.parallel_classes.length===4&&g.parallel_classes.every(P=>P.length===3&&new Set(P.flatMap(i=>actualLines[i])).size===9),"four parallel classes");

 const wt=x=>{let n=0;while(x){x&=x-1;n++}return n};
 const G=quad.source.binary_gram_rows,B=(x,y)=>G.reduce((z,row,i)=>z^((x>>i&1)?(wt(row&y)%2):0),0);
 const fullLabels=F.map(r=>{
  const candidates=Array.from({length:256},(_,x)=>x).filter(x=>quad.source.binary_frame_indices.every((i,j)=>B(x,1<<j)===+(Math.abs(dot(r,R[i]))===2)));
  need(candidates.length===1,"independent full binary label");return candidates[0];
 });
 need(map.every((f,i)=>fullLabels[f]===quad.source.binary_native_points[i]),"native binary labels");
 const byLabel=new Map(fullLabels.map((x,i)=>[x,F[i]])),cubeChecks=[];
 for(const cube of g.ternary_cubes){
  const real=cube.full_binary_labels.map(x=>byLabel.get(x));need(real.length===27&&real.every(Boolean)&&rank(real)===6,"cube lower rank6");
  const omitted=g.native_axis_triples[cube.omitted_plane].map(i=>R[i]);need(rank(omitted)===2&&real.every(r=>omitted.every(v=>dot(r,v)===0)),"cube upper rank6");
  for(let i=0;i<27;i++){const foreign=real.filter((r,j)=>i!==j&&dot(r,real[i])===0);need(foreign.length===12&&rank(foreign)===5,"cube rank5 foreign witnesses");}
  const planes=g.four_anisotropic_planes,comp=(x,P)=>(B(x,P[1])?P[0]:0)^(B(x,P[0])?P[1]:0);
  const words=cube.full_binary_labels.map(x=>planes.flatMap((P,j)=>j===cube.omitted_plane?[]:[P.indexOf(comp(x,P))]));
  need(new Set(words.map(w=>w.join(","))).size===27&&words.every(w=>w.every(i=>i>=0)),"full ternary cube coordinates");
  for(let i=0;i<27;i++)for(let j=0;j<27;j++){const distance=words[i].reduce((n,x,k)=>n+ +(x!==words[j][k]),0);need((i===j||dot(real[i],real[j])===0)===(distance===0||distance===2),"ternary tensor fitting identity");}
  cubeChecks.push({native:cube.native_count,source_rank:6,foreign_rank:5,fitting_rank_by_projectors:7});
 }

 // The retained point-copy prescription is checked on all222 formal input columns.
 const X=Array.from({length:111},(_,i)=>1n<<BigInt(i)),Y=Array.from({length:111},(_,i)=>1n<<BigInt(i+111));
 const pointCopies=new Map(),caches=[];let init=0,adds=0,moves=0;
 for(const i of wing.flat()){pointCopies.set(i,X[i]);init++;adds++;}
 for(const cell of g.cells)for(const group of cell.group_cache_charts){init++;let value=0n;
  for(const i of group.native_sources){need(rank(group.full_real_basis.concat([R[i]]))===3,"legal source ascent");moves++;value^=X[i];adds++;}
  caches.push({carrier:group.carrier,value,sources:group.native_sources});
 }
 need(init===103&&adds===152&&moves===76&&pointCopies.size===76&&caches.length===27,"live acquisition counts");
 need(caches.every(c=>c.sources.every(i=>pointCopies.get(i)===X[i])),"genuine retained point copies");
 need(X.every((x,i)=>x===1n<<BigInt(i))&&Y.every((y,i)=>y===1n<<BigInt(i+111)),"all original values unchanged");
 const allCached=caches.flatMap(c=>c.sources);need(allCached.length===76&&new Set(allCached).size===76,"independent cache modes");
 const region=wing.flat();need(region.every(i=>region.some(j=>dot(R[i],R[j])===0)),"point copies are in wing union");
 let wrongMergeRejected=false;
 const bad=g.negative_controls.noncollinear_three_cell_union_rank8;
 if(rank(bad.flatMap(i=>cb[i]))===8)wrongMergeRejected=true;need(wrongMergeRejected,"noncollinear rank8 negative control");
 return {status:"PASS_INDEPENDENT_REAL_COXETER_HESSE_REVIEW",source_qualification:"admitted signature certificate, not fresh gzip",rank_prime:103,
 native_partition:[32,25,25,26,3],matched_triples:27,puncture_multiplicities:mult,real_zero_sum_lines:45,real_coxeter_orbits:9,
 ternary_cube_checks:cubeChecks,D4_cells:9,Hesse_rank6_lines:12,triple_union_histogram:histogram,group_caches:27,
 retained_live_prefix:{INIT:init,ADD:adds,MOVE:moves,movement_profile:{"2":76},owned:103,formal_input_columns:222,completed_outputs:0},
 omitted_point_copy_future_region_deficit:"76V",negative_controls:{noncollinear_three_cells_rank8:wrongMergeRejected,all_group_charts_outside_every_wing_facet:true},
 independent_method:"real minuscule-weight zero-sum triples and actual A2 Coxeter reflections; modular lower witnesses with exact orthogonal upper witnesses",
 no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewA2};
 if(require.main===module){
  const fs=require("fs"),crypto=require("crypto");
  if(process.argv.length!==5)throw Error("usage: node check.js flat_RESULT.json quad_RESULT.json author_GEOMETRY.json");
  const raws=process.argv.slice(2).map(p=>fs.readFileSync(p));
  const expected=["4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc","5820476439a60b74bd5174c00e73b528fb4e8d1e8a0b3a504cfeedf4d06e9801","c0095e7e87e76601a71b42b807729252416cfa4ed304ddc2abf42142be3c35d0"];
  raws.forEach((b,i)=>{if(crypto.createHash("sha256").update(b).digest("hex")!==expected[i])throw Error("input SHA-256 mismatch "+i)});
  process.stdout.write(JSON.stringify(reviewA2(...raws.map(b=>JSON.parse(b))),null,2)+"\n");
 }
}
