"""Independent dense400 dyadic replay; no author engine imported."""
import argparse,collections,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dense_engine import run,span,eqrow
if not __debug__:raise SystemExit('Exact checks require Python without -O')
PINS={'native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','caller':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','manifest':'968d32f22757790f3c2217b29be5c4f3df931ee65822ee50d5dcf2f05475d1ab','parent':'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','word':'806280ff6b56eada3927251ff09ae8b26e9388fd770320dd7fa382aef1782502','m3':'5d795c178ea2b6fd4acec89740a515ca41c2d42372e1c3c7bd673b7d6dd5018f'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p,pin):
 b=p.read_bytes();assert sha(b)==pin,(str(p),sha(b));return json.loads(gzip.decompress(b))
def rank(rows):
 basis={}
 for row in rows:
  d={i:F(v) for i,v in enumerate(row) if v}
  while d:
   p=min(d)
   if p not in basis:
    c=d[p];basis[p]={i:v/c for i,v in d.items()};break
   c=d[p]
   for i,v in basis[p].items():
    w=d.get(i,F(0))-c*v
    if w:d[i]=w
    elif i in d:del d[i]
 return len(basis)
def root9(n):
 bits=[i for i in range(9) if n>>i&1]
 if len(bits)==3:return [2 if i in bits else -1 for i in range(9)]
 assert len(bits)==7;a,b=[i for i in range(9) if i not in bits]
 return [3*int(i==a)-3*int(i==b) for i in range(9)]
def integer_root(n,k):
 v=1<<((n.bit_length()+k-1)//k)
 while True:
  z=((k-1)*v+n//v**(k-1))//k
  if z>=v:break
  v=z
 while (v+1)**k<=n:v+=1
 while v**k>n:v-=1
 assert v**k<=n<(v+1)**k
 return v
def main(a):
 mb=(a.bundle/'MANIFEST.json').read_bytes();assert sha(mb)==PINS['manifest'];man=json.loads(mb)
 for name,pin in man['artifacts'].items():assert sha((a.bundle/name).read_bytes())==pin,name
 s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',PINS['native']);q=load(a.bundle/'source-evidence/rail-consumer.json.gz',PINS['parent']);w=load(a.bundle/'output/rail-dyadic.json.gz',PINS['word']);m3=load(a.bundle/'m3/WORD.json.gz',PINS['m3'])
 receipt=json.loads((a.bundle/'output/RESULT.json').read_text());mr=json.loads((a.bundle/'m3/RESULT.json').read_text())
 roles={int(k):v for k,v in q['source_role_map'].items()};rev={v:k for k,v in roles.items()}
 assert sorted(rev)==list(range(400)) and q['initial']==[s['initial'][rev[i]] for i in range(400)]
 assert all(w[k]==q[k] for k in ['initial','source_role_map','frames','owned_fields'])
 spaces=list(map(span,w['frames']));assert spaces[3]=={0} and len(spaces[127])==512
 live=s['live'];DP={live[k] for k in s['hosted']['Dports']};U=sorted(set(live)-DP);assert U==[17,19,30,38,40,47,52,60]
 u={17:1,19:-1,38:-1,40:1};yp=roles[129]
 host={live[k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
 assert len(host)==96 and len(live)==104 and tuple(F(s['hosted'][k]) for k in ['alpha','beta','alpha2','beta2'])==(F(-1),F(1,2),F(-1),F(0))
 oldprefix=[];prefix=[]
 for j in U:
  L=s['initial'][j];oldprefix.extend([['INIT',400,3],['ADD',400,roles[j+112],'1',3],['MOVE',400,3,L,True],['ADD',roles[j],400,'-1',L],['CLEAR',400,L]])
 for j,c in u.items():
  L=s['initial'][j];prefix.extend([['INIT',400,3],['ADD',400,yp,'1',3],['MOVE',400,3,L,True],['ADD',roles[j],400,str(-c),L],['CLEAR',400,L]])
 prefix += [['SCALE',roles[j+112],'1/2',3] for j in U if j!=17]
 prefix += [['ADD',roles[j+112],yp,str(F(c,2)),3] for j,c in u.items() if j!=17]
 assert len(prefix)==30 and q['program'][:40]==oldprefix and w['program']==prefix+q['program'][40:]
 print('Replaying parent and changed400-input words',flush=True)
 old,do,lo,oldbill,_=run(q,spaces);new,dn,ln,bill,sn=run(w,spaces,capture_before={30:('prefix',list(range(400)))})
 assert ln==lo=={i:s['final'][rev[i]] for i in range(400)}
 dp,pre,pl=sn['prefix'];one=1<<dp
 for i in range(400):
  want=[int(i==j)*one for j in range(400)];native=rev[i]
  if native in U:want[yp]-=u.get(native,0)*one
  if native-112 in U:
   j=native-112;want=[int(k==i)*(one//2) for k in range(400)];want[yp]+=u.get(j,0)*(one//2)
  assert pre[i]==want and pl[i]==q['initial'][i]
 # Parent-row precomposition T, independently applied to all400 coefficients.
 for i,row in old.items():
  target=[2*x for x in row]
  for j in U:
   x,y=roles[j],roles[j+112];target[y]+=row[x]-row[y];target[yp]+=u.get(j,0)*(row[y]-row[x])
  assert eqrow(new[i],dn,target,do+1),(i,'parent precomposition')
 for j in U:
  x,y=roles[j],roles[j+112];c=u.get(j,0)
  assert [2*pre[y][k]-c*pre[yp][k] for k in range(400)]==[int(k==y)*one for k in range(400)]
  assert [pre[x][k]+c*pre[yp][k] for k in range(400)]==[int(k==x)*one for k in range(400)]
  assert eqrow(new[x],dn,pre[x],dp)
 # Original-input endpoint targets, not precomposed targets.
 d=max(do,dn,1);os={i:[x<<(d-do) for x in r] for i,r in old.items()};ns={i:[x<<(d-dn) for x in r] for i,r in new.items()};unit=1<<d
 errors_old={};errors_new={};H={};completed=[]
 for i in live:
  y=roles[i+112];ideal=[0]*400;ideal[roles[i]]=ideal[y]=unit//(2 if i in U else 1)
  eo=[x-y for x,y in zip(os[y],ideal)];en=[x-y for x,y in zip(ns[y],ideal)]
  errors_old[i]=eo;errors_new[i]=en;h={j:eo[roles[j]] for j in live if eo[roles[j]]};H[i]=h
  ro=[0]*400;rn=[0]*400
  for j,c in h.items():
   ro[roles[j]]+=c;rn[roles[j]]+=c
   if j in U:ro[roles[j+112]]-=c
   rn[yp]-=u.get(j,0)*c
  assert ro==eo and rn==en,(i,'forward residual H a')
  if not any(en):completed.append(i)
 counts=[sum(len(h) for h in H.values()),sum(sum(bool(v) for v in row) for row in errors_old.values()),sum(sum(bool(v) for v in row) for row in errors_new.values())]
 assert counts==[4569,4920,4573] and completed==[5,56,65,69,77,96,100,103]
 hosted=[];host_complete=[];coupled=[]
 for i,(b,y) in host.items():
  assert ns[roles[b]]==os[roles[b]] and ns[roles[y]]==os[roles[y]]
  assert ns[roles[y]]==[int(k==roles[y])*unit for k in range(400)]
  r=ns[roles[b]].copy();r[roles[b]]-=unit;r[roles[y]]+=unit;hosted.append(r)
  if not any(r):host_complete.append(i)
 for j in U:
  r=ns[roles[j]].copy();r[roles[j]]-=unit;r[roles[j+112]]+=unit;coupled.append(r)
 assert [rank(hosted),rank(coupled),rank(hosted+coupled)]==[58,7,65] and len(host_complete)==24
 K=[[int(i==j)-u.get(i,0)*int(j==17) for j in U] for i in U]
 for i,r in enumerate(coupled):assert r==[K[i][U.index(rev[k]-112)]*unit if rev[k]-112 in U else 0 for k in range(400)]
 roots={i:root9(s['frames'][s['initial'][i]][0]) for i in U};assert all(sum(v*v for v in r)==18 for r in roots.values())
 G=[[F(sum(x*y for x,y in zip(roots[i],roots[j])),18) for j in U] for i in U]
 C=[[F(pre[roles[i+112]][roles[j+112]],one) for j in U] for i in U]
 assert all(sum(G[i][j]*u.get(U[j],0) for j in range(8))==0 for i in range(8)) and rank(G)==rank(G+K)==7
 schur=[[K[i][j]-sum(G[i][k]*C[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
 joint=[[F(i==j) for j in range(8)]+C[i] for i in range(8)]+[G[i]+K[i] for i in range(8)]
 assert rank(schur)==7 and rank(joint)==15
 comparison=json.loads((a.bundle/'SCHUR-COMPARISON.json').read_text());v=comparison['variants']['dyadic_rank1']
 assert C==[[F(x) for x in r] for r in v['C']]
 assert K==[[F(x)+int(i==j) for j,x in enumerate(r)] for i,r in enumerate(v['R'])]
 assert comparison['full_canonical_cross_actions_constructed'] is False
 pairs={(e[2],e[3]) for e in w['program'] if e[0]=='MOVE'};oldpairs={(e[2],e[3]) for e in q['program'] if e[0]=='MOVE'};assert pairs<=oldpairs
 den=sorted({F(e[3] if e[0] in ('ADD','COPY') else e[2]).denominator for e in w['program'] if e[0] in ('ADD','COPY','SCALE')});assert den==[1,2,4,8,16]
 assert all(bill[k]==receipt['bill'][k] for k in ['instructions','counts','lifetimes','peak']) and {str(k):v for k,v in bill['moves'].items()}==receipt['bill']['moves']
 inc={k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in set(bill['counts'])|set(oldbill['counts'])};mi={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in set(bill['moves'])|set(oldbill['moves'])};mi={k:v for k,v in mi.items() if v}
 assert mi=={1:-4} and inc=={'ADD':-5,'CLEAR':-4,'INIT':-4,'MOVE':-4,'SCALE':7}
 controls=[]
 for name,ix,column,value in [('wrong_entry_sign',8,3,'-1'),('absent_half_scale',20,2,'1'),('absent_pivot_add',27,3,'0')]:
  bad=copy.deepcopy(w);bad['program'][ix][column]=value;br,bd,bl,bb,_=run(bad,spaces)
  assert any(not eqrow(br[i],bd,new[i],dn) for i in range(400));controls.append({'name':name,'event':ix,'rejected_by':'complete400 coefficient map'})
 # Literal block composition: no claimed independent2280 coefficient replay.
 p=2280;expected=[];blocks=[]
 def mapped(e,public,mapfield):
  z=e.copy();z[1]=mapfield(z[1]) if z[1]<public else p+z[1]-public
  if z[0] in ('ADD','COPY'):z[2]=mapfield(z[2]) if z[2]<public else p+z[2]-public
  return z
 for j in range(2):
  bank=lambda i:1480+400*j+i
  start=len(expected);expected += [['ADD',bank(i),rev[i],'-1',q['initial'][i]] for i in range(400)]
  expected += [mapped(e,400,bank) for e in w['program']];blocks.append({'copy':j+1,'start':start,'stop':len(expected)})
 start=len(expected);expected += [mapped(e,1480,lambda i:i) for e in s['program']];common=[start,len(expected)]
 for j in range(2):expected += [['ADD',1480+400*j+i,rev[i],'1',s['final'][rev[i]]] for i in range(400)]
 assert m3['program']==expected and m3['public']==2280 and m3['owned_fields']==max(s['owned_fields'],w['owned_fields'])
 assert m3['initial']==s['initial']+w['initial']*2 and m3['frames']==w['frames'] and m3['private_blocks']==blocks and m3['common_block']==common
 # Separate schedule-only replay checks all2280 physical charts and lifetimes.
 loc=dict(enumerate(m3['initial']));mc=collections.Counter();mm=collections.Counter();life=peak=0
 for e in expected:
  op,i=e[:2];mc[op]+=1;assert 0<=i<2280+m3['owned_fields']
  if op=='INIT':assert i>=2280 and i not in loc;loc[i]=e[2];life+=1
  elif op=='CLEAR':assert i>=2280 and loc[i]==e[2];del loc[i]
  elif op=='MOVE':
   aa,bb,owned=e[2:];assert loc[i]==aa and owned==(i>=2280) and (spaces[aa]<spaces[bb] or owned and spaces[bb]<spaces[aa]);mm[abs(len(m3['frames'][bb])-len(m3['frames'][aa]))]+=1;loc[i]=bb
  elif op in ('ADD','COPY'):assert loc[i]==loc[e[2]]==e[4]
  elif op=='SCALE':assert loc[i]==e[3] and F(e[2])
  else:raise AssertionError(op)
  peak=max(peak,len(loc)-2280)
 assert set(loc)==set(range(2280)) and all(loc[i]==s['final'][i] for i in range(1480))
 assert all(loc[1480+400*j+i]==ln[i] for j in range(2) for i in range(400))
 mbill={'instructions':len(expected),'counts':dict(mc),'moves':dict(sorted(mm.items())),'lifetimes':life,'peak':peak}
 assert all(mbill[k]==mr['ordinary_bill'][k] for k in ['instructions','counts','lifetimes','peak']) and {str(k):v for k,v in mm.items()}==mr['ordinary_bill']['moves']
 fb=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes();assert sha(fb)==PINS['caller'];full=json.loads(fb)
 T,P=[{int(k):v for k,v in full['invoice'][name].items()} for name in ['T','P']]
 raw=collections.Counter();Gh=collections.Counter();dims=list(map(len,s['frames']))
 for e in s['program']:
  if e[0]=='MOVE':(raw if e[1] in roles else Gh)[abs(dims[e[2]]-dims[e[3]])]+=1
 Hh=collections.Counter(dims[s['final'][i]]-dims[s['initial'][i]] for i in range(1480) if i not in roles)
 assert raw=={1:990,2:360,3:105,4:112,5:133,6:8,7:2}
 assert {str(k):v for k,v in (raw+Gh).items()}==full['native']['paid'] and {str(k):v for k,v in Hh.items()}==full['native']['helpers']
 rr=set(T)|set(P)|set(Gh)|set(Hh)|set(raw)|set(bill['moves'])
 tm={r:3*T.get(r,0)-36*Hh.get(r,0) for r in rr};pm={r:3*P.get(r,0)-36*Gh.get(r,0)+36*(bill['moves'].get(r,0)-raw.get(r,0)) for r in rr}
 for r in rr:assert pm[r]==3*(P.get(r,0)-18*(raw+Gh).get(r,0))+18*mm.get(r,0)
 assert all(tm.get(r,0)==int(mr['T'].get(str(r),0)) and pm.get(r,0)==int(mr['P'].get(str(r),0)) for r in rr)
 assert sum(tm.values())==31296 and sum(pm.values())==155772 and sum(r*(tm[r]-pm[r]) for r in rr)==4524
 grid=10**30;powers={}
 for r in rr:
  n=r**199*grid**200;v0=integer_root(n,200);powers[r]=(F(v0,grid),F(v0+int(v0**200!=n),grid))
 def bounds(profile):
  lo=hi=F(0)
  for r,c in profile.items():
   aa,bb=powers[r];lo+=c*(aa if c>=0 else bb);hi+=c*(bb if c>=0 else aa)
  return [lo,hi]
 margin=bounds({r:F(tm[r]-pm[r],36) for r in rr});assert margin[0]>0
 aa,bb=map(F,mr['per_rail_moment_bounds']);assert max(aa,margin[0])<=min(bb,margin[1])
 out={'status':'PASS_INDEPENDENT_DENSE400_DYADIC_AND_STRUCTURAL_M3_REVIEW','pins':PINS,'all400_input_coefficients_replayed':True,'full2280_coefficient_replay':False,'m3_literal_structure_and_all2280_chart_schedule_checked':True,'m3_symbolic_formula':'common=Wu; private_j=pi*Wu+L_new*(v_j-pi*u)','all400_native_exit_charts':True,'parent_bill':oldbill,'dyadic_bill':bill,'ordinary_increment':inc,'movement_increment':mi,'prefix_input_inverse':{'y':'2c-u*c17','x':'a+u*c17'},'forward_residual_counts':{'current_a':counts[0],'parent_original_inputs':counts[1],'new_original_inputs':counts[2]},'completed_firstY_ports':completed,'completed_hosted_reverse_ports':host_complete,'hosted_reverse_rank':58,'coupled_reverse_rank':7,'joint_reverse_rank':65,'completed_coupled_reverse_ports':[U[k] for k,row in enumerate(coupled) if not any(row)],'coupled_K':K,'coupled_Gram_rank':7,'coupled_K_in_Gram_rowspan':True,'conditional_canonical_cross_condensed_rank':7,'conditional_canonical_cross_joint_rank':15,'actual_canonical_cross_actions_or_Gram_acquisition_supplied':False,'new_chart_pairs':[],'dyadic_scalar_denominators':den,'negative_controls':controls,'m3_bill':mbill,'T_m3':tm,'P_m3':pm,'perrail_m3_margin_bounds':list(map(str,margin)),'perrail_m3_margin_decimal':float(margin[0]),'scope':'Changed partial original-input operator; hosted rank58 and coupled rank7 reverse debt, forward debt, complete endpoint, all-width physical compiler, both strict suppliers and five foundations remain. Shared premises are pinned native source/caller, admitted native endpoint and fixed-m composition, and our independently written local dense kernel-review engine.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','dyadic_bill','forward_residual_counts','hosted_reverse_rank','coupled_reverse_rank','joint_reverse_rank','m3_bill','perrail_m3_margin_decimal','negative_controls']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
