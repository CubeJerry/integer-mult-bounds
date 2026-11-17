#!/usr/bin/env python3
"""Construct a single six-receiver source and check every physical record."""
import argparse
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

NATIVE = 'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
PIN = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
SIX = (1, 3, 73, 76, 77, 80)
CANON = (0, 1, 2, 4, 8, 9, 14, 30, 59)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def canonical(roots):
    rows = [sum(1 << j for j, r in enumerate(roots) if i == j or dot(r, roots[i]) == 0)
            for i in range(len(roots))]
    coding = {0: ()}
    for i in CANON:
        new = {x ^ rows[i]: w+(i,) for x, w in coding.items()}
        require(not set(coding) & set(new), 'canonical independence')
        coding.update(new)
    require(all(x in coding for x in rows), 'all canonical rows')
    return rows, [coding[x] for x in rows]


def assignment(mixed, targets):
    # One rank-six anchoring visit per receiver. Preserve one private destination
    # per nonempty group, since its unmasked original carries the sum there.
    def assign(index, choices):
        if index == len(targets):
            return choices.copy()
        i = targets[index]
        for group in mixed:
            if i not in group or list(choices.values()).count(group) >= len(group) - 1:
                continue
            choices[i] = group
            result = assign(index+1, choices)
            if result is not None:
                return result
            del choices[i]
        return None
    out = assign(0, {})
    require(out is not None, 'rank-six anchor assignment')
    return out


def build(R):
    groups = defaultdict(list)
    for j, r in enumerate(R):
        groups[tuple(i for i in SIX if dot(r, R[i]) == 0)].append(j)
    mixed = sorted(u for u in groups if 1 < len(u) < len(SIX))
    anchors = assignment(mixed, SIX)
    chart_specs = {'zero': {'kind':'zero'}, 'Hub': {'kind':'ambient'}}
    for j in range(len(R)):
        chart_specs[f'L{j}'] = {'kind':'line', 'role': j}
        chart_specs[f'F{j}'] = {'kind':'kernel', 'normals': [j]}
    def meet(u):
        if len(u) == 1:
            return f'F{u[0]}'
        name = 'C_' + '_'.join(map(str,u))
        chart_specs[name] = {'kind':'kernel', 'normals':list(u)}
        return name
    ops, tags, owners, sites = [], [], [], []
    outstanding = defaultdict(list)
    raw_held = {}
    def op(tag, *args):
        ops.append(list(args)); tags.append(tag)
    def snapshot(tag, name, site, sources):
        op(tag+'_birth','INIT',name,site); owners.append(name)
        for src in sources:
            op(tag+'_capture','ADD',src,name)
    inverse = []
    for u, donors in sorted(groups.items()):
        if not u:
            for j in donors: op('unneeded_X_endpoint','MOVE',f'X{j}','Hub')
            continue
        c = meet(u)
        if u == SIX or len(u)==1:
            for j in donors: op('common_or_private_source_arrival','MOVE',f'X{j}',c)
            name = 'SUM_'+c
            snapshot('stationary_group',name,c,[f'X{j}' for j in donors])
            for i in u: outstanding[i].append((c,name))
            for j in donors: op('common_or_private_source_restore','MOVE',f'X{j}','Hub')
            sites.append({'signature':u,'donors':donors,'common_site':c,'anchored':u, 'stationary_owner':name})
            continue
        anchored = [i for i in u if anchors[i] == u]
        private = [i for i in u if i not in anchored]
        require(1<=len(private)<=len(donors),'available distinct original carriers')
        pivot = donors[0]
        backups = list(zip(private[1:],donors[1:len(private)]))
        for i,q in backups:
            require(q not in SIX and q not in raw_held, 'additional point diagonal')
            raw_held[q] = (i, f'RAW_{q}')
            snapshot('point_backup',f'RAW_{q}',f'L{q}',[f'X{q}'])
            op('point_backup_descent','MOVE',f'RAW_{q}','zero')
        for j in donors: op('signature_source_gather','MOVE',f'X{j}',c)
        intra = [(j,pivot) for j in donors[1:]] + [(pivot,q) for i,q in backups]
        for src,dst in intra:
            op('source_recode','ADD',f'X{src}',f'X{dst}')
        inverse.extend(intra[::-1])
        if anchored:
            name = 'ANCHOR_'+c
            snapshot('anchor',name,c,[f'X{pivot}'])
            for i in anchored: outstanding[i].append((c,name))
        selected = dict(zip(donors[:len(private)],private))
        for j in donors:
            if j in selected:
                i=selected[j]; site=f'F{i}'
                op('terminal_visit','MOVE',f'X{j}',site)
                name = f'TERMINAL_{j}_{i}'
                snapshot('terminal',name,site,[f'X{j}']); outstanding[i].append((site,name))
            op('signature_X_endpoint','MOVE',f'X{j}','Hub')
        sites.append({'signature':u,'donors':donors,'common_site':c,'anchored':anchored,
                      'pure_pivot':[pivot,private[0]],'masked_carriers':[[q,i] for i,q in backups]})
    for a,b in inverse: op('inverse_source_recode','ADD',f'X{a}',f'X{b}')
    cuts={'source_restored':len(ops)}
    K, decomp = canonical(R)
    for j in CANON:
        name=f'K{j}';snapshot('canonical',name,'Hub',[f'X{k}' for k in range(len(R)) if (K[j]>>k)&1]);op('canonical_descent','MOVE',name,'zero')
    cuts['canonical_at_ground']=len(ops)
    for i in SIX:
        for j in decomp[i]:op('canonical_preload','ADD',f'K{j}',f'Y{i}')
    for q,(i,raw) in raw_held.items():
        op('mask_precompensation','ADD',raw,f'Y{i}')
        op('point_diagonal','ADD',raw,f'Y{q}')
    for i in range(len(R)):
        if i not in SIX:
            op('other_Y_endpoint','MOVE',f'Y{i}',f'F{i}'); continue
        ysites=[meet(SIX),meet(anchors[i]),f'F{i}']
        for c in ysites:
            op('target_Y_route','MOVE',f'Y{i}',c)
            for s,cache in outstanding[i]:
                if s==c: op('deferred_read','ADD',cache,f'Y{i}')
        require({s for s,cache in outstanding[i]}==set(ysites),'all scheduled source reads')
    cuts['before_retirement']=len(ops)
    for n in owners:op('retire','CLEAR',n)
    return {'schema':'x-only-signature-cache-six-v1', 'native_path':NATIVE,'native_sha256':PIN,
            'network_receiver_roles':list(SIX),'additional_paid_point_diagonals':sorted(raw_held),
            'all_completed_roles':sorted(set(SIX)|set(raw_held)),'canonical_basis':list(CANON),
            'canonical_preloads':{i:decomp[i] for i in SIX},'source_cohorts':sites,'charts':chart_specs,
            'milestones':cuts,'operations':ops,'operation_tags':tags}


def rref(rows):
    a=[list(map(Fraction,r)) for r in rows]; p=0; piv=[]
    for c in range(8):
        k=next((j for j in range(p,len(a)) if a[j][c]),None)
        if k is None: continue
        a[p],a[k]=a[k],a[p]; d=a[p][c]; a[p]=[v/d for v in a[p]]
        for j in range(len(a)):
            if j!=p and a[j][c]:
                s=a[j][c]; a[j]=[x-s*y for x,y in zip(a[j],a[p])]
        piv.append(c); p+=1
    return tuple(map(tuple,a[:p])),piv


def nullspace(rows):
    a,piv=rref(rows); out=[]
    for c in range(8):
        if c in piv: continue
        x=[0]*8;x[c]=1
        for j,p in enumerate(piv):x[p]=-a[j][c]
        out.append(tuple(x))
    return tuple(out)


def replay(w,R,geometry=None,omit=None):
    if geometry is None: geometry=geometry_map(w,R)
    sites,subset=geometry
    K,_=canonical(R); n=len(R); names=[f'X{j}' for j in range(n)]+[f'Y{j}' for j in range(n)]
    vals={name:1<<i for i,name in enumerate(names)}; init=vals.copy()
    loc={f'X{j}':f'L{j}' for j in range(n)}|{f'Y{j}':'zero' for j in range(n)}
    own=set(); used=set();counts=Counter();mov=Counter();bytype=Counter();peak=dirty=0;cuts={}
    for index,((op,a,*arg),tag) in enumerate(zip(w['operations'],w['operation_tags'])):
        if index==omit: continue
        counts[op]+=1;bytype[tag]+=1
        if op=='INIT':
            require(a not in used and a not in vals,'fresh birth'); used.add(a);own.add(a);loc[a]=arg[0];vals[a]=0
        elif op=='MOVE':
            x,y=loc[a],arg[0];d=len(sites[y])-len(sites[x]);require(d<0 and subset(y,x) if a in own else d>0 and subset(x,y),'proper physical route '+str((index,a,x,y)))
            if a in own: require(tag in ('point_backup_descent','canonical_descent'),'stationary cache motion')
            mov[abs(d)]+=1;loc[a]=y
        elif op=='ADD':
            b=arg[0];require(a!=b and loc[a]==loc[b],'ADD at actual common chart');vals[b]^=vals[a]
        elif op=='CLEAR':
            require(a in own,'retained clear');dirty+=bool(vals[a]);own.remove(a);del vals[a],loc[a]
        else:raise ValueError(op)
        peak=max(peak,len(own))
        for name,step in w['milestones'].items():
            if index+1!=step:continue
            if name in ('source_restored','canonical_at_ground'):
                require(all(loc[f'X{j}']=='Hub' and vals[f'X{j}']==1<<j and loc[f'Y{j}']=='zero' and vals[f'Y{j}']==1<<(n+j) for j in range(n)),'all raw X and untouched Y before preload')
            if name=='canonical_at_ground':require(all(loc[f'K{j}']=='zero' and vals[f'K{j}']==K[j] for j in CANON),'literal canonical rows')
            cuts[name]={'step':step,'live_fields':len(vals),'owners':len(own)}
    require(not own and set(vals)==set(init),'all owners retired')
    for j in range(n):
        x,y=f'X{j}',f'Y{j}'; delta=(1<<j) if j in w['all_completed_roles'] else 0
        require(loc[x]=='Hub' and vals[x]==init[x] and loc[y]==f'F{j}' and vals[y]==(init[y]^delta),'public endpoint '+str(j))
    return {'counts':dict(counts),'movement_profile':dict(sorted(mov.items())),'peak_owned':peak,
            'dirty_CLEAR':dirty,'milestones':cuts,'tagged_counts':dict(bytype),'all_original_columns':2*n}


def geometry_map(w,R):
    native={}
    for n,c in w['charts'].items():
        if c['kind']=='line': q=[R[c['role']]]
        elif c['kind']=='kernel': q=nullspace([R[j] for j in c['normals']])
        elif c['kind']=='ambient': q=nullspace([])
        else:require(c['kind']=='zero','known chart');q=[]
        native[n]=tuple(map(tuple,q))
    @lru_cache(None)
    def subset(a,b):return len(rref(native[b]+native[a])[0])==len(native[b])
    return native,subset


@lru_cache(None)
def integer_price(g):
    scale=10**30; target=g**199*scale**200;low=0;high=g*scale+1
    while high-low>1:
        mid=(low+high)//2
        if mid**200<=target:low=mid
        else:high=mid
    return Fraction(low,scale),Fraction(low if low**200==target else low+1,scale)


def price(profile):
    lo=hi=Fraction(0)
    for d,n in profile.items():
        a,b=integer_price(d);lo+=n*(a if n>=0 else b);hi+=n*(b if n>=0 else a)
    return lo,hi


def iv(t):
    with localcontext() as ctx:
        ctx.prec=55
        return {'rational':list(map(str,t)),'decimal':[str(Decimal(z.numerator)/Decimal(z.denominator)) for z in t]}


def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=a.native.read_bytes();require(sha256(raw).hexdigest()==PIN,'native source pin');R=json.loads(raw)['native_roots']
    w=build(R);write(a.out/'WORD.json',w);geom=geometry_map(w,R);res=replay(w,R,geom)
    controls=[]
    for tag in ['point_backup_capture','point_backup_descent','source_recode','terminal_visit','terminal_capture','anchor_capture','inverse_source_recode','canonical_capture','canonical_descent','canonical_preload','mask_precompensation','point_diagonal','target_Y_route','deferred_read','retire']:
        i=w['operation_tags'].index(tag)
        try:replay(w,R,geom,omit=i)
        except (ValueError,KeyError) as exc:controls.append({'tag':tag,'omitted':i,'rejected':True,'reason':str(exc)})
        else:raise AssertionError('omission accepted: '+tag)
    q=price(res['movement_profile']);cap={127:37,64:74,1:-74}
    for j in range(1,9): cap[1+7*j]=cap.get(1+7*j,0)+74;cap[7*j]=cap.get(7*j,0)-74
    cap=tuple(x/6 for x in price(cap));room=(cap[0]-q[1],cap[1]-q[0]);require(room[0]>0,'limiting movement gate')
    result={'status':'PASS_X_ONLY_SIGNATURE_CACHE_SIX','word_sha256':sha256((a.out/'WORD.json').read_bytes()).hexdigest(),'native_sha256':PIN,
            'receiver_roles':w['network_receiver_roles'],'additional_paid_point_diagonals':w['additional_paid_point_diagonals'],
            'mixed_signature_charts':7,'rank_six_anchor_visits':6,'supplementary_raw_point_descents':5,
            **res,'moment_at_199_over_200':iv(q),'necessary_limiting_room':iv(room),'controls':controls,
            'complete_supplier':False,'new_complete_kappa':False}
    write(a.out/'RESULT.json',result);print(result['status'],result['word_sha256'],res['counts'],res['movement_profile'],iv(q)['decimal'],iv(room)['decimal'])

if __name__=='__main__':main()
