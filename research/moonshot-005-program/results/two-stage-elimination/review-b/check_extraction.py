#!/usr/bin/env python3
"""Independent exact noncommutative control of the two-stage extraction."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def mm(A,B):return [[sum(a*b for a,b in zip(row,col))for col in zip(*B)]for row in A]
def neg(A):return [[-a for a in row]for row in A]
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def inv(A):
    n=len(A);W=[list(map(F,row))+unit for row,unit in zip(A,eye(n))]
    for j in range(n):
        k=next(i for i in range(j,n)if W[i][j]);W[j],W[k]=W[k],W[j]
        c=W[j][j];W[j]=[x/c for x in W[j]]
        for i in range(n):
            if i!=j:
                c=W[i][j];W[i]=[x-c*y for x,y in zip(W[i],W[j])]
    return [row[n:]for row in W]
def blk(A,B,C,D):return [a+b for a,b in zip(A,B)]+[c+d for c,d in zip(C,D)]
def main(out):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins'];need(hashlib.sha256((HERE/'source/ROOT-PROOF.md').read_bytes()).hexdigest()==pins['source/ROOT-PROOF.md'],'reviewed proof pin')
    a=[[F(1),F(1)],[F(0),F(1)]];b=[[F(1),F(0)],[F(2),F(1)]]
    D1=[[F(2),F(1)],[F(1),F(1)]];D2=[[F(1),F(2)],[F(0),F(1)]]
    I=eye(2);Z=[[F(0)]*2 for _ in range(2)];U=lambda x:blk(I,x,Z,I);L=lambda x:blk(I,Z,x,I);delta=lambda x:blk(x,Z,Z,x)
    c=mm(mm(mm(inv(b),D1),inv(a)),inv(D1));d=mm(mm(D2,inv(b)),inv(D2))
    F1=mm(delta(D1),U(a));F2=mm(delta(D2),L(neg(b)));swap=blk(Z,neg(I),I,Z)
    whole=mm(swap,mm(U(d),mm(F2,mm(blk(c,Z,Z,I),F1))))
    want=blk(mm(mm(D2,D1),inv(a)),Z,Z,mm(mm(D2,inv(b)),D1))
    need(whole==want,'all four independent scalar columns under noncommuting2x2 blocks')
    need(mm(a,b)!=mm(b,a)and mm(D1,a)!=mm(a,D1)and mm(D2,b)!=mm(b,D2),'genuine noncommuting controls')
    wrongc=mm(mm(mm(D1,inv(b)),inv(a)),inv(D1));wrongd=inv(b)
    badc=mm(swap,mm(U(d),mm(F2,mm(blk(wrongc,Z,Z,I),F1))))
    badd=mm(swap,mm(U(wrongd),mm(F2,mm(blk(c,Z,Z,I),F1))))
    need(badc!=want and badd!=want,'wrong c order and dropped d conjugation rejected')
    enc=lambda A:[[str(x)for x in row]for row in A]
    r={'status':'PASS_INDEPENDENT_NONCOMMUTING_EXTRACTION_CONTROL','root_proof_sha256':pins['source/ROOT-PROOF.md'],
       'all4_original_columns':True,'a':enc(a),'b':enc(b),'D1':enc(D1),'D2':enc(D2),'c':enc(c),'d':enc(d),'actual_endpoint':enc(whole),
       'wrong_c_order_rejected':True,'dropped_d_conjugation_rejected':True,'universal_claim_requires_algebraic_proof':True,'new_kappa':False}
    out.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'EXTRACTION.json');a=p.parse_args();main(a.output)
