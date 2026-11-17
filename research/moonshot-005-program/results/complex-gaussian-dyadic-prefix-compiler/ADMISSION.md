# Exact determinant criterion for finite-prefix compilation

**Proved constructive classification in a specified primitive class.** Put
R=Z[i,1/2], pi=1+i. Fix any positive prefix dimension d and b>=2 equal banks.
The primitives are whole-bank ADD, whole-bank SCALE by R-units, and all
root-four prefix MONOs, each tensored with a common arbitrary tail identity.
All inputs are arbitrary; no initialized zero bank or erasure is used.

For M in GL_(bd)(R), a finite literal word for M tensor I_N exists iff

    d divides v_pi(det M).

The same word works for every positive N and uses only the existing b banks.
Its length may depend on M,d and coefficient heights. The target diag(A,I)
gives the restored-borrower corollary for one-bank A. Additional restored
equal-width borrowers cannot remove the determinant obstruction.

Necessity follows because each SCALE contributes dN times an integer
valuation, while ADD/MONO contribute zero; the target contributes
N v_pi(det M). For sufficiency, split each Gaussian-dyadic shear coefficient
into signed Gaussian binary units, even if the coefficient is a nonunit.
A monomial/scalar source transform, whole-bank ADD, and inverse transforms
restore the source. The identity E_ab=(P_ab−D_a P_ab)/2 supplies any cross-bank
coordinate shear. P_ab swaps a,b; D_a negates coordinate a.

For internal I+rE_ab with a!=b, the four cross-bank shears using P=rE_ab,
Q=E_bb exploit QP=0 and PQ=P and restore an arbitrary existing helper bank.
Gaussian-integer Euclid after algebraic denominator clearing reduces every
unimodular column to a unit pivot. Six elementary shears implement paired
diag(g^-1,g), without granting a selective scalar primitive. Recursive SL
elimination ends with pivot1. Finally one whole-bank scale and one root-four
coordinate phase normalize det M=i^e*pi^(dk) to1; compile the SL part and
undo these admitted normalizers.

At d=4, diag(2,1,1,1) is invertible over R but has determinant valuation2,
so it cannot be compiled with all other banks restored. Paired
diag(2,1/2,1,1) has determinant1 and is compilable. A larger scalar ring or
noninvertible cleanup changes the model and needs a different theorem.

[C's all-size proof](../../sessions/2026-11-17-S020/checkpoint9-evidence/C/gaussian-dyadic-prefix-compiler/PROOF.md)
includes literal programs, inverse replay, odd dimensions and an actual
Euclid compilation with nonunit first pivot3(1+i), using Fraction arithmetic.
[Root's independent review](../../sessions/2026-11-17-S020/checkpoint9-evidence/R/prefix-compiler-review/REVIEW.md)
checks the full proof and uses separate SymPy primitive replay: Walsh and
odd-dimension two-term selectors, nonunit coefficients3 and(3+5i)/8,
arbitrary-helper restoration, paired unit scales and omitted-ADD controls.
Finite checks support the identities; the proof carries all-d,b,N quantifiers.

Full prefix monomial availability is essential. A smaller catalogue requires
its own selector synthesis. No uniform resource bound as d or heights grow,
general noncommutative ordinary-unit compiler, ownership/erasure/precision
implementation or recursive/analytic guarantee follows. Prefix operations
remain paid. Credit root's proposal, C's proof and two-term selector,
retained paid-normalizer commutators, @CubeJerry and OpenAI assistance.
No new complete κ. The selected conditional bound remains .00363005817. Both strict suppliers, the outer assembly and all five foundations remain open. The programme is ongoing and is not PR-ready.
