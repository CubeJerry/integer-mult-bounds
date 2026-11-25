# A formula-size interface for the remaining representation gap

Status: **proved conditional transfer; independent review requested**.
This follows from the cyclic construction and complete physical invoice;
it is not an additional unconditional improvement. It identifies a concrete
sufficient algebraic target for the open matrix-root hypothesis.

## 1. Finite formula contract

Let \(P_m\) be the actual dyadic integral predictor in (A1) of
[THEOREM.md](THEOREM.md), with source degree
\(D_m=O(\sqrt{m\log(m+2)})\). Consider a binary arithmetic formula with
variable/dyadic-constant leaves and addition/multiplication nodes. Assign
syntactic degree one to variables, zero to constants, maximum at addition,
and sum at multiplication. Require output syntactic degree at most \(D_m\).

Suppose one total deterministic finite-tape algorithm outputs a valid such
formula, with \(F_m\) nodes, at every source-applicable \(m\ge2\). Bounded
source-window exceptions use an explicitly supplied valid baseline formula;
validity is never conditional on passing an unknown asymptotic cutoff.
Numerator bit lengths, dyadic denominator exponents, actual formula-generation
time and workspace must eventually be polynomial in \(m+F_m\), with absolute
degrees. The complexity bounds may hold only eventually; correctness holds
at every parameter used. Let \(f(m)\ge m+2\) be a nondecreasing upper envelope
for \(F_m\).

This is a contract for a finite polynomial, not a multiplication runtime
assumption. It excludes free circuit sharing, arbitrary odd denominators,
high-degree intermediate terms whose cancellation is ignored, and
unbounded search for a short formula. All duplicated formula nodes count.

## 2. Complete finite-data transfer

**Lemma G1.** Under the contract, both source branches have a full-rate
predictor/repair implementation with complete finite budget

\[
 S(m)\le 2^{C\{m^C+F_m\log_2(m+2)\}}.                  \tag{G1}
\]

This includes actual generation, dense scalar data, coefficient bits,
numerical logarithmic norm majorants, address integer values, radix value
and finite geometry. The label parameter is bounded by a fixed power of
\(m\); enlarging the absolute \(C\) covers it.

**Proof.** The cyclic construction in
[FORMULA-FACTORIZATION-COMPRESSION.md](route-c/FORMULA-FACTORIZATION-COMPRESSION.md)
gives \(\log_2 K\le F_m\log_2\max(2,D_m)\). Factor lengths never exceed \(D_m\).
The common root order is at most \(D_m!\), with logarithm
\(O(m\log(m+2))\). One final padding and free regular-representation descent
multiply dimension by at most \(O(D_m D_m!)\) and give a dyadic affine root
on every coordinate.

Entry operations are copying, root shifts, addition and constant scaling.
Constant-only subtrees may be evaluated first; their numerator bit lengths
are at most the sum of leaf numerator bit lengths and leaf dyadic
denominator exponents, plus the addition count. Thus coefficient bits
and denominator exponents are polynomial in \(m+F_m\) before descent.
Dense cyclotomic generation and companion powers have polynomial cost in
\(D_m!\) and those lengths. Literal intermediate matrices and generation
therefore fit (G1).

All shifts, frequency patterns, power-of-two Hermite tables and subsequent
basis expansions multiply that budget by fixed powers and at most
\(2^{O(m)}\). The target scalar becomes the scalar times the entire identity,
so there is no initialized-subspace loss. The identity specializes in every
required odd characteristic and also supplies the characteristic-zero
Fourier branch. Logarithmic instruction norms have the same budget.

Refined address geometry contributes values and generation at most
\(2^{m^C}\). A compatible prime above the full width and bad-value product,
its trial-division search, padding and scaling pieces cost a fixed power
of those values. Absorb all fixed powers into \(C\). ∎

## 3. Complete rate implications

Let \(Z_j=(j+2)^3\log_2(j+3)\). Both accepted source arities have
\(\log_2 m_j=O(Z_j)\); use their maximum with the nondecreasing envelope.
The physical compiler, common-space chunking and actual restart schedule
give the joint estimates

\[
 d_j\le C\{m_j^C+f(m_j)\log_2(m_j+2)\}^2,\qquad
 b_j\le C\{m_j^C+f(m_j)\log_2(m_j+2)\}.             \tag{G2}
\]

Here \(d_j=\log_2(2^{i_j}A_j)\) and
\(b_j=\log_2(1+\log_2 N_j)\). The square pays for the full sum-diagonal
index. These are complete cost and eligibility coordinates, including
actual generation and the common all-length visited-space contract.

For fixed real \(a\ge1,b\ge0\), assume the specified formula constructor has

\[
 f(m)\le2^{C[\log_2(m+2)]^a
                    [\log_2\log_2(m+4)]^b}.             \tag{G3}
\]

Then (G2) implies

\[
 d_j,b_j\le2^{C' Z_j^a[\log_2(Z_j+2)]^b}.            \tag{G4}
\]

The address term \(m_j^C\) is included because \(a\ge1\); all squares only
enlarge the fixed coefficient in this exponent.

**Theorem G2.** Under the finite formula contract and (G3), one fixed
exact deterministic finite-alphabet multitape multiplier visits \(O(n)\)
cells and has

\[
 T(n)\le n\sqrt L\;
 2^{O\!\left(x
    \left(\frac{[\log_2(z+2)]^{a+b}}{z}\right)^{1/(3a)}
       \right)},\quad
 L=1+\log_2n,\quad x=\log_2L,\quad z=\log_2(x+16).       \tag{G5}
\]

Choose the integer

\[
 j=\left\lfloor c
    \left(\frac{z}{[\log_2(z+2)]^{a+b}}\right)^{1/(3a)}
    \right\rfloor
\]

with sufficiently small fixed \(c>0\). Its unrounded value tends to infinity.
The exponent in (G4) is \(O(j^{3a}[\log(j+3)]^{a+b})\), hence at most
\(z/2\) eventually. Both coordinates are then at most
\(\sqrt{x+16}\le2\sqrt x\), proving eligibility. Adding \(x/(j+2)\) bounds the
certificate. Integer rounding changes only a constant and \(\sqrt x\) is
negligible on the displayed scale. The actual fixed schedule, correct
fallback and common physical fences give (G5). No parameter oracle or
free circuit compilation is used. ∎

| Formula size with the degree/bit contract | \(a,b\) | Sufficient exponent of \(H\) | Status |
|---|---|---|---|
| \(\exp(O(\log^2m))\) | \(2,0\) | \(O(x([\log(z+2)]^2/z)^{1/6})\) | Balanced formula and cyclic construction proved in this session. |
| \(\exp(O(\log m\log\log m))\) | \(1,1\) | \(O(x([\log(z+2)]^2/z)^{1/3})\) | Requires this bound with syntactic degree and dyadic-generation control; general small-formula results do not automatically supply it. |
| \(m^{O(1)}\) | \(1,0\) | \(O(x(\log(z+2)/z)^{1/3})\) | A polynomial-size degree-preserving dyadic formula would suffice for MR; no such family is proved here. |

These are upper-transfer theorems, not lower bounds on the smallest formula
or multiplier. The polynomial-formula condition is sufficient for the
stronger matrix-root hypothesis but need not be necessary: a direct matrix
construction could satisfy MR without a small scalar formula.

## 4. Endpoint scope

Even the polynomial-formula row retains \(m_j=2^{O(j^3\log j)}\) and the
complete source cost/threshold profile. The displayed sufficient rate remains larger in
scale than \(2^{O(x^\beta)}\) for every fixed \(\beta<1\). Better formulas alone,
through this invoice, do not prove bounded overhead. Window depth, repair,
local call mass and physical costs remain separate questions.

The concrete obligation is to control formula size **and syntactic degree**,
coefficient localization, generation and full independent-row occupancy
together. An abstract ring of unit-cost scalars or a small determinant
expression does not itself meet this contract.

Credits: the cyclic tensor-factorization literature cited in Route C; the
pinned OpenAI predictor and physical construction; S002 rational-height
and conditional-IP work; @CubeJerry. Prepared with GPT-6 Astra Pro assistance.

