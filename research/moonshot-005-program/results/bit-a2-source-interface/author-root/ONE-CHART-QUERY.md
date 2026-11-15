# Exact separability criterion for one-chart canonical source queries

**Proved algebraic/physical interface lemma, independent review pending.**

Let an actual invertible source cut give a direct sum H⊕D, where H consists
of current Hub original rows and D=⊕_(c in C)D_c consists of independently
held original rows at pairwise distinct dimension-six charts. Let K⊆H⊕D
be the desired final canonical code. Write P=π_D(K), P_c=π_(D_c)(P).
Assume held rows stay at those charts until the canonical source completes.
A source field starts from an arbitrary charged linear combination of H,
descends, reads an arbitrary charged linear combination at at most one held
chart, then reaches ground. Every completed field must lie in K, and the
completed fields must span K. The allowed linear operations must themselves
be explicitly implementable and paid in any machine realization.

Such a family exists algebraically, and geometrically whenever the described
Hub-to-chart-to-ground paths are available, if and only if

    P = direct-sum_c (P intersect D_c),

or equivalently

    Delta = sum_c dim(P_c) − dim(P) = 0.

Necessity: each field's held projection lies in P∩D_c for one c, or is zero.
Their span must be P. Distinct D_c sum directly, so P is their direct sum.
Then each projected marginal equals P∩D_c. Conversely, choose bases of these
intersections and lift each basis vector through K. The Hub part is available
in H and its held part at one actual chart. Add a basis of K∩H. These form a
basis of K by projection and rank-nullity and provide the stated queries.
Equivalence with Delta0 follows because P embeds in ⊕P_c; equality of their
dimensions makes that embedding onto, which is precisely separability.

There is no claim that rank-nullity alone provides a physical source: the
actual cut, retained originals, chart paths and operation implementation are
premises. Since equal-dimensional distinct charts are incomparable, a
monotonically descending field cannot visit two of these charts. Extra
redundant fields whose final values still belong to K do not repair Delta>0.
Moving held values to a common lower chart or changing their trajectories is
a different and potentially useful source interface with additional costs.

## Consequence for the current private-pivot recipe

Suppose q receiver groups use disjoint private source roles, with four proper
charts per receiver and two encoded binary pivot records at each chart. All
4q charts are distinct. The recipe therefore holds h=8q binary bank records.
Assume, as in the current construction, that each pivot inverse column is
supported on one native root and the pivot's local encoder is invertible.
For the canonical four-copy code K of dimension36, projection onto every
individual two-record chart block has rank two: scalar evaluation at the
pivot root is nonzero (K_j(j)=1), and its two selected inverse-encoder columns
are independent. Hence sum_c dim(P_c)=8q while dim(P)≤36.

At q≥5, Delta≥8q−36≥4. A canonical-only, one-held-chart-per-field acquisition
cannot span K in this recipe, even with arbitrarily many redundant canonical
fields. This is an exact interface obstruction, not a lower bound on arbitrary
five-receiver constructions. Shared/coincident charts, reusing pivots across
receivers, noncanonical helper histories, common-chart transport, changed
encoders or a different source can remove its premises and must be costed.

At q2/q3 the current actual sources have held projection ranks16/24 and
Delta0, as their exact unit-query bases demonstrate. The lemma explains both
the successful adaptation and the first obligatory structural change when
attempting to extend this particular disjoint private-pivot recipe.

Credit @CubeJerry, the direct-query basis and source-locality predecessors,
and root's separability interface theorem, with OpenAI assistance. No new κ.
