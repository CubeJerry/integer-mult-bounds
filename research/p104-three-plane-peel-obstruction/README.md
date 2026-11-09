# A third independent shear cannot be obtained by one-pair endpoint peeling of the frozen shared native

**Result.** For the exact two-plane native of CrocSwap/integer-mult-bounds#6902, no one of 984 eligible helper pairs can become a third independent unit-shear plane by removing its first/last rank-one moves and changing only the endpoint ordinary basis operations. The proof permits arbitrary invertible constant basis changes within every resulting initial and final frame group. It uses an exhaustive exact inventory and a forward/inverse matrix-block invariant, not a failed numerical search. **No new κ.**

The narrow hypothesis matters: the interior scalar word is frozen. The result does not exclude a redesigned core, additional helper circulation, simultaneous promotion of several pairs, or a different native endpoint.

## Why investigate this interface?

The shared native already serves two independent planes. A further plane that reuses its helper circulation would change the complete recursive invoice. In the candidate class here, two zero-to-full helper jobs would be promoted to mains, and two paid rank-one MOVEs removed. At one port, a complete additional chain root of L stages would change the signed rank surplus by L−1; thus this was a meaningful potential improvement rather than a search on a nonbinding component. The proposed interface fails its all-input linear identity before any stronger bound can be claimed.

## Exact object and new result

The frozen source has 1375 public fields and 38334 events. Its endpoint is `X=x, Y=y+x, X2=x2−y2, Y2=y2`, with every helper unchanged. All zero-frame scalar gates precede the first MOVE; all full-frame scalar gates follow the last MOVE. The interior contains neither endpoint chart.

For each of the 104 retained ports q, we considered a helper h whose first MOVE is zero→span(q), and a helper g whose last MOVE is q-perp→full. Both helpers must originally run from zero to full. Removing these two MOVEs gives the correct labels for an additional main pair. All other recursive jobs and all interior scalar gates remain fixed. The candidate endpoint adds either `h←h−g` or `g←g+h` while retaining the two existing planes and every helper identity.

There are 363 eligible h choices, 295 eligible g choices, and 984 same-port pairs. Exact forbidden-block witnesses eliminate all but two pairs: q268 with g1352 and either h793 or h1202. For each residual pair, the forward block has rank 1 and the corresponding inverse block also has rank 1. A third forward plane requires ranks (2,1); a third reverse plane requires(1,2). The inverse condition supplies the decisive rejection for the reverse candidates.

This is new relative to the source construction: CrocSwap/integer-mult-bounds#6902 supplies the successful two-plane word; this package proves that a specific endpoint-only attempt to extract a third plane cannot work on its frozen scalar core. It does not audit or retract the source's two-plane claim.

## Reproduce

From the repository root, using Python 3 and only the standard library:

```sh
python3 -I -B research/p104-three-plane-peel-obstruction/check.py
```

Expected:

```text
PASS_P104_THREE_PLANE_ENDPOINT_PEEL_OBSTRUCTION
984 helper pairs excluded; 104 source two-plane controls; 1375 exact inverse rows; two exact residual inverse blocks of rank 1.
```

`check.py --write-result` reproduces `RESULT.json`. The default command reads that retained result and requires exact equality. All proof-relevant arithmetic is `fractions.Fraction`, and the checker imports no predecessor verifier. The only executable data dependency is the package-local byte-identical compressed word.

## Verification and controls

The replay checks the source endpoint on every public input, reconstructs the scalar core and its inverse from the endpoint blocks, and checks all 1375 rows of their product over the rationals. It regenerates the complete eligible-pair inventory and every exact forbidden-block witness. All 104 original paired ports pass the baseline forward/inverse rank(1,1) controls.

A doubled first interior ADD changes the exact native endpoint and is rejected. The residual pairs deliberately pass the forward rank test for a proposed reverse plane, demonstrating that omitting the inverse test would miss the obstruction. Source hashes, census counts, and residual pair identities are pinned. Normal and `-O` executions are recorded in `CHECKS.json`; no proof check relies on Python assertions.

A separate research agent reviewed the theorem and supplied `review.py`, `REVIEW.md`, and `RECEIPT.json`. This oracle pulls back exact scalar functionals, verifies the four relevant inverse rows by composition, checks direct minors, independently recounts the eligible family, and rejects four corrupted inverse functionals. It does not claim a second independent evaluation of every nonresidual forbidden coefficient. Both implementations run through `scripts/research_package.py`.

## Scope and assumptions

The theorem is a statement about the formal finite linear map of a pinned native word, with INIT/CLEAR interpreted as the source's ideal owned resets. It does not admit A6, LAMBDA, a BIT saving, or a multiplication theorem. The rank argument actually excludes arbitrary invertible rational or Gaussian-rational endpoint matrices with the required frame-group blocks, a larger class than the permitted dyadic elementary gates. It allows mixing inside a frame group, including mixing the proposed mains with existing mains of that same frame, but never mixes different frame groups or introduces a field persisting through the core.

The source and exact base pins are in `SOURCES.json` and `TASK.json`. Canonical main at selection was `7c49fe32c55de02c2c873655c804b16e4c3fef0a`; the source is CrocSwap/integer-mult-bounds#6902 at `e4d42607f24d7a049b0fca329dc4c34882405c25`. The selected frontier is unchanged.

## Open next questions

1. Can new interior main-helper contacts produce a third independent odd shear while retaining a favorable complete helper/paid invoice? This theorem does not address that changed core.
2. Do simultaneous endpoint promotions or a cross-plane coupled target evade the obstruction? They require a fresh target map and exact interface accounting.
3. Does the same obstruction survive a newer native word? No transfer to changed words is automatic; replay the exact inventory and core before applying it.

## Credit and attribution

Research and implementation by @CubeJerry with substantial OpenAI GPT-6 Astra assistance for mathematical reasoning, code, exact experiments, and prose. The retained native word is by DreamingOfClouds with Claude Opus 5.5 assistance, from CrocSwap/integer-mult-bounds#6902; its original lineage and notices are preserved in `SOURCE-NOTICE`. The new checker is independent source code and imports no predecessor implementation. See `LICENSE` and `NOTICE`.
