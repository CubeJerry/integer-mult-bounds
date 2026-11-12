
function pyjson(x,path=''){
 if(x===null)return 'null';
 if(typeof x==='string')return JSON.stringify(x).replace(/[\u007f-\uffff]/g,c=>'\\u'+c.charCodeAt(0).toString(16).padStart(4,'0'));
 if(typeof x==='number'||typeof x==='boolean')return JSON.stringify(x);
 if(Array.isArray(x))return '['+x.map((v,i)=>pyjson(v,path+'/'+i)).join(',')+']';
 let keys=Object.keys(x);if(path==='/coupled_precondition/original_D_singleton_exit_coverage')keys.sort((a,b)=>+a-+b);else keys.sort();
 return '{'+keys.map(k=>pyjson(k)+':'+pyjson(x[k],path+'/'+k)).join(',')+'}';
}

function emitEntry(s,p,permuted){
 const need=(x,m)=>{if(!x)throw Error(m);};const pop=n=>{let c=0;for(;n;n&=n-1)c++;return c;};
 const qroot=v=>{const ones=Array.from({length:9},(_,i)=>i).filter(i=>(v>>i)&1);if(ones.length===3)return Array.from({length:9},(_,i)=>ones.includes(i)?2:-1);const absent=Array.from({length:9},(_,i)=>i).filter(i=>!ones.includes(i));need(ones.length===7,'root');return Array.from({length:9},(_,i)=>3*((i===absent[0]?1:0)-(i===absent[1]?1:0)));};
 const fraction=(a,b)=>{let x=Math.abs(a),y=b;while(y){const z=x%y;x=y;y=z;}a/=x;b/=x;return b===1?String(a):a+'/'+b;};
 const raw=p.private_role_map,H={};s.hosted.Dports.forEach((k,j)=>H[s.live[k]]=[s.hosted.X2[j],s.hosted.Y2[j]]);
 const U=s.live.filter(x=>!(x in H));need(U.join(',')==='17,19,30,38,40,47,52,60','coupled');
 const lines=Object.fromEntries(s.live.map(x=>[x,s.frames[s.initial[x]][0]])),roots=Object.fromEntries(s.live.map(x=>[x,qroot(lines[x])]));
 const mode=permuted?[5,56,69,65,96,103,100,77]:U,K={},coverage={};
 U.forEach((u,k)=>{K[u]=[];for(const xs of Object.keys(H)){const x=+xs,num=roots[mode[k]].reduce((a,b,j)=>a+b*roots[x][j],0)/9;if(num)K[u].push([H[x][1],num]);}});
 for(const xs of Object.keys(H)){const x=+xs,d=H[x][1];coverage[x]=U.filter(u=>K[u].some(([dd])=>dd===d)&&(pop(lines[u]&lines[x])%2));}
 if(permuted)need(Object.values(coverage).every(x=>x.length),'coverage');
 const skip={};
 for(const u of U){const y=u+112;let t=400;for(;t<p.program.length;t++){const e=p.program[t];if(e[1]===raw[y]||(['ADD','COPY'].includes(e[0])&&e[2]===raw[y]))break;}need(JSON.stringify(p.program[t])===JSON.stringify(['SCALE',raw[y],'1/2',3]),'first halfscale');skip[t]=u;}
 const ops=[],lineage=[],mapping={},boundaries={},preloads=[],temp=1880;
 const emit=(o,parent=null)=>{const t=ops.length;ops.push(o);lineage.push(parent);return t;};
 p.program.forEach((e,t)=>{
 if(t===400)for(const u of U){const y=u+112,L=s.initial[u],rec={X:u,Y:y,line:L,first_event:ops.length,K_row:K[u].map(([d,n])=>[d,fraction(n,2)])};
 emit(['INIT',temp,3]);emit(['ADD',temp,raw[y],'1',3]);for(const[d,n]of K[u])emit(['ADD',temp,raw[d],fraction(n,2),3]);rec.packet_ready=ops.length;
 emit(['MOVE',temp,3,L,true]);rec.consumer=emit(['ADD',raw[u],temp,'-1',L]);emit(['CLEAR',temp,L]);for(const[d,n]of K[u])emit(['ADD',raw[y],raw[d],fraction(n,4),3]);rec.end=ops.length;preloads.push(rec);}
 boundaries[t]=ops.length;if(t in skip)return;mapping[t]=emit([...e],t);
 });
 const pc={source_roles:U,formula:'a_U=x_U-y_U-Kd; b_U=2y_U+Kd',temporary:temp,preloads,K:Object.fromEntries(U.map(u=>[u,K[u].map(([d,n])=>[d,fraction(n,2)])])),K_rank:permuted?8:7,deleted_parent_half_scales:Object.keys(skip).map(Number).sort((a,b)=>a-b),coupled_X_debt:'-K d; no completed coupled reverse endpoint is claimed',forward_residual:'H*(x-D_U*y_U-D_U*K*d); original coupled diagonal unchanged',pure_D_Hub_claim:false};
 if(permuted){pc.mode_rows_in_coupled_order=mode;pc.original_D_singleton_exit_coverage=coverage;}
 const w=JSON.parse(JSON.stringify(p));w.parent_paired_collection_provenance=w.paired_collection;delete w.paired_collection;
 Object.assign(w,{schema:permuted?'moonshot-S008-permuted-coupled-entry-rank8-debt-v1':'moonshot-S008-mixed-coupled-entry-rank7-debt-v1',program:ops,parent_event_of_output:lineage,parent_word_sha256:'bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17',marks:Object.fromEntries(Object.entries(p.marks).map(([k,v])=>[k,boundaries[v]])),native_event_to_physical:p.native_event_to_physical.map(v=>{need(v in mapping,'native event not deleted');return mapping[v];}),coupled_precondition:pc});
 w.marks.all_mixed_donors_restored=w.marks.all_active_donors_restored;delete w.marks.all_active_donors_restored;
 return w;
}

function checkEntryPrefix(s,p,w) {
 const need=(x,m)=>{if(!x)throw Error(m);};
 const clone=x=>({d:x.d,m:new Map(x.m)}),unit=i=>({d:0,m:new Map([[i,1n]])}),zero=()=>({d:0,m:new Map()});
 const frac=s=>{const z=String(s).split('/'),n=BigInt(z[0]),d=z.length===1?1n:BigInt(z[1]);let k=0,t=d;while(t>1n&&!(t&1n)){t>>=1n;k++;}need(t===1n,'dyadic scalar');return[n,k];};
 const norm=x=>{if(!x.m.size){x.d=0;return;}while(x.d>0&&[...x.m.values()].every(v=>!(v&1n))){x.d--;for(const[k,v]of x.m)x.m.set(k,v>>1n);}};
 const add=(x,y,ns)=>{const[n,k]=frac(ns);if(!n)return;const d=Math.max(x.d,y.d+k);if(d>x.d){for(const[j,v]of x.m)x.m.set(j,v<<BigInt(d-x.d));x.d=d;}const f=n<<BigInt(d-y.d-k);for(const[j,v]of y.m){const q=(x.m.get(j)||0n)+f*v;if(q)x.m.set(j,q);else x.m.delete(j);}norm(x);};
 const scale=(x,ss)=>{const[n,k]=frac(ss);x.d+=k;for(const[j,v]of x.m)x.m.set(j,v*n);norm(x);};
 const raw=p.private_role_map,initial=()=>{
 const v=Array.from({length:p.public},(_,i)=>unit(i));
 for(const[role,id]of Object.entries(raw))v[id]={d:0,m:new Map([[+role,1n],[id,1n]])};
 return v;};
 const pre=initial();
 for(const u of w.coupled_precondition.source_roles){
 const y=u+112,rr=w.coupled_precondition.K[u];const a={d:0,m:new Map([[u,1n],[raw[u],1n],[raw[y],-1n]])},c={d:0,m:new Map([[y,1n],[raw[y],2n]])};
 for(const[d,k]of rr){add(a,unit(raw[d]),String(k).startsWith('-')?String(k).slice(1):'-'+k);add(c,unit(raw[d]),k);}
 pre[raw[u]]=a;pre[raw[y]]=c;
 }
 const replay=(word,v,stop)=>{const st=new Map(v.map((row,i)=>[i,row])),loc=new Map(word.initial.map((c,i)=>[i,c]));
 for(let t=0;t<stop;t++){const e=word.program[t],op=e[0],a=e[1];if(op==='INIT'){need(!st.has(a),'fresh init');st.set(a,zero());loc.set(a,e[2]);}
 else if(op==='ADD'){need(st.has(a)&&st.has(e[2])&&loc.get(a)===e[4]&&loc.get(e[2])===e[4],'cochart ADD');add(st.get(a),clone(st.get(e[2])),e[3]);}
 else if(op==='SCALE'){need(st.has(a)&&loc.get(a)===e[3],'cochart SCALE');scale(st.get(a),e[2]);}
 else if(op==='COPY'){need(!st.has(a)&&st.has(e[2]),'COPY');st.set(a,clone(st.get(e[2])));loc.set(a,e[3]);}
 else if(op==='MOVE'){need(st.has(a)&&loc.get(a)===e[2],'MOVE source');loc.set(a,e[3]);}
 else if(op==='CLEAR'){need(st.has(a)&&loc.get(a)===e[2],'CLEAR');st.delete(a);loc.delete(a);}
 else throw Error('unknown opcode '+op);}
 return {st,loc};};
 const target=replay(p,pre,p.marks.common_starts),got=replay(w,initial(),w.marks.common_starts);
 need(target.st.size===got.st.size,'live field counts');
 let terms=0;for(const[id,row]of got.st){const other=target.st.get(id);need(other&&got.loc.get(id)===target.loc.get(id),'same live field/location');norm(row);norm(other);need(row.d===other.d&&row.m.size===other.m.size,'exact row denominator/support');for(const[j,v]of row.m)need(other.m.get(j)===v,'all1880 input coefficient');terms+=row.m.size;}
 need(JSON.stringify(p.program.slice(p.marks.common_starts))===JSON.stringify(w.program.slice(w.marks.common_starts)),'unchanged literal complete suffix');
 const removed=new Set(w.coupled_precondition.deleted_parent_half_scales),seen=[];
 for(let t=0;t<w.program.length;t++){const old=w.parent_event_of_output[t];if(old!==null){need(JSON.stringify(w.program[t])===JSON.stringify(p.program[old]),'unchanged inherited event');seen.push(old);}}
 need(seen.length===p.program.length-8&&seen.every((x,k)=>k===0||x>seen[k-1]),'chronological inherited events');
 const kept=new Set(seen);need(p.program.every((_,i)=>kept.has(i)!==removed.has(i)),'exactly eight deleted halfscales');
 const added=w.program.filter((_,t)=>w.parent_event_of_output[t]===null),moves=added.filter(e=>e[0]==='MOVE');
 need(moves.length===8&&moves.every(e=>e[2]===3&&s.frames[e[3]].length===1&&e[4]===true),'exact new8rank1');
 let live=0,peak=0;for(const e of added){if(e[0]==='INIT'){live++;peak=Math.max(peak,live);}if(e[0]==='CLEAR')live--;need(live>=0&&live<=1,'new temporary lifecycle');}need(live===0,'all temporary retired');
 return {status:'PASS_FRESH_EXACT_ALL1880_PREFIX_PRECOMPOSITION',basis:'1480 original common fields plus400 independent q=v-u coordinates; invertible change from all1880 original inputs',fields_compared:got.st.size,columns:1880,nonzero_coefficients_compared:terms,prefix_operations:w.marks.common_starts,literal_suffix_operations:w.program.length-w.marks.common_starts,new_owned_rank1_MOVEs:8,new_phase_peak_owned:peak,unchanged_parent_peak_owned:43,all_original_D_endpoints_preserved:true,coupled_X_debt:'-K*d; not restored',original_payload_hash_authentication_required:true,scope:'Exact dyadic symbolic prefix and literal complete-suffix composition. This is not a fresh full-common-matrix replay or complete multiplier.'};
}

export {pyjson,emitEntry,checkEntryPrefix};
