# Independent reconstruction of two overlapping H charts and their extensions

I reconstructed the 23-chart source with 68 genuine donor stars and 774 native receiver/chart inverse fibres. H263 and H642 share donor 61. Its 28 outgoing source matrices agree coefficient by coefficient across the two constructions. The remaining 21 charts use distinct donor stars. An alternate extension with 24 charts, 71 donors and 801 native receiver/chart pairs also passes the ordinary source tests. Four of those donors carry a genuine singleton. Their physical H outputs use the additional singleton-repair certificate.

## Native coordinates and common inverses

The checker uses the pinned root Gram matrix for receiver adjacency and the native plane and port incidences for every chart. It labels an off-centre plane by intersecting the radicals of its five incident central ports. These native incidences identify one singular point in every case. The SHAKE strings generate the two-dimensional sharing frames and the filler rows over six-bit field elements. An independent logarithm implementation supplies arithmetic in the field with polynomial modulus $z^6+z+1$.

For the two-centre construction, the two donor controls and the other centre's shares impose two groups of $k/3$ independent relations on $12k$ latent coordinates. The checker explicitly computes the common nullspace, with free columns in ascending order. It constructs donor 61 from each centre and compares all coefficients at all 28 actual outgoing planes. The shared early schedule uses H263's frame exactly once at this donor. Both designated centre readouts use their full unframed coordinate. At every patched donor the exact rows loaded onto real early owners form a basis of dimension 96 or 384 per pair of spinor lanes.

For each geometric receiver at a designated chart, the checker solves the complete first donor system, ordered by the centre followed by its 15 off-centre planes. It applies the inverse lift to each of the other two donor systems in the original source coordinates. The central Vandermonde readout yields the identity and every off-centre block gives zero. The entire off-centre matrix row blocks match on all three donor stars after the native plane relabelling. Rescaling one physical central output row at a second donor preserves every local rank and fails the common-lift identity at every selected chart. Each chart has 36 geometric receiver systems. Their native subsets account for 774 and 801 chart observations respectively.

| Per component | 23 charts | 24 charts before singleton repair |
| --- | ---: | ---: |
| Native special donor stars | 68 | 71 |
| Proper native source-to-H pairs on those stars | 3,973 | 4,135 |
| Proper parent donor cuts | 4,284 | 4,473 |
| Distinct exterior matrices independently reduced | 610 | 637 |
| Other native donors | 43 | 40 |
| Proper native pairs on other donors | 2,497 | 2,335 |
| Patched donors carrying a genuine singleton | 0 | 4 |

Every exterior matrix is reduced to full rank $16k$. The core and frames act on the supplied field copy coordinates, with identity on 16 spinor coordinates in the unframed ordinary maps. Early frames, paid permutations and true singleton extras have their separately stated coordinate conventions. The global 15-by-15 scalar-coefficient action and residual endpoint remain open. The prescribed target still requires an actual simultaneous operation at D, K and the receiver terminal.

## Replay

From the repository root, set `R=research/moonshot-005-program/results` and run

    python -B "$R/bit-spread-overlap-source/review/check.py" --repo . --parameters "$R/bit-spread-overlap-source/author/output/PARAMETERS.json" --out /tmp/packed-source-review --extended

The output includes every chart's native count and a digest of its 36 independently computed original-coordinate lifts. Credit @CubeJerry and the contributing source, phase, spread and native-geometry authors. The review used OpenAI assistance.
