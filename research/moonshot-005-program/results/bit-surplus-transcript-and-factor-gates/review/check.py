#!/usr/bin/env python3
"""Independent GF(257) flat census, low support test and nonlinear surplus invoice."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from fractions import Fraction as Q
from pathlib import Path

P=Path('research/moonshot-005-program')
N=P/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
C=P/'results/bit-induced95-equality-rigidity/author/FULL-SUPPORT-CERTIFICATE.json'
PR=P/'results/bit-low-exterior-formation-gate/author/output/RESULT.json'
DUAL=[
    (['.99308','.72026','.33149','.92753'],'.73402','4.46267'),
    (['.99308','.58187','.26856','.74999'],'.58717','2.51092')]


def load(repo,path,pin):
    b=(repo/path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=pin:raise ValueError(path)
    return json.loads(b)


def price(n):
    unit=10**28
    a,b=0,9*unit
    v=n**199*unit**200
    while b-a>1:
        z=(a+b)//2
        if z**200<=v:a=z
        else:b=z
    return Q(a,unit),Q(b,unit)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',required=True,type=Path);parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    roots=load(args.repo,N,'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e')['native_roots']
    code=load(args.repo,C,'012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963')['canonical_vectors']
    room=Q(load(args.repo,PR,'befef29e616a3adebe070251a87c6f85c94a81bf687db2dceafdbbf067017145')['sources'][0]['normalized_room']['rational'][1])
    labels=sorted(set(range(8,111))-{14,17,19,20,96,99,101,102})
    xi=[sum(bit<<j for j,bit in enumerate(code[str(i)])) for i in labels]
    word={s:[(x&s).bit_count()%2 for x in xi] for s in range(1,512)}
    light=[s for s,v in word.items()if sum(v)<=40]
    assert len(light)==6
    incidence=[sum(word[s][j]<<k for k,s in enumerate(light))for j in range(95)]
    raw=''.join(' '.join(map(str,roots[i]))+'\n'for i in labels)+' '.join(map(str,incidence))+'\n'
    with tempfile.TemporaryDirectory() as d:
        exe=Path(d)/'closed'
        subprocess.run([os.environ.get('CXX','c++'),'-std=c++20','-O3',str(Path(__file__).with_name('light_flats.cpp')),'-o',exe],check=True)
        rows=subprocess.run([str(exe)],input=raw,text=True,capture_output=True,check=True).stdout.splitlines()
    flats=[list(map(int,l.split()))for l in rows[:-1]];caps=list(map(int,rows[-1].split()))
    assert flats[-1]==[5,1364943,20] and caps==[16,16,16,12,17,16]
    assert all(2*v<sum(word[s])for s,v in zip(light,caps))
    probs=[Q(x,999993) for x in [0,191805,387630,610722,827177]]+[Q(1)]*4
    tariffs=[price(g) for g in range(9)]
    floors={s:[] for s in (1,2,3)}
    for weights,beta,eta in DUAL:
        W=dict(zip(range(2,6),map(Q,weights)));beta=Q(beta);eta=Q(eta)
        for o in range(1,9):
            for d in range(o):
                assert sum(w for r,w in W.items()if d<=r<o)**200<=(o-d)**199
                for a,inside in [(Q(0),False),(probs[o],True)]:
                    charge=1+sum(w for r,w in W.items() if r<o)+a*sum(w for r,w in W.items() if r>=o)
                    paid=charge-(eta*(1-a) if inside else 0)
                    assert paid<=0 or paid**200<=(o-min(d,1))**199
        for s in range(1,6):
            for a in range(s):
                demand=probs[a]*sum(w for r,w in W.items()if r>=s)
                assert demand**200<=(s-a)**199
                premium=tariffs[a][0]+tariffs[s-a][0]+tariffs[7-s][0]-tariffs[7][1]
                assert demand<=beta+premium
        for s in floors:floors[s].append(9*sum(W.values())+9+s+8-8*beta-s*eta)
    decisions=[max(floors[s])for s in (1,2,3)]
    assert list(map(str,decisions))==['3441641/100000','326223/10000','1555569/50000']
    assert [int(v-room)for v in decisions]==[3,1,0]
    result={'real_flats_by_rank':flats,'six_small_binary_masks':light,'weights':[sum(word[s])for s in light],
            'max_weights_on_one_real_five_flat':caps,'two_flat_support_contradictions':6,
            'scalar_surplus_1_2_3_pre_destination_floors':list(map(str,decisions)),'unconditionally_tolerated_destination_excess_ranks':[3,1,0]}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS 1364943 real rank-five flats, small supports and positive-slack chronology prices')

if __name__=='__main__':
    main()
