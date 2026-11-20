# The unconditional nine-bank native return floor

Every fitting of the 111 original native roles with a true b-dimensional own diagonal and arbitrary proper blocks over any field has rank at least 9b. More generally, every deterministic zero-error index code on the same side-information graph over a finite alphabet of size n has at least n⁹ distinguishable messages. Receivers may use any decoding function of their transcript and known proper donors. This result requires no bijectivity of any proper cell and allows interactions among different donors. At b=3,840 the linear floor is 34,560 native symbols. The canonical native XOR fitting attains equality over any elementary binary alphabet. An arbitrary physical circuit is subject to this converse whenever its single return transcript and the corresponding authorized local side information recover all original recipient blocks.

## Four isolated native banks and a Petersen graph

On the published native root table, take four anchor owners 0, 14, 15 and 39. Label ten additional owners by the following pairs.

| Pair | 01 | 02 | 03 | 04 | 12 | 13 | 14 | 23 | 24 | 34 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Native owner | 30 | 34 | 66 | 70 | 38 | 59 | 60 | 62 | 63 | 41 |

There is no proper link between the anchor owners, or between an anchor and any of the ten others. Two distinct pair owners have a proper link exactly when the underlying two-subsets of {0,1,2,3,4} are disjoint. This is the standard Petersen graph. All 196 ordered entries of this 14×14 owner restriction are checked by integer dot products. In a linear fitting the principal block submatrix is a direct sum of four invertible true own banks and a Petersen fitting.

## An exact certificate for five Petersen banks

Let P consist of the ten pair labels. Let h be a normalized, monotone, submodular function on subsets of P, with h(∅)=0. Give each owner one unit. Whenever S does not contain i or a Petersen neighbor of i, require h(S∪{i})−h(S)=1. Then h(P)≥5.

The 21 short predicate instances and their integer multipliers are supplied in `output/WITNESS.json`. Four are one-element monotonicity inequalities, eight are two-increment submodular inequalities and nine are genuine decoding equalities. Each template is summed over all 120 permutations of the underlying five labels. The integer verifier enumerates 1,024 raw subset coordinates, without identifying subsets in the same orbit. The full sum has only two nonzero coefficients, +240 at P and −240 at ∅. Its right-hand side is 1,200. All inequality multipliers are positive, and equality multipliers may have either sign. Thus 240(h(P)−h(∅))≥1,200. The chart is tight: the five certified disjoint Petersen links form a perfect matching, so a group sum for each pair suffices on the Petersen graph alone.

For a linear fitting of rank r factor M=UV through an r-dimensional space and let V_i denote the b-dimensional column image of each block column in that space. The true diagonal makes this block injective. The row decoder at i annihilates every V_j with j outside its own and its proper donors. Hence for each allowed S, the b-space V_i intersects the sum of V_j for j∈S trivially. The function h(S)=dim(Σ_{j∈S}V_j)/b has the stated properties over any field. This applies in particular to the actual local Petersen principal submatrix and yields its rank lower bound 5b. The four isolated invertible anchors give the full fitting rank at least 9b.

## Arbitrary nonlinear broadcasts

Fix all other native input symbols and let the remaining 14 native messages be independent and uniform on n symbols. Each of the four anchor receivers can decode its own input from the broadcast Y and the fixed external data. Together the four inputs X_C are functions of Y, so H(Y)=4 log n+H(Y|X_C). Condition on each possible X_C value. The ten Petersen messages remain independent and uniform, and every Petersen receiver can determine its input from Y and its neighboring pair variables. Set

    h(S) = H(Y | X_{P minus S}, X_C fixed) / log n.

It is monotone because removing conditioning can only increase entropy. It is submodular since H(Y,X_U) is submodular in U, H(X_U) is modular for independent X, and complementing subsets preserves submodularity. It has h(∅)=0 for a deterministic broadcast and fixed external inputs. If S excludes i and every proper donor of i, conditioning on X outside S∪{i} provides all side information to its decoder. The conditional mutual information between Y and X_i is then exactly log n, because X_i was independent of the provided symbols and the receiver reconstructs it without error. This is precisely the required decoding equality. The integer certificate gives H(Y|X_C)≥5 log n, hence H(Y)≥9 log n and |im Y|≥n⁹. The same proof applies to any separable fitting's output image and to general nonlinear fits whose own symbol is reconstructible from their corresponding output and proper donor symbols.

A binary canonical fitting of rank nine gives nine broadcast banks on this graph, meeting the lower bound exactly for elementary binary alphabets in the abstract index-code model. Physical costs and the remaining 128-symbol return allowance at the operative multiplicity require separate construction.

## Reproduction

`check.py` needs only the Python standard library, the published layout and the compact witness. It validates the native owner graph, five-link upper witness, every raw decoding antecedent, positivity of the inequality coefficients, the exact integer identity, and targeted falsifications. The optional SciPy discovery program regenerates the same owner chart and dual. The proof and replay do not depend on numerical optimization.

```sh
python work-review/petersen/check.py \
  --layout programme/research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz \
  --witness work-review/petersen/output/WITNESS.json --out work-review/petersen/output
```

Credit @CubeJerry and the original native root and index-code programme. Substantial OpenAI assistance. The result does not change κ.
