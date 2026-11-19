#!/usr/bin/env python3
"""Replay the five-class same-original-donor source cycle certificate."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
import pathlib
from field import inv,mm,mul,power,rank

LAYOUT='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
PARTITION='2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25'
CERTIFICATE='362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af'

def matching(adjacency):
    right={}
    def add(left,seen):
        for col in adjacency[left]:
            if col in seen:continue
            seen.add(col)
            if col not in right or add(right[col],seen):
                right[col]=left
                return True
        return False
    assert all(add(r,set())for r in range(len(adjacency)))
    assert len(right)==len(adjacency)
    return [[r,c]for c,r in sorted(right.items())]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=pathlib.Path,required=True)
    ap.add_argument('--nine-author',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    args=ap.parse_args()
    raw=gzip.decompress((args.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==LAYOUT
    atlas=json.loads(raw)
    roots=atlas['root_table'];planes=list(map(set,atlas['A2']));middle=list(map(set,atlas['D4']))
    ortho=[{j for j,s in enumerate(roots)if sum(x*y for x,y in zip(r,s))==0}for r in roots]
    part_raw=gzip.decompress((args.nine_author/'output/PARTITIONS.json.gz').read_bytes())
    assert hashlib.sha256(part_raw).hexdigest()==PARTITION
    parts=json.loads(part_raw)['classes']
    cert_raw=gzip.decompress((pathlib.Path(__file__).parent/'output/ALL-CLASSES-SOURCE.json.gz').read_bytes())
    assert hashlib.sha256(cert_raw).hexdigest()==CERTIFICATE
    cert=json.loads(cert_raw)
    donors=cert['donors'];receivers=cert['receivers'];cycle=cert['cycle_planes']
    assert donors==[29,36,77] and receivers==[10,33,80,95] and cycle==[249,339,791]
    assert cert['layout_sha256']==LAYOUT and cert['partition_sha256']==PARTITION
    assert cert['classes']==5 and cert['base_source_dimension_per_class']==48
    assert all(set(donors)<=ortho[i]for i in receivers)
    assert [sorted(planes[h])for h in cycle]==[[29,36,58],[29,70,77],[36,77,107]]
    actual_cycle=[h for h,p in enumerate(planes)if len(p&set(donors))>=2]
    assert actual_cycle==cycle
    for j,k in itertools.combinations(donors,2):assert k not in ortho[j]
    visible={(i,j):[h for h,p in enumerate(planes)if j in p and p<=ortho[i]]for i in receivers for j in donors}
    assert visible=={(i,j):hs for i,j,hs in cert['visible']}
    assert all(len(hs)==16 and all(max(planes[h])<111 for h in hs)for hs in visible.values())
    block={(i,h):k for i,h,k in cert['blocks']}
    assert sorted(block.values())==list(range(12))
    assert set(block)==set(itertools.product(receivers,cycle))
    source={(c,j,h):m for c,j,h,m in cert['source_maps']}
    assert len(source)==420
    assert all((c,j,h)in source for c in range(5)for j in donors for h,p in enumerate(planes)if j in p)
    assert all(len(m)==3 and all(len(r)==48 and all(0<=x<32 for x in r)for r in m) and rank(m)==3 for m in source.values())
    assert all(mul(x,power(x,30))==1 for x in range(1,32))
    v=[[power(a,j)for j in range(9)]for a in range(1,10)]
    def local(c,i,h,j):
        ports=parts[str(h)][c]
        rows=[r for r,d in enumerate(ports)if middle[d]<=ortho[i]]
        assert len(rows)==3
        jj=sorted(planes[h]).index(j)
        m=[[v[r][k]for k in range(3*jj,3*jj+3)]for r in rows]
        assert rank(m)==3
        return m
    scalar={};matchings=[]
    for j in donors:
        shared=[h for h in cycle if j in planes[h]]
        for h,p in enumerate(planes):
            if j not in p or h in shared:continue
            m=source[0,j,h];a=[]
            for k in range(16):
                b=[r[3*k:3*k+3]for r in m]
                assert all(b[r][s]==(b[0][0]if r==s else 0)for r in range(3)for s in range(3))
                a.append(b[0][0])
            scalar[j,h]=a
            assert all(source[c,j,h]==m for c in range(5))
            for i in receivers:
                if h in visible[i,j]:assert all(a[block[i,q]]==0 for q in shared)
        for i in receivers:
            hs=[h for h in visible[i,j]if h not in shared]
            cols=[k for k in range(16)if k not in {block[i,q]for q in shared}]
            mat=[[scalar[j,h][k]for k in cols]for h in hs]
            assert rank(mat)==14
            matchings.append({'donor':j,'receiver':i,'planes':hs,'columns':cols,'matching':matching([[k for k,x in enumerate(row)if x]for row in mat])})
    eye=[[int(r==s)for s in range(48)]for r in range(48)]
    common=0;identities=0;commutator_ranks=[];stacked=[]
    for c in range(5):
        for i in receivers:
            for j in donors:
                hs=visible[i,j]
                mat=sum((source[c,j,h]for h in hs),[])
                im=inv(mat)
                assert mm(im,mat)==eye
                decoded=[[0]*48 for _ in range(48)]
                for t,h in enumerate(hs):
                    lift=[[im[r][3*t+s]for s in range(3)]for r in range(48)]
                    if h in cycle:
                        expected=[[0]*3 for _ in range(48)]
                        a=local(c,i,h,j)
                        for r in range(3):expected[3*block[i,h]+r]=a[r]
                        assert lift==expected
                        common+=1
                    else:
                        a=local(c,i,h,j)
                        # Actual private output is a*f; using lift*a^-1
                        # recovers precisely this source-coordinate term.
                        assert mm(mm(lift,inv(a)),a)==lift
                    term=mm(lift,source[c,j,h])
                    for r in range(48):
                        for s in range(48):decoded[r][s]^=term[r][s]
                assert decoded==eye
                identities+=1
        for h in cycle:
            j,k=sorted(planes[h]&set(donors))
            assert rank(source[c,j,h]+source[c,k,h])==6
            stacked.append([c,h,6])
            trans=[]
            for i in receivers[:2]:
                b=block[i,h]
                trans.append(mm([r[3*b:3*b+3]for r in source[c,j,h]],inv([r[3*b:3*b+3]for r in source[c,k,h]])))
            aa,bb=mm(trans[0],trans[1]),mm(trans[1],trans[0])
            commutator_ranks.append([c,h,rank([[x^y for x,y in zip(r,s)]for r,s in zip(aa,bb)])])
    assert common==120 and identities==60
    assert sum(v>0 for c,h,v in commutator_ranks)==14
    result={
        'status':'PASS_NATIVE_TRIANGLE_ALL_FIVE_SOURCE_CLASSES',
        'layout_sha256':LAYOUT,'partition_sha256':PARTITION,'source_certificate_sha256':CERTIFICATE,
        'donors':donors,'receivers':receivers,'cycle_planes':cycle,
        'classes_glued':5,'base_dimension_per_original_donor_per_class':48,
        'base_dimension_per_original_donor_all_classes':240,
        'simultaneously_varying_base_input_dimensions':720,
        'rank_three_source_maps_checked':420,
        'source_scalar_completion_matching_checks':12,
        'common_lift_identities':common,'visible_port_decoder_block_identities':identities,
        'stacked_shared_source_ranks':stacked,
        'noncommuting_transition_pairs':14,'transition_commutator_ranks':commutator_ranks,
        'actual_balanced_early_quota_certificate_in_this_package':False,
        'proper_D_to_K_to_F_transport_constructed':False,
        'all_111_original_donors_glued':False,'complete_kappa':False,
    }
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'CHECK-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'PRIVATE-COMPLETION-MATCHINGS.json').write_text(json.dumps(matchings,indent=2)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
