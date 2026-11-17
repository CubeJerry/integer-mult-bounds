# Independent review of the nonregular dihedral row-range theorem

**Accepted.** This extends the earlier regular-character source gate and correctly excludes the unphased active swap at unbounded widths. It is a range obstruction within the retained ordinary-conjugate and fixed finite catalogue hypotheses, with no complete supplier or new κ claim.

The independent checker uses a fresh rational group-algebra implementation of D8 with elements r^k s^e and product (k,e)(l,f)=(k+(−1)^e l,e+f). It does not import or execute the root checker. It verifies the two range projectors, idempotence, orthogonality, both explicit range witnesses, and the missing projector identity. A separate QQ(i) reconstruction of the literal source verifies the two active swaps, their exact characters, and both actual forward conjugates. The receipt pins the reviewed proof, root checker, and root result bytes.

## General theorem

For unitary involutions f,t with z=(ft)² central and involutive, ft=tfz. Thus f and t commute on the z-plus sector and anticommute on the z-minus sector. On the latter sector PTP=P/2 and MTM=M/2. This proves that the displayed Rplus and Rminus are exactly the orthogonal range projectors, rather than merely containers for the two ranges. The witness PT(2Zminus P+Zplus)=Rplus and its minus counterpart establish the nontrivial inclusion explicitly.

Their sum is I−Zplus(I−T). Since the two factors in the missing projector commute, its rank equals its trace. Substitution of the three collective tensor traces gives

    delta_V=(d^V+tr(z)^V−tr(t)^V−tr(zt)^V)/4.

This is an exact formula at each width. It does not tensor a one-column range projector. In particular, a zero defect at width1 does not imply a zero defect later.

The nonscalar argument is correct for all finite dimensions d≥2. A unitary involution has eigenvalues ±1, and a nonscalar one has at least one of each, so its trace has absolute value at most d−2. If zt were scalar, then t would be scalar times the central z; consequently f and t would commute, forcing z=I and t scalar. This is a contradiction. Hence the trace bound applies to both t and zt. At even widths the z trace contributes a nonnegative term. The lower bound is positive at d=16,V=6 by the exact numerator1,718,144, and stays positive at larger even widths because (14/16)^V decreases. The stated scalar control is correct: t=−I also lifts to I at every even width.

## Source application and scope

Both ordinary forward conjugates are necessary hypotheses. They make the transported block range projector ordinary in the same fixed finite group algebra. With the retained F conjugate, all polynomial terms in F,t,z transport ordinarily, including the second bank's J conjugation. Exchanging P and M preserves the same combined rank defect.

The block projector fixes K as an actual operator. It therefore fixes the full four-source term. In the programme's sufficiently large faithful finite catalogue, class extraction commutes with ordinary multiplication and all shorter source words have no Gaussian4 component. Thus it fixes E4. Independent(4,2,1) endpoints require rank(E4)=D, whereas the ordinary range dimension is D−delta_V<D. No purity or injectivity of K is needed, and arbitrary C20 contributes at most three source factors. The argument may select arbitrarily large widths divisible by four, meeting the retained phase subsequence requirement.

For unphased SWAP_ab, the literal character yields row ranks8+8 at V=1,112+112 at V=2, and total3·16^V/4+8^V/2 generally. The width2 defect is32. For SWAP_ab Zc the old3D/4 formula is recovered. The spectator SWAP_cd has nonmonomial forward conjugates and remains outside this exclusion. The earlier frozen one-column unphased negative control is mathematically correct; only an interpretation of it as an all-width escape would be invalid.

## Reproduction

Run `python -B check.py --package PATH_TO_ROOT_DIHEDRAL_PACKAGE --out OUTPUT_DIR`. The finite checks authenticate the group algebra and literal source; the preceding proof establishes the quantified conclusion. This result closes the entire stated nonscalar dihedral prefix class, while preserving the spectator two-bank construction as an unresolved different interface. All foundational assumptions and both strict supplier obligations remain visible in the parent programme.
