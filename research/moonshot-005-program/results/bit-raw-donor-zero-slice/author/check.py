#!/usr/bin/env python3
"""Pinned exact zero-donor cuts for all single raw-bank helpers.

The inherited independent color solver is executed only after its hash check.
This is a scoped source-representation theorem, not a mixed-bank obstruction.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from pathlib import Path
from hashlib import sha256
import gzip,json,importlib.util,time


def rank(rows):
    basis={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in basis:basis[p]=x;break
            x^=basis[p]
    return len(basis)


def independent(rows):
    answer=[]
    for row in rows:
        if rank(answer+[row])>len(answer):answer.append(row)
    return answer


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();pg=args.repo/'research/moonshot-005-program'
    paths={'layout':pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
           'old_caps':pg/'results/bit-stripe-varying-port-cut/review/output/RESULT.json.gz',
           'factor':pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json',
           'solver':pg/'results/bit-stripe-varying-port-cut/review/check.py'}
    raw={k:(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes()) for k,p in paths.items()}
    pins={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
          'old_caps':'55062cf00045a9d8888fbea8cd613d9c8db65ef570381c282aa004e73d8aa0ae',
          'factor':'346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7',
          'solver':'2072dc0ceb7dfb97c977c93ab886794aba81087df7ac2b8807292f115f21ab8c'}
    for key,value in raw.items():assert sha256(value).hexdigest()==pins[key],key+' pin'
    layout=json.loads(raw['layout']);old=json.loads(raw['old_caps']);factor=dict(json.loads(raw['factor'])['factors'])
    spec=importlib.util.spec_from_file_location('admitted_color_solver',paths['solver'])
    solver=importlib.util.module_from_spec(spec);spec.loader.exec_module(solver)
    roots=layout['root_table'];H=[set(h) for h in layout['A2']];D=[set(d) for d in layout['D4']]
    native=set(range(111));full=(1<<111)-1
    O=[{j for j,v in enumerate(roots) if sum(a*b for a,b in zip(u,v))==0} for u in roots[:111]]
    K=independent([sum(1<<j for j in (o&native)^{i}) for i,o in enumerate(O)])
    assert len(K)==9
    dvis=[{i for i,o in enumerate(O) if d<=o} for d in D]
    old_records={z['plane']:z for z in old['records']}
    prepared=[]
    for hi,h in enumerate(H):
        donors=sorted(h&native);m=len(donors)
        if m<2:prepared.append({'H':hi,'donors':donors});continue
        z=old_records[hi];targets=z['joint_tight_receivers'];ds=[d for d,v in enumerate(D) if h<=v]
        masks=[sum(1<<p for p,i in enumerate(targets) if i in dvis[d]) for d in ds]
        assert len(ds)==45 and sorted(set(masks)-{0})==z['port_neighborhoods'] and masks.count(0)==z['uncovered_ports']
        prepared.append({'H':hi,'donors':donors,'targets':targets,'masks':masks,'old_alpha':z['rank_cap'],
                         'x':12//m+factor.get(hi,0)})
    args.out.mkdir(parents=True,exist_ok=True)
    checkpoint=args.out/'CHECKPOINT.json.gz'
    if checkpoint.exists():
        saved=json.loads(gzip.decompress(checkpoint.read_bytes()))
        output=saved['donors'];total_nodes=saved['search_nodes'];total_changed=saved['changed_instances']
    else:
        output=[];total_nodes=0;total_changed=0
    begin=time.monotonic();cache={}
    for zero in range(len(output),111):
        active=full^(1<<zero)
        assert rank([row&active for row in K])==9
        for i in range(111):
            if i==zero:continue
            outside=active^sum(1<<j for j in O[i]&native if j!=zero)
            assert rank([row&outside for row in K])==9,(zero,i,'outside neutrality')
        binary=Fraction(0);general=Fraction(0);hist=Counter();ghist=Counter()
        uncovered=0;direct=0;changed=[];top_fail=[];min_margin=None
        for entry in prepared:
            hi=entry['H'];donors=entry['donors'];m=len(donors)
            if zero in donors:
                grant=2*(m-1) if m>=2 else 0
                binary+=grant;general+=grant;direct+=grant
                continue
            if m==0:continue
            if m==1:binary+=3;general+=3;continue
            targets=entry['targets'];masks=entry['masks'];decision=None
            if zero not in targets:
                alpha=entry['old_alpha'];u=masks.count(0)
            else:
                removed=targets.index(zero);low=(1<<removed)-1
                reduced=[(mask&low)|((mask>>(removed+1))<<removed) for mask in masks]
                u=reduced.count(0);edges=tuple(sorted(set(reduced)-{0}));n=len(targets)-1
                key=(m,n,edges)
                if key not in cache:
                    k2=solver.solve(edges,n,2);k3=None;total_nodes+=k2['nodes']
                    if not k2['sat']:alpha=1
                    elif m==2:alpha=2
                    else:
                        k3=solver.solve(edges,n,3);total_nodes+=k3['nodes'];alpha=3 if k3['sat'] else 2
                    cache[key]=(alpha,k2,k3)
                alpha,k2,k3=cache[key]
                decision={'H':hi,'alpha':alpha,'uncovered':u,'k2':k2,'k3':k3}
                changed.append(decision);total_changed+=1
            bcap=alpha+1
            x=entry['x'];margin=45*(m-1)*x-u*m*x-180
            min_margin=margin if min_margin is None else min(min_margin,margin)
            starcap=alpha+1 if alpha<m else 2*m
            gcap=starcap if margin>0 else max(starcap,3)
            if margin<=0:top_fail.append([hi,m,x,u,margin,starcap,gcap])
            binary+=bcap+Fraction(2*u,15);general+=gcap+Fraction(2*u,15)
            uncovered+=u;hist[m,alpha]+=1;ghist[m,alpha,gcap]+=1
        required=101*32
        assert binary<required and general<required,(zero,binary,general,required)
        output.append({'zeroed_donor':zero,'binary_capacity':str(binary),'general_field_capacity':str(general),
                       'required':required,'binary_deficit':str(required-binary),'general_field_deficit':str(required-general),
                       'binary_deficit_at_r180':int(180*(required-binary)),
                       'general_field_deficit_at_r180':int(180*(required-general)),
                       'direct_grant':direct,'uncovered':uncovered,'minimum_top_gate_margin':min_margin,
                       'top_gate_exception_planes':top_fail,
                       'binary_cap_histogram':{str(k):v for k,v in sorted(hist.items())},
                       'general_cap_histogram':{str(k):v for k,v in sorted(ghist.items())},
                       'changed_color_instances':changed})
        temporary=args.out/'CHECKPOINT.tmp.gz'
        temporary.write_bytes(gzip.compress(json.dumps({'donors':output,'search_nodes':total_nodes,
                                                        'changed_instances':total_changed},separators=(',',':')).encode(),mtime=0))
        temporary.replace(checkpoint)
        if zero%10==0 or zero==110:
            print(json.dumps({'donors_completed':zero+1,'last_general_deficit_r180':output[-1]['general_field_deficit_at_r180'],
                              'unique_new_color_instances':len(cache),'search_nodes':total_nodes,
                              'elapsed_seconds':round(time.monotonic()-begin,2)}),flush=True)
    # Recompute the distinct instance count even when a prior checkpoint was resumed.
    unique_instances=set()
    for zero,record in enumerate(output):
        for decision in record['changed_color_instances']:
            entry=prepared[decision['H']];targets=entry['targets'];removed=targets.index(zero);low=(1<<removed)-1
            reduced=[(mask&low)|((mask>>(removed+1))<<removed) for mask in entry['masks']]
            unique_instances.add((len(entry['donors']),len(targets)-1,tuple(sorted(set(reduced)-{0}))))
    assert len(unique_instances)==31087 and total_changed==31793
    assert min(z['minimum_top_gate_margin'] for z in output)==24
    assert all(not z['top_gate_exception_planes'] for z in output)
    result={'status':'PASS_SINGLE_RAW_DONOR_REPEATED_TWO_SOURCE_GATE','source_hashes':{k:sha256(v).hexdigest() for k,v in raw.items()},
            'raw_donors':111,'canonical_outside_restrictions_checked':111*110,
            'new_color_instances_with_multiplicity':total_changed,'distinct_new_color_instances':len(unique_instances),
            'new_color_search_nodes':total_nodes,
            'minimum_binary_deficit_at_r180':min(x['binary_deficit_at_r180'] for x in output),
            'minimum_general_field_deficit_at_r180':min(x['general_field_deficit_at_r180'] for x in output),
            'worst_general_donors':[x['zeroed_donor'] for x in output if x['general_field_deficit_at_r180']==min(y['general_field_deficit_at_r180'] for y in output)],
            'donors':output,'mathematical_status':'Written scoped theorem; separate independent review required for admission.',
            'minimum_remaining_early_top_margin_at_r180':24,
            'new_informative_helper_scope':'Any deterministic functions of the original canonical bank and one fixed raw donor bank.',
            'original_balanced_early_source_bijection_retained':True,
            'base_quotient_maps_repeat_identically':True,
            'arbitrary_mixed_bank_helper_covered':False,'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    payload=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode()
    (args.out/'RESULT.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    summary={k:v for k,v in result.items() if k!='donors'}
    summary['payload_sha256']=sha256(payload).hexdigest()
    (args.out/'SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':main()
