# S004 third scientific checkpoint

Prepared after the observed clock 2026-11-25 23:51:49 UTC. Work continues
to 2026-11-26 01:01:15 UTC. These are written mathematical components,
with independent reviews and finite exact controls. No complete multiplier
execution, formal-kernel proof, human review, practical cutoff or priority
certification is claimed.

## 1. Complete-bound status

The shared unconditional envelope remains

    H(n)<=2^{O(s^(2/3)(log2(s+2))^(1/3))},
    s=log2(1+log2 n), uniform O(n) cells ever visited.

Concurrent E002 admitted this bound, with independent same-scale S003 and
now E003 constructions preserved. S004's JR-only conditional theorem
still gives H<=2^{O_c(s^(2/3))}; JR is open. No new unconditional S004
complete multiplier is admitted. OWL below improves only the Fourier
component and does not by itself remove the interchange loss.

## 2. Geometry results admitted

**Heterogeneous Fourier invoice (A, independent C review, lead review and
replay).** For even L=2r and q_i=2^{t_i}, binary Gram rank is exactly
D=2+sum(q_i-2), while rational charged rank is at least e_r(q_i-1).
Literal first-difference free incidence is the odd subset sum of products
t_i. The positive expression D[lambda+m rank(P)/N] has logarithm
Omega(sqrt(log m loglog m)), even without the usual hard charged-rank
guard. Heterogeneous alphabets, better Gram-rank accounting and charged
rank compression do not improve this specified invoice. This is not a
lower bound on actual Fourier time or arbitrary decompositions. Proof:
`route-a/heterogeneous-fourier-invoice-barrier.md`.

**Parity-weighted gate (A, independent C review, lead review and replay).**
An exact rational weighted rectangle representation of the odd-Hamming
graph transfers to the actual free matrix I-P with local-load multiplier
at most 2^L. A fixed vertex determines each equality-cylinder word, so
there is no q^j local factor. A basic rational solution has coefficient
bit heights O(R log R), with bounded exponential preflight and polynomial
workspace. Odd denominators are used only in the numerical rational
branch. The open OWL hypothesis asks for exp(O(L)) poly(log q) side load;
JR implies it, but no converse is proved. For q>2 the odd graph has full
rational rank N, so fewer than N terms cannot become exact just by choosing
weights. Proof: `route-a/parity-weighted-fourier-gate.md`.

**JR local-load gates (lead, independent C review).** Any rectangle cover
of C(q,k), even with correlated sides, satisfies
sqrt(ell_L ell_R)>=[2(q-1)/q]^k and
q<=binom(ell_L+ell_R,ell_L). The latter reproduces the classical set-pairs
argument. Exact partitions are sparse incidence factorizations with
intersection count zero or one. Total rank forces q^k rectangles, not
q^k local load. The earlier C(4,2) opposing-star example therefore has
globally optimal common load three and optimal rectangle count sixteen.
This finite optimum neither proves nor refutes JR. The P4-free literature
provides a sufficient global partition-count route, with no asserted
reverse transfer to the local parameter. Proof: `jr-local-load-gates.md`.

## 3. Full-alphabet algebraic bounds admitted

**Survivor quotient (C, independent B review, lead review and replay).**
For support-degree-t P over the full r-root product algebra, the quotient
by chi I-P is spanned by exponents satisfying n_h<=n_0+h t for every h.
The resulting multinomial tail improves the preceding averaged-cut bound.
Module invariance and strict weight descent are proved without commuting
coefficient matrices. For fixed r and t=o(sqrt m), the optimal limiting
normalized rank error is 1-1/r, attained by a constant scalar. Binary
rare-error tails remain stronger in some other regimes. Proof:
`route-c/survivor-basis-rank-refinement.md`.

**Equivariant-sector active volume (joint lead/C, C audit, lead replay).**
An equivariant plurality rule splits all regular monomials, including
ties, into r equal sectors cyclically permuted by chi. Every sector map
differs from chi by rank at least (1-1/r)NW. A degree-one query crosses
sectors only at a near-tie boundary of mass tau_1=O_r(m^-1/2). Completing
singular sector blocks to invertible blocks costs at most twice their
boundary rank. This treats inverse queries without assigning an artificial
small polynomial degree to their inverses. The actual network telescope,
including width changes and genuinely shared ports, gives

    E+H/W+tau_1(Q_direct+2Q_inverse)/W >= 1-1/r.

Noncommuting numerator/denominator fractions and singular compatible
denominators have explicit related bounds. The baseline is exact; only
the boundary estimate is asymptotic. The final theorem uses the sharper
top-two-count gap tested independently. Proof: `plurality-active-volume.md`.

Both results require the full root alphabet. A uniform abstract spectral
average is not automatically a physical normalized rank under unequal
multiplicities. Exact common-spectrum port implications use identities
at every spectral point. The actual order-five two-by-two gate has only
{1,zeta,zeta^-1}; no full five-root conclusion is imported. These are
scoped algebraic results, not general tape-time lower bounds.

## 4. Dense forward-recurrence correction admitted

A and C independently accepted B's H1/H2; lead read the complete proof
and replayed its self-contained checker. If an ordinary residual satisfies
a normalized forward recurrence of order <=s, its first 2s terms determine
it within that promised class. A bounded common-minor rational solve,
small prime avoiding its denominator, and prime-power modulus above twice
the error height enable exact block emission. Every block uses two short
packed products and charged coefficient reductions. With V=D tau and
K=(s+1)^3(tau+ceil(log2(s+2))+1), the bound is

    O_alpha(V(1+log2(K+1))^alpha+K^6), O(V) visited cells,
    for each fixed alpha>1/2.

K>V invokes schoolbook multiplication, preserving the common cap. A's
physical review explains the at-most-three-block reduction of raw
coefficients. For the stated subexponential orders, correction lies below
n sqrt(log n). No fast candidate supplier or general promise verifier is
provided.

The supplier obstruction uses prefix injectivity: a linear space all of
whose members have some order-<=s recurrence has dimension <=s. For W
rows the rank is <=Ws. Input-dependent recurrence coefficients do not
evade the argument. It also applies under coordinatewise zero-faithful
integer encoding, without reducing rational denominators into a field.
A terminal spike shows why a finite low Hankel rank is a different promise.
Proof and prior-art/read scope: `route-b/dense-recurrence-residual-repair.md`.

## 5. Exact evidence and reconciliation

Lead isolated replays passed:

| Component | Selected exact evidence |
|---|---|
| Heterogeneous Fourier | 13 matrix families, 101,200 entries, 1,452 profiles |
| Parity-weighted transfer | 8,720 identities, 3,176 adverse controls, eight ranks |
| Local-load gates | 11 partitions, 5,890 correlated-side capacity cases |
| Survivor quotient | 66 matrix tests, 41 noncommuting cases, 31,697 descents, 1,335 spectral ranks |
| Equivariant sectors | 4,653 phase identities, 16,383 boundary checks, six singular block completions, 36 fractions |
| Dense recurrence | 36 recoveries, 697 products, 330 blocks, 80 prime bounds, 72 prefix gates |

Finite checks supplement the named proofs; they do not prove asymptotic
claims on their own. Dependency hashes are in `replays/manifest-wave3.json`.
Dense primality predicates use integer isqrt in the final isolated replay.

Shared head d88a36eea2010113e08f83f49bbe50886111ceff is preserved. Lead fully
read E002's noncanonical zero-Gram-side incidence proof and E003's exact
one-order/laminar crown obstruction, plus E002's RV admission. They are
compatible with JR: the former retains its explicit within-side condition
and forces the two-thirds power without the logarithmic correction; the
latter rules out one global order or laminar family, not all rectangles.
E002's RV-I/RV-W physical hypotheses remain open, and its separate
conditional log-free theorem retains its own attribution. No complete
fresh S004 review of every newly arrived concurrent file is claimed.

## 6. Active portfolio

A now studies local endpoint preconditioning beyond the literal incidence
bill. B moves to bounded-amplitude dense residuals, with small-modulus
convolution and actual precision costs. C tests the missing subset-alphabet
extension for the actual order-five gate. Lead audits these interfaces and
continues durable integration. These new candidates are outside this
admission. Work remains active to the requested endpoint.

During publication, concurrent S003 checkpoint 72ad1c4e9259b43ff0ea8f76e6d4e2001d3c3ebe advanced the branch. It was reconciled without discarding any concurrent state or forcing the branch. The earlier API commit object was not adopted as a checkpoint.
