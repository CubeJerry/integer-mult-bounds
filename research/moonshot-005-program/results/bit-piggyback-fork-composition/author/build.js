function buildPayloadFork(geometry, closePartial=false) {
 const R=geometry.native_roots, n=R.length;
 if(n!==111)throw Error("source length");
 const base=[92,36,54,38,55], A=[10,49], B=[1,41], targets=[...base,...A,...B];
 const dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0);
 for(let j=0;j<5;j++)for(let k=j+1;k<5;k++)if((dot(R[base[j]],R[base[k]])===0)!==((k-j===1)||(j===0&&k===4)))throw Error("not induced pentagon");
 for(const [S,others] of [[A,[0,1,2,3]],[B,[0,2,3,4]]]){if(dot(R[S[0]],R[S[1]])!==0)throw Error("payload nonorthogonal");for(const i of S)for(const j of others)if(dot(R[i],R[base[j]])!==0)throw Error("payload locality");}
 const charts={}; const ann=(id,ids)=>{charts[id]={kind:"ann",rows:ids.map(i=>R[i]),normal_roles:ids};return id;};const span=(id,ids)=>{charts[id]={kind:"span",rows:ids.map(i=>R[i]),source_roles:ids};return id;};
 charts.zero={kind:"span",rows:[]};ann("Hub",[]);for(let i=0;i<n;i++){span("L"+i,[i]);ann("F"+i,[i]);}
 ann("D",[base[0],base[2],base[3]]);ann("E_A",[base[0],base[2]]);ann("E_B",[base[0],base[3]]);span("Q_A",A);span("Q_B",B);
 const classes=[[base[1],...A],[base[4],...B]];
 for(let k=0;k<2;k++)for(let j=1;j<=3;j++)ann((k?"B":"A")+j,[base[0],base[k?3:2],...classes[k].slice(0,j)]);
 const ops=[],move=(r,c)=>ops.push(["MOVE",r,c]),add=(s,t)=>ops.push(["ADD",s,t]),init=(r,c)=>ops.push(["INIT",r,c]),clear=r=>ops.push(["CLEAR",r]);
 const X=i=>"X"+i,Y=i=>"Y"+i;
 const ownCharts={H:"F"+base[0],W:"F"+base[0],p:"D",S1:"E_A",S4:"E_B",S3:"F"+base[2],S2:"F"+base[3]};
 for(const [r,c] of Object.entries(ownCharts))init(r,c);
 for(const cl of classes){add(Y(cl[0]),Y(cl[1]));add(Y(cl[1]),Y(cl[2]));}
 for(let k=0;k<2;k++){
  const [first,a,b]=classes[k],tag=k?"B":"A",q="Q_"+tag,e="E_"+tag,s=k?"S4":"S1";
  move(Y(a),"L"+b);add(X(b),Y(a));
  move(X(a),q);move(X(b),q);add(X(a),X(b));
  move(Y(first),q);add(X(b),Y(first));
  move(Y(first),tag+"1");move(Y(a),tag+"2");move(Y(b),tag+"3");
  move(X(a),"Hub");
  move(X(b),"D");add(X(b),"p");move(X(b),e);add(X(b),s);
  move(X(b),"F"+base[0]);add(X(b),"W");move(X(b),"Hub");add(X(a),X(b));
  move(X(first),e);add(X(first),s);move(X(first),"F"+base[0]);add(X(first),"W");move(X(first),"Hub");
 }
 move(X(base[2]),"F"+base[3]);add(X(base[2]),"S2");move(X(base[2]),"Hub");
 move(X(base[3]),"F"+base[2]);add(X(base[3]),"S3");move(X(base[3]),"Hub");
 move(X(base[0]),"Hub");
 for(const j of [2,3]){move(Y(base[j]),"D");add("p",Y(base[j]));move(Y(base[j]),j===2?"E_A":"E_B");}
 move(Y(base[0]),"E_A");
 init("P","Hub");init("Q","Hub");
 for(const i of [base[0],base[1],base[4],...A,...B])add(X(i),"P");
 for(const i of base)add(X(i),"Q");
 move("P","F"+base[0]);move("Q","F"+base[0]);
 add("Q","H");add("Q","P");add("H","Q");add("P","Q");
 const sw=(a,b)=>{add(a,b);add(b,a);add(a,b);};
 move("P","E_A");sw("P","S1");move("Q","E_B");sw("Q","S4");
 add("S1",Y(base[0]));move(Y(base[0]),"F"+base[0]);add("H",Y(base[0]));add("W",Y(base[0]));
 add("S1",Y(base[2]));move(Y(base[2]),"F"+base[2]);add("S3",Y(base[2]));
 add("S4",Y(base[3]));move(Y(base[3]),"F"+base[3]);add("S2",Y(base[3]));
 for(let k=0;k<2;k++){const pkt=k?"Q":"P",tag=k?"B":"A";for(let j=0;j<3;j++){const yi=Y(classes[k][j]);move(pkt,tag+(j+1));add(pkt,yi);add(yi,pkt);move(yi,"F"+classes[k][j]);}move(pkt,"zero");clear(pkt);}
 for(const r of Object.keys(ownCharts))clear(r);
 if(closePartial)for(let i=0;i<n;i++)if(!targets.includes(i)){move(X(i),"Hub");move(Y(i),"F"+i);}
 return {format:"literal-monotone-linear-word-v1",source_recovery_blob:"8eba43d142c819c206dce5df87ea4571aaead287",native_sha256:"51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78",base,A,B,targets,closed_partial:closePartial,charts,operations:ops};
}

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

if(typeof module!=="undefined")module.exports={buildPayloadFork,buildNestedPayloadFork};
