# Independent review of the fixed Cmix total-head gate

**PASS within the stated uniform fixed-catalogue / fixed-prefix model.**
The specified first interface forces every independent three-bank Gaussian
endpoint to have total head rank at most six. Its complete three-native
common-body price then exceeds every permitted endpoint price for every
0<t<1. Changed first interfaces remain open. No new kappa follows.

Reviewed author files:

- PROOF.md SHA256 `c6ad8e957faaec91b6cf9a67e601f60088ccc76bb8f4d1297a596ab0cb931b73`.
- check.py SHA256 `9b64ad117dfde8654099f0756b83f7c06b6874e830b3bb0cd9a04190658ca4d3`.

The independent checker imports no author implementation and no inherited
source arithmetic engine. It reconstructs the literal sixteen-letter source
using SymPy exact rational matrices, then uses its own formal tensor-word
algebra. It independently checks the entire decisive output row, all class-zero
coefficients, the class-one/two/three projections, the two noncommuting
reductions, the exact return monomial, the complete optimistic cost, and
meaningful physical-kernel controls.

## 1. Source reconstruction and matrix order

From the literal bit permutation and phases, the reviewer obtains

    A=C_b Rsrc,    s=SWAP_bc,    h=SWAP_bc D_b D_c^-1,
    A s A = B : (a,b,c,d) -> (d,1-c,a,b), scalar phase +1.

Both s and h are involutions. The one-column row-density classes of
A,A²,A³,A h A,A h A² are 1,2,3,1,2. The source's previously admitted Gaussian
normalizations establish their actual head types; for the obstruction it is
enough that different displayed classes have different constant row support
sizes, which ordinary monomial left and right multiplication preserve.

The checker independently builds C=Rot12(s)Rot01(h), L and U, and computes
L C U in a formal collective-word algebra. It groups words only when they
differ by a root-four scalar, legitimate on widths divisible by four. It does
not multiply the finite matrices and then improperly lift their linear
relations through a tensor power.

For the arbitrary last Q column (p,z,w), the first output is exactly

    [a²(p-z)+(a h a)(p+z)-a³z-(a h a²)z]/2.

The complete ordinary-class column is

    (0, B(p+z)/4, P_s w).

The rightmost L fixes this input bank, so the selected column is genuinely
a column of L C U Q L. Choosing this one column does not fix the second
interface Q or the ordinary input/output endpoint gauges.

For the class-two cancellation test the order is

    a^-2 (a h a²) = a^-1 h a² = m.

For the class-one test after p=-z, the third output has class-one component
N_s h a z, and the left multiplication is

    a^-1 h N_s h a z = (I-a^-1 h s h a) z/2
                     = (I-q)z/2.

No factors were commuted. The reconstructed one-column m has eight nonzero
entries per row and q has four. Both are nonmonomial. These are the exact
nonmonomial properties required below.

## 2. Why the physical kernel does not invalidate the proof

The potential trap is real: q²=I, tr(q)=8, and (I+q)/2 is a rank-twelve
projector at width one. Therefore I-q is physically singular, and a proof
that simply claimed physical injectivity would be false.

The applicable statement is instead about **ordinary operator coefficients**
in one fixed finite collective catalogue. Let G denote the root-four monomial
one-column group modulo scalar. If v is nonmonomial, the sets G and vG are
disjoint: v g=h would imply v=h g^-1 is monomial. If a finite collection of
unitaries is projectively distinct, its normalized Hilbert--Schmidt Gram
entries after width-W tensoring are

    [ tr(u_i* u_j)/16 ]^W.

Off-diagonal moduli are strictly less than one. Thus the Gram matrix tends
to identity and is invertible for all sufficiently large W, including the
subsequence divisible by four. A direct bound is
(N-1) mu^W<1, where N is the number of distinct projective words and mu<1
is their largest normalized trace overlap. Consequently no nontrivial linear
combination of words in G can equal a combination of words in vG at those
widths.

Arbitrary fixed-prefix coefficient matrices cause no problem: expand them in
matrix units and apply this linear independence to each coefficient. Scalar
and prefix coefficients may depend on W. Invertibility holds at each
sufficiently large width, so W-dependent coefficients cannot manufacture a
nonzero kernel inside that fixed ordinary coefficient space. A growing tail
catalogue or changed first interface is outside this argument.

The reviewer adds an explicit adversarial control. At width one, (I+q)/2 has
an exact expansion in **ten ordinary Hermitian Pauli monomials**. Thus a
physical ordinary z with (I-q)z=0 really exists at that width. Lift the same
ten monomials with the same coefficients collectively. Then the normalized
squared Hilbert--Schmidt norm of (I-q^(tensor W))z_W is:

    W=1: 0,
    W=4: 11/8.

For that example's twenty projective words from G and qG, the largest overlap
squared is 1/4; the exact Gershgorin condition already holds at W=8. This
finite example does not replace the all-catalogue proof. It makes explicit
why a genuine finite physical kernel cannot be used as a uniform ordinary
coefficient solution.

## 3. Arbitrary positive heads and zero-head cases

For three positive endpoint heads, ordinary class zero is absent. The exact
coefficient column then forces p=-z and P_s w=0. The column of invertible Q
has a left inverse. It cannot have p=z=0: then its remaining w image is inside
N_s, whose dimension is (16^W-8^W)/2, less than a full bank. A fixed identity
prefix multiplies both dimensions and does not remove the defect.

Thus z is nonzero. Three classes must appear:

- Class three: -a³z/2 is nonzero because a is invertible.
- Class two: a putative cancellation reduces to (I+m/2)z=0, with ordinary
  z and nonmonomial m. The disjoint-coset argument forces z=0, contradiction.
- Class one: a putative cancellation reduces to (I-q)z=0; the same
  fixed-catalogue argument applies, despite the physical kernel of I-q.

An ordinary-gauged independent three-head endpoint can contain only the
three classes of its three heads. It must therefore have multiset {1,2,3},
with total rank six. No inverse of an ordinary coefficient p,z,w was assumed.
The only invertibility used is that the full Q column has a left inverse.

For a zero head and total head rank at least seven, the exhaustive possibilities
in {0,1,2,3,4} are {0,3,4} and {0,4,4}. Both lack classes one and two.
Class-two absence gives (p-z)-m z=0. Ordinary/nonordinary separation forces
p=z=0. The last column reduces to (0,-a N_s w,P_s w). Class-one absence then
forces N_s w=0. Its image lies in P_s, of dimension (16^W+8^W)/2 strictly below
a whole bank. Again it has no left inverse. These cases are excluded.

This covers every independent endpoint with total rank above six. The proof
holds for arbitrary ordinary endpoint encoders and decoders with finite fixed
catalogues, not only for a selected literal diagonal column.

## 4. Whole native bill

The independently checked retained optimistic three-native common-body invoice
is

    P(t)=3[1]+6[7]+3[8],       [r]=r^t.

Each endpoint bank carries body rank21. Since the head ranks sum to at most
six, concavity and monotonicity imply

    T(t)=sum_j (21+r_j)^t <= 3*23^t.

For 0<t<1, strict subadditivity gives

    1+7^t+7^t+8^t > (1+7+7+8)^t = 23^t.

Therefore P(t)>T(t) for the entire interval, independently of a numerical
search. At t=199/200 the independently bounded deficit is
0.418410265240105705308957031557... . Ordinary interfaces, actual prefix
restoration, precision, ownership, erasure, native normalization, and recursive
expenses remain additional. None can repair this already-negative optimistic
bill. This is a scoped no-profit result for the specified Cmix source and
invoice, not a general impossibility theorem for three natives.

## 5. Reproduction and assessment

Run:

    python -B check.py --author AUTHOR_PACKAGE --out FRESH_OUTPUT

Expected marker: PASS_INDEPENDENT_ALL_PROFILE_CMIX_GATE.
The script uses Python and SymPy 1.14.0, exact rational arithmetic throughout.
It records author byte pins and emits the independently reconstructed source
matrices, coefficient-check receipt, complete price interval, and explicit
finite-kernel negative control. Removing the cubic or clock-square term
changes the formal source identity; deleting the h phase changes its rank-one
clock class to the ordinary return class.

The universal conclusion rests on the arguments above and the author's
precise source statement, not on replaying an author's certificate. This is
an independent research-agent review, not human or proof-kernel approval.
The fixed Cmix source is closed at the complete optimistic invoice for every
independent endpoint profile in scope. A changed first transport requires a
fresh coefficient and cost argument.

Credit S021 B's all-profile proof, the inherited return/clock source and
collective-tail separation predecessors, C's independent reconstruction and
physical-kernel control, root's adversarial review request, @CubeJerry, and
substantial OpenAI assistance.
