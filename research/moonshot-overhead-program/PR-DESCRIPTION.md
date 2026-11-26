# Explicit overhead for exact integer multiplication on fixed tapes

## Result

One deterministic finite-alphabet multitape machine computes the full $2n$-bit product for every input length in
$$
 O\!\left(n\sqrt L\,2^{O((x^2\log_2(x+2))^{1/3})}\right)
 \quad\text{steps and } O(n)\text{ cells ever visited},
 \qquad L=1+\log_2 n,\quad x=\log_2 L.
$$
This is the programme's retained unconditional written result. The published tape theorem gives a vanishing logarithmic excess. The contribution exposes an explicit rate, parameters and tape costs in one [direct-space proof](contributions/explicit-overhead/README.md). E002 and E003 give independent same-order constructions. The exact square-root upper bound, polynomial overhead in $x$, and literature priority remain open.

## Changes available for review

- The [elementary sieve](contributions/explicit-overhead/coprime-axes.md) certifies the released descending gcd search at its original widths. The [interchange schedule](contributions/explicit-overhead/AQ-P.md) prices full-volume returns and the union of tape cells visited. Fixed Toom-3 covers the outer full-word products.
- The [modular Walsh executor](contributions/explicit-overhead/modular-walsh.md) carries out each rational row operation on bounded words and rounds at the boundary. Its short scalar has [fixed-head code](contributions/explicit-overhead/modular-scalar-machine.mjs). The [Lean proof](contributions/explicit-overhead/formal/ModularWalshExact.lean) recovers exact signed sums of the published target under its integer magnitude bound.
- The [binary CRT experiment](sessions/2026-11-26-S006/stable-four-point-bundles.md) classifies whole-block supports, supplies a reversible trace layout at every $3\mid b$, and reaches the $O(2^b\sqrt b)$ clock for $\Theta(\sqrt b/\log^2 b)$ consecutive layers on its declared endpoints. Rounding the caller's degree costs at most two bits. Lean verifies additive interpolation and the [two-way transport of conjugate remainders](contributions/explicit-overhead/formal/BundleTransport.lean), including nonzero representative shifts. A [second reversible prefix](sessions/2026-11-26-S006/stable-four-point-bundles.md#the-contiguous-binary-coefficient-input) begins at the actual binary coefficient stream, with kernel-checked quotient and remainder. Grouped remainders have an independent encoding of exactly $2^b$ bits. Full conversion between these partial transforms, literal per-factor operations and the precision carries remain open.

## Verification

Independent AI reviewers reconstructed the binding algebra and physical resource counts. Eight modules and 56 designated axiom checks cover the source Walsh target, transform identities and actual grouped quotient and remainder. The contribution includes exact finite replays, negative controls, source hashes and [Lean receipts](sessions/2026-11-26-S006/lean-axioms.txt). The complete machine has written proof and awaits human review. [Verification scope](contributions/explicit-overhead/verification.md) · [Earlier programme history](https://github.com/CubeJerry/integer-mult-bounds/blob/69632d87c99b5a75d0b44a7d964e6550e457e016/research/moonshot-overhead-program/PR-DESCRIPTION.md)

## Credits

Jerry Chen (@CubeJerry) directed the programme with substantial ChatGPT research and multi-agent assistance. OpenAI's source authors supplied the 2026 tape and Fourier constructions. S002/E001, E002, S003/E003, S004 and S005 supplied the preceding credited proofs, conditional transfers and negative results. The cited authors retain credit for combinatorial sieves, fast integer multiplication, Toom–Cook interpolation, Frobenius partitions, additive Fourier transforms and normal-basis theory.
