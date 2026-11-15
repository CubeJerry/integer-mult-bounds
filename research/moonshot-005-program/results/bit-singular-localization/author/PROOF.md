# Exact localization of the singular fitting code and the direct-acquisition gate

**Author result; independent review pending. Fixed-source algebraic theorems and
a narrowly specified acquisition obstruction. No new kappa.**

This is a fresh reconstruction and proof. The S013 checkpoint mentions a pending
singular-localization/trellis investigation, but no corresponding proof or
certificate is present in the exact starting tree
`9fb0a34adad2f5903d3169fee7f7a7fcb6f03e3a`. We do not claim to have recovered or
verified that unpublished worker result.

## 1. Fixed source and definitions

Use the 111 rational native root lines in
`sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`, Git blob
`8eba43d142c819c206dce5df87ea4571aaead287`, SHA-256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
That file is the admitted exact recovery from authenticated source witnesses;
this result does not relabel it as a fresh replay of the original gzip source.
The original source hash remains
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.

Let the real roots be `r_i`, their own final facets `F_i=r_i^perp`, and the
singular binary functional be `h`, with mask 189 in the admitted frame
`(0,1,2,4,8,14,30,59)`. Its pivot is 38. The native D8 set `D={h=0}` has 52
indices; the half-spinor set `S={h=1}` has 59. Write `K_ij=1+B(x_i,x_j)` and

`A_ij = K_ij (1+h_i+h_j)`.

The predecessor proves that the binary row code `W=row(A)` has the direct sum
decomposition

`W = W_D + W_S`, with dimensions `7+8=15`,

where the summands are supported on the disjoint sets D and S. This is the same
singular code `C_s+hC` in `results/bit-singular-pivot-split/author/PROOF.md`.

For any real chart C, let `L_C` be the coordinate space supported on native root
lines contained in C. Put `W(C)=W intersect L_C`. A word is *properly supported*
if the real span of the roots in its nonzero support has dimension below eight.
All claims below refer to this actual real support, including charts absent
from the old word; a binary polar subspace is not substituted for a real chart.

## 2. Exact localization theorem

**Theorem 1.** The following statements hold for the actual native source.

1. W has exactly 69 nonzero properly supported binary words. Every one has real
   support rank exactly seven. There are no nonzero W words supported in a real
   chart of dimension at most six.
2. Their support spans are exactly 61 facets of full E8 root lines. The complete
   list of nonzero localized codes is:

   | Facet normal | Number of facets | Dimension of W(C) |
   |---|---:|---:|
   | Native D8 root | 52 | 1 |
   | Omitted D8 root | 4 | 2 |
   | Omitted half-spinor root | 5 | 1 |

   Every other proper real chart has zero localized code. In particular, all 59
   native half-spinor receiver facets have zero localized code.
3. At a native D8 receiver `i`, the localized code is exactly
   `W(F_i)=span(h K_i)`, a pure half-spinor mode. At an omitted D8 facet the two
   dimensions split into one D8 mode and one half-spinor mode.
4. The span of all properly supported W words has dimension 12. Its D8
   projection has dimension four and its half-spinor projection has dimension
   eight. There are exactly four nonzero pure D8 localized patterns and 61
   nonzero pure half-spinor localized patterns; the remaining four proper words
   are their sums within the four two-dimensional omitted D8 facet codes.

### Exact finite proof

The independent checker reconstructs the binary coordinate system and W directly
from the pinned rational roots. It imports no predecessor checker or precomputed
singular-code basis. It enumerates all `2^15-1=32767` nonzero words exactly.
For 32698 words it exhibits rank eight modulo 103, proving real rank eight. For
each of the remaining 69 it exhibits seven independent support roots modulo
103 and computes a nonzero rational normal annihilating **every** supported
root. The two bounds give exact real rank seven. The certificate retains each
word, its complete support, the seven-row witness and the primitive integer
normal. There is no numerical rank tolerance.

Grouping by the exact normal gives 57 one-dimensional and four two-dimensional
localized codes: `57*1+4*3=69` nonzero words. Each normal is identified with one
of the reconstructed full 120 real root lines. Native/omitted status and D/S
class are checked against the pinned coordinates. Binary elimination verifies
the stated spans and the native receiver identities. Since every nonzero proper
word has support rank seven, an unlisted proper chart cannot contain it: its
support span already determines its unique proper facet. This certifies all
real charts, not only the 61 listed candidates.

The computation proves a finite-source proposition exactly. The next paragraph,
not sampling of extension fields, supplies its universal algebraic extension.

### Arbitrary characteristic-two fields and block widths

Let K be any field of characteristic two. A word of `W_K=W tensor_F2 K` has
finitely many coefficient scalars. Choose an F2 basis for their finite F2 span
and expand the word in that basis. This expresses it as a K-linear combination
of binary W words whose support union is exactly its support: independence of
the coefficient basis prevents cancellation between these components. Thus a
K-word supported in C has every binary component supported in C. Conversely,
K-linear combinations of `W(C)` are supported in C. Therefore

`W_K intersect L_C(K) = W(C) tensor_F2 K`.

Every localization statement and dimension above persists over K. Tensoring
the coordinate space with `K^V`, for any integer `V>=1`, multiplies localized
dimensions by V. This does not require commuting block maps or scalar copies
of an algorithm.

## 3. Every fitting contained in W has full rank 15V

**Theorem 2.** Fix any characteristic-two field K and `V>=1`. Let M be any block
fitting of this native source: its own blocks are `I_V`, its noncontact blocks
are zero, and every row lies in `W_K tensor K^V`. No restriction is imposed on
commutation or rank of the remaining V-by-V blocks. Then

`row(M)=W_K tensor K^V`, and `rank(M)=15V`.

**Proof.** Compare receiver i's V rows with the corresponding V rows of
`A tensor I_V`. Their difference has zero own and noncontact blocks, hence is
supported on native lines in `F_i`. It also lies in the W tensor space. For a
half-spinor receiver Theorem 1 makes this intersection zero. Its rows are
therefore forced to be precisely the split fitting rows. Across all 59 such
receivers these span `W_S tensor K^V`, dimension `8V`.

For a D8 receiver the permitted difference is in `span(hK_i) tensor K^V`,
contained in that already-forced half-spinor space. On projecting to the D8
columns, its rows are again forced to be those of `A tensor I_V`. Their projected
rank is `7V`. Consequently M has rank at least `8V+7V=15V`; containment in the
15V-dimensional W tensor space supplies equality. This proves the claim. QED.

Theorem 2 closes a concrete possible decoder escape: changing the fitting
coefficients while staying inside W cannot reduce the global fitting dimension.
It says nothing about a fitting in a larger or different code, and it does not
equate fitting rank with the number of mutable physical packets.

## 4. The exact direct-acquisition capacity is three dimensions

Consider, first, the following purely algebraic acquisition problem. For each
proper real chart C, choose a subspace

`U_C <= (W_K tensor K^V) intersect L_C(K^V)`.

Let `I_C` contain every original input index on which some row of `U_C` has a
nonzero block. Require the sets `I_C` for distinct charts to be disjoint. This
expresses direct use of unchanged original records at at most one incomparable
facet; it grants arbitrary cochart computation and arbitrary reuse within that
one facet. It does not grant copies or recoded local carriers to another facet.

**Theorem 3.** For every such family,

`dim(sum_C U_C) <= 3V`.

Equality is attained in the algebraic acquisition problem.

**Proof.** All nonzero localized modes have rank-seven support, so each
nontrivial chart is one of Theorem 1's facets. At a given facet, its D8 projection
is either zero or the tensor product of one of four scalar D8 patterns with a
subspace of `K^V`. Exact source checks show that these four patterns have
pairwise intersecting supports. If two distinct facets had nonzero D8
projection, each would require an original input from their common support,
contrary to disjointness. Thus the sum of the D8-projection dimensions is at
most V.

Likewise each localized half-spinor projection uses one of 61 scalar patterns.
The exact disjointness graph on these patterns consists of 28 disjoint edges
and five isolated vertices. Every edge is a complementary pair with XOR equal
to h; no three patterns have pairwise disjoint supports. Thus at most two
distinct facets can have nonzero half-spinor projection, for total dimension
at most `2V`. Each `U_C` has dimension at most the sum of the dimensions of its
two projections. Summing gives the claimed `3V` bound. This argument permits
arbitrary partial-rank block subspaces; it is not a rounding of scalar widths.

For equality, use the omitted D8 normal
`b=(0,0,1,1,0,0,1,-1)` and the native partner `a=r_72`. The first facet supplies
its full two-dimensional local code, with one D8 and one half-spinor mode. The
second supplies its one-dimensional half-spinor mode. The two half-spinor
patterns are complementary; the D8 pattern has disjoint block support from
both. Thus the two facets use disjoint sets of original inputs and provide
three independent scalar modes. Tensor with `K^V`. QED.

The 28-edge matching statement is a complete exact check of a fixed 61-vertex
graph; all modes are independently reconstructed from the pinned source. No
failure to find a larger family is used as an impossibility argument.

## 5. A scoped q>=12 source gate

**Corollary, direct-code acquisition model.** Suppose a proposed source has:

- at most q whole-V seed values acquired at Hub, with their X coefficient rows
  lying in `W_K tensor K^V`;
- proper-chart W innovations acquired directly from unchanged original X
  records, each original visiting at most one rank-seven facet;
- no copying of raw local X information or recoding of originals that exports
  local information to a second facet, and no transport of temporary local
  forms outside W between acquisition cells;
- all global W observations used by the receivers generated from those seed
  rows and direct proper-chart innovations, by arbitrary linear arithmetic;
- a complete native fitting inside W, allowing arbitrary block coefficients.

Then `q>=12`.

The global observation span has dimension at most `qV+3V` by Theorem 3. Its
complete fitting has rank `15V` by Theorem 2. Thus `15V<=qV+3V`. This can also
be read as a cellwise chronological induction: imported global rows do not add
rank outside the current span, and an exported new W row differs from imported
W rows by a directly acquired local W form. Lower-dimensional cells have no
such forms. A raw local temporary may be used inside its acquisition cell, but
transporting it to another cell changes the declared model.

The dimension bound is sharp as an abstract construction: the certificate
selects a 12-dimensional complement of the three witness innovations inside W.
No physical source word for that 12-seed relaxation is asserted. The retained
target screen already rejects 11 or more complete Hub descents, so direct
unchanged-original acquisition cannot realize this target code within that
specific source/caller grammar.

**Scope is essential.** Mere membership of the final packet values in W, or an
all-history normal form `W+L_C`, does not imply the direct-code premises.
Uncharged local copies are forbidden here, not by the general source model.
Actual copied or recoded originals, outside-W transported local forms, changed
routes, and an enlarged global history code are possible escape mechanisms.
They must be constructed and priced. The corollary is not a universal q8 or q10
impossibility theorem. It does not lower-bound the number of copied records.

In particular, the predecessor's static eight-seed/seven-proper-addition basis
cannot be acquired directly by assigning unchanged inputs to incomparable
facets. At least four of its seven independent additions require a mechanism
beyond this direct-acquisition model. This counts independent W directions;
it does not automatically mean four additional physical records or routes.

## 6. Negative control: no automatic terminal-span gate

The absence of local W words below dimension seven does **not** imply that all
past W histories lie in the final packet span. Let a packet at any legal
cochart carry a nonzero W form u, and let an actual receiver carry independent
original y. The two reversible ADDs

`Y <- Y+P;  P <- P+Y`

give

`(P,Y)=(u,y) -> (y,y+u)`.

Both packet/receiver X projections remain in W. The packet's final X
projection is zero, while Y retains u. No original X is recoded and no new
local W form is acquired. This literal two-ADD identity disproves the inference
that W-valued packet histories freeze below facets in the presence of rank-losing
handoffs into ascending Y. Retained owned caches give another possible export.
This example is a local scope counterexample, not a full decoder or invoice.

A q>=15 theorem derived from the **final** packet span would need additional
proved conditions preventing or accounting for such exports. We do not assume
those conditions. Theorem 2 uses the complete historical observation span;
Corollary 5 counts all permitted innovations and survives this particular
export because exporting u creates no new global direction.

## 7. Verification, relationship and next questions

Run from the repository root:

```sh
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/check.py \
  --source research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json \
  --output research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/RESULT.json
```

Expected status: `PASS_SINGULAR_LOCALIZATION_AND_ACQUISITION`. The output
contains the complete 69-word certificate, 61 charts, exact rank witnesses,
matching/overlap controls, the capacity-three witness, an abstract twelve-seed
complement and the terminal-span counterexample. The checker uses explicit
runtime checks, so Python optimization does not remove verification.

This builds on the singular-pivot fitting, coordinate-history localization,
class-history closure and dynamic downset/source-history principles already
published by the programme. It adds the complete real-support localization of
the **different singular code**, arbitrary-block full-rank fitting rigidity,
the exact disjoint-input acquisition capacity, and a sharply scoped physical
consequence. It does not recycle the older class-code localization theorem.

The next constructive question is whether actual reversible original-carrier
recoding can supply and share the missing directions through smaller charts,
with every masked intermediate coefficient and restoration accounted for.
Alternatively, seek a larger history code whose supported local forms permit
a cheaper chronology. The terminal-history counterexample requires any future
trellis or terminal-rank argument to retain Y/cache exports explicitly.

No complete source, strict uniform supplier, precision/compiler theorem,
ownership discharge, outer recursive theorem or new kappa follows. All five
foundational assumptions remain. Credit @CubeJerry, the original native source
authors, the singular-pivot construction and prior localization/cut authors.
Developed by the S014 adversarial worker with substantial OpenAI assistance;
independent review is a separate admission gate.
