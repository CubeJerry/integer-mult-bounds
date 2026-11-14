#!/usr/bin/env python3
"""Source and integer-root premises for the fixed-continuation facet tariff."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
import runpy
from pathlib import Path

NATIVE_PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
GEOMETRY_PIN='244bedc78693645fdd70ed4540689e7d047e0a6eb260c3d40403ac691d43b7e8'
REPLAY_PIN='f99bfc2896163e373224a4ce86608bf0452f49f0367db5d006aeca03a4180cbe'
MOMENT_PIN='6a88ca1fb962391190626539ce098517785a717c34ea0af61b533ea64821b1d1'


def need(ok,message):
    if not ok:raise ValueError(message)


def load(path,pin=None):
    raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    if pin is not None:need(digest==pin,('pin',str(path)))
    return json.loads(gzip.decompress(raw)),digest


def coalesce(word):
    out=json.loads(json.dumps(word));fr=word['frames'];pending={};ops=[]
    def dim(c):return fr[str(c)]['dim']
    def flush(f):
        if f in pending:
            c,d=pending.pop(f);ops.append(['MOVE',f,c,d])
    for op in word['program']:
        kind,f=op[:2]
        if kind=='MOVE':
            _,f,c,d=op
            if f not in pending:pending[f]=(c,d)
            else:
                start,end=pending[f]
                need(end==c,'pending route continuity')
                if (dim(d)-dim(c))*(dim(end)-dim(start))>0:
                    pending[f]=(start,d)
                else:
                    flush(f);pending[f]=(c,d)
        else:
            flush(f)
            if kind=='ADD':flush(op[2])
            need(kind in ('INIT','ADD','CLEAR'),'unexpected opcode')
            ops.append(op)
    for f in list(pending):flush(f)
    out['program']=ops
    out['schema']=word['schema']+'-actual-coalesced'
    out['scope']=word['scope']+' Actual coalescing of unread/unwritten monotone MOVE runs only; every access stop is preserved.'
    return out


def main(a):
    native,native_sha=load(a.native,NATIVE_PIN)
    for path,pin in ((a.geometry,GEOMETRY_PIN),(a.replayer,REPLAY_PIN),(a.moment_checker,MOMENT_PIN)):
        need(hashlib.sha256(path.read_bytes()).hexdigest()==pin,('dependency pin',str(path)))
    g=runpy.run_path(str(a.geometry));replay=runpy.run_path(str(a.replayer))['replay'];m=runpy.run_path(str(a.moment_checker))
    combine,moment,record=m['combine'],m['moment'],m['record']
    pre,pre_sha=load(a.prefix);close,close_sha=load(a.closed)
    cp,cc=coalesce(pre),coalesce(close);receipts={}
    for name,raw,coal in (('prefix',pre,cp),('closed',close,cc)):
        rr=replay(raw,g);rc=replay(coal,g)
        for key in ('rows','owned_rows','owned_where','owned_lifetimes','peak_owned'):
            need(rr[key]==rc[key],('coalesced semantic equality',name,key))
        need({k:v for k,v in rr['counts'].items()if k!='MOVE'}=={k:v for k,v in rc['counts'].items()if k!='MOVE'},'ordinary operations unchanged')
        need(sum(int(k)*v for k,v in rr['paid_profile'].items())==sum(int(k)*v for k,v in rc['paid_profile'].items()),'rank length preservation')
        receipts[name]={k:v for k,v in rc.items()if k not in ('rows','owned_rows','owned_where','clear_rows','snapshots')}
    need(cp['final'][:111]==native['final'][:111],'all original X at native Hub endpoint')
    need(all(cp['final'][111+i] in (0,native['final'][111+i])for i in range(111)),'handoff Y ground or own final facet')
    spaces={int(k):g['rref'](v['B'])for k,v in cp['frames'].items()}
    facets={g['rref'](native['frames'][str(native['final'][111+i])]['B']):i for i in range(111)}
    need(len(facets)==111,'distinct native facets')
    anchored=set();events=[];arrival=Counter();depart=Counter()
    for opnum,op in enumerate(cp['program']):
        if op[0]!='MOVE':continue
        _,f,c,d=op;dc,dd=len(spaces[c]),len(spaces[d])
        if f<222:need(dd>dc,'fixed public prefix monotonicity')
        if dd>dc and spaces[d] in facets:
            i=facets[spaces[d]]
            if f==111+i and f not in anchored:anchored.add(f)
            else:
                arrival[i]+=1;events.append({'operation':opnum,'field':f,'facet':i,'kind':'upward_arrival'})
        if dd<dc and spaces[c] in facets:
            i=facets[spaces[c]];depart[i]+=1;events.append({'operation':opnum,'field':f,'facet':i,'kind':'downward_departure'})
    t=Counter(arrival);t.update(depart)
    need(dict(t)=={0:57}and dict(arrival)=={0:56}and dict(depart)=={0:1},'nonanchor prefix facet events concentrated at F0')
    prefix_cap=sum(min(2,v)for v in t.values())
    Q=Counter({int(k):v for k,v in receipts['closed']['paid_profile'].items()})
    prefix_Q=Counter({int(k):v for k,v in receipts['prefix']['paid_profile'].items()})
    remaining=[i for i in range(111)if cp['final'][111+i]!=native['final'][111+i]]
    need(Q==prefix_Q+Counter({7:len(remaining)}),'closing suffix contains only direct remaining Y routes')
    N=Counter(abs(native['frames'][str(o[3])]['dim']-native['frames'][str(o[2])]['dim'])for o in native['program']if o[0]=='MOVE')
    H={2:1,4:25,6:1,8:410}
    P2=combine((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
    T2=combine((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
    M2=combine((1,T2),(-1,P2));B=combine((1,N),(-1,H),(F(1,36),M2))
    need(moment(M2)[1]<0,'strictly negative finite-m correction')
    phi={0:{},**{r:{r:1}for r in range(1,6)},6:{7:1,1:-1},7:{7:1,1:-1},8:{7:1}}
    need(moment({7:1,5:-1,1:-1})[0]>0,'potential monotonicity at rank5-to6')
    inequalities=[]
    for x in range(9):
        for y in range(9):
            if x==y:continue
            event=int((x==7 and y<7)or(x<7 and y==7))
            slack=combine((1,{abs(x-y):1}),(-1,phi[x]),(1,phi[y]),(-event,{1:1}))
            if slack:
                enclosure=moment(slack);need(enclosure[0]>=0,('potential inequality',x,y,slack))
            else:enclosure=(F(0),F(0))
            inequalities.append({'from_rank':x,'to_rank':y,'event':event,'slack_profile':{str(k):str(v)for k,v in slack.items()},'slack':record(enclosure)})
    n=a.future_packets;Elo,Ehi=moment(combine((1,B),(-1,Q),(-n,{7:1})))
    cap=Ehi.numerator//Ehi.denominator
    need(Elo>cap and Ehi<cap+1,'strict nonintegral future-event floor')
    full=combine((1,Q),(n,{8:1}));L=moment(combine((1,B),(-1,full)))
    need(L[0]>0,'positive optimistic direct-mode room')
    stop_cost=moment({1:1,7:1,8:-1});need(stop_cost[0]>0,'actual facet stop is not free')
    need(not combine((3,{1:1}),(1,{7:1}),(-1,phi[8]),(-3,{1:1})),'three-event packet route is tight')
    a.output.mkdir(parents=True,exist_ok=True)
    pins={name:g['save_word'](a.output/name,w)for name,w in (('COALESCED-PREFIX.json.gz',cp),('COALESCED-CLOSED-PARTIAL.json.gz',cc))}
    out={'status':'PASS_FIXED_MODE_NATIVE_FACET_TARIFF_PREMISES','native_sha256':native_sha,'source_pins':{'prefix_gzip':pre_sha,'closed_gzip':close_sha},'dependency_pins':{'geometry':GEOMETRY_PIN,'replayer':REPLAY_PIN,'moment_checker':MOMENT_PIN},'coalesced_word_pins':pins,'coalesced_receipts':receipts,'prefix_native_facet_events':events,'prefix_nonanchor_up_arrivals':dict(arrival),'prefix_down_departures':dict(depart),'prefix_capped_fitting_support_charge':prefix_cap,'remaining_monotone_public_Y':remaining,'t':'199/200','future_Hub_to_ground_packets':n,'limiting_allowance':record(moment(B)),'limiting_direct_mode_room':record(L),'future_native_facet_event_bound':record((Elo,Ehi)),'integer_future_event_cap':cap,'full_fitting_foreign_support_charge_cap':prefix_cap+cap,'rank_potential_inequalities':inequalities,'controls':{'positive_extra_cost_of_facet_read_in_direct_packet':record(stop_cost),'three_event_tight_rank_route':[8,7,6,7,0],'uncharged_own_Y_anchor_receivers':sorted(f-111 for f in anchored)},'scope':'Fixed emitted prefix; original X frozen at Hub; public Y monotone to own facets; each specified future Hub-born record reaches ground; all other owned movement extra; retained complete caller at kappa=1/200. Necessary fitting condition only.','complete_supplier':False,'new_kappa':False}
    (a.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'prefix_facet_counts':dict(t),'direct_mode_room':record(L)['lower_decimal'],'future_facet_cap':cap,'full_fitting_charge_cap':prefix_cap+cap,'event_upper':record((Elo,Ehi))['upper_decimal']}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('prefix','closed','native','geometry','replayer','moment-checker','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--future-packets',type=int,default=6)
    main(p.parse_args())
