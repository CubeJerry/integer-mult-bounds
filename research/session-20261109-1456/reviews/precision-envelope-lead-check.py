"""Independent source/guard check for the frozen precision envelope.

No submitted checker is imported. The universal conditional proof and
norm contracts were reviewed separately. Prepared for @CubeJerry with
substantial OpenAI assistance; not human or proof-kernel acceptance.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha1, sha256
import gzip
import json
import sys


def need(value, message):
    if not value:
        raise ValueError(message)


p = Path(sys.argv[1])
payload = (p / 'data/word.json.gz').read_bytes()
need(sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
     == 'd93e67ca7628bf5531ae6e369da4dd7b7907b88f', 'frozen native source')
w = json.loads(gzip.decompress(payload))
ev = w['program']
need(len(ev) == 71144 and w['public'] == 1461, 'current native source size')
size = w['public'] + w['owned_fields']
m = [F(i < w['public']) for i in range(size)]
e = [F(0) for _ in range(size)]
maximum_m, maximum_e = F(1), F(0)
numerators, denominators = [], []
for i, row in enumerate(ev):
    op, target = row[:2]
    if op in ('INIT', 'CLEAR'):
        m[target] = e[target] = F(0)
    elif op == 'MOVE':
        e[target] += 1
    else:
        c = abs(F(row[2] if op == 'SCALE' else row[3]))
        numerators.append((abs(c.numerator), i))
        denominators.append((c.denominator, i))
        if op == 'SCALE':
            m[target], e[target] = c*m[target], c*e[target]
        else:
            source = row[2]
            maximum_m = max(maximum_m, c*m[source])
            maximum_e = max(maximum_e, c*e[source])
            m[target] += c*m[source]
            e[target] += c*e[source]
        if c.denominator != 1:
            e[target] += 1
    maximum_m = max(maximum_m, m[target])
    maximum_e = max(maximum_e, e[target])
actual = {'M': maximum_m, 'Sigma': maximum_e, 'Gamma': max(e[:w['public']])}
receipt = json.loads((p / 'ENVELOPES.json').read_text())
for key, value in actual.items():
    bound = receipt['native']['bounds'][key]
    need(value == F(bound['exact']), 'independent native '+key)
    need(value < 1 << bound['strict_power_of_two'], 'strict native bound')

need(ev[37476] == ['MOVE', 697, 1042, 591, False], 'actual completed MOVE cut')
need(ev[37480] == ['SCALE', 697, '-2/3', 591], 'actual odd scalar consumer')
need(all(697 not in r[1:3] for r in ev[37477:37480]), 'intervening disjoint fields')
need(max(numerators)[0] == 14729531 and max(denominators)[0] == 393216,
     'actual source temporary widths')

v = 1920
H = 141616 * 10**14
K = v * 153**v * (H+1)**2
need((H+1)**2226 < 1 << 141616, 'current strictification threshold')
need((4096*K).bit_length() <= H, 'K versus N without constructing N')
for d in range(1, 4097):
    g = 5 if d < 19 else 0
    need((d+3)**4 <= 1 << (d+2*g-1), 'small-level error guard')
    need((d+3)**2 <= 1 << (d+3), 'small-level radius guard')
for k in range(16, 4097):
    need(4*k+7 <= 1 << (k-3), 'large-D logarithm domination')

rounded_cases = 0
for a in range(-9, 10):
    for b in range(1, 20):
        for n in range(-64, 65):
            rounded = (a*n+b//2)//b
            need(2*abs(b*rounded-a*n) <= b, 'signed nearest-up residual')
            rounded_cases += 1
need((-2+1)//3 == -1 and (-2) % 3 != 0, 'rounded versus exact -2/3 boundary')
need((-1+1)//2 == 0 and (1+1)//2 == 1, 'upward ties not odd')

result = dict(
    status='PASS_INDEPENDENT_PRECISION_SOURCE_AND_GUARDS',
    native_events=len(ev), exact_native_majorants_checked=3,
    small_D_guards=4096, large_log_integer_checks=4081,
    signed_rounding_oracle_cases=rounded_cases,
    current_Kstar_bits=K.bit_length(), scaled_Kstar_bits=(4096*K).bit_length(),
    proof_sha256=sha256((p/'PROOF.md').read_bytes()).hexdigest(),
    mathematical_review=['complete-fibre rather than coordinate sup norm',
                        'actual-input total child contracts',
                        'positive propagation and independent backward witnesses',
                        'S1-S5 and normalizer assumptions remain explicit',
                        'N(D+3) wrapper admission guard',
                        'temporary versus output signed bounds',
                        'optimistic scan model is not a physical tariff'],
    scope='Critical source constants and guard arithmetic, not complete caller execution or assumption discharge')
print(json.dumps(result, sort_keys=True, indent=2))
