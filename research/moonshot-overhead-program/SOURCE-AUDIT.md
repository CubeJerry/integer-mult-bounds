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

## S002 pre-close pin refresh and remaining limits

At 2026-11-25 15:57:17 UTC, direct remote-head reads confirmed canonical main
`e54523517d0f03e58352e647c403a5af3e525a57` and OpenAI math main
`3344da59991ed94f9ba711217b29c1d760badfa6`, unchanged. At 15:58:38 UTC,
the GitHub connector confirmed prompt blob
`b5762a4dacb999703e83621301a455fbb12755f7`, unchanged; the lead reread the
requested session instructions. This is a source freshness check, not a new
full-source audit. Companion proofs, full formal dependencies and complete
community/novelty coverage retain their listed limits.

The lead additionally inspected primary positive-characteristic symmetric
polynomial literature at the scopes recorded in EXTERNAL-RESEARCH.md. It is
not imported as an unexamined dependency or treated as proof of novelty.

## E001 formula-source and primary literature reconciliation

Root read the complete new cyclic construction, regular dyadic descent and physical transfer, and rechecked arbitrary batch-width source interfaces. B independently checked finite-ring repair and binary/Walsh widths. Root also read S002's formula construction, cyclotomic generator, extraction and lead review at58c754b583815e4fe40d333ec9d71e4c254749ba; the same-rate derivations retain separate credit.

The scoped MR symmetry/module audit is results/epsilon-uniformity/route-a/mr-symmetry-literature.md, with a separate C review. No nearby existence theorem is imported as an actual finite-free dyadic generator. Hrubes--Yehudayoff's homogeneous multilinear formula theorem is the explicitly identified external input for the new restricted recipe lower bound, independently reviewed by A and root.

## Fresh concurrent fixed-field result — 16:09 UTC

Before publishing this focused checkpoint, remote848fbf1d7a5e192aa352d79b4d3e36fa06be21ee was read and preserved. S002's new characteristic-two count formulas establish IP4 and its stronger third-root envelope. E001's dyadic formula theorem remains a separate weaker result. Root has read the new finite formula, complete extraction and lead review; additional E001 finite and physical reviews are in progress. The dyadic MR hypothesis remains open even though its displayed rate is now attained by S002's different fixed-field construction.

## S002 closing freshness and concurrent preservation — 16:18 UTC

Canonical and OpenAI main were rechecked directly, and the prompt file's blob
was rechecked through the connected GitHub file reader. All three pins remain
unchanged. The newly arrived E001 head
`d1f3baccdcc547263c0c0cc7241aa0cb1ef12bee` was fetched; its 42 changed files
were reconciled, including 35 focused-session files preserved byte-for-byte.
The lead read its shared-state and summary changes. This reconciliation is not
a claim to have independently reread all of its new focused proofs. S002's
current fixed-field result remains the stronger explicit programme envelope.

## E001 closing integration — 16:23 UTC

E001 root read S002 B1-B11, Q1-Q13, its lead gate and IP4 bridge. E001 C separately audited the finite constructor and A separately audited both-branch physical composition at848fbf1, with exact blob receipts. Root read both audits. The final28a7435 theorem diff is a scope wording correction; optional prime-carry and structured-check additions are preserved without a fresh E001 proof audit. Source branch heads remained unchanged16:20:39 UTC; focused and parent prompt blobs were verified unchanged16:15:45 UTC.

## S003 resumption and critical-chain audit

Remote canonical main, OpenAI main and prompt pins remain as recorded at resumption. Lead reread the complete source interchange, selected Walsh and first single-machine section, plus S002 Q1-Q13, count/label formulas, physical compiler, cyclic and structured-shift interfaces, and current S003 proofs. Root guidance, selected record and relevant family/priority sections were read. Public Discussion1163 start-here guidance and newest1166/1167 pages were retrieved; full comment coverage is not claimed. The newest50 open-PR metadata were inspected; #8102 now has head `a739963c682d47b07e949861da58d2a1bcdbc4c6`. A limited current search found no applicable stronger explicit envelope; this is not a novelty certification. Historical, companion and full formal-dependency reading remains staged.

## E002 physical-profile admission audit

OpenAI and canonical source heads remain pinned unchanged. The focused and
parent prompt contents were rehashed at 22:10 UTC and match their original
blobs. Fresh tape/Fourier critical-interface reading, formalization scope
and actual Main.lean/comparator distinction, current PR/discussion coverage,
primary literature and unread dependencies are recorded in
`results/epsilon-uniformity/sessions/E002/SOURCE-AUDIT-E002.md`. The complete
P2--P11 proof was independently reviewed by A/C and audited by the lead.
No new formal build or exhaustive novelty certification is asserted.

## S003 polynomial-profile milestone

Lead/C reread pinned Walsh, guarded-XOR/controlled-block, integer shape/precision/carry, common-machine scheduling and Fourier normalization sections. Remote9e84956f, E002 same-scale theorem and S004/E003 records were preserved. C separately reviewed E002 height-priced streams and repair. Novelty audit remains nonexhaustive.

## E003 reading and concurrent reconciliation — first checkpoint

E003 root read the complete pinned tape single-machine and Walsh sections,
Fourier spectral repair, and September elementary-stream/ordered-affine
proofs; read relevant interchange geometry and the actual preceding
rational Newton/finite contraction and auxiliary-cost proofs. It read
S003's full new dyadic geometry at concurrent c65aac11 and is checking the
remaining physical interfaces. It independently reviewed E003 HFS and
matrix/recursive-invoice proofs and replayed exact finite rank tests.
A limited current primary-source search did not identify a stronger
applicable rate in the retrieved material; it is not a novelty audit.
Full historical, companion and formal-dependency reading remains staged.

## S004 scoped refresh and critical-chain read

Canonical main `e54523517d0f03e58352e647c403a5af3e525a57`, OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`, prompt blob `b5762a4dacb999703e83621301a455fbb12755f7` were refreshed at launch. Lead read complete tape interchange.tex and walsh.tex, named S002 fixed-field suppliers and S003 compact profile/geometry/interchange. Prior archive and companion-paper coverage remains staged. Relevant PR metadata includes #8102, a direct fixed-epsilon specialization; metadata does not verify a proof. Live Discussion fetch was rejected, so discussion completeness is not claimed. Concurrent E003 checkpoint df91e4c8e is preserved; overlap and new two-scale proofs remain under separate review.

## E002 variable-profile admission — 22:42 UTC

E002 root completed fresh full reads of Fourier repair.tex, kernel.tex, binary.tex and grids.tex at OpenAI 3344da59991ed94f9ba711217b29c1d760badfa6, alongside the earlier tape/source audits. A/C outer transfers inspect the actual guarded permutations and integer pipeline. The circuit all-length theorem is not imported as a tape primitive. OpenAI and canonical main pins were unchanged during this phase; focused prompt unchanged in content at the later reread. S003/E003 concurrent checkpoints are preserved; their optional advances retain separate review scope. No priority claim is made.

## S003 adaptive caller audit

Pin3344da59991ed94f9ba711217b29c1d760badfa6 remains unchanged. A read all491 lines of `integers.tex`, all `permutations.tex` and `walsh.tex`, and relevant generation/precision/cap portions of `uniformity.tex`. Exact replacement map/lemma labels: `sessions/2026-11-26-S003/route-a/audit-adaptive-integer-caller.md`. C independently audited complete AQ; root reread changed phase/recovery/physical interfaces.

The outer ledger has a fixed log^4 factor and polynomial(k) setup. Norm requests13k/50k and phase errors70k suffice even with the executable b<=4k guard. An integer precision majorant replaces literal all-key coefficient maximization. Shape tests avoid requiring a computed prime-gap cutoff. No new source revision or formal rebuild is asserted.

### E003 update — 2026-11-25T22:59:43Z

E003 lead read complete pinned tape interchange/permutations/walsh/integers/uniformity and Fourier repair/kernel/binary, plus September elementary streams. PS/CL/FP, fixed-three geometry and P-O accepted in results/epsilon-uniformity/sessions/E003/lead/review-source-composition.md. Full archive and novelty audit remain partial.

## S004 second-wave source and dependency audit

Lead read E002's complete variable-profile theorem, admission, sharp interchanger-space supplier and independent review; E003's complete two-scale note and recursive-port floor and its weighted matrix-rank proof sections. A and C checked the full JR replacement against the admitted E002 chain at 8af1911b02c04d0c410dd181597fd160582a78b4. The source Fourier free-endpoint cross-orthogonality interface was read directly; correlated rectangle sides need no artificial anchor.

For the Euclidean companion, lead read the main/intro files, the protocol theorem and surrounding beginning, and the beginning of width including approximation and amplification setup. The resulting scoped note is S004 `lead/spectral-price-source-scope.md`: zero Euclidean spectral price is not free physical movement, and contradiction-hypothesis tagged routing is not an unconditional tape primitive. Remaining companion proof coverage is staged. Source pins and lack of exhaustive priority certification remain as previously stated.

## E002 conditional and geometry checkpoint — 2026-11-25T23:33:42.601963+00:00

E002 refreshed and read the complete focused prompt again, unchanged. New reviewers read the full pinned Fourier kernel and the actual characteristic-two/Newton interfaces for the conditional and query-volume statements. Preserved S003 checkpoint2fde2b0c and E003 checkpoint3b220847, including S003 same-scale independent AQ construction. No fresh exhaustive audit of all concurrent new proofs, priority claim or upstream PR.


## E003 checkpoint update — 2026-11-25T23:37:13Z

E003 lead completed the primary interchange, permutations, Walsh, integers, uniformity, rational repair, kernel, binary and September elementary-stream reads listed in its admission manifest. Additional literature lead: Cardinal, McCarty and Yuditsky, Biclique decompositions from Welzl orders, arXiv:2606.09785v2; introduction and complete Section 2 read, not the entire paper. Its order-to-partition construction motivated E003 exact crown-product run/tree calculations. Pinto EJC21(1)P1.19 was read only at abstract/introduction scope; SEA2025 fractional-rank work only at search-excerpt scope. No comprehensive literature-priority audit is claimed.

## S003 fifth-wave checkpoint

Canonical main e54523517d0f03e58352e647c403a5af3e525a57 and OpenAI main3344da59991ed94f9ba711217b29c1d760badfa6 were live-rechecked unchanged at23:36 UTC. Root reread the Fourier kernel endpoint section and read the full S004 JRT-U transfer, independent C review and second-wave admission at af5d7983. Root read E002's complete noncanonical incidence proof at a8dd6c24, including its constant-weight rank and binomial bounds; no S003 replay of its checker is claimed. The E002 RV admission was read, not all RV suppliers. Broader manuscript and archive coverage remains staged as previously recorded.

## S004 third-wave source scope

Lead read the complete newly published E002 noncanonical zero-Gram-side incidence proof and E003 crown-product ordering/laminar obstruction, plus E002's RV admission. They retain their exact premises and concurrent credit; no complete S004 reread of all newly arrived suppliers is claimed. The P4-free primary-source reading covers the ITC2021 introduction, Theorem 8, Sections 5.1/5.4/6.1 and Section 7; Pinto's local definitions and crown argument were inspected. These global-count/local-load distinctions are recorded in S004 `lead/jr-local-load-gates.md`. B's separate Bostan--Mori recurrence reading and its limits are recorded in B's proof; no unread implementation is imported as a tape primitive.


## E002 final integration — 26 November 2026

E002 refreshed OpenAI math main and canonical main at 23:44 UTC: unchanged at3344da59991ed94f9ba711217b29c1d760badfa6 and e54523517d0f03e58352e647c403a5af3e525a57. Both full prompt contents were rehashed at23:47:41 UTC: focused ce6fe4edbf039aa964a08aaec216a1cc60dbfe2a and parent b5762a4dacb999703e83621301a455fbb12755f7 unchanged. Focused Pinto cover/partition and Ghosal-Karrenbauer binary-rank primary-source reads are recorded with partial-read limits; no priority claim. Complete local source endpoint subsection read for late ER/SS/WC reviews; no full transitive formal audit.

### S004 fourth checkpoint — 2026-11-26T00:21:33Z

S004 lead reread the pinned Fourier endpoint subsection, Bostan--Mori Section 2.1/Lemma 1/Algorithms 1--2 (https://mathexp.eu/bostan/publications/BoMo21.pdf), and Cantor--Kaltofen Sections 1--2 through cyclotomic operation bounds (https://kaltofen.math.ncsu.edu/bibliography/91/CaKa91.pdf). Fully read E002 WEYL-STAR-BATCHING and E003 rank-weighted invoice, star-transposition normal form and support-monotone shared-sum obstruction at 8fbe12b3c. No full-paper/novelty audit or unrestricted routing lower bound is claimed.


## S003 final handoff — 2026-11-26T00:19:10Z

S003 final refresh at00:12 UTC: canonical main e54523517d0f03e58352e647c403a5af3e525a57 and OpenAI math main3344da59991ed94f9ba711217b29c1d760badfa6 unchanged. Final finite proof/code reviews include LP, O4 and TPC. The staged audit outside the reused critical chain remains partial. B's two exploratory web leads are explicitly unread and unused in its PORTFOLIO. No literature-priority certification or formal kernel build is claimed.

### S004 fifth checkpoint — 2026-11-26T00:45:05Z

S004 lead read Gashkov--Sergeev2012 Lemma16 and convolution application at pp1443--1444 (https://web.vu.lt/mif/s.jukna/boolean/Gashkov-Sergeev-Sbornik.pdf). Also fully read E002 COMPATIBLE-ENDPOINT-REUSE and SWAP-WEYL-CONTRACTION-GATE. These have their stated physical/model limits. A renewed local-biclique product search found no verified resolution of JR; no exhaustive literature claim is made.

## E003 final-science checkpoint — 2026-11-26T00:51:12.839544+00:00

E003 records complete reading of the primary tape interchange, permutations, Walsh, integers and uniformity files, Fourier kernel, binary and repair files, and September elementary streams at the pinned OpenAI commit. The wider archive and literature/priority audit remain partial. Concurrent S004 span-weighted preconditioning and E002 occupied-parameter contraction results were read after reconciliation; their provenance is retained.


### S004 final-wave evidence (2026-11-26)

S004 lead fully read E003 ROUTING-STATE-WALK-SHARING.md atbaeb200f5, including Gray walk and binary exception. Overlap retains E003 credit. B read indexed primary Cooley–Tukey p297; lead read the self-contained FFT proof, not the complete primary article. No exhaustive novelty audit.

S004 final provenance addition: Route B actually read Filmus, Smolensky's Lower Bound, Section5/Theorem5.2/Corollary5.3 at https://yuvalfilmus.cs.technion.ac.il/Manuscripts/Smolensky.pdf. The scalar complement/binomial-tail method retains that prior-art pointer; this does not expand the lead's claimed primary-paper read scope.

## S005 source refresh and critical-chain coverage

Programme start62d9d8e9 was reconciled through S004/E003 completion at8a5d9b06. Canonical main e54523517d0f03e58352e647c403a5af3e525a57 and OpenAI main3344da59991ed94f9ba711217b29c1d760badfa6 were live rechecked unchanged. Current prompt and strategy pins are in S005 SESSION.json. Lead read the actual OAI NearSquareRoot/Main.lean closure and relevant AQ, numerical, kernel/binary and outer source sections; C reconstructed the critical source/physical chain; B/C reread outer logarithms for CT. The source vanishing excess alone does not imply AQ's envelope. Coverage remains partial: no full matching-toolchain build, comparator, complete transitive formal audit, exhaustive archive/literature audit or human review. Precise boundaries are in S005's admission and reviews.


## S005 second-wave checkpoint

S005 lead and C independently read the actual general-fare controller, floor clock, exact tie closure and mixed-space interfaces at OpenAI3344da59. Arbitrary fare and floor rounding already exist; separated long-time/small-workspace body execution is the missing bridge. Lead additionally reconstructed the complete named characteristic-two finite suppliers, including current power-of-two cyclic factors and compact check-node field. Exact read scope and limits: sessions/2026-11-26-S005/lead/FINITE-ALGEBRA-AUDIT.md and adaptive-source-interface.md. No full matching-toolchain closure or comparator was run.


## S005 final scientific checkpoint

S005 canonical e54523517d0f03e58352e647c403a5af3e525a57 and OpenAI3344da59991ed94f9ba711217b29c1d760badfa6 refreshed unchanged at02:20:40UTC. Lead/C checked Bshouty–Diab–Kawar–Shahla2016 section2 deterministic fixed-field preprocessing and the published Annals2021 multitape multiplier statement; no full reread of the latter long proof is claimed. Scoped Tal revision1 and Perles–Weinstein operation-model reads are recorded in S005 lead/LITERATURE-REFRESH.md. Wider transitive/archive/priority coverage remains partial.

### S005 final upstream refresh

At 02:41:20 UTC on 26 November 2026, canonical main remained `e54523517d0f03e58352e647c403a5af3e525a57` and OpenAI math main remained `3344da59991ed94f9ba711217b29c1d760badfa6`. The research branch was confirmed at `b07df605a6724c017d0dbf3c3b9952e3fd2a6c58`. The frozen report's earlier 02:20 refresh remains a true historical observation.
