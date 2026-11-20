"""Native geometry and finite GF64 source calculations shared by the certificate replays."""
from __future__ import annotations

import hashlib
import importlib.util
from functools import lru_cache
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def coefficients(tag, shape):
    size = int(np.prod(shape))
    raw = hashlib.shake_256(tag.encode("ascii")).digest(size)
    return np.frombuffer(raw, dtype=np.uint8).reshape(shape) & 63


class Atlas:
    def __init__(self, repo):
        results = repo / "research/moonshot-005-program/results"
        self.previous_path = results / "bit-spread-h263-source/author"
        self.previous = module(self.previous_path / "check.py", "h263_source")
        (self.algebra, self.planes, self.charts, self.masks, self.adj,
         self.quota, self.spread) = self.previous.load_inputs(repo)
        self.marked = set(self.spread["selected_D"])
        self.product, self.inverse = self.algebra.field(67)
        self.native = set(range(111))
        self.by_donor = [[h for h,P in enumerate(self.planes) if j in P] for j in range(111)]

    def rank(self, matrix):
        return self.algebra.rank(matrix, self.product, self.inverse)

    def mm(self, left, right):
        return self.previous.multiply(left, right, self.product)

    def vandermonde(self, nodes, n):
        return self.previous.power_rows(list(nodes), n, self.product)

    @lru_cache(maxsize=128)
    def hermite(self, node, rows, columns):
        powers = self.vandermonde([node], columns)[0]
        return np.array([[powers[t-s] if (t & s) == s else 0
                          for t in range(columns)] for s in range(rows)], dtype=np.uint8)


class Chart:
    def __init__(self, atlas, h, k):
        self.atlas, self.h, self.k = atlas, h, k
        self.donors = sorted(atlas.planes[h])
        require(set(self.donors) <= atlas.native, "all three actual donors")
        first, second = (atlas.masks[j] for j in self.donors[:2])
        polar = atlas.algebra.polar

        def project(v):
            return v ^ (first if polar(v, second) else 0) ^ (second if polar(v, first) else 0)

        self.point = {}
        for j in self.donors:
            relative = {}
            for plane in atlas.by_donor[j]:
                if plane == h:
                    continue
                points = {project(atlas.masks[t]) for t in atlas.planes[plane] - {j}}
                require(len(points) == 1, "unique orthogonal projected point")
                relative[plane] = points.pop()
            self.point[j] = relative
        self.singular = sorted(set(self.point[self.donors[0]].values()))
        require(len(self.singular) == 27 and all(x and not atlas.algebra.quadratic(x)
                for x in self.singular), "27 genuine singular points")
        require(all(len(rows) == 27 and set(rows.values()) == set(self.singular)
                    for rows in self.point.values()), "all three point-labelled source stars")
        self.ports = [d for d,Q in enumerate(atlas.charts) if atlas.planes[h] <= Q
                      and (d in atlas.marked) == (k == 3)]
        self.radical = {d: sorted(set(atlas.spread["D_radicals"][d]) - {0}) for d in self.ports}
        self.views = [i for i in range(120) if atlas.planes[h] <= atlas.adj[i]]
        self.exterior = [tuple(x for x in self.singular if polar(x,t)) for t in self.singular]
        self.V = atlas.vandermonde(range(1,3*k+1), 3*k)
        eye = np.eye(16*k, dtype=np.uint8)
        self.controls = [eye[j*k:(j+1)*k] for j in range(3)]
        self.label = f"{h}/{k}/"
        require(len(self.ports) == 3*k and len(self.views) == 36
                and all(len(z) == 16 for z in self.exterior), "native chart dimensions")

    def core(self, seed):
        k, atlas = self.k, self.atlas
        grouped = {x: [] for x in self.singular}
        for q, port in enumerate(self.ports):
            differences = np.zeros((2,6*k), dtype=np.uint8)
            differences[:, :k] = self.V[q,:k]
            differences[0,k:2*k] = self.V[q,k:2*k]
            differences[1,2*k:3*k] = self.V[q,2*k:3*k]
            for attempt in range(100):
                change = coefficients(f"core/{self.label}{seed}/{port}/{attempt}", (2,2))
                if atlas.rank(change) == 2:
                    break
            else:
                raise ValueError("core transform selection")
            rows = np.vstack([np.zeros((1,6*k), dtype=np.uint8), atlas.mm(change,differences)])
            rows[:,3*k+q] = 1
            for x,row in zip(self.radical[port],rows):
                grouped[x].append(row)
        require(all(len(group) == k//3 for group in grouped.values()), "exact share reservation")
        return {x: np.array(rows, dtype=np.uint8) for x, rows in grouped.items()}

    def point_table(self, core_seed, fill_seed):
        k, atlas = self.k, self.atlas
        core = self.core(core_seed)
        width = 2*k//3
        table = {}
        for t,x in enumerate(self.singular):
            extra = coefficients(f"fill/{self.label}{fill_seed}/{x}", (width,6*k))
            table[x] = np.block([[core[x], np.zeros((k//3,10*k), dtype=np.uint8)],
                                 [extra, atlas.hermite(t+1,width,10*k)]])
        for subset in self.exterior:
            require(atlas.rank(np.vstack([table[x] for x in subset])) == 16*k,
                    "all exterior cuts invertible")
        return table

    def maps(self, point_table, donor, control=None):
        rows = {h: point_table[x] for h,x in self.point[donor].items()}
        rows[self.h] = self.controls[self.donors.index(donor)] if control is None else control
        return rows

    def source_views(self, maps, j, full_rank=True):
        atlas = self.atlas
        for i in atlas.adj[j]:
            visible = [p for p in maps if atlas.planes[p] <= atlas.adj[i]]
            require(len(visible) == 16, "geometry-wide 16-plane cut")
            if full_rank:
                require(atlas.rank(np.vstack([maps[p] for p in visible])) == 16*self.k,
                        "geometry-wide source invertibility")
            elif self.h not in visible:
                signature = tuple(sorted(self.point[j][p] for p in visible))
                require(signature in self.exterior, "membership in verified exterior cuts")

    def check_readouts(self, point_table, controls):
        atlas, k = self.atlas, self.k
        for i in self.views:
            xs = [x for x in self.singular if not atlas.algebra.polar(x,atlas.masks[i])]
            visible = [q for q,d in enumerate(self.ports) if atlas.charts[d] <= atlas.adj[i]]
            require(len(visible) == k and len(xs) == 15, "actual receiver cut")
            require(all(len(set(xs) & set(self.radical[d])) == (3 if q in visible else 1)
                        for q,d in enumerate(self.ports)), "full-or-single observation")
            annihilator = np.vstack([point_table[x] for x in xs])
            require(atlas.rank(annihilator) == 15*k, "ordinary inverse-fibre dimension")
            common = None
            for j in range(3):
                minor = self.V[np.ix_(visible,range(j*k,(j+1)*k))]
                require(atlas.rank(minor) == k, "actual donor minor")
                form = atlas.mm(minor, controls[j])
                if common is None:
                    require(atlas.rank(np.vstack([annihilator,form])) == 16*k,
                            "common readout injective")
                    common = form
                else:
                    require(atlas.rank(np.vstack([annihilator,common ^ form])) == 15*k,
                            "same port readout on entire source kernel")

    def early(self, j, maps, seed, fixed_centres=()):
        atlas, k = self.atlas, self.k
        rows = []
        constrained = set(fixed_centres) | {self.h}
        for h,F in sorted(maps.items()):
            quota = atlas.quota[j,h] // 15
            require(quota in (1,2,3), "actual donor early quota")
            if quota >= 2:
                rows.append(np.kron(np.eye(2,dtype=np.uint8), F))
                if quota == 3:
                    rows.append(coefficients(f"extra/{self.label}{j}/{h}/{seed}", (k,32*k)))
            elif h in constrained:
                rows.append(np.hstack([F, np.zeros_like(F)]))
            else:
                A = coefficients(f"early/{self.label}{j}/{h}/{seed}", (k,2*k))
                require(atlas.rank(A) == k, "local early rows extend to full quotient frame")
                rows.append(np.hstack([atlas.mm(A[:,:k],F), atlas.mm(A[:,k:],F)]))
        early = np.vstack(rows)
        require(early.shape == (32*k,32*k) and atlas.rank(early) == 32*k, "paid early basis")

def singleton_jet(atlas, h, k, receiver):
    """Physical rank-2k Hasse readout from the one donor's 3k early inputs."""
    ports = [d for d,D in enumerate(atlas.charts)
             if atlas.planes[h] <= D and (d in atlas.marked) == (k == 3)]
    nodes = [t+1 for t,d in enumerate(ports) if atlas.charts[d] <= atlas.adj[receiver]]
    require(len(nodes) == k, "singleton view on actual sorted component ports")
    return np.vstack([np.array([atlas.hermite(a,2,3*k)[order] for a in nodes])
                      for order in (0,1)])


def generic_singleton(atlas, j, k):
    """Scale the independent extra-node evaluation to admit all physical H views."""
    nodes = atlas.previous.ordinary_source(j,atlas.planes,atlas.quota)
    high = [h for h in nodes if atlas.quota[j,h] == 45]
    if not high:
        return None
    require(len(high) == 1,"at most one singleton on an actual donor star")
    p = high[0]
    full = [h for h in nodes if atlas.quota[j,h] >= 30]
    half = [h for h in nodes if atlas.quota[j,h] == 15]
    extra = 29
    split = 16-len(full)
    extra_lane = int(len(half) >= split)
    identity = np.eye(k,dtype=np.uint8)
    zero = np.zeros_like(identity)
    reduced = []
    for i in sorted(atlas.adj[j] & atlas.native):
        if not atlas.planes[p] <= atlas.adj[i]:
            continue
        others = [n for h,n in nodes.items() if h != p and atlas.planes[h] <= atlas.adj[i]]
        c = d = 1
        for n in others:
            c = atlas.product[c,n ^ nodes[p]]
            d = atlas.product[d,n ^ extra]
        require(len(others) == 15 and c and d,"two nonzero polynomial evaluations")
        reduced.append((singleton_jet(atlas,p,k,i),atlas.product[d,atlas.inverse[c]]))
    for scale in range(1,64):
        for J,ratio in reduced:
            z = atlas.product[scale,ratio] * identity
            extra_row = np.hstack([zero,z]) if extra_lane else np.hstack([z,zero])
            source = np.vstack([np.eye(2*k,dtype=np.uint8),extra_row])
            if atlas.rank(atlas.mm(J,source)) != 2*k:
                break
        else:
            return {"plane":p,"scale":scale,"tested_views":len(reduced),"extra_lane":extra_lane}
    raise ValueError("no admissible multiplier on the additional genuine evaluation")
