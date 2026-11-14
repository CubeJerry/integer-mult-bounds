import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const here=dirname(fileURLToPath(import.meta.url));
for(const p of JSON.parse(readFileSync(resolve(here,'SOURCE-PINS.json'),'utf8'))){if(createHash('sha256').update(readFileSync(resolve(here,p.path))).digest('hex')!==p.sha256)throw new Error('Source pin mismatch: '+p.path);}
function verifyRecovery() {
  function q(r=0n,i=0n,e=0){r=BigInt(r);i=BigInt(i);if(r===0n&&i===0n)return[0n,0n,0];while(e>0&&(r&1n)===0n&&(i&1n)===0n){r>>=1n;i>>=1n;e--;}return[r,i,e];}
  const zero=q(),one=q(1),ii=q(0,1);
  function add(a,b){const e=Math.max(a[2],b[2]);return q((a[0]<<BigInt(e-a[2]))+(b[0]<<BigInt(e-b[2])),(a[1]<<BigInt(e-a[2]))+(b[1]<<BigInt(e-b[2])),e);}
  function neg(a){return q(-a[0],-a[1],a[2]);}
  function mul(a,b){return q(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0],a[2]+b[2]);}
  function conj(a){return q(a[0],-a[1],a[2]);}
  function eq(a,b){return a[0]===b[0]&&a[1]===b[1]&&a[2]===b[2];}
  function cmp(a,b){if(a[1]!==0n||b[1]!==0n)throw Error("ordered nonreal");const e=Math.max(a[2],b[2]);const d=(a[0]<<BigInt(e-a[2]))-(b[0]<<BigInt(e-b[2]));return d<0n?-1:d>0n?1:0;}
  function fmt(a){return String(a[0])+(a[1]<0n?"":"+")+String(a[1])+"i / 2^"+a[2];}
  function Z(n,m=n){return Array.from({length:n},()=>Array.from({length:m},()=>zero));}
  function I(n){const a=Z(n);for(let j=0;j<n;j++)a[j][j]=one;return a;}
  function mm(a,b){const c=Z(a.length,b[0].length);for(let i=0;i<a.length;i++)for(let j=0;j<b[0].length;j++)for(let k=0;k<b.length;k++)c[i][j]=add(c[i][j],mul(a[i][k],b[k][j]));return c;}
  function ma(a,b){return a.map((r,i)=>r.map((x,j)=>add(x,b[i][j])));}
  function mn(a){return a.map(r=>r.map(neg));}
  function star(a){return a[0].map((_,j)=>a.map(r=>conj(r[j])));}
  function me(a,b){return a.length===b.length&&a.every((r,i)=>r.length===b[i].length&&r.every((x,j)=>eq(x,b[i][j])));}
  function block(a,b,c,d){return a.map((r,i)=>r.concat(b[i])).concat(c.map((r,i)=>r.concat(d[i])));}
  function diag(a,b){return block(a,Z(a.length,b.length),Z(b.length,a.length),b);}
  function scalarDiag(xs){const a=Z(xs.length);xs.forEach((x,i)=>a[i][i]=x);return a;}
  function up(a){return block(I(a.length),a,Z(a.length),I(a.length));}
  function low(a){return block(I(a.length),Z(a.length),a,I(a.length));}
  function need(x,m){if(!x)throw Error(m);}
  function rowSupport(a){return Math.max(...a.map(r=>r.filter(x=>!eq(x,zero)).length));}
  function colSupport(a){return rowSupport(star(a));}
  function minSupport(a){return Math.min(...a.map(r=>r.filter(x=>!eq(x,zero)).length));}
  function maxEntry2(a){let v=zero;for(const row of a)for(const x of row){const z=mul(x,conj(x));if(cmp(z,v)>0)v=z;}return v;}
  function rowNorm2(a){let v=zero;for(const row of a){const z=row.reduce((t,x)=>add(t,mul(x,conj(x))),zero);if(cmp(z,v)>0)v=z;}return v;}
  function scale(a,k){return a.map(r=>r.map(x=>mul(x,k)));}
  const eye=I(4),zz=Z(4),H=[[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]].map(r=>r.map(x=>q(x,0,1)));
  const Q=scalarDiag([one,q(-1),ii,q(0,-1)]),Qi=star(Q),lambda=scalarDiag([one,one,ii,ii]),li=star(lambda);
  const S=mm(lambda,Qi),sign=scalarDiag([one,q(-1),one,one]),perm=I(4);[perm[0],perm[2]]=[perm[2],perm[0]];
  const Rs=[H,mm(mm(sign,H),sign),mm(mm(perm,H),star(perm))];
  need(me(mm(H,H),eye)&&me(mm(S,S),eye)&&me(mm(lambda,lambda),mm(Q,Q)),"head involution premises");
  const Bs=Rs.map(r=>mm(r,lambda)),Bi=Rs.map(r=>mm(li,r)),As=Bs.map(b=>mm(b,ma(S,mn(eye)))),Cs=Bi.map(b=>mm(ma(S,eye),b));
  let restored=0,reverse=0;
  for(let j=0;j<3;j++){
    const G=mm(Rs[j],Q),Gi=mm(Qi,Rs[j]);
    let w=up(G);
    for(const op of [diag(eye,lambda),diag(eye,Rs[j]),up(mn(eye)),diag(eye,Rs[j]),diag(eye,li)])w=mm(op,w);
    need(me(w,up(As[j])),"upper literal program");restored++;
    w=low(Gi);
    for(const op of [diag(Rs[j],eye),diag(li,eye),low(eye),diag(lambda,eye),diag(Rs[j],eye)])w=mm(op,w);
    need(me(w,low(Cs[j])),"lower literal program");restored++;
    need(!me(G,As[j])&&!me(Gi,Cs[j]),"omitted corrections");
    for(let k=0;k<3;k++){
      need(me(mm(As[j],Cs[k]),zz),"cross-stage annihilation");
      const ca=mm(Cs[k],As[j]);need(me(mm(ca,ca),zz),"reverse square-zero");
      if(!me(ca,zz))reverse++;
    }
  }
  need(reverse>0,"reverse order not silently zero");
  const events=[["U",0],["L",1],["U",2],["L",0],["U",1],["L",2],["U",0]];
  let w=I(8),sumA=Z(4),sumC=Z(4),tail=I(4);
  for(const [kind,j]of events){if(kind==="U"){w=mm(up(As[j]),w);sumA=ma(sumA,As[j]);}else{w=mm(low(Cs[j]),w);sumC=ma(sumC,Cs[j]);tail=ma(tail,mm(Cs[j],sumA));}}
  need(me(w,block(eye,sumA,sumC,tail)),"ordered head-only word");
  const a=q(1,1,1),b=q(1,-1,1),L=[[one,zero],[q(0,-1),one]],D=scalarDiag([a,q(1,1)]),U=[[one,q(0,-1)],[zero,one]];
  need(me(mm(mm(L,D),U),[[a,b],[b,a]]),"whole-field lambda pair LDU");
  const signs=[];
  for(const x of[-1,1])for(const y of[-1,1])for(const z of[-1,1]){
    let rank=24,e=0;for(const s of[x,y,z]){if(s<0){rank--;e=0;}else{rank+=e? -1:1;e=1;}}
    const single=24+y;need(rank+single<=48,"shared-middle rank");
    signs.push({sigma:[x,y,z],single,three:rank});
  }
  const unit=[eye,H,Rs[1],mm(Rs[1],H)];let unitTests=0;
  for(const uu of unit)for(const cc of unit)for(const vv of unit){
    const tt=mm(mm(uu,cc),vv),support=minSupport(tt);
    const rhs=mul(q(support*rowSupport(uu)*colSupport(vv)),maxEntry2(cc));
    need(cmp(rhs,one)>=0,"unitary sparse-row lemma");unitTests++;
  }
  let normTests=0;
  for(let power=1;power<=4;power++)for(let sh=0;sh<4;sh++)for(const tt of[eye,H,Rs[1]]){
    const dd=scalarDiag([q(1n<<BigInt(power)),q(1,0,power),one,one]);
    const di=scalarDiag([q(1,0,power),q(1n<<BigInt(power)),one,one]),e1=I(4),e1i=I(4);e1[0][1]=q(sh);e1i[0][1]=q(-sh);
    const uu=mm(dd,e1),ui=mm(e1i,di),cc=H,vv=mm(mm(star(cc),ui),tt);
    need(me(mm(mm(uu,cc),vv),tt),"arbitrary inverse-adapter factorization");
    const rhs=mul(mul(mul(q(minSupport(tt)*rowSupport(uu)*colSupport(vv)),rowNorm2(uu)),rowNorm2(star(vv))),maxEntry2(cc));
    need(cmp(rhs,one)>=0,"norm-aware bound");
    need(me(mm(vv,star(vv)),mm(mm(star(cc),mm(ui,star(ui))),cc)),"unitarily similar inverse Gram");
    normTests++;
  }
  const vv=I(4);for(let j=1;j<4;j++)vv[0][j]=q(-1);const uu=scale(eye,q(2)),tt=mm(mm(uu,H),vv);
  const falseBound=mul(q(minSupport(tt)*rowSupport(uu)*colSupport(vv)),maxEntry2(H));
  const corrected=mul(mul(falseBound,rowNorm2(uu)),rowNorm2(star(vv)));
  need(me([tt[0]],[eye[0]])&&cmp(falseBound,one)<0&&cmp(corrected,one)>=0,"norm omission control");
  const scaleInt=10n**24n, cache={};
  function pw(n){if(cache[n])return cache[n];const target=BigInt(n)**199n*scaleInt**200n;let l=0n,h=BigInt(n)*scaleInt;while(h-l>1n){const m=(l+h)/2n;if(m**200n<=target)l=m;else h=m;}need(l**200n<=target&&h**200n>target,"root brackets");return cache[n]=[l,h];}
  const paidLow=336n*[2,3,5,6].reduce((a,n)=>a+pw(n)[0],0n);
  const room2=224n*pw(25)[1]-paidLow,room1=112n*(pw(25)[1]+pw(24)[1])-paidLow,cost2=112n*pw(2)[0];
  const gap=112n*(pw(25)[1]+pw(23)[1])-paidLow;
  need(cost2>room2&&112n*scaleInt>room1&&gap<0n,"exact repair prices");
  return {status:"PASS_FRESH_RECOVERY_EXACT_CONTROLS",execution:"Pure JavaScript exact dyadic complex arithmetic and BigInt integer-root enclosures; original Python receipts are not reproduced.",
    complementary:{restored_programs:restored,cross_stage_pairs:9,nonzero_reverse_pairs:reverse,head_only_events:events.length,lambda_LDU:true},
    canonical_sign_cases:signs,unitary_controls:unitTests,nonunitary_controls:normTests,
    norm_negative_control:{incorrect:fmt(falseBound),corrected:fmt(corrected)},
    prices:{denominator:String(scaleInt),two_head_room_upper:String(room2),two_head_repair_lower:String(cost2),one_head_room_upper:String(room1),one_head_repair_lower:String(112n*scaleInt),maximal_sign_pair_gap_upper:String(gap)},
    scope:"Formal exact controls for the recovered proofs. No compressed source-word recreation, independent Python replay, completed productive caller or new kappa.",
    new_kappa:false};
}
console.log(JSON.stringify(verifyRecovery(),null,2));
