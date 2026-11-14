function reviewMatchedD5(g,flat){
 const R=g.native_roots,N=111,all=(1n<<111n)-1n,bit=i=>1n<<BigInt(i),dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),need=(x,s)=>{if(!x)throw Error(s)};
 function basis(rows){const m=new Map();for(let x of rows){while(x){const k=x.toString(2).length-1;if(m.has(k))x^=m.get(k);else{m.set(k,x);break}}}return[...m.values()]}
 function kernel(rows,mask){const m=new Map(),out=[];for(let row of rows){let x=row&mask,y=row;while(x){const k=x.toString(2).length-1;if(m.has(k)){const [u,v]=m.get(k);x^=u;y^=v}else{m.set(k,[x,y]);break}}if(!x&&y)out.push(y)}return basis(out)}
 const ids=x=>Array.from({length:N},(_,i)=>i).filter(i=>x&bit(i)),mask=xs=>xs.reduce((a,i)=>a|bit(i),0n);
 const K=R.map((r,i)=>mask(R.map((v,j)=>i===j||dot(r,v)===0?j:-1).filter(j=>j>=0))),C=basis(K),products=[];
 for(let i=0;i<C.length;i++)for(let j=i;j<C.length;j++)for(let k=j;k<C.length;k++)products.push(C[i]&C[j]&C[k]);const Q=basis(products);need(C.length===9&&Q.length===84,"canonical and cubic codes");
 const simple=[[0,0,0,0,2,0,0,0],[-1,1,0,0,-1,1,0,0],[1,-1,0,0,0,0,-1,-1],[0,0,1,-1,0,0,1,1],[-1,0,-1,0,0,-1,0,-1]];
 need(simple.every((r,i)=>simple.every((v,j)=>dot(r,v)===(i===j?4:Math.abs(i-j)===1?-2:0))),"A5 Gram");
 const root=(i,j)=>simple.slice(i,j).reduce((a,v)=>a.map((x,k)=>x+v[k]),Array(8).fill(0));
 const edges=[];for(let i=0;i<6;i++)for(let j=i+1;j<6;j++)edges.push([i,j]);
 const banks=edges.map(e=>{const vertices=Array.from({length:6},(_,i)=>i).filter(i=>!e.includes(i)),norm=vertices.slice(1).map(i=>root(vertices[0],i)),cohort=R.map((r,i)=>norm.every(v=>dot(r,v)===0)?i:-1).filter(i=>i>=0),m=mask(cohort);return{edge:e,cohort,mask:m,code:kernel(Q,all^m)}});need(banks.every(b=>b.code.length===5),"local dimension5");
 const I=mask([23,61]);for(let i=0;i<15;i++)for(let j=i+1;j<15;j++)need(((banks[i].mask&banks[j].mask&~I)===0n)===(banks[i].edge.every(x=>!banks[j].edge.includes(x))),"105 matching incidences");
 const matchings=[];function rec(left,chosen){if(!left.length){matchings.push(chosen);return}const a=left[0];for(const b of left.slice(1)){const k=edges.findIndex(e=>e[0]===a&&e[1]===b);rec(left.filter(x=>x!==a&&x!==b),chosen.concat(k))}}rec([0,1,2,3,4,5],[]);need(matchings.length===15,"all perfect matchings");

 const p=107,inv=x=>{let z=1;for(let i=0;i<p-2;i++)z=z*x%p;return z},rr=rows=>{const a=rows.map(r=>r.map(x=>(x%p+p)%p));let k=0;for(let j=0;j<(a[0]?.length||0)&&k<a.length;j++){let t=k;while(t<a.length&&!a[t][j])t++;if(t===a.length)continue;[a[k],a[t]]=[a[t],a[k]];const u=inv(a[k][j]);a[k]=a[k].map(x=>x*u%p);for(let l=k+1;l<a.length;l++){const c=a[l][j];if(c)a[l]=a[l].map((x,z)=>(x-c*a[k][z]%p+p)%p)}k++}return k};
 const canonical=r=>{const x=r.find(x=>x);return (x<0?r.map(x=>-x):r).join(",")},a5=new Set(edges.map(([i,j])=>canonical(root(i,j)))),full=flat.full_roots;need(a5.size===15&&full.filter(r=>rr([...simple,r])===5).length===15,"complete A5 normal root system");need(full.filter(r=>rr([...simple,r])===5).every(r=>a5.has(canonical(r))),"all normal roots");
 need(banks.reduce((a,b)=>a&b.mask,all)===I,"common native coordinates");
 const quadratic=r=>{const v=[];for(let i=0;i<8;i++)for(let j=i;j<8;j++)v.push(r[i]*r[j]);return v};
 const findings=[];for(const m of matchings){const S=basis([...C,...m.flatMap(i=>banks[i].code),bit(23),bit(61)]);need(S.length===26,"granted code dimension26");let chi=0,forcedRows=[];for(let i=0;i<N;i++){const forbidden=mask(R.map((r,j)=>j===i||dot(R[i],r)!==0?j:-1).filter(j=>j>=0)),H=kernel(S,forbidden),movable=H.reduce((a,x)=>a|x,0n),forced=(K[i]^bit(i))&~movable,rs=ids(forced).map(j=>R[j]),lr=rr(rs),qr=rr(rs.map(quadratic)),lower=qr===28?2:lr===7?1:0;chi+=lower;forcedRows.push({receiver:i,identity_columns:ids(forced),linear_lower:lr,quadratic_lower:qr,charge_lower:lower})}findings.push({matching:m,edges:m.map(i=>edges[i]),source_union:ids(m.reduce((a,i)=>a|banks[i].mask,0n)).length,charge_lower:chi,forced_rows:forcedRows})}
 const minimum=Math.min(...findings.map(x=>x.charge_lower));need(minimum===197,"exact matching lower bound197");
 const overlap=basis([...C,...banks.flatMap(b=>b.code)]);need(overlap.length===64&&basis([...overlap,bit(23),bit(61)]).length===66,"overlap scope control");
 return{status:"PASS_ROOT_MATCHED_D5_GATE",prime:p,banks:15,pairs:105,matchings:15,forced_rows:1665,local_code_dimension:5,granted_code_dimension:26,lower_bounds:findings.map(x=>x.charge_lower),minimum_charge_lower:minimum,overlap_control_dimensions:[64,66],findings,scope:"Only A3-normal D5 banks at the pinned common chart, disjoint outside I, cubic shortenings plus common-coordinate repairs. Raw or overlapping histories outside scope.",new_kappa:false};
}
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
 const read=(p,pin)=>{const raw=fs.readFileSync(p);if(crypto.createHash("sha256").update(raw).digest("hex")!==pin)throw Error("Source SHA256 mismatch: "+p);return JSON.parse(raw.toString("utf8"))};
 if(process.argv.length!==4)throw Error("Usage: node check.js FLAT-CUBIC-RESULT.json SOURCE-RECOVERY.json");
 const flat=read(process.argv[2],"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc"),geo=read(process.argv[3],"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e");
 console.log(JSON.stringify(reviewMatchedD5(geo,flat),null,2));
}
