#!/usr/bin/env python3
"""Deferred h770 initialization from its strict frame115 native history."""
from collections import Counter
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
import gzip, importlib.util, json, sys, time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
FIRST=33814;H=770;FRAME=115
def load(name,path):
    sp=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(sp);sys.modules[name]=mod;sp.loader.exec_module(mod);return mod
def dot(row,probe):return sum((v*probe.get(j,0) for j,v in row.items()),Q(0))
def run():
    start=time.monotonic();A=load('past_gate',ROOT/'worker-a/past-constraint/subsets.py');need=A.need
    wp=ROOT/'reference/pr7481/WORD.json.gz';raw=wp.read_bytes();need(sha256(raw).hexdigest()==PIN,'actual source pin');w=json.loads(gzip.decompress(raw));classes=list(map(A.framekey,w['frames']));key=classes[FRAME]
    stagepath=ROOT/'worker-a/cache-41646-construction/STAGE1.json';stage=json.loads(stagepath.read_text());need(stage['source_sha256']==PIN,'relation source pin');u=A.decode(stage['relation']);need(u[H]==Q(-17,32),'exact h770 coefficient')
    target={j:-v/u[H] for j,v in u.items() if j!=H};free={937:Q(1)}
    n,owned=w['public'],w['owned_fields'];rows=[{j:Q(1)} for j in range(n)]+[None]*owned;charts=w['initial'].copy()+[None]*owned
    observations=[];counts=Counter();zero_inits=0;touches=[]
    def observe(event,a,frame,kind):
        if a!=H and classes[frame]==key:
            need(H not in rows[a],'provider independent of absent h770');observations.append({'event':event,'owner':a,'frame':frame,'kind':kind,'row':rows[a].copy()})
    for a,f in enumerate(w['initial']):observe(-1,a,f,'entrance')
    for event,e in enumerate(w['program'][:FIRST]):
        if event%256==0:need(time.monotonic()-start<60,'bounded full-rational prefix replay')
        op,a=e[:2];counts[op]+=1
        if a==H or (op in ('ADD','COPY') and e[2]==H):touches.append(event)
        if op=='MOVE':need(charts[a]==e[2] and rows[a] is not None,'MOVE source');charts[a]=e[3];observe(event,a,e[3],'arrival')
        elif op=='INIT':
            need(a>=n and charts[a] is None and rows[a] is None,'fresh owned INIT');charts[a],rows[a]=e[2],{}
            if classes[e[2]]==key:zero_inits+=1
        elif op=='CLEAR':need(a>=n and charts[a]==e[2],'owned CLEAR');charts[a],rows[a]=None,None
        elif op=='SCALE':need(charts[a]==e[-1] and Q(e[2]),'nonzero SCALE');rows[a]={j:Q(e[2])*v for j,v in rows[a].items()}
        elif op in ('ADD','COPY'):
            b=e[2];need(a!=b and charts[a]==charts[b]==e[-1],'coframed scalar contact')
            if op=='COPY':need(a>=n and not rows[a],'fresh zero COPY')
            A.add(rows[a],rows[b],Q(e[3]))
        else:raise ValueError(op)
    need(not touches and rows[H]=={H:Q(1)} and charts[H]==FRAME,'no earlier h770 use or dependency')
    need(w['program'][FIRST]==['COPY',1525,770,'1',FRAME],'literal first native use')
    bank={}
    for o in observations:A.insert(bank,o['row'])
    extended={p:r.copy() for p,r in bank.items()};A.insert(extended,free);residual=A.normal(target,extended)
    result={'source_sha256':PIN,'relation_receipt_sha256':sha256(stagepath.read_bytes()).hexdigest(),'first_use_event':FIRST,'first_use_literal':w['program'][FIRST],'prefix_instructions':FIRST,'earlier_h770_touches':touches,'provider_frame':FRAME,'provider_frame_basis':w['frames'][FRAME],'provider_observations':len(observations),'provider_kinds':dict(Counter(o['kind'] for o in observations)),'free_zero_INITs':zero_inits,'provider_bank_rank':len(bank),'bank_plus_e937_rank':len(extended),'target':A.encode(target),'e937_affine_parameter_granted_free':True,'target_residual':A.encode(residual),'provider_basis':A.encbasis(bank),'extended_basis':A.encbasis(extended),'h770_sole_cheapest_R4_coordinate':True,'other_support_rank_minimum':None,'scope':'Deferred initialization at first use; strictly earlier same-subspace observations excluding h770 entrance. No added paid transport or changed prefix. One relation family; other retained inputs arbitrary. No source or kappa.'}
    pr=json.loads((ROOT/'worker-a/past-constraint/SUBSETS.json').read_text());choice=next(r for r in pr['subsets'] if r['events']==[41646]);need(choice['cheapest_coordinates']==[H],'sole R4 support coordinate')
    support=choice['coordinate_support'];ranks={h:abs(len(w['frames'][w['initial'][h]])-len(w['frames'][w['final'][h]])) for h in support};result['other_support_rank_minimum']=min(v for h,v in ranks.items() if h!=H);result['support_target_ranks']={str(h):v for h,v in ranks.items()}
    if not residual:
        result['status']='AFFINE_DEFERRED_TARGET_IN_POOLED_HISTORY';result['seconds']=time.monotonic()-start
        result['observations']=[{**{k:v for k,v in o.items() if k!='row'},'row':A.encode(o['row'])} for o in observations]
        (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('observations','target','provider_basis','extended_basis','support_target_ranks')},indent=2));return
    # An independent integral input probe from exact dual back substitution.
    p=min(residual);need(p not in extended,'free quotient coordinate');probe={p:Q(1)}
    for pivot in sorted(extended,reverse=True):
        v=-sum((q*probe.get(j,0) for j,q in extended[pivot].items() if j!=pivot),Q(0))
        if v:probe[pivot]=v
    den=lcm(*(v.denominator for v in probe.values()));probe={j:int(v*den) for j,v in probe.items()};g=reduce(gcd,(abs(v) for v in probe.values()));probe={j:v//g for j,v in probe.items()}
    need(not probe.get(H) and not probe.get(937),'probe has no h770 or affine coordinate')
    vH=dot(target,probe);need(vH and all(not dot(o['row'],probe) for o in observations),'dual separator')
    factor=vH.denominator;probe={j:v*factor for j,v in probe.items()};probe[H]=int(vH*factor);g=reduce(gcd,(abs(v) for v in probe.values()));probe={j:v//g for j,v in probe.items()}
    need(dot(u,probe)==0 and not probe.get(937) and probe[H],'one constraint satisfied for every affine parameter')
    values=[Q(probe.get(j,0)) for j in range(n)]+[None]*owned;charts=w['initial'].copy()+[None]*owned;scalar=Counter();scalar_contacts=0
    def scalar_observe(event,a,frame,kind):
        if a!=H and classes[frame]==key:
            need(values[a]==0,'direct scalar provider observation zero');scalar[kind]+=1
    for a,f in enumerate(w['initial']):scalar_observe(-1,a,f,'entrance')
    for event,e in enumerate(w['program'][:FIRST]):
        if event%256==0:need(time.monotonic()-start<60,'bounded scalar prefix replay')
        op,a=e[:2]
        if op=='MOVE':need(charts[a]==e[2],'scalar MOVE');charts[a]=e[3];scalar_observe(event,a,e[3],'arrival')
        elif op=='INIT':need(charts[a] is None,'scalar INIT');charts[a],values[a]=e[2],Q(0)
        elif op=='CLEAR':need(charts[a]==e[2],'scalar CLEAR');charts[a],values[a]=None,None
        elif op=='SCALE':
            need(charts[a]==e[-1],'scalar SCALE')
            if classes[e[-1]]==key:need(values[a]==0,'scalar frame115 SCALE zero');scalar_contacts+=1
            values[a]*=Q(e[2])
        elif op in ('ADD','COPY'):
            b=e[2];need(a!=b and charts[a]==charts[b]==e[-1],'scalar contact')
            if op=='COPY':need(values[a]==0,'scalar COPY zero')
            if classes[e[-1]]==key:need(values[a]==values[b]==0,'scalar frame115 contact operands zero');scalar_contacts+=1
            values[a]+=Q(e[3])*values[b]
    need(dict(scalar)==result['provider_kinds'],'all scalar observation counts match symbolic pass');need(values[H]==probe[H] and values[H]!=0,'nonzero required helper at first use')
    result.update({'status':'NO_AFFINE_DEFERRED_H770_PROVIDER_WITHOUT_TRANSPORT','integer_input_probe':{str(j):v for j,v in sorted(probe.items())},'probe_satisfies_entire_relation_family':True,'probe_h770_value':str(values[H]),'probe_e937_value':0,'direct_scalar_observations':dict(scalar),'direct_scalar_frame115_contacts_zero':scalar_contacts,'complete_prefix_passes':2,'event_counts_symbolic':dict(counts),'seconds':time.monotonic()-start,'observations':[{**{k:v for k,v in o.items() if k!='row'},'row':A.encode(o['row']),'probe_value':'0'} for o in observations]})
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('target','provider_basis','extended_basis','observations','support_target_ranks')},indent=2))
if __name__=='__main__':run()
