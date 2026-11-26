# S004 fourth scientific checkpoint

Prepared during the active three-hour session after the observed clock
2026-11-26 00:16:10 UTC. Work continues to 01:01:15 UTC. This admission
concerns written components, independent review and exact finite controls.
It does not report an executed full multiplier, formal proof or human review.

## Complete-bound status

The shared unconditional written construction remains
H(n)<=2^{O(s^(2/3)(log2(s+2))^(1/3))}, s=log2(1+log2 n), with one O(n)
bound on cells ever visited. E002 supplied the first admitted variable
profile of this scale; S003 and E003 independently obtained the same scale.
S004's complete conditional theorem remains JR => H<=2^{O_c(s^(2/3))},
where the exact local-load rectangle hypothesis JR is open. None of the
following components supplies a new unconditional complete multiplier.

## Fourier endpoints: a changed local executor

A's EP1--EP13, independently reviewed by C and the lead, precompute a full
auxiliary Fourier transform per label. A requested partial transform then
needs only the inverse complementary axes. For a free rectangle I x J and
r_I=dim span(I), choose H=span(I)^perp. With

    K=(1/N) sum_R [(r_I-1)|I|+r_I|J|],

the sufficient free-axis bill is 2(D-1)+2K. Charged terms, coordinate maps,
copies, rational heights and numerical guards remain paid. Fixed auxiliary
phases are independent of j; distinguished-coordinate phases stay in the
middle maps. The symmetric two-channel extension chooses the smaller of
(r_I-1)|I|+r_I|J| and r_J|I|+(r_J-1)|J| per rectangle, paying at most
4(D-1) global axes. Output phase order P_w^* F_w^* is essential.

For literal first-difference rectangles, proper product sides have rank
1+sum(a_i-1), giving K=lambda+2(q-1-t)lambda'. At q=4,L=4 the exact local
axis invoice falls from 800 to 306. This is not a runtime benchmark. The
specified positive invoice, even with charged-rank compression, retains
logarithm Omega(sqrt(log m loglog m)); no complete exponent changes.

The lead subsequently read E003's independently derived rank-weighted
Walsh invoice at 8fbe12b3c76979ce11355a63bddfcdfcd4227585, containing the
same balanced formula with a separate physical executor gate. These are
parallel derivations; no priority claim is made. S004 supplies its own
source-phase proof and asymmetric two-channel option.

Proof: `../route-a/fourier-endpoint-preconditioning.md`.
Review: `../route-c/REVIEW-FOURIER-ENDPOINT-PRECONDITIONING.md`.
Lead isolated replay: 153,896 partial identities, 4,368 phase/adjoint entries,
84 channel aggregations and 8,408 side ranks, with adverse phase controls.

## Actual subset spectra and physical multiplicities

C's SB1--SB8, independently reviewed by B and the lead, provide the missing
invariant decomposition for the actual order-five gate. Five selected points
in two ternary coordinates have all five target products; the other four are
singleton pieces. Four binary coordinates similarly contain a regular piece.
For physical field-pair multiplicities, an explicit selected-word construction
retains regular fraction at least 5/256 uniformly in the unequal field sizes.

Dimension-weighted tensor strata give K_* as a sum of independent Bernoulli
variables. Put pi_0=Pr[K_*=0] and eta_d=E[tau_d(K_*)]. The actual-rank bound is

    E+H/W+eta_1(Q_direct+2Q_inverse)/W >= (4/5)(1-pi_0).

Since eta_d=O((d+1)/sqrt(m)) and pi_0 decays exponentially, degree o(sqrt(m))
or active volume o(W sqrt(m)) forces limiting error plus port rank at least
4/5. Scalar prediction attains the constant in the fixed-coset model. Target
powers F1,F2,F4, noncommuting fractions and arbitrary ports mixing strata
retain the stated conclusions. This is a common-spectrum linear-model rank
theorem, not an efficient physical basis change or a general tape lower bound.

Proof: `../route-c/subset-spectrum-blocking.md`.
Review: `../route-b/review-subset-spectrum-blocking.md`.
Lead replay: 4,808 invariant entries, 161 target transitions, three inverse
completions, six noncommuting fractions, three strata-mixing ports, 256 actual
multiplicity blocks and 192 boundary profiles. Later improved constants and
ratio-subgroup classification are separate drafts outside this admission.

## Dense bounded-amplitude correction

B reconstructs the classical radix-three cyclotomic convolution over Z/2^a
with explicit principal roots, an idempotent deleting one third of pointwise
products, canonical coefficient lifting and a fixed-tape schedule. It is not
presented as a new polynomial multiplication algorithm. If |(AB-C)_i|<=B,
choose 2^a>2B and recover the residual by centered modular lifting. For
D=2h, tau=ceil(log2(2Emax+2)), V=D tau and fixed alpha>1/2, the cost is

    O_alpha(V+h a(1+log h)
                  [1+loglog(h+2)+(1+log(a+1))^alpha]),
    O(V) cells ever visited.

The normalized recurrence is F(ell)<=2F(ceil(ell/2))+O(ell), with exactly
2k children. A's stack supplier consumes parent frequency operands from
their ends and appends child results above current-frame boundaries on fixed
tapes. Transfer and cleanup are O(ma) per child, with no parent-prefix scan;
sibling regions are reused. Geometric storage alone would not prove this.

Under structural E_i>=0 and a capped budget 1<=a<=tau, least-nonnegative residues and sum r_i=E(1) give a
sound acceptance test. Review caught a missing scalar-product charge: this
optional test additionally costs O_alpha(tau(1+log(tau+1))^alpha). It is
absorbed in the usual h=Theta(n/log n) regime, but not for constant h and
arbitrarily long coefficients. The promised corrector itself needs no test.
Small amplitudes permit fast correction, but no fast candidate supplier is
provided. Basis-vector and bilinear matrix witnesses limit the studied
suppliers without excluding arbitrary later nonlinear constructions.

Proof: `../route-b/bounded-amplitude-residual-repair.md`.
Independent A review: `../route-a/review-bounded-amplitude-residual.md`.
Scheduling proof: `../route-a/amplitude-fixed-tape-stack-supplier.md`.
A reviewed the core snapshot 206372011b3951cfaeef20c60626e0b36efa84597f24919d3c3a6820cddb38b4.
The only later proof change caps the optional modulus width at tau; C found
that guard and the lead checked the exact diff and its space justification.
Lead read both proofs completely and replayed 60 full cyclotomic products,
405 recursive 2k invoices, 192 orthogonality sums, 24 FFT/inverse controls and
12 ordinary repairs, including aliasing/sign controls. No tape simulation.

## A precisely shaped tall-Hankel extension

For H_s(E)=(E_(i+j)), 0<=i<D-s and 0<=j<=s, rank<=s implies a normalized
forward recurrence of order at most s on the first D-s coordinates. Take a
nonzero kernel vector and its highest nonzero coordinate; no leading minor
is assumed. The admitted recurrence corrector recovers that prefix; a short
reversed product supplies the final s coefficients. At D=2h the last product
coefficient is zero and the formal reversal degree is D-2. Previous full
cost and space bounds remain. First-s/last-s projection injectivity gives
image dimension at most 2s, or 2Ws for W rows.

The terminal impulse is covered, but arbitrary Hankel conventions and a
general promise verifier are not. Proof: `../route-b/dense-hankel-tail-extension.md`.
The lead independently reviewed it and wrote `verify_tall_hankel.py`: 19,305
sequences, 249 promised cases, 684 recurrence identities, 108 reversed tails,
nine terminal impulses and seven unpromised hidden-middle controls passed.

## Sources and continuing work

The lead reread the full pinned Fourier endpoint subsection. Additional
primary reading covers Bostan--Mori Section 2.1, Lemma 1 and Algorithms 1--2,
and Cantor--Kaltofen Sections 1--2 through the cyclotomic operation bounds.
These give prior-art context, not a free tape-cost supplier or novelty audit.

The lead fully read E002's Weyl-star batching component and E003's exposed
star-transposition normal form and support-monotone shared-sum obstruction.
A commuting Weyl common basis does not automatically diagonalize the actual
noncommuting star swaps. The shared-sum theorem is not a physical routing
lower bound. Those limitations are preserved.

Active work now concerns reuse among preconditioned transforms, mixed dense
small/sparse large residuals, and the ratio subgroup of a subset spectrum.
Concurrent S003/E002/E003 records are preserved. All claims retain their
explicit models, unproved premises and exact-check scope.

Publication reconciliation preserves E002 final checkpoint ba39de853d247c06158eff1bebd4022f297f24a4 and its earlier endpoint-reuse checkpoint. Their files and completion state were retained without force-push; no fresh full audit of every final concurrent file is claimed.
