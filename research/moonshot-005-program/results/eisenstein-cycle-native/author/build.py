#!/usr/bin/env python3
"""Literal zero-owner 120-port order-three paired shear, with independent row replay."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,gzip,hashlib,json

def need(c,m):
 if not c:raise ValueError(m)
def brank(vs):
 piv={}
 for x in vs:
  while x:
   p=x.bit_length()-1
   if p in piv:x^=piv[p]
   else:piv[p]=x;break
 return len(piv)
def contains(U,V):return brank(U+V)==brank(U)
def facet(v):
 p=(v&-v).bit_length()-1
 return [(1<<j)^((1<<p)if v>>j&1 else 0)for j in range(9)if j!=p]
def rowadd(a,b,c):
 out=dict(a)
 for j,v in b.items():
  out[j]=out.get(j,F(0))+c*v
  if not out[j]:del out[j]
 return out

def replay(w):
 frames=w['frames'];loc=w['initial'][:];rows=[{j:F(1)}for j in range(w['public'])];hist=Counter();max_l1=1;maxsupport=1
 for k,e in enumerate(w['program']):
  if e[0]=='MOVE':
   _,j,u,v,owned=e;need(not owned,'unexpected owner');need(loc[j]==u,f'location at MOVE {k}');U,V=frames[u],frames[v];need(contains(V,U),f'nonascending MOVE {k}');r=len(V)-len(U);need(r>0,f'nonpositive MOVE {k}');hist[r]+=1;loc[j]=v
  elif e[0]=='ADD':
   _,j,l,c,u=e;need(loc[j]==loc[l]==u,f'cochart ADD {k}');need(j!=l,f'self ADD {k}');rows[j]=rowadd(rows[j],rows[l],F(c));max_l1=max(max_l1,sum(abs(x)for x in rows[j].values()));maxsupport=max(maxsupport,len(rows[j]))
  else:raise ValueError('unknown operation')
 P=w['normals'];p=len(P);ix={v:j for j,v in enumerate(P)};per=w['permutation'];need(len(per)==p,'permutation length');inv=[None]*p
 for h,j in enumerate(per):need(inv[j]is None,'permutation');inv[j]=h
 for h in range(p):
  need(rows[h]=={h:F(1)},'X endpoint');need(rows[p+h]=={p+h:F(1),per[h]:F(1)},'Y endpoint');need(rows[2*p+h]=={2*p+h:F(1),3*p+inv[h]:F(-1)},'B endpoint');need(rows[3*p+h]=={3*p+h:F(1)},'D endpoint');need(loc[h]==loc[2*p+h]==1,'Hub endpoint');need(loc[p+h]==loc[3*p+h]==2+p+h,'facet endpoint')
 inverse = []
 for e in reversed(w['program']):
  if e[0]=='MOVE':inverse.append(['MOVE',e[1],e[3],e[2],False])
  else:inverse.append(['ADD',e[1],e[2],str(-F(e[3])),e[4]])
 invhist=Counter()
 for k,e in enumerate(inverse):
  if e[0]=='MOVE':
   _,j,u,v,_=e;need(loc[j]==u,'inverse MOVE location');need(contains(frames[u],frames[v]),'inverse descending MOVE');invhist[len(frames[u])-len(frames[v])]+=1;loc[j]=v
  else:
   _,j,l,c,u=e;need(loc[j]==loc[l]==u,'inverse cochart ADD');rows[j]=rowadd(rows[j],rows[l],F(c))
 need(all(rows[j]=={j:F(1)}for j in range(w['public'])),'inverse arbitrary-input identity');need(loc==w['initial'],'inverse endpoint charts');need(invhist==hist,'same-price inverse')
 return {'literal_inverse_restores_all_inputs':True,'same_price_inverse_move_histogram':dict(sorted(invhist.items())),'move_histogram':dict(sorted(hist.items())),'events':len(w['program']),'operation_counts':dict(Counter(e[0]for e in w['program'])),'all_public_inputs':4*p,'owned_fields':0,'peak_live_owned':0,'max_scalar_row_l1':str(max_l1),'max_scalar_row_support':maxsupport,'integer_grid_exact':all(c.denominator==1 for row in rows for c in row.values()),'all_input_endpoint_identities':True}

def make(sym):
 P=sorted(v for cyc in sym['cycles']for v in cyc);p=len(P);ix={v:j for j,v in enumerate(P)};pi={cyc[i]:cyc[(i+1)%3]for cyc in sym['cycles']for i in range(3)};need(p==120,'full root lines');per=[ix[pi[v]]for v in P];need(all(per[per[per[h]]]==h and per[h]!=h for h in range(p)),'order-three permutation')
 frames=[[],[1<<j for j in range(9)]]+[[v]for v in P]+[facet(v)for v in P];initial=[2+h for h in range(p)]+[0]*p+[2+h for h in range(p)]+[0]*p;program=[]
 for h in range(p):
  j=per[h];L=2+j;H=2+p+h;need((P[h]&P[j]).bit_count()%2==0,'edge orthogonality')
  program +=[['MOVE',3*p+h,0,L,False],['ADD',2*p+j,3*p+h,'-1',L],['MOVE',3*p+h,L,H,False]]
 for h in range(p):
  j=per[h];L=2+j;H=2+p+h
  program +=[['MOVE',p+h,0,L,False],['ADD',p+h,j,'1',L],['MOVE',p+h,L,H,False]]
 for h in range(p):
  program +=[['MOVE',h,2+h,1,False],['MOVE',2*p+h,2+h,1,False]]
 return {'schema':'moonshot-S013-full120-Eisenstein-cycle-native-v1','public':4*p,'owned_fields':0,'normals':P,'permutation':per,'frames':frames,'initial':initial,'program':program,'logical_endpoints':'X=x; Y=y+R x; B=b-R^T d; D=d; (R x)_h=x_pi(h)','source_pins':{'symmetry':hashlib.sha256(json.dumps(sym,indent=2,sort_keys=True).encode()+b'\n').hexdigest()}}

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--symmetry',type=Path,default=Path(__file__).with_name('SYMMETRY.json'));pa.add_argument('--output-dir',type=Path,default=Path(__file__).parent);a=pa.parse_args();sym=json.loads(a.symmetry.read_text());w=make(sym);r=replay(w);a.output_dir.mkdir(parents=True,exist_ok=True);raw=gzip.compress(json.dumps(w,sort_keys=True,separators=(',',':')).encode(),mtime=0);(a.output_dir/'WORD.json.gz').write_bytes(raw)
 controls={}
 for name,change in [('wrong_ADD_sign',lambda z:z['program'][1].__setitem__(3,'1')),('wrong_cross_port',lambda z:z['program'][1].__setitem__(1,2*120)),('changed_D_endpoint',lambda z:z['program'][2].__setitem__(3,2+120+1))]:
  bad=copy.deepcopy(w);change(bad)
  try:replay(bad)
  except ValueError:controls[name]=True
  else:controls[name]=False
 need(all(controls.values()),'negative control admitted');r.update(status='PASS_EXACT_FULL120_ORDER_THREE_NATIVE',word_sha256=hashlib.sha256(raw).hexdigest(),symmetry_sha256=hashlib.sha256(a.symmetry.read_bytes()).hexdigest(),negative_controls_rejected=controls,physical_column_phase_checked=False,caller_admission=False,no_new_kappa=True);(a.output_dir/'RESULT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
if __name__=='__main__':main()
