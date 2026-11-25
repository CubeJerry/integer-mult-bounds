# A concrete algebraic hypothesis removing one exponential layer

Status: **complete conditional profile implication, pending independent review**.
The hypothesis below is open. It is not used in the unconditional source
extraction and does not assert that a compact predictor has been constructed.

## 1. The finite algebraic hypothesis

Let P_m(q_1,...,q_m) be the exact source binary predictor for shift zero,
with its prescribed central window and degree D=Theta(sqrt(m log m)).
Let B_m=Z[1/2][q_1,...,q_m]/(q_1^2-1,...,q_m^2-1).

**Hypothesis IP.** There are an absolute C>=1 and a deterministic finite
constructor such that for every sufficiently large m it constructs:

* a finite free commutative Z[1/2]-algebra E_m, with an explicit basis,
  unit, and dyadic structure constants;
* an integer w_m and t_m affine matrix pencils
  L_{m,a}=A_{m,a,0}+sum_{i=1}^m A_{m,a,i}q_i over E_m, each w_m-square;
* a verified identity in Mat_{w_m}(E_m tensor B_m),

      L_{m,t_m} ... L_{m,1} = P_m I_{w_m},                (IP1)

with t_m<=C sqrt(m log2(2m)). The algebra degree, w_m, total description
size, numerator/denominator bit lengths, and actual construction time and
workspace are all <=2^{m^C}. Arithmetic is ordinary bit arithmetic. The
bound must describe the specified constructor, not follow from output size
or an unbounded existence search.

For totality at every m>=2, dovetail this proposed constructor and its finite
identity check with the known source constructor and its check. Return the
first valid family meeting a fixed stage bound C_*sqrt(m log2(2m)), where
C_* bounds both the hypothesis constant and the source's absolute binary
constant. The source branch ensures termination even at the finitely many
initial m where the proposed constructor has no guarantee. For sufficiently
large m, the hypothesis branch and check finish in 2^{m^{C'}} time. By then
the partially executed source branch has used at most the same order of
time and visited workspace; it cannot have retained more data than its
charged work. If that branch finishes first, its complete output is bounded
by this same budget. Thus dovetailing preserves a singly exponential
generation, description and workspace profile and prevents an early trial
from hanging. Fixed extra tapes and clocks are charged in this construction.

The coefficient localization is essential: only powers of two may appear
in denominators. Consequently every identity specializes to every odd
characteristic, including the small characteristic required by interchange.
IP1 accepts arbitrary independent input on every matrix coordinate. There
are no zero-initialized auxiliary rows whose lost occupancy is ignored.
An identity only over Q, or a circuit with many scratch rows, does not meet IP.

This is a property of explicitly specified finite polynomial/algebra data.
It is stronger than the source's known quantitative representation bound,
but does not assume a tape multiplier or any input-length overhead. Its
truth is presently unknown. Given a proposed construction, finite checking
can reduce all q_i^2 to one and inspect its 2^m coefficient vectors; the
entire check remains within 2^{m^{C'}} time under the stated size bounds.

## 2. It supplies the full-rate repair family in all odd characteristics

For a shift beta, substitute q_i -> (-1)^{beta_i}q_i in the pencils and
multiply one pencil by (-1)^{|beta|}. The source count formula gives

    P_beta(q)=(-1)^{|beta|} P_m((-1)^{beta_1}q_1,...).

Thus IP1 supplies all 2^m shifts with the same stage count and w_m independent
rows per shift. Their total row count is <=2^{m^{O(1)}}. Every frequency
has at most a 1/(2m^3) fraction of shifted rows outside the central window.
The predictor is diagonal on the individual rows at every common sign
frequency, exactly as required by the source Hermite repair.

Adjoin a power-of-two cyclotomic root whose order is at least this row count.
Tensoring the explicit free algebra with that cyclotomic ring keeps degree
and construction cost <=2^{m^{O(1)}}. Pairwise node differences are units
by the explicit product formula whose product is two. Vandermonde inverses
and all 2^m Hermite tables have coordinate bit heights and dimensions
polynomial in the existing row count and algebra size. Their construction
therefore remains <=2^{m^{O(1)}}.

Four predictor applications and at most 4s row conversions give exact repair.
For the Fourier template descend to base dyadic coordinates; for interchange
reduce modulo the chosen odd p and descend to F_p coordinates. The number
of independent input rows and the number of calls both multiply by the
algebra degree. Stage count and per-input call ratios are preserved. No
new field extension is incurred at recursive depths.

This argument uses IP1 only on commuting involutions, which both source
applications provide. It does not require a polynomial identity on arbitrary
query values or ordinary-count evaluation in F_p.

## 3. Conditional finite and physical profiles

The source label and address construction is unchanged. The sharper call
analysis gives log2 m_j=O(J^3 log J), J=j+2; the absolute stage constant
in IP only changes its fixed sufficient threshold constant. The exact
call tests retain the /2 interchange and /4 pre-padding Walsh margins.

Rational address heights and numeric radices are at most 2^{m^{O(1)}}.
Section 2 bounds all scalar data by the same singly exponential envelope.
There is consequently a local finite-data bound

    P_j<=2^{m_j^{C'}},                                  (IP2)

with actual generator time/workspace bounded by a fixed power of P_j.
Apply the accepted physical ledger, including its fixed-degree setup,
numeric address-map costs, binary scalar representation, record precision,
fixed short multiplier, stream serialization, and unchanged child volumes.
It gives a_j,c_j,g_j,d_j<=P_j^{C''} and
U_j<=max{U_abs,2^{P_j^{C''}}}. All exponents here are absolute constants
depending on the single constructor in IP, not on j or input length.

The common-cap chunking and fixed restart schedule therefore give

    log2 D_j, log2 L(N_j)<=2^{C''' J^3 log2 J}.            (IP3)

Compare this with the double exponential in the unconditional extraction.
All other expenses are still charged; only the proved finite representation
bound supplied by the hypothesis removes that one exponential layer.

## 4. The complete conditional overhead theorem

Put s=log2 L(n), z=log2 s, and

    Y=[z/(2C''' log2 z)]^{1/3}.

Choose J=2^h as the largest power of two at most Y, so Y/2<J<=Y and
j=J-2 is an actual scheduled candidate. For sufficiently large n,

    C''' J^3 log2 J<=z/2,
    log2 D_j, log2 L(N_j)<=2^{z/2}=sqrt(s).

In particular n>=N_j, and sqrt(s)=o(s/Y). The fully charged schedule and
common-cap assembly give the following implication:

**Theorem IP2.** If Hypothesis IP holds, one fixed deterministic finite-alphabet
multitape machine computes exact full integer products and satisfies

    T(n)=O(n sqrt(L(n))
             2^{O(s(n)[log2 log2 s(n)/log2 s(n)]^{1/3})}),
    visited cells=O(n),                                  (IP4)

with correct fallback at every other input length. The machine executes
the constructor and actual shape tests under the same time/space caps;
the proof does not give it free advice or omit generation. The fixed
absolute prime-shape cutoff is independent of j and need not be known for
correctness.

## 5. Why this is the right next finite question

Characteristic-zero scalar count factorization satisfies an analogous
identity over a larger localization, but does not establish IP: it loses
the odd-characteristic specialization required by the label routing.
`chow-compression-barrier.md` proves that polynomially many affine products
cannot represent the literal multilinear predictor at the needed degree.
That rules out merely shortening the source tensor-product decomposition.

IP leaves two concrete possibilities: an integral identity in the Boolean
quotient that is much smaller than the literal polynomial representation,
or a different full-rate matrix factorization. Neither has been constructed
here. Failure of one decomposition scheme is not evidence against all such
families. Conversely a representation with a small dimension but enormous
coefficient heights or an unbounded search time would not prove IP4.

The conditional envelope remains larger than 2^{O(s^beta)} for every fixed
beta<1. It does not settle the polynomial or constant-overhead targets and
has no benchmark kappa_ov. This is a precise finite-algebra bridge for future
research, not an extra premise silently attached to the unconditional claim.

Credits: OpenAI source interpolation, repair and tape constructions and
their predecessors; @CubeJerry; AI-assisted conditional bridge development.
