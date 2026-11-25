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
