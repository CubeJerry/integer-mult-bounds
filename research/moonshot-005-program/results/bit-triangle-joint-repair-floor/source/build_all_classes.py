#!/usr/bin/env python3
"""Extend the discovered source cycle to all five actual port classes."""
import gzip
import argparse
import hashlib
import itertools
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
from field import inv,mm,mul,power,rank

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=pathlib.Path,required=True)
    ap.add_argument('--nine-author',type=pathlib.Path,required=True)
    args=ap.parse_args()
    repo=args.repo
    raw=gzip.decompress((repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    layout=json.loads(raw)
    R=layout['root_table'];A=list(map(set,layout['A2']));D=list(map(set,layout['D4']))
    O=[{j for j,s in enumerate(R)if sum(a*b for a,b in zip(r,s))==0}for r in R]
    part_raw=gzip.decompress((args.nine_author/'output/PARTITIONS.json.gz').read_bytes())
    partitions=json.loads(part_raw)['classes']
    base=json.loads(gzip.decompress((HERE/'output/SOURCE-CERTIFICATE.json.gz').read_bytes()))
    donors=base['donors'];receivers=base['receivers'];cycle=base['cycle_planes']
    block={(i,h):k for i,h,k in base['blocks']}
    original={(j,h):m for j,h,m in base['source_maps']}
    visible={(i,j):hs for i,j,hs in base['visible']}
    v9=[[power(a,j)for j in range(9)]for a in range(1,10)]
    identity=[[int(i==j)for j in range(48)]for i in range(48)]
    def local(i,h,j,cl):
        ports=partitions[str(h)][cl]
        rows=[k for k,d in enumerate(ports)if D[d]<=O[i]]
        dj=sorted(A[h]).index(j)
        assert len(rows)==3
        return [[v9[r][k]for k in range(3*dj,3*dj+3)]for r in rows]
    all_maps={};stack_ranks=[];commutators=[];common_lifts=0;decoder_identities=0
    for cl in range(5):
        maps={}
        for (j,h),old in original.items():
            if h not in cycle:
                maps[j,h]=old
            else:
                f=[[0]*48 for _ in range(3)]
                for i in receivers:
                    m=inv(local(i,h,j,cl));k=block[i,h]
                    for r in range(3):f[r][3*k:3*k+3]=m[r]
                maps[j,h]=f
        for (j,h),m in maps.items():
            assert rank(m)==3
            all_maps[cl,j,h]=m
        for i in receivers:
            for j in donors:
                hs=visible[i,j]
                matrix=sum((maps[j,h]for h in hs),[])
                im=inv(matrix)
                assert mm(im,matrix)==identity
                decoded=[[0]*48 for _ in range(48)]
                for t,h in enumerate(hs):
                    if h in cycle:
                        lift=[[im[r][3*t+c]for c in range(3)]for r in range(48)]
                        expected=[[0]*3 for _ in range(48)]
                        localmap=local(i,h,j,cl)
                        for r in range(3):expected[3*block[i,h]+r]=localmap[r]
                        assert lift==expected
                        common_lifts+=1
                        term=mm(expected,maps[j,h])
                    else:
                        lift=[[im[r][3*t+c]for c in range(3)]for r in range(48)]
                        term=mm(lift,maps[j,h])
                    for r in range(48):
                        for c in range(48):decoded[r][c]^=term[r][c]
                assert decoded==identity
                decoder_identities+=1
        for h in cycle:
            j,k=[j for j in donors if(j,h)in maps]
            stack_ranks.append([cl,h,rank(maps[j,h]+maps[k,h])])
            transitions=[]
            for i in receivers:
                b=block[i,h]
                transitions.append(mm([r[3*b:3*b+3]for r in maps[j,h]],inv([r[3*b:3*b+3]for r in maps[k,h]])))
            aa,bb=mm(transitions[0],transitions[1]),mm(transitions[1],transitions[0])
            commutators.append([cl,h,rank([[x^y for x,y in zip(r,s)]for r,s in zip(aa,bb)])])
    out=HERE/'output'
    cert={
        'layout_sha256':hashlib.sha256(raw).hexdigest(),
        'partition_sha256':hashlib.sha256(part_raw).hexdigest(),
        'donors':donors,'receivers':receivers,'cycle_planes':cycle,
        'blocks':base['blocks'],'visible':base['visible'],
        'classes':5,'base_source_dimension_per_class':48,
        'source_maps':[[cl,j,h,m]for (cl,j,h),m in sorted(all_maps.items())],
    }
    cert_raw=json.dumps(cert,sort_keys=True,separators=(',',':')).encode()
    (out/'ALL-CLASSES-SOURCE.json.gz').write_bytes(gzip.compress(cert_raw,mtime=0))
    result={
        'status':'PASS_NATIVE_TRIANGLE_ALL_FIVE_SOURCE_CLASSES',
        'source_certificate_sha256':hashlib.sha256(cert_raw).hexdigest(),
        'source_maps':len(all_maps),'common_lift_identities':common_lifts,
        'visible_port_decoder_block_identities':decoder_identities,
        'stacked_source_ranks':stack_ranks,'transition_commutator_ranks':commutators,
        'balanced_early_quota_assignment_in_this_certificate':False,
        'proper_downstream_transport_constructed':False,
        'all_111_original_donors_glued':False,
        'complete_kappa':False,
    }
    (out/'ALL-CLASSES-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
