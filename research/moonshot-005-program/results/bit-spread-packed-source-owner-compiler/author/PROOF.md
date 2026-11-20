# Binary source programs for four native chart placements

Two independently specified source words supply the native H interfaces. For the 23-chart placement, 68 patched donor stars use explicit early matrix words and cache their late parities. The other 43 donors use the singleton-aware source program. For the alternative 24-chart placement, 71 patched donor stars use the same compilation with all three real singleton coordinate groups integrated where required. The other 40 use the singleton-aware background.

| Complete source-only quantity | 23 charts, 774 native fibres | 24 charts, 801 native fibres |
| --- | ---: | ---: |
| Forward binary ADD | 1,709,119,124 | 1,782,446,364 |
| Optional pure-X inverse ADD | 1,407,198,044 | 1,470,152,892 |
| Forward plus inverse ADD | 3,116,317,168 | 3,252,599,256 |
| INIT and dirty CLEAR | 2,165,760 each | 2,151,360 each |
| Additional MOVE | 0 | 0 |

The figures count whole-record binary instructions on literal owners. They give the source contribution to the proposed staged computation. The current inverse-fibre conditions cover the displayed chart observations. The required global coefficient graph at D, K and the output remains open.

## Owners, source basis and timing

A native donor $j$ starts with 3,840 original six-bit field records. They have IDs $3840j+8c+b$, where $c$ is its native coordinate and $0\le b<8$ its copy. The Y space has an additional offset of $111\cdot3840$. For either special placement the marked component occupies ordinals 0 through 767 and the unmarked component 768 through 3839. Scalar column $s$ and spinor coordinate $t$ use ordinal (16s+t) within the component. Each pair $(b,b+8)$ is handled by a common $32k$-by-$32k$ field word, with $k=3,12$. This fixes the original coordinate ordering in all shared inverse identities, including donor 61.

The compiler enumerates the actual native route lines, sorts X and Y field IDs by donor and H plane, and enforces the phase counts from those routes. The 23-chart case reconstructs one shared full coefficient table at donor 61 and 67 other literal stars. At full early incidences the ordinary quotient of each spinor lane is loaded. Mixed incidences use the prescribed $k$-by-$2k$ frame. Each is completed by elementary coordinate rows indexed by the nonpivot columns of that frame, in ascending order. At a mixed designated chart this is exactly the unframed second spinor lane bundle. At singleton-bearing stars in the 24-chart placement, all $3k$ ordered rows of the literal repaired matrix are genuine early coordinates in each stripe. Each of the eight repeats therefore contributes separately to the local value and first Hasse derivative word. The arbitrary ground Y at these singleton planes arrives independently.

Across marked and unmarked components, every donor's early matrix placements partition all its 3,840 original X records and target each of its 3,840 true outgoing X holders exactly once. Fully early three-donor planes use degree before the 16 spinor lanes. Mixed two-donor and singleton planes use degree before the eight stripes and consume respectively $2k$ or $3k$ fields when the source supplies their entire early bundle. Half-early donor groups supply $k$ fields before the eight stripes. These orders match the physical H source and port permutations.

The compiler reduces both early matrices to identity and replays the inverse streams on every original field basis column. Its binary primitives come from the source owner compiler. The six-bit scalar multiplication words are replayed on their binary bases. The holder permutation is replayed on all 3,840 labels. Each chosen late coordinate is a single original-spinor parity. It is computed on stationary fresh records while all original X values are available. The word adds that parity to the incoming true Y baseline and clears its cache. The pure inverse replays the reverse X permutation and the component reductions once the unchanged downstream early word has been reversed.

| Patched donors only | 68 stars | 71 stars |
| --- | ---: | ---: |
| Early basis ADD | 1,354,971,848 | 1,421,038,368 |
| Actual X owner permutation ADD | 4,632,048 | 4,837,536 |
| Late parity accumulation ADD | 265,340,640 | 278,256,072 |
| True Y injection ADD | 1,175,040 | 1,229,760 |
| Cache INIT and dirty CLEAR | 1,175,040 each | 1,229,760 each |
| Pure-X inverse ADD | 1,359,603,896 | 1,425,875,904 |

The remaining source entries are copied from the per-donor manifest, restricted to exactly the complementary donors. For the 43-star background, the early basis, shuffle, late evaluation and snapshot counts are 44,631,096, 2,963,052, 34,414,680 and 990,720. The pure-X inverse is 47,594,148. For the 40-star background these four forward counts are 41,520,792, 2,756,196, 31,886,040 and 921,600. Its pure-X inverse is 44,276,988. Each background snapshot counts one binary ADD, INIT and dirty CLEAR.

## Fifteen two-centre components

The same program accepts the two-centre packing parameter table. Its 30-chart option compiles all 75 special stars and the 36 remaining singleton-aware background stars. Its 31-chart option includes eight true special singleton stars, 78 patched donors in total and 33 regular background donors. Within each pair the shared donor receives exactly one early frame and one physical source word. Every literal repaired singleton has all three coordinate groups early. The two raw word manifests charge all H input addresses and bind every field operation stream.

| Complete source-only quantity | 30 charts, 1,005 local fibres | 31 charts, 1,041 local fibres |
| --- | ---: | ---: |
| Forward binary ADD | 1,738,948,668 | 1,811,051,516 |
| Optional pure-X inverse ADD | 1,463,687,780 | 1,528,136,740 |
| Forward plus inverse ADD | 3,202,636,448 | 3,339,188,256 |
| INIT and dirty CLEAR | 2,125,440 each | 2,113,920 each |
| Additional MOVE | 0 | 0 |

For the 30-chart version the patched donors use 1,418,802,656 early-basis ADDs, 5,109,840 holder-permutation ADDs, 244,250,008 early parity ADDs and 1,296,000 Y-injection ADDs. The corresponding figures for the 31-chart version are 1,486,329,112, 5,312,880, 254,610,496 and 1,353,600. The complementary ordinary-source manifests charge respectively 829,440 and 760,320 snapshot lifetimes. The receiver and middle equations remain separate.

The corresponding options are `--parameters "$R/bit-spread-two-centre-packing/author/output/PARAMETERS.json"` for the 30-chart case, with `--singleton-coefficients "$R/bit-spread-two-centre-packing/author/output/SINGLETONS.json.gz"` added for the 31-chart case. The receipts are `output-30/RESULT.json` and `output-31/RESULT.json`.

## Reproduction

From a pristine repository checkout set `R=research/moonshot-005-program/results`. Run the compiler with the following inputs and any fresh output path. Python 3 and NumPy are sufficient.

    python -B "$R/bit-spread-packed-source-owner-compiler/author/compile_pack.py" --repo . --parameters "$R/bit-spread-overlap-source/author/output/PARAMETERS.json" --background "$R/bit-spread-rs-physical-word/author/source-output/PER-DONOR-COSTS.json" --out /tmp/packed23

To generate the 24-chart receipt add the option below and choose a different output directory.

    --singleton-coefficients "$R/bit-spread-singleton-fibre-repair/author/output/SINGLETON-COEFFICIENTS.json.gz"

`output/RESULT.json` and `output-24/RESULT.json` retain the complete input pins, stage counts, per-donor prices and digests of every reduced field stream and native holder dictionary. Add `--emit-words` to materialize these streams and native holder records. The uncompressed contents are deterministic. To inspect the literal binary instruction stream for a generated special donor, run

    python -B "$R/bit-spread-source-owner-compiler/author/expand.py" --word-dir /tmp/packed23 --donor 61 --stage early --limit 50

The available stages are prepare, early, deliver and inverse. The source compiler, independently reconstructed packing and independent six-bit field checker are loaded from their repository paths by default. Corresponding CLI options permit those same files to be supplied explicitly. Credit @CubeJerry and the native source, phase, spread and chart contributors. This implementation used OpenAI assistance. The complete multiplication bound and strict recursive suppliers remain open.
