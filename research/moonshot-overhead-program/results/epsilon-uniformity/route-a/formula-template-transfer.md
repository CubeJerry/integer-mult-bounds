# From cyclic formula factorizations to complete tape profiles

Status: **complete downstream proof, independently reviewed by the lead and
Route C**; see `../route-c/FORMULA-TRANSFER-REVIEW.md`. The algebraic
construction is `../route-c/FORMULA-FACTORIZATION-COMPRESSION.md`. This note
prices coefficients and the literal generator, inserts it into both source
branches, and derives complete physical candidate profiles. It does not
assume the stronger singly-exponential matrix-root hypothesis in the MR note.

Original manuscripts: OpenAI `math` at
`3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier `build/repair.tex`
(integral predictor, matrix root, Hermite repair, `cor:swap-repair`),
`kernel.tex`, `binary.tex`; tape `interchange.tex`, `walsh.tex`, `integers.tex`,
`uniformity.tex`. Physical costs are in `compiler-invoice.md`. Rational
address heights use S002 `routes/A/rational-address-and-generator-bounds.md`
at `96028cba1342c02bdca1f537ae9a80485087bdf3` and the corroborating
`rational-geometry-height.md` with Route C's review.

## 1. Algebraic interface

For `m>=2` commuting involutory queries, use the source window `[u,v]`,
`D=v-u=O(sqrt(m log m))`, and

\[
 P_m(X)=(-1)^u\sum_{h=0}^{D}(-2)^h[T^h](1+T)^{-u}
 \prod_{a=1}^m\left(1+\frac{1-X_a}{2}T\right).
\]

The finitely many small source windows outside `0<=u<v<=m` use the
original finite construction, as specified in Theorem F; increasing an
absolute constant absorbs them. All large selected template arities use
the formula construction below.

This equals `sum_(s=0)^D c_s e_s((1-X_1)/2,...,(1-X_m)/2)`, omitting
`s>m`, with integer coefficients

\[
 c_s=(-1)^u\sum_{h=s}^{D}(-2)^h{-u\choose h-s}
\]

of `poly(m)` bits. Balanced variable division and convolution give a
division-free formula of size

\[
 T_m\le2^{C(\log_2(m+2))^2}. \tag{1}
\]

Cyclic factorization products concatenate tensor factors; sums use the
graded tensor sum at common length; scalars multiply one factor. Omitting
unit children and padding constants by identities preserves length `D`.
Formula size is not used as the pencil-stage count.

The equal-rank recurrences are `K_product=K_1 K_2` and
`K_sum=d K_1 K_2`, `d<=D`. Therefore

\[
 \log_2K\le T_m\log_2\max(2,D)
 \le2^{C'(\log_2(m+2))^2}. \tag{2}
\]

Every cyclic product is `P_m I_K`. Pad to the least power of two
`b>=max(2,D)` and form the cyclic block matrix. It has dimension `bK`,
is affine in the queries, and its `b`-th power is `P_m I_(bK)` on every
coordinate. Factors use `Z[1/2,zeta_M]`, with `M=lcm(1,...,D)`; including
a harmless factor two covers sign conventions. Thus `M<=2D!` and
`log M=O(D log(2D))=poly(m)`.

## 2. Coefficient heights and the literal generator

A large matrix-operation count alone would not bound coefficient heights.
Here every new factor entry is obtained by copying an old entry, multiplying
by a root of unity, adding at most two inherited entries, or scaling by a
coefficient `c_s`. Product composition concatenates `A_i tensor I` and
`I tensor B_j`; it does not multiply two affine factors into one entry.

Temporarily represent coefficients by polynomials of degree below `M` in
`zeta_M`, with a common dyadic denominator. Root multiplication is a cyclic
array shift because `zeta_M^M=1`. This redundant representation is valid;
the identities hold in the cyclotomic quotient, not necessarily in the full
group ring. Formula paths have at most `T_m` additions/scalings. Numerator
bits and dyadic exponents are consequently `poly(T_m,m)`. There is no
height-doubling recurrence once per entry of an expanded dense matrix.

Choose an absolute constant in

\[
 Q_m=2^{\,2^{C(\log_2(m+2))^2}}
\]

large enough. Equations (1)--(2), `M<=2D!`, and the coefficient estimate
bound every intermediate rank, list length, array length and bit height by
a fixed power of `Q_m`. At each formula node, expand the matrices literally
and write their dense affine coefficient lists. Sequential scans and
schoolbook integer operations give an actual generator with `Q_m^c` bit
time and visited cells, for absolute `c`. It does not enumerate possible
matrices or treat a compressed formula as a free dense expansion.

### Descent to dyadic coefficients before specialization

Construct the cyclotomic polynomial `Phi_M` explicitly. Its degree is at
most `M`, and its coefficients have at most `M+1` bits: they are sums of
products of unit-modulus roots, bounded by binomial coefficients. Divisor
enumeration and recursive exact monic polynomial division of `X^d-1`
construct every needed `Phi_d` in `poly(M)` bit work. A deliberately
loose polynomial bound also covers temporary coefficients: at most `M`
division steps each add at most a polynomial in `M` to their bit lengths.

Reduce each coefficient to the basis `1,Y,...,Y^(phi(M)-1)` and replace it
by its regular multiplication matrix. Reduction and multiplication matrices
have bit lengths polynomial in `M` and the previous height. This adds only
a fixed power of `Q_m` to dimensions, output length and generation work.
The resulting affine matrix `L_m` has dyadic coefficients and dimension

\[
 d_m=bK\phi(M)\le Q_m^{c},\qquad L_m(X)^b=P_m(X)I_{d_m}. \tag{3}
\]

The target `P_m` is dyadic, so its regular representation is precisely
`P_m I`. The identity retains all coordinates and introduces no initialized
auxiliary input. No integer divisor of `M` is inverted. Thus it can later
be reduced modulo every odd prime even when an intermediate cyclotomic
order was divisible by that prime.

## 3. All shifts, repair, and both source branches

The source shifted predictor is

\[
 P_{m,\beta}(X)=(-1)^{|\beta|}
 P_m((-1)^{\beta_1}X_1,\ldots,(-1)^{\beta_m}X_m).
\]

Use the common factor skeleton: substitute the query signs and multiply
one factor by `(-1)^|beta|` before forming the cyclic block and descending.
Every cyclic product picks up that sign once, so the resulting matrix has
`b`-th power `P_(m,beta) I`, the same dimension, and dyadic coefficients.
Use one block of `d_m` independent input rows for every shift. The raw width
`R=2^m d_m` remains `Q_m^c`. Each shift occurs equally often, so the original
Hoeffding argument still marks at most `R/(2m^3)` exceptional rows at every
frequency. No component of a factorization block is treated as zero-filled
scratch or discarded.

Adjoin a power-of-two root of order between `R` and `2R` for distinct
Hermite nodes. The resulting power-of-two ring has degree at most
`poly(R,b)`. For a nontrivial node ratio `eta^a`, choose its
half-order `s`, so `(eta^a)^s=-1`. Then

\[
 (1-\eta^a)^{-1}=\tfrac12\sum_{h=0}^{s-1}\eta^{ah}.
\]

All differences are therefore units over the dyadic ring and after odd-prime
specialization. Lagrange formulas generate the Vandermonde inverses and
repair tables using polynomially many operations on arrays of polynomial
size in `R`. Their coefficient bit lengths remain polynomial in `R` and
the earlier bit bounds. Enumerating all `2^m` patterns and writing all
dense tables, without an on-demand shortcut, costs `Q_m^c` bit time/space.

Binary Hermite repair applies the predictor four times. It still uses
`4b=O(sqrt(m log m))` pencil stages and the same exceptional conversion
fraction. If base change expands an algebra-valued row into several
independent base rows, the input-row count and pencil/conversion call count
are multiplied together. All normalized call ratios are unchanged.

For **interchange**, reduce the dyadic/power-of-two-ring identities modulo
the chosen odd characteristic. The source queries are commuting swaps, so
substitution is valid. Finite free basis expansion produces `F_p` matrices;
no field assumption, count division, or `p`-adic lift is required. The
label-rank, rectangle-incidence and reserve estimates remain exactly those
already established. Their fixed strict contraction margin survives.

This does not contradict the count-modulo-`p` obstruction: the compiled
polynomial retains elementary symmetric functions of the individual
queries. It is not replaced by a scalar function of their field-valued
sum. Integer coefficient preparation is completed before specialization;
only dyadic denominators occur in the resulting matrices.

For **Fourier/Walsh**, use the characteristic-zero identity and descend
the remaining power-of-two cyclotomic ring to dyadic scalar matrices as
in the source. Every row still undergoes the intended query product.
The source normalization, even-width dyadic layout and fixed odd-width
butterfly remain valid. Replacing both branches is essential: retaining
the old Fourier Clifford matrix would retain a third tower elsewhere.

### Numerical conditioning is included

Every new matrix dimension, entry count and coefficient bit length is
`Q_m^c`. Its logarithmic row-sum norm is therefore `Q_m^c`, after an
absolute power enlargement. The finite stage list and all check/table maps
have product logarithmic gain `Q_m^c` as well. This is deliberately coarse,
but it does not introduce another exponential into the precision bits.

Completed normalized transforms are unitary. The same common-ancestor error
argument in `T/uniformity` applies with these actual finite norm majorants,
giving working integer/fractional widths `poly(S)(1+k)`. The exact bit
interchanger has no numerical faults. Scalar approximation, word arithmetic
and final exact rounding are priced by the existing compiler invoice.

## 4. Complete source-template budget as a function of `j`

Set `theta_j=1/2+1/(j+2)` and `rho_j=1/2+1/(2(j+2))`, as before, and
write `Z_j=(j+2)^3 log_2(j+3)`. The explicit interchange labels give

\[
 p=O(j+2),\qquad r_I=O(p\log(p+1)),\qquad
 m_I=2^{r_Ip^2},\qquad \log m_I=O(Z_j).
\]

The new predictor does not alter its pencil-stage count, so the proved
strict interchange margin remains valid at these parameters. Equation (2)
and the complete scalar costs in Sections 2--3 give

\[
 Q_{m_I}^{c}\le E_2(CZ_j^2).
\]

The Fourier arity has `log m_F=O((j+2)^2 log(j+3))`; its new scalar budget
is `E_2(O((j+2)^4 log^2(j+3)))`, inside the interchange bound. Thus both
branches have the same sufficient common budget.

Rational address geometry has `poly(m_I)` entries of polynomial bit height,
including all factors and inverses. Its integer values, bad-value product
and explicit generation cost are `2^(poly(m_I))<=E_2(O(Z_j))` by the refined
geometry proof. Expanded scalar rows `W` have the larger bound
`E_2(O(Z_j^2))`. A prime address radix above `max(W,B,2)` can be found by
trial division in a fixed polynomial of its value. Its padding factor
and monotone scaling pieces therefore fit the common bound as well.

Consequently a complete generated finite budget can be chosen with

\[
 S_j\le E_2(CZ_j^2). \tag{4}
\]

It covers total list lengths, all coefficients and row roles, stage/pass
counts, radix/scaling **values**, source generation steps, and visited
generation cells. These are actual expanded quantities. An arbitrary slow
generator or an extension-alphabet lookup table is not being bounded.

## 5. Transfer through the physical compiler and common space cap

The independent source/compiler audit in `compiler-invoice.md` uses the
finite data only through fixed powers of `S`. Its estimates do not require
that an older sufficient bound on `S` had height three. With (4), it gives
complete interpreted core profiles

\[
 \begin{aligned}
 t_j(u)&\le a_j u(1+\log_2u)^{\theta_j} &&(u\ge U_j),\\
 \operatorname{space}_j(u)&\le c_j(u+1) &&(u\ge1),\\
 a_j,c_j&\le S_j^c,\qquad
 \log_2U_j\le S_j^c+\log_2U_{\rm abs}+O(1).
 \end{aligned} \tag{5}
\]

In particular the new finite widths and norms are not silently absorbed
into a free arithmetic operation. Their powers of `S_j` appear in the
physical row scans, scalar products, code interpretation, precision and
per-volume workspace. The fixed short multiplier remains an independent
known primitive, with reused additive scratch bounded by its time.

All input-dependent non-volume setup is at most
`G(S_j)(1+k)^(E(S_j))`, with `G,E<=S_j^c`. The same sufficient
`k>=64(E+ceil(log G)+1)^2` absorbs it into `2^(k/4)`. The machine uses
the actual source shape/padding checks, aggregate setup-microstep clock
and auxiliary cell fences; it does not need an unknown absolute constant
as input. Preserved-input fallback gives the all-length space bound.

Choose a power-of-two chunk count just above `2c_j`. The complete wrapper
then has `A_j<=C a_j c_j`, threshold `N_j=max(4c_j,R_j U_j)` and one
common `O(n)` visited-cell bound. With standard sum-diagonal enumeration,
`i_j=O((j+log S_j)^2)`. Thus

\[
 d_j=\log_2(2^{i_j}A_j)\le E_1(CZ_j^2),\qquad
 b_j=\log_2(1+\log_2N_j)\le E_1(CZ_j^2). \tag{6}
\]

This is the complete profile supplied to the lead's envelope inversion.
Both feasibility and cost lose one tower. The constants remain analytical
and unspecified; no practical crossover or full astronomical execution is
claimed. Written algebraic and physical review, rather than a finite
matrix example alone, is required for the asymptotic conclusion.

## 6. Relation to the stronger open target

Concurrent S002 independently established the same balanced-formula
full-rate construction and complete global envelope at commit
`58c754b583815e4fe40d333ec9d71e4c254749ba`. Its corresponding notes are
`routes/B/formula-full-rate-linearization.md`,
`routes/A/formula-extraction-theorem.md`, and
`routes/C/FORMULA-CYCLOTOMIC-GENERATOR.md`. The present derivation and
physical transfer have separate written proof and review; no priority
claim is made.

The proved generator scale here is
`exp(exp(O(log^2 m)))=exp(m^(O(log m)))`. It is not bounded by
`exp(m^C)` for one fixed `C` on the strength of this estimate. Therefore
the stronger singly-exponential hypothesis MR remains open, and its
`E_2(CZ_j)` profile must remain separately conditional. This formula
construction supplies `E_2(CZ_j^2)` instead.

Credits: @CubeJerry; the original OpenAI constructions; the cited cyclic
factorization work and Route C's explicit construction; S002's label and
rational-address estimates; Route B's common-space chunk transfer; the
source/compiler independent reviews. Developed with GPT-6 Astra Pro
assistance. No priority claim is made.
