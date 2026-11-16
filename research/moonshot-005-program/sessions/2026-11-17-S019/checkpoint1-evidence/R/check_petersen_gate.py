"""Source-bound nonlinear descent obstruction with exact Shannon certificate."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, permutations
from collections import defaultdict
import argparse,copy,hashlib,json
J=[5,35,90,93,96,97,109,110]
K4=[96,97,109,110]
EDGES={31:[96,97],32:[109,110],55:[96,110],56:[97,110],57:[96,109],58:[97,109]}
ISOLATES=[5,35,90,93]
EXPECTED_WORD='3643c6db33ce5ed1ea61724b126a8a3cad28be0c728376193b1f11fbf0457565'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def rref(rows):
 a=[[F(x)for x in r]for r in rows];rank=0;piv=[]
 for j in range(8):
  k=next((k for k in range(rank,len(a))if a[k][j]),None)
  if k is None:continue
  a[rank],a[k]=a[k],a[rank];v=a[rank][j];a[rank]=[x/v for x in a[rank]]
  for k in range(len(a)):
   if k!=rank:
    v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[rank])]
  piv.append(j);rank+=1
 return a[:rank],piv
def chart(c):
 a,piv=rref(c['rows'])
 if c['kind']=='span':return a
 need(c['kind']=='ann','chart kind');out=[]
 for j in range(8):
  if j in piv:continue
  v=[F(0)]*8;v[j]=F(1)
  for k,p in enumerate(piv):v[p]=-a[k][j]
  out.append(v)
 return out
def subset(a,b):return len(rref(a+b)[0])==len(b)
def verify_dual(d):
 pairs=list(combinations(range(5),2));need(d['pair_labels']==list(map(list,pairs)),'pair labels')
 idx={p:i for i,p in enumerate(pairs)}
 maps=[[idx[tuple(sorted((p[a],p[b])))]for a,b in pairs]for p in permutations(range(5))]
 def act(s,p):return sum(1<<p[i]for i in range(10)if s>>i&1)
 canon={s:min(act(s,p)for p in maps)for s in range(1024)}
 need(d['orbit_representatives']==sorted(set(canon.values())),'orbit catalogue')
 neigh=[sum(1<<j for j,q in enumerate(pairs)if not set(p)&set(q))for p in pairs]
 lhs=defaultdict(F);rhs=F(0)
 for rec in d['terms']:
  weight=F(rec['multiplier']);need(weight>0,'positive weight')
  kind,*z=rec['inequality']
  if kind=='initialize':need(not z,'initialize format');raw=[(1023,-1)];b=-10
  else:
   need(len(z)==(3 if kind=='submodularity'else 2),'shape');s,i,*jj=z
   need(0<=s<1024 and 0<=i<10 and not s>>i&1,'increment disjoint')
   u=s|1<<i
   if kind=='slope':raw=[(u,1),(s,-1)];b=1
   elif kind=='monotonicity':raw=[(s,1),(u,-1)];b=0
   elif kind=='decode':
    need(neigh[i]&s==neigh[i],'decoder has all neighbors');raw=[(u,1),(s,-1)];b=0
   elif kind=='submodularity':
    j=jj[0];need(0<=j<10 and j!=i and not s>>j&1,'second increment disjoint');raw=[(s,1),(u|1<<j,1),(u,-1),(s|1<<j,-1)];b=0
   else:raise ValueError('unknown inequality')
  coeff=defaultdict(int)
  for s,c in raw:coeff[canon[s]]+=c
  coeff={s:c for s,c in coeff.items()if c}
  need({str(s):c for s,c in coeff.items()}==rec['orbit_coefficients'],'orbit coefficient identity');need(b==rec['rhs'],'right hand side')
  for s,c in coeff.items():lhs[s]+=weight*c
  rhs+=weight*b
 need({s:c for s,c in lhs.items()if c}=={0:F(-1)},'exact telescope lhs');need(rhs==-5,'exact telescope bound')
 return {'inequalities':len(d['terms']),'automorphisms':len(maps),'subset_orbits':len(set(canon.values())),'exact_conclusion':'H(transcript) >= 5 log|alphabet| for the Petersen instance'}
def source_check(repo,word):
 raw=word.read_bytes();need(hashlib.sha256(raw).hexdigest()==EXPECTED_WORD,'word pin');w=json.loads(raw)
 src=(repo/w['source_path']).read_bytes();need(hashlib.sha256(src).hexdigest()==w['source_sha256'],'native source pin');R=json.loads(src)['native_roots'];dot=lambda i,j:sum(F(x)*F(y)for x,y in zip(R[i],R[j]))
 cb={n:chart(c)for n,c in w['charts'].items()};U=set(range(111))-set(w['targets']);S=sorted(set(J)|set(EDGES));need(set(S)<=U,'unfinished witness')
 for i in S:
  need(subset([R[i]],cb[f'L{i}'])and len(cb[f'L{i}'])==1,'native line');need(len(cb[f'F{i}'])==7 and all(sum(F(x)*F(y)for x,y in zip(R[i],v))==0 for v in cb[f'F{i}']),'actual target facet')
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 for op,n,*z in w['operations'][:w['carrier_interface_before_operation']]:
  if op=='INIT':vals[n]=0;loc[n]=z[0]
  elif op=='ADD':need(cb[loc[n]]==cb[loc[z[0]]],'prefix add co-location');vals[z[0]]^=vals[n]
  elif op=='MOVE':loc[n]=z[0]
  elif op=='CLEAR':del vals[n],loc[n]
  else:raise ValueError('prefix opcode')
 witnessmask=sum(1<<i for i in S);support={};memo={}
 def below(a,b):
  if (a,b)not in memo:memo[a,b]=subset(cb[a],cb[b])
  return memo[a,b]
 for i in S:
  vis=0
  for n,val in vals.items():
   if val&witnessmask and below(loc[n],f'F{i}'):vis|=val&witnessmask
  expected=sum(1<<j for j in S if dot(i,j)==0);need(vis==expected,'actual initial-chart side information');support[i]=[j for j in S if vis>>j&1]
 base={v:k for k,v in enumerate(K4)};labels={v:(4,base[v])for v in K4}
 for e,ends in EDGES.items():labels[e]=tuple(sorted(set(range(4))-{base[v]for v in ends}))
 need(len(set(tuple(sorted(x))for x in labels.values()))==10,'bijection with five-choose-two')
 for i in S:
  for j in S:
   actual=(j in support[i]);expected=(i in labels and j in labels and not set(labels[i])&set(labels[j]))
   need(actual==expected,'Petersen plus four isolates graph')
 suffix=w['operations'][w['carrier_interface_before_operation']:];originals={f'{p}{i}'for p in 'XY'for i in range(111)};moves=defaultdict(int)
 for op,n,*z in suffix:
  need(op=='CLEAR'or(op=='MOVE'and n in originals),'direct-close suffix')
  if op=='MOVE':moves[n]+=1
 need(max(moves.values())<=1,'one minimum closing move each')
 # Exact static upper bound: binary canonical fitting, authenticated native graph.
 fitting=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)]
 b={};selected=[]
 for i,row in enumerate(fitting):
  z=row;c=1<<i
  while z:
   k=z.bit_length()-1
   if k in b:r,cf=b[k];z^=r;c^=cf
   else:b[k]=(z,c);selected.append(i);break
 need(len(b)==9,'rank-nine static fitting upper bound')
 need(all(row>>i&1 for i,row in enumerate(fitting)),'identity diagonal')
 columns=sorted(b,reverse=True)
 minor=[sum(((fitting[i]>>j)&1)<<k for k,j in enumerate(columns))for i in selected]
 mb={}
 for z in minor:
  while z:
   k=z.bit_length()-1
   if k in mb:z^=mb[k]
   else:mb[k]=z;break
 need(len(mb)==9,'nonsingular minor for every characteristic-two extension')
 static={'canonical_fitting_rank':9,'row_basis_indices':selected,'nonsingular_minor_columns':columns,'scope':'Static public transcript and freely granted native raw neighbors; exact nonlinear optimum9 for finite characteristic-two fields and all positive record widths.'}
 return {'static_nonlinear_optimum':static,'word_sha256':EXPECTED_WORD,'native_source_sha256':w['source_sha256'],'cut':w['carrier_interface_before_operation'],'unfinished_witness':S,'isolated_roles':ISOLATES,'petersen_labels':{str(i):sorted(v)for i,v in labels.items()},'exact_initial_chart_neighbors':support,'direct_original_closure_suffix':True}
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--dual',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=json.loads(a.dual.read_text());dual=verify_dual(d);source=source_check(a.repo,a.word)
 controls=[]
 for kind in ['weight','decoding','orbit','bound']:
  bad=copy.deepcopy(d)
  if kind=='weight':bad['terms'][0]['multiplier']='-1'
  elif kind=='decoding':next(x for x in bad['terms']if x['inequality'][0]=='decode')['inequality'][1]=0
  elif kind=='orbit':bad['terms'][0]['orbit_coefficients']={'0':-1}
  else:bad['terms'][0]['rhs']=-11
  try:verify_dual(bad)
  except ValueError:controls.append(kind)
  else:raise ValueError('negative control accepted '+kind)
 out={'status':'PASS_EXACT_NONLINEAR_NINE_DESCENT_GATE','dual_sha256':hashlib.sha256(a.dual.read_bytes()).hexdigest(),'entropy_certificate':dual,'source':source,'negative_controls':controls,'scope':'Every fixed-schedule zero-error deterministic continuation with a finite whole-record alphabet and legal chart operations requires at least9 future whole-record descents after this exact source cut. Neither eight-descents nor any changed source is claimed sufficient. Current source price plus9 fails the necessary target allowance.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status']);print('21 exact entropy inequalities; Petersen plus4 isolates;9 nonlinear descents')
if __name__=='__main__':main()
