#!/usr/bin/env python3
"""Primary exact constructor checks; @CubeJerry + OpenAI Codex, Apache-2.0."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
from construct import Block, capacity_parameters, concatenated_reads, require
P=Path(__file__).resolve().parent
ROOT=P.parent.parent

def rejects(fn):
    try: fn()
    except ValueError: return 1
    raise RuntimeError('negative control accepted')

def check(word,reads,c,mask,k):
    require(Counter(word)==Counter({j:c for j in range(k)}),'source multiplicities')
    require(len(reads)<=c and all(0<=t<=len(word) for t in reads),'read budget')
    at=Counter(reads); prefix=[0]*k; result=[0]*k
    for t in range(len(word)+1):
        for j in range(k): result[j]+=at[t]*prefix[j]
        if t<len(word): prefix[word[t]]+=1
    require([v%c for v in result]==[(mask>>j)&1 for j in range(k)],'literal prefix sum')
    require(all(v%c==0 for v in prefix),'restoration')

def main():
    controls=cases=masks=0
    for row in json.loads((P/'SOURCES.json').read_text())['files']:
        if row['usage']!='input': continue
        raw=(ROOT/row['path']).read_bytes()
        require(sha256(raw).hexdigest()==row['sha256'],'source digest')
        controls+=rejects(lambda raw=raw,row=row: require(sha256(raw+b'\n').hexdigest()==row['sha256'],'source mutation'))
    fixtures=json.loads((P/'FIXTURES.json').read_text())
    for f in fixtures:
        block=Block(f['groups'],f['width'],f['characteristic']); copies=f['copies']
        word=[i*block.sources+j for i in range(copies) for j in block.word()]
        require(word==f['source_word'],'independent source fixture')
        for m,times in f['reads'].items():
            reads=concatenated_reads(block,copies,int(m))
            require(list(reads)==times,'independent read fixture')
            check(word,reads,block.characteristic,int(m),block.sources*copies); masks+=1
        cases+=1
    for c in range(2,19):
        for D in range(1,min(4,c-1)+1):
            for b in range(1,4):
                if D*((1<<b)-1)>c or D*b>8: continue
                block=Block(D,b,c); word=list(block.word())
                require(block.reads(0)==(),'empty part')
                for m in range(1,1<<block.sources):
                    reads=block.reads(m); require(len(reads)<=D+1,'depth')
                    check(word,reads,c,m,block.sources); masks+=1
                cases+=1
    block=Block(2,2,6); word=list(block.word()); reads=list(block.reads(15))
    bad=list(reads); bad[-1]+=1
    controls+=rejects(lambda: check(word,bad,6,15,4))
    controls+=rejects(lambda: check(word[:-1],reads,6,15,4))
    controls+=rejects(lambda: check(word,[block.round_for(0,3)*4+2],6,3,4))
    controls+=rejects(lambda: Block(3,1,3))
    controls+=rejects(lambda: Block(2,3,13))
    controls+=rejects(lambda: concatenated_reads(block,3,1))
    controls+=rejects(lambda: block.reads(16))
    for c in range(2,65537):
        b,copies,n=capacity_parameters(c); D=b.groups; w=b.width
        require(D*((1<<w)-1)<=c<D*((1<<(w+1))-1),'maximal width')
        require(n==D*w*copies and copies*(D+1)<=c,'capacity formula')
        require(n>=c*w-c-D*(D+1),'elementary integer lower estimate')
    table=[]
    for e in (4,8,16,32,64,128,1024,4096):
        c=1<<e; b,_,n=capacity_parameters(c)
        require(n>=c*b.width-c-b.groups*(b.groups+1),'large capacity')
        table.append({'log2_c':e,'groups':b.groups,'width':b.width,'ratio_ppm':10**6*n//(c*e)})
    print('PASS_ROUND_OFFSET_CAPACITY '+json.dumps({'schedule_cases':cases,'masks':masks,'capacity_integers':65535,'negative_controls':controls,'table':table},sort_keys=True))
if __name__=='__main__': main()
