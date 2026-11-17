"""A receiver rank certificate using evaluations away from the source nodes."""
from functools import reduce
from operator import xor


def product_mod(x, y):
    # Multiply as polynomials over F2, then divide by z^6+z+1.
    raw = 0
    while y:
        if y & 1:
            raw ^= x
        y >>= 1
        x <<= 1
    while raw.bit_length() > 6:
        raw ^= 67 << (raw.bit_length() - 7)
    return raw


PRODUCT = [[product_mod(a,b) for b in range(64)] for a in range(64)]
INVERSE = [None] + [PRODUCT[a].index(1) for a in range(1,64)]


def rref_with_trace(rows):
    n = len(rows)
    cols = len(rows[0])
    mat = [r[:] + [int(j == i) for j in range(n)] for i,r in enumerate(rows)]
    rank = 0
    determinant = 1
    for col in range(cols):
        pivot = next((j for j in range(rank,n) if mat[j][col] != 0), None)
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        scale = mat[rank][col]
        determinant = PRODUCT[determinant][scale]
        mat[rank] = [PRODUCT[INVERSE[scale]][a] for a in mat[rank]]
        for j in range(n):
            if j != rank and mat[j][col]:
                m = PRODUCT[mat[j][col]]
                mat[j] = [a^m[b] for a,b in zip(mat[j],mat[rank])]
        rank += 1
    if rank != n:
        determinant = 0
    return rank, determinant, [r[cols:] for r in mat[rank:]]


def certificate(H, normals):
    h = sum(1 << k for k in (7,8,9))
    center = H.index(h)
    receivers = [0,5,49,18,106,17,6,80,79,51,34,91,109,107,108,110]
    assert all(normals[center] & (1 << i) for i in receivers)
    frames = {}
    result = {}
    for donor in (7,8):
        pencil = sorted((m for m in range(len(H)) if H[m] & (1<<donor)), key=H.__getitem__)
        assert len(pencil) == 28
        rows = []
        # The full-rank Vandermonde evaluation at 28..43 is an invertible
        # common basis change from the monomial coefficients (all degree <=15).
        for i in receivers:
            visible = [q for q,j in enumerate(pencil) if j != center and normals[j] & (1 << i)]
            assert len(visible) == 15
            rows.append([reduce(lambda x,y:PRODUCT[x][y], (t^q for q in visible), 1) for t in range(28,44)])
        frames[donor] = rows
        rank,det,dependences = rref_with_trace(rows)
        result[str(donor)] = {'rank':rank,'evaluation_determinant':det,'dependency':dependences}
    assert result['7']['rank'] == 15 and result['8']['rank'] == 16
    relation = result['7']['dependency'][0]
    relations = {str(j):[reduce(xor,(PRODUCT[c][r[q]] for c,r in zip(relation,frame))) for q in range(16)]
                 for j,frame in frames.items()}
    assert not any(relations['7']) and any(relations['8'])
    return {'center': [7,8,9], 'donors':[7,8], 'receivers':receivers,
            'field':'GF(2)[z]/(z^6+z+1)', 'evaluation_basis_nodes':list(range(28,44)),
            'pencil_order':'increasing binary mask of three parent root indices', 'center_rank_witnesses':result,
            'donor7_relation_applied_to_donor8':relations['8']}
