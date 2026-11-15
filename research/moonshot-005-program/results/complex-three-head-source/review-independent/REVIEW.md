# Independent three-head source and component review

**Source/interface and scoped one-query argument checked. No caller or new
kappa.** Root's separate SymPy implementation reconstructs the eight-coordinate
Gaussian matrices without author imports. It verifies the three ordinary
permutation gauges, all twelve powers of the common head, and the field-level
minus at tensor width two. All coefficient identities are multiplicative,
so these finite controls accompany an all-width algebraic proof.

## Source and cost boundary

For the cycle a->c, b->a, c->b, S C_b S^-1=C_a and S^3=I. Thus
R=C_a^-1 S C_b S=S^2 and B=C_b S. The original source coefficient identities
give the two blocks [[B,0],[I,B]] and [[B,-B^2],[0,B]], exactly. The body
directions remain disjoint. B^3=C_a C_b C_c, B^6=X_a X_b X_c, and B^12=I.
The Gaussian rank sequence modulo six is 0,1,2,3,2,1.

Adding the spectator line to every real source chart preserves every chart
inclusion and every MOVE rank difference, and preserves all ADD cocharts.
It tensors the operator with the spectator identity. The ambient array volume
grows by 2^V on source and target sides. That common factor may be retained
in the normalized rank moment, but actual compilation must account for the
larger arrays and new descriptor/layout constants. Three actual ordinary
coordinate permutations are added per half. No new owner or Gaussian call is
hidden by this source lift. This is not itself a supplier-admission theorem.

## One-query component proof

Root checked the author's proof using the filtration F_j spanned by Gaussian
rank at most j in a sufficiently large faithful fixed Clifford tensor algebra.
The binary symplectic rank inequality gives F_j F_k subset F_(j+k), and each
rank component is an ordinary bimodule. With one rank-one query after the
native, every affected-row coefficient L,M before the native's last factor
belongs to F_1. The active columns are LA and -LA^2+MA, with r(A)=1.
If the whole word has zero rank-two component, pi_2(LA)=0. Since LA belongs
to F_2, it then belongs to F_1. Both (LA)A and MA belong to F_2. No rank-three
component survives in the affected row, and the other rows already belong to
F_2. Invertible ordinary outer encodings preserve both zero components and
nonzero component rank by bimodularity. The transpose reduction for a query
before the native preserves Gaussian rank and monomial ordinary maps; a role
swap restores upper triangular form. Inverse and cross-identity orientations
are covered. Thus endpoint(3,1) is excluded within this one-query model.

The inherited one-native low-component compression theorem also generalizes
immediately to any fixed number of heads: N_low=(pi_0+pi_1)N is invertible,
so the number of endpoint jobs of rank at least two is at most the number of
one-role queries, regardless of query rank. In particular endpoint(3,2) needs
at least two such queries. The algebraic argument, not a one-column test,
establishes this conclusion.

## A three-head reflection potential

This is an additional root lemma for assessing the new inventory. On the
28 odd quadratic refinements of F_2^6, group forms by their nonzero restriction
to the computational Lagrangian L. There are seven groups of four. Let E_L
be orthogonal projection onto the functions constant on each group, and set
P_L=2E_L-I. Every computational-monomial symplectic map preserves this
partition, so its permutation representation commutes with P_L.

For two Lagrangians L,M with Gaussian distance r, the intersection of the two
spaces of partition-constant functions has dimension equal to the number of
connected components of their bipartite incidence graph. A symplectic basis
puts M in the form obtained by exchanging r computational x/z axes. The two
restriction labels share a tail w of length 3-r. Each nonzero w gives one
complete bipartite connected component. When w=0, the two nonzero r-bit labels
alpha,beta must satisfy alpha dot beta=1. This graph is connected: for r>=2,
any two distinct nonzero alpha have a common beta solving the two independent
linear equations; r=1 is a single edge. Thus for r>=1 the component count is
2^(3-r). For r=0 both partitions agree and the dimension is seven.

Two orthogonal projectors of equal rank seven obey
rank(E_L-E_M)=2(7-dim(im E_L intersection im E_M)). Consequently the
permutation pair rho and P_L rho P_L has difference ranks

    r=0,1,2,3:   0,6,10,12.

The phase-safe auxiliary tensor lift used in the full two-head theorem carries
this pair to the same physical Clifford algebra. Native square-block
factorization then gives the three-head necessary inequality

    sum_i f(r_i) <= 6m + sum_j f(query_rank_j),
    f(0)=0, f(1)=3, f(2)=5, f(3)=6.

This is not the earlier linear head-rank conservation. It neither constructs
a caller nor proves a saving. The checker tests all four canonical rank
representatives and generators of the full monomial symplectic subgroup; the
partition/intersection argument proves the all-group statement.

Combining this potential with the component gate excludes every rank-three
endpoint for one native and one rank-one query: any additional rank-two job
would already exceed potential nine, while without rank-two endpoints the
component gate forbids rank three. For a single rank-two query, the low-rank
compression count excludes(3,2). Surviving multiple-query inventories still
need an actual caller and a complete invoice.

## Verification

`check.py` writes `RESULT.json`. Expected status
`PASS_INDEPENDENT_THREE_HEAD_GAUGE_AND_ODD_REFLECTION`.
The runtime used Python 3.12 and SymPy 1.14.0. The checker rejects tensoring
the field-level source minus. It does not assert that its four representative
checks alone prove all-group or all-width claims.

Credit @CubeJerry, the actual source/compiler and tensor-rank authors,
Worker B's spectator/gauge and component proof, and root's separate source
checks and odd-reflection extension, with substantial OpenAI assistance.
All five foundations remain; no complete source caller/supplier or new kappa.
