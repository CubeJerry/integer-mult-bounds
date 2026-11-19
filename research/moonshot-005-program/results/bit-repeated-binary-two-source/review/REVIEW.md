# Independent review of the repeated binary two-dimensional source gate

**Accept the stated exact-source theorem**, with its field, repetition,
canonical-bank and fixed-route hypotheses retained. This is a scoped exclusion
of one source representation. It is not an exclusion of arbitrary arrays, a
movement lower bound, a repair-channel theorem or a new complete κ.

The proof, implementation and output hashes reviewed are in
`output/RESULT.json`. The author package is
`workers/native_gluing/repeated-binary-two/author` in this session. The review
implementation imports no author implementation and does not execute it.

## 1. The full shared-port range follows from saturation

The decisive hypothesis is exact recovery through the full fifteen-port tuple,
whose entire product alphabet has the same cardinality as the target. It is
not enough merely to observe that individual ports have full marginal ranges.

For one ordinary plane H and a jointly tight receiver i, fix every other
visible source quotient at each donor of H. Their H quotient values remain
independent and range over their complete alphabets because each donor's
sixteen visible quotients are a bijection. The balanced proper-source
restriction means no other varying plane can enter the receiver from these
changes. The admitted canonical-zero argument supplies the needed outside
inputs without adding a proper channel from them.

The receiver's native sum varies over its full 2r-dimensional H target. Its
fifteen H-to-D exits have exactly2r bits altogether. If the exit tuple allowed
two distinct target values to coincide, exact recovery would fail. Since its
alphabet has at most as many values as the target, it is exactly a bijective
relabelling of that target. In particular its image equals the complete
product alphabet of the fifteen physical ports. Projecting that product onto
any shared set of q ports yields every possible shared subtuple, with
2qr/15 bits of information.

The shared physical H-to-D values are the same functions of the same H inputs
for both receivers. Each factors through both target maps. Translation
invariance under each target kernel makes it invariant under their sum, so it
factors through the intersection of the target row spaces. This applies to
nonlinear port functions as well as linear ones.

Because the same binary base matrix repeats in every copy, the relevant
intersection is `(W_i intersect W_j) tensor F2^r`. Its dimension is an integer
multiple of r. The exact native q=3 or6 shared exits therefore force a nonzero
base intersection. No inference of this form has been made for independently
varying base blocks.

The independent finite check rejects the tempting weaker condition by the
tuple(x0,x0): both one-bit marginal ranges are full, but the joint tuple has
only two values and cannot carry a two-bit target. It also enumerates every
Boolean function of every binary graph target in the two-donor case. The
functions that factor through both targets are exactly the functions of their
intersection, including the nonlinear cases.

## 2. The binary graph-plane lemma is valid

Choose two distinct2-spaces with intersection line L. If a third avoids L,
pairwise intersection puts it in their3-dimensional sum T. A further plane
outside T can meet both initial planes only in L, and hence cannot also meet
the third plane. Therefore a pairwise-intersecting family either has a common
line or lies in one3-space.

In the latter case every donor projection T to F2^2 is surjective and has a
line kernel. At least two such kernels differ, because the full embedding of
T into the donor direct sum is injective. A graph plane is a hyperplane of T
avoiding both kernel lines. A nonzero binary functional defining that
hyperplane must take value1 on each of their two distinct generators. These
are two independent conditions on a3-dimensional dual space and leave exactly
two possible functionals. Thus at most two distinct graph planes are available
in T, and they already share a line. This proves the stated lemma.

The checker independently enumerates all ambient binary planes from vector
pairs. It finds35 ambient planes and6 graph planes for two donors, and651
ambient planes and36 graph planes for three donors. All108 pairwise-intersecting
three-donor triples have a common line. This suffices to cover larger families:
any family with no common line would contain a triple consisting of two
distinct members and one member avoiding their intersection.

For every possible common line, the full family of graph planes containing it
has span dimension at mostm+1. The independent enumeration gives9 two-donor
line stars of size2 and span3, and27 three-donor line stars of size4 and span4.
The author's universal span argument is also sound: the binary nonzero value
of each chosen donor functional is necessarily1, putting every vector outside
the common line in one affine space of dimensionm.

This field restriction is essential. A separate GF4 fixture in this review
uses graph maps

    I, [[1,1],[0,1]], [[1,0],[0,omega^2]],

where omega^2+omega+1=0. The three graph planes have pairwise intersections of
four elements but only zero in common. The review also exhibits a varying-copy
direct sum whose total intersection is nonzero even though one base summand
has zero intersection. Those controls prevent transfer to the excluded field
and repetition interfaces.

## 3. The inherited color caps give the claimed total

Once all target planes contain one line, any port neighborhood containing two
different target planes can transmit only information in that line. If a
receiver had no monochromatic incident neighborhood, its entire port tuple
would factor through only r bits, contradicting its required2r bits. Thus the
author correctly obtains the already admitted self-cover coloring condition.

When alpha_H<m, the inherited cap bounds the number of distinct planes, and
their span is at mostalpha_H+1. When the cap is truncated at m, there could be
more than m colors, but the separately proved graph-star span boundm+1 supplies
the same conclusion. This distinction is handled correctly in the proof.

The review reconstructs every ordinary plane, jointly tight receiver set,
visible D4 exit and port neighborhood from the pinned integer geometry. All
1,108 instances match the inherited independent color certificate. The new
shared-port census has201,929 receiver pairs sharing three exits and275,160
pairs sharing six. Every receiver has fifteen of the forty-five exits.

The inherited cap histogram is exactly
204(2,1),23(2,2),630(3,1),249(3,2),2(3,3). Its new covered information total is
2,492r bits. The1,436 uncovered ports receive their full2r/15 allowance, and
the eleven singleton planes receive their full3r source allowance each. Thus
the total is40747r/15. The canonical-zero input has3264r dimensions, leaving
the strict deficit8213r/15, or98,556 bits at the base balancedr=180.

The existing color partition decisions are authenticated and their exact
instances are matched; this review does not claim to rerun or independently
reprove the earlier coloring search. The new graph-plane and geometric
claims have separate code checks and the written arguments above.

## 4. Admission scope and reproduction

The theorem requires the original canonical code and exact native recovery on
the original balanced routes. Added Hub information, a replacement canonical
bank or a deliberately approximate native map breaks the saturation premise
and requires a fresh argument. The numerical deficit must not be carried into
such interfaces by subtracting the number of new messages.

The source maps may be arbitrary rank-two binary2-by32 matrices and need not
commute. They must repeat identically in the common original-copy coordinates.
Larger coupled bases, independent per-copy changes, global donor changes of
basis mixing copies, and larger base fields remain outside the result.

Reproduce with

    python3 check.py --repo REPOSITORY --author AUTHOR_PACKAGE --out OUTPUT

Expected status: `PASS_INDEPENDENT_REPEATED_BINARY_TWO_REVIEW`.

Credit retained authors, @CubeJerry and Worker A. This is a distinct Worker-B
mathematical/code review with substantial OpenAI assistance. It is not
independent human review or formal-kernel verification. No foundation is
discharged and no new κ follows.
