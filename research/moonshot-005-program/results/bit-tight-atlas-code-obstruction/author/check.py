#!/usr/bin/env python3
"""Check the interpolation obstruction directly from the 111 signed root lines."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from collections import Counter
from itertools import combinations
from pathlib import Path

P = Path('research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json')
PIN = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def require(test, message):
    if not test:
        raise ValueError(message)


def dot(u,v):
    return sum(a*b for a,b in zip(u,v))


def positive(v):
    return v if next(x for x in v if x)>0 else tuple(-x for x in v)


def atlas(native):
    original = list(map(tuple,native))
    require(all(positive(v)==v and dot(v,v)==4 for v in original), 'integral norm-four source')
    lines = set(original)
    while True:
        added = set()
        for v,w in combinations(lines,2):
            inner=dot(v,w)
            if abs(inner)==2:
                added.add(positive(tuple(a-(inner//2)*b for a,b in zip(v,w))))
        if added<=lines:
            break
        lines.update(added)
        require(len(lines)<=120,'finite reflection closure')
    roots = original+sorted(lines-set(original))
    require(len(roots)==120,'parent root system')
    ids = {v:i for i,v in enumerate(roots)}
    planes = set()
    for j,k in combinations(range(120),2):
        a,b=roots[j],roots[k]
        inner=dot(a,b)
        if abs(inner)==2:
            ell=ids[positive(tuple(x-(inner//2)*y for x,y in zip(a,b)))]
            planes.add(tuple(sorted((j,k,ell))))
    planes=sorted(planes,key=lambda h:sum(1<<j for j in h))
    perp=[{i for i in range(111) if all(dot(roots[i],roots[j])==0 for j in h)} for h in planes]
    N=[{i for i in range(111) if dot(roots[i],r)==0} for r in roots[:111]]
    star=[[q for q,h in enumerate(planes) if j in h] for j in range(111)]
    require(len(planes)==1120 and all(len(p)==28 for p in star),'parent pencils')
    require(all(sum(i in perp[q] for q in star[j])==16 for j in range(111) for i in N[j]),'16-evaluation cuts')
    active=[q for q,h in enumerate(planes) if h[0]<111]
    counts=Counter(len(perp[q]&N[j]) for q in active for j in range(111))
    require(len(active)==1119 and min(counts)>0,'every plane and donor have a common native perpendicular')
    return roots,planes,perp,N,star,active,counts


def closures(roots):
    with tempfile.TemporaryDirectory() as d:
        exe=Path(d)/'closure'
        subprocess.run([os.environ.get('CXX','c++'),'-O3','-std=c++20',str(Path(__file__).with_name('closure.cpp')),'-o',str(exe)],check=True)
        run=subprocess.run([str(exe)],input=''.join(' '.join(map(str,r))+'\n' for r in roots[:111]),text=True,capture_output=True,check=True)
    rows=[list(map(int,line.split()))for line in run.stdout.splitlines()]
    require(len(rows)==111 and all(i==r[0] and r[1]==r[2] and r[4]==0 for i,r in enumerate(rows)),'two-seed propagation')
    require(sum(r[1]*(r[1]-1)//2 for r in rows)==185428 and max(r[3] for r in rows)==3,'enumeration controls')
    return rows


def checked_source(repo):
    raw=(repo/P).read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,'native input pin')
    return json.loads(raw)['native_roots']


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repo',required=True,type=Path)
    cli.add_argument('--out',required=True,type=Path)
    args=cli.parse_args()
    roots,planes,perp,N,star,active,counts=atlas(checked_source(args.repo))
    rows=closures(roots)
    d=min(map(len,N))
    min_cover=(111+2)//3
    large_upper=(len(active)-28*min_cover)//(d-min_cover)
    small_lower=28-large_upper
    require(d==55 and min_cover==37 and small_lower==24 and small_lower>16,'palette contradiction')
    result={'native_sha256':PIN,'parent_lines':len(roots),'planes':len(planes),'active_planes':len(active),
            'foreign_pairs':sum(map(len,N)),'active_plane_and_donor_common_normal_count_distribution':dict(sorted(counts.items())),
            'minimum_native_degree':d,'two_seed_tests':185428,'worst_closure_rounds':3,'closure_failures':0,
            'checks_by_receiver_degree_min_closure_max_rounds_failures':rows,'global_colors_if_feasible':28,
            'minimum_planes_per_color':min_cover,'max_colors_with_at_least_55_planes':large_upper,
            'minimum_colors_forced_into_every_16_element_receiver_palette':small_lower}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS geometry, 185428 two-seed closures, at least 24 colors required at a size-16 receiver')


if __name__=='__main__':
    main()
