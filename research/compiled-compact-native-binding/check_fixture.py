"""Independent record-address oracle and literal coded source execution."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from types import SimpleNamespace
from time import monotonic
from provider import Provider,SCHEMA
from codec import DenseTape,A,need
from ordinary import Ordinary
from macro_code import Code
from source_binding import Service,fixture_events

def factory(q=2):
    return Ordinary(q,SimpleNamespace(codes=SimpleNamespace(q=q)),SimpleNamespace(families=0),
                    (Code((('unreachable',),),0),),capacity=64)

def coded(symbols):return [((v>>k)&1) for v in symbols for k in (2,1,0)]

def load(tape,bits):
    start=tape.origin
    tape.cells[start:]=bytearray(bits)
    tape.head=start;tape.high=start+len(bits)

def body(tape):
    out=[]
    for value in tape.cells[tape.origin:]:
        if value==6:break
        out.append(value)
    return out

def header_bits(values):
    out=[]
    for name in SCHEMA:
        n=values[name];digits=[int(x) for x in bin(n)[2:][::-1]]
        out += [1]*len(digits)+[0]+digits
    return out

def fixture(f=1,K=1,H=1,rows=1,outer=1,late=False,rank=2,source=0,target=1,rho=0,
            component_width=None):
    source,target=(target,source) if late else (source,target)
    e=rank*f;a=3*H+e*K;back=2*H+e*K
    minimum=max(1,((outer*rows*(1<<a)-1).bit_length()+1)//2)
    w=minimum if component_width is None else component_width
    need(type(w) is int and w>=minimum,'distinct complete fixture record labels')
    b=6*(w+1)
    values=dict(outer=outer,rows=rows,stock=1,row_bits=(1<<a)*b,within_bits=a,
                record_bits=b,p=max(e,2),d=e,K=K,G=1,H=H,q0=3,qF=0,qB=0,D=e,
                f=f,rho=rho,active_start=2*H,back_start=back,selected_axes=e,
                entry_start=2*H,remainder=0,cutoff=rank)
    records=[]
    for label in range(outer*rows*(1<<a)):
        symbols=[]
        for part in (label&((1<<w)-1),label>>w):
            symbols += [(part>>i)&1 for i in range(w)]+[2]
        records.append(coded(symbols))
    expected=[None]*len(records)
    for row in range(outer*rows):
        for address in range(1<<a):
            destination=address
            for j in range(f):
                spos=2*H+(source*f+j)*K+rho
                tpos=2*H+(target*f+j)*K+rho
                if (address>>(a-1-spos))&1:destination ^= 1<<(a-1-tpos)
            expected[row*(1<<a)+destination]=records[row*(1<<a)+address]
    return values,[v for rec in records for v in rec],[v for rec in expected for v in rec],source,target

def run_case(mutate=None,reuse=None,return_state=False,**case):
    values,initial,expected,source,target=fixture(**case)
    source_events,source_report=fixture_events()
    event=next(e for e in source_events if e.token[3:5]==(source,target))
    if reuse is None:
        service=Service(event,case.get('rank',2),factory)
        p=service.provider
        work=[DenseTape(3+i%5) for i in range(p.port_count)]
        field,context=DenseTape(9),DenseTape(11)
    else:
        service,p,work,field,context=reuse
        need(service.token==event.token,'reused fixed source service')
    for tape in (*work,field,context):
        for i in range(tape.origin-1):tape.cells[i]=i%2
    load(field,initial);hb=header_bits(values);load(context,hb)
    ancestors=[bytes(t.cells[:t.origin]) for t in (*work,field,context)]
    if mutate is not None:mutate(p)
    if reuse is None:
        service.bind(work,{service.owner:A.CodedPort(field)},A.BinaryContextPort(context))
    before_actions=sum(t.actions() for t in (*work,field,context))
    before_calls=dict(p.engine.calls)
    start=monotonic();service.run()
    need(body(field)==expected,'independent complete record-address endpoint')
    need(body(context)==hb,'protected exact descriptor')
    need(all(t.head==t.origin and all(v==6 for v in t.cells[t.origin:]) for t in work),
         'all native work physically blank at current origins')
    need(field.head==field.origin and context.head==context.origin,'declared public/context heads')
    need(all(bytes(t.cells[:t.origin])==before for t,before in zip((*work,field,context),ancestors)),
         'current-segment isolation from ancestors')
    report=dict(case=case,bits=len(initial),records=values['outer']*values['rows']*(1<<values['within_bits']),
                source_token=service.token,source_record=service.record,source_report=source_report,
                native_ports=p.port_count,native_calls={k:v-before_calls[k] for k,v in p.engine.calls.items()},
                physical_actions=sum(t.actions() for t in (*work,field,context))-before_actions,
                retained_cells=sum(len(t.cells) for t in work),seconds=round(monotonic()-start,6))
    return (report,(service,p,work,field,context)) if return_state else report

if __name__=='__main__':
    import json
    which=sys.argv[1] if len(sys.argv)>1 else 'single'
    case=({'f':1,'K':2,'H':1,'rho':0,'rows':1} if which=='single' else
          {'f':2,'K':1,'H':1,'late':which=='late'})
    print(json.dumps(run_case(**case),sort_keys=True))
