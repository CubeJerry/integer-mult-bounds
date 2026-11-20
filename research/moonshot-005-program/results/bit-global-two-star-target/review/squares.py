#!/usr/bin/env python3
"""Actual noncentral invariant fibre excludes every canonical four-cycle on untouched source branches."""
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json,sys
from pathlib import Path
import numpy as np
from check import mod,req
def main(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','gf');geo=mod(root/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);h=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','price');ar=mod(a.arithmetic,'gfop').Arithmetic(a.library,f,h);pr=mod(a.previous,'targets');terms=pr.target_blocks(root);_,_,lane=pr.coords()
    adj=[set(geo.adj[i])&set(range(111)) for i in range(111)];J=sorted(set(range(111))-adj[80]-{10});I=sorted(set(range(111))-adj[10]-{80});req(len(I)==49 and len(J)==48,'true free endpoints after full two-star assignment')
    rim=np.load(a.rim,mmap_mode='r');req(sha256(rim).hexdigest()==json.loads(a.receipt.read_bytes())['rim_global_original_sha256'],'real numerical one-copy rim')
    z=np.load(a.functional);vs=pr.rand('native virigin unframed holonomy witness',(480,1));native=defaultdict(dict);inverse={};count=0;tested_roles=sorted(set(range(111))-{80});R={};outputs={}
    for j in J:
        tap=np.load(a.taps/f'T{j}.npz');req(all(not('H-0-'+str(e))in tap for e in range(1,8)),'no free source moves a noncentral input into the center')
    for i in tested_roles:
        if f'A-{i}' in z:req(all(f'Q-{i}-{e}'not in z for e in range(1,8)),'true facet early correction has no rim-to-center action')
        nj=sorted(adj[i].intersection(J));R[i]={j:rim[480*i:480*(i+1),480*j:480*(j+1)]for j in nj};req(not any((i,j)in terms for j in nj),'all tested unassigned proper transfers are canonical')
        outputs[i]={j:ar.mm(r,vs)[:,0]for j,r in R[i].items()};table=np.stack([outputs[i][j]for j in nj],axis=1)
        for row,j in enumerate(nj):
            iv=ar.reduce(R[i][j],True)[0];images=ar.mm(iv,table);req(np.array_equal(images[:,row],vs[:,0]),'physical inverse restores the complete test on its own branch')
            for q,k in enumerate(nj):
                if j==k:continue
                if j<k:native[j,k][i]=images[:,q].tobytes()
                if a.six and i in I:inverse[i,j,k]=images[:,q].copy()
            count+=1
    rectangles=corect=0;digest=sha256()
    for edge,vals in sorted(native.items()):
        req(len(set(vals.values()))==len(vals),'actual four-cycle monodromy nonidentity on an original field vector')
        rectangles+=len(vals)*(len(vals)-1)//2;nu=sum(i in I for i in vals);corect+=nu*(nu-1)//2
        for i,v in sorted(vals.items()):digest.update(bytes([*edge,i]));digest.update(v)
    def upper(n,m):
        e=0
        for k in range(n*m+1):
            q,r=divmod(k,n);cost=(n-r)*q*(q-1)//2+r*q*(q+1)//2
            if cost>m*(m-1)//2:break
            e=k
        return e
    free_bound=min(upper(len(I),len(J)),upper(len(J),len(I)));allbound=min(upper(110,len(J)),upper(len(J),110))
    res={'all_real_canonical_free_donor_edges':count,'true_canonical_rectangles_excluded':rectangles,'free_donor_and_free_receiver_rectangles_excluded':corect,'maximum_full_canonical_edges_on_49_by_48_free_endpoints':free_bound,'maximum_full_canonical_edges_on_110_by_48_unrestricted_receivers':allbound,'digest_of_real_original_transport_tests':digest.hexdigest(),'arbitrary_separate_endpoint_bijections':True,'target_specific_fixed_native_bilateral_precursor':True,'new_complete_kappa':False}
    if a.six:
        hashes=sha256();pairs=0;paths=0
        for i in I:
            njs=list(R[i]);rec=defaultdict(dict)
            for j in njs:
                plist=[(u,k,v) for (u,jj,k),v in inverse.items() if jj==j and u!=i]
                if not plist:continue
                X=ar.mm(R[i][j],np.stack([v for u,k,v in plist],axis=1))
                for m,(u,k,v)in enumerate(plist):
                    val=X[:,m].tobytes();prev=rec[k]
                    req(val not in prev,'six-edge route collisions on virgin native field bank')
                    prev[val]=[u,j];hashes.update(bytes([i,k,u,j]));hashes.update(val);paths+=1
            for k,vals in rec.items():
                pairs+=len(vals)*(len(vals)-1)//2
                if k in outputs[i]:req(outputs[i][k].tobytes() not in vals,'no length-three map agrees with a direct proper map')
        res['three_hop_simple_native_transports']=paths;res['same_endpoints_distinct_path_pairs_separated']=pairs;res['six_edge_transport_sha256']=hashes.hexdigest()
    a.out.mkdir(parents=True,exist_ok=True);(a.out/('GIRTH-EIGHT.json' if a.six else 'GIRTH-SIX.json')).write_text(json.dumps(res,sort_keys=True,indent=2)+'\n');print(res,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','arithmetic','library','previous','rim','receipt','functional','taps','out'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--six',action='store_true');main(p.parse_args())
