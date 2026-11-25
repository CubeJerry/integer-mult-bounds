# Independent review of the cross-pinned rectangle partition

Reviewer: E002 conditional review C. Gate: **PASS for the constructive partition, source algebraic compatibility and exact counts**.

Reviewed complete Route A note, SHA-256
`08fcb6b9e2ceb0479e6a3d67eb7231b64ea9206cd1d1b9193bc071df3dbf8371`.
I also read its complete checker and the pinned tape `interchange.tex` endpoint and rectangle-delivery proof. This review does not supply a new compact tape generator/layout compiler.

For each ordered inner pair at distance d, its unequal set S and outside letters are determined. The source letter at the first selected coordinate uniquely fixes a, and the destination letter at the second uniquely fixes b. The other d-2 coordinates have unique first-differing-bit parts. These choices put the pair in exactly one proposed rectangle. Every cross pair in that rectangle disagrees at all selected coordinates. Thus coverage is exact and disjoint, including d=2 where the list of remaining bit partitions is empty.

The pin positions on opposite sides need not coincide. Within the source side the first coordinate is fixed, and within the destination side the second is fixed. Each side therefore varies in at most d-1 positions and has no far pair. The source endpoint lemma requires only the resulting within-side and cross-side Gram values; it does not require a shared pinned coordinate. At the outer level this gives k=0 within either side and k=d across, exactly as needed for its oriented Gram blocks. The scalar P* and its rank factorization remain unchanged.

For a fixed source word the source pin and outside letters are forced. The destination pin has q-1 possibilities; each other selected coordinate has exactly t containing bit rectangles. This gives `alpha_new=binom(h,d)(q-1)t^(d-2)` on both sides. Enumerating all actual choices instead gives

`R_in,new=binom(h,d) q^(h-d) q^2 [2(q-1)]^(d-2)`.

Since h=2d-1, this is CP2. Dividing by the old count yields `q/[2(q-1)^2]`, while dividing the incidences yields 1/t. The two ratios are indeed different. The average-side-size formula follows from total incidence q^h alpha_new and is correct.

The outer product independently chooses d varying positions. Consequently `lambda_new=binom(h,d) alpha_new^d`, proving CP5 and its exact saving t^d. Its normalized output count is

`binom(h,d)(R_in,new/q^h)^d`

and the powers of q simplify to CP6. In particular at d=2 it is exactly 27 for every dyadic q. There is no surviving positive q power in that expression.

The distinction between counts and a delivery algorithm is preserved. The new family is genuinely different from the canonical old partition, so the old exact-incidence theorem does not prohibit the improvement. However the remaining `d(d-2) log t + d log(q-1) + O(d^2)` incidence logarithm has the same leading optimized order for unbounded d. The rational dimension cost also remains present. Neither log-free two-thirds multiplication nor the rectangle-volume physical hypotheses follow.

## Independent replay

I copied the exact note and checker into `e002-review-c/replay-cross-pinned/` and ran the checker there. The replay compares generated rectangles with independently enumerated distance-d ordered pairs and tests actual within-side distances. It also verifies regular incidence and the outer formulas, with omission, unpinning and obsolete-count controls. Its timestamped receipt records the checker and note hashes; `execution.log` contains the full result.

These finite checks support the concrete partition. The universal statement rests on the unique-parameter and pin arguments above. No full tape execution, physical runtime lower bound, formal proof or literature-priority claim is made.

Credits: @CubeJerry; the pinned source; Route A's cross-pinned construction; E002 exact-count work; substantial ChatGPT multi-agent assistance.
