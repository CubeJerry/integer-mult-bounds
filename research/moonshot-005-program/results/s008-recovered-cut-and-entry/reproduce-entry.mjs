#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import zlib from 'node:zlib';
import {pyjson,emitEntry,checkEntryPrefix} from './entry-core.mjs';
const repo=path.resolve(process.argv[2]||'.'),out=path.resolve(process.argv[3]||'/tmp/s008-entry-reproduction');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const native=fs.readFileSync(path.join(repo,'research/shared-wire-split-composition/data/final.json.gz'));
const parent=fs.readFileSync(path.join(repo,'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz'));
if(hash(native)!=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'||hash(parent)!=='bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17')throw Error('source/parent gzip pin');
const s=JSON.parse(zlib.gunzipSync(native)),p=JSON.parse(zlib.gunzipSync(parent));
if(hash(pyjson(p))!=='bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a')throw Error('parent canonical serialization');
fs.mkdirSync(out,{recursive:true});
const results={};
for(const permuted of [false,true]){
 const mode=permuted?'permuted':'aligned',w=emitEntry(s,p,permuted),payload=Buffer.from(pyjson(w));
 const expected=permuted?'06844c10a8dba2145c07cb517a7f9d8a383806aa5a42feff8ce6d7b36cad8bd8':'91e3358f3e09ada6eb81b9bc9d40086912872e2df8216e9dc265ce8af00c456a';
 if(hash(payload)!==expected)throw Error('original payload not reproduced');
 const review=checkEntryPrefix(s,p,w),blob=zlib.gzipSync(payload,{level:9});
 fs.writeFileSync(path.join(out,mode+'-WORD.json.gz'),blob);
 const controls=[],rec=w.coupled_precondition.preloads[0];
 for(const[name,index,change]of[
 ['packet-sign',rec.first_event+2,e=>{e[3]=e[3][0]==='-'?e[3].slice(1):'-'+e[3];}],
 ['wrong-packet-line',rec.consumer-1,e=>{e[3]=3;}],
 ['missing-Y-compensation',rec.consumer+2,e=>{e[3]='0';}],
 ['wrong-independent-source',rec.first_event+1,e=>{e[2]=w.private_role_map[rec.K_row[0][0]];}]
 ]){
  const v={...w,program:[...w.program]};v.program[index]=[...v.program[index]];change(v.program[index]);
  let reason=null;try{checkEntryPrefix(s,p,v);}catch(e){reason=e.message;}
  if(reason===null)throw Error('mutant passed '+name);controls.push({mode,name,rejected:true,reason});
 }
 results[mode]={payload_sha256:hash(payload),gzip_sha256:hash(blob),review,controls,scope:'Original payload identity; gzip wrapper may differ.'};
}
fs.writeFileSync(path.join(out,'REPRODUCTION.json'),JSON.stringify(results,null,2)+'\n');
console.log(JSON.stringify(Object.fromEntries(Object.entries(results).map(([k,v])=>[k,{payload_sha256:v.payload_sha256,status:v.review.status,controls:v.controls.length}])),null,2));
