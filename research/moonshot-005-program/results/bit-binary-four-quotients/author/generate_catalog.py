from pathlib import Path
import gzip,json,itertools,hashlib,time,collections
from fractions import Fraction as F
import numpy as np
import argparse
if not __debug__:raise SystemExit("Assertions required; no python -O")
p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--output",type=Path,required=True);args=p.parse_args()
blob=(args.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(blob).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78';s=json.loads(gzip.decompress(blob));roots=[]
for i in range(111):
 v=[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]];n=sum(x*x for x in v);v=[x*(2 if n==1 else 1) for x in v];assert all(x.denominator==1 for x in v);v=list(map(int,v));assert sum(x*x for x in v)==4;roots.append(v)
R=np.array(roots,dtype=np.int64);D=R@R.T;A=D//2;deg=(D==0).sum(axis=1);full=(1<<111)-1
T=[sum(1<<j for j in range(111) if j==i or D[i,j]==0) for i in range(111)];O=[t^(1<<i) for i,t in enumerate(T)];low={s:sum(1<<i for i in range(111) if deg[i]<=52+s) for s in range(1,9)}
flats={};trips=np.array(list(itertools.combinations(range(111),3)));high={};st=time.time();calls=0
for start in range(0,len(trips),2048):
 ids=trips[start:start+2048];x=A[ids[:,0],ids[:,1]];y=A[ids[:,0],ids[:,2]];z=A[ids[:,1],ids[:,2]];det=8-2*(x*x+y*y+z*z)+2*x*y*z;ok=det>0;ids=ids[ok];x=x[ok];y=y[ok];z=z[ok];det=det[ok]
 d0=A[ids[:,0]];d1=A[ids[:,1]];d2=A[ids[:,2]];val=(4-z*z)[:,None]*d0*d0+(4-y*y)[:,None]*d1*d1+(4-x*x)[:,None]*d2*d2+2*(y*z-2*x)[:,None]*d0*d1+2*(x*z-2*y)[:,None]*d0*d2+2*(x*y-2*z)[:,None]*d1*d2
 for ids0,m in zip(ids,val==2*det[:,None]):
  key=np.packbits(m).tobytes()
  if key not in flats:flats[key]=tuple(map(int,ids0))
def add(v):
 global calls
 calls+=1;s=len(v);mask=0;m=full
 for i in v:mask|=1<<i;m&=T[i]
 j=m&mask;u=m^j;gain=2*j.bit_count()+(u&low[s]).bit_count()
 if gain>=13:high[mask]={'support':list(v),'gain':gain,'two_saving_rows':[i for i in range(111) if j>>i&1],'one_saving_rows':[i for i in range(111) if (u&low[s])>>i&1]}
# All relevant rank3 supports and isolated-root extensions of rank3 supports.
for key,ids in flats.items():
 V=np.flatnonzero(np.unpackbits(np.frombuffer(key,dtype=np.uint8))[:111]).tolist()
 if len(V)<4:continue
 outside=O[ids[0]]&O[ids[1]]&O[ids[2]];Js=[i for i in range(111) if outside>>i&1]
 for w in range(4,len(V)+1):
  for sub in itertools.combinations(V,w):
   add(sub)
   for j in Js:add((*sub,j))
print('after flats',len(high),'calls',calls,'sec',time.time()-st,flush=True)
# Every four-root support with an isolated root (over-includes harmless rank3 cases).
for j in range(111):
 vv=[i for i in range(111) if O[j]>>i&1]
 for sub in itertools.combinations(vv,3):add((*sub,j))
print('after isolated quads',len(high),'calls',calls,'sec',time.time()-st,flush=True)
# All actual orthogonal cliques of sizes5..8.
clique_counts=collections.Counter()
def walk(prefix,cand):
 while cand:
  b=cand&-cand;i=b.bit_length()-1;cand^=b;new=prefix+(i,);clique_counts[len(new)]+=1
  if len(new)>=5:add(new)
  if len(new)<8:walk(new,cand&O[i])
walk((),full)
rows=sorted(high.items());hist=collections.Counter(r['gain'] for _,r in rows)
lines=[];S=set(high)
S14={m for m,r in high.items() if r["gain"]>=14}
for a,b in itertools.combinations(sorted(S14),2):
 c=a^b
 if c in S:lines.append([hex(a),hex(b),hex(c),high[c]['gain']])
out={'status':'EXPLORATORY_BINARY_HIGH_GAIN_COSET_CATALOG','source_sha256':hashlib.sha256(blob).hexdigest(),'minimum_gain':13,'catalog_size':len(high),'gain_histogram':dict(sorted(hist.items())),'clique_counts':dict(sorted(clique_counts.items())),'candidate_calls':calls,'binary_additive_lines':lines,'rows':[{'mask':hex(m),**r} for m,r in rows]}
assert len(high)==38324 and dict(hist)=={13:20290,14:9988,15:6912,16:1122,17:12}
assert not lines and calls==6329841
assert [clique_counts[k] for k in range(1,9)]==[111,3235,29939,90079,77003,35667,9443,1094]
out['status']='PASS_EXHAUSTIVE_BINARY_HIGH_GAIN_COSET_CATALOG'
args.output.mkdir(parents=True,exist_ok=True)
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode();gz=gzip.compress(raw,mtime=0)
(args.output/'CATALOG.json.gz').write_bytes(gz)
# The exact17 row sets cannot be assigned to two distinct directions at once.
seventeen=[set(r['one_saving_rows']) for r in high.values() if r['gain']==17]
assert len(seventeen)==12 and all(len(x)==17 for x in seventeen)
inter=collections.Counter(len(a&b) for a,b in itertools.combinations(seventeen,2))
assert dict(inter)=={8:30,11:19,6:8,5:8,9:1}
# Elementary Fano-plane control, covering all subsets of its seven nonzero points.
fano_caps=[]
for k in range(8):
 for sub in itertools.combinations(range(1,8),k):
  ss=set(sub)
  if any(a^b in ss for a,b in itertools.combinations(sub,2)):continue
  assert k<=4
  if k==4:
   assert sub[0]^sub[1]^sub[2]^sub[3]==0;fano_caps.append(sub)
assert len(fano_caps)==7
highrows=[(m,r) for m,r in rows if r['gain']>=14]
with (args.output/'high-input.txt').open('w') as f:
 f.write(str(len(highrows))+'\n')
 for m,r in highrows:
  one=sum(1<<i for i in r['one_saving_rows']);two=sum(1<<i for i in r['two_saving_rows']);assert not one&two and one.bit_count()+2*two.bit_count()==r['gain']
  f.write(' '.join(map(str,[m>>64,m&((1<<64)-1),one>>64,one&((1<<64)-1),two>>64,two&((1<<64)-1),r['gain']]))+'\n')
summary={'status':'PASS_EXACT_BINARY_CATALOG_PAIR_RELATIONS_AND_FANO_FACT','source_sha256':hashlib.sha256(blob).hexdigest(),'catalog_gzip_sha256':hashlib.sha256(gz).hexdigest(),'catalog_payload_sha256':hashlib.sha256(raw).hexdigest(),'catalog_size':len(high),'gain_histogram':dict(sorted(hist.items())),'high_size':len(highrows),'all_high_pair_sums_gain_at_most12':True,'seventeen_row_set_intersection_histogram':dict(sorted(inter.items())),'at_most_one_direction_can_attain17':True,'candidate_calls':calls,'fano_four_caps':fano_caps,'high_input_sha256':hashlib.sha256((args.output/'high-input.txt').read_bytes()).hexdigest(),'independent_review_complete':False}
(args.output/'CATALOG-RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2));print('seconds',time.time()-st)
