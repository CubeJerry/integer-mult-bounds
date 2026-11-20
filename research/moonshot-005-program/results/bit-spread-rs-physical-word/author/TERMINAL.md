# Actual GF64 K-to-facet maps preserving every native donor rank

For either of the pinned spread and mixed K words, there is a specified
physical terminal map at each of the 111 facets. The composite right-hand
linear map from the actual donor-relevant K arrival fields to the final
Y bank has rank 3,840 at all 6,470 foreign pairs. This includes the eleven
facets with a singleton K, whose terminal Ys cannot be discarded. The F
word uses earlier actually visiting X fields through paid stationary storage,
preserves an invertible map on all original late Ys, and adds no movement.

## Physical decoder

Use GF(2)[z]/(z^6+z+1). Let y be the 3,840 actual Y coordinates at facet i,
including any proper signal they already carry. Let e be its genuine X
visits before their departure for Hub. Physically compute

    E_i^T y + L_i^T e.

Transpose here is field-matrix transpose. The implemented six-bit matrices
are obtained by expanding field coefficients *after* taking this transpose.
Multiplication by an arbitrary field element need not be symmetric in the
polynomial binary basis. There is no reversal of owner travel or free adjoint.

The output is grouped into 240 channels of sixteen power-basis coefficients.
In the spread case, n=9,36 separately; in the mixed case, n=45. Each n has
k=n/3 and eight base copies of 2k channels, split as k coordinates A and k
coordinates B. Give the 28 K planes through native i distinct field nodes
1,...,28 in increasing chart order. In the following dual description, a
channel corresponds to a formal polynomial f of degree below 16. The rows
of E_i assign a linear functional of f to every actual Y. Rows of L_i similarly
assign functionals to actual X visits. No K closure to Hub is treated as an
F input.

- At fully late K on a three-receiver plane, put full A,B evaluations on
  its two actual Y stripes. The asymmetric large receiver at a two-native
  plane uses all 2k Y rows.
- At an ordinary half-late incidence, assign the A evaluations to its Y
  rows and B to its X rows on the first twelve such planes through i by
  chart order. At the other such incidences exchange A and B.
- At a singleton all terminal inputs are Y. Use the 2k ordinary channel
  evaluations on its initial 2k rows, and scaled first derivatives
  delta f'_c(x0) for c in A on the final k rows.

Exactly as in the source interpolation proof, the Y functionals at a regular
receiver consist of sixteen distinct-node evaluations per channel. At a
singleton receiver, each A channel has fifteen distinct-node evaluations
and the nonzero scaled derivative at one of those nodes, while each B
channel has sixteen ordinary evaluations. Hence E_i is invertible. The
true Ys are permuted by physical holder IDs into the ordered channel
constraint lists, then E_i^T is compiled in place by binary elimination.
For L_i^T, cache each genuine visiting X before departure (INIT and ADD),
add its indicated field coefficients to the final Y registers, then
dirty-CLEAR that snapshot. The pure Y inverse reserved for preloading at
Ground is the reverse of the late permutation and late invertible word.
It must occur in the whole-word inverse order.

## Dual kernel on the pinned K words

Fix a foreign receiver i and donor j. At each of the sixteen K charts,
the donor occupies fifteen of the 45 incoming D flags. Each component
has k of its n ordered nodes visible to j. The rows and columns here come
from the actual K word: each n-stripe uses V_n^T, and the cached early row
t-1 is added to late output t for odd t<2k at mixed native K. At a small
two-native receiver, both its early and late rows use the last k consecutive
degrees. At the large receiver its 2k late rows supply dual confluent
evaluation, and all formal derivative rows they need are present. These
relations are reconstructed against both pinned owner payloads and the
explicit K ADD templates. The right nodes are ordered by incoming D ID.
This generally differs from ordering by D-perpendicular.

Take the field transpose of the actual right (F after K) matrix *to test its
rank*. In the resulting kernel calculation an ordinary K observation
recovers all its 2k channel evaluations by the nonzero-node Vandermonde
or confluent-Vandermonde argument. Thus sixteen such K charts give injective
interpolation. This covers 6,110 pairs per word family.

For each of the remaining 360 pairs, vanishing at the fifteen ordinary
planes fixes the ratio r=phi'(x0)/phi(x0), with phi the product of their
fifteen monic linear factors. For the k nodes in the authentic singleton
K, put A(Z),B(Z) for the two polynomials of degree below k carrying the
singleton channel values. The dual observation at a visible z is

    ordinary:   A(z)+z^k B(z)+delta*r*z^(2k) A(z),
    derivative: (A(Z)+Z^k B(Z))' evaluated at z.

The high k columns enter values but *do not* enter derivatives: the given
K word stops its stored derivative at 2k. Together with the incoming D
order this is why a literal transpose of the left singleton proof would
be unjustified. With the following actual scales all relevant 2k-square
matrices have full rank.

| Facet i | Singleton K | n=9 | n=36 | n=45 |
| ---: | ---: | ---: | ---: | ---: |
| 49 | 956 | 2 | 1 | 2 |
| 97 | 982 | 2 | 1 | 2 |
| 53 | 983 | 1 | 1 | 3 |
| 77 | 1008 | 1 | 2 | 1 |
| 93 | 1009 | 1 | 1 | 1 |
| 8 | 1062 | 1 | 1 | 2 |
| 82 | 1063 | 1 | 1 | 1 |
| 58 | 1064 | 1 | 1 | 2 |
| 106 | 1090 | 4 | 1 | 1 |
| 31 | 1091 | 1 | 1 | 1 |
| 105 | 1118 | 1 | 1 | 1 |

The replay rebuilds 103,520 receiver/donor/K incidences and checks all 720
spread and 360 mixed singleton minors. For example, at F49 on donor104
with n=9, replacing delta=2 by one drops the rank to 5 of 6. At F8 on
donor3 with n=45, the same change drops rank to 29 of 30. Independence of
each subspace at one K does not by itself imply this whole-facet theorem.

## Costs, composition and reproduction

| Binary whole-record operations | Spread K to F | Mixed K to F |
| --- | ---: | ---: |
| Late E_i^T ADD | 115,166,664 | 115,166,040 |
| Actual Y permutation ADD | 7,646,796 | 7,651,512 |
| Early to late field ADD | 88,184,400 | 88,184,400 |
| Genuine early snapshot copy ADD, also INIT and dirty CLEAR each | 1,926,000 | 1,926,000 |
| Forward F ADD | 212,923,860 | 212,927,952 |
| Reserved pure Y inverse ADD | 122,813,460 | 122,817,552 |
| Forward with reserved inverse ADD | 335,737,320 | 335,745,504 |
| Extra MOVE | 0 | 0 |

A single F uses at most 18,000 extra binary owners. Across all F the bound
is 1,926,000. The construction charges all 321,000 original X visits and
uses all 426,240 actual terminal Y fields. These are costs of the explicit
F word; other methods can use fewer stationary owners.

For each pair the left source/H matrix and the right K/F matrix are square
and invertible on their relevant 3,840-coordinate D boundaries. The
published D interface requires each of sixty pair-specific D blocks to be
an invertible 8-by-8 matrix at bank480 (eight copies here). Rows through
other H, D or K cannot contain this donor's input at this receiver: the
nested chart routes would force the same incidence. Thus the pair matrix
is right times the direct sum of sixty D blocks times left, up to the
permutations of genuine boundary labels. Once the D word has been separately
pinned and verified, this proves full rank on every foreign block for the
*same* finite source, H, D, K and F. It specifies no required common inverse
for different donors. In particular it gives no fitting-rank guarantee,
strict supplier or new κ.

Run terminal.py with `--repo . --k-words PATH_TO_K_AUTHOR_OUTPUT --out FRESH`.
The checker pins both K owner payloads and their shared templates, verifies
actual recipients, timings and terminal baseline owners, and replays
each distinct transposed binary word. RESULT.json and the companion lists
of singleton minors and word hashes are deterministic. Source and K
contributors retain credit. This facet construction and its check used
substantial OpenAI assistance.
