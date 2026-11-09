"""Independent current-format phase observer on sparse physical hardware.

Imports the production adapter, never its fixture or address oracle. Checks
small current-format joins, suffix coefficients and signed retries; does not
independently establish the inherited phase/Compact theorem.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from types import SimpleNamespace

SCHEMA = ('outer', 'rows', 'stock', 'row_bits', 'within_bits', 'record_bits',
          'p', 'd', 'K', 'G', 'H', 'q0', 'qF', 'qB', 'D', 'f', 'rho',
          'active_start', 'back_start', 'selected_axes', 'entry_start',
          'remainder', 'cutoff')


def require(ok, message):
    if not ok:
        raise ValueError(message)


class SparseTape:
    def __init__(self, origin):
        self.origin = self.head = origin
        self.cells = {i: (i + origin) % 2 for i in range(origin - 1)}
        self.cells[origin - 1] = 2
        self.operations = 0
        self.high = origin

    def read(self):
        self.operations += 1
        return self.cells.get(self.head, 6)

    def write(self, value):
        require(type(value) is int and 0 <= value < 7, 'physical alphabet')
        self.operations += 1
        self.high = max(self.high, self.head + 1)
        if value == 6:
            self.cells.pop(self.head, None)
        else:
            self.cells[self.head] = value

    def move(self, direction):
        require(direction in (-1, 1), 'one physical head step')
        self.operations += 1
        self.head += direction
        require(self.head >= 0, 'one-sided physical tape')

    def install(self, bits):
        for position in tuple(self.cells):
            if position >= self.origin:
                self.cells.pop(position)
        self.cells.update((self.origin + i, bit) for i, bit in enumerate(bits))
        self.head = self.origin
        self.high = max(self.high, self.origin + len(bits))

    def body(self):
        return {position - self.origin: value for position, value in self.cells.items()
                if position >= self.origin}

    def prefix(self):
        return tuple(self.cells.get(i, 6) for i in range(self.origin))


def triple(symbol):
    return (symbol // 4, (symbol // 2) % 2, symbol % 2)


def encode_pairs(records, h):
    out = []
    for coefficients in records:
        for real, imaginary in coefficients:
            for value in (real, imaginary):
                require(-(2 ** (h - 1)) <= value < 2 ** (h - 1), 'oracle signed range')
                for position in range(h):
                    out.extend(triple((value % (2 ** h) // (2 ** position)) % 2))
                out.extend((0, 1, 0))
    return out


def encode_header(values):
    out = []
    for name in SCHEMA:
        value = values[name]
        length = max(1, value.bit_length())
        out.extend([1] * length + [0])
        out.extend((value // (2 ** i)) % 2 for i in range(length))
    return out


def phase_action(real, imaginary, power):
    for _ in range(power % 4):
        real, imaginary = -imaginary, real
    return real, imaginary


def fixture(*, columns=1, spacing=2, residue=0, tail=0, row_count=1,
            component=3, coefficient_count=2, linear=3, toggle=False,
            inverse=False, extrema=False, reject=False):
    # Rank one isolates this format/phase boundary; there is no ordinary call.
    # Selected rank-nine MOVE and full Compact are outside this observer.
    front = 1
    start = 2 * front
    back = start + columns * spacing
    address_bits = back + front + tail
    per_row = 2 ** address_bits
    record_bits = 6 * coefficient_count * (component + 1)
    values = dict(outer=1, rows=row_count, stock=1,
                  row_bits=record_bits * per_row, within_bits=address_bits,
                  record_bits=record_bits, p=max(2, columns), d=columns,
                  K=spacing, G=1, H=front, q0=3, qF=0, qB=0, D=columns,
                  f=columns, rho=residue, active_start=start, back_start=back,
                  selected_axes=columns, entry_start=start, remainder=0, cutoff=1)
    literal = dict(matrix_rows=(1,), offset=int(toggle), linear_Z4=(linear,),
                   quadratic_rows=(0,), phase=1)
    positions = [address_bits - 1 - start - j * spacing - residue
                 for j in range(columns)]
    mask = sum(2 ** bit for bit in positions)

    def rule(address):
        digits = sum((address // (2 ** bit)) % 2 for bit in positions)
        phase = (columns + linear * digits) % 4
        return (address ^ mask if toggle else address), phase

    bound = 2 ** (component - 1) - 1
    modulus = 2 * bound + 1
    initial = [[((i + 3 * c) % modulus - bound,
                 (2 * (i // modulus) + 5 * c) % modulus - bound)
                for c in range(coefficient_count)]
               for i in range(row_count * per_row)]
    if extrema:
        require(not inverse and not toggle, 'extrema fixture at original addresses')
        one = next(i for i in range(per_row) if rule(i)[1] == 1)
        zero = next(i for i in range(per_row) if rule(i)[1] == 0)
        initial[one][0] = (-(bound + 1), 1)
        initial[zero][-1] = (-(bound + 1), -(bound + 1))
    if reject:
        require(not inverse and not toggle, 'headroom rejection at original address')
        late = max(i for i in range(row_count * per_row) if rule(i % per_row)[1] == 1)
        real, _imaginary = initial[late][-1]
        initial[late][-1] = (real, -(bound + 1))

    expected = [None] * len(initial)
    if not reject:
        for row in range(row_count):
            for address in range(per_row):
                destination, phase = rule(address)
                if inverse:
                    source, target, sign = destination, address, -1
                else:
                    source, target, sign = address, destination, 1
                expected[row * per_row + target] = [phase_action(real, imag, sign * phase)
                    for real, imag in initial[row * per_row + source]]
    return values, literal, encode_pairs(initial, component), (
        None if reject else encode_pairs(expected, component))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    package = Path(args.package).resolve()
    source_names = ('phase_adapter.py', 'phase_binding.py')
    source_pins = {name: sha256((package / name).read_bytes()).hexdigest()
                   for name in source_names}
    sys.path.insert(0, str(package))
    import phase_adapter as prod
    from ordinary import Ordinary
    from macro_code import Code
    require(tuple(prod.SCHEMA) == SCHEMA, 'independent exact twenty-three-field order')

    def native_factory():
        return Ordinary(2, SimpleNamespace(codes=SimpleNamespace(q=2)),
                        SimpleNamespace(families=0), (Code((('unreachable',),), 0),), capacity=64)

    report = []
    controls = []

    def run(label, case, previous=None, provider_type=prod.Provider, expect_wrong=False,
            expected_error=None):
        values, literal, initial, expected = fixture(**case)
        if previous is None:
            owner = provider_type(literal, native_factory, case.get('inverse', False))
            work = [SparseTape(3 + i % 5) for i in range(owner.port_count)]
            field, context = SparseTape(9), SparseTape(17)
            owner.bind(work)
        else:
            owner, work, field, context = previous
        field.install(initial)
        header = encode_header(values)
        context.install(header)
        tapes = [*work, field, context]
        prefixes = [t.prefix() for t in tapes]
        before = sum(t.operations for t in tapes)
        original_compact = dict(owner.engine.compact.calls)
        error = None
        try:
            owner.run(prod.S.abi.CodedPort(field), prod.S.abi.BinaryContextPort(context))
        except prod.S.phase.SignedHeadroomError:
            error = 'headroom'
        except ValueError as exc:
            error = str(exc)
        if expected_error is not None:
            require(error is not None and expected_error in error, label + ': exact injected error')
            controls.append(label)
            return None
        require(error == ('headroom' if case.get('reject') else None), label + ': signed guard outcome')
        wanted = initial if case.get('reject') else expected
        equal = field.body() == dict(enumerate(wanted))
        require(not equal if expect_wrong else equal, label + ': independent complete physical result')
        require(context.body() == dict(enumerate(header)), label + ': unchanged complete context')
        require(field.head == field.origin and context.head == context.origin, label + ': public origins')
        require(all(t.head == t.origin and not t.body() for t in work), label + ': blank private bodies')
        require([t.prefix() for t in tapes] == prefixes, label + ': ancestor prefixes')
        require(owner.engine.closed and not owner.pool.live and not owner.engine.pool.live,
                label + ': successful/rejected owner is reusable')
        require(dict(owner.engine.compact.calls) == original_compact, label + ': no hidden ordinary call')
        actions = sum(t.operations for t in tapes) - before
        row = dict(case=label, options=case, records=values['rows'] * 2 ** values['within_bits'],
                   physical_bits=len(initial), actions=actions, work_ports=owner.port_count,
                   headroom_rejected=error == 'headroom', output_sha256=sha256(bytes(wanted)).hexdigest())
        if expect_wrong:
            controls.append(label)
        else:
            report.append(row)
        return (owner, work, field, context), actions

    run('rho_zero_and_allowed_signed_minima', dict(extrema=True))
    run('rho_one_nonpower_rows_and_two_suffix_bits', dict(residue=1, row_count=3, tail=1))
    run('two_columns_global_phase_and_folded_suffix', dict(columns=2, spacing=1, tail=1, linear=1))
    run('inverse_toggle_source_address_phase', dict(toggle=True, inverse=True, linear=1))
    state, first_actions = run('headroom_baseline', {})
    state, _ = run('late_folded_field_headroom_rejection', dict(reject=True), previous=state)
    _state, retry_actions = run('valid_retry_after_headroom', {}, previous=state)
    require(retry_actions == first_actions, 'rejection history does not alter a valid retry bill')

    class WrongRho(prod.Provider):
        def prepare(self, header, h, cleanup):
            widths, _rho, coefficients, rows = super().prepare(header, h, cleanup)
            wrong = prod.Count(header['rho'])
            cleanup.callback(wrong.close)
            return widths, wrong, coefficients, rows

    run('unconverted_current_rho_changes_physical_endpoint', {},
        provider_type=WrongRho, expect_wrong=True)

    class LostSuffix(prod.Provider):
        def prepare(self, header, h, cleanup):
            widths, rho, _coefficients, rows = super().prepare(header, h, cleanup)
            wrong = prod.Count.literal(2)
            cleanup.callback(wrong.close)
            return widths, rho, wrong, rows

    run('discarded_suffix_coefficients_fail_complete_packet', dict(tail=1),
        provider_type=LostSuffix, expected_error='complete Gaussian monomial packet')
    require(all(sha256((package / name).read_bytes()).hexdigest() == source_pins[name]
                for name in source_names), 'production sources stayed frozen during review')
    receipt = dict(scope='Independent current coded-format and suffix/phase join on small rank-one packets',
                   phase_adapter_sha256=source_pins['phase_adapter.py'],
                   phase_binding_sha256=source_pins['phase_binding.py'],
                   cases=report, negative_controls=controls,
                   limitation='No independent old phase/Compact theorem, selected rank-nine execution or faster-rate admission',
                   status='PASS_INDEPENDENT_CURRENT_PHASE_FORMAT')
    Path(args.output).write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
