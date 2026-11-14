#!/usr/bin/env python3
"""Literal arbitrary-input dyadic112-port R0 ordinary bank codec."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def add(a,b,c):
    out=a.copy()
    for j,v in b.items():
        z=out.get(j,F(0))+c*v
        if z:out[j]=z
        else:out.pop(j,None)
    return out
def main(out):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for p,z in pins.items():need(hashlib.sha256((HERE/p).read_bytes()).hexdigest()==z,'pin '+p)
    w=json.loads(gzip.decompress((HERE/'source/R0.json.gz').read_bytes()));d=w['logical_involution'];P=d['ports'];ix={h:i for i,h in enumerate(P)}
    R={int(h):{int(j):F(v)for j,v in row.items()}for h,row in d['R_rows'].items()};ops=[];factorizations=[]
    def hadamard(fields,C):
        W=[[2*x for x in row]for row in C];cs=W[0];rs=[row[0]*cs[0]for row in W]
        V=[[rs[i]*W[i][j]*cs[j]for j in range(4)]for i in range(4)]
        H=[[F((-1)**((i&j).bit_count()%2))for j in range(4)]for i in range(4)]
        perm=[H.index(row)for row in V];need(len(set(perm))==4,'actual signed Hadamard factor')
        for j,c in enumerate(cs):
            if c==-1:ops.append(['SCALE',fields[j],'-1'])
        for bit in(1,2):
            for i in range(4):
                if not i&bit:
                    a,b=fields[i],fields[i|bit];ops.extend([['ADD',a,b,'1'],['SCALE',b,'-2'],['ADD',b,a,'1']])
        for f in fields:ops.append(['SCALE',f,'1/2'])
        labels=list(range(4))
        for i,j in enumerate(perm):
            k=labels.index(j)
            if k!=i:ops.append(['SWAP',fields[i],fields[k]]);labels[i],labels[k]=labels[k],labels[i]
        for i,c in enumerate(rs):
            if c==-1:ops.append(['SCALE',fields[i],'-1'])
        factorizations.append({'fields':fields,'column_signs':list(map(str,cs)),'row_signs':list(map(str,rs)),'output_row_permutation':perm})
    for c in range(14):
        records=[h for h in d['halves']if h['class']==c];need(len(records)==2,'both authentic halves')
        T=records[0]['ports'];S=records[0]['sources'];need(records[1]['ports']==S and records[1]['sources']==T,'actual opposite cohorts')
        C=[[R[h][j]for j in S]for h in T]
        for h,j in zip(T,S):ops.append(['SWAP',ix[h],ix[j]])
        hadamard([ix[h]for h in T],C);hadamard([ix[h]for h in S],[list(row)for row in zip(*C)])
    def replay(program):
        rows=[{i:F(1)}for i in range(112)]
        for op in program:
            if op[0]=='SWAP':_,a,b=op;rows[a],rows[b]=rows[b],rows[a]
            elif op[0]=='SCALE':_,a,c=op;need(F(c)!=0,'no erasure scale');rows[a]={j:F(c)*v for j,v in rows[a].items()}
            elif op[0]=='ADD':_,a,b,c=op;need(a!=b,'distinct ordinary fields');rows[a]=add(rows[a],rows[b],F(c))
            else:raise ValueError('unexpected primitive')
        return rows
    want=[{ix[j]:v for j,v in R[h].items()}for h in P];need(replay(ops)==want,'all112 arbitrary original codec inputs')
    bad=[op.copy()for op in ops];k=next(k for k,op in enumerate(bad)if op[0]=='ADD');bad[k][3]='-1';need(replay(bad)!=want,'wrong butterfly sign rejected')
    counts=Counter(op[0]for op in ops);need(counts['ADD']==224,'complete Walsh butterfly count')
    result={'status':'PASS_LITERAL_ORDINARY_R0_CODEC','ports':P,'public_fields':112,'owned_or_zero_fields':0,'opcodes':ops,
       'counts':dict(counts),'all112_original_inputs':True,'all12544_output_coefficients':True,'all28_signed_Hadamard_factors':factorizations,
       'allowed_nonzero_scales':['-2','-1','1/2'],'wrong_butterfly_sign_rejected':True,'source_pins':pins,
       'scope':'Caller ordinary coindexed-bank service, not native raw-chart access and not a Gaussian supplier.'}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(dict(counts))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'R0-CODEC.json');a=p.parse_args();main(a.output)
