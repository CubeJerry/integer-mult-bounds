# A parity-specific weighted rectangle gate for the Fourier branch

Status: **proved reduction and exact obstruction; the proposed small-load
family remains open**. This is a separate sufficient Fourier component,
not a new unconditional multiplier. It records why solving every exact
coordinate-inequality graph is stronger than what this branch requires.

Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, complete
Fourier `build/kernel.tex`, especially the weighted routing-block identity,
binomial charged decomposition and arbitrary cross-orthogonal endpoint proof.
The S004 both-profile JR transfer and heterogeneous invoice barrier are
preceding local notes. Coefficients in this note are rational, not reduced
into the characteristic-two data algebra of the interchange branch.

## 1. The weaker finite target

For even L>=2 and q=2^t let labels be [q]^L, N=q^L, and put

    O(v,w)=1 if Delta(v,w) is odd, and 0 otherwise.

A permitted rectangle A x B has O=1 on every cross pair. Unlike a
partition, an exact weighted representation may overlap:

    O=sum_R alpha_R 1_(A_R) 1_(B_R)^T,   alpha_R in Q.      (PW1)

Its local load counts nonzero summands containing a vertex on a specified
side, without weighting by the magnitude or sign of alpha_R. Every claimed
load is a maximum on each side separately.

**OWL.** There is one absolute c>=2 such that for every t and even L,
PW1 has maximum side load at most c^L(t+1)^c.

JR implies OWL by applying its disjoint partitions separately at each odd
unequal-position set and common outside word. The load is at most
(1+c)^L(t+1)^c. No converse is established. OWL asks only for one
parity graph and allows exact rational cancellations; JR asks for exact
disjoint partitions of every all-coordinate-unequal graph.

The hypothesis deliberately specifies exact coefficients. A cheap ordinary
cover supplies no equality in PW1, even though every permitted rectangle
has the right zero support. Coefficients cannot simply be declared to
exist from coverage.

## 2. Transfer to the source's weighted free matrix

Retain the source polynomial

    p(k)=product_(h=1)^(L/2)(1-k/(2h)),
    P(v,w)=p(Delta(v,w)),
    p(k)=sum_(j=0)^(L/2) c_j binom(L-k,j).

Its integer values and c_j are dyadic. Since p(0)=1 and p vanishes
at all positive even distances,

    I-P = - O entrywise-multiplied-by P.                    (PW2)

**Lemma PW1.** If PW1 has side load lambda, then I-P has a weighted
cross-orthogonal rectangle decomposition with side load at most

    lambda sum_(j:c_j!=0) binom(L,j) <=2^L lambda.           (PW3)

Proof. Each charged binomial term is a sum of equality cylinders:
fix j positions S and their common word a, obtaining C_(S,a) x C_(S,a).
For every weighted rectangle A x B in PW1, intersect both sides with
this cylinder and assign weight -alpha_R c_j. Empty pieces are discarded.
Intersections remain inside the odd-distance graph, hence their binary
Gram cross values Gamma=1-Delta are zero. Summing gives PW2 exactly.

For a fixed vertex and a fixed S, its common word a is determined. Thus
it belongs to at most one of these intersections for each S. Multiplying
by its original lambda incidences gives PW3; no factor q^j enters this
*local* count. QED.

The charged matrix P and its charge count are unchanged. Arbitrary
correlated sides satisfy the source's shared endpoint proof. Coefficient
heights and a constructor are justified separately below. Consequently
OWL alone yields the same improved Fourier local profile as JR:

    sigma_m/W_m <= sqrt(A_m) 2^{O_c(sqrt(log m))}.

Choose L=Theta(sqrt(log m)) and log q=2+ceil(2log(m)/L), exactly as in
JRT5--JRT8. This is a Fourier component. The current unchanged interchange
profile still dominates the complete unconditional logarithmic envelope.
A separately improved interchange interface is needed to obtain the
log-free global 2/3 envelope; OWL does not provide one.

## 3. Rational coefficient heights need not be a second hypothesis

Suppose some real weights on an allowed support list of R rectangles
solve PW1. Regard their incidence vectors as columns of an N^2-by-R
zero-one matrix A. The right-hand side is the zero-one vector O.
Choose a basis of columns that spans O and a nonsingular set of rows
for that basis. If its size is r<=R, the resulting r-by-r matrix and
all its Cramer replacements have zero-one entries.

Hadamard's determinant bound gives numerator and denominator magnitude
at most r^(r/2). Thus this same support list has rational coefficients of
bit height O(R log(R+2)), with zero coefficients removed if needed.
The local load never increases. Real solvability here is equivalent to
rational solvability because the linear system has rational coefficients.
No numerical conditioning argument or floating-point solution is needed.

Under OWL, R<=N lambda, since every rectangle has a nonempty source side.
At the chosen Fourier parameters N<=m^3 eventually and lambda=m^o(1),
so R, all support bitmaps and all coefficient bit heights are polynomial m.
Multiplying by c_j adds only O(L log(L+2)) bits. The admitted exact rational
record-scaling and polynomial norm-gain suppliers therefore apply after
enlarging their fixed exponent. A coefficient of large absolute magnitude
is not treated as a unit-norm operation.

These new weights may have odd denominator factors. This reduction is for
the rational numerical Walsh branch, where the exact operator identities
extend from Z[1/2] into Q and the admitted short-rational scaling primitive
accepts every supplied rational denominator. It does not claim a circuit
whose coefficients all remain in Z[1/2], nor any characteristic-two
specialization of these weights. The output operator is still the exact
rational normalized Walsh matrix before numerical rounding.

There is also an explicit bounded constructor. Enumerate all support lists
of length at most N lambda, with each side encoded by N membership bits.
Reject a list unless every rectangle is inside O and both loads obey the
bound. Solve its exact rational linear system and verify PW1. The first
successful list is retained as a compact plan. Enumeration takes
2^{m^{C_c}} time and polynomial-m workspace; an unsuccessful finite
search returns failure, so the constructor halts even without OWL.
Only preflight performs this search. Runtime reads the polynomial compact
list with charged scans, and never enumerates supports per data record.

## 4. Full rational rank blocks the shortest-cover shortcut

**Lemma PW2.** For homogeneous q>2, rank_Q O=N. For q=2 it is two.

Proof. Put M_q=2I_q-J_q. Its entries are +1 on equality and -1
on inequality, hence

    O=[J_N - M_q^(tensor L)]/2.                            (PW4)

Over Q, M_q has eigenvalue 2-q on the constant line and 2 on its
(q-1)-dimensional zero-sum complement. For q>2, every tensor eigenvalue
is nonzero. On a tensor space with at least one zero-sum coordinate,
J_N acts as zero, so O has a nonzero eigenvalue. On the all-constant
line its eigenvalue is [q^L-(2-q)^L]/2, also nonzero. Hence rank N.

For q=2, M_2 has rank one, on the all-contrast direction. J_N has
rank one on the distinct all-constant direction. PW4 therefore has rank
exactly two. Equivalently it is the two complete directed rectangles
between even and odd binary parity classes. QED.

It follows that any exact rational weighted rectangle representation for
q>2 has at least N nonzero summands. In particular a cover with fewer
than N pieces cannot be made exact by choosing weights. OWL permits
R up to N lambda and is not disproved by this rank bound. The required
progress concerns local load and support structure, not merely finding
one small cover.

For heterogeneous q_i, the same calculation gives full rank N when all
q_i>2. If at least one q_i=2, the rank is

    1+product_(i:q_i>2) q_i.

The tensor product term annihilates the all-constant line and has the
listed product rank; the separate J_N term contributes one dimension.
This makes another explicit distinction between characteristic-zero rank
and the much smaller binary Gram rank from HF4.

## 5. Exact finite checks

`verify_parity_weighted_fourier.py` and its JSON receipt verify 8,720
weighted identity entries across five families. The input representations
have actual overlapping rectangles, negative coefficients and coefficients
with odd denominators; exact rational arithmetic checks their conversion
to I-P and the per-vertex load bound. The binary parity examples include
rectangles containing more than one odd Hamming distance, so this is not
just a replay of the exact-distance construction. Omitting the multiplier
p rejects 3,176 entrywise controls.

Eight exact modular rank computations, at a checked good odd prime, agree
with PW2 and its heterogeneous extension, including a full-rank 256-label
case. The checker imports helpers from the two earlier Fourier checkers.
These finite tests verify the reduction on examples; they do not establish
the open OWL load bound or execute a tape multiplier.

## 6. Falsifiable next gate and current limits

A useful next result would give explicit allowed supports with local load
exp(O(L)) poly(t), then solve and verify their weighted incidence equation.
Support enumeration for small parameters can reject a candidate family,
but a finite optimum cannot establish OWL. The rank test should precede
an expensive weight search: R<N is immediately impossible for q>2.

The known first-difference partition solves PW1 with the larger load
sum_(odd k) binom(L,k)t^k. The heterogeneous invoice theorem shows why
its literal profile does not reach the improved square-root logarithm.
Thus this reduction does not hide the missing combinatorial work in an
unpriced coefficient oracle: the open part is now exactly a bounded-load
linear-span problem with explicit finite certificates.

Credits: the pinned source weighted rectangle identity and endpoint proof;
S004 lead's JR hypothesis and both-profile transfer; E002 rational scaling,
compact execution and precision; @CubeJerry; substantial ChatGPT research
assistance. No unconditional new multiplication bound, formal refinement,
human referee certification or literature priority is asserted.
