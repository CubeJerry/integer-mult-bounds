// Independent literal integer ADD interpreter and negative controls.
function run() {
function I(n){return Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>BigInt(i===j)));}
function add(R,a,b,c){R[a]=R[a].map((x,j)=>x+BigInt(c)*R[b][j]);}
function eq(A,B){return A.every((r,i)=>r.every((x,j)=>x===B[i][j]));}
function bus(R,m,sgn){for(let i=0;i<m;i++){add(R,m+i+1,0,-1);add(R,0,i+1,sgn[i]);}for(let i=0;i<m;i++){add(R,0,i+1,-sgn[i]);add(R,m+i+1,0,1);}}
function swap(R,a,b,s=1){add(R,a,b,s);add(R,b,a,-s);add(R,a,b,s);}
function mixed({encode=true,cancel=true,signs=[1,1,-1,-1],stale=false}={}){
 const R=I(9);if(encode){swap(R,5,6);swap(R,7,8);}bus(R,4,signs);
 swap(R,5,6,-1);swap(R,7,8,-1);if(stale)add(R,1,2,1);
 if(cancel)for(let i=0;i<4;i++)for(let j=0;j<4;j++)if((i<2)!==(j<2))add(R,i+5,j+1,i%2?1:-1);
 if(stale)add(R,1,2,-1);return R;
}
function need(b,m){if(!b)throw Error(m);}
for(let m=1;m<=16;m++){
 const R=I(2*m+1),E=I(2*m+1);bus(R,m,Array(m).fill(1));
 for(let i=0;i<m;i++)for(let j=0;j<m;j++)E[m+i+1][j+1]=BigInt(Number(j>i)-Number(j<i));
 need(eq(R,E),"bus "+m);
}
const goal=I(9);[1,1,-1,-1].forEach((s,i)=>goal[i+5][i+1]=BigInt(s));
need(eq(mixed(),goal),"mixed goal");
const controls=[{encode:false},{cancel:false},{signs:[1,1,1,1]},{stale:true}];
controls.forEach((c,i)=>need(!eq(mixed(c),goal),"negative "+i));
const stale=mixed({stale:true});

return {status:"PASS_INDEPENDENT_INTEGER_MATRIX_REPLAY",tested_m:"1..16",
four_plane_map:"(S,D,H) -> (S,D+diag(1,1,-1,-1)S,H)",
controls:["omitted input encoding","omitted cross cancellations","wrong reverse signs","changed source versions during cross correction, then restored"],
stale_target_residual_rows:stale.slice(5).map((r,i)=>r.map((x,j)=>String(x-goal[i+5][j]))),
scope:"Literal exact ADD algebra; hypothetical matching-chart access windows and native itinerary remain required."};
}
const result=run();
if(typeof text==="function")text(result);
else console.log(JSON.stringify(result,null,2));
