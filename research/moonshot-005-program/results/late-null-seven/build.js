"use strict";
// S009 actual late-null augmentation; coefficient identities use exact BigInt rationals.

const need=(q,m)=>{if(!q)throw Error(m)};
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a};
const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);need(d!==0n,"nonzero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]};
const parse=x=>{let v=String(x).split("/");return Q(v[0],v[1]??1)};
const plus=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const neg=x=>[-x[0],x[1]];
const minus=(x,y)=>plus(x,neg(y));
const mul=(x,y)=>Q(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>mul(x,Q(y[1],y[0]));
const str=x=>x[1]===1n?String(x[0]):String(x[0])+"/"+x[1];
const zero=()=>Q(0),one=()=>Q(1);
const mm=(A,B)=>A.map(row=>B[0].map((_,j)=>row.reduce((s,v,k)=>plus(s,mul(v,B[k][j])),zero())));
const tr=A=>A[0].map((_,j)=>A.map(row=>row[j]));
const eye=n=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>Q(i===j?1:0)));
const rref=A=>{let B=A.map(r=>r.slice()),piv=[],k=0;for(let j=0;j<(B[0]?.length??0)&&k<B.length;j++){let z=B.findIndex((r,i)=>i>=k&&r[j][0]!==0n);if(z<0)continue;[B[k],B[z]]=[B[z],B[k]];let v=B[k][j];B[k]=B[k].map(x=>div(x,v));for(let i=0;i<B.length;i++)if(i!==k){let c=B[i][j];B[i]=B[i].map((x,h)=>minus(x,mul(c,B[k][h])))}piv.push(j);k++}return {rows:B,pivots:piv,rank:k}};
const inverse=A=>{let n=A.length,B=rref(A.map((r,i)=>r.concat(eye(n)[i])));need(B.pivots.slice(0,n).every((j,i)=>j===i),"invertible");return B.rows.map(r=>r.slice(n))};
const rank=A=>rref(A).rank;
const serialize=A=>A.map(r=>r.map(str));

function buildNullSeven(s,p,receipt){
 const raw=Object.fromEntries(Object.entries(p.private_role_map).map(([k,v])=>[Number(k),v]));
 const host=Object.fromEntries(s.hosted.Dports.map((k,i)=>[s.live[k],[s.hosted.X2[i],s.hosted.Y2[i]]]));
 const B=[5,56,65,69,77,96,100,103],U=[17,19,30,38,40,47,52,60],I=U.slice(1),first=1880+p.owned_fields;
 const ghost=Object.fromEntries(I.map((u,i)=>[u,first+i])),ret=first+7,insert=new Map(),events=[];
 const put=(at,ops,kind,ports)=>{if(!insert.has(at))insert.set(at,[]);insert.get(at).push({ops,kind,ports})};
 const M=Array.from({length:8},()=>Array.from({length:8},zero));
 const sourceRoot=v=>{const bits=Array.from({length:9},(_,i)=>i).filter(i=>v>>i&1);if(bits.length===3)return Array.from({length:8},(_,i)=>bits.includes(8)?2*Number(bits.includes(i)):bits.includes(i)?1:-1);need(bits.length===7,"actual E8 root source");const [i,j]=Array.from({length:9},(_,k)=>k).filter(k=>!bits.includes(k));return Array.from({length:8},(_,k)=>j===8?(k===i?1:-1):2*(Number(k===i)-Number(k===j)))};
 const roots=Object.fromEntries(s.live.map(x=>[x,sourceRoot(s.frames[s.initial[x]][0])]));const gram=(x,y)=>Q(roots[x].reduce((z,v,j)=>z+v*roots[y][j],0),8);
 need(JSON.stringify(s.live.filter(x=>!host[x]).sort((a,b)=>a-b))===JSON.stringify(U),"actual eight missing hosted roles");for(const x of B)for(const y of B)need(str(gram(x,y))===String(Number(x===y)),"actual selected Gram frame");
 for(const g of receipt.source_coupled_groups){
  const old=p.paired_collection.groups.find(x=>x.chart===g.chart);need(old,"actual old group");const frame=g.chart<s.frames.length?s.frames[g.chart]:p.additional_charts.find(x=>x.index===g.chart).frame;need(frame.length===6,"actual C6 acquisition");
  for(let i=0;i<g.receivers.length;i++)for(let k=0;k<g.coupled_donors.length;k++){const u=g.coupled_donors[k],v=parse(g.matrix[i][k]),row=p.corrections[String(g.receivers[i])];need(str(v)===str(neg(gram(g.receivers[i]-112,u))),"coefficient from actual native root");const hit=row.find(([j])=>j===u);need(hit&&hit[1]===str(v),"actual retained primal coefficient");}
  for(let k=0;k<g.coupled_donors.length;k++)for(let i=0;i<g.receivers.length;i++)M[U.indexOf(g.coupled_donors[k])][B.indexOf(g.receivers[i]-112)]=neg(parse(g.matrix[i][k]));
  const us=g.coupled_donors.filter(u=>u!==17);if(!us.length)continue;
  if(old.kind==="rank2_direct_cochart"){
   need(old.chart===1105&&JSON.stringify(old.receivers)===JSON.stringify(g.receivers),"actual exceptional direct source");const ops=[];
   for(const u of us){const j=g.coupled_donors.indexOf(u);ops.push(["INIT",ghost[u],g.chart]);for(let i=0;i<4;i++)ops.push(["ADD",ghost[u],raw[host[g.receivers[i]-112][1]],str(neg(parse(g.matrix[i][j]))),g.chart]);ops.push(["MOVE",ghost[u],g.chart,127,true])}
   put(old.reads[0].event,ops,"direct null acquisition",us);
  }else{
   need(old.kind==="inverse_transpose"&&JSON.stringify(old.receivers)===JSON.stringify(g.receivers),"actual reciprocal source");
   const pre=[],post=[];for(const u of us){const j=g.coupled_donors.indexOf(u);pre.push(["INIT",ghost[u],g.chart]);for(let i=0;i<4;i++){const r=raw[old.injections[i].carrier_X2],c=parse(g.matrix[i][j]);pre.push(["ADD",ghost[u],r,str(neg(c)),g.chart]);post.push(["ADD",ghost[u],r,str(c),127])}pre.push(["MOVE",ghost[u],g.chart,127,true])}
   put(old.encoded,pre,"affine null encoding and arrival",us);put(old.at_hub,post,"affine null decoding before hosted inverse",us);
  }
 }
 need(rank(M)===7&&rank(M.slice(1))===7,"actual rank7 observation basis");
 const T=M.slice(1).concat([eye(8)[B.indexOf(56)]]),D=inverse(T),inputs=I.map(u=>ghost[u]).concat([ret]);
 need(D.flat().filter(x=>x[0]!==0n).length===33,"literal decoder33 additions");
 const dr=host[56][1],facet=s.final[dr],finish=[["INIT",ret,facet],["ADD",ret,raw[dr],"1",facet],["MOVE",ret,facet,127,true]];
 for(let i=0;i<8;i++)for(let j=0;j<8;j++)if(D[i][j][0]!==0n)finish.push(["ADD",raw[host[B[i]][0]],inputs[j],str(neg(D[i][j])),127]);
 for(const r of inputs)finish.push(["CLEAR",r,127]);put(p.marks.common_starts,finish,"one original return, exactB decoder and retirement",B);
 const ops=[],lineage=[],bound=[];for(let i=0;i<p.program.length;i++){for(const item of insert.get(i)??[]){let begin=ops.length;ops.push(...item.ops);lineage.push(...item.ops.map(()=>null));events.push({kind:item.kind,ports:item.ports,parent_boundary:i,begin,end:ops.length})}bound[i]=ops.length;ops.push(p.program[i]);lineage.push(i)}bound[p.program.length]=ops.length;
 const w=JSON.parse(JSON.stringify(p));w.schema="moonshot-S009-late-null-seven-plus-one-source-v1";w.parent_word_sha256="bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17";w.program=ops;w.parent_event_of_output=lineage;w.owned_fields=p.owned_fields+8;w.marks=Object.fromEntries(Object.entries(p.marks).map(([k,v])=>[k,bound[v]]));w.native_event_to_physical=p.native_event_to_physical.map(i=>bound[i]);w.parent_paired_collection_provenance=w.paired_collection;delete w.paired_collection;
 for(const x of B){const b=host[x][0],d=host[x][1];need(!w.paired_reverse_corrections[String(b)],"B output authentic in parent");w.paired_reverse_corrections[String(b)]=[[d,"-1"]]}
 w.late_null_seven={events,source_coupled_ports:U,selected_ghost_ports:I,omitted:17,ghost_fields:ghost,original_return_port:56,original_return_field:ret,observation_matrix:serialize(M),decoder:serialize(D),decoder_input_order:I.map(u=>"g"+u).concat(["d56"]),decoder_output_order:B,zero_relation:"g17-g19-g38+g40=0",all_old_raw_routes_literal:true};
 need(ops.length===77905,"exact new source instruction count");return w;
}

function rowAdd(a,b,c){
 const out=new Map(a);for(const [j,v]of b){const x=plus(out.get(j)??zero(),mul(c,v));if(x[0]===0n)out.delete(j);else out.set(j,x)}return out;
}
function prefix(s,w,stop=w.marks.common_starts){
 const state=Array.from({length:1880},(_,i)=>new Map([[i,one()]])),loc=w.initial.slice();
 for(let t=0;t<stop;t++){
  const e=w.program[t],[op,r]=e;
  if(op==="INIT"){need(!state[r]&&r>=1880,"new prefix owned lifetime");state[r]=new Map();loc[r]=e[2]}
  else if(op==="CLEAR"){need(state[r]&&loc[r]===e[2]&&r>=1880,"prefix owned retirement");state[r]=undefined;loc[r]=undefined}
  else if(op==="MOVE"){need(state[r]&&loc[r]===e[2],"prefix current MOVE at "+t);loc[r]=e[3]}
  else if(op==="SCALE"){need(state[r]&&loc[r]===e[3],"prefix scale cochart");const c=parse(e[2]);need(c[0]!==0n,"nonzero scalar");state[r]=new Map(Array.from(state[r],([j,v])=>[j,mul(c,v)]))}
  else{need(op==="ADD"||op==="COPY","prefix opcode");need(r!==e[2]&&state[r]&&state[e[2]]&&loc[r]===e[4]&&loc[e[2]]===e[4],"prefix scalar cochart at "+t);state[r]=rowAdd(state[r],state[e[2]],parse(e[3]))}
 }
 return {state,loc};
}
function equalRows(a,b){return a?.size===b?.size&&(!a||Array.from(a).every(([j,v])=>b.has(j)&&str(v)===str(b.get(j))))}
function frameSpan(f){let S=new Set([0]);for(const v of f)for(const x of Array.from(S))S.add(x^v);return S}
function typed(s,w){
 const frames=s.frames.concat((w.additional_charts??[]).map(x=>x.frame)),spaces=frames.map(frameSpan),loc=w.initial.slice(),raw=new Set(Object.values(w.private_role_map)),counts={},ranks={},rawRanks={};let living=0,peak=0,life=0;
 const inc=(m,k,n=1)=>m[k]=(m[k]??0)+n,sub=(a,b)=>a.size<b.size&&Array.from(a).every(v=>b.has(v));
 for(let t=0;t<w.program.length;t++){
  const e=w.program[t],[op,r]=e;inc(counts,op);need(r>=0&&r<1880+w.owned_fields,"declared physical field");
  if(op==="INIT"){need(r>=1880&&loc[r]===undefined,"fresh owned lifetime");loc[r]=e[2];life++;living++;peak=Math.max(peak,living)}
  else if(op==="CLEAR"){need(r>=1880&&loc[r]===e[2],"actual owned retirement");loc[r]=undefined;living--}
  else if(op==="MOVE"){const [a,b,own]=e.slice(2);need(loc[r]===a&&typeof own==="boolean"&&own===(r>=1880),"actual MOVE source and owner at "+t);need(sub(spaces[a],spaces[b])||own&&sub(spaces[b],spaces[a]),"strict nested actual MOVE at "+t);const k=Math.abs(frames[a].length-frames[b].length);inc(ranks,k);if(raw.has(r))inc(rawRanks,k);loc[r]=b}
  else if(op==="SCALE")need(loc[r]===e[3]&&parse(e[2])[0]!==0n,"actual scale");
  else{need(op==="ADD"||op==="COPY","known scalar opcode");need(r!==e[2]&&loc[r]===e[4]&&loc[e[2]]===e[4],"actual full scalar cochart at "+t)}
 }
 need(living===0&&loc.slice(0,1880).every(x=>x!==undefined)&&loc.slice(1880).every(x=>x===undefined),"all new and old owned lifetimes retired");return {bill:{instructions:w.program.length,opcode_counts:counts,move_rank_histogram:ranks,raw_histogram:rawRanks,owned_lifetimes:life,peak_owned:peak,final_owned:living},final_locations:loc.slice(0,1880)};
}

function verifyWord(s,p,w,parentReceipt){
 const old=prefix(s,p),now=prefix(s,w),raw=Object.fromEntries(Object.entries(w.private_role_map).map(([k,v])=>[Number(k),v])),host=Object.fromEntries(s.hosted.Dports.map((k,i)=>[s.live[k],[s.hosted.X2[i],s.hosted.Y2[i]]])),B=w.late_null_seven.decoder_output_order,changes=new Map();
 for(const x of B){const [b,d]=host[x];changes.set(raw[b],new Map([[raw[d],Q(-1)],[d,Q(1)]]))}
 for(let r=0;r<Math.max(old.state.length,now.state.length);r++){need(old.loc[r]===now.loc[r],"all live prefix locations preserved");let want=old.state[r];if(changes.has(r))want=rowAdd(want,changes.get(r),one());need(equalRows(want,now.state[r]),"exact1880 all-input source delta at field "+r)}
 const first=1880+p.owned_fields;const projection=w.program.filter(o=>o[1]<first&&!((o[0]==="ADD"||o[0]==="COPY")&&o[2]>=first));need(JSON.stringify(projection)===JSON.stringify(p.program),"old instruction projection entirely literal");
 const observationBoundary=w.late_null_seven.events.find(e=>e.kind==="one original return, exactB decoder and retirement").begin,observed=prefix(s,w,observationBoundary),actualObservations=[];
 for(const u of w.late_null_seven.selected_ghost_ports){const r=w.late_null_seven.ghost_fields[u],j=w.late_null_seven.source_coupled_ports.indexOf(u);let want=new Map();for(let k=0;k<B.length;k++){const d=host[B[k]][1],q=new Map([[raw[d],one()],[d,Q(-1)]]);want=rowAdd(want,q,parse(w.late_null_seven.observation_matrix[j][k]))}need(observed.loc[r]===127&&equalRows(observed.state[r],want),"authentic pure-D ghost observation at hub");actualObservations.push({port:u,field:r,chart:127,row:Array.from(observed.state[r],([j,c])=>[j,str(c)]).sort((a,b)=>a[0]-b[0])})}
 const tail=w.program.slice(w.marks.common_starts);need(JSON.stringify(tail)===JSON.stringify(p.program.slice(p.marks.common_starts)),"literal original common suffix");
 for(const x of B){const b=host[x][0],r=raw[b];const uses=tail.filter(o=>o[1]===r||(o[0]==="ADD"||o[0]==="COPY")&&o[2]===r);need(JSON.stringify(uses)===JSON.stringify([["ADD",r,b,"1",127]]),"no changed raw output feeds common execution")}
 const oldTyped=typed(s,p),t=typed(s,w);need(JSON.stringify(t.final_locations)===JSON.stringify(oldTyped.final_locations),"all final public charts");
 const keys=new Set([...Object.keys(t.bill.opcode_counts),...Object.keys(oldTyped.bill.opcode_counts)]),delta=Object.fromEntries(Array.from(keys,k=>[k,(t.bill.opcode_counts[k]??0)-(oldTyped.bill.opcode_counts[k]??0)]));need(delta.ADD===86&&delta.MOVE===8&&delta.INIT===8&&delta.CLEAR===8&&delta.SCALE===0&&delta.COPY===0,"exact actual invoice increment");
 need(JSON.stringify(t.bill.raw_histogram)===JSON.stringify(oldTyped.bill.raw_histogram),"all actual raw paths retained");const dr={};for(const k of new Set([...Object.keys(t.bill.move_rank_histogram),...Object.keys(oldTyped.bill.move_rank_histogram)])){const n=(t.bill.move_rank_histogram[k]??0)-(oldTyped.bill.move_rank_histogram[k]??0);if(n)dr[k]=n}need(JSON.stringify(dr)===JSON.stringify({"1":1,"3":7}),"all new owned calls charged");
 const H=Object.keys(host).map(Number),outside=H.filter(x=>!B.includes(x));for(const x of B)for(const y of H)need(plus(Q(x===y?1:0),now.state[raw[host[x][0]]].get(raw[host[y][1]])??zero())[0]===0n,"complete zero B residual row");for(const x of outside)for(const y of outside)need(str(plus(Q(x===y?1:0),now.state[raw[host[x][0]]].get(raw[host[y][1]])??zero()))===String(Number(x===y)),"actual88 by88 identity residual minor");
 const P={...parentReceipt.conditional_caller.P_partial},T=parentReceipt.conditional_caller.T4;P["1"]+=18;P["3"]+=126;
 const den=1n<<100n,N=(3n**199n)*(den**200n);let lo=0n,hi=3n*den+1n;while(hi-lo>1n){const m=(lo+hi)>>1n;if(m**200n<=N)lo=m;else hi=m}const costLo=plus(mul(Q(7),Q(lo,den)),one()),costHi=plus(mul(Q(7),Q(hi,den)),one()),mlo=minus(parse(parentReceipt.conditional_caller.remaining_moment_per_native_lower),costHi),mhi=minus(parse(parentReceipt.conditional_caller.remaining_moment_per_native_upper),costLo);
 return {status:"PASS_ACTUAL_LATE_NULL_SEVEN_PLUS_ONE_SOURCE_WORD",independent_input_coordinates:1880,bill:t.bill,ordinary_increment:delta,new_owned_move_profile:dr,hosted_reverse_residual_rank:88,completed_hosted_first_ports:B,completed_hosted_roles:B.map(x=>host[x][0]),source_word_payload_sha256:"bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a",source_native_sha256:"2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883",observation_rank:7,observation_boundary:observationBoundary,actual_observations:actualObservations,selected_ghost_ports:w.late_null_seven.selected_ghost_ports,one_original_return:56,conditional_caller:{P_partial:P,T4:T,paid_positions:Object.values(P).reduce((a,b)=>a+b,0),target_positions:Object.values(T).reduce((a,b)=>a+b,0),rank_surplus:Object.keys({...P,...T}).reduce((sum,k)=>sum+Number(k)*((T[k]??0)-(P[k]??0)),0),remaining_moment_per_native_lower:str(mlo),remaining_moment_per_native_upper:str(mhi),remaining_moment_per_native_decimal:Number(mlo[0])/Number(mlo[1]),all_eight_original_rank9_forward_packets_retained:true},scope:"Actual all1880-input finite source extension and full ownership invoice. No new kappa; complete global paired code, source access admission, ordinary/precision and all five foundations remain."};
}
if(typeof module!=="undefined")module.exports={buildNullSeven,verifyWord,prefix,typed,parse,str,rank,inverse,Q,one,neg,rowAdd,equalRows,need};
