# Independent review of the same-plus fixed-output gate

**PASS within its precise fixed-output / fixed-tail-catalogue scope.**
The positive routed input-column identity is retained. For the specified O
and literal heads a4,a2,a, no ordinary second interface and input endpoint unit
can complete the source, even after arbitrary third-input shear repairs g,h.
A changed output complement or changed first two source columns remains open.

Reviewed proof SHA256:
`5d34d4e386aab40e82722a8b118ec67b5deda56cf38eb46d93f6caa7985080a5`.
Reviewed checker SHA256:
`e202ab0a202d49aceba8981075962dcbf1a679d8fb5cde7f69c52db5780d285d`.
The independent review imports neither author code nor an inherited arithmetic
engine. It verifies the full source equation in a free noncommutative polynomial
algebra, reconstructs the source and nonordinary witness with exact SymPy
matrices, and provides a genuine finite-width physical-kernel control.

## 1. Complete source repairs are retained without commuting coefficients

Let T(g,h)=I+e02(g)+e12(h). Its nilpotent part squares to zero, so its inverse
is T(-g,-h) for arbitrary coefficient operators g,h. They need not be units.
The independent free-algebra checker treats a,S,g,h as opaque noncommuting
symbols, expands P=(I+S)/2, N=(I-S)/2, and obtains identically

    O^-1 L C T(g,h) U =
      [[a P a, -a P a², a(Pg-N)],
       [P a,     N a²,  Pg-N+a h],
       [a,       0,     S+g+a h]].

No finite g,h example is substituted for this universal identity. Replacing
Pg with gP or deleting the final a h term changes the free polynomial and is
rejected. Both repair inverse orders are verified in the same algebra.
Because T acts identically on every vector with zero third component, it
preserves the already established routed whole input column immediately after
U. The obstruction concerns its missing complement, not a defect in that
positive result.

## 2. Independent elimination of the missing second Q column

Write Q[:,1]=(u,v,w)^T. The corresponding rightmost-L column is (0,a,0)^T.
After dividing the output by D=diag(a4,a²,a), each row times a must be ordinary.
Equivalently each row belongs to B a^-1, where B is the allowed ordinary
coefficient algebra.

The third row is

    u+h w+a^-1(S+g)w.

Its first two terms are class zero; the last and B a^-1 are class one.
Eventual fixed-catalogue class independence therefore gives u=-h w.
This step does not claim that a^-1 B equals B a^-1.

Substituting into the second row gives

    a^-1 N1 h w + N2 v + a^-2(Pg-N)w in B a^-1.

The displayed terms have classes one, zero, and two, respectively. Their
separation forces N2v=0 and (Pg-N)w=0. No coefficient has been inverted.
Since v=P2v, the first row reduces exactly to

    -a^-2 P1 h w-a^-1 v in B a^-1.

Thus P1h w=0, and t=a^-1 v a must be ordinary. Again no g,h,a or projector
factors have been commuted. The checker separately verifies the inverse
one-column head support sizes2 and4, giving the necessary class distinction.

From v=P2v follows

    t=P3t,
    P3=(I+Z_sigma tensor q^(tensor W))/2,
    q=A^-1 SWAP_ab A.

The exact source reconstruction verifies q is the third source conjugate,
is a unitary involution, and has four nonzero entries in each row. It is
nonmonomial.

## 3. The ordinary coefficient conclusion is uniform, not physical injectivity

The equation t=P3t gives

    t=(Z_sigma tensor q^(tensor W))t.

For an ordinary coefficient t with one fixed finite collective monomial tail
catalogue, the two sides have supports in disjoint tail cosets G and qG.
Distinct projective unitary words become linearly independent at sufficiently
large W because their normalized Hilbert--Schmidt Gram matrix tends to the
identity. One can use (N-1)mu^W<1 as a quantitative sufficient condition.
This holds on the width subsequence divisible by four required by the model.
Arbitrary fixed-prefix coefficient matrices are handled entrywise, and the
left multiplication by Z_sigma is invertible. Hence t=0 at every sufficiently
large width, including when the exterior coefficients depend on W.

This does **not** assert that P3 or I-P3 is physically injective. In fact P3
has rank16 out of32 in the explicit reduced-prefix/tail-one representation.
More generally the genuine prefix sign bit makes its trace exactly half the
full bank dimension at every W, so its physical range is always nonzero.

The reviewer constructs an explicit ordinary one-width Pauli expansion of P3
with fixed prefix matrices. It solves (I-Z_sigma tensor q)t=0 at W=1. Lifting
that same finite catalogue collectively gives normalized squared failure

    W=1: 0,
    W=4: 15/16.

Thus the finite physical kernel is preserved as a control, while the proposed
uniform ordinary coefficient solution fails. The all-catalogue proof is the
coset/Gram argument, not this one example. Growing catalogues, growing source
prefixes, noncollective operations, and changed output units are not covered.

## 4. Actual physical rank deficiency of the Q column

Since t=0, v=0. Left-multiplying (Pg-N)w=0 by N gives Nw=0, because NP=0.
It follows that w=Pw. The entire second Q column is therefore

    (-h w,0,w)^T=(-h,0,I)^T w.

Its rank is at most rank w, hence at most rank P. The fixed prefix sign bit
makes rank P equal to half a bank at every width, with unused fixed prefix
identities scaling both ranks equally. Every column of an invertible
three-bank Q has a left inverse on an entire bank. The half-rank bound
contradicts that requirement.

This is a full-column contradiction for arbitrary ordinary Q and input
endpoint unit. It includes nonunit, nonscalar and noncommuting g,h and the
unrepaired g=h=0 case. It fixes the exact output O and literal left head gauges.
Right ordinary head gauges can be absorbed in the arbitrary input endpoint
unit. Changing the output complement or left head gauges is a new premise
and must be analyzed separately.

## 5. Assessment and reproduction

Run `python -B check.py --author AUTHOR_GATE_PACKAGE --out FRESH_OUTPUT`.
Expected marker: PASS_INDEPENDENT_SAMEPLUS_FIXED_OUTPUT_GATE. Outputs record
the frozen author pins, universal free-source polynomial, exact source witness,
physical-prefix kernel control and reviewed elimination chain. All arithmetic
is exact; no author checker is run as the independent proof.

The gate shows that the simplest output unit attached to the successful
whole-column construction cannot be extended by changing only Q, the input
endpoint unit, or these third-input source shears. It does not invalidate the
positive C,Q0,O,I0 words or their exact primitive invoices. It does not rule
out a changed output complement, another source, extra natives, or a different
uniform model. No new complete kappa or foundational discharge is claimed.

Credit S021 B's gate, the retained source/faithful-algebra predecessors,
C's independent free-algebra/source review and physical-prefix control,
root's review request, @CubeJerry, and substantial OpenAI assistance.
