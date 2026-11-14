#!/usr/bin/env python3
"""Direct exact audit of the pinned PR7583 eight-row decoder; no source imports."""
from pathlib import Path
from fractions import Fraction as F
import json,gzip,hashlib,argparse
HERE=Path(__file__).resolve().parent
PAIRS=[(117,107),(114,106),(111,108),(104,110),(115,109),(112,119),(105,118),(116,113)]
PIN='4a91033b56fe23feb897b90e6259b33dfbe428ff07ad7ce511a73835074f2708'
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def dot(x,y):return(x&y).bit_count()%2
def basis(rows):
    P={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in P:x^=P[j]
            else:P[j]=x;break
    return list(P.values())
def qrank(rows):
    A=[list(map(F,r))for r in rows];i=0
    for j in range(len(A[0])):
        k=next((k for k in range(i,len(A))if A[k][j]),None)
        if k is None:continue
        A[k],A[i]=A[i],A[k];d=A[i][j];A[i]=[v/d for v in A[i]]
        for k in range(i+1,len(A)):
            d=A[k][j]
            if d:A[k]=[v-d*w for v,w in zip(A[k],A[i])]
        i+=1
    return i
def main(native,out):
    raw=(HERE/'source/lines120.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'PR exact data pin')
    data=json.loads(raw);U=data['labels'];G=data['gram'];n=104
    need(len(U)==120 and len(set(U))==120 and all(dot(q,q)for q in U),'distinct odd source labels')
    need(all(dot(U[i],U[j])==(G[i][j]+1)%2 for i in range(120)for j in range(120)),'every exact Gram/label parity entry')
    need(all(G[i][j]==G[j][i]for i in range(120)for j in range(120))and all(G[i][i]==2 for i in range(120)),'Gram symmetry and diagonal')
    need(hashlib.sha256(native.read_bytes()).hexdigest()==NATIVE,'actual native pin');W=json.loads(gzip.decompress(native.read_bytes()))
    qlive=[W['frames'][W['initial'][h]][0]for h in W['live']]
    need(len(set(qlive))==104 and set(qlive)==set(U[:n]),'all104 native labels match as distinct sets')
    native_by_label=dict(zip(qlive,W['live']));permutation=[qlive.index(q)for q in U[:n]]
    rows=[];ws=[];us=[]
    for d,s in PAIRS:
        c=G[d][s];need(c in(-1,1),'dual nonport pairing')
        w=[G[i][d]for i in range(n)];u=[G[i][s]*c for i in range(n)];ws.append(w);us.append(u)
        D=[i for i in range(n)if w[i]];S=[i for i in range(n)if u[i]]
        db=basis(U[i]for i in D);sb=basis(U[i]for i in S)
        pair=[sum(dot(U[i],U[j])<<k for k,j in enumerate(S))for i in D]
        need(len(D)==len(S)==52 and len(db)==len(sb)==8 and len(basis(pair))==7,'exact price7 asymmetric support')
        need(all(not dot(q,U[d])for q in db)and all(not dot(q,U[s])for q in sb),'actual source/deposit hyperplanes')
        need(len(basis(db+sb))==9 and dot(U[d],U[s])==0,'distinct dual hyperplanes')
        db2=basis(db+[q<<9 for q in db]);sb2=basis(sb+[q<<9 for q in sb])
        need(len(db2)==len(sb2)==16,'tensor row support span16')
        rows.append(dict(deposit_virtual=d,gather_virtual=s,deposit_normal=U[d],gather_normal=U[s],deposit_ports=D,gather_ports=S,
                         native_deposit_fields=[native_by_label[U[i]]for i in D],native_gather_fields=[native_by_label[U[i]]for i in S],
                         deposit_basis=db,gather_basis=sb,tensor_deposit_basis=db2,tensor_gather_basis=sb2))
    need(all(sum(ws[k][i]*us[k][j]for k in range(8))==G[i][j]for i in range(n)for j in range(n)),'rankone sum M=G/2 on all104 squared entries')
    need(all(i==j or not dot(U[i],U[j])or G[i][j]==0 for i in range(n)for j in range(n)),'decoder odd-cell zeroes')
    need(qrank(list(zip(*ws)))==qrank(list(zip(*us)))==8,'matrix and off-block rank8')
    for i in range(8):
        for j in range(i):
            need(len(basis(rows[i]['tensor_gather_basis']+rows[j]['tensor_gather_basis']))==18,'distinct gather spans fill ambient')
            need(len(basis(rows[i]['tensor_deposit_basis']+rows[j]['tensor_deposit_basis']))==18,'distinct deposit spans fill ambient')
    wrong=[sum(ws[k][i]*us[k][j]*(-1 if k==0 else 1)for k in range(8))for i in range(n)for j in range(n)]
    need(any(wrong[i*n+j]!=G[i][j]for i in range(n)for j in range(n)),'flipped dual scalar control')
    symmetric_prices=[len(basis([sum(dot(U[i],U[j])<<k for k,j in enumerate(r['deposit_ports']))for i in r['deposit_ports']]))for r in rows]
    need(symmetric_prices==[8]*8,'same-support Gram rows are price8 control')
    R=dict(status='PASS_PINNED_TENSOR_ROW_GEOMETRY',native_sha256=NATIVE,source_sha256=PIN,ports=n,tensor_ports=208,rows=rows,
      tensor_row_price=14,tensor_source_dimension=16,tensor_scatter_annihilator_dimension=2,off_block_rank=8,
      exact_decoder_entries=n*n,pr_to_native_live_permutation=permutation,all_distinct_gather_and_deposit_span_pairs_fill_ambient=True,
      wrong_sign_control=True,same_support_price8_control=True,
      scope='Exact scalar row-cover geometry and native-label identification; no actual h18 acquisition/delivery word.')
    out.write_text(json.dumps(R,indent=2,sort_keys=True)+'\n');print(json.dumps({k:R[k]for k in('status','tensor_ports','tensor_row_price','off_block_rank','scope')},sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('--out',type=Path,default=HERE/'ROWS.json');a=p.parse_args();main(a.native,a.out)
