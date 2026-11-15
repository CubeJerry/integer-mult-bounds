# Exact chartwise criterion for an early canonical query basis

**Proved linear interface theorem with an explicit source realization under stated acquisition rules. No new κ.** This characterizes the direct-query mechanism used in the one-, two- and three-receiver sources. Full held-coordinate surjectivity is sufficient but not necessary.

## 1. Source cut and query interface

Work over any field K. At a fixed cut, actual current original-input records form an invertible coordinate basis with row space H direct-sum D. Actual H records are cocharted at Hub. Held current rows partition by actual geometric chart, giving D=direct-sum_a D_a; geometric aliases are identified first. Every D_a basis record remains at its chart C_a until queries finish. The desired terminal code is C contained in H direct-sum D, dimension c.

An admitted principal field is initialized at Hub and formed from actual H records. It either descends directly to ground or visits exactly one C_a, reads a linear combination of actual D_a records there, and then descends to ground. No second query chart, additional retained side information, movement of the held originals, noncanonical terminal fields or earlier receiver copy is granted. Exactly c terminal fields must form a basis of C. All linear maps must have an admitted, charged implementation; for the present fixed binary words this is the emitted ADD circuit. Source retention and all original/owner route directions are premises.

Let R=pi_D(C), where pi_D is coordinate projection along H.

## 2. Necessary and sufficient condition

The specified c-field interface exists if and only if

    R = sum_a (R intersect D_a).                        (1)

The sum is direct, so equivalently dim R=sum_a dim(R intersect D_a).

Necessity: each terminal field h+d belongs to C and has d supported in a single D_a, or d=0. Thus its D projection belongs to R intersect D_a. The terminal fields span C, so their projections span R, proving(1).

Sufficiency: take a basis of each R intersect D_a and lift every vector d through C to a vector h+d. Append a basis of C intersect H. There are dim R+dim(C intersect H)=c selected rows. Their projections prove independence modulo H, then the Hub-only basis proves full independence. Form h from actual Hub rows and query d from the held records at the selected chart. Every source stays until all necessary reads finish. The resulting fields are a basis of C at ground.

For ambient dimension m and chart dimension d_a, a field assigned to chart a pays[m−d_a]+[d_a]; a Hub-only field pays[m]. There is one actual owner per code basis row, and all seeding/query ADDs and dirty retirements are charged. The theorem supplies neither cheap acquisition of D_a nor a terminal/history-rank identification.

Full projection R=D automatically satisfies(1), recovering the unit-coordinate query basis. Surjectivity is not necessary: if two held records share one chart, the span of their sum satisfies(1). At two distinct charts that same diagonal projection fails(1). Rank alone is insufficient.

## 3. Full held native blocks require independent evaluations

Let E be a scalar code with generator column v_j at native role j. Fix a set A of roles with every v_j nonzero, and take b physically separate value copies. Suppose that for each j in A there are b held current coordinates whose inverse columns are supported on original native block j and form an invertible b-by-b basis there. The current held rows themselves may contain other native inputs through aggregation; the inverse-column hypothesis is what controls code projection. Each actual query chart contains coordinates from at most one native block; it may contain any subset of that block's coordinates. No chart mixes different native source blocks.

For terminal code E tensor K^b, criterion(1) holds if and only if the columns {v_j:j in A} are linearly independent.

For necessity, group the finer chart partition by native block. Condition(1) implies that the projected code is a sum of codewords individually supported on native blocks. A nonzero projected codeword supported only at j exists exactly when v_j is outside the span of all other columns: a scalar linear functional must annihilate all the other columns but not v_j. Tensoring with K^b and applying the invertible within-block map preserves this condition; the block-supported space has dimension b when it holds and zero otherwise.

If the nonzero columns are dependent, some v_j belongs to the span of the others. The projected code has nonzero values in block j, since v_j is nonzero, but has no nonzero word supported only in that block. It cannot decompose into block-supported subspaces, contradicting(1). Thus the columns are independent. Conversely independence makes the held projection full, so every actual chart partition satisfies(1).

For the pinned rank9 scalar canonical code, the restricted mechanism therefore cannot hold more than nine full native blocks at source-separated query charts. The current four-copy private-MDS layout uses two distinct full held native blocks per completed receiver. Private charts for distinct receiver facets are distinct: a shared dimension6 chart would be their common facet intersection and could not contain their private source lines. Under these exact unchanged assumptions, more than four receiver groups would require more than nine independent native evaluation columns. This is a limitation of that query layout, not an impossibility theorem for five receivers or a complete supplier.

The actual two-port source has four held native blocks of independent evaluation and projection rank16. The actual three-port A2 source has six such blocks and projection rank24. They satisfy the criterion; their explicit words supply the costs and source access.

## 4. Scope and constructive use

This theorem concerns one fixed, already acquired cut and precisely the chosen canonical terminal space. Multiple query charts, moving held originals together, additional actual caches, extra noncanonical terminal fields, a different desired code, earlier receiver interactions or another source transformation change its premises. They remain open mechanisms.

The earlier common-intersection patch is a concrete example: copying held rows to one shared lower chart changes the available chart groups and can repair(1), with its actual extra owners and routes paid. A larger simultaneous source can compute R and its chart-local intersections before emitting a word. A positive decomposition gives the exact query basis; a failure identifies a missing source-sharing or route obligation. Neither outcome alone determines a complete multiplication bound. All foundational assumptions and κ≥0.005 remain unresolved.

Credit @CubeJerry and the canonical/finite-record source predecessors; the direct-query mechanism developed in the programme; Worker C's exact characterization and full-block corollary. Developed with OpenAI assistance. Finite controls support, and do not replace, the written all-field proof.
