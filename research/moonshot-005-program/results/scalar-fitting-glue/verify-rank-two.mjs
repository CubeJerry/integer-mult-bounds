function verifyRankTwoException(){
 const omitted=[7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491];
 const need=(q,m)=>{if(!q)throw Error(m);};
 const pop=n=>{let c=0;while(n){n&=n-1;c++;}return c;};
 const N=Array.from({length:512},(_,n)=>n).filter(n=>[3,7].includes(pop(n))&&!omitted.includes(n));
 function root(n){const b=[];for(let j=0;j<9;j++)if(n>>j&1)b.push(j);if(b.length===3)return Array.from({length:8},(_,j)=>b.includes(8)?2*Number(b.includes(j)):(b.includes(j)?1:-1));const z=Array.from({length:9},(_,j)=>j).filter(j=>!b.includes(j));return Array.from({length:8},(_,j)=>z[1]===8?(j===z[0]?1:-1):2*(Number(j===z[0])-Number(j===z[1])));}
 const A=N.map(root),dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0);
 const active=[13,505,11], [i,j,k]=active.map(n=>N.indexOf(n));
 need(i>=0&&j>=0&&k>=0&&dot(A[i],A[j])===-4&&A[k].every((x,l)=>x===A[i][l]+A[j][l]),"actual native A2 triple");
 const h=A.map(a=>dot(A[k],a)===0?dot(A[i],a):0);
 need(h.some(x=>x!==0),"extra direction nonzero");
 for(let q=0;q<104;q++){
  if(dot(A[i],A[q])===0||dot(A[j],A[q])===0)need(h[q]===0,"first two local restrictions");
  if(dot(A[k],A[q])===0)need(h[q]===dot(A[i],A[q]),"third local restriction");
 }
 const K8=A.map((a,s)=>A.map((b,t)=>s===i||s===j?dot(a,b)+8*h[t]:s===k?-8*dot(A[i],b)+5*dot(A[k],b)+8*h[t]:dot(a,b)));
 for(let s=0;s<104;s++)for(let t=0;t<104;t++){if(s===t)need(K8[s][t]===8,"unit fitting diagonal");if(dot(A[s],A[t])===0)need(K8[s][t]===0,"all forbidden fitting entries");}
 function det(rows){const M=rows.map(r=>r.map(BigInt)),n=M.length;let prev=1n,sign=1n;for(let c=0;c<n-1;c++){let r=c;while(r<n&&!M[r][c])r++;if(r===n)return 0n;if(r!==c){[M[r],M[c]]=[M[c],M[r]];sign=-sign;}const v=M[c][c];for(let s=c+1;s<n;s++){for(let t=c+1;t<n;t++){const x=M[s][t]*v-M[s][c]*M[c][t];need(x%prev===0n,"exact Bareiss division");M[s][t]=x/prev;}M[s][c]=0n;}prev=v;}return sign*M[n-1][n-1];}
 const minorNormals=[11,13,14,19,21,26,35,69,131],indices=minorNormals.map(n=>N.indexOf(n));
 const dd=det(indices.map(r=>indices.map(c=>K8[r][c])));need(dd===8388608n,"rank-nine exact integer minor");
 const mutant=indices.map(r=>indices.map(c=>K8[r][c]));mutant[8]=mutant[0].slice();need(det(mutant)===0n,"duplicate minor row negative control");
 const inactiveBasis=[14,19,21,26,35,69,131,259];need(inactiveBasis.every(n=>!active.includes(n)),"inactive basis excludes active rows");const inactiveDet=det(inactiveBasis.map(n=>A[N.indexOf(n)]));need(inactiveDet!==0n,"inactive source roots retain rank eight");
 const result={inactive_basis_normals:inactiveBasis,inactive_integer_determinant:String(inactiveDet),status:"PASS_SHARP_RANK_TWO_ACTIVE_EXCEPTION",active_normals:active,active_roots:[A[i],A[j],A[k]],root_relation:"a3=a1+a2; a1 dot a2=-4",nonzero_h:h.map((v,q)=>[N[q],v]).filter(x=>x[1]),source_entries_checked:104*104,rank:9,minor_matrix:"8K",minor_rows:minorNormals,minor_columns:minorNormals,integer_determinant:String(dd),classification:"Explicit scalar rank-nine fitting matrix and sharp counterexample to dropping active-span-at-least-three. Algebraic rank upper bound follows from the displayed nine-mode factorization. No source-word or all-volume admission."};
 return result;
}
console.log(JSON.stringify(verifyRankTwoException()));
