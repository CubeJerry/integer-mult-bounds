# External research and attribution

## S008 source comparison and priority

The November integer-multiplication release states a single-machine \(n(1+\log n)^{1/2+o(1)}\) upper bound with linear visited space. Its lower-bound claim has a separate variable-count Weak ETH hypothesis. The present positive clock uses the published transform, the fork's earlier variable-arity derivation and new numerical tape bills. The [consolidated proof](contributions/explicit-overhead/README.md) retains the earlier attribution. [Source repository](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6) · [November manuscript](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026)

Targeted searches of public results and issue/PR text in CrocSwap/integer-mult-bounds and openai/math for “0.501”, numerical thresholds, double logarithms and quantitative excess yielded no matching whole-program cutoff in the inspected material. These searches do not establish priority.

## S007 comparison

Csizmadia's November 2 paired-phase manuscript already claims $O(n\log^{1301/1302}n)$ for two arbitrary binary polynomial inputs in the same fixed-tape time model. Its claim record describes the formal and human review status. The statement supplies a stronger standalone time than the present corollary. The present package develops the reversible factor interface, its positive-precision lift and cumulative linear space. Priority for those constructions has not been established. [Earlier claim](https://github.com/arpcs/finite-field-polynomial-multiplication/blob/e85bc1f6ca0ec9c13281c94b6a3e88ec2cdb4fc5/papers/03-best-binary/versions/0.2.1/CLAIM.json) · [Comparison and sources](sessions/2026-11-26-S007/ordinary-binary-product.md)

## S006 external comparisons

- OpenAI's [integer tape paper](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026) and [finite Fourier paper](https://github.com/openai/math/tree/3344da59991ed94f9ba711217b29c1d760badfa6/preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026) supply the transform identities, tape layout and caller. The quantitative extraction uses the earlier project constructions. The simulated scalar and formal dense-reference theorem refine the proof interface.
- The elementary axis witness uses classical combinatorial sieve ideas. Its contribution here is a sufficient result for the unchanged programmed window with an explicit eventual cutoff. [Koukoulopoulos, chapter 19](https://dms.umontreal.ca/~koukoulo/documents/publications/primes.pdf)
- The ordinary additive butterfly, novel polynomial basis and Frobenius evaluation savings are established. Li et al. and Chen et al. treat Frobenius partitions, with explicit Cantor-basis constructions at power-of-two extension degrees. The 2026 general-basis work already gives arbitrary decompositions and operation counts for the ordinary butterfly. S006's distinct claim is a specific full-field, fixed-head, two-direction representative invoice for $3\mid b$ and its attachment to the caller, covering a contiguous subset of layers. Priority for that refinement remains unestablished. [Li et al.](https://arxiv.org/abs/1802.03932) · [Chen et al.](https://arxiv.org/abs/1803.11301) · [General-basis additive FFT](https://arxiv.org/abs/2608.20855)
- The Frobenius annihilator/conjugate-rank relation is classical. The dimension optimization is applied only to the allowed whole-block support grouping. The finite-field preparation imports polynomial-time normal basis construction; the tape proof prices its stream arithmetic separately. [Huczynska et al.](https://people.math.carleton.ca/~dthomson/Research/pdfs/DThomson-k-normal.pdf) · [Bshouty et al., §2](https://arxiv.org/abs/1602.05032v3)
- Harvey and van der Hoeven provide the published multitape short-integer supplier used in the stronger consecutive-layer count. Fixed Toom-3 already suffices for an unbounded weaker count and for the AQ multiplication proof's outer arithmetic. [Harvey and van der Hoeven](https://annals.math.princeton.edu/2021/193-2/p04)

The relative trace polynomial, its additive fibres and ordinary polynomial CRT use established finite-field algebra. S006 prices a specific coefficient-side prefix and gives a source-matched grouped factor and ordered-stream interpretation. The [general mixed-coordinate division proof](contributions/explicit-overhead/formal/GroupedComposition.lean) establishes both quotient and remainder. Literature priority for the decomposition is unclaimed.

## Earlier checkpoints

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

## S002 matrix-factorization prior art

Richie Sheng and Tim Tribone, [Tensor products of d-fold matrix factorizations](https://doi.org/10.1017/nmj.2025.12), Nagoya Mathematical Journal 261 (2026), e2 (published online 2025). The lead and C read the ring hypothesis, Definition 3.1 and Proposition 3.2. This is established graded tensor-product machinery, with earlier generalized Clifford predecessors. The programme claims no invention of that operation. Its balanced-formula predictor application, effective finite bounds and physical composition are separately proved.

## Restricted multilinear compiler barrier (S002 fifth wave)

Primary author copy: Pavel Hrubes and Amir Yehudayoff, *Homogeneous formulas and symmetric polynomials*, Computational Complexity 20 (2011), 559–578, <https://users.math.cas.cz/~hrubes/PDFs/SymPoly.pdf>. The lead read the model definitions and Theorem 1(i), with portions of its supporting proof; C independently checked the primary theorem and model. No full-paper proof audit is claimed. The published leaf lower bound gives B's scoped width obstruction for the canonical uncompressed compiler on literal characteristic-zero multilinear predictors. It does not constrain the new nonmultilinear characteristic-two spectral formulas. Both the derived count/pruning argument and this distinction passed independent C and lead review.

## S002 final count-formula prior-art check

- Ian Orzel, *Computing the Elementary Symmetric Polynomials in Positive
  Characteristics*, ECCC TR25-128, revision 2 dated 9 February 2026,
  <https://eccc.weizmann.ac.il/report/2025/128/revision/2/download/>. The lead
  read the abstract, introduction, Theorem 1.1 and preceding-work discussion.
  Its literal-polynomial formula model and large-field interpolation results
  are relevant context; they are not automatically the programme's prescribed
  syntactic-degree quotient representation. No complete paper audit or
  priority comparison is claimed.
- Behera, Limaye, Ramanathan and Srinivasan, *New Bounds for the
  Ideal Proof System in Positive Characteristic*, 2025,
  <https://eccc.weizmann.ac.il/report/2025/079/download/> and
  <https://drops.dagstuhl.de/doi/10.4230/LIPIcs.ICALP.2025.22>. The lead inspected
  the primary abstract/contents and the retrieved Claim 4.2 Lucas/symmetric
  function passage. Attempts to retrieve the detailed later PDF section timed
  out; the complete section and proof were not read. The low-digit Lucas
  observation is standard prior art, not an invention claimed by this session.

Neither lead is a premise of the locally proved carry identities. The specific
full-rate matrix application and physical composition still require external
novelty review. The session does not certify discovery priority.

## S004 partition and sparse-repair route

Lead read definitions and introductory theorem statements in Trevor Pinto, *Biclique Covers and Partitions*, EJC21(1) P1.19 (2014), and the introduction/definitions of Ghosal--Karrenbauer, SEA2025, DOI10.4230/LIPIcs.SEA.2025.18. Covers, fractional partitions and exact local partitions are kept distinct; neither paper is claimed to settle JR. Route B read the specified sections of Giorgi--Grenet--Perret du Cray--Roche, *Fast interpolation and multiplication of unbalanced polynomials* (2024), on cyclic folds, derivatives and sparse recovery. Its established derivative-ratio method is credited; the new note proves its own deterministic all-moduli and physical implementation claims. Huang's derivative-based sparse interpolation paper remains a staged full-text lead. Exact reading scope and URLs are in the S004 proof files.

## S003 current-source search and concurrent provenance

A live search used the exact November tape/Fourier titles and overhead/quantitative terms, with a recent-publication filter. It recovered unchanged primary OpenAI sources and derivative listings, but no additional explicit overhead theorem. Only primary manuscript facts are imported. This narrow search is not evidence of priority or exhaustive coverage.

E002 checkpoint8af1911b independently admits the same2/3 log^(1/3) envelope through a different physical/space wrapper. S003 lead read its complete theorem/admission and preserved it; this is not a fresh review of every E002 supplier. S003 supplies direct absolute-space AI/NW/AQ with its own review chain. E003df91e4c8 records a conditional same-scale candidate; S004's separate rectangle/sparse-repair work remains preserved. Established tensor, moment, interpolation and scheduling machinery retain prior-art credit.

## S004 sparse-repair primary-source confirmation

Lead independently read the abstract/introduction, related work, Sections 2.2--2.4 and the start of Section 3 through Lemma 3.4 of Giorgi, Grenet, Perret du Cray and Roche, *Fast interpolation and multiplication of unbalanced polynomials* (2024), https://www-verimag.imag.fr/~grenetb/publis/GGPR24.pdf. Derivative-based recovery and cyclic folding are established prior art; the S004 deterministic all-moduli physical bound and one-sided three-moment certificate are separately proved, with no claim that the paper's randomized algorithm is a deterministic tape primitive. No novelty certification follows from this scoped reading.

## S003 fifth-wave checkpoint

Fresh narrow GitHub searches found only already-known PR8102 and issue8100 among the queried November overhead/title updates; this is not exhaustive novelty coverage. Root read primary Pinto definitions/introduction and Ghosal--Karrenbauer abstract/introduction/definitions on exact versus fractional biclique partitions; neither settles JR. Concurrent S004 af5d7983 supplies JR-only log-free two-thirds; E002 a8dd6c24 supplies separate conditional RV contracts and a stronger noncanonical incidence floor. These are credited, preserved and kept distinct from S003's direct absolute-space AQ and its narrower invoice proofs.


## S003 final handoff — 2026-11-26T00:19:10Z

S003 preserves concurrent E002/E003 same-scale constructions and S004 JR-only conditional transfer with separate provenance. The final carry formula uses standard Vandermonde/telescoping and is credited as a specific compiler application, not a new general addition identity. No primary-source revision was observed on final refresh. Searches and finite checks do not establish novelty.
