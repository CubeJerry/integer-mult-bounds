# The source outer reduction accepts a general uniform interchange envelope

Status: **source-transfer component proved; independent review pending**.
This independently reads the source outer reduction and replaces each use
of the fixed exponent by its actual interchange or selected-Walsh call.
It closes the outer black-box premise P-O of `TWO-SCALE-RECURSION.md`.
It does not certify the physical implementations supplying P-I and P-W.

## 1. Source pins and scope

OpenAI repository commit:
`3344da59991ed94f9ba711217b29c1d760badfa6`.

All three files below were read in full under
`preprints/The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026/build/`:

| File | SHA-256 |
| --- | --- |
| `permutations.tex` | `b906160eabe26a4cf4637d9388a465bab572ca66db80f968b4098b0520f31782` |
| `walsh.tex` | `4f28d915ef8f1b540d84037e00835078d12e30027380656db8a01532e90a6249` |
| `integers.tex` | `25d8f600ccc46e38825c4855d18b5084869f9c6cab313ff1b0b84e75c196bc44` |

The finite algebra, the prime-interval result, the normalized short-axis
Fourier factorization and the fixed short-word multiplier cited by the
source are imports. This note checks the claimed new dependence on the
interchange/selected-Walsh interfaces. It does not rerun those papers or
claim a new proof of their external theorems.

Put `N=2^k`, let numerical record width be between two fixed positive
multiples of k, and let V denote actual bit volume. All address fields on
which a permutation operates have complete ranges; arbitrary occupied
spectator fields and arbitrary positive leading row counts are allowed.

Suppose one fixed bit-permutation processor interchanges two width-u
fields in time `V I(u)+k^C` and visits at most `V S(k)+k^C` cells in
these outer applications, where I is a nondecreasing upper envelope with
`I(u)>=1` and C is an absolute fixed exponent. The harmless displayed
`k^C` term can instead be absorbed into the actual volume whenever the
relevant executor does so. E003 uses

```
I(u) <= sqrt(u+2) 2^(C Phi(log2(u+2))),
S(k) <= (1+log2(k+2))^C,
Phi(y)=y^(2/3)[log2(y+2)]^(1/3).
```

The same conclusions hold after replacing these functions by larger
monotone envelopes, which removes any issue about a small-width branch.

## 2. Packed XOR uses the envelope linearly

The proof of source `lem:packed-xor` does not use a special algebraic
property of `u^rho`. It uses a bounded number of interchanges of two
width-L chunks during each guarded pass. Every other operation is a scan,
a controlled cyclic rotation, or repair of a sparse exceptional set.

Choose `G=C_g ceil(log2(2k))` with one fixed sufficiently large integer
C_g. At a pass with a segment, `L>=G`, and a control prefix precedes
at least `2^L>=2^G` target records. That run pays for the fixed-degree
polynomial-k computation of its rotation amount. The eight-shift word
has a fixed number of chunk interchanges and scans. Thus one pass costs

```
O(V[1+I(L)]) + k^C.                                  (O1)
```

For s segment pairs, the exceptional fraction is at most `80s 2^-G`.
The source has `s=O(k)`. Each exceptional record receives a destination
key of O(k) bits, is processed in polynomial-k time, and participates
in O(k) stable binary radix passes. Fixing C_g after the degrees of
these explicit computations makes all exceptional work O(V). The
guarded word and the desired flips agree off the exceptional set;
both preserve the set, so the sparse repair is an exact permutation
even with arbitrary data in every auxiliary position.

There are O(log k) residue classes of guarded segments. The high bits
with insufficient guard, including the entire case `L<G`, use O(log k)
elementary two-bit moves. Consequently

```
packed-XOR time <= C V[1+I(L)](1+log k)+k^C.           (O2)
```

Only a fixed number of full streams is live. Tags add O(k) bits to
records already of width Theta(k), so they change the volume by an
absolute factor. Interchange scratch is reused between calls, and
the exceptional sort uses a fixed number of tagged streams. Its
visited-space bound is therefore `C V[1+S(k)]+k^C`.

For the Walsh application the control of each flip is one source bit.
Its degree does not grow with the local arity. Even overcounting the
polynomial-m number of calls or local control roles uses only one fixed
polynomial exponent in k, since m<=k in every nonbase outer call. Thus
the guard constant C_g is genuinely fixed.

## 3. Position and short-block permutations

Source `cor:bit-positions` factors an address-position permutation into
two involutions. Its three-chunk construction uses a bounded number of
packed XORs on widths at most k, plus a fixed number of individual bit
moves. Monotonicity of I and O2 give

```
position-permutation time <= C V[1+I(k)](1+log k)+k^C.  (O3)
```

The polynomial-k cycle/list preparation has an absolute degree and is
absorbed by the full `2^k`-record volume in the outer use. No constant
from a separate fixed-rho theorem is substituted here.

For source `lem:controlled-blocks`, retain fixed delta>0, target-block
width at most a fixed multiple of log k, and fixed-degree polynomial
table generation at each control setting. A guarded target batch uses
two applications of O3 and one guarded pass. O(log k) block batches,
each with O(log k) Benes stages, yield

```
controlled-block time <= C V[1+I(k)](1+log k)^3+k^C.   (O4)
```

The preceding visited-space argument still applies. The number of
iterations is a time factor; it does not create new disjoint scratch
regions. Marked streams are erased and reused after each return.

All constants in O1--O4 depend only on the fixed control/table degrees,
block-width constant and delta. They do not depend on a spectral label
parameter, the arity schedule or an inverse exponent epsilon.

## 4. The integer reduction has fixed outer parameters

In source `integers.tex` set

```
b=ceil(log2 n), h=ceil(n/b),
k=ceil(log2(4h)), N=2^k.
```

Then `Nk=Theta(n)` and `k=Theta(log n)` with absolute constants.
The source short-axis construction uses
`l=20 ceil(log2 k)`, trial division of candidates of size `k^O(1)`,
and a possible final power-of-two axis. Its axis count is
O(k/log k), each axis width is O(log k), and the padded box still
contains N records. The machine checks size/coprimality. The imported
prime-interval theorem implies success for every sufficiently large k;
its unspecified cutoff is not an algorithmic oracle.

The balanced CRT tree has O(log k) depths. At each depth its controls
occupy at most `k/2+O(log k)` bits; a fixed delta, for example 1/4,
therefore works eventually. Rotation tables have polynomial-k size
and fixed-degree generation. Equation O4 applies at every depth in
both directions, including invalid padded addresses, which the source
explicitly fixes. This costs

```
V[1+I(k)](1+log k)^C+k^C.                             (O5)
```

Source `lem:synchronized-short` builds O(log k) layers of block
permutations, unit-modulus diagonals and selected-bit Walsh transforms.
The block widths, eight occupied-fiber batches, at most seven axes per
block, and 64 amplification iterations are absolute choices. In
particular they do not grow when the Walsh/interchange schedule varies.
Every borrowed coordinate is restored in the ideal linear map, on
arbitrary data. Block permutations use O4. Walsh selections have at
most `c k/log(2+k)` bits for one fixed c.

Phase preparation uses fixed-degree polynomial-k computation at a
fixed multiple of k precision; its denominators remain bounded away
from zero in the source construction. Alternating prefix tapes emit
fewer than 2N phase products altogether. A streamed phase layer and
its application cost `O(Nk log k)+poly(k)`.

The short exact word products in that statement use the source's
previously known fixed multitape O(k log k) multiplier. They do not
recursively invoke the new integer routine being proved. Even its
O(k log k) time bound alone bounds its reused visited workspace by
poly(k), negligible beside Nk. No independent linear-space theorem
for that short-word multiplier is needed at this interface.

## 5. Uniform precision supplies the same exact full product

Assume the selected-Walsh supplier accepts arbitrary represented inputs
of norm at most `2^(13k)`, returns the same record layout with error at
most `2^(-50k)`, and uses at most `C_0 k` integer/fractional bits for
one absolute C_0. The nonstationary precision argument in the two-scale
note is exactly the supplier of this premise; admitting its physical
execution remains separate. Its explicit numerical guard
`k>=m_max^K_2` is tested before this format is chosen; time/space caps
alone are not a numerical accuracy test.

The completed exact Walsh layers are normalized unitaries. Therefore
all completed layers of each short-axis transform are unitary, just as
in the source. Local nonunitary intermediate gains within a Walsh call
do not multiply across the completed outer layer boundaries. With phase
errors `2^(-70k)`, O(log k) layers yield transform error below `2^(-40k)`
on the source norm range, using the same induction.

The two input digit vectors have norm at most `2^(4k)`. The source
coordinatewise-product estimate gives product-vector error below
`2^(-30k)` and norm below `2^(12k)`. Applying the adjoint, multiplying
by the prepared `sqrt(S)<=2^(k/2)`, and rounding gives Euclidean error
less than 1/2. Each true coefficient is integral, so every coordinate
rounds exactly. Inverse CRT and the O(k)-bit carry scan then emit the
full 2n-bit product in the required order. Thus the new overhead is
compatible with exact multiplication, not merely approximate output.

## 6. The resulting black-box transfer

Let J(k) bound the time per numerical bit volume of a complete selected
Walsh layer, including position permutations, and assume its visited
space is `V S(k)+Q(k)`. Let Q(k) also dominate all newly introduced
additive template preparation. If `Q(k)=2^(k^o(1))`, then for large k
it is smaller than N even after any fixed polynomial number of repeats.

The source construction, using O3--O5, consequently has

```
time <= C n [1+I(k)+J(k)](1+log k)^C+Q(k),
visited cells <= C n[1+S(k)]+Q(k),
k=Theta(log n).                                       (O6)
```

For E003, the two-scale recurrence gives

```
I(k), J(k) <= sqrt(k) 2^(C Phi(log2(k+2)))(1+log k)^C,
S(k)<=(1+log k)^C, Q(k)=2^(k^o(1)).
```

Substitution into O6 proves M1/G2 of the two-scale note. Its separately
proved sequential chunk wrapper then enforces one absolute O(n)
visited-space cap, increasing time only by a polynomial in log log n.
This note has no unresolved outer-dependent epsilon constant.

Exact guarded branches handle the bounded unsuccessful shape/precision
range. A marked-region cap can abort before leaving its prescribed
workspace, clear the marked intervals, and run the fixed
schoolbook fallback from the preserved inputs. The eventual inequalities
show that the cap is inactive at all sufficiently large lengths. The
wrapper also takes its explicit schoolbook branch when its prescribed
chunk count exceeds n.

Remaining hypotheses for a new complete E003 theorem are the actual
uniform P-I/P-W physical processors, their full-rate row shapes, their
visited-space schedules and the numerical gain/rounding premise used
above. The outer source reduction introduces no additional growing
template parameter or uniformity requirement beyond those interfaces.

Credits: @CubeJerry; the pinned OpenAI tape construction and its cited
prime-distribution, short-transform and short-multiplication predecessors;
E003 two-scale recursion; substantial ChatGPT multi-agent assistance.
No full multiplier execution, formal-kernel check or human review is
claimed.
