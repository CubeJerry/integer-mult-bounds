"""Bind the complete star correction to the exact signed chart-move convention."""
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent

def need(flag,label):
    if not flag:
        raise ValueError(label)

def load(name,digest):
    path=ROOT/'sources'/name
    need(hashlib.sha256(path.read_bytes()).hexdigest()==digest,'engine fingerprint '+name)
    spec=importlib.util.spec_from_file_location('star_'+path.stem,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    return mod

def bind(frames, pairs):
    need(__debug__,'inherited exact compiler requires enabled assertions')
    c=load('clifford_exact.py','2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962')
    v=load('native_verify.py','3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38')
    receipts=[]
    for a,b in sorted(pairs):
        f,h=tuple(frames[a]),tuple(frames[b])
        r,_=c.lower_child(c.canonical_frame(9,f).adjoint().then(c.canonical_frame(9,h)))
        need(r['rank']==1 and abs(len(f)-len(h))==1,'nonunit repair grade')
        want=v.adjoint(v.frame(f,9))+v.frame(h,9)
        v.equal(v.recipe(r),want,'exact signed repair transfer')
        if not receipts:
            bad=copy.deepcopy(r)
            bad['left']['phase']=(bad['left']['phase']+1)%4
            try:
                v.equal(v.recipe(bad),want,'mutated global phase')
            except ValueError:
                pass
            else:
                raise ValueError('ignored global phase')
        receipts.append({'from':a,'to':b,'recipe':r})
    return receipts

if __name__=='__main__':
    word=json.loads(gzip.decompress((ROOT/'sources'/'rail-base.json.gz').read_bytes()))
    corr=json.loads(gzip.decompress((ROOT/'sources'/'base-correction.json.gz').read_bytes()))
    sites=word['initial'].copy()+[None]*word['owned_fields']
    for op in word['program']:
        if op[0]=='MOVE':sites[op[1]]=op[3]
    pairs={(sites[int(j)],sites[i])for i,row in enumerate(corr)for j,c in row.items()if sites[int(j)]!=sites[i]}
    need(len(pairs)==192,'complete pair count')
    receipts=bind(word['frames'],pairs)
    encoded=json.dumps(receipts,separators=(',',':'),sort_keys=True).encode()
    (ROOT/'output'/'SIGNED-RECIPES.json.gz').write_bytes(gzip.compress(encoded,mtime=0))
    print('Verified signed global phase on',len(receipts),'star transfers',hashlib.sha256(encoded).hexdigest())
