# Lead end-to-end review of the explicit source extraction

Status: **accepted as an unconditional quantitative extraction from the pinned November source construction**. Accepted 2026-11-25 during S002. This is an AI-assisted mathematical proof review, not independent human refereeing, a Lean build, or execution of the enormous generated multiplier. No improvement over an unspecified published o(1) is inferred merely from making its rate explicit.

For L(n)=1+log2 n and s(n)=log2 L(n), the accepted theorem gives one fixed deterministic finite-alphabet multitape machine computing the exact 2n-bit product, with

    T(n)=O(n sqrt(L(n)) 2^{O(s(n)/(log2 log2 s(n))^(1/6))}),
    visited cells=O(n),

for sufficiently large n. A correct fixed fallback handles every remaining input length. No conjectural complexity assumption or Weak ETH is used for this upper bound.

## Completed gates

1. The complete integral binary predictor, matrix root, cyclotomic inverse and full-rate basis descent are retained. They specialize to every odd data characteristic. No characteristic-zero count polynomial is substituted into the source's finite-characteristic interchanger.
2. Route C independently accepted the actual finite generator, rational address dependency chain and unit list. All costs are bounded for explicit loops, rather than inferred from output size. The guard N_I<=m^5, N_F<=m^3, p<=m and D_predict<=m covers early successful candidates. Failed trials are bounded by the successful dimensions.
3. The revised pre-padding Walsh acceptance test is sigma/W<=A^rho/4. Even a factor-two padding loss retains contraction at most one half. The full interchange invoice already includes its digit split and occupied reserve descents. Both exact inequalities can be checked by integer powers.
4. The lead separately accepted the physical compiler within its numerical finite-data envelope P. Route B independently audited integer packing, CRT, short transforms, numerical precision, four logarithmic factors and workspace reuse. The one-control stream decomposition keeps the variable word-arithmetic degree absolute. Code, alphabet coordinates, numeric address magnitudes and all storage are charged.
5. The source's fixed O(k log k) short multiplier is used on records; schoolbook arithmetic is used only in finite or polynomial-size setup. PC3 uses 1001+ceil(log2 P), including the extra root-piece factor. A threshold k>=P^C absorbs setup and makes a single absolute multiple of k precision bits sufficient.
6. The prime-shape cutoff U_abs is one absolute eventual cutoff, independent of the target exponent. The primary Baker-Harman-Pintz theorem supports effectivity, but no numerical cutoff is claimed or needed for correctness: actual shapes are tested and failures use the exact fallback.
7. The uniform restart/chunk proof charges candidate generation, fixed descriptions, all failed attempts, index decoding, cleanup, convolution, carry propagation, tape movement and output. Chunking r_j<8c_j brings every completed candidate under one common O(n) visited-cell cap. Sparse indexing avoids hiding an exponential schedule penalty.

## Final rate calculation

The accepted local search succeeds with log2 m_j=O((j+2)^6), and the complete finite envelope is Rhat(m)=2^(2^(m^100000)). Therefore log2 of every profile coefficient and log2 L of each validity threshold is at most 2^(2^(C(j+2)^6)). Fixed powers and scheduler/chunk coefficients remain within that form.

Set X=(log2 log2 s/(2C))^(1/6) and choose j+2 as the largest power of two at most X. The profile majorant is at most 2^(sqrt(log2 s)), eventually less than s and o(s/X). The first inequality proves eligibility at the actual input length, rather than just optimizing a formal exponent. The final overhead logarithm is at most that majorant plus 2s/X. This proves the displayed rate with absolute constants.

The machine need not know C or U_abs to execute this optimization: it runs the explicit uniform schedule. The parameter choice is used only to establish an upper bound on its runtime.

## Evidence and limits

The lead read the entire relevant November tape implementation chain and Fourier repair/kernel/binary interfaces. Isolated finite replays include the scheduler/chunk checker, cyclotomic checks, and Route C's independent generator controls. The latter passed 120 exact inverse products, 480 odd-characteristic reductions, 184 Vandermonde entries, 48 matrix-root cases and 257 parameter invoices. These checks support specific identities; the unbounded-size assertions rely on the written proofs and source interfaces.

This is a very slow explicit subpower overhead. It does not establish 2^{O(s^beta)} for any fixed beta<1, polynomial-in-s overhead, or constant overhead. No kappa_ov is assigned. No numerical practical threshold, complete generated tape program, runtime benchmark, formal kernel certification, literature-priority claim, or upstream acceptance is claimed.

## Reviewed snapshot

| File | SHA-256 |
|---|---|
| `routes/A/bounded-source-generator.md` | `a5bb4762b300e760ce7a8b35bdd30f41284f44f0d8424bb92937b317e405929c` |
| `routes/A/physical-compiler-ledger.md` | `9f23013f778af635cc6512fdba67c95b16d118d7f131bffd45d7c4dc8c8f7cd9` |
| `routes/A/rational-address-and-generator-bounds.md` | `42d75be8fecc7a3d0fdd9af7878f1fab4dbfc0ccfdda0cfeaf92ad026c94d28d` |
| `routes/A/scalar-template-growth.md` | `e71dcae1cebe2e86c80e7e89a6b37cfff4115d39330a1f5b29b1a2d195604538` |
| `routes/A/explicit-extraction-theorem.md` | `ac170e6062950c14826e948582603d6d9e640edfbaf1f87c52b5c0a976bd790f` |
| `routes/A/scheduler-and-chunking.md` | `f0c7c42d825dd18b17a554492107968811c4992c670f3508a2010da9d39875bd` |
| `routes/C/REVIEW-A-BOUNDED-GENERATOR.md` | `878a2b7c76cb2fde946a006d5862044fc60a673a27185fc711e2a8db76718740` |

The status-only revisions in this snapshot do not change the independently reviewed mathematical contents. If a later note improves the profile, this accepted weaker theorem remains a separately replayable checkpoint.

Credits: OpenAI's November/September constructions and their credited predecessors; Jerry Chen (@CubeJerry); three independent route workers and the lead, with substantial AI assistance. Concurrent E001 work is preserved with separate provenance; no priority is claimed over overlapping independently developed results.
