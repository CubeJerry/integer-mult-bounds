"""Left spread-body rows in the genuine input-owner order of each D."""
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
from build import grouped_sources, require, unpack
from transfer import INV, TABLE, rank_fast


class SpecialSource:
    def __init__(self, atlas, repo, coefficients, frames=()):
        self.atlas = atlas
        raw = gzip.decompress(Path(coefficients).read_bytes())
        require(hashlib.sha256(raw).hexdigest() == "66fe6820e16e2a1a221cc59656b6356087f92b685ff121ef174a67c7c4890a0e", "original H263 source")
        self.coefficients = json.loads(raw)
        self.donors = self.coefficients["donors"]
        self.h = self.coefficients["H"]
        spread = json.loads(unpack(Path(repo) / "research/moonshot-005-program/results", "spread"))
        radicals = [set(row) - {0} for row in spread["D_radicals"]]
        charts = [d for d, ds in enumerate(atlas.D) if atlas.H[self.h] <= ds]
        self.points = {}
        for j in self.donors:
            for h in atlas.ks[j]:
                if h == self.h:
                    continue
                visible = [d for d in charts if atlas.H[h] <= atlas.D[d]]
                common = set.intersection(*(radicals[d] for d in visible))
                require(len(visible) == 5 and len(common) == 1, "native point of off-plane")
                self.points[j, h] = common.pop()
        self.frames = {(z["donor"], z["H"]): (z["early"], np.array(z["matrix"], dtype=np.uint8)) for z in frames}

    def quotient(self, j, h, k):
        width = 16 * k
        s = self.coefficients["components"][str(k)]
        if h == self.h:
            q = self.donors.index(j)
            return np.eye(width, dtype=np.uint8)[q*k:(q+1)*k]
        return np.array(s["off_H"][str(self.points[j, h])], dtype=np.uint8)

    def complete(self, j, h, k):
        atlas = self.atlas
        pair = np.kron(np.eye(2, dtype=np.uint8), self.quotient(j, h, k))
        quota = atlas.phase[str(h)]["donor_early"][str(j)]
        e = k if quota == 15 else 2*k
        if k == 3 and (j, h) in self.frames:
            ne, frame = self.frames[j,h]
            require(e == ne and h != self.h and rank_fast(frame) == 2*k, "retuned ordinary frame")
            return atlas.ops.matmul(frame, pair), e
        if e == 2*k:
            return pair, e
        s = self.coefficients["components"][str(k)]
        early = np.array(s["early"][str(j)][str(h)],dtype=np.uint8)
        late = np.eye(2*k,dtype=np.uint8)[s["complementary_late_coordinate_rows"][str(j)][str(h)]]
        return atlas.ops.matmul(np.vstack([early,late]), pair), e

    @lru_cache(maxsize=3)
    def left(self, j):
        atlas = self.atlas
        if j not in self.donors:
            return atlas.left(j)
        out = {}
        for h in atlas.ks[j]:
            p = atlas.phase[str(h)]
            donors = sorted(atlas.H[h] & set(range(111)))
            quotas = {int(v):e for v,e in p["donor_early"].items()}
            for ds in atlas.h_ports[h]:
                n = len(ds)
                k = n//3
                source, e = self.complete(j,h,k)
                prior = {}
                for ph, tag in (("X","early"), ("Y","late")):
                    if not p[tag]:
                        continue
                    cols = grouped_sources(ph,donors,p["m"],k,quotas)
                    for stripe in range(p[tag]):
                        rows = np.zeros((n,32*k),dtype=np.uint8)
                        for t, owner in enumerate(cols):
                            if owner != j:
                                continue
                            if e == k:
                                q = (0 if ph == "X" else k) + t % k
                            elif p["early"] == 2:
                                q = stripe*k + t % k
                            else:
                                require(p["m"]==2 and ph=="X" and t<2*k, "genuine fully early mixed donor")
                                q = t
                            rows[t] = source[q]
                        mapped = atlas.ops.matmul(atlas.V[n], rows)
                        if ph == "X":
                            prior[stripe] = rows
                        elif p["m"] == 2:
                            cross = atlas.deriv[n].copy()
                            cross[:,2*k:] = 0
                            mapped ^= atlas.ops.matmul(cross, prior[stripe])
                        full = np.zeros((n,480),dtype=np.uint8)
                        start = 0 if k == 3 else 96
                        full[:,start:start+32*k] = mapped
                        for r,d in enumerate(ds):
                            out[atlas.left_flags[h,d,ph][stripe]] = full[r]
        return out


def inverse(matrix):
    n = len(matrix)
    require(matrix.shape == (n,n), "square inverse")
    values = np.hstack([matrix.copy(), np.eye(n,dtype=np.uint8)])
    for c in range(n):
        hits = np.flatnonzero(values[c:,c])
        require(len(hits), "invertible field matrix")
        p = c + int(hits[0])
        values[[c,p]] = values[[p,c]]
        values[c] = TABLE[INV[values[c,c]],values[c]]
        coefficients = values[:,c].copy()
        coefficients[c] = 0
        values ^= TABLE[coefficients[:,None], values[c,None,:]]
    return values[:,n:]


def marked_left(atlas, source, i, j):
    off = [d for d in sorted(atlas.marked) if j in atlas.D[d] and i in atlas.D[atlas.dual[d]]]
    require(len(off) == 12, "twelve marked native D cuts")
    values = source.left(j)
    matrices = []
    for d in off:
        ids = [t for t in atlas.middle[d,"X"]+atlas.middle[d,"Y"] if t in values]
        require(len(ids) == 8, "eight actual H coordinates in one D section")
        rows = np.stack([values[u] for u in ids])
        require(not np.any(rows[:,96:]), "marked section is pure in the small component")
        matrices.append(rows[:,:96])
    return off, np.vstack(matrices)


def fibre(atlas, source, i, j, d):
    ds, matrix = marked_left(atlas,source,i,j)
    order = ds.index(d)
    return inverse(matrix)[:,8*order:8*order+8].T
