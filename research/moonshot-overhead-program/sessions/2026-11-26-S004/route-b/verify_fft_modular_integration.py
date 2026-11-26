#!/usr/bin/env python3
"""Integrate the actual dyadic supplier and triadic modular engine."""
from pathlib import Path
from random import Random
import hashlib
import json
import verify_certified_fft_supplier as supplier
import verify_bounded_amplitude as modular

def evaluate(coefficients,radix):
    z=0
    for x in reversed(coefficients):
        z=z*radix+x
    return z

def main():
    rng=Random(2026112613)
    cases=0
    coefficients=0
    for h in (3,8,17):
        for bits in (3,7):
            for budget in (1,4,7):
                a=[rng.randrange(1<<bits) for _ in range(h)]
                b=[rng.randrange(1<<bits) for _ in range(h)]
                candidate,_=supplier.supplier(a,b,bits,budget)
                modulus=1<<budget
                product_residue=modular.convolution_mod(a,b,modulus)+[0]
                correction=[(x-y)%modulus for x,y in zip(product_residue,candidate)]
                corrected=[x+y for x,y in zip(candidate,correction)]
                assert corrected==supplier.ordinary(a,b)
                assert sum(correction)==sum(a)*sum(b)-sum(candidate)
                assert evaluate(corrected,1<<bits)==evaluate(a,1<<bits)*evaluate(b,1<<bits)
                cases+=1
                coefficients+=2*h
    maximum_cases=0
    for h in (1,3,8,17):
        for bits in (1,7):
            n=4
            while n<2*h:
                n*=2
            ell=n.bit_length()-1
            for budget in (1,2*bits+ell):
                a=b=[(1<<bits)-1]*h
                candidate,_=supplier.supplier(a,b,bits,budget)
                modulus=1<<budget
                product_residue=modular.convolution_mod(a,b,modulus)+[0]
                correction=[(x-y)%modulus for x,y in zip(product_residue,candidate)]
                corrected=[x+y for x,y in zip(candidate,correction)]
                assert corrected==supplier.ordinary(a,b)
                assert sum(correction)==sum(a)*sum(b)-sum(candidate)
                assert evaluate(corrected,1<<bits)==evaluate(a,1<<bits)*evaluate(b,1<<bits)
                cases+=1
                coefficients+=2*h
                maximum_cases+=1
    names=('verify_certified_fft_supplier.py','verify_bounded_amplitude.py')
    hashes={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in names}
    result={'status':'all exact integration controls passed','seed':2026112613,
            'complete_supplier_triadic_repair_cases':cases,'corrected_coefficients':coefficients,
            'all_maximum_digit_controls':maximum_cases,
            'dependency_sha256':hashes,
            'scope':'both actual finite arithmetic engines, exact mass and base-2^b carry identity'}
    Path(__file__).with_name('fft-modular-integration-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':
    main()
