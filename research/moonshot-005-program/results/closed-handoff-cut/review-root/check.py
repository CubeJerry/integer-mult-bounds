#!/usr/bin/env python3
"""Independent arithmetic review; source maps inherit the separately reviewed replay."""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
from intervals import add,moment,need

BASE=Path(__file__).resolve().parents[2]
def box(x):return {'exact':[str(z)for z in x],'approx':[float(z)for z in x]}
def wrapper(a):
    return add((1,{1+16*a:2}),(-1,{1:4}),*( (1,{1+8*j:4})for j in range(1,a+1)),*((-1,{8*j:4})for j in range(1,a)))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,default=BASE/'worker-a/closed-handoff-cut');ap.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));args=ap.parse_args()
    proof=args.author/'PROOF.md'
    need(hashlib.sha256(proof.read_bytes()).hexdigest()=='57d9a62285df0d972e1ce800636b57e16affb44cdcd3ab4111d7732dff756744','frozen theorem')
    signs={a:moment(add((a,wrapper(a+1)),(-a-1,wrapper(a))))for a in[5,6]}
    need(signs[5][0]>0 and signs[6][1]<0,'global optimizer boundary signs')
    allowance=add((F(104,12),wrapper(6)))
    c={1:1,9:1,8:-1}; rows=[]
    for name,r,q in [('gram',104,{1:112,2:112,3:96,5:208,8:224}),('parity',56,{1:320,2:112,3:304,4:208,5:208,8:16})]:
        rem=moment(add((1,allowance),(-1,q)));minimum=moment(add((r,c)))
        need(minimum[0]>rem[1]>0,'closed source excluded at best arm')
        rows.append({'name':name,'rank':r,'remaining':box(rem),'minimum':box(minimum)})
    tested=0
    for a in range(9):
        for b in range(9):
            lhs=moment(add((1,{9-a:1}),(1,{9-b:1}),(-1,{abs(a-b):1})if a!=b else(1,{}),(-1,c)))
            # Equality at ranks0,8; otherwise exact positive margin.
            need(lhs[0]>=0 or (a,b)in[(0,8),(8,0)],'nested proper endpoint tariff')
            tested+=1
    bad=moment(add((1,{1:2,2:-1}),(-1,c)))
    need(bad[1]<0,'nonnested credit counterexample remains outside theorem')
    out={'status':'PASS_INDEPENDENT_PROOF_AND_ARITHMETIC_REVIEW','author_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'optimizer_signs':{str(a):box(x)for a,x in signs.items()},'closed_sources':rows,'proper_endpoint_pairs':tested,'nonnested_extension_rejected':True,'scope':'Universal route and information-rank proof reviewed separately. Source rows inherit A independent replay and C native-repartition review. No new source interpreter or kappa claim.'}
    args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print('PASS: scoped helper-aware rank cut, all-arm prices and nonnested boundary')
if __name__=='__main__':main()
