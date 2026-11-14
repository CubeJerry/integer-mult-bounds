#!/usr/bin/env python3
"""Exact native distance premise and disjoint-support matrix controls."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def need(ok,msg):
 if not ok:raise ValueError(msg)
def echelon(rows):
 piv={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return piv
def reduce(x,piv):
 for p,v in sorted(piv.items(),reverse=True):
  if x>>p&1:x^=v
 return x
def rank(rows):return len(echelon(rows))
def all_words(basis):
 out=[0]
 for b in basis:out += [x^b for x in list(out)]
 return out
def gf(a,b):
 out=0
 while b:
  if b&1:out^=a
  a<<=1;b>>=1
  if a&4:a^=7
 return out
def lifted(word,t,V):return sum(((word>>j)&1)<<(V*j+t) for j in range(111))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 raw=args.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native byte pin');n=json.loads(gzip.decompress(raw))
 roots=[list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 K=[sum(int(i==j or sum(a*b for a,b in zip(r,s))==0)<<j for j,s in enumerate(roots)) for i,r in enumerate(roots)]
 C=list(echelon(K).values());code=all_words(C);full=(1<<111)-1
 need(len(C)==9 and len(set(code))==512,'entire canonical binary code')
 records=[];restrictions=[]
 for i,k in enumerate(K):
  z=full^k;piv=echelon([c&z for c in C]);need(len(piv)==8,'single forbidden restriction rank8')
  words={c&z for c in code};need(len(words)==256 and sum(not(c&z) for c in code)==2,'exact restriction code')
  nonzero=[x for x in words if x];minimum=min(x.bit_count() for x in nonzero)
  witness=min(x for x in nonzero if x.bit_count()==minimum);need(minimum>=18,'minimum forbidden distance18')
  records.append({'receiver':i,'distance':minimum,'minimum_word_hex':hex(witness)});restrictions.append(piv)
 census=dict(sorted(Counter(x['distance'] for x in records).items()))
 need(census=={18:7,19:24,20:52,21:16,22:11,23:1},'exact distance census')
 minimum_record=next(x for x in records if x['distance']==18);i=minimum_record['receiver'];w=int(minimum_record['minimum_word_hex'],16)
 points=[j for j in range(111) if w>>j&1];p,q=sum(1<<j for j in points[:9]),sum(1<<j for j in points[9:])
 rp,rq=reduce(p,restrictions[i]),reduce(q,restrictions[i]);need(rp==rq!=0,'disjoint nine-point residual collision')
 normalized=[]
 for r in roots:
  factor=(2 if sum(x*x for x in r)==1 else 1)*(1 if next(x for x in r if x)>0 else -1)
  rr=[x*factor for x in r];need(all(x.denominator==1 for x in rr),'integral native root normalization');normalized.append(list(map(int,rr)))
 halfclasses={}
 for j,r in enumerate(normalized):
  key=(tuple(t for t,x in enumerate(r) if x),sum(x<0 for x in r)%2);halfclasses.setdefault(key,[]).append(j)
 groups=list(halfclasses.values());need(len(groups)==36 and max(map(len,groups))==4,'native disjoint halfclass sizes')
 hs=[sum(1<<j for j in group) for group in groups];local_counts=Counter()
 for i,k in enumerate(K):
  z=full^k;residuals=[reduce(h&z,restrictions[i]) for h in hs]
  need(all((r==0)==(h&z==0) for h,r in zip(hs,residuals)),'zero residual iff literal local support')
  nz=[r for r in residuals if r];need(len(set(nz))==len(nz),'nonzero named residuals are distinct')
  local_counts[len(hs)-len(nz)]+=1
 # Width-two rank-one cancellation is possible only in the opposite channel.
 cases=zeros=0
 for t,c,u,s,d,v in itertools.product(range(2),range(1,4),itertools.product(range(4),repeat=2),range(2),range(1,4),itertools.product(range(4),repeat=2)):
  M=[[int(r==z)^(gf(c,u[r]) if z==t else 0) for z in range(2)] for r in range(2)]
  cancel=all(M[r][z]==(gf(d,v[r]) if z==s else 0) for r in range(2) for z in range(2));cases+=1
  expected=all(gf(c,u[r])==int(r==t) for r in range(2)) and s==1-t and all(gf(d,v[r])==int(r==s) for r in range(2))
  need(cancel==expected,'exact GF4 width-two cancellation classification')
  if cancel:zeros+=1;need(tuple(u)!=tuple(v),'own generator cannot cancel its opposite paired support')
 high=[]
 for V in (3,4):
  I=sum(1<<(V*r+r) for r in range(V));count=0
  for t,u,s,v in itertools.product(range(V),range(1<<V),range(V),range(1<<V)):
   M=I^sum(((u>>r)&1)<<(V*r+t) for r in range(V));R=sum(((v>>r)&1)<<(V*r+s) for r in range(V))
   need(M!=R,'higher-width rank-one correction cannot erase identity perturbation');count+=1
  high.append({'width':V,'cases':count,'whole_block_cancellations':0})
 # Exact native width-two one-saving witness, with disjoint tiny supports.
 i=next(i for i,k in enumerate(K) if k.bit_count()-1==55);T=[j for j in range(111) if j!=i and K[i]>>j&1][:3];tw=sum(1<<j for j in T)
 A=[];ell=0
 for j,k in enumerate(K):
  words=[1<<i,k^tw] if j==i else [k,k]
  need(all(x>>j&1 and x&~k==0 for x in words),'native diagonal/forbidden controls')
  support=words[0]|words[1];foreign=support.bit_count()-1;ell+=int(foreign>36)+int(foreign>52)
  A.extend([lifted(words[t],t,2) for t in range(2)])
 CV=[lifted(c,t,2) for c in C for t in range(2)];need(ell==221 and rank(A+CV)-18==2,'width-two actual saving and quotient')
 # Overlap alone breaks the V>=3 no-deletion conclusion.
 V=3;receiver=0;A=[lifted((1<<receiver) if i==receiver else k,t,V) for i,k in enumerate(K) for t in range(V)]
 CV=[lifted(c,t,V) for c in C for t in range(V)];need(rank(A+CV)-27==3,'overlap counterexample actual quotient')
 out={'status':'PASS_DISJOINT_SPARSE_OPERATOR_GATE','native_sha256':PIN,'canonical_basis_hex':list(map(hex,C)),
      'forbidden_distance_census':census,'all_restriction_distances':records,'restricted_codes_enumerated':111,'binary_words_per_restriction':512,
      'nine_point_boundary':{'receiver':minimum_record['receiver'],'first_support':points[:9],'second_support':points[9:],'common_nonzero_residual_hex':hex(rp)},
      'halfclass_sizes':list(map(len,groups)),'named_locality_census':dict(sorted(local_counts.items())),
      'GF4_width_two_matrix_cases':cases,'GF4_cancellation_cases':zeros,'higher_width_matrix_controls':high,
      'native_width_two_control':{'receiver':i,'removed_contacts':T,'foreign_support':52,'ell':221,'actual_canonical_quotient':2},
      'overlap_control':{'width':3,'receiver':receiver,'ell':220,'actual_canonical_quotient':3,'violated_hypothesis':'three scalar component supports share the same point'},
      'universal_claim':'proved in PROOF.md, not inferred from finite matrix controls','new_kappa':None}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:out[k] for k in ['status','forbidden_distance_census','GF4_width_two_matrix_cases','GF4_cancellation_cases']}))
if __name__=='__main__':main()
