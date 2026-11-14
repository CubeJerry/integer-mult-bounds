#!/usr/bin/env python3
"""Exact handoff-specific all-route tariff; proof in ALL-ROUTE-EXTENSION.md."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import runpy

NATIVE_PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
MOMENT_PIN='6a88ca1fb962391190626539ce098517785a717c34ea0af61b533ea64821b1d1'
CASES={'canonical-pivot':58,'halfclass-banks':56,'halfclass-two-triples':50,'plain':52,'joined':50}


def need(ok,message):
    if not ok:raise ValueError(message)


def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==NATIVE_PIN,'native pin')
    need(hashlib.sha256(a.moment_checker.read_bytes()).hexdigest()==MOMENT_PIN,'moment checker pin')
    n=json.loads(gzip.decompress(raw));m=runpy.run_path(str(a.moment_checker));combine,moment,record=m['combine'],m['moment'],m['record']
    N=Counter(abs(n['frames'][str(o[3])]['dim']-n['frames'][str(o[2])]['dim'])for o in n['program']if o[0]=='MOVE')
    H={2:1,4:25,6:1,8:410}
    P2=combine((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
    T2=combine((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
    M2=combine((1,T2),(-1,P2));B=combine((1,N),(-1,H),(F(1,36),M2))
    need(moment(M2)[1]<0,'finite multiplicity correction is strictly negative')
    clo,chi=moment({1:1,8:1,7:-1});need(1<clo<chi<2,'reflected downward excursion coefficient')
    pins=json.loads((a.bundle/'PINS.json').read_text());results={}
    for name,expected in CASES.items():
        p=a.bundle/name/'RESULT.json';rb=p.read_bytes();digest=hashlib.sha256(rb).hexdigest()
        need(digest==pins[str(p.relative_to(a.bundle))],('frozen source receipt pin',name))
        r=json.loads(rb)
        need(r['prefix_nonanchor_up_arrivals']=={'0':56}and r['prefix_down_departures']=={'0':1}and r['prefix_capped_fitting_support_charge']==2,'prefix facet concentration')
        wp=a.bundle/name/'COALESCED-CLOSED-PARTIAL.json.gz';wb=wp.read_bytes()
        need(hashlib.sha256(wb).hexdigest()==r['coalesced_word_pins'][wp.name]['gzip_sha256'],'coalesced source word pin')
        w=json.loads(gzip.decompress(wb));Q=Counter(abs(w['frames'][str(o[3])]['dim']-w['frames'][str(o[2])]['dim'])for o in w['program']if o[0]=='MOVE')
        need(dict(Q)=={int(k):v for k,v in r['coalesced_receipts']['closed']['paid_profile'].items()},'source-derived profile equals receipt')
        rlo,rhi=moment(combine((1,B),(-1,Q)));ratio=(2*rlo/chi,2*rhi/clo)
        upper=ratio[1].numerator//ratio[1].denominator
        need(ratio[0]>upper and ratio[1]<upper+1 and upper==expected,('exact all-route integer cap',name))
        dcap=(rhi/clo).numerator//(rhi/clo).denominator;feasible=[]
        for d in range(dcap+1):
            hi=rhi-d*clo;mm=hi.numerator//hi.denominator
            while mm>=0:
                gap=(rlo-mm-d*chi,rhi-mm-d*clo)
                if gap[0]>0:
                    feasible.append({'M':mm,'D':d,'weighted_gap':record(gap),'facet_count':mm+2*d});break
                need(gap[1]<=0,('interval cannot resolve count witness',name,mm,d));mm-=1
        best=max(feasible,key=lambda x:(x['facet_count'],-x['D']))
        need(best['facet_count']==upper,'integer relaxation arithmetic control attains count cap')
        mono_cap=rhi.numerator//rhi.denominator
        results[name]={'source_receipt_sha256':digest,'coalesced_closed_word_sha256':hashlib.sha256(wb).hexdigest(),'Q0_profile':dict(Q),'Q0_moment':record(moment(Q)),'limiting_future_weighted_room':record((rlo,rhi)),'twice_room_over_c':record(ratio),'future_M_plus_2D_cap':upper,'future_public_downward_MOVE_cap':dcap,'full_fitting_charge_cap':2+upper,'monotone_public_future_fitting_cap':2+mono_cap,'limiting_integer_count_witness':best,'all_feasible_max_M_by_D':feasible,'six_Hub_interval_special_case_charge_cap':r['full_fitting_foreign_support_charge_cap']}
    # Two actual distinct coordinate-native facets share a rank-six chart.
    roots=[[F(v)for v in n['frames'][str(n['start'][i])]['B'][0]]for i in (0,1)]
    supports=[[j for j,v in enumerate(row)if v]for row in roots]
    need(all(len(s)==1 for s in supports)and supports[0]!=supports[1],'two coordinate source roots')
    remaining=[j for j in range(8)if all(j not in s for s in supports)]
    q=[[int(j==c)for c in range(8)]for j in remaining]
    need(len(q)==6 and all(sum(x*y for x,y in zip(row,b))==0 for row in roots for b in q),'real rank-six facet intersection')
    out={'status':'PASS_FIXED_PREFIX_ALL_ROUTE_FACET_TARIFF_PREMISES','native_sha256':NATIVE_PIN,'moment_checker_sha256':MOMENT_PIN,'t':'199/200','downward_public_coefficient':record((clo,chi)),'limiting_complete_allowance':record(moment(B)),'cases':results,'negative_control':{'receiver_route':['F0','F0_intersect_F1','F1','F0_intersect_F1','F0'],'intersection_basis':q,'future_public_downward_MOVEs':2,'future_nonanchor_native_facet_events':4,'purpose':'Actual legal turns show why the occurrence bound needs2D rather thanD.'},'scope':'Fixed already executed source prefix only; arbitrary future legal public/owned turns, proper births/erasures and all whole-record linear maps; complete original endpoints and strict retained caller at t=.995. No packet-endpoint or static-code premise. No new kappa.','complete_supplier':False,'new_kappa':False}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'complete_fitting_caps':{name:r['full_fitting_charge_cap']for name,r in results.items()},'c':record((clo,chi))['lower_decimal']}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('native','moment-checker','bundle','output'):p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
