#!/usr/bin/env python3
"""Explicit causal full-plane F64 array interface and whole-record ADD compiler."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR_HASH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
MOD=67
def need(q,msg):
    if not q:raise ValueError(msg)
def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&64:a^=MOD
    return z
def power(a,n):
    z=1
    while n:
        if n&1:z=mul(z,a)
        a=mul(a,a);n>>=1
    return z
def binary_rows(matrix):
    ans=[]
    for row in matrix:
        for bit in range(6):
            z=0
            for j,c in enumerate(row):
                for k in range(6):
                    if mul(c,1<<k)>>bit&1:z|=1<<(6*j+k)
            ans.append(z)
    return ans
def binary_rank(rows):
    b={}
    for z in rows:
        while z and z.bit_length()in b:z^=b[z.bit_length()]
        if z:b[z.bit_length()]=z
    return len(b)
def compile_rows(rows):
    n=len(rows);r=list(rows);ops=[]
    def add(a,b):r[a]^=r[b];ops.append([a,b])
    for col in range(n):
        p=next(i for i in range(col,n)if r[i]>>col&1)
        if p!=col:add(col,p);add(p,col);add(col,p)
        for i in range(n):
            if i!=col and r[i]>>col&1:add(i,col)
    need(r==[1<<j for j in range(n)],'binary Gaussian reduction')
    word=ops[::-1];replayed=[1<<j for j in range(n)]
    for a,b in word:replayed[a]^=replayed[b]
    need(replayed==rows,'all independent columns of actual ADD word')
    return word
def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--factor',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    lr=gzip.decompress(a.layout.read_bytes());fr=a.factor.read_bytes()
    need(sha256(lr).hexdigest()==LAYOUT_HASH and sha256(fr).hexdigest()==FACTOR_HASH,'source pins')
    w=json.loads(lr);f=json.loads(fr);add=dict(f['factors']);need(f['denominator']==2,'factor scale')
    # The quotient ring is a field: every nonzero element has the displayed inverse.
    need(all(mul(x,power(x,62))==1 for x in range(1,64)),'F64 field inverse check')
    nodes=list(range(1,46));V=[[power(x,j)for j in range(45)]for x in nodes]
    M=binary_rows(V);need(binary_rank(M)==270,'whole V45 invertible')
    word=compile_rows(M)
    control=[1<<j for j in range(270)]
    for p,(x,y)in enumerate(word):
        if p!=len(word)//2:control[x]^=control[y]
    need(control!=M,'omitted binary ADD is rejected')
    # Duplicate a selected evaluation node: even a donor projection loses rank.
    small=[[power(nodes[i],j)for j in range(15)]for i in range(15)]
    need(binary_rank(binary_rows(small))==90,'one genuine 15-row donor projection')
    small[1]=small[0];need(binary_rank(binary_rows(small))==84,'duplicate-node control loses one field rank')
    A=[set(h)for h in w['A2']];D=[set(d)for d in w['D4']];R=w['root_table'];N=set(range(111))
    F=[{j for j in range(120)if sum(x*y for x,y in zip(r,R[j]))==0}for r in R[:111]]
    entries=[];hist=Counter();shared=Counter();incidences=0;all_blocks=0
    for h,H in enumerate(A):
        if len(H&N)!=3:continue
        x=4+add.get(h,0);eh=3*x;lh=24-eh
        need(x in[4,5,6]and eh>0 and lh>0,'actual balanced colours')
        need(15*eh==45*x and 15*lh==360-45*x,'actual donor temporal capacities')
        ports=[d for d,DD in enumerate(D)if H<=DD];need(len(ports)==45,'45 genuine D4 exits')
        index={d:k for k,d in enumerate(ports)};receivers={}
        for i in range(111):
            if not H<=F[i]:continue
            ids=[index[d]for d in ports if D[d]<=F[i]];need(len(ids)==15,'actual receiver has 15 ports')
            # Exact Vandermonde product proves every source-block determinant.
            det=1
            for s,t in combinations(ids,2):det=mul(det,nodes[s]^nodes[t])
            need(det!=0,'all actual V15 determinants nonzero')
            dets=[]
            for j in range(3):
                q=det
                for k in ids:q=mul(q,power(nodes[k],15*j))
                need(q!=0,'scaled donor projection invertible');dets.append(q);all_blocks+=1
            receivers[i]={'ports':ids,'field_determinants':dets};incidences+=1
        for i,k in combinations(receivers,2):
            c=len(set(receivers[i]['ports'])&set(receivers[k]['ports']));shared[c]+=1
        hist[x]+=1
        entries.append({'H':h,'native_donors':sorted(H&N),'x':x,'early_lanes_per_port':eh,'late_lanes_per_port':lh,'actual_D4_ports':ports,'receiver_subsets':receivers})
    need(len(entries)==881,'all full native planes')
    word_payload={'schema':'F64-V45-whole-record-binary-ADD-v1','field_modulus':MOD,'nodes':nodes,'binary_records':270,'ADD':word}
    wr=json.dumps(word_payload,separators=(',',':')).encode()+b'\n'
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'ADD-WORD.json.gz').write_bytes(gzip.compress(wr,mtime=0))
    (a.out/'COEFFICIENTS.json').write_text(json.dumps({'field_modulus':MOD,'nodes':nodes,'matrix':V},separators=(',',':'))+'\n')
    result={'status':'PASS_EXPLICIT_CAUSAL_FULL_PLANE_ARRAY_INTERFACE','layout_uncompressed_sha256':LAYOUT_HASH,'factor_sha256':FACTOR_HASH,'field_modulus':MOD,'field_degree':6,'full_native_planes':len(entries),'factor_x_histogram':dict(sorted(hist.items())),'actual_H_receiver_incidences':incidences,'actual_donor_projection_determinants':all_blocks,'receiver_pair_shared_port_histogram':dict(sorted(shared.items())),'base_binary_records':270,'base_ADD_count':len(word),'base_extra_INIT_CLEAR_MOVE':0,'ADD_per_plane_without_physical_permutation':24*len(word),'physical_input_permutation_ADD_bound_per_stripe':792,'ADD_per_plane_with_permutation_bound':24*(len(word)+792),'ADD_all_881_planes_bound':881*24*(len(word)+792),'full_plane_input_and_output_field_dimension':1080,'receiver_target_field_dimension':360,'common_port_field_dimension':24,'binary_ADD_word_uncompressed_sha256':sha256(wr).hexdigest(),'negative_controls':{'omitted_ADD_rejected':True,'duplicated_node_field_rank':14},'global_native_source_constructed':False,'later_D_K_F_transport_constructed':False,'new_complete_kappa':False,'planes':entries}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],len(entries),'planes',incidences,'receiver sets','ADDbase',len(word),'ADDperH',result['ADD_per_plane_with_permutation_bound'])
if __name__=='__main__':main()
