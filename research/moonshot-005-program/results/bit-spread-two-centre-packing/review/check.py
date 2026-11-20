#!/usr/bin/env python3
"""Rebuild both maximum one/two-centre packings and their actual H fibres."""
from argparse import ArgumentParser
from hashlib import sha256
import gzip,importlib.util,json
from pathlib import Path
import numpy as np

def mod(path,name):
    spec=importlib.util.spec_from_file_location(name,path);v=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    return v

def require(v,msg):
    if not v:raise ValueError(msg)

def verify_component(r,sr,n,cset,maps,seed,shared,repairs):
    k=cset[0].k;cs={c.h for c in cset}
    chart_stats={};rep={};rank_cache={}
    for c in cset:
        count,digest=r.test_chart(c,maps)
        chart_stats[c.h]={'native':count,'parent':len(c.receivers),'lift_sha256':digest}
    for j,source in maps.items():
        c=next(c for c in cset if j in c.donors)
        real_single=[p for p in n.hlist[j] if n.early[j,p]==45]
        if real_single:
            require((c.h,j,k) in repairs and shared is not None and shared!=j,'actual singleton leaf repair')
            e=repairs[c.h,j,k]
            require(e['singleton']==real_single[0],'literal source plane label')
            rep[j]=sr.check_case(r,n,{'early':seed['early']},e,maps,shared)
        else:
            r.schedule(n,c,j,source,seed['early'][str(j)],cs)
        for i in n.adj[j]:
            hs=n.views[j,i]
            if any(h in hs for h in cs):continue
            label=tuple(sorted(sha256(source[h].tobytes()).digest() for h in hs))
            if label not in rank_cache:
                rank_cache[label]=n.f.eliminate(np.vstack([source[h] for h in hs]))[0]
            require(rank_cache[label]==16*k,'all original parent exterior source cuts')
    return {'charts':chart_stats,'parent_donor_cuts':sum(len(n.adj[j]) for j in maps),
            'native_donor_cuts':sum(len(n.adj[j]&set(range(111))) for j in maps),
            'distinct_exterior_source_stacks':len(rank_cache),'physical_singletons':rep}

def main():
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for opt in ('packing-review','singleton-review','field-review','parameters','coefficients'):p.add_argument('--'+opt,type=Path)
    a=p.parse_args();base=a.repo/'research/moonshot-005-program/results'
    r=mod(a.packing_review or base/'bit-spread-overlap-source/review/check.py','packed_review')
    sr=mod(a.singleton_review or base/'bit-spread-singleton-fibre-repair/review/check.py','singleton_review')
    f=mod(a.field_review or base/'bit-spread-h263-source/review/check.py','field_review')
    raw=(a.parameters or base/'bit-spread-two-centre-packing/author/output/PARAMETERS.json').read_bytes()
    cr=(a.coefficients or base/'bit-spread-two-centre-packing/author/output/SINGLETONS.json.gz').read_bytes()
    require(sha256(raw).hexdigest()=='972939d6c9937d1c18cf90f69399112bf2c9c95eab1b194186b164a2331f5d6c' and
            sha256(cr).hexdigest()=='107eb64f87489ee31b2fae02f3f93d512bd5a5cf2485d78181dd825d35d21526','all finite inputs pinned')
    pars=json.loads(raw);sing=json.loads(gzip.decompress(cr));n=r.Native(a.repo,f)
    repairs={(e['h'],e['donor'],e['k']):e for e in sing}
    params={tuple(v['centres']):v for v in pars['pairs']}
    native=set(range(111))
    resource=native-({10,80}|n.adj[80])
    singleton_donors={j for j in native if any(n.early[j,h]==45 for h in n.hlist[j])}
    eligible={h for h,P in enumerate(n.H) if P<=native and 10 not in P and not P<=n.adj[80]}
    require(len(eligible)==540 and len(resource)==47 and len(resource-singleton_donors)==46 and
            all(len(n.H[h]&resource)==2 for h in eligible),'independent packing resource upper bound')
    hist={};families={};tested=set()
    for label in ('singleton_free_30','complete_31'):
        cfg=pars[label]
        used=set();hused=set();stats={k:[] for k in (3,12)}
        for h,q,j in cfg['pairs']:
            P,Q=n.H[h],n.H[q]
            require(P&Q=={j} and {h,q}<=eligible and not (P|Q)&used,'literal disjoint pair components')
            used|=P|Q;hused|={h,q}
            par=params[h,q]
            for k in (3,12):
                key=f'{h},{q},{k}'
                if key not in hist:
                    charts=[r.Chart(n,z,k) for z in (h,q)]
                    maps=r.paired(charts,par[str(k)])
                    hist[key]=verify_component(r,sr,n,charts,maps,par[str(k)],j,repairs)
                stats[k].append(hist[key])
                for v in hist[key]['physical_singletons'].values():tested.add((v['h'],v['j'],v['k']))
        for h in cfg['singles']:
            require(h in eligible and not used&n.H[h],'disjoint leftover single centre')
            used|=n.H[h];hused.add(h)
            for k in (3,12):
                par=pars['one_centre'][str(k)]
                c=r.Chart(n,h,k);maps=c.single(par);key=f'{h},{k}'
                hist[key]=verify_component(r,sr,n,[c],maps,par,None,repairs)
                stats[k].append(hist[key])
        require(set(cfg['charts'])==hused and len(cfg['pairs'])==15,'every labelled centre recovered')
        pool=resource if label=='complete_31' else resource-singleton_donors
        require(len(hused)==2*len(pool)//3 and
                (label=='complete_31' or not used&singleton_donors),'sharp in specified component class')
        summary={}
        for k,zs in stats.items():
            census=sum(sum(v['native'] for v in z['charts'].values()) for z in zs)
            cuts=sum(z['native_donor_cuts'] for z in zs);background=sum(len(n.adj[j]&native) for j in native-used)
            require(cuts+background==6470,'all native proper pairs across the single chosen source')
            summary[k]={'native_designated_fibres':census,'parent_designated_fibres':36*len(hused),
                        'special_native_donor_cuts':cuts,'other_native_donor_cuts':background,
                        'parent_special_donor_cuts':sum(z['parent_donor_cuts'] for z in zs),
                        'local_component_exterior_rank_classes':sum(z['distinct_exterior_source_stacks'] for z in zs)}
        families[label]={'charts':len(hused),'special_donors':len(used),'remaining_donors':len(native-used),
                         'singleton_patched_donors':sorted(used&singleton_donors),'resource_donors':len(pool),
                         'physical':summary}
    require(tested==set(repairs) and len(tested)==16,'all genuine repaired pairs checked')
    a.out.mkdir(parents=True,exist_ok=True)
    result={'parameters_sha256':sha256(raw).hexdigest(),'singleton_sha256':sha256(cr).hexdigest(),
            'families':families,'actual_component_audits':hist,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(families,sort_keys=True))

if __name__=='__main__':main()
