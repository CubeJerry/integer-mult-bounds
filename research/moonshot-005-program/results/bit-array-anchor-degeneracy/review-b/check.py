#!/usr/bin/env python3
"""Independent dense-inverse audit of the native array-anchor polynomials.

Reuses the pinned independent stdlib GF64 multiplication table only. Native
adjugate columns are obtained by dense elimination, not RS interpolation.
"""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

PINS = {
    'sources': ('bit-array-anchor-degeneracy/SOURCE-PINS.json', '2bdffd4fb6d81284e39b9938ead06d0106116d41a84b4846dbc342f7a6102207'),
    'proof': ('bit-array-anchor-degeneracy/author/PROOF.md', '308e65f7dfd5e0f5e7227e236012bba6627fdea94e1be93dc89e88734dea85e7'),
    'author_checker': ('bit-array-anchor-degeneracy/author/check.py', '7d5671b6066bb5ad234d90715c665cb76a7f089f98773f06cf320e48c5c68946'),
    'author_result': ('bit-array-anchor-degeneracy/author/output/RESULT.json', '4bb1347e595566f55f5ac47d422362c3bada6b87a60e88d49e6c5314080ea565'),
    'independent_field': ('bit-rs-source-fibre-census/review-large-kappa/check.py', '2408c2321a112d6aff8d2ca9d0a54ea235572cf54cf9da6886cd9c60f8cfc489'),
}

def need(value, message):
    if not value:
        raise ValueError(message)

class Field:
    def __init__(self, earlier):
        self.mul = earlier.MUL; self.inv = earlier.INV

    def dot(self, a, b):
        result = 0
        for x, y in zip(a, b):
            result ^= self.mul[x][y]
        return result

    def power(self, a, n):
        result = 1
        while n:
            if n & 1:
                result = self.mul[result][a]
            a = self.mul[a][a]; n >>= 1
        return result

    def row(self, x):
        return [self.power(x, n) for n in range(16)]

    def inverse_det(self, matrix):
        n = len(matrix)
        need(all(len(row) == n for row in matrix), 'square native source matrix')
        rows = [list(row) + [int(i == j) for j in range(n)] for i, row in enumerate(matrix)]
        determinant = 1
        for col in range(n):
            pivot = next((i for i in range(n-1, col-1, -1) if rows[i][col]), None)
            need(pivot is not None, 'invertible native tensor RS view')
            rows[col], rows[pivot] = rows[pivot], rows[col]
            scalar = rows[col][col]; determinant = self.mul[determinant][scalar]
            rows[col] = [self.mul[self.inv[scalar]][x] for x in rows[col]]
            for r in range(n):
                if r == col or not rows[r][col]:
                    continue
                scale = self.mul[rows[r][col]]
                rows[r] = [x ^ scale[y] for x, y in zip(rows[r], rows[col])]
        need(all(row[:n] == [int(i == j) for j in range(n)] for i, row in enumerate(rows)), 'dense inverse reduces every original column')
        return tuple(tuple(row[n:]) for row in rows), determinant

    def det(self, matrix):
        # Reverse pivot order, independent of the author's forward elimination.
        rows = [list(row) for row in matrix]; n = len(rows)
        need(all(len(row) == n for row in rows), 'square selected minor')
        determinant = 1
        for col in range(n-1, -1, -1):
            pivot = next((i for i in range(col+1) if rows[i][col]), None)
            if pivot is None:
                return 0
            rows[col], rows[pivot] = rows[pivot], rows[col]
            scalar = rows[col][col]; determinant = self.mul[determinant][scalar]
            for r in range(col):
                scale = self.mul[rows[r][col]][self.inv[scalar]]
                if scale:
                    table = self.mul[scale]
                    rows[r] = [x ^ table[y] for x, y in zip(rows[r], rows[col])]
        return determinant

def main():
    cli = ArgumentParser(description=__doc__)
    cli.add_argument('--repo', type=Path, required=True); cli.add_argument('--out', type=Path, required=True)
    args = cli.parse_args(); args.out.mkdir(parents=True, exist_ok=True)
    base = args.repo/'research/moonshot-005-program/results'; payload = {}
    for key, (name, digest) in PINS.items():
        raw = (base/name).read_bytes()
        need(sha256(raw).hexdigest() == digest, 'review source pin ' + key); payload[key] = raw
    source_pins = json.loads(payload['sources'])
    for name, item in source_pins['files'].items():
        raw = (args.repo/name).read_bytes()
        need(len(raw) == item['bytes'] and sha256(raw).hexdigest() == item['sha256'], 'inherited physical and nonlinear premise pin ' + name)
    spec = importlib.util.spec_from_file_location('earlier_independent_GF64', base/PINS['independent_field'][0])
    earlier = importlib.util.module_from_spec(spec); spec.loader.exec_module(earlier); F = Field(earlier)
    geometry = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    certificate = json.loads(gzip.decompress((base/'bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz').read_bytes()))['witnesses']
    planes = list(map(frozenset, geometry['A2'])); roots = geometry['root_table']; native = set(range(111))
    perp = [{j for j, y in enumerate(roots) if sum(a*b for a, b in zip(x, y)) == 0} for x in roots]
    audience = [native.intersection(*(perp[j] for j in H)) for H in planes]
    stars = {j: [h for h, H in enumerate(planes) if j in H] for j in native}
    nodes = {j: {h: n+1 for n, h in enumerate(stars[j])} for j in native}
    views = {(j, r): [h for h in stars[j] if r in audience[h]] for j in native for r in perp[j] & native}
    singleton = {next(iter(H & native)) for H in planes if len(H & native) == 1}
    eligible = native-singleton-{10}
    need(len(eligible) == 99 and len(singleton) == 11 and len(views) == 6470, 'actual anchor and source-view universe')
    need(all(len(v) == 16 for v in views.values()) and all(len(s) == 28 for s in stars.values()), 'all source observation dimensions')
    root_index = {tuple(x): j for j, x in enumerate(roots)}
    root_index.update({tuple(-a for a in x): j for j, x in enumerate(roots)})
    @lru_cache(None)
    def reflection(c):
        permutation = []
        for x in roots:
            dot = sum(a*b for a, b in zip(x, roots[c]))
            doubled = [2*a-dot*b for a, b in zip(x, roots[c])]
            need(all(v % 2 == 0 for v in doubled), 'integral geometric reflection')
            image = tuple(v//2 for v in doubled)
            need(image in root_index, 'reflected root remains an actual line')
            permutation.append(root_index[image])
        need(len(set(permutation)) == 120, 'reflection permutation')
        return permutation
    node_rows = {x: F.row(x) for x in range(1, 29)}
    @lru_cache(None)
    def inverse_view(j, r):
        hs = views[j, r]
        need(r != 80, 'unmodified identity-target propagation receiver')
        M = tuple(tuple(node_rows[nodes[j][q]]) for q in hs)
        inverse, determinant = F.inverse_det(M)
        return hs, M, inverse, determinant
    @lru_cache(None)
    def adjugate_column(j, h, r):
        hs, M, inverse, determinant = inverse_view(j, r)
        need(h in hs, 'actual shared-plane insertion block')
        column = hs.index(h)
        C = tuple(F.mul[determinant][row[column]] for row in inverse)
        need([F.dot(row, C) for row in M] == [determinant if q == h else 0 for q in hs],
             'independent dense adjugate-column identity')
        return C, determinant
    expected = json.loads(payload['author_result']); summaries = []; minor_histogram = Counter()
    seen = set(); receivers_used = set(); duplicate_control = None; tensor_control = None
    for witness, published in zip(certificate, expected['witnesses']):
        j = witness['anchor']; k, l = witness['leaf_donors']; h1, h2, h3 = witness['centres']; i = witness['final_receiver']
        need(j in eligible and j not in seen and k in eligible and l in eligible and len({j,k,l}) == 3, 'three distinct eligible donor roles')
        need({j,k} <= planes[h1] and {j,l} <= planes[h2] and {k,l} <= planes[h3], 'literal triangle source incidences')
        need(i != 80 and i in audience[h3] and i not in perp[j], 'final receiver outside anchor star')
        seen.add(j); values = []; mapped = []; tensor_factor = 1
        need(len(witness['propagations']) == 2, 'two propagation arms')
        for branch, leaf, centre in zip(witness['propagations'], [k,l], [h1,h2]):
            need(branch['leaf'] == leaf and branch['centre'] == centre, 'actual propagation arm binding')
            third = planes[centre]-{j,leaf}; need(len(third) == 1, 'unique reflection line')
            permutation = reflection(next(iter(third)))
            need(permutation[j] == leaf and permutation[leaf] == j, 'actual leaf reflection')
            required = set(views[leaf,i])-{h3}; records = branch['quotient_propagations']
            need(len(required) == len(records) == 15 and centre not in required, 'fifteen off-final quotients')
            used = set(); found = []
            for entry in records:
                q = entry['leaf_plane']; R = entry['anchor_plane']; rr = entry['receivers']
                need(q in required and q not in used and R in stars[j] and R != centre, 'off-centre source observation')
                need({permutation[x] for x in planes[q]} == planes[R], 'actual reflected observation plane')
                need(len(rr) == len(set(rr)) == 15 and 80 not in rr, 'fifteen distinct admissible native receivers')
                need(set(rr) <= audience[centre] & audience[q] & audience[R], 'common visibility of H, Q and R')
                need(all(permutation[r] == r for r in rr), 'native receivers fixed by reflection')
                columns = []
                for r in rr:
                    C, determinant = adjugate_column(j, centre, r)
                    need(F.dot(node_rows[nodes[j][R]], C) == 0, 'propagation directions lie in the same anchor quotient kernel')
                    columns.append(C); tensor_factor = F.mul[tensor_factor][determinant]
                selected = [[C[row] for C in columns] for row in range(1,16)]
                minor = F.det(selected)
                need(minor != 0, 'chosen propagation minor is nonzero')
                values.append(minor); minor_histogram[minor] += 1; found.append(R); used.add(q); receivers_used.update(rr)
                if duplicate_control is None:
                    broken = [row[:-1] + [row[0]] for row in selected]
                    need(F.det(broken) == 0, 'duplicate propagation column negative control')
                    duplicate_control = {'anchor': j, 'centre': centre, 'leaf_plane': q, 'correct_minor': minor, 'fault_minor': 0}
                    tensor_control = {'anchor': j, 'centre': centre, 'receivers': rr, 'scalar_minor': minor}
            need(used == required and len(set(found)) == 15, 'exact complete quotient propagation')
            mapped.append(found)
        need(mapped == witness['distinct_anchor_plane_sets'] and len(values) == 30, 'thirty literal propagation records')
        A,B = map(set,mapped); union = sorted(A|B)
        need(len(A&B) == 10 and len(union) == 20, 'final twenty-plane observation set')
        chosen = union[:16]; matrix = [node_rows[nodes[j][q]] for q in chosen]
        final = F.det(matrix); need(final, 'selected final sixteen-plane minor nonzero')
        need(F.det(matrix[:-1]+[matrix[0]]) == 0, 'duplicate final-plane negative control')
        delta = final
        for value in values:
            delta = F.mul[delta][value]
        need(delta != 0, 'entire necessary polynomial has a nonzero scalar RS value')
        row = {'anchor': j, 'quotient_width_checked': 1, 'propagation_minor_values': values,
               'final_sixteen_planes': chosen, 'final_determinant': final, 'polynomial_value': delta}
        need(row == published, 'every scalar value agrees with the frozen receipt')
        row['tensor_determinant_factor'] = tensor_factor
        row['tensor_values_from_proved_formula'] = {str(t): F.mul[F.power(delta,t)][F.power(tensor_factor,t*(t-1))] for t in (2,3,240)}
        need(all(row['tensor_values_from_proved_formula'].values()), 'nonzero tensor witness values')
        summaries.append(row)
    need(seen == eligible and len(certificate) == len(expected['witnesses']) == len(summaries) == 99, 'all ninety-nine anchors')
    need(sum(minor_histogram.values()) == 2970 and adjugate_column.cache_info().currsize == 5960, 'all native polynomial minors and columns')
    need({str(k): v for k,v in sorted(minor_histogram.items())} == expected['nonzero_minor_value_histogram'], 'entire scalar-minor histogram')
    need(singleton <= receivers_used, 'singleton donor labels are permitted as receivers')
    # A small direct tensor control validates the row-order and scaling formula.
    # The unbounded positive-width assertion is proved separately in REVIEW.md.
    tensor_checks = {}; j = tensor_control['anchor']; h = tensor_control['centre']
    for t in (2,3):
        big_columns = []; determinant_product = 1
        for r in tensor_control['receivers']:
            hs, M, scalar_inverse, scalar_det = inverse_view(j,r)
            expanded = [[M[a//t][b//t] if a%t == b%t else 0 for b in range(16*t)] for a in range(16*t)]
            inverse, determinant = F.inverse_det(expanded)
            need(determinant == F.power(scalar_det,t), 'native tensor determinant')
            scalar_C, _ = adjugate_column(j,h,r)
            scale = F.power(scalar_det,t-1)
            for lane in range(t):
                C = [F.mul[determinant][row[hs.index(h)*t+lane]] for row in inverse]
                need(C == [F.mul[scale][scalar_C[a//t]] if a%t == lane else 0 for a in range(16*t)],
                     'direct dense tensor adjugate column equals the proved scaling')
                big_columns.append(C)
            determinant_product = F.mul[determinant_product][scalar_det]
        chosen_rows = [[C[a] for C in big_columns] for a in range(t,16*t)]
        actual = F.det(chosen_rows)
        predicted = F.mul[F.power(tensor_control['scalar_minor'],t)][F.power(determinant_product,t*(t-1))]
        need(actual == predicted != 0, 'first-t-row deletion and complete tensor-minor scaling')
        tensor_checks[str(t)] = {'selected_minor': actual, 'predicted_minor': predicted, 'size': 15*t}
    degrees = {str(t): 30*(15*t)*(16*t-1)+16*t for t in (1,2,3,240)}
    need(all(value == 7200*int(t)**2-434*int(t) for t,value in degrees.items()), 'exact homogeneous polynomial degree')
    result = {'status': 'PASS_INDEPENDENT_ARRAY_ANCHOR_POLYNOMIAL_REVIEW', 'source_pins': PINS,
              'anchors': 99, 'propagation_minors': 2970, 'dense_adjugate_columns': adjugate_column.cache_info().currsize,
              'distinct_native_dense_inverses': inverse_view.cache_info().currsize,
              'nonzero_minor_value_histogram': dict(sorted(minor_histogram.items())),
              'duplicate_column_control': duplicate_control, 'duplicate_final_plane_controls': 99,
              'direct_tensor_control': tensor_checks, 'degree_formula': '7200*t*t-434*t', 'degree_examples': degrees,
              'all_positive_width_nonzero_statement': 'proved by the tensor determinant identity in REVIEW.md',
              'ambient_codimension': 99, 'codimension_scope': 'common zero locus in independent donor coefficient blocks over the algebraic closure of GF64',
              'finite_field_probability_claim': False, 'all_foundations_retained': True, 'new_complete_kappa': False,
              'witnesses': summaries}
    (args.out/'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({key: result[key] for key in ('status','anchors','propagation_minors','dense_adjugate_columns','distinct_native_dense_inverses')},sort_keys=True),flush=True)

if __name__ == '__main__':
    main()
