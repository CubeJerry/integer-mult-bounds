# Targeted upstream triage — S010

Checked 2026-11-13 12:54 UTC. Repository is `CrocSwap/integer-mult-bounds`; the GitHub API reported current `main` at `e54523517d0f03e58352e647c403a5af3e525a57`. Both reviewed PRs are open and use that exact base. No upstream files were integrated or changed.

## PR #7498 — fixed-paid endpoint exchanges

Source: [PR #7498](https://github.com/CrocSwap/integer-mult-bounds/pull/7498), head `f69879a7dc7e633151e582dae11f4480290405c9`, base `e54523517d0f03e58352e647c403a5af3e525a57`.

The PR's stated result is **no verified gain**. On the signed #7481 word and #7113 caller, it reports two endpoint-window enumerators agreeing on 60,806 coframed two-role windows, with eight positive relaxed-price windows. The eight exact two-role actions are single shears, not crossed monomial exchanges. It also checks one named three-role cycle at chart 1049: the relaxed rank change `(9,5,2) -> (5,7,4)` has gross about `0.12252572644` raw against 17 raw units for one added rank-one paid position per copy. Two exact prefix probes rule out the required contrasts; an independent suffix minor limits output-preserving carrier changes to dimension at most one, while the cycle requires rank two. The paid itinerary and κ are unchanged; the PR explicitly does not claim a new supplier or complete κ replay.

The finite scope is material: the two-role check has 30-second runner caps, a 64-event window limit and a 32-case positive-window cap; the cycle argument is for the single named cut and three carriers. Its source pins identify the #7481 word archive (`acee3236…fcc0a9`), decompressed native word (`64fca675…ed68b8`), application (`1d93fae9…b1799`), and caller (`255d89f3…b47bc`). The proof identity and selected file pins are in `MANIFEST.json`.

**Independent review:** I inspected the proof and the independent window, prefix and suffix checkers. The finite exclusion logic is internally consistent: fixed-sum strict concavity makes rank imbalance the sign test; a shear with both diagonal entries nonzero is not a crossed monomial; the prefix probes are exact linear separators; and the displayed nonzero suffix minor gives the stated one-dimensional kernel bound. I did not fetch the large pinned word or rerun the upstream wrapper, so the reported enumerator totals and source replay remain upstream claims, not independently replayed results here.

**Relevance to the q8 histories/Y-feedback work:** This is useful as a narrow no-gain result for fixed-paid endpoint rearrangements on the unchanged #7481 caller. It does not address the current changed q8 histories, altered source encoding, historical packet trajectories, or arbitrary Y-feedback. Those mechanisms change the word/interface and are outside the fixed-paid windows and one named cycle proved here. It therefore neither supplies nor rules out the q8 construction under review.

## PR #7496 — Lean ledger and rank-one obstruction

Source: [PR #7496](https://github.com/CrocSwap/integer-mult-bounds/pull/7496), head `5dfe94ea4855b54bc31c2b4d55f86ddb78f8510b`, base `e54523517d0f03e58352e647c403a5af3e525a57`.

The PR adds an `Init`-only Lean file and a short report. Its five theorems check (i) rational inequalities and the supplier/invoice margins for the cited Frontier 7000 constants, (ii) literal main/helper job and rank-mass sums, and (iii) the determinant-zero identity for two rows that are scalar multiples of one shared wire, plus a Role 275 instance. The source has no explicit imports and ends with `#print axioms` for all five theorems. The core obstruction is simply
`det(s₁(a,b), s₂(a,b)) = 0`; therefore two required probe rows with nonzero determinant cannot both come from one common scalar wire.

**Independent review:** I inspected the complete Lean source and report, and checked the determinant argument algebraically. I did not compile the module locally (Lean/Lake are not installed in this workspace). The source proves arithmetic on embedded constants; it does not parse or validate the underlying native word, Python ledger, or source history. The generic determinant identity is mathematically reusable over any commutative ring when the target determinant is nonzero, but this file formalizes it over `Int`, not an arbitrary field. The named Role 275 determinant is 4 over the integers and becomes 0 modulo 2, so that particular instance cannot be used as an F₂ obstruction.

**Relevance to the q8 histories/Y-feedback work:** This is a useful small lemma for ruling out a rank-one, two-probe fusion when the exact target minor is nonzero. It does not establish a rank-q obstruction, constrain which historical rows can be acquired, handle chart motion or carrier chronology, or exclude arbitrary Y-feedback. It is compatible with the current q8 analysis but does not close its remaining construction question.

## Decision

Neither PR changes the five foundations or the current q8/Y-feedback proof interface. #7498 contributes a bounded no-gain family check on an unchanged source; #7496 contributes formalized arithmetic and a narrow rank-one identity. Treat the authors' finite replay and build statements as claims unless separately rerun from the pinned artifacts. #7497 was not needed for this q8/Y-feedback triage.
