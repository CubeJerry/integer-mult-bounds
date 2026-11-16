#!/usr/bin/env python3
"""Exact source support geometry and universal routing identities."""
from pathlib import Path
import itertools,json,hashlib

import argparse
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);source_repo=parser.parse_args().repo.resolve()
source_helper=Path(__file__).with_name('cyclic_quarter_search.py')
exec(compile(source_helper.read_text().split('bankperms=list(itertools.permutations(range(3)))')[0].replace("repo=Path('/workspace/scratch/5b84182f4f70/programme')",'repo=Path('+repr(str(source_repo))+')'),str(source_helper),'exec'))

# Every first-four source path has a different destination. An inserted
# diagonal unit can change path phases but cannot remove or cancel a path.
path_checks=[]
for length in range(1,5):
    row_counts=[0]*16
    for x in range(16):
        destinations=[]
        for flips in itertools.product([0,1],repeat=length):
            y=x
            for flip in flips:y=((y>>1)|((y&1)<<3))^(2*flip)
            destinations.append(y);row_counts[y]+=1
        assert len(destinations)==len(set(destinations))==2**length
    assert row_counts==[2**length]*16
    path_checks.append({'head_count':length,'column_support':2**length,'row_support':2**length,'all_paths_unique':True})

joint=[Ds[2].power(u)@Ds[4].power(v)for u in range(4)for v in range(4)]
joint_types={str(k):[kind(A.power(k)@d@A)for d in joint]for k in [1,2,3]}
assert all(joint_types[str(k)]==[k+1]*16 for k in [1,2,3])
clock_bounds=[]
for theta in range(4):
    hh=S.star()@Ds[2].power(theta)
    assert A@hh==C[2]@Ds[2].power(theta)
    for d in joint:
        g=A@hh@d@A
        assert max(sum(z!=(0,0)for z in row)for row in g.a)<=2
    clock_bounds.append({'theta':theta,'joint_samples':16,'maximum_row_support':2})
assert all(A@Ds[2].power(e)==Ds[1].power(e)@A for e in range(4))

# Exhaustive two-coordinate phase pair controls for an arbitrary diagonal
# root-four table inside C_b d C_b. The other bits are spectators.
pair_controls=[]
for u,v in itertools.product(range(4),repeat=2):
    d=m.monomial(list(range(16)),[u if not x&2 else v for x in range(16)])
    block=C[2]@d@C[2]
    supports=sorted({sum(z!=(0,0)for z in row)for row in block.a})
    assert max(supports)<=2;pair_controls.append({'phases':[u,v],'row_supports':supports})

# Free associative algebra: no commutation or numerical width is substituted
# for the exact block products used by the proof.
def atom(x):return {(x,):1}
oid={():1};oz={}
def plus(*polys):
    out={}
    for q in polys:
        for w,c in q.items():out[w]=out.get(w,0)+c
    return {w:c for w,c in out.items()if c}
def neg(q):return {w:-c for w,c in q.items()}
def times(*polys):
    out=oid
    for q in polys:
        nxt={}
        for u,c in out.items():
            for v,d in q.items():nxt[u+v]=nxt.get(u+v,0)+c*d
        out={w:c for w,c in nxt.items()if c}
    return out
def pmatrix_product(x,y):return [[plus(*(times(x[r][j],y[j][c])for j in range(3)))for c in range(3)]for r in range(3)]
def multiply(*matrices):
    out=matrices[0]
    for z in matrices[1:]:out=pmatrix_product(out,z)
    return out
a=atom('a');f=atom('f');h=atom('h');gg=plus(oid,neg(f));qs={(i,j):atom(f'q{i}{j}')for i in range(3)for j in range(3)}
ll=[[a,oz,oz],[oid,a,oz],[oz,oz,oid]]
uu=[[a,neg(times(a,a)),oz],[oz,a,oz],[oz,oz,oid]]
cc=[[oid,oz,oz],[oz,times(h,f),times(h,gg)],[oz,gg,f]]
qq=[[oz,oz,qs[0,2]],[qs[1,0],oz,oz],[qs[2,0],qs[2,1],qs[2,2]]]
ee=multiply(ll,cc,uu,qq,ll)
assert ee[0][0]==neg(times(a,a,a,qs[1,0],a))
assert ee[0][1]==oz and ee[0][2]==times(a,a,qs[0,2])
assert ee[2][0]==plus(times(gg,a,qs[1,0],a),times(f,qs[2,0],a),times(f,qs[2,1]))
assert ee[2][1]==times(f,qs[2,1],a)and ee[2][2]==times(f,qs[2,2])
def f_zero(poly):return {w:c for w,c in poly.items()if'f'not in w}
assert f_zero(ee[2][0])==times(a,qs[1,0],a)
assert f_zero(ee[2][1])==oz and f_zero(ee[2][2])==oz

# Before-routing clock: retain the complete generic routing column with its
# idle entry zero, and verify the highest-head-degree path without assuming
# commutativity of any coefficient.
rr=[[atom(f'r{i}{j}')if(i,j)!=(2,0)else oz for j in range(3)]for i in range(3)]
dh=[[oid,oz,oz],[oz,h,oz],[oz,oz,oid]]
fullq=[[qs[i,j]for j in range(3)]for i in range(3)]
before=multiply(ll,rr,dh,uu,fullq,ll)
highest=[[{w:c for w,c in z.items()if w.count('a')==4}for z in row]for row in before]
expected=[[oz for _ in range(3)]for _ in range(3)]
for r in [0,1]:
    for c in [0,1]:expected[r][c]=neg(times(a,rr[r][0],a,a,qs[1,c],a))
assert highest==expected

# A joint scalar unit alone does not guarantee that the rank4 row survives:
# a sector can route the entire second input row into the idle third column.
sector_counts={}
from math import comb as binomial
for width in [1,2,3,4]:
    c=[sum(binomial(width,k)for k in range(width+1)if k%4==s)for s in range(4)]
    counts=[[4**width*c[s]*c[t]for t in range(4)]for s in range(4)]
    assert sum(sum(row)for row in counts)==16**width
    sector_counts[str(width)]=counts
assert sector_counts['1'][3][3]==0 and sector_counts['2'][3][3]==0 and sector_counts['3'][3][3]>0
bad_sector=[[1,0,0],[0,0,1],[0,1,0]]
assert scalar_det(bad_sector)!=0 and bad_sector[1][0]==bad_sector[1][1]==0

repo=source_repo
paths=['research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md','research/moonshot-005-program/results/complex-four-bit-concentration/author/PROOF.md']
pins={p:hashlib.sha256((repo/p).read_bytes()).hexdigest()for p in paths if(repo/p).exists()}
result={'status':'PASS_SOURCE_TRANSPORTED_ROUTING_AND_SCOPED_OBSTRUCTION','baseline':'3057acc9311101cfedfcfacf7f68fb0866507871','scope':'Analytic obstruction for quarter-sector bank-permutation first interface followed by one active clock and arbitrary diagonal second algebra; exact constructive decoder for reversed first order. No actual independent421 caller.','unique_path_support_checks':path_checks,'joint_quarter_source_types':joint_types,'clock_support_bounds':clock_bounds,'all_phase_pair_controls':pair_controls,'universal_associative_block_formulas':True,'universal_highest_degree_path':True,'joint_sector_counts':sector_counts,'negative_control':'An invertible hidden scalar sector can have zero active row pair, destroying full rank4 at V>=3.','source_sha256':pins,'source_helper_sha256':hashlib.sha256(source_helper.read_bytes()).hexdigest()}
Path(__file__).with_name('SOURCE-TRANSPORT-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'unique_path_lengths':4,'exact_joint_source_words':48,'phase_pair_controls':16,'universal_block_identities':True},indent=2))
