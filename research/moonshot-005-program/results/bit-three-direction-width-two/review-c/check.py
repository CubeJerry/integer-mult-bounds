#!/usr/bin/env python3
"""Independent finite pencil/Jordan controls, not a new native scalar proof."""
import argparse, hashlib, itertools, json
from collections import Counter
from pathlib import Path

PIN = '2a35dcb0a8b804b3c30d3759533070d903699c0b1dbb237618586511ce9d2bb5'


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def brank(rows):
    piv = {}
    for x in rows:
        while x:
            p = x.bit_length()-1
            if p in piv:
                x ^= piv[p]
            else:
                piv[p] = x
                break
    return len(piv)


def multiply(a,b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


M = [[multiply(a,b) for b in range(4)] for a in range(4)]
INV = {1:1,2:3,3:2}


def field_rank(rows):
    piv = {}
    for original in rows:
        row = list(original)
        for p in sorted(piv):
            if row[p]:
                a = row[p]
                row = [x ^ M[a][y] for x,y in zip(row,piv[p])]
        if any(row):
            p = next(j for j,x in enumerate(row) if x)
            piv[p] = [M[INV[row[p]]][x] for x in row]
    return len(piv)


def dot(a,b):
    out = 0
    for x,y in zip(a,b):
        out ^= M[x][y]
    return out


def solve(columns, target):
    rows = [[columns[c][r] for c in range(3)]+[target[r]] for r in range(4)]
    piv = []
    current = 0
    for c in range(3):
        hits = [r for r in range(current,4) if rows[r][c]]
        if not hits:
            continue
        r = hits[0]
        rows[current],rows[r] = rows[r],rows[current]
        z = INV[rows[current][c]]
        rows[current] = [M[z][x] for x in rows[current]]
        for r in range(4):
            if r != current and rows[r][c]:
                z = rows[r][c]
                rows[r] = [x ^ M[z][y] for x,y in zip(rows[r],rows[current])]
        piv.append(c)
        current += 1
    if any(not any(row[:3]) and row[3] for row in rows):
        return None
    a = [0]*3
    for r,c in enumerate(piv):
        a[c] = rows[r][3]
    kernels = []
    for free in range(3):
        if free not in piv:
            v = [0]*3
            v[free] = 1
            for r,c in enumerate(piv):
                v[c] = rows[r][free]
            kernels.append(v)
    return a,kernels


def polymul(a,b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        a <<= 1
        b >>= 1
    return out


PERMS = list(itertools.permutations(range(3)))


def determinant_polynomial(a,b):
    out = 0
    for perm in PERMS:
        term = 1
        for r,c in enumerate(perm):
            term = polymul(term, ((a >> (3*r+c)) & 1) | (((b >> (3*r+c)) & 1) << 1))
        out ^= term
    return out


def pencil_data(a,b):
    ar = [(a >> (3*r)) & 7 for r in range(3)]
    br = [(b >> (3*r)) & 7 for r in range(3)]
    ac = [sum(((a >> (3*r+c)) & 1) << r for r in range(3)) for c in range(3)]
    bc = [sum(((b >> (3*r+c)) & 1) << r for r in range(3)) for c in range(3)]
    images = [0]
    for x,y in zip(ac,bc):
        z = x | (y << 3)
        images += [w ^ z for w in list(images)]
    image_set = set(images)
    full = [w for w in range(1,8) if w in image_set and w << 3 in image_set]
    return brank(ar+br),brank(ac+bc),full


def encode(matrix):
    return sum(matrix[r][c] << (3*r+c) for r in range(3) for c in range(3))


def pencils():
    matrices = []
    for x in range(512):
        rows = [(x >> (3*r)) & 7 for r in range(3)]
        cols = [sum(((x >> (3*r+c)) & 1) << r for r in range(3)) for c in range(3)]
        matrices.append((rows,cols,brank(rows)))
    admissible = singular = regular = 0
    example = None
    line_counts = Counter()
    for a,(ar,ac,ra) in enumerate(matrices):
        for b,(br,bc,rb) in enumerate(matrices):
            if brank(ar+br) != 3 or brank(ac+bc) != 3:
                continue
            admissible += 1
            if ra == 3 or rb == 3 or determinant_polynomial(a,b):
                regular += 1
                continue
            singular += 1
            injection,envelope,full = pencil_data(a,b)
            need(injection == envelope == 3 and full, 'every admissible singular square pencil forces a full tensor line')
            line_counts[len(full)] += 1
            if example is None:
                example = {'H0_bits':a,'H1_bits':b,'full_scalar_lines':full}
    need(admissible == regular+singular and singular > 0, 'nonempty complete pencil test')
    # A constant cokernel permits a line-free three-space in a two-direction envelope.
    a = encode([[1,0,0],[0,1,0],[0,0,0]])
    b = encode([[0,0,1],[1,0,0],[0,0,0]])
    need(pencil_data(a,b) == (3,2,[]) and determinant_polynomial(a,b) == 0, 'full envelope hypothesis is essential')
    # A common kernel permits the completely coupled two-column chain.
    c = encode([[0,0,0],[1,0,0],[0,1,0]])
    need(pencil_data(a,c) == (2,3,[]) and determinant_polynomial(a,c) == 0, 'injectivity hypothesis is essential')
    # A regular binary pencil may have no invertible binary projective projection.
    h0 = [[0,0,0],[0,1,0],[0,0,1]]
    h1 = [[1,0,0],[0,1,0],[0,0,0]]
    d0,d1 = encode(h0),encode(h1)
    need(determinant_polynomial(d0,d1) == 6, 'nonzero polynomial t+t^2')
    need(all(field_rank(mat) == 2 for mat in [h0,h1,[[x^y for x,y in zip(a,b)] for a,b in zip(h0,h1)]]), 'all binary value projections singular')
    projected = [[h0[r][c] ^ M[2][h1[r][c]] for c in range(3)] for r in range(3)]
    need(field_rank(projected) == 3, 'F4 value projection repairs graph reduction')
    return {'binary_pencil_pairs':512**2,'injective_full_envelope_pairs':admissible,
            'regular_pairs':regular,'singular_pairs':singular,
            'singular_full_line_census':dict(line_counts),'singular_example':example,
            'dropped_envelope_control':[a,b],'dropped_injectivity_control':[a,c],
            'regular_pencil_requiring_field_extension':{'H0':h0,'H1':h1,'det_polynomial_bits':6,'F4_parameter':2}}


def qualifies(coefficients, a, kernel):
    # Coefficients are the constant/t/s coefficient vectors of a formal
    # linear polynomial c. Vanishing is checked symbolically, not by
    # substituting finitely many field values for transcendental variables.
    return all(dot(c,v) == 0 for c in coefficients for v in kernel) and any(dot(c,a) != 0 for c in coefficients)


def jordan():
    out = []
    I = [1,0,0,1]
    e = [[1,0,0],[0,1,0],[0,0,1]]
    for q in (2,4):
        vectors = list(itertools.product(range(q),repeat=3))
        us = [(a,b) for a in vectors for b in vectors if field_rank([a,b]) == 2]
        need(len(us) == (q**3-1)*(q**3-q), 'all rank-two selector matrices')
        cases = []
        for lam in range(q):
            cases += [('J3',lam,lam,[[lam,1,0],[0,lam,1],[0,0,lam]],[[e[0],e[1]]],1),
                      ('J2_same',lam,lam,[[lam,1,0],[0,lam,0],[0,0,lam]],[[e[0]]],1)]
            for mu in range(q):
                if mu != lam:
                    cases.append(('J2_distinct',lam,mu,[[lam,1,0],[0,lam,0],[0,0,mu]],[[e[0]],[e[0],e[1]],[e[0],e[2]]],2))
        for eigenvalues in itertools.combinations(range(q),3):
            T = [[eigenvalues[r] if r == c else 0 for c in range(3)] for r in range(3)]
            cases.append(('diagonal_distinct',list(eigenvalues),None,T,[[v] for v in e],2))
        for name,lam,mu,T,codes,required in cases:
            counts = Counter()
            kernel_counts = Counter()
            examples = {}
            relevant = 0
            for U in us:
                mats = [[U[0][b],dot(T[b],U[0]),U[1][b],dot(T[b],U[1])] for b in range(3)]
                solution = solve(mats,I)
                if solution is None:
                    continue
                a,kernel = solution
                relevant += 1
                need(len(kernel) <= 1, 'coefficient kernel is zero or a line')
                if kernel:
                    v = kernel[0]
                    Ttv = [dot([T[r][c] for r in range(3)],v) for c in range(3)]
                    need(field_rank([v,Ttv]) == 1 and dot(U[0],v) == dot(U[1],v) == 0,
                         'coefficient kernel equals a selector-kernel eigenline')
                good = [i for i,c in enumerate(codes) if qualifies(c,a,kernel)]
                need(len(good) >= required, 'claimed fixed formal scalar codes dominate each eligible row')
                if kernel:
                    for z in range(q):
                        moved = [x ^ M[z][y] for x,y in zip(a,kernel[0])]
                        need([qualifies(c,moved,kernel) for c in codes] == [qualifies(c,a,kernel) for c in codes], 'domination criterion is independent of preimage choice')
                counts[len(good)] += 1
                kernel_counts[len(kernel)] += 1
                examples.setdefault(str(len(good))+'_'+str(len(kernel)), {'U':U,'preimage_I':a,'kernel':kernel,'qualifying_codes':good})
            out.append({'field_order':q,'case':name,'lambda':lam,'mu':mu,'selector_matrices':len(us),
                        'identity_in_coefficient_span':relevant,'qualification_census':dict(counts),
                        'kernel_dimension_census':dict(kernel_counts),'examples':examples})
        for lam in range(q):
            for mu in range(q):
                T = [[lam,0,0],[0,lam,0],[0,0,mu]]
                shifted = [[T[r][c] ^ (lam if r == c else 0) for c in range(3)] for r in range(3)]
                need(field_rank(shifted) <= 1, 'repeated-eigenvalue scalar contraction')
    return out


def chain_control():
    out = []
    for q in (2,4):
        checked = 0
        for a,b,c in itertools.product(range(q),repeat=3):
            if not (a or b or c):
                continue
            need(field_rank([[a,b,c,0],[0,a,b,c]]) == 2, 'four-direction chain has no nonzero pure tensor')
            checked += 1
        out.append({'field_order':q,'nonzero_vectors':checked,'pure_tensors':0})
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--proof',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a = p.parse_args()
    need(hashlib.sha256(a.proof.read_bytes()).hexdigest() == PIN, 'reviewed proof pin')
    out = {'status':'PASS_INDEPENDENT_THREE_DIRECTION_WIDTH_TWO_ALGEBRA','proof_sha256':PIN,
           'author_checker_imported':False,'pencil_census':pencils(),'jordan_cases':jordan(),
           'four_direction_chain_control':chain_control(),
           'classification':'independent universal proof review plus finite algebra controls; native scalar205 inherited, not reproved; no new kappa',
           'new_kappa':None}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'binary_pencils':512**2,'admissible_singular':out['pencil_census']['singular_pairs'],
                      'jordan_cases':len(out['jordan_cases']),'identity_span_rows':sum(x['identity_in_coefficient_span'] for x in out['jordan_cases'])}))


if __name__ == '__main__':
    main()
