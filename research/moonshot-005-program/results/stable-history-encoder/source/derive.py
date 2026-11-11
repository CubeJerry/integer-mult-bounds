import argparse,gzip,json,collections,hashlib
from fractions import Fraction as F
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--donor',type=int,default=77);ap.add_argument('--receiver',type=int,default=189);ap.add_argument('--repository',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
R=args.repository;raw=(R/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('native source pin mismatch')
w=json.loads(gzip.decompress(raw));P=w['program'];X,Y=args.donor,args.receiver
if (X,Y)!=(77,189):raise ValueError('this bounded certificate is for pair77,189')

def sp(f):
 s={0}
 for x in f:s|={x^v for v in list(s)}
 return frozenset(s)
C=list(map(sp,w['frames']));hub=C[127];paths={j:[C[w['initial'][j]]] for j in (X,Y)}
for e in P:
 if e[0]=='MOVE' and e[1] in paths:paths[e[1]].append(C[e[3]])
source_charts=set(paths[X]);receiver_charts=set(paths[Y])
if source_charts&receiver_charts:raise ValueError('this implementation expects disjoint donor and receiver itineraries')
def axpy(a,b,c):
 a=a.copy()
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
 return a
rows={j:{j:F(1)} for j in range(w['public'])};locations=dict(enumerate(w['initial']));E={};observations=[];observation_rows=[];basis={};relations=[]
def insert(event,role,chart):
 if C[chart] not in receiver_charts:return
 ident=len(observations);observations.append({'after_event':event,'role':role,'chart':chart});observation_rows.append(rows[role].copy());a=rows[role].copy();co={ident:F(1)}
 while a:
  p=min(a)
  if p in basis:
   b,c=basis[p];z=-a[p];a=axpy(a,b,z);co=axpy(co,c,z)
  else:
   z=a[p];basis[p]=({j:v/z for j,v in a.items()},{j:v/z for j,v in co.items()});break
 else:relations.append(co)
for j,c in enumerate(w['initial']):insert(-1,j,c)
for k,e in enumerate(P):
 op,j=e[:2]
 if k==29098:E={i:rows[i].copy() for i,c in locations.items() if C[c]==C[71]}
 if op=='MOVE':locations[j]=e[3]
 elif op=='INIT':locations[j]=e[2]
 elif op=='CLEAR':locations.pop(j,None)
 if op=='INIT':rows[j]={}
 elif op=='CLEAR':rows.pop(j,None)
 elif op=='SCALE':rows[j]={i:F(e[2])*v for i,v in rows[j].items() if F(e[2])*v}
 elif op in ('ADD','COPY'):rows[j]=axpy(rows.get(j,{}) if op=='ADD' else {},rows[e[2]],F(e[3]))
 elif op=='MOVE':insert(k,j,e[3])
print('history',len(observations),'rank',len(basis),'relations',len(relations),flush=True)

def put(B,a,co):
 a=a.copy();co=co.copy()
 while a:
  p=min(a)
  if p in B:
   b,c=B[p];z=-a[p];a=axpy(a,b,z);co=axpy(co,c,z)
  else:
   z=a[p];B[p]=({j:v/z for j,v in a.items()},{j:v/z for j,v in co.items()});return

def reduce(B,a):
 a=a.copy();co={}
 for p,(b,c) in sorted(B.items()):
  if p in a:
   z=a[p];a=axpy(a,b,-z);co=axpy(co,c,z)
 return a,co

def show(a):return {str(j):str(v) for j,v in sorted(a.items())}
WT={};EB={};V={};initial=[];final=[]
for j,c in enumerate(w['initial']):
 if C[c]==C[w['initial'][Y]]:put(V,{j:F(1)},{('initial',j):F(1)});initial.append(j)
for j in range(w['public']):
 if C[w['final'][j]]==C[127]:put(WT,rows[j],{j:F(1)})
 if C[w['final'][j]] in receiver_charts:put(V,rows[j],{('final',j):F(1)});final.append(j)
for j,a in E.items():put(EB,a,{j:F(1)})
roles=sorted(E);qrows={};residuals={}
for i,j in enumerate(roles):
 residuals[j]={}
 for name,B in [('WT',WT),('F0',basis)]:
  a,_=reduce(B,E[j]);residuals[j][name]=a
  for p,v in a.items():qrows.setdefault((name,p),{})[i]=v
QB={}
for label,a in sorted(qrows.items()):put(QB,a,{label:F(1)})
free=[i for i in range(len(roles)) if i not in QB];DB={}
for f in free:
 v={f:F(1)}
 for p in sorted(QB,reverse=True):
  z=-sum(c*v.get(j,F(0)) for j,c in QB[p][0].items() if j!=p)
  if z:v[p]=z
 a={}
 for i,c in v.items():a=axpy(a,E[roles[i]],c)
 put(DB,a,{roles[i]:c for i,c in v.items()})
answers=[]
for _,(a,eco) in sorted(DB.items()):
 aw,wco=reduce(WT,a);af,fco=reduce(basis,a);av,vco=reduce(V,a)
 if aw or af or av:raise ValueError('bad intersection/stable basis')
 checks=[(eco,E),(wco,rows),(fco,dict(enumerate(observation_rows))),(vco,{('initial',j):{j:F(1)} for j in initial}|{('final',j):rows[j] for j in final})]
 for coeffs,source in checks:
  reconstructed={}
  for j,c in coeffs.items():reconstructed=axpy(reconstructed,source[j],c)
  if reconstructed!=a:raise ValueError('basis reconstruction mismatch')
 answers.append({'row':show(a),'E_coefficients':show(eco),'WT_endpoint_coefficients':show(wco),'F0_observation_coefficients':[dict(observations[i],coefficient=str(c)) for i,c in sorted(fco.items())],'initial_plus_receiver_final_coefficients':[{'kind':k,'role':j,'coefficient':str(c)} for (k,j),c in sorted(vco.items())] if not av else None})
result={'status':'EXACT_SOURCE_D_INTERSECTION','source_sha256':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','cut_before_event':29098,'source_instruction':P[29098],'donor':X,'receiver':Y,'chart':71,'cochart_roles':roles,'E_rows':{str(j):show(a) for j,a in E.items()},'E_rank':len(EB),'WT_rank':len(WT),'F0_count':len(observations),'F0_rank':len(basis),'initial_receiver_observations':len(initial),'receiver_final_roles':final,'initial_plus_receiver_final_rank':len(V),'combined_quotient_constraint_rank':len(QB),'cochart_coefficient_kernel_dimension':len(free),'D_dimension':len(DB),'D_basis':answers,'quotient_residuals':{str(j):{name:show(a) for name,a in rs.items()} for j,rs in residuals.items()},'scope':'One exact triple rowspace intersection; no positive encoding/control gain or new kappa.'}
expected=(roles,len(EB),len(WT),len(observations),len(basis),len(initial),final,len(V),len(QB),len(DB))
if expected!=([287,847,1050],3,1022,1065,1056,1046,[189,953],1047,2,1):raise ValueError('source census mismatch')
if answers[0]['row']!={'77':'1'}:raise ValueError('D basis mismatch')
if rows[77]!={77:F(1)} or rows[189]!={77:F(1),189:F(1)}:raise ValueError('simple terminal representation mismatch')
result['simple_stable_decoder']={'final_endpoint_189':'1','initial_input_189':'-1'}
result['negative_controls']={'remove_final_189':bool(reduce({p:v for p,v in V.items() if p!=77},{77:F(1)})[0]),'replace_basis_u77_by_u78':bool(reduce(EB,{78:F(1)})[0])}
if not all(result['negative_controls'].values()):raise ValueError('negative control unexpectedly accepted')
args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print({k:v for k,v in result.items() if k not in ('E_rows','D_basis','quotient_residuals')});print('D_basis',answers)
