#!/usr/bin/env python3
"""Independent recovery review: no author/predecessor code imports.

Input bytes are read only. Values are full 222-coordinate symmetric-difference
sets; real charts use exact Fraction row operations. The all-width implications
are in REVIEW.md rather than inferred from execution.
"""
from __future__ import annotations
import argparse, copy, hashlib, json
from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path

N=111
SOURCE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
CP='research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint6-evidence'

def insist(p,msg):
    if not p: raise ValueError(msg)

@cache
def reduced(rows):
    a=[list(map(Fraction,r)) for r in rows]
    k=0
    for c in range(8):
        ix=next((i for i in range(k,len(a)) if a[i][c]),None)
        if ix is None: continue
        a[k],a[ix]=a[ix],a[k]
        q=a[k][c];a[k]=[x/q for x in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][c]:
                q=a[i][c];a[i]=[x-q*y for x,y in zip(a[i],a[k])]
        k+=1
    return tuple(tuple(r) for r in a[:k])

def chart(spec):
    rows=reduced(tuple(tuple(r) for r in spec['rows']))
    if spec['kind']=='span': return rows
    insist(spec['kind']=='ann','unrecognized chart kind')
    pivots=[next(i for i,x in enumerate(r) if x) for r in rows]
    result=[]
    for c in range(8):
        if c in pivots: continue
        v=[Fraction(0)]*8;v[c]=1
        for p,r in zip(pivots,rows):v[p]=-r[c]
        result.append(tuple(v))
    return reduced(tuple(result))

@cache
def subset(a,b):return len(reduced(a+b))==len(b)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def replay(w,source,snapshot_indices=()):
    R=source['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
    for i,r in enumerate(R):
        insist(C[f'L{i}']==chart({'kind':'span','rows':[r]}),'native line identity')
        insist(C[f'F{i}']==chart({'kind':'ann','rows':[r]}),'native facet identity')
    insist(len(C['zero'])==0 and len(C['Hub'])==8,'native extremal charts')
    values={f'X{i}':frozenset([i])for i in range(N)}
    values.update({f'Y{i}':frozenset([N+i])for i in range(N)})
    loc={f'X{i}':f'L{i}'for i in range(N)};loc.update({f'Y{i}':'zero'for i in range(N)})
    owned=set();born=set();counts=Counter();profile=Counter();dirty=peak=0;snapshots={};events=[]
    wanted=set(snapshot_indices)
    for k,op in enumerate(w['operations']):
        if k in wanted:snapshots[k]=(values.copy(),loc.copy())
        tag,name,*rest=op;counts[tag]+=1
        if tag=='INIT':
            insist(name not in values and name not in born,(k,'fresh owner',op))
            insist(rest[0] in C,(k,'known chart',op));owned.add(name);born.add(name);values[name]=frozenset();loc[name]=rest[0]
        elif tag=='ADD':
            dst=rest[0];insist(name in values and dst in values and name!=dst,(k,'distinct live add',op))
            insist(C[loc[name]]==C[loc[dst]],(k,'same real chart',op,loc[name],loc[dst]))
            values[dst]=values[dst]^values[name]
        elif tag=='MOVE':
            insist(name in values and rest[0] in C,(k,'live move',op))
            a,b=C[loc[name]],C[rest[0]]
            insist(subset(b,a) if name in owned else subset(a,b),(k,'directed move',op,loc[name]))
            d=abs(len(a)-len(b));insist(d>0,(k,'strict move',op));profile[d]+=1
            events.append((k,name,loc[name],rest[0],d,name in owned));loc[name]=rest[0]
        elif tag=='CLEAR':
            insist(name in owned,(k,'owned retirement',op));dirty+=bool(values[name]);owned.remove(name);del values[name];del loc[name]
        else:raise ValueError((k,'opcode',tag))
        peak=max(peak,len(owned))
    insist(not owned and len(values)==222,'all original lifetimes closed')
    targets=set(w['targets']);actual=[]
    for i in range(N):
        insist(values[f'X{i}']==frozenset([i]) and C[loc[f'X{i}']]==C['Hub'],('original restoration',i))
        expected=frozenset([N+i]+([i]if i in targets else []))
        insist(values[f'Y{i}']==expected and C[loc[f'Y{i}']]==C[f'F{i}'],('receiver endpoint',i))
        if values[f'Y{i}']==frozenset([N+i,i]):actual.append(i)
    return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'dirty_clear':dirty,'peak_owned':peak,'completed_outputs':actual,'all_222_column_endpoints':True},snapshots,C,events

def binary_basis(rows):
    base={}
    for row in rows:
        z=sum(1<<i for i in row)
        while z:
            p=z.bit_length()-1
            if p in base:z^=base[p]
            else:base[p]=z;break
    return base

def in_span(row,b):
    z=sum(1<<i for i in row)
    while z:
        p=z.bit_length()-1
        if p not in b:return False
        z^=b[p]
    return True

@cache
def power_interval(d):
    # Exact independent binary-search enclosure of d^(199/200).
    scale=10**36;target=d**199*scale**200
    lo,hi=0,d*scale+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    insist(lo**200<=target<hi**200,'root interval certificate')
    if lo**200==target:hi=lo
    return Fraction(lo,scale),Fraction(hi,scale)

def moment(profile):
    lo=hi=Fraction(0)
    for d,c in profile.items():
        a,b=power_interval(int(d));lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi

def interval_json(v):
    from decimal import Decimal,localcontext
    with localcontext()as ctx:
        ctx.prec=60
        return {'rational':[str(x)for x in v],'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in v]}

def canonical_audit(w,source,snap,C,stats):
    R=source['native_roots'];S=set(w['targets']);U=set(range(N))-S;v,loc=snap[w['carrier_interface_before_operation']]
    insist(len(S)==48 and len(U)==63,'48/63 source split')
    primal=[4,74,78,15,35,13,1,2,0];names=['ZFIRST3','ZFIRST4','ZFIRST5']+[f'CANONICAL9_MODE_{i}'for i in primal[3:]]
    K=[({i}^{j for j in range(N)if sum(a*b for a,b in zip(R[i],R[j]))==0})&U for i in range(N)]
    for p,n in zip(primal,names):
        insist(v[n]==K[p] and C[loc[n]]==C['M1'],('canonical mode at actual common chart',p))
    base=binary_basis(v[n]for n in names)
    insist(len(base)==9 and all(in_span(z,base)for z in K),'complete canonical9 envelope')
    native=[];ground=[]
    for i in U:
        n=f'CANONICAL_NATIVE_RAW_{i}';insist(v[n]=={i} and C[loc[n]]==C[f'L{i}'],('native copy',i));native.append(i)
        insist(v[f'X{i}']=={i} and C[loc[f'X{i}']]==C['Hub'],'unknown original at Hub')
        insist(v[f'Y{i}']=={N+i} and C[loc[f'Y{i}']]==C['zero'],'unknown original Y at ground')
    for i in S:
        n=f'CANONICAL_RESET_RAW_{i}';insist(v[n]=={i} and C[loc[n]]==C['zero'],('known ground raw',i));ground.append(i)
    # Full initial-value dependence graph, without using metadata about access.
    access={i:set()for i in U}
    for n,z in v.items():
        for i in U:
            if subset(C[loc[n]],C[f'F{i}']):access[i]|=set(z)&U
    geometric={i:{j for j in U if sum(a*b for a,b in zip(R[i],R[j]))==0}for i in U}
    insist(access==geometric,'full cut access equals raw native orthogonality')
    J=[5,35,90,93,96,97,109,110]
    insist(set(J)<=U and all(sum(a*b for a,b in zip(R[i],R[j]))!=0 for i in J for j in J),'eight-role identity fitting frame')
    edges={i:[j for j in J if j in access[i]]for i in U-set(J)};edges={i:e for i,e in edges.items()if len(e)==2}
    insist(len(edges)==15,'fifteen retained edge roles')
    incident={j:sorted(i for i,e in edges.items()if j in e)for j in J}
    checks=[]
    for j,roles in incident.items():
        for i in roles:
            for k in roles:
                if i<k:
                    insist(k not in access[i]and i not in access[k],('incident edge noncontact',j,i,k));checks.append([j,i,k])
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    allow=tuple(x/6 for x in moment(gate));q=moment(stats['movement_profile'])
    return {'known_ground_coordinates':sorted(ground),'native_unknown_coordinates':sorted(native),'canonical_rank':9,'initial_access':{i:sorted(a)for i,a in access.items()},'frame':J,'edge_roles':edges,'incident_edge_noncontact_checks':checks,'eight_descent_room':interval_json((allow[0]-q[1]-8,allow[1]-q[0]-8)),'nine_descent_excess':interval_json((q[0]+9-allow[1],q[1]+9-allow[0])),'necessary_allowance':interval_json(allow)}

def parameter_family(w,source,base):
    R=source['native_roots'];S=set(base['targets'])|{61,67};U=set(range(N))-S
    primaries=[4,74,78]
    groups={}
    for i in sorted(U):
        key=tuple(p for p in primaries if sum(a*b for a,b in zip(R[p],R[i]))==0)
        groups.setdefault(key,[]).append(i)
    donors=sorted(i for g,ii in groups.items()if g for i in ii)
    insist(len(donors)==57,'57 independent masks')
    position={i:222+j for j,i in enumerate(donors)}
    values={f'X{i}':frozenset([i])for i in range(N)}
    values.update({f'Y{i}':frozenset([N+i])for i in range(N)})
    events=[];formal_cut=None
    for k,op in enumerate(w['operations']):
        if k==w['carrier_interface_before_operation']:formal_cut=values.copy()
        tag,n,*rest=op
        if tag=='INIT':values[n]=frozenset()
        elif tag=='ADD':
            if n.startswith('X')and n[1:].isdigit()and int(n[1:])in position:
                i=int(n[1:]);insist(values[n]=={i},('parameter read must be immutable raw',k,i))
                values[rest[0]]=values[rest[0]]^{position[i]};events.append([k,i,rest[0]])
            else:values[rest[0]]=values[rest[0]]^values[n]
        elif tag=='CLEAR':del values[n]
    insist(len(events)==227,'227 coupled mask events')
    for i in range(N):
        insist(values[f'X{i}']=={i},('formal original restoration',i))
        insist(values[f'Y{i}']==({N+i,i}if i in w['targets']else{N+i}),('formal arbitrary-Y endpoint',i))
    for group,ii in groups.items():
        if group:
            n='ASC_GROUP_'+'_'.join(map(str,group))
            insist(formal_cut[n]=={position[i]for i in ii},('formal actual group',group))
    insist(not any(op[0]=='ADD'and op[2]in{f'X{i}'for i in donors}for op in w['operations']),'parameter donors immutable')
    return {'independent_parameters':57,'input_columns':279,'coupled_raw_read_events':events,'all_parameter_original_and_receiver_identities':True,'donors':donors}


def controls(w,source):
    result=[]
    for label,event,expected in [
        ('missing native unknown capture',['ADD','X15','CANONICAL_NATIVE_RAW_15'],'source'),
        ('missing local code donor',['ADD','X5','ZFIRST4'],'source'),
        ('missing local donor arrival',['MOVE','X5','F74'],'geometry'),
        ('missing local code descent',['MOVE','ZFIRST4','M1'],'source'),
        ('missing owner retirement',['CLEAR','ZFIRST4'],'lifetime'),
        ('missing known receiver load',['ADD','CANONICAL_RESET_RAW_74','Y74'],'endpoint')]:
        bad=copy.deepcopy(w);ix=bad['operations'].index(event);bad['operations'].pop(ix)
        if ix<bad['carrier_interface_before_operation']:bad['carrier_interface_before_operation']-=1
        try:
            stats,snaps,C,events=replay(bad,source,[bad['carrier_interface_before_operation']])
            canonical_audit(bad,source,snaps,C,stats)
        except (ValueError,KeyError)as exc:result.append({'control':label,'expected_failure_kind':expected,'observed_rejection':str(exc)})
        else:raise ValueError('invalid control passed: '+label)
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    paths=['A/local-canonical9-source/WORD.json','A/canonical9-source/WORD.json','A/mode-preserving48/WORD.json','A/mode-preserving50/WORD.json','A/ascending-canonical3/WORD.json','A/ascending-canonical3-native65/WORD.json','C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json','C/canonical3-reset-source/MATCHED-CUT-WORD.json','C/first-unknown49/WORD.json','C/canonical3-reset-control/RESET-CONTROL-WORD.json']
    report={'status':'PASS_INDEPENDENT_RECOVERED_BIT_REPLAY_AND_CANONICAL_SOURCE_CUT','words':{}}
    for rel in paths:
        path=a.evidence/rel;w=json.loads(path.read_text());source_path=a.repo/w['source_path'];insist(sha(source_path)==w['source_sha256']==SOURCE_SHA,'published native source pin')
        source=json.loads(source_path.read_text());cut=w.get('carrier_interface_before_operation');indices=[]if cut is None else[cut]
        stats,snaps,C,events=replay(w,source,indices)
        item={'sha256':sha(path),'stats':stats,'moment':interval_json(moment(stats['movement_profile']))}
        if rel.startswith('A/local-canonical9-source')or rel.startswith('A/canonical9-source'):
            item['source_cut']=canonical_audit(w,source,snaps,C,stats)
            if rel.startswith('A/local-canonical9-source'):item['negative_controls']=controls(w,source)
        if rel=='A/ascending-canonical3/WORD.json':
            base=json.loads((a.evidence/'A/pruned78/WORD.json').read_text());item['parameter_family']=parameter_family(w,source,base)
        report['words'][rel]=item;print(rel, len(stats['completed_outputs']), stats['counts'],item['moment']['decimal'][0])
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
