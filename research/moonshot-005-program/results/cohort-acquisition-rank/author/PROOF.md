# Cohort-order filtration for sparse physical acquisition

**Proved universal linear-algebra theorem. Its physical use requires the
specified fixed global row space and actual acquisition support. Packet counts
are not automatically global row-space dimensions. No new kappa.**

Let a field k, a width V>=1, and n independent source blocks x_j in k^V be
given. Partition the n indices into nonempty cohorts C_1,...,C_m. Let P be an
nV-by-nV block matrix and U be block diagonal by cohorts, with arbitrary
V-by-V internal coefficients. U may be singular, and its blocks need not
commute. Assume P[C_i,C_i]=0 for every cohort. For acquisition row block j
in C_i, let S_j be the set of other source cohorts on which P[j,*] is nonzero,
and write s_j=|S_j|. Define

    A=I-UP,    r=rank(A).

For any linear order pi of the cohorts, call row block j good when its target
cohort precedes every cohort in S_j. An empty S_j is good for every order.
Let g(pi) count good row blocks. Then

    r >= V max_pi g(pi)
      >= V ceil(sum_(j=1)^n 1/(s_j+1)).                  (1)

In particular, if every s_j<=k, then

    r >= V ceil(n/(k+1)).                              (2)

## Proof by an actual kernel filtration

Fix an order and relabel cohorts accordingly. Put Z=ker(A), and for i=0,...,m
let Z_i be the subspace of Z with coordinates on all cohorts after i equal
to zero. Thus Z_0=0 and Z_m=Z. Projection of Z_i onto the coordinates of C_i
has kernel exactly Z_(i-1), so its image dimension is

    dim Z_i - dim Z_(i-1).

For x in Z_i, the identity A x=0 gives x[C_i]=U_i (P x)[C_i]. Every good
acquisition row in C_i has all its source cohorts after i, and therefore its
row block of P x vanishes. If b_i rows in C_i are bad, the remaining vector
(P x)[C_i] lies in a coordinate subspace of dimension b_i V. Applying even a
singular U_i cannot increase that dimension. Hence

    dim Z_i - dim Z_(i-1) <= b_i V.

Summing and using sum_i b_i=n-g(pi) gives dim Z<=V(n-g(pi)). Rank-nullity
proves r>=V g(pi). This argument neither inverts U nor discards nuisance inputs.

In a uniformly random cohort order, the target cohort of row j is first
among itself and its s_j distinct source cohorts with probability1/(s_j+1).
Linearity of expectation gives E[g]=sum_j1/(s_j+1), even though the row events
may be dependent. Some order attains at least the ceiling of that expectation.
This proves (1) and (2), over finite fields as well as infinite fields, with
no field extension and no commutativity premise.

## Exact scope and sharpness

Suppose a proposed source supplies an nV-by-nV global correction G plus the
cohort-local contribution UP, so that I=G+UP. Then G=A and its row-space
dimension must obey (1). If all actually available global X histories span
at most qV dimensions, q>=ceil(sum_j1/(s_j+1)) is necessary. If those histories
change during a packet trajectory, their aggregate rank may exceed the
number of physical packets. Such a source must use its actual historical
row space here; it is not excluded merely by counting its packet records.

For k=1 and n=111, (2) requires rankG>=56V. Even one source COHORT per acquisition
row, possibly containing many source coordinates, is subject to this bound.
This is stronger than counting one original source point per row. In a
q=8,9,10 fixed-global-mode model, the maximal source-cohort support must thus
be at least13,12,11 respectively. These are bounds on the maximum support;
they do not assert that every row has that many supports. The heterogeneous
sum in (1) is a more informative screen.

The constant in (2) is attained as a general algebraic bound. Partition the
n singleton cohorts into groups of size k+1, with one smaller remainder.
Set U=I and P=I-J separately on each group, where J is its all-ones matrix.
Then A is the direct sum of those J matrices. Every row sees at most k other
cohorts, and rankA=ceil(n/(k+1))V after tensoring with I_V, over every field.
This is an algebraic sharpness construction, not a physical native-word
compiler or a favorable invoice.

For the complex source's fourteen independent parity pairs, every row's
source cohort is the opposite half. Optimizing the order separately for
each disjoint pair gives max_pi g(pi)=sum_pairs max(|C|,|C*|)=14*4=56.
Thus the exact56V parity locality gate is also a special case of (1), agreeing
with its separate direct principal-block proof.

## Rectangular paid acquisition extension

If cohort i instead has b_i acquisition row blocks for n_i target row blocks,
let U_i have shape n_i V by b_i V and P_i have b_i V rows. Preserve the same
absence of source support in the target cohort. Put b=sum_i b_i, n=sum_i n_i,
and define good rows as above. The identical filtration gives

    rank(I-UP) >= V (n-b+max_pi g(pi))
      >= V (n-b+ceil(sum_(j=1)^b 1/(s_j+1))).           (3)

The right side may be negative, in which case rank nonnegativity is stronger.
Additional real acquisition carriers/observations change b and must be priced;
they are not silently treated as the n existing target carriers. If every
s_j<=k, a necessary fixed-global-mode screen is q>=n-b+ceil(b/(k+1)).

## Provenance and classification

Worker C identified the sparse-cohort acquisition problem and a displacement-
rank approach. Root supplied this stronger cohort-order kernel filtration and
the rectangular extension. The displacement proof remains a useful independent
weaker check, not the basis of (1). Independent adversarial review and finite
controls are recorded separately. All ordinary, owned, physical/compiler,
precision, strict supplier and recursive requirements remain. @CubeJerry;
OpenAI assistance. No complete conditional or unconditional kappa is claimed.
