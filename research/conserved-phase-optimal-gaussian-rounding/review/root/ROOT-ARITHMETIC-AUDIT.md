# Exact arithmetic audit of the root checker

The unchanged source `check_candidate.py` is a `Fraction` implementation of
the proposed map. This note records an independent line-by-line arithmetic
check before its outputs were compared with the frozen integer checker.

## Grid pair and branch

Its `B(a,b)=(a+b,a-b)` is the proof's matrix `H`; `J(a,b)=(-b,a)`. In the
mixed parity branch, `t=B(Jd)/2` is exactly `T J d`, `M(t,p)` toggles the
least-score coordinate with type `p` on axis zero and `1-p` on axis one,
and `B(M(t,p))` is the output difference `d'`. The inverse first computes
`t=B(d')/2=M(t_old,p)`, toggles again, then applies `-J H`; this is the
proof's `d=-J H M_p(Td')`. In the equal-parity branch it uses `Jd` forward
and `-Jd'` backward. The returned four integers are ordered as the two real
coordinates of `u'`, then the two real coordinates of `v'`.

`pair2` uses exact half-integers. Type 0 pairs magnitudes
`1/2+2k` with `3/2+2k`; type 1 toggles the central `-1/2,+1/2` pair and
pairs `3/2+2k` with `5/2+2k`. Lower scores for the two phases are disjoint,
so `M`'s `need` check correctly requires a unique selected axis. The score
is unchanged by toggling, making the same selection on the reverse pass.

## Exact sum, error and radial checks

The output reconstruction checks divisibility by two exactly. Its
`C2` matrix is `2 C_+` in real coordinates `(Re u, Im u, Re v, Im v)`:

```text
 1 -1  1  1
 1  1 -1  1
 1  1  1 -1
-1  1  1  1
```

Therefore `err4=sum((2*y-C2*x)^2)` is four times the combined squared
Euclidean error. It equals zero in the equal-parity branch and four in the
mixed branch, matching the proof's exact error values zero and one.

For input/output pair squared norms `n,m`, its integer radial predicate is
equivalent to `|sqrt(m)-sqrt(n)| <= 1/sqrt(2)`: after squaring the desired
inequality, it is `2m+2n-1 <= 4 sqrt(mn)`. A nonpositive left side passes
automatically; otherwise both sides are nonnegative and the exact test is
`(2m+2n-1)^2 <= 16mn`. No floating-point square root is used.

The checker also verifies both inverse compositions, exact sum, global `i`
covariance, wire swap, and `F(Cx)=C(F^{-1}(x))`, equivalent to
`F^{-1}=CFC`. Its randomized cases use a fixed seed and exact integers. All
validations use explicit `need` calls, so `python -O` does not disable them.

## Cross-check and limits

`verify.py` compiles these recorded source bytes directly and compares them
with the frozen doubled-half-grid integer implementation. The cross-check
covers the complete integer cube `[-4,4]^4`, the exact 60-case deterministic
large sequence, and the 20 fixed power-of-two cases. It also records the
phase-assignment mutant
`u=(-2-2i), v=(-2-i)`, for which the wrong phase rule violates global `i`
covariance, and the exact `F^4` counterexample from the proof result.

This is a finite implementation cross-check of a shared candidate formula.
It is not a formal proof, blind review, or evidence of any selected caller or
physical implementation.

## Transfer of the #6778 row/column obstruction

The related theorem is pinned at head
`f711bd201a037ba6a7e3fed72d00bfcbf4f0420a`, path
`research/gaussian-rounding-tensor-obstruction/PROOF.md`, Git blob
`8da4abbf5e3b3eb7fc02fc24feeea6cff631f439`, SHA-256
`8d5480e061b9ec00b5d9bbcf6d1c6945857606814efd526ddf4c3d2c72ec81ec`.
It proves that a map with global Gaussian-unit covariance and exactness on
all integral ideal images of `U=M^{tensor n}` cannot commute with applying
that same map separately to rows and columns.

For `n=1`, `U=M` is exactly `C_+`. The candidate has global `i` covariance;
applying it twice gives covariance under `-1`, so it has the required four
global Gaussian units. An ideal image `C_+(u,v)` is Gaussian integral exactly
when the real-coordinate parities of `s=u+v` agree: `d` has the parity of
`s`, and `Jd` has that same parity precisely in this branch. The candidate
selects `d'=Jd` there, hence returns `C_+(u,v)` exactly. Both #6778
hypotheses therefore hold for this map.

The verifier checks the theorem's `n=1` witness in its matrix convention.
Here `lambda=(-i,1)`, `e0=(1,0)`, and `X=lambda e0^T` has rows `(-i,0)`
and `(1,0)`. The candidate sends `F(e0)=(0,1)`. The two orders are
`R_F C_F(X)=((1,-i),(0,0))` and
`C_F R_F(X)=((0,1-i),(0,0))`; their commutator is the nonzero first row
`(1,-1)`. The exact check is a finite application control; universal
impossibility comes from the pinned #6778 theorem. This excludes same-map
stateless row/column commutation but does not exclude ordered execution,
different maps, or an enlarged state/representation.
## Forward-only optimum under conjugation-as-inverse

Let K conjugate both entries; K preserves the Euclidean pair norm. For any
bijection F satisfying F^{-1}=K F K, the identity F(K F(x))=K x shows
that every radial change Delta=||F(x)||-||x|| is paired with -Delta at
y=K F(x). Therefore the forward outward supremum equals the bilateral
supremum. This is an all-input algebraic implication, not a finite test.

Applying it to the proved map gives forward outward supremum exactly
1/sqrt(2). The universal bilateral lower bound in proof/PROOF.md implies
the same lower bound for every exact-sum, error-at-most-one bijection that
also satisfies this conjugation-as-inverse identity. Thus the constant is
optimal for forward outward slack in that narrower interface class. No
forward-only lower bound is claimed for exact-sum maps lacking that inverse
identity. This corollary uses no additional phase or periodicity premise.
