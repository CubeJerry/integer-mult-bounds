
function reviewPiggyback(word,flat,options={}){
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
 if(a==="P"||a==="Q")for(const i of word.targets){const x=fields.get("X"+i);need(x.v===bit(i)&&same(x.chart,"Hub"),"original restored before Hub packet");}}
 else if(op==="MOVE"){const x=fields.get(a);need(x&&chart[b],"known MOVE");need(x.owned?subset(b,x.chart):subset(x.chart,b),"illegal "+a+" "+x.chart+" -> "+b+" at "+index);const d=Math.abs(chart[x.chart].dim-chart[b].dim);need(d>0,"positive MOVE rank");profile[d]=(profile[d]||0)+1;x.chart=b;if(x.owned){owners.get(a).path.push(chart[b].dim);owners.get(a).moves++;}}
 else if(op==="ADD"){const x=fields.get(a),y=fields.get(b);need(x&&y&&a!==b&&same(x.chart,y.chart),"cocharted ADD at "+index);y.v^=x.v;}
 else if(op==="CLEAR"){const x=fields.get(a);need(x?.owned,"owned clear");retired.push({role:a,chart:x.chart,rank:chart[x.chart].dim,dirty:x.v!==0n,value:x.v.toString(16),...owners.get(a)});fields.delete(a);}
 else throw Error("unknown operation");
 for(const a of["P","Q"]){const x=fields.get(a);if(x&&!same(x.chart,"Hub")){history.push(x.v&xmask);if(x.v>>111n)packetsPure=false;}}
 for(const [name,n]of Object.entries(word.markers||{}))if(index+1===n){const complete=Array.from({length:111},(_,i)=>i).filter(i=>fields.get("Y"+i).v===(bit(111+i)^bit(i))&&same(fields.get("Y"+i).chart,"F"+i));snapshots[name]={after:index+1,completed:complete,packet_values:Object.fromEntries(["P","Q"].filter(x=>fields.has(x)).map(x=>[x,fields.get(x).v.toString(16)])),live_owners:[...fields].filter(([_,x])=>x.owned).map(([name,x])=>({name,chart:x.chart,value:x.v.toString(16)})),history_rank:rankBinary(history)};}
 }
 const remainingOwners=[...fields].filter(([_,x])=>x.owned);need(!remainingOwners.length,"all owners retired");
 const done=[];for(let i=0;i<111;i++){const x=fields.get("X"+i),y=fields.get("Y"+i),served=word.targets.includes(i);
 need(x.v===bit(i),"X restored "+i);need(y.v===(bit(111+i)^(served?bit(i):0n)),"Y coefficient "+i);
 need(same(x.chart,served||word.closed_partial?"Hub":"L"+i),"X endpoint chart");need(same(y.chart,served||word.closed_partial?"F"+i:"zero"),"Y endpoint chart");if(served)done.push(i);}
 const packetPaths=Object.fromEntries(["P","Q"].map(x=>[x,owners.get(x).path]));
 need(retired.filter(x=>x.moves).length===2&&retired.filter(x=>x.moves).every(x=>["P","Q"].includes(x.role)),"only two owned moving lifetimes");
 return{status:"PASS_INDEPENDENT_EXACT_NESTED_FORK_REPLAY",field_columns:222,targets:done,closed_partial:word.closed_partial,operations:word.operations.length,counts,profile,rank_length:Object.entries(profile).reduce((s,[r,c])=>s+Number(r)*c,0),peak_owners:peak,retirements:retired,packet_paths:packetPaths,X_projection_history_rank:rankBinary(history),packets_always_pure_X:packetsPure,snapshots,exact_chart_method:"rational reduced row bases and nullspaces",untouched_original_pairs:111-done.length,all_owners_retired:true,dirty_erasure_foundation_retained:true,no_new_kappa:true};
}

function reviewForkPrices(profiles,author){
 const need=(x,m)=>{if(!x)throw Error(m)},S=10n**30n,memo=new Map();
 const root=r=>{if(memo.has(r))return memo.get(r);if(r===1){const v=[S,S];memo.set(r,v);return v}const N=BigInt(r)**199n*S**200n;let a=0n,b=BigInt(r)*S;while(b-a>1n){const m=(a+b)/2n;if(m**200n<=N)a=m;else b=m}need(a**200n<=N&&b**200n>N,"integer bracket");const v=[a,b];memo.set(r,v);return v};
 const moment=coeff=>{let a=0n,b=0n;for(const[r,c0]of Object.entries(coeff)){const c=BigInt(c0),[l,u]=root(+r);a+=c*(c>=0n?l:u);b+=c*(c>=0n?u:l)}return[a,b]},add=(p,r,c)=>p[r]=(p[r]||0)+c;
 const sixAllowance={1:-74,64:74,127:37};for(let j=1;j<=8;j++){add(sixAllowance,1+7*j,74);add(sixAllowance,7*j,-74)}
 const allowance=moment(sixAllowance),out={};
 for(const[name,p]of Object.entries(profiles)){need(Object.entries(p).reduce((s,[r,c])=>s+(+r)*c,0)===1570,"rank telescoping");const value=moment(p),frozen=author[name].price.moment;
 need(value[0]*BigInt(frozen.denominator)<=BigInt(frozen.lower_numerator)*S&&value[1]*BigInt(frozen.denominator)>=BigInt(frozen.upper_numerator)*S,"independent contains finer author bracket");
 const isolated={7:222,8:3};for(const[r,c]of Object.entries(p))add(isolated,+r,-c);const saving=moment(isolated);need(saving[0]>0n,"strict partial saving");
 const remaining={};for(const q of[7,8]){const terms={...sixAllowance};for(const[r,c]of Object.entries(p))add(terms,+r,-6*c);add(terms,8,-6*q);const v=moment(terms);need(v[0]>0n,"optimistic margin");remaining[q]={lower:v[0].toString(),upper:v[1].toString(),denominator:(6n*S).toString()};}
 out[name]={moment:{lower:value[0].toString(),upper:value[1].toString(),denominator:S.toString()},partial_saving_vs_three_isolated:{lower:saving[0].toString(),upper:saving[1].toString(),denominator:S.toString()},optimistic_remaining:remaining};
 }

 return{status:"PASS_INDEPENDENT_PARTIAL_FORK_INVOICE",method:"bisection integer200th roots, independently derived limiting paired-caller profile",t:"199/200",limiting_allowance:{lower:allowance[0].toString(),upper:allowance[1].toString(),denominator:(6n*S).toString()},alternatives:out,costs_not_added:true,no_complete_supplier:true,no_new_kappa:true};
}

function reviewThirdForkChart(word){
 const R=Array.from({length:111},(_,i)=>word.charts["L"+i].rows[0]),N=[92,54,38,36,55,1].map(i=>R[i]),p=101,A=N.map(r=>r.map(x=>(x%p+p)%p));let rank=0;
 for(let c=0;c<8&&rank<6;c++){let r=rank;while(r<6&&!A[r][c])r++;if(r===6)continue;[A[r],A[rank]]=[A[rank],A[r]];let u=1;while(A[rank][c]*u%p!==1)u++;A[rank]=A[rank].map(x=>x*u%p);for(let i=rank+1;i<6;i++){let t=A[i][c];A[i]=A[i].map((x,j)=>(x-t*A[rank][j]%p+p)%p);}rank++;}
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),roles=R.flatMap((r,i)=>N.every(n=>dot(r,n)===0)?[i]:[]);if(rank!==6||JSON.stringify(roles)!=="[41,110]")throw Error("third chart");
 return{normal_rank:6,normal_rank_lower_certificate_prime:101,normal_rank_upper:"six supplied vectors",common_chart_dimension:2,native_source_roles:roles,gram:roles.map(i=>roles.map(j=>dot(R[i],R[j]))),scope:"same common-local three-fresh-input template only; changed/off-D handoffs remain open"};
}

function reviewPiggybackPackage(flat,words,author){
 const names={nested_live:"NESTED.json",nested_closed:"NESTED-CLOSED.json",nine_live:"NINE-TARGET.json",nine_closed:"NINE-TARGET-CLOSED.json"},runs={};
 for(const[k,n]of Object.entries(names))runs[k]=reviewPiggyback(words[n],flat);
 const profiles={nested:runs.nested_closed.profile,nine_target:runs.nine_closed.profile},price=reviewForkPrices(profiles,author),controls=[];
 function reject(name,w){let error;try{reviewPiggyback(w,flat)}catch(e){error=e.message}if(!error)throw Error("negative accepted: "+name);controls.push({name,rejected:true,error});}
 let bad=JSON.parse(JSON.stringify(words["NESTED.json"]));bad.operations=bad.operations.filter(x=>JSON.stringify(x)!==JSON.stringify(["ADD","X55","NS2"]));delete bad.markers;reject("omit acquired X55 correction",bad);
 bad=JSON.parse(JSON.stringify(words["NESTED.json"]));bad.charts.G3={kind:"ann",rows:[92,54,38,1].map(i=>bad.charts["L"+i].rows[0]),normal_roles:[92,54,38,1]};reject("use D intersection F1 instead of off-D G3",bad);
 bad=JSON.parse(JSON.stringify(words["NINE-TARGET.json"]));bad.operations=bad.operations.filter(x=>JSON.stringify(x)!==JSON.stringify(["ADD","Y36","Y10"]));reject("omit original Y mask",bad);
 bad=JSON.parse(JSON.stringify(words["NINE-TARGET.json"]));bad.charts.D=JSON.parse(JSON.stringify(bad.charts.E_A));reject("replace D by E_A",bad);
 return{status:"PASS_INDEPENDENT_PIGGYBACK_PACKAGE",runs,price,third_chart:reviewThirdForkChart(words["NESTED.json"]),negative_controls:controls,source_scope:"authenticated84-signature native recovery, not fresh gzip",all_dirty_clear_costs_and_foundations_retained:true,no_new_kappa:true};
}

if(typeof module!=="undefined"){
 module.exports={reviewPiggybackPackage,reviewPiggyback,reviewForkPrices};
 if(require.main===module){
  const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),hash=b=>crypto.createHash("sha256").update(b).digest("hex");
  if(process.argv.length!==3)throw Error("usage: node check.js PATH_TO_FLAT_CUBIC_RESULT_JSON");
  const raw=fs.readFileSync(process.argv[2]);if(hash(raw)!=="4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc")throw Error("flat source SHA256 mismatch");
  const pins={"NESTED.json":"eefb251c16c9ee4d5f56b32bc3f46260fd6612316ebd7db0bfc64e4f020295cf","NESTED-CLOSED.json":"85605862cd98ce08e0d029f0f1f1012ee69259b6d2b5c08983246504d62af0d1","NINE-TARGET.json":"495e94fd836df2ae8e60e0f20afe3fa206ca1bfe32f3f677b26d47f8fb9ead7e","NINE-TARGET-CLOSED.json":"df28644da4a6a183292d584c228e7bd7f04a6c4337457c0da5c4a396617dd17a","RESULT.json":"d02623ed8ac9b74a02062d8f34e1e9acf9fb7833b61d3d9f4ed6434a38a5217c"},words={};let author;
  for(const[name,pin]of Object.entries(pins)){const b=fs.readFileSync(path.join(__dirname,"../author",name));if(hash(b)!==pin)throw Error("fixture mismatch "+name);if(name==="RESULT.json")author=JSON.parse(b);else words[name]=JSON.parse(b);}
  process.stdout.write(JSON.stringify(reviewPiggybackPackage(JSON.parse(raw),words,author),null,2)+"\n");
 }
}
