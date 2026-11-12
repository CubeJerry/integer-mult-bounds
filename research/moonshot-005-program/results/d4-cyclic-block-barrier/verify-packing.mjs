import {readFileSync} from "node:fs";
function verifyD4FullPacking(catalogue){
 const require=(v,m)=>{if(!v)throw Error(m);};
 const excluded=new Set([7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491,81,273,262,98,290,268,164,280]);
 const wt=n=>{let k=0;for(;n;n>>=1)k+=n&1;return k;};
 const hosted=Array.from({length:512},(_,n)=>n).filter(n=>(wt(n)===3||wt(n)===7)&&!excluded.has(n)), H=new Set(hosted);
 require(hosted.length===96,"hosted inventory");const records=Array.isArray(catalogue)?catalogue:catalogue.records;
 require(records.length===3150,"complete D4 catalogue");
 const full=records.filter(r=>r.normals.every(n=>H.has(n))).map(r=>r.normals.slice().sort((a,b)=>a-b)).sort((a,b)=>{for(let i=0;i<12;i++)if(a[i]!==b[i])return a[i]-b[i];return 0;});
 require(full.length===90&&new Set(full.map(x=>x.join(","))).size===90,"ninety distinct full hosted blocks");
 const masks=full.map(a=>a.reduce((m,n)=>m|(1n<<BigInt(hosted.indexOf(n))),0n));
 const tuples=[[]], counts=[1], maximal=[];
 function visit(ids,available){if(!available.length)maximal.push(ids.slice());for(let k=0;k<available.length;k++){const i=available[k], next=[...ids,i];counts[next.length]=(counts[next.length]||0)+1;tuples.push(next);visit(next,available.slice(k+1).filter(j=>(masks[i]&masks[j])===0n));}}
 visit([],masks.map((_,i)=>i));require(JSON.stringify(counts)==="[1,90,847,604,43]","complete packing census");
 for(const t of tuples){let mask=0n;for(const i of t){require((mask&masks[i])===0n,"tuple disjoint");mask|=masks[i];}}
 const density=[];
 for(let R=0;R<=35;R++){let max=-1,best=[];for(let a=0;4*a<=R;a++)for(let b=0;4*a+3*b<=R;b++)for(let c=0;4*a+3*b+2*c<=R;c++){const d=R-4*a-3*b-2*c, s=11*a+Math.min(4,a)+6*b+3*c+d;if(s>max){max=s;best=[[a,b,c,d]];}else if(s===max)best.push([a,b,c,d]);}density.push({R,max_size:max,rank4_rank3_rank2_rank1_counts:best});}
 require(density.slice(0,35).every(x=>x.max_size<=95),"rank at most34 cannot cover96");
 return {status:"PASS_INDEPENDENT_D4_MAXIMUM_FULL_PACKING_FOUR",method:"Independent exhaustive increasing-index set-packing enumeration over the complete Q9 D4 catalogue.",hosted_normals:hosted,full_block_count:full.length,all_disjoint_packings_by_size:counts,total_nodes:tuples.length,maximal_packing_counts:maximal.reduce((o,t)=>(o[t.length]=(o[t.length]||0)+1,o),{}),maximum_full_packing:4,minimum_total_rank:35,relaxed_density:density.filter(x=>x.R>=32),full_blocks:full,all_packings:tuples,one_maximum_witness:tuples.find(x=>x.length===4).map(i=>full[i]),scope:"Partition of exactly96 hosted source root directions into subsets of the complete D4 catalogue; no shared joint-return rank or unrestricted physical-code lower bound."};
}
const input=JSON.parse(readFileSync(process.argv[2]||"CATALOGUE.json","utf8"));
console.log(JSON.stringify(verifyD4FullPacking(input),null,2));
