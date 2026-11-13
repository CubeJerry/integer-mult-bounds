import argparse,collections,gzip,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';FP='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def root(n):
 t=[i for i in range(9) if n>>i&1]
 if len(t)==3:return [2 if i in t else -1 for i in range(9)]
 z=[i for i in range(9) if i not in t];return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def brank(ns):
 b={}
 for x in ns:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)
def floorroot(n,k):
 x=1<<((n.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+n//x**(k-1))//k
  if y>=x:break
  x=y
 while (x+1)**k<=n:x+=1
 while x**k>n:x-=1
 assert x**k<=n<(x+1)**k;return x

def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();fb=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes();assert hashlib.sha256(sb).hexdigest()==SP and hashlib.sha256(fb).hexdigest()==FP;s=json.loads(gzip.decompress(sb));full=json.loads(fb)
 H=[s['live'][i] for i in s['hosted']['Dports']];normal={h:s['frames'][s['initial'][h]][0] for h in H};hn=[normal[h] for h in H]
 for h,y in zip(H,s['hosted']['Y2']):
  fr=s['frames'][s['final'][y]];assert len(fr)==8 and brank(fr)==8 and all(not((normal[h]&z).bit_count()%2) for z in fr) and s['frames'][s['initial'][y]]==[]
 eligible={z:sum(1<<i for i,n in enumerate(hn) if not((n&z).bit_count()%2)) for z in range(1,512)}
 h2=collections.Counter();w2=None
 for z in range(1,512):
  for t in range(z+1,512):
   if (z^t)<t:continue
   q=(eligible[z]&eligible[t]).bit_count();h2[q]+=1
   if w2 is None or q>w2[0]:w2=(q,[z,t])
 assert sum(h2.values())==43435 and max(h2)==35
 h3=collections.Counter();w3=None
 for piv in itertools.combinations(range(9),3):
  free=[(i,j) for i,p in enumerate(piv) for j in range(p+1,9) if j not in piv];rows=[1<<p for p in piv]
  for k in range(1<<len(free)):
   if k:
    i,j=free[(k&-k).bit_length()-1];rows[i]^=1<<j
   q=(eligible[rows[0]]&eligible[rows[1]]&eligible[rows[2]]).bit_count();h3[q]+=1
   if w3 is None or q>w3[0]:w3=(q,rows.copy())
 assert sum(h3.values())==788035 and max(h3)<=24
 caps={r:2**(r-1) for r in range(1,6)}|{6:24,7:35}
 tri=[(sum(caps[r] for r in rs),rs) for rs in itertools.combinations_with_replacement(range(1,8),3) if sum(rs)<=17];duo=[(sum(caps[r] for r in rs),rs) for rs in itertools.combinations_with_replacement(range(1,8),2) if sum(rs)<=8];assert max(x[0] for x in tri)==74 and max(x[0] for x in duo)==36
 print('chart_caps',sum(h2.values()),w2,sum(h3.values()),w3,flush=True)
 N=[n for n in range(512) if n.bit_count() in(3,7)];R={n:root(n) for n in N};seen=set();census=collections.Counter();candidates=[]
 for n,m in itertools.combinations(N,2):
  f=tuple(k for k in N if dot(R[k],R[n])==dot(R[k],R[m])==0)
  if f in seen:continue
  seen.add(f);kind='E6' if dot(R[n],R[m]) else'D6';groups=collections.defaultdict(list);zero=[]
  assert len(f)==(36 if kind=='E6' else 30)
  for h,k in zip(H,hn):
   x,y=dot(R[k],R[n]),dot(R[k],R[m])
   if not(x or y):zero.append(h);continue
   d=math.gcd(x,y);x//=d;y//=d
   if x<0 or x==0 and y<0:x=-x;y=-y
   groups[x,y].append(h)
  census[kind,len(groups)]+=1
  if len(groups)<=3:
   assert kind=='E6' and len(groups)==3;parts=[]
   for direction,roles in groups.items():
    ns=[normal[h] for h in roles];rk=brank(ns);assert rk==7
    C=[z for z in range(1,512) if all(not((z&n).bit_count()%2) for n in ns)];assert len(C)==3
    parts.append({'direction':list(direction),'source_roles':roles,'binary_rank':rk,'max_birth_nonzero_vectors':C})
   candidates.append({'A2_pair':[n,m],'zero_group':zero,'parts':parts})
 assert len(seen)==4900 and len(candidates)==6 and all(len(p['source_roles'])>=20 for c in candidates for p in c['parts'])
 assert dict(census)=={('E6',5):468,('E6',4):93,('D6',4):3780,('E6',6):553,('E6',3):6}
 best=max(candidates,key=lambda c:len(c['zero_group']));assert len(best['zero_group'])==30 and sum(len(p['source_roles']) for p in best['parts'])==66
 print('projection_census',dict(census),'best',best['A2_pair'],flush=True)
 # Exact fixed-m complete caller comparison, with8forward rank9+8entry rank1.
 T,P=[{int(k):v for k,v in full['invoice'][x].items()} for x in ['T','P']];Hh,Np=[{int(k):v for k,v in full['native'][x].items()} for x in ['helpers','paid']]
 grid=10**30;ranks=set(T)|set(P)|set(Hh)|set(Np)|set(range(1,10));power={}
 for r in ranks:
  q=r**199*grid**200;l=floorroot(q,200);power[r]=(F(l,grid),F(l+int(l**200!=q),grid))
 def bounds(profile):
  lo=hi=F(0)
  for r,c in profile.items():
   l,h=power[r];lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
  return lo,hi
 remaining={r:Np.get(r,0)-Hh.get(r,0)+F(T.get(r,0)-P.get(r,0),18)-400*int(r==8)-8*int(r==9)-8*int(r==1) for r in ranks}
 allowed=bounds(remaining);gap_profile={r:8*int(r==9)-remaining[r] for r in ranks};gap=bounds(gap_profile);assert gap[0]>0
 candidate={2:66,6:66,7:3,8:-66,9:6};candidate_cost=bounds(candidate);candidate_gap=bounds({r:candidate.get(r,0)-remaining[r] for r in ranks});assert candidate_gap[0]>0
 # For all six fibers, maximal dimension2 gives the cheapest one-chart path.
 for q in range(20,26):
  c0={9:1};c1={8:1-q,1:q,7:q};c2={7:1,2:q,6:q,8:-q}
  assert bounds({r:c0.get(r,0)-c2.get(r,0) for r in ranks})[0]>0 and bounds({r:c1.get(r,0)-c2.get(r,0) for r in ranks})[0]>0
 def qrank(rows):
  e={}
  for rr in rows:
   x=list(map(F,rr))
   for j in range(len(x)):
    if not x[j]:continue
    if j in e:
     c=x[j];x=[v-c*w for v,w in zip(x,e[j])]
    else:
     c=x[j];e[j]=[v/c for v in x];break
  return len(e)
 zero_basis=[]
 for h in best['zero_group']:
  if qrank([R[normal[j]] for j in zero_basis+[h]])>len(zero_basis):zero_basis.append(h)
  if len(zero_basis)==6:break
 assert len(zero_basis)==6
 packet_rows=[[F(dot(R[normal[h]],R[normal[j]]),18) for j in H] for h in zero_basis]
 for part in best['parts']:
  x,y=part['direction'];u,v=best['A2_pair'];rs=set(part['source_roles'])
  packet_rows.append([F(dot(R[normal[j]],R[u]),9*x) if j in rs and x else F(dot(R[normal[j]],R[v]),9*y) if j in rs else F(0) for j in H])
 assert qrank(packet_rows)==9 and qrank(packet_rows+[[R[normal[j]][k] for j in H] for k in range(9)])==9
 out={'status':'PASS_NINE_FRESH_NO_LINE_SOURCE_CAPS_AND_BUDGET','source_pin':SP,'complete_caller_pin':FP,'plane_count':43435,'plane_population_histogram':dict(sorted(h2.items())),'plane_max_witness':w2,'three_chart_count':788035,'three_chart_population_histogram':dict(sorted(h3.items())),'three_chart_max_witness':w3,'rank_caps':caps,'three_local_rank_sum17_max_support':74,'three_local_max_profile':max(tri),'two_local_rank_sum8_max_support':36,'two_local_max_profile':max(duo),'projection_fiber_census':{f'{k[0]}:{k[1]}':v for k,v in census.items()},'three_direction_candidates':candidates,'packet_only_lower_profile':{9:8},'limiting_return_allowance_bounds':list(map(str,allowed)),'limiting_gap_bounds':list(map(str,gap)),'best_A2_candidate':best,'best_A2_global_E6_basis_roles':zero_basis,'best_A2_packet_rows':[[str(v) for v in r] for r in packet_rows],'best_A2_packet_span_rank':9,'best_A2_target_contained':True,'best_A2_acquisition_profile':candidate,'best_A2_acquisition_bounds':list(map(str,candidate_cost)),'best_A2_limiting_gap_bounds':list(map(str,candidate_gap)),'scope':'All-V nine no-line fresh interface; universal proof needs separately audited zero-born quotient and E6/D6 completeness lemmas. Fixed8forward9+8entry1 caller only. Line births and additional informative moving fields excluded; no native or kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','limiting_return_allowance_bounds','limiting_gap_bounds','best_A2_acquisition_bounds','best_A2_limiting_gap_bounds']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
