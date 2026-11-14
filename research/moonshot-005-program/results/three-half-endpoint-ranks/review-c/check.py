#!/usr/bin/env python3
"""Independent direct-binary-matrix path ranks and exact small Gauss sums."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse,gzip,hashlib,itertools,json
HERE=Path(__file__).resolve().parent;AUTHOR=HERE.parents[1]/'worker-a/three-half-endpoint-ranks';N=33
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(name,pin):
    p=HERE/'source'/name;need(sha(p)==pin,'source pin');return json.loads(gzip.decompress(p.read_bytes())if name.endswith('.gz')else p.read_bytes())
def bits(x):
    while x:
        v=x&-x;yield v.bit_length()-1;x^=v
def dot(x,y):return(x&y).bit_count()%2
def apply(cols,x):
    a=0
    for i in bits(x):a^=cols[i]
    return a
def rank(cols):
    piv={}
    for z in cols:
        while z:
            b=z.bit_length()-1
            if b in piv:z^=piv[b]
            else:piv[b]=z;break
    return len(piv)
def main(out):
    need(sha(AUTHOR/'FREEZE.json')=='bb2861c8428b6402256e5ec771ac45bac08644fbabacbd9876bbe5c98c2a5530','author manifest')
    need(sha(AUTHOR/'PROOF.md')=='a59e5484f347863607b87c44dfdc25125fd89d43620f38adaf34b87160d0b2f5','author proof')
    w=load('R0-WORD.json.gz','d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c');rt=load('ROUTES.json','ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a')
    ports=w['logical_involution']['ports'];roles=w['logical_involution']['role_map'];X={int(h):i for h,i in roles['X'].items()};Y={int(h):i for h,i in roles['Y'].items()};R={h:{}for h in ports}
    for j in ports:
        state=[F(0)for _ in range(448)];state[X[j]]=F(1)
        for e in w['program']:
            if e[0]=='ADD':state[e[1]]+=F(e[3])*state[e[2]]
            else:need(e[0]=='MOVE','source alphabet')
        for h in ports:
            if state[Y[h]]:R[h][j]=state[Y[h]]
    rec={r['port']:r for r in rt['route_records']if r['stage']==1};q={h:rec[h]['normal']for h in ports}
    for h in ports:
        need(len(R[h])==4 and dot(q[h],q[h])==1,'actual four contacts and odd normal')
        for j,c in R[h].items():need(R[j].get(h)==c and abs(c)==F(1,2)and dot(q[h],q[j])==0,'actual symmetric orthogonal dyadic edge')
    P={}
    for s,h in itertools.product((1,2,3),ports):
        bb=rec[h]['orthogonal_complement'];need(all(dot(a,b)==int(i==j)for i,a in enumerate([q[h]]+bb)for j,b in enumerate([q[h]]+bb)),'actual orthonormal head completion')
        vv=[b^(1<<(9+8*(s-1)+k))for k,b in enumerate(bb)]
        cols=[]
        for i in range(N):
            z=1<<i
            for a in vv:
                if dot(a,1<<i):z^=a
            cols.append(z)
        need(all(apply(cols,c)==1<<i for i,c in enumerate(cols)),'orthogonal swap involution')
        P[s,h]=tuple(cols)
    start=tuple((1<<i)if i>=9 else 0 for i in range(N))
    def step(K,s,h,j,require=True):
        ph,pj=P[s,h],P[s,j]
        # P=Ph Pj; its transpose is Pj Ph. Direct conjugation of K columns.
        cols=[]
        for i in range(N):
            z=apply(pj,ph[i]);z=apply(K,z);z=apply(ph,apply(pj,z));cols.append(z)
        if require:need(apply(cols,q[h])==q[h],'removable actual eigenvector')
        for i in bits(q[h]):cols[i]^=q[h]
        return tuple(cols)
    one=Counter();three=Counter();two=Counter()
    for i in ports:
        for j in R[i]:
            K1=step(start,1,j,i);need(rank(K1)==23,'rank23 first stage');one[rank(K1)]+=1
            for k in R[j]:
                K2=step(K1,2,k,j);need(rank(K2)==22,'rank22 second fresh stage');two[rank(K2)]+=1
                for h in R[k]:
                    K3=step(K2,3,h,k);need(rank(K3)==21,'rank21 third fresh stage')
                    need(all(apply(K3,c)==c for c in K3),'exact final projection');three[rank(K3)]+=1
    h=ports[0];j=next(iter(R[h]));rep=step(step(start,1,h,j),1,j,h,False);diag=step(start,1,h,h,False)
    need(rank(rep)==24 and rank(diag)==25,'fresh/orthogonal boundary controls')
    # Enumerate exact Z[i] Fourier sums in dimension three, including dependent
    # and singular kernels and all linear sign translations. No floating point.
    gaussian_cases=0;unit=((1,0),(0,1),(-1,0),(0,-1))
    for mask in range(128):
        vv=[v for v in range(1,8)if mask>>(v-1)&1]
        K=[]
        for i in range(3):
            z=0
            for v in vv:
                if v>>i&1:z^=v
            K.append(z)
        rk=rank(K)
        for shift in range(8):
            amplitudes=[]
            for x in range(8):
                a=b=0
                for z in range(8):
                    phase=(sum(dot(v,z)for v in vv)+2*dot(shift^x,z))%4
                    c,d=unit[phase];a+=c;b+=d
                if a or b:amplitudes.append(a*a+b*b)
            need(len(amplitudes)==2**rk and set(amplitudes)=={2**(6-rk)},'exact Gauss support and uniform magnitude')
            gaussian_cases+=1
    data={'status':'PASS_INDEPENDENT_FRESH_PATH_RANK_REVIEW','source_columns':112,'source_edges':sum(map(len,R.values())),'first_path_ranks':dict(one),'second_path_ranks':dict(two),'third_path_ranks':dict(three),'all_final_kernels_projections':True,'small_exact_Gauss_sum_cases':gaussian_cases,'negative_controls':{'repeated_stage_rank':rank(rep),'nonorthogonal_self_edge_rank':rank(diag)},'support_scope':'Per-path rank and support exactly; complete path sums only upper-bounded. Actual caller chronology remains a separate dependency.','new_kappa':False}
    out.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps(data,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--author',type=Path,default=AUTHOR);args=p.parse_args();AUTHOR=args.author;main(args.output)
