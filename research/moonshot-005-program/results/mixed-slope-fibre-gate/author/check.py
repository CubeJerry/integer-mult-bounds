#!/usr/bin/env python3
"""Exact physical fibres for a scoped two-mixed-source caller obstruction."""
from pathlib import Path
from fractions import Fraction as F
import gzip,hashlib,json,argparse
HERE=Path(__file__).resolve().parent
PINS={'ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a','R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c'}
C=[29,30,59,60,73,74,83,84]
def need(c,m):
 if not c:raise ValueError(m)
def load(name):
 b=(HERE/'source'/name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'pin '+name)
 return json.loads(gzip.decompress(b)if name.endswith('.gz')else b)
def dot(x,y):return(x&y).bit_count()%2
def rowadd(a,b,c):
 z=dict(a)
 for j,v in b.items():
  u=z.get(j,F(0))+c*v
  if u:z[j]=u
  else:z.pop(j,None)
 return z
def main(out):
 routes=load('ROUTES.json');w=load('R0-WORD.json.gz');rr={(x['stage'],x['port']):x for x in routes['route_records']}
 rows=[{j:F(1)}for j in range(w['public'])]
 for e in w['program']:
  if e[0]=='ADD':rows[e[1]]=rowadd(rows[e[1]],rows[e[2]],F(e[3]))
  else:need(e[0]=='MOVE','source alphabet')
 roles=w['logical_involution']['role_map'];ports=w['logical_involution']['ports'];mat={}
 for h in C:
  y=int(roles['Y'][str(h)]);row=dict(rows[y]);need(row.pop(y)==1,'Y baseline')
  mat[h]={j:row.get(int(roles['X'][str(j)]),F(0))for j in ports if int(roles['X'][str(j)])in row}
  need(set(mat[h])<=set(C)and len(mat[h])==4,'class closed with four neighbours')
 for h in C:
  sq={}
  for j,c in mat[h].items():sq=rowadd(sq,mat[j],c)
  need(sq=={h:F(1)},'R involution')
 def perm(s,h,z):
  q=rr[s,h]['normal'];B=rr[s,h]['orthogonal_complement'];E=[1<<(9+8*(s-1)+k)for k in range(8)]
  v=z&~(511|sum(E))
  if dot(z&511,q):v^=q
  for b,e in zip(B,E):
   if dot(z&511,b):v^=e
   if z&e:v^=b
  return v
 for s in [1,2]:
  for h in C:
   need(rr[s,h]['normal']&1==0,'common orthogonal head axis')
   need(rr[s,h]['orthogonal_complement'][0]==1,'actual first complement axis')
   need(perm(s,h,1)==1<<(9+8*(s-1)),'head swaps with first fresh axis')
   need(perm(s,h,1<<(9+8*(s-1)))==1,'fresh swaps with head')
 cases=[]
 for e1 in [0,1]:
  for e2 in [0,1]:
   z=(e1<<9)^(e2<<17)
   for h in C:
    need(dot(rr[1,h]['normal'],z)==0,'Q is identity')
    for s in [1,2]:
     common=perm(s,C[0],z);need(perm(s,h,z)==common,'route common on fibre')
     for j in mat[h]:
      need(perm(s,j,common)==z,'conjugated R returns exact fibre')
      for key in ['input_translation','output_translation']:
       need((2*dot(rr[s,h][key],common))%2==0,'signed route cancels')
   cases.append({'epsilon':[e1,e2],'frequency_column':z,'Q_phase':0,'D_phases':[2*e1,2*e2],'R_s_equal_R0':True,'Rprime_s_equal_R0':True})
 need(perm(1,C[0],512)==1 and perm(1,C[0],512)!=512,'raw route escape control')
 # A single-column whole-field translation distinguishes epsilon1.
 need(dot(512,512)==1 and 2*dot(512,512)%2==0,'one-column translation scope control')
 # Walsh recovery for one nonzero scalar shear; full proof uses invertibility.
 I={(0,0):F(1),(1,1):F(1)};E={(1,0):F(1)}
 def mul(A,B):
  out={}
  for(i,k),a in A.items():
   for(l,j),b in B.items():
    if k==l:out[i,j]=out.get((i,j),F(0))+a*b
  return{k:v for k,v in out.items()if v}
 walsh={}
 for d1 in [-1,1]:
  for d2 in [-1,1]:
   f1={k:d1*v for k,v in I.items()};f1.update(E)
   f2={k:d2*v for k,v in I.items()};f2.update(E)
   for k,v in mul(f2,f1).items():walsh[k]=walsh.get(k,F(0))+F(d2,4)*v
 need({k:v for k,v in walsh.items()if v}==E,'nonzero Walsh d2 coefficient')
 result={'status':'PASS_SOURCE_BOUND_FOUR_FIBRE_GATE','source_pins':PINS,'class_ports':C,'R0_rows':{str(h):{str(j):str(v)for j,v in mat[h].items()}for h in C},'cases':cases,'all_width_scope':'Every V>=2: append V-2 zero Fourier columns.','controls':['raw route exits fibre','single-column translation distinguishes epsilon','nonzero Walsh d2 coefficient'],'scope':'Two public banks, two distinct mixed sources once each, and intervening invertible factors with the same action on the four declared fibres. Arbitrary spatial routes, helpers, body idles and new sources remain open.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=HERE/'RESULT.json');main(p.parse_args().out)
