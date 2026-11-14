#!/usr/bin/env python3
"""Exact finite native-code evidence; all-subset/all-width theorem is in PROOF.md."""
import argparse, gzip, hashlib, json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
BASIS=[0,1,2,4,8,9,14,30,59]
def need(ok,msg):
 if not ok: raise ValueError(msg)
def rank(rows):
 piv={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in piv:x^=piv[j]
   else:piv[j]=x;break
 return len(piv)
def xsum(rows):
 out=0
 for x in rows:out^=x
 return out
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native byte pin')
 n=json.loads(gzip.decompress(raw));root=[[Fraction(x)for x in n['frames'][str(n['start'][i])]['B'][0]]for i in range(111)]
 K=[sum(1<<j for j in range(111)if i==j or sum(x*y for x,y in zip(root[i],root[j]))==0)for i in range(111)]
 G=[K[i]for i in BASIS];need(rank(K)==rank(G)==9,'canonical9')
 words=[xsum(G[j]for j in range(9)if mask>>j&1)for mask in range(512)];need(len(set(words))==512,'complete distinct code')
 full=(1<<111)-1;details=[];sharp=None
 for i in range(111):
  N=full^K[i];restr={w&N for w in words};d=min(w.bit_count()for w in restr if w)
  need(len(restr)==256 and rank([g&N for g in G])==8,'forbidden rank8')
  need([w for w in words if not w&N]==[0,K[i]],'kernel exactly canonical row')
  details.append({'receiver':i,'forbidden_columns':N.bit_count(),'rank':8,'distinct_words':256,'minimum_nonzero_weight':d})
  if d==18 and sharp is None:
   w=min(w for w in restr if w and w.bit_count()==18);r=rank([g&(N^w)for g in G]);need(r==7,'sharp18 deletion drops rank to7')
   sharp={'receiver':i,'deleted_columns':[j for j in range(111)if w>>j&1],'restricted_word_hex':hex(w),'rank_before':8,'rank_after':r,'source_codeword_hex':hex(next(v for v in words if v&N==w))}
 census=Counter(x['minimum_nonzero_weight']for x in details);need(census=={18:7,19:24,20:52,21:16,22:11,23:1},'restriction census')
 degrees=[w.bit_count()-1 for w in K];need(Counter(degrees)=={55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1},'foreign-degree census')
 bounds=[{'coordinate_count':s,'possible_second_indicator_losses':sum(f<=52+s for f in degrees),'ell_lower_bound':2*(111-s)-sum(f<=52+s for f in degrees)}for s in range(5)]
 need([x['ell_lower_bound']for x in bounds]==[222,220,218,215,202],'target exclusions')
 # A real algebraic fitting with more coordinates guards against overextending
 # this theorem to arbitrary coordinate additions. No physical word is supplied.
 S=[0,1,2,3,4,9,30,8];sm=sum(1<<j for j in S);A=[(1<<i)if i in S else w&~sm for i,w in enumerate(K)]
 need(all((w>>i)&1 and not(w&~K[i])for i,w in enumerate(A)),'eight-coordinate finite fitting')
 ell=sum((w.bit_count()-1>36)+(w.bit_count()-1>52)for w in A);need(ell==183,'eight-coordinate scoped negative control')
 need(all(rank(G+[1<<s for s in S]+[w])==rank(G+[1<<s for s in S])for w in A),'negative control has prescribed history space')
 # At an included coordinate the diagonal need not use the canonical row.
 need(A[0]==1 and A[0]!=K[0],'inside-S canonical-row counterexample')
 out={'status':'PASS_EXACT_NATIVE_CANONICAL_COORDINATE_GATE','native_sha256':PIN,'basis_indices':BASIS,'canonical_rows_hex':[hex(w)for w in K],'code_dimension':9,'minimum_canonical_weight':min(w.bit_count()for w in words if w),'receiver_restrictions':details,'distance_census':dict(census),'all_subset_deletion_robustness':17,'sharpness_control':sharp,'foreign_degree_census':dict(Counter(degrees)),'coordinate_support_lower_bounds':bounds,'necessary_target_ell_upper':194,'scope_guard_eight_coordinate_fitting':{'coordinates':S,'rank':rank(A),'ell':ell,'physical_word_constructed':False},'universal_scope':'Written proof lifts fixed finite code evidence to EVERY <=17 deleted-coordinate subset, every characteristic-two field and arbitrary matrix coefficients/width. Target exclusion established for <=4 coordinate directions only.','new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k]for k in['status','distance_census','sharpness_control','coordinate_support_lower_bounds','scope_guard_eight_coordinate_fitting']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
