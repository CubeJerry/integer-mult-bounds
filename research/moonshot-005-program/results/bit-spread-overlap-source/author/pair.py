"""Jointly construct two three-donor H charts incident to the named primary donor."""
from __future__ import annotations
import numpy as np


def null_basis(matrix, atlas):
    """Columns form the reduced-echelon kernel in increasing free-column order."""
    matrix = np.array(matrix,dtype=np.uint8,copy=True)
    n,m = matrix.shape
    pivots = []
    for col in range(m):
        row = len(pivots)
        possible = np.flatnonzero(matrix[row:,col])
        if not len(possible):
            continue
        other = row + int(possible[0])
        matrix[[row,other]] = matrix[[other,row]]
        matrix[row,col:] = atlas.product[atlas.inverse[matrix[row,col]],matrix[row,col:]]
        factors = matrix[:,col].copy()
        factors[row] = 0
        matrix[:,col:] ^= atlas.product[factors[:,None],matrix[row,None,col:]]
        pivots.append(col)
        if len(pivots) == n:
            break
    free = np.setdiff1d(np.arange(m),pivots)
    basis = np.zeros((m,len(free)),dtype=np.uint8)
    basis[free] = np.eye(len(free),dtype=np.uint8)
    basis[pivots] = matrix[:len(pivots),free]
    return basis


def pair_source(atlas, families, k, parameters):
    require = families.require
    centres = parameters["centres"]
    primary = parameters["shared_donor"]
    require(len(centres) == 2 and centres[0] != centres[1] and
            (atlas.planes[centres[0]] & atlas.planes[centres[1]]) == {primary},
            "actual primary donor intersection")
    charts = [families.Chart(atlas,h,k) for h in centres]
    seed = parameters[str(k)]
    w = k//3
    dim = 12*k
    core = []
    controls = []
    for side,chart in enumerate(charts):
        shares = chart.core(seed["core"])
        by_plane = {}
        for h,x in chart.point[primary].items():
            raw = np.zeros((w,dim),dtype=np.uint8)
            raw[:,6*k*side:6*k*(side+1)] = shares[x]
            by_plane[h] = raw
        core.append(by_plane)
        read = {}
        for pos,j in enumerate(chart.donors):
            start = 6*k*side + pos*k
            matrix = np.zeros((k,dim), dtype=np.uint8)
            matrix[:,start:start+k] = np.eye(k,dtype=np.uint8)
            read[j] = matrix
        controls.append(read)
    relations = np.vstack([controls[0][primary][:w] ^ core[1][centres[0]],
                           controls[1][primary][:w] ^ core[0][centres[1]]])
    lift = null_basis(relations,atlas)
    base = dim - 2*w
    tail = 16*k - base
    require(lift.shape == (dim,base) and not np.any(atlas.mm(relations,lift)),
            "both reserved central cross relations")
    central = {}
    for t,h in enumerate(atlas.by_donor[primary]):
        if h in centres:
            M = atlas.mm(controls[centres.index(h)][primary],lift)
            central[h] = np.hstack([M,np.zeros((k,tail),dtype=np.uint8)])
        else:
            M = atlas.mm(np.vstack([core[0][h],core[1][h]]),lift)
            fixed = np.hstack([M,np.zeros((2*w,tail),dtype=np.uint8)])
            random = families.coefficients(f"pairfill/{centres}/{k}/{seed['fill']}/{h}",(w,base))
            central[h] = np.vstack([fixed,np.hstack([random,atlas.hermite(t+1,w,tail)])])
    all_maps = {}
    signs = {}
    for side,chart in enumerate(charts):
        for j in chart.donors:
            read = atlas.mm(controls[side][j],lift)
            signs[chart.h,j] = np.hstack([read,np.zeros((k,tail),dtype=np.uint8)])
        points = {x:central[h] for h,x in chart.point[primary].items()}
        chart.check_readouts(points,[signs[chart.h,j] for j in chart.donors])
        for j in chart.donors:
            rows = chart.maps(points,j,signs[chart.h,j])
            if j in all_maps:
                require(all(np.array_equal(rows[p],all_maps[j][p]) for p in rows),
                        "one literal source at every plane of common donor")
            else:
                all_maps[j] = rows
                chart.early(j,rows,seed["early"][str(j)],fixed_centres=centres)
                chart.source_views(rows,j)
    return charts,all_maps,{"cross_equations_rank":2*w,"joint_control_mask_dimension":base,
                            "tail_dimension":tail,"ordinary_source_rows":16*k,
                            "shared_actual_source_planes":len(central)}
