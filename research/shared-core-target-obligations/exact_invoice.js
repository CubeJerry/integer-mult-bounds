// Independent exact arithmetic; no contributor scientific code imported.
function run() {
const T={1:234,2:324,3:792,4:3870,5:1224,6:756,7:324,8:1206,9:11126,17:416,25:416,33:416,41:416,49:416,57:416,65:416,73:416,145:208};
const P={1:73766,2:14904,3:14598,4:4338,5:5760,6:306,7:216,8:812,16:416,24:416,32:416,40:416,48:416,56:416,64:416};
const H={1:13,2:18,3:44,4:215,5:68,6:42,7:18,8:67,9:595};
const G={1:3085,2:468,3:706,4:129,5:187,6:9,7:10,8:6};
const O={1:20,2:9,3:2,4:13,5:2,6:1};
const keys=Array.from(new Set([...Object.keys(T),...Object.keys(P)]),Number);
const den=10n**15n;
function need(b,m){if(!b)throw Error(m);}
function iroot(N,k){
 let x=1n<<BigInt(Math.ceil(N.toString(2).length/Number(k)));
 while(true){const y=((k-1n)*x+N/x**(k-1n))/k;if(y>=x)break;x=y;}
 while((x+1n)**k<=N)x++;while(x**k>N)x--;
 need(x**k<=N&&N<(x+1n)**k,"root bound");return x;
}
let M4lo=0n,M4hi=0n,Mlo=0n,Mhi=0n,gainlo=0n,gainhi=0n,Olo=0n,Ohi=0n,tn=0,pn=0,mass=0;
const T4={},P4={};
for(const r of keys){
 const q=iroot(BigInt(r)**199n*den**200n,200n);
 const a=2*(T[r]||0)-18*(H[r]||0),b=2*(P[r]||0)-18*(G[r]||0);
 need(a>=0&&b>=0,"counts");if(a)T4[r]=a;if(b)P4[r]=b;tn+=a;pn+=b;mass+=r*(a-b);
 M4lo+=BigInt(a)*q-BigInt(b)*(q+1n);M4hi+=BigInt(a)*(q+1n)-BigInt(b)*q;
 Mlo+=BigInt(T[r]||0)*q-BigInt(P[r]||0)*(q+1n);
 Mhi+=BigInt(T[r]||0)*(q+1n)-BigInt(P[r]||0)*q;
 gainlo+=18n*(BigInt(G[r]||0)*q-BigInt(H[r]||0)*(q+1n));
 gainhi+=18n*(BigInt(G[r]||0)*(q+1n)-BigInt(H[r]||0)*q);
 Olo+=BigInt(O[r]||0)*q;Ohi+=BigInt(O[r]||0)*(q+1n);
}

need(1771183385n*10n**9n<M4lo&&M4hi<1771183386n*10n**9n,"moment target");
need(tn===27344&&pn===152424&&mass===5056,"profile totals");
const dupLo=M4lo-18n*Ohi,dupHi=M4hi-18n*Olo;
need(dupHi<0n,"duplicated owned bank fails target moment");
const scalar=2*1777040+96*20*16,routes=8020+2160+800+1600+216;
const native=18*(scalar+routes*1000),caller=2*599605216,conversion=18*1880*104,lambda=2*14480000,total=native+caller+conversion+lambda;
need(total===1526544192,"ordinary total");
return {status:"PASS_INDEPENDENT_EXACT_BIGINT_RECOMPUTATION",
denominator:String(den),T4,P4,productive_count:tn,paid_count:pn,rank_surplus:mass,
M4_numerator_bounds:[String(M4lo),String(M4hi)],
selected_M_numerator_bounds:[String(Mlo),String(Mhi)],
sharing_gain_numerator_bounds:[String(gainlo),String(gainhi)],
owned_moment_numerator_bounds:[String(Olo),String(Ohi)],
duplicated_owned_M_numerator_bounds:[String(dupLo),String(dupHi)],
necessary_owned_saving_per_native:{numerator_bounds:[String(-dupHi),String(-dupLo)],denominator:String(18n*den),strict:true},
source_invoice:{scalar,routes,native,caller,conversion,lambda,total},
scope:"Conditional profile arithmetic from manually transcribed pinned source census. No H4 word or physical total."};
}
const result=run();
if(typeof text==="function")text(result);
else console.log(JSON.stringify(result,null,2));
