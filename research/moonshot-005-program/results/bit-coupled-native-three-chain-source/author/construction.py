"""One literal source on a connected chain of three native H centres.

The point quotients are shared by incidence.  Each radical port imposes two
control-difference equations with unrestricted two-row coefficients at each
of its three points.  This changes the rank-one share model used by the older
one- and two-centre ramp constructions.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def require(ok, message):
    if not ok:
        raise ValueError(message)


def context(repo):
    root = repo / "research/moonshot-005-program/results"
    families = module(root / "bit-spread-disjoint-h-sources/author/families.py", "chain_families")
    previous = module(root / "bit-spread-overlap-source/author/pair.py", "chain_kernel")
    return families, families.Atlas(repo), previous


def quotient_classes(atlas, charts):
    """Identify the same singular-point quotient across each centre's donors."""
    donors = sorted(set.union(*(set(chart.donors) for chart in charts)))
    flags = [(j, h) for j in donors for h in atlas.by_donor[j]]
    parent = {flag: flag for flag in flags}

    def find(flag):
        while parent[flag] != flag:
            parent[flag] = parent[parent[flag]]
            flag = parent[flag]
        return flag

    def join(left, right):
        left, right = find(left), find(right)
        if left != right:
            parent[max(left, right)] = min(left, right)

    for chart in charts:
        for point in chart.singular:
            refs = [(j, next(h for h, x in chart.point[j].items() if x == point))
                    for j in chart.donors]
            join(refs[0], refs[1])
            join(refs[0], refs[2])
    labels = sorted({find(flag) for flag in flags})
    index = {label: n for n, label in enumerate(labels)}
    groups = {flag: index[find(flag)] for flag in flags}
    return donors, labels, groups


def build(families, atlas, previous, centres, k, seed):
    charts = [families.Chart(atlas, h, k) for h in centres]
    donors, labels, groups = quotient_classes(atlas, charts)
    require(len(labels) == 34 and len(donors) == 7, "the prescribed three-centre chain")
    require(all(len({groups[j, h] for h in atlas.by_donor[j]}) == 28 for j in donors),
            "no source planes identified within a donor")
    columns = len(labels) * k
    equations = []
    for side, chart in enumerate(charts):
        control = [groups[j, chart.h] for j in chart.donors]
        for q, port in enumerate(chart.ports):
            difference = np.zeros((2, columns), dtype=np.uint8)
            for row in (0, 1):
                difference[row, control[0]*k:(control[0]+1)*k] ^= chart.V[q, :k]
            difference[0, control[1]*k:(control[1]+1)*k] ^= chart.V[q, k:2*k]
            difference[1, control[2]*k:(control[2]+1)*k] ^= chart.V[q, 2*k:]
            for attempt in range(100):
                change = families.coefficients(f"core/{chart.label}{seed}/{port}/{attempt}", (2, 2))
                if atlas.rank(change) == 2:
                    break
            else:
                raise ValueError("invertible contrast frame")
            equation = atlas.mm(change, difference)
            first = chart.donors[0]
            for point in sorted(chart.radical[port]):
                h = next(h for h, x in chart.point[first].items() if x == point)
                group = groups[first, h]
                coefficient = families.coefficients(
                    f"general-relations/{centres}/{k}/{seed}/{side}/{port}/{point}", (2, k))
                equation[:, group*k:(group+1)*k] ^= coefficient
            equations.extend(equation)
    constraint = np.vstack(equations)
    require(constraint.shape == (18*k, 34*k), "two equations per actual port")
    embedding = previous.null_basis(constraint, atlas)
    require(embedding.shape == (34*k, 16*k), "full constraint rank and original input width")
    require(not np.any(atlas.mm(constraint, embedding)), "all simultaneous port equations")
    maps = {j: {h: embedding[groups[j, h]*k:(groups[j, h]+1)*k]
                for h in atlas.by_donor[j]} for j in donors}
    return charts, maps, groups, constraint, embedding
