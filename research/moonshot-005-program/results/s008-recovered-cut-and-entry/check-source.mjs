#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';

function verifyRecovery(src,invoice) {
 const need=(x,s)=>{if(!x)throw Error(s);};
 const pop=n=>{let c=0;for(;n;n&=n-1)c++;return c;};
 const dot=(a,b)=>pop(a&b)&1;
 const span=bs=>{let out=[0];for(const b of bs){out=Array.from(new Set(out.concat(out.map(x=>x^b))));}return out.sort((a,b)=>a-b);};
 const qroot=b=>{const I=Array.from({length:9},(_,i)=>i).filter(i=>(b>>i)&1);if(I.length===3)return Array.from({length:9},(_,i)=>I.includes(i)?2:-1);need(I.length===7,'root label');const J=Array.from({length:9},(_,i)=>i).filter(i=>!I.includes(i));return Array.from({length:9},(_,i)=>3*((i===J[0]?1:0)-(i===J[1]?1:0)));};
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c;}return a;};
 const rank=M=>{const A=M.map(r=>r.map(BigInt));let p=0;if(!A.length)return 0;for(let j=0;j<A[0].length&&p<A.length;j++){let k=p;while(k<A.length&&!A[k][j])k++;if(k===A.length)continue;[A[k],A[p]]=[A[p],A[k]];for(let i=p+1;i<A.length;i++)if(A[i][j]){const aa=A[p][j],bb=A[i][j];for(let h=j;h<A[i].length;h++)A[i][h]=aa*A[i][h]-bb*A[p][h];let g=0n;for(let h=j;h<A[i].length;h++)g=gcd(g,A[i][h]);if(g)for(let h=j;h<A[i].length;h++)A[i][h]/=g;}p++;}return p;};
 const X=[...src.live].sort((a,b)=>a-b),H=src.hosted.Dports.map(k=>X[k]).sort((a,b)=>a-b),HS=new Set(H),U=X.filter(i=>!HS.has(i));
 need(X.length===104&&H.length===96&&U.join(',')==='17,19,30,38,40,47,52,60','source families');
 const L=Object.fromEntries(X.map(i=>[i,src.frames[src.initial[i]][0]]));
 const A=Object.fromEntries(X.map(i=>[i,qroot(L[i])]));
 const G2=(i,j)=>A[i].reduce((s,x,k)=>s+x*A[j][k],0)/9;
 need(X.every(i=>G2(i,i)===2),'independent Q9 norm normalization');
 need(rank(H.map(i=>A[i]))===8,'hosted rank8');
 const hosted=Object.fromEntries(src.hosted.Dports.map((k,j)=>[X[k],[src.hosted.X2[j],src.hosted.Y2[j]]]));
 for(const i of H){const [b,d]=hosted[i];need(src.initial[b]===src.initial[i]&&src.final[b]===127,'B endpoints');need(src.initial[d]===3&&src.final[d]===src.final[i+112],'D endpoints');}
 need(X.every(i=>src.initial[i+112]===3&&src.final[i]===127),'first family endpoints');
 const facets=Object.fromEntries(X.map(i=>[i,new Set(span(src.frames[src.final[i+112]]))]));
 need(X.every(i=>facets[i].size===256&&!facets[i].has(L[i])),'odd self facets');
 need(X.every(i=>[...facets[i]].every(v=>!dot(v,L[i]))),'native facet normal');
 const nnz=H.reduce((s,i)=>s+H.filter(j=>G2(i,j)!==0).length,0);need(nnz===4350,'hosted Gram support');
 const entry=U.map(u=>{const support=H.filter(i=>G2(u,i)!==0);need(support.length>=42,'coupled minimum weight');need(H.every(i=>(G2(u,i)!==0)===facets[i].has(L[u])),'coupled incidence without diagonal exception');return {role:u,line:L[u],support,weight:support.length};});
 const singleton={};for(const i of H){const n=U.filter(u=>!facets[i].has(L[u])).length;singleton[n]=(singleton[n]||0)+1;}
 need(Object.keys(singleton).length>0&&Object.keys(singleton).every(k=>+k>0),'arbitrary entry can exit singleton');
 const frame=[5,56,65,69,77,96,100,103];need(frame.every(i=>frame.every(j=>G2(i,j)===(i===j?2:0))),'frame orthogonality');
 const groups=new Map();for(const x of X)if(!frame.includes(x)){const key=frame.filter(i=>G2(i,x)!==0).join(',');need(key.split(',').length===4,'cohort recipients');groups.set(key,true);}
 need(groups.size===14,'14 source cohorts');
 const births=[...groups.keys()].sort().map(key=>{const f=key.split(',').map(Number),C=Array.from({length:512},(_,v)=>v).filter(v=>f.every(i=>!dot(v,L[i])));need(C.length===64,'C6 cohort');const support=H.filter(i=>C.every(v=>!dot(v,L[i])));need(support.length===4,'C6 support four');return {receivers:f,chart:C,support};});
 const cuts=[];for(let g=0;g<births.length;g++)for(let h=g+1;h<births.length;h++){const W=new Set([...births[g].support,...births[h].support]),J=H.filter(i=>!W.has(i));need(W.size<42&&rank(J.map(i=>A[i]))===8,'union complement Gram rank');const inside=v=>J.some(i=>facets[i].has(v));const insideA=X.filter(i=>inside(L[i])),insideB=H.filter(i=>inside(L[i]));need(U.every(u=>inside(L[u])),'all coupled entries stay inside');const outsideY=X.filter(i=>!J.includes(i)),outsideD=H.filter(i=>!J.includes(i));need(outsideY.length===104-J.length&&outsideD.length===96-J.length,'distinct final facets');const firstRank=insideA.length+outsideY.length;const capacity=insideA.length+insideB.length+outsideY.length+outsideD.length+7;const target=firstRank+insideB.length+outsideD.length+8;need(target===capacity+1,'one field cut deficit');cuts.push({birth_pair:[g,h],removed:W.size,n_A:insideA.length,n_B:insideB.length,first_family_rank:firstRank,outward_capacity:capacity,required_rank:target});}
 const knap=(R,s)=>{if(R<0)return -1;const d=new Array(R+1).fill(0);for(let c=1;c<=R;c++)for(let r=1;r<=Math.min(c,s);r++)d[c]=Math.max(d[c],d[c-r]+2**(r-1));return d[R];};
 const k48=Array.from({length:6},(_,i)=>knap(48-7*(i+1),i+1)),k49=Array.from({length:6},(_,i)=>knap(49-7*(i+1),i+1));
 need(k48.join(',')==='41,34,36,40,36,32'&&k49.join(',')==='42,35,37,41,40,33','exact distance-only knapsack');
 let checked=0,pass=[];function profiles(n,r,counts){if(r===1){const cc={...counts};if(n)cc[1]=n;checked++;const list=[];for(const [k,v] of Object.entries(cc))for(let a=0;a<v;a++)list.push(+k);list.sort((a,b)=>a-b);const c=list.slice(0,Math.max(0,list.length-7)).reduce((s,k)=>s+2**(k-1),0);if(list.length>=8&&c>=42)pass.push(cc);return;}for(let nR=0;nR<=Math.floor(n/r);nR++){const c={...counts};if(nR)c[r]=nR;profiles(n-nR*r,r-1,c);}}
 profiles(49,9,{});need(checked===40831&&pass.length===1&&pass[0][1]===49&&Object.keys(pass[0]).length===1,'rank49 census');
 need(50n**200n>9n*49n**200n,'rank50 price exceeds49');
 const D=10n**30n,D200=D**200n,cache=new Map();
 const power=r=>{if(cache.has(r))return cache.get(r);const target=BigInt(r)**199n*D200;let lo=0n,hi=BigInt(r)*D+1n;while(hi-lo>1n){const m=(hi+lo)/2n;if(m**200n<=target)lo=m;else hi=m;}need(lo**200n<=target&&hi**200n>target,'directed power bracket');const pair=[lo,hi];cache.set(r,pair);return pair;};
 const moment=h=>{let lo=0n,hi=0n;for(const [r,c]of Object.entries(h)){const [a,b]=power(+r);lo+=BigInt(c)*a;hi+=BigInt(c)*b;}return [lo,hi];};
 const raw={1:990,2:360,3:105,4:112,5:133,6:8,7:2};
 const paid=owned=>{const h={...invoice.P4};for(const [r,n]of Object.entries(raw))h[r]-=18*n;h[8]=(h[8]||0)+18*400;for(const [r,n]of Object.entries(owned))h[r]=(h[r]||0)+18*n;need(Object.values(h).every(v=>v>=0),'nonnegative invoice');return h;};
 const T=moment(invoice.T4),allow=owned=>{const pp=paid(owned),P=moment(pp);return {paid:pp,lower:(T[0]-P[1]).toString(),upper:(T[1]-P[0]).toString(),denominator:(18n*D).toString()};};
 const old=allow({9:8}),late=allow({1:1,7:1,8:1,9:6});const den=18n*D;
 need(57n*den>BigInt(late.upper),'all-private total57 exceeds allowance');
 need(63n*den>BigInt(late.upper),'63 mode bound exceeds allowance');
 const p5=power(5),pglo=10n*p5[0],pghi=10n*p5[1];need(pglo*18n>BigInt(late.upper),'two-gate floor exceeds late invoice');
 const paretoC=[[2,12],[4,10],[6,8],[8,4]],paretoD=paretoC.map(([a,b])=>[b,a]);let supportBound=0,corner=[];
 for(const [x,y]of paretoC)for(const [ap,B]of paretoD){const a=Math.min(x,ap),b=y,bp=Math.min(B,y),v=a*b+(ap-a)*bp+Math.min(ap-a,b-bp);corner.push([a,b,ap,bp,v]);supportBound=Math.max(supportBound,v);}
 need(supportBound===70&&Math.ceil(nnz/supportBound)===63&&62*70<nnz,'63 support consequence');
 const aligned=U.map(u=>H.filter(i=>G2(u,i)!==0).length).reduce((a,b)=>a+b,0);
 const assign=[5,56,69,65,96,103,100,77];
 const permutedTerms=assign.reduce((s,r)=>s+H.filter(i=>G2(r,i)!==0).length,0);
 const coverage=H.filter(i=>U.some((u,k)=>!facets[i].has(L[u])&&G2(assign[k],i)!==0));
 need(aligned===354&&permutedTerms===360&&coverage.length===96,'entry mode source facts');
 return {status:'PASS_FRESH_CLOUD_SOURCE_AND_EXACT_PRICE_RECONSTRUCTION',source_gzip_sha256:'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',source_payload_sha256:'8f248653791e44acc88aab2e149957e9c2cb3ffa5f7bb958002c9994631a16ca',independent_root_model:'nine-coordinate zero-sum integer roots; squared norm18',hosted_Gram_nonzero_blocks:nnz,coupled_entry_rows:entry,singleton_entry_exit_histogram:singleton,cohort_births:births,union_cut_cases:cuts,rank49_profiles_checked:checked,rank49_profiles_passing:pass,knapsack48:k48,knapsack49:k49,retained_distance_only_moment_floor:49,eight_entry_total_floor:57,old_allowance:old,late_two_allowance:late,two_gate_price:{lower:pglo.toString(),upper:pghi.toString(),denominator:D.toString()},all_private_deficit_lower:{numerator:(57n*den-BigInt(late.upper)).toString(),denominator:den.toString()},pure_mode_support_upper:70,pure_mode_minimum:63,pareto_corners:corner,aligned_terms:aligned,permuted_terms:permutedTerms,permuted_singleton_coverage:coverage.length,negative_controls:['Singleton coverage is not inherited for arbitrary changed entry payloads.','Rank49 relaxation only permits49rank1.','62 modes cover at most4340 of4350 nonzero blocks.','Entry singleton coverage is not a restoration theorem.'],scope:'Fresh finite source and exact interval reconstruction after runtime loss. Universal proofs and the inherited distance42/Pareto theorems are separate. No original CP5 byte recovery or new complete kappa claimed.'};
}

const repo=path.resolve(process.argv[2]||'.');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const source=fs.readFileSync(path.join(repo,'research/shared-wire-split-composition/data/final.json.gz'));
if(hash(source)!=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883')throw Error('source pin');
const payload=zlib.gunzipSync(source);
if(hash(payload)!=='8f248653791e44acc88aab2e149957e9c2cb3ffa5f7bb958002c9994631a16ca')throw Error('source payload');
const bill=fs.readFileSync(path.join(repo,'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json'));
if(hash(bill)!=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248')throw Error('invoice pin');
const result=verifyRecovery(JSON.parse(payload),JSON.parse(bill));
const text=JSON.stringify(result,null,2)+'\n';
if(process.argv[3])fs.writeFileSync(process.argv[3],text);
console.log(JSON.stringify({status:result.status,source_cuts:result.union_cut_cases.length,rank49_profiles:result.rank49_profiles_checked,exact_all_private_floor:result.eight_entry_total_floor,pure_mode_floor:result.pure_mode_minimum},null,2));
