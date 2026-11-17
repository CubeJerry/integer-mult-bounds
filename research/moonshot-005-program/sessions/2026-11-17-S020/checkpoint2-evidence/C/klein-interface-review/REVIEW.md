# Independent review of the Klein three-bank source interface

**Accepted as an exact all-width ordinary interface and source identity.**
The supplied three-bank maps `C`, `C_inverse`, `H`, and `H_inverse` act
correctly on all three arbitrary bank inputs, have literal dyadic primitive
words, and require no zero bank or new owner. The exact two ordinary kernel
channels have dimension `D/4`, and the displayed source map has rank `3D/4`.
Its aligned Gaussian-four and Gaussian-two pieces have the claimed full
individual rank. Their images overlap in dimension `D/2`; these are not yet
two independent whole-bank outputs. No complete caller, supplier, or new
kappa follows from this interface alone.

The independent checker imports neither B's checker nor the retained
Gaussian matrix engine. It uses four scalar characters for the universal
ordinary unit, and a separate sparse-column implementation over exact
Gaussian rationals for the literal source and all phase-sensitive maps.

## 1. Universal unit, inverse, and all-width scope

Let `s,t` be commuting involutions in any characteristic-zero operator
algebra. Set `e_uv=(1+u*s)(1+v*t)/4`, and write

    E=e_-+, F=e_--,
    Ps=(1+s)/2, Pt=(1+t)/2, Pst=(1+st)/2.

The supplied shear word has the explicit matrix

    C = [[Ps, -E,   -F],
         [Pt, 1-E,   0],
         [Pst, 0,  1-F]],

and inverse

    C^-1 = [[ Ps, E,   F],
            [-Pt, 1-E, 0],
            [-Pst, 0, 1-F]].

On the four orthogonal character idempotents these are respectively a
lower triangular unit, identity, the determinant-one rotation of banks
0 and 1, and the corresponding rotation of banks 0 and 2, together with
their scalar inverses. The four scalar character evaluations separate the
four-dimensional rational Klein algebra. Consequently the independent
checks certify the identities in that algebra, before any particular
physical representation or width is chosen.

This is why all-width validity does not depend on extrapolating the
physical width-one matrix. In the literal source representation, the
`(-,+)` sector has dimension zero at width one but dimension 32 at width
two. A wrong unit on that sector could be invisible in a width-one check.
All four character sectors are explicitly checked here.

The first column `(Ps,Pt,Pst)` is a split copy of one free ordinary bank
inside three plus sectors. The full matrix and inverse make this stronger
than the earlier abstract split embedding: they give an actual three-bank
completion, with the other two inputs arbitrary throughout. The capacity
theorem permits this case because `2*1<3`.

## 2. Literal source, phases, and transported channels

For a basis vector indexed by bits `(a,b,c,d)`, the independent checker
constructs the admitted one-column source directly as

    A|abcd> = (-1)^(abd)/2 *
              ((1+i)|bcda> + (1-i)|b,1-c,d,a>).

This is exactly `C_b D_(acd) P` with the documented rotation. The checker
verifies both unitary inverse identities over `Q(i)`, constructs
`s=SWAP_cd` and `t=X_c X_d` from their literal permutations, and obtains
the supplied tables by matrix conjugation. All phases are compared, not
only the destination permutation. It confirms

    A^-1 s A = SWAP_ad,       A^-2 s A^2 = SWAP_ab,
    A^-1 t A, A^-2 t A^2,    Ht=A t A^-1

are root-four monomials. Erasing the phases of the second transported `t`
changes the operator. The forward conjugate of `s` is not a monomial.
No forward ordinary transport of `s` has been assumed.

For width `V>=1`, write `a=A^tensor(V)` and use collective `s,t` in the
projectors. Each displayed conjugacy lifts because tensor powers respect
products and inverses. Projectors and exterior scalar coefficients are
formed after the lift. In particular `(1-s)(1-t)/4` is not the tensor
power of its width-one counterpart: the former has rank 64 at width two,
whereas the latter would have rank 16.

The traces of the four collective Klein elements are

    D, 8^V, 0, 8^V,       D=16^V.

Thus the four character dimensions are

    (D+2*8^V)/4, D/4, (D-2*8^V)/4, D/4.

They are nonnegative for all positive widths, and the common minus
projector always has rank `D/4`.

## 3. What the source and kernel identities establish

With `K=(a Ps a, a Pt a, 0)^T`, the two vanishing conditions are exactly

    K X=0   <=>   X=(a^-1 e_-- a) X,
    K a X=0 <=>   X=(a^-2 e_-- a^2) X.

To prove the first equivalence, multiply out the two active components.
Invertibility of `a` reduces them to `Ps aX=Pt aX=0`. Since `s,t` commute,
their common minus space is precisely `im(e_--)`. Multiplication by
`a^-1` gives the assertion. The second is the same argument with `a^2X`.
This holds for arbitrary operator columns `X`; none is commuted past `a`.
The displayed transports make both right projectors actual ordinary
idempotents. Equivalently

    K* K = a^-1 (Ps+Pt) a,

whose sector eigenvalues are `2,1,1,0`. Hence `rank(K)=3D/4`.

There are two qualifications to preserve in downstream use. First, `K`
is the source column governing the four-source terms in the retained
expanded word. Its identity does not itself supply a standalone routine
that extracts this column from the complete word with arbitrary other
inputs. Second, the ordinary kernel projectors are not free whole-bank
resources. Both have ordinary augmentation zero, so the previously
reviewed capacity theorem rules out a split free ordinary bank in either
kernel, or in any finite direct sum consisting only of such kernels,
under that theorem's fixed-catalogue faithful-width hypotheses. This does
not prevent a larger invertible `Q` from having some entries in these
kernels; it constrains interpretations that would treat a kernel as an
independent bank.

## 4. Exact alignment and remaining image overlap

The retained phase-sensitive Gaussian gauges independently verify

    A^4 = ordinary_left * C_0 C_1 C_2 C_3 * ordinary_right,
    B2=A s A^3 = ordinary_left * C_0 C_1 * ordinary_right.

Both are full-rank unitaries. Their Gaussian ranks four and two follow
from the exact gauges, not merely from counting nonzero entries. Lifting
these gauges supplies the corresponding identities for every width.

Since `Ht=A t A^-1` is ordinary, its collective plus projector `P'_t`
is ordinary. Elementary multiplication gives

    a Ps a^3 = (a^4+B2)/2,
    a Pt a^3 = P'_t a^4,

and the supplied actual unit

    H = [[2,0,0],[-2 P'_t,1,0],[0,0,1]]

therefore gives

    H K a^2 = (a^4+B2, -P'_t B2, 0)^T.

The checker independently verifies this identity over exact Gaussian
rationals. Its all-width proof is the preceding algebra, with exterior
addition performed after tensor lifting.

The Gaussian-four image column is `(I,0,0)^T`; the Gaussian-two residue
has ordinary image column `(I,-P'_t,0)^T`. Their intersection is

    {(x,0,0): P'_t x=0},

of dimension `D/2`, since `trace(Ht^tensor(V))=0`. In particular the map
from two independent inputs through these two columns has rank `3D/2`,
not `2D`. No invertible left endpoint alone can separate these unchanged
columns into two full independent banks. Further contributions and the
actual `Q` must resolve this deficiency. This observation agrees with,
and makes precise, B's stated boundary of the positive result.

## 5. Full ordinary word receipts

The independently replayed primitive words give:

| Map | ADD | SCALE | MONO | MONO passes with `st` expanded | Peak magnitude factor |
|---|---:|---:|---:|---:|---:|
| C | 32 | 64 | 48 | 64 | 16 |
| C inverse | 32 | 64 | 48 | 64 | 18 |
| H | 2 | 5 | 2 | 2 | 3 |
| H inverse | 2 | 5 | 2 | 2 | 2 |

The magnitude factor assumes all three input banks have coordinate
magnitude at most one and bounds every primitive prefix by triangle
inequality. Every MONO has modulus-one entries, and every SCALE is a
nonzero dyadic with its inverse explicitly restored when it implements
an additive coefficient. Each temporary source modification is undone;
arbitrary source contents are preserved. All 68 single-ADD omissions
change the corresponding universal map. No owner, clean bank, or
Gaussian invocation is introduced by these four words.

These receipts are full invoices for the listed ordinary maps. They are
not a complete supplier invoice. Their finite operations, full-field
passes, precision requirements, and constants still need to be included
alongside the missing `Q`, endpoints, compiler, erasure, and recursive
costs. The retained gross Gaussian margin is a necessary allowance for
that future assembly, not evidence that the final margin survives.

## 6. Reproduction and provenance

Run the independent checker with the exact source snapshot and B package:

    python -B workers/C/klein-interface-review/check.py \
      --repo source --author workers/B/klein-three-bank-interface \
      --out workers/C/klein-interface-review/output

The result pins B's supplied words/proof and the admitted Gaussian gauges.
Additional controls reject missing Gaussian phases, an incorrect active
swap, collective/tensor projector confusion, and reliance on the
nonfaithful width-one Klein representation.

Credit @CubeJerry, the retained source authors, B's dyadic unit and source
application, root/C's Klein-capacity observation, the ordinary-capacity
proof, and substantial OpenAI assistance. Worker C supplied this
independent arithmetic implementation and all-width review. All five
foundational assumptions remain; no strict supplier or new complete
kappa is claimed.
