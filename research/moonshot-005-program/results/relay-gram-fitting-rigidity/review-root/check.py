#!/usr/bin/env python3
"""Independent exact check of the seventeen-port rigidity witness."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c'

def root(v):
 if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
 z=[i for i in range(9) if not(v>>i&1)];assert len(z)==2
 return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rankmod(a,p):
 a=[[x.numerator*pow(x.denominator,-1,p)%p for x in row] for row in a];r=0
 for j in range(len(a[0])):
  k=next((i for i in range(r,len(a)) if a[i][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][j],-1,p);a[r]=[x*v%p for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    v=a[i][j];a[i]=[(x-v*y)%p for x,y in zip(a[i],a[r])]
  r+=1
 return r

def run(path):
 raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN
 w=json.loads(gzip.decompress(raw));rm={int(k):v for k,v in w['source_role_map'].items()}
 ports=sorted(h for h in rm if h<112);H=sorted(map(int,w['relay']['permutation']))
 masks={h:w['frames'][w['initial'][rm[h]]][0] for h in ports}
 basis=[root(z) for z in w['relay']['ground_Gram_frame']]
 g={h:[F(dot(root(masks[h]),z),18) for z in basis] for h in ports}
 forbidden=lambda i,j:(masks[i]&masks[j]).bit_count()%2==1
 assert all(dot(g[h],g[h])==1 for h in ports)
 assert all((dot(g[i],g[j])==0)==forbidden(i,j) for i in ports for j in ports if i!=j)
 frame=(0,7,20,27,36,46,57,111)
 assert set(frame)<=set(H)
 assert [[dot(g[i],g[j]) for j in frame] for i in frame]==[[F(i==j) for j in range(8)] for i in range(8)]
 f={h:[dot(g[h],g[b]) for b in frame] for h in ports}
 witnesses=[(1,12,0,4),(1,8,1,4),(1,10,1,5),(2,10,2,5),(2,13,0,3),(4,9,6,4),(5,9,6,7)]
 connected={0};edges=[]
 for i,j,a,b in witnesses:
  assert i in H and j in H and forbidden(i,j)
  assert [4*x*y for x,y in zip(f[i],f[j])]==[F(k==a)-F(k==b) for k in range(8)]
  edges.append((a,b))
 for _ in range(8):
  for a,b in edges:
   if a in connected or b in connected:connected|={a,b}
 assert len(connected)==8
 used=set(frame)|{i for row in witnesses for i in row[:2]};assert len(used)==17
 S=w['relay']['unrestored_ports']
 C=[[sum(g[h][i]*g[h][j] for h in S) for j in range(8)] for i in range(8)]
 cm=[[C[i][j]-F(i==j) for j in range(8)] for i in range(8)]
 assert rankmod(cm,127)==6
 return {'status':'PASS_INDEPENDENT_SEVENTEEN_PORT_RIGIDITY','source_sha256':PIN,
  'orthogonal_frame':frame,'equality_tree':witnesses,'distinct_native_ports':len(used),
  'C_minus_I_rank_mod127':6,'proof_scope':'Universal operator-block rigidity follows from scalar-frame diagonalization and connected equality tree; scalar values were not substituted for unknown operator blocks.','no_new_kappa':True}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
