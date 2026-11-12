const closure=(function(){
const need=(x,m)=>{if(!x)throw Error(m)},pc=x=>{let n=0;while(x){n++;x&=x-1;}return n};
const normals=Array.from({length:512},(_,i)=>i).filter(n=>pc(n)===3||pc(n)===7);
const root=n=>{if(pc(n)===3)return Array.from({length:8},(_,j)=>n&256?((n>>j&1)?2:0):((n>>j&1)?1:-1));const miss=Array.from({length:9},(_,j)=>j).filter(j=>!(n>>j&1));return Array.from({length:8},(_,j)=>miss[1]===8?(j===miss[0]?1:-1):2*((j===miss[0]?1:0)-(j===miss[1]?1:0)));};
const canon=v=>{const sign=v.find(x=>x!==0)>0?1:-1;return v.map(x=>x*sign).join(",");};
const roots=normals.map(root),lookup=new Map(roots.map((r,i)=>[canon(r),normals[i]])),idx=new Map(normals.map((n,i)=>[n,i]));
const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),cat=new Map();let frames=0;
for(let i=0;i<120;i++)for(let j=i+1;j<120;j++){if(dot(roots[i],roots[j]))continue;for(let k=j+1;k<120;k++){
if(dot(roots[i],roots[k])||dot(roots[j],roots[k]))continue;
const nl=normals[i]^normals[j]^normals[k],l=idx.get(nl);
if(l===undefined||l<=k||dot(roots[i],roots[l])||dot(roots[j],roots[l])||dot(roots[k],roots[l]))continue;
frames++;const ff=[i,j,k,l],members=ff.map(q=>normals[q]);
for(let signs=0;signs<8;signs++){
const v=Array.from({length:8},(_,d)=>(roots[i][d]+[j,k,l].reduce((s,q,z)=>s+((signs>>z&1)?1:-1)*roots[q][d],0))/2);
need(v.every(Number.isInteger),"D4 half signs integral");const n=lookup.get(canon(v));need(n!==undefined,"D4 half signs native root");members.push(n);
}
need(new Set(members).size===12,"twelve distinct roots");members.sort((a,b)=>a-b);cat.set(members.join(","),members);
}}
need(frames===9450&&cat.size===3150,"independent eight-coordinate closure census");
const exclude=new Set([7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491,81,273,262,98,290,268,164,280]);
const H=normals.filter(n=>!exclude.has(n)),hi=new Map(H.map((n,i)=>[n,i]));
const mask=ns=>ns.reduce((a,n)=>a|(1n<<BigInt(hi.get(n))),0n);
const blocks=[...cat.values()].map(ns=>ns.filter(n=>!exclude.has(n)));
const full=blocks.filter(ns=>ns.length===12).map(mask);
need(full.length===90,"ninety full blocks");
const eleven=new Set();
for(const ns of blocks)if(ns.length===11)eleven.add(mask(ns).toString());else if(ns.length===12){const m=mask(ns);for(const n of ns)eleven.add((m^(1n<<BigInt(hi.get(n)))).toString());}
need(eleven.size===1686,"eleven set census");
const all=(1n<<96n)-1n;let nodes=0,pack7=0,pack8=0,rank33=0;const counts=Array(9).fill(0),witnesses=[];
function dfs(chosen,used,candidates){
nodes++;need(nodes<10000000,"review budget reached without conclusion");
counts[chosen.length]++;
if(chosen.length===7){pack7++;const rem=all^used;let m=rem;while(m){const z=m&-m;if(eleven.has((rem^z).toString())){rank33++;witnesses.push({chosen,singleton:H[z.toString(2).length-1]});}m-=z;}if(candidates.length)pack8+=candidates.length;return;}
if(chosen.length+candidates.length<7)return;
for(let p=0;p<candidates.length;p++){if(chosen.length+candidates.length-p<7)break;const q=candidates[p],fm=full[q];const next=candidates.slice(p+1).filter(r=>(full[r]&fm)===0n);dfs([...chosen,q],used|fm,next);}
}
dfs([],0n,full.map((_,i)=>i));
need(pack8===0&&rank33===0,"rank32 and33 excluded by independent seven-full-block enumeration");
return {status:"PASS_INDEPENDENT_ROOT_D4_CLOSURE_AND_PACKING",root_model:"eight-coordinate norm8; explicit half-sign completion",frames,D4:cat.size,hosted:H.length,full_blocks:full.length,eleven_subsets:eleven.size,nodes,depth_counts:counts,seven_full_packings:pack7,eight_full_packings:pack8,rank33_completions:rank33,normal_catalogue:[...cat.values()]};
})();

function allFullPackings(catalogue){
 const ex=new Set([7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491,81,273,262,98,290,268,164,280]);
 const H=Array.from(new Set(catalogue.flat())).filter(n=>!ex.has(n)).sort((a,b)=>a-b),ix=new Map(H.map((n,i)=>[n,i]));
 const full=catalogue.filter(r=>r.every(n=>!ex.has(n))),masks=full.map(r=>r.reduce((s,n)=>s|(1n<<BigInt(ix.get(n))),0n));
 const counts=Array(9).fill(0);let nodes=0,max=0,example=[];
 function dfs(chosen,candidates){nodes++;counts[chosen.length]++;if(chosen.length>max){max=chosen.length;example=chosen.slice();}for(let i=0;i<candidates.length;i++){const q=candidates[i];dfs([...chosen,q],candidates.slice(i+1).filter(j=>!(masks[q]&masks[j])));}}
 dfs([],full.map((_,i)=>i));if(max!==4||nodes!==1585)throw Error("full packing census");
 let largest=0,best=null;
 for(let a=0;a<=8;a++)for(let b=0;b<=11;b++)for(let c=0;c<=17;c++){const d=34-4*a-3*b-2*c;if(d<0)continue;const n=11*a+Math.min(a,4)+6*b+3*c+d;if(n>largest){largest=n;best={a,b,c,d};}}
 if(largest!==95)throw Error("density optimization");
 return {status:"PASS_EXACT_ALL_FULL_PACKINGS_AND_RANK35",nodes,counts,maximum_full_blocks:max,example:example.map(i=>full[i]),maximum_roots_at_rank34:largest,best_shape:best};
}

const packing=allFullPackings(closure.normal_catalogue);
const result={closure:{...closure,normal_catalogue:undefined},packing};
console.log(JSON.stringify(result,null,2));
