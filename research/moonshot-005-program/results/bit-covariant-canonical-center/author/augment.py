"""Overlay all of S028's center contribution along both complete target stars."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np


def require(ok,label):
    if not ok:raise ValueError(label)


def dump(word):return json.dumps(word,sort_keys=True,separators=(',',':')).encode()


def load(path,pin):
    b=gzip.decompress(path.read_bytes());require(hashlib.sha256(b).hexdigest()==pin,'pin '+str(path));return json.loads(b)


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    native=a.repo/'research/moonshot-005-program/results';geo=load(native/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
    raw=gzip.decompress((native/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
    require(hashlib.sha256(raw).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','physical owners')
    routes=[json.loads(r) for r in raw.splitlines()];ledger=json.loads((a.base/'RESULT.json').read_bytes());additional={}
    for side,early in [('row',True),('column',False)]:
        tag='row' if early else 'column';phase='X' if early else 'Y';offset=0 if early else 53280
        word=load(a.base/(side+'-word.json.gz'),ledger['word_SHA256'][side]);reg=set(word['regular']);counts={'endpoint':0,'plane':0}
        for ell,j in enumerate(word['regular'],1):
            # In the early adjoint this sends the additional center to the original tail.
            role=offset+480*j
            for g in range(8):word['endpoint'][str(j)].append(['a',role+g,role+8*ell+g,1]);counts['endpoint']+=48
        for st,k in word['internal_anchor'].items():
            j=int(st);regular=min(reg.intersection(geo['A2'][k]));site=3 if early else 5
            def owners(who):
                result=sorted(offset+480*t[1]+t[2] for t in routes if t[0]==phase and t[1]==who and t[site]==k)[:8]
                require(len(result)==8,'real internal and pivot outlets');return result
            active=owners(regular);partial=owners(j)
            for x,y in zip(active,partial):
                for c in range(8):word['plane'][str(k)].append(['c',8*y+c,8*x+c]);counts['plane']+=6
        dat=dump(word);(a.out/(side+'-word.json.gz')).write_bytes(gzip.compress(dat,mtime=0));ledger['word_SHA256'][side]=hashlib.sha256(dat).hexdigest()
        for stage,price in counts.items():ledger['word_costs'][side]['pure_by_stage_binary_ADD'][stage]+=price
        ledger['word_costs'][side]['OPCODE_counts_including_bundles']['endpoint']['a']+=counts['endpoint']//48
        ledger['word_costs'][side]['OPCODE_counts_including_bundles']['plane']['c']+=counts['plane']//6
        for label in ('pure_forward_ADD','pure_reverse_ADD'):ledger['word_costs'][side][label]+=sum(counts.values())
        ledger['word_costs'][side]['total_ADD']+=2*sum(counts.values());additional[side]=counts
    ledger['additional_base_overlay_forward_stage_ADD']=additional
    ledger['total_binary_ADD']=sum(x['total_ADD'] for x in ledger['word_costs'].values())
    ledger['target']='Entire S028 Delta plus the canonical central I64 at all 123 modified edges.'
    ledger['correct_entire_F80_center_on_every_source']=True;ledger['correct_entire_transfer_on_line10_center']=True
    (a.out/'RESULT.json').write_text(json.dumps(ledger,sort_keys=True,indent=2)+'\n');print(ledger['total_binary_ADD'],additional)


if __name__=='__main__':main()
