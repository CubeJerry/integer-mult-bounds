
function reviewDegreeFour(){
 const p=5,need=(v,m)=>{if(!v)throw Error(m)},mod=x=>(x%p+p)%p,mul=(A,B)=>A.map(r=>B[0].map((_,j)=>mod(r.reduce((s,x,k)=>s+x*B[k][j],0)))),eq=(A,B)=>JSON.stringify(A)===JSON.stringify(B),I=[[1,0],[0,1]],rank2=A=>{const d=mod(A[0][0]*A[1][1]-A[0][1]*A[1][0]);return d?2:A.flat().some(Boolean)?1:0};
 let good=0;for(let a=0;a<p;a++)for(let b=0;b<p;b++)for(let c=0;c<p;c++)for(let d=0;d<p;d++){const X=[[a,b],[c,d]],Y=I.map((r,i)=>r.map((x,j)=>mod(x-X[i][j]))),idem=eq(mul(X,X),X);need((rank2(X)+rank2(Y)===2)===idem,"rank idempotence");if(idem)good++;}
 need(rank2([[0,1],[0,0]])===1&&rank2([[1,4],[0,1]])===2,"nilpotent negative control");
 const inverse=A=>{const det=mod(A[0][0]*A[1][1]-A[0][1]*A[1][0]);let iv=1;while(mod(iv*det)!==1)iv++;return [[A[1][1],-A[0][1]],[-A[1][0],A[0][0]]].map(r=>r.map(x=>mod(x*iv)))};
 const edges=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)edges.push([a,b]);
 const row=Array.from({length:5},(_,a)=>Array.from({length:6},(_,j)=>+(j===a))).concat(edges.map(([a,b])=>Array.from({length:6},(_,j)=>+(j===a||j===b||j===5))));
 const col=row.map((r,i)=>r.map((x,j)=>i>=5&&j===5?-x:x));
 const G=row.map((_,i)=>mul([[1,mod(i)],[0,1]],[[1,0],[mod(i*i+1),1]])),Gi=G.map(inverse);
 const blocks=row.map((r,i)=>col.map((s,j)=>{const z=mod(r.reduce((t,x,k)=>t+x*s[k],0));return mul(G[i],Gi[j]).map(v=>v.map(x=>mod(z*x)))}));
 for(let i=0;i<15;i++)need(eq(blocks[i][i],I),"diagonal");
 let zeros=0;for(let i=0;i<15;i++)for(let j=0;j<15;j++){let forbidden=false;if(i<5&&j<5)forbidden=i!==j;else if(i<5)forbidden=!edges[j-5].includes(i);else if(j<5)forbidden=!edges[i-5].includes(j);else forbidden=i!==j&&edges[i-5].some(a=>edges[j-5].includes(a));if(forbidden){need(blocks[i][j].flat().every(x=>!x),"mask");zeros++;}}
 const M=Array.from({length:30},(_,i)=>Array.from({length:30},(_,j)=>blocks[i>>1][j>>1][i&1][j&1]));
 let r=0;for(let c=0;c<30&&r<30;c++){let s=r;while(s<30&&!M[s][c])s++;if(s===30)continue;[M[r],M[s]]=[M[s],M[r]];let iv=1;while(mod(iv*M[r][c])!==1)iv++;M[r]=M[r].map(x=>mod(x*iv));for(let i=r+1;i<30;i++){const k=M[i][c];M[i]=M[i].map((x,j)=>mod(x-k*M[r][j]));}r++;}
 need(r===12,"degree4 saturated rank");
 const noncommuting=G.some(A=>G.some(B=>!eq(mul(A,B),mul(B,A))));need(noncommuting,"noncommuting vertex gauges");
 for(let e=0;e<10;e++){const S=mul(G[5+e],Gi[5+e].map(r=>r.map(x=>mod(-x))));need(eq(S,[[4,0],[0,4]]),"intrinsic Schur minusI");}
 return{status:"PASS_INDEPENDENT_DEGREE_FOUR_EQUALITY_CONTROLS",idempotent_check:{field:5,dimension:2,matrices:625,idempotents:good},positive_control:{graph:"K5",minimum_degree:4,width:2,field:5,rank:r,expected_rank:12,noncommuting_vertex_gauges:true,forced_zero_blocks:zeros,all_intrinsic_S:"-I"},negative_control:"nonzero nilpotent [[0,1],[0,0]] has rank1 plus complement rank2, so does not meet the idempotent equality",universal_status:"written proof independently reviewed; finite controls are supplementary",no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewDegreeFour};
 if(require.main===module){
  const fs=require("node:fs"),crypto=require("node:crypto"),pins=[];
  if(process.argv.length!==pins.length+2)throw Error("supply the authenticated input paths in README order");
  const raws=process.argv.slice(2).map(x=>fs.readFileSync(x));
  raws.forEach((b,i)=>{if(crypto.createHash("sha256").update(b).digest("hex")!==pins[i])throw Error("input SHA256 mismatch "+i)});
  process.stdout.write(JSON.stringify(reviewDegreeFour(),null,2)+"\n");
 }
}
