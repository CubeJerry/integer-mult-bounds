const fs=require("node:fs"),vm=require("node:vm"),path=require("node:path");
const here=__dirname,read=n=>fs.readFileSync(path.join(here,n),"utf8");
for(const n of ["build.js","check.js","geometry-check.js","price.js","negative-check.js","scaling-check.js"])vm.runInThisContext(read(n),{filename:n});
const G=JSON.parse(read("SOURCE-GEOMETRY.json")),out={};
for(const closed of [false,true]){const word=buildTwoD5Word(G,closed),f=closed?"CLOSED.json":"PREFIX.json";if(JSON.stringify(word)!==JSON.stringify(JSON.parse(read(f))))throw Error("emission mismatch "+f);out[f]=checkPayloadFork(word,G);}
out.negative=checkTwoD5NegativeControls(JSON.parse(read("PREFIX.json")),G);
out.scaling=checkOneDirectionRestriction(G,JSON.parse(read("PREFIX.json")));
out.geometry=checkTwoD5Geometry(G,JSON.parse(read("PREFIX.json")));
out.price=priceTwoD5(out["CLOSED.json"].movement_profile);
console.log(JSON.stringify({status:"PASS",negative_controls:out.negative,scaling_status:out.scaling.status,all_original_input_columns:222,prefix_counts:out["PREFIX.json"].counts,closed_counts:out["CLOSED.json"].counts,profile:out["CLOSED.json"].movement_profile,history_rank:out["PREFIX.json"].carried_x_rank,geometry:out.geometry,moment:out.price.moment},null,2));
