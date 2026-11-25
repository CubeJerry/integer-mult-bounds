#!/usr/bin/env python3
from pathlib import Path
import json
import random


def pack_passes(data,prefix,h,omega):
    assert h>0 and h&(h-1)==0 and len(data)==prefix*h*omega
    out=list(data); bits=h.bit_length()-1
    for i in range(bits-1,-1,-1):
        pre=prefix*(1<<i); suffix=1<<(bits-i-1)
        nxt=[]
        for p in range(pre):
            for w in range(omega):
                for b in range(2):
                    pos=((p*2+b)*omega+w)*suffix
                    nxt.extend(out[pos:pos+suffix])
        out=nxt
    return out


def unpack(data,prefix,h,omega):
    return [data[(p*omega+w)*h+c] for p in range(prefix) for c in range(h) for w in range(omega)]


def swap_packed(data,prefix,h,q):
    return [data[(p*q*q+y*q+x)*h+c] for p in range(prefix) for x in range(q) for y in range(q) for c in range(h)]


def swap_binary(data,prefix,h,q):
    return [data[(p*h+c)*q*q+y*q+x] for p in range(prefix) for c in range(h) for x in range(q) for y in range(q)]

rng=random.Random(2673)
positions=cases=independent_inputs=negative=0
for prefix,h,q in [(1,2,3),(2,4,3),(3,8,3),(2,16,9)]:
    omega=q*q; n=prefix*h*omega
    labels=list(range(n))
    packed=pack_passes(labels,prefix,h,omega)
    direct=[labels[(p*h+c)*omega+w] for p in range(prefix) for w in range(omega) for c in range(h)]
    assert packed==direct and unpack(packed,prefix,h,omega)==labels
    positions+=n; cases+=1
    values=[]
    if n<=20:
        for i in range(n): values.append([int(j==i) for j in range(n)])
    values.extend([[rng.randrange(2) for _ in range(n)] for _ in range(12)])
    for bits in values:
        transported=swap_packed(pack_passes(bits,prefix,h,omega),prefix,h,q)
        got=unpack(transported,prefix,h,omega)
        assert got==swap_binary(bits,prefix,h,q)
        independent_inputs+=1
        wrong=[transported[(p*omega+w)*h+(h-1-c)] for p in range(prefix) for c in range(h) for w in range(omega)]
        negative+=wrong!=got
assert negative>0
out={'status':'passed','packing_shapes':cases,'exact_moved_positions':positions,
     'full_independent_binary_inputs':independent_inputs,'wrong_unpacked_basis_negative_controls':negative,
     'scope':'Actual short-coordinate digit-pass permutation, inverse and complete spatial swap on independent bits. Does not execute the full scalar template or adaptive tape machine.'}
Path(__file__).with_name('field-packing-verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
