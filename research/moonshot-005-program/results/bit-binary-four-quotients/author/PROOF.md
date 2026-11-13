# Four independent binary quotient dimensions are necessary for the q8 target

Status: new source-specific obstruction with exact finite evidence, pending
independent proof and implementation review. Do not treat this note as an
admitted theorem until that review is recorded.

## Exact scope

This extends the frozen17-savings theorem, not the all-V downset theorem.
It concerns scalar F2 fittings, the admitted monotone generated-cache source
interface WITHOUT Y feedback, and the specified q8 unit-refined movement
profile Q={1:1618}. At most three additional unit arrivals fit any finite
fixed-m caller for that profile. Different profiles, Y feedback, larger scalar
fields, and entangled block operators remain outside this result.

Let C be the canonical nine-dimensional binary code. If a fitting A completes
this interface, then

    dim_F2((rowspan(A)+C)/C) >= 4.                     (1)

This does NOT prove rank(A)>=13. It implies dimension>=13 only for a historical
code that actually contains C as well as the fitting rows. Arbitrary rank-ten
spaces that do not contain C are not classified by (1).

## A complete finite catalogue of large savings

For a nonzero coset h+C, let gamma(h) be the greatest total saving in the
ell_i row-arrival lower bounds obtainable using that ONE direction on any
set of rows; all other rows stay canonical. Each row may be chosen independently
for this algebraic upper bound. The17 theorem gives gamma<=17.

If gamma>=13, choose all positively improved rows and apply the gluing theorem.
There are at least seven such rows, so their binary normals span rank>=3.
This yields a binary representative g with support V, and all those fitting
rows have the unique form A_i=(1-g_i)K_i+g. The569-case envelope in the17
proof restricts (r,s,j) to the following forms:

- r=3, s=4,5,6, contained in an actual rank-three root flat;
- r=4, s=4 with at least one isolated root in V;
- r=4, s=5,6,7, consisting of an isolated root plus a subset spanning an
  actual rank-three flat orthogonal to that root;
- V is a mutually orthogonal set of size5,6,7 or8.

Here an isolated root in V is real-orthogonal to every other root in V.
For example the cases r=s=6,j=5 and r=s=7,j=6 force the entire set to be
orthogonal, so they are included in the last family. These assertions are
also checked by listing every envelope case with bound>=13. No form has
support larger than eight.

Every such V is enumerated. For its binary indicator g, put
M(V)=intersection_{j in V} T_j, J=M(V) intersect V, U=M(V) minus V.
The fitting rows indexed by M(V) are valid. Since s<=8, their exact positive
saving masks are

    two(V)=J,
    one(V)={i in U: a_i<=52+s},
    Gamma(V)=2|two(V)|+|one(V)|.

This enumerates38324 distinct classes with Gamma>=13:

| Gamma | Classes |
|---:|---:|
|13|20290|
|14|9988|
|15|6912|
|16|1122|
|17|12|

There is no ambiguity from changing a code representative. Distinct supports
of size<=8 cannot differ by a nonzero word of C, whose minimum distance is48.
If this coset had any additional positively improved row outside the listed
masks, apply gluing to the enlarged improving set. Its total saving is still
>=13, so the same envelope supplies another representative of weight<=8.
Uniqueness forces the same g, and the row formula forces the displayed masks.
Thus the catalogue records exact gamma and exact rowwise saving masks for
every high-saving coset. Lower-saving cosets need not be enumerated.

The generator enumerates all actual independent triple spans (as in the17
proof), all isolated four-subsets, all isolated-root extensions of rank-three
subsets, and all orthogonal cliques of sizes5..8. It makes6329841 support
candidate calls, with duplicates collapsed by the actual111-bit support.
The clique counts for sizes5..8 are77003,35667,9443,1094. These are exhaustive
fixed-source integer calculations, not a search over unbounded sizes.

## Two exact relations between high-saving classes

Call a class high if gamma>=14; there are18034 of them.

First, exhaustive pair comparison finds that the sum of TWO DISTINCT high
classes never has gamma>=13. If that sum were in the catalogue, the three
small representatives would sum to a codeword of weight<=24<48, hence to zero.
The comparison tests that exact XOR relation and finds none. Therefore

    gamma(a+b)<=12 for distinct high a,b.              (2)

In particular the high classes are sum-free in the quotient.

Second, the12 gamma17 classes are six-root rank-three flats. Their seventeen
one-saving row sets have pairwise intersections of size at least five
(exact pair histogram:5:8,6:8,8:30,9:1,11:19). A fitting assigns each row to
only one quotient direction. Thus at most ONE direction can actually save17;
every other direction saves at most16. This concerns attained row assignments,
not a false claim that the other cosets' individual gamma is smaller.

## Exhaustive dangerous-cap check

Suppose four distinct high classes sum to zero. They form an affine plane
inside their three-dimensional quotient span. The three remaining nonzero
directions are pair sums and each has gamma<=12 by (2).

If the sum of the four individual gamma values is<=63, their total assigned
savings plus the other three directions is at most63+36=99 already.
Only four-tuples with potential sum>=64 need checking. Such a tuple contains
at least two classes with gamma>=16: with at most one, the largest possible
sum would be17+15+15+15=62. There are1134 classes with gamma>=16.

The exact checker stores XORs of all pairs of those1134 classes and matches
every pair of high classes against them. It retains four distinct classes,
zero XOR, and potential>=64, and deduplicates sorted four-tuples. This covers
every dangerous cap, with no arbitrary search limit. It yields3989 caps.

For each cap, union its two-saving masks and its one-saving masks. Even granting
each row its best direction, the four high directions save at most

    2|union(two)| + |union(one) minus union(two)|.

The exact maximum over the3989 caps is46. The distribution is
{32:3935,41:12,42:14,43:4,44:3,45:18,46:3}. Thus every dangerous cap actually
saves at most46+36=82 after granting the remaining directions. The favourable
per-direction sum is never mistaken for a simultaneous construction.

The C++ checker uses exact111-bit masks in unsigned128-bit integers, retains
assertions, and reports632287 distinct top-pair XOR keys and23880 candidate
cap occurrences before deduplication. The Python source generator and both
small-source/rational proofs remain separately pinned. No compiled executable
is needed as a source artifact.

## Three-dimensional quotient spaces fail

Assume all fitting rows project into a binary quotient space of dimension at
most three. Extend that space to dimension three for an optimistic bound;
it has seven nonzero directions. By sum-freeness (2), at most four are high:
for a high a, the high set and its translate by a are disjoint subsets of the
eight-element group.

If there are at most two high directions, at most one can save17 and the
other saves at most16; all five other directions save at most13. Total saving
is at most17+16+5*13=98.

If there are three high directions, they are independent because they contain
no additive triple. Three of the other four are their pair sums, with gamma
at most12; the last has gamma at most13. Total saving is at most
17+16+16+3*12+13=98.

If there are four high directions, every four-point sum-free subset of the
seven nonzero elements of F2^3 is an affine plane. Their sum is zero; the
remaining three are pair sums. The dangerous-cap argument gives total saving
at most99. A direct eight-element enumeration also verifies this elementary
Fano-plane fact; it is not assumed for higher-dimensional spaces.

Consequently every such fitting satisfies

    sum ell_i(A) >=222-99=123.

The q8 profile has at most111+8+3=122 facet arrivals under its generous limiting
allowance. Every finite m therefore fails within this interface. At m6 only
one extra arrival fits, so the gap is larger. This proves (1) subject to the
stated exact finite premises and their independent verification.

The result says a binary code close to the canonical code in quotient dimension
cannot supply the target. It does not prohibit larger historical codes, new
noncommuting block representations, Y feedback, or a differently priced route
architecture. Every actual historical mode, all222 endpoint identities and
both strict suppliers still require construction. No new complete kappa.
