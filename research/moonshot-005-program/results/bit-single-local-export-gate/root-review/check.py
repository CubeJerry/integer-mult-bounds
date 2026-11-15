#!/usr/bin/env python3
"""Independent dual verification and quotient geometry by rational nullspaces."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
import sympy as S

def parity(a,b):return (a&b).bit_count()%2
def combine(rows,tag):
    r=0
    for i,x in enumerate(rows):
        if tag>>i&1:r^=x
    return r
def rank(rows):
    piv={}
    for r in rows:
        while r:
            k=(r&-r).bit_length()-1
            if k in piv:r^=piv[k]
            else:piv[k]=r;break
    return len(piv)
def replay(word):
    r={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    for o in word['operations']:
        if o[0]=='INIT':r[o[1]]=0
        elif o[0]=='ADD':r[o[2]]^=r[o[1]]
        elif o[0]=='CLEAR':del r[o[1]]
    return r
def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--certificate',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args()
    p=args.repo/'research/moonshot-005-program';cert=json.loads(args.certificate.read_text())
    for f,h in cert['source_pins'].items():assert hashlib.sha256((p/f).read_bytes()).hexdigest()==h
    roots=json.loads((p/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_text())['native_roots']
    vectors=[S.Matrix(r)for r in roots]
    outside=[sum(1<<j for j,s in enumerate(vectors)if (r.T*s)[0]!=0)for r in vectors]
    summaries={}
    for mode,variant in cert['variants'].items():
        word=json.loads((p/f'results/bit-coupled-singular-delivery/worker-a/two-receiver-output/{mode}-WORD.json').read_text());values=replay(word)
        G=[values[f'P{i}']for i in range(8)]+[1<<j for j in[16,19,38,49,50,56,57]]
        assert rank(G)==15
        missing=[i for i in range(111)if i not in[17,34]and rank([g&outside[i]for g in G]+[1<<i])>rank([g&outside[i]for g in G])]
        assert len(missing)==100
        rows=variant['chart_certificates']
        stats=Counter();exception=None
        assert sorted(row['source_chart']for row in rows)==sorted({v['chart']for n,v in word['expected_owned_at_handoff'].items()if n.startswith(('DC','SC'))})
        for row in rows:
            name=row['source_chart'];normals=S.Matrix(word['charts'][name]['rows']);basis=normals.nullspace()
            local=sum(1<<i for i,r in enumerate(vectors)if normals*r==S.zeros(normals.rows,1))
            assert row['source_local_indices']==[i for i in range(111)if local>>i&1]
            groups={};inside=[]
            for i in missing:
                signature=tuple((v.T*vectors[i])[0]for v in basis)
                first=next((q for q in signature if q!=0),None)
                if first is None:inside.append(i)
                else:groups.setdefault(tuple(q/first for q in signature),[]).append(i)
            assert inside==row['inside_source_normal_span']
            assert sorted(groups.values())==sorted(g['reachable_missing_roles']for g in row['groups'])
            excluded={int(i):int(q,16)for i,q in row['excluded_receiver_duals'].items()}
            possible={int(i):v for i,v in row['possible_receiver_witnesses'].items()}
            assert set(excluded)|set(possible)==set(missing)and not set(excluded)&set(possible)
            for i,q in excluded.items():
                assert q>>i&1 and not q&~(outside[i]&~local)and all(not parity(g,q)for g in G)
                stats['individual_duals']+=1
            for i,w in possible.items():
                z=int(w['payload_hex'],16);l=int(w['local_correction_hex'],16);g=combine(G,w['G_combination_bits'])
                assert z and not z&~local and not l&outside[i] and (1<<i)==g^z^l
                stats['positive_payloads']+=1
            for group in row['groups']:
                good=sorted(set(group['reachable_missing_roles'])&set(possible))
                assert good==group['individually_possible_roles']
                stats[f'groups_{len(good)}']+=1
                if len(good)>1:
                    assert name=='D4'and good==[2,13]and exception is None
                    exception=(local,G,outside)
        assert exception is not None
        local,G,outs=exception
        q2=sum(1<<i for i in[2,85,89,92,94,95]);q13=sum(1<<i for i in[2,85,89,92,100,102]);u13=int('5412a000000000000000002000',16)
        assert q2>>2&1 and not(q13>>13&1)and u13>>13&1
        for q,i in[(q2,2),(q13,13),(u13,13)]:assert not q&~outs[i]and all(not parity(g,q)for g in G)
        assert q2&local==q13&local==sum(1<<i for i in[85,89,92])
        assert stats['groups_2']==1 and sum(stats[f'groups_{i}']for i in range(3))==1774
        summaries[mode]=dict(stats)
    result={'status':'PASS_INDEPENDENT_SOURCE_LOCAL_EXPORT_GATE','certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),'variants':summaries,'method':'Rational nullspace evaluation for projective quotient groups, independent least-bit GF2 elimination, explicit source replay and every supplied dual/payload identity. Universal block argument separately reviewed.','new_complete_kappa':False}
    args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
