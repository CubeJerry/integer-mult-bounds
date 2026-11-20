# PR #7834 gives a reusable original-digit Gaussian recovery contract

Ali Romman's PR #7834, commit `4f0c67d5bb41d4af5501dcd40b3b388b35e0ff02`, executes two binary operands through source-prime CRT placement, generated Gaussian expansion pages, an opposite-sign transform on the same real coordinates, integer rounding, inverse CRT and ordinary carry. The checked outputs include the actual original convolution coefficients before carry. Its literal asymptotic outer invoice has power \(0.998268211\) on \(\log_2 n\), giving a pre-polylog saving \(0.001731789\). The target requires power at most \(0.995\). [Pinned upstream source](https://github.com/CrocSwap/integer-mult-bounds/tree/4f0c67d5bb41d4af5501dcd40b3b388b35e0ff02/research/fine-prime-gaussian-product)

## What the outer product can reuse

| Original multiplication obligation | Upstream evidence and transfer condition |
| --- | --- |
| Recover the original unsigned coefficient, with no cyclic alias | Use the genuine pairwise-coprime prime axes and the same source mask for both signs. Product of source axes \(S\) must satisfy \(2\lceil n/b\rceil-1\le S\). The normalized opposite transform returns convolution divided by \(S^2\). `crt_route.py` and `product.py` restore the original ordinal and carry a full \(2n\)-bit result. |
| Uniform precision on actual payload and holes | `ACCURACY.md` and `RECOVERY-RADII.md` bound both geometric operator error and absolute fixed-grid error, including all original and padded intermediate fields of every factor. An alternative C/H word needs the same action on every input, the indicated guard/headroom, indexed signs and scaling, and a proved digital loss on every admitted intermediate. |
| Real tape, backing and costs for the middle | `MIDDLE.md`, `ROUTING.md`, `BUTTERFLIES.md` and `DISJOINT-CNOT.md` account for actual grouped transformations, arbitrary spectator bytes and inverse restoration. The old conditional dyadic source and compact ordinary service are explicit premises. A cheaper local field operation or a partial native block does not establish those whole-operator contracts. |
| Unbounded outer geometry | `PROOF.md` ties its fine-prime regime, Gaussian page admission, full catalogue generation, acyclic short-word operations and tape price to cited source results. Finite outputs verify the concrete payload, chronology and normalization; the proposed \(0.005\) route still needs the faster compatible BIT and complex words, their uniform tariffs and existing outer/framework premises. |

Write \(h=2^{-q}\), \(K=2^\Gamma\) for the total scale loss of one whole transform, \(z=1/4\) for maximum original digit norm, and \(C=S^2 2^{2b+4}\). The published calculation applies when the true transform differs from its correctly signed, rescaled Fourier map by at most \(\eta\lVert x\rVert+e\), where \(\eta\) sums the certified geometric page defects and \(e\) bounds absolute digital loss. In the supplied word \(e=(64d+64)h\) over \(d\) source axes. Put

\[
D=K(\eta z+e),\qquad f=z+D,\qquad w=f^2+2K^2 h.
\]

The native controller checks its intermediate half-disk condition and uses the rounded-up pre-carry radius

\[
 C\bigl[D(f+z)+2K^2h+K\eta w+K^3e\bigr]<\tfrac12.
\]

The full original unscale is \(C K^3\), retaining two source-size normalizations and the loss from all three Gaussian transforms. The strict bound makes nearest-integer recovery unique before carry. For the growing retained configuration, \(q=8p\), \(p=6b\), \(S<2^b\) and \(\Gamma=O(d\log p)=o(p)\). The simple guard then has logarithm at most \(4b+3\Gamma+O(\log d)-48b\). This gives ample separation independently of the operand values, conditional on the quantified operator and digital bounds at that geometry.

## Price at the requested target

At the published axis power \(a=0.997\), both source-field permutations and grouped physical butterflies use the exponent \(1-a\cdot0.001737=0.998268211\). The dense per-axis term already has power \(a\). For a common valid saving \(\delta\) on both primitive interfaces, the two terms \(a,1-a\delta\) yield at best saving \(\delta/(1+\delta)\). Strictly exceeding \(1/200\) therefore requires \(\delta>1/199\). A hypothetical direct compatible \(0.0050000002\) service on both sides gives only \(0.0049751245761\ldots\) on this comparison. This is an admission limit of the stated accounting.

The original ordinary wrapper in `ORDINARY.md` first turns a covered source saving \(c\) into \(c(1-c)\). Even granting its interface the programme's strict raw fixed-tariff ceiling \(c<0.00504325518581\), monotonicity gives \(\delta<0.005017820762940801\) and \(\delta/(1+\delta)<0.00499276794827\). This last test generously grants the matching complex service the same price. A direct, sharper ordinary service avoids this particular first contraction only after matching the physical domain, arbitrary spectators, chronology and price. The lemma and finite executions give no new complete multiplication exponent.

## Original-coordinate controls

The verifier authenticates every blob in the 53-file upstream tree. It independently computes every raw convolution coefficient by base-digit schoolbook multiplication, carries them back to the fixed-length original result, recomputes the controller's two possible radius branches in exact rational arithmetic, and checks the actual residual against its all-input radius. The primary geometry \((5,7)\to(8,8)\), \(b=8,q=128\), returns 345550037539 for 741503 times 466013, with first five original coefficients 11811, 10996, 4152, 868, 77. Padding those operands to 145 bits selects \((31,29)\to(32,32)\), \(b=4,q=96\). It recovers all 899 original coefficients, with two strict Gaussian interior coordinates, a uniform radius below 0.000247 and no live transform holders after output. The public finite fixtures take the small primitive branch; they do not execute the eventual full production GL64 payload.

The replay deliberately removes one final binary normalization bit. It also deliberately exchanges original digit positions zero and one at the inverse-CRT output, after the geometric radius check and before the true carry scan. A third control uses individually admissible Gaussian page defects that fail the joint three-transform rounding test. Exact outcomes and all source hashes are in `output/RESULT.json`.

    python -B PATH/author/check.py --canonical CANONICAL_CHECKOUT --out FRESH --with-interior

The canonical checkout must contain the pinned PR head. Python 3.12 and Git suffice. `--source` optionally reuses its extracted package, subject to the exact Git blob verification. Credit Ali Romman and the upstream authors identified in `SOURCES.md`. Substantial OpenAI assistance.
