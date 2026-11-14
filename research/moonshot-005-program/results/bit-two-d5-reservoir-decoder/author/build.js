function buildTwoD5Word(geometry,closed=false) {
 const R=geometry.native_roots,n=111,charts={zero:{kind:"span",rows:[]},Hub:{kind:"ann",rows:[]}},operations=[],markers={};
 for(let i=0;i<n;i++){charts["L"+i]={kind:"span",rows:[R[i]],source_roles:[i]};charts["F"+i]={kind:"ann",rows:[R[i]],normal_roles:[i]};}
 const D1=[1,10,11,18,23,27,31,35,41,49,57,61,65,72,73,80,89,110],D2=[3,7,16,21,38,39,53,54,67,68,71,72,81,84,85,88,92,104,108],L=[5,12,15,22,26,30,34,40,47,50,58,64,76,77,93,106],a=D1.filter(i=>i!==72),b=D2.filter(i=>i!==72),c=[...new Set([...a,...b,72,...L])].sort((u,v)=>u-v);
 const dot=(x,y)=>x.reduce((s,v,k)=>s+v*y[k],0),g=R.map((r,i)=>i===92||dot(r,R[92])===0?i:-1).filter(i=>i>=0),sources=[...new Set([...c,...g])].sort((u,v)=>u-v),points=sources.filter(i=>i!==72);
 const mask=ids=>ids.reduce((v,i)=>v^(1n<<BigInt(i)),0n),hex=ids=>mask(ids).toString(16),xor=(u,v)=>[...new Set([...u,...v])].filter(i=>u.includes(i)!==v.includes(i)).sort((x,y)=>x-y);
 charts.D1={kind:"ann",rows:[R[92],R[54],R[38]],normal_roles:[92,54,38]};
 charts.D2={kind:"ann",rows:[R[1],R[18],R[31]],normal_roles:[1,18,31]};
 charts.I={kind:"ann",rows:[R[92],R[54],R[38],R[1],R[18],R[31]],normal_roles:[92,54,38,1,18,31]};
 charts.E={kind:"ann",rows:[R[72],[0,0,1,1,0,0,1,-1]]};
 const op=(...x)=>operations.push(x);
 op("INIT","A","D1");op("INIT","B","D2");op("INIT","F","E");
 for(const i of sources){
  if(i!==72){op("INIT","R"+i,"L"+i);op("ADD","X"+i,"R"+i);}
  let chart,cache;if(a.includes(i)){chart="D1";cache="A";}else if(b.includes(i)){chart="D2";cache="B";}else if(L.includes(i)){chart="E";cache="F";}
  if(chart){op("MOVE","X"+i,chart);op("ADD","X"+i,cache);}
  op("MOVE","X"+i,"Hub");
 }
 markers.acquired_local_modes=operations.length;
 op("INIT","P","Hub");op("INIT","Q","Hub");
 for(const i of xor(c,g))op("ADD","X"+i,"P");
 for(const i of g)op("ADD","X"+i,"Q");
 markers.loaded_canonical_pair=operations.length;
 op("MOVE","P","D1");op("ADD","A","P");
 op("MOVE","Q","D2");op("ADD","B","Q");
 op("MOVE","P","I");op("MOVE","Q","I");op("ADD","Q","P");
 markers.coupled_at_intersection=operations.length;
 op("MOVE","P","zero");op("MOVE","Q","zero");
 op("ADD","P","Y72");op("MOVE","Y72","E");op("ADD","F","Y72");op("MOVE","Y72","F72");op("CLEAR","F");
 markers.decoded_row72=operations.length;
 const expected_owned_roles=Object.fromEntries(points.map(i=>["R"+i,{chart:"L"+i,value:hex([i])}]));
 expected_owned_roles.A={chart:"D1",value:hex(a)};expected_owned_roles.B={chart:"D2",value:hex(b)};
 expected_owned_roles.P={chart:"zero",value:hex([72,...L])};expected_owned_roles.Q={chart:"zero",value:hex(xor(g,b))};
 if(closed){for(const role of Object.keys(expected_owned_roles))op("CLEAR",role);for(let i=0;i<n;i++){if(!sources.includes(i))op("MOVE","X"+i,"Hub");if(i!==72)op("MOVE","Y"+i,"F"+i);}}
 return {format:"literal-monotone-linear-word-v1",construction:"coupled-two-D5-local-reservoirs",coefficient_field:"F2",charts,operations,targets:[72],completed_targets:[72],moved_original_sources:sources,closed_partial:closed,markers,live_owned_expected:closed?0:Object.keys(expected_owned_roles).length,expected_owned_roles:closed?{}:expected_owned_roles,source_partition:{a,b,foreign:L,own:[72],canonical_c:c,canonical_background:g,all_moved:sources,retained_point_copies:points},scope:"Exact one-receiver decoder and retained mixed global mode; no complete111-target supplier."};
}
