#!/usr/bin/env python3
"""Independent finite controls; the universal argument is in REVIEW.md."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sympy as S

def need(value, message):
    if not value: raise ValueError(message)

def mul(p, q): return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    q = [0] * len(p)
    for i, j in enumerate(p): q[j] = i
    return tuple(q)
def setmul(X, Y): return {mul(x, y) for x in X for y in Y}

def group_controls():
    group = set(itertools.permutations(range(3))); identity = (0, 1, 2)
    groups = []; rest = sorted(group - {identity})
    for bits in range(1 << len(rest)):
        H = {identity} | {x for i, x in enumerate(rest) if bits >> i & 1}
        if setmul(H, H) <= H: groups.append(H)
    cases = 0; overlaps = []
    for H in groups:
        for a in group - H:
            for g in group - H:
                gHa = setmul(setmul({g}, H), {a}); gH = setmul({g}, H); Ha = setmul(H, {a})
                need(not (gHa & gH), "gHa intersects gH")
                need(not (gHa & Ha), "gHa intersects Ha")
                double = setmul(setmul(H, {inv(a)}), H)
                need(not (double & H), "ordinary group intersects Ha^-1H")
                need(not (gH & setmul({g}, double)), "gH intersects gHa^-1H")
                if gH & Ha: overlaps.append((sorted(H), a, g))
                cases += 1
    need(overlaps, "allowed gH/Ha intersections omitted")
    H = {identity, (1, 0, 2)}
    need(setmul(setmul({identity}, H), {identity}) & H, "ordinary-unit negative control")
    return {"ambient_group": "S3", "all_subgroups": len(groups), "nonordinary_a_g_cases": cases,
            "allowed_gH_Ha_intersections": len(overlaps), "ordinary_unit_mutation_rejected": True,
            "scope": "Illustrates universal group-support identities; not the physical Clifford rank model."}

def block_controls():
    I, Z = S.eye(2), S.zeros(2)
    a = S.Matrix([[1, 1], [0, 1]]); p = S.Matrix([[0, 0], [1, 0]])
    A = S.Matrix([[2, 1], [1, 1]]); B = S.Matrix([[1, 0], [2, 1]])
    need(p.det() == 0 and a * p != p * a, "singular noncommuting control")
    R1, R2 = a * a, a * p * a; S1, S2 = a, I + p * a
    Y, T2 = A * R1 + B * S1, A * R2 + B * S2
    need(T2 == Y * a.inv() * p * a + B, "first common-right-factor identity")
    need(T2 * a.inv() == Y * a.inv() * p + B * a.inv(), "second common-right-factor identity")
    need(T2 * a.inv() != Y * p * a.inv() + B * a.inv(), "wrong noncommutative order accepted")
    need(A * R2 + B * (I + a * p) != T2, "wrong ordinary correction order accepted")
    P = S.diag(1, 0); O = P.row_join(I-P).col_join((I-P).row_join(P))
    need(O * O == S.eye(4), "ordinary projector boundary not invertible")
    need(all(O[r:r+2, c:c+2].det() == 0 for r in [0, 2] for c in [0, 2]), "individual blocks not singular")
    D = S.diag(a, a); L = a.row_join(I).col_join(Z.row_join(a)); w, z = O[:2, :], O[2:, :]
    q = S.Matrix([[0, -1], [1, 0]]); R = q * w * D; oldS = z * L; T = A * R + B * oldS
    invO = O.inv(); right = T * D.inv() * invO
    need(right[:, 2:] == B + B*z[:, :2]*a.inv()*invO[2:, 2:], "in-place second-block identity")
    need(R * D.inv() * invO == q.row_join(Z), "normalized affected row identity")
    b, c = S.Matrix([[1, 2], [0, 1]]), S.Matrix([[0, 1], [1, 1]])
    U = S.Matrix([[1, 0, 2, 1], [0, 1, 1, 3]]); component = b.col_join(c) * U; R = component[:2, :]
    need(component.rank() == 2 and R.rank() == 2 and b.det() != 0, "rank component control")
    need(component[2:, :] == c*b.inv()*R, "ordinary component separation")
    need((P.col_join(c)*U)[:2, :].rank() < 2, "singular pivot retained full row rank")
    return {"matrix_field": "Q", "block_dimension": 2, "noncommuting_singular_p_identities": True,
            "invertible_ordinary_boundary_with_all_four_blocks_singular": True, "rank_pivot_and_separation": True,
            "rejecting_controls": ["wrong product order", "wrong correction order", "singular pivot"],
            "scope": "Exact algebraic and zero-divisor controls; no Gaussian grading inferred from these matrices."}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--package", type=Path, required=True); ap.add_argument("--out", type=Path, default=Path(__file__).parent)
    args = ap.parse_args(); depraw = (args.package/"DEPENDENCIES.json").read_bytes(); deps = json.loads(depraw)
    authenticated = []
    for item in deps["dependencies"]:
        raw = (args.repo/item["path"]).read_bytes(); sha = hashlib.sha256(raw).hexdigest()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        need(sha == item["sha256"] and blob == item["git_blob"], "dependency mismatch")
        authenticated.append({"path": item["path"], "sha256": sha, "git_blob": blob})
    proof = (args.package/"PROOF.md").read_bytes()
    result = {"status": "PASS_INDEPENDENT_THREE_QUERY_COSET_CONTROLS", "reviewed_proof_sha256": hashlib.sha256(proof).hexdigest(),
              "reviewed_dependencies_sha256": hashlib.sha256(depraw).hexdigest(), "authenticated_dependencies": authenticated,
              "group_support_controls": group_controls(), "block_identity_controls": block_controls(),
              "sympy_version": S.__version__, "author_verifier_executed": False,
              "universal_proof_is_written_review_not_finite_search": True, "new_complete_kappa": False}
    args.out.mkdir(parents=True, exist_ok=True); (args.out/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))

if __name__ == "__main__": main()
