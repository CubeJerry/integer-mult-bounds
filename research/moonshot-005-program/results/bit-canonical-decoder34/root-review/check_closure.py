#!/usr/bin/env python3
"""Independent fresh information-envelope audit of the changed actual47 word."""
from pathlib import Path
import argparse,hashlib,json
from optimize_word import independent_replay
from review_leaf_capacity import chart_basis,binary_basis

WORD='a910bb4504cf2a96303e8d560f076463268c4cb3ad4e6631d5f598c895db0567'
def fits(rows,target):
    basis={r.bit_length()-1:r for r in binary_basis(rows)}
    while target:
        j=target.bit_length()-1
        if j not in basis:return False
        target^=basis[j]
    return True
def main():
    p=argparse.ArgumentParser()
    for n in ['repo','word','author-result','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw)
    src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots'];replay=independent_replay(w)
    charts={n:chart_basis(rec)for n,rec in w['charts'].items()};visible={(i,c):all(sum(x*y for x,y in zip(row,roots[i]))==0 for row in C)for i in range(111)for c,C in charts.items()}
    val={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    history=[(loc[n],z)for n,z in val.items()];stock=None
    for step,(op,n,*q)in enumerate(w['operations']):
        if op=='CLEAR':
            if stock is None:stock=(step,val.copy(),loc.copy())
            del val[n],loc[n];continue
        if op=='INIT':val[n],loc[n]=0,q[0]
        elif op=='ADD':val[q[0]]^=val[n];n=q[0]
        elif op=='MOVE':loc[n]=q[0]
        history.append((loc[n],val[n]))
    mask=(1<<111)-1;targets=set(w['targets']);grant=[1<<i for i in targets];step,sv,sl=stock
    current={i:[z for n,z in sv.items()if z>>111==0 and visible[i,sl[n]]]for i in range(111)}
    locals={i:[1<<j for j in range(111)if sum(x*y for x,y in zip(roots[i],roots[j]))==0]for i in range(111)}
    past={i:[z&mask for c,z in history if visible[i,c]]for i in range(111)}
    models={'current_stock_and_completed_point_grants':current,'current_stock_native_locals_completed_point_grants':{i:current[i]+locals[i]for i in range(111)},'all_actual_history_X_parts_and_raw_point_feedback':past}
    author=json.loads(a.author_result.read_text());assert author['word_sha256']==WORD and author['stock_cut_before_operation_index']==step
    reports={}
    for name,rows in models.items():
        known=targets.copy();waves=[]
        while True:
            found={i for i in range(111)if fits(rows[i]+[1<<j for j in known],1<<i)};assert known<=found
            if found==known:break
            waves.append(sorted(found-known));known=found
        expected=author['models'][name];assert sorted(known)==expected['closure']==sorted(targets)and waves==expected['waves']==[]
        duals={z['receiver']:int(z['dual_hex'],16)for z in expected['remaining_duals']};assert set(duals)==set(range(111))-targets
        for i,d in duals.items():assert d>>i&1 and all((d&r).bit_count()%2==0 for r in rows[i]+grant)
        reports[name]={'closure':sorted(known),'waves':waves,'independently_verified_dual_count':len(duals),'all_stored_duals_annihilate_exact_visible_rows_and_completed_grants':True}
    own=[i for i in range(111)if i not in targets and any(z>>i&1 for z in past[i])];quotient=[]
    for i in sorted(set(range(111))-targets):
        keep=mask^(sum(locals[i])|sum(grant));rank=len(binary_basis(z&keep for z in past[i]))
        if rank:quotient.append({'receiver':i,'rank':rank})
    assert own==[z['receiver']for z in author['unfinished_receivers_with_visible_own_coordinate']]
    assert quotient==author['unfinished_receivers_with_nonzero_history_quotient_mod_locals_and47']
    assert len(own)==36 and len(quotient)==64
    result={'status':'PASS_ROOT_INDEPENDENT_FRESH_ACTUAL47_CLOSURES','word_sha256':WORD,'author_result_sha256':hashlib.sha256(a.author_result.read_bytes()).hexdigest(),'native_source_sha256':w['source_sha256'],'method':'Separate Fraction-chart/native-orthogonality visibility, all222-column replay and binary elimination; author closure code not imported. Every one of192 stored duals is checked against independently reconstructed observations.','replay':replay,'models':reports,'unfinished_receivers_with_visible_own_coordinate':own,'unfinished_nonzero_quotient_ranks':quotient,'old_own_zero_obstruction_cannot_be_inherited':True,'scope':'Three source-specific optimistic information closures stop at47; all64 unfinished receivers have nonzero quotient observations and36 have their own coordinate present. None is thereby decoded. Historical and completed-point grants are not physical routes. No general coding impossibility or complete supplier.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
