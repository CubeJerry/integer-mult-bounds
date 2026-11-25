# External research and attribution

- OpenAI, November 24, 2026: *The logarithmic exponent of integer multiplication on tapes*, source openai/math at 3344da59991ed94f9ba711217b29c1d760badfa6. All n L^(1/2+o(1)) claims derive from this paper.
- OpenAI, November 24, 2026: *The logarithmic exponent of finite Fourier transforms*, companion proof; detailed audit pending.
- CrocSwap #8102 by zxv: source-specific formal/repository contract specialization to any fixed kappa<1/2; this is not an overhead rate and no new algorithm is claimed here.
- CrocSwap #7000 and the original research/moonshot-005-program are historical source archives; any transferred construction must retain contributor-level credit. All five prior assumptions are not automatically inherited.
- Further prior art and independently applicable theorem searches pending.

## S002 literature check (2026-11-26 local)

The live canonical and OpenAI source pins remain e54523517d0f03e58352e647c403a5af3e525a57 and 3344da59991ed94f9ba711217b29c1d760badfa6 at this checkpoint. The narrow PR search found #8102's fixed-kappa corollary, already recorded; no complete new overhead theorem was identified. This is not an exhaustive novelty search. The Discussion connector rejected its endpoint, so live discussion coverage remains incomplete.

- Josh Alman and Ryan Williams, *Probabilistic Polynomials and Hamming Nearest Neighbors* (2015), [author-hosted full version](https://people.csail.mit.edu/rrw/polys-hamming.pdf), Theorems 1.1–1.2. The paper gives degree O(sqrt(n log(1/epsilon))) probabilistic polynomials for symmetric Boolean functions over fields and integers. Read abstract, definitions and theorem statements in this session, not the full proof. This establishes relevant prior art: low-degree symmetric probabilistic prediction is not a new concept of this programme. The application here additionally requires a deterministic finite batch, full-rate row semantics, exact spectral repair and physical cost accounting.
- Srikanth Srinivasan, Utkarsh Tripathi and S. Venkitesh, *On the Probabilistic Degrees of Symmetric Boolean Functions* (FSTTCS 2019), [primary proceedings paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol150-fsttcs2019/LIPIcs.FSTTCS.2019.28/LIPIcs.FSTTCS.2019.28.pdf), Theorems 3–4. Read definitions and theorem statements. Its classification spans fixed positive characteristic and characteristic zero, up to polylogarithmic factors. Do not equate its general probabilistic-polynomial model with the programme's more restricted shifted-count model or claim the programme invented their degree scale.
- Alman, Chan and Williams, *Polynomial Representations of Threshold Functions and Algorithmic Applications* (2016), [arXiv record](https://arxiv.org/abs/1608.04355). Identified as a relevant low-randomness precursor. The proceedings PDF retrieval returned HTTP 401; detailed proof and applicability remain unread. No theorem is imported from this lead.
- OpenAI, *Average sensitivity of polynomial threshold functions* (September 25, 2026), [source directory](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/Average-Sensitivity-of-Polynomial-Threshold-Functions-September-25-2026), [formalization scope](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/lean/docs/127.md). The stated 8d sqrt(n) influence bound is a relevant possible nonsymmetric-prediction obstruction. Only the theorem/scope were inspected; no new claim relies on an independently rebuilt proof of it.

Current novelty position: claim source-specific constructions, scoped quantitative proofs and verified applications. No priority claim is made for the general moment method, interpolation, limited independence, universal search, or the square-root degree scale.

## S002 additional primary-source checks

- Baker, Harman and Pintz, *The difference between consecutive primes, II* (2001), [paper](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/BakerHarmanPintz.pdf). Read Theorem 1 and effectivity comment. The eventual exponent 0.525 is stronger than the source's 0.6 use. The absolute cutoff is not computed; the full proof was not reread.
- David Harvey, October 20, 2026, [commentary](https://web.maths.unsw.edu.au/~davidharvey/research/subnlogn.pdf). Read the opening summary only, which distinguishes plausibility comments from full proof review. This is not a premise or validation of the November result.

A narrow current-source search did not identify a prior explicit November overhead rate. This is not comprehensive coverage or evidence for priority. The result is described as a quantitative source extraction.
