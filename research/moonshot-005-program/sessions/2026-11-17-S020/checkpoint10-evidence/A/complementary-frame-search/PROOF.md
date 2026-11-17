# A scoped obstruction to three binary complementary-frame meeting rounds

**Accepted premises, exact finite certificate, no general supplier claim.**
The attempted eight-receiver module cannot supply all eight own-frame triples
using one native-unit seed per record and three actual cross-frame matching
rounds of invertible binary two-record maps.

## 1. Source, demands, and exact scope

The admitted full-half reservoir word has SHA256
`6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980`,
cut1893. Its frames A=[14,17,19,20] and B=[96,99,101,102] comprise eight
nonzero pairwise orthogonal real native lines and thus an ambient basis.
The actual NATIVE_i fields are pure x_i at L_i; all eight Y records are at
ground. The checker authenticates the roots and admitted cut inventory and
checks these facts. Existing axis preloads contain none of these eight inputs.

The desired new A_i correction is the sum of the other three A inputs;
the desired B_j correction is the sum of the other three B inputs. Arbitrary
cross-frame terms may remain. Original Y variables are arbitrary and must
be restored exactly.

The module permits arbitrary invertible preconditioning of these eight Ys,
exactly one pure native-unit read per Y, and then three rounds. Each round
is an ACTUAL COCHART perfect matching between the four A and four B records.
Every matched pair physically reaches a common chart, even if its chosen
binary map is identity. The local map may be any element of GL(2,F2).
Public routes are nested upward and end in their native receiver facets.
There are no further X reads, outside-record interactions, or owned arrivals.
An abstract identity edge skipped without a physical rendezvous is outside
this model. Additional records, coded seeds, later reads, larger meetings,
or arbitrary nonbinary/block-linear local maps are also outside its scope.

## 2. Complete geometric reduction

Condition all X inputs outside these eight to zero. Each remaining input is
needed by three outputs. Exactly eight unit reads with no later information
must therefore read all eight inputs once: the seed assignment is a bijection.

A record's history mask lists initial seed carriers whose native lines have
entered its chart. At each actual meeting both history masks become their
union. This is necessary even for an identity payload map. The lines are
independent, so each mask has exact dimension equal to its cardinality.

At a final meeting of A_i with B_j, their two desired corrections require
the three other A lines and the three other B lines. Thus the common chart
contains at least six distinct seed lines. It lies inside F_(A_i) intersect
F_(B_j), whose real dimension is six, so it contains at most six. Its history
is exactly those six lines; the omitted lines are precisely A_i and B_j.

Relabel B to normalize the first matching to identity. The remaining two
matchings give576 schedules. Exactly120 have six-element final unions at
all four meetings. The independent checker enumerates all40320 seed
permutations for each, retaining exactly192 legal schedule/seed cases.
It does not import the separate discovery case generator or its candidate
list. Properness of these final charts also ensures properness of all their
nested earlier history charts.

For every final pair in every legal case, record the incoming history masks
U,V and required triples T_A,T_B. The four differences

    T_A minus U, T_A minus V, T_B minus U, T_B minus V

are all nonempty. The result supplies768 exact witnesses, including the
schedule, seed assignment, incoming masks, and four nonzero missing masks.

## 3. Binary obstruction and arbitrary Y restoration

The incoming X rows u,v have supports contained in U,V because there are no
later source reads. The A output needs T_A, contained in neither U nor V.
Its binary coefficient row must therefore use both inputs: (1,1). The B
output similarly needs both inputs, so its coefficient row is also (1,1).
The resulting local matrix is singular. None of the six GL(2,F2) matrices
has two identical rows. Such a map would lose an independent original-Y
direction, which invertible preconditioning and this eight-record-only
continuation cannot restore. Every final pair is therefore obstructed.

For uniform opposite-frame seeds there is a shorter proof: after two rounds
each incoming history has at most two sources from each frame, so both
three-source outputs need both incoming rows. This short counting assertion
is not assumed for arbitrary seeds. The192-case certificate handles every
legal bijective seed placement and establishes the required four missing
supports directly.

## 4. Corroborating coefficient search and attempted invoice

The separate C++ program enumerates all6^8 two-round GL(2,F2) prefixes for
each of the192 legal cases, then tests all six choices independently at each
of the four final meetings. All322486272 prefixes have zero full completions.
This is corroboration; the768 support witnesses and binary argument already
prove the scoped gate.

The initially proposed schedule had opposite-frame seeds and matchings
B_(i+1), B_(i+2), B_(i+3), indices modulo four. Each public route had ranks
0,1,2,4,6,7. Relative to eight direct ground-to-facet moves, its complete
public path profile would add24[1]+16[2]-8[7], a moment increase of
approximately0.431501231313214375 at t=199/200, with no owned movement.
This is only an attempted path invoice: the required payload network does
not exist, and no completed service word or new source is admitted.

## 5. Remaining constructive interface and reproduction

An escape must change a declared premise, for example by an actual additional
information arrival before a final meeting or a different meeting network.
A proper-chart export could make an incoming record depend on a source
outside its native history. Such an export must be physically acquired,
delivered, charged, and restored. No export is supplied here, and this gate
implies no general lower bound on their number or total cost.

Primary exact-integer reproduction (Python and NumPy):

    python workers/A/complementary-frame-search/check.py \
      --repo source --parent workers/A/full-half-reservoir --out /tmp/frame-review

Optional coefficient search:

    python workers/A/complementary-frame-search/make_cases.py
    g++ -O3 -std=c++17 workers/A/complementary-frame-search/search.cpp -o /tmp/frame-search
    /tmp/frame-search --cases workers/A/complementary-frame-search/CASES.txt

The primary checker accepts a separate output directory. The optional case
generator rewrites its auxiliary case files. The package is a finite exact
geometry certificate and a general binary support argument under the stated
module hypotheses, not a source-bank or complete-supplier exclusion.

Worker A, S020, 2026-11-17. Credit root's complementary-frame proposal,
the retained source and source reviews, and substantial OpenAI assistance.
