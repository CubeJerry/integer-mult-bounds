export function checkDegreeFourControls(){
 const assert=(p,m)=>{if(!p)throw Error(m)};
 function rank(M,p){M=M.map(r=>r.map(x=>(x%p+p)%p));let k=0;for(let c=0;c<M[0].length&&k<M.length;c++){let s=k;while(s<M.length&&M[s][c]===0)s++;if(s===M.length)continue;[M[s],M[k]]=[M[k],M[s]];let inv=1;while(M[k][c]*inv%p!==1)inv++;for(let j=c;j<M[0].length;j++)M[k][j]=M[k][j]*inv%p;for(let i=k+1;i<M.length;i++){const a=M[i][c];for(let j=c;j<M[0].length;j++)M[i][j]=(M[i][j]-a*M[k][j]%p+p)%p;}k++;}return k;}
 const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], assigned=[1,0,4,4,3,2],unit=a=>Array.from({length:5},(_,i)=>i===a?1:0);
 const rows=Array.from({length:4},(_,i)=>unit(i)).concat(assigned.map(unit));
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),M=rows.map(a=>rows.map(b=>dot(a,b)));
 assert(M.every((r,i)=>r[i]===1),"control diagonal");
 for(let a=0;a<4;a++)for(let b=0;b<4;b++)if(a!==b)assert(M[a][b]===0,"point zeros");
 for(let e=0;e<6;e++){assert(edges[e].includes(assigned[e])||assigned[e]===4,"support");for(let a=0;a<4;a++)if(!edges[e].includes(a))assert(M[4+e][a]===0&&M[a][4+e]===0,"nonendpoint zero");}
 for(let e=0;e<6;e++)for(let f=0;f<e;f++)if(edges[e].some(a=>edges[f].includes(a)))assert(M[e+4][f+4]===0&&M[f+4][e+4]===0,"incident edge zero");
 assert(rank(M,2)===5&&rank(M,3)===5,"control rank five");
 const schur=assigned.map(a=>a===4?1:0);assert(schur.filter(x=>x===0).length===4,"four zero Schur blocks");
 const G=Array(4).fill(0),gamma=edges.map((e,i)=>e.map(a=>{const g=(assigned[i]===a||assigned[i]===4)?1:0;G[a]+=g;return g}));
 let slack=0;for(let e=0;e<6;e++)for(const a of edges[e]){const s=2*(gamma[e][0]+gamma[e][1])-G[a];assert(s>=0,"control LR");slack+=s;}
 assert(slack===8&&G.every(x=>x===2),"degree3 summation slack");
 const finite=[];
 for(const [n,p] of [[2,2],[2,3],[3,2]]){
  let satisfying=0;const count=p**(n*n);
  for(let code=0;code<count;code++){let t=code;const X=Array.from({length:n},()=>Array.from({length:n},()=>{const z=t%p;t=Math.floor(t/p);return z;}));
   const comp=X.map((r,i)=>r.map((x,j)=>((i===j?1:0)-x+p)%p));
   const equality=rank(X,p)+rank(comp,p)===n;
   const idem=X.every((r,i)=>r.every((x,j)=>X[i].reduce((s,z,k)=>s+z*X[k][j],0)%p===x));
   assert(equality===idem,"idempotent rank lemma finite control");if(equality)satisfying++;
  }
  finite.push({dimension:n,field_size:p,matrices_checked:count,idempotents:satisfying});
 }
 return {status:"PASS_DEGREE_FOUR_STAR_CONTROLS",predecessor_proof_git_blob:"f9f0b56e2a06231fba611ab248819ab2543a480b",degree_three_counterexample:{edges,assigned_coordinates:assigned,rank:5,Schur_diagonals:schur,star_G:G,total_LR_slack:slack},finite_idempotent_controls:finite,universal_theorem_is_written_proof:true,no_native_source_or_new_kappa:true};
}

import { resolve } from "node:path";
import { fileURLToPath } from "node:url";
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url))process.stdout.write(JSON.stringify(checkDegreeFourControls(),null,2)+"\n");
