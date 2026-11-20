#!/usr/bin/env python3
"""Independent column-rank and reverse-kernel audit of seventeen applications."""
from argparse import ArgumentParser
from collections import Counter
import ctypes
from functools import lru_cache
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import numpy as np

ANCHORS = {'all111': [26,32,66,95,100,103], 'chain': [0,25,45,47,61,62,100], 'hybrid': [0,25,47,100]}
PINS = {'SOURCE-PINS.json': 'edc58e710098d92375a3510a3d3695e7d29a216129403802b1a781f58dd9048f',
        'PROOF.md': 'c3e42329e36f08770602b1301348ad4cf4deb7eea7f740e576d1900dcd4e922f',
        'check.py': '0cb17b8a0a803128a818cacc02f0a9386437d165af6895fddb1e5a069bb56a14',
        'output/RESULT.json': '87d3aea2b5f10f6f58e46a9507eeeda147bef25b85745abcedbb89d352e969b3'}

def need(ok,message):
    if not ok:
        raise ValueError(message)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value

class IndependentField:
    def __init__(self,library,product):
        self.lib=ctypes.CDLL(str(library.resolve()))
        self.lib.gf_product_review.argtypes=[ctypes.c_int,ctypes.c_int]
        self.lib.gf_product_review.restype=ctypes.c_int
        self.lib.column_rank_review.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int]
        self.lib.column_rank_review.restype=ctypes.c_int
        self.lib.reverse_null_review.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_int]
        self.lib.reverse_null_review.restype=ctypes.c_int
        self.lib.product_review.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        need(all(self.lib.gf_product_review(a,b)==int(product[a,b]) for a in range(64) for b in range(64)),
             'independent bit-shift field table agrees on all scalar products')

    def rank(self,matrix):
        A=np.ascontiguousarray(matrix,dtype=np.uint8)
        return self.lib.column_rank_review(A.ctypes.data,*A.shape)

    def mm(self,left,right):
        A=np.ascontiguousarray(left,dtype=np.uint8);B=np.ascontiguousarray(right,dtype=np.uint8)
        need(A.shape[1]==B.shape[0],'independent product dimensions')
        out=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
        self.lib.product_review(A.ctypes.data,B.ctypes.data,out.ctypes.data,A.shape[0],A.shape[1],B.shape[1])
        return out

    def kernel(self,matrix,width):
        A=np.ascontiguousarray(matrix,dtype=np.uint8);K=np.zeros((A.shape[1],width),dtype=np.uint8)
        rank=self.lib.reverse_null_review(A.ctypes.data,*A.shape,K.ctypes.data,width)
        need(rank==A.shape[1]-width,'entire off-H kernel dimension by reverse elimination')
        need(self.rank(K)==width and not np.any(self.mm(A,K)),'independent complete nullspace residual and rank')
        return K

def source_arrays(repo,out):
    base=repo/'research/moonshot-005-program/results'
    chain_builder=load(base/'bit-coupled-native-three-chain-source/review-b/construct.py','pinned_independent_chain')
    chain=chain_builder.context(repo,out/'chain-constructor')
    hybrid_builder=load(base/'bit-coupled-native-three-chain-source/review-fibre-only-b/construct.py','pinned_independent_hybrid')
    hybrid=hybrid_builder.context(repo,out/'hybrid-constructor')
    prior=load(base/'bit-coupled-native-forty-h-source/review-all-donors-b/check.py','pinned_independent_all111')
    payload={}
    for key,(name,digest) in prior.PINS.items():
        raw=(base/name).read_bytes()
        if name.endswith('.gz'):
            raw=gzip.decompress(raw)
        need(sha256(raw).hexdigest()==digest,'all111 construction source pin '+key);payload[key]=raw
    geom=load(base/prior.PINS['coefficient_review'][0],'pinned_independent_pair_coefficients')
    parameters=json.loads(payload['parameters']); wanted=set(ANCHORS['all111']); arrays={}
    # Reconstruct the exact pair/single components containing the six anchors.
    # All other banks and their invoices were independently audited earlier.
    for record in parameters['pairs']:
        h,q=record['centres']
        if not wanted & (chain.H[h]|chain.H[q]):
            continue
        for width in (3,12):
            charts=[geom.Chart(chain.native,p,width) for p in (h,q)]
            maps=geom.paired(charts,record[str(width)])
            for j in wanted & set(maps):
                need((j,width) not in arrays,'one original all111 anchor array')
                arrays[j,width]=maps[j]
    for text,options in parameters['singles'].items():
        h=int(text)
        if not wanted & chain.H[h]:
            continue
        for width in (3,12):
            chart=geom.Chart(chain.native,h,width)
            maps=chart.single(options[str(width)])
            for j in wanted & set(maps):
                need((j,width) not in arrays,'one original singleton-component anchor array')
                arrays[j,width]=maps[j]
    need(set(arrays)=={(j,w) for j in wanted for w in (3,12)},'all twelve all111 anchor components reconstructed')
    return chain,{'all111':arrays,'chain':chain.maps,'hybrid':hybrid.maps}

def main():
    cli=ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();args.repo=args.repo.resolve();args.out.mkdir(parents=True,exist_ok=True)
    folder=Path(__file__).resolve().parents[1];base=args.repo/'research/moonshot-005-program/results'
    for name,digest in PINS.items():
        need(sha256((folder/name).read_bytes()).hexdigest()==digest,'frozen application source '+name)
    for name,item in json.loads((folder/'SOURCE-PINS.json').read_bytes())['files'].items():
        raw=(args.repo/name).read_bytes()
        need(len(raw)==item['bytes'] and sha256(raw).hexdigest()==item['sha256'],'application inherited source '+name)
    expected=json.loads((folder/'output/RESULT.json').read_bytes())
    ctx,arrays=source_arrays(args.repo,args.out)
    library=args.out/'review-linear64.so'
    subprocess.run(['c++','-O3','-std=c++17','-shared','-fPIC',str(Path(__file__).with_name('linear64.cpp')),'-o',str(library)],check=True)
    F=IndependentField(library,ctx.field.product)
    certificate=json.loads(gzip.decompress((base/'bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz').read_bytes()))['witnesses']
    records={row['anchor']:row for row in certificate}
    singleton={next(iter(H & set(range(111)))) for H in ctx.H if len(H & set(range(111)))==1}
    eligible=set(range(111))-singleton-{10}
    need(len(eligible)==99 and all(set(js)<=eligible for js in ANCHORS.values()),'all tested anchors are ordinary and nonexceptional')
    all_results={};receiver_counts=Counter();kernel_counts=Counter();source_hashes={}
    for label,anchors in ANCHORS.items():
        published={row['anchor']:row for row in expected['results'][label]};out_rows=[]
        for j in anchors:
            record=records[j];left,right=record['leaf_donors'];h1,h2,h3=record['centres'];i=record['final_receiver']
            need(left in eligible and right in eligible and len({j,left,right})==3,'all triangle source roles ordinary')
            need({j,left}<=ctx.H[h1] and {j,right}<=ctx.H[h2] and {left,right}<=ctx.H[h3],'actual triangle incidences')
            need(i<111 and i!=80 and ctx.H[h3]<=ctx.perp[i] and j not in ctx.perp[i],'actual final identity receiver')
            propagations=[];mapped=[]
            for branch,leaf,h in zip(record['propagations'],[left,right],[h1,h2]):
                need(branch['leaf']==leaf and branch['centre']==h,'actual propagation edge')
                qs=set(ctx.views[leaf,i])-{h3};found=[];used=set()
                need(len(qs)==15 and h not in qs and len(branch['quotient_propagations'])==15,'complete fifteen final quotients')
                for entry in branch['quotient_propagations']:
                    Q=entry['leaf_plane'];R=entry['anchor_plane']
                    need(Q in qs and Q not in used and Q!=h and R!=h and R in ctx.stars[j],'actual off-H source pair')
                    required=ctx.H[h]|ctx.H[Q]|ctx.H[R]
                    receivers=[r for r in range(111) if r!=80 and required<=ctx.perp[r]]
                    need(set(entry['receivers'])<=set(receivers),'full native receiver family contains admitted original witnesses')
                    propagations.append({'centre':h,'leaf':leaf,'leaf_plane':Q,'anchor_plane':R,'receivers':receivers})
                    receiver_counts[len(receivers)]+=1;used.add(Q);found.append(R)
                need(used==qs and len(set(found))==15,'one propagation for every final quotient')
                mapped.append(found)
            need(mapped==record['distinct_anchor_plane_sets'] and len(propagations)==30,'exact original triangle and thirty conditions')
            components={};union=sorted(set(mapped[0])|set(mapped[1]))
            need(len(union)==20 and len(set(mapped[0])&set(mapped[1]))==10,'actual twenty-plane final union')
            for width in (3,12):
                maps=arrays[label][j,width]
                need(set(maps)==set(ctx.stars[j]) and all(A.shape==(width,16*width) for A in maps.values()),'literal complete source array dimensions')
                source_hash=sha256(b''.join(maps[q].tobytes() for q in sorted(maps))).hexdigest()
                need(source_hash==published[j]['components'][str(width)]['source_coefficient_sha256'],'pinned frozen application source coefficients')
                source_hashes[f'{label}/{j}/{width}']=source_hash
                cache={};ranks=[]
                for entry in propagations:
                    h=entry['centre'];R=entry['anchor_plane'];pieces=[]
                    need(F.rank(maps[R])==width,'transported quotient rank by independent column basis')
                    for r in entry['receivers']:
                        planes=ctx.views[j,r]
                        need(len(planes)==16 and h in planes and R in planes,'actual sixteen-plane view for every receiver')
                        key=h,r
                        if key not in cache:
                            off=np.vstack([maps[q] for q in planes if q!=h])
                            K=F.kernel(off,width)
                            need(F.rank(F.mm(maps[h],K))==width,'central quotient completes a full-rank native view')
                            cache[key]=K;kernel_counts[width]+=1
                        K=cache[key]
                        need(not np.any(F.mm(maps[R],K)),'every inverse fibre lies in the required quotient kernel')
                        pieces.append(K)
                    span=np.hstack(pieces);rank=F.rank(span)
                    need(rank==15*width,'all thirty complete quotient kernels generated')
                    ranks.append(rank)
                final=F.rank(np.vstack([maps[q] for q in union]))
                need(final==16*width,'independent full final-union rank')
                first=next(iter(cache.values()))
                need(F.rank(first)==width and F.rank(np.vstack([maps[union[0]]]*20))==width,
                     'single-fibre and repeated-final-observation negative controls')
                components[str(width)]={'propagation_ranks':ranks,'final_union_rank':final,'distinct_native_views':len(cache),
                    'source_coefficient_sha256':source_hash,'single_fibre_control_rank':width,'repeated_final_control_rank':width}
            row={'anchor':j,'leaves':[left,right],'centres':[h1,h2,h3],'final_receiver':i,'propagations':propagations,
                 'components':components,'full_bank_propagation_rank':3600,'full_bank_final_union_rank':3840,
                 'frozen_anchor_obstructs_arbitrary_separated_neighbours':True}
            need(row==published[j],'entire frozen finite application reproduced independently')
            out_rows.append(row)
            print('PASS_INDEPENDENT_ANCHOR',label,j,flush=True)
        all_results[label]=out_rows
    need(sum(map(len,all_results.values()))==17 and sum(receiver_counts.values())==510,'seventeen applications and thirty records each')
    result={'status':'PASS_INDEPENDENT_SEVENTEEN_FROZEN_ARRAY_APPLICATIONS','source_pins':PINS,
            'source_words':3,'anchor_certificates':17,'scalar_component_propagation_checks':1020,
            'all_receiver_family_size_histogram':dict(sorted(receiver_counts.items())),
            'distinct_off_H_kernels_checked':dict(kernel_counts),'coefficient_sha256':source_hashes,
            'independent_arithmetic':'right-pivot nullspaces and column-span elimination in separately authored C++',
            'results':all_results,'bank_GF64_fields':3840,'quotient_GF64_fields':240,
            'full_bank_propagation_rank':3600,'full_bank_final_union_rank':3840,
            'rank_nine_corollary':'reviewed in REVIEW.md under the admitted 221-tree-block invertibility premise',
            'strict_rank_bound_at_bank_3840_GF64':34560,'claim_rank_greater_than_34688':False,
            'all_foundations_retained':True,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],flush=True)

if __name__=='__main__':
    main()
