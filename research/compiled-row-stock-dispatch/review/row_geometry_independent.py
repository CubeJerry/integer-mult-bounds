"""Root review of encoded ordinary geometry using independent hardware/codec.

The subject is the finite table, not the author's interpreter or fixtures.
The earlier root review supplies only its separately written hardware/codec.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('root_row_hardware', HERE/'row_dispatch_independent.py')
h = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = h
spec.loader.exec_module(h)
r = h.r


def execute(table, values, result=False):
    ports = [h.Hardware(offset=5+i % 9) for i in range(r.FIRST_ROLE)]
    original = h.encode(values)
    ports[r.HEADER] = h.Hardware(original, offset=17)
    pc = 0
    decision = None
    for tick in range(20_000_000):
        instruction = table[pc]
        op = instruction[0]
        if op == 'done':
            break
        if op == 'result':
            decision = instruction[1]
            break
        if op in ('reject','quarantine'):
            raise ValueError('subject table rejected')
        if op == 'goto':
            pc = instruction[1]
        elif op == 'read':
            pc = instruction[2][ports[instruction[1]].read()]
        else:
            port = ports[instruction[1]]
            if op == 'write':
                port.write(instruction[2])
            elif op == 'move':
                port.move(instruction[2])
            else:
                raise ValueError('unknown subject opcode')
            pc += 1
    else:
        raise ValueError('bounded review did not finish')
    h.require(ports[r.HEADER].text() == original, 'borrowed parent preserved')
    for port in ports:
        port.check()
    kept = {r.HEADER} if result else {r.HEADER,r.CHILD_HEADER}
    h.require(all(not port.text() for i,port in enumerate(ports) if i not in kept),
              'all descriptor work retired')
    if result:
        h.require(type(decision) is bool, 'literal decision terminal')
        return decision,tick+1
    h.require(decision is None, 'ordinary header terminal')
    return h.decode(ports[r.CHILD_HEADER].text()),tick+1


def base(rank, extent, span, k, cutoff):
    values = {name:(i*11+3) % 29 for i,(name,_) in enumerate(r.SCHEMA)}
    values.update(rows=150,stock=150,outer=3,selected_axes=extent,
                  entry_start=span,active_start=0,remainder=0,f=0,K=k,
                  cutoff=cutoff,within_bits=9,record_bits=6,row_bits=1)
    return values


def reject(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError('invalid ordinary boundary accepted')


def main():
    roots=children=leaves=negative=0
    longest=0
    histories=[]
    # Full paths with nonzero remainders at different levels. Geometry is
    # checked without materializing an exponentially large numerical packet.
    for rank,extent,k,cutoff in ((2,127,1,2),(3,251,5,4),(5,877,7,7),(7,1429,3,8)):
        current=base(rank,extent,13,k,cutoff)
        table=r.compile_prepare(5,rank=rank,root=True)
        got,ticks=execute(table,current)
        expected=dict(current,rows=30,stock=30,row_bits=6*(2**9),
                      f=extent//rank,remainder=extent%rank,
                      active_start=13+(extent%rank)*k)
        h.require(got==expected,'root complete e=Nf+r descriptor')
        roots+=1;longest=max(longest,ticks)
        path=[got['selected_axes']]
        current=got
        # Replenish only row stock for the isolated geometry tests; source
        # row-only review separately tests actual conserved nested stock.
        while current['f']>cutoff:
            current=dict(current,rows=150,stock=150)
            got,ticks=execute(r.compile_prepare(5,rank=rank),current)
            e=current['f'];begin=current['active_start']
            expected=dict(current,rows=30,stock=30,selected_axes=e,
                          f=e//rank,remainder=e%rank,entry_start=begin,
                          active_start=begin+(e%rank)*k)
            h.require(got==expected,'child requested width and placement')
            h.require(got['active_start']+rank*got['f']*k==begin+e*k,
                      'remainder and full blocks partition exactly the request')
            children+=1;longest=max(longest,ticks)
            path.append(e);current=got
        decision,ticks=execute(r.compile_leaf(rank),current,result=True)
        h.require(decision,'terminal path reaches exact f cutoff')
        leaves+=1;longest=max(longest,ticks);histories.append(path)
    # Descriptors can be large without decoding into runtime host integers.
    for rank in (2,3,5,11):
        for requested in (rank+1,rank**3-1,10**70+rank**2+1):
            current=base(rank,rank*requested+1,29,2**83+7,rank)
            current.update(f=requested,active_start=2**91+31,remainder=1)
            got,ticks=execute(r.compile_prepare(3,rank=rank),current)
            expected=dict(current,rows=50,stock=50,selected_axes=requested,
                          f=requested//rank,remainder=requested%rank,
                          entry_start=current['active_start'],
                          active_start=current['active_start']+(requested%rank)*current['K'])
            h.require(got==expected,'large encoded geometry exact')
            children+=1;longest=max(longest,ticks)
        for cutoff in (rank,rank+1,2**37+9):
            for f in sorted({1,cutoff-1,cutoff,cutoff+1,cutoff*2+1}):
                current=base(rank,3*f+1,7,3,cutoff);current['f']=f
                decision,ticks=execute(r.compile_leaf(rank),current,result=True)
                h.require(decision==(f<=cutoff),'inclusive source stopping boundary')
                leaves+=1;longest=max(longest,ticks)
        current=base(rank,rank*rank+1,5,7,rank);current['f']=rank
        reject(lambda:execute(r.compile_prepare(3,rank=rank),current));negative+=1
        bad=dict(current,cutoff=rank-1)
        reject(lambda:execute(r.compile_leaf(rank),bad,result=True));negative+=1
    report=dict(status='PASS_ROOT_INDEPENDENT_ORDINARY_GEOMETRY',root_cases=roots,
                child_cases=children,leaf_cases=leaves,rejections=negative,
                paths=histories,maximum_table_steps=longest,
                source_sha256=hashlib.sha256(h.SOURCE.read_bytes()).hexdigest(),
                scope='encoded descriptor and cutoff tables; numerical bodies excluded')
    print(json.dumps(report,sort_keys=True))


if __name__=='__main__':
    main()
