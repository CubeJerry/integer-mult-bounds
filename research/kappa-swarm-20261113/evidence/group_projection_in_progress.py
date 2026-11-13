#!/usr/bin/env python3
"""Exact charged-row projection ranks within fixed helper boundary groups.
No arbitrary-subspace theorem follows unless every assigned family passes.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import gzip,hashlib,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('K',ROOT/'worker-b/relocate/kernel_scan.py')
K=importlib.util.module_from_spec(sp);sp.loader.exec_module(K)

def need(ok,label):
    if not ok:raise ValueError(label)

def insert(basis,row,event):
    value,rep=row.copy(),{event:F(1)}
    while value:
        p=max(value)
        if p not in basis:
            q=1/value[p];basis[p]=({i:v*q for i,v in value.items()},
                                  {i:v*q for i,v in rep.items()});return None
        old,mask=basis[p];q=-value[p];K.add(value,old,q);K.add(rep,mask,q)
    return {str(i):str(v) for i,v in rep.items()}

def run():
    started=time.monotonic();deadline=started+60
    raw=(ROOT/'reference/pr7481/WORD.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==K.PIN,'source pin')
    w=json.loads(gzip.decompress(raw));n=w['public']
    assignmentraw=(ROOT/'worker-b/cold-single/ASSIGNMENT.json').read_bytes()
    assignment={r['event']:r for r in json.loads(assignmentraw)}
    need(len(assignment)==468,'full assignment')
    mains=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    members=defaultdict(set)
    for h in set(range(n))-mains:members[w['initial'][h],w['final'][h]].add(h)
    group_of={h:g for g,hs in members.items() for h in hs}
    families={g:dict(basis={},rows=[],dependencies=[]) for g in members}
    rows=[{i:F(1)} if i<n else {} for i in range(n+w['owned_fields'])]
    charts=w['initial']+[None]*w['owned_fields'];last=-1;complete=False
    try:
        for event,e in enumerate(w['program']):
            last=event
            if event%128==0 and time.monotonic()>deadline:raise TimeoutError
            op,a=e[:2]
            if op=='MOVE':
                need(charts[a]==e[2],'MOVE chart')
                if event in assignment:
                    charge=assignment[event];h=charge['assigned_helper'];g=group_of[h]
                    need(not(set(rows[a])&mains) and rows[a].get(h),'literal main-free charged row')
                    r=abs(len(w['frames'][e[3]])-len(w['frames'][e[2]]))
                    R=abs(len(w['frames'][g[1]])-len(w['frames'][g[0]]))
                    need(r==charge['rank'] and R==charge['target_rank'] and r<=R,'exact rank domination')
                    projected={i:v for i,v in rows[a].items() if i in members[g]}
                    dep=insert(families[g]['basis'],projected,event)
                    families[g]['rows'].append(dict(event=event,owner=a,assigned_helper=h,paid_rank=r,
                        projection={str(i):str(v) for i,v in projected.items()}))
                    if dep is not None:families[g]['dependencies'].append(dep)
                charts[a]=e[3]
            elif op=='INIT':need(charts[a] is None,'fresh INIT');charts[a]=e[2];rows[a]={}
            elif op=='CLEAR':need(charts[a]==e[2],'CLEAR chart');charts[a]=None;rows[a]={}
            elif op=='SCALE':
                need(charts[a]==e[-1],'SCALE chart');q=K.rational(e[2]);rows[a]={i:q*v for i,v in rows[a].items() if q*v}
            elif op in ('ADD','COPY'):
                need(charts[a]==charts[e[2]]==e[-1],'scalar cochart')
                if op=='COPY':need(not rows[a],'COPY zero');rows[a]={}
                K.add(rows[a],rows[e[2]],K.rational(e[3]))
            else:raise ValueError(op)
        complete=True;need(charts==w['final']+[None]*w['owned_fields'],'all endpoints')
    except TimeoutError:pass
    records=[]
    for g,hs in sorted(members.items()):
        family=families[g];rank=len(family['basis']);count=len(family['rows'])
        # Recheck every dependence against the stored original projected rows.
        lookup={r['event']:{int(i):F(v) for i,v in r['projection'].items()} for r in family['rows']}
        for dependency in family['dependencies']:
            zero={}
            for event,q in dependency.items():K.add(zero,lookup[int(event)],F(q))
            need(not zero,'exact projected-family dependence witness')
        records.append(dict(entrance_frame=g[0],exit_frame=g[1],members=sorted(hs),member_count=len(hs),
            target_rank=abs(len(w['frames'][g[1]])-len(w['frames'][g[0]])),assigned_rows=count,
            projected_rank=rank,independent=rank==count,rows=family['rows'],dependencies=family['dependencies']))
    bad=[r for r in records if not r['independent']]
    result=dict(status='COMPLETE_EXACT_GROUP_PROJECTION_RANKS' if complete else 'TIME_LIMIT_PARTIAL_GROUP_RANKS',
        source_sha256=K.PIN,assignment_sha256=hashlib.sha256(assignmentraw).hexdigest(),last_event=last,
        boundary_groups=len(records),charged_groups=sum(bool(r['assigned_rows']) for r in records),
        charged_rows=sum(r['assigned_rows'] for r in records),all_move_ranks_dominated=True,
        all_assigned_families_independent=not bad,dependent_groups=len(bad),records=records,
        seconds=time.monotonic()-started,scope='Literal identical entrance AND exit frame IDs; no mixing boundary groups. Necessary sufficient-independence test only. No arbitrary-killed-subspace theorem is inferred when a family is dependent.')
    (HERE/'RANKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    print('dependent',[(r['entrance_frame'],r['exit_frame'],r['member_count'],r['assigned_rows'],r['projected_rank']) for r in bad])

if __name__=='__main__':run()
