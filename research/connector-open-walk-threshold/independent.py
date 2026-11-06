#!/usr/bin/env python3
"""Independent integer-coefficient execution of open-path connectors.

Written for CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
No imports from the primary constructor/verifier. The finite source words use
only positive immutable-source and output calls; symbols A_m, B_j stay formal.
"""
import copy
import json
from pathlib import Path

class Rejected(ValueError):
    pass

def need(value, message):
    if not value:
        raise Rejected(message)

def construct(data):
    k=data['dimension']; c=data['max_flip_count'];steps=data['transitions']
    need(type(k) is int and 2<=k<=10, 'dimension')
    need(type(c) is int and 2<=c<=128, 'characteristic')
    need(type(steps) is list and len(steps)==(1<<k)-1, 'path length')
    position=0; observed={0}; increases=[]; decreases=[];cuts={0:(0,0)}
    frequencies=[0]*k
    for axis in steps:
        need(type(axis) is int and 0<=axis<k,'axis')
        frequencies[axis]+=1
        if (position>>axis)&1:
            decreases.append(axis)
        else:
            increases.append(axis)
        position^=1<<axis
        need(position not in observed,'repeated vertex')
        observed.add(position)
        cuts[position]=(len(increases),len(decreases))
    need(len(observed)==1<<k,'cube coverage')
    need(frequencies==data['flip_counts'],'flip count declaration')
    need(max(frequencies)==c,'claimed maximum')
    need(c==((1<<k)-1+k-1)//k,'sharp length lower bound')
    padding=[]
    for axis, count in enumerate(frequencies):
        need(count<=c,'insufficient characteristic')
        padding.extend([axis]*(c-count))
    source_word=increases+padding+list(reversed(decreases))
    requests={mask:[0]*(c-2)+[u,k*c-d] for mask,(u,d) in cuts.items() if mask}
    return k,c,source_word,requests

def execute(k,c,word,requests):
    """Check full action using formal z0, B_j*x_j and each target's y0."""
    need(type(word) is list and len(word)==k*c,'source call count')
    need(set(requests)==set(range(1,1<<k)),'output set')
    bucket=[[] for _ in range(len(word)+1)]
    output_rows={mask:[1]+[0]*(k+1) for mask in requests}
    for mask,times in requests.items():
        need(len(times)==c,'output call count')
        for time in times:
            need(type(time) is int and 0<=time<=len(word),'read boundary')
            bucket[time].append(mask)
    # q = z0 + sum q_j B_j*x_j, evaluated by actual calls alone.
    q=[1]+[0]*k;calls=[0]*k
    for boundary in range(len(word)+1):
        for mask in bucket[boundary]:
            row=output_rows[mask]
            for j,coefficient in enumerate(q):
                row[j+1]=(row[j+1]+coefficient)%c
        if boundary<len(word):
            axis=word[boundary]
            need(type(axis) is int and 0<=axis<k,'source axis')
            q[axis+1]=(q[axis+1]+1)%c
            calls[axis]+=1
    need(calls==[c]*k,'source multiplicities')
    need(q==[1]+[0]*k,'dirty connector restoration')
    for mask,row in output_rows.items():
        expected=[1,0]+[(mask>>j)&1 for j in range(k)]
        need(row==expected,'arbitrary-input target action')
    return {'dimension':k,'characteristic':c,'masks':(1<<k)-1,
            'source_calls':len(word),'output_calls':c*((1<<k)-1),
            'complete_calls':c*(k+(1<<k)-1),
            'formal_coefficients_checked':((1<<k)-1)*(k+2)}

def rejects(operation):
    try:
        operation()
    except Rejected:
        return
    raise RuntimeError('negative control accepted')

def controls(data):
    k,c,w,req=construct(data)
    faults=[]
    x=copy.deepcopy(data);x['dimension']=True;faults.append(lambda x=x:construct(x))
    x=copy.deepcopy(data);x['transitions'][0]=k;faults.append(lambda x=x:construct(x))
    x=copy.deepcopy(data);x['transitions'][1]=x['transitions'][0];faults.append(lambda x=x:construct(x))
    x=copy.deepcopy(data);x['flip_counts'][0]+=1;faults.append(lambda x=x:construct(x))
    x=copy.deepcopy(data);x['max_flip_count']-=1;faults.append(lambda x=x:construct(x))
    faults.append(lambda:execute(k,c,w[:-1],req))
    r=copy.deepcopy(req);r[1]=r[1][1:];faults.append(lambda r=r:execute(k,c,w,r))
    r=copy.deepcopy(req);del r[1];faults.append(lambda r=r:execute(k,c,w,r))
    r=copy.deepcopy(req);r[1][-1]=len(w)+1;faults.append(lambda r=r:execute(k,c,w,r))
    # An actual one-boundary shift changes exactly one source coefficient.
    r=copy.deepcopy(req);r[1][-2]+=1;faults.append(lambda r=r:execute(k,c,w,r))
    # Losing one baseline-cancelling read and adding it after one source call
    # retains c output calls but must corrupt one target coefficient.
    r=copy.deepcopy(req);r[1][0]=1;faults.append(lambda r=r:execute(k,c,w,r))
    for f in faults:rejects(f)
    return len(faults)

def main():
    bundle=json.loads(Path(__file__).with_name('WITNESSES.json').read_text())
    need(bundle['schema']=='cube-covering-open-walk-v1','schema')
    need([x['dimension'] for x in bundle['walks']]==[6,9,10],'fixture inventory')
    results=[]
    for data in bundle['walks']:
        k,c,w,r=construct(data)
        result=execute(k,c,w,r);result['controls']=controls(data)
        results.append(result)
    print(json.dumps({'results':results,'status':'PASS_INDEPENDENT_OPEN_PATH_CONNECTOR'},sort_keys=True))

if __name__=='__main__':main()
