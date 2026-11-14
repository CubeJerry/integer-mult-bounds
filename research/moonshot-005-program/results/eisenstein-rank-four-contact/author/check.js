
function check(s) {
  const need=(c,m)=>{if(!c)throw Error(m)};
  const pc=x=>{let n=0;for(;x;x&=x-1)n++;return n};
  const dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
  const root=v=>pc(v)===3?Array.from({length:9},(_,i)=>(v>>i&1)?2:-1):(()=>{const q=Array.from({length:9},(_,i)=>i).filter(i=>!(v>>i&1));need(q.length===2,"root weight");return Array.from({length:9},(_,i)=>3*((i===q[0])-(i===q[1])));})();
  const twox=x=>{const [a,b="1"]=x.split("/").map(Number);need((2*a)%b===0,"half integral");return 2*a/b};
  const S=s.real_matrix.map((r,i)=>r.map((x,j)=>twox(x)+(i===j?1:0)));
  const Z=[7,25,42,52,76,82,97,127].map(root),P=s.cycles.flat().sort((a,b)=>a-b),n=P.length;
  need(n===120&&new Set(P).size===120,"120 roots");
  const p=P.map(v=>Z.map(z=>{let a=dot(root(v),z);need(a%9===0,"half integral root row");return a/9}));
  const sp=p.map(v=>S.map(r=>dot(r,v)));
  const A=p.map(v=>p.map(w=>dot(v,w))),C=p.map(v=>sp.map(w=>dot(v,w)));
  const ix=new Map(P.map((v,i)=>[v,i])),cl=new Map(),phase=new Map();
  s.cycles.forEach((q,i)=>q.forEach((v,j)=>{cl.set(v,i);phase.set(v,j)}));
  const cyc=s.cycles.map(q=>q.map(v=>ix.get(v)));
  for(let i=0;i<8;i++)for(let j=0;j<8;j++){
    need(S[i][j]===-S[j][i],"skew");
    need(S[i].reduce((z,x,k)=>z+x*S[k][j],0)===(i===j?-3:0),"S squared");
  }
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)need((A[i][j]===0)===(pc(P[i]&P[j])%2===1),"binary forbidden equals real orthogonality");
  const orth=[],gain=[];
  for(let i=0;i<40;i++)for(let j=i+1;j<40;j++){
    let u=cyc[i][0],v=cyc[j][0];
    if(A[u][v]===0&&C[u][v]===0){orth.push([i,j]);continue}
    let bad=[0,1,2].filter(k=>A[u][cyc[j][k]]===0);need(bad.length===1,"unique bad phase");
    let k=bad[0];for(let a=0;a<3;a++)for(let b=0;b<3;b++)need((A[cyc[i][a]][cyc[j][b]]===0)===((b-a+3)%3===k),"relative phase gain");
    gain.push([i,j,k]);
  }
  need(orth.length===240&&gain.length===540,"complex pair counts");
  const adj=A.map((r,i)=>r.map((v,j)=>i!==j&&v===0&&C[i][j]!==0));
  const qs=new Map();
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(adj[i][j])
    for(let k=j+1;k<n;k++)if(adj[i][k]&&adj[j][k])
      for(let l=k+1;l<n;l++)if(adj[i][l]&&adj[j][l]&&adj[k][l]){
        let vs=[P[i],P[j],P[k],P[l]],classes=vs.map(v=>cl.get(v)).sort((a,b)=>a-b);
        need(new Set(classes).size===4,"four different classes");let key=classes.join(",");
        if(!qs.has(key))qs.set(key,{classes,root_witness:vs,phase_witness:vs.map(v=>[cl.get(v),phase.get(v)])});
      }
  need(qs.size===90,"ninety pencils");let cover=new Map();
  for(const q of qs.values())for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){let k=[q.classes[i],q.classes[j]].join(",");cover.set(k,(cover.get(k)||0)+1)}
  need(cover.size===540&&[...cover.values()].every(x=>x===1),"pencil pair partition");
  for(const [i,j] of gain)need(cover.has([i,j].join(",")),"every nonorthogonal pair covered");
  const reps=cyc.map(q=>q[0]),a40=reps.map(i=>reps.map(j=>A[i][j])),c40=reps.map(i=>reps.map(j=>C[i][j]));
  for(let i=0;i<40;i++)for(let j=0;j<40;j++){
    let aa=0,cc=0,ac=0,ca=0;
    for(let k=0;k<40;k++){aa+=a40[i][k]*a40[k][j];cc+=c40[i][k]*c40[k][j];ac+=a40[i][k]*c40[k][j];ca+=c40[i][k]*a40[k][j]}
    need(3*aa-cc===120*a40[i][j]&&ac+ca===40*c40[i][j],"H squared equals ten H");
  }
  function rankmod(M,prime=101){
    let m=M.map(r=>r.map(x=>(x%prime+prime)%prime)),p=0;
    function inv(x){let y=1;for(let k=0;k<prime-2;k++)y=y*x%prime;return y}
    for(let j=0;j<m[0].length&&p<m.length;j++){
      let q=p;while(q<m.length&&!m[q][j])q++;if(q===m.length)continue;[m[p],m[q]]=[m[q],m[p]];let z=inv(m[p][j]);m[p]=m[p].map(x=>x*z%prime);
      for(let q=p+1;q<m.length;q++){let z=m[q][j];if(z)m[q]=m[q].map((x,k)=>(x-z*m[p][k]%prime+prime)%prime)}
      p++;
    }return p;
  }
  need(rankmod(a40)===8&&rankmod(c40)===8,"canonical rational rank eight lower witnesses");
  const B=a40.map((r,i)=>r.map((a,j)=>+(i!==j&&a===0&&c40[i][j]===0)));
  for(let i=0;i<40;i++){
    need(B[i].reduce((a,b)=>a+b,0)===12,"degree twelve");
    for(let j=0;j<40;j++)need(B[i].reduce((z,x,k)=>z+x*B[k][j],0)===(i===j?12:B[i][j]?2:4),"GQ parameters");
  }
  const dual=B.map((r,i)=>r.map((x,j)=>2*(i===j)-x));need(rankmod(dual)===16,"dual rank16 lower witness");
  // Finite check of every one of the 81 phase assignments on each pencil.
  let minimum=9;
  for(const q of qs.values())for(let code=0;code<81;code++){
    let z=code,ph=[];for(let k=0;k<4;k++){ph.push(z%3);z=Math.floor(z/3)}
    let b=0;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)b+=+(A[cyc[q.classes[i]][ph[i]]][cyc[q.classes[j]][ph[j]]]===0);
    need(b>=1,"pigeonhole control");minimum=Math.min(minimum,b);
  }
  return {status:"PASS_JS_RECOVERY_EISENSTEIN_CONTACT_GATE",source_commit:"12b269a98e461ebf5e83e24cc16765540bec9626",source_path:"research/moonshot-005-program/results/eisenstein-cycle-native/author/SYMMETRY.json",source_git_blob:"8b0fc7779990f0a3ad15494af97f082be3592944",field:"Q(theta),theta^2=-3",H:"A/4+theta C/12",A40:a40,C40:c40,rankH:4,H_squared:"10H",canonical_rankG:8,canonical_rankB:8,orthogonal_pairs:orth,nonorthogonal_pair_gains:gain,pencils:[...qs.values()],universal_bad_unordered_contacts_lower_bound:90,canonical_bad_contacts:gain.filter(x=>x[2]===0).length,all_pencil_phase_assignments_checked:90*81,minimum_per_pencil:minimum,hermitian_graph:[40,12,2,4],canonical_dual_fitting_rank:16,movement_lower_bound_claimed:false,no_new_kappa:true};
}

if (typeof module !== "undefined") {
  module.exports={check};
  if (require.main===module) {
    const fs=require("fs"),crypto=require("crypto");
    if(process.argv.length!==3) throw Error("usage: node check.js PATH_TO_PINNED_SYMMETRY_JSON");
    const raw=fs.readFileSync(process.argv[2]);
    if(crypto.createHash("sha256").update(raw).digest("hex")!=="ffe061f5986a5982a18fca2ff479447db06cf22b5a8db6bd305c8de3c11315cf") throw Error("source SHA-256 mismatch");
    process.stdout.write(JSON.stringify(check(JSON.parse(raw.toString("utf8"))),null,2)+"\n");
  }
}
