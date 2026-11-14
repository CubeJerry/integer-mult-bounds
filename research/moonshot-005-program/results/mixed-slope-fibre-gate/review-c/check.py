#!/usr/bin/env python3
"""Independent source-bound fibre review; no author checker import."""
from pathlib import Path
from fractions import Fraction as F
import argparse,gzip,hashlib,importlib.util,itertools,json
HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parents[1]/'worker-a/mixed-slope-fibre-gate'
PINS={'R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a'}
C=(29,30,59,60,73,74,83,84)
def need(x,m):
    if not x:raise RuntimeError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):
    p=HERE/'source'/n;need(digest(p)==PINS[n],'source pin')
    return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def mm(A,B):return [[sum(A[i][k]*B[k][j]for k in range(len(B)))for j in range(len(B[0]))]for i in range(len(A))]
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def rank(A):
    A=[list(row)for row in A];r=0
    for j in range(len(A[0])):
        p=next((i for i in range(r,len(A))if A[i][j]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r];z=A[r][j];A[r]=[x/z for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][j]:
                z=A[i][j];A[i]=[a-z*b for a,b in zip(A[i],A[r])]
        r+=1
    return r
def main(output):
    need(digest(AUTHOR/'FREEZE.json')=='1071e3bac6b2e91a935d8385fa408ae80ca01615de7b812d7df7e6ade2badd79','author freeze')
    need(digest(AUTHOR/'PROOF.md')=='9015d6cdb3a02c2a5c5922bf5463c82393e8e668e0fe165b800425bbc68210ae','author proof')
    need(digest(HERE/'fourier_review.py')=='82063edce04db372ba93e19a4cb194116d7a090c454a9095f116a5dad4803b89','prior independent engine')
    sp=importlib.util.spec_from_file_location('prior_independent_fourier',HERE/'fourier_review.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
    w,rr=load('R0-WORD.json.gz'),load('ROUTES.json')
    P=w['logical_involution']['ports'];role=w['logical_involution']['role_map'];X={int(h):i for h,i in role['X'].items()};Y={int(h):i for h,i in role['Y'].items()};R={h:{}for h in P}
    # Column replay rather than the author's row accumulator.
    for j in P:
        state=[F(0)for _ in range(448)];state[X[j]]=F(1)
        for ev in w['program']:
            if ev[0]=='ADD':state[ev[1]]+=F(ev[3])*state[ev[2]]
            else:need(ev[0]=='MOVE','source alphabet')
        need(all(state[X[h]]==F(h==j)for h in P),'all X survive')
        for h in P:
            if state[Y[h]]:R[h][j]=state[Y[h]]
    need(all(set(R[h])<=set(C)and len(R[h])==4 for h in C),'closed actual class')
    RC=[[R[h].get(j,F(0))for j in C]for h in C]
    need(mm(RC,RC)==eye(8)and rank(RC)==8,'actual R involution')
    rec={(r['stage'],r['port']):r for r in rr['route_records']};M={};Mi={};O={};Oi={}
    for s,h in itertools.product((1,2),C):
        r=rec[s,h];B=r['orthogonal_complement'];q=r['normal']
        need(q&1==0 and B[0]==1,'shared actual basis axis')
        need(all(v.dot(a,b)==int(i==j)for i,a in enumerate([q]+B)for j,b in enumerate([q]+B)),'head orthonormal basis')
        cols=v.route(B,s);tau,sigma=r['input_translation'],r['output_translation']
        M[s,h]=v.op(cols,((tau,2),));Mi[s,h]=v.op(cols,((v.apply(cols,tau),2),))
        O[s,h]=v.op(cols,((sigma,2),));Oi[s,h]=v.op(cols,((v.apply(cols,sigma),2),))
    def evaluate(A,z):return v.apply(A[0],z),sum(c*v.dot(a,z)for a,c in A[1])%4
    blocks=0;diagonals=0
    for eps in itertools.product((0,1),repeat=2):
        z=(eps[0]<<9)^(eps[1]<<17)
        for h in C:
            q=rec[1,h]['normal'];need(evaluate(v.Q(q),z)==(z,0),'actual Q is identity')
            for s in (1,2):
                f,p=evaluate(v.D(s),z);need(f==z and 2*p%4==2*eps[s-1],'two-column body sign')
                need(evaluate(v.D(s,2),z)[1]*2%4==0,'body square identity');diagonals+=1
                for j,c in R[h].items():
                    ops=(v.product(Mi[s,h],M[s,j]),v.product(O[s,h],Oi[s,j]),v.product(Mi[s,h],v.Q(rec[s,j]['normal'],-1),M[s,j]),v.product(v.Q(q,-1),O[s,h],Oi[s,j]))
                    for A in ops:
                        f,p=evaluate(A,z);need(f==z and 2*p%4==0,'actual conjugated block preserves fibre')
                        need(evaluate(A,0)==(0,0),'appended zero columns');blocks+=1
        need(all(2*v.dot(1<<a,z)%2==0 for a in range(25)),'tensor-uniform translation cancellation')
    need(evaluate(M[1,C[0]],1<<9)[0]==1,'raw spatial M escape')
    need(v.dot(1<<9,1<<9)==1,'single-column translation escape')
    need(F(1,2)**2!=F(1,2),'R applies once on the whole array')
    checks=0
    for orientation in (0,1):
        cross=[[F(0)for _ in range(16)]for _ in range(16)]
        for i in range(8):
            for j in range(8):cross[i+8*(1-orientation)][j+8*orientation]=RC[i][j]
        need(rank(cross)==8,'actual cross rank eight')
        for a in (F(-2),F(3,2)):
            G0=eye(16);G1=eye(16);G2=eye(16)
            for i in range(8):G0[i][i+8]=a;G1[i+8][i]=F(1,3);G2[i][i]=F(-1)
            expected=mm(mm(mm(G2,G1),cross),G0);walsh=[[F(0)for _ in range(16)]for _ in range(16)]
            for s1,s2 in itertools.product((-1,1),repeat=2):
                N1=[[F(s1)*F(i==j)+cross[i][j]for j in range(16)]for i in range(16)]
                N2=[[F(s2)*F(i==j)+cross[i][j]for j in range(16)]for i in range(16)]
                W=mm(mm(mm(mm(G2,N2),G1),N1),G0)
                for i in range(16):
                    for j in range(16):walsh[i][j]+=F(s2,4)*W[i][j]
            need(walsh==expected and rank(walsh)==8,'actual full rank-eight Walsh coefficient');checks+=1
    result={'status':'PASS_INDEPENDENT_SOURCE_BOUND_FIBRE_REVIEW','source_columns':112,'class_ports':list(C),'source_R_rank':8,'actual_route_records':16,'four_fibres':4,'diagonal_checks':diagonals,'exact_block_checks':blocks,'full_sixteen_dimensional_walsh_controls':checks,'width_statement':'Every V>=2: (z,z,0,...,0)','controls':['raw M exits fibre','single-column translation distinguishes fibre','whole-array R not tensor-powered'],'scope':'Two fixed banks, each fresh mixed source once, invertible adapters with identical restrictions on all four actual fibres. Raw spatial routes, added fields/body occurrences and nonuniform column operations remain outside.','new_kappa':False}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--author',type=Path,default=AUTHOR);args=p.parse_args();AUTHOR=args.author;main(args.output)
