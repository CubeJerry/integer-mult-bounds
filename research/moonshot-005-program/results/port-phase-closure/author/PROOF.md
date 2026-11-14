# A uniform period48 for the native port coupling, and the exact old-normalizer gate

**Proved in the explicitly defined normalized character model. No new κ.**
This package extends the root's one-class phase discovery to all fourteen
native classes and every number of character columns. It proves a fixed
period by a two-qubit algebraic argument, independently enumerates the exact
2048-element phase family, and locates the failure of the retained ordinary
normalizer. It does not identify different physical stages with one common
operator or supply a profitable caller.

Credit: the root identified the normalized character family, ran the first
exact one-class spectrum/closure screen, and derived the corrected
old-normalizer criterion. Worker C established the all-class native
conjugacies, quadratic phase reduction, two-qubit period proof and bounded
denominator proof, and independently reconstructed the finite spectrum using
Gaussian integers without the root's NumPy implementation. Worker B supplied
the actual112-port source. Native root geometry and earlier source packages
retain their credit. All work is under @CubeJerry's direction with OpenAI
assistance.

## 1. Exact model and main theorem

Let P be the112 native normals consisting of all weight-three or weight-seven
vectors in F2^9 except

`[7,25,42,52,76,82,97,127]`.

Use the authentic port labels in the pinned R0-minimal word
`c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336`.
For the real roots ρ(v), the fourteen eight-port classes and the class-block
Gram matrix B, use the exact definitions in the independently reviewed
full112 source. Put R=I−B. This R is symmetric and satisfies R²=I.

For every integer m≥0 and every list of actual binary character columns
z₁,…,z_m∈F2^9, define

\[
p_h=\sum_{\ell=1}^{m}(v_h\cdot z_\ell\bmod2)\pmod4,
\qquad Q_p=\operatorname{diag}(i^{p_h}),\qquad A_p=Q_pR.
\]

**Theorem1.** For every such m and list of columns,

\[
A_p^{48}=I_{112}.
\]

In every nonzero eight-port block, every power of A_p has entries in
`(1/2) Z[i]`. The same statements hold with RQ_p in place of Q_pR, since
these two products are similar. The least positive exponent that works
uniformly for this whole family is48. The exact possible block orders are
2,4,6,8,12,16,24; some individual blocks have order16 and others have order24.
No block of order48 is needed for the least-common-period statement.

The quantifier is over all finite widths, not a finite experimental range.
It is essential that the port phases come from the displayed native
characters. Arbitrary independent phases on the eight ports need not have
period48.

## 2. All native classes have the same signed Fourier representation

For each class, its parity halves T,S are affine planes u+W and v+W,
where W is a common two-dimensional binary radical. The spans of T and S
have dimension three, and their sum has dimension four. Choose a basis a,b
of W and index the class in the order

\[
u+x_1a+x_2b\quad\hbox{and}\quad v+x_1a+x_2b,
\qquad(x_1,x_2)\in\mathbb F_2^2.
\]

The exact native cross-Gram matrix K has entries±1/2. There are recorded
diagonal signs D_T,D_S such that

\[
D_TKD_S=H,\qquad
H_{x,y}=\tfrac12(-1)^{x_1y_2+x_2y_1}.
\]

Consequently the signed permutation of port coordinates conjugates the
class restriction of R to

\[
R_*=-\begin{pmatrix}0&H\\H&0\end{pmatrix}.
\]

The signs commute with every diagonal phase. Thus they change no phase
family or order calculation after the native port permutation. All fourteen
conjugacies, their actual native labels and their explicit signs are
reconstructed from integer roots in `check.py`, rather than inferred from
one class. The exact witnesses appear in `RESULT.json:class_conjugacies`.
This finite native premise was independently established in the full112
source review's `FOURIER-STRUCTURE.md`.

Introduce x₃=0 on the u half and x₃=1 on the v half. The eight native labels
are the affine three-flat

\[
u+x_1a+x_2b+x_3(u+v).
\]

Since u,a,b,u+v are independent, restricting the512 genuine linear
characters of F2^9 to this flat gives exactly the sixteen affine Boolean
functions on F2^3. Surjectivity follows by prescribing a linear functional
on these four independent vectors and extending it to F2^9. The checker
also enumerates the512 restrictions at every native class, and records a
native column giving the repeated-character counterexample below.

## 3. The exact all-width phase group

The additive Z4 span of the sixteen affine Boolean functions is exactly

\[
\mathcal Q=\left\{c+\sum_{j=1}^{3}a_jx_j
  +2\sum_{1\leq j<k\leq3}b_{jk}x_jx_k\pmod4:
  c,a_j\in\mathbb Z/4,\ b_{jk}\in\mathbb F_2\right\}.
\]

To prove containment, expand an XOR as an integer polynomial modulo4.
Linear terms have coefficient1, pair terms coefficient−2, and all terms of
degree≥3 vanish modulo4. Complementing a Boolean function subtracts it from1.
Conversely, constants and coordinates are generators, and

\[
2x_jx_k=x_j+x_k-(x_j\mathbin{\mathrm{xor}}x_k)\pmod4.
\]

Negating a generator is the same as adding it three times. Hence every
quadratic expression above is realized by a nonnegative number of genuine
columns. Its coefficients are unique: evaluate first at0, then at the three
singletons, then at the three pairs. Thus there are
`4^4 2^3=2048` phases. This algebraic reduction proves that every width enters
this fixed finite family. Exhaustively examining a bounded width is not the
reason for the all-width assertion.

An independent breadth-first traversal proves the useful supplementary
finite fact that every phase has a representation with at most five genuine
columns. Padding with the zero character realizes it at every larger width.
The root's independently written closure calculation gives the same census.

## 4. A structural proof of period48

Write an allowed q∈Q on the two halves as q₀(x₁,x₂), q₁(x₁,x₂). Its form gives

\[
q_1-q_0=c'+2e_1x_1+2e_2x_2\pmod4.
\]

Let D₀,D₁ be the corresponding four-by-four diagonal phase matrices, and
let `Z^e=diag((-1)^(e₁x₁+e₂x₂))`. Then D₁=i^{c'}Z^eD₀. Put U=D₀H.
Apart from its harmless global minus sign, the eight-port operator is

\[
A=\begin{pmatrix}0&U\\i^{c'}Z^eU&0\end{pmatrix}.
\]

Therefore A² has diagonal blocks
`U T U^{-1}` and `T`, where

\[
T=i^{c'}Z^e U^2.
\]

We next show T^{24}=I. This uses four-dimensional matrices only, independent
of the original number of character columns.

### 4.1 Binary Pauli action

On functions on F2², let X_j translate coordinate j and Z_j multiply by
`(-1)^x_j`. A Pauli matrix is a phase times a product of these four matrices.
Both D₀ and H conjugate Pauli matrices to Pauli matrices. For D₀ this follows
by taking the first difference of its quadratic phase; for H,
`H X₁ H=Z₂`, `H X₂ H=Z₁`, and conversely. Such a unitary is called Clifford
here only as shorthand for this stated conjugation property.

Record a Pauli by its binary translation/sign pair `(x₁,x₂,z₁,z₂)`, ignoring
its scalar phase. If the two linear coefficients of q₀ have parities a,b
and its cross term is2c x₁x₂, the binary action of U is

\[
S=\begin{pmatrix}I&0\\C&I\end{pmatrix}H_{\rm bin},\qquad
C=\begin{pmatrix}a&c\\c&b\end{pmatrix},
\]

where H_bin exchanges x₁ with z₂ and x₂ with z₁. Direct multiplication gives
the complete eight-case table:

| a | b | c | Order of S | Order d of S² |
|---:|---:|---:|---:|---:|
|0|0|0|2|1|
|0|0|1|3|3|
|0|1|0|4|2|
|0|1|1|6|3|
|1|0|0|4|2|
|1|0|1|6|3|
|1|1|0|6|3|
|1|1|1|4|2|

The matrices and their powers are included in the independently reconstructed
proof table. Multiplying by Z^e or a scalar does not change the binary Pauli
action. Thus the action of T has order d∈{1,2,3}, and T^d acts trivially on
binary Pauli labels.

### 4.2 Lifting the binary action

A unitary acting trivially on binary Pauli labels is a scalar times a Pauli.
Indeed, its conjugation on each Hermitian X_j,Z_j is a sign. Choose a Pauli
with the same four signs; after dividing by it, the unitary commutes with
every X_j,Z_j. Commutation with all Z's makes it diagonal, and commutation
with all translations makes that diagonal constant.

Every entry of T^d belongs to Z[i,1/2]. Its scalar factor ζ therefore belongs
to this ring and has absolute value1. Such a Gaussian dyadic scalar is one
of±1,±i: in a reduced expression `(r+is)/2^k`, the equation
`r²+s²=2^(2k)` is impossible modulo4 for k>0 if r,s are not both even.
Thus `(T^d)^4=I`. Since d is1,2 or3, `T^{24}=I`, and the displayed two-block
square gives `A^{48}=I`.

This proves Theorem1's uniform period without relying on the2048-case
spectrum as a substitute for the all-width argument.

## 5. The denominator bound and sharp common period

Every even power of A is block diagonal with two-qubit Clifford blocks;
every odd power is block antidiagonal with such blocks. Every block entry is
Gaussian dyadic, since D₀,D₁ and H have that property.

**Lemma.** Every four-dimensional Gaussian dyadic Clifford unitary has all
entries in `(1/2)Z[i]`.

**Proof.** Each column is a simultaneous eigenvector of two independent
commuting Pauli operators, obtained by transporting the two computational
Z eigenvalue equations. Let the binary translation projection of this
stabilizer have rank r∈{0,1,2}. Its pure-Z subgroup has rank2−r and cuts out
an affine support set of size2^r. Its translation subgroup acts transitively
on that set, and the Pauli equations make all nonzero coefficient magnitudes
equal. Normalization makes their squared magnitude2^{-r}.

If a nonzero entry is `(a+ib)/2^k` in reduced form, then
`a²+b²=2^(2k−r)`. The same modulo4 argument shows that its reduced denominator
is at most2 for r=0,1,2. More explicitly, magnitudes1,1/√2,1/2 give entries
among Gaussian units, `(±1±i)/2`, and half Gaussian units, respectively.
Therefore every entry belongs to `(1/2)Z[i]`. ∎

Applying this lemma to every nonzero block proves the claimed bound for
every power. It is a pointwise normalized-character statement. It does not
bound the complexity of implementing a character-dependent block function
in the physical source representation, or the costs of its frame adapters.

The exact independent finite spectrum has the following counts:

| Exact order | Number of phases |
|---:|---:|
|2|4|
|4|220|
|6|256|
|8|416|
|12|256|
|16|384|
|24|512|

The complete2048-phase calculation uses only Gaussian integers and powers
of two, reducing every exact denominator along the way. It finds an
identity for each phase at its first reported positive power, not merely
at a common candidate exponent. Explicit order16 and order24 witnesses are
stored with their quadratic coefficients and minimum character widths.
They prove that any uniform exponent must be a multiple of
`lcm(16,24)=48`. Combined with Section4 this proves sharpness of the common
period. The maximum observed reduced matrix denominator is2, independently
checking the proved denominator lemma on the entire phase family.

## 6. Corrected retained-normalizer obstruction

This result concerns the stated old normalization, not every possible new
normalizer. Define

\[
\Lambda=\operatorname{diag}\bigl(1\text{ if }p_h\text{ is even};
\ i\text{ if }p_h\text{ is odd}\bigr),\qquad
J=\Lambda Q_p^{-1}
 =\operatorname{diag}\bigl((-1)^{\lfloor p_h/2\rfloor}\bigr).
\]

**Theorem2.** Within each native eight-port class,

\[
\bigl(\Lambda(Q_pR)^{-1}\bigr)^2=I
\quad\Longleftrightarrow\quad
J\text{ is constant on that class}.
\]

**Proof.** Conjugating by Λ gives

\[
\Lambda^{-1}\bigl(\Lambda(Q_pR)^{-1}\bigr)\Lambda
 =RQ_p^{-1}\Lambda=RJ.
\]

Both R and J are involutions. Hence `(RJ)^2=I` is equivalent to RJ=JR.
Entrywise, a diagonal J commutes with R precisely when its two signs agree
on every nonzero R edge. The graph of the class has all sixteen cross-half
edges and is connected, so all eight signs must agree. The converse is
immediate. ∎

Every single-column phase has entries0 or1, so J=I and the old-normalizer
test **passes at width one**, including single-column phases for which
`(Q_pR)^4≠I`. Thus a fourth-power counterexample alone is not a valid proof
that the normalized involution condition fails.

At width two, repeat a genuine nonconstant character. Then p=2χ and
J=diag((-1)^χ) is nonconstant. The normalized square fails. The checker
records one actual native column producing this character in each of the
fourteen classes. It independently verifies the criterion on all2048 phase
patterns:32 pass and2016 fail. These are finite counts accompanying the
general commutator argument, not its proof.

The obstruction does not exclude a changed paid normalizer, a different
operator target, or a caller using other identities. The root/Worker A
physical two-normalizer construction is a separate line of work and is not
silently admitted by this theorem.

## 7. Scope controls and reproduction

The exact phase `q=x₁x₂` with odd quadratic coefficient1 is outside the
character closure. Its eight-vector is `(0,0,0,1,0,0,0,1)` in the canonical
order. The checker computes a nonzero entry of `A^{48}−I` for this phase.
This is a meaningful boundary control: extending the theorem to arbitrary
independent port phases would be false. No infinite-order claim is needed.

The sixteen genuine one-column phases all pass Theorem2, while the stated
repeated-character width-two case fails. The finite spectrum also stores a
genuine one-column fourth-power counterexample, preserving the distinction
between the two normalization questions.

Reproduce from the session workspace:

```sh
python3 worker-c/port-phase-closure/author/check.py
python3 -O worker-c/port-phase-closure/author/check.py --output /tmp/port-phase-optimized.json
cmp worker-c/port-phase-closure/author/RESULT.json /tmp/port-phase-optimized.json
```

The checker uses only standard Python and exact integers/Fractions. It
imports no source builder, root phase checker, NumPy or floating arithmetic.
Its native fixture is pinned. `--word` allows path relocation while retaining
that exact hash. The independent root review uses its separately written
NumPy-object Gaussian-integer implementation and source-geometry review;
these are distinct implementations, not repeated execution of this checker.

## 8. What remains open

The theorem describes one normalized operator `Q_pR` in a shared character
basis. An actual caller stage may be an adapter conjugate
`M_s^{-1}(Q_pR)M_s`, with M_s depending on the stage. Powers of one normalized
matrix do not identify a product of different conjugates. A current body
need not commute with those adapters or with the port mixing. Proving that
interface, pricing the actual queries and normalizers, and preserving all
productive targets are still necessary.

Likewise, the bounded coefficient denominators do not manufacture an
ordinary-cost implementation of the block function. All recursive calls,
raw and owned geometry, precision, source access, storage/erasure, and
foundational assumptions retain their original obligations. This package
supplies a uniform exact algebraic reduction, a sharp fixed period, and a
precise old-normalizer failure. It establishes no new complete conditional
or unconditional multiplication exponent.
