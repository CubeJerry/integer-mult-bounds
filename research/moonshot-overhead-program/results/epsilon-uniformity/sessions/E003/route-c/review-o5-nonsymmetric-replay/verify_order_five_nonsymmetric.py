#!/usr/bin/env python3
"""Exact all-gate checks of the nonsymmetric converter-word extension."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent

def field(q,modulus):
    def mul(a,b):
        value=0
        while b:
            if b&1:value^=a
            a<<=1
            if a&q:a^=modulus
            b>>=1
        return value
    table=[[mul(a,b) for b in range(q)] for a in range(q)]
    inverse=[0]+[next(b for b in range(1,q) if table[a][b]==1) for a in range(1,q)]
    def mm(a,b):
        return (table[a[0]][b[0]]^table[a[1]][b[2]],
                table[a[0]][b[1]]^table[a[1]][b[3]],
                table[a[2]][b[0]]^table[a[3]][b[2]],
                table[a[2]][b[1]]^table[a[3]][b[3]])
    return table,inverse,mm

def inspect(q,modulus):
    mul,inv,mm=field(q,modulus)
    def diag(s,t):return (s,0,0,t)
    def order(a):
        x=1
        for n in range(1,q):
            x=mul[x][a]
            if x==1:return n
        raise AssertionError('nonzero element lacks order')
    def equivalent(c,s):
        if any(bool(x)!=bool(y) for x,y in zip(c,s)):return False
        for a1 in range(1,q):
            factors=[]
            for j in range(2):
                if c[j]:factors.append(mul[s[j]][inv[c[j]]])
                else:factors.append(mul[s[2+j]][inv[mul[a1][c[2+j]]]])
            if mm(mm(diag(1,a1),c),diag(*factors))==s:return True
        return False
    totals={'q':q,'ordered_split_gates':0,'one_converter_gates':0,
            'nontriangular_converters':0,'triangular_converters':0,
            'joint_gates':0,'joint_nonsymmetric':0,'diagonal_word_trials':0,
            'one_converter_eigenvalue_orders':{},'nontriangular_orders':{}}
    for lam in range(2,q):
        mu=inv[lam];tau=lam^mu
        assert tau
        for a in range(q):
            d=tau^a
            for b in range(q):
                for c in range(q):
                    z=mul[b][c]
                    if mul[a][d]^z!=1:continue
                    totals['ordered_split_gates']+=1
                    gate=(a,b,c,d)
                    columns=[]
                    for eigen in (lam,mu):
                        if b:columns.append((1,mul[eigen^a][inv[b]]))
                        elif eigen==a:columns.append((1,mul[c][inv[tau]]))
                        else:columns.append((0,1))
                    basis=(columns[0][0],columns[1][0],columns[0][1],columns[1][1])
                    assert mm(gate,basis)==mm(basis,diag(lam,mu))
                    assert mul[basis[0]][basis[3]]^mul[basis[1]][basis[2]]
                    converter=equivalent(gate,basis)
                    classified=(a==mul[mul[mu][mu]][inv[tau]] and
                                d==mul[mul[lam][lam]][inv[tau]] and
                                z==mul[mul[tau][tau]^1][inv[mul[tau][tau]]])
                    if z:assert converter==classified
                    aa=mul[a][mul[tau][a]^1];dd=mul[d][mul[tau][d]^1]
                    cross=mul[tau][z]
                    assert mul[aa][dd]^mul[cross][cross]==1^mul[z][mul[tau][tau]^1]
                    if not converter:continue
                    totals['one_converter_gates']+=1
                    o=order(lam)
                    totals['one_converter_eigenvalue_orders'][o]=totals['one_converter_eigenvalue_orders'].get(o,0)+1
                    if z:
                        totals['nontriangular_converters']+=1
                        totals['nontriangular_orders'][o]=totals['nontriangular_orders'].get(o,0)+1
                        beta=mul[tau^1][inv[tau]];g=mul[beta][inv[b]]
                        assert g and mm(mm(diag(g,1),gate),diag(inv[g],1))==(a,beta,beta,d)
                    else:totals['triangular_converters']+=1
                    square=mm(gate,gate);swap_exists=False
                    for s in range(1,q):
                        for t in range(1,q):
                            totals['diagonal_word_trials']+=1
                            word=mm(mm(gate,diag(s,t)),square)
                            if word[0]==word[3]==0:
                                assert word[1] and word[2]
                                assert mm(diag(inv[word[1]],inv[word[2]]),word)==(0,1,1,0)
                                swap_exists=True
                    prediction=(o==5 and a==mul[mul[mu][mu]][inv[tau]] and
                                d==mul[mul[lam][lam]][inv[tau]] and z==mul[tau][tau])
                    assert swap_exists==prediction
                    if not z:assert not swap_exists
                    totals['joint_gates']+=swap_exists
                    totals['joint_nonsymmetric']+=bool(swap_exists and b!=c)
    return totals

def main():
    results=[inspect(4,0b111),inspect(8,0b1011),inspect(16,0b10011)]
    assert [x['ordered_split_gates'] for x in results]==[40,432,3808]
    assert [x['nontriangular_converters'] for x in results]==[0,42,180]
    assert [x['joint_gates'] for x in results]==[0,0,60]
    assert results[2]['joint_nonsymmetric']==56
    controls={
        'triangular_one_converters_do_exist':all(x['triangular_converters']>0 for x in results),
        'one_converter_does_not_force_order_five':7 in results[1]['nontriangular_orders'] and 15 in results[2]['nontriangular_orders'],
        'joint_gates_need_not_be_symmetric':results[2]['joint_nonsymmetric']>0,
        'no_order_five_in_F4_or_F8':results[0]['joint_gates']==results[1]['joint_gates']==0,
    }
    assert all(controls.values())
    receipt={'status':'passed','fields':results,'negative_controls':controls,
             'scope':'Finite exact all-gate checks; universal classification uses the companion proof.',
             'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                       [Path(__file__).name,'order-five-nonsymmetric-extension.md']}}
    (ROOT/'order-five-nonsymmetric-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
