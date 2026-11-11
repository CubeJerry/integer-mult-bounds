#!/usr/bin/env node
"use strict";
const fs=require("node:fs");
const crypto=require("node:crypto");
const zlib=require("node:zlib");
const path=require("node:path");
const verifyWord=function verifyWord(w) {
const need=(b,s)=>{if(!b)throw Error(s);};
need(w.public===659&&w.owned_fields===237&&w.program.length===34137,"source dimensions");
let rows=Array.from({length:w.public+w.owned_fields},(_,i)=>i<w.public?1n<<BigInt(i):0n),mrows=Array.from({length:222},(_,i)=>1n<<BigInt(i)),cross=[];
for(let i=0;i<w.program.length;i++){const e=w.program[i],a=e[1],b=e[2];
 if(e[0]==="ADD"){rows[a]^=rows[b];if(a<222&&b<222)mrows[a]^=mrows[b];}
 else if(e[0]==="SWAP"){[rows[a],rows[b]]=[rows[b],rows[a]];if(a<222&&b<222)[mrows[a],mrows[b]]=[mrows[b],mrows[a]];else if((a<222)!==(b<222))cross.push([i,a,b]);}
 else if(e[0]==="INIT"||e[0]==="CLEAR")rows[a]=0n;
}
const expected=i=>(1n<<BigInt(i))^(i>=111&&i<222?1n<<BigInt(i-111):0n);
need(rows.slice(0,w.public).every((x,i)=>x===expected(i)),"original public endpoint");
need(cross.length===0,"no cross main/core SWAP");need(mrows.every((x,i)=>x===(1n<<BigInt(i))),"main-only word is identity");
const results=[];
for(const m of [2,4,6]){
 const pub=222*m+(w.public-222),n=pub+w.owned_fields+1,tmp=n-1,map=(a,c=0)=>a<222?c*222+a:222*m+a-222;
 let rr=Array.from({length:n},(_,i)=>i<pub?1n<<BigInt(i):0n),at=Array(n).fill(null),paid={},events=0;
 for(let c=0;c<m;c++)for(let a=0;a<222;a++)at[map(a,c)]=w.start[a];
 for(let a=222;a<w.public;a++)at[map(a)]=w.start[a];
 function emit(e){events++;const [op,a,b,f]=e;
  if(op==="ADD"){need(at[a]===f&&at[b]===f,"same-chart ADD");rr[a]^=rr[b];}
  else if(op==="SWAP"){[rr[a],rr[b]]=[rr[b],rr[a]];[at[a],at[b]]=[at[b],at[a]];}
  else if(op==="MOVE"){need(at[a]===b,"MOVE entrance");const rank=Math.abs(w.frames[String(b)].dim-w.frames[String(f)].dim);need(rank>0,"positive paid MOVE");paid[rank]=(paid[rank]||0)+1;at[a]=f;}
  else if(op==="INIT"){need(at[a]===null,"fresh owned INIT");at[a]=b;rr[a]=0n;}
  else if(op==="CLEAR"){need(at[a]===b,"owned CLEAR chart");at[a]=null;rr[a]=0n;}
  else throw Error(op);
 }
 for(const e of w.program){const [op,a,b,f]=e;
  if(op==="ADD"||op==="SWAP"){need(op!=="SWAP"||((a<222)===(b<222)),"cross-class SWAP");
   if(a<222){for(let c=0;c<m;c++)emit([op,map(a,c),map(b,b<222?c:0),f]);}else emit([op,map(a),map(b,0),f]);
  }else if(a<222){for(let c=0;c<m;c++)emit([op,map(a,c),...e.slice(2)]);}else emit([op,map(a),...e.slice(2)]);
 }
 let before=0;for(let c=0;c<m;c++)for(let a=0;a<222;a++){const wanted=(1n<<BigInt(map(a,c)))^(a>=111?1n<<BigInt(map(a-111,c)):0n);if(rr[map(a,c)]!==wanted)before++;}
 need(before===111*(m-1),"precise missing shears");
 for(let c=1;c<m;c++)for(let p=0;p<111;p++){
  const xx=map(p,c),x0=map(p,0),y=map(111+p,c),fi=at[xx],fo=at[y];
  need(w.frames[String(fi)].dim===8&&w.frames[String(fo)].dim===7&&at[x0]===fi,"repair frame dimensions");
  emit(["INIT",tmp,fi]);emit(["ADD",tmp,xx,fi]);emit(["ADD",tmp,x0,fi]);emit(["MOVE",tmp,fi,fo]);emit(["ADD",y,tmp,fo]);emit(["CLEAR",tmp,fo]);
 }
 for(let i=0;i<pub;i++){let wanted=1n<<BigInt(i);if(i<222*m&&(i%222)>=111)wanted^=1n<<BigInt(i-111);need(rr[i]===wanted,"all new public endpoint coefficients");}
 const ending=[];for(let c=0;c<m;c++)ending.push(...w.final.slice(0,222));ending.push(...w.final.slice(222));
 for(let i=0;i<n;i++)need(at[i]===(i<pub?ending[i]:null),"all final frames and owned lifetimes");
 results.push({m,public_fields:pub,owned_labels:w.owned_fields+1,events,paid,missing_rows_before_repair:before,endpoint_mismatches_after_repair:0,repair_rank_one_calls:111*(m-1)});
}
const S=1n<<128n,cache=new Map();
function root(v,n){if(v<2n)return v;let x=1n<<BigInt(Math.ceil(v.toString(2).length/n));for(let j=0;j<10000;j++){const y=(BigInt(n-1)*x+v/(x**BigInt(n-1)))/BigInt(n);if(y>=x){need(x**BigInt(n)<=v&&(x+1n)**BigInt(n)>v,"adjacent root enclosure");return x;}x=y;}throw Error("root convergence");}
function pow(r){if(!cache.has(r)){const value=BigInt(r)**199n*S**200n,lo=root(value,200);cache.set(r,[lo,lo**200n===value?lo:lo+1n]);}return cache.get(r);}
let main={},core={},helper={};for(const e of w.program)if(e[0]==="MOVE"){const r=Math.abs(w.frames[String(e[2])].dim-w.frames[String(e[3])].dim),d=e[1]<222?main:core;d[r]=(d[r]||0)+1;}
for(let a=222;a<w.public;a++){const r=Math.abs(w.frames[String(w.start[a])].dim-w.frames[String(w.final[a])].dim);helper[r]=(helper[r]||0)+1;}
function delta(d,r,n){d[r]=(d[r]||0)+n;}
let M={};for(const r in helper)delta(M,+r,36*helper[r]);for(const r of new Set([...Object.keys(main),...Object.keys(core)]))delta(M,+r,-36*((main[r]||0)+(core[r]||0)));
delta(M,127,222);for(let j=1;j<=9;j++)delta(M,1+7*j,444);delta(M,1,-444);for(let j=1;j<=8;j++)delta(M,7*j,-444);
let D={};for(const r in core)delta(D,+r,core[r]);for(const r in helper)delta(D,+r,-helper[r]);
function interval(profile){let lo=0n,hi=0n;for(const[r,n]of Object.entries(profile)){const[a,b]=pow(+r);lo+=BigInt(n)*(n>=0?a:b);hi+=BigInt(n)*(n>=0?b:a);}return[lo,hi];}
const mi=interval(M),di=interval(D);need(mi[1]<-444n*S&&di[1]<88n*S,"full repaired-lift margin");
return {status:"PASS_FINITE_SOURCE_REPLAY_AND_SCOPED_COST_SCREEN",independent_review:"NOT_COMPLETED",base_commit:"e54523517d0f03e58352e647c403a5af3e525a57",main_only_identity:true,no_cross_main_core_swaps:true,source_public_endpoint_mismatches:0,source_finite_coefficients:659*659,results,main_paid:main,core_paid:core,helpers:helper,exact_moments:{scale:S.toString(),M2:mi.map(String),core_minus_helper:di.map(String),M2_upper:"-444",core_delta_upper:"88",repaired_lift_upper:"-222*m-414*(m-1) <0 for all integers m>=2"},new_kappa:null};
};
if(require.main===module){
 const input=process.argv[2];if(!input)throw Error("usage: node verify.js BIT-NATIVE-WORD.json.gz");
 const bytes=fs.readFileSync(input);
 if(crypto.createHash("sha256").update(bytes).digest("hex")!=="51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78")throw Error("source SHA256");
 const result=verifyWord(JSON.parse(zlib.gunzipSync(bytes).toString("utf8")));
 const expected=JSON.parse(fs.readFileSync(path.join(__dirname,"RESULT.json"),"utf8"));
 if(JSON.stringify(result)!==JSON.stringify(expected))throw Error("frozen result mismatch");
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
}
module.exports={verifyWord};
