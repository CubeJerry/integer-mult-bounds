"""An independent two/four-point Walsh tape base, with real modular data.

Inputs A, M and S are streams. Residues and M have K low-first digits, with
high zero padding allowed. S is a canonical high-first suffix record count.
runpy loads the fixed generic rule builder; it never sees data in compilation.
"""
import itertools
import json
from pathlib import Path
import random
import runpy

T=runpy.run_path(str(Path(__file__).with_name("node-tapes.py")))
Builder,Action,Simulation=(T[n] for n in ("Builder","Action","Simulation"))
B,H,STAR,STOP=(T[n] for n in ("BLANK","HOME","MARK","HALT"))

def bind_bits(b,tapes,leaf,known=()):
    if not tapes:
        a=leaf(known)
        return b.op(a.target,a.writes,a.moves)
    t=tapes[0]
    return b.sel(b.label("read operand bit"),t,
        {str(v):Action(bind_bits(b,tapes[1:],leaf,known+(v,))) for v in range(2)})

def signed_sum(b,regs,v,output,target):
    """T = 4M + sum sign(u,v)*X[u]. Output in K+3 bits. Return all heads."""
    next_state=b.reset_group(("M",output)+regs,target)
    states={c:b.label("signed carry") for c in range(-4,8)}
    signs=[-1 if (i&v).bit_count()%2 else 1 for i in range(len(regs))]
    moves=tuple((t,1) for t in regs+("M",output))
    for carry,p in states.items():
        cases={}
        for mbit in (0,1):
            def leaf(vals,mbit=mbit,carry=carry):
                total=carry+4*mbit+sum(s*x for s,x in zip(signs,vals))
                return Action(states[total//2],((output,str(total%2)),),moves)
            cases[str(mbit)]=Action(bind_bits(b,regs,leaf))
        if carry>=0:
            end=next_state
            for j in reversed(range(3)):
                end=b.op(end,((output,str((carry>>j)&1)),),((output,1),))
            cases[B]=Action(end)
        b.sel(p,"M",cases)
    return states[0]

def mod_addsub(b,*,subtract,target_no,target_extra):
    """T +=/-= M mod 2^(K+3); select continuation by carry/borrow."""
    directions=(("T",1),("M",1))
    normal=[b.label("add/subtract modulus") for _ in range(2)]
    high=[b.label("high digit") for _ in range(2)]
    def digit(x,y,c):
        n=x-y-c if subtract else x+y+c
        return n%2,int(n<0 if subtract else n>=2)
    for c in range(2):
        choices={}
        for y in range(2):
            def step(vals,y=y,c=c):
                v,flag=digit(vals[0],y,c)
                return Action(normal[flag],(("T",str(v)),),directions)
            choices[str(y)]=Action(bind_bits(b,("T",),step))
        choices[B]=Action(high[c])
        b.sel(normal[c],"M",choices)
        after=b.reset_group(("M","T"),target_extra if c else target_no)
        cases={B:Action(after)}
        for x in range(2):
            v,flag=digit(x,0,c)
            cases[str(x)]=Action(high[flag],(("T",str(v)),),(("T",1),))
        b.sel(high[c],"T",cases)
    return normal[0]

def word(b,regs,v,dest,half,nxt):
    emit=b.run("k",b.rewind("T",b.erase("T",nxt)),((dest,("copy","T")),),
               (("T",1),(dest,1)))
    if half:
        skip=b.op(emit,moves=(("T",1),))
        odd=mod_addsub(b,subtract=False,target_no=skip,target_extra=skip)
        emit=b.test("T",{"0":skip,"1":odd})
    for _ in range(7):
        undo=mod_addsub(b,subtract=False,target_no=emit,target_extra=emit)
        emit=mod_addsub(b,subtract=True,target_no=emit,target_extra=undo)
    return signed_sum(b,regs,v,"T",emit)

def compile_walsh(q,half):
    if q not in (2,4):
        raise ValueError(q)
    b=Builder()
    lanes=tuple(f"D{i}" for i in range(q))
    out=tuple(f"F{i}" for i in range(q))
    regs=tuple(f"U{i}" for i in range(q))
    tapes=("A","M","S","s","k","temp","T") + lanes+out+regs
    nxt=T["boundaries"](b,tapes,STOP,close=True)
    for t in ("s","k"):
        nxt=b.erase(t,nxt)
    nxt=b.reset_group(("A",)+out,nxt)
    merge=b.label("merge prefix")
    def block(src,dst,nxt,clear):
        return b.unary_loop("s",lambda after: T["plain_copy"](b,"k",src,dst,after,clear=clear),nxt)
    row=merge
    for i in reversed(range(q)):
        row=block(out[i],"A",row,True)
    b.sel(merge,out[0],{B:Action(nxt)},Action(row))
    nxt=b.reset_group(lanes+out,merge)
    compute=b.label("stage a full q-tuple")
    after=compute
    for t in regs:
        after=b.erase(t,after)
    for v in reversed(range(q)):
        after=word(b,regs,v,out[v],half,after)
    after=b.reset_group(regs,after)
    action=tuple((u,("copy",d)) for u,d in zip(regs,lanes))+tuple((d,B) for d in lanes)
    moves=tuple((t,1) for t in regs+lanes)
    stage=b.run("k",after,action,moves)
    b.sel(compute,lanes[0],{B:Action(nxt)},Action(stage))
    top=b.label("split prefix")
    row=top
    for i in reversed(range(q)):
        row=block("A",lanes[i],row,True)
    b.sel(top,"A",{B:Action(b.reset_group(("A",)+lanes,compute))},Action(row))
    cnt=b.label("derive padded K directly from M")
    b.sel(cnt,"M",{B:Action(b.reset_group(("M","k"),top))},
          Action(cnt,(("k",STAR),),(("M",1),("k",1))))
    first=b.unary_from_binary("S","s","temp",cnt)
    return b,tapes,T["boundaries"](b,tapes,first,close=False)

def little(x,k):
    return format(x,f"0{k}b")[::-1]

def check_case(program,q,half,mod,k,p,s,data):
    raw="".join(little(x,k) for x in data)
    inputs={"A":raw,"S":format(s,"b"),"M":little(mod,k)}
    oracle=[]
    for j in range(p):
        for v in range(q):
            for h in range(s):
                val=sum((-1 if (i&v).bit_count()%2 else 1)*data[(j*q+i)*s+h]
                        for i in range(q))
                oracle.append((val*(pow(2,-1,mod) if half else 1))%mod)
    sim=Simulation(program,inputs).execute(2**14*len(raw))
    expected={**inputs,"A":"".join(little(x,k) for x in oracle)}
    assert all(sim.contents(t)==expected.get(t,"") and sim.head[t]==0 for t in sim.tapes)
    assert sim.visited<=128*len(raw)
    return sim.steps,sim.visited

def check_group_pipeline(programs):
    """Exercise both selected-bit groups, preserving every unselected position.

    The chosen outer position permutation, integer shift and centered lift are
    specification-level operations here. Every 2/4-point butterfly below runs
    its literal finite transition list.
    """
    rng=random.Random(51493)
    tests=steps=0
    counts={}
    for k,picks in ((1,(0,1)),(2,(0,1,2,3)),(3,(0,1,3,5,7)),
                    (4,(1,5,12,15)),(5,(3,7,13,19,25,31)),(6,(11,23,45,63))):
        count=1<<k
        modulus=65537
        width=modulus.bit_length()+1
        for mask in picks:
            data=[rng.randrange(-31,32) for _ in range(count)]
            expected=[sum((-1 if ((i&j&mask).bit_count()&1) else 1)*data[j]
                          for j in range(count) if (i^j)&~mask==0) for i in range(count)]
            selected=[i for i in range(k) if mask>>i&1]
            cut=(k+1)//2
            working=list(data)
            for group in (selected[:cut],selected[cut:]):
                if not group:
                    continue
                # In new addresses bit 0 is group[0]; all spectators preserve
                # their relative order. The same index array later scatters
                # back to old addresses.
                order=group+[i for i in range(k) if i not in group]
                old=[sum(((n>>s)&1)<<i for s,i in enumerate(order)) for n in range(count)]
                shift=1<<(len(group)//2)
                bank=[(shift*working[i])%modulus for i in old]
                for pos in range(0,len(group),2):
                    q=4 if pos+1<len(group) else 2
                    half=(q==4)
                    suffix=1<<pos
                    inputs={"A":"".join(little(x,width) for x in bank),
                            "M":little(modulus,width),"S":format(suffix,"b")}
                    sim=Simulation(programs[q,half],inputs).execute(2**14*width*count)
                    assert all(sim.head[t]==0 and sim.contents(t)==inputs.get(t,"")
                               for t in sim.tapes if t!="A") and sim.head["A"]==0
                    stream=sim.contents("A")
                    bank=[int(stream[n*width:(n+1)*width][::-1],2) for n in range(count)]
                    steps+=sim.steps
                    counts[q]=counts.get(q,0)+1
                centered=[x if 2*x<=modulus else x-modulus for x in bank]
                working=[None]*count
                for i,x in zip(old,centered):
                    working[i]=x
            assert working==expected
            tests+=1
    return {"group_executions":tests,"group_transitions":steps,"group_passes":counts}

def main():
    rng=random.Random(27441)
    count=steps=cells=maximum=0
    programs={}
    for q,half in ((2,False),(2,True),(4,True)):
        program=compile_walsh(q,half)
        programs[q,half]=program
        for mod,k in ((3,2),(5,7),(17,5),(63,6),(73,10),(511,9)):
            for p,s in ((1,1),(1,2),(2,1),(2,3)):
                data=[rng.randrange(mod) for _ in range(p*s*q)]
                t,c=check_case(program,q,half,mod,k,p,s,data)
                steps+=t; cells+=c; maximum=max(maximum,t); count+=1
        if q==4:
            for data in itertools.product(range(3),repeat=4):
                t,c=check_case(program,q,half,3,2,1,1,data)
                steps+=t; cells+=c; maximum=max(maximum,t); count+=1
    result=dict(executions=count,transitions=steps,visited_sum=cells,max_transitions=maximum)
    result.update(check_group_pipeline(programs))
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":
    main()
