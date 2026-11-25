# Independent Route B audit of the two-converter endpoint

Reviewed `route-c-work/two-converter-repair-floor.md`, Sections 1--5,
on 2026-11-25 at 23:02 UTC. The restricted invoice theorem and its stated
scalar sharpness **pass**. This audit does not identify the invoice with
physical tape time, nor claim a multiplication lower bound.

## Restriction and parity correction

Fixing any subset of coordinates cannot increase the degree of the
table-free predictor. The target factor from fixed coordinates is a
nonzero scalar, so the two-point rank theorem applies to the remaining
coordinates without changing the normalized port-width accounting.
Averaging restores the original width/error charge. Thus all inequalities
`h/W>=delta_n(t)` for `t<n<=m` are available at once.

When `m-t` is even, `t<m` implies `t<=m-2`, so the chosen `n=m-1`
still exceeds `t`; there is no missing endpoint. When `n-t` is odd,
exact binomial symmetry removes at most `t/2` copies of the largest atom
from a half of the distribution, including the half-central-atom case
when `n` is even. This proves (T3).

The central atoms of `Bin(2v,1/2)` and `Bin(2v-1,1/2)` agree. The atom
of `Bin(2v+1,1/2)` is smaller. Consequently `M*_m` upper-bounds both
possible selected atoms, with the `m=1` case direct. In particular the
zero-stage port width is at least `W/2`, exactly what the q=2 induction
needs. The original even-m bound alone would lose that fact.

## Tree induction and constants

The estimate `A_m<=m` follows because `M*_m` is the largest atom of a
distribution on `m` outcomes for `m>=2`. Thus the stated leaves pay the
potential. At an internal node, the complete child invoices pay at least
`2A_m sum h_i`; combining with the local `Wt` charge and (T4) gives
`A_m W` exactly. Larger local degrees, extra calls, or extra nonnegative
costs only increase this invoice. Finite structural induction is valid
without any uniform depth hypothesis.

The asymptotic `A_m~sqrt(pi m/2)` is the standard central-binomial
asymptotic. The stated elementary bound yields the `6/5` consequence
precisely because `3(m-1)/2>=(36/25)m` for `m>=25`.

## All restriction inequalities permit the claimed scalar sharpness

The relaxed t=1 example must satisfy every available n-restriction, not
only the selected one. It does. Put
`p_(2r)=binom(2r,r)/4^r`. For even `n=2r`,

    delta_(2r)(1)=(1-p_(2r))/2.

The central atom decreases with r, so this value increases with r. For
odd `n=2r+1>1`,

    delta_(2r+1)(1)=1/2-p_(2r+1),
    p_(2r+1)=[(2r+1)/(2r+2)]p_(2r)>p_(2r)/2.

Thus the odd value is smaller than the preceding even value. The maximum
of all `delta_n(1)` for `1<n<=m` is therefore attained at the largest
even n, and is exactly `(1-M*_m)/2`. The relaxed construction using that
port mass satisfies all the corrected rank constraints.

Its finite-depth recurrence has local cost one and total child mass
`1-M*_m`, hence the displayed geometric sum converges to `1/M*_m`.
Since these masses are rational, a sufficiently divisible integer root
width realizes each finite relaxed tree with integer widths. No actual
predictor or physical transform construction is implied by this scalar
feasibility check.

## Scope

The full-batch Wt pricing and the two independent complete child invoices
are indispensable model premises. Correlated inputs, shared subcomputations,
changing spectral dimension, or partially active queries cannot be
silently assigned these invoices. The note states these limitations.

Prepared for @CubeJerry with substantial ChatGPT assistance.

## Additional audit: lead's active-row and inverse-gate composition

Section 6, equations (T7)--(T9), was read at 23:05 UTC and **passes**.
For odd n the central two-point cut has target commutator rank exactly
`2^n W`, and query boundary ratio
`kappa_n=2 binom(n,(n-1)/2)/2^n`. The audited weighted commutator theorem
therefore gives `kappa_n Q+2H>=W` at an exact node. Fixing one coordinate
for even m preserves affine local queries and every everywhere-defined
inverse, and averaging restores the original active-width charges.

With `B_m=1/kappa_n`, the inequality becomes `Q+2B_m H>=B_m W`.
Port-free leaves satisfy the bound directly. Each port has two complete
child invoices on its h rows, so structural induction is exact and needs
neither a polynomial output nor full-batch local gates. The common
spectral decomposition and separately charged child computations remain
essential premises.

For even `m=2v`, the central atom for `n=2v-1` equals `M*_m`, giving
`B_m=A_m/2`. For odd `m=2v+1`, that atom is
`[m/(m+1)]M*_m`, giving `B_m=(m+1)A_m/(2m)`. The claimed asymptotic
and the m=1 edge case follow. This is a positive active-volume floor;
its asymptotic constant is below one and is not promoted to a physical
time lower bound. Attribution to the lead's recursive composition is
explicit.
