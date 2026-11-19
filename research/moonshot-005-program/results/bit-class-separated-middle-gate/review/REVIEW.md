# Independent review of the fixed-class middle-cut theorem

**Verdict: accept in its stated exact-proper-sum representation.** This is
a coefficient-independent obstruction, stronger than the old frozen
triangle coefficient census. It is not an obstruction to arbitrary
proper transfers B, arbitrary donor-dependent source gauges, a changed
class labeling, or paid additional information.

## Argument checked

For a fixed donor and source class, the selected receiver sees sixteen
quotients of3rho coordinates and must recover48rho independent coordinates.
The source stack is therefore invertible. A local H projection on any one
of these quotients is also invertible: otherwise a lost coordinate of
that quotient cannot be reconstructed from the other independent quotient
coordinates. This inference uses the actual no-extra-information premise.

Across all active donors, those quotient coordinates are independent.
Every H output tuple is surjective because at least one active donor has
an invertible local contribution. Different H tuples use disjoint quotient
coordinates, so their product is surjective. This remains true when several
donors share H; those shared sums reduce the number of source coordinates,
not the range of the port tuple. Consequently a successful decoder from
the complete boundary is unique, and it is linear. Allowing arbitrary
nonlinear downstream maps does not change that function.

At a fixed D, one donor's four actual port columns are part of an invertible
source-coordinate basis. They are independent, and their output class
dimensions are exactly rho times the port count profile. The complete
D contribution contains each donor's span, hence its class-c image has
dimension at least the largest of those class-c dimensions. Distinct
output classes are direct sums. This proves the claimed lower bound
`rho*sum_c max_j n_c(j,D)`.

There are exactly four counted D-to-K flags that can reach the receiver.
Fixing all other independent boundary coordinates leaves the chosen D
contribution freely variable; it must be distinguished by an alphabet
of size at most |F|^(4rho). This proves the lower bound cannot exceed4rho.
The argument accounts for caches only through their actual outgoing
carriers. It does not give early Hub closures or return banks a free path.

If count vectors all sum to four, their coordinatewise-max sum is four
if and only if every vector equals that maximum. Thus profile equality
is necessary. It is not sufficient, because equal-dimensional class
subspaces can still have a larger combined span.

## Separate finite verification

The review checker imports no author code. It authenticates the two frozen
geometry/partition inputs, reconstructs all signed-root orthogonality,
reconstructs D perpendicular charts without using the supplied dual labels,
checks the rational ranks of all1,120 A2 and3,150 D4 charts, and rebuilds
the five classes from their actual H-to-D incidences.

It checks three visible ports in every class, four H ports through each
donor at a D, all6,470 foreign and6,110 tight source pairs, and exactly four
eligible outgoing K flags at every native receiver/D pair. It then forms
profiles by accumulating the actual contained H incidences, in a different
loop order from the author checker. Every one of34,965 cuts is compared
with the author's published profile, lower bound and outgoing flag set.

The reconstructed global histogram is:

| Lower bound per stripe | Number of cuts |
| ---: | ---: |
|4|540|
|5|98|
|6|1758|
|7|7337|
|8|8282|
|9|9394|
|10|7081|
|11|475|

Thus34,425 cuts fail the four-symbol capacity. The triangle contains156
multi-donor cuts, of which151 fail. All39 at receiver10 have lower bound6.
At D81, donors29/36 have profiles `(0,2,0,2,0)` and `(0,2,0,0,2)`; the
four actual right planes are424,605,674,916. Their bound6rho is less than
the frozen source's7rho but applies to every coefficient choice in the
specified source class representation.

A separate alphabet control exhibits16 distinct target values across a
two-bit transcript cut. A different equal-profile example has combined
span dimension4 while each source span has dimension2. An explicit donor
coordinate permutation aligns this latter example, confirming that changed
donor gauges lie outside the fixed-class conclusion rather than being
silently ruled out.

Reproduction:

    python3 -B check.py --repo REPOSITORY --author AUTHOR_PACKAGE --out OUTPUT

Expected marker: `PASS_INDEPENDENT_NATIVE_CLASS_GATE_REVIEW`. Source and
reviewed-author hashes are recorded in the output. This is independent
mathematical review and a separate finite implementation, not human or
formal-kernel verification. No new kappa, MOVE tariff, global repair-rank
bound, or foundational discharge follows.

Reviewed by S027 Worker C with substantial OpenAI assistance. Credit
@CubeJerry, the retained source and port-atlas authors, and Worker B for
the theorem and author certificate.
