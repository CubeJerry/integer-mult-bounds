#!/usr/bin/env python3
"""Independent of the witness-search script; exact source/certificate checks."""
import argparse,copy,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,why):
 if not ok:raise ValueError(why)
def load_graph(raw):
 need(hashlib.sha256(raw).hexdigest()==PIN,'native byte pin')
 data=json.loads(gzip.decompress(raw));fs={int(k):v for k,v in data['frames'].items()}
 roots=[[Fraction(t) for t in fs[data['start'][i]]['B'][0]] for i in range(111)]
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 for i,r in enumerate(roots):
  need(fs[data['start'][i]]['dim']==1,'actual source line')
  f=fs[data['final'][111+i]];need(f['dim']==7,'actual target facet')
  need(all(dot(r,list(map(Fraction,z)))==0 for z in f['B']),'line/facet pairing')
 return [[int(i==j or dot(roots[i],roots[j])==0) for j in range(111)] for i in range(111)]
def verify_certificate(cert,K):
 need(cert['source_native_sha256']==PIN,'certificate source')
 covered=set();details=[]
 for number,cfg in enumerate(cert['configurations']):
  frame=cfg['frame'];skip=cfg['omitted_index']
  need(len(frame)==8 and len(set(frame))==8 and all(i in range(111) for i in frame),'eight distinct source roles')
  need(skip in range(8),'omitted coordinate')
  need(all(K[i][j]==int(i==j) for i in frame for j in frame),'actual independent frame')
  signatures={}
  for j in range(111):
   if j in frame:continue
   ss=tuple(a for a,i in enumerate(frame) if K[i][j])
   if len(ss)==2:signatures.setdefault(ss,[]).append(j)
  subset=[a for a in range(8) if a!=skip];edge_roles={}
  for ends in itertools.combinations(subset,2):
   need(len(signatures.get(ends,[]))==1,'unique actual two-point edge role')
   edge_roles[ends]=signatures[ends][0]
  need(len(set(edge_roles.values()))==21,'21 distinct edge roles')
  for e,f in itertools.combinations(edge_roles,2):
   if set(e)&set(f):need(K[edge_roles[e]][edge_roles[f]]==0,'shared-endpoint noncontact')
  pairs={tuple(sorted((frame[a],j))) for e,j in edge_roles.items() for a in e}
  need(len(pairs)==42,'42 point-edge contacts')
  need(all(K[i][j] for i,j in pairs),'actual permitted contact')
  covered|=pairs;details.append({'number':number,'contacts':len(pairs)})
 counts=Counter(i for e in covered for i in e)
 support=[counts[i] for i in range(111)];arrival=sum(int(n>36)+int(n>52) for n in support)
 need(len(covered)==cert['unordered_contacts'],'declared contact coverage')
 need(support==cert['row_guaranteed_supports'],'declared row supports')
 need(arrival==cert['arrival_lower_bound'],'declared arrival bound')
 need(len(covered)==3019 and min(support)==41 and sum(n>52 for n in support)==86 and arrival==197,'stated source consequence')
 masks=[sum(1<<j for j in range(111) if tuple(sorted((i,j))) in covered) for i in range(111)]
 return {'configurations':len(details),'unordered_contacts':len(covered),'row_supports':support,'coverage_masks':masks,'rows_above_36':sum(n>36 for n in support),'rows_above_52':sum(n>52 for n in support),'arrival_bound':arrival}
def linear_certificate():
 edges=list(itertools.combinations(range(7),2));keys=[(e,a) for e in edges for a in e];at={z:i for i,z in enumerate(keys)};h=len(keys);N=h+1
 def plus(u,v,m=1):return [a+m*b for a,b in zip(u,v)]
 def G(a):
  v=[0]*N
  for e in edges:
   if a in e:v[at[e,a]]+=1
  return v
 def g(e,a):
  v=[0]*N;v[at[e,a]]=1;return v
 def LR(e,a):
  v=[0]*N;v[h]=1
  for b in e:v[at[e,b]]+=2
  return plus(v,G(a),-1)
 W=list(range(2,7));ab=(0,1);x=g(ab,0)
 internal=[0]*N
 for c in W:
  for d in W:
   if c!=d:internal=plus(internal,LR(tuple(sorted((c,d))),c))
 local=[0]*N
 for c in W:local=plus(local,LR((0,c),0))
 qb=[0]*N
 for c in W:qb=plus(qb,g((1,c),c))
 total=plus(internal,local,2);total=plus(total,plus(G(0),x,-1),6);total=plus(total,qb,4)
 expected=[0]*N;expected[h]=30;expected[at[ab,0]]=-10
 need(total==expected,'exact nonnegative LR certificate for 3h-x')
 # Exact abstract LR-feasible witness establishes that this inequality set
 # alone does not yield coefficient two. No fitting realization is claimed.
 values=[0]*N;values[h]=1;values[at[ab,0]]=3
 for c in W:values[at[(0,c),c]]=1
 residuals=[sum(a*b for a,b in zip(LR(e,a),values)) for e in edges for a in e]
 need(min(residuals)>=0,'abstract LR witness satisfies every inequality')
 need(values[at[ab,0]]>2*values[h],'coefficient-two mutation rejected')
 need(sum(a*b for a,b in zip(total,values))==0,'coefficient three attained in LR relaxation')
 return {'endpoint_variables':42,'inequalities_checked':42,'internal_oriented_inequalities':20,'point_inequalities_weight_two':5,'identity':'sum_internal_LR+2sum_point_LR+6(G_a-x)+4Q_b=30h-10x','relaxation_control_only':True}
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path);p.add_argument('--native',type=Path);p.add_argument('--certificate',type=Path,default=Path(__file__).with_name('CERTIFICATE.json'));p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 native=a.native or a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz';raw=native.read_bytes();K=load_graph(raw);cert=json.loads(a.certificate.read_text());source=verify_certificate(cert,K);linear=linear_certificate();controls=[]
 bad=copy.deepcopy(cert);bad['configurations'][0]['frame'][0]=bad['configurations'][0]['frame'][1]
 try:verify_certificate(bad,K)
 except ValueError:controls.append('duplicate frame role rejected')
 else:raise ValueError('duplicate frame role accepted')
 bad=copy.deepcopy(cert);bad['configurations'].pop()
 try:verify_certificate(bad,K)
 except ValueError:controls.append('missing coverage witness rejected')
 else:raise ValueError('missing witness unexpectedly retains complete stated coverage')
 bad=copy.deepcopy(cert);bad['arrival_lower_bound']+=1
 try:verify_certificate(bad,K)
 except ValueError:controls.append('overstated arrival bound rejected')
 else:raise ValueError('overstated arrival count accepted')
 try:load_graph(raw+b' ')
 except ValueError:controls.append('source-byte mutation rejected')
 else:raise ValueError('source mutation accepted')
 out={'status':'PASS_BIT_UNIFORM_BLOCK_RANK_GAP_FINITE_PREMISES','native_sha256':PIN,'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'source_witnesses':source,'general_inequality_certificate':linear,'negative_controls':controls,'universal_claim':'Written proof: sum ell<=196 implies rank>=ceil(28V/3), characteristic two, every V.','new_complete_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'configurations':source['configurations'],'contacts':source['unordered_contacts'],'arrival_lower_bound':source['arrival_bound'],'controls':len(controls)+1}))
if __name__=='__main__':main()
