#!/usr/bin/env python3
"""Independent exact identities and controls for the literal-target gate."""
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
import sympy as s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path.cwd())
    ar = ap.parse_args()
    base = Path(__file__).parent
    hp = ar.repo / 'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
    assert hashlib.sha256(hp.read_bytes()).hexdigest() == '1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
    sp = importlib.util.spec_from_file_location('literal_gate_dyadic', hp)
    m = importlib.util.module_from_spec(sp)
    sys.modules[sp.name] = m
    sp.loader.exec_module(m)
    x = s.symbols('x', nonzero=True)
    K = s.Matrix([[1, 0, x-1], [x, 0, -x], [1, 1, -1]])
    Ki = s.Matrix([[1/x, 1/x-1/x**2, 0], [0, -1/x, 1], [1/x, -1/x**2, 0]])
    B = s.Matrix([[x, x-2+1/x, x-1], [x, 0, -x], [x, x-1+1/x, -1]])
    assert s.simplify(K*Ki) == s.eye(3)
    assert s.simplify(Ki*K) == s.eye(3)
    assert s.simplify(Ki*s.diag(x**3, x**2, x**2)*Ki-B) == s.zeros(3)
    assert s.simplify(Ki*s.diag(x**2, x**2, x**2)*Ki-K) == s.zeros(3)
    I = m.eye(8)
    Xb = m.monomial([j^2 for j in range(8)], [0]*8)
    Cb = m.M((I.scale((1,1)) + Xb.scale((1,-1))).a, 1).norm()
    S = m.monomial([0,4,1,5,2,6,3,7], [0]*8)
    A = Cb @ S
    assert m.gaussian_rank(A) == 1 and m.gaussian_rank(A.power(2)) == 2
    cases = []
    for V in (1, 2):
        a = A.tp(V)
        i, z = m.eye(a.n), m.zero(a.n)
        ai, aii = a.power(-1), a.power(-2)
        k = m.block([[i,z,a+i.scale((-1,0))],[a,z,a.scale((-1,0))],[i,i,i.scale((-1,0))]])
        ki = m.block([[ai,ai+aii.scale((-1,0)),z],[z,ai.scale((-1,0)),i],[ai,aii.scale((-1,0)),z]])
        b = m.block([[a,a+i.scale((-2,0))+ai,a+i.scale((-1,0))],[a,z,a.scale((-1,0))],[a,a+i.scale((-1,0))+ai,i.scale((-1,0))]])
        target = m.diagonal([a.power(3),a.power(2),a.power(2)])
        assert k @ ki == m.eye(3*a.n) and ki @ k == m.eye(3*a.n)
        assert ki @ target @ ki == b
        assert ki @ m.diagonal([a.power(2)]*3) @ ki == k
        assert k.power(3) == m.diagonal([a.power(2)]*3)
        cases.append({'width':V, 'all_columns':3*a.n, 'laurent_inverse_identity':True,
                      'literal_target_B_identity':True, 'base_222_positive_control':True})
    # Ordinary-square negative control: a=i times the two-qubit real Hadamard.
    h = s.Matrix([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]]) / 2
    an = s.I*h
    assert an**2 == -s.eye(4) and an.inv() == -an
    ii, zz = s.eye(4), s.zeros(4)
    bn = s.BlockMatrix([[an,an-2*ii+an.inv(),an-ii],
                        [an,zz,-an],[an,an-ii+an.inv(),-ii]]).as_explicit()
    rr = s.Matrix.vstack(zz,ii,zz)
    assert bn*rr == s.Matrix.vstack(-2*ii,zz,-ii)
    out = {'status':'PASS_EXACT_LITERAL_TARGET_LINEAR_GATE_DIAGNOSTICS',
           'proof_sha256':hashlib.sha256((base/'LINEAR-INTERSECTION-GATE.md').read_bytes()).hexdigest(),
           'helper_sha256':hashlib.sha256(hp.read_bytes()).hexdigest(),
           'formal_laurent_identities':True, 'physical_all_column_checks':cases,
           'ordinary_square_negative_control_nonzero_ordinary_preimage':True,
           'scope':'The coset argument proves the all-width obstruction in the faithful group-span model. Small-width checks validate identities only. Arbitrary outer ordinary endpoint encodings are not excluded. No new kappa.'}
    (base/'LINEAR-GATE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))

if __name__ == '__main__':
    main()
