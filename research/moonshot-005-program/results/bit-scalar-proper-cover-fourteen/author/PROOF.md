# Sharp proper-cover capacity of one native scalar quotient direction

**Proposed source-specific theorem over every characteristic-two field; independent review pending. No new kappa.**

## 1. Statement and the distinct charges

Let K be the canonical111-port BIT fitting, C=row(K), and k any field of
characteristic two. Geometry is that of the pinned actual real source lines
and their rank7 receiver facets F_i. For foreign support S in F_i, put
chi_i(S)=0 when one proper linear subspace covers S (including empty S),
chi_i(S)=1 when two suffice but one does not, and chi_i(S)=2 otherwise.

**Theorem.** Every native scalar fitting A with row(A) contained in C+k h
for an arbitrary h in k^111 satisfies

    sum_i chi_i(supp_foreign(A_i)) >= 208.

The bound is sharp. Equivalently one projective quotient direction can save
at most14 capped proper-cover charges from the canonical total222. The
same bound applies to the contribution of any one direction inside a larger
fitting, by replacing all other rows with their canonical rows.

This is not a cardinality-capacity14 theorem. The earlier cardinality
capacity17 remains sharp. The admitted one/two-proper-chart bounds36/52
imply ell<=chi, while the quadratic incidence argument implies gamma<=chi.
Neither comparison asserts gamma>=ell. Full quadratic span in Sym^2(F_i),
dimension28, is sufficient for chi=2; rank deficiency is not sufficient for
chi<=1. The proof only uses the sufficient full-rank direction.

## 2. Inherited algebra and finite parameter reduction

Use the admitted all-field scalar gluing theorem and its569-case support
envelope from bit-quotient-direction-savings. Its proof SHA256 is
8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b.
The source and the cardinality bounds are unchanged. We strengthen the
geometric analysis, not the already sharp cardinality conclusion.

Let I be the changed rows in the nonzero quotient direction. If |I|<=3,
their chi saving is at most6. Otherwise the gluing theorem supplies a
common representative g supported on the intersection of their closed
canonical supports. Write V=supp(g), s=|V|, r=real rank(V), J=I intersect V,
j=|J|, U=I minus V. Then

    A_i=(1-t_i g_i)K_i+t_i g,       t_i != 0.

Every receiver in U is orthogonal to V. Every line in J is orthogonal to
all other lines of V, so J is an orthogonal direct summand of rank j.
The admitted native root bounds are N=(0,1,3,6,12,20,36,111,111). Hence

    r<=s<=N_r, 0<=j<=min(r,s), s<=j+N_(r-j).

If H(t) counts native canonical foreign degrees at most t, the cardinality
saving, and therefore the chi saving, is at most

    min(N_(8-r),H(52+s)) + min(N_(8-r),H(36+s)) + 2j.

Every one of the569 admissible integer triples gives at most14 except:

| r | s | j | Unrefined upper bound |
|---|---|---|---|
|3|5|0|20|
|3|6|0|20|
|4|4|2|16|
|4|4|3|18|
|4|4|4|20|
|4|5|2|16|
|5|5|5|16|
|6|6|6|15|
|7|7|7|15|
|8|8|8|16|

We now resolve precisely these ten cases. The degree histogram is the
admitted {55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}.

## 3. Rank-three supports

For r=3 and s=5 or6, let P be the full actual rank3 flat containing V.
All changed receivers are outside V and orthogonal to P. Their rows retain
coefficient1 at every canonical foreign contact outside P. The complete
flat/width census contains74396 flats from220934 independent triples and
11761 relevant width5/6 cases. Only94 cases have at least15 potentially
saving outside receivers. All94 have width6, with eligible counts15,16,17
occurring54,28,12 times. Every other case already saves at most14 by
cardinality, for any coefficients or subset of receivers.

For every orthogonal receiver of each of the94 exceptional flats, the
canonical contacts outside the entire flat have quadratic span28. Explicit
nonzero integer28-by28 minors certify this. Thus every changed receiver in
an exceptional flat has chi=2, and the chi saving in that case is0.

The extended threshold15 census reuses the credited exact Gram method of
the admitted threshold17 census. It enumerates every triple basis, rather
than selecting binary examples. All coordinate products are small bounded
integers; the vectorized integer arithmetic cannot overflow. The source
coefficients in g are arbitrary elements of k and never enter this census.

## 4. Rank-four supports

For r=s=4 and j>=3, all four source lines are mutually orthogonal. For
j=2, the remaining two are either orthogonal, giving the same class, or
are a nonorthogonal pair. For r=4,s=5,j=2, the remaining three lines span
rank2; some pair is nonorthogonal and spans that remainder.

For two mutually orthogonal native lines J and a nonorthogonal pair a,b
orthogonal to J, the complete663805-configuration census gives at most6
common orthogonal native lines. Thus both nonorthogonal-remainder cases
have at most6 outside savings and4 inside savings, total at most10.
No special choice of the third rank2 line is needed: the pair already
spans its real plane.

For four mutually orthogonal lines, the admitted complete90079-subset
census bounds the number of common orthogonal receivers of degree<=56
by7. Thus j<=3 gives at most13 savings. For j=4, at most six such receivers
already gives at most14. Exactly two four-subsets have seven eligible
receivers. For both, every common orthogonal receiver retains quadratic
span28 outside the four-line support. Thus all outside chi savings vanish,
leaving at most8 inside savings. The only cardinality15 four-line cases
are therefore excluded geometrically.

## 5. Orthogonal supports of sizes five through eight

The cases r=s=j=5,6,7,8 have mutually orthogonal support lines. The complete
native clique census has77003 orthogonal five-subsets and35667 six-subsets.
Their common orthogonal native sets have sizes at most3 and2 respectively.
Since removing at most six contacts cannot bring a degree at least55 below
37, each outside row saves at most one cardinality charge. The total upper
bounds are therefore10+3=13 and12+2=14.

There are9443 orthogonal seven-subsets. Their real orthogonal complement
has rank1, so there is at most one outside receiver. An outside receiver
of degree>=60 cannot save even cardinality after deleting seven contacts.
Exactly6856 seven-subsets have an outside receiver of degree<=59. At each,
the remaining canonical contacts have quadratic span28, certified by an
explicit nonzero integer minor. There is no outside chi saving. The seven
inside rows save at most14 altogether.

For an orthogonal eight-subset, U is empty. At any inside receiver i put
alpha=1-t_i g_i. If alpha=0, all other seven support coefficients t_i g_j
are nonzero. Their independent real source lines span F_i, so chi_i>=1.
If alpha!=0, every canonical contact outside the eight-subset survives.
There are at least55-7=48 such foreign contacts, more than36; therefore
chi_i>=ell_i>=1. Each of the eight rows saves at most one, total at most8.
This argument is valid for unequal nonbinary values g_j and all allowed k.

All ten exceptional parameter cases now have chi saving at most14. Together
with the569-case reduction and the small-I case this proves the theorem.

## 6. Sharpness, exact evidence and scope

Take S={54,56,57,59,61,63,64}, seven mutually orthogonal native lines,
and h its indicator. Set A_i=h for i in S and A_i=K_i otherwise. The
diagonal remains1 and all forbidden entries are zero. Each selected row
has six independent foreign roots, contained in a proper facet subspace,
so chi_i=0. Every other canonical row has full quadratic span and chi_i=2.
The total charge is208, realizing14 savings over every characteristic-two
field. The weight-seven h is outside C by the admitted distance48 premise.

The certificate package retains all exceptional cases and8737 nonzero
exact integer minors in compressed, reproducible files. It also includes
complete clique and mixed-configuration counts. The duplicated-minor control
has determinant0. The old cardinality17 witness has no chi saving, preserving
the essential distinction between these quantities. The rank-three census
is credited predecessor-method reuse; independent review remains separate.

Native SHA256:51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.
The quadratic incidence dependency is bit-geometric-facet-charge/author/
PROOF.md, SHA2568fed71e8698ce84e1fa0f09deb7433f3338f21f3a35b912d08e2de046426d8ab.
The previously reviewed capacity16 remains correct and is superseded only
in strength, not invalidated. Operator consequences require the separate
support-monotone capacity bridge and its hypotheses. No physical source,
ordinary service, strict supplier, complete kappa or foundation is supplied.

Credit @CubeJerry, admitted scalar gluing/census and real-incidence authors,
root construction, and OpenAI assistance.
