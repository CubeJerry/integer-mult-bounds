#!/usr/bin/env python3
"""Independent mapped graph, rational entropy dual and five actual-cut audits."""
from pathlib import Path
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
OLD_CERT='c5d40e71246008699cb137eaa2badd2674253b0567c87e54fa7fa5809bacc79f'
OLD_REVIEW='582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23'
SOURCE_REVIEW='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
MAPPED='67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e'
CORE=[61,82,83,20,18,71,70,69,74,76,63];ISOLATES=[65,109,107]
EIGHT=[14,16,60,63,84,85,107,109];PERM=[0,5,1,4,3,6,2,7]
CASES=[('low-retention-corrections','c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe',268),
       ('proper-query-exports','4d4e0a4163483d35741505c747981a2bc8b8da1bc373bb0cb8d10f0aa651f96c',292),
       ('direct-pair-exports-4','33a07beacc3895822300eb34ebb847f5b9ff030cc2ad82cdfbc3152fe8402fc0',271),
       ('direct-pair-exports-12','6472eee72de969e204b546549fabdd9bd1cfaa5353ea8d4078b94d5ab1a44e05',277),
       ('direct-pair-exports-16','91cd623b23d299d44da5355838d5ead01614bc2ce6f2cf696a8d6500b73824c1',280)]

def load(path,pin,name):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def normalize(row):
    first=next(v for v in row if v)
    return tuple(v if first>0 else-v for v in row)

def record(interval):
    with localcontext()as c:
        c.prec=55
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--inputs',type=Path,default=BASE/'workers/A')
    ap.add_argument('--certificate',type=Path,default=BASE/'workers/R/entropy54/CERTIFICATE.json')
    ap.add_argument('--mapped',type=Path,default=BASE/'workers/R/fresh-transcript-nine/output/MAPPED-DUAL.json')
    ap.add_argument('--entropy-review',type=Path,default=BASE/'workers/C/entropy54-review/check.py')
    ap.add_argument('--source-review',type=Path,default=BASE/'workers/C/proper-query-export-review/check.py')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(a.native.read_bytes()).hexdigest()==NATIVE
    assert hashlib.sha256(a.certificate.read_bytes()).hexdigest()==OLD_CERT
    assert hashlib.sha256(a.mapped.read_bytes()).hexdigest()==MAPPED
    R=json.loads(a.native.read_text())['native_roots'];old=json.loads(a.certificate.read_text());mapped=json.loads(a.mapped.read_text())
    e=load(a.entropy_review,OLD_REVIEW,'own_entropy');m=load(a.source_review,SOURCE_REVIEW,'own_source')
    m.geo=m.load_arithmetic(a.arithmetic)
    original=e.review_dual(old,R)
    assert mapped['roles']==CORE and mapped['isolates']==ISOLATES
    for key in ['terms','adjacency_masks','core_bound','full_bound']:assert mapped[key]==old[key]
    old_roles=old['roles']+old['isolates'];new_roles=CORE+ISOLATES;mapping=[]
    for i,j in zip(old_roles,new_roles):
        v=[0]*8
        for k,x in enumerate(R[i]):v[PERM[k]]=(-x if k==0 else x)
        assert normalize(v)==normalize(R[j]);mapping.append({'old':i,'new':j})
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
    assert all((dot(i,j)==0)==(dot(u,v)==0)for i,u in zip(old_roles,new_roles)for j,v in zip(old_roles,new_roles))
    # The frozen independent verifier is parametrized only by new role labels
    # in memory; no dependency file is modified.
    e.CORE=CORE;e.ISO=ISOLATES
    exact=e.review_dual(mapped,R)
    assert exact['terms']==106 and exact['core_bound']=='11/2'and exact['full_bound']=='17/2'
    bad=json.loads(json.dumps(mapped));bad['terms'].pop()
    try:e.review_dual(bad,R)
    except ValueError as err:omission=str(err)
    else:raise AssertionError('missing rational dual term accepted')
    expired=set(range(8))|set(range(22,46))|set(range(88,96));fresh=sorted(set(range(111))-expired)
    assert len(fresh)==71 and set(new_roles+EIGHT)<=set(fresh)
    assert all(dot(i,j)!=0 for i in EIGHT for j in EIGHT)
    K=[(1<<i)^sum(1<<j for j in fresh if dot(i,j)==0)for i in fresh]
    assert len(m.binary_basis(K))==9
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));cases=[]
    fresh_mask=sum(1<<i for i in fresh);eight_mask=sum(1<<i for i in EIGHT)
    for name,pin,expected_inside in CASES:
        raw=(a.inputs/name/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        w=json.loads(raw);charts={n:m.geo.chart(c)for n,c in w['charts'].items()}
        stats,V,P=m.replay(w,charts,[int(v,16)for v in w['Y_correction_rows_hex']],check_cut=False)
        assert all(P[f'X{i}']==P[f'NATIVE_{i}']==f'L{i}'and V[f'X{i}']==V[f'NATIVE_{i}']==1<<i for i in fresh)
        def audit(values,places):
            checks=[]
            for i in fresh:
                neighbors=sum(1<<j for j in fresh if dot(i,j)==0)
                names=[n for n in values if m.geo.contained(charts[places[n]],charts[f'F{i}'])]
                assert f'Y{i}'in names
                leaks=[n for n in names if values[n]&fresh_mask&~neighbors]
                if leaks:raise ValueError('nonlocal initial fresh-input leak')
                checks.append({'receiver':i,'inside_fields':len(names)})
            return checks
        checks=audit(V,P)
        inside=[n for n in V if any(m.geo.contained(charts[P[n]],charts[f'F{i}'])for i in EIGHT)]
        assert len(inside)==expected_inside and all(not(V[n]&eight_mask)for n in inside)
        carrying=[n for n in V if V[n]&eight_mask]
        assert set(carrying)=={f'X{i}'for i in EIGHT}|{f'NATIVE_{i}'for i in EIGHT}
        assert not(set(carrying)&set(inside))
        planted=dict(V);places=dict(P);planted['LEAK_CONTROL']=1<<CORE[0];places['LEAK_CONTROL']='zero'
        try:audit(planted,places)
        except ValueError as err:leak_control=str(err)
        else:raise AssertionError('planted current leak accepted')
        profile=dict(stats['movement_profile']);profile[1]+=84
        lower=m.geo.moment(profile);excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>0
        cases.append({'source':name,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],'live_fields':len(V),
                      'fresh_receiver_checks':checks,'nonlocal_leaks':[],'eight_facet_region_count':len(inside),
                      'eight_input_carriers':carrying,'planted_leak_rejected':leak_control,
                      'bank_independent_future_descent_lower_bound':9,'conditional_75_plus_9_profile':profile,
                      'conditional_84_move_target_excess':record(excess)})
        print(name,'71 independent locality audits; eight-cut count',len(inside),'nine descents; conditional excess',excess[0])
    out={'status':'PASS_INDEPENDENT_MAPPED_NONLINEAR_WITNESS_AND_FIVE_CUTS','native_sha256':NATIVE,
         'prior_entropy_certificate_sha256':OLD_CERT,'independent_entropy_verifier_sha256':OLD_REVIEW,
         'independent_source_verifier_sha256':SOURCE_REVIEW,'mapped_certificate_sha256':MAPPED,
         'role_map':mapping,'graph_pair_checks':196,'core':CORE,'isolates':ISOLATES,'exact_dual_terms':106,
         'core_entropy_bound':'11/2','witness_entropy_bound':'17/2','all_field_linear_block_bound':'rank>8m',
         'canonical_scalar_rank_on_fresh71':9,'eight_clique_roles':EIGHT,'cases':cases,'omitted_term_rejected':omission,
         'scope':'Fixed schedules, monotone public routes and arbitrary paid nested owned routes. At least9 future whole-record descents: linear over the admitted fields, and deterministic zero-error finite alphabets. Conditional84-move exclusions separately require the precise75-ascent bank theorem.'}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    (a.out/'EXPANDED-MAPPED-DUAL.json').write_text(json.dumps(exact,indent=2)+'\n')

if __name__=='__main__':main()
