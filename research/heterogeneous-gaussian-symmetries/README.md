# Distinct fine-prime Gaussian widths prevent long symmetry orbits

**Exact classification and scoped dense-certificate obstruction. No new
kappa and no foundational assumption discharge.**

For the normalized Gaussian tensor

\[
H_{xy}=\exp\left[-\sum_i\gamma_i(x_i-y_i)^2
                 +2\sum_i\gamma_i a_i(x_i-y_i)\right]
\]

on a rectangular grid with n_i>=2 and gamma_i>0, every exact simultaneous
row/column permutation symmetry is a signed coordinate permutation.
It can exchange axes only when their n_i and gamma_i agree; its signs
must also match their shifts. This includes two-point axes and coincident
physical side lengths. The proof quantifies over all vertex permutations.

If the widths are distinct, only reflections of zero-shift axes remain.
Every symmetry has order at most two and at least T/2 vertex cycles,
where T is the chosen tile volume. If all shifts are nonzero, only the
identity remains. The same exact symmetry group applies to the inverse.

The retained fine-prime source supplies distinct odd primes s_i and target
sizes t_i in {r,r/2}. Writing m_i=(r/t_i)s_i gives distinct integers below r:

| Normalized kernel | Width | Minimum separation |
|---|---|---|
| Broad | b0 m_i/r | at least b0/r |
| Narrow | A r/m_i | greater than A/r |

Thus the preceding homogeneous long-orbit construction does not transfer
to a square normalized tile of the displayed form across these distinct source axes.
The row and column index sets and translated shifts must match that form;
rectangular or differently indexed source blocks need a separate interface.
Its specified dense format retains exactly 2cT scalar slots, so it now lies between
T² and 2T². This is a statement about that explicit format, with prescribed
zero slots retained. It is not a displacement-rank or runtime lower bound.

## Rounding remains scoped and explicit

For |a_i|<=1/2, every ideal entry is at most one. Entry error eps changes
a pair product by at most rho=2eps+eps². Let

`A*=exp(-2 gamma_max)-exp(-4 gamma_min)`,

`B*=2 exp(-2 gamma_max) min_(i!=j)|gamma_i-gamma_j|`.

If gamma_max<2 gamma_min and `2rho<min(A*,B*)`, each exact stored symmetry
preserves the colored unit-edge graph. Connectivity then forces each
coordinate map to be identity or reflection. No lower bound on tiny shifts
is needed, and no equality with all reflections is claimed.

For the retained fine-prime widths these gaps are at least 2^-o(p), so
`poly(p)2^(-Cp)` entry errors satisfy the guard eventually. This applies
at the ideal normalized boundary only. Gauges, repeated copies, identity
spectators, periodic tails and a complete current caller are not silently
identified with this tensor.

## Verification

```sh
python3.12 -I -W error -B research/heterogeneous-gaussian-symmetries/verify.py
python3.12 -I -W error -O -B research/heterogeneous-gaussian-symmetries/verify.py
```

Expected status: `PASS_HETEROGENEOUS_GAUSSIAN_SYMMETRIES`.
The verifier is read-only and uses only the Python standard library.
It imports no predecessor executable. All symmetry decisions use exact
rational exponents or rigorously enclosed and rounded dyadic entries.

Eleven complete searches inspect 243,414 vertex permutations, including
two-point axes, unequal edge counts in a square hull, coincident axis and
diagonal lengths, opposite shifts and repeated widths. Three more complete
small-grid searches verify the rounding guard. Controls include equal-width
long cycles, coarse rounding to an identity matrix, tiny shifts that lose
their asymmetry, and a bounded nonuniform perturbation that destroys a
reflection. Finite checks corroborate the universal written proof.

See [PROOF.md](PROOF.md) for the exact theorem, inverse statement, minimum
cycle formula, complete source boundary and limits; [RESULT.json](RESULT.json)
and [VALIDATION.json](VALIDATION.json) record executed checks.

## Provenance and credit

Canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`.
The exact homogeneous predecessor is CubeJerry commit
`2ae2fa14eeefe301652f62313b137a97036ab13d`. Its proof and the two canonical
source notes are retained unchanged with full byte/Git pins in
[DEPENDENCIES.json](DEPENDENCIES.json). The selected frontier is unchanged.

Prepared for **@CubeJerry** with substantial **OpenAI assistance**.
Credit the homogeneous orbit authors, Chafik Boukhalfa's fine-prime work,
IdeaOuter and the fractional-shift contributors, Vlado Vojdanovski and the
Gaussian audits, and all authors named in the retained notices. See
[NOTICE.md](NOTICE.md). No human or proof-kernel certification is asserted.

## Open next questions

Identify a complete current caller boundary that has these exact normalized
factors and an authenticated entrywise error contract. The retained source
notes alone do not establish that full-map identification.

Find an implicit, compressed or different-successor representation that
avoids the specified dense global-symmetry cycle format. This proof does
not bound arbitrary displacement rank or the cost of such alternatives.
