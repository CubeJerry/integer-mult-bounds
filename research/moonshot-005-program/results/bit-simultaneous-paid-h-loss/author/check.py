#!/usr/bin/env python3
"""Actual fixed-frontier owner census and exact joint-loss movement screens."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import gzip,hashlib,importlib.util,itertools,json

def need(ok,why):
    if not ok: raise ValueError(why)

ap=ArgumentParser(); ap.add_argument('--repo',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args(); here=Path(__file__).resolve().parent; base=args.repo/'research/moonshot-005-program/results'
for p,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
    need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest()==h,'pin '+p)
layout=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
owner_H={};quota=Counter()
for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
    phase,j,x,h,d,_,source,_=json.loads(line)
    if phase=='X' and h is not None:
        owner=(j,int(x)); need(source==j and owner not in owner_H,'disjoint genuine original owner')
        owner_H[owner]=h;quota[h,j]+=1
need(len(owner_H)==53280 and set(j for j,x in owner_H)==set(range(111)),'entire original X frontier')
need(all({x for j0,x in owner_H if j0==j}==set(range(480)) for j in range(111)),'all480 source coordinates at every donor')
profiles=Counter();double=[];single=[]
for h,donors in enumerate(layout['A2']):
    if all(j<111 for j in donors):
        profile=tuple(sorted(quota[h,j] for j in donors));profiles[profile]+=1
        if profile==(30,30,30):double.append(h)
        if profile==(15,15,15):single.append(h)
need(profiles=={(30,30,30):65,(15,15,15):816},'exact native same-quota H census')
graph=defaultdict(set);degree=Counter()
for h in double:
    for j in layout['A2'][h]:
        graph[('H',h)].add(('X',j));graph[('X',j)].add(('H',h));degree[j]+=1
seen={next(iter(graph))};stack=list(seen)
while stack:
    for y in graph[stack.pop()]:
        if y not in seen:seen.add(y);stack.append(y)
need(len(seen)==len(graph)==158 and len(degree)==93 and Counter(degree.values())=={1:32,2:30,3:21,4:10},'single native double-quota incidence component')

# Exhaust every original input of a coupled invertible four-bit preparation.
fibres=defaultdict(list);overlap=defaultdict(list)
for x in itertools.product(range(2),repeat=4):
    z=(x[0]^x[1],x[1]^x[2],x[2]^x[3],x[3])
    fibres[(z[0],z[2])].append((x,(z[1],z[3]),z[1]^z[3]))
    overlap[(z[0],z[2],z[3])].append(x)
need(len(fibres)==4 and all(len(v)==4 and len({t for x,t,p in v})==4 and len({p for x,t,p in v})==2 for v in fibres.values()),'two independent losses require four joint transcripts; parity fails')
need(len(overlap)==8 and set(map(len,overlap.values()))=={2},'overlapping nominal losses are not additive')

spec=importlib.util.spec_from_file_location('retained_exact_price',base/'kappa-significant-gain-screen/root-review/check.py')
price=importlib.util.module_from_spec(spec);spec.loader.exec_module(price)
old_n={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};old_h={2:1,4:25,6:1,8:410}
gap=price.hist((36,old_h),(-36,old_n),(111,price.wrapper(9)))
allowance=price.hist((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}))
for j in range(1,9):allowance[7*j+1]+=F(37,3);allowance[7*j]-=F(37,3)
Q0={1:F(4451,8),2:F(7213,16),4:F(24)}
def margin(e,m,q=34560):
    h=price.hist((1,allowance),(-1,Q0),(-F(q,3840),{8:1}),(-F(e,3840),{6:1}))
    if m is not None:h=price.hist((1,h),(F(1,36*(m-1)),gap))
    return price.moment(h,F(1,200))
caps=[]
for m,wanted in [(870,21),(None,22)]:
    signs=[]
    for units in range(26):
        lo,hi=margin(8*units,m);need(lo>0 or hi<0,'strict rational sign')
        signs.append({'eight_field_units':units,'exports':8*units,'passes':lo>0,'margin':[str(lo),str(hi)]})
    maximum=max(x['eight_field_units'] for x in signs if x['passes']);need(maximum==wanted,'exact loss-unit cap')
    need(margin(16*65,m)[1]<0,'uniform rank44 use at all65 double-quota centres fails')
    caps.append({'m':m,'maximum_eight_field_loss_units':maximum,'maximum_double_quota_rank_one_centres':maximum//2,'signs':signs})
need(margin(16,870,34675)[0]>0 and margin(16,870,34676)[1]<0,'one constructed H retains exact return cap34675')
result={'status':'PASS_SIMULTANEOUS_PAID_H_LOSS_OWNER_AND_PRICE','base_owners':53280,'donors':111,'coordinates_per_donor':480,
        'native_double_quota_H':double,'native_single_quota_count':816,'active_double_quota_donors':93,'double_quota_degree_histogram':dict(sorted(Counter(degree.values()).items())),
        'double_quota_component_count':1,'cycle_rank':195-158+1,'loss_budget':caps,'joint_nonlinear_transcript_control':True,'overlapping_groups_control':True,
        'actual_complete_source_preparation_constructed':False,'arbitrary_new_route_price_lower_bound':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],53280,65,816,21,22,flush=True)
