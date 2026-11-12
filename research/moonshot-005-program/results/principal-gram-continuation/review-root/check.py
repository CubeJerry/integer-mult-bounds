#!/usr/bin/env python3
"""Independent reconstruction of the source preconditioner; no author imports."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(gzip.decompress(p.read_bytes()))
def add(a,b,c):
 r=dict(a)
 for k,v in b.items():
  t=r.get(k,Q(0))+c*v
  if t:r[k]=t
  else:r.pop(k,None)
 return r
def space(vs):
 s={0}
 for v in vs:s.update([w^v for w in tuple(s)])
 return s

def run(w,s,linear=True):
 frames=s['frames']+[x['frame'] for x in w['additional_charts']];spaces=list(map(space,frames));loc=dict(enumerate(w['initial']));rows={i:{i:Q(1)} for i in range(1880)};cnt=Counter();ranks=Counter();rawrank=Counter();raw=set(w['private_role_map'].values());peak=0
 stop=w['marks']['common_starts'] if linear else len(w['program'])
 for t,o in enumerate(w['program'][:stop]):
  k,d=o[:2];cnt[k]+=1;need(0<=d<1880+w['owned_fields'],'role bound')
  if k=='INIT':
   need(d>=1880 and d not in loc,'fresh owned');loc[d]=o[2]
   if linear:rows[d]={}
  elif k=='CLEAR':
   need(d>=1880 and loc.get(d)==o[2],'owned retirement');del loc[d]
   if linear:del rows[d]
  elif k=='MOVE':
   a,b,own=o[2:];need(loc.get(d)==a and type(own)is bool and own==(d>=1880),'route binding');need(spaces[a]<spaces[b] or own and spaces[b]<spaces[a],'nesting');loc[d]=b;rank=abs(len(frames[a])-len(frames[b]));ranks[rank]+=1
   if d in raw:rawrank[rank]+=1
  elif k=='SCALE':
   need(Q(o[2]) and loc.get(d)==o[3],'scale');
   if linear:rows[d]={i:Q(o[2])*v for i,v in rows[d].items()}
  elif k in ('ADD','COPY'):
   r,c,at=o[2:];need(r!=d and loc.get(r)==loc.get(d)==at,'read '+str(t))
   if linear:need(k!='COPY' or not rows[d],'zero COPY');rows[d]=add(rows[d],rows[r],Q(c))
  else:raise ValueError(k)
  peak=max(peak,len(loc)-1880)
 return rows,loc,dict(cnt),dict(ranks),dict(rawrank),peak

def bound(r,D=10**18):
 target=r**199*D**200;l=0;h=r*D+1
 while l+1<h:
  m=(l+h)//2
  if m**200<=target:l=m
  else:h=m
 need(l**200<=target<(l+1)**200,'root bound');return Q(l,D),Q(l if l**200==target else l+1,D)

def root9(v):
 T=[i for i in range(9) if v>>i&1]
 if len(T)==3:return [Q(2 if i in T else -1) for i in range(9)]
 need(len(T)==7,'root domain');i,j=[k for k in range(9) if k not in T];return [Q(3*(int(k==i)-int(k==j))) for k in range(9)]
def main(a):
 sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz';need(sha(sp.read_bytes())=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source');need(sha(gzip.decompress(pp.read_bytes()))=='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','parent');s,w=load(sp),load(pp)
 raw={int(k):v for k,v in w['private_role_map'].items()};H=[s['live'][i] for i in s['hosted']['Dports']];host={h:(x,y) for h,x,y in zip(H,s['hosted']['X2'],s['hosted']['Y2'])};B=[5,56,65,69,77,96,100,103];S=[0,7,20,27,36,46,57,111];K=B+S;rt={h:root9(s['frames'][s['initial'][h]][0]) for h in H};G={(h,k):sum(x*y for x,y in zip(rt[h],rt[k]))/18 for h in H for k in H}
 need(all(G[h,k]==int(h==k) for A in (B,S) for h in A for k in A),'orthogonal full frames')
 rows,loc,*_=run(w,s);M={(h,k):Q(h==k)+rows[raw[host[h][0]]].get(raw[host[k][1]],Q(0)) for h in H for k in H}
 for h in H:
  want={raw[host[h][0]]:Q(1),host[h][0]:Q(-1)}
  for k in H:
   c=M[h,k]-int(h==k);want=add(want,{raw[host[k][1]]:Q(1),host[k][1]:Q(-1)},c)
  need(rows[raw[host[h][0]]]==want,'actual source has only b and d terms')
  for k in H:
   v=Q(h==k)+(G[h,k] if h not in B and k in B or h in B and k in S else Q(0));need(M[h,k]==v,'complete current residual formula')
 candidates=[]
 for t in H:
  if t in K:continue
  Bt=[h for h in B if G[h,t]];St=[h for h in S if G[h,t]];need(len(Bt)==len(St)==4,'all80 contact census');need(all(abs(G[h,t])==Q(1,2) for h in Bt+St),'half contacts')
  N=dict(M);changed=[]
  for h in Bt+St:need(not N[h,t],'column term genuinely missing');N[h,t]=G[h,t];changed.append([h,t])
  for k in St:need(not N[t,k],'row term genuinely missing');N[t,k]=G[t,k];changed.append([t,k])
  A=K+[t];outside=[h for h in H if h not in A]
  need(all(N[h,k]==G[h,k] for h in A for k in A),'enlarged principal block')
  need(all(not N[h,k] for h in A for k in outside),'principal outside block zero')
  need(all(N[h,k]==int(h==k) for h in outside for k in outside),'outside identity')
  sparse={h:[(k,v) for (j,k),v in N.items() if j==h and v] for h in H}
  for u in S+[t]:
   z={h:(-G[h,u] if h in B else Q(h==u) if h in S+[t] else G[h,u]) for h in H};need(all(z[k]==int(k==u) for k in S+[t]),'nine kernel pivots')
   need(all(sum(v*z[k] for k,v in sparse[h])==0 for h in H),'full actual96-coordinate kernel')
  remaining=B+outside;need(len(remaining)==87 and all(N[h,k]==int(h==k) for h in B for k in remaining),'upper unit minor block');need(all(N[h,k]==int(h==k) for h in outside for k in outside),'lower unit minor block')
  need(all(rt[t][j]==sum(G[k,t]*rt[k][j] for k in St) for j in range(9)),'five-column dependence');need(all(G[h,k]==int(h==k) for h in St for k in St),'four independent support columns')
  candidates.append({'port':t,'missing':changed,'updated_columns':[t]+St,'root_column_rank':4,'rank':87,'kernel_dimension':9,'unit_minor_dimension':87})
 need(len(candidates)==80,'all possible ports')
 report={'status':'PASS_ROOT_INDEPENDENT_PRINCIPAL_CONTINUATION_REVIEW','source_sha256':sha(sp.read_bytes()),'parent_payload_sha256':sha(gzip.decompress(pp.read_bytes())),'all1880_prefix_columns_replayed':True,'current_rank':88,'candidate_count':len(candidates),'each_candidate_exact_rank':87,'each_candidate_new_coefficients':12,'five_updated_columns_rank':4,'all_explicit_kernels_and_unit_minors_pass':True,'candidates':candidates,'scope':'Independent algebraic/source certificate. Physical realization is a separate source-word theorem.'}
 a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report['status'],len(candidates))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
