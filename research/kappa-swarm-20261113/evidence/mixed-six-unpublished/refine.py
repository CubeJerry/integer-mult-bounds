#!/usr/bin/env python3
"""Per-new-cache refinement of the frozen two-component generic pilot."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from hashlib import sha256
import argparse,gzip,importlib.util,json,sys,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def need(ok,label):
    if not ok:raise ValueError(label)
def run(output):
    start=time.monotonic();deadline=start+60
    raw=(HERE/'RESULT.json').read_bytes();g=json.loads(raw);payload=g.copy();payload.pop('seconds',None)
    normpin=sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    need(normpin=='f46a387b47c3298e7e64af5b767ff08a6adfa2a5c3e4e40ce173126bd2d4801e','frozen logical generic receipt')
    need(sha256((HERE/'scan.py').read_bytes()).hexdigest()=='7f1214145e3f8b9ea83850a4753bbd8f7b721863d57a20fc7ddd00875cc910d2','independent exact rank code')
    spec=importlib.util.spec_from_file_location('mixed_exact',HERE/'scan.py');M=importlib.util.module_from_spec(spec);sys.modules[spec.name]=M;spec.loader.exec_module(M)
    wr=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(wr).hexdigest()==g['source_sha256'],'word pin');w=json.loads(gzip.decompress(wr))
    zr=(ROOT/'worker-b/helper-graph/ROWS.json').read_bytes();need(sha256(zr).hexdigest()==M.ROWPIN,'zero rows pin');zeros={r['event']:r for r in json.loads(zr)['records']}
    T={h:len(w['frames'][w['final'][h]])-len(w['frames'][w['initial'][h]]) for h in range(w['public'])}
    L={s['event']:[M.decode(r) for r in s['L_basis']] for s in g['site_evidence']}
    mins={e:min(T[h] for r in rows for h in r) for e,rows in L.items()}
    pp=ROOT/'budget_price.py';need(sha256(pp.read_bytes()).hexdigest()==g['input_sha256']['budget_price.py'],'price pin')
    sp=importlib.util.spec_from_file_location('refined_price',pp);P=importlib.util.module_from_spec(sp);sys.modules[sp.name]=P;sp.loader.exec_module(P)
    iraw=P.INVOICE.read_bytes();need(sha256(iraw).hexdigest()==P.PIN,'invoice pin');iv=json.loads(iraw)
    ta={int(k):n for k,n in iv['after']['T'].items()};pa={int(k):n for k,n in iv['after']['P'].items()};base={r:ta.get(r,0)-pa.get(r,0) for r in ta.keys()|pa.keys()};kappa=Q(g['kappa'])
    def prof(ranks):
        need(ranks[0]==0 and all(ranks[k]>=ranks[k-1] for k in range(1,10)),'valid prefix ranks')
        return {k:ranks[k]-ranks[k-1] for k in range(1,10) if ranks[k]!=ranks[k-1]}
    def price_case(benefit,debit):
        d=Counter(benefit);d.subtract(debit);d={k:n for k,n in d.items() if n}
        return dict(profile=d,native=P.moment(d,kappa),full=P.moment({r:base.get(r,0)+17*d.get(r,0) for r in base.keys()|d.keys()},kappa))
    results=[];total=0;casecount=0
    for c in g['components']:
        events=c['cache_events'];zevents=c['zero_events'];rows=[M.decode(zeros[e]['row']) for e in zevents]
        need(len(M.echelon(rows))==6,'all six zero rows independent')
        need(all(zeros[e]['rank']<=min(T[h] for h in r) for e,r in zip(zevents,rows)),'zero row support domination')
        preL={e:[M.echelon({h:a for h,a in r.items() if T[h]<=k} for r in L[e]) for k in range(10)] for e in events}
        records=[]
        cacheR={s['event']:abs(len(w['frames'][s['literal'][2]])-len(w['frames'][s['literal'][3]])) for s in g['site_evidence']}
        for mask in range(64):
            need(time.monotonic()<deadline,'bounded refinement')
            selected=[i for i in range(6) if mask>>i&1];bp=[];zpre=[]
            for k in range(10):
                zp=[{h:a for h,a in rows[i].items() if T[h]<=k} for i in selected];zpre.append(zp);bp.append(len(M.echelon(zp)))
            need(bp==c['subsets'][mask]['zero_prefix_ranks'],'independent beta recomputation')
            beta=prof(bp);A=c['subsets'][mask]['already_enabled'];remaining=[e for e in events if e not in A];individual={}
            for e in remaining:
                up=[len(M.echelon(list(preL[e][k].values())+zpre[k])) for k in range(10)]
                gp=[min(bp[k]+1,up[k]) for k in range(10)];need(gp[9]==bp[9]+1,'new cache adds row')
                individual[e]=(gp,prof(gp))
            if mask==0 and events==[35448,35452]:
                need(individual[35448][0][3]==1 and individual[35452][0][3]==0 and individual[35452][0][4]==1,'individual versus union debit control')
            for nmask in range(1<<len(remaining)):
                N=[e for i,e in enumerate(remaining) if nmask>>i&1];benefit=Counter(zeros[zevents[i]]['rank'] for i in selected)
                benefit.update(cacheR[e] for e in A+N);evaluations=[]
                for e in N or [None]:
                    debit=beta if e is None else individual[e][1];evaluations.append((e,debit,price_case(benefit,debit)))
                native=(min(v['native'][0] for e,d,v in evaluations),min(v['native'][1] for e,d,v in evaluations))
                full=(min(v['full'][0] for e,d,v in evaluations),min(v['full'][1] for e,d,v in evaluations))
                controlling=min(evaluations,key=lambda t:t[2]['native'][1])[0]
                record=dict(mask=mask,zero_events=[zevents[i] for i in selected],already_enabled=A,proposed_new=N,
                    beta_prefix=bp,beta_profile=beta,individual_gamma_prefix={str(e):individual[e][0] for e in N},
                    individual_debit_profiles={str(e):d for e,d,v in evaluations},controlling_cache=controlling,
                    native_bound=P.display(native),full_signed17_bound=P.display(full),positive_native=native[0]>0,positive_full=full[0]>0)
                records.append(record);casecount+=1
                if mask==0 and len(N)==2:need(native[1]<0,'individual debit closes generic false positive')
            total+=1
        bounds=(max(Q(r['native_bound']['exact'][0]) for r in records),max(Q(r['native_bound']['exact'][1]) for r in records))
        best=max(records,key=lambda r:Q(r['native_bound']['exact'][1]))
        results.append(dict(cache_events=events,zero_events=zevents,subsets=64,cases=len(records),zero_rows_full_rank=6,
            zero_row_support_minimum=min(T[h] for row in rows for h in row),individual_L_support_minimum={str(e):mins[e] for e in events},
            all_already_enabled_sets_empty=all(not r['already_enabled'] for r in records),max_native_bound=P.display(bounds),best_upper_case=best,
            positive_native_cases=sum(r['positive_native'] for r in records),positive_full_cases=sum(r['positive_full'] for r in records),records=records))
    gap=P.moment({4:1,2:-1,1:-1},kappa);need(gap[0]>0,'both cache prices below required rank4')
    out=dict(status='COMPLETE_INDIVIDUAL_NEW_CACHE_REFINEMENT',source_sha256=g['source_sha256'],generic_receipt_sha256=sha256(raw).hexdigest(),generic_payload_sha256=normpin,
        rank4_minus_both_cache_prices=P.display(gap),
        kappa=str(kappa),subsets_covered=total,cases_evaluated=casecount,components=results,seconds=time.monotonic()-start,
        controls=dict(beta_recomputed=True,individual_prefix_distinguishes_caches=True,generic_false_positive_closed=True),
        scope='Local exact arithmetic: actual debit at least each individual gamma_E, hence max_E. Global linear-domain/source partition proof pending C40 review. No construction or kappa claim.')
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='components'},indent=2))
    for c in results:print(json.dumps({k:v for k,v in c.items() if k!='records'},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE/'REFINED.json');a=p.parse_args();run(a.output)
