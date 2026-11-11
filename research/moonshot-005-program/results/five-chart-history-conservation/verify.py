"""Authenticate every timed endpoint/history dual on the pinned native."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path
from source_core import PIN, add, check_dual, need, span

def main(args):
    package=Path(__file__).resolve().parent
    raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin')
    w=json.loads(gzip.decompress(raw));P=w['program'];C=list(map(span,w['frames']))
    cert_raw=(package/'CERTIFICATE.json').read_bytes();cert=json.loads(cert_raw)
    need(cert['source_sha256']==PIN and cert['donor']==77 and cert['receiver']==189,'certificate source and pair')
    ds=[w['initial'][77]]+[e[3] for e in P if e[:2]==['MOVE',77]]
    rs=[w['initial'][189]]+[e[3] for e in P if e[:2]==['MOVE',189]]
    need(ds==cert['station_charts']==[71,312,324,232,127],'all actual donor stations')
    need(rs==cert['receiver_charts']==[3,307,901,198],'all actual receiver stations')
    station={C[x] for x in ds};route={C[x] for x in rs}
    need(not station&route,'disjoint actual chart spaces')
    need(cert['endpoint']=={'role':189,'chart':w['final'][189]} and C[w['final'][189]]!=C[127],'actual required off-hub endpoint')
    loc=dict(enumerate(w['initial']));column={77:Q(1)};observations=[]
    initial=[j for j,ch in loc.items() if C[ch] in route]
    for t,e in enumerate(P):
        op,j=e[:2]
        if op=='ADD':add(column,j,column.get(e[2],Q(0))*Q(e[3]))
        elif op in ('COPY','SCALE'):
            z=column.get(e[2],Q(0))*Q(e[3]) if op=='COPY' else column.get(j,Q(0))*Q(e[2])
            column.pop(j,None)
            if z:column[j]=z
        elif op=='INIT':column.pop(j,None);loc[j]=e[2]
        elif op=='CLEAR':column.pop(j,None);loc.pop(j)
        elif op=='MOVE':
            loc[j]=e[3]
            if C[e[3]] in route:observations.append({'after_event':t,'role':j,'chart':e[3],'endpoint_coefficient':str(column.get(j,Q(0)))})
        else:raise ValueError(op)
    need(initial and len(initial)==cert['initial_observation_count']==1046,'complete initial observation census')
    need(observations==cert['arrival_observations'] and len(observations)==19,'complete ordered arrival census and source coefficients')
    need(column.get(189)==1,'source input77 gives unit endpoint189 response')
    checked=[check_dual(w,C,obs,station) for obs in observations]
    negatives=[]
    bad=dict(next(o for o in observations if Q(o['endpoint_coefficient'])))
    bad['endpoint_coefficient']=str(Q(bad['endpoint_coefficient'])+1)
    try:check_dual(w,C,bad,station)
    except ValueError as e:negatives.append({'mutation':'change a nonzero endpoint coefficient','rejected':str(e)})
    else:raise ValueError('wrong coefficient accepted')
    outside=next(o for o in observations if (o['after_event'],o['role'])==(37192,1145))
    try:check_dual(w,C,outside,station|{C[8]})
    except ValueError as e:negatives.append({'mutation':'grant additional controls at chart8','rejected':str(e)})
    else:raise ValueError('extra-station counterexample not detected')
    need(any(Q(x['endpoint_coefficient']) for x in observations),'endpoint restoration premise is necessary')
    result={'status':'PASS_FIVE_CHART_RANK_ONE_HISTORY_CONSERVATION','source_sha256':PIN,'certificate_sha256':hashlib.sha256(cert_raw).hexdigest(),'native_instructions':len(P),'public_inputs':w['public'],'station_charts':ds,'receiver_charts':rs,'initial_observations':len(initial),'arrival_observations':len(observations),'endpoint_coefficients':dict(sorted(Counter(x['endpoint_coefficient'] for x in observations).items())),'all_time_station_adjoint_checks':sum(r['station_checks'] for r in checked),'all_19_duals_checked':True,'COPY_zero_guards_not_needed_for_obstruction':True,'source_input77_positive_control':{'final189_response':'1','nonzero_arrival_responses':sum(bool(Q(x['endpoint_coefficient'])) for x in observations)},'negative_controls':negatives,'claim':'For this fixed native chronology and five station spaces, restoring common endpoint189 forces every receiver189 native history to remain unchanged under arbitrary local additive interventions, including data-dependent feedback. No new kappa.','new_complete_kappa':None}
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
