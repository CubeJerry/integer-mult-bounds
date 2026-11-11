# Four stationary accumulators realize the historical owned-difference returns

**Conditionally proved constructive source rewrite, with a complete exact
homogeneous-rail replay. No full shared native or new kappa is claimed.**
The identities and their original historical-observation certificates are due to
Worker B in the sibling `historical-owned` package. This packet supplies a
literal, version-safe implementation, including a complete lifecycle ledger.

## 1. Interface and the four required identities

Use the pinned 71,261-event source with SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Let Delta be the difference of two virtual copies with independent main inputs
and identical arbitrary helper inputs. Their entering helper differences are
zero, by equality of shared inputs; their common helper values remain arbitrary.

The source's normalized scalar difference rail has 400 independent entering q
coordinates. We condition on an actual representation supplying each named
Delta observation at its precise chart and time, with all prior storage,
acquisition, helper-difference synthesis and transport already accounted for.
This is not a grant of 1,080 free helper-difference arrays. A physical whole-lift
construction still must supply that interface, while preserving the shared
common source and every original foundational assumption.

Every term below is sampled immediately AFTER its indicated source MOVE:

| Replaced return | Destination | Accumulated historical row |
|---:|---:|---|
| 28141, owned1526 | 470 | -4 Delta1162@27283 + (3/4) Delta1499@28113 |
| 33554, owned1524 | 431 | -4 Delta1135@32137 - (1/4) Delta1497@32558 |
| 34467, owned1522 | 394 | 4 Delta1098@34199 - 8 Delta1100@34200 - (1/2) Delta1495@34450 |
| 37597, owned1511 | 520 | -4 Delta992@37297 - 32 Delta1482@37548 |

The exact identities, last value-change pins and dirty-common residuals belong
to `historical-owned/WITNESSES.json` and its independent checker. Five of the
nine observations are helper differences and four are owned differences. A
single earlier owned difference does not suffice for any displayed return.
The required helper observations remain an explicit mathematical obligation.

## 2. General stationary-accumulator lemma

Suppose a virtual owned role r would move from A to B at event t, and its
normalized row is a fixed sum of earlier source-version observations:

    Delta_r(t) = sum_j a_j Delta_sj(t_j),  with t_j < t.

Each observation is physically available at B at its stated time. Choose one
fresh owned accumulator Z. Immediately before the first sampled version is
consumed, INIT Z=0 in B. At time t_j, after the source event defining the exact
sample and before any following source event, emit
`ADD Z += a_j Delta_sj(t_j)` in B. If a sample is decoded from several actual
holders, substitute that already-certified cochart expression at this time.
Z never moves and no later version is substituted for an earlier one.

By induction, Z holds the sum of exactly the terms already sampled. At t it
therefore equals the row of r that would have arrived in B. Retire the old
physical difference owner of r in A using the retained owned-erasure service.
Rebind virtual r to the actual holder Z in B. Every later instruction involving
r uses Z; the source's eventual CLEAR of r clears Z. No payload is physically
moved by this owner substitution, and its bookkeeping and source-control costs
must be included in the compiler invoice.

This is a valid causal implementation of the same difference state. Other
virtual roles retain their actual holders. The old r is owned and no observer
aliases its newly chosen accumulator. A subsequent source INIT of the same
virtual label begins a fresh actual lifetime. The proof depends on the exact
source-version identity and on actual observation availability, not on a cache
of unmaterialized symbolic history.

For K literal observation terms the macro adds K ADDs, one INIT and one CLEAR,
and one owned lifetime, while removing the single differential MOVE. The original
common MOVE remains. The accumulator may add one live owned holder before the
return; after the old owner is retired it replaces that owner. A compiler that
cannot rebind physical owners may instead copy Z into a new destination owner;
that alternative has additional ADD/lifecycle charges and is not the emitted
implementation here. Dirty CLEAR is not zero-uncomputation or free erasure.

## 3. Literal source rewrite and complete ledger

`rewrite.py` rewrites the entire homogeneous source rail. Source roles initially
use their original names. Four fresh owned names1531–1534 hold the accumulators.
At each removed return it checks exact equality of the old source-row payload
and the completed destination accumulator, then changes the physical-owner map.
All later ADD, SCALE, MOVE, COPY and CLEAR operands use that map. Every physical
MOVE's ownership flag, live operand and current chart is checked.

The resulting word is equivalent on all 400 independent main-difference inputs,
including every one of its 1,480 public difference endpoints. This is the
appropriate homogeneous input subspace for two copies with shared arbitrary
helper inputs. It is deliberately not an all-column native certificate with
1,480 arbitrary independent difference inputs, and it does not claim to allocate
or pay the helper-difference interface in a complete lift.

| Quantity | Original homogeneous rail | Rewritten rail |
|---|---:|---:|
| ADD | 61,180 | 61,189 |
| MOVE | 6,310 | 6,306 |
| INIT / CLEAR | 54 / 54 | 58 / 58 |
| SCALE / COPY | 3,662 / 1 | 3,662 / 1 |
| Declared owned labels | 51 | 55 |
| Owned lifetimes | 54 | 58 |
| Peak simultaneously live owned fields | 43 | 44 |
| Final live owned fields | 0 | 0 |

The actual four accumulation intervals are disjoint before owner replacement,
so their auxiliary live overhead is at most one. The exact full-source replay
finds peak44. A simultaneous unchanged common rail adds its own original owned
allocation; the conservative combined live upper bound is43+44=87, before any
other decoder sidecars. Declared labels, historical backing and scalar control
are distinct from this active-peak count and remain in the physical invoice.

The removed differential MOVE histogram is rank2 three times and rank5 once.
Thus the additional saving over the ten current-cochart substitutions is exactly
`3*2^(199/200) + 5^(199/200)` per native, conditional on the compatible supplied
observations. The sibling historical-owned budget computes the rigorous interval
and complete H4-profile consequence. No other cost is canceled by this identity.
If observations use decoded physical expressions, replace the nine-ADD count by
the actual flattened support count; pay its coefficient, source and precision
services. The largest displayed coefficient magnitude is32 and all denominators
divide4, but this does not bound arbitrary composed decoders.

## 4. Verification and negative controls

The transcript is `difference-rail.json.gz`; it contains the actual typed word,
physical rebindings and its conditional input contract. `RESULT.json` binds its
canonical uncompressed payload and the exact sibling witness file. Run:

    python rewrite.py --source PATH/TO/final.json.gz --certificate ../historical-owned/WITNESSES.json --output /tmp/accumulator-result.json --transcript /tmp/difference-rail.json.gz

The author checker independently replays both complete source and rewritten
words with rational arithmetic. It checks current charts, true owned flags,
nested transport, COPY-zero, live lifecycle, equality at all four returns and
all public endpoints. Wrong historical coefficient, wrong observation chart,
and omission of the source-owner retirement are rejected. Exact source identities
and independently reviewed dirty-input cancellation are checked by the sibling
certificate, rather than inferred from the source author's verifier.

This packet converts four historical row relations into an actual causal storage
and lifecycle schedule. It leaves the physical helper-difference supplier open.
The conditioned rail may be used inside a future richer code, but neither its
unmodified baseline nor its rewritten word is asserted to fit the H4 shared-core
budget as a whole. All five foundational assumptions remain.

Prepared for @CubeJerry by Worker A with substantial OpenAI assistance. Credit
Worker B for the historical identities and budget, Worker C for the preceding
ten current-cochart identities, and the selected source/predecessor authors.
