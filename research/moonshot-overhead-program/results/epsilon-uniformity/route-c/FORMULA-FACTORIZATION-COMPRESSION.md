# Compressing the integral predictor by formula factorizations

Status: **proved local algebra and explicit generator; independently reviewed by Route A and the lead**. The global tape consequence uses the separately reviewed `../route-a/compiler-invoice.md` and rational-address bounds. This is not a practical implementation or an endpoint `O(n sqrt(log n))` algorithm.

The construction uses a standard tensor product of matrix factorizations, applied to a degree-preserving formula for the source's original integral predictor. The tensor product is credited to the matrix-factorization literature. The purpose here is to pay for its use in the pinned integer-multiplication template, including every independent input row, all shifts, coefficient descent, generation, and the resulting tower height.

Concurrent S002 independently admitted the same balanced-formula full-rate construction and global envelope at commit `58c754b583815e4fe40d333ec9d71e4c254749ba`, in `routes/B/formula-full-rate-linearization.md`, `routes/A/formula-extraction-theorem.md` and `routes/C/FORMULA-CYCLOTOMIC-GENERATOR.md`. The separate derivations and their common sources are credited; no priority claim is made.

## 1. Statement and source interface

Let `m>=2`, `0<=u<v<=m`, and `D=v-u`. Put

\[
 b_i=(1-X_i)/2,\qquad
 P_{m,u,v}(X)=(-1)^u\sum_{h=0}^{D}(-2)^h[T^h]
 (1+T)^{-u}\prod_{i=1}^{m}(1+b_iT).                 \tag{F1}
\]

This is the integral binary predictor of `lem:count-predict` in the November Fourier `build/repair.tex` at source commit `3344da59991ed94f9ba711217b29c1d760badfa6`. Its coefficients lie in `Z[1/2]`; the generating-function expression performs no factorial division in the execution ring. On a simultaneous Boolean query eigenvector whose number of negative signs is `c in [u,v]`, it equals `(-1)^c`.

**Theorem F.** Let `b` be the least power of two at least `max(2,D)`. There is one deterministic finite-tape generator which, given `m,u,v`, constructs dyadic square matrices `A_0,...,A_m` of common dimension `k_m` such that

\[
 L(X)=A_0+\sum_{i=1}^{m}A_iX_i,
 \qquad L(X)^b=P_{m,u,v}(X)I_{k_m}.                \tag{F2}
\]

This is a formal polynomial identity. It acts on every input coordinate. For an absolute `C`, all of the following are bounded by

\[
 \mathcal S(m)=2^{\,2^{\,C(\log_2(m+2))^2}}:       \tag{F3}
\]

- `k_m`, total dense output length, actual generation time and visited work cells;
- every coefficient numerator's bit length and every dyadic denominator exponent, not just that exponent's encoded length;
- the same quantities for the direct sum of all `2^m` shifted predictors.

The stage count `b<2 max(2,D)` has the same order as the source's original matrix-root stage count. The replacement improves the row dimension, not the central-window depth. It does not evade `WINDOW-PREDICTOR-DEPTH.md`.

For the source central window, sufficiently large `m` has `D=O(sqrt(m log m))` and `0<=u<v<=m`. The finitely many smaller values can use the original source construction; enlarging the absolute constant in (F3) covers them.

## 2. A formula with controlled syntactic degree

Write `e_a(b)` for the elementary symmetric polynomial. Expanding only the formal variable `T` in (F1) gives

\[
 P=\sum_{a=0}^{D}c_a e_a(b),\qquad
 c_a=(-1)^u\sum_{h=a}^{D}(-2)^h { -u\choose h-a}\in\mathbb Z. \tag{F4}
\]

For `u=0`, use `(1+T)^0=1`. For `u>0`, `binom(-u,t)=(-1)^t binom(u+t-1,t)`. Exact integer arithmetic generates these coefficients, with

\[
 \log_2(1+|c_a|)=O(D\log_2(m+2)).                 \tag{F5}
\]

There is no need to enumerate `binom(m,a)` monomials. Split a variable set `I` into balanced halves and use

\[
 E_{I,a}=\sum_r E_{I_1,r}E_{I_2,a-r}.             \tag{F6}
\]

Include only indices for which both factors exist. Boundary values are `E_(I,0)=1` and `E_({i},1)=b_i`. Omit identity factors and impossible terms. Duplicate every recursively needed subformula: this is a formula, with no free sharing of a circuit computation. Every summand at this node has syntactic degree exactly `a`; scalar multiplication by `c_a` has degree zero.

If `F` counts all leaves and binary operations in the resulting formula, then

\[
 F\le [C_0(D+1)]^{\lceil\log_2m\rceil+2}
   =2^{O(\log(m+2)\log(D+2))}.                   \tag{F7}
\]

At each balanced split there are at most `D+1` products and two recursive calls per product; the depth is at most `ceil(log_2m)`. The outer sum adds one factor `O(D+1)`. Literal formula generation takes time polynomial in `F,m` and (F5). Its maximum syntactic degree is `D`. A small general interpolation circuit without this degree control would not establish the next section's stage count.

## 3. Cyclic factorizations and composition

A cyclic `d`-factorization of a scalar polynomial `f` consists of affine matrix pencils `B_0,...,B_(d-1)` of common rank `a` such that every cyclic product of the `d` matrices equals `f I_a`. Equivalently, put a copy of `R[X]^a` in each grade of `Z/dZ`; the corresponding degree-minus-one operator `delta` satisfies `delta^d=f I` on their direct sum. Throughout, the coefficient ring is commutative and variables are central.

### 3.1 Multiplication and constants

For factorizations of `f,g` of lengths `d_1,d_2` and ranks `a_1,a_2`, concatenate the factors

\[
 B_i\otimes I_{a_2}\quad(0\le i<d_1),\qquad
 I_{a_1}\otimes C_j\quad(0\le j<d_2).            \tag{F8}
\]

The two families commute. In any cyclic rotation of the whole list, their two subsequences are cyclic rotations of their original lists. Regrouping the commuting families gives `fg I`. The new length is `d_1+d_2`, rank is `a_1 a_2`, and entries remain affine.

Multiplication by a scalar constant `c` scales one factor; it adds no stage or row. A scalar summand to be added to a positive length `d` has rank-one factor list `(c,1,...,1)` of length `d`. Two constant expressions are evaluated directly. These conventions avoid extra stages for `e_0=1`, coefficient multiplication, or zero coefficients. Inserting identity matrices into a cyclic factorization preserves every cyclic-product identity.

### 3.2 Addition by a graded tensor product

Pad two factor lists by identities to common length `d=max(d_1,d_2)`. Suppose the coefficient ring contains a primitive `d`-th root `zeta` from the integral cyclotomic ring. Write `U=direct-sum U_i` and `V=direct-sum V_j`, with `rank(U_i)=a_1`, `rank(V_j)=a_2`, and degree-minus-one operators `delta_U^d=f I`, `delta_V^d=g I`. Set

\[
 \Delta(x\otimes y)=\delta_U(x)\otimes y
                  +\zeta^i x\otimes\delta_V(y),
 \qquad x\in U_i.                               \tag{F9}
\]

Let `Z` multiply grade `U_i` by `zeta^i`. Then `Z delta_U=zeta^(-1) delta_U Z`, so the two summands `delta_U tensor I` and `Z tensor delta_V` commute up to `zeta^(-1)`. The Gaussian-binomial identity gives

\[
 \Delta^d=\delta_U^d\otimes I+Z^d\otimes\delta_V^d
          =(f+g)I.                              \tag{F10}
\]

There is no division by `d`, `1-zeta^r`, or any intermediate Gaussian-binomial denominator. Prove the vanishing of the mixed coefficients first in `Z[zeta]` embedded in `C`: the relevant Gaussian-binomial polynomials vanish at a primitive root. Since their coefficients are integral, this is an identity over the integral cyclotomic ring and survives every base change. The case `d=1` is ordinary addition.

The operator lowers total grade `i+j` by one. Every total-grade summand has rank `d a_1 a_2`. Its `d` transition blocks therefore form a cyclic `d`-factorization of `f+g`; every transition block is affine. The entire grade consists of independent input coordinates. No coordinates must start at zero.

This tensor construction is standard. See Richie Sheng and Tim Tribone, *Tensor products of d-fold matrix factorizations*, Definition 3.1 and Proposition 3.2, Nagoya Mathematical Journal 261 (2026), e2, DOI <https://doi.org/10.1017/nmj.2025.12>. Their base-ring hypothesis is a commutative `Z[zeta_d]`-algebra; no unramified-field assumption is imposed. An earlier source-relevant construction is Markus Blaser, David Eisenbud and Frank-Olaf Schreyer, *Ulrich complexity*, Differential Geometry and its Applications 55 (2017), 128--145, Theorem 2.1 and Proposition 2.2, DOI <https://doi.org/10.1016/j.difgeo.2017.06.001>.

### 3.3 Ring choice and the dimension bound

Perform all formula operations in the common ring

\[
 R_0=\mathbb Z[1/2,\zeta_M],\qquad
 M=\operatorname{lcm}(1,2,\ldots,D).              \tag{F11}
\]

Every required root is `zeta_d=zeta_M^(M/d)`. Every factor length is the corresponding syntactic degree, hence at most `D`. Addition pads only to a maximum; multiplication adds lengths. Thus induction on the formula produces a cyclic **D**-factorization of `P` without repeated power-of-two roundings.

Leaves have rank one. Multiplication multiplies ranks; addition multiplies the two ranks and a number at most `D`. If `s` is the number of addition nodes, the resulting rank `K` obeys

\[
 K\le\max(2,D)^s\le\max(2,D)^F,
 \qquad \log_2K\le F\log_2\max(2,D).             \tag{F12}
\]

This explicitly counts duplicated subformulas. The root order obeys `M<=D!<=2^(O(m log(m+2)))`. No assumption that an odd prime is coprime to `M` is required; descent in the next section happens in characteristic zero before any reduction modulo that prime.

## 4. One repeated pencil and descent to dyadic coefficients

Pad the final `D` factors by identities to length `b`, the least power of two at least `max(2,D)`. Form the block-cyclic matrix which sends grade `i` to grade `i-1` using the `i`-th factor. It has dimension `bK`, is affine in the query variables, and satisfies

\[
 L_0(X)^b=P(X)I_{bK}.                            \tag{F13}
\]

All cyclic products were established in Section 3, so every grade satisfies this identity. Merely establishing the product from one preferred grade would not have been enough. The construction requires no `b`-th root of the scalar coefficients and no additional root of unity.

The ring `R_0` is finite free over `Z[1/2]` with power basis of length `t=phi(M)`. Replace each coefficient by its `t`-by-`t` regular multiplication matrix. This is an injective ring homomorphism. Since `P` already has coefficients in `Z[1/2]`, (F13) becomes

\[
 L(X)^b=P(X)I_{bKt},\qquad k_m=bK\varphi(M).       \tag{F14}
\]

Every basis coordinate is independent input data. The identity acts as the same scalar polynomial on every one of them; this descent is not an initialization of extra work registers.

In particular `L` now has dyadic coefficients. It may be reduced modulo any odd prime `p` directly over `F_p`, even when `p` divides `M` or an internal factor length. One could alternatively base-change through the possibly nonreduced algebra `F_p[z]/Phi_M(z)`, but no such interpretation is needed for the final template. Only powers of two are inverted.

This does not contradict the count-modulo-`p` obstruction. The construction retains the elementary symmetric query functions, whose Boolean values are integer binomial coefficients reduced modulo `p`. For example `e_p` distinguishes counts zero and `p`. Such functions are not ordinary polynomials in the reduced scalar count alone, and the construction never obtains them by dividing by `p!` in `F_p`.

## 5. Explicit bit generation and coefficient heights

The following elementary algorithm provides actual finite-tape bounds, not an arithmetic-operation oracle.

First generate (F4)--(F7), with all duplicated formula nodes explicit. During factor composition represent an element of `Z[zeta_M]` redundantly by an `M`-slot integer coefficient array for powers `1,z,...,z^(M-1)`, using `z^M=1` to shift root phases. This representation need not be unique in the cyclotomic ring; evaluating the array at `zeta_M` gives its intended value.

Each matrix-entry operation in Sections 3--4 is a copy, zero insertion, multiplication by a root monomial, scalar multiplication by one of the integer coefficients, or addition. Tensor products there always have an identity or a scalar root in the other factor: they do not multiply two arbitrary affine entries. Each coefficient is therefore a sum of terms whose scalar multiplications lie on formula paths. A crude bound on its numerator bit length is `O(F(1+B_0)+log M)`, where `B_0=O(D log(m+2))` from (F5). For this particular formula the only variable leaves are `(1-X_i)/2`, and all subsequent scalar operations are integral, so every matrix entry has denominator dividing `2`. The weaker bound of `O(F)` on the denominator exponent would also suffice.

All intermediate ranks are at most `K`; there are at most `F` nodes and at most `D` factors per node. Thus even storing every intermediate matrix densely, with an affine coefficient list and an `M`-slot array per entry, costs a fixed polynomial in

\[
 m,F,D,K,M,B_0.                                  \tag{F15}
\]

The operations on those arrays have bit cost polynomial in the same quantities. This deliberately wasteful algorithm is a fixed finite-tape algorithm: fixed nested loops, dense scans, schoolbook integer arithmetic and rewinds suffice. A fixed polynomial overhead for implementing arrays by tapes does not change the bound.

To perform regular-representation descent, generate the monic cyclotomic polynomial `Phi_M` and its companion matrix. An elementary polynomial-time-in-`M` algorithm generates `Phi_r` for `1<=r<=M` recursively from
`z^r-1=product_(d|r) Phi_d(z)`, using exact dense integer polynomial arithmetic and trial division for divisibility tests. Every cyclotomic coefficient has at most `O(M)` bits: its roots have absolute value one, and each coefficient is bounded by the corresponding binomial coefficient. Products arising in this generation have degree at most `M` and roots of absolute value one; long-division intermediates have polynomially bounded bit lengths as well.

The companion matrix has dimension at most `M` and entries of `O(M)` bits. Its powers through exponent `M-1` therefore have `O(M^2+M log(M+1))` coefficient bits by the elementary matrix-norm bound. Generate all those powers by literal multiplication. Replacing each redundant root coefficient array by the corresponding linear combination of these matrices adds at most `O(M^2+log M)` bits to the preceding bound. This produces all dyadic coefficient matrices in time and space polynomial in (F15).

By (F7), (F12), `D<=m` and `M<=D!`, every quantity in (F15) and every fixed polynomial of them is at most (F3), after enlarging its absolute constant. This proves the stated dense output, height, denominator, work and space bounds. The space assertion here concerns finite template generation, not yet linear space in the multiplication input length.

## 6. All shifts and full input occupancy

For `beta in {0,1}^m`, the source shifted predictor is

\[
 P_\beta(X)=(-1)^{|\beta|}
 P((-1)^{\beta_1}X_1,\ldots,(-1)^{\beta_m}X_m).   \tag{F16}
\]

Use the same factor-list skeleton for every shift. Substitute the query signs in every affine factor, and multiply one factor by `(-1)^|beta|`. Every cyclic product gains that sign exactly once. The cyclic block matrix and its regular-representation expansion therefore have the same dimension `k_m` for all shifts and their `b`-th powers are `P_beta I`.

Taking their direct sum gives raw batch dimension `R=2^m k_m`, within (F3), with each shift present exactly `k_m` times. Thus the source's exceptional-shift fraction is unchanged. The repeated pencil acts on all `R` independent streams. The construction requires neither zero-filled auxiliary streams nor a data-dependent encoding of the input into a special subspace.

For any commuting involutory query operators, scalar row matrices commute with those queries. Substitution into the formal identity is therefore valid. This supplies exactly the full-batch matrix-root interface of `lem:matrix-root` and `cor:swap-repair`; the same `b` source pencil stages may be used in each invocation of the predictor.

## 7. Complete physical consequence and limits

The downstream proof is `../route-a/formula-template-transfer.md`, independently checked in `FORMULA-TRANSFER-REVIEW.md`. It pays for Hermite repair over a power-of-two cyclotomic extension, all dense tables, both odd-characteristic interchange and characteristic-zero Fourier, numerical norms, refined rational address geometry, compatible radix search, finite tape compilation, all-length space fences, chunking, and the specified weighted schedule.

Write `E_1(t)=2^t`, `E_2(t)=2^(2^t)` and `Z_j=(j+2)^3 log_2(j+3)`. The chosen interchange arity has `log m=O(Z_j)`, and the Fourier arity is smaller. Theorem F therefore reduces the complete finite-template budget to

\[
 S_j\le E_2(CZ_j^2),
 \quad d_j=\log_2 D_j\le E_1(CZ_j^2),
 \quad b_j=\log_2(1+\log_2N_j)\le E_1(CZ_j^2).    \tag{F17}
\]

Here `D_j` includes the scheduled attempt's slowdown and `N_j` is its actual sufficient threshold. These are the complete physical profiles, not only local query-call counts. The `O(n)` visited-cell constant is common to the selected attempts after the reviewed chunking wrapper.

Put `L=1+log_2 n`, `x=log_2 L`, `z=log_2(x+16)` and `w=log_2(z+2)`. With a sufficiently small absolute `c>0`, choose for analysis
`j=floor(c(z/w^2)^(1/6))`. Eventually `CZ_j^2<=z/2`, so both profile terms in (F17) are at most `2 sqrt x`. The actual weighted schedule is consequently certified by

\[
 T(n)\le n\sqrt L\,
 2^{\,O\!\left(x\frac{(\log_2(z+2))^{1/3}}{z^{1/6}}\right)}.
                                                               \tag{F18}
\]

The machine has fixed finite tape count and alphabet and returns exact full products with a common `O(n)` visited-work-cell bound. The input-dependent choice of `j` above is a proof of the scheduled envelope, not an unpriced selection oracle. Written mathematical review is required for this conclusion; finite examples below do not prove the asymptotic theorem.

The proved row bound is `exp(exp(O(log^2 m)))=exp(m^(O(log m)))`. It does **not** meet the stronger `exp(m^C)` target with fixed `C` in `../route-a/single-exponential-root-hypothesis.md`; that sharper profile remains conditional. No bounded residual factor or endpoint algorithm follows from (F18).

Concurrent S002's formal Chow barrier at commit `4689161c5bc6c9e64536034d4fa6af033d26a3e0` concerns a flat sum of bounded-degree affine products followed by one tensor factor per product. The present construction uses nested degree-preserving sums and products, composing factorizations at each node. It does not assert a smaller flat product decomposition and therefore is not excluded by that specified barrier. Likewise it retains the source's `Theta(sqrt(m log m))` predictor/repair resource scale; it changes its finite row cost, not the depth lower bound.

Credits: @CubeJerry; the pinned OpenAI sources; the cited matrix-factorization constructions; concurrent S002's label and rational-address bounds; Route A's finite-template and tape transfer; Route B's common-space wrapper and independent algebra audit; the lead's independent review. Developed with GPT-6 Astra Pro assistance. No literature-priority claim is made.

## Finite verification and review receipt

`python3 -I -B check_formula_factorization.py` passes with the adjacent JSON receipt. It checks 84 predictor instances, all 152 cyclic products in their factor lists, and 72 full-coordinate regular matrix-root identities over the integers, `F_3` and `F_5`; the largest descended matrix has dimension 96. Cases include unequal-degree sum padding, constants, length-three addition, final length-three-to-four padding, and every shifted sign pattern in the selected non-Boolean examples. A wrong-phase negative control fails as intended. At characteristic three the test explicitly verifies a nontrivial unipotent order-three phase in the nonreduced cyclotomic algebra. The full matrix identity, including every off-diagonal entry, is tested. These finite examples do not certify the asymptotic generator or tape bound.

The lead independently read Sections 1--6 on 2026-11-25 and reported no blocker after checking cyclic products, mixed-order roots, constants and degree one, syntactic degree, final padding, regular representation, coefficient/generator bounds and full input occupancy. Written reviews are `../route-a/FORMULA-FACTORIZATION-REVIEW.md` and `../ROOT-FORMULA-REVIEW.md`; the lead's isolated checker replay is `../root-formula-replay.json`. Route B's further review is maintained separately. The downstream Route A transfer and stronger conditional MR transfer were reviewed in `FORMULA-TRANSFER-REVIEW.md`.
