# Independent review: all 111 native sources and 44 centres

**Verdict: accepted as a source construction and a fully priced source word.**
This review independently reconstructs all 222 field components, all 6,470
physical source cuts in each component, the 1,474 common inverse fibres in each
component, all 111 source-information changes, and the complete source invoice.
It does not certify a complete BIT interior, a dirty return, a supplier, or a
new value of kappa.

## Reproduction and independence

From the repository root, run:

```sh
python -I -B research/moonshot-005-program/results/bit-coupled-native-forty-h-source/review-all-donors-b/check.py --repo . --out /tmp/all111-review-fresh
```

The checker compiles the adjacent `linear64.cpp` into the chosen output
directory. It needs Python, NumPy and a C++17 compiler. The supplied
`RESULT.json` records the completed full run, including cost reconstruction;
`MANIFEST.json` freezes the reviewed author files and review files.

No Python code in the new author package is imported. The coefficient
constructors from two separately authored, pinned predecessor reviews are
reused; this is an explicit dependency, rather than a claim that every source
coefficient was derived with an unrelated formula. The new checks of the
finite field, elimination, source cuts, inverse equations, physical owner
placements, literal source word, binary prices and non-RS information are in
this review. The C++ arithmetic multiplies polynomials modulo `0x43`; all
4,096 products are compared with a separate Python polynomial implementation.
Every nonzero scalar is checked for its unique inverse. The binary scalar
implementation is replayed on all six basis bits.

## Native geometry and source coverage

The certificate contains 21 disjoint two-centre components, each involving
five donors, and the two single-centre components at H701 and H333, each
involving three donors. Thus the construction covers all 111 donor banks and
uses 44 distinct native centres. All selected centres are mixed; none is an
all-early centre. The shared donor of each two-centre component is ordinary.
The 11 singleton donors occur among leaves or single-centre components, and
all 22 literal singleton matrices are checked.

The exact roots, planes and native incidences are rebuilt from the pinned
geometry and compared with the predecessor native model. Actual X ownership
is reconstructed from the pinned route certificate, without taking the new
author's holder dictionaries as geometry. There are 426,240 individual X
field owners after the eight copies, and 321,000 late Y taps. The two scalar
components have parameters k=3 and k=12; each has 16 spinor lanes, giving
768 and 3,072 field coordinates, respectively, for a full 3,840-coordinate
source bank.

All 222 chronological early matrices are full rank. These matrices include
the literal singleton replacements where applicable. At an ordinary mixed
plane, the early projection and complementary late coordinates are checked
against the prescribed source quotient. At an all-early plane, the actual
placement of the two halves is used. At a singleton, the literal three-group
replacement is used. The resulting 222 coefficient hashes exactly match the
frozen author receipt.

## All physical source cuts

For each component the checker verifies 6,110 ordinary receiver cuts and
360 singleton receiver cuts, totalling 6,470. At an ordinary cut, the stack
of the 16 actual plane quotients has full rank 16k.

The singleton cuts need a different calculation. The nullspace of the other
15 actual quotients has dimension k. The checker constructs the value and
derivative readout from the actual singleton port nodes, rather than
treating the singleton as an ordinary quotient. Its composition with the
two halves of the supplied singleton matrix has rank 2k on that nullspace.
The first 2k coordinates of the reduced singleton matrix also have rank 2k,
as required by the physical early placement. These tests cover every actual
singleton cut, in both components. Full rank of a fictitious 16-plane stack
would not have sufficed for this part of the review.

The early bases and placements give a literal reversible change of source
coordinates on the original X registers. Late parities are formed from
original coordinates before that basis change, then added to the actual
late Y registers. The baseline Y coefficient is preserved by these source
additions. Thus the checked source map has the declared physical meaning,
including the split early and late owners.

## Common inverse fibres

For each selected centre and each receiver in its native audience, the
checker solves the unique source-cut system for the first donor to obtain
the inverse lift K: the selected H readout is the identity and all other
visible source information is zero. It then evaluates the same K against
the other two donors' actual source cuts. All three lifts agree exactly.

An ordinary off-centre plane is tested by its quotient matrix. A singleton
off-centre observation is tested by its actual value/derivative readout
composed with the literal singleton matrix. Since each full physical cut
was independently shown injective, these vanishing conditions identify the
whole off-centre fibre with its intended dimension; they are not merely
containment checks on a potentially larger kernel.

There are 1,474 common H/receiver inverse graphs in each component, and
4,422 donor/H/receiver inverse equations after including the three donors.
All affected singleton equations are included. The checked target is the
**canonical foreign identity on these 44 H interfaces**. It is not a claim
that the earlier S028 two-star perturbation has been extended to this
construction. In particular, some selected centres involve the exceptional
labels 10 or 80 from that earlier target, so those target conventions cannot
be silently interchanged.

## All 111 source-information changes

Each donor has a witness consisting of 16 actual ordinary plane labels,
excluding its singleton plane if it has one. Their stack in the marked
k=3 component has rank below 48. The independent rank census is:

| Marked component rank | Donors | Full-bank rank deficit at least |
| --- | ---: | ---: |
| 47 | 75 | 16 |
| 46 | 28 | 32 |
| 45 | 6 | 48 |
| 44 | 2 | 64 |

The unmarked component has at most its full 3,072-dimensional rank, so these
are genuine deficiencies of the combined 3,840-coordinate observation.
The original degree-below-16 RS source is injective on every set of 16
distinct ordinary nodes. Injectivity of a joint observation is unchanged
by any bijective recoding of the input bank and any bijective recoding of
the individual observations. Consequently these 111 failures of
injectivity prove 111 genuine changes of source information. The conclusion
allows arbitrary nonlinear source bijections, including ones mixing field
components, spinor lanes, binary coordinates or copies. It is not merely a
comparison of displayed coefficient matrices.

These witness sets are not claimed to be native receiver cuts. Their
noninjectivity therefore does not conflict with the separate full-rank
checks of every native receiver cut.

## Literal source invoice

The checker independently compiles all 222 early matrices into the author's
declared deterministic Gauss-Jordan reduction order. Each matrix reduces to
the identity. Every serialized field-operation stream hash matches the
author receipt. A stream record is six bytes, with opcode, destination,
source and scalar in the declared little-endian representation. Scalar ADD
costs are obtained from the six-bit multiplication matrix. Scalar SCALE
costs are obtained by constructing and replaying its binary XOR word;
register swaps cost 18 binary ADDs. The forward source basis is implemented
by reversing those actual binary operations.

Actual X labels are then followed through every source placement
permutation. All 111 holder-dictionary hashes match, and the permutation
cycles are priced and executed independently. The 111 source components
cover every field coordinate exactly once. Late parity rows are rebuilt
from the source coefficients and the actual mixed-plane complement
coordinates. Their write, read, INIT and dirty CLEAR counts are included;
every actual late Y tap is visited exactly once.

| Item | Binary count |
| --- | ---: |
| Early field-basis ADDs | 2,118,152,064 |
| Placement permutation ADDs | 7,563,312 |
| Late-cache write ADDs | 362,475,368 |
| Late-cache read ADDs | 1,926,000 |
| Forward source ADDs | 2,490,116,744 |
| Inverse source ADDs | 2,125,715,376 |
| Total forward and inverse ADDs | **4,615,832,120** |
| INIT | 1,926,000 |
| Dirty CLEAR | 1,926,000 |

All per-donor invoices also match the frozen author file. This is a
source-only invoice, not a full interior or supplier cost. It pays for
the parity caches and uses the existing source route visits; it does not
assume an uncharged extra MOVE.

## Sensitivity controls and scope

Three exact controls test distinct obligations. Zeroing one literal
singleton replacement drops its early rank from 96 to 87. Multiplying one
donor's central readout by a nontrivial scalar preserves its individual
rank but breaks the common inverse lift. Omitting a nonzero late-parity
coefficient changes the declared source on an explicit original basis
input. These controls distinguish full-rank source bases, common-fibre
compatibility and correct physical parity routing.

The accepted output is a complete checked source on all 111 native banks,
with common canonical fibres on 44 selected centres and a fully charged
literal source implementation. It is meaningful progress past the old
unchanged-RS-source obstruction. The D/K/F middle stages, the whole dirty
return, and a strict supplier remain additional obligations. No new
complete kappa follows from this package alone.
