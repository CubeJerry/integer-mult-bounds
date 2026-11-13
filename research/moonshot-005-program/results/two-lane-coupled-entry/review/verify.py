"""Independent dense400 rational two-lane replay; no author engine imported."""
import argparse,collections,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dense_engine import run,span,eqrow
if not __debug__:raise SystemExit('Exact checks require Python without -O')
PINS={'native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','caller':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','manifest':'fa7fe7b08cdf5820b8c65e3112690f992a7cb30a62a752ed33129daf22980253','parent':'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','word':'e68cf993d0975c4e05bc366a4fefe9fea1b59e5ca0990c9c75f8c79ad62159d7','m3':'ec31ae8840c4191dc503abc736dd90f9c4369b2e1e32b5bab792beccbe1f292b'}
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
def inverse(A):
 n=len(A);B=[[F(x) for x in r]+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  p=next(i for i in range(j,n) if B[i][j]);B[j],B[p]=B[p],B[j];c=B[j][j];B[j]=[x/c for x in B[j]]
  for i in range(n):
   if i!=j:
    c=B[i][j];B[i]=[x-c*y for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B]
def matmul(A,B):return [[sum(a*B[k][j] for k,a in enumerate(r)) for j in range(len(B[0]))] for r in A]
def main(a):
 mb=(a.bundle/'MANIFEST.json').read_bytes();assert sha(mb)==PINS['manifest'];man=json.loads(mb)
 for e in man['files']:assert sha((a.bundle/e['path']).read_bytes())==e['sha256']
 s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',PINS['native']);q=load(a.bundle/'source-evidence/rail-consumer.json.gz',PINS['parent']);w=load(a.bundle/'output/rail-two-lane.json.gz',PINS['word']);m3=load(a.bundle/'m3/WORD.json.gz',PINS['m3'])
 receipt=json.loads((a.bundle/'output/RESULT.json').read_text());mr=json.loads((a.bundle/'m3/RESULT.json').read_text())
 roles={int(k):v for k,v in q['source_role_map'].items()};rev={v:k for k,v in roles.items()};assert sorted(rev)==list(range(400))
 assert all(w[k]==q[k] for k in ['initial','source_role_map','frames','owned_fields'])
 assert w['initial']==[s['initial'][rev[i]] for i in range(400)]
 spaces=list(map(span,w['frames']));live=s['live'];DP={live[k] for k in s['hosted']['Dports']};U=sorted(set(live)-DP);S=[17,19,38,40]
 assert U==[17,19,30,38,40,47,52,60] and tuple(F(s['hosted'][k]) for k in ['alpha','beta','alpha2','beta2'])==(F(-1),F(1,2),F(-1),F(0))
 roots={j:root9(s['frames'][s['initial'][j]][0]) for j in S};G=[[F(sum(x*y for x,y in zip(roots[i],roots[j])),18) for j in S] for i in S]
 C=inverse([[F(i==j)+G[i][j] for j in range(4)] for i in range(4)]);R=matmul([[G[i][j]-int(i==j) for j in range(4)] for i in range(4)],C)
 assert all(C[i][j]+R[i][j]/2==F(int(i==j),2) for i in range(4) for j in range(4))
 oldprefix=[];prefix=[]
 for j in U:
  L=s['initial'][j];b=[['INIT',400,3],['ADD',400,roles[j+112],'1',3],['MOVE',400,3,L,True],['ADD',roles[j],400,'-1',L],['CLEAR',400,L]];oldprefix.extend(b)
  if j not in S:prefix.extend(b)
 assert q['program'][:40]==oldprefix
 for i,j in enumerate(S):prefix.extend([['INIT',400+i,3],['ADD',400+i,roles[j+112],'1',3]])
 for i,j in enumerate(S):prefix += [['ADD',roles[j+112],400+i,'-1',3]]+[['ADD',roles[j+112],400+k,str(c),3] for k,c in enumerate(C[i]) if c]
 prefix += [['CLEAR',400+i,3] for i in range(4)];precode_end=len(prefix)
 def chart(V):return spaces.index(frozenset(V))
 EA=chart(span([s['frames'][s['initial'][j]][0] for j in [17,38]]));EB=chart(span([s['frames'][s['initial'][j]][0] for j in [19,40]]));line=chart(spaces[EA]&spaces[EB]);CA=chart(spaces[s['final'][129]]&spaces[s['final'][150]]);CB=chart(spaces[s['final'][131]]&spaces[s['final'][152]])
 assert spaces[line]=={0,51} and len(spaces[EA])==len(spaces[EB])==4 and len(spaces[CA])==len(spaces[CB])==128 and spaces[EB]<spaces[CA] and spaces[EA]<spaces[CB]
 prefix += [['ADD',roles[129],roles[150],'-1',3],['SCALE',roles[131],'-1',3],['ADD',roles[131],roles[152],'1',3]]
 xchart={17:EA,38:EA,19:EB,40:EB};replace={}
 for j in S:
  x=roles[j];k=next(k for k,e in enumerate(q['program']) if e[0]=='MOVE' and e[1]==x);e=q['program'][k]
  assert e[2]==s['initial'][j] and spaces[xchart[j]]<spaces[e[3]] and len(spaces[e[3]])==64
  assert not any(z[1]==x or z[0] in ('ADD','COPY') and z[2]==x for z in q['program'][40:k])
  prefix.append(['MOVE',x,e[2],xchart[j],False]);replace[k]=['MOVE',x,xchart[j],e[3],False]
 prefix += [['MOVE',roles[131],3,EA,False],['MOVE',roles[129],3,EB,False],['ADD',roles[17],roles[131],'-1/2',EA],['ADD',roles[38],roles[131],'1/2',EA],['ADD',roles[19],roles[129],'1/2',EB],['ADD',roles[40],roles[129],'-1/2',EB]]
 xs=[roles[j] for j in live];ys=[roles[j+112] for j in live];pos={j:k for k,j in enumerate(live)};packets=[];alpha=[];beta=[[F(0)]*8 for _ in live]
 for k,e in enumerate(q['program']):
  if e!=['INIT',451,127]:continue
  end=next(t for t in range(k+1,len(q['program'])) if q['program'][t]==['CLEAR',451,3]);mv=next(t for t in range(k+1,end) if q['program'][t][0]=='MOVE')
  assert q['program'][mv]==['MOVE',451,127,3,True];ar=[F(0)]*104
  for z in q['program'][k+1:mv]:assert z[0]=='ADD' and z[1]==451 and z[2] in xs and z[4]==127;ar[xs.index(z[2])]+=F(z[3])
  n=len(packets)
  for z in q['program'][mv+1:end]:assert z[0]=='ADD' and z[1] in ys and z[2]==451 and z[4]==3;beta[ys.index(z[1])][n]+=F(z[3])
  packets.append((k,end+1));alpha.append(ar)
 assert len(packets)==8 and all(packets[i][1]==packets[i+1][0] for i in range(7))
 r=[a-b for a,b in zip(beta[pos[17]],beta[pos[38]])];assert r==[a-b for a,b in zip(beta[pos[19]],beta[pos[40]])] and any(r)
 pivot=next(k for k,v in enumerate(r) if v);T=[r]+[[F(i==j) for j in range(8)] for i in range(8) if i!=pivot];Ti=inverse(T);packetT=copy.deepcopy(T);ap=matmul(T,alpha);bp=matmul(beta,Ti)
 assert matmul(bp,ap)==matmul(beta,alpha)
 assert [bp[pos[17]][k]-bp[pos[38]][k] for k in range(8)]==[F(1)]+[F(0)]*7
 assert [-bp[pos[19]][k]+bp[pos[40]][k] for k in range(8)]==[F(-1)]+[F(0)]*7
 np=[]
 for k in range(8):
  np += [['INIT',451,127]]+[['ADD',451,xs[j],str(c),127] for j,c in enumerate(ap[k]) if c]
  if k==0:np += [['MOVE',451,127,EA,True],['ADD',roles[131],451,'-1',EA],['MOVE',451,EA,line,True],['MOVE',451,line,EB,True],['ADD',roles[129],451,'1',EB],['MOVE',451,EB,3,True]]
  else:np.append(['MOVE',451,127,3,True])
  np += [['ADD',ys[j],451,str(bp[j][k]),3] for j in range(104) if live[j] not in [17,19] and bp[j][k]]+[['CLEAR',451,3]]
 late=[['MOVE',roles[129],EB,CA,False],['MOVE',roles[150],3,CA,False],['ADD',roles[129],roles[150],'1',CA],['MOVE',roles[129],CA,s['final'][129],False],['MOVE',roles[150],CA,s['final'][150],False],['MOVE',roles[131],EA,CB,False],['MOVE',roles[152],3,CB,False],['SCALE',roles[131],'-1',CB],['ADD',roles[131],roles[152],'1',CB],['MOVE',roles[131],CB,s['final'][131],False],['MOVE',roles[152],CB,s['final'][152],False]]
 drop=set()
 for j in S:
  y=roles[j+112];uses=[(k,z) for k,z in enumerate(q['program'][40:],40) if z[1]==y or z[0] in ('ADD','COPY') and z[2]==y]
  out=[(k,z) for k,z in uses if not any(a<=k<b for a,b in packets)];assert len(out)==1 and out[0][1]==['MOVE',y,3,s['final'][j+112],False];drop.add(out[0][0])
 expected=prefix.copy();k=40
 while k<len(q['program']):
  if k==packets[0][0]:expected+=np+late;k=packets[-1][1];continue
  if k not in drop:expected.append(replace.get(k,q['program'][k]))
  k+=1
 assert w['program']==expected and len(prefix)==65 and precode_end==52
 print('Independent dense rational replay of parent and two-lane400',flush=True)
 old,do,lo,oldbill,_=run(q,spaces);new,dn,ln,bill,sn=run(w,spaces,capture_before={52:('physical_c',ys),65:('postentry',xs)})
 assert ln==lo=={i:s['final'][rev[i]] for i in range(400)}
 old={i:[F(v,do) for v in row] for i,row in old.items()};new={i:[F(v,dn) for v in row] for i,row in new.items()}
 for i,row in old.items():
  target=row.copy()
  for j,h in enumerate(S):target[roles[h+112]]=sum(row[roles[t+112]]*C[k][j]+row[roles[t]]*(R[k][j]+C[k][j]) for k,t in enumerate(S))
  assert target==new[i],(i,'all400 parent substitution')
 dc,pc,lc=sn['physical_c'];da,pa,la=sn['postentry']
 for j in live:
  av=[F(int(k==roles[j])) for k in range(400)]
  if j in S:
   for k,h in enumerate(S):av[roles[h+112]]+=R[S.index(j)][k]
  elif j in U:av[roles[j+112]]-=1
  assert [F(v,da) for v in pa[roles[j]]]==av and new[roles[j]]==av
 for i,j in enumerate(S):
  cv=[sum(C[i][k]*int(t==roles[h+112]) for k,h in enumerate(S)) for t in range(400)]
  assert [F(v,dc) for v in pc[roles[j+112]]]==cv and lc[roles[j+112]]==3
  orig=[sum((int(i==k)+G[i][k])*F(pc[roles[h+112]][t],dc) for k,h in enumerate(S)) for t in range(400)]
  assert orig==[F(int(t==roles[j+112])) for t in range(400)]
 H={};errs={};complete=[]
 for i in live:
  ideal=[F(0)]*400;ideal[roles[i]]=ideal[roles[i+112]]=F(1,2) if i in U else F(1)
  eo=[x-y for x,y in zip(old[roles[i+112]],ideal)];en=[x-y for x,y in zip(new[roles[i+112]],ideal)];H[i]={j:eo[roles[j]] for j in live if eo[roles[j]]};errs[i]=en
  rebuilt=[sum(c*new[roles[j]][k] for j,c in H[i].items()) for k in range(400)];assert rebuilt==en
  if not any(en):complete.append(i)
 assert sum(map(len,H.values()))==4569 and sum(sum(bool(v) for v in r) for r in errs.values())==5020
 host={live[k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};hr=[];cr=[];hc=[]
 for i,(b,y) in host.items():
  assert new[roles[b]]==old[roles[b]] and new[roles[y]]==old[roles[y]] and new[roles[y]]==[F(int(k==roles[y])) for k in range(400)]
  r=new[roles[b]].copy();r[roles[b]]-=1;r[roles[y]]+=1;hr.append(r)
  if not any(r):hc.append(i)
 for j in U:
  r=new[roles[j]].copy();r[roles[j]]-=1;r[roles[j+112]]+=1;cr.append(r)
 assert [rank(hr),rank(cr),rank(hr+cr)]==[58,3,61] and len(hc)==24 and [j for j,r in zip(U,cr) if not any(r)]==[30,47,52,60]
 assert all(bill[k]==receipt['bill'][k] for k in ['instructions','counts','lifetimes','peak']) and {str(k):v for k,v in bill['moves'].items()}==receipt['bill']['moves']
 inc={k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in set(bill['counts'])|set(oldbill['counts'])};mi={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in set(bill['moves'])|set(oldbill['moves'])};mi={k:v for k,v in mi.items() if v}
 assert mi=={1:6,2:3,4:4,5:-2,7:3,8:-4,9:-1} and inc=={'ADD':-21,'CLEAR':0,'INIT':0,'MOVE':9,'SCALE':2}
 assert all(F(e[3]) for e in expected if e[0] in ('ADD','COPY'))
 den=sorted({F(e[3] if e[0] in ('ADD','COPY') else e[2]).denominator for e in expected if e[0] in ('ADD','COPY','SCALE')});assert den==[1,2,4,6,8,12,16]
 oldpairs={(e[2],e[3]) for e in q['program'] if e[0]=='MOVE'};pairs={(e[2],e[3]) for e in expected if e[0]=='MOVE'}-oldpairs;assert len(pairs)==20
 # Independently discovered geometry/pairs, shared frozen signed-Pauli checker.
 import importlib.util,sys
 vp=a.repo/'research/shared-wire-split-composition/frozen/native_verify.py';assert sha(vp.read_bytes())=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'
 spec=importlib.util.spec_from_file_location('bridge_two_lane_phase',vp);phase=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase;spec.loader.exec_module(phase)
 maps=json.loads((a.bundle/'CHART-MAPS.json').read_text());by_pair={(m['source'],m['target']):m for m in maps['maps']};assert set(by_pair)==pairs
 for aa,bb in pairs:
  m=by_pair[aa,bb];f,g=w['frames'][aa],w['frames'][bb];assert m['source_frame']==f and m['target_frame']==g and m['rank']==m['recipe']['rank']==abs(len(g)-len(f))
  phase.equal(phase.recipe(m['recipe']),phase.adjoint(phase.frame(f,9))+phase.frame(g,9),'independent two-lane chart map')
 bad=copy.deepcopy(next(iter(by_pair.values())));bad['recipe']['right']['phase']=(bad['recipe']['right']['phase']+1)%4
 try:phase.equal(phase.recipe(bad['recipe']),phase.adjoint(phase.frame(bad['source_frame'],9))+phase.frame(bad['target_frame'],9),'wrong phase')
 except ValueError:pass
 else:raise AssertionError('wrong global phase accepted')
 controls=[]
 tests=[('missing_physical_half',next(k for k,e in enumerate(expected) if e[:3]==['ADD',roles[17],roles[131]]),3,'-1'),('wrong_lane_sign',expected.index(['ADD',roles[131],451,'-1',EA]),3,'1'),('missing_late_inverse',expected.index(['SCALE',roles[131],'-1',CB]),2,'1')]
 for name,ix,col,val in tests:
  bad=copy.deepcopy(w);bad['program'][ix][col]=val;br,bd,bl,bb,_=run(bad,spaces);assert any([F(v,bd) for v in br[i]]!=new[i] for i in range(400));controls.append({'name':name,'event':ix,'rejected_by':'complete400 rational map'})
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
 assert sum(tm.values())==31296 and sum(pm.values())==156240 and sum(r*(tm[r]-pm[r]) for r in rr)==4452
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
 out={'status':'PASS_INDEPENDENT_DENSE_RATIONAL400_TWO_LANE_AND_STRUCTURAL_M3','pins':PINS,'all400_original_coefficients_replayed':True,'full2280_coefficient_replay':False,'all2280_chart_schedule_checked':True,'bill':bill,'parent_bill':oldbill,'ordinary_increment':inc,'move_increment':mi,'pair_charts':{'EA':EA,'EB':EB,'line':line,'CA':CA,'CB':CB},'physical_C':[[str(v) for v in r] for r in C],'entry_R':[[str(v) for v in r] for r in R],'packet_basis':[[str(v) for v in r] for r in packetT],'packet_basis_product_preserved':True,'new_chart_pairs':sorted(pairs),'all20_phase_recipes_pass':True,'wrong_phase_rejected':True,'scalar_denominators':den,'forward_current_a_terms':4569,'forward_original_terms':5020,'completed_firstY_ports':complete,'hosted_reverse_rank':58,'hosted_completed_ports':hc,'coupled_reverse_rank':3,'joint_reverse_rank':61,'completed_coupled_ports':[30,47,52,60],'negative_controls':controls,'m3_bill':mbill,'T_m3':tm,'P_m3':pm,'perrail_m3_margin_bounds':list(map(str,margin)),'perrail_m3_margin_decimal':float(margin[0]),'shared_phase_checker_sha256':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','m3_symbolic_formula':'common=Wu; private_j=pi*Wu+L_two_lane*(v_j-pi*u)','scope':'Changed partial rational400-input source; rank61 reverse debt,4569 forward coefficients, mixed cross actions and observations, full endpoint, compiler/precision, both strict suppliers and all five foundations remain. Native endpoint and fixed-m theorem shared; no author interpreter imported.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','bill','move_increment','all20_phase_recipes_pass','hosted_reverse_rank','coupled_reverse_rank','joint_reverse_rank','m3_bill','perrail_m3_margin_decimal','negative_controls']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
