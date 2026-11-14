#!/usr/bin/env python3
"""Independent native premises and boundary controls for the odd-cycle theorem."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path

def need(b,s):
    if not b:raise ValueError(s)

def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native source pin')
    n=json.loads(gzip.decompress(raw));roots=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
    dot=lambda u,v:sum(x*y for x,y in zip(u,v))
    orthcycle=[92,36,54,38,55];nonorthcycle=[92,38,36,55,54]
    gram=[[dot(roots[i],roots[j]) for j in orthcycle] for i in orthcycle]
    need(all(bool(gram[i][j])==(i==j or (i-j)%5 in (2,3)) for i in range(5) for j in range(5)),'exact induced orthogonality pentagon')
    need(all(dot(roots[i],roots[j]) for i,j in zip(nonorthcycle,nonorthcycle[1:]+nonorthcycle[:1])),'actual odd nonorthogonality cycle')
    # Rebuild the quotient without loading either author's code or core rows.
    groups={}
    for j,v in enumerate(roots[8:],8):groups.setdefault((tuple(k for k,x in enumerate(v) if x),sum(x<0 for x in v)%2),[]).append(j)
    piv=[10,11,20,21,28,24,36,37,38,39,50,49,55,54,59,65,67,70,79,74,81,84,88,92,101,97,108,107]
    rows=[]
    for i,v in enumerate(roots):
        r=sum(1<<j for j,w in enumerate(roots) if i==j or dot(v,w)==0)&~255
        for p,g in zip(piv,groups.values()):
            if i==p or dot(v,roots[p])==0:r^=sum(1<<j for j in g)
        rows.append(r)
    mask=sum(1<<j for j in orthcycle);need(all(not(r&mask) for r in rows),'every granted core row vanishes on selected independent inputs')
    need(all(not(mask>>j&1) for j in [8,9,16]),'historical donor units also vanish')
    zero_neighbors={i:[j for j in orthcycle if dot(roots[i],roots[j])==0] for i in orthcycle}
    need(all(len(z)==2 for z in zero_neighbors.values()),'after three receiver entries no selected source line is local')
    proof=a.proof.read_bytes();section_hash=hashlib.sha256(proof.split(b'## 5.')[0]).hexdigest()
    need(section_hash=='48d3fbbe0692e8ced9e124cf5ddd8b450be5ac0787e25167dc3743c3dc9cb9c6','unchanged independently reviewed universal proof')
    # Test the strongest claimed scope control on all four two-target blocks.
    def mul(A,B):return [[sum(x*y for x,y in zip(row,col))%2 for col in zip(*B)] for row in A]
    def add(A,B):return [[x^y for x,y in zip(r,s)] for r,s in zip(A,B)]
    I=[[1,0],[0,1]];Z=[[0,0],[0,0]]
    embed=[[[1,0],[0,0]],[[0,0],[1,0]]],[[[0,1],[0,0]],[[0,0],[0,1]]]
    selectors=[[[1,0],[0,0]],[[0,0],[1,0]]],[[[0,1],[0,0]],[[0,0],[0,1]]]
    # Packet p carries coordinate p of both inputs. Receiver i selects slot i.
    for i in range(2):
        for j in range(2):need(add(mul(selectors[i][0],embed[0][j]),mul(selectors[i][1],embed[1][j]))==(I if i==j else Z),'noncommuting two-target actual decoder')
    own=[mul(selectors[i][0],embed[0][i]) for i in range(2)]
    need(add(*own)==Z and Z!=I,'arbitrary blocks do not obey scalar alternating contribution')
    out=dict(status='PASS_INDEPENDENT_NATIVE_ODD_CYCLE_AND_SCOPE_REVIEW',native_sha256=hashlib.sha256(raw).hexdigest(),author_proof_sha256=hashlib.sha256(proof).hexdigest(),reviewed_sections_sha256=section_hash,orthogonality_cycle=orthcycle,nonorthogonality_cycle=nonorthcycle,Gram=[[int(x) for x in row] for row in gram],all_core_restrictions_zero=True,local_read_deadline=3,noncommuting_two_target_decoder_verified=True,universal_proof='Read independently: first-entry cyclic module, reciprocal edge identity, alternating decoder weight over every nonzero commutative ring with 2=0.',scope='Exactly two independent channels; excludes genuinely coupled packet/Y history and arbitrary noncommuting blocks. No physical pentagon decoder is supplied.',new_kappa=None)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'native_cycle':nonorthcycle}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for s in ['native','proof','output']:p.add_argument('--'+s,type=Path,required=True)
    main(p.parse_args())
