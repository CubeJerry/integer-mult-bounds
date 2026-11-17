#!/usr/bin/env python3
"""Independent forced-source fanout and fresh four-facet information cut."""
from pathlib import Path
from collections import Counter
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
REVIEW_PIN='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
CASES=[('low-retention-corrections','c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe',False),
       ('proper-query-exports','4d4e0a4163483d35741505c747981a2bc8b8da1bc373bb0cb8d10f0aa651f96c',True)]

def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b

def residual(x,b):
    for p in sorted(b,reverse=True):
        if x>>p&1:x^=b[p]
    return x

def dual_for(rows,target):
    b=basis(rows);r=residual(target,b);assert r
    p=r.bit_length()-1
    d=sum(((residual(1<<j,b)>>p)&1)<<j for j in range(111))
    assert (d&target).bit_count()%2==1 and all((d&v).bit_count()%2==0 for v in rows)
    return d

def record(interval):
    with localcontext()as c:
        c.prec=55
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--inputs',type=Path,default=BASE/'workers/A')
    ap.add_argument('--forced',type=Path,default=BASE/'workers/C/forced-raw-reactivation/output/CERTIFICATE.json')
    ap.add_argument('--source-review',type=Path,default=BASE/'workers/C/proper-query-export-review/check.py')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(a.source_review.read_bytes()).hexdigest()==REVIEW_PIN
    s=importlib.util.spec_from_file_location('independent_source_review',a.source_review)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.geo=m.load_arithmetic(a.arithmetic)
    raw=a.native.read_bytes();assert hashlib.sha256(raw).hexdigest()==NATIVE
    R=json.loads(raw)['native_roots'];xmask=(1<<111)-1
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    K=[(1<<i)^sum(1<<j for j in N[i])for i in range(111)]
    fraw=a.forced.read_bytes();forced=json.loads(fraw)
    _,correction,_=m.derive(R,json.loads((a.inputs/'proper-query-exports/WORD.json').read_text()))
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));cases=[]
    U=[8,9,14,15];umask=sum(1<<i for i in U)
    assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in U for j in U)
    for name,pin,sign in CASES:
        raw=(a.inputs/name/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        w=json.loads(raw);charts={n:m.geo.chart(c)for n,c in w['charts'].items()}
        stats,V,P=m.replay(w,charts,correction,check_cut=False)
        E=[i for i in range(111)if len(charts[P[f'X{i}']])>1];assert len(E)==40 and not(set(E)&set(U))
        ground=[i for i in range(111)if not charts[P[f'Y{i}']]];assert ground==[4,5,6,7]
        D=[r&(~255 if sign else xmask)for r in correction];G=list(basis(K+D).values());assert len(G)==21
        fc=next(c for c in forced['cases']if c['source']==name);assert fc['word_sha256']==pin
        requirements={z['receiver']:z['forced_raw_coordinates']for z in fc['receiver_requirements']}
        locals={i:[V[n]&xmask for n in V if not n.startswith('NATIVE_')and m.geo.contained(charts[P[n]],charts[f'F{i}'])]for i in range(111)}
        fanout=[]
        for j in E:
            demanded=[i for i in range(111)if j in requirements[i]];chosen=[];rowbasis=()
            for i in demanded:
                trial=m.geo.basis(rowbasis+(tuple(R[i]),))
                if len(trial)>len(rowbasis):chosen.append(i);rowbasis=trial
            assert chosen and all(j in N[i]for i in chosen)
            witnesses=[]
            for i in chosen:
                eligible=sorted(set(E)&N[i]);obs=G+locals[i]+[1<<k for k in eligible if k!=j]
                dual=dual_for(obs,1<<i)
                assert (dual>>j)&1
                witnesses.append({'receiver':i,'dual_hex':hex(dual),'eligible_raw_coordinates':eligible})
            rank=len(rowbasis);assert rank in [6,7]
            if rank==7:assert m.geo.kernel(rowbasis)==charts[f'L{j}']
            fanout.append({'expired_role':j,'demand_normal_rank':rank,'independent_receiver_roles':chosen,
                           'normal_row_basis':[[str(x)for x in r]for r in rowbasis],
                           'dual_witnesses':witnesses,'minimum_native_line_departures':2 if rank==7 else 1})
        hist=Counter(z['demand_normal_rank']for z in fanout);assert dict(hist)=={7:39,6:1}
        assert [z['expired_role']for z in fanout if z['demand_normal_rank']==6]==[3]
        exits=sum(z['minimum_native_line_departures']for z in fanout);assert exits==79
        owned_up=exits-len(ground);assert owned_up==75
        inside=[n for n in V if any(m.geo.contained(charts[P[n]],charts[f'F{i}'])for i in U)]
        assert all(V[n]&umask==0 for n in inside)
        carrying=[n for n in V if V[n]&umask]
        assert set(carrying)=={f'X{i}'for i in U}|{f'NATIVE_{i}'for i in U}
        assert not(set(carrying)&set(inside))
        owned_down=len(U);moves=owned_up+owned_down;assert moves==79
        mandatory=dict(stats['movement_profile']);mandatory[1]+=moves
        assert all(1<=int(d)<=7 and c>=0 for d,c in mandatory.items())
        Q=m.geo.moment(stats['movement_profile']);lower=m.geo.moment(mandatory)
        excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>0
        cases.append({'source':name,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],
                      'global_bank':'canonical_plus_sign_queries'if sign else'canonical_plus_full_queries',
                      'fanout':fanout,'demand_rank_histogram':dict(hist),'minimum_native_line_departures':exits,
                      'maximum_public_line_departures':len(ground),'minimum_owned_upward_moves':owned_up,
                      'fresh_cut_roles':U,'fresh_cut_inside_field_count':len(inside),'fresh_cut_U_carriers':carrying,
                      'minimum_owned_downward_moves':owned_down,'minimum_total_future_owned_moves':moves,
                      'Q0':record(Q),'mandatory_profile':mandatory,'target_excess':record(excess)})
        print(name,'75 owned ascents +4 descents; strict target excess',excess[0])
    out={'status':'PASS_INDEPENDENT_FIXED_QUERY_BANK_FANOUT_EXCLUSION','native_sha256':NATIVE,
         'source_review_sha256':REVIEW_PIN,'forced_candidate_sha256':hashlib.sha256(fraw).hexdigest(),
         'cases':cases,'scope':'Fixed audited cut, monotone public routes, linear continuation and every future downward X payload in the stated C-plus-query bank. Owned turns are allowed and fully charged. New pair/other descending modes or public turns escape this theorem.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
