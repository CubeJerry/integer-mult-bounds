/* Fresh independent D4 proof core; no Node or external dependencies. */
(function(){
function buildIndependentD4Catalogue(){
 const need=(x,m)=>{if(!x)throw new Error(m)};
 const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
 const span=rows=>{let a=[0];for(const r of rows){a=[...new Set([...a,...a.map(x=>x^r)])]}return a.sort((a,b)=>a-b)};
 const normals=Array.from({length:512},(_,i)=>i).filter(x=>[3,7].includes(pop(x)));
 const roots=normals.map(v=>{if(pop(v)===3)return Array.from({length:9},(_,i)=>(v>>i&1)?2:-1);const missing=Array.from({length:9},(_,i)=>i).filter(i=>!(v>>i&1));return Array.from({length:9},(_,i)=>3*((i===missing[0]?1:0)-(i===missing[1]?1:0)))});
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 const gram=roots.map(a=>roots.map(b=>dot(a,b)));
 need(normals.length===120,"full root domain");
 need(gram.every((row,i)=>row[i]===18&&row.every((x,j)=>j===i||[0,-9,9].includes(x))),"Q9 inner products");
 const catalog=new Map(), counts={4:0,12:0}, xorClass={four_zero:0,four_nonzero:0,twelve_zero:0,twelve_nonzero:0};
 let frames=0;
 for(let i=0;i<120;i++)for(let j=i+1;j<120;j++){if(gram[i][j])continue;
  for(let k=j+1;k<120;k++){if(gram[i][k]||gram[j][k])continue;
   for(let l=k+1;l<120;l++){if(gram[i][l]||gram[j][l]||gram[k][l])continue;
    const F=[i,j,k,l];frames++;
    const members=[];
    for(let q=0;q<120;q++)if(F.reduce((v,r)=>v+gram[q][r]**2,0)===324)members.push(q);
    need(members.length===4||members.length===12,"real span type");
    counts[members.length]++;const xor=F.reduce((v,r)=>v^normals[r],0);
    xorClass[(members.length===4?"four":"twelve")+"_"+(xor===0?"zero":"nonzero")]++;
    if(members.length===12){
     need(xor===0,"complete D4/XOR correspondence");
     const patterns=new Set(members.filter(x=>!F.includes(x)).map(q=>{const row=F.map(r=>gram[q][r]/9);need(row.every(x=>Math.abs(x)===1),"half sign roots");return row.map(x=>x*row[0]).join(",")}));
     need(patterns.size===8,"all eight projective sign patterns");
     const key=members.join(",");if(!catalog.has(key))catalog.set(key,{normals:members.map(r=>normals[r]),families_normals:[]});
     catalog.get(key).families_normals.push(F.map(r=>normals[r]));
    }else need(xor!==0,"four-root spans have nonzero XOR");
   }
  }
 }
 const records=[...catalog.values()];
 for(const row of records){
  const fs=row.families_normals;need(fs.length===3&&new Set(fs.flat()).size===12,"three complete disjoint families");
  const spaces=fs.map(span);need(spaces.every(s=>s.length===8),"binary dimension three");
  for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){
   const join=span([...fs[i],...fs[j]]),k=3-i-j;
   need(join.length===16&&fs[j].every(x=>!spaces[i].includes(x)),"binary pair dimension four");
   need(join.every(x=>fs[k].every(y=>pop(x&y)%2===0)),"third family facet containment");
  }
  const total=span(fs.flat());need(total.length===32&&total.includes(511),"total binary dimension five and characteristic vector");
 }
 need(frames===122850&&counts[12]===9450&&counts[4]===113400&&records.length===3150,"complete independent census");
 return {source:"Fresh independent pure-JS reconstruction; not recovered filesystem bytes.",normal_model:"all nine-bit weight3/7; Q9 norm18",all_normals:normals,all_orthogonal_quadruples:frames,span_counts:counts,xor_classification:xorClass,D4_count:records.length,records};
}
function certifyIndependentD4Cover(catalogue){
 const need=(x,m)=>{if(!x)throw new Error(m)};
 const omitted=[7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491];
 const coupled=[81,273,262,98,290,268,164,280];
 const excluded=new Set([...omitted,...coupled]);need(excluded.size===24,"disjoint published exclusions");
 const nativeOrder=[];
 for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)for(let k=j+1;k<9;k++)nativeOrder.push((1<<i)|(1<<j)|(1<<k));
 for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)nativeOrder.push(511^(1<<i)^(1<<j));
 need(nativeOrder.length===120&&new Set(nativeOrder).size===120&&nativeOrder.every(x=>catalogue.all_normals.includes(x)),"complete explicit normal order");
 const H=nativeOrder.filter(x=>!excluded.has(x)), hs=new Set(H), index=new Map(H.map((n,i)=>[n,i]));
 need(H.length===96,"actual hosted normal count");
 const records=catalogue.records.map(r=>({...r,hosted_normals:r.normals.filter(x=>hs.has(x)).sort((a,b)=>index.get(a)-index.get(b))}));
 const full=records.filter(r=>r.hosted_normals.length===12);
 const toMask=values=>values.reduce((m,n)=>m|(1n<<BigInt(index.get(n))),0n);
 const fullMasks=full.map(r=>toMask(r.hosted_normals));
 const bybit=H.map((_,i)=>fullMasks.filter(m=>(m>>BigInt(i))&1n));
 const bits=function*(m){while(m){const z=m&-m;yield z.toString(2).length-1;m-=z}};
 const everything=(1n<<96n)-1n;
 const pivot=H.reduce((best,h)=>bybit[index.get(h)].length<bybit[index.get(best)].length?h:best,H[0]);
 const firstChoices=[];
 for(const chosen of bybit[index.get(pivot)]){
  const stranded=H.find(h=>!((chosen>>BigInt(index.get(h)))&1n)&&bybit[index.get(h)].every(m=>(m&chosen)!==0n));
  need(stranded!==undefined,"each first full block strands an uncovered host");
  firstChoices.push({chosen:[...bits(chosen)].map(i=>H[i]),stranded,all_stranded_blocks:bybit[index.get(stranded)].map(m=>({block:[...bits(m)].map(i=>H[i]),intersection:[...bits(m&chosen)].map(i=>H[i])}))});
 }
 need(firstChoices.length===3,"three exhaustive first choices");
 const elevenMap=new Map();
 for(const r of records){
  if(r.hosted_normals.length===11){const m=toMask(r.hosted_normals);elevenMap.set(m.toString(),m)}
  if(r.hosted_normals.length===12){const m=toMask(r.hosted_normals);for(const h of r.hosted_normals){const z=m^(1n<<BigInt(index.get(h)));elevenMap.set(z.toString(),z)}}
 }
 const elevens=[...elevenMap.values()].sort((a,b)=>a<b?-1:a>b?1:0);
 let nodes=0,singletonCases=0;const strandedHistogram={}, initialCertificates=[];
 function finish(rem){
  nodes++;if(rem===0n)return true;
  let choices=null;
  for(const i of bits(rem)){const c=bybit[i].filter(m=>(m&rem)===m);if(choices===null||c.length<choices.length)choices=c;if(c.length===0)return false}
  return choices.some(m=>finish(rem^m));
 }
 for(const eleven of elevens){
  const rem=everything^eleven;
  const stranded=[...bits(rem)].filter(i=>!bybit[i].some(m=>(m&rem)===m));
  strandedHistogram[stranded.length]=(strandedHistogram[stranded.length]||0)+1;
  if(stranded.length>1){initialCertificates.push({eleven:eleven.toString(16),two_stranded:stranded.slice(0,2).map(i=>H[i])});continue}
  const possibilities=stranded.length?stranded:[...bits(rem)];
  for(const singleton of possibilities){singletonCases++;need(!finish(rem^(1n<<BigInt(singleton))),"no rank33-shape cover exists")}
 }
 const hostedHistogram={};for(const r of records)hostedHistogram[r.hosted_normals.length]=(hostedHistogram[r.hosted_normals.length]||0)+1;
 need(full.length===90&&elevens.length===1686&&singletonCases===1073,"complete source cases agree independently");
 need((strandedHistogram[0]||0)===12&&(strandedHistogram[1]||0)===53&&initialCertificates.length===1621,"all eleven-subset domain accounted");
 return {status:"PASS_FRESH_JS_D4_RANK_AT_LEAST_34",provenance:"Fresh pure-JS reconstruction using explicit published omitted/coupled normal lists; not recovered old filesystem bytes.",omitted,coupled,hosted_normal_order:H,hosted_size_histogram:hostedHistogram,full_hosted_blocks:full.length,no_eight_full_cover:{pivot_normal:pivot,first_choices:firstChoices},rank33_shape:{eleven_subsets:elevens.length,at_least_two_initial_stranded:initialCertificates.length,stranded_histogram:strandedHistogram,singleton_cases:singletonCases,DFS_nodes:nodes,cover_exists:false,two_stranded_certificates:initialCertificates},minimum_total_block_rank:34,mathematical_density:"A D4 subset of rank1,2,3,4 has size at most1,3,6,12. Rank32 forces8full blocks; rank33 forces7full12+one11+one singleton.",scope:"Independent total block-rank accounting on a partition of these96 hosted roots into D4 subsets; not a lower bound on the rank of an overlapping joint code."};
}
function certifyD4Budget(invoice,nativeRaw,rankLower=34){
 const need=(x,m)=>{if(!x)throw new Error(m)};
 const precision=160,den=1n<<160n,cache=new Map();
 function power(rank){
  if(cache.has(rank))return cache.get(rank);
  const r=BigInt(rank),target=(r**199n)*(den**200n);let lo=0n,hi=r*den+1n;
  while(hi-lo>1n){const m=(lo+hi)>>1n;if(m**200n<=target)lo=m;else hi=m}
  need(lo**200n<=target&&(lo+1n)**200n>target,"exact power bracket");
  const out=[lo,lo**200n===target?lo:lo+1n];cache.set(rank,out);return out;
 }
 function interval(coeff){
  let lo=0n,hi=0n;
  for(const [key,v] of Object.entries(coeff)){const c=BigInt(v);if(!c)continue;const [l,h]=power(Number(key));lo+=c*(c>=0n?l:h);hi+=c*(c>=0n?h:l)}
  return [lo,hi];
 }
 const exact=[1,2,3,4,5,6,7].reduce((s,r)=>s+r*(nativeRaw[r]||0),0);
 need(exact===3200,"all native raw rank mass");
 const paid={...invoice.P4};
 for(const [r,n]of Object.entries(nativeRaw))paid[r]=(paid[r]||0)-18*n;
 paid[8]=(paid[8]||0)+7200;paid[9]=(paid[9]||0)+144;paid[1]=(paid[1]||0)+144;
 const head={};for(const r of new Set([...Object.keys(paid),...Object.keys(invoice.T4)]))head[r]=(invoice.T4[r]||0)-(paid[r]||0);
 const headInt=interval(head),delta=interval({1:2,2:1,3:1,4:1,5:1,8:-2}),beta=interval({1:2,2:2,5:2,8:-2});
 need(delta[0]>0n&&6n*delta[1]<den&&beta[0]>0n&&6n*beta[1]<den,"monotone rank-plus-refinement bounds");
 const shape=[];
 for(let a=0;a<=4;a++)for(let b=0;b<=4;b++)for(let c=0;c<=4;c++){const s=a+b+c;if(s<9)continue;const large=[a,b,c].filter(x=>x>=3).reduce((q,x)=>q+x,0);need(large>=3*(s-8),"dense-family port bound");shape.push({sizes:[a,b,c],large,minimum:3*(s-8)})}
 const base={1:1,2:1,5:1};
 function legCheck(ranks){
  const c={};for(const r of ranks)c[r]=(c[r]||0)+1;for(const [r,v]of Object.entries(base))c[r]=(c[r]||0)-v;
  need(interval(c)[0]>=0n,"ambient-chart exact leg bound");
 }
 for(let own=3;own<=5;own++)for(let join=own+1;join<=8;join++)legCheck([own-1,join-own,9-join]);
 for(let join=4;join<=6;join++)for(let first=1;first<join;first++)legCheck([first,join-first,8-join]);
 const coefficient=3*(96-2*rankLower);
 const floor=delta.map(x=>BigInt(rankLower)*den+BigInt(coefficient)*x),ambient=beta.map(x=>BigInt(rankLower)*den+BigInt(coefficient)*x);
 const lateOwned={9:2,8:-1,7:-1,1:-1},lateRaw={1:104,5:2,6:24,7:50,8:-76},lateNet={};
 for(const r of new Set([...Object.keys(lateOwned),...Object.keys(lateRaw)]))lateNet[r]=(lateOwned[r]||0)-(lateRaw[r]||0);
 const saving=interval(lateNet),actualHead=[headInt[0]+18n*saving[0],headInt[1]+18n*saving[1]];
 need(18n*ambient[0]>actualHead[1],"ambient block price exceeds complete implemented late-two headroom");
 const onlyOwned=interval(lateOwned);
 need(18n*ambient[1]<headInt[0]+18n*onlyOwned[0],"negative control: omitting mandatory forward raw cost would falsely remove this obstruction");
 const pack=(x,d=den)=>({lower_numerator:x[0].toString(),upper_numerator:x[1].toString(),denominator:d.toString(),approx:Number(x[0])/Number(d)});
 return {status:"PASS_FRESH_JS_D4_BLOCKWISE_BUDGET",precision_bits:precision,rankLower,native_raw_histogram:nativeRaw,invoice_git_blob:"8f369f208313c4c8a8c591e9527f2b6585565eba",invoice_source_commit:"1f21379ca624a40c44edbe616000c00cabcafe81",delta:pack(delta),ambient_delta:pack(beta),minimal_chart_floor:pack(floor),ambient_chart_floor:pack(ambient),original_forward_headroom:pack(headInt,18n*den),implemented_late_two_saving:pack(saving),implemented_late_two_headroom:pack(actualHead,18n*den),ambient_original_gap:pack([18n*ambient[0]-headInt[1],18n*ambient[1]-headInt[0]],18n*den),ambient_late_two_gap:pack([18n*ambient[0]-actualHead[1],18n*ambient[1]-actualHead[0]],18n*den),family_shapes:shape,late_owned_saving:lateOwned,mandatory_late_first_bank_raw:lateRaw,negative_control_omit_late_raw_rejected:true,scope:"Independent D4 block return rank plus cyclic family-chart routes. Original8rank9+8coupled or the exact implemented late-two forward tariff only; larger complete headroom/new shared current-row codes remain outside this obstruction.",native_bridge_status:"Explicit native raw histogram recovered from pre-outage source output; root will separately bind it and hosted normals to the pinned native gzip. No old artifact byte recovery claimed."};
}
function bindNativeD4Source(native,catalogue,cover){
 const need=(x,m)=>{if(!x)throw new Error(m)};
 const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
 const span=rows=>{let s=[0];for(const v of rows)s=[...new Set([...s,...s.map(x=>x^v)])];return s};
 const nOf=h=>{const row=native.frames[native.initial[h]];need(row.length===1,"native source root line");return row[0]};
 const liveNormals=native.live.map(nOf),hostedRoles=native.hosted.Dports.map(i=>native.live[i]),hostedNormals=hostedRoles.map(nOf);
 const eq=(a,b)=>JSON.stringify([...a].sort((x,y)=>x-y))===JSON.stringify([...b].sort((x,y)=>x-y));
 need(native.live.length===104&&hostedRoles.length===96,"native104/96 port counts");
 need(eq(hostedNormals,cover.hosted_normal_order),"fresh hosted normals exactly native");
 const liveSet=new Set(liveNormals),hostedSet=new Set(hostedNormals);
 need(eq(catalogue.all_normals.filter(n=>!liveSet.has(n)),cover.omitted),"all16 omitted normals native-bound");
 need(eq(liveNormals.filter(n=>!hostedSet.has(n)),cover.coupled),"all8 coupled normals native-bound");
 for(let i=0;i<hostedRoles.length;i++){
  const x=hostedRoles[i],b=native.hosted.X2[i],d=native.hosted.Y2[i],normal=nOf(x);
  need(nOf(b)===normal&&native.frames[native.initial[d]].length===0,"genuine hosted dual source charts");
  const facet=native.frames[native.final[d]];
  need(facet.length===8&&span(facet).length===256&&facet.every(v=>pop(v&normal)%2===0),"actual native final receiver facet");
 }
 const privateRoles=new Set([...native.live,...native.live.map(x=>x+112),...native.hosted.X2,...native.hosted.Y2]);
 need(privateRoles.size===400,"four independent physical private banks");
 const histogram={};
 for(const e of native.program)if(e[0]==="MOVE"&&privateRoles.has(e[1])){const r=Math.abs(native.frames[e[3]].length-native.frames[e[2]].length);histogram[r]=(histogram[r]||0)+1}
 const expected={1:990,2:360,3:105,4:112,5:133,6:8,7:2};
 need(JSON.stringify(Object.entries(histogram).sort((a,b)=>Number(a[0])-Number(b[0])))===JSON.stringify(Object.entries(expected)),"all native raw histogram entries independently bound");
 return {status:"PASS_FRESH_NATIVE_SOURCE_BINDING",native_hosted_count:hostedNormals.length,native_live_count:liveNormals.length,omitted:cover.omitted,coupled:cover.coupled,native_raw_histogram:histogram,all_hosted_initial_lines_and_final_facets_checked:true};
}
return {buildIndependentD4Catalogue,certifyIndependentD4Cover,certifyD4Budget,bindNativeD4Source};
})()
