# A sharp factor-two image gap for finite-abelian native sums

For the 111 native owners let A be any finite abelian group of order n>1. Give each proper ordered cell a function fᵢⱼ from A to A fixing zero, and define

    Tᵢ(x) = xᵢ + Σⱼ fᵢⱼ(xⱼ).

Assume bijectivity only on the prescribed native 221-edge bipartite tree in the transcript. If |im T| < 2n⁹, then A is a vector space over F₂. There are additive automorphisms Pᵢ of A with fᵢⱼ=PᵢPⱼ⁻¹ on every one of the 6,470 proper cells. Conversely these maps have exactly n⁹ outputs. The strict cutoff is optimal even when all proper functions are bijective and the binary dimension is at least two. The theorem concerns separable sums, including normalized edge functions obtained by translating constant offsets.

## The native restricted images

A transcript chart has two receiver rows r,s, eight exterior anchors C with no pair of distinct proper links within C, and a set D of 3 to 10 exterior donors. Every row-donor cell on {r,s}×D is proper. For c∈C and u∈{r,s}, a proper (u,c) implies absence of every (c,d) with d∈D. The verifier reconstructs each D directly from the published native root dot products and checks the eight diagonal pivot owners.

For any B⊆D, restrict the input to C∪B and observe the two receiver rows and eight anchor outputs. Fix arbitrary anchor outputs y_c and donor inputs x_d. Each x_c is uniquely determined by y_c minus its incoming donor contributions. Any c contributing to r or s has x_c=y_c. The resulting restricted projection therefore has precisely n⁸ times the size of the sum of graphs Γ_d for d∈B, where Γ_d consists of (f_rd(x),f_sd(x)) as x ranges over A. Each fixed anchor output translates the sumset by a constant. It follows that every such sumset has fewer than 2n points.

## Three donors identify an additive automorphism

Suppose three graph columns project bijectively onto one common row. Write their raw graphs as (x,h₁(x)), (y,h₂(y)), (z,h₃(z)), with h_j(0)=0. Their threefold sum projects onto A. Since this sum has fewer than 2n pairs, some first-coordinate value t has just one second-coordinate value b. Thus

    h₁(x)+h₂(y)+h₃(t−x−y)=b    for every x,y∈A.

Comparison with (x+y,0) gives h₁(x)+h₂(y)=h₁(x+y). Taking x=0 identifies h₂=h₁, and h₁ is additive. The displayed equation and h₃(0)=0 now give h₃=h₁. If one of the three columns is bijective on both rows, h₁ is an automorphism. The argument permits the other two functions on the second row to be arbitrary at the outset.

Once a particular donor graph equals the graph H of an additive automorphism, |H+Γ_d|<2n for every other eligible donor d. H has n elements, and this sum is a union of H-cosets. It therefore consists of H alone, since Γ_d contains zero. Every (f_rd(x),f_sd(x)) lies in H, with no initial bijectivity requirement on d.

## Propagation in the original coordinates

Fix row and column permutations Pᵢ,Qⱼ along the 221 tree edges such that fᵢⱼ=PᵢQⱼ there, choosing P₀=id. Existence follows by walking the bipartite tree, composing or inverting known bijections. Every permutation fixes zero. No output sum is acted on by a row permutation at this point.

Maintain the proper cells already known to have their prescribed factor PᵢQⱼ, and maintain components of rows for which P_sP_r⁻¹ is known to be additive. A chart names a donor known at both rows. If the two rows are in different components, its record exhibits two further distinct donors whose functions are known on the same first row as the named donor. The three-column argument proves the transition is additive, because on the named donor it agrees with P_sQ_j(P_rQ_j)⁻¹=P_sP_r⁻¹ (or its inverse for the swapped orientation). This joins the two components. Once the transition is additive, the named graph equals its subgroup. The two-graph coset argument places all other eligible graph pairs in that subgroup. Any donor with one previously known factor now has both prescribed factors.

The physical certificate uses 2,965 charts, comprising 110 new additive row joins and 2,855 applications with the requisite transition already known. It certifies every proper cell and one connected component of all rows. All Pᵢ are therefore additive automorphisms of A. Each Qⱼ is still only a permutation. The independently replayable transcript occupies 17 KiB compressed. Its uncompressed SHA-256 is `c1164d41f47ffc27e0a437f0b49914ebe6a56ddeb3de4daddd5b21477060fbd4`.

## Recovering the alphabet and the true own terms

Reparameterize each input by zⱼ=Qⱼ(xⱼ) and apply Pᵢ⁻¹ to the ith output. These bijections preserve image size. The proper summands become zⱼ. The own term becomes dᵢ(z)=Pᵢ⁻¹Qᵢ⁻¹(z).

Take the certified native disjoint ten-by-ten 0–1 minor of signed determinant ±2. Its nine unit Smith invariants and one factor of 2 give restricted image n¹⁰/|A[2]| over A. The strict global hypothesis gives [A:A[2]]<2. Thus all of A is killed by 2. It is now an F₂-vector space.

For each i take the nine native rows and nine columns disjoint from each other and i with an odd scalar determinant, whose border at i using canonical own diagonal 1 has even determinant. The nine rows determine the nine column inputs uniquely for every chosen zᵢ and every fixed set of their nine outputs. In the ith output, substituting this solution leaves a constant plus dᵢ(zᵢ)−zᵢ, since the scalar Schur coefficient is one over F₂. The restricted image contains n⁹ times the number of values of dᵢ(z)−z. This positive integer multiplier must be one. It is zero at z=0, so dᵢ=id, and Qᵢ=Pᵢ⁻¹. The canonical native scalar binary matrix K has rank nine, giving the converse by coordinate changes. Both the ten-square and all 111 bordered witnesses were independently rechecked on the native owner table in the global rank-rigidity package.

## The strict endpoint

Choose any proper cell (i,j) outside the prescribed tree. On A=F₂ᵐ start with every proper function the identity and change only this cell to I+uλ with u a nonzero vector and λ a nonzero linear functional. For m≥2 choose λ(u)=0, making the changed cell a transvection and keeping every proper function invertible. For m=1 the changed cell may be zero. The 9×9 native pivots avoiding each i and each j imply eᵢ is outside the column space of K and eⱼᵀ is outside its row space. Consequently the rank-one perturbation (eᵢ⊗u)(eⱼᵀ⊗λ) increases the binary rank of K⊗I from 9m to 9m+1. Its image has exactly 2n⁹ elements. The verifier directly checks native (1,0) at m=1,2,3,6.

## Independent replay

From the workspace, run the following command against the published layout. Certificate generation optionally accepts `--seeds` pointing to the upstream CLOSURE and WEIGHTED files. Replay of the included certificate needs only the native layout.

```sh
python work-review/nonlinear-rigidity/triples.py \
  --layout programme/research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz \
  --out work-review/nonlinear-rigidity/output
```

The four targeted faults independently replace an exterior anchor by a receiver, collide two of the three identified donors, remove a required additive join, and use an ineligible pivot donor. Each is rejected for its intended reason.
