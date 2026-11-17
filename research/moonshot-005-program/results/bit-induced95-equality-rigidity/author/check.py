#!/usr/bin/env python3
"""Exact induced95 star-rigidity and canonical support certificate.

Source premises for the all-field/block proof; not a finite-width theorem substitute.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from itertools import combinations
import argparse,json,hashlib,math

NATIVE_REL=Path('research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json')
NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
T={14,17,19,20,96,99,101,102}

def need(x,s):
 if not x:raise ValueError(s)
def brank(rows):
 piv={}
 for v in rows:
  while v:
   j=v.bit_length()-1
   if j in piv:v^=piv[j]
   else:piv[j]=v;break
 return len(piv)
def det(M):
 n=len(M);A=[list(map(int,r))for r in M];last=1;sign=1
 if n==1:return A[0][0]
 for k in range(n-1):
  p=next((i for i in range(k,n)if A[i][k]),None)
  if p is None:return 0
  if p!=k:A[k],A[p]=A[p],A[k];sign=-sign
  for i in range(k+1,n):
   for j in range(k+1,n):
    num=A[i][j]*A[k][k]-A[i][k]*A[k][j]
    need(num%last==0,'Bareiss exact division');A[i][j]=num//last
  last=A[k][k]
  for i in range(k+1,n):A[i][k]=0
 return sign*A[-1][-1]
def norm(v):
 divisor=math.gcd(*v);v=[x//divisor for x in v]
 if next(x for x in v if x)<0:v=[-x for x in v]
 return tuple(v)
def binverse(rows):
 n=len(rows);A=[r|(1<<(n+i))for i,r in enumerate(rows)]
 for j in range(n):
  p=next(i for i in range(j,n)if A[i]>>j&1);A[j],A[p]=A[p],A[j]
  for i in range(n):
   if i!=j and A[i]>>j&1:A[i]^=A[j]
 need([r&((1<<n)-1)for r in A]==[1<<i for i in range(n)],'binary inverse');return[r>>n for r in A]

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/programme'))
 p.add_argument('--star',type=Path,default=Path(__file__).with_name('STAR-CERTIFICATE.json'))
 p.add_argument('--support',type=Path,default=Path(__file__).with_name('FULL-SUPPORT-CERTIFICATE.json'))
 p.add_argument('--out',type=Path,default=Path(__file__).with_name('output'));a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 raw=(a.repo/NATIVE_REL).read_bytes();need(hashlib.sha256(raw).hexdigest()==NATIVE_SHA,'native pin');R=json.loads(raw)['native_roots']
 U=set(range(8,111))-T;S=json.loads(a.star.read_bytes());C=json.loads(a.support.read_bytes());F=S['frame'];edges=S['edges']
 need(S['source_roles']==sorted(U),'exact95 source domain')
 K=lambda i,j:int(i==j or sum(x*y for x,y in zip(R[i],R[j]))==0)
 need(len(F)==len(set(F))==8 and set(F)<=U,'point frame');need(all(K(i,j)==int(i==j)for i in F for j in F),'point noncontacts')
 E={tuple(z['points']):z['role']for z in edges};need(len(E)==21 and len(set(E.values()))==21,'21 distinct edge roles')
 need(set(E.values())<=U-set(F),'all edge roles retained')
 degrees=[sum(j in e for e in E)for j in range(8)];need(degrees==[5,5,5,5,5,5,7,5],'saturated minimum degree5')
 for e,r in E.items():need(tuple(j for j,f in enumerate(F)if K(r,f))==e,'exact edge-point mask')
 for e,f in combinations(E,2):
  if set(e)&set(f):need(K(E[e],E[f])==K(E[f],E[e])==0,'shared-star edge noncontact')
 first=edges[0];u,v=first['points'];r=first['role']
 X={i:sum(K(i,j)<<k for k,j in enumerate(F))|((K(i,r)^K(i,F[u])^K(i,F[v]))<<8)for i in sorted(U)}
 need(brank(X.values())==9,'canonical rank9')
 need(all((X[i]&X[j]).bit_count()%2==K(i,j)for i in U for j in U),'all95 canonical Gram blocks')
 need(all(X[f]==1<<k for k,f in enumerate(F)),'normalized point coordinates')
 for e,r in E.items():need(X[r]==(1<<e[0])|(1<<e[1])|(1<<8),'canonical edge coordinates')
 seen=set(F)|set(E.values());anchors=[]
 for i,ns in S['ordered_anchors']:
  need(i in U-seen and len(ns)==len(set(ns))==8 and set(ns)<=seen,'ordered anchor use')
  need(all(not K(i,j)and not K(j,i)for j in ns),'two-sided actual noncontacts')
  need(brank(X[j]for j in ns)==8,'eight independent canonical anchors')
  need(all((X[i]&X[j]).bit_count()%2==0 for j in ns),'specified one-dimensional annihilator')
  anchors.append([i,ns]);seen.add(i)
 need(seen==U and len(anchors)==66,'propagation covers all95')
 need(C['canonical_vectors']=={str(i):[(X[i]>>j)&1 for j in range(9)]for i in sorted(U)},'support certificate same canonical factors')
 allwords=C['all_nonzero_words'];need([x['binary_code_mask']for x in allwords]==list(range(1,512)),'all511 codewords, no omitted mask')
 histogram=Counter();proper=[];lookup={norm(r):i for i,r in enumerate(R)}
 for word in allwords:
  mask=word['binary_code_mask'];support=[i for i in sorted(U)if (X[i]&mask).bit_count()%2]
  need(word['support']==support,'exact canonical support')
  rank=word['real_support_rank'];need(rank in [7,8],'support rank7or8')
  ids=word['independent_root_roles'];cols=word['minor_columns'];need(len(ids)==len(cols)==rank and set(ids)<=set(support),'minor from support')
  d=det([[R[i][c]for c in cols]for i in ids]);need(d==word['integer_minor_determinant']and d!=0,'nonzero exact integer minor')
  ann=word['annihilator_basis'];need(len(ann)==8-rank,'complete support upper-bound annihilator')
  need(all(sum(x*y for x,y in zip(n,R[i]))==0 for n in ann for i in support),'every support root annihilated')
  histogram[rank]+=1
  if rank==7:
   line=norm(ann[0]);native_role=lookup.get(line)
   need(native_role not in U,'proper normal not a remaining receiver role')
   proper.append({'mask':mask,'support_size':len(support),'normal_line':list(line),'native_role':native_role})
 need(histogram=={8:486,7:25},'exact486/25 split')
 need(len({tuple(x['normal_line'])for x in proper})==25,'25distinct proper normal lines')
 actual=[x['native_role']for x in proper if x['native_role']is not None]
 need(set(actual)==set(range(8))|T and len(actual)==16,'16deleted native roles plus9 absent roots')
 need(brank(x['mask']for x in proper)==9,'proper code directions span entire canonical space')
 # An invertible decoder-factor basis using only proper support directions.
 chosen=[]
 for x in proper:
  if brank(chosen+[x['mask']])>len(chosen):chosen.append(x['mask'])
  if len(chosen)==9:break
 Lambda_rows=[sum(((chosen[j]>>i)&1)<<j for j in range(9))for i in range(9)]
 dual=binverse(Lambda_rows)
 need(all(((dual[i]&sum(((chosen[j]>>k)&1)<<k for k in range(9))).bit_count()%2)==int(i==j)for i in range(9)for j in range(9)),'actual coefficient/decoder dual basis')
 result={'status':'PASS_INDUCED95_RIGIDITY_AND_EXACT_SUPPORT_CLASSIFICATION','native_sha256':NATIVE_SHA,
  'source_roles':sorted(U),'star_frame':F,'star_edges':edges,'degrees':degrees,'ordered_anchor_count':66,
  'canonical_vectors_hex':{str(i):hex(X[i])for i in sorted(U)},'canonical_scalar_rank':9,
  'support_real_rank_histogram':dict(histogram),'all511_exact_integer_minors_checked':True,
  'proper_codewords_and_normal_lines':proper,'proper_directions_binary_rank':9,
  'all_line_destination_decoder_basis':chosen,'dual_payload_basis':dual,
  'linear_equality_consequence':'At exactly9b whole-record downward entries into the remaining95 receiver downset, all entry destinations have rank at most1; nonzero destination lines belong to the listed25. Ground-only and universal Hub-birth conclusions are not established and, without cost restrictions, are false.',
  'counterexample_to_all_supports_span8':next(x for x in allwords if x['binary_code_mask']==31),
  'scope':'Arbitrary characteristic-two fields, all positive blockwidths, nonsymmetric/noncommuting fittings; source-specific equality at exact transcript dimension. No costed formation or complete supplier theorem.'}
 (a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
 print(result['status'],'star21 anchors66','support ranks',dict(histogram),'proper basis',chosen,flush=True)
if __name__=='__main__':main()
