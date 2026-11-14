# Pointwise fine-prime specialization of the arbitrary-order rank theorem

Status: GO, allocated by the lead after the bounded feasibility stage.
A9 is published at `085b30f8e036f69421d5953d0993ac4974ec3f24`, tree
`547ecf1409e2c3738218cd7678c931c4110bda43`, proof SHA
`3e87c32b9cb3695dc42c2ef10da9c05e74d1742a37e49ce0fe5890ea093463dc`.
Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.

## Exact proposed statement

Let g>=1, N=2^g, let s_1,...,s_g be distinct odd primes, t_i positive
powers of two, and alpha a common positive integer. Set

    q_i = exp(-pi alpha^2 t_i/s_i),
    H = tensor_i [[1,q_i],[q_i,1]],
    R_N = 2 ceil((N+3)/5),
    r = min(R_N, min_i s_i - 1).

Every vertex ordering of H and every correspondingly ordered exact inverse
has ordinary nilpotent Stein rank at least r. The conclusion is pointwise
for every tuple in this declared family. Both quantities in the minimum
are even because the primes are odd. For 2^g<=min_i s_i-1, the full A9
lower bound R_N is recovered.

No gcd(alpha,s_i)=1 condition is needed when alpha is common: absorb
alpha^2 into the common transcendental base. The source uses an integer
alpha, so a larger algebraic parameter domain is unnecessary.

## Proof route

A9 constructs, for each ordering, a principal minor of size r_v>=R_N with
coefficient ±1 at (q^v)^r_v. Its matching-coefficient matrix is a union of
even paths. For any even r<=r_v, retain an even prefix of each path with
lengths summing to r. This remains a union of even paths with determinant
±1. Thus a size-r Gaussian minor is a nonzero integer polynomial f with
each individual variable degree at most r.

Write S=product_i s_i and z=exp(-pi alpha^2/S). Then q_i=z^e_i where
e_i=t_i S/s_i. For exponent vectors 0<=a_i,b_i<s_i, equality of the weighted
exponent sums implies modulo s_k that (a_k-b_k)t_k(S/s_k)=0. Its other
factors are invertible, hence a_k=b_k for every k. Distinct monomials in
this degree box give distinct powers of z, so substituted f is nonzero.

Gelfond-Schneider makes z transcendental: use base -1, log(-1)=i*pi,
and algebraic irrational exponent i alpha^2/S. A nonzero integer polynomial
cannot vanish there. A9's exact Schur-complement/reversal identity transfers
the all-order bound to inverses. Each q_i lies in (0,1), so H is SPD.

This gives no minor-magnitude or singular-value bound. The degree restriction
is essential: when t_1=t_2, q_1^s_1=q_2^s_2. These parameters are not
algebraically independent without a degree restriction.

## Source interface and group scale

Exact canonical sources are
`research/native-kappa-30201655/modern-sources/FINE-PRIME-PADDING.md`
and `research/native-kappa-30201655/modern-sources/GAUGEFREE-INTERIORS.md`.
FINE-PRIME section 1 supplies distinct odd primes and dyadic targets;
section 2 fixes alpha=ceil(sqrt((4/pi) log(16p))). GAUGEFREE section 2
identifies narrow gamma_i=pi alpha^2 t_i/s_i and the normalized shifted
kernel exp(-gamma_i u^2+2 gamma_i shift_i u).

Removing its linear shift by exact diagonal conjugation yields an unshifted
Toeplitz core whose two-point factor is [[1,q_i],[q_i,1]]. The physical
narrow block also has a chirp similarity. Ordinary Stein rank is not
invariant under these diagonal similarities. The claim is about the exact
unshifted normalized core, not the shifted/chirped/rounded physical matrix.
Nor does a two-point principal section automatically lower-bound the
ordinary Stein rank of an arbitrarily ordered larger matrix containing it;
the one-step shift changes when vertices are deleted.

The source has d=Theta(p^epsilon), log r_source=Theta(p/d), and
min s_i=Theta(r_source), hence log(min s_i)=Theta(p^(1-epsilon)).
Small groups g=O(p^(1-epsilon)) satisfying 2^g<=min s_i-1 receive the full
linear A9 floor. If g=Theta(p^beta) with beta>1-epsilon, the cap instead
supplies rank at least exp(Theta(p^(1-epsilon))), still superpolynomial in p
but not linear in N=2^g. Dense separate generator-vector storage is at least
2Nr scalar slots for this exact core format only. No physical cost or
multiplication consequence follows without further interfaces and error bounds.

## Primary citation and bounded overlap

Primary source opened and read: A. Gelfond, *Sur le septieme probleme de
Hilbert*, Bulletin de l'Academie des Sciences de l'URSS (1934), no. 4,
623-634, logarithm theorem on p. 628. Official record with full text:
https://www.mathnet.ru/eng/im4924 . The theorem is a cited classical input,
not re-proved or numerically certified. Schneider's independent 1934 proof
retains its classical credit. No novelty claim attaches to transcendence
or the CRT injectivity argument by itself.

Bounded live GitHub searches returned no Gelfond or Schneider PR match.
The transcendental+Gaussian query returned #6976 (remaining diagonal),
#6131 (concentration), #684 (chirp-domain audit) and #524 (carry convolution);
their bodies concern other interfaces. Monomial+transcendence returned
#3974/#3992 Toom work. Nonvanishing+prime found cyclotomic/inverse work.
This is not complete history, Discussion or unpublished-work coverage.
A9 is the immediate mathematical predecessor.

## Initial exact evidence and next action

FEASIBILITY-CHECK.json records three exact exponent-box injections and the
high-degree collision q1^3=q2^5 for s=(3,5), t=(8,8). It evaluates no
floating exponential and makes no finite transcendence claim.
The written path-trimming/CRT arguments supply the universal statements.

The lead approved a 60-minute source-specialization package. It will retain
source bytes/pins, prove the smaller-minor lemma, verify literal exponent
collisions and trimmed polynomial minors by exact methods, preserve a
noncoprime-denominator countercontrol, and obtain separate review.
No Cp margin, physical-gauge transfer, full caller or kappa claim is allowed.
