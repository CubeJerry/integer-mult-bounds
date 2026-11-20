# Independent address review and exact integral gluing groups

Let P be a rational idempotent on Qⁿ of rank r, d its least positive denominator, and L=Zⁿ. Put U=L∩im(P) and V=L∩ker(P). The finite group A=L/(U+V) has exponent exactly d, at most min(r,n−r) generators, and order dividing d^min(r,n−r). This statement also applies to nonsymmetric compiler splits.

Map x in L to Px modulo U. Its kernel is exactly U+V. Its image lies in (d⁻¹U)/U. The complementary projection gives an injection into (d⁻¹V)/V as well. Smith reduction bounds the number of generators by both r and n−r. An integer t annihilates A exactly when tP maps every integer column into L, since tx=tPx+t(I−P)x. Thus the annihilating ideal is dZ and the stated order bound follows.

For computation put E=dP. The map x↦Ex modulo dL has kernel U+V. Unimodular Smith reduction preserves its image group. A Smith value s contributes a cyclic factor of order d/gcd(s,d). Thus the gluing group can be computed without using an adapted integral basis.

The 3,150 D charts give 14 trivial groups, 336 of type (2,2), 112 of type (2,2,2,2), 1,792 of type (4,4), and 896 of type (2,2,4,4). The A2 types are (3) on 224 charts and (2,6) on 896. Both 2 and 3 occur in the specified rational addresses. The full group distinguishes charts that have the same determinant or denominator.

The checker uses the Euclidean Gram projector of the first rationally independent root vectors. It imports no author routines or projectors. It reconstructs 636 original frames plus 120 line, 1,120 plane and 3,150 four-space projectors. It checks both multiplication orders on every one of the 50,400 incidences and all complementary four-spaces. An exterior line with denominator five verifies the stated catalogue scope. The [receipt](output/RESULT.json) records all finite gluing types.

For the uniform assertion, the bases of U and V concatenate into a matrix whose determinant is a unit in Z[1/6]. This diagonalizes P over that ring. Equal-rank projectors can consequently be matched and positive coordinate ranks split inside an adapted basis. Tensoring with an identity preserves every free rank. Conjugations, tensor products, sums, composites and specialization modulo q^w for primes q≥5 preserve the resulting address constructions. The author's paired caller calculation assumes its stated original X/Y trace, owned helpers and physical costs. The five full-framework obligations and both strict suppliers remain open. No new κ.

Reproduce with Python, NumPy and SymPy.

    python -B PATH/check.py --repo REPO --out FRESH
