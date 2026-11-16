#!/usr/bin/env python3
"""Independent rational-chart replay and actual-history visibility auditor."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction
from pathlib import Path

def rref(rows):
    a=[list(map(Fraction,r))for r in rows];k=0
    for j in range(8):
        p=next((q for q in range(k,len(a))if a[q][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
        for q in range(len(a)):
            if q!=k and a[q][j]:v=a[q][j];a[q]=[x-v*y for x,y in zip(a[q],a[k])]
        k+=1
    return tuple(tuple(v)for v in a[:k])
def null(rows):
    rr=rref(rows);ps=[next(j for j,v in enumerate(row)if v)for row in rr];out=[]
    for j in range(8):
        if j in ps:continue
        v=[Fraction(0)]*8;v[j]=1
        for p,row in zip(ps,rr):v[p]=-row[j]
        out.append(v)
    return rref(out)
def contained(a,b):return len(rref(a+b))==len(b)
def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b
def solve(rows,v):
    b={}
    for j,x in enumerate(rows):
        c=1<<j
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p][0];c^=b[p][1]
            else:b[p]=(x,c);break
    c=0
    while v:
        p=v.bit_length()-1
        if p not in b:return None
        x,m=b[p];v^=x;c^=m
    return c

def replay(w,roots,seed,mode,invoice=True):
    C={k:(rref(v['rows'])if v['kind']=='span'else null(v['rows']))for k,v in w['charts'].items()}
    for j in range(111):assert C[f'L{j}']==rref([roots[j]])and C[f'F{j}']==null([roots[j]])
    assert len(C['Hub'])==8 and not C['zero']
    val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)}
    at={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)}
    owners=set();born=set();count=Counter();hist=Counter();dirty=0;snaps=[];cuts={};moveok={}
    def snap(n,step,phase):
        snaps.append({'index':len(snaps),'step':step,'phase':phase,'packet':n,'chart':at[n],'row_hex':hex(val[n])})
    for step,o in enumerate(w['operations'],1):
        op=o[0];count[op]+=1
        if op=='ADD'and o[2].startswith('P')and at.get(o[2])not in [None,'Hub']:snap(o[2],step,'before')
        if op=='INIT':
            _,n,c=o;assert n not in val and n not in born and c in C;val[n]=0;at[n]=c;owners.add(n);born.add(n)
        elif op=='ADD':
            _,s,t=o;assert s in val and t in val and C[at[s]]==C[at[t]],(step,o);val[t]^=val[s]
        elif op=='MOVE':
            _,n,c=o;assert n in val and c in C;old=at[n]
            key=(old,c,n in owners)
            if key not in moveok:moveok[key]=contained(C[c],C[old])if n in owners else contained(C[old],C[c])
            assert moveok[key],(step,o,'direction');dist=abs(len(C[c])-len(C[old]));assert dist>0
            at[n]=c;hist[dist]+=1
        elif op=='CLEAR':
            _,n=o;assert n in owners;dirty+=bool(val[n]);owners.remove(n);del val[n];del at[n]
        else:raise AssertionError(op)
        if op=='ADD'and o[2].startswith('P')and at[o[2]]!='Hub':snap(o[2],step,'after')
        if op=='MOVE'and o[1].startswith('P')and at[o[1]]!='Hub':snap(o[1],step,'arrival')
        if step==w['milestones']['source_cut']:
            assert len(basis(val[f'X{j}']for j in range(111)))==111
            if 'source_cut'in w:
                for n,rec in w['source_cut'].items():assert val[n]==int(rec['row_hex'],16)and at[n]==rec['chart']
            cuts['source']={'values':val.copy(),'charts':at.copy()}
        if step==w['milestones']['seed8_before_Y']:
            assert all(val[f'Y{j}']==1<<(111+j)and at[f'Y{j}']=='zero'for j in range(111))
            S=[val[f'P{j}']for j in range(8)];assert S==[int(v,16)for v in w['seed_rows_hex']]
            assert all(at[f'P{j}']=='zero'for j in range(8))and len(basis(S+seed))==8
            for j in w['point_targets']:assert val[f'E{j}']==1<<j and at[f'E{j}']=='zero'
            cuts['seed']={'values':val.copy(),'charts':at.copy()}
        if step==w['milestones']['all_X_restored']:assert all(val[f'X{j}']==1<<j and at[f'X{j}']=='Hub'for j in range(111))
    for j in range(111):
        assert val[f'X{j}']==1<<j and at[f'X{j}']=='Hub'
        assert val[f'Y{j}']==((1<<(111+j))^((1<<j)if j in w['targets']else 0))and at[f'Y{j}']==f'F{j}'
    assert not owners and len(val)==222
    if invoice:
        expected={15:({1:43,2:56,3:30,4:30,5:62,6:19,7:114,8:5},[19,426,359,19]),12:({1:69,2:50,3:16,4:15,5:54,6:48,7:112,8:1},[63,671,365,63])}
        hh,cc=expected[mode]
        if mode==15 and 'history_cache_metadata'in w:hh,cc={1:58,2:56,3:36,4:35,5:69,6:19,7:106,8:1},[63,673,380,63]
        assert dict(hist)==hh and [count[k]for k in ['INIT','ADD','MOVE','CLEAR']]==cc
    return {'C':C,'cuts':cuts,'snapshots':snaps,'count':dict(count),'profile':dict(sorted(hist.items())),'dirty_CLEAR':dirty}

def delete(w,i):
    z=copy.deepcopy(w);z['operations'].pop(i);z['milestones']={k:v-(v>i)for k,v in z['milestones'].items()};z.pop('source_cut',None);return z

def history_audit(w,run,roots,reported):
    assert run['snapshots']==reported
    rows=[int(s['row_hex'],16)for s in reported];h=w['singular_h'];dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    W=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or not dot(roots[i],roots[j])))for i in range(111)]
    hr=56 if len(w['targets'])==12 else 58
    assert len(basis(W))==15 and len(basis(rows))==hr and len(basis(rows+W))==hr
    seedcut=run['cuts']['seed'];val=seedcut['values'];at=seedcut['charts'];C=run['C']
    live=[val[n]for n in val if at[n]!='Hub'and not n.startswith('Y')]
    dim=len(basis(live));inter=dim+15-len(basis(live+W));assert inter==15
    if len(w['targets'])==12:assert dim==64
    allrows=live+[val[f'Y{j}']for j in range(111)]
    assert len(basis(allrows))+15-len(basis(allrows+W))==15
    D=[int(m['row_hex'],16)for m in w['history_cache_metadata']]
    S=[int(v,16)for v in w['seed_rows_hex']]
    assert len(basis(D))==44 and len(basis(S+D))==52 and len(basis(D))+15-len(basis(D+W))==7
    witness=[]
    for m in w['history_cache_metadata']:
        assert val[m['name']]==int(m['row_hex'],16)and at[m['name']]==m['chart']
        found=[]
        for k,s in enumerate(reported[:-1]):
            t=reported[k+1]
            if s['phase']=='before'and t['phase']=='after'and s['step']==t['step']:
                o=w['operations'][s['step']-1]
                if o[0]=='ADD'and o[1]==m['name']:
                    assert int(s['row_hex'],16)^int(t['row_hex'],16)==int(m['row_hex'],16);found.append([k,k+1])
        assert len(found)==1;witness.append({'cache':m['name'],'snapshot_indices':found[0]})
    access=[];completion=[];fitting=[]
    ground=[val[n]for n in val if at[n]=='zero'and not n.startswith('Y')]
    for i in range(111):
        F=C[f'F{i}'];vis=[val[n]for n in val if not n.startswith('Y')and contained(C[at[n]],F)]
        vis +=[row for row,s in zip(rows,reported)if contained(C[s['chart']],F)]
        hit=solve(vis,1<<i)is not None
        if hit:completion.append(i)
        foreign=[1<<j for j in range(111)if not dot(roots[i],roots[j])]
        fit=solve(ground+foreign,1<<i)is not None
        if fit:fitting.append(i)
        access.append({'receiver':i,'optimistic_rank':len(basis(vis)),'target_available':hit,'ground_fitting':fit})
    assert completion==sorted(w['targets'])and fitting==[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80]
    positive_visible=sorted({i for i in range(111)for s in reported if C[s['chart']]and contained(C[s['chart']],C[f'F{i}'])})
    assert positive_visible==([3,4,74,76,78,80]if len(w['targets'])==12 else[3,4,21,64,65,74,76,78,80])
    return {'snapshot_count':len(rows),'history_rank':hr,'W_rank':15,'all111_fitting_witnesses':[hex(solve(rows,v))for v in W],
            'cache_difference_witnesses':witness,'live_inventory_rank':dim,'live_inventory_W_intersection':inter,
            'W_intersection_with_all_Y_nuisance_columns':15,'filtered_cache_rank':44,'S_plus_D_rank':52,'D_intersect_W_rank':7,
            'optimistically_completable_receivers':completion,'ground_fitting_receivers':fitting,'access':access,
            'positive_snapshot_visible_facets':positive_visible,
            'scope':'Only snapshots of actual principal packets at their actual charts plus actual live fields; no new original-source captures, movement, relocalization or changed source schedule; arbitrary incompatible receiver ordering is generously ignored.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--seed',type=Path,required=True);p.add_argument('--mode',type=int,choices=[12,15],required=True);p.add_argument('--snapshots',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.word.read_bytes();w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots'];S=[int(v,16)for v in json.loads(a.seed.read_text())['seed_rows']]
    run=replay(w,roots,S,a.mode);tests=[]
    if a.mode==15:
        pred=[('donor_mask',lambda o:o==['ADD','E1','Y21']),('fork',lambda o:o==['ADD','X10','X1']),('old_facet_aggregate',lambda o:o==['ADD','X10','X21']),('held_seed_query',lambda o:o[0]=='ADD'and o[1]=='X21'and o[2].startswith('P')),('donor_restore',lambda o:o==['ADD','X3','X1']),('retirement',lambda o:o==['CLEAR','Q0'])]
        if 'history_cache_metadata'in w:pred +=[('filtered_capture',lambda o:o[0]=='ADD'and o[2]=='H0_0'),('filtered_query',lambda o:o[0]=='ADD'and o[1]=='H0_0'),('filtered_retirement',lambda o:o==['CLEAR','H0_0'])]
    else:
        pred=[('filtered_capture',lambda o:o[0]=='ADD'and o[2]=='H0_0'),('filtered_query',lambda o:o[0]=='ADD'and o[1]=='H0_0'),('filtered_retirement',lambda o:o==['CLEAR','H0_0']),('early_capture',lambda o:o==['ADD','X1','E1']),('cache_delivery',lambda o:o[0]=='ADD'and o[1]=='Q0'and o[2]=='Y3')]
    for name,pred in pred:
        ix=[j for j,o in enumerate(w['operations'])if pred(o)];assert ix,name;i=ix[-1]if name=='donor_restore'else ix[0];mut=delete(w,i)
        try:replay(mut,roots,S,a.mode,False)
        except AssertionError:tests.append(name)
        else:raise AssertionError(('accepted mutation',name))
    out={'status':'PASS_INDEPENDENT_SOURCE_AND_HISTORY_REVIEW','word_sha256':hashlib.sha256(raw).hexdigest(),'native_source_sha256':hashlib.sha256(src).hexdigest(),'all_columns':222,'completed_targets':sorted(w['targets']),'count':run['count'],'profile':run['profile'],'dirty_CLEAR':run['dirty_CLEAR'],'semantic_negative_controls':tests,'negative_controls_disable_invoice_and_source_cut_metadata':True}
    if 'history_cache_metadata'in w:
        assert a.snapshots;out['history']=history_audit(w,run,roots,json.loads(a.snapshots.read_text()))
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='history'}))

if __name__=='__main__':main()
