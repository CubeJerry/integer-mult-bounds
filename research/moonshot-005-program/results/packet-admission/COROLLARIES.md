# Two useful exact consequences of the packet criterion

These are algebraic corollaries of `PROOF.md`, under the same physical interface. They do not assert that their matrices have been realized in the source.

## Injective debt prevents packet compression

If row(J)=row(D), then

    row([J;E]) = row([D;R]).

Indeed E=R-BT^{-1}D+AVJ differs from R by rows already in row(D)=row(J). The equality follows in both directions. A sufficient condition is that Z_o is injective on the control-increment image im(T^{-1}D): J and D then have the same kernel and hence row space. If the desired receiver difference map R has full column rank m, the minimum packet count is exactly m. A control family with independent off-hub debt for every independent signal cannot compress this initial-correction interface, even if its receiver gain looks promising in isolation.

For the admitted unit17 construction, D is the 17-by-17 identity and J has rank17, so the fixed-family minimum is17 packets. This explains precisely why its debt packets do not yield a new local price. It does not exclude other controls with useful zero-debt combinations.

## An r-packet completion needs a large exact-gain space

Suppose R is an invertible m-by-m matrix, as for the full first-Y target with its nonzero diagonal coupled scalings. Define G=R^{-1}B T^{-1}D. Then

    ker([J;E]) = {q : Jq=0 and Gq=q},
    rank([J;E]) = m - dim(ker J intersect ker(I-G)).

Proof: when Jq=0, the AVJ term vanishes and Eq=Rq-BT^{-1}Dq. Since R is invertible, Eq=0 is equivalent to Gq=q. Rank-nullity proves the second identity. This identity does not require AV=0.

Consequently a full104-coordinate first-Y completion with at most10 packets requires an at-least94-dimensional subspace on which the admitted controls have zero off-hub debt and exactly the required receiver gain. At eight packets the dimension is at least96. These are necessary and sufficient **algebraic** conditions inside the fixed packet interface, in addition to its separate guards, actual cache access, chronology, complete raw restoration and cost obligations. They provide a more precise next construction target than searching only for a low-rank off-hub debt matrix.
