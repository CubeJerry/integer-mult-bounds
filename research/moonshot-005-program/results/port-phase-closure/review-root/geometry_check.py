#!/usr/bin/env python3
"""Root's source geometry and proof-table review, independent of C code."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import numpy as np

HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]
def need(v,s):
    if not v:raise ValueError(s)
def roots(q):
    ix=[i for i in range(9)if q>>i&1]
    if len(ix)==3:return [2 if i in ix else-1 for i in range(9)]
    need(len(ix)==7,'root');a,b=[i for i in range(9)if i not in ix];return [3*(int(i==a)-int(i==b))for i in range(9)]
def gram(a,b):return F(sum(x*y for x,y in zip(roots(a),roots(b))),18)
def rank(xs):
    b={}
    for x in xs:
        while x:
            k=x.bit_length()-1
            if k in b:x^=b[k]
            else:b[k]=x;break
    return len(b)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--geometry',type=Path,default=BASE/'worker-b/FULL112-GEOMETRY.json');ap.add_argument('--native',type=Path,default=BASE/'programme/research/moonshot-005-program/results/complex-proper-born-clique/author/dependencies/native.json.gz');ap.add_argument('--out',type=Path,default=HERE/'GEOMETRY-RESULT.json');args=ap.parse_args()
    need(hashlib.sha256(args.geometry.read_bytes()).hexdigest()=='e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6','geometry pin')
    need(hashlib.sha256(args.native.read_bytes()).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin')
    g=json.loads(args.geometry.read_text());n=json.loads(gzip.decompress(args.native.read_bytes()));out=[]
    for h in g['old_ports']:need(n['frames'][n['initial'][h]][0]==g['normal_by_port'][str(h)],'actual old normal')
    for c in g['classes']:
        aa,bb=[x['normals']for x in c['halves']];u,v=min(aa),min(bb);W={q^u for q in aa};need(W=={q^v for q in bb}and len(W)==4,'shared affine direction')
        w1=min(W-{0});w2=min(W-{0,w1});need(W=={0,w1,w2,w1^w2}and rank([u,v,w1,w2])==4,'affine three-flat')
        def seq(a):return[a^(w1 if x&1 else 0)^(w2 if x&2 else 0)for x in range(4)]
        A,B=seq(u),seq(v);m=[[int(2*gram(a,b))for b in B]for a in A]
        expected=[[(-1)**(((x&1)*(y>>1)+(x>>1)*(y&1))%2)for y in range(4)]for x in range(4)]
        got=[[m[x][y]*m[x][0]*m[0][y]*m[0][0]for y in range(4)]for x in range(4)];need(got==expected,'actual signed symplectic Fourier')
        patterns={tuple((q&z).bit_count()%2 for q in A+B)for z in range(512)};need(len(patterns)==16,'all sixteen genuine affine phases')
        out.append({'ports':c['ports'],'bases':[u,v,w1,w2],'characters':len(patterns)})
    # Authenticate the separate root NumPy screen's actual matrix from native roots.
    s=json.loads((HERE/'SPECTRAL-SCREEN.json').read_text());qs=s['labels'];need(qs==g['classes'][2]['normals'],'root screen real class')
    need([[str(F(i==j)-gram(a,b))for j,b in enumerate(qs)]for i,a in enumerate(qs)]==s['R0'],'independent original normalized matrix')
    H=np.zeros((4,4),dtype=np.int64)
    for i,j in[(0,3),(1,2),(2,1),(3,0)]:H[i,j]=1
    I=np.eye(4,dtype=np.int64);table=[]
    for a,b,c in product(range(2),repeat=3):
        L=I.copy();L[2,0]=a;L[2,1]=c;L[3,0]=c;L[3,1]=b;S=(L@H)%2;P=I.copy();order=None
        for k in range(1,13):
            P=(P@S)%2
            if np.array_equal(P,I):order=k;break
        need(order in[2,3,4,6],'two-qubit binary order');table.append([a,b,c,order,order//2 if order%2==0 else order])
    receipt={'status':'PASS_ROOT_ALL_CLASS_GEOMETRY_AND_PERIOD_PROOF_TABLE','classes':out,'binary_action_table':table,'screen_matrix_authentic':True,'scope':'Independent source reconstruction and proof-table check. Separate phase_closure.py uses exact Gaussian integers in NumPy object arrays; author code is not imported.'}
    args.out.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print('PASS: fourteen native conjugacies and eight binary proof cases')
if __name__=='__main__':main()
