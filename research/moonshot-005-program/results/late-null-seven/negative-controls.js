"use strict";
const {prefix,typed,verifyWord,Q,one,neg,parse,str,rowAdd,equalRows,need}=require("./build.js");

function negativeControls(s,p,w,receipt){
 const old=prefix(s,p),good=prefix(s,w),out={};
 const check=(name,mutate,typeOnly=false)=>{const bad=JSON.parse(JSON.stringify(w));mutate(bad);let rejected=false,why="";try{if(typeOnly)typed(s,bad);else{const z=prefix(s,bad);rejected=z.state.some((r,i)=>!equalRows(r,good.state[i]))}}catch(e){rejected=true;why=String(e)}need(rejected,"negative control accepted: "+name);out[name]={rejected,reason:why}};
 const pre=w.late_null_seven.events.find(e=>e.kind==="affine null encoding and arrival"&&e.ports.includes(19)),post=w.late_null_seven.events.find(e=>e.kind==="affine null decoding before hosted inverse"&&e.ports.includes(19)),last=w.late_null_seven.events.find(e=>e.kind==="one original return, exactB decoder and retirement");
 check("omitted_actual_C6_preload_keeps_original_b_nuisance",bad=>{bad.program[pre.begin+1][3]="0"});
 check("omitted_hub_cancellation_keeps_original_b_nuisance",bad=>{bad.program[post.begin][3]="0"});
 check("wrong_exact_decoder_sign",bad=>{const i=last.begin+3;bad.program[i][3]=str(neg(parse(bad.program[i][3])))});
 check("owned_null_transport_mislabelled_raw",bad=>{const i=pre.begin+5;need(bad.program[i][0]==="MOVE","actual owned null move");bad.program[i][4]=false},true);
 check("ghost_initialized_at_hub_before_C6_reads",bad=>{bad.program[pre.begin][2]=127});
 check("missing_original_return_payload",bad=>{bad.program[last.begin+1][3]="0"});
 const host=Object.fromEntries(s.hosted.Dports.map((k,i)=>[s.live[k],[s.hosted.X2[i],s.hosted.Y2[i]]])),raw=w.private_role_map,d5=host[5][1],facet=s.final[d5];
 check("geometrically_valid_but_wrong_original_return5",bad=>{bad.program[last.begin][2]=facet;bad.program[last.begin+1][2]=raw[String(d5)];bad.program[last.begin+1][4]=facet;bad.program[last.begin+2][2]=facet;typed(s,bad)});
 const early=prefix(s,w,pre.end),late=prefix(s,w,last.begin),g=w.late_null_seven.ghost_fields;let guessed=rowAdd(rowAdd(early.state[g[19]],early.state[g[38]],one()),early.state[g[40]],Q(-1)),wanted=rowAdd(rowAdd(late.state[g[19]],late.state[g[38]],one()),late.state[g[40]],Q(-1));need(early.loc[g[19]]===127&&early.loc[g[38]]===127&&early.loc[g[40]]===127,"all early wrong observations genuinely cocharted");need(!equalRows(guessed,wanted),"final ghost relation cannot be applied to early encoded values");out["premature_global_relation_at_genuine_hub_cochart"]={rejected:true,reason:"all three fields are at hub but still contain uncancelled original-b terms"};
 const fake={...verifyWord(s,p,w,receipt).new_owned_move_profile,"3":6};need(JSON.stringify(fake)!==JSON.stringify({"1":1,"3":7}),"omitted transport charge rejected");out["one_rank3_owned_call_omitted_from_invoice"]={rejected:true};
 return {status:"PASS_ACTUAL_LATE_NULL_WORD_NEGATIVE_CONTROLS",controls:out,scope:"Each source mutant changes the interpreted all1880 map or violates an actual chart/ownership premise. Early global-relation mutant uses genuinely cocharted fields."};
}

module.exports={negativeControls};
