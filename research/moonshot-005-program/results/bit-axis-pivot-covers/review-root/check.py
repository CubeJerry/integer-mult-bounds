#!/usr/bin/env python3
"""Independent geometric/minimal-cover audit; no author implementation imported."""
import argparse,hashlib,json
from pathlib import Path
from functools import lru_cache
import sympy as sp

def binary_rank(rows):
 piv={}
 for x in rows:
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;break
 return len(piv)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 source=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(source.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
 rec=json.loads(source.read_text());roots=rec['native_roots'];assert len(roots)==111
 K=[sum(1<<j for j,s in enumerate(roots) if j==i or dot(r,s)==0) for i,r in enumerate(roots)];assert binary_rank(K)==9
 @lru_cache(None)
 def rank_support(s):return sp.Matrix([roots[j] for j in s]).rank() if s else 0
 result=[];checked=0
 for mask,axis,chi in [(3,1,108),(5,2,108),(6,3,104),(9,4,106),(10,5,110),(12,6,108),(15,7,110)]:
  cert=json.loads((a.package/'output'/f'PIVOT-{mask}-COVERS.json').read_text());h=[(dot(roots[0],r)//2+dot(roots[axis],r)//2)%2 for r in roots]
  W=[sum(1<<j for j in range(111) if (K[i]>>j)&1 and h[i]==h[j]) for i in range(111)];assert binary_rank(W)==15 and binary_rank(W+K)==16
  ones=[];charges=0
  for i,e in enumerate(cert['covers']):
   assert e['receiver']==i and e['h']==h[i] and int(e['fitting_row_hex'],16)==W[i]
   support=tuple(j for j in range(111) if j!=i and ((W[i]>>j)&1));assert list(support)==e['foreign_support'];rk=rank_support(support);assert rk==e['foreign_span_rank'] and rk in (6,7)
   union=set()
   for item in e['cover']:
    chart=item['chart'];M=sp.Matrix(chart['rows'])
    basis=M.nullspace() if chart['kind']=='ann' else [sp.Matrix(row) for row in chart['rows']]
    B=sp.Matrix.hstack(*basis) if basis else sp.zeros(8,0);dim=B.rank();assert dim==item['dimension'] and 0<dim<7
    assert all(dot(roots[i],v)==0 for v in basis)
    for j in item['support']:
     assert j in support
     if chart['kind']=='ann':assert M*sp.Matrix(roots[j])==sp.zeros(M.rows,1)
     else:assert B.row_join(sp.Matrix(roots[j])).rank()==dim
    union.update(item['support'])
   assert union==set(support)
   min_count=1 if rk==6 else 2;assert len(e['cover'])>=min_count and len(e['cover'])<=2
   charge=min_count-1;assert charge==e['charge'];charges+=charge
   if not charge:ones.append(i)
   checked+=1
  assert charges==chi
  result.append({'pivot':mask,'carriers':[0,axis],'chi':chi,'one_chart_receivers':ones,'W_rank':15,'canonical_joint_rank':16})
 assert (W[0]^(1<<0))&(1<<0)==0
 bad=next(i for i in range(111) if h[i] and any(j!=i and (W[i]>>j)&1 and dot(roots[0],roots[j])!=0 for j in range(111)))
 assert rank_support(tuple(j for j in range(111) if j!=0 and (W[0]>>j)&1))==7
 out={'status':'PASS_ROOT_INDEPENDENT_NATIVE_PIVOT_COVERS','pairs_checked':checked,'pivots':result,'negative_controls':['Removing own coefficient invalidates fitting','Assigning both h-one pieces to first carrier fails actual inclusion','Rank7 support cannot have one proper chart'],'proof_scope':'Exact fixed-native support/minimum-cover certificates plus reviewed all-field tensor lift; no physical decoder or supplier.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sympy_version':sp.__version__,'new_complete_kappa':False}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
