
function reviewInjection(word,flat,options={}){
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
 if(a==="P"||a==="Q")for(let i=0;i<111;i++){const x=fields.get("X"+i);need(x.v===bit(i),"all originals restored before Hub packet");need(same(x.chart,word.moved_original_sources.includes(i)?"Hub":"L"+i),"source path before packet birth");}}
 else if(op==="MOVE"){const x=fields.get(a);need(x&&chart[b],"known MOVE");need(x.owned?subset(b,x.chart):subset(x.chart,b),"illegal "+a+" "+x.chart+" -> "+b+" at "+index);const d=Math.abs(chart[x.chart].dim-chart[b].dim);need(d>0,"positive MOVE rank");profile[d]=(profile[d]||0)+1;x.chart=b;if(x.owned){owners.get(a).path.push(chart[b].dim);owners.get(a).moves++;}}
 else if(op==="ADD"){const x=fields.get(a),y=fields.get(b);need(x&&y&&a!==b&&same(x.chart,y.chart),"cocharted ADD at "+index);y.v^=x.v;}
 else if(op==="CLEAR"){const x=fields.get(a);need(x?.owned,"owned clear");retired.push({role:a,chart:x.chart,rank:chart[x.chart].dim,dirty:x.v!==0n,value:x.v.toString(16),...owners.get(a)});fields.delete(a);}
 else throw Error("unknown operation");
 for(const a of["P","Q"]){const x=fields.get(a);if(x&&!same(x.chart,"Hub")){history.push(x.v&xmask);if(x.v>>111n)packetsPure=false;}}
 for(const [name,n]of Object.entries(word.markers||{}))if(index+1===n){const complete=Array.from({length:111},(_,i)=>i).filter(i=>fields.get("Y"+i).v===(bit(111+i)^bit(i))&&same(fields.get("Y"+i).chart,"F"+i));snapshots[name]={after:index+1,completed:complete,packet_values:Object.fromEntries(["P","Q"].filter(x=>fields.has(x)).map(x=>[x,fields.get(x).v.toString(16)])),live_owners:[...fields].filter(([_,x])=>x.owned).map(([name,x])=>({name,chart:x.chart,value:x.v.toString(16)})),history_rank:rankBinary(history)};}
 }

 const z=BigInt("0x"+word.injected_mode_hex),support=Array.from({length:111},(_,i)=>i).filter(i=>z&bit(i));
 need(JSON.stringify(support)===JSON.stringify(word.injected_mode_support),"mode support");
 need(((z>>1n)^(z>>18n))%2n===0n,"carrier equality");
 const base=[92,36,54,38,55,23,1,18],extra=support.filter(i=>!base.includes(i));
 const prefix=word.mode==="prefix",done=prefix?[92,54,38]:base;
 const expected=prefix?{NH:["N0",0n],NS1:["N02",bit(23)],NS4:["N03",bit(18)],NS3:["N2",bit(1)],NS2:["G3",bit(55)],Z:["D",z],P:["D",bit(36)^bit(23)^bit(18)^z],Q:["D",bit(55)^bit(1)^z]}:{};
 if(prefix)for(const i of extra)expected["R"+i]=["L"+i,bit(i)];
 const remaining=[...fields].filter(([_,x])=>x.owned);
 need(remaining.length===Object.keys(expected).length,"actual live owner inventory");
 for(const [name,[c,v]]of Object.entries(expected)){const x=fields.get(name);need(x&&same(x.chart,c)&&x.v===v,"actual retained owner "+name);}

 for(let i=0;i<111;i++){const x=fields.get("X"+i),y=fields.get("Y"+i),served=done.includes(i);
 need(x.v===bit(i),"X restored "+i);need(y.v===(bit(111+i)^(served?bit(i):0n)),"Y coefficient "+i);
 need(same(x.chart,word.closed_partial||base.includes(i)||extra.includes(i)?"Hub":"L"+i),"X endpoint chart "+i);
 need(same(y.chart,word.closed_partial||served?"F"+i:"zero"),"Y endpoint chart "+i);}
 const moving=[...owners].filter(([_,x])=>x.moves);
 need(moving.length===2&&moving.every(([n])=>n==="P"||n==="Q"),"only two moving owned lifetimes");
 return{status:"PASS_ROOT_CUBIC_INJECTION_REPLAY",field_columns:222,mode:word.mode,support,extra_sources:extra,completed_targets:done,operations:word.operations.length,counts,profile,rank_length:Object.entries(profile).reduce((s,[r,c])=>s+Number(r)*c,0),peak_owners:peak,live_owners:remaining.map(([name,x])=>({name,chart:x.chart,value:x.v.toString(16)})),retirements:retired,packet_paths:Object.fromEntries(["P","Q"].map(x=>[x,owners.get(x).path])),X_projection_history_rank:rankBinary(history),packets_always_pure_X:packetsPure,snapshots,exact_chart_method:"rational row bases and nullspaces",new_complete_kappa:false};
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


function reviewInjectionPackage(words,geo,flat,builder,d5,author){
 const need=(x,m)=>{if(!x)throw Error(m)},bit=i=>1n<<BigInt(i),rank=rows=>{const p=new Map();for(let x of rows)while(x){const k=x&-x;if(p.has(k))x^=p.get(k);else{p.set(k,x);break;}}return p.size;};
 const modes=Array.from({length:32},(_,m)=>{let z=0n;d5.basis.forEach((s,k)=>{if(m>>k&1)s.forEach(i=>z^=bit(i));});return z;});
 const preferred={};for(const [mode,w]of Object.entries(words)){const r=reviewInjection(w,flat);preferred[mode]=r;
 need(JSON.stringify(builder(geo,BigInt("0x"+w.injected_mode_hex).toString(),mode))===JSON.stringify(w),"literal builder match "+mode);}
 const all=[];for(const z of modes.slice(1)){const p=reviewInjection(builder(geo,z.toString(),"prefix"),flat),c=reviewInjection(builder(geo,z.toString(),"closed"),flat),w=p.support.length,e=p.extra_sources.length,a=Number(z>>1n&1n);
 need(p.counts.INIT===15+e&&p.counts.ADD===52+e+2*w-a&&p.counts.MOVE===39+2*e&&p.counts.CLEAR===7&&p.live_owners.length===8+e,"prefix counts");
 need(c.counts.INIT===15+e&&c.counts.CLEAR===15+e&&c.counts.ADD===75+e+2*w-a&&c.counts.MOVE===262+e&&c.rank_length===1570,"closed counts");
 const expected={1:31,2:5,3:11+e,4:e,5:3,6:3,7:209-e};need(Object.entries(expected).every(([r,n])=>(c.profile[r]||0)===n),"incremental profile");
 need(p.X_projection_history_rank===4&&c.X_projection_history_rank===7,"history ranks");all.push({mode:z.toString(),support:p.support,extra_sources:p.extra_sources,prefix_counts:p.counts,closed_counts:c.counts,closed_profile:c.profile});}

 const row=ids=>ids.reduce((x,i)=>x^bit(i),0n),A=row([92,36,55,23,18,1]),B=row([92,36,54,38,55]),h=row([36,23,18]),u=row([55,1]);
 const spaces=modes.map(z=>[A,B,h^z,u^z]);need(spaces.every(s=>rank(s)===4),"code family dimension");
 let pairs=0;for(let i=0;i<32;i++)for(let j=i+1;j<32;j++){need(rank(spaces[i].concat(spaces[j]))===5,"pair intersection");pairs++;}
 need(rank(spaces.flat())===9&&rank([A,B,h^u])===3,"ambient and common dimensions");
 const controls=[];for(const [label,mode,target]of [["carrier_one","prefix","ADD|Z|X1"],["carrier_eighteen","prefix","ADD|Z|X18"],["source_capture","prefix","ADD|X11|Z"],["retained_point_copy","prefix","ADD|X11|R11"],["restore_shear","prefix","ADD|X18|X1"],["uninject_packet","closed","ADD|Z|P"]]){
 const w=JSON.parse(JSON.stringify(words[mode])),i=w.operations.findIndex(x=>x.join("|")===target);need(i>=0,"mutation location");w.operations.splice(i,1);let reason="";try{reviewInjection(w,flat);}catch(e){reason=e.message;}need(reason,"negative control");controls.push({label,index:i,rejected:true,reason});}
 const price=reviewForkPrices({injection:preferred.closed.profile},{injection:{price:author.price}});
 return{status:"PASS_ROOT_CUBIC_HISTORY_INJECTION_PACKAGE",preferred,all31_modes:all,code_family:{choices:32,individual_dimension:4,common_dimension:3,pairwise_intersection_dimension:3,pairs_checked:pairs,ambient_dimension:9},negative_controls:controls,price,source_qualification:"Independent recovery from84 flat signatures; no fresh native gzip replay",productive_decoder:false,new_complete_kappa:false};
}
if(typeof module!=="undefined")module.exports={reviewInjection,reviewInjectionPackage};
if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
 const read=(file,pin)=>{const b=fs.readFileSync(file);if(pin&&crypto.createHash("sha256").update(b).digest("hex")!==pin)throw Error("SHA256 mismatch "+file);return JSON.parse(b.toString("utf8"));};
 if(process.argv.length!==4)throw Error("usage: node check.js FLAT-CUBIC-RESULT.json SOURCE-RECOVERY.json");
 const flat=read(process.argv[2],"4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc"),geo=read(process.argv[3],"8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e");
 const {reviewD5}=require("../../bit-d5-cubic-local-history/review-root/check.js");
 const buildPath=path.join(__dirname,"../author/build.js"),raw=fs.readFileSync(buildPath);
 if(crypto.createHash("sha256").update(raw).digest("hex")!=="d613c521d96deaa307e46b1bbadd3dd5db9a7fd6b1f985be148dca5b10f6b8b3")throw Error("builder pin");
 const {buildCubicInjection}=require(buildPath),author=read(path.join(__dirname,"../author/RESULT.json"));
 const words={};for(const[mode,file]of[["prefix","PREFIX.json"],["control","ENDPOINT-CONTROL.json"],["closed","CLOSED-CONTROL.json"]])words[mode]=read(path.join(__dirname,"../author",file));
 console.log(JSON.stringify(reviewInjectionPackage(words,geo,flat,buildCubicInjection,reviewD5(flat,geo),author),null,2));
}
