# Analytic recovery wave 1: overlap and scale audit

Base `e54523517d0f03e58352e647c403a5af3e525a57`; selected conditional kappa
`0.00363005817`. Research checkpoint only; no proposed PR or new theorem.
Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.

## Outcome

No independently publishable result was established. A scale omission in
the historical accretive Toeplitz statement is real under a uniform reading,
but later retained work already provides a stronger correctly scaled
interface. The selected conditional bound is not refuted.

At `c52345caa318fc6b1b6e2659c57d746317a72823`,
`research/fine-prime-padding/vendor/pr1758/outer/GAUGEFREE-INTERIORS.md`,
Theorem 4.1 bounds logarithms of prefix/suffix/inverse-prefix norms by
`O(log N * log(2+Lambda/mu) + log N)` for arbitrary accretive Toeplitz H.
Under constants uniform in Lambda and mu, take dyadic N and `H=2^N I`,
`Lambda=mu=2^N`. Endpoint logarithm is N log 2 versus O(log N).
For `H=2^-N I`, the inverse endpoint has the same obstruction. Allowing
the hidden constant to depend on absolute scale avoids the contradiction
but does not provide the desired uniform precision transfer.

The byte-exact source is retained at
`sources/research/fine-prime-padding/vendor/pr1758/outer/GAUGEFREE-INTERIORS.md`.
SHA256 `d1423ac0ea0003521797209f4396e6981a66994bbee4f8b48026e5b95f8c5116`,
Git blob `20585e44fa4e49b13b5d8495bbf6ed254459a362`, 18,370 bytes including
original CRLF line endings.

An elementary safe transfer normalizes by dyadic `r=2^ceil(log2 Lambda)`,
uses a normalized-circuit theorem for H/r, then appends N scalar r gates.
If all four normalized cut operators have cap B, the scaled circuit has
cap `B max(1,r,r^-1) <= 2 S B`, `S=max(1,Lambda,mu^-1)`, including
partial final scalar layers. Scaling multiplies operator error by r;
any output rounding is a separate term. This is not claimed as novel.

Actual normalized Gaussian G'_s has diagonal one. Thus `mu<=1<=Lambda`
and `S<=Lambda/mu`: the original ratio guard remains adequate there.
External positive gauges and raw scalars retain their existing charges.

## Superseding work already read

- `research/rational-unitary-fft/FULL-PROOF.md` on pinned main assumes
  `Lambda,Q>=1` separately, bounds all leading-section inverses by Q,
  and supplies a polynomial four-cut envelope using `chi=Lambda Q`.
  Its online width includes `log Lambda + log Q`. It cites #1758 as
  predecessor and is already stronger than the proposed correction.
- #4253 at `ac14c1409c261d64d9856a5a473d8b7f2be8c302`,
  `research/rational-fft-fixed-h/DENSE-PROOF.md`, pays E0 in suffix
  amplification and gives a scaled zero-shear control. No scientific
  predecessor replay was run; both written proofs were read.
- #4193 at `52e962e318423be1fe8ed9d705dba92067795b61` already preserves
  raw alpha^-1 and gauges in its inverse bound. Open #7180 at
  `f1401fd8618394634c4f2a2171a668ba5f6915c2` is a distinct half-shift
  inverse-envelope refinement.

## Other candidates excluded by overlap

- Original transform/recovery identities and S factors: #4320 and
  `certified-gaussian-recovery` already cover them.
- Fine-prime existence and theta conditioning: #1797 and
  `fine-prime-trudgian-audit` already provide scoped audits.
- Partial matching cuts: #4976/#5940; actual matching rounding: #5240.
- Deferred normalized recovery: CubeJerry #6993 provides 3Gamma and the
  native endpoint, with production-controller obligations retained.
- Original-q T-to-S extraction: `original-q-field-extraction` implements
  the encoded O(Tp0) boundary, including history and origin contracts.
- CRT whole-tree state and encoded frontend: CubeJerry #7152/#7154.

Coverage: pinned main metadata, named proofs/README files, direct PR
metadata and narrow search queries. Not exhaustive novelty certification.

## Restart

Do not publish this historical scale correction as new assumption removal.
Wave 2 targets one missing compositional preservation/error contract at
the actual #7152/#7154 physical CRT frontend/state boundary, on their
exact heads. All five assumptions remain; no new kappa.
