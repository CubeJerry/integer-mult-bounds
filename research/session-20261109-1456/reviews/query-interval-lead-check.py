"""Independent dense character audit; no submitted arithmetic imported.
Two D9 values suffice only because each word has exactly one D9 service.
Four exact q characters retain all 38 independent input columns.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
import hashlib,json,sys
P=Path(sys.argv[1]).resolve();sys.path.insert(0,str(P))
from replacement import transform,three_queries,START,STOP
Z=(F(0),F(0));ONE=(F(1),F(0))
def need(x,m):
    if not x:raise ValueError(m)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,x):return(a[0]*x,a[1]*x)
def power(a,k):
    out=ONE
    for _ in range(k%4):out=mul(out,a)
    return out
def run(events,n,q,D,projector=False):
    rows=[[ONE if i==j else Z for j in range(n)] for i in range(n)]
    for e in events:
        need(e[0]=='A','same-chain A operations');op,r=e[1:3]
        if op=='SWAP':rows[r],rows[e[3]]=rows[e[3]],rows[r];continue
        if op=='ADD':c=(F(e[4]),F(0));src=rows[e[3]];rows[r]=[add(a,mul(c,b)) for a,b in zip(rows[r],src)];continue
        if op=='QUERY':c=power(q,e[4]);src=rows[e[3]];rows[r]=[add(a,mul(c,b)) for a,b in zip(rows[r],src)];continue
        if op=='SCALE':c=(F(e[3]),F(0))
        elif op=='QSELF':c=power(q,e[3])
        elif op=='IDLE_ONE':need(e[3]==[9],'single D9');c=(F(D),F(0))
        elif op=='LAMBDA':
            sign=0 if projector else e[3];c=scale(add((F(1),F(sign)),mul((F(1),F(-sign)),power(q,2))),F(1,2))
        else:raise ValueError(op)
        rows[r]=[mul(c,a) for a in rows[r]]
    return rows
caller=json.loads((P/'data/caller_efree.json').read_text());new=transform(caller)
old=caller['events'][START:STOP];fresh=new['events'][START:START+223]
need(new['events'][:START]==caller['events'][:START] and new['events'][START+223:]==caller['events'][STOP:],'same context')
for word in [old,fresh]:need(sum(e[1]=='IDLE_ONE' for e in word)==1,'degree-one D bound')
chars=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1))];matrices=0;controls=set()
for q in chars:
    for D in [0,2]:
        want=run(old,38,q,D);need(run(fresh,38,q,D)==want,'full dense interval identity');matrices+=1
        bad=deepcopy(fresh);bad.pop(next(i for i,e in enumerate(bad) if e==['A','ADD',0,2,'-1']))
        if run(bad,38,q,D)!=want:controls.add('omitted conjugation correction')
        if run(fresh,38,q,D,projector=True)!=want:controls.add('unit lambda replaced by projector')
        bad=deepcopy(fresh);j=next(i for i,e in enumerate(bad) if e[1]=='IDLE_ONE');bad.insert(j,bad[j][:])
        if run(bad,38,q,D)!=want:controls.add('D9 square differs from D9')
    target=[['A','QSELF',0,-1],['A','QSELF',1,-1],['A','QUERY',2,3,-1]]
    need(run(three_queries(0,1,2,3),4,q,0)==run(target,4,q,0),'arbitrary four-field gadget')
need(len(controls)==3,'all independent controls detected')
print(json.dumps(dict(status='PASS_INDEPENDENT_DENSE_INTERVAL',independent_inputs=38,central_characters=4,D9_values=[0,2],D9_degree_bound=1,dense_matrices=matrices,scalar_equalities=matrices*38*38,controls=sorted(controls),emitter_sha256=hashlib.sha256((P/'replacement.py').read_bytes()).hexdigest(),source_caller_sha256=hashlib.sha256((P/'data/caller_efree.json').read_bytes()).hexdigest(),scope='Exact local polynomial certificate in different representation; shared candidate emitter; no physical/compiler admission'),sort_keys=True))
