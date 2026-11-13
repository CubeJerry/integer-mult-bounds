# Seventeen saved facet visits per scalar quotient direction

Status: source-specific theorem with exact exhaustive finite premises, pending
independent review. No new source, supplier or complete kappa.

## Model and dependencies

Work over any scalar field F of characteristic two, on the pinned actual111
BIT roots. Let K be the canonical fitting, C its nine-dimensional row code,
and a_i the foreign support size of K_i. The exact histogram is
{55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}.
T_i is its closed support and Z_i its prescribed zero set. A fitting has
diagonal one and is zero on each Z_i. No algorithm is supplied by a fitting.

We use the independently reviewed E7 source-arrival interface, including
generated upward local copies, with NO Y feedback. A foreign support of more
than52 needs at least two X/packet proper-chart arrivals beyond the Y last
proper chart; more than36 needs at least one. Thus define

    ell_i(A) = 1[foreign_weight(A_i)>52] + 1[foreign_weight(A_i)>36].

Any complete source in this interface with q descending paths and e additional
upward-local facet arrivals must satisfy sum ell_i(A)<=111+q+e. An extra
arrival still requires a paid positive-rank MOVE. Canonical rows have ell=2.
This interface is narrower than the separate all-V downset cut allowing Y
feedback; the present result must not be transferred to that broader model.

The one-extra-coset gluing theorem supplies the following exact source fact.
If a coset h+C is available on a set I of rows, and its binary coefficient
normals span dimension at least three, there is one representative g in h+C
supported in intersection_{i in I} T_i. If those normals have rank at most
two, I has at most three rows. The rank statement is unchanged over extension
fields because binary matrix ranks are unchanged. The source gluing premise
uses all111 single zero-set ranks8 and all6105 pair zero-set ranks7; it is a
finite certified source fact, not a conjectured property of an arbitrary code.

Real geometry uses the admitted root-flat bounds
N_0=0, N_1=1, N_2=3, N_3=6, N_4=12, N_5=20, N_6=36.
For ranks7 and8 use the deliberately loose bound111. These count projective
root lines, not signed roots. Scalar characteristic-two algebra and real
source geometry have distinct roles throughout the proof.

## One projective quotient direction

Let I be the rows whose nonzero classes A_i+C lie in ONE fixed projective
direction of F^111/C. Choose h representing that direction. Then
A_i=c_i+t_i h for c_i in C and nonzero t_i. The fitting conditions imply
availability of h at every i in I. If |I|<=3, these rows save at most6 visits.
Otherwise their normals span rank>=3 and gluing gives a common g as above.
Absorb its global codeword difference into c_i. Zero-set rank8 and diagonal
one then force the exact formula

    A_i=(1-t_i g_i) K_i+t_i g.                         (1)

Let V=supp(g), s=|V|, r=dim_R span{root_j:j in V},
J=I intersect V, j=|J|, and U=I minus V. The nonzero coset ensures s>=1.
Every root in U is orthogonal to every root in V, so |U|<=N_(8-r).
Every root in J is orthogonal to all OTHER roots in V. Thus the j roots in
J are mutually orthogonal and form a direct orthogonal summand of span(V).
The remaining s-j roots have span dimension r-j, giving

    r<=s<=N_r, 0<=j<=min(r,s), s<=j+N_(r-j).           (2)

For i in U, g_i=0 and (1) gives A_i=K_i+t_i g, deleting at most s foreign
nonzeros. For i in J we generously permit both visits to be saved. Put
H(t)=#{i:a_i<=t}. The total saved visits in this direction are therefore at most

    min(N_(8-r),H(52+s)) + min(N_(8-r),H(36+s)) + 2j.  (3)

This holds for arbitrary nonzero scalar coefficients and arbitrary choices
of I; it does not assume binary flips or that every available row uses h.
It also holds for an arbitrary representative supplied by gluing, not only a
minimum-support representative.

There are569 integer triples satisfying (2) with these bounds. Exact integer
evaluation of (3) has maximum20. The ONLY cases where the bound is at least17
are (r,s,j)=(3,5,0),(3,6,0),(4,4,3),(4,4,4). This short finite parameter check
is included verbatim in the verifier. All other cases have upper bound<=16.

## The two remaining finite geometric cases

If r=3 and s=5 or6, select any three independent roots in V. Its actual
rank-three root flat contains V. For each such flat, all roots orthogonal
to V are exactly those orthogonal to that three-root basis. Exhaustively
enumerating every independent triple of the actual111 roots, using integer
Gram determinants and exact membership, produces220934 independent triples
and74396 distinct actual flats. The11761 relevant flat/width cases with
width5 or6 contain at most17 orthogonal roots of degree <=52+s.
The second term in (3) is zero and j=0. Hence these cases save at most17.

If r=s=4 and j>=3, V has exactly four independent roots and three are
orthogonal to every other root in V. All four are therefore mutually
orthogonal. Exhaustively enumerating the90079 actual orthogonal four-subsets
shows that at most seven common orthogonal roots have degree<=56. Thus (3)
is at most7+2j<=15. The enumeration is independent of which roots belong to I.

All computations use only exact integers. Gram entries divided by two are
in{-2,-1,0,1,2}, with diagonal2, and the explicit three-by-three determinant
and adjugate formulas have tiny bounds compared with signed64-bit capacity.
No numerical rank tolerance, random search, or finite-size extrapolation is
used. Exhaustion of bases is a proof for this fixed finite source geometry;
the field-general conclusion then follows from the preceding algebra.

Consequently EACH nonzero projective quotient direction used by fitting rows
saves at most SEVENTEEN facet visits. This is a sharp source-specific bound.

## Sharp algebraic witness and negative control

Take V={0,2,38,41,42,45}, an actual rank-three six-root flat, and let U be all
twenty actual roots orthogonal to its span. Set h to the indicator of V and
u to the indicator of U. Then A=K+u h is a fitting: U and V are disjoint and
cross-orthogonal. Its code is contained in C+span(h), its binary rank is10,
and its exact row visit lower bound is205, saving222-205=17.
Thus replacing17 by16 is false even algebraically. This is not a physical
word or proof that205 visits suffice. The h coset is nonzero: its weight6
is below the canonical code's minimum distance48.

Binary minimum distance is unchanged by scalar extension. Indeed, expand
the finitely many coefficients of a codeword in a basis of their finite
F2-span. Each coefficient component is a binary codeword, and the extended
word's support is the union of the supports of its nonzero components.
Equivalently, punctured binary generator ranks are invariant under extension.
This also validates the extension-field sharpness and coordinate-exception
arguments in the predecessor gluing proof.

## Direction count and two-extra-mode obstruction

Let d(A) be the number of distinct nonzero projective classes among rows
A_i+C. Rows in C are uniquely K_i and save nothing. Summing the bound over
the disjoint direction classes gives

    sum ell_i(A) >= 222-17 d(A),
    d(A) >= ceil((111-q-e)/17) for any complete source.  (4)

For q8, e=0,1,3 require respectively at least7,6,6 directions. For q9,
e=0 or11 both require at least6. These e are generous movement allowances:
q8/m6 allows only one, all finite q8 callers allow at most three, and the
optimistic q9 direct-route limit allows at most eleven.

If the quotient span of the fitting rows over C has dimension at most two,
it has at most three nonzero projective directions over F2 and at most five
over F4. Formula (4) then forces respectively at least171 or137 facet visits.
The q8 limit supplies at most122; the q9 limit at most131. Both fail even
under those optimistic allowances. Thus over F2 and F4 at least THREE
independent quotient dimensions outside C are necessary in this interface.
The same statement holds relative to every canonical vertex-gauged code:
diagonal conjugation preserves fitting zeros, support weights, projective
quotient directions and all arrival counts.

In particular a historical code containing C and at most two extra scalar
modes cannot complete either priced target over F2 or F4. If it contains C,
its dimension must be at least12. This is NOT a lower bound12 on arbitrary
fitting rank: a rank-ten space need not contain C. More generally the proved
statement is dim((row(A)+C)/C)>=3. A code containing some actual eight-mode
subcode of C would consequently need total dimension at least11, IF those
eight modes are indeed in that historical code. Merely computing eight
initial Hub values does not automatically put them in the scattering G.

For larger characteristic-two fields there are more projective directions;
the all-field direction-count theorem remains, but the dimension-three
conclusion is not asserted. Entangled block operators are also outside this
scalar argument. General Y feedback, changed routes, arbitrary codes without
the stated arrival interface, complete endpoint realizability and all costs
remain open. No supplier or new complete kappa follows.
