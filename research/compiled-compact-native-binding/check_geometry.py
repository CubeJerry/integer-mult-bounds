"""Encoded producer checked against independently calculated complete spans."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contextlib import ExitStack
from codec import A,DenseTape,execution,need
from provider import Provider,SCHEMA
from check_fixture import factory,header_bits,load

def inspect_count(value):
    # Outside execution(): checker observation only, never a machine operand.
    value.rewind();result=0;place=1
    while value.read()!=3:
        bit=value.read();need(bit in (0,1),'observer canonical Count')
        result+=place*bit;place*=2;value.step(1)
    value.rewind();return result

def input_case(rank,f,K,G,d,source,target,rho,rows,outer,leading=0,after=0,tail=0):
    H=d*G;active=2*H+leading;back=active+rank*f*K+after;a=back+H+tail;b=24
    values=dict(outer=outer,rows=rows,stock=1,row_bits=(1<<a)*b,within_bits=a,record_bits=b,
                p=max(a,d),d=d,K=K,G=G,H=H,q0=17,qF=1,qB=2,D=d,f=f,rho=rho,
                active_start=active,back_start=back,selected_axes=rank*f,
                entry_start=active,remainder=0,cutoff=rank)
    return values

def run_one(case,change=None):
    values=input_case(**case)
    if change:change(values)
    p=Provider(case['rank'],case['source'],case['target'],factory)
    work=[DenseTape(2+i%7) for i in range(p.port_count)];context=DenseTape(13)
    hb=header_bits(values);load(context,hb);p.bind(work);p.cohort.start()
    with p.scope.installed(),ExitStack() as cleanup:
        with execution():
            h=p.read_header(A.BinaryContextPort(context))
            for v in h.values():cleanup.callback(v.close)
            widths,n,rho,record,rows=p.prepare(h,cleanup)
        got=dict(widths=[inspect_count(v) for v in widths],n=inspect_count(n),rho=inspect_count(rho),
                 record=inspect_count(record),outer_rows=inspect_count(rows))
    p.pool.empty();p.cohort.finish()
    f,K,G,H=values['f'],values['K'],values['G'],values['H']
    compact=(f-1)*G;chunk=f*K
    first=values['active_start']+min(case['source'],case['target'])*chunk
    second=values['active_start']+max(case['source'],case['target'])*chunk
    suffix=values['within_bits']-values['back_start']-compact
    want=dict(widths=[compact,H-compact,compact,H-compact,first-2*H,chunk,
                      second-first-chunk,chunk,values['back_start']-second-chunk,compact],
              n=f-1,rho=K-1-values['rho'],record=values['record_bits']*(1<<suffix),
              outer_rows=values['outer']*values['rows'])
    need(got==want,'independent exact layout/fibre oracle')
    need(sum(got['widths'])+suffix==values['within_bits'],'no dropped complete-row bit')
    need((1<<sum(got['widths']))*got['record']==values['row_bits'],'complete row volume equality')
    for block in (case['source'],case['target']):
        left=values['active_start']+block*f*K
        native=[left+f*K-1-got['rho']-j*K for j in range(f)]
        current=[left+j*K+values['rho'] for j in range(f)]
        need(native==list(reversed(current)),'paired reverse-column selected coordinates')
    need(context.head==context.origin and list(context.cells[context.origin:])==hb,'raw header exact/origin')
    need(all(t.head==t.origin and all(x==6 for x in t.cells[t.origin:]) for t in work),'geometry work exact cleanup')
    return dict(case=case,encoded_header_bits=len(hb),result=got)

def run():
    cases=[dict(rank=2,f=3,K=3,G=1,d=7,source=0,target=1,rho=1,rows=5,outer=7,leading=2,after=1,tail=3),
           dict(rank=3,f=2,K=5,G=2,d=6,source=2,target=0,rho=4,rows=11,outer=3,leading=1,after=2,tail=1),
           dict(rank=5,f=1,K=2,G=3,d=5,source=4,target=1,rho=0,rows=3,outer=10**70+3)]
    positive=[run_one(case) for case in cases]
    negatives=[]
    for label,mutate in [('wrong_row_length',lambda h:h.update(row_bits=h['row_bits']+1)),
                         ('rho_outside_chunk',lambda h:h.update(rho=h['K'])),
                         ('lost_back_reservation',lambda h:h.update(within_bits=h['back_start'])),
                         ('wrong_ordinary_geometry',lambda h:h.update(selected_axes=h['selected_axes']+1))]:
        try:run_one(cases[0],mutate)
        except ValueError:negatives.append(label)
        else:raise ValueError('geometry mutation accepted: '+label)
    return dict(cases=positive,rejections=negatives)

if __name__=='__main__':
    import json
    print(json.dumps(run(),sort_keys=True))
