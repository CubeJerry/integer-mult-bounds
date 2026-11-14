const fs=require("node:fs"),vm=require("node:vm"),crypto=require("node:crypto"),path=require("node:path");
if(process.argv.length!==3)throw Error("usage: node run.cjs RECOVERED_NATIVE_ROOTS.json");
const raw=fs.readFileSync(process.argv[2]);
if(crypto.createHash("sha256").update(raw).digest("hex")!=="8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e")throw Error("recovery SHA-256 mismatch");
const body=fs.readFileSync(path.join(__dirname,"check.js"),"utf8");
const result=vm.runInNewContext(body+"\ncheckWingStrict(g)",{g:JSON.parse(raw)},{timeout:30000});
process.stdout.write(JSON.stringify(result,null,2)+"\n");
