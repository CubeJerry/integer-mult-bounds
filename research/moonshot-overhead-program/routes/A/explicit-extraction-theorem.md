# An explicit slow overhead envelope from the source construction

Status: **accepted for the stated source-extraction contract after independent review**. The finite-generator gate is recorded in `../C/REVIEW-A-BOUNDED-GENERATOR.md`; the physical and end-to-end gates are recorded in `../../verification/S002/lead-review-physical-compiler.md` and `../../verification/S002/lead-review-explicit-extraction.md`. This is an AI-assisted mathematical audit, not a formal build or execution of the complete multiplier.

The source is OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`.
This is a quantitative extraction from the November construction, with the
new restart/chunk assembly of `scheduler-and-chunking.md`. It is not a claim
of asymptotic improvement over an unspecified published o(1).

## 1. Precise source-profile inputs

For each integer j>=1, put

    theta_j=1/2+1/(j+2),   rho_j=1/2+1/[2(j+2)].

The independently audited finite constructor and physical-compiler lemmas establish the following profiles for the pinned source interfaces. There are absolute constants
C0,C1 and a fixed input cutoff U_abs, independent of j, such that:

* An actual finite search through m=2^u+1 accepts by
  m_j<=2^{C0(j+2)^6}. It verifies the complete interchange coefficient
  <=m^rho_j/2 and pre-padding Walsh coefficient <=A^rho_j/4. Padding by
  at most two therefore preserves a factor-two contraction margin in
  both recursions; exact V/W tape children need no such extra factor.
* Set Rhat(m)=2^{2^{m^100000}}. For some P_j<=Rhat(m_j)^{C1}, all local
  instruction counts, expanded sizes, numeric address coefficients/radix,
  and numerical coefficient bit heights are bounded by P_j. The finite
  construction uses explicit ring arithmetic and the complete rational
  compatibility list, including factor inverses and diagonal units.
* The actual generator time g_j, its retained/work space d_j, interpreted
  time coefficient a_j, and proportional visited-space coefficient c_j
  are at most P_j^{C1}. The candidate is correct at every input length,
  using exact shape checks and schoolbook fallback when needed. For
  u>=U_j it satisfies

      tau_j(u)<=a_j u L(u)^theta_j,
      space_j(u)<=c_j u+d_j,
      U_j<=max{U_abs,2^{P_j^{C1}}}.                        (E1)

Here L(u)=1+log2 u. We may enlarge P_j so a_j,c_j>=1 and 1/(theta_j-rho_j)
<=P_j. The visible log^4 L factor from the physical ledger is absorbed
using P1 of `parameter-thresholds.md`, with polynomial 1/slack coefficient.

U_abs is the source's absolute prime-shape/short-geometry cutoff. No numeric
value is asserted. Correctness never requires knowing it: the actual
candidate checks every needed shape and uses the correct fallback. The
asymptotic profile contains one fixed cutoff independent of j, which is
all that the asymptotic rate proof uses.

The finite bounds above are justified by `scalar-template-growth.md`,
`rational-address-and-generator-bounds.md`, `bounded-source-generator.md`,
and `physical-compiler-ledger.md`; no arbitrary generator delay is inferred
from output size. A finite matrix/call identity and a tape implementation
are separate obligations, and both appear in this input list.

## 2. A uniform profile majorant

**Lemma E1.** The preceding profiles imply, after increasing one absolute
constant C and taking the bounded initial range separately,

    log2 P_j, log2(g_j+d_j+a_j+c_j+2), log2 L(U_j)
        <= E_j := 2^{2^{C(j+2)^6}}.                       (E2)

Proof. From log2 m_j<=C0(j+2)^6,

    m_j^100000<=2^{100000 C0(j+2)^6},
    log2 Rhat(m_j)=2^{m_j^100000}
        <=2^{2^{100000 C0(j+2)^6}}.

Fixed powers and fixed multiplicative constants are absorbed by enlarging
C. Also log2 L(2^{P_j^{C1}})=log2(1+P_j^{C1})=O(1+log2 P_j).
The fixed log2 L(U_abs) is covered by another absolute enlargement of C.
This is an existence of an absolute bound, not a claimed computed numerical
prime-gap cutoff. QED.

## 3. One candidate fits a common physical cap

Use only the sparse subsequence j_h=2^h-2, h>=2. Its exponent excess is
exactly 2^{-h}. For each h and chunk exponent k>=0, try r=2^k chunks,
skipping r>n. Reserve a separate first attempt for the fixed schoolbook
multiplier. Enumerate (h,k) diagonally as in A3, so its attempt index i obeys

    i <= (h+k+1)^2.                                      (E3)

For a fixed j=j_h choose r_j to be the least power of two >=4c_j. Thus
4c_j<=r_j<8c_j. Set

    N_j=max{8c_j,4(c_j+d_j),r_j U_j},                     (E4)

rounding upward to an integer. If n>=N_j and u=ceil(n/r_j), then u>=U_j,
r_j<=n, and

    c_j u+d_j <= c_j n/r_j+c_j+d_j <= n/2.                (E5)

This includes generation/description workspace d_j rather than treating
it as a proportional space coefficient. The wrapper's input, output,
diagonal accumulator and schedule occupy their own absolute O(n) regions.

A4's physical diagonal assembly computes all chunk products in time

    t_j(n)<=g_j+C(a_j+1)c_j n L(n)^theta_j.               (E6)

Its proof charges operand positioning, the r_j^2 products, convolution
diagonals, low-part additions, amortized high-part carry increments, erasure,
and exact 2n-bit output. In particular the movement/carry wrapper is O(nr_j),
not an unquantified O_{r_j}(n). It uses O(n) visited cells uniformly in r_j.
All scratch is reused after each digit multiplication.

## 4. The fixed restart machine

The code lengths in A1 are

    ell_i=floor(log2 i)+2ceil(log2(1+floor(log2 i)))+3.

In round v give every eligible i with ell_i<=v a fresh budget 2^{v-ell_i}.
Their Kraft mass is exactly 3/16. The proved decoder/clock/cleanup estimate
makes the total round cost O(2^v), with one initial O(n) marking scan.
For a successful attempt taking t steps this gives

    T(n)<=C[n+i(1+log2 i)^2(t+1)].                        (E7)

Generating a template, reading the input, operand copies and all chunk work
are inside the timed attempt. Abort before leaving the marked regions.
Unsuccessful attempts return no result; every completed candidate returns
the correct product, since its own short/failed-shape branch is exact.
The separate schoolbook attempt ensures termination at every length, and
the last round is O(log n), so the clocks and schedule fit the same O(n)
visited-cell allowance. Thus this is one fixed deterministic finite-alphabet
multitape machine with a common number of tapes, not a choice of machine
depending on n.

Let k_j=log2 r_j and combine (E3), (E6), and (E7). There are coefficients
D_j and thresholds N_j such that

    T(n)<=C n sqrt(L(n)) [1+D_j L(n)^{1/(j+2)}]
                                  whenever n>=N_j,     (E8)
    log2 D_j, log2 L(N_j)<=2^{2^{C'(j+2)^6}}.             (E9)

To check the constants, k_j=O(1+log2 c_j), so the scheduling factor is at
most O((h+k_j+1)^2(1+log2(h+k_j+1))^2). It is polynomial in log P_j and
h, hence bounded by a fixed power of P_j. The additive g_j and t+1 also
fit a fixed power of P_j times n L(n)^theta_j. Equation (E4) gives
log2 L(N_j)=O(1+log2 P_j)+log2 L(U_abs) by (E1). Lemma E1 absorbs these
fixed powers and constants. This proves (E9) without ignoring the schedule,
chunk count, generation time, or a validity threshold.

## 5. Choosing an eligible sparse parameter

Write s=log2 L(n). Let C' be large enough for (E9), and for sufficiently
large s put

    X(s)=[log2 log2 s/(2C')]^{1/6},
    h=floor(log2 X(s)),   j=2^h-2.                       (E10)

When X>=4 this is an allowed h>=2, and

    X/2 < j+2 <= X.

The right side of (E9) is then at most

    2^{2^{C' X^6}}=2^{sqrt(log2 s)}=:F(s).               (E11)

For sufficiently large s, F(s)<s and F(s)=o(s/X). The first inequality
ensures log2 L(N_j)<s=log2 L(n), hence n>=N_j: the chosen parameter is
actually eligible. The second follows by taking a binary logarithm of
F(s)X/s, which is sqrt(log2 s)-log2 s+log2 X and tends to minus infinity.

Finally, (E8) gives

    log2 H(n) <= O(1)+log2 D_j+s/(j+2)
               <= O(1)+F(s)+2s/X
               = O(s/(log2 log2 s)^{1/6}).               (E12)

**The assembled source-extraction theorem**, after acceptance of the precise source-profile proofs in Section 1, is therefore

    T(n)=O(n sqrt(L(n))
             2^{O(s(n)/(log2 log2 s(n))^{1/6})}),
    visited cells=O(n),                                  (E13)

for one fixed machine and sufficiently large n. Equivalently its logarithmic
exponent excess is O((log2 log2 s(n))^{-1/6}), which tends to zero. The
bounded initial range is handled by the already installed correct fallback.

## 6. Meaning and limits

This is an explicit rate for the construction's residual subpower overhead.
It is much slower than 2^{O(s^beta)} for every fixed beta<1, and does not
reach the poly(s) benchmark or the constant-overhead endpoint. No benchmark
kappa_ov is assigned. An explicit rate alone cannot be called an improvement
over the published unspecified o(1); it quantifies what the audited source
construction and its compiler guarantee.

The dominant dependence is the finite polynomial-linearization/cyclotomic
repair description, retained to preserve the odd-characteristic interchange
identities. The characteristic-zero compact count predictor has not been
substituted into that construction. Route C's count-residue obstruction
explains why such a direct substitution would be invalid.

The theorem is an asymptotic rate with absolute constants, not a practical
implementation estimate or a numerical starting threshold. No Lean kernel
certification or full tape-program execution is asserted. Finite exact
checkers support the algebraic and scheduler lemmas; independent source
review is recorded separately.

Next: sharpen the quantitative profile and compare with any quantitative extraction already in the literature. All source-profile review gates listed above are accepted. Credits:
OpenAI's November and September constructions and cited predecessors,
@CubeJerry, and AI-assisted proof extraction and verification.
