"""Independent native stock row ranks modulo the Fermat prime 65,537."""
import argparse,ctypes,gzip,hashlib,json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True);p.add_argument('--lib',type=Path,required=True)
p.add_argument('--out',type=Path,required=True);a=p.parse_args()
raw=gzip.decompress(a.source.read_bytes());digest=hashlib.sha256(raw).hexdigest()
assert digest=='7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48'
w=json.loads(raw);f=ctypes.CDLL(str(a.lib.resolve())).rank_mod;f.argtypes=[ctypes.c_void_p,ctypes.c_size_t,ctypes.c_size_t];f.restype=ctypes.c_size_t
prime=65537;m=w['first_output'];moves={e:(a,b) for e,a,b in w['moves']};fo={};rev=defaultdict(list);qcache={}
for e,terms in w['forms']:
    ff=[]
    for j,q in terms:
        if q not in qcache:
            k=Fraction(q);qcache[q]=(k.numerator*pow(k.denominator,-1,prime))%prime
        ff.append((j,qcache[q]));rev[j if j in moves else m+~j].append((e if e in moves else ~(e-m),qcache[q]))
    fo[e]=ff
results={}
for label,terms,sched,source in [('forward',fo,w['schedule'],w['initial']),('adjoint',rev,[e for e in reversed(w['schedule']) if e in moves]+list(range(m,m+len(w['initial']))),w['final'])]:
    n=len(source);locations=defaultdict(list);offsets={~i:i for i in range(n)}
    vals=np.zeros((len(sched)+n,n),dtype=np.int64);vals[:n]=np.eye(n,dtype=np.int64)
    for j,role in enumerate(source):locations[role].append(j)
    for step,e in enumerate(sched):
        oo=n+step
        ins,charges=zip(*terms[e])
        vals[oo]=np.asarray(charges,dtype=np.int64) @ vals[[offsets[i] for i in ins]] % prime
        offsets[e]=oo
        if e in moves:locations[moves[e][1 if label=='forward' else 0]].append(oo)
    total=0
    for role,vec in locations.items():
        mag=np.ascontiguousarray(vals[vec],dtype=np.uint32)
        r=f(mag.ctypes.data,*mag.shape)
        assert r==len(vec),(role,r,len(vec))
        total+=r
    results[label]={'prime':prime,'charts':len(locations),'total_independent_rows':total}
a.out.mkdir(exist_ok=True,parents=True)
(a.out/'BANKS.json').write_text(json.dumps(results,indent=2)+'\n')
print(results)
