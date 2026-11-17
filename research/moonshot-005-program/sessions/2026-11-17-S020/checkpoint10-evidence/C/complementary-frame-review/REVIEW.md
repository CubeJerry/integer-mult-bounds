# Three-round complementary-frame gate: independent proof without case search

**The scoped binary obstruction is sound. The argument below covers every
bijective native-seed assignment without enumerating schedules or seed cases.**

Worker C, S020. A's frozen `complementary-frame-search` remains unchanged;
its192 legal cases and768 final-pair witnesses corroborate this proof. They
are not needed for its completeness.

## 1. Exact premises and source

The two frames are A=[14,17,19,20] and B=[96,99,101,102]. Their eight native
real lines are nonzero and mutually orthogonal, hence form the ambient
eight-dimensional basis. At the admitted full-half-reservoir cut1893, their
native owners contain the eight pure x inputs at their lines; all eight Y
records are at ground. Their current X coefficients contain none of these
eight inputs. The checker authenticates the native data and C's independently
replayed406-field cut, and checks these facts directly.

Condition every other X input to zero. The module allows arbitrary invertible
ground preconditioning of these eight arbitrary Y records, then exactly one
native-unit read per record, followed by three actual cochart perfect-matching
rounds between A and B. All public paths are nested upward and stay in their
native final facets. Every matched pair physically meets, even when its local
map is identity. Each local payload map is invertible over F2. There are no
later source reads, owned arrivals, outside records, or larger meetings.

Each A output must contain its three other A inputs; each B output must
contain its three other B inputs. Cross-frame terms are unrestricted. The
eight initial unit reads must be a bijection onto all eight source inputs:
each is demanded and there is no later information source. Initial Y
preconditioning supplies no missing X input and preserves eight independent
baseline Y directions.

## 2. Four disjoint source pairs after the first actual round

Label the first-round meetings arbitrarily. Their two native seed inputs
partition the eight source inputs into four disjoint pairs P1,P2,P3,P4.
At an actual meeting, both public charts contain the union of their prior
native seed lines, even if the chosen payload map is identity. Thus after the
first round both records of a pair contain that pair's source lines in their
chart histories. After the second round, each incoming record to the last
round has a history comprising at most two whole P blocks.

This is a chart statement, not an assertion that a current payload retains
every previous coefficient. Payload cancellation cannot remove a direction
from a nested upward public chart.

## 3. Each first-round pair contains one source from each frame

Consider a final meeting of A_i and B_j. Their required corrections jointly
contain the six sources other than their own A_i and B_j inputs. With no
later arrivals, the common chart must contain all six source lines. It also
lies inside F_(A_i) intersect F_(B_j), a six-dimensional space, so it is exactly
the span of those six lines and omits precisely the two own-source lines.

The final chart history is a union of whole P blocks. Six distinct seed lines
are exactly three blocks, so this final meeting omits exactly one whole P
block. That omitted block is {A_i,B_j}, containing one source of each frame.

The last round is a perfect matching. Its four own-source pairs {A_i,B_j}
are disjoint and exhaust all eight sources. Therefore the four omitted P
blocks are distinct and exhaust P1,P2,P3,P4. Every first-round P block must
contain exactly one A source and one B source.

No assumption about uniform opposite-frame seeding was made. The balance of
every first-round source pair follows from final properness and the matching.

## 4. Binary invertibility contradiction

Each incoming history before the final round contains at most two P blocks,
so it contains at most two A sources and at most two B sources. Neither
incoming payload can alone contain the three required A sources or the three
required B sources, because payload support is contained in chart history.

Let u,v be the two incoming scalar binary payload rows. Each final output
needs a source absent from u's history and a source absent from v's history.
Its local coefficient row must therefore use both inputs. Over F2 that row
is necessarily (1,1). Both outputs would have the same coefficient row,
making the last local 2-by-2 map singular. This contradicts its required
invertibility and loses an independent arbitrary-Y direction that no outside
record or later input can restore.

The contradiction applies to every possible first, second, and third matching
and every possible native-seed bijection under the premises. A's finite
enumeration is useful corroboration, not the universal proof.

## 5. Scope and reproduction

This is a restriction on the stated three-round binary module. It does not
exclude additional source arrivals, proper exports, a fourth round, a larger
meeting, additional records, skipped physical identity meetings, or nonbinary
and block-linear local coefficient maps. It is not a lower bound on an
arbitrary supplier or a claim that the entire admitted reservoir is closed.
No productive source or completed-output word is supplied by this gate.

Run:

    python -B check.py --native NATIVE.json --cut INDEPENDENT-CUT.json \
      --cases A-RESULT.json --out RESULT.json

The checker uses only Python's standard library. It authenticates the source
and the prior independent cut, then independently reconstructs the first
blocks and their omissions for all192 supplied legal cases. It checks the
balance forced by the omitted-block argument, all768 incoming-history bounds,
and all four missing-demand supports per final pair. It does not import A's
discovery generator or verifier. Its proof of all cases is Sections2--4 above.

Credit A's exact scoped model and finite certificates, root's complementary
frame proposal and independent review, and substantial OpenAI assistance.
