#!/usr/bin/env python3
"""Independent source-deletion and block-distance premises for strict capacity."""
import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import itertools
import json
from pathlib import Path

def need(c,m):
    if not c:raise ValueError(m)

def basis(rows):
    p={}
    for r in rows:
        while r:
            j=r.bit_length()-1
            if j in p:r^=p[j]
            else:p[j]=r;break
    return list(p.values())

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    source=a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
    raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','source pin')
    n=json.loads(gzip.decompress(raw));roots=[list(map(Fraction,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
    dot=lambda x,y:sum(u*v for u,v in zip(x,y))
    K=[sum(int(i==j or dot(x,y)==0)<<j for j,y in enumerate(roots)) for i,x in enumerate(roots)]
    programme=a.repo/'research/moonshot-005-program';certificate=programme/'results/bit-fitting-rigidity/global/CERTIFICATE.json';cert=json.loads(certificate.read_text())
    proof=programme/'results/bit-saturated-star-rigidity/author/PROOF.md'
    factors=cert['canonical_factor_rows_9bit']
    need(all(((factors[i]&factors[j]).bit_count()%2)==(K[i]>>j&1) for i in range(111) for j in range(111)),'all canonical factor products source-bound')
    retained=[i for i in range(111) if i not in (15,54,84,92)]
    F=cert['identity_frame_roles'];seed=set(cert['seed_roles']);edges=cert['sparse_edge_roles']
    need(len(F)==8 and len(seed)==35 and seed<=set(retained),'entire seed retained')
    need(all(factors[i]==1<<c for c,i in enumerate(F)),'frame normalization')
    need(set(F)|{e['role'] for e in edges}==seed and len(edges)==27,'exact sparse seed roles')
    endpoint_pairs={tuple(e['endpoints']) for e in edges}
    need(endpoint_pairs==set(itertools.combinations(range(8),2))-{(0,4)},'K8 minus one seed graph')
    need(min(Counter(v for e in endpoint_pairs for v in e).values())>=6,'saturated-star degree hypothesis')
    for e in edges:
        u,v=e['endpoints'];need(factors[e['role']]==(1<<u)|(1<<v)|(1<<8),'canonical sparse edge vector')
    anchors={entry['role']:entry['eight_noncontact_seed_roles'] for entry in cert['extension_anchors']}
    extension=[]
    for i in retained:
        if i in seed:continue
        A=anchors[i]
        need(len(A)==len(set(A))==8 and set(A)<=seed,'eight retained seed anchors')
        need(all(not(K[i]>>j&1) for j in A),'actual noncontact anchor equations')
        need(len(basis([factors[j] for j in A]))==8,'anchor rank eight')
        need((factors[i]&factors[i]).bit_count()%2==1,'own diagonal normalization')
        extension.append(i)
    need(len(extension)==72,'all retained extensions')
    first=anchors[extension[0]];need(len(basis([factors[j] for j in first[:-1]]))==7,'missing-anchor negative control')
    code=basis([sum(((K[i]>>j)&1)<<c for c,j in enumerate(retained)) for i in retained]);need(len(code)==9,'restricted canonical dimension nine')
    words=[0]
    for row in code:words += [w^row for w in words]
    need(len(words)==len(set(words))==512,'all binary canonical words')
    histogram=Counter(w.bit_count() for w in words if w);distance=min(histogram)
    need(distance==46,'restricted canonical distance46')
    ell=sum((((K[92]&K[54])>>j)&1)<<c for c,j in enumerate(retained));need(ell.bit_count()==32 and ell not in words,'sparse retained mode outside canonical code')
    witness=next(w for w in words if w.bit_count()==46)
    parity_path=programme/'results/bit-minimum-rank-nine/CERTIFICATE.json'
    parity=json.loads(parity_path.read_text());frames=parity['frames_pairwise_REAL_NONorthogonal'];counts=Counter(i for F in frames for i in F)
    need(len(frames)==9 and len(counts)==26 and set(counts)<=set(retained) and all(v%2==0 for v in counts.values()),'original odd-frame witness survives fourth deletion')
    need(all(len(set(F))==8 and all(dot(roots[i],roots[j])!=0 for i,j in itertools.combinations(F,2)) for F in frames),'all parity frames exact')
    out=dict(status='PASS_INDEPENDENT_POINT_PUNCTURE_STRICT_CAPACITY',source_sha256=hashlib.sha256(raw).hexdigest(),rigidity_certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest(),saturated_star_proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),retained_roles=retained,seed_roles=sorted(seed),seed_edges=27,extension_roles=extension,canonical_dimension=9,minimum_block_distance=distance,nonzero_binary_weight_histogram=dict(sorted(histogram.items())),distance_witness=[retained[j] for j in range(len(retained)) if witness>>j&1],retained_mode_support=[retained[j] for j in range(len(retained)) if ell>>j&1],retained_mode_weight=32,negative_missing_anchor_rank=7,review='REVIEW.md',future_capacity='strictly greater than8V',whole_width_future_transfer_events_at_least=9,new_complete_kappa=False)
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('retained_roles','seed_roles','extension_roles','distance_witness','retained_mode_support')}))

if __name__=='__main__':main()
