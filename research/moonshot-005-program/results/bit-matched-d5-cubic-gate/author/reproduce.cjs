const fs=require("node:fs"),vm=require("node:vm"),path=require("node:path");
const read=n=>fs.readFileSync(path.join(__dirname,n),"utf8");
vm.runInThisContext(read("check.js"),{filename:"check.js"});
const out=checkMatchedD5Family(JSON.parse(read("SOURCE-GEOMETRY.json")),JSON.parse(read("CERTIFICATE.json")));
console.log(JSON.stringify(out,null,2));
