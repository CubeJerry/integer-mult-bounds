#!/usr/bin/env python3
"""Rebuild frame-bank demands; exact integer quadratic noncover verification."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations_with_replacement,combinations
from math import gcd
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
SOURCE='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
ALGEBRA='f7666c123fdcd1df5b46adb3920ebffff55c0e306a2104397961343ae88070d2'
QUADRATIC='8bce0a94b5a94b334d5e107d34db1d9979280ad10b9bcd1cc68ea67b4c0eab96'
CASES=[('ground','4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'),
 ('ground_frame','4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'),
 ('join','bad2213d8bab1c61d08a97bff2e1e21f24bdff9d22be6f7de09c84853b2efe85'),
 ('meet','54fada571a96571697f3e87b50ee613a9042ee9577703f90ab13b2f7a172ff95')]
def load(path,pin,name):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def primitive(v):
    d=gcd(*v)
    if d:v=[x//d for x in v]
    return [-x for x in v]if next((x for x in v if x),1)<0 else v
def independent(rows):
    """Exact rational row independence by integer cross-multiplication and gcd."""
    B={};selected=[]
    for index,row in enumerate(rows):
        v=list(row)
        for p in sorted(B):
            if v[p]:v=primitive([B[p][p]*x-v[p]*y for x,y in zip(v,B[p])])
        if any(v):p=next(i for i,x in enumerate(v)if x);B[p]=primitive(v);selected.append(index)
    return selected
def main():
    p=argparse.ArgumentParser()
    for flag,default in [('native','workers/C/native.json'),('ground','workers/A/ground-retention-known8/WORD.json'),
     ('join','workers/A/frame-derived-proper-export/WORD.json'),('meet','workers/C/meet-frame-export/output/WORD.json'),
     ('source-review','workers/C/proper-query-export-review/check.py'),('arithmetic','workers/C/four-plane-review/check.py'),
     ('algebra','workers/C/all-source-exit-review/check.py'),('quadratic-certificate','workers/A/quadratic-first-exit/CERTIFICATE.json')]:p.add_argument('--'+flag,type=Path,default=BASE/default)
    p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    m=load(a.source_review,SOURCE,'own_source');m.geo=m.load_arithmetic(a.arithmetic);b=load(a.algebra,ALGEBRA,'own_algebra')
    assert hashlib.sha256(a.native.read_bytes()).hexdigest()==b.NATIVE and hashlib.sha256(a.quadratic_certificate.read_bytes()).hexdigest()==QUADRATIC
    R=json.loads(a.native.read_text())['native_roots'];prior=json.loads(a.quadratic_certificate.read_text());oldq={z['source_role']:z for z in prior['source_rows']}
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    K=[(1<<i)^sum(1<<j for j in N[i])for i in range(111)];pairs=list(combinations_with_replacement(range(7),2));assert len(pairs)==28
    ground=json.loads(a.ground.read_text());oldD=[int(x,16)for x in ground['Y_correction_rows_hex']]
    oldC={n:m.geo.chart(z)for n,z in ground['charts'].items()};_,PV,PP=m.replay(ground,oldC,oldD,check_cut=False)
    S=[73,78,81,86];h=sum(1<<j for j in S);G0=K+[d&~255 for d in oldD]+[1<<i for i in range(8)]
    cb=list(b.basis(K).values());q2=list(b.basis(x&y for x in cb for y in cb).values())
    q3=list(b.basis(x&y for x in q2 for y in cb).values());axes=[1<<j for j in range(8)]
    assert [len(cb),len(q2),len(q3)]==[9,36,84]
    assert b.residual(h,b.basis(q3))and not b.residual(h^(1<<1)^(1<<4),b.basis(q3))
    assert b.residual(h,b.basis(q2+axes))
    quartets=defaultdict(list)
    for i in range(8,111):quartets[tuple(j for j,x in enumerate(R[i])if x)].append(i)
    halves=[sum(1<<i for i in I if R[i][p]==s*R[i][q])for support,I in quartets.items()for p,q in combinations(support,2)for s in [1,-1]]
    hb=b.basis(halves+axes);assert len(hb)==64 and b.residual(h,hb)and all(not b.residual(c,hb)for c in cb)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));cases=[]
    for name,pin in CASES:
        path=a.ground if name=='ground_frame'else getattr(a,name);raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        w=json.loads(raw);C={n:m.geo.chart(z)for n,z in w['charts'].items()};D=[int(x,16)for x in w['Y_correction_rows_hex']]
        assert D==oldD and all(w['charts'][n]==z for n,z in ground['charts'].items())
        stats,V,P=m.replay(w,C,D,check_cut=False)
        if name not in ['ground','ground_frame']:
            assert w['operations'][:794]==ground['operations'][:794]
            EV,EP=PV.copy(),PP.copy();H='FRAME_SOURCE'if name=='join'else'MEET_FRAME_SOURCE'
            owner='FRAME_EXPORT'if name=='join'else'MEET_FRAME_EXPORT';dest='G2_A-1'if name=='join'else'MEET_FRAME_LINE'
            assert C[H]==m.geo.basis(tuple(tuple(R[i])for i in S))and len(C[H])==3
            for i in S:EP[f'X{i}']=H
            EV['X73']=h;EV[owner]=h;EP[owner]=dest
            if name=='join':EP['X73']='FRAME_JOIN';EV['X31']^=h
            assert V==EV and P==EP and len(b.basis(V[f'X{i}']for i in range(111)))==111
        source_review=join_review(w,ground,C,D,m,stats)if name=='join'else None
        G=list(b.basis(G0+([h]if name!='ground'else[])).values());assert len(G)==(29 if name=='ground'else 30)
        native={n:next(j for j in range(111)if C[P[n]]==C[f'L{j}'])for n in V if len(C[P[n]])==1 and n!='MEET_FRAME_EXPORT'}
        assert all(V[n]==1<<j for n,j in native.items())
        L={i:[v&((1<<111)-1)for n,v in V.items()if n not in native and m.geo.contained(C[P[n]],C[f'F{i}'])]for i in range(8,111)}
        demands={j:[]for j in range(111)}
        for i in range(8,111):
            obs=b.basis(G+L[i]);t=b.residual(1<<i,obs);cols={j:b.residual(1<<j,obs)for j in N[i]}
            assert not b.residual(t,b.basis(cols.values()))
            for j in N[i]:
                if b.residual(t,b.basis(cols[k]for k in N[i]if k!=j)):demands[j].append(i)
        finish_case(name,pin,m,b,R,w,C,V,P,N,G,L,demands,oldq,pairs,stats,ceiling,cases)
        if source_review:cases[-1]['independent_join_source_review']=source_review
    base={z['source_role']:z for z in cases[0]['source_rows']}
    common=[i for i in range(8,111)if set(S)<=N[i]];assert len(common)==18
    for case in cases[1:]:
        changed=[]
        for z in case['source_rows']:
            before=set(base[z['source_role']]['all_forced_receivers']);after=set(z['all_forced_receivers'])
            if before!=after:
                changed.append(z['source_role']);assert before-after==set(common)&before and len(before-after)==10 and after<=before
        assert changed==S;case['source_roles_with_changed_demand_sets']=changed
        case['removed_common_forced_receivers']=sorted(set(common)&set(base[S[0]]['all_forced_receivers']))
    artificial=[[int(i==j)for j in range(7)]for i in range(7)]
    assert len(independent(artificial))==7 and all(v[0]*v[1]==0 for v in artificial)
    (a.out/'CERTIFICATE.json').write_text(json.dumps({'status':'PASS_INDEPENDENT_QUADRATIC_EXIT_GATES_AND_FRAME_SOURCES',
     'native_sha256':b.NATIVE,'candidate_quadratic_certificate_sha256':QUADRATIC,'quadratic_monomial_order':list(map(list,pairs)),
     'rank_method':'Integer cross-multiplication with primitive-row gcd reduction; exact rational independence, no modular or symbolic-library rank calls.',
     'mode_membership':{'canonical_schur_ranks':[9,36,84],'complete_axis_half_rank':64,'frame_outside_axis_half_bank':True,
       'frame_outside_Q3':True,'frame_in_Q3_plus_axes':True,'frame_outside_Q2_plus_axes':True,'added_axis_roles_for_Q3':[1,4]},
     'rank7_two_hyperplane_control_verified':True,
     'cases':cases},indent=2)+'\n')

def join_review(w,parent,C,D,m,stats):
    prefix=[['MOVE',f'X{i}','FRAME_SOURCE']for i in [73,78,81,86]]
    prefix +=[['ADD',f'X{i}','X73']for i in [78,81,86]]
    prefix +=[['MOVE','X73','FRAME_JOIN'],['INIT','FRAME_EXPORT','FRAME_JOIN'],['ADD','X73','FRAME_EXPORT'],
      ['MOVE','FRAME_EXPORT','G2_A-1'],['ADD','FRAME_EXPORT','X31']]
    inverse=[['ADD','X73','X31']]+[['ADD',f'X{i}','X73']for i in [78,81,86]]
    assert parent['operations'][794:905]==[['MOVE',f'X{i}','Hub']for i in range(111)]
    expected=parent['operations'][:794]+prefix+parent['operations'][794:905]+inverse+parent['operations'][905:]+[['CLEAR','FRAME_EXPORT']]
    assert w['operations']==expected and w['carrier_interface_before_operation']==806
    assert C['FRAME_JOIN']==m.geo.basis(C['FRAME_SOURCE']+C['G2_A-1'])and len(C['FRAME_JOIN'])==5
    assert stats['counts']=={'INIT':120,'ADD':612,'MOVE':316,'CLEAR':120}
    assert stats['movement_profile']=={1:72,2:22,3:1,4:16,5:19,6:16,7:170}
    assert stats['owned_downward_profile']=={1:8,2:1}and stats['peak_owned']==stats['dirty_CLEAR']==120
    controls={}
    for label,j in [('encode',798),('capture',803),('descent',804),('carrier_load',805),('carrier_unload',917),('source_inverse',918)]:
        alt=json.loads(json.dumps(w));del alt['operations'][j]
        if j<806:alt['carrier_interface_before_operation']-=1
        try:m.replay(alt,C,D,check_cut=False)
        except ValueError as err:controls['omit_'+label]=str(err)
        else:raise AssertionError('missing join operation accepted')
    alt=json.loads(json.dumps(w));alt['operations'][917:921]=inverse[1:]+inverse[:1]
    try:m.replay(alt,C,D,check_cut=False)
    except ValueError as err:controls['inverse_before_unload']=str(err)
    else:raise AssertionError('wrong inverse order accepted')
    return {'status':'PASS_INDEPENDENT_LITERAL_JOIN_SOURCE','all222_columns':True,'entire_word_reconstructed':True,
      'all342_cut_fields_verified':True,'arbitrary_Y_identity_preserved':True,'controls':controls}

def finish_case(name,pin,m,b,R,w,C,V,P,N,G,L,demands,oldq,pairs,stats,ceiling,cases):
    rows=[]
    for j in range(8,111):
        D=demands[j];normals=[R[i]for i in D];normal_indices=independent(normals);normal_rank=len(normal_indices)
        assert normal_rank>0 and set(D)<=set(oldq[j]['all_forced_receivers'])
        deleted=next(k for k,x in enumerate(R[j])if x);coords=[k for k in range(8)if k!=deleted]
        Qrows=[[R[i][coords[a]]*R[i][coords[c]]for a,c in pairs]for i in D]
        qindices=independent(Qrows);qrank=len(qindices);assert qrank<=27
        poly=None;matrix_rank=None
        if qrank==27:
            poly=oldq[j]['primitive_quadratic_kernel'];assert poly is not None and len(poly)==28 and any(poly)
            assert oldq[j]['deleted_normal_coordinate']==deleted and oldq[j]['remaining_normal_coordinates']==coords
            assert all(sum(x*y for x,y in zip(row,poly))==0 for row in Qrows)
            matrix=[[0]*7 for _ in range(7)]
            for(a,c),v in zip(pairs,poly):matrix[a][c]=matrix[c][a]=2*v if a==c else v
            matrix_rank=len(independent(matrix));assert matrix_rank==6
            selected=[D[t]for t in qindices];minimum=3
            altered=poly.copy();altered[0]+=1
            assert any(sum(x*y for x,y in zip(row,altered))for row in Qrows)
        else:
            selected=[D[t]for t in(normal_indices if normal_rank==7 else normal_indices[:1])]
            minimum=2 if normal_rank==7 else 1
        duals=[]
        for i in selected:
            d=b.dual_for(G+L[i]+[1<<h for h in N[i]if h!=j],1<<i);assert d>>j&1
            duals.append({'receiver':i,'dual_hex':hex(d)})
        rows.append({'source_role':j,'all_forced_receivers':D,'normal_rank':normal_rank,'deleted_normal_coordinate':deleted,
         'remaining_normal_coordinates':coords,'quadratic_evaluation_rank':qrank,'primitive_quadratic_kernel':poly,
         'symmetric_twice_quadratic_matrix_rank':matrix_rank,'minimum_native_departures':minimum,'duals':duals})
    total=sum(z['minimum_native_departures']for z in rows)
    active=[z['source_role']for z in rows if P[f"X{z['source_role']}"]==f"L{z['source_role']}"]
    ground=[i for i in range(111)if not C[P[f'Y{i}']]];assert len(ground)==95
    owned=max(0,total-len(active)-len(ground));profile=dict(stats['movement_profile']);profile[1]+=owned
    Q=m.geo.moment(stats['movement_profile']);lower=m.geo.moment(profile);excess=(lower[0]-ceiling[1],lower[1]-ceiling[0])
    result={'source':name,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],'stats':stats,'bank_rank':len(G),
     'source_rows':rows,'normal_rank_histogram':dict(Counter(z['normal_rank']for z in rows)),
     'quadratic_rank_histogram':dict(Counter(z['quadratic_evaluation_rank']for z in rows)),
     'departure_histogram':dict(Counter(z['minimum_native_departures']for z in rows)),
     'native_departures':total,'active_native_public_roles':active,'active_native_public_allowance':len(active),
     'ground_public_allowance':len(ground),'minimum_future_owned_ascents':owned,
     'source_moment':b.record(Q),'mandatory_profile':profile,'target_excess':b.record(excess),'strict_exclusion':excess[0]>0}
    cases.append(result)
    print(name,'normal',result['normal_rank_histogram'],'quadratic',result['quadratic_rank_histogram'],
     'exits',result['departure_histogram'],'owned',owned,'excess',b.record(excess)['decimal'][0],flush=True)

if __name__=='__main__':main()

