"""Independent C5 algebra, factor linkage and pruning checks; no full packet replay.

Apache-2.0. Prepared for @CubeJerry with substantial OpenAI assistance.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
import types


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def linear(rows, value):
    return sum(((row & value).bit_count() % 2) << bit for bit, row in enumerate(rows))


def source_algebra(package, producer, linear_module):
    span, columns = {0}, []
    for value in (137, *(1 << bit for bit in range(9))):
        if value not in span:
            columns.append(value)
            span |= {entry ^ value for entry in span}
    need(columns == [137, 1, 2, 4, 8, 16, 32, 64, 256], 'canonical ordered basis')
    matrix = tuple(sum(((column >> i) & 1) << j for j, column in enumerate(columns))
                   for i in range(9))
    inverse_permutation = {linear(matrix, x): x for x in range(512)}
    need(len(inverse_permutation) == 512, 'invertible actual chart')
    inverse_columns = [inverse_permutation[1 << i] for i in range(9)]
    inverse = tuple(sum(((column >> i) & 1) << j for j, column in enumerate(inverse_columns))
                    for i in range(9))
    quadratic = tuple((1 << i) ^ sum(((u & v).bit_count() % 2) << j
                                    for j, v in enumerate(inverse_columns))
                      for i, u in enumerate(inverse_columns))
    need(matrix == producer.G and quadratic == producer.Q, 'independent G/Q derivation')
    source = load(package/'inputs/lifetime/inputs/move/reference/source/native_verify.py',
                  '_review_actual_source_definition')
    zero = (0,)*9
    expected = (('D', quadratic, zero), ('P', inverse), ('C', 1, 1),
                ('P', matrix), ('D', quadratic, zero))
    need(source.frame((137,), 9) == expected, 'actual canonical circuit/phase')

    def phase(x):
        return sum(((quadratic[i] >> j) & 1) * ((x >> i) & 1) * ((x >> j) & 1)
                   for i in range(9) for j in range(i+1, 9)) % 2

    word = linear_module.cnot_word(matrix)
    need(len(word) == 21, 'fixed word length')
    for x in range(512):
        need(phase(x) == (((x >> 7) & 1) * (((x >> 0) ^ (x >> 3)) & 1)), 'direct quadratic')
        need((phase(x)+phase(x ^ 137)) % 2 == ((x & 9).bit_count() % 2), 'absolute conjugated sign')
        y = inverse_permutation[x]
        actual = {}
        for z, coefficient in ((y, (1, 1)), (y ^ 1, (1, -1))):
            destination = linear(matrix, z)
            sign = (-1) ** (phase(x)+phase(destination))
            actual[destination] = tuple(sign * value for value in coefficient)
        sign = (-1) ** ((x & 9).bit_count() % 2)
        need(actual == {x: (1, 1), x ^ 137: (sign, -sign)}, 'independent two-term kernel')
        forward = backward = x
        for target, control in word:
            forward ^= ((forward >> control) & 1) << target
        for target, control in reversed(word):
            backward ^= ((backward >> control) & 1) << target
        need(forward == linear(matrix, x) and backward == inverse_permutation[x], 'fixed word action')
    need(source.frame((239,), 9) != expected, 'source239 separated')
    reverse_bits = lambda x: sum(((x >> i) & 1) << (8-i) for i in range(9))
    need((reverse_bits(137), reverse_bits(9), reverse_bits(129)) == (290, 288, 258), 'packed bit order')
    witnesses = []
    for width in (2, 3, 6, 31):
        value = -(1 << (width-1))
        output = ((value//2, value//2), (-value//2, value//2))
        need(all(-(1 << (width-1)) <= v < (1 << (width-1)) for pair in output for v in pair), 'endpoint fit')
        need(phase(129) == 1 and -value == 1 << (width-1), 'first phase overflow')
        witnesses.append({'width': width, 'native_address': 129, 'packed_address': 258,
                          'input_real': value, 'complete_components': output,
                          'unrepresentable_first_phase': -value})
    return {'all_512_columns': True, 'matrix_rows': matrix, 'quadratic_rows': quadratic,
            'cnot_gates_each_direction': len(word), 'endpoint_witnesses': witnesses}, word


def signatures(rules):
    return [(rule.tests, rule.writes, rule.moves, rule.target) for rule in rules]


def closure(graph, starts, stop=()):
    seen, pending = set(), list(starts)
    while pending:
        state = pending.pop()
        if state == 'HALT' or state in seen or state in stop:
            continue
        need(state in graph.rules, 'undefined graph edge')
        seen.add(state)
        pending.extend(rule.target for rule in graph.rules[state])
    return seen


def compare_scans(left, left_entry, right, right_entry):
    pairs, mapping, inverse = [(left_entry, right_entry)], {}, {}
    while pairs:
        a, b = pairs.pop()
        if a == 'HALT' or b == 'HALT':
            need(a == b, 'same scan terminal')
            continue
        if a in mapping:
            need(mapping[a] == b, 'scan state isomorphism')
            continue
        need(b not in inverse, 'injective scan isomorphism')
        mapping[a], inverse[b] = b, a
        aa, bb = left.rules[a], right.rules[b]
        need(len(aa) == len(bb), 'same scan branch count')
        for u, v in zip(aa, bb):
            need((u.tests, u.writes, u.moves) == (v.tests, v.writes, v.moves), 'exact scan effects')
            pairs.append((u.target, v.target))
    return len(mapping)


def factors_and_ports(producer, c4, r2, home, word):
    native, alphabet, starts = producer.compile_native()
    need(len(native) == 75391 and starts['commit'] == 75357, 'exact native extent and commit')
    factors = [('right_D_', r2.PHASE.compile_phase((0,)*9, producer.Q, 0)),
               ('right_G_', r2.compile_word(tuple(reversed(word)))),
               ('central_C_', r2.LEAF.compile_leaf()),
               ('left_G_', r2.compile_word(word)),
               ('left_D_', r2.PHASE.compile_phase((0,)*9, producer.Q, 0))]
    checked = 0
    for index, (name, (code, symbols)) in enumerate(factors):
        begin = starts[name]
        after = starts[factors[index+1][0]] if index+1 < len(factors) else starts['commit']
        need(after-begin == len(code), 'unmodified factor instruction extent')
        for pc, instruction in enumerate(code):
            op, *args = instruction
            port = lambda t: 0 if t == 0 else 2 if t == 1 else t+2
            if op == 'read':
                expected = (op, port(args[0]), {s: begin+target for s, target in args[1].items()})
            elif op in ('write', 'move'):
                expected = (op, port(args[0]), args[1])
            elif op == 'goto':
                expected = (op, begin+args[0])
            elif op == 'halt':
                expected = ('goto', after)
            else:
                raise ValueError('unknown factor instruction')
            need(native[begin+pc] == expected, 'exact factor pc/port relocation')
            checked += 1
    need(not any(row[:2] == ('write', 1) for row in native[:starts['commit']]),
         'original native DATA stays unchanged before complete commit')
    need(not any(row[:2] == ('write', 0) for row in native), 'native header is read-only')
    graph = home.D.Graph()
    producer.embed_native(graph, native, 'AFTER')
    names = list(graph.rules)
    need(len(names) == len(native), 'one outer state per native instruction')
    for pc, instruction in enumerate(native):
        op, *args = instruction
        nxt = names[pc+1] if pc+1 < len(native) else 'AFTER'
        if op == 'read':
            expected = [(((3+args[0], symbol),), (), (), names[target])
                        for symbol, target in args[1].items()]
        elif op == 'write':
            expected = [((), ((3+args[0], args[1]),), (), nxt)]
        elif op == 'move':
            expected = [((), (), ((3+args[0], args[1]),), nxt)]
        elif op == 'goto':
            expected = [((), (), (), names[args[0]])]
        else:
            need(op == 'halt', 'native instruction alphabet')
            expected = [((), (), (), 'AFTER')]
        need(signatures(graph.rules[names[pc]]) == expected, 'exact adapter native embedding')
    old_scan, new_scan = home.D.Graph(), home.D.Graph()
    old_entry = home.primitive(old_scan, 'MOVE28141', 1, 'HALT', parser_only=True)
    new_entry, _ = producer.adapter(new_scan, (), 'HALT', stale=True)
    scan_states = compare_scans(old_scan, old_entry, new_scan, new_entry)
    return {'factor_instructions_checked': checked, 'all_native_instructions_relocated': len(native),
            'exact_scan_states': scan_states, 'native_commit_pc': starts['commit'],
            'no_original_DATA_write_before_commit': True, 'native_header_readonly': True}


def graph_join(producer, c4):
    graph, meta = producer.compile_join()
    original, old_meta = c4.compile_protocol()
    preserved = closure(original, [old_meta['entries'][event] for event in (28037, 28041)])
    need(len(preserved) == 4927, 'retained C4 entry closure')
    for state in preserved:
        need(state in graph.rules and signatures(graph.rules[state]) == signatures(original.rules[state]),
             'every inherited INIT/SUB rule is unchanged')
    need(closure(graph, meta['entries'].values()) == set(graph.rules), 'exact fixed reachability pruning')
    need(len(graph.rules) == 71524 and producer.digest(graph)
         == 'fec60dd4653c6c06846850b2d318d9eec0b7d9856af6b65bae2d336d5c5f99a0',
         'frozen joined graph')
    producer_states = closure(graph, [meta['entries'][28039]])
    touched = {t for state in producer_states for rule in graph.rules[state]
               for pairs in (rule.tests, rule.writes, rule.moves) for t, _ in pairs}
    need(touched == {3, 43} | set(range(5, 37)), 'producer uses only declared borrowed work/bank')
    prefix = closure(graph, [meta['entries'][28039]],
                     stop=(meta['producer_stages']['primitive_return'],))
    need(not any(t == 43 for state in prefix for rule in graph.rules[state] for t, _ in rule.writes),
         'no public donor write before completed adapter return')
    # A returning-interface omission must fail the same exact preservation check.
    entry = old_meta['entries'][28041]
    need(graph.rules[entry], 'nonempty retained SUB entrance')
    mutant = dict(graph.rules)
    mutant[entry] = []
    need(signatures(mutant[entry]) != signatures(original.rules[entry]), 'deleted C4 edge detected')
    # Exact complete envelope arithmetic, without floating approximations.
    need(2*65536*65 + 1024*84 + 2*8192 + 65536 + 31 == 8687647, 'fV coefficient')
    need(2*65536 + 2*8192 + 65536 == 212992, 'E coefficient')
    need(2*65536 + 2*8192 + 65536 + 27 == 213019, 'constant coefficient')
    need(max(8687647, 212992, 213019) < (1 << 24), 'complete native envelope')
    need(128+2*11 == 150 and 128+2*16+1 == 161, 'producer delivery price')
    need(150+4096+19 == 4265 and 161+4096+34+1+41 == 4333, 'prefix linear price')
    need(4265 <= 8192 and 4333 <= 8192+128, 'INIT/producer/SUB linear envelope')
    return {'joined_states': len(graph.rules), 'retained_C4_states': len(preserved),
            'producer_states': len(producer_states), 'producer_ports': sorted(touched),
            'all_edges_retained_after_pruning': True, 'unchanged_C4_rules': True,
            'public_donor_write_only_after_adapter_return': True,
            'deleted_return_edge_detected': True, 'exact_cost_envelopes': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    package = args.package.resolve()
    raw = (package/'producer.py').read_bytes()
    source_hash = 'e183c38866223a8b896c8210f65e6531f89b0836b88541cb45b27e7ebc672c2f'
    need(sha256(raw).hexdigest() == source_hash, 'frozen scientific producer source')
    producer = load(package/'producer.py', '_review_source_producer')
    c4 = producer.lifetime()
    _, _, home = c4.inputs()
    r2 = home.C
    algebra, word = source_algebra(package, producer, r2.LINEAR)
    witness = json.loads((package/'SOURCE-EVENT.json').read_text())
    producer.source_binding(witness)
    wrong = dict(witness, frames={'3': [], '601': [239]})
    try:
        producer.source_binding(wrong)
    except ValueError as error:
        need(str(error) == 'actual source frames', 'specific wrong-frame binding rejection')
    else:
        raise ValueError('wrong source239 binding accepted')
    result = {'status': 'PASS', 'producer_sha256': source_hash, 'algebra': algebra,
              'factor_and_scan_linkage': factors_and_ports(producer, c4, r2, home, word),
              'joined_graph': graph_join(producer, c4),
              'wrong_frame_binding_rejected': True,
              'scope': 'Independent algebra, exact instruction/port/scan linkage, pruning and costs; no full native packet replay.'}
    rendered = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.receipt:
        args.receipt.write_text(rendered)
    print(json.dumps({'status': 'PASS', 'columns': 512, 'native_instructions': 75391,
                      'joined_states': 71524, 'preserved_C4_states': 4927}, sort_keys=True))


if __name__ == '__main__':
    main()
