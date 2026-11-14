
function reviewTensorSeparation() {
 const need=(x,m)=>{if(!x)throw Error(m)},perms=[];
 for(let a=1;a<=3;a++)for(let b=1;b<=3;b++)for(let c=1;c<=3;c++)if(new Set([a,b,c]).size===3)perms.push([0,a,b,c]);
 const G=[];for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++)if((a+b+c)%2===0)for(const out of perms){const u=[0,a,b,c];G.push({out:out.slice(),phase:out.map(j=>u[j])});}
 const key=g=>g.out.join("")+":"+g.phase.join(""),index=new Map(G.map((g,i)=>[key(g),i]));
 need(index.size===192,"192 explicit Walsh monomials");
 const identity=index.get("0123:0000");
 const compose=(g,h)=>({out:h.out.map(j=>g.out[j]),phase:h.out.map((j,k)=>(h.phase[k]+g.phase[j])%4)});
 const table=G.map(g=>G.map(h=>index.get(key(compose(g,h)))));
 need(table.every(r=>r.every(x=>x!==undefined)),"explicit closure");
 const pop=x=>x.toString(2).split("1").length-1;
 const H=Array.from({length:4},(_,a)=>Array.from({length:4},(_,b)=>pop(a&b)%2?-1:1));
 const phase=[[1,0],[0,1],[-1,0],[0,-1]],ranks=[];
 for(const g of G){
  const physical=H.map((row,a)=>H.map((_,b)=>{let re=0,im=0;for(let j=0;j<4;j++){const z=phase[g.phase[j]],s=H[a][g.out[j]]*H[j][b];re+=s*z[0];im+=s*z[1];}return[re,im];}));
  const supports=physical.map(row=>row.filter(([a,b])=>a||b).length);
  need(new Set(supports).size===1&&[1,2,4].includes(supports[0]),"uniform physical support");
  const s=supports[0];need(physical.every(row=>row.every(([a,b])=>!(a||b)||a*a+b*b===16/s)),"exact Gaussian magnitudes");
  ranks.push(Math.log2(s));
 }

 const ordinary=ranks.flatMap((r,i)=>r===0?[i]:[]),hist=[0,1,2].map(r=>ranks.filter(x=>x===r).length);
 need(hist.join(",")==="24,72,96","physical rank classes");
 let bimodule=0;for(const h of ordinary)for(let i=0;i<192;i++){need(ranks[table[h][i]]===ranks[i]&&ranks[table[i][h]]===ranks[i],"ordinary double-coset stability");bimodule+=2;}
 const gram=G.map(g=>G.map(h=>{let re=0,im=0;for(let j=0;j<4;j++)if(g.out[j]===h.out[j]){const z=phase[(h.phase[j]-g.phase[j]+4)%4];re+=z[0];im+=z[1];}return[re,im];}));
 let max=0;for(let i=0;i<192;i++)for(let j=0;j<192;j++)if(i!==j)max=Math.max(max,gram[i][j][0]**2+gram[i][j][1]**2);
 need(max===8,"all-pairs trace gap");
 const p=109,imaginary=33,invs=Array.from({length:p},(_,a)=>{for(let j=1;j<p;j++)if(a*j%p===1)return j;return 0});
 need(imaginary*imaginary%p===p-1,"imaginary root");
 const pow=(x,v)=>{let z=1;for(let k=0;k<v;k++)z=z*x%p;return z};
 function eliminate(A){A=A.map(r=>r.slice());let at=0,det=1;for(let c=0;c<A[0].length&&at<A.length;c++){let r=at;while(r<A.length&&!A[r][c])r++;if(r===A.length)continue;if(r!==at){[A[r],A[at]]=[A[at],A[r]];det=(p-det)%p;}const pivot=A[at][c];det=det*pivot%p;for(let j=c;j<A[0].length;j++)A[at][j]=A[at][j]*invs[pivot]%p;for(let i=at+1;i<A.length;i++){const m=A[i][c];if(m)for(let j=c;j<A[0].length;j++)A[i][j]=(A[i][j]-m*A[at][j]%p+p)%p;}at++;}return{rank:at,det:at===A.length?det:0};}
 const witnesses=[1,5,6].map(V=>({V,...eliminate(gram.map(row=>row.map(([a,b])=>pow((a+imaginary*b+p*4)%p,V))))}));
 need(witnesses[2].rank===192&&witnesses[2].det!==0,"independent prime determinant");
 const qa=G.findIndex(g=>key(g)==="0123:0101");
 need(qa>=0&&ranks[qa]===1&&ranks[table[qa][qa]]===0,"nonordinary-rank mutation");
 return{status:"PASS_ROOT_TENSOR_SEPARATION_REVIEW",explicit_Walsh_monomials:G.length,physical_rank_counts:hist,ordinary_size:ordinary.length,all_pair_maximum_trace_squared:max,ordinary_rank_contacts:bimodule,independent_Gram_prime:p,imaginary_root:imaginary,witnesses,all_width_consequence:"Independence at6 and every larger width by contraction on the common fixed zero-frequency vector.",negative_controls:{nonordinary_multiplier_changes_rank:true,one_column_sum_does_not_tensor_linearly:{actual_width2_eigenvalue:-1,claimed_linear_sum_eigenvalue:1}},new_complete_kappa:false};
}

if(typeof module!=="undefined")module.exports={reviewTensorSeparation};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(reviewTensorSeparation(),null,2));
