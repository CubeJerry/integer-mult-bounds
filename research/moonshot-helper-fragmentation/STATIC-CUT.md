# No static first 3/6 cut for a balanced ternary helper on selected #7000

**Scoped exact obstruction; No new κ.** This addresses one constructive gap
behind the sharp profile's 554 rank9→3+3+3 requirements. It supplies neither
a ternary construction nor a general impossibility theorem.

## Exact statement

Freeze the selected #7000 word at canonical
`e54523517d0f03e58352e647c403a5af3e525a57`, source
`research/shared-wire-split-composition/data/final.json.gz`, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883` and
Git blob `74563a7867d9d762b6588f65362369668841bb3e`.
Let G be exactly its 595 current public roles with initial frame3 (zero space)
and final frame127 (full nine-space). Fix the literal scalar event order and
every original frame. At any chronological cut on an existing rank3 or rank6
frame F, allow all currently coframed public and owned roles R_F.

Let P and S be the exact normalized prefix and suffix maps. The retained
boundary-only split contract requires a row a and column b supported on R_F
such that aP=c, Sb=d, supp(c),supp(d)⊆G, and a·b=c·d=1. Coefficients may be
arbitrary rationals, with no restriction to sampled pivot directions.
This is Ali Romman's existing helper-split criterion, not a new criterion.

**There is no such pair at any of these cuts.** The statement grants ideal
normalized operations, so it does not require a new native provider theorem.
It includes all actual scalar events and owned resets in P/S. COPY uses the
source's ADD-into-ideal-zero semantics in both directions; it is not replaced
by an overwrite in the reverse pass.

## Proof and coverage

For each cut, construct the full linear subspace A of coframed coefficient
vectors whose prefix images are supported on G, and the analogous suffix
space B. A pure image may be zero; those coefficient vectors are retained.
The checker solves one exact rational equation per forbidden input/output
coordinate by transposed RREF, producing a full kernel basis.

There are exactly4,657 chart/cut classes:

| Reason normalization is impossible | Classes |
|---|---:|
| Every G-supported prefix image is zero | 4,496 |
| Prefix exists; every G-supported suffix image is zero | 136 |
| Both have nonzero images, but a·b vanishes on A×B | 25 |

In the last25 classes, every entry of the local pairing matrix on full kernel
bases is exactly zero. Bilinearity proves the exclusion for every rational
coefficient choice. The same zero-space argument holds after any
characteristic-zero scalar extension. Checking only selected basis pairs for
nonexistence would be insufficient without this whole-matrix vanishing proof.

One class is checked after every event touching F. Between two such events,
its live role set, prefix rows and suffix columns are unchanged, so these
represent all chronological cuts. At the initial boundary, no rank3/6 role
contains a nonzero G-supported initial image: G starts at zero frame3.
The exact frame/event replay checks1,095 independent GF(2)^9 frame bases,
all71,261 events, nested MOVEs and coframed scalar operations. The propagated
source returns all595 arbitrary helper inputs identically and clears owned
roles at the end. These checks do not claim an independent full main-map or
physical all-width native admission.

A sequential positive-rank refinement from9 into3+3+3 by two standard binary
cuts must begin3+6 or6+3. Both are excluded on the unchanged source. This
conclusion does not apply to simultaneous edits that change the first cut,
new frames, retimed scalar contacts, temporal gathers, paid transports,
changed boundary groups, or a different native word. It also does not show
that the sharp ideal profile is physically attainable or impossible.

## Reproduction and limits

```sh
python -I -B research/moonshot-helper-fragmentation/static_cut.py
python -I -O -B research/moonshot-helper-fragmentation/static_cut.py
```

Expected marker: PASS_STATIC_3_6_CUT_OBSTRUCTION and counts4657;4496/136/25.
Default replay is read-only and compares all STATIC-RESULT.json fields.
Explicit --write regenerates the receipt. The exact canonical gzip source is declared as a live input and authenticated
before decompression. An exported checkout must include that declared input;
--source PATH permits an explicit alternate location with the same byte pins. No source-engine imports are used.
A genuine positive toy cut must not be labelled excluded; a disjoint-coordinate
pair with nonzero boundary images must be excluded for zero local pairing.

The earlier workspace's independent review is historical evidence only.
These rebuilt bytes require fresh review, recorded in the integrated review
packet. No finite-width or fixed-state check is extrapolated to an unbounded
multiplication theorem. All five foundational assumptions remain unchanged.

Matarener's p104-helper-split-exhaustion already establishes this form of census
on an older source. This contribution changes the source to selected#7000,
targets the rank3/6 prerequisite forκ=1/200, and uses transposed constraints.
Credit Ali Romman, Matarener, DreamingOfClouds, Jerry Chen and the full retained
native/split lineage. Prepared for @CubeJerry with substantial OpenAI assistance.
