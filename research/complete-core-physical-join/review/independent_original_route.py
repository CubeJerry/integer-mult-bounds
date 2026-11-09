"""Independent boundary-only check; the numerical Core is an explicit test double.

The actual OriginalCore wrapper and retained global routers are executed. An
independent flat-bit address oracle checks both boundaries. This is not a
physical numerical Core replay or an all-size native-supplier proof.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch


def require(ok, message):
    if not ok:
        raise ValueError(message)


def expected_indices(lengths, selected, m):
    """Flat bit extraction; does not call Layout.gather/address/inverse."""
    starts = []
    for width in lengths:
        starts.append(sum(lengths[:len(starts)]))
    selected_positions = [starts[a] + b for a in selected for b in range(m)]
    destinations = list(range(len(selected_positions)))
    vacant_low = sorted(set(destinations) - set(selected_positions))
    vacated_high = sorted(set(selected_positions) - set(destinations))
    source_at_destination = list(range(sum(lengths)))
    for new, old in zip(destinations, selected_positions):
        source_at_destination[new] = old
    for old, new in zip(vacant_low, vacated_high):
        source_at_destination[new] = old
    require(len(set(source_at_destination)) == sum(lengths), 'oracle permutation')
    packed_of_original = []
    for old_address in range(1 << sum(lengths)):
        digits = [(old_address >> b) & 1 for b in range(sum(lengths))]
        packed_of_original.append(sum(digits[source] << new
                                      for new, source in enumerate(source_at_destination)))
    return packed_of_original


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--package', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    package = Path(args.package).resolve()
    sys.path[:0] = [str(package), str(package/'retained/cohort')]
    from join_sources import physical
    from core_layout import Layout
    cases = [((2, 2, 1), (1, 0), 1),
             ((1, 2, 2), (2, 1), 1),
             ((2, 1, 2), (2,), 2),
             ((1, 1, 2), (0, 2), 1)]
    results = []
    rejected_controls = []
    with physical():
        import original_layout as implementation
        import check_composed
        from records import Tape
        from cardinal_counts import Count
        from physical_controls import emit_signed
        from session import erase_marker, initialize_marker
        from words import BLANK
        from fixture_tools import body, snapshot, integer

        def decode(tape, width):
            bits = body(tape)
            require(len(bits) % (2*width) == 0, 'complete test complex field')
            return tuple((integer(bits[i:i+width]), integer(bits[i+width:i+2*width]))
                         for i in range(0, len(bits), 2*width))

        # Purposefully separate from every numerical provider implementation.
        # The double records the field actually delivered by the first route,
        # then returns distinct context/coordinate tagged records. It cannot
        # establish any numerical or native-provider claim.
        class SemanticCoreDouble:
            def __init__(self, root, observe=None):
                self.output = Tape()
                erase_marker(self.output)
                self.pending = False
                self.closed = True
                self.received = None
                self.returned = None
                self.width = None

            def idle(self):
                require(not self.pending and self.output.read() == BLANK,
                        'double return consumed')

            def run(self, payload, *parameters):
                self.idle()
                initialize_marker(self.output)
                self.received = decode(payload, self.width)
                payload.rewind()
                for pair in self.returned:
                    for value in pair:
                        emit_signed(self.output, value, self.width)
                self.output.rewind()
                self.pending = True
                return self.output

            def consume(self):
                require(self.pending, 'double has a protected return')
                self.output.clear()
                erase_marker(self.output)
                self.pending = False

        for lengths, selected, m in cases:
            layout = Layout(lengths, selected, m)
            expected = expected_indices(lengths, selected, m)
            # Metadata-only test fixture, explicitly not an admitted numerical
            # Reference. All numerical-source admissions are tested elsewhere.
            family = []
            for c in range(layout.labels):
                original_zero = expected.index(c << (layout.g*m))
                starts = [sum(lengths[:a]) for a in range(len(lengths))]
                entries = []
                for a in selected:
                    first = (original_zero >> starts[a]) & ((1 << lengths[a])-1)
                    entries.append(SimpleNamespace(first=first, size=1 << m,
                        reference=SimpleNamespace(target_size=1 << lengths[a]),
                        validate=lambda: None))
                family.append(tuple(reversed(entries)))
            width = 12
            prepared = implementation.PreparedRoutes(layout, family, width)
            root, _ = check_composed.fixture('standard', False)
            with patch.object(implementation, 'CompleteCore', SemanticCoreDouble):
                owner = implementation.OriginalCore(root)
            owner.core.width = width
            inputs = tuple((3*i-100, 101-5*i) for i in range(1 << layout.n))
            packed = [None] * len(inputs)
            for old, new in enumerate(expected):
                packed[new] = inputs[old]
            tagged = tuple((111+7*i, -333+11*i) for i in range(len(inputs)))
            owner.core.returned = tagged
            expected_output = tuple(tagged[expected[old]] for old in range(len(inputs)))
            payload = Tape()
            for pair in inputs:
                for value in pair:
                    emit_signed(payload, value, width)
            payload.rewind()
            controls = tuple(Tape() for _ in range(5))
            ip = tuple(Count.literal(layout.n if i == 0 else 1) for i in range(16))
            fp = tuple(Count.literal(layout.n if i == 0 else 1) for i in range(16))
            up = tuple(Count.literal(x) for x in (layout.g, 1 << m, m, 1, width, 1))
            ports = (payload, prepared.forward, prepared.inverse, *controls,
                     *(v.tape for v in (*prepared.parameters, *ip, *fp, *up)))
            before = snapshot(ports)
            returned = owner.run(payload, prepared.forward, prepared.inverse,
                prepared.parameters, *controls, ip, fp, up)
            actual = decode(returned, width)
            require(owner.core.received == tuple(packed), 'original to packed full field')
            require(actual == expected_output, 'packed to original full field')
            require(snapshot(ports) == before, 'all borrowed ports restored')
            require(owner.calls['gathers'] == 2, 'exactly two paid global boundaries')
            owner.consume()
            owner.idle()
            require(all(t.head == 1 and all(x == BLANK for x in t.cells)
                        for t in (*owner.pool.tapes, owner.output, owner.core.output)),
                    'outer/double owned roles blank, native roles separately inherited')
            require(tuple(packed) != inputs, 'nonidentity original-coordinate fixture')
            require(tagged != expected_output, 'inverse route is observable')
            results.append(dict(lengths=lengths, selected=selected, local_bits=m,
                records=len(inputs), labels=layout.labels, global_routes=owner.calls['gathers'],
                output_sha256=sha256(repr(actual).encode()).hexdigest()))
            if len(results) == 1:
                # Execute deliberate omissions on the actual outer wrapper.
                # These affect transport only; no numerical provider is used.
                original_gather = owner.gather
                for skip in (1, 2):
                    calls = [0]
                    def omit_one(*call_args):
                        calls[0] += 1
                        if calls[0] != skip:
                            return original_gather(*call_args)
                    with patch.object(owner, 'gather', omit_one):
                        wrong_return = owner.run(payload, prepared.forward, prepared.inverse,
                            prepared.parameters, *controls, ip, fp, up)
                    wrong_output = decode(wrong_return, width)
                    failed = (owner.core.received != tuple(packed) if skip == 1
                              else wrong_output != expected_output)
                    require(failed, 'independent oracle must detect omitted boundary')
                    rejected_controls.append('omitted first route' if skip == 1 else 'omitted inverse route')
                    owner.consume()
                    require(snapshot(ports) == before, 'negative-control borrowed ports restored')
                for invalid, label in ((family[:-1], 'missing coarse context'),
                                       ([tuple(SimpleNamespace(first=p.first+1, size=p.size,
                                           reference=p.reference, validate=p.validate) for p in family[0])]
                                        + family[1:], 'wrong original window origin')):
                    try:
                        implementation.PreparedRoutes(layout, invalid, width)
                    except ValueError:
                        rejected_controls.append(label)
                    else:
                        raise ValueError('invalid original source binding was accepted')
            for value in (*ip, *fp, *up):
                value.close()
                erase_marker(value.tape)
            prepared.close()
            for t in (payload, *controls):
                t.clear()
                erase_marker(t)
        receipt = dict(status='PASS_INDEPENDENT_ORIGINAL_COORDINATE_BOUNDARIES',
            scope='actual wrapper and global routers; explicit semantic Core double; no numerical claim',
            cases=results, implementation_sha256=sha256((package/'original_layout.py').read_bytes()).hexdigest(),
            negative_controls=rejected_controls)
        Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
        print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
