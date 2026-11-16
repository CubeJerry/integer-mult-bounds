#!/usr/bin/env python3
"""Literal paid raw-return comparator on root's protected41 source."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load
BASE='9053904c95084269c8d2df3f883a8c32dfadff763a2c0338a5ebf7c45d4d6267'
POINTS=[8,9,36,37,50]

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw)
    src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots']
    e=load(a.engine,'raw46_geometry');price=load(a.price_engine,'raw46_price');C,H,before=e.replay(old,R)
    assert set(POINTS).isdisjoint(old['targets'])
    names={f'Y{i}':i for i in POINTS}
    assert not any(o[0]=='ADD'and(o[1]in names or o[2]in names)for o in old['operations'])
    w=copy.deepcopy(old);ops=[]
    for i in POINTS:ops += [['INIT',f'ADDED_RAW{i}',f'L{i}'],['ADD',f'X{i}',f'ADDED_RAW{i}'],['MOVE',f'ADDED_RAW{i}','zero']]
    for o in old['operations']:
        if o[0]=='MOVE'and o[1]in names:
            i=names[o[1]];assert o[2]==f'F{i}';ops.append(['ADD',f'ADDED_RAW{i}',o[1]])
        ops.append(o)
    ops += [['CLEAR',f'ADDED_RAW{i}']for i in POINTS]
    w.update(operations=ops,targets=sorted(old['targets']+POINTS),schema='five-paid-native-returns-protected46-comparator-v1',base_word_sha256=BASE,added_native_returns=POINTS,scope='Actual46 endpoint comparator with five paid native raw returns, retaining root protected41 source contracts. No new all111 supplier or kappa.')
    C,H,after=e.replay(w,R);profile=before['movement_profile'].copy();profile[1]+=5;assert after['movement_profile']==profile
    for k,n in [('INIT',5),('ADD',10),('MOVE',5),('CLEAR',5)]:assert after['counts'][k]==before['counts'][k]+n
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};protected={}
    for op,n,*q in w['operations']:
        if op=='INIT':values[n]=0;at[n]=q[0]
        elif op=='ADD':values[q[0]]^=values[n]
        elif op=='MOVE':at[n]=q[0]
        elif op=='CLEAR':
            if n in old['protected_source_contracts']:protected[n]={'value_hex':hex(values[n]),'chart':at[n]}
            del values[n],at[n]
    assert protected==old['protected_source_contracts']
    controls=[]
    for i in POINTS:
        for op in [['ADD',f'X{i}',f'ADDED_RAW{i}'],['MOVE',f'ADDED_RAW{i}','zero'],['ADD',f'ADDED_RAW{i}',f'Y{i}']]:
            bad=copy.deepcopy(w);bad['operations'].remove(op)
            try:e.replay(bad,R)
            except (AssertionError,KeyError)as ex:controls.append({'removed':op,'failure':str(ex)})
            else:raise AssertionError(('accepted omission',op))
    Q=price.moment(profile);B={127:37,64:74,1:-74}
    for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
    limit=tuple(x/6 for x in price.moment(B));room=limit[0]-Q[1],limit[1]-Q[0]
    a.out.mkdir(parents=True,exist_ok=True);encoded=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(encoded)
    out={'status':'PASS_ACTUAL_FIVE_PAID_RETURNS_PROTECTED46','word_sha256':hashlib.sha256(encoded).hexdigest(),'base_word_sha256':BASE,'before':before,'after':after,'added_outputs':POINTS,'protected_source_contracts':protected,'signed_movement_increment':{'1':5},'price':{'moment':price.display(Q),'limiting_room':price.display(room)},'negative_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in['status','word_sha256','after','price']}))

if __name__=='__main__':main()
