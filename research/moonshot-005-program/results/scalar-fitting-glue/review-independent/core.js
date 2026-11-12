(function independentScalarGluingReview(){
 const assert=(v,m)=>{if(!v)throw Error(m);}, omitted=new Set([7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491]);
 const wt=n=>{let s=0;for(;n;n>>=1)s+=n&1;return s;};
 const all=[];for(let n=0;n<512;n++)if(wt(n)===3||wt(n)===7)all.push(n);
 function q(n){const bits=Array.from({length:9},(_,j)=>(n>>j)&1);if(wt(n)===3)return bits.map(x=>3*x-1);const holes=bits.map((v,j)=>v?-1:j).filter(j=>j>=0);return bits.map((_,j)=>3*(Number(j===holes[0])-Number(j===holes[1])));}
 const N=all.filter(n=>!omitted.has(n)), Q=N.map(q), dot=(a,b)=>a.reduce((s,v,k)=>s+v*b[k],0);
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;};
 function rankWitness(rows,limit=Infinity){const b=[],selected=[],cols=[];for(let z=rows.length-1;z>=0;z--){let v=rows[z].map(BigInt);for(const e of b){const t=v[e.p];if(!t)continue;const u=e.v[e.p];v=v.map((x,k)=>u*x-t*e.v[k]);let g=0n;for(const x of v)g=gcd(g,x);if(g>1n)v=v.map(x=>x/g);}let p=v.findIndex(x=>x!==0n);if(p<0)continue;if(v[p]<0n)v=v.map(x=>-x);let g=0n;for(const x of v)g=gcd(g,x);if(g>1n)v=v.map(x=>x/g);b.push({p,v});b.sort((x,y)=>x.p-y.p);selected.push(z);cols.push(p);if(b.length===limit)break;}return {rank:b.length,selected,cols};}
 function determinant(M){const n=M.length,cache=new Map();function rec(mask,row){if(row===n)return 1n;if(cache.has(mask))return cache.get(mask);let d=0n,sgn=1n;for(let c=0;c<n;c++)if(!(mask&(1<<c))){d+=sgn*BigInt(M[row][c])*rec(mask|(1<<c),row+1);sgn=-sgn;}cache.set(mask,d);return d;}return rec(0,0);}
 assert(N.length===104&&all.length===120,"source counts");assert(Q.every(v=>dot(v,v)===18&&v.reduce((s,x)=>s+x,0)===0),"Q9 exact model");
 const G=Q.map(a=>Q.map(b=>dot(a,b))), F=G.map(r=>r.map((x,j)=>x===0?j:-1).filter(j=>j>=0));
 const single=[],pairs=[],hist={};let minSingle=9,minPair=9;
 for(let i=0;i<104;i++){assert(F[i].length===55,"single forbidden count");const w=rankWitness(F[i].map(j=>Q[j]),7);assert(w.rank===7,"single rank");const rr=w.selected.map(k=>F[i][k]), d=determinant(rr.map(r=>w.cols.map(c=>Q[r][c])));assert(d!==0n,"single minor");single.push([N[i],rr.map(j=>N[j]),w.cols,String(d)]);minSingle=Math.min(minSingle,w.rank);
 for(let j=i+1;j<104;j++){assert([0,9,-9].includes(G[i][j]),"projective geometry");assert((G[i][j]!==0)===((wt(N[i]&N[j])&1)===0),"binary nonorthogonal criterion");const S=F[i].filter(k=>G[j][k]===0);const v=rankWitness(S.map(k=>Q[k]),6);assert(v.rank===6,"overlap rank");const chosen=v.selected.map(k=>S[k]), e=determinant(chosen.map(r=>v.cols.map(c=>Q[r][c])));assert(e!==0n,"pair minor");pairs.push([N[i],N[j],chosen.map(k=>N[k]),v.cols,String(e)]);minPair=Math.min(minPair,v.rank);const key=(G[i][j]?"nonorthogonal:":"orthogonal:")+S.length;hist[key]=(hist[key]||0)+1;}}
 const removed=[42,44,50,52,193,223,321,351,385,415], aa=q(7), bb=q(25), overlap=all.filter(n=>dot(q(n),aa)===0&&dot(q(n),bb)===0), retained=overlap.filter(n=>!removed.includes(n));
 assert(overlap.length===30&&removed.every(n=>overlap.includes(n))&&retained.length===20,"deletion control source");
 const deletionRank=rankWitness(retained.map(q)).rank;assert(deletionRank===5,"deletion control rank five");
 const active=[13,505,11], [ia,ib,ic]=active.map(n=>N.indexOf(n)), h=Q.map((v,j)=>G[ic][j]===0?G[ia][j]:0);
 assert(Q[ic].every((x,k)=>x===Q[ia][k]+Q[ib][k])&&G[ia][ib]===-9,"A2 dependence");
 for(let j=0;j<104;j++){if(G[ia][j]===0||G[ib][j]===0)assert(h[j]===0,"local a,b restriction");if(G[ic][j]===0)assert(h[j]===G[ia][j],"local c restriction");}
 const K18=G.map((row,i)=>row.map((g,j)=>i===ia||i===ib?g+8*h[j]:i===ic?-8*G[ia][j]+5*g+8*h[j]:g));
 for(let i=0;i<104;i++)for(let j=0;j<104;j++){if(i===j)assert(K18[i][j]===18,"diagonal one");if(G[i][j]===0)assert(K18[i][j]===0,"all forbidden entries");if(!active.includes(N[i]))assert(K18[i][j]===G[i][j],"inactive rows literal Gram");}
 const kw=rankWitness(K18), kd=determinant(kw.selected.map(i=>kw.cols.map(j=>K18[i][j])));assert(kw.rank===9&&kd!==0n,"independent full matrix rank nine");
 const quoted=[11,13,14,19,21,26,35,69,131].map(n=>N.indexOf(n)), quotedDet=determinant(quoted.map(i=>quoted.map(j=>K18[i][j])));assert(quotedDet===12397455648n,"independent scale converted quoted determinant");
 const duplicate=kw.selected.map(i=>kw.cols.map(j=>K18[i][j]));duplicate[8]=duplicate[0].slice();assert(determinant(duplicate)===0n,"duplicate witness control");
 const badC=K18[ic].map((v,j)=>v-G[ic][j]);assert(badC[ic]!==18,"diagonal coefficient mutant");
 const badH=K18[ic].map((v,j)=>v-8*h[j]);assert(F[ic].some(j=>badH[j]!==0),"missing third local correction mutant");
 const inactive=Q.filter((_,i)=>!active.includes(N[i]));assert(rankWitness(inactive).rank===8,"inactive roots span eight");
 let clique=null;
 function findClique(chosen,candidates){if(chosen.length===8){clique=chosen;return true;}if(chosen.length+candidates.length<8)return false;for(let k=0;k<candidates.length;k++){const v=candidates[k];if(findClique([...chosen,v],candidates.slice(k+1).filter(w=>G[v][w]!==0)))return true;}return false;}
 assert(findClique([],N.map((_,i)=>i)),"source clique eight exists");
 const common=clique.map(i=>N[i]);const commonNeighbours=N.filter((n,j)=>clique.every(i=>G[i][j]!==0));assert(JSON.stringify(commonNeighbours.slice().sort((a,b)=>a-b))===JSON.stringify(common.slice().sort((a,b)=>a-b)),"eight clique common neighborhood itself");
 const cliqueSet=new Set(clique), g8=G.map((_,j)=>cliqueSet.has(j)?18:0);
 const Kcl=G.map((row,i)=>cliqueSet.has(i)?g8.slice():row.slice()), Delta=Kcl.map((row,i)=>row.map((v,j)=>v-G[i][j]));
 const dc=rankWitness(Delta),kc=rankWitness(Kcl),wc=rankWitness(Q.filter((_,i)=>!cliqueSet.has(i)));
 assert(dc.rank===8&&kc.rank===9&&wc.rank===8,"sharp eight-row perturbation");
 const dcDet=determinant(dc.selected.map(i=>dc.cols.map(j=>Delta[i][j])));assert(dcDet!==0n,"rank-eight perturbation exact minor");
 const out={status:"PASS_INDEPENDENT_SCALAR_GLUING_REVIEW",method:"Fresh Q9 roots, exact integer gcd elimination and Laplace minors; no author checker run or imported.",source_normals:N,single_count:single.length,pair_count:pairs.length,single_rank:minSingle,pair_rank:minPair,overlap_cardinality_histogram:hist,exception:{active_normals:active,rank:kw.rank,full_entries:10816,selected_rows:kw.selected.map(i=>N[i]),selected_columns:kw.cols.map(i=>N[i]),determinant_matrix:"18K",integer_determinant:String(kd),quoted_determinant_scaled_to_18K:String(quotedDet),inactive_rank:8},new_corroboration:{eight_clique_normals:common,common_neighborhood:commonNeighbours,sharp_difference_rank:dc.rank,sharp_fitting_rank:kc.rank,sharp_inactive_root_rank:wc.rank,delta_rows:dc.selected.map(i=>N[i]),delta_columns:dc.cols.map(i=>N[i]),delta_minor_matrix:"18(K-G)",delta_integer_determinant:String(dcDet)},negative_controls:{self_pair_rank:7,arbitrary_deletion_rank:deletionRank,duplicate_row_zero:true,wrong_c_diagonal_rejected:true,missing_c_local_term_rejected:true},single_witnesses:single,pair_witnesses:pairs};return out;
})()