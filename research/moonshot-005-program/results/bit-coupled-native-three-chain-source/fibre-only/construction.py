"""Preserve common inverse fibres while changing individual quotient kernels."""
from __future__ import annotations
from collections import defaultdict
import importlib.util
from pathlib import Path
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(ok, message):
    if not ok:
        raise ValueError(message)


def context(repo):
    base = module(Path(__file__).parent.parent / "author/construction.py", "fibre_only_predecessor")
    return base.context(repo)


def hybrid(families, atlas, previous, centres, k):
    base = module(Path(__file__).parent.parent / "author/construction.py", "fibre_only_classes")
    charts = [families.Chart(atlas, h, k) for h in centres]
    donors, labels, groups = base.quotient_classes(atlas, charts)
    require(centres == [263, 642, 135] and len(labels) == 34, "the frozen chain")
    width = len(labels)*k
    rows = []
    w = k//3
    for side, chart in enumerate(charts):
        local = {x: 0 for x in chart.singular}
        control = [groups[j, chart.h] for j in chart.donors]
        for q, port in enumerate(chart.ports):
            delta = np.zeros((2, width), dtype=np.uint8)
            for t in (0, 1):
                delta[t, control[0]*k:(control[0]+1)*k] ^= chart.V[q, :k]
            delta[0, control[1]*k:(control[1]+1)*k] ^= chart.V[q, k:2*k]
            delta[1, control[2]*k:(control[2]+1)*k] ^= chart.V[q, 2*k:]
            for attempt in range(100):
                U = families.coefficients(f"core/{chart.label}0/{port}/{attempt}", (2, 2))
                if atlas.rank(U) == 2:
                    break
            else:
                raise ValueError("invertible port contrast")
            relation = atlas.mm(U, delta)
            first = chart.donors[0]
            if chart.h == 642:
                positions = []
                for x in sorted(chart.radical[port]):
                    h = next(h for h, y in chart.point[first].items() if y == x)
                    positions.append(groups[first, h]*k + side*w + local[x])
                    local[x] += 1
                for t in (0, 1):
                    relation[t, positions[0]] ^= 1
                    relation[t, positions[t+1]] ^= 1
            else:
                for x in sorted(chart.radical[port]):
                    h = next(h for h, y in chart.point[first].items() if y == x)
                    group = groups[first, h]
                    A = families.coefficients(f"general-relations/{centres}/{k}/0/{side}/{port}/{x}", (2, k))
                    relation[:, group*k:(group+1)*k] ^= A
                    local[x] += 1
            rows.extend(relation)
        require(all(v == w for v in local.values()), "exact point/port multiplicity")
    R = np.vstack(rows)
    N = previous.null_basis(R, atlas)
    require(R.shape == (18*k, 34*k) and N.shape == (34*k, 16*k) and not np.any(atlas.mm(R, N)),
            "hybrid source dimension and all constraints")
    maps = {j: {h: N[groups[j, h]*k:(groups[j, h]+1)*k] for h in atlas.by_donor[j]} for j in donors}
    return charts, maps, groups, R, N


def fibres_and_spaces(atlas, previous, charts, maps, k, native_only=False):
    fibres = {}
    constraints = defaultdict(list)
    for chart in charts:
        first = chart.donors[0]
        for i in chart.views:
            if native_only and i not in atlas.native:
                continue
            off = np.vstack([maps[first][h] for h in maps[first]
                             if h != chart.h and atlas.planes[h] <= atlas.adj[i]])
            K = previous.null_basis(off, atlas)
            require(K.shape[1] == k, "whole original inverse fibre")
            fibres[chart.h, i] = K
            for j in chart.donors:
                for h in maps[j]:
                    if h != chart.h and atlas.planes[h] <= atlas.adj[i]:
                        constraints[j, h].append(K)
    spaces = {flag: previous.null_basis(np.hstack(parts).T, atlas).T
              for flag, parts in constraints.items()}
    return fibres, spaces


def build_detailed(families, atlas, previous, centres, k, seed):
    charts, old, groups, R, N = hybrid(families, atlas, previous, centres, k)
    fibres, spaces = fibres_and_spaces(atlas, previous, charts, old, k)
    flexible = {flag: E for flag, E in spaces.items() if E.shape[0] > k and flag[1] not in centres}
    require(set(flexible) == {(0, 116), (25, 394), (47, 652), (62, 643)}, "all four noncentral flexible flags")
    require(all(len(E) == (6 if k == 3 else 20) for E in flexible.values()), "exact fibre annihilator dimensions")
    maps = {j: dict(rows) for j, rows in old.items()}
    for (j, h), E in flexible.items():
        coefficient = families.coefficients(f"fibre-only/{k}/{seed}/{j}/{h}", (k, len(E)))
        maps[j][h] = atlas.mm(coefficient, E)
    return charts, maps, old, groups, R, N, fibres, spaces, flexible


def build(families, atlas, previous, centres, k, seed):
    charts, maps, _, groups, R, N, _, _, _ = build_detailed(families, atlas, previous, centres, k, seed)
    return charts, maps, groups, R, N
