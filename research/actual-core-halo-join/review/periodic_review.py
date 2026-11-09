"""Independent original-periodic/window matrix observer for Core/halo exports.

Only the pinned original Reference supplies matrix entries. Expected values
use independent full elimination and original-coordinate arithmetic, never
the producer's Schur factors, staged oracle or rectangle interpreter.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
import importlib.machinery
import json
from pathlib import Path
import sys
from types import ModuleType

REFERENCE_INPUTS = {
    'research/rational-unitary-fft/gaussian_reference.py':
        'ed4d0908646e391d4a0ea32c988a0301a1793a72294ac7058a664ed3283ca3c3',
    'research/rational-unitary-fft/exact.py':
        'c9b89d7357210af69865690ba12e695366961f8b501a8fab9d0fefe3fb30c479',
    'research/rational-unitary-fft/gaussian.py':
        '08155357fd39b5fd7959f51f1d205b6511b8577b51520d793c89f92368b399ab',
    'research/certified-gaussian-recovery/intervals.py':
        '159d2a7d32a8cc7c8f56632a8ef127308b984a0a6753c9d6bdccacc6e7d6d4df',
}
INVERSE_OBSERVER_CACHE = {}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(name, path):
    module = ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def pairs(values):
    need(type(values) in (tuple, list) and all(type(pair) in (tuple, list)
         and len(pair) == 2 and all(type(x) is int for x in pair) for pair in values),
         'complete observed complex integer pairs')
    return tuple(tuple(pair) for pair in values)


def squared_error(first, second):
    need(len(first) == len(second), 'complete Euclidean field extent')
    return sum((Q(x)-Q(y))**2 for a,b in zip(first,second) for x,y in zip(a,b))


def inward(value, bits):
    value = Q(value) * 2**bits
    magnitude = abs(value.numerator) // value.denominator
    return -magnitude if value < 0 else magnitude


def rounded_periodic_halo(matrix, initial, q, shift, iterations):
    """Independent whole-period recurrence, not a sparse-domain execution."""
    need(q >= shift >= 0 and iterations >= 1, 'funded recurrence domain')
    scale = 2**q
    size = len(matrix)
    coefficients = [[inward(Q(int(i == j))-matrix[i][j],q)
                     for j in range(size)] for i in range(size)]
    def truncate(value):
        magnitude = abs(value) // scale
        return -magnitude if value < 0 else magnitude
    current = tuple(tuple((-1 if x < 0 else 1)*(abs(x)//2**shift) for x in pair)
                    for pair in initial)
    for _ in range(1,iterations):
        current = tuple(tuple(truncate(initial[i][part]*2**(q-shift)
                            + sum(coefficients[i][j]*current[j][part]
                                  for j in range(size))) for part in (0,1))
                        for i in range(size))
    return current


def review_one(observed, reference, oracle):
    """One original active axis; the separate coordinate preflight covers g>1."""
    allocation, halo = observed['allocation'], observed['halo']
    need(allocation['g'] == 1 and len(halo['normalizer_shifts']) == 1,
         'this observer names its one-axis fixture scope')
    initial, returned = pairs(observed['initial']), pairs(observed['returned'])
    size, side = reference.target_size, allocation['side']
    need(len(initial) == len(returned) == size and size % side == 0,
         'all original periodic coordinates')
    q, precision, width = halo['q'], allocation['P'], allocation['width']
    need(precision >= q and width >= precision, 'exact admitted Core precision lift')
    shift, = halo['normalizer_shifts']
    normalizer = 2**shift
    gap, radius_in, radius_carrier = Q(halo['gap']), Q(halo['input_radius']), Q(halo['carrier_radius'])
    need(gap == reference.narrow_gap and normalizer*gap >= 1, 'same funded original source gap')
    need(all(sum(abs(x) for x in pair) <= radius_in*2**q for pair in initial),
         'actual component-l1 input radius')
    need(allocation['R0']**2 >= size*radius_in**2, 'complete Euclidean input-radius funding')
    matrix = [[reference.entry('narrow',i,j).value for j in range(size)] for i in range(size)]
    error = [[Q(int(i == j))-matrix[i][j] for j in range(size)] for i in range(size)]
    offsets = [(i,j,min((i-j)%size,(j-i)%size)) for i in range(size) for j in range(size)
               if error[i][j]]
    actual_band = max((offset for i,j,offset in offsets),default=0)
    need(actual_band <= halo['halfwidth'], 'whole original source cyclic bandwidth')
    need(all(sum(abs(x) for x in row) <= 1-gap for row in error), 'actual full row-l1 source gap')
    key = reference.description_hash, side
    if key not in INVERSE_OBSERVER_CACHE:
        INVERSE_OBSERVER_CACHE[key] = (oracle.inverse(matrix),
                                      oracle.principal_window_inverse(matrix,side))
    full_inverse, local_inverse = INVERSE_OBSERVER_CACHE[key]
    values = tuple(tuple(Q(x,2**q) for x in pair) for pair in initial)
    exact_local = oracle.apply_msf_tensor((local_inverse,),values)
    exact_periodic = tuple(tuple(x/normalizer for x in pair)
                          for pair in oracle.apply_msf_tensor((full_inverse,),values))
    bridge = observed['bridge_observations']
    lifted, native = pairs(bridge['lifted_input']), pairs(bridge['original_core_return'])
    need(len(lifted) == len(native) == size, 'complete observed native endpoints')
    need(lifted == tuple(tuple(x*2**(precision-q) for x in pair) for pair in initial),
         'independent exact incoming lift')
    need(all(-(2**(width-1)) <= x < 2**(width-1) for pair in native for x in pair),
         'returned native signed carrier')
    native_values = tuple(tuple(Q(x,2**precision) for x in pair) for pair in native)
    core_squared = squared_error(native_values,exact_local)
    epsilon = Q(1,2**(allocation['target']+1))
    need(core_squared <= epsilon**2, 'actual Core versus direct original principal inverses')
    grid_width = q + int(radius_carrier).bit_length() + 1
    need(grid_width == halo['data_width'] and radius_carrier.denominator == 1,
         'same input/output halo carrier schema')
    normalized = oracle.transport_decode(bridge['normalized_source'],grid_width)
    need(normalized == pairs(observed['core_normalized']), 'literal normalized stream versus observation')
    expected_return = tuple(tuple(oracle.toward_zero(x,precision+shift-q) for x in pair)
                            for pair in native)
    need(normalized == expected_return, 'toward-zero normalized return from actual native integers')
    need(all(sum(abs(x) for x in pair) <= radius_carrier*2**q for pair in normalized),
         'actual complete output carrier')
    need(2*epsilon/normalizer <= radius_in and radius_carrier >= 2*radius_in,
         'separate sufficient output-carrier funding')
    rounded_halo = rounded_periodic_halo(matrix,initial,q,shift,halo['terms'])
    margin = halo['boundary']
    need(side > 4*margin and halo['halo'] < margin
         and halo['halo'] == (halo['terms']-1)*halo['halfwidth'], 'first-face geometry')
    kept = tuple(i for i in range(size) if margin <= i%side < side-margin)
    discarded = tuple(i for i in range(size) if i not in kept)
    need(returned == tuple(normalized[i] if i in kept else rounded_halo[i] for i in range(size)),
         'actual merged values at every original address')
    finite_normalized = tuple(tuple(x/normalizer for x in pair) for pair in exact_local)
    returned_values = tuple(tuple(Q(x,2**q) for x in pair) for pair in returned)
    normalized_values = tuple(tuple(Q(x,2**q) for x in pair) for pair in normalized)
    conversion_bound = 2*epsilon/normalizer+Q(2,2**q)
    need(oracle.component_error(normalized_values,finite_normalized) <= conversion_bound,
         'normalized Core error plus paid final quantization')
    kept_tail_operator = max((sum(abs(local_inverse[i][j]-full_inverse[i][j])
                                  for j in range(size))/normalizer for i in kept),default=Q(0))
    local_degree = margin//halo['halfwidth']+1 if halo['halfwidth'] else 1
    retained_locality_bound = 2*(1-gap)**local_degree/(normalizer*gap)
    need(kept_tail_operator <= retained_locality_bound, 'direct kept-tail check against Neumann locality')
    keep_bound = conversion_bound + radius_in*kept_tail_operator
    halo_bound = ((2*halo['halfwidth']+1)*radius_carrier+2)*Q(1,2**q)/gap
    halo_bound += radius_carrier*(1-gap)**halo['terms']/(normalizer*gap)
    need(oracle.component_error(tuple(returned_values[i] for i in kept),
                               tuple(exact_periodic[i] for i in kept)) <= keep_bound,
         'kept output versus exact original periodic inverse')
    need(oracle.component_error(tuple(returned_values[i] for i in discarded),
                               tuple(exact_periodic[i] for i in discarded)) <= halo_bound,
         'discarded output versus exact original periodic inverse')
    # A loose admitted epsilon alone could hide an identity replacement for
    # small inputs. This fixture-specific separation is an additional check.
    identity_squared = squared_error(values,exact_local)
    need(identity_squared > 0 and 16*core_squared < identity_squared,
         'nonidentity Core witness distinguished from input passthrough')
    wrong_source = rounded_periodic_halo(matrix,normalized,q,shift,halo['terms'])
    need(any(wrong_source[i] != returned[i] for i in discarded),
         'using mutated Core values as halo inputs is detected')
    kept_halo_distinguished = any(normalized[i] != rounded_halo[i] for i in kept)
    need(any(x < 0 and abs(x) % 2**(precision+shift-q) for pair in native for x in pair),
         'actual fixture exercises negative nonintegral normalization')
    return dict(period=size,side=side,q=q,precision=precision,native_width=width,
                normalizer_shift=shift,kept=len(kept),discarded=len(discarded),
                actual_cyclic_bandwidth=actual_band,
                omitted_by_wrong_width_one=[(i,j) for i,j,offset in offsets if offset>1],
                original_entries=size*size,full_inverse_residual=True,window_inverse_residual=True,
                core_euclidean_error_squared=str(core_squared),admitted_core_epsilon=str(epsilon),
                identity_replacement_error_squared=str(identity_squared),
                normalized_core_l1_error=str(oracle.component_error(normalized_values,finite_normalized)),
                normalization_quantization_allowance=str(conversion_bound),
                exact_kept_operator_tail=str(kept_tail_operator),retained_locality_bound=str(retained_locality_bound),
                kept_error_allowance=str(keep_bound),halo_error_allowance=str(halo_bound),
                actual_periodic_max_error=str(oracle.component_error(returned_values,exact_periodic)),
                all_original_addresses_checked=True,bit_exact_merge_and_rounding=True,
                wrong_mutated_halo_input_rejected=True,
                kept_halo_substitution_numerically_distinguished=kept_halo_distinguished)


def source_check(reference, oracle):
    size = reference.target_size
    matrix = [[reference.entry('narrow',i,j).value for j in range(size)]
              for i in range(size)]
    offsets = [(i,j,min((i-j)%size,(j-i)%size)) for i in range(size) for j in range(size)
               if matrix[i][j] != int(i == j)]
    maximum = max((k for i,j,k in offsets), default=0)
    need(maximum == 2 and any(k > 1 for i,j,k in offsets), 'actual width-two source and W1 control')
    need(all(sum(abs(Q(int(i == j))-matrix[i][j]) for j in range(size))
             <= 1-reference.narrow_gap for i in range(size)), 'full source row gap')
    whole = oracle.inverse(matrix)
    local = oracle.principal_window_inverse(matrix,size//2)
    need(any(local[i][j] != whole[i][j] for i in range(size) for j in range(size)),
         'finite windows and global inverse are distinct')
    return dict(period=size,original_entries=size*size,cyclic_bandwidth=maximum,
                identity_holes=list(reference.holes),
                off_band_for_wrong_W1=[(i,j) for i,j,k in offsets if k > 1],
                gap=str(reference.narrow_gap),
                whole_and_window_inverse_residuals=True,
                full_source_sha256=reference.description_hash)


def adversarial(observed, reference, oracle):
    """Corrupt exported observations to show that the observer checks reject."""
    variants = []
    wrong = deepcopy(observed)
    wrong['halo']['halfwidth'] = 1
    variants.append(('width-one-omits-original-source-entries',wrong))
    wrong = deepcopy(observed)
    wrong['allocation']['R0'] = 1
    variants.append(('per-coordinate-radius-substituted-for-whole-field',wrong))
    wrong = deepcopy(observed)
    wrong['bridge_observations']['lifted_input'] = deepcopy(wrong['initial'])
    variants.append(('omitted-input-grid-lift',wrong))
    wrong = deepcopy(observed)
    wrong['bridge_observations']['original_core_return'][0][0] += 2**wrong['allocation']['P']
    variants.append(('core-return-corrupted-by-one-unit',wrong))
    wrong = deepcopy(observed)
    drop = wrong['allocation']['P'] + sum(wrong['halo']['normalizer_shifts']) - wrong['halo']['q']
    floor = tuple(tuple(x//2**drop for x in pair)
                  for pair in wrong['bridge_observations']['original_core_return'])
    wrong['core_normalized'] = floor
    wrong['bridge_observations']['normalized_source'] = oracle.transport_encode(
        floor,wrong['halo']['data_width'])
    variants.append(('negative-floor-replaces-toward-zero',wrong))
    size, side = reference.target_size, observed['allocation']['side']
    matrix = [[reference.entry('narrow',i,j).value for j in range(size)] for i in range(size)]
    halo = observed['halo']; shift, = halo['normalizer_shifts']
    initial_halo = rounded_periodic_halo(matrix,pairs(observed['initial']),halo['q'],shift,halo['terms'])
    mutated_halo = rounded_periodic_halo(matrix,pairs(observed['core_normalized']),halo['q'],shift,halo['terms'])
    wrong = deepcopy(observed)
    wrong['returned'] = [observed['returned'][i] if halo['boundary'] <= i%side < side-halo['boundary']
                         else mutated_halo[i] for i in range(size)]
    variants.append(('halo-consumes-mutated-core-source',wrong))
    kept = [i for i in range(size) if halo['boundary'] <= i%side < side-halo['boundary']]
    if any(initial_halo[i] != tuple(observed['core_normalized'][i]) for i in kept):
        wrong = deepcopy(observed)
        wrong['returned'] = [initial_halo[i] if i in kept else observed['returned'][i]
                             for i in range(size)]
        variants.append(('current-kept-core-replaced-by-halo-term',wrong))
    wrong = deepcopy(observed)
    wrong['returned'][kept[0]][0] += 1
    variants.append(('current-kept-output-corrupted-by-one-grid-unit',wrong))
    controls = []
    for name, wrong in variants:
        try:
            review_one(wrong,reference,oracle)
        except ValueError as error:
            controls.append(dict(name=name,rejection=str(error)))
        else:
            raise ValueError('adversarial observation accepted: '+name)
    return controls


def run(package, observations):
    sys.set_int_max_str_digits(0)
    here = Path(__file__).resolve().parent
    oracle = load('_independent_original_oracle',here/'signed_oracle.py')
    importlib.machinery.SourceFileLoader.get_code = lambda self,name: compile(
        self.get_data(self.get_filename(name)),self.get_filename(name),'exec')
    bindings = load('halo_core_sources',package/'halo_core_sources.py')
    sources = bindings.core_sources()
    results, source_preflight = [], []
    with sources.numerical() as runtime:
        for key, expected in REFERENCE_INPUTS.items():
            need(sha256(runtime.raw[key]).hexdigest() == expected,
                 'independently pinned original Reference input '+key)
        if not observations:
            for parameters in ((15,1,2,1,3,64),(31,1,2,1,3,64)):
                reference = runtime.reference.Reference(runtime.raw,*parameters)
                source_preflight.append(source_check(reference,oracle))
        for path in observations:
            content = path.read_bytes()
            observed = json.loads(content)
            need(observed['status'].startswith('PASS_'), 'completed producer observation')
            parameters = tuple(observed['source']['parameters'])
            reference = runtime.reference.Reference(runtime.raw,*parameters)
            need(reference.description_hash == observed['source']['reference_sha256'],
                 'original Reference identity in producer observation')
            result = review_one(observed,reference,oracle)
            result['adversarial_observation_controls'] = adversarial(observed,reference,oracle)
            result['observed_status'] = observed['status']
            result['observed_scope'] = observed.get('scope',
                'Semantic Core plus literal bridge and actual halo; no physical Core execution.'
                if observed.get('physical_core_executed') is False
                else 'Producer execution kind requires the accompanying source report.')
            result['observation_sha256'] = sha256(content).hexdigest()
            result['observation_file'] = path.name
            results.append(result)
    return dict(status=('INDEPENDENT_ORIGINAL_CORE_HALO_OBSERVER_PASS' if results
                        else 'INDEPENDENT_ORIGINAL_SOURCE_PREFLIGHT_PASS'),
                scope='Original-entry full rational inverses and separate global rounded halo recurrence; observer of exported actual words, not another physical Core replay.',
                source_preflight=source_preflight,observations=results,
                original_source_sha256=REFERENCE_INPUTS,
                reviewer_sha256={name:sha256((here/name).read_bytes()).hexdigest()
                                 for name in ('periodic_review.py','signed_oracle.py')})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package',type=Path,required=True)
    parser.add_argument('--observed',type=Path,nargs='*',default=[])
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(args.package.resolve(),args.observed),
                                     sort_keys=True,indent=2)+'\n')
