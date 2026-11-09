"""Adverse controls specific to the new encoding, ownership and binding join."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from types import SimpleNamespace,MethodType
from codec import (S,A,SymbolPort,DenseTape,ParkingAdapter,execution,need)
from check_fixture import run_case,factory
from source_binding import Service,fixture_events

def rejects(call,label):
    try:call()
    except ValueError:return label
    raise ValueError('adverse control accepted: '+label)

def alphabet():
    p=DenseTape(7);port=SymbolPort(p);port.initialize()
    for value in range(14):
        port.write(value);need(port.read()==value,'exact native symbol encoding');port.step(1)
    for _ in range(14):port.step(-1)
    for value in range(14):
        need(port.read()==value,'native alphabet independent round trip');port.step(1)
    negative=[rejects(lambda:port.write(14),'unused_native_code_rejected')]
    A.retire(p);need(p.head==p.origin and all(x==6 for x in p.cells[p.origin:]),'encoded symbols physically erased')
    bad=DenseTape(3);q=SymbolPort(bad);q.initialize()
    bad.cells[bad.head:bad.head+3]=bytes([1,1,1])
    negative.append(rejects(q.read,'unused_A_code_rejected'))
    return dict(symbols=14,actions=p.actions(),rejections=negative)

def parking():
    from parking_machine import Machine
    raw=(DenseTape(5),DenseTape(8));ports=tuple(SymbolPort(p) for p in raw)
    owner=SimpleNamespace(machine=Machine(),codec_counts=dict(reads=0,writes=0,moves=0,slot_tests=0,commands=0))
    adapter=ParkingAdapter(owner,ports);adapter.initialize()
    owner._move(1,-1);owner._write(1,'^');owner._move(1,1)
    need(owner.machine.tapes==[{}, {0:'^'}],'initial local parking baseline')
    owner._command('begin')
    need(not(owner.machine.tapes[0]=={}),'nonempty stack at blank top is rejected')
    data='10110'
    for value in data+'$':owner._write(1,value);owner._move(1,1)
    owner._move(1,-1)
    while owner._read(1)!='^':owner._move(1,-1)
    owner._move(1,1);owner._command('push')
    need(not(owner.machine.tapes[0]=={}),'pushed nonempty stack at blank top is rejected')
    owner._command('pop')
    observed=''
    while owner._read(1)!='$':
        observed+=owner._read(1);owner._write(1,'_');owner._move(1,1)
    need(observed==data,'actual unchanged parking table restores all bits')
    owner._write(1,'_');owner._move(1,-1)
    while owner._read(1)!='^':owner._move(1,-1)
    owner._move(1,1);owner._command('end')
    need(owner.machine.tapes==[{}, {0:'^'}],'matched complete parking baseline')
    owner._write(1,'1')
    need(not(owner.machine.tapes[1]=={0:'^'}),'dirty packet baseline rejected')
    owner._write(1,'_');owner._move(1,1)
    need(not(owner.machine.tapes[1]=={0:'^'}),'wrong packet head rejected')
    owner._move(1,-1)
    for tape in raw:A.retire(tape)
    return dict(payload=data,actions=sum(t.actions() for t in raw),
                controls=['nonempty_begin_top','nonempty_pushed_top','dirty_packet','wrong_packet_head'])

def mutations():
    def wrong_rho(p):
        original=p.prepare
        def bad(header,cleanup):
            widths,n,rho,record,rows=original(header,cleanup)
            return widths,n,header['rho'],record,rows
        p.prepare=bad
    def dirty_return(p):p.cohort.finish=lambda:None
    reports=[rejects(lambda:run_case(mutate=wrong_rho,f=1,K=2,H=1,rho=0),
                     'unconverted_rho_fails_actual_endpoint'),
             rejects(lambda:run_case(mutate=dirty_return,f=1,K=1,H=1),
                     'omitted_raw_cleanup_fails_actual_work_return')]
    event=fixture_events()[0][0];service=Service(event,2,factory)
    reports.append(rejects(lambda:service.bind([],{},None),'wrong_compiled_owner_rejected'))
    # Inspection of retained host arrays is not a permitted physical primitive.
    tape=service.provider.cohort.tapes[0]
    with execution():reports.append(rejects(lambda:tape.cells,'runtime_host_backing_access_rejected'))
    return reports

def reuse():
    small=dict(f=1,K=1,H=1,rows=1,outer=1,component_width=4)
    large=dict(f=1,K=1,H=1,rows=3,outer=2,component_width=4)
    fresh=run_case(**small)
    bigger,state=run_case(return_state=True,**large)
    after=run_case(reuse=state,**small)
    need(after['physical_actions']==fresh['physical_actions'],'no historical backing scan in smaller call')
    need(after['retained_cells']==bigger['retained_cells']>fresh['retained_cells'],
         'retained backing remains larger while current work is unchanged')
    return dict(fresh_small=fresh,large=bigger,reused_small=after)

def run():return dict(alphabet=alphabet(),parking=parking(),mutations=mutations(),reuse=reuse())

if __name__=='__main__':
    import json
    print(json.dumps(run(),sort_keys=True))
