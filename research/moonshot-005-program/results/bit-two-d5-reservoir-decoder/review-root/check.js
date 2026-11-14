
function reviewTwoBank(word,flat){
 const need=(b,m)=>{if(!b)throw Error(m)},gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r}return a},
 Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}const g=gcd(n,d);return[n/g,d/g]},
 add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]),div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]),zero=()=>Q(0);
 function rref(input){const A=input.map(r=>r.map(x=>Array.isArray(x)?Q(x[0],x[1]):Q(x))),piv=[];let r=0;for(let c=0;c<8&&r<A.length;c++){let s=r;while(s<A.length&&!A[s][c][0])s++;if(s===A.length)continue;[A[r],A[s]]=[A[s],A[r]];const z=A[r][c];A[r]=A[r].map(x=>div(x,z));for(let i=0;i<A.length;i++)if(i!==r&&A[i][c][0]){const w=A[i][c];A[i]=A[i].map((x,j)=>add(x,neg(mul(w,A[r][j]))));}piv.push(c);r++;}return{rows:A.slice(0,r),piv};}
 const nullspace=input=>{const a=rref(input);return Array.from({length:8},(_,j)=>j).filter(j=>!a.piv.includes(j)).map(j=>{const v=Array.from({length:8},zero);v[j]=Q(1);a.piv.forEach((p,k)=>v[p]=neg(a.rows[k][j]));return v})};
 const canon=input=>rref(input).rows,serialize=B=>JSON.stringify(B.map(r=>r.map(x=>x[0]+"/"+x[1]))),signatures=flat.full_roots.map((_,i)=>flat.independent_generators.map(w=>+(w.full_frame0.includes(i)!==w.full_frame1.includes(i))).join(""));
 need(new Set(signatures).size===120,"root signatures");const mapping=Array.from({length:111},(_,i)=>signatures.indexOf(flat.independent_generators.map(w=>+w.native_difference.includes(i)).join("")));need(mapping.every(x=>x>=0)&&new Set(mapping).size===111,"native mapping");const R=mapping.map(i=>flat.full_roots[i]);
 const chart={};for(const[name,c]of Object.entries(word.charts)){need(["ann","span"].includes(c.kind)&&c.rows.every(r=>r.length===8&&r.every(Number.isSafeInteger)),"chart syntax");
 if(c.normal_roles)need(JSON.stringify(c.rows)===JSON.stringify(c.normal_roles.map(i=>R[i])),"normal source");
 if(c.source_roles)need(JSON.stringify(c.rows)===JSON.stringify(c.source_roles.map(i=>R[i])),"span source");
 if(c.source_expressions)need(JSON.stringify(c.rows)===JSON.stringify(c.source_expressions.map(e=>Array.from({length:8},(_,j)=>e.reduce((s,[i,a])=>s+a*R[i][j],0)))),"linear source expressions");
 const B=canon(c.kind==="span"?c.rows:nullspace(c.rows));chart[name]={B,dim:B.length,key:serialize(B)};}
 for(let i=0;i<111;i++){need(chart["L"+i].key===serialize(canon([R[i]])),"original source line");need(chart["F"+i].key===serialize(canon(nullspace([R[i]]))),"original target facet");}
 need(chart.zero.dim===0&&chart.Hub.dim===8,"ground and Hub");
 const inclusion=new Map(),subset=(a,b)=>{const key=a+" -> "+b;if(!inclusion.has(key))inclusion.set(key,canon(chart[a].B.concat(chart[b].B)).length===chart[b].dim);return inclusion.get(key)},same=(a,b)=>chart[a].key===chart[b].key;

 const fields=new Map(),bit=i=>1n<<BigInt(i),profile={},counts={},owners=new Map(),retired=[],history=[],snapshots={};
 for(let i=0;i<111;i++){fields.set("X"+i,{chart:"L"+i,v:bit(i),owned:false});fields.set("Y"+i,{chart:"zero",v:bit(111+i),owned:false});}
 const rankBinary=rows=>{const piv=new Map();for(let x of rows){while(x){const k=x&-x;if(piv.has(k))x^=piv.get(k);else{piv.set(k,x);break;}}}return piv.size},xmask=bit(111)-1n;let peak=0,packetsPure=true;
 for(let index=0;index<word.operations.length;index++){
 const [op,a,b]=word.operations[index];counts[op]=(counts[op]||0)+1;
 if(op==="INIT"){need(!fields.has(a)&&chart[b],"new zero owner");fields.set(a,{chart:b,v:0n,owned:true});owners.set(a,{birth:index,birth_chart:b,path:[chart[b].dim],moves:0});peak=Math.max(peak,[...fields.values()].filter(x=>x.owned).length);
 if(a==="P"||a==="Q")for(let i=0;i<111;i++)need(fields.get("X"+i).v===bit(i),"all X restored before packet birth");}
 else if(op==="MOVE"){const x=fields.get(a);need(x&&chart[b],"known MOVE");need(x.owned?subset(b,x.chart):subset(x.chart,b),"illegal "+a+" "+x.chart+" -> "+b+" at "+index);const d=Math.abs(chart[x.chart].dim-chart[b].dim);need(d>0,"positive MOVE rank");profile[d]=(profile[d]||0)+1;x.chart=b;if(x.owned){owners.get(a).path.push(chart[b].dim);owners.get(a).moves++;}}
 else if(op==="ADD"){const x=fields.get(a),y=fields.get(b);need(x&&y&&a!==b&&same(x.chart,y.chart),"cocharted ADD at "+index);y.v^=x.v;}
 else if(op==="CLEAR"){const x=fields.get(a);need(x?.owned,"owned clear");retired.push({role:a,chart:x.chart,rank:chart[x.chart].dim,dirty:x.v!==0n,value:x.v.toString(16),...owners.get(a)});fields.delete(a);}
 else throw Error("unknown operation");
 for(const a of["P","Q"]){const x=fields.get(a);if(x&&!same(x.chart,"Hub")){history.push(x.v&xmask);if(x.v>>111n)packetsPure=false;}}
 for(const [name,n]of Object.entries(word.markers||{}))if(index+1===n){const complete=Array.from({length:111},(_,i)=>i).filter(i=>fields.get("Y"+i).v===(bit(111+i)^bit(i))&&same(fields.get("Y"+i).chart,"F"+i));snapshots[name]={after:index+1,completed:complete,packet_values:Object.fromEntries(["P","Q"].filter(x=>fields.has(x)).map(x=>[x,fields.get(x).v.toString(16)])),live_owners:[...fields].filter(([_,x])=>x.owned).map(([name,x])=>({name,chart:x.chart,value:x.v.toString(16)})),history_rank:rankBinary(history)};}
 }

 const dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0),D1=R.flatMap((r,i)=>[92,54,38].every(j=>dot(r,R[j])===0)?[i]:[]),D2=R.flatMap((r,i)=>[1,18,31].every(j=>dot(r,R[j])===0)?[i]:[]),L=[5,12,15,22,26,30,34,40,47,50,58,64,76,77,93,106];
 const mask=ids=>ids.reduce((x,i)=>x^bit(i),0n),a=mask(D1)^bit(72),b=mask(D2)^bit(72),f=mask(L),c=a^b^bit(72)^f,g=mask(R.flatMap((r,j)=>j===92||dot(r,R[92])===0?[j]:[])),moved=Array.from({length:111},(_,i)=>i).filter(i=>(c|g)&bit(i));
 need(moved.length===81&&JSON.stringify(moved)===JSON.stringify(word.moved_original_sources),"actual source union");
 need(chart.D1.dim===5&&chart.D2.dim===5&&chart.I.dim===2&&chart.E.dim===6,"source/decoder chart ranks");
 const q=[0,0,1,1,0,0,1,-1];need(chart.E.key===serialize(canon(nullspace([R[72],q]))),"exact correction chart");
 const expected=word.closed_partial?{}:{A:["D1",a],B:["D2",b],P:["zero",bit(72)^f],Q:["zero",g^b]};
 if(!word.closed_partial)for(const i of moved)if(i!==72)expected["R"+i]=["L"+i,bit(i)];
 const live=[...fields].filter(([_,x])=>x.owned);need(live.length===Object.keys(expected).length,"actual live inventory");
 for(const [name,[chartName,value]]of Object.entries(expected)){const x=fields.get(name);need(x&&x.v===value&&same(x.chart,chartName),"retained value "+name);}

 for(let i=0;i<111;i++){const x=fields.get("X"+i),y=fields.get("Y"+i);need(x.v===bit(i),"X restored "+i);need(y.v===(bit(111+i)^(i===72?bit(72):0n)),"Y endpoint "+i);need(same(x.chart,word.closed_partial||moved.includes(i)?"Hub":"L"+i),"X endpoint chart "+i);need(same(y.chart,word.closed_partial||i===72?"F"+i:"zero"),"Y endpoint chart "+i);}
 const moving=[...owners].filter(([_,x])=>x.moves);need(moving.length===2&&moving.every(([n])=>n==="P"||n==="Q"),"only two continuous owned movers");
 need(["P","Q"].every(n=>owners.get(n).path.join(",")==="8,5,2,0"),"actual packet paths");
 need(rankBinary(history)===4,"carried history rank");
 return{status:"PASS_ROOT_TWO_D5_DECODER_WORD",field_columns:222,completed_targets:[72],closed_partial:word.closed_partial,moved_original_sources:moved,untouched_original_sources:111-moved.length,counts,profile,rank_length:Object.entries(profile).reduce((s,[r,c])=>s+Number(r)*c,0),peak_owners:peak,live_owners:live.map(([name,x])=>({name,chart:x.chart,value:x.v.toString(16)})),retirements:retired,packet_paths:Object.fromEntries(["P","Q"].map(n=>[n,owners.get(n).path])),X_projection_history_rank:rankBinary(history),packets_always_pure_X:packetsPure,snapshots,source_method:"Independent84-signature recovery and rational chart bases",productive_complete_supplier:false,new_complete_kappa:false};
}
function reviewTwoBankNegatives(base,flat){
 const tests=[
 ["single source lost from first reservoir",w=>{const k=w.operations.findIndex(o=>o[0]==="ADD"&&o[1]==="X1"&&o[2]==="A");w.operations.splice(k,1)}],
 ["reverse packet cancellation",w=>{const k=w.operations.findIndex(o=>o.join(",")==="ADD,Q,P");w.operations[k]=["ADD","P","Q"]}],
 ["use original after it left its line",w=>{const k=w.operations.findIndex(o=>o.join(",")==="ADD,X1,R1");w.operations.splice(k,1);const j=w.operations.findIndex(o=>o.join(",")==="MOVE,X1,Hub");w.operations.splice(j+1,0,["ADD","X1","R1"])}],
 ["retire live second packet before meeting",w=>{const k=w.operations.findIndex(o=>o.join(",")==="MOVE,Q,I");w.operations.splice(k+1,0,["CLEAR","Q"])}],
 ["foreign correction has wrong receiver",w=>{const k=w.operations.findIndex(o=>o.join(",")==="ADD,F,Y72");w.operations[k]=["ADD","F","Y71"]}]
 ];const receipt=[];for(const[name,mutate]of tests){const w=JSON.parse(JSON.stringify(base));mutate(w);let error;try{reviewTwoBank(w,flat)}catch(e){error=String(e.message)}if(!error)throw Error("Negative control passed: "+name);receipt.push({name,status:"REJECTED",reason:error})}return receipt;
}function reviewNativeInvoice(profile){
 const S=10n**30n,cache={};function r(n){if(cache[n])return cache[n];if(n===0)return[0n,0n];const t=BigInt(n)**199n*S**200n;let lo=0n,hi=BigInt(n)*S;while(lo<hi){const mid=(lo+hi+1n)>>1n;if(mid**200n<=t)lo=mid;else hi=mid-1n}return cache[n]=[lo,lo**200n===t?lo:lo+1n]}
 function sum(terms){let a=0n,b=0n;for(const[n,c]of terms){const[x,y]=r(n),z=BigInt(c);a+=z>=0n?z*x:z*y;b+=z>=0n?z*y:z*x}return[a,b]}
 const terms=Object.entries(profile).map(([n,c])=>[+n,c]),mom=sum(terms),allowTerms=[[127,37],[64,74],[1,-74]];for(let j=1;j<=8;j++)allowTerms.push([1+7*j,74],[7*j,-74]);const allow=sum(allowTerms);
 const fmt=x=>x.map(String),margins={};for(const q of[7,8])margins[q]=fmt(sum([...allowTerms,...terms.map(([n,c])=>[n,-6*c]),[8,-6*q]]));
 return{status:"PASS_INDEPENDENT_PARTIAL_INVOICE",scale:String(S),moment_numerator:fmt(mom),allowance_denominator:6,allowance_numerator:fmt(allow),bare_additional_lifetimes:margins,margin_denominator:6,scope:"Only this closed partial word; extra lifetimes omit all source, corrections, retirement and restoration operations. No complete supplier."};
}
function reviewCoupledDirection(geo) {
 const R=geo.native_roots,need=(x,m)=>{if(!x)throw Error(m)},bit=i=>1n<<BigInt(i),dot=(a,b)=>a.reduce((s,x,j)=>s+x*b[j],0);
 const rk=rows=>{const b=new Map();for(let x of rows)while(x){const t=x&-x;if(b.has(t))x^=b.get(t);else{b.set(t,x);break;}}return b.size;};
 const K=R.map((r,i)=>R.reduce((x,s,j)=>i===j||dot(r,s)===0?x|bit(j):x,0n)),all=(1n<<111n)-1n;
 const z=K[92]&K[54]&K[38],zz=K[1]&K[18]&K[31],d=z^zz,cert=[];
 need(rk(K)===9&&rk(K.filter((_,i)=>i!==72))===9&&rk(K.concat(d))===10,"canonical ranks");
 for(let i=0;i<111;i++){const mask=all^K[i],c=K.map(x=>x&mask),r=rk(c),j=rk(c.concat(d&mask));
 need(r===8&&j===(i===72?8:9),"local quotient restriction "+i);
 cert.push({receiver:i,canonical_restriction_rank:r,extended_restriction_rank:j});}
 const L=[5,12,15,22,26,30,34,40,47,50,58,64,76,77,93,106],target=L.reduce((x,i)=>x|bit(i),bit(72)),H=K[72]^target;
 need(!(H&bit(72))&&!(H&~K[72])&&rk(K.concat(H,d))===10,"normalized local innovation");
 const tests=[];for(let mask=0;mask<16;mask++){const Z=[[mask&1,(mask>>1)&1],[(mask>>2)&1,(mask>>3)&1]],isI=mask===9,rankZ=rk(Z.map(r=>BigInt(r[0]|r[1]<<1)));let surviving=0;
 for(let j=0;j<111;j++)if(j!==72&&(K[72]&bit(j))){const h=Number(H>>BigInt(j)&1n);const M=Z.map((row,a)=>row.map((v,b)=>(+(a===b))^(h&v)));if(M.some(row=>row.some(Boolean)))surviving++;}
 need((surviving===16)===isI,"partial block deletion control");tests.push({mask,rank_Z:rankZ,total_fitting_rank:18+rankZ,receiver72_foreign_blocks:surviving,charge:isI?220:222});}
 return{status:"PASS_ROOT_COUPLED_DIRECTION_CLASSIFICATION",canonical_rank_without_receiver72:9,restriction_certificates:cert,only_noncanonical_receiver:72,all_field_block_family:"A_i=K_i tensor I for i!=72; A_72=K_72 tensor I+(K_72+target_72) tensor Z",rank_formula:"9V+rank(Z)",charge_dichotomy:"220 if Z=I;222 otherwise",width2_F2_controls:tests,new_complete_kappa:false};
}

if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
 const read=(p,pin)=>{const raw=fs.readFileSync(p);if(crypto.createHash("sha256").update(raw).digest("hex")!==pin)throw Error("Source SHA256 mismatch: "+p);return JSON.parse(raw.toString("utf8"))};
 if(process.argv.length!==4)throw Error("Usage: node check.js FLAT-CUBIC-RESULT.json SOURCE-RECOVERY.json");
 const flat=read(process.argv[2],"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc"),geo=read(process.argv[3],"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e");
 const prefix=read(path.join(__dirname,"../author/PREFIX.json"),"14c3185fac2cc14516810143aba5c2cd2279056a4ff187acb017a408ad3e2507"),closed=read(path.join(__dirname,"../author/CLOSED.json"),"43d3f98fd126133399917805de6c275f989f98b37a83b7fa2ab18e00a5783f01");const a=reviewTwoBank(prefix,flat),b=reviewTwoBank(closed,flat);console.log(JSON.stringify({prefix:a,closed:b,negative_controls:reviewTwoBankNegatives(prefix,flat),budget:reviewNativeInvoice(b.profile),scaling:reviewCoupledDirection(geo)},null,2));
}
