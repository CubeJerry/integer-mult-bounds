# Independent review of the ordinary row-range gate and spectator kernels

**Accept the scoped row-range obstruction and the constructive spectator source
bridge.** Neither C_new, its column-swapped completion nor Q_kernel is a complete
independent (4,2,1) caller. No strict supplier or new kappa is established.

The accompanying checker independently rebuilds the literal source using SymPy
DomainMatrix arithmetic over Q(i). It imports no author arithmetic or verifier.
All reviewed proof/data SHA256 pins are recorded in output/RESULT.json.

## 1. Universal active-swap row range

Let f=Z_a and t=SWAP_ab Z_c be the actual one-column involutions. Independent
permutation/phase closure gives eight distinct group elements, identity trace
16 and seven zero traces. With z=(ft)^2, literal multiplication verifies
z^2=1, z central, and ft=tfz. Thus their collective tensor action at width V
has trace 16^V at identity and zero elsewhere: trace(g^tensor V)=trace(g)^V.
Its character is D/8 copies of the regular D8 character, D=16^V. Equivalently,
any group-algebra expression has trace D times its identity coefficient.
This proves the all-width trace claim; it is not an extrapolation of rank at
one width. In particular nonidentity group elements cannot collapse to the
identity at an even width.

Write P=(1+f_V)/2, M=1-P, T=(1+t_V)/2 and Zplus=(1+z_V)/2. On Zplus the two
involutions commute, so PT is itself the product range projector. On Zminus
they anticommute, giving PTP=P/2 and MTM=M/2. Therefore PT maps onto all of P
in that sector, and MT maps onto all of M. The exact range projectors are

    Rplus=P(Zminus+Zplus T),
    Rminus=M(Zminus+Zplus T).

One may check both inclusions without a rank argument: Rplus PT=PT, and
PT(2 Zminus P+Zplus)=Rplus, with the analogous M formula. The two central
sectors are orthogonal, so these are self-adjoint idempotents. Their identity
coefficients are 3/8, hence both have rank 3D/8.

The exact forward conjugates A t A^-1 and A J t J A^-1 are root-four monomial
matrices, with phases retained. A f A^-1=Z_d and J commutes with f. Expanding
the displayed projectors therefore makes both conjugated projectors ordinary
in the declared finite coefficient algebra. Their block diagonal combination
fixes the active two-bank source column and has total rank 3D/4. Exchanging
P and M preserves the conclusion.

In E=L C U Q L only the four-source term can contain Gaussian class four.
Every other word has at most three two-support source factors and therefore
one-column support at most eight. Ordinary multiplication commutes with the
Gaussian-class projection under the retained finite-catalogue separation
hypothesis. An ordinary projector fixing K thus fixes E4. A complete
independent rank-four endpoint would have rank(E4)=D after ordinary invertible
input/output transformations, contradicting rank(R)=3D/4.

This argument permits arbitrary ordinary C20, completions of C and Q within
the fixed finite root-four tensor catalogue, including actual endpoint inverse
catalogues. It needs sufficiently large faithful widths; it is not a numerical
class projection at V=1. It does not exclude growing, unpinned operator alphabets
or silently prove the retained compiler foundations.

A useful independent negative control deletes Z_c. The two one-column row
ranges then have ranks eight and eight, rather than six and six. Their sum
is D, so the strict 3D/4 gate disappears. The trace-zero premise is essential.

## 2. Exact spectator source and both ordinary kernels

For tau=SWAP_cd, the checker verifies the following literal equalities with
all complex phases, using independently reconstructed A,R2,J and Kdec:

    A^-1 tau A=SWAP_ad,
    A^-2 tau A^2=SWAP_ab,
    A J tau A^-1=Kdec,
    A tau A^3=A^3 SWAP_ab A=B2.

It also verifies tau commutes with F and J, and Kdec commutes with Fhat.
These product identities tensor directly at every V.

Projectors are formed AFTER collective lifting:

    T_V=(I+tau^tensor V)/2.

They are not tensor powers of the one-column projector. A four-bit coordinate
swap has eight fixed addresses and trace eight. Hence

    rank(T_V)=(D+8^V)/2,
    rank(I-T_V)=(D-8^V)/2.

For example at V=2 the first rank is 160, not the tensor-of-one-column value
144 and not the half-bank value 128. The exact formula matters at every width.

Let Kold=(aPa,aJMa,0)^T. Orthogonality of P,M and unitarity of a,J give
Kold* Kold=I. For K=Kold a^-1 T_V a, this implies K* K=a^-1 T_V a. Thus the
prefix rank is exactly (D+8^V)/2; it is never half of D.

The actual ordinary output unit H=O diag(I,Kdec^-1,I) satisfies

    H K=(a T_V a,0,0)^T.

Indeed the second active row becomes a tau_V M T_V a=a M T_V a; the
complementary Fhat-controlled route O combines it with a P T_V a. This proof
uses exact source identities, not a hypothetical image identification.

Putting R1plus=(I+SWAP_ad^tensor V)/2 and
R2plus=(I+SWAP_ab^tensor V)/2 gives

    H K=(a^2 R1plus,0,0)^T,
    H K a=(a^3 R2plus,0,0)^T.

Since H,a are units, for every compatible operator column X,

    KX=0 iff X=R1minus X,
    KaX=0 iff X=R2minus X.

This covers arbitrary operator columns, not merely scalar or ordinary columns.
The ordinary kernels have exact dimension (D-8^V)/2 and are nonzero for all
positive widths. The checker rejects swapping the two kernel projectors.

The projectors are ordinary mathematical blocks; they are not claimed to be
free irreversible one-bank operations. Their complementary controlled routes
are implemented as actual invertible three-bank words with charged primitives.

## 3. Pure components and actual ordinary interface words

The checker independently validates every one of the twenty supplied Gaussian
gauges against a freshly constructed canonical Gaussian product. The actual
left and right permutations and fourth-root phases are checked exactly. The
sixteen source terms in the finite P/M,T expansion are therefore genuinely
pure class two or three as asserted; purity is not inferred from support size.
The remaining gauges verify A^4, B2 and the two nonmonomial forward spectator
conjugates. The latter are class two, so the particular active-swap forward
ordinary-range proof does not apply to them. This is not a claim that no other
ordinary range obstruction could exist.

The aligned four-source column has its only nonzero bank equal to

    -a T_V a^3=-(a^4+B2^tensor V)/2.

The quartic and quadratic class components are each one-half of a unitary and
have full rank D. Their sum has the smaller rank (D+8^V)/2. Class extraction
can increase physical rank; using rank(K) alone as an endpoint obstruction
would be invalid. At sufficiently large faithful widths the two classes are
distinct. The coefficient 1/2 is outside the tensor lift, rather than raised
to the Vth power.

Every literal ordinary word and inverse is independently replayed on all three
arbitrary banks. Results agree with the prescribed block matrices. The actual
counts are:

| Interface | ADD | SCALE | MONO |
|---|---:|---:|---:|
| C_new and inverse | 8 | 8 | 3 |
| C_new SWAP12 and inverse | 11 | 11 | 3 |
| Drow and inverse | 0 | 0 | 1 |
| O and inverse | 4 | 4 | 1 |
| Q_kernel and inverse | 4 | 4 | 1 |

All 54 one-ADD omissions are independently rejected. Triangle-inequality
prefix bounds are reconstructed from the actual words: 22 for C_new in both
directions, 74/43 for the swapped completion and inverse, 1 for Drow, and 14
for O and Q_kernel and their inverses. Every MONO remains a full-field pass;
there is no free owner, lane split, volume reduction or uncharged inverse.

The primitive controlled route is H2^-1 diag(I,G) H2 with H2^2=2I. Its
block formula follows for every involution G, so the finite literal replay
extends to collective tensor controls at every V without tensoring a three-bank
matrix into 3^V banks. The two necessary source commuting identities are also
termwise tensor identities, supplying the all-width justification separately
from the one-column execution.

Replacing each literal monomial by one gives epsilon(C_new)=I,
epsilon(C_new SWAP12)=SWAP12 and epsilon(Q_kernel)=I. These are exactly the
necessary scalar completion controls at the faithful widths divisible by four.
The column swap preserves the first column and passes that necessary condition.
It does not prove full endpoint independence.

## 4. Accepted scope and remaining proof obligation

The active-swap SZ_c source is excluded in both first-column orientations.
Its previously verified kernel channels and source identities remain true;
this stronger row-range obstruction supersedes only their continuation status.

The spectator swap supplies two actual ordinary kernel channels and an
ordinary alignment of a full quartic component. It escapes the hypotheses of
the reviewed physical-injectivity, ordinary-column-injectivity and active-swap
row-range arguments. Passing necessary conditions is not sufficient for a
caller. Q_kernel has the nonzero q12=R2minus needed by the last-column rank-three
condition, but the rank-two residue and the independent rank-one job have not
been placed in independent outputs.

A complete (4,2,1) identity still needs actual ordinary C,Q and endpoint units
with their inverse recipes, followed by the retained native-source, caller,
owner, precision, compiler and recursive bills. The optimistic three-native
movement expression 3[1]+6[7]+3[8] against [25]+[23]+[22] is retained only as an
optimistic screen. Both strict suppliers and all five foundational premises
remain unresolved. No new kappa.

## Reproduction and credit

```
python -B check.py --package FORWARD_ROW_RANGE_PACKAGE --out output
```

This portable CLI needs SymPy and the five pinned package files; it does not
import any repository checker. Expected status:
PASS_INDEPENDENT_ORDINARY_ROW_RANGE_AND_SPECTATOR_BRIDGE.

Credit Worker B's constructive source and row-range proofs, Root's earlier
source/character reviews, the retained literal four-bit and S018 predecessors,
and @CubeJerry. Independent proof review and separate arithmetic by Worker C,
with substantial OpenAI assistance. This is agent mathematical review, not
human or proof-kernel acceptance.
