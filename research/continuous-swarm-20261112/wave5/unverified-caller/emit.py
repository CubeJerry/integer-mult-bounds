#!/usr/bin/env python3
"""Lossless, lazy metadata for the actual #7000 complex caller.

No payload is read or moved by this module. Every emitted operator has the
complete-array semantics in PROOF.md. In particular C means a completed
positive job, not a free callback; its physical implementation is excluded.
"""
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path

from geometry import (need, central_basis, stage_route, stage_axes, axis_order)

HERE = Path(__file__).resolve().parent
AMBIENT = 153
CENTRAL = tuple(range(9))


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def scalar(text):
    q = Fraction(text)
    need(q != 0, 'nonzero fixed scalar')
    return [q.numerator, q.denominator]


def bank(owner):
    """Physical logical-bank identity; lifetime is retained in the full owner."""
    if owner[0] == 'owned':
        return tuple(owner[:3])
    if owner[0] == 'aux':
        return tuple(owner[:2])
    return tuple(owner)


class SelectedStream:
    def __init__(self, directory=HERE):
        self.directory = Path(directory)
        reference = self.directory / 'reference'
        pins = json.loads((self.directory / 'SOURCES.json').read_text())
        for pin in pins['files']:
            if 'local_path' in pin:
                need(hashlib.sha256((self.directory / pin['local_path']).read_bytes()).hexdigest()
                     == pin['sha256'], 'source bytes: ' + pin['path'])
            if 'extracted_path' in pin:
                need(hashlib.sha256((self.directory / pin['extracted_path']).read_bytes()).hexdigest()
                     == pin['extracted_sha256'], 'retained authenticated q-basis extract')
        self.word = json.loads(gzip.decompress((reference / 'word.json.gz').read_bytes()))
        self.caller = json.loads((reference / 'caller.json').read_text())
        self.bases = {int(q): v for q, v in json.loads((reference / 'q-bases.json').read_text()).items()}
        catalogue = json.loads(gzip.decompress((self.directory / 'catalogue.json.gz').read_bytes()))
        self.recipes = {(a, b): recipe for a, b, recipe in catalogue['maps']}
        self.boundaries = {q: (a['left'], b['left']) for q, a, b in catalogue['main']}
        for i, (start, stop) in enumerate(((0, 1000), (1000, 2000), (2000, 3057))):
            text = (reference / f'native-catalogue-{i}.log').read_text()
            receipt = json.loads(text[text.index('{'):])
            need(hashlib.sha256(encoded(catalogue['maps'][start:stop])).hexdigest()
                 == receipt['exact_recipe_digest'], 'complete accepted native recipe bytes')
            if i == 2:
                need(hashlib.sha256(encoded(catalogue['main'])).hexdigest()
                     == receipt['main_boundary_digest'], 'accepted main boundary bytes')
        W, C = self.word, self.caller
        self.second = dict(zip(W['hosted']['Dports'], zip(W['hosted']['X2'], W['hosted']['Y2'])))
        self.main_slots = set(W['live']) | {x+112 for x in W['live']}
        self.main_slots |= set(W['hosted']['X2']) | set(W['hosted']['Y2'])
        self.helpers = sorted(set(range(W['public']))-self.main_slots)
        self.central_routes = {q: central_basis(q, self.bases[q]) for q in W['ports']}
        self.stage_routes = {q: stage_route(q, self.bases[q]) for q in W['ports']}
        need(len(W['program']) == 71261 and len(C['events']) == 3095, 'actual source sizes')
        need(len(self.main_slots) == 400 and len(self.helpers) == 1080, 'actual native slots')
        need(len(self.recipes) == 3057 and len(self.boundaries) == 104, 'complete finite catalogue')
        need(C['ambient_rank'] == AMBIENT and C['stages'] == 18, 'selected ambient')
        need([e[1] for e in C['events'] if e[0] == 'J'] == list(range(1, 19)), 'selected chronology')

    def record(self, op, owner, source, raw, part, *, chart_in='caller', chart_out='caller', **data):
        return dict(op=op, owner=list(owner), source=list(source), raw=raw, part=part,
                    chart_in=chart_in, chart_out=chart_out, ambient=AMBIENT, **data)

    def mono(self, owner, source, raw, part, recipe, inverse=False, **contact):
        return self.record('MONOMIAL', owner, source, raw, part, axes=list(CENTRAL),
                           recipe=recipe, inverse=inverse, tensor='bit-lane', **contact)

    def affine(self, owner, source, raw, part, axes, rows, offset=0, inverse=False, **contact):
        return self.record('AFFINE', owner, source, raw, part, axes=list(axes), rows=list(rows),
                           offset=offset, inverse=inverse, tensor='bit-lane', **contact)

    def permute(self, owner, source, raw, part, order, inverse=False, **contact):
        return self.record('AXIS_PERMUTATION', owner, source, raw, part, order=list(order),
                           inverse=inverse, tensor='bit-lane', **contact)

    def translate(self, owner, source, raw, part, q, **contact):
        return self.record('TRANSLATION', owner, source, raw, part, axes=list(CENTRAL),
                           offset=q, tensor='bit-lane', **contact)

    def targets(self):
        W, C = self.word, self.caller
        for ty in ('A', 'B'):
            d = C['types'][ty]
            for i, diagonal in enumerate(d['diagonal']):
                qp, zero, *mask = diagonal
                need(qp in (-1, 0, 1) and zero == 0 and len(mask) == 18
                     and set(mask) <= {0, 1} and any(mask), 'actual positive root target')
                for pi in d['ports']:
                    yield ['main', pi, d['offset']+i], abs(qp)+8*sum(mask)
        for ci, e in enumerate(C['events']):
            if e[0] == 'J':
                for r in self.helpers:
                    yield ['helper', ci, r], len(W['frames'][W['final'][r]])-len(W['frames'][W['initial'][r]])

    def root_boundaries(self, entrance):
        """Explicit canonical whole-job input/output charts for root owners."""
        W, C = self.word, self.caller
        for ty in ('A', 'B'):
            kind = C['types'][ty]
            for i, diagonal in enumerate(kind['diagonal']):
                qp, _, *mask = diagonal
                selected = ([0] if qp else []) + list(stage_axes([j+1 for j, yes in enumerate(mask) if yes]))
                order = axis_order(selected)
                role = kind['offset']+i
                rank = len(selected)
                for pi in kind['ports']:
                    owner = ['main', pi, role]
                    q = W['ports'][pi]
                    provenance = ['root', ty, i, pi]
                    raw = [ty, 'DIAGONAL', role, diagonal]
                    if entrance:
                        yield self.permute(owner, provenance, raw, 'root-input-axis-order', order,
                            chart_in=['target-input', rank], chart_out=['root-route', rank] if qp else 'caller')
                        if qp:
                            yield self.affine(owner, provenance, raw, 'root-input-q-basis', CENTRAL,
                                self.central_routes[q], chart_in=['root-route', rank])
                    else:
                        if qp == -1:
                            yield self.translate(owner, provenance, raw, 'root-negative-q-correction', q)
                        if qp:
                            yield self.affine(owner, provenance, raw, 'root-output-q-basis', CENTRAL,
                                self.central_routes[q], inverse=True, chart_out=['root-route', rank])
                        yield self.permute(owner, provenance, raw, 'root-output-axis-order', order, inverse=True,
                            chart_in=['root-route', rank] if qp else 'caller', chart_out=['target-output', rank])

    def mapping(self, ci, event):
        W = self.word
        _, _, plane_a, plane_b = event
        need(len(set(plane_a)) == 4 and len(set(plane_b[:2])) == 2, 'distinct main roles')
        mapping = {}
        for pi, x in enumerate(W['live']):
            pair = plane_a[:2] if pi in self.second else plane_b[:2]
            mapping[x], mapping[x+112] = ['main', pi, pair[0]], ['main', pi, pair[1]]
            if pi in self.second:
                x2, y2 = self.second[pi]
                mapping[x2], mapping[y2] = ['main', pi, plane_a[2]], ['main', pi, plane_a[3]]
        mapping.update({r: ['helper', ci, r] for r in self.helpers})
        need(len(mapping) == len({tuple(x) for x in mapping.values()}) == W['public'],
             'actual native public mapping is injective')
        return mapping

    def native_call(self, ci, event):
        W = self.word
        mapping = self.mapping(ci, event)
        stage = event[1]
        source = [ci, 'boundary']
        stage_support = CENTRAL + stage_axes([stage])
        # Every public field, including independent helper inputs, is normalized
        # before the body. No helper normalizer is moved inside a paid MOVE.
        for pi, x in enumerate(W['live']):
            q = W['ports'][pi]
            pairs = [(x, x+112)] + ([self.second[pi]] if pi in self.second else [])
            rows, _ = self.stage_routes[q]
            for a, b in pairs:
                for r in (a, b):
                    yield self.affine(mapping[r], source+[r], event, 'main-stage-entry', stage_support,
                        rows, chart_out=['main-entry', ci, r] if r == a else ['native', W['initial'][r]])
                yield self.mono(mapping[a], source+[a], event, 'main-input-normalizer', self.boundaries[q][0],
                    chart_in=['main-entry', ci, a], chart_out=['native', W['initial'][a]])
        for r in self.helpers:
            a, b = W['initial'][r], W['final'][r]
            recipe = self.recipes[(a, b)]
            yield self.mono(mapping[r], source+[r], event, 'helper-inverse-right', recipe['right'], inverse=True,
                chart_in=['target-input', recipe['rank']], chart_out=['native', a])
        for r in range(W['public']):
            frame = ['native', W['initial'][r]]
            yield self.record('SCALE', mapping[r], source+[r], event, 'scale-1125', coefficient=[1125, 1],
                scalar_scope='outside-tensor', chart_in=frame, chart_out=frame)

        frames = dict(enumerate(W['initial']))
        untouched = set()
        active_owned = set()
        for ni, raw in enumerate(W['program']):
            op, r = raw[:2]
            provenance = [ci, ni]
            if op == 'INIT':
                need(r >= W['public'] and r not in frames, 'fresh owned INIT')
                mapping[r] = ['owned', ci, r-W['public'], ni]
                frames[r] = raw[2]
                untouched.add(r)
                active_owned.add(r)
                yield self.record('INIT', mapping[r], provenance, raw, 'native', zero=True,
                    chart_in='inactive', chart_out=['native', raw[2]])
                continue
            need(r in frames, 'live native destination')
            owner = mapping[r]
            if op == 'CLEAR':
                need(r in active_owned and frames[r] == raw[2], 'typed owned CLEAR')
                yield self.record('CLEAR', owner, provenance, raw, 'native',
                    chart_in=['native', raw[2]], chart_out='inactive')
                del frames[r]
                del mapping[r]
                active_owned.remove(r)
                untouched.discard(r)
            elif op == 'MOVE':
                _, _, a, b, owned = raw
                need(frames[r] == a and owned == (r >= W['public']), 'typed actual MOVE')
                recipe = self.recipes[(a, b)]
                k = recipe['rank']
                child_in, child_out = ['child-input', ci, ni], ['child-output', ci, ni]
                yield self.mono(owner, provenance, raw, 'move-right', recipe['right'],
                    chart_in=['native', a], chart_out=child_in)
                yield self.record('C', owner, provenance, raw, 'move-child', rank=k,
                    axes=list(range(k)), tensor='bit-lane', completed_return=True,
                    projection=[ci, ni, list(bank(owner)), k, a, b],
                    chart_in=child_in, chart_out=child_out)
                yield self.mono(owner, provenance, raw, 'move-left', recipe['left'],
                    chart_in=child_out, chart_out=['native', b])
                frames[r] = b
                untouched.discard(r)
            elif op == 'SCALE':
                need(frames[r] == raw[3], 'typed native SCALE')
                chart = ['native', raw[3]]
                yield self.record('SCALE', owner, provenance, raw, 'native', coefficient=scalar(raw[2]),
                    scalar_scope='outside-tensor', chart_in=chart, chart_out=chart)
                untouched.discard(r)
            else:
                need(op in ('ADD', 'COPY'), 'actual native event grammar')
                s, coeff, frame = raw[2:]
                need(s in frames and s != r and frames[r] == frames[s] == frame, 'typed scalar contact')
                if op == 'COPY':
                    need(r in untouched and scalar(coeff) == [1, 1], 'COPY only into initialized zero')
                chart = ['native', frame]
                yield self.record('ADD', owner, provenance, raw, 'native', from_owner=list(mapping[s]),
                    coefficient=scalar(coeff), scalar_scope='outside-tensor',
                    initialized_copy=(op == 'COPY'), chart_in=chart, chart_out=chart)
                untouched.discard(r)
        need(not active_owned and [frames[r] for r in range(W['public'])] == W['final'],
             'complete native lifecycle and final charts')
        for r in range(W['public']):
            chart = ['native', W['final'][r]]
            yield self.record('SCALE', mapping[r], source+[r], event, 'unscale-1125', coefficient=[1, 1125],
                scalar_scope='outside-tensor', chart_in=chart, chart_out=chart)
        for r in self.helpers:
            a, b = W['initial'][r], W['final'][r]
            recipe = self.recipes[(a, b)]
            yield self.mono(mapping[r], source+[r], event, 'helper-inverse-left', recipe['left'], inverse=True,
                chart_in=['native', b], chart_out=['target-output', recipe['rank']])
        for pi, x in enumerate(W['live']):
            q = W['ports'][pi]
            pairs = [(x, x+112)] + ([self.second[pi]] if pi in self.second else [])
            rows, shift = self.stage_routes[q]
            for a, b in pairs:
                yield self.mono(mapping[b], source+[b], event, 'main-output-normalizer', self.boundaries[q][1],
                    chart_in=['native', W['final'][b]], chart_out=['main-exit', ci, b])
                for r in (a, b):
                    yield self.affine(mapping[r], source+[r], event, 'main-stage-exit', stage_support,
                        rows, offset=shift, chart_in=['native', W['final'][r]] if r == a else ['main-exit', ci, r])

    def outer(self, ci, raw):
        ty, op, role, *args = raw
        kind = self.caller['types'][ty]
        for pi in kind['ports']:
            owner = ['main', pi, role]
            provenance = [ci, 'outer', pi]
            q = self.word['ports'][pi]
            if op == 'ADD':
                yield self.record('ADD', owner, provenance, raw, 'outer',
                    from_owner=['main', pi, args[0]], coefficient=scalar(args[1]),
                    scalar_scope='outside-tensor', initialized_copy=False)
            elif op == 'SCALE':
                yield self.record('SCALE', owner, provenance, raw, 'outer', coefficient=scalar(args[0]),
                    scalar_scope='outside-tensor')
            elif op == 'SWAP':
                yield self.record('SWAP', owner, provenance, raw, 'outer', other_owner=['main', pi, args[0]],
                    semantics='exchange-full-values-retain-banks')
            elif op == 'QUERY':
                src, sign = args
                need(sign in (-1, 1), 'query sign')
                scratch = ['aux', 0, 'QUERY', ci, pi]
                yield self.record('INIT', scratch, provenance, raw, 'query-init', zero=True,
                    chart_in='inactive', chart_out='caller')
                yield self.record('ADD', scratch, provenance, raw, 'query-copy-by-add',
                    from_owner=['main', pi, src], coefficient=[1, 1], scalar_scope='outside-tensor', initialized_copy=True)
                yield self.affine(scratch, provenance, raw, 'query-input-basis', CENTRAL,
                    self.central_routes[q], inverse=True, chart_out=['query-child-input', ci, pi])
                yield self.record('C', scratch, provenance, raw, 'query-child', rank=1, axes=[0],
                    tensor='bit-lane', completed_return=True,
                    projection=[ci, 'QUERY', ['query_scratch', ci, pi], 1],
                    chart_in=['query-child-input', ci, pi], chart_out=['query-child-output', ci, pi])
                yield self.affine(scratch, provenance, raw, 'query-output-basis', CENTRAL, self.central_routes[q],
                    chart_in=['query-child-output', ci, pi])
                if sign == -1:
                    yield self.translate(scratch, provenance, raw, 'query-negative-correction', q)
                yield self.record('ADD', owner, provenance, raw, 'query-add-back', from_owner=scratch,
                    coefficient=[1, 1], scalar_scope='outside-tensor', initialized_copy=False)
                yield self.record('CLEAR', scratch, provenance, raw, 'query-clear', chart_out='inactive')
            elif op == 'IDLE_ONE':
                axes = stage_axes(args[0])
                order = axis_order(axes)
                yield self.permute(owner, provenance, raw, 'idle-input-basis', order, inverse=True,
                    chart_out=['idle-child-input', ci, pi])
                yield self.record('C', owner, provenance, raw, 'idle-child', rank=len(axes), axes=list(range(len(axes))),
                    tensor='bit-lane', completed_return=True,
                    projection=[ci, 'IDLE_ONE', owner, len(axes)],
                    chart_in=['idle-child-input', ci, pi], chart_out=['idle-child-output', ci, pi])
                yield self.permute(owner, provenance, raw, 'idle-output-basis', order,
                    chart_in=['idle-child-output', ci, pi])
            elif op == 'LAMBDA':
                sign = args[0]
                need(sign in (-1, 1), 'lambda sign')
                scratch = ['aux', 0, 'LAMBDA', ci, pi]
                yield self.record('INIT', scratch, provenance, raw, 'lambda-init', zero=True,
                    chart_in='inactive', chart_out='caller')
                yield self.record('ADD', scratch, provenance, raw, 'lambda-copy-by-add', from_owner=owner,
                    coefficient=[1, 1], scalar_scope='outside-tensor', initialized_copy=True)
                yield self.translate(scratch, provenance, raw, 'lambda-translation', q)
                yield self.record('GAUSSIAN_INTEGER', owner, provenance, raw, 'lambda-first-numerator',
                    matrix=[[1, -sign], [sign, 1]], scalar_scope='outside-tensor')
                yield self.record('GAUSSIAN_INTEGER', scratch, provenance, raw, 'lambda-second-numerator',
                    matrix=[[1, sign], [-sign, 1]], scalar_scope='outside-tensor')
                yield self.record('ADD', owner, provenance, raw, 'lambda-sum-numerators', from_owner=scratch,
                    coefficient=[1, 1], scalar_scope='outside-tensor', initialized_copy=False)
                yield self.record('SCALE', owner, provenance, raw, 'lambda-final-half', coefficient=[1, 2],
                    scalar_scope='outside-tensor')
                yield self.record('CLEAR', scratch, provenance, raw, 'lambda-clear', chart_out='inactive')
            else:
                raise ValueError('unknown actual caller opcode: ' + op)

    def records(self, root_charts=True):
        if root_charts:
            yield from self.root_boundaries(True)
        for ci, event in enumerate(self.caller['events']):
            if event[0] == 'J':
                yield from self.native_call(ci, event)
            else:
                yield from self.outer(ci, event)
        if root_charts:
            yield from self.root_boundaries(False)


def paid_digest(records):
    """Streaming canonical JSON-array digest, equal to the reviewer's digest."""
    h = hashlib.sha256()
    h.update(b'[')
    count = 0
    for record in records:
        if record['op'] == 'C':
            if count:
                h.update(b',')
            h.update(encoded(record['projection']))
            count += 1
    h.update(b']')
    return count, h.hexdigest()


if __name__ == '__main__':
    count, digest = paid_digest(SelectedStream().records())
    print(json.dumps(dict(paid_positions=count, complete_paid_position_digest=digest), indent=2))
