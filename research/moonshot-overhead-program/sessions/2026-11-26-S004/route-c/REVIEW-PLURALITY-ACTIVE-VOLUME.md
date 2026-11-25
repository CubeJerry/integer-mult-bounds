# Independent audit of the equivariant-sector active-volume theorem

**Verdict: pass for PA1–PA9 in the stated regular linear-network model.**
Reviewed the complete lead draft, including the refreshed top-two-count
boundary and unequal-physical-multiplicity qualification. The result is a
scoped algebraic invoice, with a sharp limiting error constant. It does
not establish a tape-time lower bound or an efficient physical inverse.

## Algebra and scope

The tie rule is genuinely equivariant: translating every exponent and
the anchor by one preserves every compared cyclic residue. Hence the
entire regular monomial basis, including ties, splits into exactly equal
cyclic sectors. No probabilistic tie deletion is required. For a sector
map D, the equations chi v_(j-1)=D_j v_j determine all components from
one chosen component backwards around the cycle. This proves the exact
rank floor (1-1/r)NW without assuming D invertible or A-linear.

Outside the top-two-count gap boundary B_d, changing at most d exponent
coordinates preserves the unique plurality symbol. Each count difference
can move by at most 2d. Thus every potentially off-sector column is one
of the h copies of B_d, proving PA5 even for arbitrary, noncommuting
coefficient matrices. Constants in fact have zero off-sector loss; the
tau_0 convention in PA7 is conservative, as the draft explicitly says.

The block completion is valid over finite fields as well as infinite
ones. Rank normal form lets one fill a square block with exactly its
nullity many independent corrections. Nullity(G_0) is at most
rank(G-G_0) when G is invertible. Consequently the completed comparison
has distance at most twice the off-block rank, and multiplication by
invertible maps preserves the rank of the inverse difference. The
comparison may mix regular coordinates within one sector: this is an
enlargement for a rank proof, not an uncharged operation offered to the
physical algorithm.

For a finite linear network, replacing one actual gate changes the output
by a prefix–local-difference–suffix product. Copying, reuse, width changes,
and additions can be represented as rectangular constant row maps, so
the rank inequality remains valid without charging a copied port again.
Actually repeated port applications are separate occurrences. A general
K-linear low-rank port gives the regular-rank version; a spectral-average
interpretation additionally requires A-linearity. These distinctions are
present in the reviewed draft and are necessary.

The fraction argument uses no commutation between numerator and
denominator. After completion to an invertible sector map, the ordinary
product-difference identity bounds the error by the numerator loss plus
twice the denominator boundary loss. If the original denominator is
singular, its nullity contributes once more. From A=PB, the identity
P-A_block B_completed^-1 = [P(B_completed-B)+(A-A_block)]
B_completed^-1 proves the stated rank sum. The BP order is symmetric.

The elementary count-difference atom estimate and a union bound over
pairs imply the top-gap boundary estimate. For fixed r and sub-square-root
active query volume, PA2 follows. A constant root-of-unity scalar attains
error 1-1/r exactly, so the asymptotic constant is sharp. The spectral
average is uniform for the regular representation. A physical payload
with unequal multiplicities needs its actual representation checked;
mere presence of each root is insufficient. The order-five two-by-two
gate exposes only three roots and cannot use the full r=5 conclusion.

## Independent exact checks

`verify_phase_block_rank.py` was written independently of the lead prose.
Its top-two-count boundary now matches the refreshed theorem. Its saved
receipt `phase-block-rank-verification.json` passes:

- 4,653 equivariant phase identities and 16,383 off-boundary preservation
  checks for alphabet sizes two through five;
- six invertible affine-pencil completions over F4 and F5, all six with
  genuinely singular sector-diagonal parts;
- six exact witnesses attaining the cyclic rank floor;
- 36 left/right fraction rank bounds and 18 arbitrary sector-map bounds.

The completion routine actually performs elimination, fills the missing
rank, transforms back, and checks both invertibility and exact correction
rank. The negative control rejects the ordinary least-index tie rule on
(0,1,2). These finite controls supplement the proof and do not certify
unbounded parameter ranges on their own.

Credit is joint lead/C as stated in the source note: the lead supplied
the written network composition; C supplied the equivariant tie rule,
fraction extension, independent checker, and this adversarial audit.
