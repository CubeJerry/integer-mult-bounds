#!/usr/bin/env python3
"""Coalesce only unread consecutive X moves; independent exact replay follows.

Other records may act between these moves, but no operation may read or write
the moved X record. This is a source transformation, not a decoder.
"""
import argparse, copy, gzip, hashlib, json
from collections import Counter
from pathlib import Path

def need(b,s):
    if not b: raise ValueError(s)

def coalesce(w):
    chains={}; edits={}; removed=set(); evidence=[]
    def finish(i):
        chain=chains.pop(i,[])
        if len(chain)<2:return
        first,last=w['program'][chain[0]],w['program'][chain[-1]]
        need(all(w['program'][a][3]==w['program'][b][2] for a,b in zip(chain,chain[1:])), 'same-record chain')
        edits[chain[0]]=['MOVE',i,first[2],last[3]]
        removed.update(chain[1:])
        evidence.append(dict(field=i,original_indices=chain,start=first[2],end=last[3]))
    for k,o in enumerate(w['program']):
        op,i=o[:2]
        if op=='MOVE' and i<111:chains.setdefault(i,[]).append(k)
        elif op=='ADD':
            for j in o[1:3]:
                if j<111:finish(j)
        elif i<111:finish(i)
    for i in list(chains):finish(i)
    z=copy.deepcopy(w);z['program']=[edits.get(k,o) for k,o in enumerate(w['program']) if k not in removed]
    z['coalescence']={'rule':'Only original-X same-record MOVE chains without any intervening read or write of that record','removed_moves':len(removed),'chains':evidence}
    return z

def replay(w):
    from fractions import Fraction as F
    def rref(rows):
        a=[list(map(F,r)) for r in rows];p=0
        for j in range(8):
            k=next((k for k in range(p,len(a)) if a[k][j]),None)
            if k is None:continue
            a[p],a[k]=a[k],a[p];t=a[p][j];a[p]=[x/t for x in a[p]]
            for k in range(len(a)):
                if k!=p:
                    t=a[k][j];a[k]=[x-t*y for x,y in zip(a[k],a[p])]
            p+=1
        return tuple(tuple(row) for row in a[:p])
    spaces={int(k):rref(v['B']) for k,v in w['frames'].items()}
    at=dict(enumerate(w['start']));rows={i:1<<i for i in range(222)};bill=Counter();xp=Counter();other=Counter();checked=set()
    for o in w['program']:
        op,i=o[:2];bill[op]+=1
        if op=='INIT':need(i not in at and i>=222,'fresh owned');at[i]=o[2];rows[i]=0
        elif op=='CLEAR':need(at.get(i)==o[2] and i>=222,'actual erasure');del at[i];del rows[i]
        elif op=='ADD':
            _,i,j,c=o;need(i!=j and at.get(i)==at.get(j)==c,'actual cochart');rows[i]^=rows[j]
        elif op=='MOVE':
            _,i,c,d=o;need(at.get(i)==c,'actual source');a,b=spaces[c],spaces[d];delta=len(b)-len(a)
            need(delta>0 if i<222 else delta<0,'unchanged monotone direction')
            if (c,d) not in checked:
                need(len(rref(a+b))==max(len(a),len(b)),'actual nested endpoints');checked.add((c,d))
            (xp if i<111 else other)[abs(delta)]+=1;at[i]=d
        else:raise ValueError(op)
    return rows,at,dict(counts=dict(bill),X_profile=dict(sorted(xp.items())),other_profile=dict(sorted(other.items())),nested_pairs=len(checked))

def main(a):
    a.output.mkdir(parents=True,exist_ok=True);receipts={}
    for name,pin in [('PREFIX.json.gz','a19e5d28edc7cbd0eea9a636233cf99a7b83693d955b4959f16fb59fc0299869'),('CLOSED-WORD.json.gz','3cfc771872c2d5d656f62ac1d59fd771bb73e748eb8ef0ce04d6e0979782d393')]:
        raw=(a.bundle/name).read_bytes();need(hashlib.sha256(raw).hexdigest()==pin,'frozen source pin');w=json.loads(gzip.decompress(raw));z=coalesce(w)
        rr,ll,bb=replay(w);rz,lz,bz=replay(z);need((rr,ll)==(rz,lz),'every public and owned row/chart unchanged')
        need({k:v for k,v in bb['counts'].items() if k!='MOVE'}=={k:v for k,v in bz['counts'].items() if k!='MOVE'},'all nonmovement costs retained')
        payload=(json.dumps(z,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);(a.output/name).write_bytes(blob)
        receipts[name]=dict(input_sha256=pin,output_sha256=hashlib.sha256(blob).hexdigest(),before=bb,after=bz,coalesced_chains=len(z['coalescence']['chains']),removed_moves=z['coalescence']['removed_moves'])
    need(receipts['CLOSED-WORD.json.gz']['after']['X_profile']=={1:4,2:15,3:84,4:84,5:15,6:4,7:8},'independently realized halfspan X profile')
    need(receipts['CLOSED-WORD.json.gz']['after']['other_profile']=={1:801},'Y777 plus three descending24 unit moves')
    out=dict(status='PASS_EXACT_X_ONLY_MOVE_COALESCENCE',receipts=receipts,all222_columns_and_live_owned_rows=True,actual_decoder_supplied=False,scope='Fixed prefix and its non-target closed preconditioner only; new decoder reads can split these chains.',new_kappa=None)
    (a.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'closed_profile':receipts['CLOSED-WORD.json.gz']['after']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
