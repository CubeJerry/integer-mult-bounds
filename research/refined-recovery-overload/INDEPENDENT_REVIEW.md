# Independent review of the lower bound and integer attainment

The construction worker separately checked the lower-bound worker's
`PROOF.md` after deriving and implementing the actual integer lifts.
No unresolved mathematical objection was found in the weighted relation
reduction, the 30-type pointwise domination, the all-`y>=4` AM-GM exclusion,
the allocation argument, the source-lattice realization, or the distinction
between zero-fiber cardinality and a worst-output packed tag. This is an
AI-assisted mathematical review, not independent human or proof-kernel
acceptance.

The source-specific integer construction and all-output check are in
`LIFT_PROOF.md` and `independent_attainment.py`. They do not import the
primary lower-bound code. In addition, the following independent reduction
avoids both its 816-multiset enumeration and its greedy allocator.

## Eight closed-form classes replace the small enumeration

Use the primary proof's justified relaxation

    sum_(u!=0) a^(x_u) d^(o_u),
    a=51,008,161/50,979,600, d=50,983,170/50,979,600,
    sum_u x_u=27-y.

For `0<=y<=3`, the nonzero linear functionals have the following complete
classification by repetition and rank. Entries in the last column count
nonzero vectors `u` having `o_u=0,1,...,y`.

| y | Class | Incidence histogram |
|---|---|---|
| 0 | Empty list | (15) |
| 1 | One nonzero functional | (7,8) |
| 2 | Two equal | (7,0,8) |
| 2 | Two distinct | (3,8,4) |
| 3 | All equal | (7,0,0,8) |
| 3 | Two equal, one different | (3,4,4,4) |
| 3 | Three distinct of rank two | (3,0,12,0) |
| 3 | Three independent | (1,6,6,2) |

Completeness is elementary over F2. Distinct nonzero pairs are independent.
Three distinct forms are either independent or their sum is zero. A rank-r
map has `2^(4-r)` preimages of each value; delete the zero vector from the
zero-value fiber. In the dependent distinct triple, every nonzero two-bit
value gives exactly two ones. These observations give every entry in the
table without enumerating a choice of forms.

Exact rational arithmetic gives `1<d` and `d^3<a`. At a minimum of the
allocation problem every `x_u` is one or two. If one were zero, because
`27-y>=24`, another would be at least two; transferring one unit to the
zero bin strictly lowers the cost since its weight is at most `d^3<a`.
Once all bins are positive, an entry at least three forces another entry
equal to one because `27-y<30`. Transferring a unit again strictly lowers
the cost, using the same inequality. Thus each bin gets one unit, and
exactly `12-y` bins get a second. The latter go to the smallest incidence
values `o_u`, since their added costs are `a(a-1)d^(o_u)`.

`independent_histograms.py` substitutes this closed formula into the eight
table rows. It uses `Fraction` only and imports no other scientific module.
The `y=0` row is exactly `3a+12a^2`; every positive-y row is strictly larger.
It separately verifies `d^8>a` and

    15^15 a^23 d^32 > (3a+12a^2)^15,

which are the independent rational forms of the universal AM-GM tail checks.
Therefore this eight-class calculation independently certifies the same
finite minimization as the primary enumeration. It does not replace the
quantified relation-space and domination proofs.

## Execution and scope

Both normal and optimized executions of `independent_attainment.py` agree
byte for byte. They check all 3,024 columns of the 27 actual integer frames,
all source-mode images, the four-dimensional relation, 121 complete
27-stage forward/reconstruction examples and seven semantic controls. The
largest absolute entry in any cumulative integer frame is 57. The ordered
frame-operation receipt has SHA-256
`617ec2729e4abfab572fae6d304eaa62c5691834c75fe489cb977d1d812966ef`.

Both normal and optimized eight-histogram executions agree. This review
claims no physical runtime, memory saving, new κ, whole multiplication
theorem, or selected-assumption discharge. Exact cardinality of the largest
fiber of the constructed map remains open. The exact zero-fiber optimum
and 696-bit fixed-tag optimum are distinct established statements.

Prepared for @CubeJerry with substantial OpenAI Codex assistance in
independent construction, verification and review. The source and prior
mechanisms retain the #5444/#6327/#6660 and underlying lineage credit.
Apache-2.0.
