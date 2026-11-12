"use strict";
// Recovery transcription check only; not a full source-word verifier.
function checkRecoveredGroup(manifest) {
  const g = manifest.packages.eight_cohort.group_zero;
  const I = g.pivots.map(x => g.donors.indexOf(x));
  if (new Set(I).size !== 4 || I.some(x => x < 0)) throw Error("pivot indices");
  const A2 = g.A_half_integer_rows.map(r => I.map(i => r[i]));
  const B = g.A_I_inverse;
  const mul = (a,b) => a.map(r => b[0].map((_,j) => r.reduce((s,x,k) => s+x*b[k][j],0)));
  const twiceIdentity = Array.from({length:4},(_,i) => Array.from({length:4},(_,j) => 2*Number(i===j)));
  if (JSON.stringify(mul(A2,B)) !== JSON.stringify(twiceIdentity) ||
      JSON.stringify(mul(B,A2)) !== JSON.stringify(twiceIdentity)) throw Error("pivot inverse");
  const parity = n => { let p=0; while(n) { p^=n&1; n>>>=1; } return p; };
  let C=[0];
  for (const b of g.frame) C=[...new Set([...C,...C.map(x=>x^b)])];
  const perp=Array.from({length:512},(_,x)=>x).filter(x=>g.frame.every(b=>parity(x&b)===0));
  const odd=perp.filter(parity);
  if (C.length!==64 || JSON.stringify(perp)!==JSON.stringify(g.annihilator) ||
      JSON.stringify(odd)!==JSON.stringify(g.odd_annihilator_vectors)) throw Error("binary geometry");
  const J=g.donors.map((_,i)=>i).filter(i=>!I.includes(i));
  let inputSamples=0;
  for (let z=0;z<2187;z++) {
    let q=z;
    const v=Array.from({length:7},()=>{const t=q%3-1;q=Math.floor(q/3);return t;});
    const encoded2=g.A_half_integer_rows.map(r=>r.reduce((s,x,i)=>s+x*v[i],0));
    const minus2=encoded2.map((a,k)=>a-J.reduce((s,j)=>s+g.A_half_integer_rows[k][j]*v[j],0));
    const recovered2=B.map(r=>r.reduce((s,x,i)=>s+x*minus2[i],0));
    if (recovered2.some((x,k)=>x!==2*v[I[k]])) throw Error("inverse evaluation");
    inputSamples++;
  }
  return {
    status:"PASS_RECOVERY_TRANSCRIPTION_ALGEBRA_ONLY",
    source_manifest_blob:"a795e186d68d9b93173442614100e3230626ee2b",
    source_manifest_sha256:"8c9808c42298cf562b48462951ef3bb18a4be2cf2b865e8dbd9d2c601babb42f",
    field:"exact rational via doubled integer coefficients",
    both_minor_inverse_identities:true,
    integer_input_samples:inputSamples,
    binary_chart_dimension:6,
    annihilator:perp,
    odd_annihilator:odd,
    scope:"Fresh independent root JavaScript check of the recovered group-zero matrix/inverse and binary-space arithmetic. Does not authenticate source label associations, other13 groups, physical word, route maps, invoice or full cohort correctness. No independent full-word PASS."
  };
}
if (typeof module!=="undefined") {
  module.exports={checkRecoveredGroup};
  if (require.main===module) {
    const fs=require("node:fs"), path=require("node:path"), crypto=require("node:crypto");
    const input=process.argv[2] || path.join(__dirname,"SOURCE-COUPLING-RECOVERY.json");
    const bytes=fs.readFileSync(input);
    const expected="8c9808c42298cf562b48462951ef3bb18a4be2cf2b865e8dbd9d2c601babb42f";
    if (crypto.createHash("sha256").update(bytes).digest("hex")!==expected) throw Error("manifest pin");
    console.log(JSON.stringify(checkRecoveredGroup(JSON.parse(bytes.toString("utf8"))),null,2));
  }
}
