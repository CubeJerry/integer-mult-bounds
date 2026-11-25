# Exact local-load gates for the joint inequality graph

Status: elementary component proof; independent review requested. This note
neither establishes nor refutes JR and gives no new complete multiplier.

Let C(q,k) have a left and a right copy of [q]^k, with x adjacent to y iff
x_i != y_i for every coordinate. A valid rectangle A x B is any nonempty
biclique; its two sides may be arbitrarily correlated subsets of [q]^k.
Let ell_L, ell_R bound the maximum per-vertex incidence on the two sides
in a rectangle cover. A partition is a cover with every edge used once.

## 1. The incidence quantity is a sparse exact factorization

For a family indexed by a finite set U, define S_x={u:x in A_u} and
T_y={u:y in B_u}. It is an exact partition precisely when

    |S_x intersect T_y| = product_i [x_i != y_i].                 (JL1)

The side loads are max_x |S_x| and max_y |T_y|. This equivalence follows
by counting the rectangles containing each pair; it includes arbitrary
correlations and requires no common coloring of the rectangles. Conversely
any such set system defines its rectangles by incidence and is a partition.
The universe size and side loads are different parameters.

Over Q the adjacency matrix is (J_q-I_q) tensor-powered k times. Each
factor has eigenvalues q-1 and -1, so the rank is q^k. Every rectangle has
rank one. Thus any exact partition, or any exact weighted rank-one sum,
uses at least q^k nonzero rectangles. This does not lower-bound local
load by q^k: a label can occur in very few of a large number of rectangles.
A Boolean cover is not an exact weighted sum merely because it covers.

## 2. Universal side-load bounds, valid even for covers

**Theorem JL2.** Every valid rectangle cover satisfies

    sqrt(ell_L ell_R) >= [2(q-1)/q]^k,                         (JL2)
    q <= binom(ell_L+ell_R, ell_L).                            (JL3)

In particular, a common load ell obeys

    ell >= max(ceil([2(q-1)/q]^k), (log2 q)/2).                (JL4)

Proof of JL2. Let a_u=|A_u| and b_u=|B_u|. For each coordinate, the
coordinate projections of A_u and B_u are disjoint: otherwise one may
choose an element from each side having the same coordinate, contradicting
validity. If their projection sizes are a_i,b_i, then a_i+b_i<=q and

    a_u b_u <= product_i a_i b_i <= (q^2/4)^k.

This holds for correlated sides too. Set M=(q/2)^k. Since sqrt(a_u b_u)
<=M, Cauchy--Schwarz and the side-incidence budgets imply

    q^k(q-1)^k <= sum_u a_u b_u
               <= M sum_u sqrt(a_u b_u)
               <= M sqrt((sum_u a_u)(sum_u b_u))
               <= M q^k sqrt(ell_L ell_R).

The first inequality uses only coverage; no disjointness assumption is
needed. Rearranging gives JL2.

Proof of JL3. Restrict to diagonal words d_a=(a,...,a), a in [q], which
induce the crown graph. Put S_a=S_(d_a), T_a=T_(d_a). We have
S_a intersect T_a empty and S_a intersect T_b nonempty for a!=b. Choose a
uniform random ordering of the finite universe. Let E_a be the event that
all of S_a precedes all of T_a. Its probability is
1/binom(|S_a|+|T_a|,|S_a|). Distinct E_a,E_b are disjoint: take
u in S_a intersect T_b and v in S_b intersect T_a. The first event forces
u before v, while the second forces v before u. Therefore the sum of
these probabilities is at most one. Monotonicity of binomial coefficients
in each of their two size arguments gives JL3. Finally
binom(2ell,ell)<=4^ell gives JL4. This is the classical set-pairs argument,
reproduced here for the exact family; no new general inequality is claimed.

The exponential-in-k and logarithmic-in-q necessities are consistent with
JR. For any fixed candidate constant c<2, JL2 rules out a bound
c^k poly(log q) uniform in k and q: fix q sufficiently large that
2(q-1)/q>c, then let k tend to infinity. The recorded JR explicitly allows
c>=2. These bounds do not exclude its stated exponential base and fixed
polynomial logarithmic factor.

## 3. The small certificate has an exact optimality proof

There is a simple partition of C(q,2) into q^2 rectangles indexed by
(a,b) in [q]^2:

    A_(a,b)={(x,b):x!=a}, B_(a,b)={(a,y):y!=b}.                (JL5)

An edge ((x1,x2),(y1,y2)) belongs to exactly the rectangle (y1,x2).
Both side loads are q-1. At q=4 this is the previously saved 16-rectangle,
load-three certificate. JL2 gives ell>=ceil(9/4)=3; hence its load is
optimal among all rectangle covers, including correlated sides, and its
16 rectangles also attain the rank lower bound for an exact partition.
The solver is unnecessary for this conclusion. At q=3 the same argument
gives optimal common load two. This is a small exact statement, not JR.

Taking products of the q=4 two-coordinate partition and, if needed, one
ordinary q=4 first-difference partition yields for every k

    ell(C(4,k)) <= 3^(floor(k/2)) * 2^(k mod 2).               (JL6)

The edge-unique product construction multiplies local loads. It improves
the exponential constant relative to 2^k for this fixed alphabet; it does
not address the growing-alphabet logarithm that motivates JR.

## 4. A related primary-source lead, with its limit

Block, Branzei, Maji, Mehta, Mukherjee and Nguyen, *P4-free Partition and
Cover Numbers & Applications*, ITC 2021, DOI 10.4230/LIPIcs.ITC.2021.16,
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITC.2021.16,
studies partitions into unions of vertex-disjoint bicliques. The lead read
its introduction, Theorem 8, Sections 5.1/5.4/6.1 and Section 7. Such a
partition into d subgraphs implies a local rectangle partition of load at
most d. Their inequality-graph result and product inequality reproduce
an available (log2 q)^k upper bound here; they do not prove JR. Their graph
embedding parameter counts global coordinate classes, whereas JL1 only
bounds the memberships at each individual vertex. No equivalence of those
parameters, or reverse transfer of their lower bounds to local load, is
asserted.

Pinto, *Biclique Covers and Partitions*, EJC21(1)P1.19 (2014),
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i1p19/pdf/,
provides the established local-cover/partition terminology and crown
lower-bound context. The lead inspected its definitions and the crown
argument in Section 4. The proofs above are supplied directly. No
exhaustive literature search or originality claim is made.

## 5. Decision

The finite example is fully explained and optimal. It cannot be promoted
to the growing-q hypothesis. Exact partition existence remains the useful
open combinatorial gate. Future constructions must provide JL1 and small
side memberships simultaneously; a small Boolean cover, a low global
rank or a finite solver instance does not do so.

Credits: @CubeJerry; pinned OpenAI endpoint geometry motivating JR;
classical set-pairs/rank methods and the cited graph literature; substantial
ChatGPT research assistance. No full tape execution or formal proof.
