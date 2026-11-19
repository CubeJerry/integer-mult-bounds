#!/usr/bin/env python3
"""Exact fixed-triangle donor-gauge obstruction; standard library only."""
import argparse
from collections import defaultdict
import gzip
from hashlib import sha256
import json
from pathlib import Path

PINS={
 'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
 'partition':'2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25',
 'source':'362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af',
}
CUTS=[(33,97),(33,101),(33,395),(33,473),(33,771),
      (80,88),(80,94),(80,97),(80,278),(80,573),(80,640),(80,726),
      (95,82),(95,94),(95,101),(95,573),(95,726),(95,771)]

def mul(a,b):
 out=0
 while b:
  if b&1:out^=a
  a<<=1;b>>=1
  if a&32:a^=0x25
 return out

MUL=[[mul(a,b)for b in range(32)]for a in range(32)]

def power(a,n):
 out=1
 while n:
  if n&1:out=MUL[out][a]
  a=MUL[a][a];n//=2
 return out

INV=[0]+[power(a,30)for a in range(1,32)]

def elimination(matrix,inverse=False,relation=False):
 a=[list(row)for row in matrix];n=len(a);m=len(a[0])if n else 0
 if inverse or relation:
  if inverse:assert n==m
  a=[row+[int(i==j)for j in range(n)]for i,row in enumerate(a)]
 pivots=[];p=0
 for c in range(m):
  k=next((k for k in range(p,n)if a[k][c]),None)
  if k is None:continue
  a[p],a[k]=a[k],a[p];tab=MUL[INV[a[p][c]]];a[p]=[tab[x]for x in a[p]]
  for k in range(n):
   if k!=p and a[k][c]:
    tab=MUL[a[k][c]];a[k]=[x^tab[y]for x,y in zip(a[k],a[p])]
  pivots.append(c);p+=1
  if p==n:break
 if inverse:
  assert p==n
  return [row[m:]for row in a]
 if relation:
  assert p<n and not any(a[p][:m])
  return p,a[p][m:],pivots
 return p

def mm(a,b):
 out=[]
 for row in a:
  dest=[0]*len(b[0])
  for k,x in enumerate(row):
   if x:
    tab=MUL[x]
    for c,y in enumerate(b[k]):dest[c]^=tab[y]
  out.append(dest)
 return out

def combination(coefficients,vectors):
 out=[0]*len(vectors[0])
 for c,row in zip(coefficients,vectors):
  if c:
   tab=MUL[c]
   for i,v in enumerate(row):out[i]^=tab[v]
 return out

def load_pinned(path,name):
 raw=gzip.decompress(path.read_bytes())
 assert sha256(raw).hexdigest()==PINS[name],(name,path)
 return json.loads(raw)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
 ap.add_argument('--triangle-author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
 args=ap.parse_args();base=args.repo/'research/moonshot-005-program/results'
 lay=load_pinned(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout')
 part=load_pinned(base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz','partition')['classes']
 cert=load_pinned(args.triangle_author/'output/ALL-CLASSES-SOURCE.json.gz','source')
 assert cert['donors']==[29,36,77] and cert['receivers']==[10,33,80,95]
 roots=lay['root_table'];H=list(map(set,lay['A2']));D=list(map(set,lay['D4']))
 O=[{j for j,s in enumerate(roots)if sum(a*b for a,b in zip(r,s))==0}for r in roots]
 source={(c,j,h):a for c,j,h,a in cert['source_maps']}
 visible={(i,j):hs for i,j,hs in cert['visible']}
 v9=[[power(a,t)for t in range(9)]for a in range(1,10)]
 eye=[[int(i==j)for j in range(48)]for i in range(48)]
 assert all(MUL[a][INV[a]]==1 for a in range(1,32))
 spaces={};labels={};stacks=0;boundary_checks=0
 decoders={};local_outputs={}
 for i in cert['receivers']:
  for j in cert['donors']:
   hs=[h for h,U in enumerate(H)if j in U and U<=O[i]]
   assert hs==visible[i,j] and len(hs)==16
   byD=defaultdict(list);bylabels=defaultdict(list)
   for c in range(5):
    M=[r for h in hs for r in source[c,j,h]];M1=elimination(M,inverse=True)
    assert mm(M1,M)==eye;stacks+=1
    for idx,h in enumerate(hs):
     ds=part[str(h)][c];portrows=[t for t,d in enumerate(ds)if D[d]<=O[i]]
     assert len(portrows)==3
     pos=sorted(H[h]).index(j);A=[[v9[r][t]for t in range(3*pos,3*pos+3)]for r in portrows]
     lift=[[row[3*idx+s]for s in range(3)]for row in M1]
     dec=mm(lift,elimination(A,inverse=True));key=c,i,h
     if key in decoders:assert decoders[key]==dec
     else:decoders[key]=dec
     local_outputs[c,i,h,j]=mm(A,source[c,j,h])
     for at,p in enumerate(portrows):
      vec=[0]*240;vec[48*c:48*c+48]=[row[at]for row in dec]
      byD[ds[p]].append(vec);bylabels[ds[p]].append([h,c,at])
   for d,vecs in byD.items():
    assert j in D[d] and D[d]<=O[i]
    assert len(vecs)==elimination(vecs)==4
    spaces[i,j,d]=vecs;labels[i,j,d]=bylabels[d]
  for c in range(5):
   boundary=[]
   for h in sorted({h for j in cert['donors']for h in visible[i,j]}):
    rows=[[0]*144 for _ in range(3)]
    for at,j in enumerate(cert['donors']):
     if j in H[h]:
      for r,row in enumerate(local_outputs[c,i,h,j]):rows[r][48*at:48*at+48]=row
    boundary+=rows
   assert len(boundary)==135 and elimination(boundary)==135;boundary_checks+=1
 full=[(i,d)for i in cert['receivers']for d,W in enumerate(D)if {29,36}<=W and W<=O[i]]
 assert len(full)==60 and set(CUTS)<=set(full)
 capacities=[]
 for i,d in CUTS:
  right=[k for k,U in enumerate(H)if i in U and U<=D[lay['dual_D4'][d]]]
  assert len(right)==4
  capacities.append({'receiver':i,'middle':d,'right_flags':right})
 matrices={j:[v for i,d in CUTS for v in spaces[i,j,d]]for j in [29,36]}
 assert [elimination(matrices[j])for j in [29,36]]==[72,71]
 rank,relation,pivots=elimination(matrices[36],relation=True)
 assert rank==71 and any(relation) and not any(combination(relation,matrices[36]))
 # All proper subcollections formed by deleting one witness cut happen to
 # have equal rank. This is a finite property only, not global minimality.
 deletion=[]
 for a in CUTS:
  chosen=[z for z in CUTS if z!=a]
  rr=[elimination([v for i,d in chosen for v in spaces[i,j,d]])for j in [29,36]]
  assert rr==[68,68];deletion.append({'deleted':a,'ranks':rr})
 audit=[]
 for name,chosen,expected in [('all_four_receivers',full,[232,223]),('three_receivers',[a for a in full if a[0]!=10],[180,178])]:
  ranks=[elimination([v for i,d in chosen for v in spaces[i,j,d]])for j in [29,36]]
  assert ranks==expected
  audit.append({'scope':name,'cuts':len(chosen),'ranks':ranks})
 bad=relation[:];idx=next(k for k,v in enumerate(bad)if v);bad[idx]=0
 assert any(combination(bad,matrices[36]))
 assert any(combination(relation,matrices[29]))
 witness={'donors':[29,36],'cuts':CUTS,'column_labels':{str(j):[{'receiver':i,'middle':d,'port':p}for i,d in CUTS for p in labels[i,j,d]]for j in [29,36]},'lift_columns':matrices,'donor36_relation':relation,'donor36_echelon_pivot_coordinates':pivots,'actual_outgoing_flags':capacities}
 args.out.mkdir(parents=True,exist_ok=True)
 raw=json.dumps(witness,sort_keys=True,separators=(',',':')).encode()
 (args.out/'WITNESS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
 result={'status':'PASS_FROZEN_TRIANGLE_DONOR_GAUGE_OBSTRUCTION','source_pins':PINS,'witness_decompressed_sha256':sha256(raw).hexdigest(),'source_stacks':stacks,'surjective_boundaries':boundary_checks,'cuts':18,'lift_columns_each':72,'ranks':[72,71],'larger_audits':audit,'single_cut_deletions_checked':len(deletion),'nonzero_relation_terms':sum(bool(v)for v in relation),'controls':{'delete_nonzero_relation_term_rejected':True,'deficient_relation_fails_on_independent_side':True,'all_single_cut_deletions_equalize_rank':True},'scope':'Frozen source and H arrays; arbitrary invertible donor coordinate changes across classes/copies; fixed proper routes; no added informative return','new_complete_kappa':False}
 (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
