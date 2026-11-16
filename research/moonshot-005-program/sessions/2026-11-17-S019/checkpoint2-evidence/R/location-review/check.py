from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,importlib.util,json
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--root-source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
spec=importlib.util.spec_from_file_location('own_previous_source',a.root_source);own=importlib.util.module_from_spec(spec);spec.loader.exec_module(own)
# Reuse only root's separately implemented chart/source arithmetic, never C's census or interpreter.
proof=own.source_check(a.repo,a.word);w=json.loads(a.word.read_text());R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];C={n:own.chart(x)for n,x in w['charts'].items()}
V={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};L={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
for op,n,*z in w['operations'][:w['carrier_interface_before_operation']]:
 if op=='INIT':V[n]=0;L[n]=z[0]
 elif op=='ADD':assert C[L[n]]==C[L[z[0]]];V[z[0]]^=V[n]
 elif op=='MOVE':L[n]=z[0]
 else:assert op=='CLEAR';del V[n],L[n]
U=sorted(set(range(111))-set(w['targets']));assert len(U)==63
for i in U:assert not any(x>>i&1 and own.subset(C[L[n]],C[f'F{i}'])for n,x in V.items())
def reduce(rows):
 piv={}
 for row in rows:
  v=list(map(F,row))
  for k,r in sorted(piv.items()):z=v[k];v=[x-z*y for x,y in zip(v,r)]
  k=next((j for j,x in enumerate(v)if x),None)
  if k is None:continue
  z=v[k];v=[x/z for x in v]
  for j,r in list(piv.items()):piv[j]=[x-r[k]*y for x,y in zip(r,v)]
  piv[k]=v
 return tuple(tuple(piv[k])for k in sorted(piv))
M=C['M1'];assert len(M)==5;points=sorted({reduce([[sum(F(x)*y for x,y in zip(R[i],b))for b in M]])[0]for i in U});assert len(points)==20 and len(reduce(points))==5
# Independent incremental flat lattice, instead of enumerating r-point subsets.
prev={()};counts={};hist={}
for dim in range(1,5):
 now={reduce(list(b)+[p])for b in prev for p in points};now={b for b in now if len(b)==dim};c=Counter()
 for b in now:
  piv=[next(j for j,x in enumerate(r)if x)for r in b];ann=[]
  for j in range(5):
   if j not in piv:
    z=[F(0)]*5;z[j]=1
    for k,r in zip(piv,b):z[k]=-r[j]
    ann.append(z)
  c[sum(all(sum(x*y for x,y in zip(p,z))==0 for z in ann)for p in points)]+=1
 counts[str(dim)]=len(now);hist[str(dim)]={str(k):v for k,v in sorted(c.items())};prev=now
claim=json.loads(a.author.read_text());assert counts==claim['flat_counts'] and hist==claim['flat_capacity_histograms']
def power(n):
 N=n**199<<(128*200);lo=0;hi=1<<((N.bit_length()+199)//200)
 while hi-lo>1:
  m=(lo+hi)//2
  if m**200<=N:lo=m
  else:hi=m
 return F(lo,1<<128),F(hi,1<<128)
p2,p3,p4=map(power,[2,3,4]);slope=((p3[0]-1)/6,(p3[1]-1)/6);assert 0<slope[0]<slope[1]<1 and p2[0]-1>2*slope[1] and 9+11*slope[0]>8+p4[1]
assert any(L[n]=='L5'and x==1<<5 for n,x in V.items()) and not own.subset(M,C['L5'])
result={'status':'PASS_INDEPENDENT_LOCATION_FLAT_LATTICE','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'all63_initial_own_coordinates_absent':True,'flat_counts':counts,'flat_histograms':hist,'capacity_maxima':{d:max(map(int,h))for d,h in hist.items()},'independent_root_intervals':{'rank2_slope':True,'all_small_rank_cost_strictly_above_8_plus_4t':True,'bits':128},'scope':'All later downward departures must contain initial M1. Downset first-arrival proof separately reviewed; actual native5-to-ground control lies outside premise. Static nine-message bound is inherited from separately reviewed exact entropy proof.'}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
