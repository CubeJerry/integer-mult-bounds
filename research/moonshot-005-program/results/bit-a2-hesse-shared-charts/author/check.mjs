// Exact source geometry. Caller authenticates the two pinned JSON input files.
export function checkA2Geometry(flat, quad) {
const need=(b,m)=>{if(!b)throw new Error(m);};
const pin="51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78";
need(flat.native_sha256===pin&&quad.source.source_sha256===pin,"inherited native source pin");
const F=flat.full_roots,Wit=flat.independent_generators,G=quad.source.binary_gram_rows,X=quad.source.binary_native_points;
need(F.length===120&&Wit.length===84&&X.length===111,"source dimensions");
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),pc=x=>{let n=0;while(x){x&=x-1;n++;}return n;};
const B=(x,y)=>G.reduce((s,r,i)=>s^((x>>i&1)?pc(r&y)&1:0),0);
function q(x){let z=pc(x)&1;for(let i=0;i<8;i++)if(x>>i&1)for(let j=i+1;j<8;j++)if(x>>j&1)z^=G[i]>>j&1;return z;}
const fs=F.map(()=>0n),ns=X.map(()=>0n);
Wit.forEach((w,j)=>{const A=new Set(w.full_frame0),D=new Set(w.full_frame1);need(A.size===8&&D.size===8&&[...A].filter(x=>D.has(x)).length===4,"adjacent frames");
for(const L of [w.full_frame0,w.full_frame1])for(let a=0;a<8;a++)for(let b=a+1;b<8;b++)need(!dot(F[L[a]],F[L[b]]),"frame orthogonality");
for(let i=0;i<120;i++)if(A.has(i)!==D.has(i))fs[i]|=1n<<BigInt(j);for(const i of w.native_difference)ns[i]|=1n<<BigInt(j);});
need(new Set(fs.map(String)).size===120&&new Set(ns.map(String)).size===111,"signature uniqueness");
const sig=new Map(fs.map((s,i)=>[String(s),i])),nativeToFull=ns.map(s=>sig.get(String(s)));
need(nativeToFull.every(Number.isInteger),"native signature recovery");const R=nativeToFull.map(i=>F[i]);
function solve(rows,rhs){let a=rows.map((r,i)=>r|(rhs[i]<<8)),at=0;for(let c=0;c<8;c++){let k=at;while(k<8&&!(a[k]>>c&1))k++;if(k===8)continue;[a[k],a[at]]=[a[at],a[k]];for(let j=0;j<8;j++)if(j!==at&&(a[j]>>c&1))a[j]^=a[at];at++;}need(at===8,"polar inverse");return a.reduce((s,r,i)=>s|((r>>8&1)<<i),0);}
const frame=quad.source.binary_frame_indices,labels=F.map(r=>solve(G,frame.map(i=>Math.abs(dot(r,R[i]))===2?1:0)));
need(new Set(labels).size===120&&labels.every(q)&&X.every((x,i)=>x===labels[nativeToFull[i]]),"full/native labels");
for(let i=0;i<120;i++)for(let j=0;j<120;j++)need(B(labels[i],labels[j])===(Math.abs(dot(F[i],F[j]))===2?1:0),"all polar pairings");
const RF=new Map(labels.map((x,i)=>[x,F[i]])),NI=new Map(X.map((x,i)=>[x,i]));
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}
function rank(rows){let A=rows.map(r=>r.map(BigInt)),at=0;for(let c=0;c<(A[0]?.length||0);c++){let k=at;while(k<A.length&&A[k][c]===0n)k++;if(k===A.length)continue;[A[k],A[at]]=[A[at],A[k]];for(let i=at+1;i<A.length;i++)if(A[i][c]!==0n){const p=A[at][c],t=A[i][c];A[i]=A[i].map((x,j)=>p*x-t*A[at][j]);let d=A[i].reduce((s,x)=>gcd(s,x),0n);if(d)A[i]=A[i].map(x=>x/d);}at++;}return at;}
function brank(rows){let P=new Map();for(let w of rows)while(w){let p=w.toString(2).length-1;if(P.has(p))w^=P.get(p);else{P.set(p,w);break;}}return P.size;}
const a=X[92],b=X[15],c=X[106],U=[a,b,c],ar=R[92],br=R[15].map(x=>-x),cr=R[106].map(x=>-x);
need((a^b^c)===0&&B(a,b)===1&&U.every(q),"binary A2");
need(ar.every((x,i)=>x+br[i]===cr[i])&&dot(ar,br)===-2,"real A2");
const T=[ar.map((x,i)=>-x-2*br[i]),ar.map((x,i)=>2*x+br[i]),ar.map((x,i)=>br[i]-x)],proj=x=>(B(x,b)?a:0)^(B(x,a)?b:0);
const E=Array.from({length:256},(_,x)=>x).filter(x=>!B(x,a)&&!B(x,b));
need(E.length===64&&E.filter(q).length===36,"minus E6");
const common=X.flatMap((x,i)=>proj(x)===0?[i]:[]),wings=U.map(u=>X.flatMap((x,i)=>proj(x)===u&&x!==u?[i]:[]));
need(common.length===32&&JSON.stringify(wings.map(x=>x.length))==="[25,25,26]","native classes");
const W=E.filter(x=>x&&!q(x)),triples=[];
for(const w of W){let V=null,oriented=[];for(let j=0;j<3;j++){let r=RF.get(w^U[j]),d=dot(r,T[j]);need(Math.abs(d)===4,"projection");r=r.map(x=>(d<0?-1:1)*x);let v=r.map((x,i)=>3*x-T[j][i]);need(!V||v.every((x,i)=>x===V[i]),"shared E6 weight");V=v;oriented.push(r);}
need(dot(V,V)===24&&!dot(V,ar)&&!dot(V,br)&&rank([ar,br,V])===3,"weight geometry");
triples.push({w,native_indices:U.map(u=>NI.get(w^u)??null),full_binary_labels:U.map(u=>w^u),oriented_roots:oriented,e6_projection_times_three:V});}
const TM=new Map(triples.map(t=>[t.w,t]));need(triples.length===27,"27 weights");
for(let i=0;i<27;i++)for(let j=i+1;j<27;j++)need([-12,6].includes(dot(triples[i].e6_projection_times_three,triples[j].e6_projection_times_three)),"distinct minuscule weight angles");
const qlines=[];for(let i=0;i<27;i++)for(let j=i+1;j<27;j++)if(!B(W[i],W[j])){let z=W[i]^W[j];need(TM.has(z),"GQ closure");let L=[W[i],W[j],z].sort((a,b)=>a-b);if(L[0]!==W[i]||L[1]!==W[j])continue;const V=L.map(w=>TM.get(w).e6_projection_times_three);need(V[0].every((_,i)=>V.reduce((s,v)=>s+v[i],0)===0)&&rank(V)===2,"zero-sum line");qlines.push(L);}
need(qlines.length===45&&W.every(w=>qlines.filter(L=>L.includes(w)).length===5),"GQ45 lines degree5");
const planes=[[196,45,233],[2,129,131],[14,116,122],[40,199,239]],axis=planes.map(P=>P.map(x=>NI.get(x)));
need(axis.flat().every(Number.isInteger),"12 native axes");
for(const P of planes)need((P[0]^P[1]^P[2])===0&&P.every(q)&&B(P[0],P[1])===1,"anisotropic plane");
for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)need(planes[i].every(x=>planes[j].every(y=>!B(x,y)))&&axis[i].every(x=>axis[j].every(y=>!dot(R[x],R[y]))),"orthogonal A2 planes");
const component=(x,P)=>(B(x,P[1])?P[0]:0)^(B(x,P[0])?P[1]:0);
const turn=x=>planes.slice(1).reduce((s,P)=>{const z=component(x,P),j=P.indexOf(z);return s^(j<0?0:P[(j+1)%3]);},0);
const seen=new Set(),cells=[];
for(const t of triples){if(seen.has(t.w))continue;const ws=[t.w,turn(t.w),turn(turn(t.w))].sort((a,b)=>a-b);need(new Set(ws).size===3&&(ws[0]^ws[1]^ws[2])===0&&ws.every(w=>TM.has(w)),"spread orbit");ws.forEach(w=>seen.add(w));
const vs=ws.map(w=>TM.get(w).e6_projection_times_three),native=ws.flatMap(w=>TM.get(w).native_indices.filter(i=>i!==null)).sort((a,b)=>a-b),basis=[ar,br,...vs.slice(0,2)];
need(rank(basis)===4&&rank(native.map(i=>R[i]))===4,"D4 ranks");
const fullSources=ws.flatMap(w=>U.map(u=>w^u)),fullInside=labels.filter((x,i)=>rank(basis.concat([F[i]]))===4);
need(fullInside.length===12&&fullInside.every(x=>U.includes(x)||fullSources.includes(x)),"exact D4 root set");
const facets=R.flatMap((r,i)=>basis.every(v=>!dot(r,v))?[i]:[]);
const groupCharts=U.map((u,j)=>{const C=ws.map(w=>RF.get(w^u)),sources=ws.map(w=>TM.get(w).native_indices[j]).filter(i=>i!==null);
need(rank(C)===3&&sources.length>=1,"nonempty source group");for(let s=0;s<3;s++)for(let t=s+1;t<3;t++)need(!dot(C[s],C[t]),"orthogonal group");
const access=R.flatMap((r,i)=>C.every(v=>!dot(r,v))?[i]:[]);need(access.length===facets.length+1&&access.includes(axis[0][j])&&facets.every(i=>access.includes(i)),"exact cache access");
return{carrier:axis[0][j],native_sources:sources,full_real_basis:C,containing_receiver_facets:access};});
cells.push({id:cells.length,weights:ws,native_wing_sources:native,real_basis:basis,containing_receiver_facets:facets,group_cache_charts:groupCharts});}
need(cells.length===9&&seen.size===27&&new Set(cells.flatMap(C=>C.native_wing_sources)).size===76,"cell partition");
const hesse=[],hist={};let negative=null;
for(let i=0;i<9;i++)for(let j=i+1;j<9;j++){need(rank(cells[i].real_basis.concat(cells[j].real_basis))===6,"pair rank6");for(let k=j+1;k<9;k++){const basis=cells[i].real_basis.concat(cells[j].real_basis,cells[k].real_basis),r=rank(basis);hist[r]=(hist[r]||0)+1;if(r===8&&!negative)negative=[i,j,k];if(r===6){const normals=labels.filter((x,s)=>basis.every(v=>!dot(F[s],v)));need(normals.length===3&&(normals[0]^normals[1]^normals[2])===0&&normals.every(x=>proj(x)===0),"A2 normal triple");hesse.push({cells:[i,j,k],full_normal_binary_labels:normals,native_normal_roles:normals.flatMap(x=>NI.has(x)?[NI.get(x)]:[]).sort((a,b)=>a-b),native_sources:[...new Set([i,j,k].flatMap(c=>cells[c].native_wing_sources))].sort((a,b)=>a-b)});}}}
need(hesse.length===12&&hist[6]===12&&hist[8]===72,"Hesse rank census");
for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)need(hesse.filter(L=>L.cells.includes(i)&&L.cells.includes(j)).length===1,"Steiner pairs");
need(new Set(hesse.flatMap(L=>L.full_normal_binary_labels)).size===36&&new Set(hesse.flatMap(L=>L.native_normal_roles)).size===32,"common-root normal partition");
const parallel=[];for(let i=0;i<12;i++){const P=[i,...hesse.flatMap((L,j)=>L.cells.every(c=>!hesse[i].cells.includes(c))?[j]:[])].sort((a,b)=>a-b);need(P.length===3&&new Set(P.flatMap(j=>hesse[j].cells)).size===9,"parallel partition");if(!parallel.some(A=>JSON.stringify(A)===JSON.stringify(P)))parallel.push(P);}need(parallel.length===4,"four parallel classes");
const cubes=[];for(let omitted=0;omitted<4;omitted++){const full=labels.filter(x=>component(x,planes[omitted])===0&&planes.filter(P=>component(x,P)!==0).length===3);need(full.length===27,"cube cardinality");const indices=full.map(x=>labels.indexOf(x)),K=indices.map(i=>indices.reduce((m,j,k)=>m|(BigInt(i===j||dot(F[i],F[j])===0)<<BigInt(k)),0n));need(brank(K)===7&&rank(indices.map(i=>F[i]))===6,"cube ranks");for(let z=0;z<27;z++){const foreign=indices.filter((i,k)=>k!==z&&((K[z]>>BigInt(k))&1n));need(foreign.length===12&&rank(foreign.map(i=>F[i]))===5,"cube foreign rank5");}const native=full.flatMap(x=>NI.has(x)?[NI.get(x)]:[]).sort((a,b)=>a-b);cubes.push({omitted_plane:omitted,full_binary_labels:full,native_indices:native,full_count:27,native_count:native.length,real_rank:6,canonical_restriction_rank:7,foreign_full_real_rank:5});}
need(JSON.stringify(cubes.map(C=>C.native_count))==="[23,25,25,26]"&&negative!==null,"native cube and Hub controls");
const multiplicities={};for(const t of triples){let n=t.native_indices.filter(x=>x!==null).length;multiplicities[n]=(multiplicities[n]||0)+1;}
return{status:"PASS_AUTHOR_A2_E6_D4_HESSE_SHARED_GEOMETRY",source_native_sha256:pin,admitted_flat_certificate_path:"research/moonshot-005-program/results/bit-proper-flat-cubic-generators/author/RESULT.json",admitted_flat_certificate_sha256:"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc",source_qualification:"Native roots independently recovered from84 admitted frame-difference signatures; no fresh gzip replay.",rank_method:"Exact fraction-free BigInt elimination with integer gcd normalization.",native_to_full:nativeToFull,carrier_roles:[92,15,106],carrier_binary_labels:U,carrier_real_roots:[R[92],R[15],R[106]],real_relation:"r92 = r15 - r106",common_native_indices:common,wing_native_indices:wings,full_partition:[36,27,27,27,3],native_partition:[32,25,25,26,3],e6_minuscule_triples:triples,native_triple_multiplicity_histogram:multiplicities,gq_lines:qlines,four_anisotropic_planes:planes,native_axis_triples:axis,cells,pair_union_rank:6,triple_union_rank_histogram:hist,hesse_lines:hesse,parallel_classes:parallel,ternary_cubes:cubes,acquired_cache_prefix:{classification:"No-point-copy restored control; future entry capacity at least76V into the wing downset union. The retained-point live acquisition is separate.",cache_count:27,independent_cache_modes:27,wing_sources_restored:76,other_original_sources_unchanged:35,outputs_completed:0,INIT:27,ADD:76,MOVE:152,move_profile:{"2":76,"5":76},cache_chart_rank:3,downward_moves:0,complete_source:false},negative_controls:{noncollinear_three_cell_union_rank8:negative,all_source_triples_present:false,no_cached_cell_mode_readable_by_a_wing_receiver:true},complete_supplier:false,new_complete_kappa:false};
}
