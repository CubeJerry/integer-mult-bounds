# Every native proper donor is necessary at the nine-bank optimum

Write h=rank(M)−9b for a native fitting over an arbitrary field with true b-dimensional own blocks. For each of its 6,470 proper cells,

    b−rank(Mᵢⱼ) ≤ 6h.

There is no initial nonsingularity assumption. In particular every proper cell is invertible at rank 9b. The native global rectangle theorem then implies that rank 9b occurs exactly in characteristic two and that every such fitting is the canonical K under simultaneous changes of basis on the 111 native roles.

There is an entropy statement for arbitrary zero-error nonlinear broadcast. Write B=log n for a uniform input bank and ε=H(Y)−9B. If receiver i can decode its bank given the transcript, its other proper donors, and a compressed version g(Xⱼ) of one proper donor, then

    B−H(g(Xⱼ)) ≤ 6ε.

Every one of the 6,470 directed native arcs is individually critical. Removing any one arc gives entropy at least (9+1/6)B and at least n^(55/6) possible messages. This applies without separation or additivity assumptions on the broadcast. For a native finite-abelian separable-sum fitting at |im T|=n⁹, each individual proper term fᵢⱼ(Xⱼ) serves as such compressed side information for its own receiver. Thus every fᵢⱼ is bijective. The sharp finite-abelian theorem with the prescribed tree then applies automatically, giving elementary binary alphabets and fᵢⱼ=PᵢPⱼ⁻¹ with additive native gauges. Without separability the conclusion is the arc-information bound.

## One five-variable conditional marginal in the Petersen graph

Use the ten pair labels (01,02,03,04,12,13,14,23,24,34), numbered 0 through 9. Set S={0,1,3,4,5} and v=9. For any monotone submodular function H on those ten variables, normalized by H(∅)=0, with each legal decoding increment equal to B,

    H(S∪{v})−H(S) ≤ 2(H(P)−5B).

The second integer certificate uses only the two permutations of the five underlying labels fixing this particular S and v. Its 6 monotonicity, 26 submodularity, 20 decoding and one empty-set terms give the exact raw coefficient +8 at P, +4 at S, and −4 at S∪{v}, with right-hand side 40B. Inequalities carry nonnegative multipliers. `horn.py` expands the group and checks integer equality on all 1,024 unconstrained subset coordinates. The coefficient 1/2 in the corresponding lower bound H(P)≥5B+Δ/2 was found by a rationally certified Shannon relaxation. The bound also applies after any of the 120 label permutations, giving 60 distinct five-premise implications.

Each physical chart used in the transcript has four true isolated own diagonals C and ten genuine Petersen roles P. For linear fittings put H(S)=dim(Σ_{j∈S} col(M_:j)), where M_:j is a native block column. The rows of C annihilate all columns of P and supply an invertible diagonal on C. Thus H(P)+4b≤rank M and the local increment is at most 2h. For nonlinear codes use H(S)=H(Y|X outside S) on the entire native alphabet. Decoding the four isolated anchors given the other native inputs outside C∪P gives H(P∪C)=H(P)+4B. Thus the same marginal is at most 2ε. All Petersen decoding equalities remain valid on these global functions.

## A three-step entropy deduction for each true directed arc

Fix a native recipient i and proper donor j. Start with S₀ containing j and every role that is neither i nor a proper donor of i. In each of the first two certified steps a genuine five-premise Petersen set lies inside S₀, so each new marginal costs at most 2ε by submodularity. In the third step another actual five-premise set lies inside the enlarged set and its new role is i. The three resulting rank or entropy increments total at most 6ε, or 6h over a field. Therefore

    H(S₀∪{i})−H(S₀) ≤ 6ε.

The transcript has exactly three steps at each of all 6,470 directed proper cells. It draws on 2,673 distinct 14-owner native charts and names two independent antecedent additions per direction. The verifier starts from the published native roots, validates every chart and all 19,410 actual role implications, and rejects damaged weights, charts, order, recipients and missing directions. The uncompressed transcript SHA-256 is `d043279392b20c74f0367b3b66abb282a522ff60cabba802544536bb7b16e665`.

For a linear fitting, row i annihilates S₀ except for Mᵢⱼ and has the identity on column i. Projection at row i shows that adjoining its own block to S₀ increases dimension by at least b−rank(Mᵢⱼ). This proves the corank bound for every field.

For a zero-error broadcast, the conditional increment is I(Y;Xᵢ|X_W), where W consists of all other proper donors of i, excluding j. The inputs are independent, so this equals B−H(Xᵢ|Y,X_W). Since the decoder can also use g(Xⱼ), the remaining conditional entropy is at most H(g(Xⱼ)). The claimed lower bound on the compressed donor entropy follows. Deleting the edge takes g constant. At ε=0 the image of g must have at least n elements, giving bijectivity for an n-to-n proper function.

At the programme's b=3,840, a deleted proper block would require q≥35,200, 512 above the 34,688 limit. At q≤34,688 every proper block has rank at least 3,072. In particular a physical candidate cannot simply drop one entire directed donor and recover its loss through other donors within that return budget.

```sh
python research/moonshot-005-program/results/bit-native-petersen-converse/author/horn.py \
  --layout research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz \
  --horn research/moonshot-005-program/results/bit-native-petersen-converse/author/output/HORN.json.gz \
  --dual research/moonshot-005-program/results/bit-native-petersen-converse/author/output/LOCAL-LEAK.json --out /tmp/native-petersen-replay
```

## Exact integrality for additive edge maps

Suppose every proper function is a homomorphism of a common finite abelian group, with no bijectivity premise. Split the alphabet into its primary groups Aₚ. Homomorphisms preserve these components, so the image size factors over p. The unconditional nine-bank lower bound holds separately on each Aₚ. Both |im Tₚ| and |Aₚ|⁹ are powers of p, so each ratio is either one or at least p. Consequently |im T|<2n⁹ forces exact equality on every component. The preceding classification gives an elementary binary alphabet and canonical simultaneous additive gauges. Every other additive fitting has at least 2n⁹ outputs. The earlier single-transvection example attains this endpoint with all proper cells invertible.
