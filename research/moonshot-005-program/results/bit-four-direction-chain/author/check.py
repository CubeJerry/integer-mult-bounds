#!/usr/bin/env python3
"""Native coupled chain fitting and exact fixed-code support optimum."""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def basis(rows):
 piv={};original=[]
 for row in rows:
  x=row
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;original.append(row);break
 return original
def rank(rows):return len(basis(rows))
def combos(rows):
 out=[0]
 for r in rows:out += [x^r for x in list(out)]
 return out
def lift(h,t):return sum(((h>>j)&1)<<(2*j+t) for j in range(111))
def xor(rows):
 out=0
 for x in rows:out^=x
 return out
def kernel(rows,mask):
 piv={};out=[]
 for row in rows:
  z=row&mask;r=row
  while z:
   p=z.bit_length()-1
   if p in piv:s,t=piv[p];z^=s;r^=t
   else:piv[p]=(z,r);break
  if not z:out.append(r)
 need(rank(out)==len(out)==len(rows)-rank([r&mask for r in rows]),'restriction kernel')
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw))
 rr=[list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 K=[sum(int(i==j or sum(x*y for x,y in zip(r,s))==0)<<j for j,s in enumerate(rr)) for i,r in enumerate(rr)]
 C=basis(K);need(len(C)==9,'canonical rank');receivers=[7,24,25];common=K[7]&K[24]&K[25]
 for i in receivers:common &= ~(1<<i)
 T=[j for j in range(111) if common>>j&1];need(len(T)==36,'shared contacts');P,tips=T[:-4],T[-4:];p=sum(1<<j for j in P)
 hs=[p^(1<<tips[0]),1<<tips[1],1<<tips[2],p^(1<<tips[3])];need(rank(C+hs)==13,'scalar envelope four')
 H=[[hs[0],hs[1]],[hs[1],hs[2]],[hs[2],hs[3]]];selectors=[[1,4],[3,4],[1,6]];A=[];rows=[]
 even=sum(1<<(2*j) for j in range(111));full=(1<<111)-1
 for i,k in enumerate(K):
  U=selectors[receivers.index(i)] if i in receivers else [0,0]
  block=[[xor(H[b][t] for b in range(3) if U[r]>>b&1)^(k if r==t else 0) for t in range(2)] for r in range(2)]
  need(all((block[r][t]>>i&1)==int(r==t) for r in range(2) for t in range(2)),'identity diagonal');need(all(x&~k==0 for row in block for x in row),'forbidden zeros')
  support=block[0][0]|block[0][1]|block[1][0]|block[1][1];foreign=support.bit_count()-1;ell=int(foreign>36)+int(foreign>52)
  A += [lift(block[r][0],0)^lift(block[r][1],1) for r in range(2)]
  rows.append({'i':i,'U':U,'foreign_support':foreign,'ell':ell,'blocks_hex':[[hex(x) for x in row] for row in block]})
 CV=[lift(c,t) for c in C for t in range(2)];E=[lift(h[0],0)^lift(h[1],1) for h in H]
 need(sum(x['ell'] for x in rows)==216,'six saving units');need(rank(A+CV)-18==rank(E+CV)-18==3,'actual quotient three');need(all(rows[i]['foreign_support']==28 for i in receivers),'exact32-block deletions')
 W=basis(CV+E);need(len(W)==21,'permitted code dimension');optimum=0;cases=0;optrows=[];dimensions=[]
 for i,k in enumerate(K):
  forbidden=lift(full^k,0)^lift(full^k,1);ker=kernel(W,forbidden);dimensions.append(len(ker));words=combos(ker)
  first=[x for x in words if (x>>(2*i))&3==1];second=[x for x in words if (x>>(2*i))&3==2];best=1000;arg=None
  for x,y in itertools.product(first,second):
   active=x|y;foreign=((active|(active>>1))&even).bit_count()-1;cases+=1
   if foreign<best:best=foreign;arg=(x,y)
  ell=int(best>36)+int(best>52);optimum+=ell;optrows.append({'i':i,'foreign_support':best,'ell':ell,'row_pair_hex':list(map(hex,arg)),'affine_pair_cases':len(first)*len(second)})
 need(optimum==216,'exact binary fixed-code optimum216')
 out={'status':'PASS_NATIVE_FOUR_DIRECTION_CHAIN','native_sha256':PIN,'receivers':receivers,'common_contacts':T,'shared_patch':P,'tips':tips,
      'scalar_directions_hex':list(map(hex,hs)),'H_raw_hex':[[hex(x) for x in row] for row in H],'scalar_envelope_dimension':4,'canonical_quotient_dimension':3,'rank_A':rank(A),'ell':216,'all_fitting_rows':rows,
      'fixed_code_optimum':{'ell':optimum,'whole_block_row_pair_cases':cases,'maximum_local_code_dimension':max(dimensions),'rows':optrows},
      'no_nonzero_decomposable_tensor_over_any_extension':'proved by shifted-column first/last nonzero coordinate argument',
      'classification':'native algebraic fitting and finite fixed-code optimum; no physical source, target or new kappa','new_kappa':None}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'ell':216,'quotient':3,'scalar_envelope':4,'exact_fixed_code_ell':optimum,'row_pair_cases':cases}))
if __name__=='__main__':main()
