#!/usr/bin/env python3
"""Independent dual certificates for every indispensable dormant coordinate."""
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

def annihilator(rows,target):
    b=basis(rows);r=residual(target,b)
    assert r
    p=r.bit_length()-1
    dual=sum(((residual(1<<j,b)>>p)&1)<<j for j in range(111))
    assert (dual&target).bit_count()%2==1
    assert all((dual&v).bit_count()%2==0 for v in rows)
    return dual

def record(interval):
    with localcontext()as c:
        c.prec=55
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--inputs',type=Path,default=BASE/'workers/A')
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
    reviewed=json.loads((a.inputs/'proper-query-exports/WORD.json').read_text())
    _,correction,_=m.derive(R,reviewed)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate))
    assert m.geo.root_interval(6)[0]>2
    cases=[]
    for name,pin,sign in CASES:
        raw=(a.inputs/name/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        w=json.loads(raw);charts={n:m.geo.chart(c)for n,c in w['charts'].items()}
        stats,V,P=m.replay(w,charts,correction,check_cut=False)
        E=[i for i in range(111)if len(charts[P[f'X{i}']])>1]
        assert len(E)==40 and all(V[f'NATIVE_{i}']==1<<i and P[f'NATIVE_{i}']==f'L{i}'for i in range(111))
        ground=[i for i in range(111)if not charts[P[f'Y{i}']]];assert ground==[4,5,6,7]
        D=[r&(~255 if sign else xmask)for r in correction]
        G=list(basis(K+D).values());assert len(G)==21 and len(basis(D))==12
        all_forced=set();cover={};receiver_rows=[]
        for i in range(111):
            eligible=sorted(set(E)&N[i])
            visible=[n for n in V if not n.startswith('NATIVE_')and m.geo.contained(charts[P[n]],charts[f'F{i}'])]
            L=[V[n]&xmask for n in visible];observation=G+L
            quotient=basis(observation);target=residual(1<<i,quotient)
            cols={j:residual(1<<j,quotient)for j in eligible}
            forced=[j for j in eligible if residual(target,basis(cols[k]for k in eligible if k!=j))]
            # This check proves sufficiency of the forced set too: every feasible
            # raw grant is exactly an arbitrary superset of this indispensable set.
            assert residual(1<<i,basis(observation+[1<<j for j in forced]))==0
            assert forced
            for j in forced:
                all_forced.add(j)
                if j not in cover:
                    constraints=observation+[1<<k for k in eligible if k!=j]
                    dual=annihilator(constraints,1<<i)
                    assert (dual>>j)&1
                    cover[j]={'expired_role':j,'witness_receiver':i,'dual_hex':hex(dual),
                              'eligible_raw_coordinates':eligible,'observation_rank':len(quotient),
                              'other_raws_granted_rank':len(basis(constraints))}
            receiver_rows.append({'receiver':i,'forced_raw_coordinates':forced,'minimum_raw_coordinates':len(forced),
                                  'eligible_raw_coordinates':eligible,'visible_initial_fields':visible})
        assert all_forced==set(E)and len(cover)==40
        # Independent short dual verification, without reusing the discovery basis.
        for j,z in cover.items():
            i=z['witness_receiver'];d=int(z['dual_hex'],16)
            visible=receiver_rows[i]['visible_initial_fields']
            assert (d>>i)&1 and(d>>j)&1
            assert all((d&v).bit_count()%2==0 for v in G+[V[n]&xmask for n in visible])
            assert all(not(d>>k&1)for k in z['eligible_raw_coordinates']if k!=j)
        hist=dict(sorted(Counter(len(z['forced_raw_coordinates'])for z in receiver_rows).items()))
        departures=len(E)-len(ground);assert departures==36
        ranks=Counter(len(charts[P[f'X{i}']])for i in range(111));assert sum(ranks.values())==111
        dp={1:111}
        for r,c in ranks.items():dp[7-r]=dp.get(7-r,0)+c;dp[8-r]=dp.get(8-r,0)-c
        delta=m.geo.moment(dp);Q=m.geo.moment(stats['movement_profile'])
        threshold=(111+ceiling[0]-Q[1]-delta[1]-departures,111+ceiling[1]-Q[0]-delta[0]-departures)
        cap=139 if sign else 151;assert cap<threshold[0]<=threshold[1]<cap+1
        cases.append({'source':name,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],
                      'global_bank':'canonical_plus_sign_queries'if sign else'canonical_plus_full_queries',
                      'global_rank':21,'expired_roles':E,'ground_Y_roles':ground,'forced_union':sorted(all_forced),
                      'exact_minimum_raw_histogram':hist,'duals':[cover[j]for j in sorted(cover)],
                      'receiver_requirements':receiver_rows,'owned_upward_departure_lower_bound':departures,
                      'priced_fitting_strict_threshold':record(threshold),'priced_fitting_integer_cap':cap})
        print(name,'all40 individually forced; upward departures>=36; conditional priced fitting cap',cap)
    out={'status':'PASS_INDEPENDENT_ALL40_FORCED_RAW_COORDINATES','native_sha256':NATIVE,'source_review_sha256':REVIEW_PIN,
         'cases':cases,'scope':'Monotone public continuation; every future descending X payload belongs to the stated common global bank. Exact local observation relaxation grants arbitrary Y coefficients and global access to that bank. No general-source impossibility or free raw reactivation.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
