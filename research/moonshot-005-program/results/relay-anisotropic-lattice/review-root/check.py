#!/usr/bin/env python3
"""Independent compositional review; never imports the source author's code."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip,hashlib,json
from pathlib import Path

OLD='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c'

def determinant(a):
    a=[list(map(F,row)) for row in a];d=F(1)
    for j in range(len(a)):
        k=next((i for i in range(j,len(a)) if a[i][j]),None)
        if k is None:return F(0)
        if k!=j:a[k],a[j]=a[j],a[k];d=-d
        v=a[j][j];d*=v
        for i in range(j+1,len(a)):
            f=a[i][j]/v
            a[i]=[x-f*y for x,y in zip(a[i],a[j])]
    return d

def root(v):
    if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
    assert v.bit_count()==7
    z=[i for i in range(9) if not(v>>i&1)]
    return [3*(int(i==z[0])-int(i==z[1])) for i in range(9)]

def run(repo,wordpath):
    oldraw=(repo/'research/moonshot-005-program/results/proper-chart-relay/author/20/WORD.json.gz').read_bytes()
    assert hashlib.sha256(oldraw).hexdigest()==OLD
    old=json.loads(gzip.decompress(oldraw));raw=wordpath.read_bytes();new=json.loads(gzip.decompress(raw))
    for key in ('public','frames','initial','owned_fields','source_role_map'):
        assert new[key]==old[key]
    assert new['public']==400
    assert new['program'][:432]==old['program'][:432]
    assert new['program'][454:]==old['program'][432:]
    # All new gates act on eight existing records at the literal ground chart.
    loc=dict(enumerate(old['initial']))
    for e in old['program'][:432]:
        if e[0]=='INIT':loc[e[1]]=e[2]
        elif e[0]=='CLEAR':del loc[e[1]]
        elif e[0]=='MOVE':
            assert loc[e[1]]==e[2]
            loc[e[1]]=e[3]
    assert all(loc[i]==3 for i in range(400,408)) and old['frames'][3]==[]
    insertion=new['program'][432:454]
    modes=[[F(i==j) for j in range(8)] for i in range(8)]
    for e in insertion:
        op,d=e[:2];assert 400<=d<408 and e[-1]==3
        if op=='SCALE':modes[d-400]=[F(e[2])*x for x in modes[d-400]]
        else:
            assert op=='ADD' and 400<=e[2]<408
            modes[d-400]=[x+F(e[3])*y for x,y in zip(modes[d-400],modes[e[2]-400])]
    desired=[[F(i==j,4) for j in range(8)] for i in range(8)]
    for i,j in ((0,2),(1,3)):
        desired[i][i]+=F(1,24);desired[j][j]+=F(1,24)
        desired[i][j]-=F(1,24);desired[j][i]-=F(1,24)
    assert modes==desired
    assert Counter(e[0] for e in insertion)=={'ADD':8,'SCALE':14}
    assert determinant(modes)==F(1,36864)
    rm={int(k):v for k,v in old['source_role_map'].items()}
    Z=[root(z) for z in old['relay']['ground_Gram_frame']]
    g={h:[F(sum(a*b for a,b in zip(root(old['frames'][old['initial'][rm[h]]][0]),z)),18) for z in Z] for h in rm if h<112}
    S=old['relay']['unrestored_ports'];T=old['relay']['restored_ports']
    B=[[sum(g[h][i]*g[h][j] for h in S) for j in range(8)] for i in range(8)]
    A=[[F(i==j)-sum(modes[i][k]*B[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
    assert determinant(A)==F(3375,128)
    # The same beta identities imply relay correctness for every matrix Lambda.
    beta=old['relay']['beta'];U=old['relay']['mode_ports']
    for h in T:
        coeff=beta[str(h)]
        assert all(sum(F(c)*g[u][j] for c,u in zip(coeff,U))==g[h][j] for j in range(8))
    return {'status':'PASS_INDEPENDENT_COMPOSITIONAL_SOURCE_REVIEW',
      'old_word_sha256':OLD,'new_word_sha256':hashlib.sha256(raw).hexdigest(),
      'literal_edit':'one22-gate insertion at432; all other executable events identical',
      'inserted_matrix':[[str(x) for x in row] for row in modes],
      'inserted_operations':dict(Counter(e[0] for e in insertion)),
      'restored_beta_identities_checked':len(T),'small_determinant':str(determinant(A)),
      'old_chart_phase_proof_inherited_by_literal_identity':True,
      'remaining_D':76,'forward_completed':0,'new_kappa':False,
      'scope':'Independent exact inserted matrix, actual ground availability, relay identities and determinant. Full400-input replay is author evidence. Forward sparsity and full price are separate obligations.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=run(a.repo.resolve(),a.word.resolve());a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='inserted_matrix'},sort_keys=True))
