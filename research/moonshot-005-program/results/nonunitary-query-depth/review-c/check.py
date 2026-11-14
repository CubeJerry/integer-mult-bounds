#!/usr/bin/env python3
"""Independent exact row-support controls, with no author checker import."""
from pathlib import Path
import argparse,gzip,hashlib,itertools,json
HERE=Path(__file__).resolve().parent;AUTHOR=HERE.parents[1]/'root-work/nonunitary-query-depth'
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def support(A):return max((sum(x!=0 for x in row)for row in A),default=0)
def main(output):
    need(sha(AUTHOR/'MANIFEST.json')=='89fb25c61c3a17c48900f2e7d05f719c502b6f37cdc0525eb13fb5918bbb6c09','author manifest')
    need(sha(AUTHOR/'PROOF.md')=='bd121f3c3e864ee65fd545346dd70458bebf0573d4080ad811ccb145ea590f55','author proof')
    pairs=0;strict=0;zero=0
    for aa in itertools.product((0,1),repeat=6):
        A=[aa[:3],aa[3:]]
        for bb in itertools.product((0,1),repeat=6):
            B=[bb[:2],bb[2:4],bb[4:]]
            product=[[sum(A[i][k]*B[k][j]for k in range(3))%2 for j in range(2)]for i in range(2)]
            lhs,rhs=support(product),support(A)*support(B)
            need(lhs<=rhs,'rectangular row-union inequality')
            pairs+=1;strict+=lhs<rhs;zero+=lhs==0
    p=AUTHOR/'source/R0-WORD.json.gz';need(sha(p)=='c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336','inherited actual source')
    d=json.loads(gzip.decompress(p.read_bytes()))['logical_involution'];q={int(h):v for h,v in d['normals'].items()};R={int(h):{int(j):c for j,c in row.items()}for h,row in d['R_rows'].items()}
    blocks=0
    for h,row in R.items():
        need(len(row)==4,'actual four port blocks')
        for j in row:
            need(len({0,q[h],q[j],q[h]^q[j]})==4,'two independent head translations');blocks+=1
    for V in range(1,33):
        need(2**(2*V+2)>(1+2**V)*2**(V+1),'N one-query ordinary requirement')
        need(2**(2*V+4)>(1+2**V)*2**(V+3),'C one-query ordinary requirement')
        need(4*(2**V)**2==4**(V+1),'sharp two-Gaussian N support template')
    # Invertible nonunitary ordinary butterflies on V distinct binary axes.
    # Each degree-two layer has L increment1; the final support is exactly2^V.
    for V in range(1,9):
        rows=[{i:1}for i in range(2**V)]
        for axis in range(V):
            nxt=[]
            for i in range(2**V):
                z=dict(rows[i])
                for j,c in rows[i^(1<<axis)].items():z[j]=z.get(j,0)+2*c
                nxt.append(z)
            rows=nxt
        need(all(len(row)==2**V for row in rows),'linear ordinary allowance escape')
    need(sha(AUTHOR/'source/C-REVIEW.md')=='cb752179d9ab89464cbe246ced06410f12f409f109ff87e73128a669239cbc7c','inherited independent C review')
    data={'status':'PASS_INDEPENDENT_NONUNITARY_SUPPORT_REVIEW','exhaustive_rectangular_binary_products':pairs,'strict_support_inequalities':strict,'zero_products':zero,'actual_N_translation_blocks':blocks,'exact_query_bound_widths':32,'linear_ordinary_escape_widths':8,'C_source_scope':'Inherited pinned independent source review, not re-executed collision enumeration','classification':'Universal row-union proof reviewed directly; finite controls; no rank-mass or arbitrary price inference','new_kappa':False}
    output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps(data,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'RESULT.json');p.add_argument('--author',type=Path,default=AUTHOR);args=p.parse_args();AUTHOR=args.author;main(args.output)
