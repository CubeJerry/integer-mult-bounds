# A matching scoped barrier for nonstationary literal invoices

Status: **proved consequence of Theorem N; independently accepted by A, B and lead**. Reviews include `../route-b/review-nonstationary-invoice-barrier.md` and `../lead/review-scoped-adaptive-obstructions.md`. This lower-bounds a stated positive invoice certificate. It is not a time lower bound for the implemented interchanger, other routing methods, or integer multiplication.

The source is A's independently reviewed `nested-label-invoice-barrier.md`, Theorem N. It applies to arbitrary depth ell>=2, power-of-two distances, the specified first-differing-bit product rectangles, the actual rational Gram dimension D, and actual scalar rank fraction a. Its literal pencil price is

    I(m)=D(1+lambda)(1+m a).

For any real J>=64, Theorem N states

    I(m)<=m^(1/J) ==> log₂m>=2^(ell-2)J³log₂J/128.       (NI1)

The exact rank, Gram and rectangle hypotheses are essential. Faster endpoint algorithms are not covered merely because they use the same labels. Define

    g(x)=(x²log₂(x+2))^(1/3), x>=0, g(0)=0.

## 1. Direct local lower bound

**Proposition NI-L.** For every integer m>=2 and every Theorem-N label choice,

    log₂I(m)>=2^(-18)g(log₂m).                          (NI2)

For x=log₂m>=2^24 the stronger coefficient1/16 is valid.

**Proof.** Put b=log₂I(m)>0. First suppose x>=2^24. If b>=x^(3/4), use log₂x<=x^(1/4), valid for x>=2^16, and log₂(x+2)<=2log₂x. These give g(x)<=2^(1/3)x^(3/4), so b>=g(x)/16.

Otherwise J=x/b>x^(1/4)>=64 and I(m)=m^(1/J). Apply NI1 and discard only the factor2^(ell-2)>=1. Then

    b³>=x²log₂J/128>=x²log₂x/512.

Consequently b>=(x²log₂x)^(1/3)/8>=g(x)/16. This uses the actual rank without imposing occupancy at most one.

For1<=x<=2^24, D>=2 gives b>=1. The function g is increasing and

    g(2^24)³<2^48*25<2^54.

Thus g(x)<2^18, proving the common coefficient2^(-18). QED.

The quantity being lower-bounded is the source's upper invoice, rather than actual operation count. This distinction persists in every statement below.

## 2. Concavity and arity accumulation

**Lemma NI-C.** The function g is increasing, strictly concave on(0,infinity), continuous at zero, and

    sum_i g(x_i)>=g(sum_i x_i)                        (NI3)

for every finite nonnegative list.

**Proof.** Monotonicity is immediate. A positive logarithm-base factor does not affect concavity. Put L=ln(x+2), f=x^(2/3)L^(1/3). Differentiation gives

    9x²(x+2)²L² f''/f
      =-2(x+2)²L²+x(x+8)L-2x².

This quadratic in L has negative leading coefficient and discriminant

    x²[(x+8)²-16(x+2)²]=-3x³(5x+16)<0.

It is strictly negative. If S=sum x_i>0, concavity and g(0)=0 imply g(x_i)>=x_i g(S)/S. Sum this inequality. The zero case is immediate. QED.

Let e_0,...,e_r be any decreasing active-width path, with m_i>=2 and independent Theorem-N label choices at each step. Put t_i=log₂e_i and x_i=log₂m_i. Assume e_r<=e_base for an absolute base and, for an absolute C>=1,

    0<t_i-t_(i+1)<=C x_i.                             (NI4)

Then NI2, NI3 and telescoping give

    log₂ product_(i<r) I(m_i)
      >=2^(-18)g(sum_(i<r)x_i)
      >=2^(-18)g((t_0-log₂e_base)/C)
      =Omega(g(t_0)).                                 (NI5)

No stationary, balanced or geometrically decreasing choice of arity is required. More levels and unequal distances do not evade this invoice statement. Very many small arities only increase the accumulated price.

## 3. A precise normalized-recurrence barrier

A product of I(m_i) must not automatically be identified with the normalized time multiplier. The following hypotheses make the inference valid.

**Theorem NI-P.** Suppose the path has the stronger regular split

    e_i/(C0 m_i)<=e_(i+1)<=e_i/m_i                    (NI6)

for an absolute C0>=1, and its declared positive call invoice satisfies

    Lambda_i>=c0 sqrt(m_i) I(m_i), c0>=sqrt(C0).       (NI7)

Let a positive invoice certificate B_i satisfy

    B_i>=Lambda_i B_(i+1), B_r>=sqrt(e_r).            (NI8)

Additive ordinary-work bills may be included; dropping them only weakens this inequality. Then

    B_0/sqrt(e_0)>=2^[c g(log₂e_0)]                   (NI9)

for all sufficiently large e_0 and some absolute c>0.

**Proof.** The normalized multiplier is

    Lambda_i sqrt(e_(i+1)/e_i)>=I(m_i)

by NI6–NI7. Iterating NI8 bounds B_0/sqrt(e_0) below by the product in NI5. Also NI6 implies NI4 with C=1+log₂C0, since x_i>=1. Apply NI5. QED.

The condition c0>=sqrt(C0) can be weakened to a per-step normalized price at least I(m_i)^epsilon for any fixed epsilon>0; the conclusion then has a different constant. What matters is retaining a positive fixed share of the logarithmic local invoice after normalization.

### Application to the current regular source invoice

In the large-width branch of AI, ell<=e/4, A=m+2a<=3m and e/A>=4 after increasing its fixed base. Consequently

    floor((e-ell)/A)>=e/(2A)>=e/(6m).

Together with f<=e/m this gives NI6 with C0=6. The literal predictor/window invoice has a declared stage budget Dp>=sqrt(m), and its pencil price uses Cg Dg(1+lambda)(1+ma), with Dg at least the exact Gram dimension D. The term8DpRpen in Q_m, and hence the complete positive invoice Lambda, is at least8Cg sqrt(m)I(m). Its absolute coefficient exceeds sqrt(6). Thus NI-P applies to the current literal normalized invoice recurrence.

This conclusion is about the recurrence **with that price**, even if the same program might admit a better operation count or different analysis. The polynomial compact executor changes storage and setup costs; that improvement alone does not remove the present product of local geometric prices. AI's upper bound2^{O(g(log e))} and NI9 match in functional order for this restricted positive invoice certificate.

### A necessary scope check

Merely knowing t_i-t_(i+1)<=C log m_i is insufficient to identify I with a normalized multiplier. For example, a formal split e_(i+1)=e_i/m_i² and call price sqrt(m_i)I_i have normalized factor I_i/sqrt(m_i), which can be below one. Such a path still satisfies NI4 with C=2, so NI5 remains a statement about product I, but NI9 does not follow. The explicit lower split in NI6 prevents this error. It is not silently assumed from concavity.

## 4. Consequences and evidence limits

Within this family and literal invoice, changing the arity at different depths, optimizing the exact scalar rank, choosing unequal distances, or adding nesting does not lower the logarithmic normalized envelope below order

    (log e)^(2/3)(log log e)^(1/3).

A change beyond that scale must leave at least one stated premise: for example a different rectangle partition or Gram realization, a delivery schedule with a smaller actual charged price, or a predictor/width allocation that changes the positive normalized recurrence. This does not assert that any particular such change succeeds. It also does not prove a2/3 lower bound for multiplication, establish optimality of the exact program, or exclude a sharper analysis that does not multiply the literal invoices.

`verify_nonstationary_invoice_barrier.py` records finite checks of the exact concavity discriminant, the algebraic cubic implication, representative nonstationary partitions and the normalized-price inference. Its high-precision numerical subadditivity checks support the calculus proof; they are not its substitute. The fast-descent countermodel is included explicitly. No full tape algorithm or formal kernel proof is executed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. Theorem N and its exact-rank/Gram proof are A's S003 work, independently reviewed by C; the symmetric precursor was independently derived by C. A and C then independently converged on the local inversion and scoped nonstationary consequence. A's `nonstationary-invoice-barrier.md` gives the sharper uniform coefficient1/128 and an explicit terminal-base factor using a decreasing-ratio proof. This note gives a separate strict-concavity calculation and general normalization interface. These are corroborating proofs of one shared consequence, not two novelty claims. Source and prior programme credits remain as stated in those notes.
