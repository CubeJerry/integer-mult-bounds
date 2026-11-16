#!/usr/bin/env python3
"""Compose root's exact early source release with the five paid native returns."""
from pathlib import Path
import argparse,copy,hashlib,json
from source_loader import load
BASE='509fe171db1fb0f82d9452c52e53166cae41da6f0c1700b10d8ef5db00ad28f2'
POINTS=[8,9,36,37,50]

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);src=(a.repo/old['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==old['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'early46_engine');price=load(a.price_engine,'early46_price');_,_,before=e.replay(old,R)
    w=copy.deepcopy(old);ops=[]
    for i in POINTS:ops += [['INIT',f'ADDED_RAW{i}',f'L{i}'],['ADD',f'X{i}',f'ADDED_RAW{i}'],['MOVE',f'ADDED_RAW{i}','zero']]
    for o in old['operations']:
        if o[0]=='MOVE'and o[1]in[f'Y{i}'for i in POINTS]:
            i=int(o[1][1:]);assert o[2]==f'F{i}';ops.append(['ADD',f'ADDED_RAW{i}',o[1]])
        ops.append(o)
    ops += [['CLEAR',f'ADDED_RAW{i}']for i in POINTS]
    w.update(operations=ops,targets=sorted(old['targets']+POINTS),schema='early-source-release-with-five-paid-returns46-v1',base_word_sha256=BASE,added_native_returns=POINTS,scope='Actual46 endpoints, early restored Hub source chronology, three protected M1 imports; all ordinary returns paid. No new full supplier or kappa.')
    C,H,after=e.replay(w,R);profile=before['movement_profile'].copy();profile[1]+=5;assert after['movement_profile']==profile
    a.out.mkdir(parents=True,exist_ok=True);blob=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(blob);out={'status':'PASS_EARLY_RELEASE_PLUS_PAID46','word_sha256':hashlib.sha256(blob).hexdigest(),'base_word_sha256':BASE,'before':before,'after':after,'moment':price.display(price.moment(profile)),'scope':w['scope']};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
