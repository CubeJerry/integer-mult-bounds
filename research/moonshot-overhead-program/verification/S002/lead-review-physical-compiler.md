# Independent lead audit: polynomial dependence of the physical compiler

Status: **physical ledger accepted within its explicit source-template
contract**, pending the separate bounded-generator and complete-rate reviews.
This is an AI-assisted source/proof audit, not a formal build or execution of
the enormous generated multiplier.

Read the complete November tape `interchange.tex`, `permutations.tex`,
`walsh.tex`, `integers.tex`, and `uniformity.tex`, plus September tape
`sections/02-streams.tex`, at the recorded source pin. The old fixed-j O
notation was not used as a substitute for a quantitative bound.

## Reviewed interface

The finite P in `routes/A/physical-compiler-ledger.md` bounds expanded lists,
roles, dimensions, counts, binary description lengths, numerical coefficient
bit heights, and numeric rational-address/radix magnitudes. Exact local
contraction margins are at least one half. Under these conditions the
source processors can be implemented with a common fixed number of tapes,
time P^{O(1)} u L(u)^rho (1+log L(u))^4, and space P^{O(1)}u+d,
above a threshold max(U_absolute,2^{P^{O(1)}}).

## Main checks

- **Address operations.** An integer scaling has at most its numeric
  magnitude many monotone pieces, with the inverse implemented by reversed
  split/merge. Rational scaling is a composition of numerator and inverse
  denominator scalings. P bounds those magnitudes. Controlled translations
  use polynomial-time arithmetic on f-digit values, paid by the complete
  b^f target fiber. Unrelated spectator counters are advanced amortized;
  reading an entire long prefix once per bit would be invalid and is not
  used. Multi-control linear maps may be decomposed into polynomially many
  one-control elementary operations, keeping their formal field count
  absolute.
- **Finite algebra.** Store its coordinates in binary blocks and implement
  prescribed scalar multiplication by its expanded linear map. This gives
  polynomial-P work, rather than an exponential truth table in all possible
  algebra letters. The same fixed encoding is used at every recursion depth.
- **Serialization.** Extract one role/class at a time and park other tracks
  on end-access stacks. The source explicitly preserves each child's
  original volume, so the interpreter overhead belongs to nonrecursive
  work and does not multiply the recurrence coefficient at every level.
  The finite instruction-list scan adds only a polynomial-P factor.
- **Interchange stack.** Main-call volumes contract by at most 2/W, W>=3;
  reserve calls retain full volume but park only descriptors after main
  work is merged. This distinction is needed for the uniform space bound.
  Binary-to-prime-radix padding costs less than b^2, included in P^2.
- **Guards and sorting.** Offset/rank computation has a fixed polynomial
  degree in k. A guard coefficient containing O(log P) pays its P factor.
  Sparse exceptions still cost O(V) after tagged stable radix sorting.
  The extra guard passes and short-field cases cost polynomial P times
  the same logarithmic factors. Controlled block permutations add two
  logarithmic factors; CRT tree depth adds one more.
- **Short tables.** Each block has at most seven axes of width at most
  20 ceil(log2 k), hence at most 2^140 k^140 positions. Explicit list
  construction, pair-routing permutations, Beneš switches, trial division,
  bounded-argument trigonometric series and bisection all have fixed
  polynomial degree. The conservative degree 1000 covers these loops.
  This is a concrete algorithmic bound, not an arbitrary poly_P(k) call.
- **Fast scalar products.** Per-record products use the same fixed
  O(k log k) short-integer multiplier as the source. Schoolbook k^2 at
  every record would invalidate the claimed budget. Slow school arithmetic
  is confined to polynomial-size setup where exponential record volume
  absorbs it.
- **Precision.** At most P row updates of coefficients of height <=P give
  log one-level gain O(P^2). The path/common-ancestor argument and the
  count <=4P(1+k)^(log2 P) yield explicit fault majorants. A polynomial-P
  lower threshold on k makes these costs fit one absolute multiple of k
  precision bits and absorbs setup into 2^k. Walsh row padding also fits
  this threshold; its total volume is then at most twice the unpadded one.
- **Exact recovery.** The source's unitary layer boundaries, norm caps,
  two forward transforms, coordinatewise product, inverse transform and
  final sqrt(S) scaling give Euclidean error below 1/2. Carry recovery and
  all copies/rewinds are linear in record volume. These steps introduce
  no new parameter-dependent exponent.

## Caveats that must survive assembly

P is a numerical envelope for the actual local data, not just the bit length
of a succinct arbitrary program. Its bounded generation cost is a separate
obligation. All coefficients required to be units after radix specialization
must be in the tested numerator/denominator list. The source prime-gap
cutoff is an absolute eventual cutoff; this review does not claim a numeric
value for it. Shape tests and correct fallback make the machine effective
without knowing that cutoff. The final asymptotic formula may use an
unspecified absolute threshold, but must not advertise a computed practical
cutoff. No whole-machine rate is admitted by this review alone.
