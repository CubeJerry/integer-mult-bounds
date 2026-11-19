#!/usr/bin/env python3
"""Separate GF(4) scaling and sharp shared-repair controls."""
import argparse,json
from pathlib import Path
def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return z
def rank(a):
    a=[r[:] for r in a if any(r)];h=0
    if not a:return 0
    for j in range(len(a[0])):
        p=next((i for i in range(h,len(a)) if a[i][j]),None)
        if p is None:continue
        a[h],a[p]=a[p],a[h]
        u=next(x for x in range(1,4) if mul(x,a[h][j])==1)
        a[h]=[mul(u,v) for v in a[h]]
        for i in range(len(a)):
            if i!=h and a[i][j]:
                c=a[i][j];a[i]=[u^mul(c,v) for u,v in zip(a[i],a[h])]
        h+=1
        if h==len(a):break
    return h
def span(rows):
    out={0}
    for r in rows:out|={x^r for x in list(out)}
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    h=[[int(j%2==k) for j in range(8)] for k in range(2)]
    o=[[int(i//2!=j//2 and i%2==j%2) for j in range(8)] for i in range(8)]
    samples=[]
    for t in (1,2,3):
        b=[[mul(v,t if j%2 else 1) for j,v in enumerate(row)] for row in o]
        err=[[v^int(i==j) for j,v in enumerate(row)] for i,row in enumerate(b)]
        samples.append({'t':t,'repair_rank':rank(h+err)-rank(h)})
    assert [x['repair_rank'] for x in samples]==[0,3,3]
    assert sum(max(0,3-x['repair_rank']) for x in samples)<=3
    sharp=[]
    for s in range(1,9):
        q=s-1;u=[1<<i for i in range(q)];z=1<<q;targets=[span(u)]
        for i in range(q):targets.append(span([v^(z if j==i else 0) for j,v in enumerate(u)]))
        common=set.intersection(*targets);ambient=span(u+[z])
        assert all(t<=ambient and len(t)==2**q for t in targets)
        assert common=={0}
        sharp.append({'receivers':s,'shared_repair_dimension':1,'port_dimension':q,'intersection_dimension':0})
    assert sharp[2]['port_dimension']>1
    out={'scaling_GF4':samples,'isolation_dimension':3,'sharp_controls':sharp,'factor_one_counterexample':True,
         'scope':'Independent algebraic controls, not physical balanced routing; all-field proof is separate.'}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS separate scaling and shared-repair controls')
if __name__=='__main__':main()
