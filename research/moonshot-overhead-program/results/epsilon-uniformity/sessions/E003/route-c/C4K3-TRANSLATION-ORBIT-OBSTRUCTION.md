# C(4,3): exact optimum for whole translation-orbit partitions

Status: **proved finite optimum in the stated candidate family;
independent review pending**. Nonmaximal product rectangles are included.
The result does not exclude an asymmetric product-rectangle partition
or a partition with correlated sides of load five.

## 1. Candidate family and exact reduction

Identify the four letters with the additive group F2^2. The group
`G=(F2^2)^3` translates source and destination words simultaneously.
Consider disjoint partitions of C(4,3) into rectangles with product sides,
whose complete collection is a union of whole G-orbits. Orbit members
are distinct rectangles. This symmetry condition is additional to JR.

For a one-coordinate supported pair A,B, the possible side-size pairs are

    (1,1), (1,2), (2,1), (1,3), (3,1), (2,2).

Put `H={h:A+h=A and B+h=B}`. The orbit has `4/|H|` rectangles and
contributes constant source/destination loads `(|A|/|H|,|B|/|H|)`.
The six types give this exact description:

| Difference footprint D=A+B | Orbit loads | Best replacement |
|---|---:|---:|
| One nonzero letter | (1,1) | (1,1) |
| Two letters, one side singleton | (1,2) or (2,1) | (1,1) |
| Two letters, both sides size two | (1,1) | (1,1) |
| All three nonzero letters | (1,3) or (3,1) | Same |

Each orbit itself partitions the edges whose difference lies in D.
With a singleton side the difference representation is unique and H is
trivial. Two disjoint two-element subsets of F2^2 are cosets of the same
subgroup H of size two; each difference in D has |H| representations,
and quotienting translations by H makes each edge occur once.

Any two-element subset D of the three nonzero letters is a nonzero
coset of a size-two subgroup. Thus a (1,2) or (2,1) orbit can be replaced
by the (1,1) coset orbit with exactly the same covered edges. Neither
load increases. All these facts tensor across the three coordinates.

Consequently, after these replacements, the problem is exactly a
partition of the 27-point difference cube

    S=(F2^2 minus {0})^3, identified with [3]^3,

into Cartesian boxes. A coordinate projection of size one or two costs
(1,1); a full three-letter projection costs (1,3) or (3,1). A box with
d full coordinates and r source-heavy orientations costs

    (3^r, 3^(d-r)).                                                    (TO1)

These costs add because every whole orbit has constant vertex loads.
Disjointness of orbit edge sets is equivalent to disjoint difference
boxes. Correlated sides and incomplete orbits are outside this reduction.

## 2. No partition fits budgets (5,5)

A box with three full coordinates is impossible by TO1. A box with two
full coordinates must cost (3,3), and all remaining boxes then have no
full coordinates and cost (1,1). There can be at most two remaining boxes.
If the first box has size nine, 18 points remain, exceeding their total
maximum size 16. If it has size 18, each remaining box has its third
projection inside a singleton and hence size at most four; two cannot
cover the nine remaining points.

Now suppose every box has at most one full coordinate. There can be at
most two one-full boxes: their costs are (3,1) or (1,3). If there are two,
they have opposite orientations and leave budget for only one further
box. Each has size at most 12, and two size-12 boxes intersect because
every coordinate projection has size at least two in a three-letter
alphabet. Thus one has size at most six. Total size is at most
`12+6+8=26`, insufficient.

If there is exactly one one-full box, the heavier-side budget leaves at
most two other boxes. When its size is at most six, total size is at
most `6+8+8=22`. When its size is 12, any disjoint box with no full
coordinate needs a singleton projection somewhere, so has size at most
four; total size is at most `12+4+4=20`.

Finally, with no full projection anywhere, at most five boxes are
available. At most one has size eight: any two boxes with all projection
sizes two intersect. The rest have size at most four. Total size is at
most `8+4*4=24`.

These cases exhaust the possible costs, proving failure of budgets (5,5).

## 3. The optimum is six

Take all three letters in each of the first two coordinates, oriented
oppositely so their combined cost is (3,3). Partition the third coordinate
into a two-element set and a singleton. The two resulting difference
boxes each cost (3,3), giving load six. Their orbit lift has 96 rectangles
and partitions all 1,728 edges.

**Theorem TO.** Among partitions consisting of whole simultaneous
F2^2-translation orbits of product rectangles, the minimum common
per-side load for C(4,3) is exactly six.

The witness is the existing opposing-star construction on two coordinates
tensored with a binary first-difference partition on the third. The new
claim is optimality in the larger whole-orbit family, including every
nonmaximal product rectangle and every local subset choice.

An unrestricted optimum need not respect translation closure. Averaging
a partition over translations gives a weighted decomposition, not another
disjoint partition at the same load. The theorem therefore does not
obstruct general JR. A load-five construction must break this closure
or use correlated sides, or both.

## 4. Three complete cases for the broader product search

Without assuming orbit closure, a load-five product partition has total
incidence at most `2*64*5=640`. It covers 1,728 edges, so some rectangle
must satisfy

    |A||B|/(|A|+|B|) > 8/3;                                            (TO2)

otherwise its total edge count is at most `640*8/3<1728`.
Enumerating the six local size pairs above, the only product shapes
satisfying TO2, up to coordinate permutation and global side exchange, are

    ((2,2),(2,2),(2,2)),
    ((2,2),(2,2),(1,3)),
    ((2,2),(1,3),(3,1)).                                                (TO3)

All are maximal; the remaining partition rectangles need not be.
Coordinatewise alphabet permutations put the selected rectangle in the
canonical representative of `search_c4k3_fixed_rectangle.py`. Its three
cases therefore cover every product-rectangle load-five partition up to
automorphism. Each current run reached its time limit without a primal
certificate. Those runs do not exclude any case mathematically.

## 5. Verification and experiment boundaries

`verify_c4k3_translation_orbits.py` checks all 50 one-coordinate supported
subset pairs, including their stabilizers, exact orbit edge counts and
loads. It exhaustively checks the finite box-volume assertions, all 216
size-profile triples in TO3, and the 96-rectangle load-six lift. These
checks do not depend on a floating-point solver; the case split above
is a complete restricted impossibility proof.

The broader 125,000-candidate MILP and three symmetry-fixed variants are
inconclusive experiments. Their JSON files preserve status and time limits.
A separate complete affine-difference-set search at C(8,2) found a
verified load-nine partition with correlated sides. Its solver-reported
optimum is not promoted to an independently certified lower bound.

No finite example or restricted failure proves or refutes unbounded JR,
and none changes the admitted multiplication profile.

Credits: S004's opposing-star control and product search; E003 route C's
orbit reduction and finite obstruction; @CubeJerry; substantial AI assistance.
