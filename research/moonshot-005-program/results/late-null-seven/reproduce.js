"use strict";
const fs=require("node:fs"),path=require("node:path"),A=require("./build.js"),C=require("./codec.js"),N=require("./negative-controls.js");
const repo=path.resolve(process.argv[2]??process.cwd()),out=path.resolve(process.argv[3]??path.join(__dirname,"output")),base=path.join(repo,"research/moonshot-005-program/results");
const sb=fs.readFileSync(path.join(repo,"research/shared-wire-split-composition/data/final.json.gz")),pb=fs.readFileSync(path.join(base,"paired-cohort/output/WORD.json.gz"));
A.need(C.sha256(sb)==="2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883","native compressed pin");
A.need(C.sha256(pb)==="bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17","paired compressed pin");
const pairedBytes=C.gunzip(pb);A.need(C.sha256(pairedBytes)==="bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a","paired payload pin");
const s=JSON.parse(C.utf8(C.gunzip(sb))),p=JSON.parse(C.utf8(pairedBytes)),g=JSON.parse(fs.readFileSync(path.join(base,"preterminal-coupled-eight/output/NULL-PADDING-CHECK.json"),"utf8")),pr=JSON.parse(fs.readFileSync(path.join(base,"paired-cohort/output/RESULT.json"),"utf8"));
const w=A.buildNullSeven(s,p,g),r=A.verifyWord(s,p,w,pr),payload=C.utf8Encode(JSON.stringify(w)),blob=C.gzipFixed(payload,C.crc32);
r.word_sha256=C.sha256(blob);r.word_payload_sha256=C.sha256(payload);r.compression="Deterministic RFC1951 fixed-Huffman LZ77; CRC and ISIZE independently decoded by recovery utility";
A.need(r.word_sha256==="35baf768106f262ff43b60f2223e243f52b331e4943cf11295a18c53a00fdf7b","new gzip pin");A.need(r.word_payload_sha256==="f1b2424537b320bf01f9c1e966d6868991df1048b4351f284ba7fcc2585c8ab6","new payload pin");A.need(C.sha256(C.gunzip(blob))===r.word_payload_sha256,"CRC/size/full payload compression roundtrip");
const controls=N.negativeControls(s,p,w,pr),frames=s.frames.concat(p.additional_charts.map(x=>x.frame)),first=1880+p.owned_fields,charts=[];
for(let i=0;i<w.program.length;i++){const o=w.program[i];if(o[0]!=="MOVE"||o[1]<first)continue;const j=p.program.findIndex(z=>z[0]==="MOVE"&&z[2]===o[2]&&z[3]===o[3]);A.need(j>=0,"inherited exact chart pair");charts.push({new_event:i,new_owned_field:o[1],from:o[2],to:o[3],rank:frames[o[3]].length-frames[o[2]].length,inherited_parent_event:j,parent_operation:p.program[j]})}
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,"WORD.json.gz"),blob);for(const [name,obj]of [["RESULT.json",r],["NEGATIVE-CONTROLS.json",controls],["CHART-INHERITANCE.json",charts]])fs.writeFileSync(path.join(out,name),JSON.stringify(obj,null,2)+"\n");
console.log(JSON.stringify({status:r.status,word:r.word_sha256,payload:r.word_payload_sha256,instructions:r.bill.instructions,peak:r.bill.peak_owned,margin:r.conditional_caller.remaining_moment_per_native_decimal},null,2));
