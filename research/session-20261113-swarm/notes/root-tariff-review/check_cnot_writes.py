"""Separate byte-tape CPU counts actual CNOT merge writes on zero fields."""
from pathlib import Path
from types import ModuleType
import hashlib,json,sys
BASE=Path(__file__).resolve().parents[2]
P=BASE/'publication/native-endpoint/research/literal-selected-move-join/reference/linear'
raw=(P/'linear.py').read_bytes()
def need(ok,why):
    if not ok:raise ValueError(why)
need(hashlib.sha256(raw).hexdigest()=='d56704082b82e37d4a360b8aad7e0af63499f4160c6bbcfd338804453c46fa33','linear source pin')
sys.dont_write_bytecode=True;sys.pycache_prefix=str(BASE/'root-work/tariff-review/absent-cache')
need(not Path(sys.pycache_prefix).exists(),'cache isolation path must be absent')
L=ModuleType('independent_counted_linear');L.__file__=str(P/'linear.py');sys.modules[L.__name__]=L
exec(compile(raw,str(P/'linear.py'),'exec'),L.__dict__)
def build(target,control):
    a=L.Builder();L.cnot_columns(a,target,control);a.op('halt');a.mark('reject');a.op('read',L.HEADER,{})
    code,alphabet=a.finish((L.BLANK,'0',L.ONE,L.MARK))
    cuts=[pc for name,pc in a.labels.items() if name.endswith('column_done')]
    need(len(cuts)==1,'one column boundary')
    return code,cuts[0]
def run(shape,target,control,mutant=False):
    f,r,p,s,w=shape;v=2*p*s*r*w*(1<<(9*f));code,cut=build(target,control)
    if mutant:
        code=list(code);hits=0
        for i,ins in enumerate(code):
            if ins[0]=='read' and ins[1]==L.F and set(ins[2])=={'1','_'} and i>cut:
                code[i]=('read',L.F,{'1':ins[2]['_'],'_':ins[2]['_']});hits+=1
        need(hits==1,'one F continuation mutant')
    cooked=[]
    for op,*a in code:
        cooked.append(({'read':0,'write':1,'move':2,'goto':3,'halt':4}[op],*(
            (a[0],{ord(k):v for k,v in a[1].items()}) if op=='read' else
            (a[0],ord(a[1])) if op=='write' else tuple(a))))
    tapes=[bytearray(b'|_') for _ in range(27)];heads=[1]*27
    for t,n in ((L.F,f),(L.R,r),(L.P,p),(L.S,s),(L.WIDTH,w)):
        tapes[t]=bytearray(b'|'+b'1'*n+b'_')
    tapes[L.A]=bytearray(b'|'+b'0'*v+b'_');tapes[L.MODE]=bytearray(b'|0_')
    pc=steps=writes=0;boundaries=[];budget=250_000_000
    while True:
        if pc==cut:boundaries.append(writes)
        ins=cooked[pc];op=ins[0];pc+=1;steps+=1
        if op==0:
            t,branches=ins[1:];value=tapes[t][heads[t]]
            if value not in branches:raise ValueError(('rejected valid zero input',t,heads[t],value))
            pc=branches[value]
        elif op==1:
            t,value=ins[1:];tapes[t][heads[t]]=value
            writes+=t in (L.A,L.B) and value in (48,49)
        elif op==2:
            t,delta=ins[1:];need(delta in (-1,0,1),'unit move');heads[t]+=delta
            need(heads[t]>=0,'origin crossed')
            if heads[t]>=len(tapes[t]):tapes[t].extend(b'_'*(heads[t]-len(tapes[t])+1))
        elif op==3:pc=ins[1]
        elif op==4:break
        need(steps<budget,'bounded replay budget')
    need(all(h==1 for h in heads),'all unit-call heads returned')
    expected_columns=1 if mutant else f
    need(boundaries==[v*(i+1) for i in range(expected_columns)],'exact actual merge writes per completed column')
    need(writes==expected_columns*v,'complete merge write count')
    destination=L.B if expected_columns%2 else L.A;old=L.A if expected_columns%2 else L.B
    need(tapes[destination][1:v+1]==b'0'*v,'zero output complete')
    need(all(z==95 for z in tapes[old][1:]),'old source retired')
    return dict(shape=shape,target=target,control=control,V=v,steps=steps,merge_writes=writes,column_boundaries=boundaries,mutant=mutant)
def main():
    cases=[run((1,2,2,3,3),0,8),run((1,1,1,1,2),8,0),run((2,1,1,1,2),0,8)]
    mutation=run((2,1,1,1,2),0,8,True)
    need(mutation['merge_writes']<2*mutation['V'],'missing second column detected by write count')
    identities=0
    for f in range(1,65):
        for high in range(8):
            for low in range(high+1,9):
                for j in range(f):
                    a=1<<((high+1)*f-1-j);m=1<<((low-high)*f-1);b=4*(1<<((8-low)*f+j))
                    need(4*a*m*b==4*(1<<(9*f)),'symbolic geometry identity specialization');identities+=1
    print(json.dumps({'marker':'PASS_INDEPENDENT_CNOT_WRITE_COUNT','source_sha256':hashlib.sha256(raw).hexdigest(),
       'cases':cases,'negative_control':mutation,'geometry_specializations':identities,
       'scope':'CNOT unit-call boundary with complete zero fields and physical unary guides; not a supplied entry producer or full selected caller',
       'method':'separate byte-tape CPU; author Machine is not executed; exact universal count is the written column/prefix/middle invariant'},indent=2))
if __name__=='__main__':main()
