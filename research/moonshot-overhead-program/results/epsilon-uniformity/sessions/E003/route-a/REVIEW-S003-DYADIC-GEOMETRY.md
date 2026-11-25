# Independent Route A review of the fixed-radix dyadic geometry

Status: **accepted written geometry/interface**, with the complete local
call constant to be recomputed when composed with a new schedule. This is
independent AI-agent review, not human refereeing or a formal proof build.

Source: S003 `route-b/explicit-dyadic-geometry.md` as read at programme
commit `c65aac1156a46d10c0ef2aa36fd846c7a93518e1`; its OpenAI source pin
is `3344da59991ed94f9ba711217b29c1d760badfa6`. The reviewer read the
complete source note, the original shared endpoint paragraphs, and its
exact replay script, then performed an isolated replay.

## Algebra and reserve-only structure

The hyperbolic completion G=[[B,I],[I,0]] is nondegenerate with the stated
inverse. Its primal vectors x_v=(e+z_v)/2 and y_v=(e-z_v)/2 give exactly
the source Gram block: <z_v,z_w>=2-4k/d yields diagonal 1-k/d and
off-diagonal k/d. The added dual coordinates do not change that block.
Dimension doubles a coarse ambient bound, rather than requiring a minimal
radical quotient; the source endpoint argument needs the Gram identities
and a nondegenerate ambient form, both supplied.

The coordinate complement C_v intersects span(e,z_v) trivially, so its
orthogonal projection is a basis of the pair complement. Equation B2.6
is the correct inverse coordinate rule: subtract the original e and z
coefficients, not bilinear pairings. The distinction is essential for
dual coordinates and was explicitly checked.

For a directed product rectangle, the nonanchor star pivots on its two
sides are disjoint. Its cross vector g has z coefficient -2, independent
of all stars. These give an actual basis of the isotropic difference
space. Replacing the distinguished anchor via B2.9 has pivot1/2 while
the preceding z replacement has pivot-2; their product is -1. Therefore
the complete basis change introduces no odd-prime diagonal unit.

The main shared-endpoint condition is genuinely satisfied. In individual
complement coordinates, the untouched C_R vectors and star vectors stay
unchanged, while g becomes `a+2 sum s` at a source and `-a+2 sum t` at
a destination. Thus the necessary preparation acts on reserve coordinates
alone and is independent of query j. It does not borrow H_j or N_j as
temporary storage. The later lower-triangular per-query adjustment is
therefore the actual source interface, not an unproved simultaneous-basis
assumption.

Every required nontrivial diagonal scale is a power of two. Shear
coefficients may have dyadic denominators; their numerators need not be
units for a shear to be invertible. Hence the fixed address modulus3^f
works for every width f. Basis-column factors must be applied in the
reversed temporal order when interpreted as address maps, as the note
explicitly records. Inverses reverse and invert that list.

## Physical scope and cost qualification

Each earlier-target shear may be implemented by two paid field exchanges
around one legal ordered shear. There are O(D) elementary factors, so the
number of recursive exchanges is O(D) with an absolute constant. Their
reserve-only arrangement preserves endpoint sharing. Current coefficient
magnitudes are small dyadics, so the old numeric-magnitude inflation is
absent, independently of the more general HFS improvement.

The exact coefficient `2^19` in E003's PS4 is tied to the preceding E002
geometry and its concrete invoice. Importing the new geometry requires
either a fresh factor count or writing a fresh absolute `C_geom` in
`Lambda<=C_geom sqrt(m) D(1+lambda)`. The asymptotic profile is unchanged,
but a fixed-exponent numerical admission test must not silently reuse the
old number. This is an integration qualification, not an algebraic flaw.

The source's b>batch-width rule is correctly separated from geometry.
Using radix3 still requires the independently proved multidigit occupied
batch block, with full binary scalar degree included in its row width.
No such packing or complete multiplier follows from this note alone.

## Actual replay

The predecessor script was copied without modification to
`dyadic-geometry-replay/verify_dyadic_geometry.py` and run there, preserving
the source receipt. Its isolated receipt reports:64 Gram-block checks,
200 isotropy pairs,3,104 individual layout basis inversions,3,088 reserve
inverse basis vectors,40 reserve geometric columns,30 modular scaling
checks, and8 detected instances of each adverse sign control. All passed.
Parameters were d=2,q=4,h=3,D=388 with four sources and four destinations.
This is a finite exact arithmetic replay, not a full routing execution or
an asymptotic proof substitute.

Credits: @CubeJerry; S003 Route B geometry and its independently credited
source constructions; pinned OpenAI manuscripts; substantial AI-assisted
E003 independent review. The geometry's authorship remains with its
predecessor record.
