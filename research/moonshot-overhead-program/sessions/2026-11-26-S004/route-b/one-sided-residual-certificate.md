# A sound budgeted repair certificate for one-sided ordinary residuals

Status: **proved component refinement, pending independent audit**. This
note strengthens the acceptance test of
`deterministic-sparse-residual-repair.md` when the candidate is known to be
a coefficientwise lower bound. Sound acceptance then requires no sparsity
promise. Fast completion still requires a small residual support, and no
fast supplier of such a lower candidate is provided.

The derivative-ratio interpolation mechanism is established prior art;
see the source discussion in the preceding note, including Giorgi,
Grenet, Perret du Cray, and Roche, *Fast interpolation and multiplication
of unbalanced polynomials* (2024), Sections 2.2--2.4 and 3,
<https://www-verimag.imag.fr/~grenetb/publis/GGPR24.pdf>. The additional
certificate below is the elementary nonnegative weighted-variance
identity, with its full integer and tape costs charged.

## 1. Assumption and theorem

Use the preceding note's input convention: `A,B` have degree below `h`
and nonnegative `b`-bit coefficients, `D=2h`, `C` has degree below `D`
and integer coefficients of absolute value at most `Cmax`, and

\[
 E=AB-C,\qquad Emax=h2^{2b}+Cmax.
\]

The additional structural assumption is

\[
                    E_i=(AB)_i-C_i\ge0\quad(0\le i<D).       \tag{P1}
\]

Nonnegativity of `C` by itself is insufficient. The algorithm does not
infer (P1) from the candidate's appearance. It must follow from the
candidate's construction or a separate proof. Negative coefficients of
`C` are allowed if (P1) still holds.

Choose a **budget** `S`, `1<=S<=D`, with no assertion that the true
support is at most `S`. Define

\[
 q=\lceil\log_2 D\rceil,\quad
 B_*={S\choose2}q,\quad K=2B_*+4,
\]

and choose the least `beta` such that

\[
 R=2^\beta>8D^3(Emax+1).
\]

Let `M_ell=R^ell-1`, `M=prod_(ell=1)^K M_ell`,
`k=beta K(K+1)/2`, and `V=D beta`.

**Theorem P1.** Fix `alpha>1/2` and a fixed exact multitape short
multiplier of time `O_alpha(u(1+log_2 u)^alpha)` and visited space
`O(u)`. There is a deterministic fixed finite-alphabet multitape
algorithm with the following properties.

1. Under assumption (P1), every accepted reconstruction equals `E`,
   regardless of its true sparsity.
2. If `E` has at most `S` nonzero terms, the algorithm reconstructs it
   and outputs the exact product in

   \[
       O_\alpha\bigl(V(1+\log_2(k+1))^\alpha+k^6\bigr)         \tag{P2}
   \]

   steps, with one `O(V)` bound on cells ever visited.
3. Without a support promise, the same budgeted procedure either returns
   a certified exact result or reports that this budget did not recover
   the entire residual. A full packed multiplication may then supply a
   deterministic exact fallback, still using `O(V)` visited cells.

The uniform constants do not depend on `h,b,Cmax,S`. The machine uses a
fixed alphabet, fixed tape count, and fixed program. This is a verified
repair interface, not an improved complete worst-case multiplication
bound.

## 2. Three exact fold families

Write `Theta=X d/dX`. Compute the values modulo `M` of

\[
\begin{aligned}
 E&=AB-C,\\
 \Theta E&=(\Theta A)B+A(\Theta B)-\Theta C,\\
 \Theta^2 E&=(\Theta^2 A)B+2(\Theta A)(\Theta B)
                    +A(\Theta^2 B)-\Theta^2 C.                \tag{P3}
\end{aligned}
\]

Each is evaluated at `R`. For each `ell<=K`, reduce these three integer
residues modulo `M_ell` and decode their cyclic folds. In a residue bin
`j mod ell`, the decoded values are exactly

\[
 u=\sum_{i\equiv j\pmod\ell} E_i,\quad
 v=\sum_{i\equiv j\pmod\ell} iE_i,\quad
 w=\sum_{i\equiv j\pmod\ell} i^2E_i.                         \tag{P4}
\]

This remains true if the true support exceeds `S`. Indeed, without any
sparsity assumption, a bin has at most `D` terms and

\[
     0\le u\le DEmax,\quad
     0\le v\le D^2Emax,\quad
     0\le w\le D^3Emax<R/8.                                 \tag{P5}
\]

The packed fold has absolute value below `M_ell/2`, and each coefficient
has absolute value below `R/8`. Centering the residue and repeated
balanced radix decoding therefore recovers the exact fold coefficients,
by the same argument as the preceding note. The moduli need not be
coprime; only `M_ell|M` is used.

The larger radix in this note is essential: a radix justified only by the
chosen sparse budget would not certify folds when the actual support was
larger than that budget.

## 3. The variance certificate for an isolated term

For every bin, direct expansion gives the integer identity

\[
 u w-v^2
     =\sum_{\substack{i<t\\i,t\equiv j\pmod\ell}}
                    E_iE_t(i-t)^2.                           \tag{P6}
\]

Every summand is nonnegative. Consequently:

- `u=0` means the bin has no positive error coefficient.
- If `u>0`, then `u w-v^2=0` if and only if exactly one error
  coefficient in the bin is positive.
- In the latter case that true term has exponent `e=v/u` and coefficient
  `u`. Its exponent is an integer in `[0,D)` and has residue `j mod ell`.

The algorithm records a term only from a positive bin with zero variance.
It additionally checks the exact division, exponent range, residue, and
coefficient-height bound. Those checks are redundant under (P1), but
make the represented record unambiguous. Every recorded term is thus a
true term of `E`, even if other bins contain arbitrarily many collisions.

Terms recorded from different moduli are deduplicated by exponent.
Under (P1), repeated occurrences necessarily have the same coefficient.
They are counted once, rather than being used to inflate a mass total.

## 4. Exact mass certifies that no term is missing

Compute the total residual mass directly:

\[
     T=E(1)=A(1)B(1)-C(1).                                   \tag{P7}
\]

Let `Rrec` denote the polynomial formed from the distinct certified
terms. The algorithm accepts precisely when

\[
                     Rrec(1)=T.                              \tag{P8}
\]

Because every recovered term is a true term with its exact positive
coefficient, `E-Rrec` is coefficientwise nonnegative. Equality (P8)
forces every coefficient of that difference to be zero. This proves
sound acceptance without any sparsity promise.

If the mass is smaller, at least one positive residual term is missing.
The procedure may report that the budget is incomplete and use the
exact fallback. A mass larger than `T`, inconsistent repeated terms, or
negative decoded values would contradict (P1) or exact arithmetic; such
states are rejected rather than silently accepted.

To prove completion when `|supp E|<=S`, apply the preceding note's
collision-free-family proof with `S` in place of `2s`. Some `ell<=K`
separates every true error exponent. Every nonempty bin for that modulus
has zero variance and yields its exact term. All terms are recovered,
so (P8) holds. Alternatively, if every nonempty bin of any single modulus
has zero variance, that modulus alone already recovers the entire
residual. The union-and-mass version also uses partial isolation from
different moduli.

## 5. Physical cost and the large-budget branch

The short-modulus reciprocal reduction and signed-stream methods in the
preceding note apply unchanged to (P3). There are a fixed number of
products and a fixed number of long scans. Forming `i^2 a_i`, `i^2 b_i`,
and `i^2 c_i` requires actual short integer multiplications; they are
charged at `O_alpha(V(1+log_2 beta)^alpha)`, which is covered by (P2).
All weighted coefficients fit in `O(beta)` bits. The factor two in (P3)
is a shift plus a possible carry.

The exact sums in (P7) have `O(beta)` bits and require linear scans;
their single product is another charged short multiplication. Decoding,
integer variance comparisons, exact division, sorting and deduplicating
records, and adding their masses fit inside the same coarse `O(k^6)`
setup/enumeration allowance. There are at most `K(K+1)/2` candidate bins,
and each recorded term takes `O(beta)` bits, so all records occupy
`O(k)` cells even when the actual residual is dense. Reusing work tapes
therefore gives `O(V)` visited cells whenever `k<=V`.

If `k>V`, skip the budgeted folds and use direct packed schoolbook
multiplication, costing `O(V^2)<O(k^6)` with `O(V)` visited cells. This
preserves (P2) even for an excessive budget. If `k<=V` but the mass test
fails, the same schoolbook fallback, or the fixed full-length multiplier,
is exact. The latter has time `O_alpha(V(1+log_2 V)^alpha)` in addition
to the attempted budgeted work. Neither fallback improves the existing
worst-case exponent.

Finally, merge the recovered ordinary error coefficients into `C`, then
propagate carries. All these scans have `O(V)` bit volume. Since

\[
 \beta=O(b+\log(D+1)+\log(Cmax+2)),\qquad
 k=O(\beta S^4\log^2(D+1)),
\]

the same below-`n sqrt(log n)` repair regimes as the preceding note hold
when `b` and candidate coefficient heights are `O(log n)` and
`S<=2^((log n)^tau)` for fixed `tau<1`.

## 6. Necessary scope and explicit false-certificate controls

The second derivative matters. For `E=1+X^2` in the sole bin modulo one,
the value and first derivative are `(u,v)=(2,2)`. Their ratio would
incorrectly suggest the term `2X`, whose total mass also equals `E(1)`.
The second derivative is `w=4`, giving `uw-v^2=4>0`, so the variance
test correctly refuses that false isolated term.

Positivity matters too. For the signed residual `E=(X-1)^3`, the total
mass and its first two Euler moments at one are all zero, although the
residual is nonzero. Thus moments and total mass alone cannot supply a
general signed-residual certificate. More generally, a dense signed
residual divisible by a sufficiently high power of every fold polynomial
can defeat any fixed finite derivative family. This note claims sound
acceptance only under (P1).

A structurally nonnegative residual can arise by omitting nonnegative
summands from ordinary convolution. Such an obvious fixed bilinear
construction does not itself yield the desired fast sparse supplier:
the input with every digit positive exposes every output with an omitted
summand. Other candidate constructions require their own cost, accuracy,
and one-sidedness proofs. This certificate leaves those tasks open.

Prepared for @CubeJerry with substantial ChatGPT assistance.
