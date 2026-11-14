#!/usr/bin/env python3
"""Independent integer rank/support and exact full-caller review of fixed preload."""
import argparse,gzip,hashlib,json,math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def qrank(rows):
 piv={}
 for row in rows:
  v=list(row)
  for j,b in sorted(piv.items()):
   if v[j]:
    x,y=v[j],b[j];v=[y*a-x*c for a,c in zip(v,b)];d=math.gcd(*v)
    if d>1:v=[x//d for x in v]
  j=next((j for j,x in enumerate(v)if x),None)
  if j is not None:piv[j]=v
 return len(piv)
def brank(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def main(a):
 need(sha(a.native)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin');n=json.loads(gzip.decompress(a.native.read_bytes()));P=n['live'];H=[P[i]for i in n['hosted']['Dports']];U=sorted(set(P)-set(H));need(U==[17,19,30,38,40,47,52,60],'coupled set')
 normal={i:n['frames'][n['initial'][i]][0]for i in P};R={}
 for i,v in normal.items():
  on=[j for j in range(9)if v>>j&1]
  if len(on)==3:r=[3*int(j in on)-1 for j in range(9)]
  else:
   off=sorted(set(range(9))-set(on));need(len(off)==2,'native normal type');r=[3*(int(j==off[0])-int(j==off[1]))for j in range(9)]
  need(sum(r)==0 and sum(x*x for x in r)==18,'root in rank8 real hyperplane');R[i]=r
 cov=[[sum(R[i][j]*R[i][k]for i in P)for k in range(9)]for j in range(9)]
 need(cov==[[234*int(j==k)-26 for k in range(9)]for j in range(9)],'9x9 covariance gives tight frame')
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
 need(all(dot(i,j)%9==0 for i in P for j in P),'integer doubled Gram')
 G2={i:{j:dot(i,j)//9 for j in P}for i in P};A2={i:{j:G2[i][j]-2*int(i==j)for j in P}for i in P}
 lam=[1,-1,0,-1,1,0,0,0];need(all(sum(lam[k]*R[u][j]for k,u in enumerate(U))==0 for j in range(9)),'coupled real relation');need(qrank([R[u]for u in U])==7,'coupled rank7')
 records=[];freedom=Counter();exception=[]
 for h in H:
  bad=[j for j in P if(normal[h]&normal[j]).bit_count()%2];M=[[A2[u][j]for u in U]for j in bad];rank=qrank(M);need(rank in [7,8],'constraint ranks7or8')
  need(all(A2[h][j]==0 for j in bad),'canonical facet support')
  if rank==7:
   need(all(sum(x*y for x,y in zip(row,lam))==0 for row in M),'one-dimensional kernel is known relation');exception.append(h)
  support=[j for j in H if A2[h][j]];selected=[];basis=[]
  for j in support:
   if brank(basis+[normal[j]])>len(basis):basis.append(normal[j]);selected.append(j)
  need(len(basis)==8 and all(not(normal[h]&v).bit_count()%2 for v in basis),'hosted support spans actual final facet')
  need(all(sum(lam[k]*A2[u][j]for k,u in enumerate(U))==0 for j in H),'affine changes vanish on hosted coordinates')
  freedom[8-rank]+=1;records.append({'hosted':h,'constraint_rank':rank,'hosted_support_size':len(support),'eight_actual_source_columns':selected,'eight_actual_normals':basis})
 need(freedom=={0:87,1:9}and exception==[7,18,27,46,77,81,87,103,111],'complete freedom census')
 # A permitted auxiliary descent defeats the discarded unrestricted induction.
 u=U[0];k=next(k for k in H if G2[u][k]);need(F(G2[u][k],24)!=0,'nonzero auxiliary preload')
 counter={'auxiliary_initial_role':u,'native_line_normal':normal[u],'permitted_move_ranks':[1,0],'nonzero_original_d_column':k,'coefficient':str(F(G2[u][k],24)),'initial_records_local_to_ground':0,'scope':'One-rank proper-chart import breaks the monotone support invariant; not a complete decoder.'}
 h=H[0];j=next(j for j in H if A2[h][j]);need(F(A2[h][j],2)*F(-11,12)!=0,'deleted hosted coefficient changes d_j')
 h0=next(z['hosted']for z in records if z['constraint_rank']==8);need(any(A2[U[0]][j]for j in P if(normal[h0]&normal[j]).bit_count()%2),'arbitrary constraint violates facet zeros')
 fh={x for x in range(512)if not(normal[H[0]]&x).bit_count()%2};fj={x for x in range(512)if not(normal[H[1]]&x).bit_count()%2};need(len(fh)==len(fj)==256 and fh-fj and fj-fh,'distinct facets incomparable')
 need(sha(a.full)=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','full caller pin');f=json.loads(a.full.read_text())
 def mix(*terms):
  p=Counter()
  for c,d in terms:
   for k,v in d.items():p[int(k)]+=c*F(v)
  return{k:v for k,v in p.items()if v}
 S=mix((F(1,18),f['invoice']['T']),(F(-1,18),f['invoice']['P']));Q=mix((1,S),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,{8:400}));grid=1<<176;cache={}
 def root(k):
  if k not in cache:
   z=k**199*grid**200;l,h=0,k*grid+1
   while h-l>1:
    m=(l+h)//2
    if m**200<=z:l=m
    else:h=m
   need(l**200<=z<h**200,'root enclosure');cache[k]=(F(l,grid),F(h,grid))
  return cache[k]
 def moment(p):
  lo=hi=F(0)
  for k,v in p.items():
   l,h=root(k);lo+=v*(l if v>0 else h);hi+=v*(h if v>0 else l)
  return lo,hi
 room=moment(Q);pen=moment(mix((-1,S)));need(room[1]<150 and room[0]>148 and pen[0]>0,'caller comparison and auxiliary threshold22')
 au=json.loads((a.author/'PRICE.json').read_text())
 for name,bounds in [('limiting_room_for_everything_else',room),('finite_m_penalty',pen)]:need(F(au[name][0])<=bounds[0]<=bounds[1]<=F(au[name][1]),'independent tighter interval')
 pins={name:sha(a.author/name)for name in ['PROOF.md','RESULT.json','PRICE.json','check.py','price.py']}
 out={'status':'PASS_INDEPENDENT_FIXED_PRELOAD_DECODER_AND_SCOPED_TOUR_REVIEW','native_sha256':sha(a.native),'caller_sha256':sha(a.full),'reviewed_pins':pins,'covariance_identity':'R^T R=234 I9-26 J9','full_Gram_identity':'G^2=13G','constraint_freedom_census':dict(freedom),'exceptional_hosted':exception,'records':records,'proper_chart_import_scope_control':counter,'negative_controls':['deleted_hosted_coefficient_changes_d_response','unrestricted_constraint_breaks_native_facet_support','distinct_facets_not_nested','permitted_auxiliary_descent_breaks_discarded_locality_claim'],'dyadic_grid':'2^-176','limiting_raw_only_room':list(map(str,room)),'finite_m_penalty':list(map(str,pen)),'terminal_tour_floor':176,'strict_tour_deficit':list(map(str,[176-room[1],176-room[0]])),'necessary_auxiliary_count_for_terminal_tours':22,'scope':'The96-visit impossibility needs all monotone carriers or the explicitly retained proper-chart locality invariant.176 applies only to terminal tours with that invariant. Fixed source algebra and arbitrary operator lift do not exclude proper-chart nonlocal imports or changed preload. Price comparison here is at t199/200.','new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'census':dict(freedom),'room':float(room[0]),'terminal_tour_deficit':float(176-room[1])}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in['native','full','author','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
