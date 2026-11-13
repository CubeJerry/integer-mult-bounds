#!/usr/bin/env python3
"""One nested rank1 import into h770's first-use frame, exact history gate."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import reduce
from hashlib import sha256
from math import gcd,lcm
from pathlib import Path
import gzip,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
FIRST=33814;H=770;FRAME=115
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def dot(row,probe):return sum((v*probe.get(j,0) for j,v in row.items()),Q(0))
def run():
    started=time.monotonic();A=load('past_gate',ROOT/'worker-a/past-constraint/subsets.py');need=A.need
    wp=ROOT/'reference/pr7481/WORD.json.gz';raw=wp.read_bytes();need(sha256(raw).hexdigest()==PIN,'native byte pin');w=json.loads(gzip.decompress(raw));classes=list(map(A.framekey,w['frames']));basekey=classes[FRAME]
    stagepath=ROOT/'worker-a/cache-41646-construction/STAGE1.json';stage=json.loads(stagepath.read_text());need(stage['source_sha256']==PIN,'relation source');u=A.decode(stage['relation']);target={j:-q/u[H] for j,q in u.items() if j!=H}
    ids=defaultdict(list)
    for i,k in enumerate(classes):ids[k].append(i)
    vec=[]
    for mask in range(32):
        v=0
        for j,b in enumerate(w['frames'][FRAME]):
            if mask>>j&1:v^=b
        vec.append(v)
    Cset=set(basekey)
    lowers={tuple(sorted(v for m,v in enumerate(vec) if (m&a).bit_count()%2==0)) for a in range(1,32)}
    uppers={tuple(sorted(Cset|{a^v for a in Cset})) for v in range(512) if v not in Cset}
    need(len(lowers)==31 and len(uppers)==15 and not lowers&uppers,'all abstract nested rank1 neighbors')
    neighbors=sorted(lowers|uppers);relevant=set(neighbors)|{basekey};pools={k:[] for k in relevant};zero_inits=Counter()
    n,owned=w['public'],w['owned_fields'];rows=[{j:Q(1)} for j in range(n)]+[None]*owned;charts=w['initial'].copy()+[None]*owned;counts=Counter();touches=[]
    def observe(event,a,frame,kind):
        if a!=H and classes[frame] in relevant:
            need(H not in rows[a],'no dependence on absent original h770');pools[classes[frame]].append({'event':event,'owner':a,'frame':frame,'kind':kind,'row':rows[a].copy()})
    for a,f in enumerate(w['initial']):observe(-1,a,f,'entrance')
    for event,e in enumerate(w['program'][:FIRST]):
        if event%256==0:need(time.monotonic()-started<60,'bounded exact prefix replay')
        op,a=e[:2];counts[op]+=1
        if a==H or(op in ('ADD','COPY') and e[2]==H):touches.append(event)
        if op=='MOVE':need(charts[a]==e[2] and rows[a] is not None,'MOVE source');charts[a]=e[3];observe(event,a,e[3],'arrival')
        elif op=='INIT':
            need(a>=n and charts[a] is None and rows[a] is None,'fresh INIT');charts[a],rows[a]=e[2],{}
            if classes[e[2]] in relevant:zero_inits[classes[e[2]]]+=1
        elif op=='CLEAR':need(a>=n and charts[a]==e[2],'owned CLEAR');charts[a],rows[a]=None,None
        elif op=='SCALE':need(charts[a]==e[-1] and Q(e[2]),'nonzero SCALE');rows[a]={j:Q(e[2])*v for j,v in rows[a].items()}
        elif op in ('ADD','COPY'):
            b=e[2];need(a!=b and charts[a]==charts[b]==e[-1],'coframed contact')
            if op=='COPY':need(a>=n and not rows[a],'fresh zero COPY')
            A.add(rows[a],rows[b],Q(e[3]))
        else:raise ValueError(op)
    need(not touches and charts[H]==FRAME and rows[H]=={H:Q(1)},'unchanged prefix before first h770 use');need(w['program'][FIRST]==['COPY',1525,770,'1',FRAME],'literal first use')
    bank={}
    for o in pools[basekey]:A.insert(bank,o['row'])
    need(len(bank)==14 and len(pools[basekey])==14,'frozen wave32 base bank control')
    extended={p:r.copy() for p,r in bank.items()};A.insert(extended,{937:Q(1)});need(len(extended)==15,'free affine-coordinate control')
    cp=ROOT/'worker-a/selected/frozen/clifford_exact.py';CL=load('retained_clifford',cp);Cframe=CL.canonical_frame(9,tuple(w['frames'][FRAME]));records=[];hits=[];allbank={p:r.copy() for p,r in extended.items()}
    for key in neighbors:
        need(time.monotonic()-started<60,'bounded neighbor elimination');other={}
        for o in pools[key]:A.insert(other,o['row']);A.insert(allbank,o['row'])
        combined={p:r.copy() for p,r in extended.items()}
        for row in other.values():A.insert(combined,row)
        residual=A.normal(target,combined);actual_rank=None
        if ids[key]:
            f=ids[key][0];op=CL.canonical_frame(9,tuple(w['frames'][f])).adjoint().then(Cframe);actual_rank=CL.rank([x for x,z,p in op.tab[9:]]);need(actual_rank==1,'actual catalog interface B rank1')
        rec={'neighbor_index':len(records),'dimension':(len(key).bit_length()-1),'span':list(key),'catalog_frame_ids':ids[key],'history_observations':len(pools[key]),'history_kinds':dict(Counter(o['kind'] for o in pools[key])),'history_rank':len(other),'combined_rank_with_base_and_e937':len(combined),'actual_catalog_interface_rank':actual_rank,'hit':not residual,'residual':A.encode(residual),'basis':A.encbasis(other)};records.append(rec)
        if not residual:hits.append(rec)
    aggregate_residual=A.normal(target,allbank)
    result={'source_sha256':PIN,'relation_receipt_sha256':sha256(stagepath.read_bytes()).hexdigest(),'clifford_code_sha256':sha256(cp.read_bytes()).hexdigest(),'first_use_event':FIRST,'target_frame':FRAME,'target_frame_basis':w['frames'][FRAME],'prefix_instructions':FIRST,'earlier_h770_touches':touches,'abstract_lower_neighbors':31,'abstract_upper_neighbors':15,'neighbors_tested':46,'catalog_lower_neighbors':sum(bool(ids[k]) for k in lowers),'catalog_upper_neighbors':sum(bool(ids[k]) for k in uppers),'catalog_frame_ids':sorted(f for k in neighbors for f in ids[k]),'base_history_observations':14,'base_history_rank':14,'hits':len(hits),'records':records,'aggregate_rank':len(allbank),'aggregate_residual':A.encode(aggregate_residual),'target':A.encode(target),'aggregate_basis':A.encbasis(allbank),'event_counts_symbolic':dict(counts),'scope':'One nested dimension4/6 rank1 import from original strict history into frame115, no added incoming transports or changed prefix. Source copies, pooled storage, affine e937, ordinary and erasure work free. Nonnested rank1 interfaces outside this domain are not asserted covered.'}
    # If a pooled one-import hit occurs, expose exact chronological coefficients.
    if hits:
        hit=hits[0];key=tuple(hit['span']);obs=pools[basekey]+pools[key];basis={}
        source_rows=[o['row'] for o in obs]+[{937:Q(1)}]
        for i,row in enumerate(source_rows):
            value=row.copy();rep={i:Q(1)}
            for p in sorted(basis):
                if value.get(p):v,r=basis[p];q=-value[p];A.add(value,v,q);A.add(rep,r,q)
            if value:
                p=min(value);q=1/value[p];basis[p]=({j:q*v for j,v in value.items()},{j:q*v for j,v in rep.items()})
        value=target.copy();rep={}
        for p in sorted(basis):
            if value.get(p):v,r=basis[p];q=value[p];A.add(value,v,-q);A.add(rep,r,q)
        need(not value,'exact one-import witness');c=rep.get(len(obs),Q(0))
        result.update({'status':'ONE_NESTED_RANK1_IMPORT_POOLED_PROVIDER_HIT','witness_neighbor':hit['neighbor_index'],'relation_lambda':str(-Q(17,32)*c),'provider_witness':[{'coefficient':str(q),**{k:v for k,v in obs[i].items() if k!='row'}} for i,q in sorted(rep.items()) if i<len(obs)],'seconds':time.monotonic()-started})
    else:
        # Prefer one common separator for every import; otherwise choose a largest-bank miss.
        if aggregate_residual:dualbank=allbank;dualres=aggregate_residual;dualkeys=relevant;dual_scope='all46_neighbors_simultaneously'
        else:
            chosen=max(records,key=lambda r:r['combined_rank_with_base_and_e937']);key=tuple(chosen['span']);dualbank={p:r.copy() for p,r in extended.items()}
            for o in pools[key]:A.insert(dualbank,o['row'])
            dualres=A.normal(target,dualbank);dualkeys={basekey,key};dual_scope={'neighbor_index':chosen['neighbor_index'],'catalog_frame_ids':chosen['catalog_frame_ids']}
        p=min(dualres);probe={p:Q(1)}
        for pivot in sorted(dualbank,reverse=True):
            v=-sum((q*probe.get(j,0) for j,q in dualbank[pivot].items() if j!=pivot),Q(0))
            if v:probe[pivot]=v
        den=lcm(*(v.denominator for v in probe.values()));probe={j:int(v*den) for j,v in probe.items()};g=reduce(gcd,(abs(v) for v in probe.values()));probe={j:v//g for j,v in probe.items()};need(not probe.get(H) and not probe.get(937),'retained dual and affine unit')
        value=dot(target,probe);need(value and all(not dot(row,probe) for row in dualbank.values()),'exact dual separator')
        den=value.denominator;probe={j:v*den for j,v in probe.items()};probe[H]=int(value*den);g=reduce(gcd,(abs(v) for v in probe.values()));probe={j:v//g for j,v in probe.items()};need(dot(u,probe)==0 and not probe.get(937),'full graph-family probe')
        values=[Q(probe.get(j,0)) for j in range(n)]+[None]*owned;charts=w['initial'].copy()+[None]*owned;scalar=Counter();contact_checks=0
        def scalar_observe(event,a,f,kind):
            if a!=H and classes[f] in dualkeys:need(values[a]==0,'direct scalar history observation zero');scalar[kind]+=1
        for a,f in enumerate(w['initial']):scalar_observe(-1,a,f,'entrance')
        for event,e in enumerate(w['program'][:FIRST]):
            if event%256==0:need(time.monotonic()-started<60,'bounded scalar dual replay')
            op,a=e[:2]
            if op=='MOVE':need(charts[a]==e[2],'scalar MOVE');charts[a]=e[3];scalar_observe(event,a,e[3],'arrival')
            elif op=='INIT':need(charts[a] is None,'scalar INIT');charts[a],values[a]=e[2],Q(0)
            elif op=='CLEAR':need(charts[a]==e[2],'scalar CLEAR');charts[a],values[a]=None,None
            elif op=='SCALE':
                need(charts[a]==e[-1],'scalar SCALE')
                if classes[e[-1]] in dualkeys:need(values[a]==0,'dual-class scalar zero');contact_checks+=1
                values[a]*=Q(e[2])
            elif op in ('ADD','COPY'):
                b=e[2];need(a!=b and charts[a]==charts[b]==e[-1],'scalar contact')
                if op=='COPY':need(values[a]==0,'scalar COPY')
                if classes[e[-1]] in dualkeys:need(values[a]==values[b]==0,'dual-class contact operands zero');contact_checks+=1
                values[a]+=Q(e[3])*values[b]
        expected=Counter(o['kind'] for k in dualkeys for o in pools[k]);need(scalar==expected,'direct observation census');need(values[H]==probe[H] and values[H],'required helper nonzero at firstuse')
        result.update({'status':'NO_ONE_NESTED_RANK1_IMPORT_PROVIDER','dual_scope':dual_scope,'integer_graph_input_probe':{str(j):v for j,v in sorted(probe.items())},'probe_h770_value':str(values[H]),'probe_e937_value':0,'direct_scalar_observations_zero':dict(scalar),'direct_scalar_contacts_zero':contact_checks,'complete_prefix_passes':2,'observations':[{'domain':'base' if k==basekey else 'neighbor','span':list(k),**{j:v for j,v in o.items() if j!='row'},'row':A.encode(o['row']),'probe_value':'0' if k in dualkeys else None} for k in sorted(relevant) for o in pools[k]],'seconds':time.monotonic()-started})
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','aggregate_residual','target','aggregate_basis','observations')},indent=2))
if __name__=='__main__':run()
