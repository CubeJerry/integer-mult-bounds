#!/usr/bin/env python3
"""Materialize all actual two-donor H causal array matrices and charged word."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json,subprocess

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
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
def compile_rows(rows):
    n=len(rows);a=list(rows);ops=[]
    def add(i,j):a[i]^=a[j];ops.append([i,j])
    for j in range(n):
        p=next(i for i in range(j,n)if a[i]>>j&1)
        if p!=j:add(j,p);add(p,j);add(j,p)
        for i in range(n):
            if i!=j and a[i]>>j&1:add(i,j)
    need(a==[1<<j for j in range(n)],'binary invertibility')
    ops.reverse();r=[1<<j for j in range(n)]
    for i,j in ops:r[i]^=r[j]
    need(r==rows,'all binary word columns')
    return ops
def xorshift(seed):
    mask=(1<<64)-1
    while True:
        seed^=(seed<<13)&mask;seed^=seed>>7;seed^=(seed<<17)&mask;seed&=mask
        yield seed&127
def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_HASH,'layout pin');w=json.loads(raw)
    A=[set(H)for H in w['A2']];D=[set(d)for d in w['D4']];R=w['root_table'];F=[{j for j in range(120)if sum(x*y for x,y in zip(r,R[j]))==0}for r in R[:111]];native=set(range(111));planes=[];lines=[]
    for h,H in enumerate(A):
        if len(H&native)!=2:continue
        ports=[d for d,DD in enumerate(D)if H<=DD];need(len(ports)==45,'45 actual ports');ix={d:k for k,d in enumerate(ports)};rec=[]
        for i in range(111):
            if H<=F[i]:
                ids=[ix[d]for d in ports if D[d]<=F[i]];need(len(ids)==15,'15 actual receiver ports');rec.append((i,[2*s+b for s in ids for b in range(2)]))
        planes.append({'H':h,'native_donors':sorted(H&native),'D4_ports':ports,'receivers':[i for i,_ in rec]});lines.append(f'{h} {len(rec)}');lines.extend(str(i)+' '+' '.join(map(str,rows))for i,rows in rec)
    need(len(planes)==227,'all two-donor H');(a.out/'INSTANCE.txt').write_text(str(len(planes))+'\n'+'\n'.join(lines)+'\n')
    cpp=Path(__file__).with_name('find.cpp');exe=a.out/'find';subprocess.run(['g++','-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True);subprocess.run([str(exe),str(a.out/'INSTANCE.txt'),str(a.out/'COEFFICIENTS.json')],check=True)
    coeff=json.loads((a.out/'COEFFICIENTS.json').read_text());need(len(coeff['planes'])==227,'coefficient count')
    need(all(mul(x,power(x,126))==1 for x in range(1,128)),'field inverses')
    V=[[power(i+1,j)for j in range(90)]for i in range(90)];binary=binary_rows(V);word=compile_rows(binary)
    wr=json.dumps({'schema':'F128-V90-binary-ADD-v1','field_modulus':MOD,'binary_records':630,'ADD':word},separators=(',',':')).encode()+b'\n';(a.out/'ADD-WORD.json.gz').write_bytes(gzip.compress(wr,mtime=0))
    weights=[sum(mul(c,1<<k).bit_count()for k in range(DEG))for c in range(128)]
    cross=[];trials=Counter()
    for entry,geom in zip(coeff['planes'],planes):
        need(entry['H']==geom['H'],'geometry and coefficients aligned');C=[[int(row[2*j:2*j+2],16)for j in range(90)]for row in entry['C_hex_rows']];need(len(C)==90,'C dimensions')
        rng=xorshift(int(entry['xorshift_seed_decimal']));need(all(c==next(rng)for row in C for c in row),'fully explicit deterministic coefficients')
        need(len(entry['conditions'])==2*len(geom['receivers'])and all(d for _,_,d in entry['conditions']),'all native receiver/donor determinants')
        cross.append(sum(weights[c]for row in C for c in row));trials[entry['trial']]+=1
    # Every literal early stripe uses45 actual fields of each donor, one per donor/D.
    # Every late stripe uses15 actual fields of each donor and60 pure-Y baselines.
    late_counts=[[0,0,0]for _ in range(6)]
    for d in range(45):
        used=[0]*6
        for donor in range(2):
            for k in range(2):
                stripe=k+2*((donor+d)%3);used[stripe]+=1;late_counts[stripe][donor]+=1
        for stripe in range(6):
            late_counts[stripe][2]+=2-used[stripe]
        need(sum(2-u for u in used)==8,'eight real pure-Y holders per D')
    need(late_counts==[[15,15,60]]*6,'actual late source holder striping')
    # A field-holder permutation of90 holders uses<=89 swaps, each21 binary ADDs.
    permutation_per_phase_stripe=89*3*DEG
    cost=[12*(len(word)+permutation_per_phase_stripe)+6*c+540*DEG for c in cross]
    result={'status':'PASS_EXPLICIT_CAUSAL_TWO_DONOR_PLANE_ARRAYS','layout_uncompressed_sha256':LAYOUT_HASH,'field_modulus':MOD,'field_degree':DEG,'planes':227,'receiver_donor_conditions':coeff['total_conditions'],'coefficient_trials':coeff['total_trials'],'trial_histogram':dict(sorted(trials.items())),'V90_binary_records':630,'V90_ADD_count':len(word),'V90_ADD_word_uncompressed_sha256':sha256(wr).hexdigest(),'C_crosswave_ADD_per_stripe_min':min(cross),'C_crosswave_ADD_per_stripe_max':max(cross),'cache_INIT_per_H':540*DEG,'cache_copy_ADD_per_H':540*DEG,'cache_dirty_CLEAR_per_H':540*DEG,'extra_MOVE':0,'full_ADD_count_all_227_H_including_permutation_bound':sum(cost),'ADD_per_H_min':min(cost),'ADD_per_H_max':max(cost),'coefficient_json_sha256':sha256((a.out/'COEFFICIENTS.json').read_bytes()).hexdigest(),'global_native_quotients_constructed':False,'later_D_K_F_transport_constructed':False,'singleton_planes_handled':False,'new_complete_kappa':False,'geometry':planes}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['receiver_donor_conditions'],'conditions','ADDall',sum(cost))
if __name__=='__main__':main()
