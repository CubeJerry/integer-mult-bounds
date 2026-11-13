#!/usr/bin/env python3
"""Independent source/parity review; no author verifier or root helper import."""
import argparse, collections, gzip, hashlib, json
from pathlib import Path

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(ok, message):
    if not ok:raise ValueError(message)

def inner(normal_a, normal_b):
    # Closed integer inner products in the sum-zero nine-coordinate E8 model.
    # This uses set intersections, independently of the author's root arrays.
    a={j for j in range(9) if normal_a>>j&1}
    b={j for j in range(9) if normal_b>>j&1}
    need(len(a) in (3,7) and len(b) in (3,7), 'Source root weights')
    if len(a)==len(b)==3:return 9*(len(a&b)-1)
    if len(a)==7 and len(b)==3:return inner(normal_b,normal_a)
    if len(a)==3:
        p,q=sorted(set(range(9))-b)
        return 9*(int(p in a)-int(q in a))
    p,q=sorted(set(range(9))-a);r,s=sorted(set(range(9))-b)
    return 9*(int(p==r)-int(p==s)-int(q==r)+int(q==s))

def main(a):
    raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'Native pin')
    src=json.loads(gzip.decompress(raw))
    H={src['live'][i] for i in src['hosted']['Dports']}
    normals={h:src['frames'][src['initial'][h]][0] for h in H}
    cert=json.loads(a.certificate.read_text());frames=cert['frames_by_native_role']
    def check(fs):
        if len(fs)%2==0:return False
        counts=collections.Counter()
        for f in fs:
            if len(f)!=8 or len(set(f))!=8 or not set(f)<=H:return False
            if any(inner(normals[i],normals[j])!=18*(i==j) for i in f for j in f):return False
            counts.update(f)
        return all(v%2==0 for v in counts.values())
    need(check(frames),'Actual odd orthoframe parity certificate')
    need(len(frames)==9,'Nine frames')
    counts=collections.Counter(h for f in frames for h in f)
    need(collections.Counter(counts.values())=={2:32,4:2},'Independent multiplicity census')
    need([[normals[h] for h in f] for f in frames]==cert['frames_by_binary_normal'],'Role/normal binding')
    need(not check(frames[:-1]),'Removed frame negative control')
    damaged=[f[:] for f in frames];damaged[0][0]=damaged[0][1]
    need(not check(damaged),'Duplicate source control')
    nonorth=next(h for h in H-set(frames[0]) if any(inner(normals[h],normals[k]) for k in frames[0][1:]))
    damaged=[f[:] for f in frames];damaged[0][0]=nonorth
    need(not check(damaged),'Hosted nonorthogonal replacement control')
    out={'status':'PASS_INDEPENDENT_CHAR2_PARITY_SOURCE_REVIEW','source_sha256':PIN,
         'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),
         'source_roles':len(H),'frames':len(frames),'integer_inner_product_checks':sum(len(f)**2 for f in frames),
         'multiplicity_histogram':dict(sorted(collections.Counter(counts.values()).items())),
         'negative_controls':{'even_number_after_deletion':True,'duplicate_role':True,'hosted_nonorthogonal_replacement':True},
         'all_volume_theorem':'For every characteristic-two field and V>=1, rank(K)>=9V on the stated complex graph.',
         'scope':'Source/parity checks plus separately reviewed rank-factorization proof. Does not identify the actual111-port BIT graph with this graph.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
