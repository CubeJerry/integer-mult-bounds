"""Read-only exact retained caller header-meter audit; no scientific edits."""
from pathlib import Path
import argparse, hashlib, json, sys, types

HERE = Path(__file__).resolve().parent
OLD = HERE/'inputs/keypass'

def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module

def fields(meter):
    return {key: getattr(meter, key) for key in ('reads', 'writes', 'moves')}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    v = load(OLD/'verify.py', '_B9_meter_retained')
    retained, previous, base, m, key_pass, hardware, caller, code, labels, metadata, _ = v.modules()
    captured = []
    original = m.route.emit_headers
    def observe(join, iterator, lease, headers, width):
        physical = {'source': iterator.source, 'axis': iterator.counters['axis'],
                    'guide': lease.actual.guide, 'result': lease.actual.result['stream'],
                    'scratch_width': iterator.counters['width']}
        indices = {name: next((i for i, port in enumerate(iterator.bank.ports)
                              if port is target), None) for name, target in physical.items()}
        old = {name: fields(port.meter) for name, port in physical.items()}
        value = original(join, iterator, lease, headers, width)
        delta = {name: {key: getattr(port.meter, key)-old[name][key]
                        for key in old[name]} for name, port in physical.items()}
        included = {name: (name in ('source', 'axis', 'scratch_width') or indices[name] is not None)
                    for name in physical}
        captured.append({'bank_indices': indices, 'header_actions': delta,
                         'included_in_old_source_meter': included,
                         'omitted_header_native_actions': sum(sum(delta[name].values())
                                                             for name in physical if not included[name])})
        return value
    m.route.emit_headers = observe
    cases = []
    for name, moduli in (('exact_7388', (5, 7, 3, 2)),
                         ('current_wire_sensitive', (5, 7, 2, 3))):
        source, payload, _ = previous.fixture_case(m, base, moduli, (3, 2, 1, 1))
        before = bytes(source.cells), source.head, dict(payload.cells), payload.head
        machine = hardware.Program(code, labels, metadata)
        for reverse in (False, True):
            receipt, _ = caller.run_leg(m, base, machine, source, payload, reverse)
            case = captured[-1]
            case.update(case=name, direction='inverse' if reverse else 'forward',
                        old_encoded_source_symbol_actions=receipt['encoded_source_symbol_actions'])
            if case['bank_indices']['guide'] != 0 or case['bank_indices']['result'] != 62:
                raise ValueError('actual bank ownership unexpected')
            if case['omitted_header_native_actions'] != 0:
                raise ValueError('old native header action omission')
            cases.append(case)
        if (bytes(source.cells), source.head, dict(payload.cells), payload.head) != before:
            raise ValueError('actual caller roundtrip changed')
    result = {'status': 'PASS_NO_HEADER_METER_OMISSION',
              'scientific_predecessor': 'f789e7318ef89b26c2e358c4c1eb09ce93d21f73',
              'cause': 'Bank.open supplies adapter.Port=Bank.take; guide is bank[0], result is bank[62], both included in numerical tuple.',
              'cases': cases}
    text = json.dumps(result, indent=2)+'\n'
    if args.receipt:
        args.receipt.write_text(text)
    print(text, end='')

if __name__ == '__main__':
    main()
