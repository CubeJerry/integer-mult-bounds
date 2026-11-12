# Independent review: dyadic eight-packet identity and its physical boundary

**Accepted as an exact algebraic source identity. No physical supplier,
complete transfer protocol, new representation claim, or new kappa follows.**
The reviewer derives the identity in nine rational coordinates and checks its
integral eight-coordinate form without importing the author's code. The source
SHA256 is `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Every field statement is over a characteristic-zero coefficient field, with
its admitted complete-field tensor lift. Restricted integral/bounded input
domains require their actual contracts.

## Universal proof on all 120 ports

For a weight-three support S in coordinates 1,...,9, put
r(S)=1_S-(1/3)1. For a weight-seven vector missing i<j, put r=e_i-e_j.
Each vector has sum 0 and squared norm 2.

For distinct triples S,T, the inner product is |S intersect T|-1. Their
binary dot is odd exactly when the intersection has size 1. For a triple S
and missing pair {i,j}, the inner product is 1_(i in S)-1_(j in S). The
binary overlap is 3-|S intersect {i,j}|, odd exactly when both or neither
missing coordinate lies in S. For distinct missing pairs, the binary overlap
is 5 plus their intersection size, odd exactly when they are disjoint. In each
case the rational inner product is zero on odd binary pairs, and +/-1 on
even binary pairs. Diagonal inner products equal 2.

For zero-sum r, set t_k=r_k+r_9/2 for k<=8. Expanding the dot product gives
`t(r).t(s)=r.s`: the two cross sums contribute -r_9 s_9 and the eight repeated
quarter terms contribute +2 r_9 s_9. Therefore a=2 t, with
`a_k=2 r_k+r_9`, has squared norm 8 and off-diagonal products 0 or+/-4.
The fractions cancel into the proposed integer cases:

- Triple containing 9: +2 at the other two positions, zero elsewhere.
- Triple omitting 9: +1 on its three positions, -1 on the other five.
- Missing pair i<j<=8: 2 e_i-2 e_j.
- Missing pair {i,9}: +1 at i, -1 elsewhere.

The checker verifies all 7,140 pairs of the full 120-vector family as controls
of this complete case proof. The physical code uses integer/dyadic
coefficients; the proof's intermediate thirds require no division-by 3 service.

## Exact source binding

The active 104 ports consist of 70 weight-three and 34 weight-seven vectors.
`ports[k]` belongs to role `live[k]`; the port list is not indexed by the
possibly nonconsecutive role ID. The source chart is exactly {0,ports[k]},
the donor's terminal chart is F_2^9, and receiver live[k]+112 finishes in its
orthogonal hyperplane. All 890 donor/receiver MOVE incidences were checked:
donor route spaces contain the source line, and receiver route spaces stay
in its orthogonal hyperplane.

The omitted 16 members of the full 120 family are
`7,25,42,52,67,76,82,97,104,127,137,162,266,289,448,491`:
14 weight-three and 2 weight-seven vectors. The 104 integer rows have rank 8.
Source roles `0,1,2,4,5,6,9,12`, ports `11,19,35,131,259,13,69,41`,
form an 8-by 8 minor with determinant **-512**. This proves the rank of this
matrix, not a lower bound on every possible index code.

## What the packets do and what they require

Let B_k=sum_j a(v_j)_k q_j. The exact identity is

`q_i=(sum_k a(v_i)_k B_k)/8 - sum_(j!=i,v_i.v_j=0 mod 2) ((a(v_i).a(v_j))/8)q_j`.

Every receiver has exactly 48 orthogonal other ports. Its correction contains
48 signed half-coefficients, or 4,992 ordered correction terms in total.
The eight broadcasts have 520 nonzero scalar source contributions. These are
formula counts, not a complete ordinary-work or transport invoice.

The correction may be provided as one aggregate rather than 48 separately
stored fields. It must nevertheless be physically supplied. Broadcast
formation and placement, receiver distribution, correction acquisition,
raw target retention, common endpoint restoration, cache lifetimes and the
complete recursive tariff remain distinct construction obligations.

A concrete ambiguity prevents silently dropping side information. Set
q_0=1,q_1=-1,q_6=-1,q_7=1 and all other q=0. All eight packets vanish,
yet q_0 differs from zero. No decoder of the packets alone, including a
nonlinear one over this field domain, can recover every source input.
The adjacent timed-side-information review tests actual source access and
supplies stronger receiver-specific indistinguishability witnesses.

## Existing research and the complementary pattern

No novelty is claimed for the E8 rank-eight representation. Relevant prior
E8 research includes [#3040](https://github.com/CrocSwap/integer-mult-bounds/pull/3040)
and [#3045](https://github.com/CrocSwap/integer-mult-bounds/pull/3045).
Their stated rigidity and square-decoder bounds are not reproved or used as
a physical broadcast service here. Examined source heads appear in
EXTERNAL-SOURCES.json.

[#7014](https://github.com/CrocSwap/integer-mult-bounds/pull/7014), examined
at head `949c0ada285aae619468ae49317c8d9f4df130f7`, imposes zeros on **even**
binary pairs and gives a rank 13 factorisation of that window. Its port list
matches the active native ports in exactly the same order. This code imposes
zeros on **odd** binary pairs. Ports 19 and 11 have even binary product but
Gram entry 4, immediately violating that PR's mask. Rank 8 here neither
improves nor contradicts its rank 13 result; the two interfaces must not be
identified. The PR remains open at the time examined.

## Controls and admission

The standalone checker authenticates the source, compares the independent
nine-dimensional derivation to all integer rows, and verifies the source
minor and 104 complete symbolic decoder rows. Changing a code coefficient
is rejected; omitting a coordinate breaks this displayed Gram decoder;
applying the complementary mask is rejected. None of these controls asserts
that every seven-packet code is impossible.

The identity is a precise target for a physical aggregate supplier. The
failure of a particular source graph does not invalidate its algebra, while
the algebra does not establish that the graph supplies its missing records.
All foundational assumptions and the complete kappa status remain unchanged.

Prepared for @CubeJerry by the S006 adversarial worker with OpenAI assistance,
crediting the retained native, E8/root-code predecessors, and the root's
proposed dyadic physical interface.
