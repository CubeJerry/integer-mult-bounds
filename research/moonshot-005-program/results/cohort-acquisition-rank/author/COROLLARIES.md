# Total incidence and the transpose test

Assume the square-cohort theorem's exact hypotheses and rank(I-UP)<=qV, q>0.
Its order expectation gives sum_j1/(s_j+1)<=q. Cauchy--Schwarz over these
positive rational counts gives

    n^2 <= (n+sum_j s_j) sum_j1/(s_j+1),

and hence

    sum_j s_j >= ceil(n^2/q-n).                         (C1)

For n=111 and q=8,9,10, the lower bounds are respectively1430,1258,1122.
This is an aggregate incidence requirement; it does not say every row has
the same support. It applies to actual input coefficient supports, not to a
count of formal names or a list of geometric containments.

There is a useful separate transpose application. Suppose I=G+L, rankG<=qV,
L has zero diagonal cohort blocks, and input block-column j of L has nonzero
rows in s_j other target cohorts. Apply the main theorem to

    I-L^T = G^T,    U'=I,    P'=L^T.

The same order and aggregate bounds apply to these COLUMN support counts.
In particular, if every independent input affects only one foreign cohort
through local operations, rankG>=V ceil(n/2).

A physical sufficient premise for that column restriction is: every original
current-a record stays pure, visits at most one receiver cohort, and no
subsequent local history crosses to another receiver cohort. This excludes
one-stop pure-source completion by eight fixed global modes, regardless of
which actual collector charts are chosen: n104 requires at least52 modes.
For n104,q8, (C1) requires at least1248 actual input-to-cohort incidences.
The sharper56 gate for the parity geometry comes from optimizing each of
its disjoint half pairs, not from rounding this general52 bound.

An original-X encoder can spread one input across several traveling records.
In that case record visits are not the input-column support counts s_j.
Similarly, a changed returning packet may increase the actual global history
rank beyond qV. Neither escape is excluded by this corollary. Both require a
real chronological word and their complete price. These statements are
necessary structural screens, not a new supplier or multiplication theorem.
