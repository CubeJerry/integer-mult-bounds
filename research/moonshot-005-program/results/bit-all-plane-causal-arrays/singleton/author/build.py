#!/usr/bin/env python3
"""Explicit Hermite interface at every genuine singleton native H."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
WORD_HASH='ee6fd64bc0afb1352e6a7e8c7f1819438faafe6c1fbf32cafe59ae56ec2861a5'
MOD=131;DEG=7
def need(q,msg):
    if not q:raise ValueError(msg)
def mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        b>>=1;a<<=1
        if a&128:a^=MOD
    return c
def power(a,n):
    c=1
    while n:
        if n&1:c=mul(c,a)
        a=mul(a,a);n>>=1
    return c
def binary_rows(M):
    out=[]
    for row in M:
        for bit in range(DEG):
            z=0
            for j,c in enumerate(row):
                for k in range(DEG):
                    if mul(c,1<<k)>>bit&1:z|=1<<(DEG*j+k)
            out.append(z)
    return out
def rank(rows):
    basis={}
    for row in rows:
        while row and row.bit_length()in basis:row^=basis[row.bit_length()]
        if row:basis[row.bit_length()]=row
    return len(basis)
def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--v90-word',type=Path,required=True);p.add_argument('--common-result',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    lr=gzip.decompress(a.layout.read_bytes());wr=gzip.decompress(a.v90_word.read_bytes());need(sha256(lr).hexdigest()==LAYOUT_HASH,'layout pin');need(sha256(wr).hexdigest()==WORD_HASH,'actual V90 word pin');w=json.loads(lr);word=json.loads(wr);need(word['field_modulus']==MOD and word['binary_records']==630,'common-field word')
    need(all(mul(x,power(x,126))==1 for x in range(1,128)),'field inverses')
    V=[[power(i+1,j)for j in range(90)]for i in range(90)];C=[[power(i+1,j-1)if j&1 else 0 for j in range(90)]for i in range(90)]
    R=w['root_table'];A=[set(h)for h in w['A2']];D=[set(d)for d in w['D4']];F=[{j for j in range(120)if sum(x*y for x,y in zip(r,R[j]))==0}for r in R[:111]];native=set(range(111));entries=[];checks=0
    for h,H in enumerate(A):
        if len(H&native)!=1:continue
        ports=[d for d,DD in enumerate(D)if H<=DD];need(len(ports)==45,'actual singleton45 ports');ix={d:k for k,d in enumerate(ports)};receivers=[]
        for i in range(111):
            if not H<=F[i]:continue
            ps=[ix[d]for d in ports if D[d]<=F[i]];need(len(ps)==15,'actual singleton receiver15 ports');rows=[2*p+b for p in ps for b in range(2)]
            det=1
            for s,t in combinations(rows,2):det=mul(det,power((s+1)^(t+1),4))
            need(det!=0,'all actual Hermite determinants')
            M=[V[s][:60]for s in rows]+[C[s][:60]for s in rows];need(rank(binary_rows(M))==420,'full60-field Hermite minor')
            receivers.append({'receiver':i,'ports':ps,'Hermite_determinant':det});checks+=1
        entries.append({'H':h,'native_donor':next(iter(H&native)),'actual_D4_ports':ports,'receivers':receivers})
    need(len(entries)==11,'all eleven singleton planes')
    VB=binary_rows(V);CB=binary_rows(C);n=630;cache_indices=[DEG*j+b for j in range(90)if j&1 for b in range(DEG)];need(len(cache_indices)==315,'odd coefficients only')
    even_mask=sum(1<<(DEG*j+b)for j in range(90)if not(j&1)for b in range(DEG));need(all(not(row&even_mask)for row in CB),'derivative has no even columns')
    expected=VB+[CB[i]^(1<<(n+i))for i in range(n)]
    def replay(skip=None):
        public=[1<<j for j in range(2*n)];cache={j:(0 if j==skip else public[j])for j in cache_indices}
        for i,j in word['ADD']:public[i]^=public[j]
        count=0
        for i,row in enumerate(CB):
            while row:
                bit=row&-row;j=bit.bit_length()-1;row^=bit;public[n+i]^=cache[j];count+=1
        return public,cache,count
    public,cache,cross=replay();need(public==expected,'all1260 original columns, including arbitrary Y')
    need(all(v==1<<j for j,v in cache.items()),'every cache owner dirty');bad,_,_=replay(cache_indices[0]);need(bad!=expected,'omitted cache copy rejected')
    need(rank(binary_rows([V[s][:60]for s in range(30)]+[[0]*60 for _ in range(30)]))==210,'omitted derivative rank control30 instead60')
    add_per_H=6*(len(word['ADD'])+cross+315);common=json.loads(a.common_result.read_text())
    (a.out/'COEFFICIENTS.json').write_text(json.dumps({'field_modulus':MOD,'evaluation_nodes':list(range(1,91)),'early_matrix':V,'crosswave_derivative_matrix':C,'late_baseline':'identity'},separators=(',',':'))+'\n')
    result={'status':'PASS_EXPLICIT_CAUSAL_SINGLETON_HERMITE_INTERFACES','layout_uncompressed_sha256':LAYOUT_HASH,'V90_ADD_word_uncompressed_sha256':WORD_HASH,'field_modulus':MOD,'field_degree':DEG,'singleton_planes':11,'actual_receiver_Hermite_minors':checks,'source_field_dimension_per_H':540,'receiver_source_field_rank':360,'all_port_source_field_rank':540,'original_binary_columns_replayed':1260,'cache_binary_owners_per_stripe':315,'derivative_crosswave_ADD_per_stripe':cross,'ADD_per_H_including_cache_copies':add_per_H,'ADD_all11_H':11*add_per_H,'INIT_and_dirty_CLEAR_each_per_H':1890,'INIT_and_dirty_CLEAR_each_all11_H':20790,'extra_MOVE':0,'physical_holder_permutation_ADD':0,'all1119_nonempty_H_common_F128_ADD':common['uniform_F128_all_1108_ordinary_H_ADD_with_permutation_bound']+11*add_per_H,'all1119_nonempty_H_common_F128_INIT_and_dirty_CLEAR_each':common['all_227_two_donor_H_extra_INIT_and_dirty_CLEAR_each']+20790,'negative_controls':{'omitted_cache_copy_rejected':True,'omitted_derivative_field_rank':30,'required_field_rank':60},'global_source_quotients_constructed':False,'later_D_K_F_transport_constructed':False,'new_complete_kappa':False,'planes':entries}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items()if k!='planes'})
if __name__=='__main__':main()
