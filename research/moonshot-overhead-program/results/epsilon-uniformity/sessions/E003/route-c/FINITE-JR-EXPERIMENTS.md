# Finite JR experiments: exact certificates and inconclusive searches

Status: **bounded experiments completed; no unrestricted JR improvement**.
The exact restricted theorems are in `MAXIMAL-RECTANGLE-OBSTRUCTION.md`
and `C4K3-TRANSLATION-ORBIT-OBSTRUCTION.md`. This note records the other
searches, including their unsuccessful outcomes, and an alternative
correlated-side construction family.

## 1. Affine partitions of the difference set

Identify `[2^t]` with F2^t and let

    G=(F2^t)^k,       S=(F2^t minus {0})^k.

Suppose S is partitioned into affine subspaces `a_r+W_r`, r=1,...,M.
For every coset u+W_r of W_r in G, form the rectangle

    (u+W_r) x (u+a_r+W_r).                                             (AD1)

These rectangles partition C(2^t,k) and have load exactly M at every
source and every destination. Indeed, an edge has difference x+y in
exactly one affine part. Within that part, the source x chooses exactly
one coset u+W_r, and its destination lies in u+a_r+W_r. Conversely any
cross pair in AD1 has difference in the supported set a_r+W_r. Each
vertex belongs once on each side for each part. The total rectangle count
is `sum_r |G|/|W_r|`.

The subspaces W_r may mix the k coordinate blocks, so AD1 can have
correlated sides. This is a genuine candidate family beyond tensoring
one-coordinate partitions, but it is still a restriction of general JR.
An affine *cover* of S does not suffice: overlaps produce the same edge
multiplicities in AD1. The construction above requires a partition.

### Complete small candidate enumeration

At t=3,k=2, the search enumerated all 2,825 linear subspaces of F2^6 and
all their distinct cosets contained in S. There are 5,929 such affine
parts. A set-partition MILP returned a nine-part solution, with part
sizes

    1, 2, 2, 4, 4, 4, 8, 8, 16.

The exact certificate is `affine-difference-q8-k2.json`. Its lift has
196 rectangles, common load nine, and 160 sides that are not coordinate
products. All 3,136 graph edges are covered exactly once. The accompanying
standalone checker validates the listed direction subspaces, cosets,
support, coverage, incidences and nonproduct counts without invoking a
solver.

The solver reported optimality with a floating-point lower bound very
close to nine. This report is retained as computational evidence only.
No exact dual or branch certificate has been extracted, and no theorem
that nine is the restricted optimum is asserted here. The verified
upper certificate does not improve the binary product load nine; the
unrestricted opposing-star partition already has load seven at C(8,2).

## 2. C(4,3), load five: all searches remain inconclusive

The known opposing-star/binary product has load six. The following
searches attempted to improve it.

| Search | Candidate rectangles | Limit | Actual outcome |
|---|---:|---:|---|
| All product rectangles, cap five | 125,000 | 90 seconds | Time limit; no primal certificate |
| Fixed balanced maximal rectangle | 109,375 remaining | 300 seconds | Time limit; no primal certificate |
| Fixed two-balanced/one-star rectangle | 113,125 remaining | 300 seconds | Time limit; no primal certificate |
| Fixed balanced/opposing-star rectangle | 115,975 remaining | 300 seconds | Time limit; no primal certificate |
| Smaller structured family, exact load-six warm start | 17,576 | 600 seconds | Time limit; load six retained |

The three fixed cases are exhaustive up to automorphism for a hypothetical
load-five product-rectangle partition, by the efficiency argument proved
in the translation-orbit note. Their unsuccessful time-limited searches
do not establish failure of any case.

The last run included all coordinate cuts that are maximal or
singleton-versus-singleton. It minimized the common load subject to exact
partition constraints and the valid global rectangle-rank cut R>=64.
It used the known 96-rectangle load-six partition as an exact incumbent.
The solver returned objective six and lower bound five, after zero
completed branch nodes. This leaves precisely the sought improvement
unresolved even in that smaller family. The returned upper certificate
was checked by integer edge and incidence counts.

JSON receipts preserve each status, time limit, candidate family and
certificate. No timed-out run is called infeasible, and no solver claim
for a restricted family is generalized to arbitrary correlated sides.
The finite search was stopped after this bounded sequence.

## 3. What the completed results establish

The exact whole-translation-orbit product family has optimum six, so a
load-five partition must break that symmetry closure or use correlated
sides. All-maximal rectangles are also insufficient: their exact
two-sided tradeoff forces common load at least `ceil(sqrt(27))=6`.
Neither restriction prevents sufficiently thin asymmetric rectangles.

The affine-difference family supplies a concrete way of generating
correlated supported rectangles with an exact edge identity. Its first
complete small search gave no improvement. There is no unbounded family
proof, no unrestricted finite optimum, and no changed multiplication
overhead from these experiments.

One primary literature lead was read during the search: Josh Alman and
Baitian Li, *Kronecker Powers, Orthogonal Vectors, and the Asymptotic
Spectrum*, arXiv:2509.14489, Sections 3.2 and 6. Their partitioning
degree measures match local rectangle incidence, and their symmetry/hole
fixing results rebalance tensor-power partitions. They do not by
themselves supply the uniform finite partition family required by JR as
q varies. No bound from that paper is imported into a programme theorem.
Primary source: https://arxiv.org/pdf/2509.14489 .

Credits: S004's crown-graph formulation and finite product search;
the cited literature for terminology and a potential future mechanism;
@CubeJerry; substantial AI-assisted experimentation. No priority claim.
