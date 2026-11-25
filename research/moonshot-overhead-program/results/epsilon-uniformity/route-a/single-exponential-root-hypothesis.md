# A full-rate matrix-root hypothesis and its complete tape consequence

Status: **proved conditional transfer, independently reviewed by the lead
and Route C**; see `../route-c/FORMULA-TRANSFER-REVIEW.md`.
Hypothesis MR is unproved. Its implication includes generation, all shifts,
cyclotomic descent, repair, precision, physical tape work, space, chunking,
thresholds and scheduling. A conjectured matrix representation is not an
unconditional multiplication improvement.

Concurrent S002 `routes/A/compact-integral-predictor-bridge.md` at
`4689161c5bc6c9e64536034d4fa6af033d26a3e0` records an overlapping
conditional integral-predictor bridge with a more general finite-algebra
interface and the same improved envelope. This note states a specific
matrix-root sufficient condition. The overlap is credited; neither its
existence nor priority is claimed here.

Sources: OpenAI `math`, `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/repair.tex` (`lem:count-predict`, `lem:matrix-root`,
`lem:hermite-repair`, `cor:swap-repair`), `kernel.tex`, `binary.tex`; tape
`interchange.tex`, `walsh.tex`, `integers.tex`, `uniformity.tex`.
Polynomial rational-address bit heights are S002
`routes/A/rational-address-and-generator-bounds.md` at
`96028cba1342c02bdca1f537ae9a80485087bdf3`, corroborated in
`rational-geometry-height.md` and Route C's review. The physical compiler
interface is `compiler-invoice.md`.

## 1. Exact algebraic target

For each integer `m>=2`, use the source binary window:

\[
 r=\lceil\log_2(2m)\rceil,\quad B=\lceil\sqrt{2mr}\rceil,\quad
 u=\lfloor m/2-B\rfloor,\quad v=\lceil m/2+B\rceil,\quad d=v-u.
\]

Let `b` be the least power of two at least `max(2,d)`. The unshifted
predictor in `Z[1/2][X_1,...,X_m]` is

\[
 P_m(X)=(-1)^u\sum_{h=0}^{d}(-2)^h[T^h](1+T)^{-u}
 \prod_{a=1}^m\left(1+\frac{1-X_a}{2}T\right). \tag{1}
\]

Only coefficients through `d` in the formal series are used. The degree
is at most `d`. At Boolean query eigenvalues, (1) is the original count
predictor. The formula remains defined if the window extends outside
`[0,m]` at small sizes.

**Hypothesis MR.** There are absolute `C,c>=1` and one deterministic
finite-tape algorithm which, given `m`, outputs a power-of-two cyclotomic
order `2^t` and square matrices `A_0,...,A_m`, of common positive dimension
`d_M`, over `R_t=Z[1/2,zeta_(2^t)]`, such that

\[
 L(X)=A_0+\sum_{a=1}^m A_aX_a,\qquad
 L(X)^b=P_m(X)I_{d_M}. \tag{MR}
\]

The identity may hold formally or modulo `(X_1^2-1,...,X_m^2-1)`.
The following quantities are all at most `2^(C(m+1)^c)`:

- `d_M` and cyclotomic basis degree;
- numerator bit lengths and dyadic-denominator exponents, in the usual
  cyclotomic power basis;
- total output length, actual bit-generation time and visited cells.

The denominator exponent itself is bounded, not merely its encoded bit
length. These are actual bit costs, not unit-cost algebra or an unexpanded
straight-line description. Fixed enlargements of `C,c` cover dense output,
zeros and small cases. One may take `t>=2` by a constant-degree extension.

The identity acts on **every** input coordinate. A circuit computing one
output using zero-initialized workspace, a determinant representation, or
a short arithmetic formula alone does not supply (MR).

## 2. Shifts and odd-characteristic specialization

The shifted predictor is

\[
 P_{m,\beta}(X)=(-1)^{|\beta|}
 P_m((-1)^{\beta_1}X_1,\ldots,(-1)^{\beta_m}X_m).
\]

Adjoin a primitive `2b`-th root `omega`. Both orders are powers of two,
so the resulting order is their maximum. Multiplying
`L((-1)^beta X)` by `omega^(|beta| mod 2)` gives a matrix whose `b`-th
power is `P_(m,beta) I`. Signs and root multiplication preserve the
height bound. Direct sum over all shifts gives

\[
 R_{\rm raw}=2^m d_M\le2^{C'(m+1)^{c'}}. \tag{2}
\]

Every input row remains independent. Each shift occurs `d_M` times, so
the source tail bound still marks at most `R_raw/(2m^3)` exceptions per
frequency. The construction makes no assumption of zero input workspace.

Reduce the dyadic cyclotomic identity modulo an odd prime `p`. The ring
is a finite free algebra `F_p[Y]/(Y^(2^(t-1))+1)`; it need not be a field.
All denominators are powers of two. The quotient version of (MR) also
specializes because the source queries are commuting involutions. No
division by an ordinary integer count, factorial inversion, or lifting
of the label matrix to `Z/p^2` is used.

## 3. Complete repair stays singly exponential in `m`

For Hermite checks, adjoin a power-of-two root with order between `R_raw`
and `2R_raw`, so every row has its own node. Combining this with the
coefficient ring again gives a power-of-two cyclotomic extension of degree
`2^(poly(m))`. For a nontrivial power `eta^a` of its check root, a half-order
`s` satisfies `(eta^a)^s=-1`, giving

\[
 (1-\eta^a)^{-1}=\frac12\sum_{h=0}^{s-1}\eta^{ah}.
\]

Thus all node differences are units over the dyadic ring and after every
odd-characteristic specialization. Lagrange inverses and Hermite tables use
polynomially many operations on power-basis arrays of polynomial length
in the extended raw width. Numerator bits and denominator exponents add
under products and remain `2^(poly(m))`. All `2^m` frequency patterns and
all dense tables can be enumerated in `2^(poly(m))` actual bit work and
storage. On-demand generation is unnecessary for this weak bound.

Binary Hermite repair uses four predictor applications. Its pencil count
is therefore `4b=O(sqrt(m log m))`, exactly the original order. Exceptional
conversion fractions are unchanged. Basis expansion multiplies rows and
calls by the same extension rank. Consequently the proved label and
reserve inequalities retain their strict margins.

This replacement applies in **both** branches: odd-characteristic tape
interchange and the characteristic-zero Fourier/binary template. Replacing
only interchange while retaining the old Fourier Clifford matrix would
leave a triple-exponential contribution elsewhere.

### Numerical norms and dyadic descent

In characteristic zero, descend the expanded cyclotomic coefficient ring
to its finite free `Z[1/2]` basis as in the original binary construction.
If an affine matrix has dimension and coefficient heights `2^(poly(m))`,
its logarithmic row-sum norm is at most `2^(poly(m))`. Polynomially many
such finite stages and repair maps have the same coarse logarithmic-gain
bound. Basis multiplication matrices have polynomial bit length in the
basis degree and initial coefficient height, so the descent does not add
an exponential.

The completed transform is still the same normalized unitary operator.
The source common-ancestor error argument therefore applies to its new
finite instruction norms. It bounds precision and magnitude widths by
`poly(S)(1+k)` once `S` covers the new template. No unproved conditioning
assumption or unit-cost exact numerical operation is added to MR.

## 4. The complete finite budget loses one tower

Use the original label choices from `elementary-tower-extraction.md`:

\[
 \epsilon_j=\frac1{2(j+2)},\quad p=O(j+2),\quad
 r_I=O(p\log(p+1)),\quad
 \log m_I=O(Z_j),\qquad Z_j=(j+2)^3\log_2(j+3).
\]

The Fourier arity has the smaller bound
`log m_F=O((j+2)^2 log(j+3))`. Under MR, Section 3 gives finite scalar
rows, coefficients, entry counts and generation at most
`2^(poly(m_I))<=E_2(CZ_j)` in both branches.

The refined rational geometry has `poly(m_I)` entries of polynomial bit
height, and a `2^(poly(m_I))` literal generator. Its bad numerator/
denominator product `B` and the expanded scalar width `W` thus both fit
`E_2(CZ_j)`. A prime address radix above `max(W,B,2)`, found by trial
division, stays at this height; so do its monotone pieces and padding.
All finite expenses are covered by

\[
 S_j\le E_2(CZ_j). \tag{3}
\]

The source compiler proof depends on finite descriptions through fixed
polynomials in `S_j`, not on the fact that the earlier sufficient `S_j`
had height three. It therefore applies unchanged, with complete interpreted
candidate constants and thresholds

\[
 a_j,c_j\le S_j^c,\qquad
 \log U_j\le S_j^c+\log U_{\rm abs}+O(1).
\]

Its setup microstep clock, array preflight, auxiliary caps, preserved-input
fallback and reused short-multiplier scratch give the same all-length
space contract. Every stream scan and finite-table interpreter cost remains
charged. Thus this is a complete physical candidate bound, not merely a
finite arithmetic-circuit estimate.

Choose a power-of-two chunk count `R_j` just above `2c_j`. Then
`A_j<=C a_j c_j` and `N_j=max(4c_j,R_j U_j)` by the linear chunk transfer.
With standard diagonal pairing, `i_j=O((j+log S_j)^2)`. Therefore

\[
 d_j=\log(2^{i_j}A_j)\le E_1(CZ_j),\qquad
 b_j=\log(1+\log N_j)\le E_1(CZ_j). \tag{4}
\]

The entire threshold and selection invoice has lost one tower. This does
not discard the possibly large constants or assume that their numerical
values are supplied to the machine.

## 5. Conditional multiplication theorem

**Theorem, conditional on MR.** One fixed deterministic multitape machine
with finite alphabet computes exact full products in `O(n)` visited work
cells and time

\[
 T(n)\le n\sqrt L\;
 2^{\,O\!\left(x\left(\frac{\log_2(z+2)}{z}\right)^{1/3}\right)},
 \quad L=1+\log_2n,\quad x=\log_2L,\quad z=\log_2(x+16),
\]

for sufficiently large `n`.

Choose `j=floor(c_0(z/log_2(z+2))^(1/3))` with sufficiently small fixed
`c_0>0`. Then `CZ_j<=z/2` eventually. Equation (4) gives
`d_j,b_j<=sqrt(x+16)<=2sqrt x`, proving feasibility. Consequently

\[
 F(x)\le2\sqrt x+\frac{x}{j+2}
 =O\!\left(x\left(\frac{\log_2(z+2)}{z}\right)^{1/3}\right).
\]

The actual weighted schedule obeys this complete certificate and common
cell fence. The chosen `j` analyzes the schedule; it is not a selection
oracle. Small lengths use the fixed fallback. A weaker expression is
`H<=2^{O(x/(log x)^(1/4))}`. Bounded `H` is not obtained.

## 6. Scope of the unproved target

MR specifies an actual uniform matrix generator with bit and space bounds.
It is a finite-algebra representation problem for (1), not an assumed fast
integer multiplier. The published literal monomial construction does not
prove it: its dimension is `b^(H_mon)`, where `H_mon` can be exponential
in `sqrt(m) log^(3/2)(m)`. A general root-existence theorem or an arithmetic
circuit alone also does not supply the quantitative full-rate identity.

The session's separately investigated balanced-formula construction has
width `exp(exp(O(log^2 m)))`. That bound does not meet the stronger
`exp(poly(m))` requirement of MR, though it can remove one global tower
with a different dependence on `j`. Its construction and downstream proof
are separate; this note does not treat it as a proof of MR.

No available construction meeting MR is claimed. There is no Weak ETH
assumption or literature-priority claim. The constants and eventual
crossover are analytical, not evaluated practical quantities. Neither
the conjectured generator nor the complete multiplier was executed or
formally verified.

Credits: @CubeJerry; the pinned OpenAI sources and predecessors; S002's
rational-address estimates; Route B's chunk transfer; Route C's compiler
review. Developed with GPT-6 Astra Pro assistance.
