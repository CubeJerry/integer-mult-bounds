# Independent source audit of the adaptive integer caller

Decision: **the pinned integer/short-transform caller accepts AI and NW with
the claimed adaptive envelope and an absolute linear visited-space bound**.
This is a source-level composition audit. It does not execute a full
multiplier or certify the source's analytic theorems by a formal kernel.

The audit was requested after the independent acceptance of B's adaptive
exact interchanger and A's nonstationary numerical Walsh component. The
lead owns the final theorem and admission. No top-level frontier file is
changed by this note.

## 1. Exact material read and the replacement map

The source revision is OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`. All paths in this paragraph
are under
`preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/`.
I read `integers.tex` in full (491 lines), `permutations.tex` in full,
`walsh.tex` in full, and the candidate-generation, precision, common-tape
and marked-space sections of `uniformity.tex`. The source geometry and
binary normalization dependencies were read separately for NW. Programme
start is `0607d044d1d09489580da0e5828588820e1a6775`.

Let

    F(x)=(x^2 log2(x+2))^(1/3),
    J(k)=sqrt(1+k) 2^[C F(log2(k+2))].

The necessary substitutions are:

| Pinned source interface | Adaptive supplier and retained cost |
|---|---|
| `thm:interchange` | B's AI1–AI11, exact encoded-bit permutation, time V J(u), visited cells C V with C absolute. |
| `lem:packed-xor` | Its eight guarded rotations and exceptional repair use AI; cost V(1+J(u))log(2+k)+poly(k). |
| `cor:bit-positions` | The same fixed number of XOR reductions, cost V J(k)log(2+k)+poly(k). |
| `lem:controlled-blocks` | Its existing batches and Beneš stages, cost V J(k)(log(2+k))^3+poly(k). |
| `lem:tape-walsh` | NW1–NW17, with fixed boundary allowances c,L,D; cost V J(k) and visited cells C V after absorbing fixed logarithmic powers into J. |
| `lem:synchronized-short` | Unchanged exact unitary layer factorization and fixed-degree phase-table preparation. Its selected bits satisfy NW's required count. |
| `eq:integer-budget` and `thm:integer` | Replace k^rho by J(k), retain the explicitly bounded logarithmic layer factors, then substitute Nk=Theta(n). |

Only the first and fifth rows require new research suppliers. The other
rows are the actual source reductions with those costs substituted. They
do not call a multiplier at the target input length as a primitive.

## 2. Fixed guard and control exponents

The source packed-XOR proof attaches an O(k)-bit destination key to an
exceptional numerical record already having Theta(k) bits. This changes
its encoded size by an absolute factor. Binary radix sorting has O(k)
passes and uses a fixed number of streams. The exceptional fraction is
at most 80 s 2^(-G), with s=O(k), so G=C0 ceil(log2(2+k)) pays for all
fixed-degree control and rank computations after choosing one absolute C0.

AI replaces the interchanges inside the rotations. It restores all
occupied auxiliary chunks and uses absolute linear space. Its internal
choice of arity does not appear in the numerical control description.
Within NW, the explicit matrices and selector algorithms have polynomial(m)
description and work, with m<=k and absolute degree. Thus those controls
also fit one fixed polynomial in k. No growing guard coefficient, fixed
rho program table or per-record logarithmic address penalty has been
left unpriced.

For the CRT tree, the left-child controls contain at most half the axes
and therefore at most k/2+O(log k) bits. For large k choose, for example,
the fixed free fraction delta=1/3 in `lem:controlled-blocks`. The target
blocks have O(log k) bits. Recovering the original left digits and
computing their controlled rotations use O(k)-bit integers and
polynomially many operations. All such exponents are source-fixed.

The short-transform block permutations have empty external controls.
Their tables have polynomial(k) size, since a block contains four to
seven axes of O(log k) bits each. The further Beneš-network switch
controls are exactly those already paid in `lem:controlled-blocks`.

Consequently one controlled-block layer costs

    O(V J(k)(1+log(2+k))^3)+poly(k),

and the O(log k) CRT depths or short-transform layers introduce at most
one further logarithmic factor. These are absolute powers, not powers
depending on the current arity.

## 3. Digit shape, prime enumeration and the absolute initial range

The source chooses

    b=ceil(log2 n), h=ceil(n/b),
    k=ceil(log2(4h)), N=2^k.

It constructs coprime cyclic lengths a_i with total padded address width
k and valid volume S>=2h, while each axis has O(log k) bits. The short
prime interval uses l=20ceil(log2 k), x=2^l, so x is polynomial in k.
Even trial division of every candidate in the indicated interval is a
fixed polynomial in k. Products, modular inverses, primality counters,
and all accepted-prime lists are similarly finite fixed-degree work.

The source explicitly checks volume, coprimality, digit width, availability
of borrowed positions and row padding. Its `uniformity.tex` explains that
the program uses schoolbook multiplication when a required shape test
fails and **does not need to compute a prime-gap cutoff**. The accepted
prime-gap theorem supplies eventual success of the tests. This remains
an absolute source dependency; the adaptive arities introduce no new
prime family or arity-dependent number-theoretic cutoff.

The new numerical plan adds computable fixed guards for its coefficient,
norm, spectator and setup bounds. Their eventual success follows from NW.
One may reject a shape that fails those guards as well. Fallback remains
correct and uses O(n) cells. Since all such failures are eventually absent,
the finitely many initial lengths change only an absolute asymptotic
constant. This audit does not supply a numerical value for the source's
prime-gap initial threshold, and none is required by the algorithm's
shape tests.

For accepted shapes, N is between 4h and 8h, k=Theta(log n), and
Nk=Theta(n). These relations are independent of the new arity choices.

## 4. Occupied short-transform workspace and phase preparation

The source proves an exact U_a direct-sum identity on arbitrary borrowed
data, using a unitary truncated-chirp block, a fixed number of amplitude
amplification reflections, and cancellation of the complement action by
conjugation. The number J=64 of reflections is absolute. The analytic
multiplier bound |lambda_xi|<=40 ensures |lambda_xi sin(pi/258)|<1/2.
Thus all L(z) and phase-factor formulas have denominators bounded away
from zero by absolute constants.

For each active axis the temporary transform uses fewer than 8a
coordinates. Dividing neighboring fibers into eight batches leaves enough
occupied coordinates to borrow from the other seven batches. The exact
identity restores every borrowed value before the next batch. Grouping
four to seven axes keeps each block at polynomial(k) coordinates and
global depth O(log k). No workspace factor is multiplied over all axes.

This source argument is unchanged by AI or NW: its primitive pair
operations become three Walsh rounds with block-dependent phases. Each
global Walsh round selects at most one bit per block, hence at most
O(k/log k) bits. NW permits arbitrary specified positions and restores
the same record order, exactly matching this interface.

Phase-table construction uses polynomially many short roots of unity,
fixed-length formulas and polynomially many summands, followed by square
roots and divisions with bounded conditioning. All tables have a fixed
polynomial number of entries. Precision Ck+O(log k) pays their error.
This is one-time polynomial(k) setup, not repeated polynomial(k) work
for each of N records.

For a full diagonal, the source extends block prefixes on two alternating
tapes. Prefix counts at least double, so fewer than 2N complex products
are emitted over the entire generation. Each product has O(k)-bit
operands and costs O(k log(2+k)) with the fixed short multiplier. Rewinds
are charged by the scans they repeat. Total time is O(Nk log(2+k));
payload storage uses an absolute number of full streams. The product's
O(k) accumulated phase error is paid by the O(log k) extra guard bits.

## 5. Explicit numerical error transfer and final exact recovery

Call NW for each selected-bit layer with fixed input norm allowance
2^(13k) and error allowance 2^(-50k). Enlarge every numerical format to a
single fixed multiple p=C0 k sufficient for NW, the phase layers, direct
butterflies, products and final scaling. NW's norm/height/operation proof
allows this enlargement and keeps both time and visited-space constants
absolute. Its internal logarithmic amplification is k^o(1), below a
fixed fraction of k above the actual guard.

The source phase layers use coefficient and local rounding error at most
2^(-70k). Their contribution on a boundary norm below 2^(13k) is at most
2^(-70k)(2^(13k)+sqrt(N)), hence below 2^(-50k) for large k. Exact layers
are unitary; O(log k) successive layers preserve the boundary allowance
and give a complete forward/adjoint error below 2^(-40k).

The source asymptotic digit estimate gives ||A||,||B||<=2^(4k). Even the
explicit weaker accepted-shape check b<=4k would give norms below
2^(5k), since h<=N/4. The same recovery allowances still work: transformed
input errors below 2^(-40k) make the rounded coordinatewise product error
below 2^(-30k), using

    ||v pointwise-multiplied by w||_2 <= ||v||_2 ||w||_2.

The product norm is below 2^(12k), so the adjoint uses the same boundary
budget and introduces at most 2^(-40k) more error. Multiplication by
sqrt(S)<=2^(k/2), approximated to 2^(-70k), and the final record rounding
still leave total Euclidean error strictly below one half. Thus every
real convolution coefficient rounds to its exact integer value.

The exact valid-address subspace is invariant under the short transforms.
Approximate leakage outside it is already included in the global Euclidean
error, so no assumption that invalid entries remain exactly zero is needed
for the rounded execution. S>=2h prevents cyclic wraparound of the true
coefficient list.

After inverse CRT, valid addresses appear in mixed-radix rank order.
Each coefficient is less than h 2^(2b). A carry bounded by a constant
times h 2^b is preserved by the ordinary radix-2^b recurrence, hence fits
O(k) bits. Emitting low digits, reversing the stream and trimming or
padding writes exactly 2n bits. These final operations cost O(Nk).

## 6. Constructive precision certification without all-key tables

The source fixed-template `uniformity.tex` describes taking a maximum
over a finite coefficient table. That literal enumeration must not be
restored in the adaptive caller. CW and NW instead give a computable
polynomial(m) rational height bound for every possible spectral key.
Together with actual polynomial-size instruction/row dimensions, it
bounds the logarithm of every one-level norm product by m^K for one
absolute K. The actual adaptive width chain is deterministic and has
polynomial(k) length and generation work.

Use these symbolic majorants, the actual chain and the polynomial node
count to form the source common-ancestor error majorant. Its logarithm
is O(k), with internal extra contribution k^o(1). Computing it requires
polynomial(k) setup and does not enumerate 2^m keys or the exponential
characteristic-two module. A fixed C0 in p=C0 k dominates the majorant
above the explicit guard. Failed guards may use exact schoolbook fallback.
This supplies an actual precision test and generation rule, rather than
declaring an input-dependent coefficient set to be free.

For clarity, a completely integer implementation of the majorant is
available. Let K be an integer simultaneously bounding the finite
instruction count, row dimensions and coefficient numerator/denominator
heights. At level i use 2^(m_i^K) as a coarse bound on a coefficient's
magnitude and include all retained identity registers and copy
multiplicities. Increase K once so 2^(m_i^K) bounds the product of the
level's operator bounds. Store its exponent m_i^K in binary. Sum these
exponents over the actual width chain, double the sum for the
common-ancestor path, and add a polynomial-node-count logarithm and the
fixed boundary exponents 13k,70k and k/2. All these integer exponents
have polynomial(k) description and arithmetic cost. The resulting
power-of-two error majorant is represented by its exponent; its full
exponential bit string is never generated. Test that the extra gain
exponent is at most k/10, or use fallback. NW17 proves eventual success.

## 7. Absolute visited cells and the resulting envelope

A fixed number of full numerical streams suffices for the two forward
outputs, current transform, pointwise product and phase-prefix work.
Controlled-block sorts store at most N records with O(k)-bit keys, and
their interchanges satisfy AI's absolute linear bound. NW has its own
absolute linear bound on all visited cells. All calls use marked regions,
return their heads and reuse the same intervals between phases; the
union of visited regions is bounded, not merely each operation's live
allocation.

Template, short-table, descriptor and arithmetic scratch are a fixed
polynomial in k. Their total is absorbed by Nk beyond a fixed guard;
bounded inputs use a fixed linear-space schoolbook routine. Combining
the constant buffer counts gives one absolute cap Cn on the physical
cells ever visited, with a fixed alphabet and number of tapes. There is
no family of space constants indexed by a target epsilon and hence no
new chunk-compression or universal-search penalty to charge.

The complete source time ledger is

    O(Nk J(k)(1+log(2+k))^4)+poly(k).

Fixed logarithmic powers are absorbed into 2^O(F(log(k+2))). Setting
L(n)=1+log2 n and s(n)=log2 L(n), the accepted shape relations yield

    O(n sqrt(L(n))
         2^[O(s(n)^(2/3)(log2(s(n)+2))^(1/3))]),
    visited cells O(n),

with one fixed machine and absolute constants. This is the precise
source-level integer consequence available for the lead's final
composition review.

After writing the source audit, I read AQ1–AQ9 of
`../lead/adaptive-extraction.md`, with particular attention to AQ5–AQ7.
Those sections match the audited interfaces. AQ5 can take its fixed
outer logarithmic exponent b=4 after increasing the exponential
constant as above. AQ6's on-demand integer majorant is the construction
in section 6, and its fixed precision/error allowances are valid for
the source rounding proof. AQ7's incoming-volume wording and native
recursive radix preserve the child-volume and marked-region estimates.
No correction beyond the already incorporated majorant clarification
was required by this independent read.

## 8. Remaining limits of this audit

No unresolved additional physical or precision interface was found in
the pinned integer caller. Admission still depends on the separately
reviewed AI and NW proofs, the pinned source's analytic/number-theoretic
theorems, and the lead's final consistency check. No complete multiplier
implementation, asymptotic-scale run, Lean build or independent human
referee certification has been performed. The source's numerical prime
cutoff has not been calculated; its deterministic shape tests and fallback
avoid requiring it as an algorithm input.

Prepared for Jerry Chen (@CubeJerry) with substantial AI assistance.
All source and predecessor credits in AI, NW and the pinned papers remain
in force; this audit adds a precise adaptive-interface composition check.
