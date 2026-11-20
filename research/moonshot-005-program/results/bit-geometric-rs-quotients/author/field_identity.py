from pathlib import Path
import importlib.util,json
import numpy as np
from argparse import ArgumentParser
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True);b=args.repo/'research/moonshot-005-program/results'
from hashlib import sha256
pin_doc=json.loads((Path(__file__).resolve().parents[1]/'SOURCE-PINS.json').read_text())
for pin_path,entry in pin_doc['files'].items():
 raw=(args.repo/pin_path).read_bytes()
 if len(raw)!=entry['bytes'] or sha256(raw).hexdigest()!=entry['sha256']:raise ValueError('Source pin '+pin_path)
s=importlib.util.spec_from_file_location('gf',b/'bit-single-rs-anchor-obstruction/author/check.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
def pwr(a,n):
 v=1
 for _ in range(n):v=int(f.M[v,a])
 return v
def q(x):return pwr(x,9)^pwr(x,18)^pwr(x,36)
zeros=[x for x in range(64)if q(x)==0];ps=[];rows=[]
for v in range(1,64):
 xs=[x for x in zeros if (q(v^x)^q(v)^q(x))==1^q(v)]
 if len(xs)!=16:raise ValueError('wrong block')
 p=f.polynomial(xs);ps.append(p);rows.append({'v':v,'q':q(v),'roots':xs,'polynomial':p.tolist()})
a=np.array(ps,dtype=np.uint8);print('GLOBAL',f.rank(a),'SUPPORT',[c for c in range(17)if np.any(a[:,c])]);print('QPOLY',f.polynomial(zeros).tolist())
print('CENTRE_RANKS',sorted(set(f.rank(np.array([p for p,row in zip(ps,rows)if x in row['roots']]))for x in zeros)))
V=np.array([[pwr(v,c)for c in range(63)]for v in range(1,64)],dtype=np.uint8);A=np.hstack([V,a]);n=63
for c in range(n):
 nz=np.flatnonzero(A[c:,c]);p=c+int(nz[0]);A[[c,p]]=A[[p,c]];A[c]=f.M[f.INV[A[c,c]],A[c]];A[:c]^=f.M[A[:c,c,None],A[c][None,:]];A[c+1:]^=f.M[A[c+1:,c,None],A[c][None,:]]
terms={str(c):[(i,int(A[i,n+c]))for i in range(63)if A[i,n+c]]for c in range(17)if np.any(a[:,c])};print('COEFF_POWERS',terms)
(args.out/'FIELD-IDENTITY.json').write_text(json.dumps({'blocks':rows,'coefficients':terms,'span_rank':f.rank(a)},indent=2)+'\n')

expected={'0':[(7,1),(16,1),(34,1),(61,1)],'1':[(6,1)],'2':[(14,1)],'4':[(30,1)],'5':[(2,1)],'8':[(62,1)],'14':[(2,1)],'16':[(0,1)]}
if terms!=expected or f.rank(a)!=7:raise ValueError('Field block formula mismatch')
for c in zeros:
 if f.rank(np.array([p for p,row in zip(ps,rows)if c in row['roots']]))!=6:raise ValueError('Single-centre rank')
 for d in zeros:
  if c==d:continue
  both=[p for p,row in zip(ps,rows)if c in row['roots']and d in row['roots']]
  if len(both)!=20 or f.rank(np.array(both))!=5:raise ValueError('Two-centre rank')
print('PASS_ALL_FIELD_BLOCK_IDENTITIES_AND_SPANS',63,28,378,flush=True)
