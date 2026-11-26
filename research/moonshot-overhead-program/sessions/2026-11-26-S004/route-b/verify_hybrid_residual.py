#!/usr/bin/env python3
"""Exact mixed-residual controls using the independently checked engines."""
from pathlib import Path
from random import Random
import hashlib
import json
import verify_bounded_amplitude as amplitude
import verify_sparse_residual as sparse
import verify_one_sided_certificate as positive

COUNTS = {}

def count(name, n=1):
    COUNTS[name] = COUNTS.get(name, 0)+n

def centered(values, modulus):
    return [x if 2*x < modulus else x-modulus for x in values]

def small_residue(a, b, candidate, modulus, signed):
    product_residue = amplitude.convolution_mod(a, b, modulus)+[0]
    residue = [(x-y) % modulus for x, y in zip(product_residue, candidate)]
    return centered(residue, modulus) if signed else residue

def main():
    rng = Random(2026112610)
    for h, bits, budget in ((2, 2, 1), (5, 3, 1), (6, 4, 2), (9, 3, 2)):
        for modulus in (8, 16):
            for _ in range(3):
                a = [rng.randrange(1 << bits) for _ in range(h)]
                b = [rng.randrange(1 << bits) for _ in range(h)]
                truth = amplitude.ordinary(a, b)+[0]
                small = [rng.randrange(-modulus//2+1, modulus//2) for _ in truth]
                large = [0]*len(truth)
                for i in rng.sample(range(len(truth)), budget):
                    large[i] = modulus*rng.choice((-7, -2, 1, 5))
                error = [x+y for x, y in zip(small, large)]
                candidate = [x-y for x, y in zip(truth, error)]
                residue = small_residue(a, b, candidate, modulus, True)
                assert residue == small
                adjusted = [x+y for x, y in zip(candidate, residue)]
                recovered, _ = sparse.recover_core(a, b, adjusted, bits, budget)
                assert recovered == {i:x for i,x in enumerate(large) if x}
                actual = [x+recovered.get(i,0) for i,x in enumerate(adjusted)]
                assert actual == truth
                emax = h*(1 << (2*bits))+max(abs(x) for x in candidate)
                assert max(abs(x) for x in adjusted) <= max(abs(x) for x in candidate)+modulus//2
                assert max(abs(x) for x in large) <= emax+modulus//2
                assert sparse.ev(actual, 1 << bits) == sparse.ev(a,1 << bits)*sparse.ev(b,1 << bits)
                count('signed_complete_mixed_repairs')
                count('signed_height_and_carry_controls')

    # Both half-modulus endpoints are outliers under the sufficient promise;
    # only the positive endpoint needs an actual nonzero sparse correction.
    modulus, h, bits = 8, 3, 2
    a, b = [1,2,3], [3,0,1]
    truth = amplitude.ordinary(a,b)+[0]
    error = [4,-4,1,-2,0,3]
    candidate = [x-y for x,y in zip(truth,error)]
    residue = small_residue(a,b,candidate,modulus,True)
    assert residue == [-4,-4,1,-2,0,3]
    adjusted = [x+y for x,y in zip(candidate,residue)]
    recovered,_ = sparse.recover_core(a,b,adjusted,bits,2)
    assert recovered == {0:8}
    count('centered_endpoint_control')

    for h, bits, budget, actual_count in ((3,2,1,1),(6,3,1,8),(8,3,2,2),(8,4,2,10)):
        for modulus in (4,16):
            for _ in range(3):
                a = [rng.randrange(1 << bits) for _ in range(h)]
                b = [rng.randrange(1 << bits) for _ in range(h)]
                truth = amplitude.ordinary(a,b)+[0]
                low = [rng.randrange(modulus) for _ in truth]
                high = [0]*len(truth)
                for i in rng.sample(range(len(truth)),actual_count):
                    high[i] = modulus*rng.randrange(1,7)
                error = [x+y for x,y in zip(low,high)]
                candidate = [x-y for x,y in zip(truth,error)]
                residue = small_residue(a,b,candidate,modulus,False)
                assert residue == low
                adjusted = [x+y for x,y in zip(candidate,residue)]
                assert all(x<=y for x,y in zip(adjusted,truth))
                recovered,accepted,_ = positive.core(a,b,adjusted,bits,budget)
                assert all(high[i]==v for i,v in recovered.items())
                if accepted:
                    assert [x+recovered.get(i,0) for i,x in enumerate(adjusted)] == truth
                if actual_count <= budget:
                    assert accepted
                count('one_sided_complete_or_incomplete_mixed_attempts')
                count('one_sided_accepted' if accepted else 'one_sided_incomplete')
                if actual_count>budget:
                    count('one_sided_false_outlier_guesses')

    # Dense positive errors with a false budget cannot pass the certificate.
    a=b=[0]*6
    modulus=8
    error=[16+i%8 for i in range(12)]
    candidate=[-x for x in error]
    residue=small_residue(a,b,candidate,modulus,False)
    adjusted=[x+y for x,y in zip(candidate,residue)]
    _,accepted,_=positive.core(a,b,adjusted,1,1)
    assert not accepted
    count('dense_positive_false_budget_rejected')

    # Zero-outlier positive mass test has both accepting and rejecting cases.
    for error in ([0,1,2,7], [0,1,8,7]):
        residues=[x%8 for x in error]
        assert (sum(error)==sum(residues)) == all(x<8 for x in error)
        count('zero_outlier_mass_controls')

    # Dropping the signed support promise remains unsound after stage one.
    # With D=512 and S=1, the prescribed family is ell=1,...,22.
    h,bits,budget,modulus=256,1,1,8
    cap=2*(2*h-1).bit_length()+4
    assert cap==22
    annihilator=[1]
    for ell in range(1,cap+1):
        annihilator=amplitude.ordinary(annihilator,[-1]+[0]*(ell-1)+[1])
    error=[modulus*x for x in amplitude.ordinary(annihilator,annihilator)]
    error += [0]*(2*h-len(error))
    assert len(error)==2*h and sum(x!=0 for x in error)>budget
    assert all(x%modulus==0 for x in error)
    recovered,_=sparse.recover_core([0]*h,[0]*h,[-x for x in error],bits,budget)
    assert recovered=={} and any(error)
    count('signed_missing_promise_false_certificate_control')

    files=('verify_bounded_amplitude.py','verify_sparse_residual.py','verify_one_sided_certificate.py')
    hashes={name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest() for name in files}
    result={'status':'all exact finite controls passed','seed':2026112610,
            'scope':'exact two-stage arithmetic and certificates; no tape timing simulation',
            'counts':COUNTS,'dependency_sha256':hashes}
    Path(__file__).with_name('hybrid-residual-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
