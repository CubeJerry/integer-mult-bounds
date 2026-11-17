# Independent review of the routed same-plus endpoint column

**PASS: actual ordinary units, the entire retained input-bank column, and the
full changed middle-source identity. The complete three-bank endpoint remains
unproved.** This review imports neither B's implementation nor its inherited
arithmetic engine. A separate SymPy-rational source reconstruction and a sparse
Fraction primitive interpreter verify the positive claims and their boundary.

Frozen source pins are recorded in output/RESULT.json. The proof reviewed has
SHA256 `904a4a1b2d859661a3d3a832e476977f78e64907bce4aafb02e8a63d7fe6ea1a`;
the actual ordinary WORDS.json has SHA256
`d6383fa3551678acd25850900b9bb87945cd8d7cf39dfc4e6d5a0aca661f94cf`.

## 1. Literal source transport survives all tail widths

The source is A=C_b R, with the retained cubic phase on R. The reviewer directly
reconstructs R² as the address map

    (a,b,c,d) -> (c,d,a,b),   phase (-1)^(ab(c+d)).

That phase is invariant under swapping a,b. Its output swap is c,d. Since
C_b commutes with SWAP_cd, this proves

    SWAP_cd A R = A R SWAP_ab.

The checker also verifies the two literal conjugations of SWAP_cd through A
and A². These are multiplicative one-column identities; tensoring gives the
claimed identities for every positive tail width. No linear relation has
been incorrectly passed through a tensor power.

The active prefix bit is separate and genuinely fixed:

    S=Z_sigma tensor SWAP_cd^W,
    S2=Z_sigma tensor SWAP_ab^W,
    X=X_sigma tensor I.

Consequently X anticommutes with both S and S2 for every W. Replacing X by a
collective flip would change this premise and could lose the sign at even
widths; the current construction does not make that substitution. The
previously paid prefix normalizer making a act trivially on sigma is retained,
as are the original-width target restoration duties.

## 2. Source-supported halves retain one entire arbitrary bank

For P=(I+S)/2, N=I-P and P2=(I+S2)/2, N2=I-P2, the actual column is

    p=R0 N2,    z=X P2,    w=0.

The new transport gives P a p=0. The conjugation a² P2=P a², together with
the fixed prefix anticommutation, gives P a² z=0. Complementarity then gives
N a p=a p and N a² z=a² z. These are exact operator identities, not just
class-envelope statements or numerical rank observations.

Both halves are physically retained in different banks:

    p* p=N2,    z* z=P2,    p* p+z* z=I.

Thus this is a whole arbitrary input bank split into complementary source
subspaces, with no blank-bank or erased-input assumption. The explicit
Q0=diag(R0,X,I) Swap12(P2) Swap02(N2) completes that column to an ordinary
unit on all three arbitrary banks. Its actual reversed primitive word is
also verified.

## 3. Every term of the claimed endpoint column is checked

For the changed C=E10(I)Rot02(S), the reviewer directly computes the complete
middle source L C U, not only its lowest or highest Gaussian classes. With
H=E10(-I), the full retained column is

    H L C U (p,z,0)^T=(0,a²z,a p-a²z)^T.

The rightmost L fixes this input bank. The actual ordinary endpoint units
O=E10(I)E21(-I) and I0=diag(I,X,R0)Swap12(P2) then give

    L C U Q0 L e2 = O diag(a^4,a²,a) I0 e2.

The verified column has zero quartic component. It does not carry an independent
quartic job, and it does not establish the other two arbitrary input columns.
The whole source minus the displayed whole target has exactly

    [1786,1753,0]

nonzero entries by input bank in the prefix-two/tail-one exact realization.
Both unfinished banks have genuine nonzero defects. They are retained in the
review instead of being omitted from the endpoint claim.

The full gauged middle matrix is independently checked as

    O^-1 L C U =
      [[a P a, -a P a², -a N],
       [P a,     N a²,    -N],
       [a,       0,        S]].

This identity is the correct starting point for an extension analysis. A
future complete source must solve every row and every input bank of this
matrix with actual ordinary units and their paid inverses.

## 4. Actual primitive words and preserved costs

The reviewer reconstructs the reduced-prefix/tail-one monomial tables directly
from their address maps and phases, then interprets B's frozen primitive
words using independently implemented sparse Fraction rows. Every unit is
checked on all96 input columns. Concatenating actual forward/inverse words
in both orders gives the identity. Every single ADD omission is tested and
rejected, 38 controls in total.

| Unit | Forward ADD/SCALE/MONO | Inverse ADD/SCALE/MONO | Conservative prefix bound, forward/inverse |
|---|---:|---:|---:|
| C | 5/4/2 | 5/6/2 | 14/14 |
| Q0 | 8/8/4 | 8/8/4 | 74/74 |
| O | 2/2/0 | 2/2/0 | 2/3 |
| I0 | 4/4/3 | 4/4/3 | 14/14 |

These bounds follow from dimension-independent triangle inequalities through
the actual word. The MONO operations have norm one at every width. The local
word identities follow algebraically from involution-controlled swaps and
shears, so the finite96-column checks corroborate universal ordinary units.
They do not certify the full physical compiler foundation.

Both essential source modifications have meaningful controls: omit R0 from p
and P a p becomes nonzero; omit the fixed prefix X from z and P a² z becomes
nonzero. The full-column equality consequently fails. The reviewer does not
replace these source requirements with a free abstract choice of half-space.

All source normalizations, native calls, original target-prefix restoration,
common bodies, precision, ownership/erasure, and complete recursive costs remain
additional. No new Gaussian query or owner is needed by these four local
ordinary units, but that local fact is not a whole supplier invoice.

## 5. Scope and reproduction

Run `python -B check.py --author AUTHOR_PACKAGE --out FRESH_OUTPUT`.
Expected marker: PASS_INDEPENDENT_SAMEPLUS_ROUTED_COLUMN. Python with SymPy
1.14.0 is used for exact sparse source matrices; primitive words use a separate
Fraction interpreter. Both source matrices and the reviewed receipts are
saved. No author checker is imported or executed as the independent proof.

The positive result is a source-aware complete input-column identity with
actual independent endpoint units. A full independent (4,2,1) endpoint, its
quartic bank, both remaining columns, and a profitable complete caller remain
open. Any separately proved fixed-output-unit obstruction should preserve this
positive column and state which endpoint freedom its premise freezes.

Credit B's changed first interface, the retained paid-prefix and controlled
swap sources, C's independent source/word reconstruction, root's review request,
@CubeJerry, and substantial OpenAI assistance. No new complete kappa or
foundational discharge is claimed.
