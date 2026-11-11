# Exact owned1481 interface after correcting the entry-snapshot extrapolation

**Status:** proved source-specific algebra and reduction; conditionally valid local four-port prefix; missing physical input acquisition and full continuation remain open. **No new κ.** This packet does not insert an oracle field into a global 1,880-input word.

## 1. Incorrect extrapolation and exact correction

The pinned source is `research/shared-wire-split-composition/data/final.json.gz`, SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. Events are zero based. Let q denote the 400 independent initial main differences; helper differences initially vanish. The full common inputs in the physical paused-loan construction remain arbitrary and are distinct from this reference-difference calculation.

At chart541 define these **actual reference values**, each at its stated version:

| Port | Source value | Snapshot | Initial q support |
|---|---|---:|---:|
| A | δ151 | before 30776, equivalently before 30773 | 3 |
| B | δ399 | before 30776 | 9 |
| M | δ130 | before 30777, equivalently before 30773 | 15 |
| G | δ1507 | before 30808 | 34 |

The three-term entry identity is correct:

    A = (q55−q101+q130)/2.

It does not remain unchanged until owner1481 is sampled. The source performs H+=B at 30776; M+=H at 30777; H−=M/2 at 30781; H*=−2 at 30783; H+=G at 30808. Therefore the two changed values are

    H = −A−B+M+G,
    M_new = M+A+B.

Here M on the right is the old fifteen-term value, not the raw carrier q130. Owner1481 copies H at 30821 and is scaled by1/2 at 30823. Its immutable payload through retirement is therefore

    r = δ1481 = (−A−B+M+G)/2.

Exact replay gives **59** nonzero initial-coordinate terms in r. In particular r[q55]=−1/4, whereas A/2 has coefficient+1/4. Setting only q55=1 gives a direct counterexample. Setting only q7=1 is an independent counterexample to acquisition from the borrowed pair, raw q130/q899 and G alone: those offered values vanish, but M=−1/2 and r=−1/4. Exact rows and both controls are in `SOURCE-ROWS.json`.

This corrects a proposed S003 bridge before admission. The verified q101→q213 paused-loan word is unaffected: it explicitly claimed one selected shear and did not claim the original δ1481 payload.

## 2. A smaller exact acquisition target

The donor encoding b=(q55−q101)/2 is locally available where q55 and q101 meet at 327; its inverse can be performed when they reunite at 127. The paid restoration lemma transports this chosen payload without changing common endpoints. Define

    U = M−B+G−q130/2,
    W = M+B+q130/2.

Then

    r = (U−b)/2,
    M_new = W+b.

Thus **one actual fused field U at 541** suffices, together with b, to form r. If the continuation also preserves current-main δ130, it additionally needs W or an equivalent construction. This is a reduction of the acquisition problem, not evidence that U or W is available.

The rows have |supp(U)|=57 and |supp(W)|=24. In the fixed chronological graph granting every main MOVE, all 47 owned MOVEs and all 354 quiet-loan windows simultaneously, **50** of U's coordinates have not reached541 before 30824. This generous graph allows unlimited local caches and message capacity. The count50 is not a claim of 50 necessary messages; it disproves free availability from that graph.

On the two absent coordinates q7,q4, the U,W matrix is

    [ −1/2  −1/2 ]
    [ −1/2   1/2 ],

with determinant−1/2. Both b and raw q130 vanish there. A single additional globally shared V-field cannot provide both U and W on this subspace; two independent field-volume dimensions are needed when both observables are demanded. For r alone the corresponding requirement is only one dimension. This is scoped to the fixed graph and current-state interface, and permits other q-informative helper traffic or a changed endpoint representation.

## 3. Conditional prefix with actual owned records

`CONDITIONAL-PREFIX.json` is a 15-instruction component whose **four input ports are already supplied at 541** with A,B,M,G. It executes the local scalar block, forms r in an owned field and follows the actual owned1481 routes541→534→117→594, of ranks 1,1,4.

At534 it creates a separate owned record 4r. At117 it creates a separate owned recordr. The traveling owner retainsr at 594. These are physical V-fields, with explicit INIT and ADD instructions.

The prefix uses 7 ADDs,2 SCALEs,3 INITs and 3 owned MOVEs. It ends with three live owned output fields and implements no CLEAR. The caller must consume or replace the receiver updates and provide legitimate retirement. The reference source retires owner1481 at 40843 only after all its reads; both extra records also need charged retirement. This component is not a complete native certificate.

Given the four ports, the exact public outputs are H=2r, M_new=M+A+B and unchanged B,G. The algebra proves these identities for every field volume V and every four values over the characteristic-zero coefficient field. Exact replay checks all four input directions and proper nested frame moves. The bounded dyadic scalars incur fixed O(V) arithmetic/storage; complete transport, precision and erasure contracts remain inherited.

## 4. Every read in the source lifetime

Each increment below factors through an actually cochart record. This proves the observation interface only. It does not apply an increment to a missing full virtual-helper receiver or construct that receiver's other dependencies.

| Event | Receiver | Increment | Chart |
|---|---|---:|---:|
| 30825 | 231 | 4 r | 534 |
| 30827 | 629 | 2 r | 117 |
| 30829 | 732 | 1 r | 117 |
| 30833 | 213 | 2 r | 594 |
| 30837 | 449 | -4 r | 594 |
| 37665 | 139 | 2 r | 594 |
| 38529 | 707 | 1 r | 594 |
| 38547 | 490 | 2 r | 594 |
| 38550 | 491 | 2 r | 594 |
| 39049 | 568 | -4 r | 594 |
| 39083 | 576 | -4 r | 594 |
| 39501 | 569 | -4 r | 594 |
| 39544 | 575 | -4 r | 594 |

There are two main receivers,213 and 139, and eleven helper receivers. The earlier four-read sketch omitted449 at 30837 and all eight later reads. Owner1481 remains live at 594 until40843. Its payload cannot disappear after the first main destination receives an update.

## 5. Remaining obligation and verification

The next construction is a source-safe physical supplier of U at 541 before the relay, compatible with the paid helper loan and complete difference continuation. If current-main130 must be realized, account for W too. Literal current B,M,G are sufficient inputs, but this packet does not provide them. Their rows show why substituting raw carriers is invalid.

A complete continuation must implement or legitimately replace all thirteen receiver updates and retire every added owned field. Three records reduce the observation interface to three chart locations; they do not solve later movement, storage, precision or ownership of the affected helper states.

Reproduce with `python3 -B verify.py --source SOURCE --output RESULT.json`; optimized mode `python3 -O -B` produces the same receipt. The verifier derives source rows, checks the local four-port program and entire owner lifetime, checks both counterexamples and the missing-observable determinant, and regenerates both certificates byte for byte. General algebra is the proof; exact calculations bind it to this source.

Credit: existing native authors and @CubeJerry's programme; root's entry identity/proposed bridge; independent S003 adversarial and bridge-worker checks of the overwritten snapshot, actual main state and full carrier; S003 adversarial reduced-interface certificates. AI assistance disclosed. No new κ.
