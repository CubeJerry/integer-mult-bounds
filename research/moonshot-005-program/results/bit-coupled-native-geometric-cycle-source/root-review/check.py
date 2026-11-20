#!/usr/bin/env python3
"""Verify all eight alternate-triangle certificates with the separate C engine.

This checks sufficient obstruction certificates, not the B search or its
additional exhaustive pair histogram. No author constructor or B rank code
is imported. The reviewed C arithmetic uses different field and pivots.
"""
import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path
import numpy as np

def need(x,s):
    if not x:raise ValueError(s)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    base=a.repo/'research/moonshot-005-program/results';p=Path(__file__).resolve().parents[1];pins=json.loads((p/'root-review/PINS.json').read_text())
    for name,h in pins.items():need(hashlib.sha256((a.repo/name).read_bytes()).hexdigest()==h,'bound source '+name)
    spec=importlib.util.spec_from_file_location('cycle_independent_C',p/'review-c/check.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=C.roots_from_files(L,B)
    H=[set(P)for P in L['A2']];adj=[{j for j,y in enumerate(roots)if j!=i and not C.b(x,y)}for i,x in enumerate(roots)];stars=[[h for h,P in enumerate(H)if j in P]for j in range(120)]
    singletons={next(iter(P&set(range(111))))for P in H if len(P&set(range(111)))==1};eligible=set(range(111))-singletons-{10};need(len(eligible)==99,'ordinary source scope')
    raw=json.loads((p/'component/output/COEFFICIENTS.json').read_text());arrays={int(j):{int(h):np.array(F,dtype=np.uint8)for h,F in rows.items()}for j,rows in raw.items()}
    cert=json.loads((p/'anchor-screen-b/output/RESULT.json').read_text());need(cert['standalone_component_obstructed_anchors']==sorted(arrays),'all eight certificate anchors')
    def point(centre,donor,plane):
        u,v=(roots[j]for j in sorted(H[centre])[:2]);images={roots[k]^(u if C.b(roots[k],v)else 0)^(v if C.b(roots[k],u)else 0)for k in H[plane]-{donor}}
        need(len(images)==1,'literal unique projected point');return images.pop()
    out=[];total=0;kernel_count=0
    for record in cert['results']:
        w=record['component_obstruction_witness'];j=w['anchor'];left,right=w['leaf_donors'];h1,h2,h3=w['centres'];i=w['final_receiver'];maps=arrays[j]
        need(j==record['anchor']and {j,left,right}<=eligible and len({j,left,right})==3,'ordinary distinct roles')
        need(len({h1,h2,h3})==3 and {j,left}<=H[h1]and {j,right}<=H[h2]and {left,right}<=H[h3],'actual native triangle')
        need(i<111 and i!=80 and H[h3]<=adj[i]and j not in adj[i],'exact final receiver and identity-target guards')
        sets=[];kernels={};counts=[]
        for branch,(centre,leaf)in zip(w['propagations'],[(h1,left),(h2,right)]):
            need((branch['centre'],branch['leaf'])==(centre,leaf),'branch binding')
            leafplanes=sorted(Q for Q in stars[leaf]if Q!=h3 and H[Q]<=adj[i]);need(len(leafplanes)==15,'fifteen actual final off-H3 observations')
            transported=[]
            for prop in branch['quotient_propagations']:
                R,Q=prop['anchor_plane'],prop['leaf_plane'];need(Q in leafplanes and R in maps and R!=centre and Q!=centre,'actual source planes')
                need(point(centre,j,R)==point(centre,leaf,Q),'orthogonal point transport')
                receivers=prop['receivers'];expected=[r for r in range(111)if r!=80 and H[centre]<=adj[r]and H[R]<=adj[r]and H[Q]<=adj[r]]
                need(receivers==expected,'complete literal propagation receiver set')
                block=[]
                for r in receivers:
                    key=centre,r
                    if key not in kernels:
                        visible=[h for h in maps if H[h]<=adj[r]];need(len(visible)==16 and centre in visible,'actual complete source view')
                        off=np.vstack([maps[h]for h in visible if h!=centre]);K=C.null(off)
                        need(K.shape==(48,3)and C.rank(C.mm(maps[centre],K))==3,'whole off-H inverse fibre')
                        kernels[key]=K;kernel_count+=1
                    K=kernels[key];need(not np.any(C.mm(maps[R],K)),'span contained in required R kernel');block.append(K)
                rank=C.rank(np.hstack(block));need(rank==prop['rank']==45,'sufficient full propagation rank');total+=1;transported.append(R)
            need(len(transported)==len(set(transported))==15 and sorted(v['leaf_plane']for v in branch['quotient_propagations'])==leafplanes,'all fifteen quotient propagations')
            sets.append(transported);counts.append(len(branch['quotient_propagations']))
        need(sets==w['distinct_anchor_plane_sets']and len(set(sets[0])&set(sets[1]))==10,'two transported plane sets')
        union=set(sets[0])|set(sets[1]);need(len(union)==20,'twenty-plane union');rank=C.rank(np.vstack([maps[h]for h in sorted(union)]));need(rank==w['final_union_rank']==48>45,'final common-fibre contradiction')
        out.append({'anchor':j,'leaves':[left,right],'centres':[h1,h2,h3],'final_receiver':i,'propagations':sum(counts),'final_union_rank':rank})
    need(total==240 and len(out)==8,'complete certificate inventory')
    result={'status':'PASS_INDEPENDENT_CYCLE_ALTERNATE_TRIANGLES','standalone_anchors':8,'propagation_certificates':total,'distinct_checked_inverse_fibres':kernel_count,'triangles':out,'independent_full_pair_census_claimed':False,'arbitrary_full_bank_component_mixing_excluded':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],8,total,flush=True)
if __name__=='__main__':main()
