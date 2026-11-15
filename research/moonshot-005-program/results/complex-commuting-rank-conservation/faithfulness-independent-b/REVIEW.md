# Independent acceptance of the explicit phase-group faithful-width threshold

**Accepted.** Worker B independently reviewed root's
`FAITHFULNESS-SUPPLEMENT.md`, SHA
`509d4c0e1ba5a796a9185e99a7782a9e1e3556e6eb0cf4ac6275918129d6d5da`,
and its accompanying independent core checker, SHA
`865380f56fd082b11a56aec49bb929b655f56a3de5a28aec4100896243a6f242`.
No mathematical correction is required. No new κ.

## Universal proof checks

1. The actual commuting group contains exactly the quadratic Z/4 phase
   functions stated in the proof. Basis directions supply linear coefficients;
   pair directions minus their two basis phases supply the even quadratic
   terms. Evaluation at basis and pair sums proves uniqueness. The Walsh-zero
   phase is always one, so no nontrivial scalar quotient is present.
2. For binary addition, the diagonal contribution to
   `f(x+z)-f(x)-f(z)` is `-2 a_i x_i z_i`, which equals the stated
   `2(a_i mod2)x_i z_i` modulo four. The off-diagonal terms are precisely the
   symmetric bilinear form. Thus the differencing identity has the correct
   sign and diagonal convention.
3. Summing the exact character identity gives
   `|S_f|²=2^d sum_{z∈ker B} i^{f(z)}`. For B nonzero its absolute value is at
   most `2^(2d-1)`. For B zero the phase is an ordinary character and its trace
   vanishes unless it is the identity. This proves the normalized bound
   `1/sqrt(2)` without sampling or approximate diagonalization.
4. For distinct actual group elements, their quotient is still a nonidentity
   actual group element. Tensor Hilbert--Schmidt inner products therefore have
   modulus at most `2^(-V/2)`. With
   `|P_d|=2^(d(d+3)/2)`, the claimed threshold `V≥d(d+3)` makes the Gram row sum
   at most `(|P_d|-1)/|P_d|<1`. Strict diagonal dominance of the Hermitian Gram
   matrix gives positive definiteness and linear independence.
5. The result concerns the linearly extended tensor representation of the
   group algebra, not the tensor power of a linear combination. It therefore
   applies to width-dependent scalar coefficients at every fixed width above
   threshold. It legitimately retains every abstract translation-character
   sector at those widths. It does not assert faithfulness in a width-one
   physical sector, nor that the sufficient threshold is minimal.

## Independent exact controls

The review checker does not import root's or the author's verifier. It builds
actual phase groups by breadth-first multiplication of the rank-one Walsh
phase generators, using two integer bit masks for each Z/4-valued phase.
It counts residues to compute exact Gaussian-integer traces, and checks the
rational Gram bounds for heads1 through4. The generated orders are
4,32,512,16384. At four heads, for example, the trace-squared histogram is
`{0:5265,16:7168,32:3360,64:560,128:30,256:1}`, and the sufficient width28
has Gram row bound16383/16384. The three-head histogram independently matches
root's512-element census exactly.

The negative control shows that substituting width16 into the same uniform
three-head estimate gives511/256>1; it does not mislabel failure of this
sufficient estimate as actual nonfaithfulness.

Reproduction:

    python check.py --proof /path/to/FAITHFULNESS-SUPPLEMENT.md --out RESULT.json

The universal conclusion comes from the checked written proof; the finite
controls are listed only at their actual scope. This is a concrete dependency
for the commuting and general-head one-relation obstructions, with no native
foundation, supplier, or multiplication-bound claim.

Credit @CubeJerry and the programme's retained tensor-Gram authors; root's
quadratic-phase proof and threshold, independently reviewed by Worker B with
OpenAI assistance.
