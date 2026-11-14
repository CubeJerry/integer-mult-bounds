function buildNestedPayloadFork(geometry, closePartial=false) {
 const R=geometry.native_roots,n=111,base=[92,36,54,38,55],fresh=[23,1,18],next=[36,23,55,1,18],targets=[...base,...fresh],charts={};
 const ann=(id,ids)=>{charts[id]={kind:"ann",rows:ids.map(i=>R[i]),normal_roles:ids};return id;},span=(id,ids)=>{charts[id]={kind:"span",rows:ids.map(i=>R[i]),source_roles:ids};return id;};
 charts.zero={kind:"span",rows:[]};ann("Hub",[]);for(let i=0;i<n;i++){span("L"+i,[i]);ann("F"+i,[i]);}
 ann("D",[92,54,38]);ann("E_A",[92,54]);ann("E_B",[92,38]);
 const dn=[92,54,38];ann("N0",[...dn,36]);ann("N2",[...dn,55]);ann("N02",[...dn,36,55]);ann("N03",[...dn,36,1]);
 charts.G3={kind:"ann",rows:[R[92],R[38],R[1],R[54].map((x,k)=>x-R[36][k])],source_expressions:[[[92,1]],[[38,1]],[[1,1]],[[54,1],[36,-1]]]};
 const ops=[],markers={},move=(r,c)=>ops.push(["MOVE",r,c]),add=(s,t)=>ops.push(["ADD",s,t]),init=(r,c)=>ops.push(["INIT",r,c]),clear=r=>ops.push(["CLEAR",r]),X=i=>"X"+i,Y=i=>"Y"+i;
 const old={H:"F92",W:"F92",p:"D",S1:"E_A",S4:"E_B",S3:"F54",S2:"F38"},freshCaches={NH:"N0",NS1:"N02",NS4:"N03",NS3:"N2",NS2:"G3"};
 for(const [r,c]of Object.entries({...old,...freshCaches}))init(r,c);
 move(X(23),"N02");add(X(23),"NS1");move(X(23),"D");
 move(X(18),"N03");add(X(18),"NS4");move(X(18),"D");add(X(23),X(18));add(X(18),"p");
 move(X(23),"Hub");move(X(18),"E_A");add(X(18),"S1");move(X(18),"F92");add(X(18),"W");move(X(18),"Hub");add(X(23),X(18));
 move(X(1),"N2");add(X(1),"NS3");move(X(1),"D");add(X(1),"p");move(X(1),"E_B");add(X(1),"S4");move(X(1),"F92");add(X(1),"W");move(X(1),"Hub");
 move(X(36),"E_A");add(X(36),"S1");move(X(36),"F92");add(X(36),"W");move(X(36),"Hub");
 move(X(55),"G3");add(X(55),"NS2");move(X(55),"E_B");add(X(55),"S4");move(X(55),"F92");add(X(55),"W");move(X(55),"Hub");
 move(X(54),"F38");add(X(54),"S2");move(X(54),"Hub");move(X(38),"F54");add(X(38),"S3");move(X(38),"Hub");move(X(92),"Hub");
 for(const[i,e]of[[54,"E_A"],[38,"E_B"]]){move(Y(i),"D");add("p",Y(i));move(Y(i),e);}move(Y(92),"E_A");
 init("P","Hub");init("Q","Hub");for(const i of[92,36,55,23,18,1])add(X(i),"P");for(const i of base)add(X(i),"Q");
 move("P","F92");move("Q","F92");add("Q","H");add("Q","P");add("H","Q");add("P","Q");
 const sw=(a,b)=>{add(a,b);add(b,a);add(a,b);};move("P","E_A");sw("P","S1");move("Q","E_B");sw("Q","S4");
 add("S1",Y(92));move(Y(92),"F92");add("H",Y(92));add("W",Y(92));
 add("S1",Y(54));move(Y(54),"F54");add("S3",Y(54));add("S4",Y(38));move(Y(38),"F38");add("S2",Y(38));
 markers.first_fork_complete=ops.length;
 for(const r of Object.keys(old))clear(r);
 move("P","D");move("Q","D");markers.common_rank5=ops.length;
 add("P","Q");move("P","N0");move("Q","N0");add("Q","NH");add("Q","P");add("NH","Q");add("P","Q");
 move("P","N02");sw("P","NS1");move("Q","N03");sw("Q","NS4");move("P","zero");move("Q","zero");
 add("P",Y(23));move(Y(23),"F23");add("Q",Y(18));move(Y(18),"F18");
 add("P",Y(36));add("Q",Y(36));move(Y(36),"N03");add("NS4",Y(36));move(Y(36),"N0");add("NH",Y(36));move(Y(36),"F36");
 move(Y(55),"N02");add("NS1",Y(55));move(Y(55),"N2");add("NS3",Y(55));move(Y(55),"F55");
 move(Y(1),"N03");add("NS4",Y(1));move(Y(1),"G3");add("NS2",Y(1));move(Y(1),"F1");
 markers.second_fork_complete=ops.length;
 for(const r of["P","Q",...Object.keys(freshCaches)])clear(r);
 if(closePartial)for(let i=0;i<n;i++)if(!targets.includes(i)){move(X(i),"Hub");move(Y(i),"F"+i);}
 return{format:"literal-monotone-linear-word-v1",source_recovery_blob:"8eba43d142c819c206dce5df87ea4571aaead287",native_sha256:"51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78",base,next,fresh,targets,closed_partial:closePartial,charts,markers,operations:ops};
}

function buildCubicInjection(geometry,zString,mode="prefix") {
 const baseWord=buildNestedPayloadFork(geometry,false),R=geometry.native_roots,baseTargets=baseWord.targets,z=BigInt(zString),support=R.map((_,i)=>i).filter(i=>(z>>BigInt(i))&1n),dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0);
 if(!z||support.some(i=>![92,54,38].every(j=>dot(R[i],R[j])===0)))throw Error("z outside D");
 if(((z>>1n)&1n)!==((z>>18n)&1n))throw Error("carrier coefficients differ");
 if(!["prefix","control","closed"].includes(mode))throw Error("mode");
 const extras=support.filter(i=>!baseTargets.includes(i)),moved=[...baseTargets,...extras].sort((a,b)=>a-b),ops=[],markers={},move=(r,c)=>ops.push(["MOVE",r,c]),add=(s,t)=>ops.push(["ADD",s,t]),init=(r,c)=>ops.push(["INIT",r,c]),clear=r=>ops.push(["CLEAR",r]),X=i=>"X"+i,Y=i=>"Y"+i;
 const old={H:"F92",W:"F92",p:"D",S1:"E_A",S4:"E_B",S3:"F54",S2:"F38"},fresh={NH:"N0",NS1:"N02",NS4:"N03",NS3:"N2",NS2:"G3"};
 for(const[r,c]of Object.entries({...old,...fresh,Z:"D"}))init(r,c);
 for(const i of extras){init("R"+i,"L"+i);add(X(i),"R"+i);}
 move(X(23),"N02");add(X(23),"NS1");move(X(23),"D");
 move(X(18),"N03");add(X(18),"NS4");move(X(18),"D");
 move(X(1),"N2");add(X(1),"NS3");move(X(1),"D");
 for(const i of extras)move(X(i),"D");
 for(const i of support)add(X(i),"Z");
 add(X(23),X(18));add("Z",X(18));add("Z",X(1));add(X(18),"p");add(X(1),"p");
 move(X(23),"Hub");for(const i of extras)move(X(i),"Hub");
 move(X(18),"E_A");add(X(18),"S1");move(X(18),"F92");add(X(18),"W");move(X(18),"Hub");
 move(X(1),"E_B");add(X(1),"S4");move(X(1),"F92");add(X(1),"W");move(X(1),"Hub");
 add(X(23),X(18));add(X(18),X(1));for(const i of support)if(i!==18)add(X(i),X(18));add(X(18),X(1));
 move(X(36),"E_A");add(X(36),"S1");move(X(36),"F92");add(X(36),"W");move(X(36),"Hub");
 move(X(55),"G3");add(X(55),"NS2");move(X(55),"E_B");add(X(55),"S4");move(X(55),"F92");add(X(55),"W");move(X(55),"Hub");
 move(X(54),"F38");add(X(54),"S2");move(X(54),"Hub");move(X(38),"F54");add(X(38),"S3");move(X(38),"Hub");move(X(92),"Hub");
 for(const[i,e]of[[54,"E_A"],[38,"E_B"]]){move(Y(i),"D");add("p",Y(i));move(Y(i),e);}move(Y(92),"E_A");
 init("P","Hub");init("Q","Hub");for(const i of[92,36,55,23,18,1])add(X(i),"P");for(const i of[92,36,54,38,55])add(X(i),"Q");markers.packets_loaded=ops.length;
 move("P","F92");move("Q","F92");add("Q","H");add("Q","P");add("H","Q");add("P","Q");
 const sw=(a,b)=>{add(a,b);add(b,a);add(a,b);};move("P","E_A");sw("P","S1");move("Q","E_B");sw("Q","S4");
 add("S1",Y(92));move(Y(92),"F92");add("H",Y(92));add("W",Y(92));
 add("S1",Y(54));move(Y(54),"F54");add("S3",Y(54));add("S4",Y(38));move(Y(38),"F38");add("S2",Y(38));
 markers.three_targets_complete=ops.length;for(const r of Object.keys(old))clear(r);move("P","D");move("Q","D");markers.injected_handoff=ops.length;
 const row=ids=>ids.reduce((x,i)=>x^(1n<<BigInt(i)),0n);
 const expectedOwned={NH:{chart:"N0",value:"0"},NS1:{chart:"N02",value:row([23]).toString(16)},NS4:{chart:"N03",value:row([18]).toString(16)},NS3:{chart:"N2",value:row([1]).toString(16)},NS2:{chart:"G3",value:row([55]).toString(16)},Z:{chart:"D",value:z.toString(16)},P:{chart:"D",value:(row([36,23,18])^z).toString(16)},Q:{chart:"D",value:(row([55,1])^z).toString(16)}};for(const i of extras)expectedOwned["R"+i]={chart:"L"+i,value:row([i]).toString(16)};
 if(mode!=="prefix"){add("Z","P");add("Z","Q");clear("Z");for(const i of extras)clear("R"+i);ops.push(...baseWord.operations.slice(baseWord.markers.common_rank5));}
 if(mode==="closed")for(let i=0;i<111;i++){if(!moved.includes(i))move(X(i),"Hub");if(!baseTargets.includes(i))move(Y(i),"F"+i);}
 return{...baseWord,construction:"shared-cubic-mode-injection",injected_mode_hex:z.toString(16),injected_mode_support:support,mode,operations:ops,markers,closed_partial:mode==="closed",moved_original_sources:moved,completed_targets:mode==="prefix"?[92,54,38]:baseTargets,expected_owned_roles:mode==="prefix"?expectedOwned:{},live_owned_expected:mode==="prefix"?Object.keys(expectedOwned).length:0};
}

if(typeof module!=="undefined")module.exports={buildNestedPayloadFork,buildCubicInjection};
