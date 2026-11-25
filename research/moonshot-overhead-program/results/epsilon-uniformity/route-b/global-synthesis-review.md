# Independent review of the global residual-exponent theorem

Reviewed on 2026-11-25 by Route B. **The synthesis passes within its stated
source-extraction scope.** No blocking quantifier, threshold, space,
inversion or circularity error was found. This is an independent audit of
the assembly from the complete Route A constructor/compiler profiles; it
does not replace Route C's separate source-by-source compiler audit or
claim a formal proof or execution of the complete multiplier.

## Snapshot actually reviewed

The following working-file bytes were compared with the blobs in checkpoint
`0961d2083f80429dde4b6ec5197585f727c7f87b`; all matched. Paths are relative
to `results/epsilon-uniformity/`.

| File | SHA-256 |
|---|---|
| `THEOREM.md` | `6e814bff4ae85f44cebd5a8fcab74a2c8383b47e0628b486de9add34a56e6097` |
| `PARAMETER-LEDGER.md` | `f7114811370ec69b18c7efd0294d0459671612418068d56826c6a536f7ffb671` |
| `route-a/elementary-tower-extraction.md` | `fa61e12164ced3f48483f289d5659ccd6c2051e18020538a48cf51f1d62e74bb` |
| `route-a/compiler-invoice.md` | `5ecd20dd366da0d62b1d3b399d07d67fb8e10a1c939a862c723c40eb2395657d` |
| `route-c/ELEMENTARY-TOWER-REVIEW.md` | `bacfed9e7bc8b21472e4feaddcf2e576a635f1ef64ca8e1cdd8be961b5924b5a` |
| `CERTIFICATE.md` | `7c40b59f17f9b1b616276e88c1782dfdb7749cce48afc72c843379138f84587b` |
| `route-b/linear-chunk-overhead.md` | `3002eef64179ee3682ad64ad5d92958a9a4c9dda95e7cf1687f34668b191fb61` |

The comparison also read S002's `routes/A/explicit-extraction-theorem.md`
directly from commit `96028cba1342c02bdca1f537ae9a80485087bdf3`; its SHA-256
is `ac170e6062950c14826e948582603d6d9e640edfbaf1f87c52b5c0a976bd790f`.
The common manuscript pin is OpenAI `math` at
`3344da59991ed94f9ba711217b29c1d760badfa6`.

## Audit findings

1. **Uniform constants and one actual machine.** Route A bounds a specified
   generator and fixed binary engine. Its finite-data budget includes total
   lengths, counts, address integer values and generation work, rather than
   merely asserting effective output. The finitely many time, space and
   threshold exponents can be replaced by one absolute maximum. Increasing
   that exponent weakens each estimate; it creates no self-referential
   requirement. The outer schedule uses one fixed pairing and common tapes.

2. **Thresholds and all-length safety.** The analytical bounds are not
   machine advice. Actual shape tests precede array materialization, numerical
   precision comes from the computed majorant, and failed preparation uses
   preserved inputs and schoolbook. The aggregate setup microstep clock,
   auxiliary marks, reused word scratch and geometrically parked stream
   volumes are needed for the all-length space claim. Finite generation may
   precede the inner setup clock, but its space is included in `c_j(u+1)`
   and is fenced by the outer attempt. The absolute prime-shape cutoff is
   separate from the parameter-dependent threshold.

3. **Common cap and complete bills.** For the least power of two
   `2c_j<r_j<=4c_j`, the integer condition
   `n>=max(4c_j,r_j U_j)` gives
   `c_j(ceil(n/r_j)+1)<n/2+2c_j<=n`. The row accumulator adds fixed
   `O(n)` regions. Its actual time is `r_j^2 t_j(ceil(n/r_j))+O(r_j n)`;
   candidate generation, code interpretation and cleanup remain inside
   `t_j`. Thus `A_j<=poly(S_j)` and the displayed threshold survive
   chunking. Aborted attempts also respect the same physical fences.

4. **Tower and integer inversion.** With
   `S_j<=E_3(C Z_j)` and `Z_j=(j+2)^3 log_2(j+3)`, the diagonal index
   `O((j+log S_j)^2)` and `log A_j=O(log S_j)` give
   `d_j,b_j<=E_2(C' Z_j)`. Fixed powers and the fixed prime cutoff are
   absorbed by one absolute enlargement of `C'`. The chosen
   `j=floor(c_0(y/log_2(y+2))^(1/3))` is positive eventually and at least
   half its unrounded value. For sufficiently small fixed `c_0`,
   `C' Z_j<=y/2` eventually. Therefore
   `d_j,b_j<=2^(sqrt(log_2(x+16)))<=sqrt(x)` eventually. This proves actual
   eligibility, as `b_j<=x` is exactly `N_j<=n`. The residual is the
   displayed `O(x(log(y+2)/y)^(1/3))`. This choice is analysis of a fixed
   search, with no free parameter-selection operation.

5. **Comparison and circularity.** S002's verified theorem uses
   `j^6`, yielding `O(x/y^(1/6))`. The new coefficient scale is strictly
   smaller because `(log(y+2)/y)^(1/3)/y^(-1/6)` tends to zero. This is
   a comparison of sufficient profiles, not actual runtimes. The short
   multiplier is the independently established `O(P log P)` algorithm;
   it is not the new multiplier recursively assumed at its target rate.
   Neither Route B's stronger conditional plan family nor Route C's
   variable-arity/radix hypotheses enters Theorem E. The source's original
   integral predictor remains in the odd-characteristic branch.

The theorem consequently has the claimed quantifier order: one fixed
machine, a common visited-space constant and an eventual time bound with
absolute constants, while every input length is computed correctly.
Its constants and crossover are not numerical. No broad verification suite
was rerun for this review; the work was a targeted proof and snapshot audit.

## Most consequential remaining mathematical obligation

Construct a substantially smaller **full-rate odd-characteristic predictor
representation** for the actual interchange query family. A concrete
structural target is to replace the source's monomial-tensor pencil of
dimension `b_0^H` by affine-query pencils of total dimension
`exp(m^{O(1)})`, with `O(sqrt(m log m))` stages, polynomially billed scalar
data in that dimension, and the same independent-input and small-error-row
contracts. For example, an identity `L_beta^b=P_beta I` with the smaller
dimension would suffice for the existing evaluation interface. The desired
identity must hold in the permitted odd-characteristic algebra on the
individual queries; count modulo `p` is insufficient.

This is an algebraic construction obligation, not the desired multiplication
bound restated. The count-aliasing and literal p-adic lift results eliminate
specific shortcuts but do not rule out these pencils. A successful result
would still require the physical routing and precision invoice. In
particular, the current conservative address-value bound also has height
three, and the retained binary branch has its own literal predictor cost;
both must be re-invoiced before claiming a lower global tower height. The
proved preflight selector alone changes the search expense without resolving
this representation expense.

Credits: the pinned OpenAI constructions and cited predecessors; @CubeJerry;
S002's independently reviewed extraction; Routes A and C for the complete
profiles and compiler audit. This review was prepared with GPT-6 Astra Pro
assistance.
