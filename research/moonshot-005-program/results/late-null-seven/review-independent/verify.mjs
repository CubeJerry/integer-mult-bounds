import {readFileSync} from "node:fs";
import {join} from "node:path";
import {gunzipSync} from "node:zlib";
import {createHash} from "node:crypto";
function independentNullSeven(native,parent,word,invoice,options={}){
 const need=(v,m)=>{if(!v)throw Error(m);}, equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const D=1n<<80n, frames=native.frames.concat(parent.additional_charts.map(x=>x.frame)), priv=parent.private_role_map, B=[5,56,65,69,77,96,100,103], U=[17,19,30,38,40,47,52,60], chosen=U.filter(x=>x!==17), first=parent.public+parent.owned_fields, hub=127;
 need(parent.public===1880&&parent.initial.length===1880&&first===1961,"source size and first fresh slot");
 need(equal(parent.initial,word.initial)&&equal(parent.additional_charts,word.additional_charts)&&equal(parent.private_role_map,word.private_role_map)&&word.public===parent.public&&word.owned_fields===parent.owned_fields+8,"unchanged input placement, charts, raw roles and exactly eight new slots");
 const ht=new Map(native.hosted.Dports.map((j,k)=>[native.live[j],{x:native.hosted.X2[k],d:native.hosted.Y2[k]}]));
 const q=n=>{const z=Array.from({length:9},(_,j)=>(n>>j)&1),w=z.reduce((s,x)=>s+x,0);if(w===3)return z.map(x=>3*x-1);need(w===7,"native normal");const h=z.map((x,j)=>x?-1:j).filter(j=>j>=0);return z.map((_,j)=>3*(Number(j===h[0])-Number(j===h[1])));};
 const roots=new Map(native.live.map((r,i)=>[r,q(native.ports[i])])),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0), G=(a,b)=>dot(roots.get(a),roots.get(b))/18;
 for(let i=0;i<8;i++)for(let j=0;j<8;j++)need(G(B[i],B[j])===(i===j?1:0),"real orthogonal hosted frame");
 const cs=v=>Number.isInteger(v)?String(v):String(v*2)+"/2", frac=s=>{const a=String(s).split("/");return [BigInt(a[0]),BigInt(a[1]||"1")];};
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}, F=(a,b=1n)=>{if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}, fa=(x,y)=>F(x[0]*y[1]+y[0]*x[1],x[1]*y[1]), fm=(x,y)=>F(x[0]*y[0],x[1]*y[1]), fn=x=>[-x[0],x[1]], fd=(x,y)=>fm(x,F(y[1],y[0])), fs=x=>x[1]===1n?String(x[0]):x[0]+"/"+x[1];
 const observation=U.map(u=>B.map(b=>G(u,b))), H=chosen.map(u=>B.map(b=>F(BigInt(G(u,b)*2),2n)));H.push(B.map(b=>F(b===56?1n:0n)));
 const M=H.map((row,i)=>row.concat(B.map((_,j)=>F(i===j?1n:0n))));
 for(let c=0;c<8;c++){let t=c;while(t<8&&M[t][c][0]===0n)t++;need(t<8,"seven plus authentic56 full rank");[M[t],M[c]]=[M[c],M[t]];const z=M[c][c];M[c]=M[c].map(x=>fd(x,z));for(let i=0;i<8;i++)if(i!==c){const v=M[i][c];M[i]=M[i].map((x,j)=>fa(x,fn(fm(v,M[c][j]))));}}
 const decoder=M.map(r=>r.slice(8));need(decoder.every(r=>r.every(x=>x[1]===1n)),"integer decoder");
 for(let j=0;j<8;j++)need(observation[0][j]-observation[1][j]-observation[3][j]+observation[4][j]===0,"final null relation");
 const kernel=[0,-1,-1,0,0,1,1,0];for(const row of observation)need(dot(row,kernel)===0,"right kernel");
 const inserts=new Map(), add=(boundary,ops)=>{if(!inserts.has(boundary))inserts.set(boundary,[]);inserts.get(boundary).push(...ops);}, fresh={}, acquisitions=[];
 for(let k=0;k<chosen.length;k++){const u=chosen[k],field=first+k;fresh[u]=field;const pg=parent.parent_cohort_collection_provenance.groups.filter(g=>g.donors.includes(u));need(pg.length===1,"unique actual primal cohort");const g=parent.paired_collection.groups.find(g=>g.chart===pg[0].chart);need(g,"actual paired group");const early=[["INIT",field,g.chart]],late=[];
 if(g.kind==="rank2_direct_cochart"){const sources=[...new Set(g.reads.map(r=>r.receiver_Y2))];for(const d of sources){const b=B.find(b=>ht.get(b).d===d);need(b!==undefined,"direct source in B");early.push(["ADD",field,priv[d],cs(G(u,b)),g.chart]);}early.push(["MOVE",field,g.chart,hub,true]);const boundary=Math.min(...g.reads.map(x=>x.event));add(boundary,early);acquisitions.push({u,chart:g.chart,boundary,kind:"direct",sources});}
 else{need(g.kind==="inverse_transpose","affine group");for(const inj of g.injections){const op=parent.program[inj.event];need(equal(op,["ADD",priv[inj.carrier_X2],priv[inj.source_Y2],"-1",op[4]]),"actual minus-d injection");const b=B.find(b=>ht.get(b).d===inj.source_Y2);need(b!==undefined,"receiver B");const v=G(u,b);need(v===.5||v===-.5,"four half Gram coefficients");early.push(["ADD",field,priv[inj.carrier_X2],cs(v),g.chart]);late.push(["ADD",field,priv[inj.carrier_X2],cs(-v),hub]);}early.push(["MOVE",field,g.chart,hub,true]);add(g.encoded,early);add(g.at_hub,late);acquisitions.push({u,chart:g.chart,boundary:g.encoded,post:g.at_hub,kind:"affine",carriers:g.injections.map(x=>priv[x.carrier_X2])});}}
 const ret=first+7, dr=ht.get(56).d, facet=native.final[dr], final=[["INIT",ret,facet],["ADD",ret,priv[dr],"1",facet],["MOVE",ret,facet,hub,true]], input=chosen.map(u=>fresh[u]).concat(ret);
 for(let i=0;i<8;i++)for(let j=0;j<8;j++)if(decoder[i][j][0])final.push(["ADD",priv[ht.get(B[i]).x],input[j],fs(fn(decoder[i][j])),hub]);
 for(const f of input)final.push(["CLEAR",f,hub]);add(parent.marks.common_starts,final);
 const expected=[],boundaries=new Map();for(let i=0;i<=parent.program.length;i++){boundaries.set(i,expected.length);if(inserts.has(i))expected.push(...inserts.get(i));if(i<parent.program.length)expected.push(parent.program[i]);}
 if(!options.skipLiteral)need(equal(expected,word.program),"independently reconstructed all instructions");
 const prefix=parent.marks.common_starts+110, observationBoundary=boundaries.get(parent.marks.common_starts);need(prefix===word.marks.common_starts&&observationBoundary===5150,"actual boundaries");
 need(equal(parent.program.slice(parent.marks.common_starts),word.program.slice(prefix)),"literal entire common suffix");
 function span(a,v){const b=Array(9).fill(0);for(let x of a){while(x){const p=31-Math.clz32(x);if(b[p])x^=b[p];else{b[p]=x;break;}}}while(v){const p=31-Math.clz32(v);if(!b[p])return false;v^=b[p];}return true;}
 const frameOK=new Map();function pair(a,b){const key=a+","+b;if(frameOK.has(key))return frameOK.get(key);const x=frames[a],y=frames[b];need(x&&y,"existing chart");const small=x.length<y.length?x:y,large=x.length<y.length?y:x;need(small.every(v=>span(large,v)),"nested exact binary MOVE");const r=Math.abs(x.length-y.length);need(r>0,"positive recursive rank");frameOK.set(key,r);return r;}
 const bump=(h,k)=>h[k]=(h[k]||0)+1;
 function audit(w){const chart=w.initial.slice().concat(Array(w.owned_fields).fill(null)),active=Array(chart.length).fill(false);for(let f=0;f<w.public;f++)active[f]=true;let live=0,peak=0,lifetimes=0;const counts={},moves={},owned={},raw={};
 for(let i=0;i<w.program.length;i++){const o=w.program[i],op=o[0],a=o[1];bump(counts,op);need(Number.isInteger(a)&&a>=0&&a<chart.length,"field range");
 if(op==="INIT"){need(a>=w.public&&!active[a],"owned activation");active[a]=true;chart[a]=o[2];need(frames[o[2]],"initialization chart");live++;lifetimes++;peak=Math.max(peak,live);}
 else{need(active[a],"live destination");if(op==="ADD"||op==="COPY"){need(active[o[2]]&&chart[a]===o[4]&&chart[o[2]]===o[4],"actual ADD/COPY cochart");}
 else if(op==="SCALE")need(chart[a]===o[3],"actual SCALE chart");
 else if(op==="MOVE"){need(chart[a]===o[2]&&o[4]===(a>=w.public),"actual MOVE source and charged ownership");const r=pair(o[2],o[3]);bump(moves,r);if(o[4])bump(owned,r);else if(a>=1480&&a<1880)bump(raw,r);chart[a]=o[3];}
 else if(op==="CLEAR"){need(a>=w.public&&chart[a]===o[2],"actual owned retirement");active[a]=false;chart[a]=null;live--;}
 else throw Error("opcode");}}
 need(live===0,"all owned retired");return {instructions:w.program.length,counts,moves,owned,raw,lifetimes,peak,finalCharts:chart.slice(0,w.public)};}
 const bill=audit(word),parentBill=audit(parent);need(equal(bill.finalCharts,parentBill.finalCharts),"all1880 final charts unchanged");
 const rowQ=role=>new Map([[priv[role],D],[role,-D]]);
 function sax(dst,src,c){const [a,b]=frac(c);for(const [j,x]of [...src]){const z=x*a;need(z%b===0n,"exact fixed-denominator coefficient");const v=(dst.get(j)||0n)+z/b;if(v)dst.set(j,v);else dst.delete(j);}}
 const roweq=(a,b)=>a&&b&&a.size===b.size&&[...a].every(([j,x])=>b.get(j)===x);
 const snapshots={};function replay(w,stop,capture){const rows=Array(w.public+w.owned_fields).fill(null);for(let i=0;i<w.public;i++)rows[i]=new Map([[i,D]]);for(let i=0;i<stop;i++){if(capture&&i===observationBoundary)for(const u of chosen)snapshots[u]=new Map(rows[fresh[u]]);if(capture&&i===1086){snapshots.earlyRelation=new Map(rows[fresh[19]]);sax(snapshots.earlyRelation,rows[fresh[38]],"1");sax(snapshots.earlyRelation,rows[fresh[40]],"-1");}
 const o=w.program[i],a=o[1];if(o[0]==="INIT")rows[a]=new Map();else if(o[0]==="CLEAR")rows[a]=null;else if(o[0]==="ADD")sax(rows[a],rows[o[2]],o[3]);else if(o[0]==="COPY"){rows[a]=new Map();sax(rows[a],rows[o[2]],o[3]);}else if(o[0]==="SCALE"){const r=new Map();sax(r,rows[a],o[2]);rows[a]=r;}}
 return rows;}
 const pr=replay(parent,parent.marks.common_starts,false),wr=replay(word,prefix,true),expectedGhost={};
 for(const u of chosen){const r=new Map();for(const b of B)sax(r,rowQ(ht.get(b).d),cs(G(u,b)));expectedGhost[u]=r;need(roweq(snapshots[u],r),"actual pure-d null observation "+u);}
 const changed=[];for(let f=0;f<parent.public+parent.owned_fields;f++){let r=pr[f]?new Map(pr[f]):null;const i=B.findIndex(b=>priv[ht.get(b).x]===f);if(i>=0){sax(r,rowQ(ht.get(B[i]).d),"-1");changed.push(f);}need((r===null&&wr[f]===null)||roweq(r,wr[f]),"all-input prefix endpoint "+f);}
 for(let f=first;f<first+8;f++)need(wr[f]===null,"fresh observer retirement");
 const suffixUses=[];for(const f of changed){const uses=[];for(let i=prefix;i<word.program.length;i++){const o=word.program[i];if(o[1]===f||(["ADD","COPY"].includes(o[0])&&o[2]===f))uses.push([i,o]);}need(uses.length===1&&equal(uses[0][1],["ADD",f,Number(Object.keys(priv).find(r=>priv[r]===f)),"1",hub]),"unique final recoupling only");suffixUses.push({field:f,event:uses[0][0],operation:uses[0][1]});}
 const hosted=[...ht.keys()], residual=hosted.map(b=>{const r=new Map(wr[priv[ht.get(b).x]]);sax(r,rowQ(ht.get(b).x),"-1");sax(r,rowQ(ht.get(b).d),"1");const vals=hosted.map(c=>r.get(priv[ht.get(c).d])||0n);for(let j=0;j<hosted.length;j++)sax(r,rowQ(ht.get(hosted[j]).d),cs(-Number(vals[j])/Number(D)));need(r.size===0,"actual residual has only original d coordinates");return vals;});
 const T=hosted.map((b,i)=>B.includes(b)?-1:i).filter(i=>i>=0);for(let i=0;i<hosted.length;i++)for(const j of T)need(residual[i][j]===(i===j?D:0n),"exact identity88 residual block");for(const b of B)need(residual[hosted.indexOf(b)].every(x=>x===0n),"eight zero residual rows");
 const earlyTarget=new Map();for(const b of B)sax(earlyTarget,rowQ(ht.get(b).d),cs(G(17,b)));need(!roweq(snapshots.earlyRelation,earlyTarget),"premature relation negative control");
 const maps=[];for(let i=0;i<word.program.length;i++){const o=word.program[i];if(o[0]==="MOVE"&&o[1]>=first){const old=parent.program.findIndex(x=>x[0]==="MOVE"&&x[2]===o[2]&&x[3]===o[3]);need(old>=0,"exact inherited phase chart pair");maps.push({event:i,field:o[1],from:o[2],to:o[3],rank:pair(o[2],o[3]),parent_event:old,parent_operation:parent.program[old]});}}
 const nativeOwned={},nativeRaw={};for(const o of native.program)if(o[0]==="MOVE"){const r=pair(o[2],o[3]);if(o[4])bump(nativeOwned,r);else if(Object.prototype.hasOwnProperty.call(priv,o[1]))bump(nativeRaw,r);}
 const P={...invoice.P4};for(const r of new Set([...Object.keys(nativeOwned),...Object.keys(nativeRaw),...Object.keys(bill.owned),...Object.keys(bill.raw)]))P[r]=(P[r]||0)+18*((bill.owned[r]||0)-(nativeOwned[r]||0)+(bill.raw[r]||0)-(nativeRaw[r]||0));
 const powerCache=new Map(),den=1n<<160n;function power(r){if(powerCache.has(r))return powerCache.get(r);const n=BigInt(r),target=n**199n*den**200n;let lo=0n,hi=n*den+1n;while(hi-lo>1n){const m=(hi+lo)>>1n;if(m**200n<=target)lo=m;else hi=m;}const v=[lo,lo**200n===target?lo:lo+1n];powerCache.set(r,v);return v;}
 let lo=0n,hi=0n;for(const r of new Set([...Object.keys(P),...Object.keys(invoice.T4)])){const c=BigInt((invoice.T4[r]||0)-(P[r]||0)),[l,h]=power(Number(r));lo+=c*(c>=0n?l:h);hi+=c*(c>=0n?h:l);}
 const Sframe=[0,7,20,27,36,46,57,111], Qframe=B.map(b=>Sframe.map(s=>G(b,s))); for(let i=0;i<8;i++)for(let j=0;j<8;j++)need(dot(Qframe[i],Qframe[j])===Number(i===j),"two-frame noncomposition orthogonality");
 const serialize=r=>[...r].sort((a,b)=>a[0]-b[0]).map(([j,v])=>[j,fs(F(v,D))]);
 return {compatibility_negative_control:{two_frame_B:B,two_frame_S:Sframe,Q:Qframe,original_principal_block:"[[I,Q],[Q^T,I]] rank8",after_unchanged_eight_B_corrections:"[[0,Q],[Q^T,I]] rank16",whole_two_frame_residual_rank_after:96,scope:"Algebraic noncomposition test against previously verified two-frame residual; no combined source word claimed."},status:"PASS_INDEPENDENT_NULL_SEVEN_SOURCE_WORD",method:"Source-root reconstruction, new exact interpreter, no author builder/checker imported",instructions_reconstructed:expected.length,independent_columns:1880,existing_prefix_fields_compared:parent.public+parent.owned_fields,changed_prefix_fields:changed,suffix_uses:suffixUses,bill:{...bill,finalCharts:undefined},ordinary_increment:Object.fromEntries(Object.keys(bill.counts).map(k=>[k,bill.counts[k]-(parentBill.counts[k]||0)])),observation:observation.map(r=>r.map(cs)),decoder:decoder.map(r=>r.map(fs)),acquisitions,actual_observations:Object.fromEntries(chosen.map(u=>[u,serialize(snapshots[u])])),premature_relation_nuisance:serialize(snapshots.earlyRelation),reverse_residual_rank:88,identity_minor_indices:T,phase_map_inheritance:maps,P4_new:P,T4:invoice.T4,remaining_moment_per_native:{lower_numerator:String(lo),upper_numerator:String(hi),denominator:String(18n*den),approx:Number(lo)/Number(18n*den)},scope:"All1880 finite source composition and complete physical-call invoice. No new kappa or foundational discharge."};
}
function independentNullSevenControls(n,p,w,inv){
 const cases=[
 ["remove_early_null_read",a=>{const j=a.program.findIndex(o=>o[0]==="ADD"&&o[1]===1966);a.program[j][3]="0";}],
 ["remove_late_null_cancellation",a=>{const j=a.program.findIndex(o=>o[0]==="ADD"&&o[1]===1966&&o[4]===127);a.program[j][3]="0";}],
 ["wrong_B_decoder_sign",a=>{a.program[5153][3]="-1";}],
 ["unpaid_owned_arrival",a=>{const j=a.program.findIndex(o=>o[0]==="MOVE"&&o[1]===1966);a.program[j][4]=false;}],
 ["wrong_birth_chart",a=>{const j=a.program.findIndex(o=>o[0]==="INIT"&&o[1]===1966);a.program[j][2]=1105;}],
 ["missing_actual_arrival",a=>{const j=a.program.findIndex(o=>o[0]==="MOVE"&&o[1]===1966);a.program[j]=["SCALE",1966,"1",1095];}],
 ["valid_wrong_missing_mode_d5",a=>{a.program[5150][2]=132;a.program[5151]=["ADD",1968,1788,"1",132];a.program[5152]=["MOVE",1968,132,127,true];}]
 ];const controls=[];for(const [name,mutate]of cases){const a={...w,program:w.program.map(o=>o.slice())};mutate(a);let reason=null;try{independentNullSeven(n,p,a,inv,{skipLiteral:true});}catch(e){reason=e.message;}if(!reason)throw Error("mutant survived: "+name);controls.push({name,rejected:true,reason});}return controls;
}
const repo=process.argv[2]||".", file=process.argv[3];
if(!file)throw Error("Usage: node verify.mjs REPOSITORY WORD.json.gz");
const hash=b=>createHash("sha256").update(b).digest("hex");
function loadPinned(path,compressed,payload){const b=readFileSync(path);if(hash(b)!==compressed)throw Error("compressed pin "+path);const raw=gunzipSync(b);if(payload&&hash(raw)!==payload)throw Error("payload pin "+path);return JSON.parse(raw.toString("utf8"));}
const native=loadPinned(join(repo,"research/shared-wire-split-composition/data/final.json.gz"),"2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883","8f248653791e44acc88aab2e149957e9c2cb3ffa5f7bb958002c9994631a16ca");
const parent=loadPinned(join(repo,"research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz"),"bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17","bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a");
const word=loadPinned(file,"35baf768106f262ff43b60f2223e243f52b331e4943cf11295a18c53a00fdf7b","f1b2424537b320bf01f9c1e966d6868991df1048b4351f284ba7fcc2585c8ab6");
const invoiceBytes=readFileSync(join(repo,"research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json"));
if(hash(invoiceBytes)!=="b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248")throw Error("H4 invoice pin");
const invoice=JSON.parse(invoiceBytes.toString("utf8"));
const result=independentNullSeven(native,parent,word,invoice);result.negative_controls=independentNullSevenControls(native,parent,word,invoice);
console.log(JSON.stringify(result,null,2));
