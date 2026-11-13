#!/usr/bin/env python3
"""Past-only arbitrary-one-helper-relation cache gate; owned erasure free.
No extra zero-MOVE credit. Wave26 is retained unchanged as zero-cleanup scope.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import gzip, importlib.util, json, time
ROOT=Path('/workspace/scratch/19b21bdb3d72'); HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
EVENTS=(30581,30593,35152,35448,35452,36346,36358,39875,39884,41646,42487,42500,44253,45656)
def need(ok,label):
    if not ok: raise ValueError(label)
def add(a,b,q):
    for j,v in b.items():
        z=a.get(j,Q(0))+q*v
        if z:a[j]=z
        else:a.pop(j,None)
def normal(row,basis):
    row=row.copy()
    for p in sorted(basis):
        if row.get(p):add(row,basis[p],-row[p])
    return row
def insert(basis,row):
    row=normal(row,basis)
    if row:
        p=min(row);basis[p]={j:v/row[p] for j,v in row.items()}
def decode(row):return {int(j):Q(v) for j,v in row.items()}
def encode(row):return {str(j):str(v) for j,v in sorted(row.items())}
def encbasis(basis):return {str(p):encode(row) for p,row in sorted(basis.items())}
def framekey(frame):
    addresses={0}
    for v in frame:addresses|={a^v for a in addresses}
    return tuple(sorted(addresses))
def kernel_lifts(rows,project):
    image={};kernel={}
    for original in rows:
        value,lift=project(original),original.copy()
        for p in sorted(image):
            if value.get(p):
                old,oldlift=image[p];q=-value[p];add(value,old,q);add(lift,oldlift,q)
        if value:
            p=min(value);q=1/value[p]
            image[p]=({j:q*v for j,v in value.items()},{j:q*v for j,v in lift.items()})
        else:insert(kernel,lift)
    return kernel,len(image)
def intersect(left,right):
    result,rank=kernel_lifts(list(left.values()),lambda r:normal(r,right))
    need(len(result)+rank==len(left),'intersection rank-nullity')
    need(all(not normal(r,left) and not normal(r,right) for r in result.values()),'intersection inclusion')
    union={}
    for row in list(left.values())+list(right.values()):insert(union,row)
    need(len(result)==len(left)+len(right)-len(union),'independent union-rank intersection formula')
    return result
def extension(old,target,mains,helpers):
    extended={p:r.copy() for p,r in old.items()};need(normal(target,old),'original target nonmembership');insert(extended,target)
    need(len(extended)==len(old)+1,'one-dimensional full extension')
    result,rank=kernel_lifts(list(extended.values()),lambda r:{j:v for j,v in r.items() if j in mains})
    need(len(result)==len(extended)-rank,'helper extension rank-nullity')
    need(all(set(r)<=helpers and not normal(r,extended) for r in result.values()),'helper-only extension inclusion')
    projected={}
    for row in extended.values():insert(projected,{j:v for j,v in row.items() if j in mains})
    need(rank==len(projected),'independent projected rank')
    return result,rank
def run():
    start=time.monotonic()
    meet=intersect({0:{0:Q(1),2:Q(1)},1:{1:Q(1)}},{1:{1:Q(1)},2:{2:Q(1)}})
    need(len(meet)==1 and not normal({1:Q(1)},meet),'synthetic intersection control')
    ext,_=extension({0:{0:Q(1)}},{0:Q(1),2:Q(2)},{0,1},{2})
    need(len(ext)==1 and not normal({2:Q(1)},ext),'synthetic helper-extension control')
    raw=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes();need(sha256(raw).hexdigest()==PIN,'word byte pin')
    w=json.loads(gzip.decompress(raw));classes=list(map(framekey,w['frames']))
    mains=set(w['live'])|{j+112 for j in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);helpers=set(range(w['public']))-mains
    need(len(mains)==400 and len(helpers)==1101,'actual main-helper partition')
    paths={'projected':ROOT/'projected-temporal-result.json','targets':ROOT/'independent-temporal-result.json','six':ROOT/'worker-b/history-cache/FILTER.json','last':ROOT/'worker-b/two-cache/FILTER.json','helpers':ROOT/'worker-b/cold-single/SCAN.json'}
    data={k:json.loads(p.read_text()) for k,p in paths.items()};need(all(d['source_sha256']==PIN for d in data.values()),'all input source pins')
    targets={r['event']:r for r in data['targets']['records'] if r['event'] in EVENTS};need(len(targets)==14,'all fourteen targets')
    need({r['event'] for r in data['projected']['records'] if r['earlier_B_hit']}==set(EVENTS),'all fourteen past-main survivors')
    two_events={r['event'] for r in data['last']['records']}
    sites={};site_records=[]
    for event in EVENTS:
        need(time.monotonic()-start<60,'bounded extension construction');rec=targets[event];literal=w['program'][event]
        need(literal==['MOVE',rec['owner'],rec['source'],rec['destination'],True],'actual owned MOVE literal')
        target=decode(rec['target']);need(set(target)&mains,'helper-only relation cannot zero main-nonzero target')
        need(rec['rank']==abs(len(w['frames'][rec['source']])-len(w['frames'][rec['destination']])),'literal paid rank')
        fields=[('past','earlier_generators' if event in two_events else 'generators','last' if event in two_events else 'six',rec['destination'])]
        spaces=[];histories=[];sides=[]
        for side,field,origin,frame in fields:
            gens=[g for g in data[origin][field] if classes[g['frame']]==classes[frame] and (g['event']<event if side=='past' else g['event']>event)]
            gens.sort(key=lambda g:g['event'],reverse=side=='future');old={}
            for g in gens:insert(old,decode(g['row']))
            need(len(old)==rec['earlier_B_rank' if side=='past' else 'later_A_rank'],'strict full history rank')
            space,mainrank=extension(old,target,mains,helpers);spaces.append(space);histories.append((side,old))
            sides.append({'side':side,'history_rank':len(old),'generator_count':len(gens),'extended_main_rank':mainrank,'helper_extension_dim':len(space),'history_basis':encbasis(old),'helper_extension_basis':encbasis(space)})
        allowed=spaces[0]
        for space in spaces[1:]:allowed=intersect(allowed,space)
        sites[event]={'space':allowed,'histories':histories,'rank':rec['rank']}
        site_records.append({'event':event,'owner':rec['owner'],'rank':rec['rank'],'literal':literal,'required_sides':sides,'joint_direction_dim':len(allowed),'joint_basis':encbasis(allowed)})
    spec=importlib.util.spec_from_file_location('budget',ROOT/'budget_price.py');price=importlib.util.module_from_spec(spec);spec.loader.exec_module(price)
    iraw=price.INVOICE.read_bytes();need(sha256(iraw).hexdigest()==price.PIN,'full invoice pin');invoice=json.loads(iraw)
    canonical=sha256(json.dumps(w,sort_keys=True,separators=(',',':')).encode()).hexdigest();need(canonical==invoice['new_native'],'actual native payload binds invoice')
    t,p=invoice['after']['T'],invoice['after']['P'];signed=Counter({r:t.get(r,0)-p.get(r,0) for r in t.keys()|p.keys()});kappa=Q(38,10000);baseline=price.moment(signed,kappa)
    ranks={h:abs(len(w['frames'][w['initial'][h]])-len(w['frames'][w['final'][h]])) for h in helpers}
    need(all(ranks[r['helper']]==r['target_rank'] for r in data['helpers']['records']),'all actual helper target ranks')
    cache={};records=[];zero_masks=[]
    for mask in range(1,1<<len(EVENTS)):
        need(time.monotonic()-start<60,'bounded subset stage');bit=mask&-mask;event=EVENTS[bit.bit_length()-1];rest=mask^bit
        space=sites[event]['space'] if not rest else (intersect(cache[rest],sites[event]['space']) if cache[rest] else {});cache[mask]=space
        if not space:
            zero_masks.append(mask);continue
        included=[e for j,e in enumerate(EVENTS) if mask&(1<<j)]
        bad=[(e,side) for e in included for side,old in sites[e]['histories'] if all(not normal(row,old) for row in space.values())]
        support=set().union(*(set(row) for row in space.values())) if space else set();eligible=bool(space) and not bad
        row={'mask':mask,'events':included,'dimension':len(space),'eligible':eligible,'contained_in_old_history':bad,'coordinate_support':sorted(support),'basis':encbasis(space)}
        if eligible:
            minrank=min(ranks[h] for h in support);cheap=sorted(h for h in support if ranks[h]==minrank)
            delta=Counter(str(sites[e]['rank']) for e in included);delta[str(minrank)]-=1;trial=signed.copy()
            for rank,count in delta.items():trial[rank]+=17*count
            interval=price.moment(trial,kappa);need(interval[0]>0 or interval[1]<0,'strict directed budget sign')
            row.update({'cheapest_demoted_target_rank':minrank,'cheapest_coordinates':cheap,'no_zero_credit_native_gain':price.display(price.moment(delta,kappa)),'optimistic_complete_moment':price.display(interval),'raw_budget_favorable':interval[0]>0})
        records.append(row)
    out={'status':'COMPLETE_EXACT_FOURTEEN_SITE_PAST_ONLY_HELPER_RELATION_SUBSETS','source_sha256':PIN,'source_payload_sha256':canonical,'input_sha256':{k:sha256(p.read_bytes()).hexdigest() for k,p in paths.items()},'invoice_sha256':price.PIN,'budget_code_sha256':sha256((ROOT/'budget_price.py').read_bytes()).hexdigest(),'site_count':14,'expected_subsets':16383,'covered_subsets':len(records)+len(zero_masks),'zero_intersections':len(zero_masks),'zero_masks':zero_masks,'eligible_subsets':sum(r['eligible'] for r in records),'raw_budget_favorable_subsets':sum(r.get('raw_budget_favorable',False) for r in records),'kappa':str(kappa),'native_calls':17,'extra_zero_MOVE_credit':False,'baseline_complete_moment':price.display(baseline),'controls':{'synthetic_intersection':True,'synthetic_helper_extension':True},'sites':site_records,'subsets':records,'seconds':time.monotonic()-start,'owned_source_erasure_granted_free':True,'scope':'Past-only optimistic gate. One arbitrary homogeneous helper-only relation; generic direction must miss all old earlier histories and retain nonzero demoted coordinate. Private source erasure, preparation, cleanup, storage and ordinary work are free. No extra zero-MOVE credit, changed operations/frames/histories, physical source or kappa.'}
    (HERE/'SUBSETS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('sites','subsets','zero_masks')},indent=2))
    print('sites',[(s['event'],[r['helper_extension_dim'] for r in s['required_sides']],s['joint_direction_dim']) for s in site_records])
    print('favorable',[(r['events'],r['dimension'],r['cheapest_demoted_target_rank'],r['optimistic_complete_moment']['decimal_display_only']) for r in records if r.get('raw_budget_favorable')])
if __name__=='__main__':run()
