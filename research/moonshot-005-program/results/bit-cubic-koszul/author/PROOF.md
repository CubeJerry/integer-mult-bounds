# Eight constructive cubic modes beyond local quadratic products

**Author construction and structural theorem; independent review pending.
No new kappa and no complete target fitting.**

The quadratic/exterior result excludes a small completely entangled
quotient in the Schur-square reservoir. We construct the next reservoir
and identify eight genuinely new local directions. They are the middle
cohomology of multiplication by a symplectic two-form in characteristic
two and have explicit cubic representatives supported on orthogonal
eight-cliques. Sharing them in a complete source remains open.

## 1. The model and the characteristic-two exterior complex

Let k have characteristic two. On F2^8 put

    q=x0 y0+x1 y1+x2 y2+x3 y3,   X={x:q(x)=1}.

The set X has120 points. The authenticated native111 source is the
nine-point puncturing proved in the companion quadratic/exterior
package. Let Q_r be the evaluation code on X of square-free polynomials
of degree at most r. Thus C=Q_1. The native Schur cube is the puncturing
of Q_3; no multiplication of unknown data is implied by using a Schur
power to describe the coefficient code.

For W with basis a1,b1,...,am,bm, let

    omega=sum_l a_l wedge b_l,
    d:Lambda^r W -> Lambda^(r+2) W,  d(z)=omega wedge z.

In characteristic two, d^2=0. Its cohomology is concentrated in degree
m and has dimension2^m, with basis choosing exactly one of a_l,b_l
from each pair. This is the classical characteristic-two spin-module
construction, not a claimed new general cohomology theorem: see Rod
Gow, [Contraction of Exterior Powers in Characteristic2 and the Spin
Module](https://doi.org/10.1023/A:1004961421891), Geometriae Dedicata64
(1997),283--295, and Peter Sin's [2004 lecture](https://people.clas.ufl.edu/sin/files/mobile.pdf),
pages16--18, for the wedge-multiplication formulation. We include the
elementary proof to make the new native-code application self-contained.
Each two-variable factor splits
as the acyclic complex span(1,a_l b_l), with d(1)=a_l b_l, and the
zero-differential space span(a_l,b_l). A tensor summand with an acyclic
factor is contractible by contracting its first such factor; cross
terms cancel in characteristic two. The only cohomology is the tensor
product of the m spaces span(a_l,b_l).

For m=4, H^2=H^3=0. Therefore the kernels of multiplication by omega
in degrees2 and3 are respectively k omega and omega wedge W, of
dimensions1 and8. For m=3 the middle kernel has dimension14, its
image from degree1 has dimension6, and the cohomology has dimension8.

## 2. Cubic dimension and duality

If a degree-at-most3 Boolean polynomial p vanishes on X, then qp=0.
The degree5 part gives omega wedge p3=0, where p3 is its leading
cubic part. The m=4 exactness gives p3=omega wedge l for some linear
form l. Subtract (q+1)l, preserving vanishing and removing degree3.
The degree4 equation for the remainder gives p2=lambda omega.
Subtract lambda(q+1). The remaining affine function vanishes on X
and is zero, since X affinely spans F2^8. Starting from e0+f0, adding
any of the other six basis vectors stays in X; starting from e1+f1
similarly detects e0 and f0. A vanishing affine function therefore has
every linear coefficient and then its constant coefficient zero.

Consequently the complete degree-at-most3 kernel is

    {(q+1)l : l is affine},

of dimension9. The domain has dimension1+8+28+56=93, so dim Q_3=84.
The same degree2 argument gives the sole relation q+1 and dim Q_2=36.
Boolean multiplication has exterior multiplication as its leading
square-free term: repeated variables lower the degree.

With the ordinary coordinate pairing on k^X,

    Q_3=Q_2^perp.

A product of a cubic and a quadratic has degree at most5. Summing it
over X equals summing its product with q over F2^8. That product has
degree at most7 and every such monomial sums to zero. Dimensions
84+36=120 prove equality. This is an exact algebraic identity for
every k, not a finite-field extrapolation.

## 3. Complete local decomposition

Choose a hyperbolic basis with receiver a=e0+f0. A direct construction
takes singular e0 with B(a,e0)=1, puts f0=a+e0, and completes their
orthogonal complement by hyperbolic pairs. The verifier does this for
every native receiver. Put J_a={x in X:B(a,x)=0} and K_a=1+B(a,x).
The64 points of J_a are parametrized by u=(x1,y1,x2,y2,x3,y3):

    x0=y0=1+q6(u),   q6=x1y1+x2y2+x3y3.

The restriction of Q_2 to J_a is

    RM(2,6)+span{q6(u)u_l:l=1,...,6},

of dimension22+6=28. RM(r,6) denotes degree-at-most-r Boolean
evaluations on all64 points. The added cubic parts omega6 wedge u_l
are independent modulo degree2.

By the duality above, the cubic functions supported in J_a form the
dual of this restriction. Boolean degree pairing gives
RM(2,6)^perp=RM(3,6). For a leading cubic gamma, orthogonality to
the six added forms is equivalent to gamma wedge omega6=0: pair with
each additional linear factor and extract the coefficient of all six
variables. Hence the literal local cubic code is exactly

    RM(2,6)+ker(omega6 wedge -:Lambda^3 W6 -> Lambda^5 W6),

of dimension22+14=36. Its product subcode K_a star Q_2 has dimension28.
The quotient of these local codes is precisely the eight-dimensional
middle cohomology ker(d_3)/im(d_1).

## 4. Explicit new modes with cheap receiver support

For each of eight choices t_l in {x_l,y_l}, l=1,2,3, define

    g_t(x)=product_(l=1)^3 (1+t_l(x)).

If all selected variables vanish, q6=0, and q=1 forces x0=y0=1.
Thus this global cubic is supported in J_a. Its support has eight
points, with the complementary variables free, and includes a.
The eight points are pairwise polar-orthogonal, hence are an actual
orthogonal eight-clique of the completed real-root configuration.

The leading local cubics choose one variable from each hyperbolic pair.
Their classes form the cohomology basis from section1. Therefore

    Q_3 intersect k^{J_a}
       = K_a star Q_2 + span{the eight g_t},

and the eight displayed directions are independent modulo the product
subcode of dimension28. This is a constructive identity at every
receiver, not merely a dimension census.

The native puncturing is injective on Q_3 and preserves all111 local
dimensions36, as checked exactly. It therefore transports this entire
local decomposition to the actual111 source over every k. Each native
g_t still has own coefficient1. If at most seven of its clique roots
survive, the foreign support has rank at most6 and chi=0. If all eight
survive, its foreign support has rank7 and admits a two-proper-subspace
cover, so chi=1. These are locally cheap fitting rows, not an assembled
global source.

## 5. Global geometry and the missing construction

The completed root system has2025 orthogonal eight-cliques. Their
indicators span Q_3 of dimension84. Native puncturing leaves sizes
8,7,6,5,4 with multiplicities1094,691,198,40,2. This provides concrete
alternative global generators; it is separate from the exterior proof.

The native local quotients (Q_3 intersect k^{J_i}+C)/C have dimension35.
Their pair intersections have dimension11 for orthogonal receiver pairs
and15 for nonorthogonal pairs. They escape the one-dimensional pair
geometry responsible for the quadratic obstruction.

What remains is to combine the new modes into one three-dimensional
width2 quotient containing suitable two-dimensional receiver planes
at enough saving rows, with all own identities and proper-cover
conditions, and no pure tensor. The companion Kronecker theorem leaves
three possible pure chain types for this target. The local construction
alone does not establish their shared global realization.

Alternatively, a chronological source could use a larger cubic history
with few live packet widths. Both routes must account for acquisition,
chart moves, original restoration, ownership and cleanup. Neither the
scalar dimension84 nor the local quotient dimension35 is converted
into a physical packet price here. All foundational assumptions remain.

## 6. Verification and credit

Native gzip SHA256:
`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
The exact checker reconstructs binary coordinates from that source,
completes the fourteen observed four-coordinate root supports to the120
real lines and checks every real/polar pairing, then verifies
the global dimensions36 and84, all111 identities28+8=36, the explicit
clique modes, all6105 pair intersections and the2025-clique span.
These finite source checks supplement the universal proof above.

```sh
python author/check.py --repo /path/to/integer-mult-bounds --output author/RESULT.json
```

If the companion source loader is not a neighbouring package, pass
`--geometry-check /path/to/bit-quadratic-exterior/author/check.py`.
Expected status: `PASS_AUTHOR_CUBIC_KOSZUL_CONSTRUCTION`.

The external coding-theoretic motivation is Randriambololona,
[On products and powers of linear codes under componentwise
multiplication](https://arxiv.org/abs/1312.0022), and [The quadratic
hull of a code and the geometric view on multiplication
algorithms](https://arxiv.org/abs/1912.06627). These papers motivate the
Schur-code/geometry viewpoint; the native local decomposition and its
exterior-complex proof are supplied here, rather than attributed to them.

An additional constructive lead is van Geemen and Marrani,
[Lagrangian Grassmannians and Spinor Varieties in Characteristic
Two](https://doi.org/10.3842/SIGMA.2019.064), SIGMA15(2019),064.
Their principal-minor map relates Lagrangian geometry to the spinor
variety in characteristic two. That map has not been used as a native
fitting or cost theorem here. It motivates the next attempt to glue
the local eight-mode spaces into shared noncommuting receiver planes.

Credit the native and code predecessors, the companion finite-geometry
package, @CubeJerry, and AI assistance. No independent review, physical
supplier, or complete target theorem is claimed before its actual
verification and admission.
