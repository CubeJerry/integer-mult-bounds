# Small subfields inside one fixed root encoding

Status: **proved algebraic/bit-complexity component; independent review
pending**. This supplies the local field enumeration needed by the optional
streamed Lagrange evaluator when all recursive data keep one larger root
field. It is not a new multiplication theorem or a premise of admitted V.

Immediate setting: E002's `variable-interchanger-space.md` chooses one
root field E=F_(2^S), with S an even power of two and an explicit polynomial
basis. Root `streamed-lagrange-coefficients.md` requires enumeration of a
field of polynomial local size. Enumerating all 2^S root elements at every
small child would not have that cost. The construction below avoids it.
The concurrent E003 common-field and full-rate packing notes are distinct
representation options; no claim of replacing or originating them is made.

## 1. Construct the subfield by a binary kernel

**Lemma SE1.** Let r divide S. Given the explicit polynomial representation
of E, one fixed deterministic binary multitape algorithm constructs an
F2 basis of the embedded subfield F_(2^r) in time and space polynomial in S.
It can then enumerate exactly its 2^r elements using O(S+r) running bits
beyond that stored basis and polynomial(S) work per emitted element.
It never enumerates E as part of finding the subfield.

Proof. Frobenius x -> x^(2^r) is F2-linear. In the supplied S-coordinate
basis, construct the binary S-by-S matrix of

    F_r(x)=x^(2^r)+x.

For each basis vector use r successive squarings and one addition.
Polynomial-basis multiplication/reduction costs polynomial(S) actual tape
steps; r<=S. Binary Gaussian elimination finds a basis of ker(F_r) with
polynomial(S) bit work and workspace. Even naive sequential matrix access
only changes the fixed polynomial degree.

The roots of T^(2^r)-T form a field: they contain 0 and 1 and are closed
under addition, multiplication and inverse. There are exactly 2^r roots
in E. To see this without a search, r|S implies T^(2^r)-T divides
T^(2^S)-T by iterating Frobenius (or telescoping its powers). The latter
polynomial is the product of T-a over all a in E. Both derivatives are
one, so every root is simple and all 2^r roots lie in E. Therefore the
kernel has F2 dimension exactly r and is the required subfield.

Enumerate the 2^r binary combinations of its r basis vectors. An r-bit
counter and a current S-bit field register suffice; recomputing a linear
combination costs polynomial(S), or a Gray-order update uses one root-field
addition. This is an injective enumeration of exactly the small field.
The basis itself occupies O(rS) bits and remains a local compact descriptor.
No polynomial factor in numeric 2^S occurs. QED.

The produced basis need not be a polynomial basis for the small field.
All arithmetic may remain in the root polynomial representation. Inverses
of nonzero local elements can use exponent 2^r-2, with O(r) root-field
multiplications; their coordinates stay in the same subfield.

## 2. Polynomial local size under a power-of-two root degree

For B>=2 local check nodes, let r be the least power of two at least
max(2,ceil(log2 B)). If the root degree S is a power of two large enough
for the largest B in the invocation, then r<=S and r|S. Moreover

    B<=q_local=2^r<4B^2.

(The loose bound also covers B=2 and B=3.) Thus all local nodes and all
nonzero local field elements can be streamed in polynomial(B,S) bit work.
Because r is even, the small field contains the embedded F4. A supplied
root omega satisfying omega^2+omega+1=0 is fixed by its 2^r Frobenius.
The same order-three constants are therefore used at every child.

For the shift construction B=Theta(m), node preparation and a complete
small-field enumeration cost polynomial(m,S). Root-field data remain
arbitrary E-valued records. Choose the first B elements of the computed
subfield enumeration as nodes. Their Vandermonde determinants are nonzero
inside the subfield and hence in E.

## 3. Streamed coefficient extraction is valid in the root field

Let F be this subfield, of size q, and let |J|<=s<q-1. Form each Lagrange
polynomial from nodes in F. Its coefficients lie in F. The character sum

    [T^i]L_j(T)=sum_(t in F*) t^(q-1-i) L_j(t)

holds inside F and therefore inside E. All accumulators can use the
unchanged S-bit root representation. Its loop length is q<4B^2, not 2^S.
The double repair sum and arbitrary-E-input proof of SL2 are unchanged;
no root-field datum is converted into a smaller field or truncated.

The complete coefficient calculation has polynomial(m,S) bit work and a
polynomial(S) local basis descriptor plus a constant number of S-bit field
registers and logarithmic loop counters. Repeated spectral membership
queries must still be supplied by the source comparison/count scans.
The physical role alignment, root-field payload format and removal of
metadata before children remain separate requirements.

At one spatial location a constant number of coefficient/count streams
has O(S+log m) bits, comparable to the S-bit input symbols. This supplies
the missing finite-field-enumeration contract for the optional low-storage
streamed repair. It does not by itself prove its entire tape layout,
endpoint space or a stronger envelope. The admitted grouped-role method
already supplies those gates without this optional alternative.

## 4. Constructive limits and next check

The divisibility r|S is essential. If the root degree is an arbitrary
integer, the same kernel has dimension gcd(r,S), which can be too small.
Choosing power-of-two root and local degrees is an explicit design choice;
it cannot be inferred just from large root-field cardinality.

The algorithm constructs the binary Frobenius matrix, performs exact
Gaussian elimination and emits linear combinations. It does not rely on
an irreducible-factor oracle or a constant-time field lookup. Existing root
field construction remains separately charged. The finite checker in
`verify_embedded_subfields.py` records exact kernel dimensions, closure and
coefficient extraction in small extensions; it is not a tape simulation.

Open next question: independently review this optional subfield contract
and compose it with an actual constant-stream comparison/count layout if
that alternative is useful. No change to admitted V is requested.

Credits: standard Frobenius and finite-field algebra; Jerry Chen (@CubeJerry),
E002 root streamed Lagrange proposal and common-root-field choice; substantial
AI-assisted constructive bit-cost analysis.
