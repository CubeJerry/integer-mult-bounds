"""Bounded exact checks for heterogeneous Gaussian permutation symmetries.

All symmetry decisions use rational log exponents or certified dyadic
entries. No floating tolerance, predecessor executable, network or writes.
The universal claims are proved in PROOF.md; these are finite controls.
Apache-2.0, prepared for @CubeJerry with substantial OpenAI assistance.
"""
from fractions import Fraction as F
from functools import cache
from hashlib import sha1, sha256
from itertools import combinations, permutations, product
from math import factorial, isqrt, lcm, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def must_fail(action, label):
    try:
        action()
    except ValueError:
        return label
    raise ValueError('missing negative control: '+label)


def source_pins():
    manifest = json.loads((HERE/'DEPENDENCIES.json').read_text())
    need(len(manifest['files']) == 3, 'exact three-source closure')
    for pin in manifest['files']:
        raw = (HERE/pin['local']).read_bytes()
        need(len(raw) == pin['bytes'], 'source length: '+pin['local'])
        need(sha256(raw).hexdigest() == pin['sha256'], 'source SHA: '+pin['local'])
        blob = sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        need(blob == pin['git_blob'], 'source Git blob: '+pin['local'])
    return [{'local':p['local'], 'sha256':p['sha256']} for p in manifest['files']]


def vertices(n):
    return tuple(product(*(range(k) for k in n)))


def validate(n, gamma, shift):
    need(len(n) >= 1 and len(n) == len(gamma) == len(shift), 'axis counts')
    need(all(type(k) is int and k >= 2 for k in n), 'nondegenerate axis')
    need(all(g > 0 for g in gamma), 'positive widths')


def log_matrix(n, gamma, shift):
    validate(n, gamma, shift)
    v = vertices(n)
    return tuple(tuple(sum((-g*(x-y)**2+2*g*a*(x-y)
                            for x,y,g,a in zip(u,w,gamma,shift)), F(0))
                       for w in v) for u in v)


def integer_logs(matrix):
    scale = lcm(*(x.denominator for row in matrix for x in row))
    return tuple(tuple(int(x*scale) for x in row) for row in matrix)


def is_symmetry(matrix, permutation):
    for i,row in enumerate(matrix):
        target = matrix[permutation[i]]
        for j,value in enumerate(row):
            if target[permutation[j]] != value:
                return False
    return True


def complete_group(matrix):
    """All vertex permutations, with no coordinate restriction in the oracle."""
    need(len(matrix) <= 8, 'bounded complete enumeration: at most eight vertices')
    return {p for p in permutations(range(len(matrix))) if is_symmetry(matrix,p)}


def axis_group(n, gamma, shift):
    """Separate proposed signed-coordinate classification."""
    points = vertices(n)
    index = {v:i for i,v in enumerate(points)}
    answer = set()
    d = len(n)
    for sigma in permutations(range(d)):
        if any(n[sigma[i]] != n[i] or gamma[sigma[i]] != gamma[i] for i in range(d)):
            continue
        for signs in product((-1,1), repeat=d):
            if any(signs[i]*shift[sigma[i]] != shift[i] for i in range(d)):
                continue
            image = []
            for x in points:
                y = [0]*d
                for i in range(d):
                    y[sigma[i]] = x[i] if signs[i] == 1 else n[i]-1-x[i]
                image.append(index[tuple(y)])
            answer.add(tuple(image))
    return answer


def cycle_data(permutation):
    seen, lengths = set(), []
    for start in range(len(permutation)):
        if start in seen:
            continue
        point, length = start, 0
        while point not in seen:
            seen.add(point)
            length += 1
            point = permutation[point]
        need(point == start, 'permutation cycle closes')
        lengths.append(length)
    return len(lengths), lcm(*lengths)


def reflection_minimum(n, shift):
    total = prod(n)
    zero = [i for i,a in enumerate(shift) if a == 0]
    if any(n[i] % 2 == 0 for i in zero):
        return total//2
    fixed = total//prod(n[i] for i in zero)
    return (total+fixed)//2


def exact_cases():
    cases = [
        ('two-distinct-zero', (2,2), (F(1),F(2)), (F(0),F(0)), 4),
        ('two-distinct-nonzero', (2,2), (F(1),F(2)), (F(1,5),F(-2,7)), 1),
        ('coincident-physical-sides', (2,3), (F(4),F(1)), (F(0),F(0)), 4),
        ('one-odd-zero-axis', (2,3), (F(4),F(1)), (F(1,4),F(0)), 2),
        ('two-point-equal-zero', (2,2,2), (F(1),)*3, (F(0),)*3, 48),
        ('equal-widths-signed-shifts', (2,2,2), (F(1),)*3, (F(1,4),F(-1,4),F(1,4)), 6),
        ('equal-width-zero-block', (2,2,2), (F(1),)*3, (F(0),F(0),F(1,4)), 8),
        ('mixed-width-opposite-shifts', (2,2,2), (F(1),F(1),F(2)), (F(1,4),F(-1,4),F(0)), 4),
        ('axis-diagonal-length-collision', (2,2,2), (F(1),F(2),F(3)), (F(0),)*3, 8),
        ('three-distinct-nonzero', (2,2,2), (F(1),F(2),F(3)), (F(1,4),F(1,4),F(-1,4)), 1),
        ('odd-single-axis', (3,), (F(2),), (F(0),), 2),
    ]
    receipt = []
    for name,n,g,a,count in cases:
        matrix = integer_logs(log_matrix(n,g,a))
        actual = complete_group(matrix)
        predicted = axis_group(n,g,a)
        need(actual == predicted and len(actual) == count, 'classification: '+name)
        cycles = [cycle_data(p) for p in actual]
        if len(set(g)) == len(g):
            need(all(order <= 2 and 2*c >= len(matrix) for c,order in cycles), 'involution bound')
            need(min(c for c,_ in cycles) == reflection_minimum(n,a), 'exact reflection minimum')
        receipt.append({'name':name, 'vertices':len(matrix),
                        'all_vertex_permutations':factorial(len(matrix)),
                        'symmetries':len(actual), 'orders':sorted({o for _,o in cycles}),
                        'minimum_cycles':min(c for c,_ in cycles)})
    for shifts,expected in [((F(0),F(0)),5),((F(0),F(1,4)),6)]:
        group = axis_group((3,3),(F(1),F(2)),shifts)
        matrix = integer_logs(log_matrix((3,3),(F(1),F(2)),shifts))
        need(all(is_symmetry(matrix,p) for p in group), 'odd-grid candidate check')
        need(min(cycle_data(p)[0] for p in group) == expected == reflection_minimum((3,3),shifts),
             'odd-grid fixed-point formula')
    return receipt


def prime(value):
    return value >= 2 and all(value % k for k in range(2,isqrt(value)+1))


def fine_prime_checks():
    pairs = intervals = 0
    for p in range(2,9):
        eta = F(1,4*p*p)
        for r in (16,32,64,128,256):
            candidates = []
            for t in (r,r//2):
                intervals += 1
                candidates.extend((t,s) for s in range(3,t,2)
                                  if prime(s) and (1-2*eta)*t < s <= (1-eta)*t)
            for (t,s),(u,z) in combinations(candidates,2):
                if s == z:
                    continue
                m,k = (r//t)*s,(r//u)*z
                need(0 < m < r and 0 < k < r and m != k, 'fine prime integer separation')
                need(abs(F(s,t)-F(z,u)) >= F(1,r), 'broad gap')
                need(abs(F(t,s)-F(u,z)) > F(1,r), 'narrow gap')
                pairs += 1
    need(F(59,64)-F(29,32) == F(1,64), 'sharp broad fixture')
    need(abs(F(64,59)-F(32,29)) > F(1,64), 'narrow fixture')
    need(pairs > 0, 'nonvacuous fine-prime controls')
    return {'p_range':[2,8], 'dyadic_r':[16,32,64,128,256],
            'target_intervals':intervals, 'distinct_prime_pairs':pairs,
            'sharp_broad_example':{'p':2,'r':64,'target':[64,32],'source':[59,29],'m':[59,58]},
            'all_size_prime_existence_reproved':False}


@cache
def exp_minus_bounds(x):
    """Exact enclosure: positive exp series, then a geometric tail bound."""
    x = F(x)
    need(0 <= x <= 64, 'bounded exponential argument')
    if x == 0:
        return F(1),F(1)
    term = total = F(1)
    for k in range(1,129):
        term *= x/k
        total += term
    first_tail = term*x/129
    tail_bound = first_tail/(1-x/130)
    return 1/(total+tail_bound),1/total


def dyadic_matrix(n, gamma, shift, bits):
    need(type(bits) is int and 0 <= bits <= 32, 'bounded rounding precision')
    scale = 1 << bits
    result = []
    for row in log_matrix(n,gamma,shift):
        target = []
        for exponent in row:
            need(exponent <= 0, 'unit-bounded ideal entry')
            lower,upper = exp_minus_bounds(-exponent)
            lo,hi = lower*scale+F(1,2),upper*scale+F(1,2)
            rounded_lo,rounded_hi = lo.numerator//lo.denominator,hi.numerator//hi.denominator
            need(rounded_lo == rounded_hi, 'certified unique dyadic rounding')
            target.append(rounded_lo)
        result.append(tuple(target))
    return tuple(result)


def rounding_guard(gamma, epsilon):
    need(len(set(gamma)) == len(gamma) and len(gamma) >= 2, 'distinct colored axes')
    low,high = min(gamma),max(gamma)
    need(high < 2*low, 'separated unit-edge band')
    edge_low = exp_minus_bounds(2*high)[0]
    nonedge_high = exp_minus_bounds(4*low)[1]
    axis_gap = min(abs(x-y) for x,y in combinations(gamma,2))
    adjacent_gap = edge_low-nonedge_high
    color_gap = 2*edge_low*axis_gap
    product_error = 2*epsilon+epsilon*epsilon
    need(2*product_error < min(adjacent_gap,color_gap), 'pair-product perturbation gap')
    return {'epsilon':str(epsilon), 'pair_product_error':str(product_error),
            'strict_edge_and_color_gaps_certified':True}


def rounding_checks():
    configs = [
        ('fine-prime-broad',(2,3),(F(59,64),F(29,32)),(F(1,4),F(-1,4)),16),
        ('fine-prime-narrow',(2,3),(F(64,59),F(32,29)),(F(0),F(0)),16),
        ('tiny-shifts-may-disappear',(2,2),(F(1),F(3,2)),(F(1,2**40),)*2,12),
    ]
    receipts = []
    for name,n,g,a,bits in configs:
        need(all(abs(x) <= F(1,2) for x in a), 'shift unit-entry domain')
        guard = rounding_guard(g,F(1,2**(bits+1)))
        rounded = dyadic_matrix(n,g,a,bits)
        actual = complete_group(rounded)
        reflections = axis_group(n,g,(F(0),)*len(n))
        need(actual <= reflections, 'rounded symmetry containment')
        need(all(cycle_data(p)[1] <= 2 and 2*cycle_data(p)[0] >= prod(n) for p in actual),
             'rounded order/cycle bound')
        if name == 'tiny-shifts-may-disappear':
            need(len(axis_group(n,g,a)) == 1 and len(actual) == 4, 'rounded tiny-shift control')
        receipts.append({'name':name,'bits':bits,'vertices':prod(n),
                         'all_vertex_permutations':factorial(prod(n)),
                         'rounded_symmetries':len(actual), 'guard':guard})
    n,g,a,bits = (2,2),(F(1),F(3,2)),(F(0),F(0)),12
    original = dyadic_matrix(n,g,a,bits)
    changed = [list(row) for row in original]
    changed[0][1] += 1
    changed = tuple(map(tuple,changed))
    rounding_guard(g,F(3,2**(bits+1)))
    need(len(complete_group(original)) == 4 and len(complete_group(changed)) == 1,
         'nonuniform bounded perturbation destroys reflections')
    return receipts


def controls():
    n,g,a = (2,2,2,2),(F(1),)*4,(F(1,4),)*4
    pts = vertices(n)
    index = {x:i for i,x in enumerate(pts)}
    rotation = tuple(index[(x[-1],)+x[:-1]] for x in pts)
    need(is_symmetry(integer_logs(log_matrix(n,g,a)),rotation), 'equal-width long orbit exists')
    need(cycle_data(rotation) == (6,4) and 2*6 < len(pts), 'equal-width violation of involution bound')
    coarse = dyadic_matrix((2,2),(F(2),F(3)),(F(0),F(0)),0)
    need(coarse == tuple(tuple(int(i == j) for j in range(4)) for i in range(4)), 'coarse identity')
    group = complete_group(coarse)
    need(len(group) == 24 and min(cycle_data(p)[0] for p in group) == 1, 'coarse long orbit')
    failures = [must_fail(lambda:validate((1,2),(F(1),F(2)),(F(0),F(0))), 'degenerate-axis'),
                must_fail(lambda:validate((2,2),(F(0),F(2)),(F(0),F(0))), 'zero-width'),
                must_fail(lambda:rounding_guard((F(1),F(3,2)),F(1,2)), 'coarse-error-guard')]
    grid = set(vertices((2,3)))
    corner_set = {(x,y) for x in (0,1) for y in (0,2)}
    square_swap = lambda point:(F(point[1],2),2*point[0])
    need({square_swap(x) for x in corner_set} == corner_set, 'square corner permutation')
    need({square_swap(x) for x in grid} != grid and square_swap((0,1)) not in grid,
         'square-hull midpoint prevents axis swap')
    return {'equal_width_long_orbit':{'vertices':16,'order':4,'cycles':6},
            'coarse_rounding_identity':{'vertices':4,'symmetries':24,'minimum_cycles':1},
            'rejected_domains':failures,
            'coincident_side_corner_swap_fails_on_midpoint':True,
            'tiny_nonzero_shift_can_gain_reflections':True,
            'bounded_nonuniform_perturbation_can_destroy_reflections':True,
            'uniform_pointwise_rounding_claimed_to_destroy_exact_symmetries':False}


def main():
    pins = source_pins()
    exact = exact_cases()
    prime_receipt = fine_prime_checks()
    rounded = rounding_checks()
    negative = controls()
    result = {'status':'PASS_HETEROGENEOUS_GAUSSIAN_SYMMETRIES',
              'verifier_sha256':sha256((HERE/'verify.py').read_bytes()).hexdigest(),
              'authenticated_sources':pins, 'exact_complete_enumerations':exact,
              'all_vertex_permutations_checked':sum(x['all_vertex_permutations'] for x in exact),
              'additional_nine_vertex_reflection_fixtures':2,
              'fine_prime_checks':prime_receipt, 'rigorous_rounding_enumerations':rounded,
              'negative_controls':negative,
              'dense_format':'exactly 2cT scalar slots; distinct widths force T^2<=2cT<=2T^2',
              'proof_scope':'Universal written classification plus bounded exact checks; no whole-caller ancestry, arbitrary-rank or runtime lower bound.',
              'new_kappa':False,'assumptions_discharged':[]}
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
