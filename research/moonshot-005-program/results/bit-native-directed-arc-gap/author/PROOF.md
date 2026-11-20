# Quantitative necessity of every original directed donor

The 111 native roles have b independent input coordinates each. A linear fitting has an identity on every true own block and zeros outside the native proper support and its diagonal. Write q for its rank, h=q−9b, and dᵢⱼ=b−rank(Mᵢⱼ) for the corank of a proper directed block. The nine-bank lower bound makes h nonnegative, without any nonsingularity premise.

For 6,462 native directions the result is dᵢⱼ≤7h/5. For the eight remaining directions it is dᵢⱼ≤122h/75. The four unordered exceptional pairs are (7,80), (10,81), (80,96), and (81,95). Both directions in each pair use the second bound. Every coefficient is unconditional on the ranks of the other proper blocks.

The same result holds for arbitrary deterministic zero-error index coding where one donor is supplied through a compressed representation g(Xⱼ). Give each input an independent uniform n-symbol bank, set B=log n, and let ε=H(Y)−9B for broadcast Y. Then replace dᵢⱼ by B−H(g(Xⱼ)) and h by ε. Removing a directed link takes g constant. If a separable fitting is the broadcast, a receiver can use its own edge function as this representation.

At b=3,840 and the programme's 34,688 limit, any proper block in the full Clebsch class must have rank at least 3,661. Each of the eight exceptions must have rank at least 3,632. Deleting one directed block gives the following whole-return lower bounds.

| Deleted direction | Count | Lower bound on q | Excess over 34,688 |
|---|---:|---:|---:|
| Full Clebsch chart | 6,462 | 37,303 | 2,615 |
| Punctured Clebsch chart | 8 | 36,921 | 2,233 |

Thus deletion of any one unspecified native direction requires at least 36,921 symbols. More than one deletion may make this bound stricter. These are native return conditions whenever the physical word realizes the declared fitting or transcript.

## The physical local graphs

On the 16 elements of F₂⁴ connect x and y whenever x+y is one of the five binary vectors represented by integers 1, 2, 4, 8 and 15. This is the Clebsch graph. Use native receiver 0, donor 1 as the local directed-edge labels. Let S contain donor 1 and all the other local vertices except receiver 0 and its other four neighbors. The punctured graph omits local vertex 6, which is adjacent to neither endpoint. Use the same definition of S on its 15 live roles.

The certificate gives 258 native charts of three anchors and 16 labelled live owners each. The three anchors see no proper donor inside the chart or among themselves. Their 16-role plate has exactly the designated Clebsch side-information graph. Together these charts contain the first 6,462 native directed links. Translation of the 16 local vectors and permutation of their five generators send the ordered local edge (0,1) to any directed local edge. The single relation among the generators is their sum zero, so these permutations preserve the graph. Each of the eight exceptional directions has a separate 3+15 chart registering the precise receiver 0, donor 1 and absent local vertex 6. The verifier rechecks every native entry by integer root dot products.

## Exact Shannon inequalities

On either local graph P, let H be a monotone submodular function with H(∅)=0. For U excluding i and all of its neighbors, require H(U+i)−H(U)=B. The two rational certificates prove

    H(P) ≥ 6B + a [H(S+0)−H(S)].

The full coefficient is a=5/7. The punctured coefficient is a=75/122. Each full dual term is a monotonicity or diminishing-returns inequality, a genuine decoding equality, or H(∅)=0. The full chart has 24 underlying generator permutations fixing ordered edge (0,1). The puncture has four also fixing the missing vertex. The verifier expands every term in these raw coordinates using exact fractions, checks every decoding antecedent and positive inequality multiplier, and confirms that only P, S and S+0 remain, with right-hand side six bank units after averaging. Its sparse accumulator represents all 65,536 or 32,768 subset coordinates. This proof is independent of the floating solver used to find an active constraint set. Algebraic elimination recovered the exact rational coefficients.

For a linear fitting take H(U) to be the dimension spanned by the complete block columns indexed by U. Row i kills columns from its nonneighbors and realizes I on its own column, giving the legal decoding equalities. The three native anchors are independent of the P columns, since restriction to their three row blocks kills P and has the true diagonal on the anchors. Consequently H(P)≤q−3b. When S is enlarged to all global nonneighbors of i together with donor j, submodularity cannot increase the marginal of adjoining i. Projection at row i shows this global marginal is at least b−rank(Mᵢⱼ). Therefore dᵢⱼ≤h/a.

For a zero-error code use H(U)=H(Y|X outside U), with independent uniform original messages. This function is submodular because H(Y,X_V) is submodular, H(X_V) is modular and complementing sets preserves the inequality. Each legal decoding increment equals B. The three anchor messages are determined by Y and the inputs outside the chart. Thus H(P)+3B≤H(Y), and the same inequality applies to the global marginal. That marginal equals I(Y;Xᵢ|X_W), where W contains all proper donors of i except j. Since i can decode with the additional input g(Xⱼ), this mutual information is at least B−H(g(Xⱼ)).

## Concrete native fittings with a missing pair

The coefficient one is impossible. One concrete binary fitting has b=406, q=4,004 and both directed blocks (0,1) and (1,0) zero. This gives corank/excess 406/350=29/25 on a pair in the full Clebsch class. A second fitting has b=13, q=128 and both (80,96) and (96,80) zero, giving ratio 13/11 on a punctured pair. These are fittings of all 111 native owners, including every independent input and true own diagonal.

Each constituent word uses either a restricted copy of the canonical binary matrix K or one sum of the inputs of a native proper clique. Every pair of owners in a clique is proper, so the all-ones principal matrix is allowed and has rank one. No constituent contains both endpoints of the deleted pair. The schedule assigns each participating owner its next unused coordinate and stops assigning that owner once it reaches b. Thus its b own rows and b own columns receive the same indices. Under independent row and column permutations the assembled matrix is a direct sum of the actual retained constituents.

The b=406 witness uses 378 canonical words and 602 clique words. The verifier assigns all 45,066 true coordinates and performs binary elimination on every retained constituent, obtaining exact rank 4,004. The smaller witness uses six copies of K with owner 80 omitted, six with owner 96 omitted, and twenty genuine clique sums. It assigns all 1,443 true coordinates and has exact rank 128. Both constructions remain valid after extension to any characteristic-two field. They specify abstract native fitting matrices. They do not supply a causal physical source-to-terminal realization or an improved κ.

## Replay

From the results directory, the Python standard library suffices.

```sh
python bit-native-directed-arc-gap/author/replay.py --out /tmp/native-arc-gap-replay
```

The script locates the original published `bit-all111-tight-port-atlas` layout relative to its own directory. `--layout` accepts an independently relocated file with the same pinned uncompressed SHA-256. Compare the four receipts produced by `replay.py` with `author/output`.

Credit @CubeJerry and the original native owner, canonical coding, rank-nine and directed-arc programmes. Substantial OpenAI assistance.
