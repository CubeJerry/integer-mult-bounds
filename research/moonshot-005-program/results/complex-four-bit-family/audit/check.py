#!/usr/bin/env python3
"""Exact trace certificate, finite counterfamily and source-scope audit controls."""
from pathlib import Path
import argparse, hashlib, importlib.util, itertools, json, random, sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, default=Path.cwd())
args = ap.parse_args()
base = Path(__file__).parent
hp = args.repo / 'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
assert hashlib.sha256(hp.read_bytes()).hexdigest() == '1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
sp = importlib.util.spec_from_file_location('four_bit_audit_exact', hp)
m = importlib.util.module_from_spec(sp)
sys.modules[sp.name] = m
sp.loader.exec_module(m)
N = 16
I = m.eye(N)
Xb = m.monomial([x ^ 2 for x in range(N)], [0] * N)
Cb = m.M((I.scale((1,1)) + Xb.scale((1,-1))).a, 1).norm()
P = m.monomial([(x >> 1) | ((x & 1) << 3) for x in range(N)], [0] * N)

def anf(f):
    co = [f >> x & 1 for x in range(16)]
    for j in range(4):
        for x in range(16):
            if x >> j & 1:
                co[x] ^= co[x ^ (1 << j)]
    return co

def monomial_truth(term):
    return sum(int(x & term == term) << x for x in range(N))

def source(f):
    return Cb @ m.monomial(list(range(N)), [2 * (f >> x & 1) for x in range(N)]) @ P

def f3(f, a, b, d):
    indices = [b + 2*b + 4*d + 8*a, d + 2*d + 4*a + 8*b, a + 2*a + 4*b + 8*d]
    return sum(f >> x & 1 for x in indices) % 2

def trace_coefficient(f):
    return sum((1 if a == b == d else -1) * (-1)**f3(f,a,b,d)
               for a,b,d in itertools.product(range(2), repeat=3))

def raw_trace(g):
    return tuple(sum(g.a[x][x][j] for x in range(len(g.a))) for j in range(2)), g.k

# Checking the complete ANF basis establishes the Boolean-parity identity by linearity.
basis = []
for term in range(16):
    f = monomial_truth(term)
    cubic = sum(f3(f,a,b,d) for a,b,d in itertools.product(range(2), repeat=3)) % 2
    assert cubic == int(term in (13,14,15))
    basis.append({'ANF_monomial_mask':term, 'F3_cubic_coefficient':cubic})

rng = random.Random(202611160234)
controls = list(dict.fromkeys([monomial_truth(t) for t in range(16)] + rng.sample(range(65536),64)))
certified = 0
for f in controls:
    co = anf(f)
    coefficient = trace_coefficient(f)
    assert coefficient % 4 == 2 * (co[13] ^ co[14] ^ co[15])
    tr, denominator_exponent = raw_trace(source(f).power(3))
    assert 4*tr[0] == -coefficient * 2**denominator_exponent
    assert 4*tr[1] == coefficient * 2**denominator_exponent
    if co[13] ^ co[14] ^ co[15]:
        assert coefficient % 4 == 2
        certified += 1

acd, bcd = monomial_truth(13), monomial_truth(14)
Z = m.monomial(list(range(N)), [2*(acd >> x & 1) for x in range(N)])
quadratic_terms = [t for t in range(16) if t.bit_count() <= 2]
conjugacies = 0
for _ in range(48):
    q = 0
    for t in quadratic_terms:
        if rng.randrange(2):
            q ^= monomial_truth(t)
    for epsilon in (0,1):
        f = q ^ (acd ^ bcd if epsilon else 0)
        Ze = Z if epsilon else I
        assert Ze @ source(f) @ Ze == source(q)
        co = anf(f)
        assert co[15] == co[7] == co[11] == (co[13] ^ co[14]) == 0
        conjugacies += 1

# A genuinely cubic source can have finite order: this is a semantic negative control.
finite_cubic = source(acd ^ bcd)
assert finite_cubic.power(16) == I
assert any(anf(acd ^ bcd)[t] for t in (7,11,13,14))

# The parity test is only sufficient. An inconclusive test is not a finite-order proof.
abc = monomial_truth(7)
assert trace_coefficient(abc) % 4 == 0
tr5, den5 = raw_trace(source(abc).power(5))
assert 2*tr5[0] == 5*2**den5 and 2*tr5[1] == 5*2**den5

# Tensor control retains the source's actual scalar and the negative valuation.
g = source(acd).power(3)
tr1, k1 = raw_trace(g)
tr2, k2 = raw_trace(g.tensor(g))
square = m.gm(tr1,tr1)
assert tuple(z*2**(2*k1) for z in tr2) == tuple(z*2**k2 for z in square)

result = {
    'status':'PASS_FOUR_BIT_WHOLE_SYSTEM_SCOPE_AND_TRACE_CONTROLS',
    'ANF_basis_F3_checks':basis,
    'literal_trace_controls':len(controls),
    'negative_valuation_controls':certified,
    'finite_cubic_conjugacy_controls':conjugacies,
    'quartic_free_trace_certified_count':16384,
    'quartic_free_finite_counterfamily_count':4096,
    'quartic_free_not_classified_by_these_two_certificates':12288,
    'negative_controls':[
        'Nonzero cubic term alone does not imply infinite order: acd+bcd has order dividing16',
        'Integral cube trace does not imply finite order: abc has nonintegral fifth-power trace',
        'Tensor trace retains the actual complex phase and denominator'
    ],
    'scope':'Written universal trace and conjugacy arguments; exact finite controls only for their stated domains. No new caller or supplier.',
    'new_kappa':False
}
(base/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'ANF_basis_F3_checks'}))
