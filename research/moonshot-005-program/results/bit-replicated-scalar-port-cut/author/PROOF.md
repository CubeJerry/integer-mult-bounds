# Identical scalar stripes cannot complete the balanced native source

## Precisely excluded construction class

Use the S022 balanced routes and factor, with `b=5760r` field slots per
native role, for any positive integer r and any finite field F of
characteristic two. Put `p=360r`, so `b=16p`, and each H-D port has
`24r=p/15` field symbols. Every source bank is decomposed in its actual
input coordinates as `X_j=(X_(j,1),...,X_(j,16))`, with each component in
`F^p`.

At every ordinary donor-plane flag assume its source quotient, up to an
arbitrary bijective relabelling of the bundle, has the form

    f_(j,H)(X_j) = sum_(s=1)^16 c_(j,H,s) X_(j,s),   c_(j,H,s) in F.

The scalar row may be completely different at every donor and every
plane. This includes independently selected scalar source bases at each
donor; it does not require a shared kernel, a common MDS dictionary or
common scalar parameters. The same scalar row is repeated on the p
coordinates of the bundle. The eleven singleton source maps are allowed
to be arbitrary functions of their full `540r`-symbol emission.

**Theorem.** No complete deterministic code in this class, even with
arbitrary nonlinear downstream operations and all same-chart stationary
caches, realizes every original native target on the paid balanced routes.
The required plane-output information has dimension at least `587520r`,
whereas all actual plane outputs together have cardinality at most
`|F|^(439284r)`.

This is not an exclusion of arbitrary block/array quotient maps, scalar
rows that vary between stripes, arbitrary full-bank donor gauges, changed
port capacities, or new paid paths. It specifically excludes the simple
identical-stripe extension of a scalar donor-dependent construction.
The four-donor F4 word is outside the theorem because it pays private
plane-to-receiver ports. No new kappa is asserted.

## A tight receiver fixes its whole plane tuple

For each ordinary H let J_H be its native donors, and let I_H be the native
receivers i seeing H for which every `(j,i)`, `j in J_H`, has the tight
5760r-symbol source cut. The balanced quotient proof shows how to
neutralize the canonical bank, and its exact geometry check identifies
these tight pairs.

At i, each donor j's sixteen visible quotient rows form an invertible
16-by-16 scalar matrix. Its varying fibre when the other fifteen bundles
are fixed is a scalar line `F v_(j,i,H)` tensored with `F^p`. Plane gluing
requires these fibres to agree at every donor on H. Thus they have one
common line `F v_(i,H)`. The desired varying sum from H, expressed in its
quotient inputs `Z_j=f_(j,H)(X_j)`, is

    v_(i,H) * sum_(j in J_H) Z_j / c_(j,H)(v_(i,H)).

Every denominator is nonzero. In the direct sum of the quotient input
spaces its p-dimensional target row space therefore is

    W_(i,H) = F rho_(i,H) tensor F^p,

where the components of rho are the displayed nonzero scalar reciprocals.
Receiver i sees exactly fifteen of H's forty-five D4 ports, with total
capacity p. Fixing all other source-plane data, their joint tuple must
distinguish all `|F|^p` possible values of this H sum. Capacity equality
therefore makes the tuple a bijective relabelling of the target. In
particular every individual visible port has its full `|F|^(p/15)` range
and is a function of that target alone.

These conclusions hold for deterministic nonlinear port encoders. If a
function factors through two linear maps, it is invariant under both
kernels and hence under their sum. The dual of that sum is the
intersection of the two target row spaces.

## A shared port forces equality of scalar target rows

Two spaces `F rho tensor F^p` and `F sigma tensor F^p` have zero
intersection unless rho and sigma are proportional, in which case they
are equal. If one actual D4 port is visible to two receivers i,k in I_H,
that port is a function of both target maps. A zero intersection would
make it constant, contradicting its full positive range. Hence
`W_(i,H)=W_(k,H)`.

Make a graph on I_H, joining receivers when they share at least one of
the actual forty-five H-D ports. The exact native census finds this graph
connected for **every one of the 1,108 ordinary planes**. Consequently all
target row spaces at those receivers agree. Every port seen by at least
one such receiver factors through this same p-dimensional aggregate.
Taken together, all covered ports therefore carry at most p dimensions of
information, regardless of their number and of downstream recoding.

Let u_H count the ports seen by no receiver in I_H. Grant every such port
its complete capacity `p/15`. The full H output is then bounded by

    p + (p/15) u_H.

This bound includes all early and late outputs, all branch choices and
all stationary caches. The code cannot use a port's existing early value
and later value as two independent free messages: the forty-five ports
already count the actual 24r early/late physical records per H-D flag.

## Exact total information and contradiction

The independent geometric census is:

| Ordinary planes | Uncovered ports per plane |
| ---: | ---: |
| 834 | 0 |
| 260 | 5 |
| 4 | 9 |
| 10 | 10 |

The sum is 1,436 uncovered ports. Give each singleton H its entire
`540r`-symbol source alphabet, rather than imposing any scalar condition.
The empty H carries no varying source input. Across every H the complete
output alphabet therefore has size at most

    |F|^[1108*360r + 1436*24r + 11*540r]
    = |F|^(439284r).

Now set every original Y to zero and restrict X to the kernel of the
complete canonical row map. The canonical rank is nine per b-coordinate
bank, so this input space has dimension `(111-9)b=587520r` over F. The
completed native output would be X itself, and hence must distinguish
every input in this subspace. All canonical descents are identically
zero on it. All remaining routes to the receivers pass through the
counted H outputs, whose smaller alphabet cannot distinguish those
inputs. This is a cardinality contradiction, with deficit `148236r`.

Using this canonical-zero slice avoids assuming a particular fixed
linear preload normal form. It does not grant unrestricted extra access
to raw Hub X: such an additional transmission is outside the pinned
route schedule and would need its own paid path.

## What a constructive successor must change

The donor-dependent tetrahedral word shows that asymmetric source kernels
can align several receivers exactly. Its two outputs at each pair plane
are independent scalar functions, transported privately. Repeating that
scalar idea identically over p coordinates would leave distinct plane
target lines with zero intersection at shared native ports. The present
proof identifies why that direct extension fails.

An array construction can instead have p-dimensional target spaces whose
intersections have intermediate dimensions. It must supply at least
`p/15` independent common dimensions for each actual shared D4 port and
the full joint rank inequalities for every receiver's fifteen-port set.
Those array intersections, their compatible source fibres at every
native receiver, and chronological physical realization remain open.

Credit @CubeJerry, the native geometry, S022 tight-plane rank test,
balanced causal atlas and source quotient arguments; S023 Worker A and
substantial OpenAI assistance. The proof uses exact source incidence,
linear algebra and cardinality, not failure of a numerical search.
