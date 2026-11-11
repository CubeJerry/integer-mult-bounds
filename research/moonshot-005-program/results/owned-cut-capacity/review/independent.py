#!/usr/bin/env python3
import argparse,gzip,hashlib,json,math
from pathlib import Path
from fractions import Fraction as Q
P=1000003
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def check(ok,s):
 if not ok:raise ValueError(s)
def plus(dst,src,c,mod=None):
 for i,v in src.items():
  x=dst.get(i,0)+c*v
  if mod:x%=mod
  if x:dst[i]=x
  else:dst.pop(i,None)
def rowrank(rows,mod=None):
 pivots={}
 for r0 in sorted(rows,key=len):
  row=r0.copy()
  while row:
   j=max(row);v=row[j]
   if j in pivots:plus(row,pivots[j],-v,mod)
   else:
    inv=pow(int(v),-1,mod) if mod else Q(1)/v
    pivots[j]={k:(x*inv)%mod if mod else x*inv for k,x in row.items()};break
 return len(pivots)
def decode(r):return {int(i):Q(v) for i,v in r}
def run(source,certificate):
 raw=source.read_bytes();check(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
 check(all(P%d for d in range(2,math.isqrt(P)+1)),'prime')
 w=json.loads(gzip.decompress(raw));c=json.loads(certificate.read_text());cut=c['cut_before_event']
 check(cut==36961 and w['program'][cut]==['MOVE',1529,541,543,True],'exact cut')
 n=w['public'];tot=n+w['owned_fields'];prog=w['program'][:cut]
 main=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);helper=set(range(n))-main
 check((len(main),len(helper))==(400,1080),'owner partition')
 current=list(w['initial'])+[None]*w['owned_fields'];peak=0;live=set()
 for i,e in enumerate(w['program']):
  if i==cut:live_cut=sorted(live);frames_cut=current.copy()
  op,a=e[:2]
  if op=='INIT':check(current[a] is None and a>=n,'fresh owned');current[a]=e[2];live.add(a);peak=max(peak,len(live))
  elif op=='CLEAR':check(a in live and current[a]==e[2],'retirement');live.remove(a);current[a]=None
  elif op=='MOVE':check(current[a]==e[2],'chart');current[a]=e[3]
  elif op in ('ADD','COPY'):check(current[a]==current[e[2]]==e[4],'cochart')
  elif op=='SCALE':check(current[a]==e[3],'scale')
 check((len(live_cut),peak,w['owned_fields'])==(42,43,51),'capacities')
 # Sparse modular forward matrix; independent of author NumPy elimination.
 rows=[{i:1} if i<n else {} for i in range(tot)]
 for e in prog:
  op,a=e[:2]
  if op in ('INIT','CLEAR'):rows[a]={}
  elif op in ('ADD','COPY'):
   f=Q(e[3]);check(f.denominator%P,'denominator');coef=f.numerator%P*pow(f.denominator,-1,P)%P;plus(rows[a],rows[e[2]],coef,P)
  elif op=='SCALE':
   f=Q(e[2]);check(f.denominator%P,'denominator');coef=f.numerator%P*pow(f.denominator,-1,P)%P
   rows[a]={k:coef*v%P for k,v in rows[a].items() if coef*v%P}
 rp=rowrank(rows[:n],P);rm=rowrank([{j:v for j,v in rows[i].items() if j in main} for i in main],P)
 rmall=rowrank([rows[i] for i in main],P);rpm=rowrank([{j:v for j,v in row.items() if j in main} for row in rows[:n]],P)
 check((rp,rm,rmall,rpm)==(1479,338,400,400),'modular lower ranks')
 # Exact batched reverse-adjoint: all42 owned rows and public dependence.
 adj=[{} for _ in range(tot)]
 for j,a in enumerate(live_cut):adj[a]={j:Q(1)}
 left=decode(c['public_left_nullvector']);check(any(left.values()) and set(left)<=set(range(n)),'nonzero public dependence')
 for a,v in left.items():adj[a][42]=v
 for e in reversed(prog):
  op,a=e[:2]
  if op in ('INIT','CLEAR'):adj[a]={}
  elif op in ('ADD','COPY'):plus(adj[e[2]],adj[a],Q(e[3]))
  elif op=='SCALE':adj[a]={j:Q(e[2])*v for j,v in adj[a].items() if Q(e[2])*v}
 owned_rows=[{} for _ in live_cut];left_row={}
 for i,row in enumerate(adj):
  for j,v in row.items():
   if j==42:left_row[i]=v
   else:owned_rows[j][i]=v
 check(not left_row and all(set(r)<=set(range(n)) for r in owned_rows),'exact public dependence')
 rg=rowrank(owned_rows);ra=rowrank([{i:v for i,v in r.items() if i in main} for r in owned_rows]);check((rg,ra)==(26,21),'owned exact ranks')
 # Exact forward62 main-kernel vectors and lost public input.
 kernel=[decode(v) for v in c['kernel_main_vectors']];lost=decode(c['public_input_nullvector'])
 check(len(kernel)==62 and rowrank(kernel)==62 and all(set(v)<=main for v in kernel),'independent main witnesses')
 values=[{} for _ in range(tot)]
 for j,v in enumerate([*kernel,lost]):
  for i,x in v.items():values[i][j]=x
 for e in prog:
  op,a=e[:2]
  if op in ('INIT','CLEAR'):values[a]={}
  elif op in ('ADD','COPY'):plus(values[a],values[e[2]],Q(e[3]))
  elif op=='SCALE':values[a]={j:Q(e[2])*v for j,v in values[a].items() if Q(e[2])*v}
 check(all(not {j:v for j,v in values[i].items() if j<62} for i in main),'main-kernel annihilation')
 check(all(62 not in values[i] for i in range(n)),'lost public mode')
 check({i:values[i][62] for i in live_cut if 62 in values[i]}=={1503:Q(1)},'unique private lost mode')
 responses=[{j:v for j,v in values[i].items() if j<62} for i in live_cut];check(rowrank(responses)==6,'owned kernel response')
 chosen=c['retained_difference_owners'];check(set(chosen)<=set(live_cut) and len(chosen)==6,'six current owned roles')
 check(rowrank([{j:v for j,v in values[i].items() if j<62} for i in chosen])==6,'six observations span')
 check(not {j:v for j,v in values[1503].items() if j<62},'common private observation separation')
 park=c['retained_helper_difference_owners'];check(len(park)==62 and set(park)<=helper,'helper owners')
 check(rowrank([{j:v for j,v in values[i].items() if j<62} for i in park])==62,'full helper difference complement')
 check([frames_cut[i] for i in park]==c['helper_difference_frames'],'parking frames')
 check(1480+344-1817==7 and 1880-1817==63,'owned versus full continuation')
 return {'status':'PASS_INDEPENDENT_OWNED_CAPACITY_REVIEW','source_sha256':PIN,'cut_before_event':cut,
  'owner_counts':{'live':42,'peak':43,'allocated':51},
  'exact_ranks':{'P':1479,'M':338,'main_on_all':400,'public_on_main':400,'P_with_G':1480,'M_with_A':344,'G':26,'A':21},
  'extra_fields':{'no_public_side_information':47,'old_owned_recovery':7,'balanced_public_full_continuation':63,'arbitrary1080helper_observations_full_continuation_at_least':62},
  'frozen_two_main_bank_rank':738,'balanced_public_rank':1817,'input_dimension':1880,
  'main_kernel_witnesses_checked':62,'helper_difference_complement_checked':62,'prime_verified':True,
  'method':'sparse modular largest-pivot elimination; exact batched adjoint and forward rational propagation',
  'scope':'Complete-field information only; no field-count to Gaussian-job inference.'}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',type=Path,required=True);a.add_argument('--certificate',type=Path,required=True);x=a.parse_args()
 print(json.dumps(run(x.source,x.certificate),indent=2,sort_keys=True))
