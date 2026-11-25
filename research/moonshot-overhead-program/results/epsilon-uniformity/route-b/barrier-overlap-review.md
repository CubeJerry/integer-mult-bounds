# Scope and provenance of the two multilinear recipe barriers

Status: **comparison passes; no contradiction or new unrestricted lower
bound is identified**. Route B read both S002 documents directly from
commit `848fbf1d7a5e192aa352d79b4d3e36fa06be21ee`:

- `routes/B/multilinear-formula-width-barrier.md`;
- `routes/C/REVIEW-B-MULTILINEAR-COMPILER-BARRIER.md`.

They were compared with E001's
`../route-c/FORMULA-RECIPE-LOWER-BOUND.md`. This is a proof/scope comparison,
not a second claim of the published formula lower bound or a priority claim.

| Reviewed file | SHA-256 |
|---|---|
| S002 `routes/B/multilinear-formula-width-barrier.md` at the commit above | `871e843bfa76be7456e0b64d16a063af53fb5cb141b4f1757539c9ab5687fec7` |
| S002 `routes/C/REVIEW-B-MULTILINEAR-COMPILER-BARRIER.md` at the commit above | `b3dfafbb3e62729cb1635860443b752941e8b525495234e0c6727bd9f855707d` |
| E001 `route-c/FORMULA-RECIPE-LOWER-BOUND.md` | `d171f3c8a01a8b6425f70dc70e9c529970e3cfaba9c2f59a24577a302afc257f` |

## Common result and differences

Both arguments start with the Hrubes--Yehudayoff homogeneous multilinear
formula lower bound for `e_D` and the top component of the original window
predictor. The highest elementary-symmetric term has coefficient
`(-1)^u(-2)^D`; substituting `(1-X_i)/2` cancels its extra signs and powers
of two, leaving `(-1)^u e_D(X)`. Query shifts give invertible variable signs
and one scalar sign, which do not change the formula lower bound.

Both require formal computation of this literal predictor, control of
syntactic degree by its actual degree `D`, and the **unreduced canonical
cyclic compiler**. Products multiply row ranks; a sum of degree `d`
multiplies them by `d`. Degree-one sums therefore have no width penalty.
Both proofs correctly count the higher-degree sums rather than applying
an unweighted formula-size bound directly to rank.

S002 folds all degree-one subformulas and proves by induction that the
number of linear leaves is at most `D(A+1)`, where `A` counts the remaining
sums. E001 removes the expensive sums and counts product components,
giving the same `O(D(A+1))` estimate. Expanding a linear leaf costs `O(m)`
ordinary leaves. The published bound then forces
`A>=D^{Omega(log D)}`. Since rank is at least `2^A`, both obtain

\[
 K\ge 2^{\,2^{\Omega((\log m)^2)}}
 \quad\text{when }D=\Theta(\sqrt{m\log m}).
\]

Together with the balanced construction this fixes the logarithm-squared
scale within the stated recipe. S002's hypothesis that every gate polynomial
is multilinear is slightly broader in presentation than E001's explicit
syntactic disjoint-support restriction. Its top-component pruning preserves
gatewise multilinearity, so that distinction causes no gap in the S002
argument and no conflict with E001's narrower claim.

## Compatibility with the new positive result

The S002 review explicitly exhibits a count-bit formula containing formal
monomials with repeated variables. Its cancellations use the relevant
spectral/Boolean quotient. Thus it does not satisfy the gatewise-multilinear,
literal-formal-predictor premises of the barrier. This independently explains
why the newly admitted fixed-field positive construction can escape it.

The obstruction must not be quoted against arbitrary matrix roots,
nonmultilinear formulas, quotient identities, shared circuits, or compressed
invariant submodules. It does not establish optimality of either global
multiplication envelope. The two sessions independently reached overlapping
restricted conclusions, with different proofs of the leaf-count step.
Both should retain their provenance and the original authors' credit.

No tests were rerun. This comparison does not independently audit the new
S002 IP4 theorem; the lead and Routes A/C own that separate gate.

Prepared with GPT-6 Astra Pro assistance for @CubeJerry. Primary lower-bound
credit remains with Hrubes--Yehudayoff; recipe derivations retain their
separate S002 and E001 credits.
