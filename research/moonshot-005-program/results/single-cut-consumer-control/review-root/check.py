#!/usr/bin/env python3
"""Independent nine-coordinate geometry check of the scoped consumer control."""
import argparse,gzip,hashlib,json
from pathlib import Path
def need(ok,msg):
    if not ok:raise ValueError(msg)
def span(vs):
    s={0}
    for v in vs:s|={x^v for x in tuple(s)}
    return s
def main(a):
    raw=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','Native identity')
    s=json.loads(gzip.decompress(raw));B=[5,56,65,69,77,96,100,103];J=[0,7,20,27,36,46,57,111]
    H={s['live'][k]:(b,d) for k,b,d in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    def root(i):
        b=s['frames'][s['initial'][i]][0];v=[j for j in range(9) if b>>j&1]
        if len(v)==3:return [2 if j in v else -1 for j in range(9)]
        need(len(v)==7,'Root normal');p,q=[j for j in range(9) if j not in v]
        return [3*(int(j==p)-int(j==q)) for j in range(9)]
    for K in (B,J):
        need(all(sum(x*y for x,y in zip(root(i),root(j)))==18*int(i==j) for i in K for j in K),'Exact orthogonal basis')
    facets={i:span(s['frames'][s['final'][d]]) for i,(b,d) in H.items()};W=span(s['frames'][127])
    need(len(W)==512 and len({tuple(sorted(v)) for v in facets.values()})==96,'Hub and distinct native facets')
    pairs={(o[2],o[3]) for o in s['program'] if o[0]=='MOVE'}
    for i in B:
        b,d=H[i];need(s['final'][b]==127 and len(facets[i])==256 and facets[i]<W,'Actual endpoint and rank-one transport')
        need((s['final'][d],127) in pairs,'Inherited native chart pair')
        need(not any(facets[i]<=facets[j] for j in J),'Move starts outside disjoint chart downset')
    reviewed={f:hashlib.sha256((a.author/f).read_bytes()).hexdigest() for f in ['CONSUMER-CUT-CONTROL.md','consumer_cut_check.py','consumer_cut_check.json']}
    out={'status':'PASS_ROOT_SINGLE_CUT_GEOMETRY_REVIEW','basis':B,'disjoint_basis':J,'single_cut_price':8,
      'counterexample_class':'Authentic original b atHub and d atfacets; not the changed cyclic currentb state.',
      'reviewed_author_files':reviewed,'scope':'Exact scalar/vector macro and one-cut sharpness only. Full-family cuts and all native endpoint obligations remain open.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['repo','author','output']:p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
