# Independent review: BIT eight-packet downset cut

Status: **accepted, with the stated route and transfer scope**. I found no mathematical or replay defect in the source-specific lower bound (q\ge 8) or in the B8 partial reference. The lower bound is an information cut; it proves necessity and does not show that eight packets suffice.

## Independent source and word checks

I parsed the pinned native directly and reconstructed all 111 source lines as exact rational vectors, then independently formed the binary matrix

\[
B_{ij}=((2g_i)\cdot(2g_j)/2)\bmod 2.
\]

The independently computed rank is 8 over \(\mathbb F_2\). For each of the nine retained 8-frames in the certificate, I checked all 64 exact real dot products, verified that each selected source line is nonorthogonal to every frame normal, checked that each selected endpoint chart is the corresponding 7-dimensional orthogonal facet, and obtained the exact principal block (B_{S,S}=I_8+J_8), of rank 8.

I then replayed all 1,070 operations in the compressed B8 reference with a separate field-value interpreter. It reached all 222 specified endpoints, restored (X=x), and produced (Y=y+Bx); all 111 target rows fail because (B_{ii}=0). It uses 230 nested moves with profile \(\{7:222,8:8\}\), 824 additions, eight zero initializations and clears, eight distinct descending lifetimes, and peak owned count one. The eight packet encoders restrict with rank 8 to every one of the nine retained frames. Thus the cut tests are all saturated while the full target still fails.

The replay verified exact chart inclusion for every MOVE. The eight packet values are built at the full Hub, each enters the zero chart once, and each is cleared before the same owned label is initialized for the next packet. Counting only the single label would be an error; the relevant count is eight physical descending lifetimes.

## Proof audit

Choose any one retained frame (S\) of eight pairwise real-nonorthogonal root lines. Let (F_i=L_i^\perp) and (U_S=\{C:C\subseteq F_i\text{ for some }i\in S\}\). Since every (L_j) for (j\in S) has nonzero inner product with every frame normal, each selected (x_j) starts outside (U_S). Every selected target chart lies inside it. The union is downward closed, including charts not explicitly present in the original word.

Fix all other independent inputs to zero. Initially no value inside (U_S) depends on (x_S\). Same-chart processing, zero initialization, and erasure cannot bring in outside dependence. An ascending move cannot enter a downset: if (C\subseteq D\) and (D\in U_S), downward closure implies (C\in U_S). An upward local copy follows the same rule. A descending physical carrier can enter (U_S) only once, because every later chart is a subchart of an inside chart and remains inside. Its crossing value has at most (V) coordinates. Therefore the entire inside computation factors through at most (qV) scalar coordinates, even if packet values are correlated, receive feedback, or undergo arbitrary same-chart block operations. The eight exact endpoints contain the identity map on (x_S\), of rank (8V\), so (8V\le qV\) and (q\ge8\).

The proof is valid over any common coefficient field and for every positive block volume (V). It does not need a Gram assumption, canonical fitting, invertibility of an intermediate cell, or absence of chronological feedback. For (q=8), the stacked first-entry map must have full rank (8V) at each retained frame cut. That is a necessary saturation test only.

Whole \((\text{chart},\text{value})\) relabeling is harmless when interpreted as relabeling physical trajectories: it does not move a value between charts. The proof does require that an actual descending physical carrier be counted as a packet trajectory regardless of its current role name, and that reinitialization after retirement starts another counted lifetime. A free exchange of values between distinct chart slots, a public route that moves down and later back up, or an uncounted downward local copy would cross the cut outside this count and invalidate the conclusion. These exceptions are explicitly excluded by the proposition; they should remain prominent in any reused statement.

Zero-initialized stationary caches and arbitrary extra upward-only copies are covered. Cache content arriving from outside can only enter through a counted packet; later copying or feedback among inside records does not increase the dimension of the entering packet vector. A packet may be encoded using outside feedback before its crossing, or combine with earlier inside information afterward; the rank bound still counts its actual (V)-coordinate crossing value once.

## Scope limits and correction to a control description

This does not prove that a q8 construction exists, or that q8 movement price is sufficient. The B8 word is a concrete cut-saturated failure. The geometric q8 theorem assumes all information entering the chosen downset via downward motion is among the counted (q) packet lifetimes. Nonzero preloaded cross-chart values, resets that create fresh descending trajectories without charging them, and nonmonotone public routes fall outside the theorem.

One small control-description issue: the root verifier's `coordinate_bus_inputs_are_inside_union` assertion checks the coordinate bus source lines against the facets indexed 0 through 7, which is not one of the nine certified nonorthogonal frames. The intended compatibility control is nevertheless true for a retained frame: all eight coordinate source lines (L_0,\dots,L_7) lie in the union for the ninth retained frame \([36,37,62,64,67,68,77,78]\). For the first retained frame, (L_0\) is outside the union. This does not affect (q\ge8\), since the coordinate bus completes no endpoints indexed by the selected first frame and so is not a counterexample; but I recommend changing the verifier/control wording to cite the ninth retained frame if the inside-union claim is kept.

The source-specific frame premise is exact: the cut theorem needs only one of the retained pairwise-nonorthogonal frames. The nine-frame parity certificate is used for the stronger necessary q8 saturation screen; it is not a prerequisite for q≥8.

## Frozen pins

Independent replay result: `RESULT.json`. Replayer: `replay_independent.py`.

- Native source: `programme/research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz`, SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
- Root proof: `root-work/bit-eight-downset-cut/PROOF.md`, SHA256 `43d72b141b2b9f477e2ab6d89c08b12590837db1516cb80f8cace755a3164bd1`.
- Root source receipt: `root-work/bit-eight-downset-cut/RESULT.json`, SHA256 `eae778a8f94f33f2bf2389e7acac212dd0c2ea4c53f6491c8b220219baf186d2`.
- Root partial word: `root-work/bit-eight-downset-cut/WORD.json.gz`, SHA256 `820ec11e14ae00d98bc0fdc109d5d8db64f6a6bea7f2cf76f5bc743a5d4abb4c`.
- Root verifier: `root-work/bit-eight-downset-cut/verify.py`, SHA256 `44a242813de96fddfb4cf22233ea35cfb62afaaba47327f7db9e7167ae51b1a0`.

The independent replay is stdlib-only and does not import or call the root verifier or the retained replay module.
