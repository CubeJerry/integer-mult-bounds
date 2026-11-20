# Four arbitrary geometric quotient edits preserve strict nonsaturation

**Author theorem; independent admission pending. No source/H construction or new kappa is implied by the bound alone.**

The earlier two-edit protection theorem can be strengthened to four edits. This provides actual freedom to change a connected source word while retaining a proved global obstruction-avoidance invariant. Full source cuts, common H maps and all physical costs remain separate requirements.

## 1. Statement

Let F be any finite extension of GF64 and k>=1. At one ordinary donor use the geometric28-node source tuple

    F_a=(1,a,...,a^15) tensor I_k, a in Q,
    Q={a:a^9+a^18+a^36=0}.

Replace the quotient at each node of an arbitrary set E, |E|<=4, by any linear k-by16k map. Require every source view used below to remain invertible. Fix distinct source nodes H,R and any finite family of actual geometric or native receivers seeing both. Let L'_i be each receiver's whole new off-H inverse fibre.

Put m=|E minus {H}|. Then

| Effective edited nodes m | Uniform bound on dim sum_i L'_i |
| ---: | ---: |
| 0 | 5k |
| 1 | 9k |
| 2 | 12k |
| 3 | 13k |
| 4 | 14k |

In particular all four-edit sources remain strictly below the15k saturated quotient kernel at every H/R pair. Every coefficient choice satisfying the source-cut premise is covered. This is not a bound only at selected construction centres or on random edits.

## 2. The geometric core span identity

For a node a define

    D_(d,a)(z)=(z^(d+1)+a^(d+1))/(z+a).

The six-dimensional normalized fibre core S_a is spanned by

    1, z+a, D_(3,a), D_(7,a), D_(13,a)+D_(4,a), D_(15,a).

This follows by expanding the previously proved U_a(v) in the six independent Moore coordinates v,v²,v⁴,v⁸,v¹⁶,v³². The displayed leading degrees are0,1,3,7,13,15, so the dimension is exactly6 over every extension.

The exact identity

    D_(15,a)+a² D_(13,a)=z^15+a z^14                 (1)

is obtained by multiplying both sides by z+a. Modulo the eight-dimensional space of polynomials of degree<8, only D_(13,a) and D_(15,a) matter. Equation(1) shows that for any r distinct nodes,

    dim sum S_a <= min(16,8+r+2) = min(16,r+10).     (2)

There are r possible D13 classes and at most two additional common directions z14,z15. No generic-rank assumption or finite enumeration enters this upper bound.

For r=1 the dimension is6. For r=2 it is10: the core-overlap lemma gives S_a intersection S_b=span{1,z}. Thus for r=1,...,5 the applicable bounds are

    6,10,13,14,15.                                  (3)

The finite checker authenticates the Moore/core formula at all28 nodes and the exact polynomial identity. Its numerical ranks illustrate sharpness of the core envelope; they are not the proof of (2).

## 3. Every new propagated fibre lies in one fixed core envelope

Let

    T={H} union E,   W=(sum_(a in T) S_a) tensor F^k.

At a receiver i, use its old invertible sixteen-quotient evaluation coordinates. On a vector in the new off-H fibre, every unchanged off-H observation is zero. Thus only old coordinate blocks belonging to H or an edited visible node can remain nonzero. Their old inverse spaces lie in the corresponding S_a tensor F^k. Hence L'_i is contained in W.

Every receiver considered sees R!=H, so its new off-H fibre is also in ker F'_R. Consequently

    sum_i L'_i <= W intersection ker F'_R.           (4)

It remains to justify subtracting k dimensions; the new R quotient must not be assumed surjective on W without proof.

If R is unedited, its evaluation map is surjective on the constant-polynomial copy F^k inside every S_a tensor F^k, hence on W.

If R is edited and the receiver family is nonempty, choose one receiver i. Its full new16-quotient view is invertible. The new inverse-R space therefore has dimension k and maps isomorphically under F'_R to F^k. All unchanged coordinates vanish on that inverse-R space except possibly at edited nodes. Since R belongs to E, that space is contained in the sum of old inverse spaces at nodes in E, and hence in W. This proves F'_R|W surjective in the edited case too. An empty receiver family has zero propagation and needs no such choice.

Thus dim(W intersection ker F'_R)=dim W-k. Using |T|=m+1 and(3) proves every entry of the table. This argument also covers H itself edited: its observation is not among the off-H constraints, which is why m omits it.

## 4. Consequences and boundaries

Any common invertible linear whole-bank change of input coordinates preserves the bound. Separate invertible output changes preserve the same kernels. Tensor repetition multiplies dimensions, and fixed coefficient-field extensions preserve all identities. General nonlinear edits are outside the theorem.

For a direct-sum source, one protected component suffices to prevent full15k-total saturation provided the other components retain invertible source cuts: each other propagation lies in its own quotient kernel and cannot exceed its15k-component bound. This is the same direct-sum interpretation as in the earlier two-edit theorem. It does not establish common H transport or defeat other joint-fibre obstructions.

The edit-count guarantee is sharp. The independently replayable literal witness in `output/FIVE-EDIT-WITNESS.json` uses scalar width k=1 at native donor0, edits nodes0,3,5,7,8 (planes806,854,293,283,13), and retains all63 geometric source cuts. For H17 (node10) and R806 (node0), the15 native receivers

    1,7,10,11,12,48,55,56,73,81,90,95,96,97,102

have inverse-H fibres spanning dimension15, exactly the edited R quotient kernel. The scalar rows are regenerated by the pinned S030 deterministic coefficient function with tags `four-edit-sharpness/3/{node}`. All matrices and fibre columns are also stored literally, so the witness does not rely on trusting the generator. Tensoring these rows and fibres with I_k proves failure of a universal five-edit strict bound for every k>=1, and the witness persists over every extension of GF64. This counterexample concerns source cuts and saturation only; it makes no claim to have compatible common H providers.

For the literal width3 construction, three edits give upper39<45 and four edits give42<45. The previously admitted two-edit component improves from the older42 bound to36. This does not change the operation invoice or the complete kappa.

## 5. Next constructive use

An extra quotient change can be chosen to annihilate all current inverse fibres at an already built H where that quotient is visible. Full source rank then preserves those entire H fibres while allowing other H fibres to move. The four-edit theorem protects the resulting source against every old saturation test, provided the full cuts still hold. The actual joint-source translation kernels and shared H providers must then be rechecked; nonsaturation alone has already proved insufficient.

Credit @CubeJerry, the S030 geometric field/Moore identities and two-edit theorem, and the S031 core-overlap proof. Substantial OpenAI assistance. Independent admission pending. No new complete kappa.

## 6. Replay and proof/evidence split

From the repository root:

```sh
python -B research/moonshot-005-program/results/bit-shared-h-s031-construction/four-edit-protection/check.py --repo . --out /tmp/s031-four-edit-review
```

Expected receipt: `PASS_FOUR_EDIT_PROTECTION_AND_FIVE_EDIT_SHARPNESS`. The checker authenticates all28 geometric cores, all756 ordered core-pair ranks, the polynomial identity, five exact envelope samples plus the six-core full-span control, all315 literal geometric bases of the admitted two-H component, and the full five-edit native saturation witness. Sections2–3 supply the universal proof; a finite check cannot replace their quantifiers.
