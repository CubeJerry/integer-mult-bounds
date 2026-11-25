# Source audit — staged, not complete

| Source | Exact pin | Coverage this checkpoint | Missing |
|---|---|---|---|
| CrocSwap AGENTS.md, autoresearch.md, CONTRIBUTING.md | e54523517d0f03e58352e647c403a5af3e525a57 | Read current guidance and conventions | Other priority and selected-review files, discussions and overlapping PR proofs |
| OpenAI tape uniformity.tex | 3344da59991ed94f9ba711217b29c1d760badfa6; blob 5ea562044e8830c8402f2a61caf8729dd2feb086 | Read complete single-machine candidate/precision/space/scheduling section, plus subsequent corollaries | All earlier constructive stages, precise recurrence and all implicit constants |
| OpenAI finite Fourier | 3344da59991ed94f9ba711217b29c1d760badfa6 | Identified as indispensable companion | Full proof, spectra and repair quantities |
| OpenAI tensor/permanent and lower-bound papers | 3344da59991ed94f9ba711217b29c1d760badfa6 | Identified | Complete reads |
| Historical moonshot STATE.json | CubeJerry/research/moonshot-005-program blob 411eb5aba139d47ff3d705cb7da51a4d42660d64 | Read state schema and sampled scoped obstructions | Full source proofs, programme history and remaining files |
| Proposed direct-corollary PR | CrocSwap #8102, head e8ac3899a03df571fbbd5d1e42a6d9bb196abde0 | Read scope, parameters, incomplete template caveat | Independent source verification and current review status |

No claim is made that the entire literature or proof-chain audit has been completed. Read all relevant primary proofs before relying on quantitative template or recurrence statements.

## S002 expanded coverage

The lead verified all 103 available source files in the five requested manuscript build directories plus Lean scope documents 130 and 379 against the pinned Git blobs. `audit/source-manifest.json` records identities. This is integrity verification, NOT a claim that all 103 proofs were read.

| Reader / source chain | Actual coverage | Reuse and limits |
|---|---|---|
| Lead: tape intro, interchange, Walsh | Read complete text of these chapters | Exact machine model; label/routing recursion; selected Walsh caller. Fixed-parameter constants remain explicit gaps. |
| Lead: tape integers | Read digit packing, CRT, short-transform construction through the sharing-workspace step | Source implementation dependencies; remaining coefficient streaming, complete rounding/carry and lower chain still staged. |
| Lead and A/B/C: Fourier repair, kernel, binary | Read complete relevant proof chain | Count interpolation, Hermite repair, generalized Clifford representation, shared routing, normalized binary closure. |
| A: tape uniformity, permutations and quantitative interfaces | Full uniformity read, relevant source chain and exact thresholds recorded in route notes | New controller/chunking proofs are separate from claiming the source constants quantified. |
| B: Fourier layers and recovered local contraction | Full route-specific read and current mathematical review | Recovered files retain original hashes and provenance; their earlier review statements do not imply fresh events. |
| Lead: Lean docs 130 and 379 | Read both scope documents | Reported formalization includes the uniform exact multiplier and Weak-ETH lower bound, while division/root and several stronger companion bounds remain unformalized. No Lean build or comparator run this session. |
| Canonical guidance and selected record | Read AGENTS, autoresearch, CONTRIBUTING, bottleneck/glossary/family status and selected-result metadata | Selected #7000 remains source-specific conditional history, not the global post-November mathematical baseline. |

The full tensor-geometry/permanent/lower-bound chain, complete historical archive and bibliography lineage remain staged reading. None of the new upper-bound component claims imports Weak ETH or the old five assumptions. Live Discussions remain unread because the available fetch endpoint rejected them.

## Focused E001 audit delta (26 November 2026 Melbourne)

All primary manuscript reads retain OpenAI pin `3344da59991ed94f9ba711217b29c1d760badfa6`. Lead read the complete single-machine proof, introduction/model, integer packing and short-transform sections, interchange label/Gram/spectral/contraction proof, and Walsh recurrence/precision proof. Route workers read the Fourier repair/kernel/binary dependencies they use. The formal files `NearSquareRoot/Main.lean`, `UniformWorstCase.lean`, `UniformMultiplicationRelease.lean`, and scope documents `lean/docs/109.md`, `130.md` were inspected; no kernel build or complete dependency audit was run.

Current community selected record is #7000/#7001, conditional kappa `0.00363005817`; the priority summary still contains an older selected value. Read Discussion #1163 and retrieved newest views of #1166/#1167; cached newest views are not complete live overlap coverage. PR #8102 remains a fixed-exponent corollary at `e8ac3899a03df571fbbd5d1e42a6d9bb196abde0`, not a quantitative overhead theorem. Hutter's 2002 primary paper was read for prior art on moving search cost into time-bound computation; no claim to invent that general principle.

Concurrent S002 compact prediction at `bbfd1086b7e629375f9891998e4602270d8801cd` was read and credited; E001 redirected overlapping work. Detailed proof/review scope is in [REVIEWS.md](results/epsilon-uniformity/REVIEWS.md). Prior source archives and the historical programme remain unchanged.

## E001 checkpoint 3 — Primary reading and implementation audit

Root read the primary Baker–Harman–Pintz paper, *The difference between consecutive primes, II* (2001), Theorem 1 and its effectivity comment, for the input-dependent-radix proof. The eventual prime theorem's absolute threshold is retained, not numerically certified. Root re-read the full November interchange and Fourier repair proofs, including the finite-basis descent in `cor:swap-repair`, while checking the original-template tower draft. That draft's physical compiler audit is still in progress. No full Lean build or complete implementation replay is claimed.

## S002 completed upper-bound source chain

The lead now read complete November tape `interchange.tex`, `permutations.tex`, `walsh.tex`, `integers.tex`, `uniformity.tex` and September `sections/02-streams.tex`. The Fourier `repair.tex`, `kernel.tex`, `binary.tex` chain was fully read and its relevant quantitative interfaces rechecked. B independently read the integer/permutation chain; C independently checked matrix-root, cyclotomic and rational-address dependencies. Accepted polynomial dependence is on actual expanded finite data, including numeric address magnitudes.

The lead also read complete tape `lower.tex`, `graphs.tex`, `advice.tex`. That conditional lower-bound chain uses variable-count Weak ETH and a partial-transposition reduction; it is not a premise of the upper bound. The complete tensor/permanent companion proofs, historical archives and formal dependencies remain outside this completed audit. No Lean build occurred.

Baker-Harman-Pintz Theorem 1 and its introductory effectivity statement were read for the absolute eventual prime cutoff; no numerical cutoff or independent number-theory proof is claimed. Harvey's October commentary was read only at summary scope and is historical context. Source pins were rechecked at 14:09 UTC and were unchanged.

## E001 checkpoint 4 — Full written compiler admission and overlap

Root and Route C independently read the critical November tape/Fourier proof chain and September elementary-stream, ordered-affine, triangular-factorization and parking proofs against E001's finite constructor and compiler invoice. Both admitted polynomial dependence on the complete finite budget S, including numeric address-scaling values, basis-expanded scalar tables, actual instruction access, precision, fallback and all visited-space regions. The specified efficient generator and explicit diagonal order are essential; arbitrary effective implementations are not covered.

Concurrent S002 checkpoint96028cba1342c02bdca1f537ae9a80485087bdf3 was read and reconciled before this update. Root read its accepted explicit extraction, bounded generator and scalar growth proofs and its general supported-lift obstruction. E001 sharpens the parameter rate and supplies a stronger large-q literal p² spectral fraction; the complementary S002 results and provenance are preserved. A limited current primary-source search found no competing quantitative statement in the retrieved material, but is not a comprehensive novelty audit. No Lean or full tape implementation replay was performed.

## S002 third-wave audit delta

The lead additionally read complete Fourier `layers.tex` and `geometry.tex`, including occupied-workspace restoration, characteristic-two order-three arithmetic closure, spectral-price interfaces and the two-phase conversion argument. The new physical order-three result is compared against that source arithmetic closure; the source already treats general finite fields algebraically, while the new note supplies its explicit physical shared-swap closure and parameter accounting.

Primary-source searches identified generalized Clifford/Ulrich representations and modular incidence-rank literature as leads. Their search excerpts or abstracts were inspected; complete external proofs were not imported. The new scoped Chow, width and sketch proofs are written out self-contained. Full companion tensor/permanent geometry proofs, remaining Fourier chapters and a complete formal dependency audit remain unfinished. The 103-file integrity manifest continues to mean byte verification only.


## E001 additional review and source refresh — 15:20 UTC

Prompt, canonical main and OpenAI manuscript heads were rechecked at2026-11-25T15:16:37Z and remained at their recorded pins. Root directly read S002's new sharper-parameter proof, compact integral IP bridge and exact formal Chow barrier at4689161c5bc6c9e64536034d4fa6af033d26a3e0. The other new characteristic-two component records are preserved, without claiming a fresh E001 audit of their complete proofs.

E001 root read the primary Sheng–Tribone tensor-factorization Proposition3.2 and Hrubes–Yehudayoff homogeneous-formula statements while investigating a different representation. The integral Gaussian-binomial identity and general scalar-ring descent are being checked self-contained. Search excerpts are not substituted for the full source proof. The proposed formula construction is not yet an admitted global premise.

## S002 fourth-wave finite representation audit

The lead reread the full physical compiler and common-cap assembly, source integral interpolation and matrix-root construction, full binary implementation, and the kernel/tape Walsh batching paragraphs. The source permits different fixed affine matrices at successive stages and arbitrary integer batch width. Its original repeated-pencil and power-of-two-width constructor are not downstream requirements. B recorded a separate varying-pencil interface audit.

The lead retrieved and read Sheng–Tribone's ring convention, Definition 3.1 and Proposition 3.2 in the publisher's primary PDF, DOI 10.1017/nmj.2025.12. C separately read those sections. The known graded tensor construction is credited; the complete external paper and all predecessor proofs are not claimed as read. Source-wide literature/formal limitations remain unchanged.

## S002 fifth-wave source-interface review

For the fixed-field theorem, the lead reread the pinned tape `walsh.tex` batch, physical recursive call, work/visited-space and precision paragraphs, plus the complete rational Newton/division and auxiliary-map notes. The source admits fixed pointwise coefficient lists and varying affine pencils; rational replacements are prepared once to dyadic precision with explicit rounding errors and setup cost. The completed characteristic-two interchanger moves encoded numerical records without identifying their coefficient rings.

The count-bit identities are proved locally and independently checked. No exhaustive literature review or new reading of every companion manuscript is claimed. Exact source pins and the prior partial-read ledger remain the provenance basis.
