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
- The [Complete ordered binary CRT](sessions/2026-11-26-S007/binary-transform-and-product.md) accepts all $2^b$ independent coefficient or factor bits in both directions and charges the full degree/Lyndon order.
- The [First carry](sessions/2026-11-26-S007/first-witt-carry.md) computes the actual first high remainder digit for the literal integer factors. The [fixed-precision extension](sessions/2026-11-26-S007/fixed-witt-precision.md) handles arbitrary independent residues over each fixed coefficient ring. Its costs at growing precision remain open.

## Verification

Component Lean modules were rebuilt with the pinned compiler and replayed in the kernel. Independent AI reviews reconstructed routing, arithmetic and the caller interfaces. Direct finite polynomial division, independent inverse inputs, and signed division modulo four check the numerical implementations. The resource bounds are written proofs awaiting human review. [Session verification](sessions/2026-11-26-S007/VERIFICATION.md) · [Session report](sessions/2026-11-26-S007/FINAL-REPORT.md)

## Credits

Jerry Chen (@CubeJerry) directed the programme with substantial ChatGPT research and multi-agent assistance. OpenAI's source authors supplied the 2026 tape and Fourier constructions. S002/E001, E002, S003/E003, S004 and S005 supplied the preceding credited proofs, conditional transfers and negative results. The cited authors retain credit for combinatorial sieves, fast integer multiplication, Toom–Cook interpolation, Frobenius partitions, additive Fourier transforms and normal-basis theory. Cantor and Kaltofen supplied the cyclotomic decomposition, Yann Tal the fixed-tape sorting theorem, Harvey and van der Hoeven the short products, and Swapnil Jain the verified finite residue word.
