# Eight arbitrary ground rows remain insufficient after the actual six point grants

**Proved by a new native application of the admitted star rank floor. No new
kappa.** The underlying rank theorem is credited to DreamingOfClouds,
CrocSwap/integer-mult-bounds#7114, and the programme's independently reviewed
`bit-saturated-star-rigidity` and `bit-joint-kernel-puncture` packages. This
short package reuses an archived certificate with the current, different
six raw point grants.

## Statement

Let E={1,6,73,75,77,79}, the actual raw point fields in the current fifteen-
output source, and J=all111 minus E. Over every field and at every positive
record width V, the native fitting minimum on J is at least 9V. In
characteristic two it is exactly 9V, because the restricted canonical C9
code supplies the matching upper bound.

Consequently, no choice of eight common width-V **linear** ground fields,
even with arbitrary noncommuting block coefficients and all six raw E
records freely available, can complete all 111 receivers using only their
geometrically permitted raw foreign coordinates. This conclusion does not
prescribe S6, S8, U8, or any particular preload code.

## Archived native certificate and proof

Use the archived `two_points/star` certificate in the pinned predecessor
SCAN.json. Its eight point roles are

    [0,16,17,32,36,38,67,71].

These all avoid E. Delete edge roles in E. The 27 retained native edges have
point degrees

    [6,7,7,7,6,7,7,7].

The literal edges are in SOURCE.json. Each edge role is orthogonal to exactly
its two incident point roots, all point pairs are real-nonorthogonal, and
distinct edges incident to a common point are real-nonorthogonal. Every
retained point and edge role lies in J. The checker verifies these facts
directly using the actual integer roots.

The admitted star rank inequality applies: for a fitting of rank 8V+j,

    sum_a (degree(a)-4) G_a <= 2 |edges| (j-V),

where the star quantities G_a are nonnegative. Since every displayed degree
is at least four, j>=V. Every fitting on J restricts to a fitting on these
35 retained roles, so its rank is at least 9V. This uses the inherited
all-field, all-width block proof, not a scalar computational extrapolation.
The canonical binary restriction to J has rank nine and proves the stated
characteristic-two equality after tensoring by the identity.

Finally, restrict the input records to J by setting all E inputs to zero.
The free raw E fields vanish. Eight common width-V linear fields have rank
at most 8V on J. If all remaining receivers could reconstruct their records
using those fields and their permitted raw side information, their endpoint
equations would factor a J-fitting through those at most 8V common rows.
This contradicts the 9V floor.

The same rank argument permits arbitrary exact decoders of the *linear*
measurements over a field: exact recovery of a linear coordinate from fixed
linear measurements requires that coordinate to belong to their row span,
by the kernel-separation argument. It does not assert a bound for arbitrary
nonlinear common encoders.

## Implication for the continuing construction

Reprogramming the eight principal ground fields can change which outputs
fit and how their source corrections are acquired. It cannot alone make
this particular six-point-grant interface complete. A successful eight-
principal construction must supply additional nonlocal receiver information
through actual histories, singular cells, transported coded fields, or a
different explicitly priced interface. The source may also change its point
grants or number of principal fields; this theorem does not price those
alternatives.

This is not a prohibition on local cache/preload recoding, the current
fifteen literal endpoints, or the full W15+C9 historical span. It identifies
which kind of new information a complete continuation must deliver. It
grants no subsequent global feedback beyond the six listed points; a
changing feedback interface needs its own argument.

## Reproduction

```sh
python3 check.py --repo REPO --source SOURCE.json --out output
```

Expected status: `PASS_ACTUAL_SIX_GRANT_RANK_NINE_PUNCTURE`. The checker pins
the archived certificate and rank-floor document, verifies every real
incidence and incident-edge noncontact, and computes the canonical rank on
all 105 retained roles. Controls corrupt a native edge, put a granted point
into the purported retained frame, and remove enough incident edges to
violate the minimum-degree hypothesis. No search failure is used. **No new
kappa.**
