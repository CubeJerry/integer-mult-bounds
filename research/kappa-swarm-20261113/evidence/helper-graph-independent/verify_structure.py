#!/usr/bin/env python3
"""Independent exact row-matroid structure check for rebuilt source rows."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json

OUT = Path(__file__).resolve().parent
REBUILT = OUT / "REBUILT-ROWS.json"
MATROID_PATH = OUT.parents[1] / "worker-b/helper-graph/MATROID-COMPONENTS.json"
MATROID_PIN = "32a0f298f0ace5f0ff1a91b5a9b4e0f32984abd75f56f6f9259ca5c6b4dae74b"
SOURCE_PIN = "acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9"
MODULUS = 1_000_003


def need(ok, label):
    if not ok:
        raise AssertionError(label)


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def add_sparse(dst, src, q):
    for k, v in src.items():
        z = dst.get(k, Q(0)) + q * v
        if z:
            dst[k] = z
        else:
            dst.pop(k, None)


def exact_basis(rows):
    """Return row basis and exact fundamental dependencies, in event order."""
    basis = {}
    basis_events = []
    relations = []
    for event, row in rows:
        v = row.copy()
        expr = {event: Q(1)}
        while v:
            p = min(v)
            old = basis.get(p)
            if old is None:
                scale = 1 / v[p]
                v = {h: x * scale for h, x in v.items() if x * scale}
                expr = {e: x * scale for e, x in expr.items() if x * scale}
                basis[p] = (v, expr)
                basis_events.append(event)
                break
            factor = v[p]
            add_sparse(v, old[0], -factor)
            add_sparse(expr, old[1], -factor)
        if not v:
            need(expr.get(event) == 1, "dependent row relation has wrong pivot coefficient")
            relations.append({e: q for e, q in sorted(expr.items()) if q})
    return basis, basis_events, relations


def mod_fraction(q):
    den = q.denominator % MODULUS
    need(den != 0, "selected modulus divides a rational denominator")
    return (q.numerator % MODULUS) * pow(den, MODULUS - 2, MODULUS) % MODULUS


def modular_basis(rows):
    basis = {}
    factors = []
    pivots = []
    for event, row in rows:
        v = {h: mod_fraction(q) for h, q in row.items()}
        v = {h: x for h, x in v.items() if x}
        while v:
            p = min(v)
            old = basis.get(p)
            if old is None:
                pivot_factor = v[p]
                inv = pow(pivot_factor, MODULUS - 2, MODULUS)
                v = {h: x * inv % MODULUS for h, x in v.items() if x * inv % MODULUS}
                basis[p] = v
                factors.append(pivot_factor)
                pivots.append(p)
                break
            factor = v[p]
            for h, x in old.items():
                z = (v.get(h, 0) - factor * x) % MODULUS
                if z:
                    v[h] = z
                else:
                    v.pop(h, None)
        else:
            raise AssertionError(f"selected exact basis row {event} is dependent modulo {MODULUS}")
    product = 1
    for x in factors:
        product = product * x % MODULUS
    return basis, pivots, product


def uf_make(items):
    return {x: x for x in items}


def uf_find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def uf_union(parent, a, b):
    ra, rb = uf_find(parent, a), uf_find(parent, b)
    if ra != rb:
        parent[rb] = ra


def groups(parent):
    out = defaultdict(list)
    for x in parent:
        out[uf_find(parent, x)].append(x)
    return [sorted(v) for v in out.values()]


def main():
    need(is_prime(MODULUS), "modular certificate modulus is not prime")
    rebuilt_raw = REBUILT.read_bytes()
    rebuilt = json.loads(rebuilt_raw)
    need(rebuilt["source_sha256"] == SOURCE_PIN, "rebuilt source pin")
    records = [(r["event"], {int(h): Q(v) for h, v in r["row"].items()})
               for r in rebuilt["records"]]
    record_by_event = dict(records)
    need(len(records) == 468 and len(record_by_event) == 468, "row inventory count")
    targets = {int(h): int(r) for h, r in rebuilt["helper_targets"].items()}
    paid = {r["event"]: int(r["rank"]) for r in rebuilt["records"]}

    # Exact global rank and five explicit full-Q row relations.
    basis, basis_events, relations = exact_basis(records)
    need(len(basis) == len(basis_events) == 463, "exact global row rank")
    need(len(relations) == 5, "exact nonbasis relation count")
    nonbasis_events = set(record_by_event) - set(basis_events)
    need(len(nonbasis_events) == 5, "five nonbasis rows")
    relation_supports = []
    for relation in relations:
        relation_supports.append(set(relation))
        zero = {}
        for event, q in relation.items():
            add_sparse(zero, record_by_event[event], q)
        need(not zero, "fundamental relation does not sum to the exact zero row")
    need({max(s) for s in relation_supports} <= nonbasis_events,
         "each dependency relation has a nonbasis pivot")
    need({next(e for e in rel if e in nonbasis_events) for rel in relations} == nonbasis_events,
         "relations do not cover all five nonbasis rows")

    # A modular nonzero maximal minor independently certifies basis independence.
    mod_basis, mod_pivots, minor_product = modular_basis(
        [(e, record_by_event[e]) for e in basis_events])
    need(len(mod_basis) == 463 and len(mod_pivots) == 463 and minor_product != 0,
         "modular nonzero 463-minor certificate")

    # Native support graph: rows connected when they share helper columns.
    support_parent = uf_make(record_by_event)
    first_for_column = {}
    for event, row in records:
        for h in row:
            if h in first_for_column:
                uf_union(support_parent, event, first_for_column[h])
            else:
                first_for_column[h] = event
    support_components = groups(support_parent)
    support_components.sort(key=lambda comp: min(comp))
    support_sizes = sorted((len(c) for c in support_components), reverse=True)
    need(support_sizes[0] == 347 and len(support_components) == 94,
         "support component census")
    giant = set(support_components[0])
    need(len(giant) == 347 and len(record_by_event) - len(giant) == 121,
         "support giant/non-giant row counts")
    need(nonbasis_events <= giant, "a nonbasis row lies outside the support giant")
    giant_rank = len(set(basis_events) & giant)
    need(giant_rank == 342 and len(giant) - giant_rank == 5,
         "giant exact rank/nullity")
    need(all(e in set(basis_events) for e in record_by_event if e not in giant),
         "non-giant support row is not independently selected")

    # Fundamental circuits generate the row-matroid connected components.
    matroid_parent = uf_make(record_by_event)
    for s in relation_supports:
        items = sorted(s)
        for e in items[1:]:
            uf_union(matroid_parent, items[0], e)
    matroid_components = groups(matroid_parent)
    matroid_components.sort(key=lambda c: (len(c), min(c)))
    dependent_blocks = [c for c in matroid_components if len(c) > 1]
    block_sizes = sorted((len(c) for c in dependent_blocks), reverse=True)
    dependent_rows = set(e for c in dependent_blocks for e in c)
    coloop_count = len(record_by_event) - len(dependent_rows)
    need(block_sizes == [11, 5, 5, 5], "fundamental-circuit component sizes")
    need(coloop_count == 442 and len(dependent_rows) == 26,
         "global coloop/dependent-element census")
    need(dependent_rows <= giant, "dependent row component escaped support giant")
    inside_giant_coloops = len(giant - dependent_rows)
    need(inside_giant_coloops == 321, "giant coloop count")
    dependent_support_overlaps = []
    for block in dependent_blocks:
        block_set = set(block)
        cols = set().union(*(set(record_by_event[e]) for e in block_set))
        outside_cols = set().union(*(set(row) for e, row in records if e not in block_set))
        dependent_support_overlaps.append({
            "rows": len(block_set),
            "columns": len(cols),
            "columns_shared_with_other_matroid_components": len(cols & outside_cols),
        })

    # Source rank weights and pointwise support domination.
    pointwise_min_ratio = None
    for event, row in records:
        need(1 <= paid[event] <= 9, f"paid rank domain at {event}")
        need(row and set(row) <= set(targets), f"invalid helper support at {event}")
        m = min(targets[h] for h in row)
        need(paid[event] <= m, f"paid rank exceeds some support target at {event}")
        ratio = Q(m, paid[event])
        pointwise_min_ratio = ratio if pointwise_min_ratio is None else min(pointwise_min_ratio, ratio)

    # Compare with the frozen author census only after independently deriving it.
    mraw = MATROID_PATH.read_bytes()
    need(sha256(mraw).hexdigest() == MATROID_PIN, "frozen matroid receipt pin")
    md = json.loads(mraw)
    need(md["source_sha256"] == SOURCE_PIN and md["rows_sha256"] == rebuilt["b_rows_sha256"],
         "author source binding mismatch")
    need(md["rank_Q"] == 342 and md["giant_rows"] == len(giant) and md["nullity"] == 5,
         "author summary disagrees with independent reconstruction")

    out = {
        "status": "PASS_INDEPENDENT_EXACT_GLOBAL_STRUCTURE",
        "source_sha256": rebuilt["source_sha256"],
        "b_rows_sha256": rebuilt["b_rows_sha256"],
        "author_matroid_sha256": sha256(mraw).hexdigest(),
        "rows": len(record_by_event),
        "exact_global_rank_Q": len(basis),
        "basis_events": basis_events,
        "exact_fundamental_relations": [
            {"pivot_nonbasis_event": next(e for e in rel if e in nonbasis_events),
             "coefficients": {str(e): str(q) for e, q in rel.items()}}
            for rel in relations
        ],
        "modular_minor": {
            "prime": MODULUS,
            "rank_of_exact_basis_rows": len(mod_basis),
            "pivot_column_count": len(mod_pivots),
            "pivot_columns": mod_pivots,
            "determinant_up_to_permutation_mod_prime": minor_product,
            "nonzero": minor_product != 0,
        },
        "support_component_count": len(support_components),
        "support_component_row_sizes_desc": support_sizes,
        "support_giant_row_count": len(giant),
        "support_giant_helper_column_count": len(set().union(*(set(record_by_event[e]) for e in giant))),
        "support_giant_rank_Q": giant_rank,
        "support_giant_nullity": len(giant) - giant_rank,
        "non_giant_rows": len(record_by_event) - len(giant),
        "non_giant_support_component_row_sizes_desc": support_sizes[1:],
        "matroid_dependent_block_sizes_desc": block_sizes,
        "matroid_dependent_blocks": [
            {"events": sorted(c), "rows": len(c)} for c in dependent_blocks
        ],
        "dependent_block_support_overlaps": dependent_support_overlaps,
        "dependent_row_elements": len(dependent_rows),
        "total_coloops": coloop_count,
        "giant_coloops": inside_giant_coloops,
        "all_paid_ranks_le_every_support_target_rank": True,
        "minimum_pointwise_target_to_paid_linear_rank_ratio": str(pointwise_min_ratio),
        "author_global_summary_matches_independent_result": True,
        "scope": "Original-source exact helper-only MOVE row matroid. No changed source or physical implementation.",
    }
    (OUT / "STRUCTURE.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("basis_events", "exact_fundamental_relations", "modular_minor")}, indent=2))
    print("modular minor:", json.dumps(out["modular_minor"], indent=2))
    print("dependent relation pivots:", [x["pivot_nonbasis_event"] for x in out["exact_fundamental_relations"]])


if __name__ == "__main__":
    main()
