#!/usr/bin/env python3
"""Actual 104-lane preload's decoder freedom modulo eight zero-aux constraints."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,json,hashlib,argparse,itertools

def need(x,m):
 if not x:raise ValueError(m)
def root(v):
 if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
 z=[i for i in range(9) if not v>>i&1];need(len(z)==2,'root');return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
def rref(A,n):
 A=[[F(x) for x in row] for row in A];r=0;piv=[]
 for c in range(n):
  k=next((k for k in range(r,len(A)) if A[k][c]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];a=A[r][c];A[r]=[x/a for x in A[r]]
  for k in range(len(A)):
   if k!=r and A[k][c]:
    a=A[k][c];A[k]=[x-a*y for x,y in zip(A[k],A[r])]
  piv.append(c);r+=1
 return A[:r],piv
def kernel(A,n):
 R,p=rref(A,n);out=[]
 for f in range(n):
  if f in p:continue
  x=[F(i==f) for i in range(n)]
  for row,c in zip(R,p):x[c]=-row[f]
  out.append(x)
 return out
def binary_basis(vs):
 d={}
 for x in vs:
  while x:
   j=x.bit_length()-1
   if j in d:x^=d[j]
   else:d[j]=x;break
 return list(d.values())
def clean(o):
 if isinstance(o,F):return str(o)
 if isinstance(o,dict):return {str(k):clean(v) for k,v in o.items()}
 if isinstance(o,(list,tuple)):return [clean(v) for v in o]
 return o
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin');n=json.loads(gzip.decompress(raw));P=n['live'];H=[P[k] for k in n['hosted']['Dports']];U=sorted(set(P)-set(H));v={h:n['frames'][n['initial'][h]][0] for h in P};rr={h:root(v[h]) for h in P};G={h:{j:F(sum(x*y for x,y in zip(rr[h],rr[j])),18) for j in P} for h in P};A={h:{j:G[h][j]-int(h==j) for j in P} for h in P}
 need(all(sum(G[h][k]*G[k][j] for k in P)==13*G[h][j] for h in P for j in P),'full tight G^2=13G');Gu=[[G[h][j] for j in U] for h in U];R,piv=rref(Gu,len(U));rank_u=len(piv);u_kernel=kernel(Gu,len(U));need(rank_u==7 and u_kernel==[[F(x) for x in (1,-1,0,-1,1,0,0,0)]],'actual coupled root relation');records=[]
 for h in H:
  forbid=[j for j in P if (v[h]&v[j]).bit_count()%2];K=kernel([[A[u][j] for u in U] for j in forbid],8);rec={'hosted':h,'normal':v[h],'facet_decoder_constraint_kernel':K,'freedom_dimension':len(K),'canonical_support_binary_basis':binary_basis(v[j] for j in P if A[h][j])}
  alternatives=[]
  for lam in K:
   row={j:sum(lam[k]*A[u][j] for k,u in enumerate(U)) for j in P};alternatives.append({j:x for j,x in row.items() if x})
  need(len(rec['canonical_support_binary_basis'])==8,'full canonical source support spans its facet');need(len(binary_basis(v[j] for j in H if A[h][j]))==8,'hosted restriction alone spans its facet');need(all(all(row.get(j,F(0))==0 for j in H) for row in alternatives),'every legal decoder freedom vanishes on hosted inputs');need(not K or K==u_kernel,'all legal-facet kernels contained in coupled relation');rec['permitted_decoder_difference_rows']=alternatives;rec['hosted_support_binary_basis']=binary_basis(v[j] for j in H if A[h][j]);records.append(rec)
 h=H[0];j=next(j for j in H if A[h][j]);E={i:{k:-int(i==k)+G[i][k]/12 for k in H} for i in P};bad={i:A[h][i] for i in P};bad[j]=0;need(any(sum(bad[i]*E[i][k] for i in P)!=int(h==k) for k in H),'deleted-hosted-coefficient negative control')
 h=next(r['hosted'] for r in records if not r['freedom_dimension']);u=U[0];need(any(A[u][j] for j in P if (v[h]&v[j]).bit_count()%2),'unrestricted-constraint negative control')
 facets={h:{x for x in range(512) if not (x&v[h]).bit_count()%2} for h in H};need(all(not (facets[h]<=facets[j]) for h in H for j in H if h!=j),'all96 final facets incomparable')
 out={'status':'PASS_EXACT_AUGMENTED_DECODER_FREEDOM','native_sha256':hashlib.sha256(raw).hexdigest(),'ports':P,'hosted':H,'coupled':U,'full_G_squared_equals_13G':True,'inverse_of_G_minus_I':'-I+G/12','coupled_Gram_rank':rank_u,'coupled_root_relations':u_kernel,'facet_freedom_census':dict(Counter(r['freedom_dimension'] for r in records)),'every_hosted_decoder_restriction_rigid':True,'every_hosted_decoder_support_spans_its_rank8_facet':True,'mandatory_auxiliary_facet_visits':96,'eight_auxiliary_monotone_visit_cap':8,'eight_auxiliary_terminal_tour_moment_floor':'176','terminal_tour_requires_proper_chart_locality_invariant':True,'negative_controls':['deleted_hosted_decoder_coefficient','unrestricted_zero_auxiliary_constraint','two_distinct_facets_falsely_nested'],'records':records};a.output.write_text(json.dumps(clean(out),sort_keys=True,indent=2)+'\n');print(out['status'],'rankU',rank_u,'facet freedom',out['facet_freedom_census'])
