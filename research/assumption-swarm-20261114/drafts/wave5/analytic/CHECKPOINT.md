# Wave 5: complete symmetry class and orbit-certificate scale

Base: `e54523517d0f03e58352e647c403a5af3e525a57`.
Exact orbit predecessor: `8f1a09fb4f696bd5f20e1953210936308571416e`.
Assigned by the orchestrator after the independent direct-switch review.
Tracks40--49/60--74. All prior packages remain frozen.

## Scope and proposed result

For the homogeneous exact Gaussian tensor on `[0,n-1]^d`, `n>=2`,
`0<q<1`, `v>0`, classify every simultaneous vertex permutation preserving
`H_xy=q^(||x-y||^2) v^(sum(x-y))`. The proposed group is coordinate
permutations for `v!=1`, and signed coordinate permutations for `v=1`.
Use this to bound the minimum *number of cycles* of one exact symmetry,
and hence the best scale of the specified orbit-boundary certificate.
No displacement-rank lower bound or algorithmic lower bound is sought.

Feasible proof: H_xy H_yx preserves squared distance; grid isometries
extend affinely from0 and `(n-1)e_i`; cube symmetries are signed coordinate
permutations. Nonzero log(v) additionally preserves coordinate sums and
forbids reversal. Symmetry orders are at most g(d) or2g(d), respectively.
Landau prime-power coordinate blocks give a matching upper orbit bound
within an absolute constant: each block correction is at most its prime
case, yielding `(3/2) exp(8/9)<4` overall.

## Verification plan and stopping rule

Prove every step symbolically. Independently compare direct finite orbits,
Burnside averages and cycle-type formulas; compare integer-partition maximum
orders with a separate distinct-prime-power dynamic program. Include finite
`d=5,n=2` control: cycles2+3 have order6 but12 orbits, whereas a5-cycle
has order5 but8 orbits. Include nonsymmetry, missing-shift, repeated-prime,
and the special4-cycle correction cases. Check only bounded finite domains;
Landau's asymptotic is an explicitly credited classical theorem.

Stop after a reviewed exact theorem, finite controls and the priced dense
materialization boundary. Do not optimize finite cycle counts, generalize to
nonuniform source factors without a proof, or claim the result applies to
arbitrary coordinate orderings, implicit generators or multiplication.

Status: proof outline derived independently; primary Deléglise--Nicolas--
Zimmermann source opened and its equations(2),(6) checked. Exact predecessor
source pins, executable checks and final package remain in progress.
