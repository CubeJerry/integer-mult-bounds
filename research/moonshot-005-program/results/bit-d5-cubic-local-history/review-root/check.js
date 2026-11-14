
function reviewD5(flat, recovered) {
 const need=(x,m)=>{if(!x)throw Error(m)};
 const sig=flat.full_roots.map((_,i)=>flat.independent_generators.map(g=>Number(g.full_frame0.includes(i)!==g.full_frame1.includes(i))).join(""));
 need(new Set(sig).size===120,"unique full signatures");
 const R=Array.from({length:111},(_,i)=>{const s=flat.independent_generators.map(g=>Number(g.native_difference.includes(i))).join("");const j=sig.indexOf(s);need(j>=0,"native signature");return flat.full_roots[j]});
 need(JSON.stringify(R)===JSON.stringify(recovered.native_roots),"independent source recovery");
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 function rank2(rows){const b=new Map();for(let x of rows){x=BigInt(x);while(x){const p=x&-x;if(b.has(p))x^=b.get(p);else{b.set(p,x);break;}}}return b.size;}
 const frame=[0,1,2,4,8,14,30,59];
 const G=frame.map(i=>frame.map(j=>((dot(R[i],R[j])/2)%2+2)%2));
 const inverse=G.map((r,i)=>r.concat(Array.from({length:8},(_,j)=>+(i===j))));
 for(let c=0;c<8;c++){let a=c;while(a<8&&!inverse[a][c])a++;need(a<8,"nonsingular binary frame");[inverse[a],inverse[c]]=[inverse[c],inverse[a]];for(let k=0;k<8;k++)if(k!==c&&inverse[k][c])inverse[k]=inverse[k].map((x,j)=>x^inverse[c][j]);}
 const X=R.map(r=>{const v=frame.map(j=>((dot(r,R[j])/2)%2+2)%2);return inverse.reduce((n,row,k)=>n|((row.slice(8).reduce((a,x,j)=>a^(x&v[j]),0))<<k),0)});
 need(new Set(X).size===111,"distinct native binary coordinates");
 const D=R.flatMap((r,i)=>[92,54,38].every(k=>dot(r,R[k])===0)?[i]:[]);
 need(D.length===18,"D cardinality");
 const dset=new Set(D),all=(1n<<111n)-1n,dm=D.reduce((s,i)=>s|(1n<<BigInt(i)),0n);
 const pop=x=>x.toString(2).split("1").length-1,poly=degree=>Array.from({length:256},(_,m)=>m).filter(m=>pop(m)<=degree).map(m=>X.reduce((b,x,i)=>((m&x)===m)?b|(1n<<BigInt(i)):b,0n));
 const Q3=poly(3),Q2=poly(2),C=poly(1);
 const qr=[rank2(Q3),rank2(Q3.map(x=>x&(all^dm))),rank2(Q2),rank2(Q2.map(x=>x&(all^dm)))];
 need(qr.join(",")==="84,79,36,36","polynomial shortening ranks");
 const axes=[[1,0,1,0,1,-2,-1,0],[1,0,1,0,-1,0,1,-2],[1,0,-1,-2,-1,0,-1,0],[1,2,-1,0,1,0,1,0],[1,-2,-1,0,1,0,1,0]];
 need(axes.every((a,i)=>axes.every((b,j)=>dot(a,b)===(i===j?8:0))),"orthogonal D5 axes");
 const edges=[];for(let a=0;a<5;a++)for(let b=a+1;b<5;b++)edges.push([a,b]);
 const edgeOf=D.map(i=>{const z=axes.map(a=>dot(R[i],a)/4);need(z.filter(x=>x).length===2&&z.every(x=>[-1,0,1].includes(x)),"D5 root");return edges.findIndex(([a,b])=>z[a]&&z[b]);});
 const columns=edges.map(([a,b])=>31^(1<<a)^(1<<b));
 need(rank2(columns)===5,"R10 rank");
 const edgeWords=[],words=[],weight={};
 for(let m=0;m<1024;m++){let h=0;for(let e=0;e<10;e++)if(m>>e&1)h^=columns[e];if(h)continue;edgeWords.push(m);weight[pop(m)]=(weight[pop(m)]||0)+1;words.push(D.reduce((x,i,k)=>(m>>edgeOf[k]&1)?x|(1n<<BigInt(i)):x,0n));}
 need(edgeWords.length===32&&new Set(words).size===32,"R10 puncture injective");
 need(JSON.stringify(weight)===JSON.stringify({0:1,4:15,6:15,10:1}),"R10 weight distribution");
 need(words.every(w=>rank2(Q3.concat(w))===84),"R10 lies in cubic shortening");
 const Z=[];for(const w of words)if(rank2(Z.concat(w))>Z.length)Z.push(w);
 need(Z.length===5,"R10 dimension");

 const prime=107,invs=Array.from({length:prime},(_,a)=>{for(let j=1;j<prime;j++)if(a*j%prime===1)return j;return 0});
 function rankp(rows){const b=[];for(let row of rows){let r=row.map(x=>(x%prime+prime)%prime);for(let c=0;c<r.length;c++)if(r[c]){if(b[c]){const z=r[c];r=r.map((x,j)=>(x-z*b[c][j]%prime+prime)%prime);}else{const z=invs[r[c]];b[c]=r.map(x=>x*z%prime);break;}}}return b.filter(Boolean).length;}
 const qev=r=>{const z=[];for(let a=0;a<8;a++)for(let b=a;b<8;b++)z.push(r[a]*r[b]);return z};
 const cert=[],local=[],hist={};let ownZero=0;
 for(let i=0;i<111;i++){
   const nz=R.flatMap((r,j)=>j!==i&&!dset.has(j)&&dot(r,R[i])!==0?[j]:[]);
   const foreign=R.flatMap((r,j)=>j!==i&&!dset.has(j)&&dot(r,R[i])===0?[j]:[]);
   const canonrank=rank2(nz.map(j=>256|X[j])),quad=rankp(foreign.map(j=>qev(R[j])));
   need(canonrank===8&&quad===28,"outside constraints at "+i);
   const zero=R.reduce((m,r,j)=>j!==i&&dot(r,R[i])!==0?m|(1n<<BigInt(j)):m,0n);
   const cr=C.map(c=>c&zero),base=rank2(cr),ids=[];
   for(let m=0;m<32;m++){let z=0n;for(let k=0;k<5;k++)if(m>>k&1)z^=Z[k];if(rank2(cr.concat(z&zero))===base)ids.push(m);}
   if(dset.has(i)){need(ids.length===1,"D-local own zero");ownZero++;}
   const dim=Math.log2(ids.length);hist[dim]=(hist[dim]||0)+1;local.push({role:i,dimension:dim,members:ids});
   cert.push({role:i,canonical_restriction_rank:canonrank,foreign_count:foreign.length,quadratic_rank_mod107:quad});
 }
 need(JSON.stringify(hist)===JSON.stringify({0:77,2:28,5:6}),"local dimension histogram");
 const bit=(x,i)=>Number(x>>BigInt(i)&1n),carriers=Z.every(z=>bit(z,1)===bit(z,18));need(carriers,"carrier equality");
 const blocks=[[[0,1],[0,0]],[[0,0],[1,0]],[[1,1],[0,1]],[[1,0],[1,1]],[[1,0],[0,1]]];
 const Zrows=[0n,0n];for(let a=0;a<2;a++)for(let j=0;j<111;j++)for(let b=0;b<2;b++){let s=0;for(let k=0;k<5;k++)s^=bit(Z[k],j)&blocks[k][a][b];if(s)Zrows[a]|=1n<<BigInt(2*j+b);}
 const T=Array.from({length:222},(_,i)=>(1n<<BigInt(i))^([2,3,36,37].includes(i)?Zrows[i%2]:0n));
 const times=(row,M)=>{let y=0n;for(let i=0;i<M.length;i++)if(bit(row,i))y^=M[i];return y};
 need(T.every((r,i)=>times(r,T)===(1n<<BigInt(i))),"noncommuting block involution");
 need(Zrows.every(r=>times(r,T)===r),"mode invariant after recoding");
 const unequal=Array.from({length:222},(_,i)=>(1n<<BigInt(i))^([2,3,36,37].includes(i)?(1n<<BigInt(2+i%2)):0n));
 const badRejected=unequal.some((r,i)=>times(r,unequal)!==(1n<<BigInt(i)));
 need(badRejected,"unequal-carrier control");
 return {status:"PASS_ROOT_D5_LOCAL_HISTORY_REVIEW",source:"Independent 84-signature recovery, compared to derived native roots; no fresh gzip replay",D,polynomial_ranks:qr,R10:{columns,rank:5,code_dimension:5,weight_distribution:weight,punctured_words_distinct:32},basis:Z.map(z=>D.filter(i=>bit(z,i))),outside_certificates:cert,local_dimension_histogram:hist,local_receiver_data:local,own_local_zero_rows:ownZero,field_for_quadratic_minors:prime,block_carrier:{width:2,noncommuting_coefficients:true,involution:true,mode_invariant:true},negative_controls:{single_unit_rejected:!words.includes(1n<<1n),single_edge_rejected:!words.includes((1n<<1n)|(1n<<18n)),unequal_carrier_rejected:badRejected},new_complete_kappa:false};
}

if(typeof module!=="undefined")module.exports={reviewD5};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto");
 const read=(path,pin)=>{const raw=fs.readFileSync(path);if(crypto.createHash("sha256").update(raw).digest("hex")!==pin)throw Error("Source SHA256 mismatch");return JSON.parse(raw.toString("utf8"));};
 if(process.argv.length!==4)throw Error("usage: node check.js FLAT-CUBIC-RESULT.json SOURCE-RECOVERY.json");
 const flat=read(process.argv[2],"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc");
 const geo=read(process.argv[3],"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e");
 console.log(JSON.stringify(reviewD5(flat,geo),null,2));
}
