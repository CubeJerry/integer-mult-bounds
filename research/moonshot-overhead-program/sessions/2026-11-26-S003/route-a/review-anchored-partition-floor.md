# Independent review of the anchored placement floor

Disposition: **accepted in its stated retained-placement and declared-guard
scope**. A read the complete lead note `anchored-partition-floor.md` and
its checker. This is an elementary narrower companion to the concurrently
reported E002 noncanonical incidence barrier, not a claim to strengthen
that separate result. I have not re-proved the E002 theorem in this review.

## Mathematical checks

For a rectangle contained in the all-coordinates-unequal relation, the
two coordinate projections are disjoint at every position. Correlation
within one side cannot invalidate the upper bound by the product of its
projection sizes. Consequently each rectangle area is at most
`(q/2)^(2k)`. Coverage gives the lower edge count even with overlaps.
Applying Cauchy--Schwarz after extracting the square root of the area
gives exactly AP1, with `rho=2(q-1)/q`. No exact-partition assumption is
used in AP1 and none should be inferred from it.

For anchored inner cells I independently recomputed the normalization:

    M q^(d-1) / q^h
      = binom(h,d) q^(h-d) q(q-1) q^(d-1) / q^h
      = binom(h,d)(q-1).

If the left/right incidence totals in cell c are L_c,R_c, AP1 gives
`sqrt(L_c R_c)>=q^(d-1)rho^(d-1)`. Cauchy--Schwarz has the needed
direction: `sqrt((sum L_c)(sum R_c))>=sum sqrt(L_c R_c)`. Thus cell
partitions may vary and be asymmetric; balancing them is not a hidden
premise of AP2.

The outer average factors because the construction retains distinct
changed-position cells and takes actual Cartesian products of the d
inner rectangle families. For one position set the unchanged outer
coordinates contribute `|U|^(h-d)` choices and the d changed coordinates
contribute `(sum |A_r|)^d` to the source incidence sum. Dividing by
`|U|^h` gives `(alpha_L^0)^d`, then summing position sets gives AP3's
factor `binom(h,d)`. The analogous destination expression is exact.
For independently chosen inner families the product of their geometric
mean lower bounds gives the same lower estimate. A rectangle family that
merges different anchor/position cells is explicitly outside this step.

The binomial lower bound is valid for every integer d>=2, not only powers
of two. With q>=2, it yields `log(1+lambda)>=d^2-1>=3d^2/4`. The declared
rank guard implies `d^2 log q>=x`, and the specified star realization
therefore has `log D>=h log q>=x/d`. Finally

    max(x/d,3d^2/4)^3 >= (x/d)^2(3d^2/4)=3x^2/4.

This checks the constant and inversion in AP6. The conclusion applies to
the explicit D and sufficient guard in AP5. The proof does not promote
that sufficient guard into a necessary rank condition for other families.

## Independent replay

Copied the supplied checker into this route's
`anchored-partition-review-replay/` and executed the copy with Python.
It passed 22 cover cases, 10,564 explicitly covered edges, 768 correlated
nonproduct rectangle sides, 20 anchored profiles and 6,144 parameter
profiles. Its four negative controls rejected an omitted rectangle and
overlapping coordinate projections, exhibited a far rectangle crossing
the retained cells, and showed that removing the rank guard defeats the
x-dependent conclusion. These controls test the important scope seams.

Source checker SHA-256:
`c696874da979be25c10ada3e2073d5c0d40f117e90cc6029b810ae4762ab407e`.
The isolated JSON remains beside the copied checker. These finite checks
supplement the proof; they establish neither JR nor a machine lower bound.

No correction requested. The separately reported E002 extension should
receive explicit convergence credit when this narrower AP result is
described in the session summary.
