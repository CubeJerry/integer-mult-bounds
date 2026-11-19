#!/usr/bin/env python3
"""Independent forward-equation/binary-rank review of the donor gauge witness."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import gzip,json

PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','partition':'2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25','source':'362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af'}

def read(path,key):
    raw=gzip.decompress(path.read_bytes());assert sha256(raw).hexdigest()==PINS[key];return json.loads(raw)

def mul(a,b):
    p=0
    for bit in range(5):
        if(b>>bit)&1:p^=a<<bit
    for bit in range(8,4,-1):
        if(p>>bit)&1:p^=0x25<<(bit-5)
    return p

M=[[mul(a,b)for b in range(32)]for a in range(32)]
def power(a,n):
    out=1
    for _ in range(n):out=M[out][a]
    return out

def b_rank(values):
    piv={}
    for value in values:
        v=value
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p]
            else:piv[p]=v;break
    return len(piv)

def expanded(vectors):
    result=[]
    for row in vectors:
        for bit in range(5):
            result.append(sum(M[1<<bit][x]<<(5*k)for k,x in enumerate(row)))
    return result

def dot(row,col):
    out=0
    for x,y in zip(row,col):out^=M[x][y]
    return out

def mm(A,B):
    return [[dot(row,col)for col in zip(*B)]for row in A]

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--triangle',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    L=read(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout');P=read(base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz','partition')['classes'];S=read(a.triangle/'output/ALL-CLASSES-SOURCE.json.gz','source')
    raw=gzip.decompress((a.author/'output/WITNESS.json.gz').read_bytes());W=json.loads(raw)
    R=L['root_table'];H=list(map(set,L['A2']));D=list(map(set,L['D4']));O=[{j for j,v in enumerate(R)if sum(x*y for x,y in zip(u,v))==0}for u in R]
    source={(c,j,h):v for c,j,h,v in S['source_maps']};receivers=[33,80,95];donors=[29,36,77]
    vis={(i,j):[h for h,U in enumerate(H)if j in U and U<=O[i]]for i in receivers for j in donors}
    V=[[power(t,k)for k in range(9)]for t in range(1,10)]
    forward={};portlists={};blocks={};full_rank_checks=0
    for i in receivers:
        for j in donors:
            assert len(vis[i,j])==16
            for c in range(5):
                rows=[]
                for h in vis[i,j]:
                    allports=P[str(h)][c];selected=[k for k,d in enumerate(allports)if D[d]<=O[i]]
                    assert len(selected)==3 and max(H[h])<111
                    g=sorted(H[h]).index(j)
                    A=[[V[k][t]for t in range(3*g,3*g+3)]for k in selected]
                    F=mm(A,source[c,j,h]);rows+=F;blocks[i,j,c,h]=F
                    portlists[i,c,h]=[allports[k]for k in selected]
                assert len(rows)==48 and b_rank(expanded(rows))==240
                forward[i,j,c]=rows;full_rank_checks+=1
    # No inverse is recomputed or trusted: every emitted column solves its forward unit equation.
    unit_checks=0;individual_cut_ranks=[]
    for j in [29,36]:
        cols=W['lift_columns'][str(j)];labels=W['column_labels'][str(j)]
        assert len(cols)==len(labels)==72
        for col,label in zip(cols,labels):
            i=label['receiver'];d=label['middle'];h,c,at=label['port']
            assert (i,d) in map(tuple,W['cuts']) and j in H[h] and H[h]<=D[d] and D[d]<=O[i]
            assert portlists[i,c,h][at]==d
            assert len(col)==240 and all(x==0 for k,x in enumerate(col)if not 48*c<=k<48*(c+1))
            local=col[48*c:48*(c+1)];expected=3*vis[i,j].index(h)+at
            values=[dot(row,local)for row in forward[i,j,c]]
            assert values==[int(k==expected)for k in range(48)];unit_checks+=1
        for start in range(0,72,4):
            rr=b_rank(expanded(cols[start:start+4]));assert rr==20;individual_cut_ranks.append(rr)
    ranks=[b_rank(expanded(W['lift_columns'][str(j)]))for j in [29,36]];assert ranks==[360,355]
    # Surjectivity uses the real common original source domain, not invented plane inputs.
    boundary_ranks=[]
    for i in receivers:
        hs=sorted({h for j in donors for h in vis[i,j]});assert len(hs)==45
        for c in range(5):
            rows=[]
            for h in hs:
                B=[[0]*144 for _ in range(3)]
                for at,j in enumerate(donors):
                    if j in H[h]:
                        for r in range(3):B[r][48*at:48*(at+1)]=blocks[i,j,c,h][r]
                rows+=B
            rank=b_rank(expanded(rows));assert rank==675;boundary_ranks.append(rank)
    for entry in W['actual_outgoing_flags']:
        i,d=entry['receiver'],entry['middle'];dual={j for j in range(120)if all(j in O[k]for k in D[d])}
        flags=[h for h,U in enumerate(H)if i in U and U<=dual]
        assert flags==entry['right_flags'] and len(flags)==4
    relation=W['donor36_relation'];assert len(relation)==72 and any(relation)
    combo=[dot(relation,col)for col in zip(*W['lift_columns']['36'])];assert not any(combo)
    cutrel=relation[:];k=next(k for k,x in enumerate(cutrel)if x);cutrel[k]=0
    assert any(dot(cutrel,col)for col in zip(*W['lift_columns']['36']))
    assert any(dot(relation,col)for col in zip(*W['lift_columns']['29']))
    # An incorrect lift coefficient fails the forward unit equation.
    col=W['lift_columns']['29'][0];label=W['column_labels']['29'][0];h,c,at=label['port'];i=label['receiver'];local=col[48*c:48*(c+1)];bad=local[:];bad[0]^=1
    assert [dot(row,bad)for row in forward[i,29,c]]!=[dot(row,local)for row in forward[i,29,c]]
    result={'status':'PASS_INDEPENDENT_DONOR_GAUGE_REVIEW','source_pins':PINS,'witness_decompressed_sha256':sha256(raw).hexdigest(),
      'source_forward_stacks_checked':full_rank_checks,'forward_unit_column_equations':unit_checks,
      'binary_union_ranks':ranks,'field_union_ranks':[72,71],'individual_cut_binary_ranks':individual_cut_ranks,
      'surjective_boundary_binary_ranks':boundary_ranks,'actual_four_flag_cuts':18,
      'controls':{'null_relation':True,'omitted_relation_term_rejected':True,'relation_fails_on_independent_side':True,'changed_lift_rejected':True},
      'author_code_imported_or_executed':False,'author_inverse_routine_used':False,'larger_60_and_45_cut_audits_rechecked':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status']);print('binary union ranks',ranks,'forward column checks',unit_checks)
if __name__=='__main__':main()
