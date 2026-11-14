# Equality in the native scalar proper-cover capacity

**Proposed all-field equality classification with exact finite source premises;
independent review pending. No new kappa.**

## 1. Statement and scope

Use the actual111 BIT root lines, canonical characteristic-two fitting K,
and C=row(K). The real receiver facet has dimension7. For a foreign support
S, chi_i(S) is0 if one proper linear subspace covers S,1 if two suffice but
one does not, and2 otherwise. Canonical supports have chi_i=2.

**Theorem.** Let k be any field of characteristic two, let h be arbitrary,
and let A be a native scalar fitting with every row in C+k h. If

    sum_i (2-chi_i(A_i)) = 14,

then there are exactly seven positive-saving rows. Their indices form a
seven-element mutually orthogonal native root set S. Every such row has
chi_i=0. There is a vector g supported exactly on S, with every g_i nonzero,
such that A_i=g/g_i for each i in S. Every other row has chi_i=2, although
it need not be the canonical row.

Conversely, every nonzero coefficient vector g supported exactly on seven
mutually orthogonal native roots gives such an equality fitting by using
g/g_i on S and K_i elsewhere. Thus equality has only double-saving rows;
in particular every subset of its positive-saving rows has even saving.

The theorem classifies support geometry and algebraic fitting rows. It
does not construct a physical history, source, supplier or multiplication
algorithm. It does not replace the distinct, sharp cardinality capacity17.

## 2. Reduction to the inherited finite envelope

The independently reviewed scalar proper-cover theorem proves saving at
most14 over every characteristic-two field, with proof SHA256
fb861bffc473928cd872a8248096b092e85c657969459147b0cef5821ab83da2.
Its all-field gluing dependency is the admitted scalar-direction proof
8e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b.

Replace every non-saving row by K_i. This preserves the row code and all
savings. Let I be the remaining positive-saving rows. Since each saves
at most2, equality requires |I|>=7. Gluing provides one common representative
g of the nonzero scalar quotient direction, supported in every closed
canonical support of I. The fitting equations then give

    A_i=(1-t_i g_i)K_i+t_i g,    t_i != 0.                 (1)

Write V=supp(g), s=|V|, r=real rank(V), J=I intersect V, j=|J|,
and U=I minus V. Lines in U are orthogonal to V; every line in J is
orthogonal to every other line of V. With

    N=(0,1,3,6,12,20,36,111,111),

the inherited parameter domain is

    r<=s<=N_r, 0<=j<=min(r,s), s<=j+N_(r-j).

If H(t) counts canonical foreign degrees at most t, every allowed triple
has the saving upper bound

    B(r,s,j)=min(N_(8-r),H(52+s))
             +min(N_(8-r),H(36+s))+2j.                    (2)

The source degrees are {55:1,56:11,57:16,58:36,59:28,60:13,61:5,62:1}.
There are569 allowed triples. The earlier sharp14 proof resolves the ten
with B>14. Exactly seven further triples have B=14:

    (3,4,1), (4,4,1), (4,5,1), (4,6,1), (4,7,1),
    (5,5,4), (8,8,7).

We show that these seven cases, and every earlier exceptional case except
the orthogonal-seven case, have saving strictly below14.

## 3. The seven newly relevant parameter cases

For (r,s,j)=(3,4,1) or(4,4,1), equality in(2) requires twelve outside
single savings. Each such receiver has degree at most56. There are exactly
twelve native receivers with degree at most56, and their real span has
rank7, certified by a nonzero minor modulo509. They cannot all lie in the
orthogonal complement of V, whose dimension is5 or4. Thus equality fails.

For r=4, s in{5,6,7}, j=1, equality likewise requires twelve outside
single savings. Their roots span rank4: a rank3 root flat contains at most
six lines. A rank4 simply-laced root subsystem has at most twelve lines,
with equality only for D4. This follows from the admitted low-rank root
classification in coordinate-return-optimum/PROOF.md, section3: A4 has10
lines, D4 has12, and all reducible rank4 types have fewer. Since all twelve
lines are actual native roots, the whole D4 is present.

Every D4 has an orthogonal four-root basis (use e1+e2,e1-e2,e3+e4,e3-e4
in the standard D4 model). The complete census of90079 native orthogonal
four-subsets therefore covers every such full native D4. It gives1121
distinct full native D4 spans. In every case, its full120-root orthogonal
complement consists of twelve D4 lines, and each of those lines is
orthogonal to precisely three other lines in that complement. These are
exact inner-product checks, independent of coefficient values in k.

But V lies in this complement, and its one member of J must be orthogonal
to its other s-1>=4 distinct roots. This contradicts the count3. Therefore
these three parameter cases cannot achieve14.

For (5,5,4), four isolated support lines force all five roots mutually
orthogonal. The inherited complete five-clique census gives at most three
outside receivers, each saving at most one, so the total is at most11.
For (8,8,7), all eight support roots are orthogonal and U is empty. At
each used receiver, alpha=1-t_i g_i either vanishes, leaving seven
independent foreign roots, or is nonzero, retaining at least48 canonical
foreign contacts outside V. In both cases chi_i>=1. Thus the total is
at most7. No binary-value assumption is made.

## 4. Making the previous exceptional cases strict

### Rank-three supports

For r=3 and s=5 or6, let P be the full native rank3 flat containing V.
The complete inherited catalogue has74396 flats from220934 independent
triples and11761 relevant flat/width cases. Its94 cases with at least15
eligible outside receivers were already shown to have no outside chi
saving by the reviewed sharp14 proof. Here eligible means degree<=52+s;
no outside row can save twice because55-s>36.

The new exact equality census finds94 flat/width cases with exactly14
eligible receivers. For each, one specified eligible receiver retains
quadratic span28 on canonical contacts outside the entire flat P. The
certificate is a28-by28 integer matrix with nonzero determinant modulo509.
Consequently this receiver cannot save; at most13 others can. Cases with
at most13 eligible receivers already have saving at most13. This covers
all coefficient choices and all subsets I, not just indicator vectors.

### Rank-four supports

The mixed rank-four cases with a nonorthogonal remainder have saving at
most10 by the earlier complete663805-configuration census. Orthogonal
four-subsets with j<=3 save at most13. When j=4, the two subsets with seven
eligible outside receivers already have no outside chi saving. Exactly
nine subsets have six eligible outside receivers; for each, the new
certificate blocks at least one with a full quadratic span outside V.
Hence they save at most8+5=13. All other four-subsets have at most five
eligible outside receivers and satisfy the same bound.

### Orthogonal supports of sizes five, six and eight

Five support roots give at most13 by the inherited common-root count3.
Eight give at most8 by the alpha argument in section3.

For six support roots, the inherited outside-root count is at most2.
Equality14 would require all six inside rows to save2 and both outside
rows i,j to save1. The exact clique census checks all35667 six-subsets;
30632 have two outside roots, and in every one those roots are mutually
orthogonal. Thus V union{j} is an orthogonal seven-subset and i is its
outside receiver. A saving at i requires its degree<=58, since only six
contacts can be deleted. The reviewed orthogonal-seven certificate applies
at i (its degree threshold is59): contacts of K_i outside V union{j}
already have quadratic span28. They are a subset of contacts forced by
(1) outside V. Hence chi_i=2, contradiction. The zero-exception check on
the two outside roots is a new explicit source premise; it is not inferred
merely from their being orthogonal to the six original roots.

## 5. The surviving equality case and its converse

Only r=s=j=7 remains. The seven support lines are mutually orthogonal.
The reviewed sharp14 proof rules out any outside chi saving for every
orthogonal seven-subset: a degree>=60 receiver cannot save cardinality,
and all6856 eligible seven-subsets have full forced quadratic span28 at
their unique possible outside receiver. Therefore I=J=V, and equality14
requires all seven rows to have chi_i=0.

In(1), if alpha=1-t_i g_i is nonzero, at least55-6=49 canonical foreign
contacts outside V survive. More than36 contacts cannot be covered by
one proper subspace in the admitted native geometry, so chi_i>=1. Thus
alpha=0, t_i=g_i^{-1}, and A_i=g/g_i as claimed. The other six support
roots are independent and span a proper six-dimensional subspace of F_i,
so these rows do indeed have chi_i=0.

For the converse, choose any seven orthogonal native roots and any nonzero
coefficient at each. The proposed rows have diagonal1 and all prescribed
zeros; all other canonical rows have chi_i=2. The word g is outside C:
its weight7 is below the inherited canonical minimum distance48, unchanged
by scalar extension. Thus this is a genuine one-direction equality fitting.

The support S is uniquely determined by its projective quotient direction.
If two seven-supported representatives g,g' define that direction, scale
one so g-g' belongs to C. Its support has size at most14<48, hence it is
zero. This uniqueness is not needed for the parity application but makes
the equality geometry intrinsic.

## 6. Exact evidence, negative controls and credit

check.py reads only the pinned actual native word and the frozen sharp14
case catalogue. It reconstructs the complete rank3, clique and native D4
domains, the seven new parameter cases, all103 new obstruction minors,
the low-degree rank7 minor and all30632 outside-pair checks. The source
root completion is verified to contain exactly120 lines and to be closed
under root reflections. A nonzero residue modulo the prime509 certifies a
nonzero integer minor, hence exact real rank; no floating tolerance is used.
The proof uses the inherited sharp14 certificates where explicitly cited,
and does not represent reusing them as a new independent review.

Controls include duplicated-row minors, an eight-root support whose rows
have seven independent foreign roots and cannot give double savings, a
seven-root sharp equality fitting, and removal of one equality row. The
author checker and its optimized execution must agree. Independent review
remains a separate requirement before admission.

Native SHA256:51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.
Exact dependency pins, reproduction commands and machine-readable case
certificates are retained beside this proof. Prepared for @CubeJerry by
Worker C with OpenAI assistance; credit the native, scalar-gluing,
low-rank-root, sharp14 and geometric-incidence predecessors. No new kappa.
