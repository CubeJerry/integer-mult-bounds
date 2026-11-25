# Independent C review of the two-scale analytic composition

Reviewer: E003 Route C. Result: **accepted conditional transfer**, with
the explicitly stated local executor contracts. This review does not
construct every physical supplier or execute a complete multiplier.
It is independent written AI-assisted review, not human refereeing or
formal verification.

Main document: `../route-b/TWO-SCALE-RECURSION.md`. I read the actual
source tape `interchange.tex`, `walsh.tex`, `permutations.tex` and
`integers.tex` in full at OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6`. I also read the
programme's rational Newton/repair construction, polynomial auxiliary
audit, E002 rational precision note and stated E003 supplier reviews.
I subsequently read `../route-b/OUTER-REDUCTION-TRANSFER.md` in full.
Its O1--O6 source transfer is accepted: it agrees with the independently
derived substitution in Section 5 below and includes the numerical guard.
My separate field-packing review is
`REVIEW-A-BINARY-FIELD-PACKING.md`. Snapshot hashes and an isolated
checker replay are recorded separately.

## 1. The two scales solve different charged recurrences

Write `Phi(y)=y^(2/3)log2(y+2)^(1/3)` and
`Psi(y)=sqrt(y log2(y+2))`. Local profiles are imported as
volume-weighted **completed** finite-template bounds. The interchange
bound includes padding and occupied reserve calls; Walsh includes finite
repair leaves. These are not merely circuit-stage counts.

For interchange, `e^beta/3<=m(e)<=e^beta` beyond a fixed base. Beta is
chosen after the fixed physical polynomial exponent C. The guarded floor
satisfies `e/(8m)<=f<=e/m`, with f>=2. Thus y=log2 e obeys
`y'=(1-beta)y+O(1)`, with root-independent constants. A large fixed base
gives strict multiplicative upper and lower bounds on y'/y.

Normalizing by sqrt(e) cancels the leading sqrt(m) call factor because
f<=e/m. The product of normalized call bills has logarithm at most

    C sum_i Phi(log2 m_i) <= C' sum_i Phi(y_i)
                             <= C'' Phi(y_0).

The last series is geometric in y^(2/3); its logarithmic factor decreases.
The normalized proportional toll is at most
`poly(log u)e^-eta`, eta>0. Successive nonbase y_i have a positive
absolute separation, so the sum of those tolls is bounded. Every product
prefix multiplying a toll is already covered above. This does not
presume that each normalized multiplier is less than one.

Additive setup `2^(C m^C)` is less than `2^(e/2)` eventually, while
every complete active interchange has volume at least `b^(2e)`. It is
absorbed separately **at each node**. No polynomial bound on the total
number of interchange nodes is needed here; large full-rate module row
widths do not invalidate this absorption.

For Walsh, a power-size arity would leave an inadmissible polynomial-m
factor in a toll already paying for interchange. Its smaller rule gives

    z=log2(m-1)=Theta(Phi(log2 a)),  A=Theta(m),
    f=2 floor(a/(2A)),  a/(2A)<=f<=a/A.

Eventually f>=sqrt(a). The logarithmic decrease is z+O(1), and adjacent
logarithmic widths remain within a fixed factor. On that interval,

    Phi(Y)-Phi(Y')
      >= c (Y-Y')Y^(-1/3)log2(Y+2)^(1/3)
      >= c' Psi(z+O(1)).

This telescopes the Walsh call loss. It also pays for m^C, whose
logarithm is O(Phi(Y)). Interchange costs at most
`sqrt(a)2^(O(Phi(Y)))`; dividing the local toll by sqrt(a) leaves the
same scale. Prefix products and the polynomial number of levels prove W9.

The width remainder contains fewer than 2A bits. Directly transforming
them takes O(m) whole-volume butterfly passes, included in the genuine
polynomial-m local bill. Their completed maps are unitary. These bits
have not been discarded as free data.

## 2. Leading rows and changing batch widths

The width chain depends only on the root, so all W_i are computable before
execution. For B=product W_i, the bounds W_i<=m_i^C and
f_i<=a_i/A_i with A_i>=m_i give

    sum_i log2 m_i <=log2 a_0,  B<=a_0^C.

The source selected-width condition supplies at least `2^(k/2)` leading
spectator rows eventually. Padding this **one** leading range to a
multiple of B costs less than two. At each child its leading count is
exactly divisible by the tail product. A separate factor-two padding
loss is not accumulated at every level.

All other coordinates remain complete spectators. Workspace and
initialized zeros are not extra arbitrary independent inputs. The
precise internal finite-repair row interface remains a P-W obligation;
given that interface, the product argument works for varying W_i.

Field changes apply only to completed spatial permutations. Finite
spectral repair children retain their parent's field and template.
Within this scope, extension degrees cancel from full-rate encoded
volume and do not multiply down the recursion.

## 3. Node count and additive preparation

At depth d the product of local branch majorants is at most
`product_(i<d)m_i^C<=a_0^C`. There are O(log a_0) levels, so the Walsh
recursion has polynomially many nodes and whole-array events. Finite
repair occurrences are already in each local template's count.

The largest arity is

    m_max=2^(O(Phi(log k)))=k^o(1).

Thus even the deliberately loose total setup bound satisfies

    poly(k) 2^(C m_max^C) (1+k)^(m_max^C)
      =2^(k^o(1))=o(2^k).

Both m_max^C and its product with log k are k^o(1). This does not
reclassify a payload scan as additive work: scanning a `2^(m^C)` table
for every input record violates P-W. Setup visited cells are bounded by
the displayed time and eventually fit the complete array volume.

## 4. Every numerical cut is bounded

The local gain contract must cover every input-to-intermediate and
intermediate-error-to-later-array map, with completed children treated
as unitaries. Merely bounding the completed target would not suffice.
Multiplying elementary norms using the local instruction count, row
dimensions and coefficient heights gives the required bound after
enlarging one fixed exponent. E002 explicitly includes partial sums and
the maximum small spectral block; spectral cardinality is not a norm
multiplier. B made this intended cut-to-cut contract explicit on review.

For an error created in one child and observed in another, use the two
paths through their first common ancestor. Completed intervening
children are unitaries. The total gain logarithm is bounded by

    2 sum_i m_i^C <= O(log k)m_max^C = k^o(1).

There are polynomially many array arithmetic events. Rounding an entire
array incurs the actual sqrt(N) Euclidean factor; coefficient errors
also incur the input norm. For allowed input norm `2^(B k)`, these
factors and the gain are bounded by `2^((B+O(1))k)` eventually. A fixed
fractional width p=C_0 k therefore gives error `2^(-D k)` and closes
the O(k)-bit integer-part bootstrap. Exact rational coefficients may
instead use E002's signed long-times-short primitive, whose only
numerical fault is final rounding; their bit heights remain charged.

I requested an explicit numerical admission guard. B added
`k>=m_max^K_2` for a fixed larger exponent, or a computed upper
gain/event budget, with exact fallback before selecting the format.
The elementary `log2(k+2)<=3sqrt(k)` argument proves sufficiency for
variable templates as well. It holds eventually since m_max=k^o(1).
This is necessary for an all-length machine: time and space caps alone
cannot detect an inaccurate rounded answer. It changes no asymptotic.

## 5. Outer source and common-space assembly

In the source packed-XOR proof, rho appears only through its interchange
calls. Offsets, exceptional-slot tests, destination keys and sparse sorts
have fixed polynomial costs in k. Substituting the monotone bound

    U(u)=sqrt(u)2^(C Phi(log2(u+2)))

therefore gives cost `V(1+U(L))poly(log k)+poly(k)`. The same guards
and exceptional fractions work. Position permutations use a bounded
number of these routines, and controlled blocks use polylogarithmically
many, yielding `V U(k)poly(log k)+poly(k)`. They move numerical records
exactly and are independent of their contents.

The unchanged integer reduction has Nk=Theta(n), k=Theta(log n),
O(log k) unitary Fourier layers and fixed polynomial preparation.
Its fixed norm/error exponents are supplied by Section 4. Completed
layers propagate previous errors without norm amplification. The
coordinatewise product, sqrt(S) scaling and carry pass keep their
original estimates. No growing parameter is substituted into a
fixed-rho constant. This checks the analytic P-O implication against
the actual source; the rational Walsh branch stays rational.

The physical space contracts supply an absolute number of payload
copies, geometric parking, descriptor-only full-volume descents,
stripped tags and marked-region reuse. Their first composition gives
`C n(1+log2 L(n))^C` visited cells, which is correctly not called O(n).
Choose the displayed power-of-two chunk count r and u=ceil(n/r).
The core then fits a fixed fraction of n eventually; all regions are
reused between calls.

There are r^2 products, with total product lengths `r^2 u=O(rn)`.
For assembly, fix one first-input chunk, process second-input chunks in
order, and combine overlapping products with carries into one shifted
row. Add that row to the output in O(n) work. Repeating for r rows costs
O(nr), including movement and returns. It does not traverse the whole
output separately for each of r^2 products.

The extra r is polynomial in `1+log2 L(n)` and is absorbed into the
displayed exponential profile. Shape, numerical, time and marked-space
guards have exact fallbacks; eventual admission gives the all-length
asymptotic. Marked region reuse bounds **all visited** cells, including
after fallback, rather than only simultaneously live data.

## 6. Reproduction and admission boundary

Copied the author's checker unchanged to `review-b-replay/` and ran it
there. It passed 2,610 exact roots, 4,110 interchange nodes across 108
chains, 1,063 Walsh nodes across 117 chains, 7,810 padding candidates,
and its profile/radix and negative controls. The receipt is separate
from the author's original. Finite checks support integer bookkeeping;
the unbounded estimates are justified by the arguments above.

No analytic contradiction was found. The conditional theorem is
accepted after the explicit numerical and cut-to-cut clarifications.
A complete new fixed-machine theorem additionally needs the separately
audited P-I/P-W suppliers: paid child volumes, numerical row alignment,
metadata removal, local movement and uniform visited-space schedules.
This review does not relabel those premises as conclusions or claim
complete multiplier execution.

Concurrent programme status is separate: E002 independently admitted the
same two-thirds scale during this review. The review establishes the
soundness of B's stated conditional argument and does not claim an E003
programme-best improvement or priority for that scale.

Credit: @CubeJerry, OpenAI and cited predecessors, E001/E002/S003
components, E003 A's physical suppliers, E003 B's two-scale proof,
and AI-assisted independent review.
