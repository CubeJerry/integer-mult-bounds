# A scalar single-extension fitting matrix changes Gram rank by at most eight

**Status: proved, with a sharp scalar example. No source-word admission and no new κ.**

Retain the scalar characteristic-zero source interface and theorem in the independently reviewed local-linearity gluing package. Then every admitted K satisfies

\[
 \boxed{\operatorname{rank}(K-G)\le8.}
\]

This includes its small active-span exception. The bound is sharp as scalar linear algebra.

## 1. The source nonorthogonality graph has clique number eight

Every source normal n has odd weight, either three or seven. For distinct source normals n,m, their real root inner product is nonzero exactly when their binary dot product is zero. This follows directly from the two explicit root formulas, and the independent checker verifies it for all source pairs.

A clique of pairwise nonorthogonal projective roots is therefore a family of binary vectors satisfying

\[
 n_i\cdot n_j=\delta_{ij}\quad\text{over }\mathbb F_2.
\]

There can be at most nine. Nine are impossible. If nine existed they would be an orthonormal basis of \(\mathbb F_2^9\), and their sum would equal the all-ones vector e, because both have dot product one against every basis vector.

Put \(q(x)=\sum_{p<q}x_p x_q\) over \(\mathbb F_2\). Every root normal has q(n_i)=1. The polarization identity is

\[
 q(x+y)=q(x)+q(y)
       +\bigl(\sum x_p\bigr)\bigl(\sum y_p\bigr)+x\cdot y.
\]

For nine pairwise binary-orthogonal odd vectors this yields
\(q(\sum_i n_i)=9+\binom92=1\). But \(q(e)=\binom92=0\), a contradiction. Thus every clique has size at most eight. An eight-clique has no external common allowed neighbor, because such a neighbor would make a nine-clique.

An actual source eight-clique is

    11,13,14,112,176,304,471,487.

Its common allowed neighborhood is exactly itself.

## 2. Bound for the fitting perturbation

For active span at least three, let I=supp(t), J=supp(g). The gluing theorem gives

\[
 K-G=t g^T-\operatorname{diag}(t\odot g)G,\qquad
 \operatorname{rank}(K-G)
 \le\min\{|I|,\,1+|I\cap J|\}.
\]

The intersection C=I intersect J is a clique. If its size is at most seven, the rank is at most eight. If its size is eight, every point of I and every point of J is allowed against every point of C. The no-external-common-neighbor property forces I=J=C. The row-support bound is then eight.

For active span at most two, only three rows can change, so the same conclusion holds.

## 3. Sharpness

Let C be the displayed actual eight-clique. Take t and g to be its indicator vectors. The fitting formula makes every active row equal to the indicator of C and leaves all inactive rows equal to G. It has all required forbidden zeros and unit diagonal.

The independent checker verifies:

- rank(K)=9;
- rank(K-G)=8;
- the inactive roots still span eight dimensions;
- g is outside the Gram row space, since it vanishes on the spanning inactive roots and is nonzero;
- an eight-by-eight minor of 18(K-G), with rows 487,471,304,176,112,14,13,11 and columns 11,19,26,131,69,14,13,35, has determinant 387,420,489.

Thus this is a genuine single scalar extension and the perturbation-rank bound is attained.

## 4. Consequence and limits

For any fixed matrix M of compatible dimensions, replacing a target Gram contribution by this K can alter the algebraic residual rank by at most eight, by the rank inequality. This is only an accounting constraint on that declared scalar substitution. It does not establish a reduction of eight in the programme's actual reverse residual, and it does not price the packet, row scaling, current-row access, endpoint restoration or any of the five foundational assumptions.

The theorem does not apply to multiple new scalar directions, arbitrary operator-valued decoders, a replacement whose row space is not contained in the fixed W plus one direction, or a new physical representation with a different residual interface.

Credit: the global-code scalar gluing theorem supplies the fitting normal form. The global-adversary worker supplied the binary clique argument, rank-eight consequence and sharp example. AI-assisted research for @CubeJerry's programme.
