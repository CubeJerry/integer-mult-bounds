"""Independent closed-form enumeration of literal small half subsets."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import itertools
import json
from review_half_sum_gate import independent_rows

HERE=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs',type=Path,default=HERE,help='Directory containing SOURCE-RECOVERY.json')
    ap.add_argument('--author-certificate',type=Path,default=HERE.parent/'R/small-half-extensions/output/CERTIFICATE.json')
    ap.add_argument('--out',type=Path,default=HERE/'small-half-review')
    args=ap.parse_args()
    source=args.inputs/'SOURCE-RECOVERY.json';raw=source.read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(raw)['native_roots'];N=[sum(1<<j for j,s in enumerate(roots)if sum(a*b for a,b in zip(r,s))==0)for r in roots]
    K=[v^(1<<i)for i,v in enumerate(N)];author_path=args.author_certificate;author=json.loads(author_path.read_text())
    assert author['native_sha256']==hashlib.sha256(raw).hexdigest()
    halves=[]
    for z in author['halves']:
        if isinstance(z,list):I=z
        else:I=z.get('roles',z.get('support'))
        assert I is not None
        H=sum(1<<i for i in I);halves.append(H)
        assert len(I)in(3,4)
        support={tuple(j for j,x in enumerate(roots[i])if x)for i in I};assert len(support)==1
        coords=next(iter(support));a,b=coords[:2]
        assert len({roots[i][a]==roots[i][b]for i in I})==1
        assert all(any(j!=i and not(N[i]>>j&1)for j in I)for i in I)
    assert len(halves)==28 and sum(h.bit_count()for h in halves)==103
    cover=0
    for H in halves:
        assert not cover&H
        cover|=H
    assert cover==sum(1<<i for i in range(8,111))
    deletions=[[H.bit_count()if H&~N[i]==0 else 0 for i in range(111)]for H in halves]
    degrees=[v.bit_count()for v in N];results=[]
    for k in range(5):
        histogram=Counter();best=223;witness=None
        for choice in itertools.combinations(range(28),k):
            degree=[degrees[i]-sum(deletions[j][i]for j in choice)for i in range(111)]
            charge=sum(int(d>36)+int(d>52)for d in degree);histogram[charge]+=1
            if charge<best:best,witness=charge,choice
        assert best==[222,219,207,197,189][k]
        ar=next(z for z in author['subset_results']if z['selected_count']==k)
        assert best==ar['minimum_charge'] and sum(histogram.values())==ar['number_of_subsets']
        assert dict(histogram)=={int(x):v for x,v in ar['charge_histogram'].items()}
        results.append({'selected_literal_half_count':k,'tested_subsets':sum(histogram.values()),'minimum_capped_charge':best,'one_minimizer':list(witness),'charge_histogram':dict(sorted(histogram.items()))})
    selected=[8,9,14,15,21];assert sum(halves[j].bit_count()for j in selected)<=17
    fit=[K[i]^sum(halves[j]for j in selected if halves[j]&~N[i]==0)for i in range(111)]
    full=(1<<111)-1;assert all(row&(full^N[i])==1<<i for i,row in enumerate(fit))
    charge=sum(int((row&N[i]).bit_count()>36)+int((row&N[i]).bit_count()>52)for i,row in enumerate(fit))
    assert charge==187 and len(independent_rows(fit))==14
    aw=author['five_half_witness']
    assert selected==aw['selected_halves'] and aw['union_support']==17
    assert charge==aw['charge'] and aw['code_rank']==aw['witness_matrix_rank']==14
    assert fit==[int(row,16)for row in aw['rows_hex']]
    out={'status':'PASS_INDEPENDENT_SMALL_LITERAL_HALF_ENUMERATION','author_certificate_sha256':hashlib.sha256(author_path.read_bytes()).hexdigest(),
         'results':results,'five_half_witness':{'halves':selected,'support_union_size':sum(halves[j].bit_count()for j in selected),'charge':187,'fitting_rank':14},
         'scope':'Exact literal chosen-subset screen for0..4 of the fixed28 disjoint pair-equality halves; five-half witness only. Not arbitrary coded combinations or a packet-count theorem.'}
    folder=args.out;folder.mkdir(parents=True,exist_ok=True);(folder/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'minima':[r['minimum_capped_charge']for r in results],'counts':[r['tested_subsets']for r in results],'witness':out['five_half_witness']}))


if __name__=='__main__':main()
