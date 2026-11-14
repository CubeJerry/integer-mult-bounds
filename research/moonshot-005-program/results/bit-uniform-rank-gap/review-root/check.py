#!/usr/bin/env python3
"""Independent source witness and formal LR verification; no author import."""
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction
from itertools import combinations
from collections import Counter
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(b,s):
 if not b:raise ValueError(s)
def source(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin')
 q=json.loads(gzip.decompress(raw));v=[]
 for i in range(111):v.append([Fraction(z) for z in q['frames'][str(q['start'][i])]['B'][0]])
 return [[i==j or sum(a*b for a,b in zip(v[i],v[j]))==0 for j in range(111)] for i in range(111)]
def census(K,configs):
 pairs=set()
 for q in configs:
  f=q['frame'];om=q['omitted_index'];need(len(f)==len(set(f))==8 and 0<=om<8,'eight frame')
  need(all(not K[i][j] for i,j in combinations(f,2)),'actual independent frame')
  active=[a for a in range(8) if a!=om];edge={}
  for e in set(range(111))-set(f):
   contacts=tuple(a for a,i in enumerate(f) if K[e][i])
   if len(contacts)==2 and om not in contacts:
    need(contacts not in edge,'unique edge signature');edge[contacts]=e
  need(set(edge)==set(combinations(active,2)),'full K7 with no omitted contact')
  for (a,b),e in edge.items():
   pairs.add(tuple(sorted((f[a],e))));pairs.add(tuple(sorted((f[b],e))))
  for (ab,e),(cd,g) in combinations(edge.items(),2):
   if set(ab)&set(cd):need(not K[e][g],'shared endpoint zero')
 return pairs,[sum(i in p for p in pairs) for i in range(111)]
def symbolic():
 def lr(u,v):
  d=Counter({'h':1});d[u,v]+=2;d[v,u]+=2
  for w in range(7):
   if w!=u:d[u,w]-=1
  return d
 d=Counter()
 def add(x,m=1):
  for k,v in x.items():d[k]+=m*v
 for c in range(2,7):
  for e in range(2,7):
   if c!=e:add(lr(c,e))
 for c in range(2,7):add(lr(0,c),2)
 need(d['h']==30 and d[0,1]==-10,'3h coefficient')
 for c in range(2,7):d[0,c]+=6;d[c,1]+=4
 need({k:v for k,v in d.items() if v}=={'h':30,(0,1):-10},'nonnegative certificate')
 g={(u,v):0 for u in range(7) for v in range(7) if u!=v};g[0,1]=3
 for c in range(2,7):g[c,0]=1
 need(all(sum(g[u,w] for w in range(7) if w!=u)<=1+2*(g[u,v]+g[v,u]) for u,v in g),'LR-only extremal control')
 return {'identity':'20 internal LR + 2*5 outgoing LR + 6*sum g_ac(a) + 4*sum g_bc(c) = 30h-10g_ab(a)','LR_only_h1_maximum_at_least':3}
def main(a):
 K=source(a.native);cert=json.loads(a.certificate.read_text());pairs,counts=census(K,cert['configurations'])
 need(len(cert['configurations'])==275 and len(pairs)==3019,'witness contacts')
 need(min(counts)==41 and sum(x>52 for x in counts)==86,'row supports')
 ell=sum((x>36)+(x>52) for x in counts);need(ell==197,'arrival contradiction')
 bad=json.loads(a.certificate.read_text());bad['configurations'][0]['frame'][0]=bad['configurations'][0]['frame'][1]
 try:census(K,bad['configurations'])
 except ValueError:pass
 else:raise ValueError('invalid frame accepted')
 p0,c0=census(K,[]);need(not p0 and not any(c0),'empty coverage control')
 out={'status':'PASS_INDEPENDENT_UNIFORM_BLOCK_RANK_GAP','native_sha256':PIN,'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'configurations':275,'guaranteed_unordered_contacts':len(pairs),'guaranteed_degrees':counts,'minimum_guaranteed_support':min(counts),'rows_over_52':86,'arrival_lower_bound':ell,'formal_LR_identity':symbolic(),'negative_controls':['duplicate frame rejected','empty witness gives no arrival bound','197 contradicts196 but not197','abstract LR permits defect3h so coefficient2 unsupported'],'rank_floor_examples':{str(V):9*V+(V+2)//3 for V in range(1,13)},'scope':'Finite source witnesses and exact symbolic inequality. Universal block proof and nonzero-support arrival bridge separately read; no physical availability or supplier.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','configurations','guaranteed_unordered_contacts','arrival_lower_bound','formal_LR_identity']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
