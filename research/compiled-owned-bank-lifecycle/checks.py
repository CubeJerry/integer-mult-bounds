"""Independent data/byte oracles and discriminating physical fixtures.

Hardware observation, host recursion, lists of values and expected outcomes
are confined to this checker. Fixture services are explicitly not Gaussians.
"""
from collections import Counter
from copy import deepcopy
from functools import lru_cache


def need(ok,message):
    if not ok:
        raise ValueError(message)


def encode(values,width):
    symbols = []
    for value in values:
        need(-(1 << (width-1)) <= value < (1 << (width-1)),"fixture signed headroom")
        symbols += [(value >> j)&1 for j in range(width)]+[2]
    return [bit for s in symbols for bit in ((s>>2)&1,(s>>1)&1,s&1)]


def body(tape,marker=2):
    start = tape.head
    while start and tape.cells[start-1] != marker:
        start -= 1
    end = start
    while end<len(tape.cells) and tape.cells[end] != 6:
        end += 1
    return list(tape.cells[start:end])


def load(tape,bits,M,marker=2):
    M.retire(tape,marker)
    for bit in bits:
        M.emit(tape,bit)
    M.origin(tape,marker)


def decode(bits,width):
    need(len(bits)%3==0,"oracle code alignment")
    symbols = [4*bits[i]+2*bits[i+1]+bits[i+2] for i in range(0,len(bits),3)]
    out = []
    while symbols:
        part,symbols = symbols[:width+1],symbols[width+1:]
        need(len(part)==width+1 and part[-1]==2 and all(x in (0,1) for x in part[:-1]),"oracle field format")
        n = sum(x << j for j,x in enumerate(part[:-1]))
        out.append(n-(1 << width) if part[-2] else n)
    return out


class FixtureRows:
    """Literal g-way complete-record split/return, with a unary depth header.

    g and two signed components per record are fixed finite control. Only
    read/write/unit-move methods drive these routines. This is a test row
    implementation, not the selected front/back or binary stock producer.
    """
    def __init__(self,M,metadata,g):
        self.M,self.metadata,self.g = M,metadata,g

    def is_leaf(self,token):
        symbol = self.metadata.read()
        self.M.need(symbol in (1,6),"unary fixture depth")
        return symbol==6

    def prepare(self,token,header):
        M = self.M
        M.need(self.metadata.read()==1,"positive fixture depth")
        M.need(header.read()==6,"empty staged header")
        self.metadata.move(1)
        while (symbol:=self.metadata.read())!=6:
            M.need(symbol==1,"unary fixture header")
            M.emit(header,symbol); self.metadata.move(1)
        M.origin(self.metadata); M.origin(header,5)

    def record(self,source,target):
        M = self.M
        for _ in range(2):
            nonempty = False
            while True:
                symbol = M.read_code(source)
                M.need(symbol in (0,1,2),"complete numerical row")
                M.write_code(target,symbol)
                if symbol==2:
                    M.need(nonempty,"positive component width")
                    break
                nonempty = True

    def install(self,bridge,header,public):
        M = self.M
        M.need(len(public)==self.g,"fixed productive role count")
        while bridge.read()!=6:
            for tape in public:
                self.record(bridge,tape)
        M.origin(bridge,5)
        for tape in public:
            M.origin(tape)
        M.transfer(header,self.metadata,source_marker=5)

    def collect(self,public,bridge):
        M = self.M
        M.need(bridge.read()==6,"empty output bridge")
        while public[0].read()!=6:
            for tape in public:
                self.record(tape,bridge)
        for tape in public:
            M.need(tape.read()==6,"complete equal output row counts")
            M.origin(tape)
        M.origin(bridge,5)


WRITE_ONE = (("write",0,1),("halt",))
IDENTITY = (("halt",),)


def program(unit,M):
    code = tuple(M.Instruction(e.op,e.fields,e.token) for e in unit.events)+(M.Instruction("RET"),)
    services = {}
    for e in code:
        if e.op=="SERVICE":
            services[e.token] = WRITE_ONE
        elif e.op=="PAID":
            services[("leaf",)+e.token] = WRITE_ONE
    return code,services


def oracle(code,public,bank_count,depth):
    """Separate value-level interpreter, with Python recursion only in oracle."""
    fields = [list(x) for x in public]+[[] for _ in range(bank_count-len(public))]
    g = len(public)
    for e in code:
        if e.op=="INIT":
            fields[e.ports[0]] = [0]*len(fields[0])
        elif e.op=="CLEAR":
            fields[e.ports[0]] = []
        elif e.op=="COPY":
            a,b = e.ports
            fields[a] = [x+y for x,y in zip(fields[a],fields[b])]
        elif e.op=="SERVICE" or (e.op=="PAID" and depth==0):
            fields[e.ports[0]][0] |= 1
        elif e.op=="PAID":
            owner = e.ports[0]
            values = fields[owner]
            rows = [values[i:i+2] for i in range(0,len(values),2)]
            need(len(rows)%g==0,"oracle integral complete rows")
            sub = [[x for row in rows[j::g] for x in row] for j in range(g)]
            out = oracle(code,sub,bank_count,depth-1)
            fields[owner] = [out[j][2*i+k] for i in range(len(rows)//g) for j in range(g) for k in (0,1)]
        elif e.op=="RET":
            break
        else:
            raise ValueError("oracle opcode")
    return fields[:g]


def arithmetic_checks(M,S):
    cases = []
    for width in (2,3,5,9):
        low,high = -(1 << (width-1)),(1 << (width-1))-1
        pairs = [(a,b) for a in range(low,high+1) for b in range(low,high+1)
                 if low <= a+b <= high] if width<=3 else [(low,0),(high,0),(-3,2),(2,-1),(0,high)]
        for a,b in pairs:
            counts = S.Counts();src=S.Tape(counts=counts);dst=S.Tape(counts=counts)
            load(src,encode([a,-a if a!=low else 0],width),M)
            load(dst,encode([b,0],width),M)
            before=counts.total
            M.copy_as_add(dst,src)
            need(decode(body(dst),width)==[a+b,-a if a!=low else 0],"actual signed COPY-as-ADD")
            need(counts.total-before==35*(2*width)+26*2+14,"exact COPY-as-ADD invoice")
            cases.append((width,a,b))
        for dirty in ([],[1],[1,0,0]*17):
            counts=S.Counts();src=S.Tape(counts=counts);dst=S.Tape(counts=counts)
            bits=encode([low,high],width);load(src,bits,M);load(dst,dirty,M)
            before=counts.total;M.initialize(dst,src)
            need(decode(body(dst),width)==[0,0],"canonical zero includes component delimiters")
            need(counts.total-before==5*len(dirty)+25*(len(bits)//3)+17,"exact dirty INIT invoice")
            before=counts.total;M.retire(dst)
            need(counts.total-before==5*len(bits)+7 and body(dst)==[],"exact complete CLEAR invoice")
    # Overflow must fail even in optimized Python.
    for a,b in ((3,1),(-4,-1)):
        src,dst=S.Tape(),S.Tape();load(src,encode([a],3),M);load(dst,encode([b],3),M)
        try:M.copy_as_add(dst,src)
        except ValueError as e:need("overflow" in str(e),"specific overflow rejection")
        else:raise ValueError("overflow accepted")
    return dict(signed_add_cases=len(cases),initialization_cases=12,overflow_controls=2)


def context_checks(M,S):
    """Runtime descriptor data reach native tables only through local ports."""
    table=(("write",1,1),("move",1,1),("write",1,4),
           ("branch",2,((0,4),(1,6)),8),("write",0,0),("goto",7),
           ("write",0,1),("halt",),("reject","empty binary context"))
    cases=[]
    for prefix in (0,17,257):
        for bit in (0,1):
            field,work,header=S.Tape([1]*prefix),S.Tape([0]*prefix),S.Tape([0]*prefix)
            load(field,encode([0,0],5),M);load(header,[bit,1,0,1],M)
            load(work,[1,0,0]*9,M)
            snapshot=list(header.cells);head=header.head
            external=[S.Tape([0]*prefix,marker=S.BASE) for _ in range(4)]
            code=(M.Instruction("SERVICE",(0,),("context",)),M.Instruction("RET"))
            controller=M.Controller(code,1,(field,work,header),*external,
                                    FixtureRows(M,header,1),{("context",):table},S.Stack,
                                    protected_ports=(2,),primitive_work=(1,),primitive_context=(2,))
            controller.run()
            need(decode(body(field),5)==[bit,0],"actual runtime binary context branch")
            need(header.cells==snapshot and header.head==head,"borrowed raw descriptor restored")
            need(body(work)==[],"native auxiliary body physically retired")
            cases.append((prefix,bit))
    controls={}
    for name,table in (
        ("write",(("write",0,1),("halt",))),
        ("origin",(("move",0,-1),("halt",))),
        ("frontier",(("move",0,1),("move",0,1),("halt",)))):
        header=S.Tape();load(header,[0],M)
        try:M.execute_table(table,(),(header,))
        except ValueError as e:controls[name]=str(e)
        else:raise ValueError("unconfined binary context accepted")
    return dict(runtime_branch_cases=len(cases),rejected=controls)


def prospective_extents(code,g,bank_count,width,records,depth,private_entry):
    """Predict every backing coordinate from source/shape, before execution."""
    @lru_cache(None)
    def payloads(rows,d,dirty):
        L=6*rows*(width+1)
        current=[L]*g+list(dirty)+[d]
        peak=list(current)
        child=payloads(rows//g,d-1,(0,)*(bank_count-g)) if d else None
        for e in code:
            if e.op=="INIT":
                i=e.ports[0];current[i]=L;peak[i]=max(peak[i],L)
            elif e.op=="CLEAR":current[e.ports[0]]=0
            elif e.op=="PAID" and d:
                need(rows%g==0,"prospective complete-row division")
                for i in range(bank_count+1):peak[i]=max(peak[i],current[i]+1+child[i])
        return tuple(peak)
    b=max(1,(len(code)-1).bit_length());q=bank_count+1
    E=payloads(records,depth,tuple(private_entry));frame=2*q+b+3
    return E+(depth*frame,b if depth else 0,6*records*(width+1) if depth else 0,max(0,depth-1))


def fixture(unit,M,S,width=7,records=1,depth=0,prefix=0,warm=0,cycles=1):
    class VisitedTape(S.Tape):
        """Observer only: retain every visited frontier, not just written cells."""
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs);self.maximum=self.head
        def read(self):
            result=super().read();self.maximum=max(self.maximum,self.head);return result
        def write(self,value):
            super().write(value);self.maximum=max(self.maximum,self.head)
        def move(self,direction):
            super().move(direction);self.maximum=max(self.maximum,self.head)
        def retained(self):
            return max(len(self.cells),self.maximum+1)
    code,services=program(unit,M)
    g=len(unit.roles);bank_count=g+len(unit.owned)
    need([name for name,_ in unit.roles]==list(range(g)),"fixture numbered public slots")
    need(tuple(unit.owned)==tuple(range(g,bank_count)),"fixture numbered private slots")
    need(records%(g**depth)==0,"fixture shrinking row divisibility")
    counts=S.Counts()
    payloads=[VisitedTape([i&1]*prefix,counts=counts) for i in range(bank_count+1)]
    control=VisitedTape([0]*prefix,marker=S.BASE,counts=counts)
    descriptor,bridge,header=[VisitedTape([0]*prefix,marker=S.BASE,counts=counts) for _ in range(3)]
    all_tapes=payloads+[control,descriptor,bridge,header]
    expected=[[(-2 if (i+j)%3==0 else 2+(i+j)%3) for j in range(2*records)] for i in range(g)]
    for tape,values in zip(payloads,expected):load(tape,encode(values,width),M)
    for i in range(g,bank_count):load(payloads[i],[1,0,0]*(i%7+1),M)
    load(payloads[-1],[1]*depth,M)
    for tape in all_tapes:tape.cells.extend([S.BLANK]*warm)
    entry=[(id(t),list(t.cells[:prefix]),len(t.cells),t.retained()) for t in all_tapes]
    predicted=prospective_extents(code,g,bank_count,width,records,depth,
                                 tuple(3*(i%7+1) for i in range(g,bank_count)))
    expected_capacities=[max(item[2],prefix+1+extent) for item,extent in zip(entry,predicted)]
    expected_visits=[max(item[3],prefix+2+extent) for item,extent in zip(entry,predicted)]
    rows=FixtureRows(M,payloads[-1],g)
    c=M.Controller(code,g,payloads,control,descriptor,bridge,header,rows,services,S.Stack,
                   protected_ports=(bank_count,))
    before=counts.total;capacities=[];dirty_clears=0;paid_private=0
    def observe(phase,pc,event):
        nonlocal dirty_clears,paid_private
        if phase=="before" and event.op=="CLEAR":
            values=decode(body(payloads[event.ports[0]]),width)
            dirty_clears+=int(any(values))
        if phase=="before" and event.op=="PAID" and event.ports[0]>=g:
            paid_private+=1
        if phase=="after" and event.op=="CLEAR":
            need(body(payloads[event.ports[0]])==[],"source CLEAR erases physical bytes immediately")
    for _ in range(cycles):
        expected=oracle(code,expected,bank_count,depth)
        c.run(observe)
        for tape,values in zip(payloads,expected):
            need(decode(body(tape),width)==values,"source-generated physical endpoint")
        need(all(body(t)==[] for t in payloads[g:bank_count]),"all private banks physically empty")
        need(body(payloads[-1])==[1]*depth,"complete parent descriptor restored")
        need(all(body(t,S.BASE)==[] for t in (control,descriptor,bridge,header)),"all control/bridge bodies retired")
        need(all(id(t)==e[0] and t.cells[:prefix]==e[1] for t,e in zip(all_tapes,entry)),"fixed tapes and dirty ancestor prefixes")
        capacities.append(sum(len(t.cells) for t in all_tapes))
        need([len(t.cells) for t in all_tapes]==expected_capacities,
             "complete coordinatewise prospective retained backing")
        need([t.retained() for t in all_tapes]==expected_visits,
             "all visited frontier cells enter coordinatewise retained backing")
    need(len(set(capacities))==1,"sibling invocations reuse retained suffix backing")
    return dict(public=g,owned=bank_count-g,events=len(code),records=records,width=width,
                depth=depth,prefix=prefix,warm=warm,cycles=cycles,actions=counts.total-before,
                retained=sum(len(t.cells) for t in all_tapes),entry_retained=sum(e[2] for e in entry),
                retained_including_visited=sum(t.retained() for t in all_tapes),
                entry_including_visited=sum(e[3] for e in entry),
                dirty_clears=dirty_clears,paid_private=paid_private,tapes=len(all_tapes))


def boundary_checks(M,S):
    cases=[]
    for width,records,depth in ((3,2,1),(5,4,2),(9,6,3)):
        for prefix in (0,17,257):
            counts=S.Counts();payloads=[S.Tape([1]*prefix,counts=counts) for _ in range(5)]
            control,descriptor,bridge,header=[S.Tape([0]*prefix,marker=S.BASE,counts=counts) for _ in range(4)]
            for i in range(4):load(payloads[i],encode([(-1 if i%2 else 2)]*(2*records),width),M)
            load(payloads[4],[1]*depth,M)
            code=(M.Instruction("PAID",(2,),("owned",)),M.Instruction("PAID",(1,),("public",)),M.Instruction("RET"))
            rows=FixtureRows(M,payloads[4],2)
            c=M.Controller(code,2,payloads,control,descriptor,bridge,header,rows,{},S.Stack,protected_ports=(4,))
            parent=[(list(t.cells),t.head) for t in payloads]
            parent_total=sum(len(body(t)) for t in payloads)
            Lin=len(body(payloads[2]));row_actions=[0]
            for name in ("prepare","install","collect"):
                method=getattr(rows,name)
                def counted(*args,method=method):
                    start=counts.total;result=method(*args);row_actions[0]+=counts.total-start;return result
                setattr(rows,name,counted)
            start=counts.total;c.descend(0);descent=counts.total-start
            load(payloads[2],[1,0,0]*23,M);load(payloads[3],[0,1,1]*7,M)
            for t in payloads[:2]:M.CodedPort(t).write(1)
            child_total=sum(len(body(t)) for t in payloads)
            Lout=sum(len(body(t)) for t in payloads[:2])
            start=counts.total;pc=c.ascend();ascent=counts.total-start
            measured=descent+ascent-row_actions[0]
            expected=M.boundary_actions(5,c.pc_bits,parent_total,child_total,Lin,Lout,depth-1)
            need(measured==expected,"complete exact call boundary invoice")
            need(pc==1,"literal saved PC")
            for i in (0,1,3,4):
                old,head=parent[i]
                need(payloads[i].cells[:len(old)]==old and payloads[i].head==head,"all nonowner parent words and heads")
            need(len(body(payloads[2]))==Lin and body(bridge,S.BASE)==[],"complete occupied owner installation")
            cases.append(dict(width=width,records=records,depth=depth,prefix=prefix,
                              administrative_actions=measured,row_actions=row_actions[0]))
    return cases


def rejection_controls(M,S,IR,source,word,seed,compiled):
    from types import SimpleNamespace
    out={}
    def reject(name,call):
        try:call()
        except (ValueError,AssertionError) as e:out[name]=str(e)
        else:raise ValueError("control was accepted: "+name)
    for name,op,mutate in (
        ("borrowed_clear","CLEAR",lambda e:e.__setitem__(1,0)),
        ("wrong_copy_coefficient","COPY",lambda e:e.__setitem__(3,"2")),
        ("integer_private_flag","MOVE",lambda e:e.__setitem__(4,int(e[4])))):
        bad=deepcopy(word);mutate(next(e for e in bad["program"] if e[0]==op))
        reject(name,lambda bad=bad:IR.current_local(bad))
    bad=deepcopy(word);bad["program"].remove(next(e for e in bad["program"] if e[0]=="INIT"))
    reject("missing_current_init",lambda:IR.current_local(bad))
    bad_events=list(seed.events);at=next(i for i,e in enumerate(bad_events) if e.op=="PAID")
    bad_events.insert(at,IR.Event("CLEAR",bad_events[at].fields))
    reject("early_parent_clear",lambda:IR.Unit("bad",seed.roles,seed.owned,tuple(bad_events)).check())
    class DepthBanks(source.Compiler):
        def alloc_bank(self,g,oname,frame,d):
            super().alloc_bank(g,oname,frame,d)
            return ("bad-depth",d,oname)
    reject("one_bank_per_depth",lambda:IR.lower(seed,15,SimpleNamespace(Rule=source.Rule,Compiler=DepthBanks)))
    nested,_,_=IR.lower(seed,15,source)
    for prefix in ("occurrence","program","base-axis"):
        events=list(nested.events)
        at=next(i for i,e in enumerate(events) if e.token and e.token[0]==prefix+"-return")
        del events[at]
        broken=IR.Unit("missing return",nested.roles,nested.owned,tuple(events))
        reject("missing_"+prefix+"_return",lambda broken=broken:IR.check_flat_ownership(broken))
    # A supplied native table may never cross the physical current delimiter.
    tape=S.Tape([1]*17);load(tape,encode([2],4),M)
    reject("native_ancestor_probe",lambda:M.execute_table((("move",0,-1),("halt",)),(tape,)))
    need(tape.cells[:17]==[1]*17,"rejected probe preserved ancestor bytes")
    # Both counterfactual COPY and zero-valued CLEAR have observable failures.
    src,dst=S.Tape(),S.Tape();load(src,encode([3],5),M);load(dst,encode([2],5),M)
    M.retire(dst);M.transfer(src,dst)
    reject("copy_overwrite_loses_residue",lambda:need(decode(body(dst),5)==[5],"actual residue must be added"))
    M.initialize(dst,src)
    reject("numerical_zero_is_not_erasure",lambda:need(body(dst)==[],"zero format still occupies coded cells"))
    # Pop-before-output and a wrong valid continuation are real controller mutations.
    Original=M.Controller
    class LoseOutput(Original):
        def ascend(self):
            for t in self.payloads:M.retire(t)
            return super().ascend()
    try:
        M.Controller=LoseOutput
        reject("pop_before_output_copy",lambda:fixture(compiled,M,S,records=2,depth=1))
    finally:M.Controller=Original
    class WrongPC(Original):
        def consume_pc(self):
            super().consume_pc()
            return 2
    try:
        M.Controller=WrongPC
        reject("wrong_return_pc",lambda:boundary_checks(M,S))
    finally:M.Controller=Original
    # Internal virtual blank is data, and must survive a binary transfer.
    tape,copy=S.Tape(),S.Tape();port=M.CodedPort(tape)
    for symbol in (1,4,0,3):port.write(symbol);port.move(1)
    M.origin(tape);M.transfer(tape,copy)
    need(body(copy)==[0,0,1,1,0,0,0,0,0,0,1,1],"coded internal logical blank survives")
    # A collapsed blank cuts the byte extent and loses a later live suffix.
    malformed=S.Tape();load(malformed,[0,0,1],M)
    malformed.cells.extend([6,0,0,0,1,1])
    short=S.Tape();M.transfer(malformed,short)
    reject("logical_blank_collapsed_to_physical_blank",
           lambda:need(body(short)==body(copy),"physical blank incorrectly truncated live suffix"))
    return out
