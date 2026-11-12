function verifyGluingSource() {
  const omitted=[7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491];
  const frame1=[7,25,42,52,76,82,97,127], frame2=[67,104,137,162,266,289,448,491];
  const need=(q,m)=>{if(!q)throw new Error(m);};
  const pop=n=>{let c=0;while(n){n&=n-1;c++;}return c;};
  function root(n) {
    const ones=[];for(let j=0;j<9;j++)if((n>>j)&1)ones.push(j);
    if(ones.length===3)return Array.from({length:8},(_,j)=>ones.includes(8)?(ones.includes(j)?2:0):(ones.includes(j)?1:-1));
    need(ones.length===7,"root weight");const z=[];for(let j=0;j<9;j++)if(!ones.includes(j))z.push(j);
    const [a,b]=z;return Array.from({length:8},(_,j)=>b===8?(j===a?1:-1):2*((j===a?1:0)-(j===b?1:0)));
  }
  const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
  const full=Array.from({length:512},(_,i)=>i).filter(n=>[3,7].includes(pop(n)));
  const N=full.filter(n=>!omitted.includes(n)), A=N.map(root);
  need(full.length===120&&N.length===104,"full/source inventory");
  need(omitted.length===16&&new Set([...frame1,...frame2]).size===16&&omitted.every(n=>frame1.includes(n)||frame2.includes(n)),"two-frame omitted partition");
  for(const frame of [frame1,frame2])for(let i=0;i<8;i++)for(let j=0;j<8;j++)need(dot(root(frame[i]),root(frame[j]))===(i===j?8:0),"omitted orthogonal frames");
  need(A.every(a=>dot(a,a)===8),"native root squared norms");
  const P=65537;
  need(Array.from({length:255},(_,i)=>i+2).every(d=>P%d!==0),"rank modulus prime");
  function power(a,n){let r=1;while(n){if(n&1)r=r*a%P;a=a*a%P;n=Math.floor(n/2);}return r;}
  function rankWitness(rows, limit=8) {
    const B=Array(8).fill(null), chosen=[], cols=[];
    for(let i=0;i<rows.length;i++){
      const row=rows[i].map(x=>(x%P+P)%P);
      for(let j=0;j<8;j++)if(row[j]){
        if(B[j]){const c=row[j];for(let k=j;k<8;k++)row[k]=(row[k]-c*B[j][k]%P+P)%P;}
        else {const inv=power(row[j],P-2);B[j]=row.map(x=>x*inv%P);chosen.push(i);cols.push(j);break;}
      }
      if(chosen.length===limit)break;
    }
    return {rank:chosen.length,chosen,cols};
  }
  function det(rows){
    const M=rows.map(r=>r.map(BigInt));const n=M.length;let old=1n,sign=1n;
    for(let j=0;j<n-1;j++){
      let p=j;while(p<n&&M[p][j]===0n)p++;if(p===n)return 0n;
      if(p!==j){[M[p],M[j]]=[M[j],M[p]];sign=-sign;}
      const pivot=M[j][j];
      for(let i=j+1;i<n;i++){
        for(let k=j+1;k<n;k++){const num=M[i][k]*pivot-M[i][j]*M[j][k];need(num%old===0n,"Bareiss exact division");M[i][k]=num/old;}
        M[i][j]=0n;
      }
      old=pivot;
    }
    return sign*M[n-1][n-1];
  }
  const singles=[],pairs=[],hist={},detHist={};let negativeSelf=null;
  for(let i=0;i<104;i++){
    const F=N.map((n,j)=>j).filter(j=>dot(A[i],A[j])===0);
    need(F.length===55,"native forbidden set cardinality");
    const w=rankWitness(F.map(j=>A[j]),7);need(w.rank===7,"single-forbidden rank seven");
    const minor=det(w.chosen.map(j=>w.cols.map(k=>A[F[j]][k])));need(minor!==0n,"single exact nonzero minor");
    singles.push([N[i],w.chosen.map(j=>N[F[j]]),w.cols,String(minor)]);
    for(let k=i+1;k<104;k++){
      need([0,4,-4].includes(dot(A[i],A[k])),"distinct source projective root geometry");
      const common=F.filter(j=>dot(A[k],A[j])===0);
      const ww=rankWitness(common.map(j=>A[j]),6);need(ww.rank===6,"double-forbidden rank six");
      const matrix=ww.chosen.map(j=>ww.cols.map(c=>A[common[j]][c]));
      const dd=det(matrix);need(dd!==0n,"double exact nonzero integer minor");
      need(common.every(j=>dot(A[i],A[j])===0&&dot(A[k],A[j])===0),"exact independent upper annihilators");
      pairs.push([N[i],N[k],ww.chosen.map(j=>N[common[j]]),ww.cols,String(dd)]);
      const key=`${dot(A[i],A[k])===0?"orthogonal":"nonorthogonal"}:${common.length}`;hist[key]=(hist[key]||0)+1;detHist[String(dd)]=(detHist[String(dd)]||0)+1;
      if(negativeSelf===null){const duplicate=matrix.map(r=>r.slice());duplicate[5]=duplicate[0].slice();need(det(duplicate)===0n,"duplicated witness row is rejected");negativeSelf=[N[i],N[k]];}
    }
  }
  need(pairs.length===5356&&singles.length===104,"complete exact source domains");
  // Cardinality alone does not imply the overlap property: delete ten roots from a D6 star.
  let counter=null;
  outer: for(let i=0;i<full.length;i++)for(let k=i+1;k<full.length;k++){
    const a=root(full[i]),b=root(full[k]);if(dot(a,b)!==0)continue;
    const C=full.filter(n=>dot(root(n),a)===0&&dot(root(n),b)===0);
    need(C.length===30,"full orthogonal-pair D6 cardinality");
    for(let x=0;x<C.length;x++)for(let y=x+1;y<C.length;y++){
      const ax=root(C[x]),ay=root(C[y]);if(dot(ax,ay)!==0)continue;
      const normal=ax.map((v,j)=>v+ay[j]);const kept=C.filter(n=>dot(root(n),normal)===0);
      if(kept.length!==20)continue;
      const removed=C.filter(n=>!kept.includes(n));
      need(removed.length===10&&rankWitness(kept.map(root)).rank===5,"arbitrary ten-root deletion destroys overlap span");
      counter={pair:[full[i],full[k]],removed_ten:removed,retained_common_roots:kept,retained_rank:5,normal};break outer;
    }
  }
  need(counter!==null,"real deletion-pattern negative control");
  const summary={status:"PASS_E8_SOURCE_LOCAL_LINEAR_GLUE_CERTIFICATE",source_normals:N,omitted_normals:omitted,omitted_orthogonal_frames:[frame1,frame2],source_inventory_provenance:"Regenerated from the 104-normal inventory and 16 omitted normals in the published minimal-eight source certificate; no unavailable filesystem bytes were re-read.",source_compressed_sha256_reference:"2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883",single_forbidden_rows:104,single_forbidden_cardinality:55,single_forbidden_rank:7,double_forbidden_pairs:5356,double_forbidden_rank:6,exact_integer_minors:5460,overlap_cardinality_histogram:hist,minor_determinant_histogram:detHist,negative_controls:{duplicate_basis_row:negativeSelf,self_pair_rank:7,arbitrary_ten_root_deletion:counter},classification:"Exact finite source linear algebra. The scalar fitting-matrix gluing and converse are proved separately; no all-volume or physical-word admission and no new kappa."};
  return {summary,single_witnesses:singles,pair_witnesses:pairs};
}
const result=verifyGluingSource();
console.log(JSON.stringify(result));
