#!/usr/bin/env python3
"""Independent literal replay of the joint A2-triple canonical/MDS source."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse
import copy
import hashlib
import json
import sympy as sp

ROOT = 'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            j = row.bit_length()-1
            if j in pivots:
                row ^= pivots[j]
            else:
                pivots[j] = row
                break
    return len(pivots)


def xor(rows):
    out = 0
    for row in rows:
        out ^= row
    return out


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def mul4(a, b):
    a0, a1, b0, b1 = a&1, a>>1, b&1, b>>1
    return (a0*b0 ^ a1*b1) | ((a0*b1 ^ a1*b0 ^ a1*b1)<<1)


def mulrows(c, rows):
    return [xor(rows[j] for j in range(2) if (mul4(c, 1<<j)>>i)&1)
            for i in range(2)]


class Geometry:
    def __init__(self, charts):
        self.bases = {}
        for name, desc in charts.items():
            rows = desc['rows']
            if desc['kind'] == 'ann':
                columns = sp.Matrix(rows).nullspace() if rows else list(sp.eye(8).columnspace())
            else:
                assert desc['kind'] == 'span'
                columns = sp.Matrix(rows).T.columnspace() if rows else []
            self.bases[name] = sp.Matrix.hstack(*columns) if columns else sp.zeros(8, 0)

    @lru_cache(None)
    def sub(self, a, b):
        return self.bases[b].row_join(self.bases[a]).rank() == self.bases[b].cols

    @lru_cache(None)
    def same(self, a, b):
        return self.sub(a, b) and self.sub(b, a)

    def dim(self, a):
        return self.bases[a].cols


def source_geometry(word,roots,geo):
    targets=(3,76,80)
    assert tuple(word['completed_native_roles'])==targets
    assert tuple(roots[80])==tuple(x-y for x,y in zip(roots[76],roots[3]))
    assert sp.Matrix([roots[i] for i in targets]).rank()==2
    for i in targets:
        assert geo.sub('CC',f'F{i}')
    assert geo.dim('CC')==6
    common=[];private={i:[] for i in targets};none=[]
    for j in range(111):
        adjacent=[i for i in targets if dot(roots[j],roots[i])==0]
        assert len(adjacent)!=2
        if len(adjacent)==3:common.append(j)
        elif adjacent:private[adjacent[0]].append(j)
        else:none.append(j)
    assert common==word['common_roles'] and len(common)==36 and none==list(targets)
    assert private=={int(i):v for i,v in word['private_roles'].items()}
    assert [len(private[i]) for i in targets]==[22,24,26]
    aggregate={(i,t):[0,0] for i in targets for t in range(4)}
    encoded={}
    supports={tuple(j for j,v in enumerate(r) if v) for r in roots if sum(v!=0 for v in r)==4}
    for i in targets:
        for t in range(4):
            c=f'C{i}_{t}';assert geo.dim(c)==6 and geo.sub(c,f'F{i}')
            desc=word['charts'][c];assert desc['kind']=='ann' and desc['rows'][0]==roots[i] and len(desc['rows'])==2
            q=desc['rows'][1];assert dot(q,q)==4 and abs(dot(roots[i],q))==2
            support=tuple(j for j,v in enumerate(q) if v)
            assert (len(support)==1 and abs(q[support[0]])==2) or (support in supports and all(abs(q[j])==1 for j in support))
        for j in private[i]:
            eligible=[t for t in range(4) if geo.sub(f'L{j}',f'C{i}_{t}')]
            assert len(eligible)>=2
            target,pair=word['private_assignments'][str(j)]
            assert target==i and len(pair)==len(set(pair))==2 and all(t in eligible for t in pair)
            a,b=pair;iv=mul4(a^b,a^b)
            left=[1<<(4*j+k) for k in range(2)]
            right=[1<<(4*j+2+k) for k in range(2)]
            for s,(t,c) in enumerate(((a,b),(b,a))):
                z=mulrows(mul4(iv,c),left);y=mulrows(iv,right)
                encoded[j,s]=[z[k]^y[k] for k in range(2)]
                for k in range(2):aggregate[i,t][k]^=encoded[j,s][k]
    held=[];pivot_at={}
    for i in targets:
        for t in range(4):
            j,s=word['private_pivots'][f'{i}:{t}']
            assert j in private[i] and word['private_assignments'][str(j)][1][s]==t
            for k in range(2):
                name=f'X{j}_{2*s+k}';held.append(name);pivot_at[name]=(i,t,k)
    assert len(held)==len(set(held))==24
    held=sorted(held,key=lambda n:(int(n[1:n.index('_')]),int(n.split('_')[1])))
    pivot_roles=sorted({int(n[1:n.index('_')]) for n in held})
    assert pivot_roles==[1,4,59,60,63,64]
    scalar=[sum(1<<j for j in range(111) if i==j or dot(roots[i],roots[j])==0) for i in range(111)]
    assert rank([sum(((r>>j)&1)<<q for q,j in enumerate(pivot_roles)) for r in scalar])==6
    return targets,common,private,aggregate,held,pivot_at


def coordinate_solver(rows):
    piv={}
    for i,row in enumerate(rows):
        c=1<<i
        while row:
            q=row.bit_length()-1
            if q in piv:row^=piv[q][0];c^=piv[q][1]
            else:piv[q]=(row,c);break
    assert len(piv)==444
    def solve(row):
        c=0
        while row:
            q=row.bit_length()-1;row^=piv[q][0];c^=piv[q][1]
        return c
    return solve


def replay(word,roots,geo,marks=True,invoice=True):
    targets,common,private,aggregate,held,pivot_at=source_geometry(word,roots,geo)
    xnames=[f'X{j}_{k}' for j in range(111) for k in range(4)]
    ynames=[f'Y{j}_{k}' for j in range(111) for k in range(4)]
    initial={n:1<<j for j,n in enumerate(xnames+ynames)};values=initial.copy()
    places={n:f'L{j//4}' for j,n in enumerate(xnames)}|{n:'zero' for n in ynames}
    owners=set();born=set();counts=Counter();profile=Counter();dirty=0
    fullC={(i,k):sum(1<<(4*j+k) for j in range(111) if i==j or dot(roots[i],roots[j])==0)
           for i in range(111) for k in range(4)}
    cspace=list(fullC.values());assert rank(cspace)==36
    cut_solver=None;seed_rows=[];transport=[];partial=[];events={};completed=[]
    at={v:k for k,v in word['milestones'].items()}
    hub_seed_reads=0;actual_queries=[];common_reads=Counter();preload_reads=Counter()
    def capture(step):
        nonlocal cut_solver
        if not marks or step not in at:return
        label=at[step]
        hub=[values[n] for n in xnames if geo.same(places[n],'Hub')]
        nowheld=[n for n in xnames if not geo.same(places[n],'Hub')]
        event={'Hub_X_rank':rank(hub),'held_originals':nowheld,
               'canonical_Hub_intersection':36+rank(hub)-rank(hub+cspace)}
        if label in ('joint_source_aggregate_cut','canonical36_at_ground_before_all_Y_moves'):
            assert nowheld==held and rank(hub)==420 and event['canonical_Hub_intersection']==12
            assert all(values[n]==initial[n] and geo.same(places[n],'zero') for n in ynames)
            d=[values[n] for n in held]
            assert rank(d)==24 and rank(hub+d)==444
            assert rank(cspace+d)==60
            for k in range(4):
                assert values[f'A{k}']==xor(initial[f'X{j}_{k}'] for j in common)
                assert geo.same(places[f'A{k}'],'CC')
            for n,(i,t,k) in pivot_at.items():
                assert values[n]==aggregate[i,t][k] and geo.same(places[n],f'C{i}_{t}')
        if label=='joint_source_aggregate_cut':
            rows=[values[n] for n in xnames];cut_solver=coordinate_solver(rows)
            invrows=[cut_solver(1<<j) for j in range(444)]
            for n in held:
                p=xnames.index(n);j=p//4
                col=sum(((row>>p)&1)<<q for q,row in enumerate(invrows))
                assert col and not(col&~(15<<(4*j)))
                assert [(row&col).bit_count()%2 for row in rows]==[int(q==p) for q in range(444)]
            event['all24_inverse_columns_actual_single_root_support_verified']=True
        if label=='canonical36_at_ground_before_all_Y_moves':
            selected=[int(s['canonical_row_hex'],16) for s in word['canonical_seeds']]
            assert len(selected)==rank(selected)==36 and rank(selected+cspace)==36
            hpos=[xnames.index(n) for n in held]
            projections=[]
            for q,(seed,row) in enumerate(zip(word['canonical_seeds'],selected)):
                assert seed['packet']==f'P{q}' and values[f'P{q}']==row and geo.same(places[f'P{q}'],'zero')
                coord=cut_solver(row)
                proj=sum(((coord>>p)&1)<<k for k,p in enumerate(hpos));projections.append(proj)
                expected_hub=[n for p,n in enumerate(xnames) if coord>>p&1 and n not in held]
                expected_held=[n for p,n in enumerate(xnames) if coord>>p&1 and n in held]
                assert seed['Hub_reads']==expected_hub and seed['direct_original_reads']==expected_held
            assert projections==[1<<j for j in range(24)]+[0]*12
            lengths=[]
            for witness in word['canonical_preload_witnesses']:
                i,k=witness['receiver'],witness['copy'];ids=witness['principal_indices'];lengths.append(len(ids))
                assert xor(selected[p] for p in ids)==fullC[i,k]
            assert lengths==[9,10,6,13,8,8,10,10,8,9,10,9] and sum(lengths)==110
            assert rank(seed_rows)==36 and rank(transport)==60 and rank(partial)==444
            event.update(ground_canonical_rank=36,completed_Hub_rank=36,completed_history_rank=60,
                         literal_partial_history_rank=444,held_projection_rank=24,
                         preload_witness_lengths=lengths)
        if label.startswith('actual_receiver_'):
            i=int(label.split('_')[2]);completed.append(i)
            for t in completed:
                for k in range(4):assert values[f'Y{t}_{k}']==initial[f'Y{t}_{k}']^initial[f'X{t}_{k}']
            event['simultaneously_completed_receivers']=completed[:]
        if label=='all_X_restored':
            assert all(values[n]==initial[n] and geo.same(places[n],'Hub') for n in xnames)
        events[label]=event
    for step,op in enumerate(word['operations']):
        capture(step);tag,n,*z=op;counts[tag]+=1
        if tag=='INIT':
            assert n not in values and n not in born and z[0] in geo.bases
            born.add(n);owners.add(n);values[n]=0;places[n]=z[0]
        elif tag=='ADD':
            m=z[0];assert n!=m and n in values and m in values
            assert geo.same(places[n],places[m]),('ADD location',step,op,places[n],places[m])
            values[m]^=values[n]
            if m.startswith('P'):
                partial.append(values[m])
                if geo.same(places[m],'Hub'):hub_seed_reads+=1
                else:transport.append(values[m]);actual_queries.append((n,m))
            if n.startswith('A') and m.startswith('Y'):common_reads[int(m[1:m.index('_')])]+=1
            if n.startswith('P') and m.startswith('Y'):
                assert geo.same(places[m],'zero');preload_reads[int(m[1:m.index('_')])]+=1
        elif tag=='MOVE':
            assert n in values and z[0] in geo.bases
            old,new=places[n],z[0]
            assert geo.sub(new,old) if n in owners else geo.sub(old,new),('MOVE direction',step,op,old)
            gap=abs(geo.dim(new)-geo.dim(old));assert gap>0;profile[gap]+=1
            if n.startswith('P'):
                partial.append(values[n]);transport.append(values[n])
                if geo.same(old,'Hub'):seed_rows.append(values[n])
            places[n]=new
        elif tag=='CLEAR':
            assert n in owners;dirty+=bool(values[n]);owners.remove(n);del values[n];del places[n]
        else:raise AssertionError(op)
    capture(len(word['operations']))
    assert not owners and born=={f'A{k}' for k in range(4)}|{f'P{q}' for q in range(36)}
    for j in range(111):
        for k in range(4):
            x,y=f'X{j}_{k}',f'Y{j}_{k}'
            assert values[x]==initial[x] and geo.same(places[x],'Hub'),('X endpoint',x)
            assert values[y]==initial[y]^(initial[x] if j in targets else 0) and geo.same(places[y],f'F{j}'),('Y endpoint',y)
    if invoice:
        assert counts==Counter(INIT=40,ADD=5012,MOVE=1416,CLEAR=40) and dirty==40
        assert profile==Counter({1:60,2:432,5:432,6:36,7:444,8:12})
        assert hub_seed_reads==3276 and len(actual_queries)==24
        assert common_reads==Counter({3:4,76:4,80:4})
        assert preload_reads==Counter({3:38,76:36,80:36})
    return {'columns':888,'completed_receivers':targets,'completed_physical_outputs':12,
            'counts':dict(counts),'profile':dict(sorted(profile.items())),'dirty_clears':dirty,
            'common_capture_inputs':36,'private_source_counts':[22,24,26],
            'actual_Hub_seed_reads':hub_seed_reads,'actual_direct_queries':len(actual_queries),
            'actual_common_reads':dict(common_reads),'actual_canonical_preloads':dict(preload_reads),
            'events':events,'completed_seed_rank':rank(seed_rows),'completed_history_rank':rank(transport),
            'literal_partial_history_rank':rank(partial)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA
    roots=json.loads(raw)['native_roots'];word=json.loads((a.source/'WORD.json').read_text());geo=Geometry(word['charts'])
    for j,r in enumerate(roots):
        assert word['charts'][f'L{j}']=={'kind':'span','rows':[r]}
        assert word['charts'][f'F{j}']=={'kind':'ann','rows':[r]}
    assert word['charts']['CC']=={'kind':'ann','rows':[roots[3],roots[76]]}
    out={'status':'INDEPENDENT_LITERAL_SHARED_A2_TRIPLE_MDS_PASS',
         'author_word_sha256':hashlib.sha256((a.source/'WORD.json').read_bytes()).hexdigest(),
         'author_proof_sha256':hashlib.sha256((a.source/'PROOF.md').read_bytes()).hexdigest(),
         'native_sha256':ROOT_SHA,'word':replay(word,roots,geo),'negative_controls':[]}
    def mutant(label,fn):
        bad=copy.deepcopy(word);fn(bad)
        try:replay(bad,roots,geo,marks=False,invoice=False)
        except (AssertionError,KeyError) as e:out['negative_controls'].append({'name':label,'rejected':True,'reason':str(e)[:180]})
        else:raise AssertionError(('mutant accepted',label))
    def replace(w,pred,new):
        q=next(q for q,o in enumerate(w['operations']) if pred(o));w['operations'][q]=new(w['operations'][q])
    mutant('wrong_held_query_bank',lambda w:replace(w,lambda o:o==['ADD','X1_0','P0'],lambda o:['ADD','X1_1','P0']))
    mutant('wrong_Hub_seed_bank',lambda w:replace(w,lambda o:o==['ADD','X0_0','P0'],lambda o:['ADD','X0_1','P0']))
    mutant('skip_actual_query_chart',lambda w:replace(w,lambda o:o[0]=='MOVE' and o[1]=='P0',lambda o:['MOVE','P0','zero']))
    mutant('wrong_shared_cache_capture',lambda w:replace(w,lambda o:o==['ADD','X0_0','A0'],lambda o:['ADD','X0_1','A0']))
    for target in (3,76,80):
        mutant(f'wrong_common_bank_at_{target}',lambda w,t=target:replace(w,lambda o:o==['ADD','A0',f'Y{t}_0'],lambda o:['ADD','A1',o[2]]))
        def remove_private(w,t=target):
            q=next(q for q,o in enumerate(w['operations']) if o[0]=='ADD' and o[1].startswith('X') and o[2].startswith(f'Y{t}_'))
            w['operations'].pop(q)
        mutant(f'missing_private_contribution_at_{target}',remove_private)
    mutant('wrong_new_canonical_basis_field',lambda w:replace(w,lambda o:o==['ADD','P0','Y3_0'],lambda o:['ADD','P1','Y3_0']))
    def remove_inverse(w):
        q=max(q for q,o in enumerate(w['operations']) if o[0]=='ADD' and o[1].startswith('X') and o[2].startswith('X'));w['operations'].pop(q)
    mutant('missing_shared_source_inverse',remove_inverse)
    def remove_clear(w):
        q=next(q for q,o in enumerate(w['operations']) if o==['CLEAR','A0']);w['operations'].pop(q)
    mutant('unretired_shared_cache',remove_clear)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['word']['counts'],len(out['negative_controls']))


if __name__=='__main__':main()


