# A fixed-output gate for every third-input shear repair of the same-plus source

**Proved scoped obstruction. The positive whole-column identity remains valid.
This fixes its simplest output unit; changed output complements remain open.**

## 1. Exact model and quantifiers

Use `sameplus-routed-endpoint-column`'s paid fixed-prefix source
a=I_prefix tensor A^(tensor W), S=Z_sigma tensor SWAP_cd^(tensor W),
S1=a^-1 S a, S2=a^-2 S a^2, P=(I+S)/2, N=I-P, Pj=(I+Sj)/2, Nj=I-Pj.
Fix C=[[P,0,-N],[P,I,-N],[N,0,P]], O=E10(I)E21(-I), D=diag(a^4,a^2,a).

For arbitrary ordinary coefficients g,h, allow

    C(g,h)=C [I+e02(g)+e12(h)].                       (1)

Here eij(g) denotes only the off-diagonal matrix entry. The bracket is a unit
with inverse I-e02(g)-e12(h), since its nilpotent part squares to zero. Neither
g nor h need be invertible, monomial, commuting, or scalar. Every physically
compiled such repair is covered; the no-go also permits the larger ordinary
coefficient algebra without claiming its full physical compiler.

There are no ordinary three-bank units Q,Iin satisfying uniformly

    L C(g,h) U Q L = O D Iin.                         (2)

All ordinary coefficients, actual inverses and g,h use one fixed finite
root-four monomial tail catalogue, with arbitrary matrices on a fixed prefix.
Exterior scalars may depend on W. The proof applies at sufficiently large
W divisible by four, using faithful tensor-word separation. It does not fix
Q's last column and includes g=h=0. Right ordinary head gauges are absorbed
into Iin. Changed left head gauges, changed O, further source changes, new
native/query calls, or a growing/noncollective tail model are outside the gate.

## 2. Exact full-source equation

Literal block multiplication, with no commutation of g,h with a,S, gives

    M(g,h)=O^-1 L C(g,h) U
      =[[a P a, -a P a^2, a(Pg-N)],
        [P a,    N a^2,   Pg-N+a h],
        [a,      0,        S+g+a h]].               (3)

For g=h=0 this is the positive package's full-source equation. Thus the
complete effects of both source repairs are retained.

## 3. The second Q column would have deficient physical rank

Write Q[:,1]=(u,v,w)^T, with zero-based index1. The corresponding column of
the rightmost L is (0,a,0)^T. Equation (2) requires every entry of
D^-1 M(g,h)(u,v,w)^T a to be ordinary. Multiplying on the right by a^-1
places every row in B a^-1, which contains only Gaussian-one coefficient
words. B is the ordinary fixed-prefix/tail coefficient algebra.

The third row is u+h w+a^-1(S+g)w. Its first two terms are ordinary and the
last has class one, so faithful Gaussian-class separation gives

    u=-h w.                                         (4)

Using P a=a P1 and (4), the second row becomes

    a^-1 N1 h w + N2 v + a^-2(Pg-N)w in B a^-1.

These three terms have classes one, zero and two. Therefore

    N2 v=0,       (Pg-N)w=0.                        (5)

The first row, using (4)-(5) and v=P2 v, becomes

    -a^-2 P1 h w-a^-1 v in B a^-1.

Consequently P1 h w=0 and t=a^-1 v a is ordinary. But v=P2 v implies

    t=P3 t,   P3=(I+Z_sigma tensor q^(tensor W))/2,
    q=A^-1 SWAP_ab A.                                (6)

The literal q has four nonzero entries per row: it is a nonmonomial
Gaussian-two involution. Ordinary words and q times ordinary words occupy
disjoint monomial cosets. Faithful fixed-catalogue separation forces t=0,
hence v=0. This is not physical injectivity: P3 is a nonzero half-bank
projector at every W. It rules out the specified ordinary collective t.

Multiplying the second equation of (5) by N gives Nw=0, hence w=Pw. Thus

    Q[:,1]=(-h w,0,w)^T=(-h,0,I)^T w,
    rank Q[:,1] <= rank w <= rank P = D_bank/2.       (7)

Every column of an invertible Q has a whole-bank left inverse from Q^-1.
Equation (7) contradicts this requirement and proves the theorem.

## 4. Preserved positive result and next task

The companion package's established (p,z,0) column has zero third entry
immediately before (1), so both repairs preserve its exact whole-column
identity. They cannot complete the caller with this fixed O and these heads:
the missing second column is deficient for every g,h, not only searched ones.

An actual changed ordinary output complement or a change to the first two
source columns is required. The positive unit/column and source transport
remain reusable. No broader endpoint or supplier impossibility follows.

## Verification

Run `python -B check.py --repo REPOSITORY_ROOT --positive POSITIVE_PACKAGE
--out FRESH_OUTPUT`. The checker authenticates the positive package and
reconstructs the source, q, its physical projector control, and equation (3)
for noncommuting and nonunit ordinary coefficient examples. The written
coefficient/coset proof carries the all-g,h and all-width quantifiers.

Credit @CubeJerry, retained source and faithful-algebra predecessors, S021 B,
and substantial OpenAI assistance. No new complete kappa or foundation claim.
