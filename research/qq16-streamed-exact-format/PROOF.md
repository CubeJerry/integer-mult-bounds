# Exact finite arithmetic at the streamed QQ16 boundary

@CubeJerry, with substantial OpenAI Codex assistance. Apache-2.0.
This is a written, source-bound numerical argument and a metered reference
lowering, not a formal proof of a physical supplier or the multiplication theorem.

## 1. Frozen object and entrance

The object is the **hosted** 3,813-event word of Chris R / Clear1nsight's PR4015,
head `0fff81d8997cef646538bcd4f60d7d455cf93b8e`. `RETAINED.json` binds its exact
word, proof, README and native recipe; the latter is read as evidence, never
executed. Its parent construction is ywz65's PR2707 and Arham Tahir's PR2681.
PR3985 supplies the rectangular correction. PR4043 supplies a separate relative
rounded-trace equivalence, not the absolute finite format proved here.

Retain the predecessor semantics: 224 current X/Y arrays are borrowed, with X
in F17 and Y_p in F17 C_qp^-1; 224 Z/W arrays are exclusively owned outputs;
up to 16 F/G arrays are private to an owner sweep. Nine deferred Z_U outputs
host the streamed query. A cover map permutes entries over the **whole cover**,
including owners; it is not assumed to act within one owner. Each signed native
line is, up to the inherited monomial wrappers, a Gaussian pair kernel on each
of lambda disjoint tensor layers. The 64 spectator axes are included in the
array length D, not silently removed from its cost. Those source semantics,
actual frame legality, and the promised output inverse identity are inherited.

Let lambda >= 1, k = ceil(lambda/2), t = k-1 and u = 2^t. Let h be a positive
power of two and P >= 0 an integer. Every borrowed **physical real/imaginary
component**, in its own stated frame, must be in h Z and have absolute value
less than 2^P h. This is a common input contract; no claim that arbitrary
producer outputs already satisfy it is made. Owned dirt can be any representable
signed value and is overwritten by CLEAR before any arithmetic read.

The sufficient common format is

```
q = h * 2^(-(3*k + 6)),             W = P + 6*k + 22 signed bits.
```

The signed-integer interval is [-2^(W-1), 2^(W-1)-1]. The theorem concerns
exact representable inputs in that contract. It supplies **zero additional
decoder rounding error**. Errors already present in the borrowed inputs are
not erased and are not bounded here.

## 2. Inherited Gaussian parity, with an interior bound

For s in {-1,1}, the pair kernel is

```
C_s(a,b) = (((1+s*i)*a + (1-s*i)*b)/2,
            ((1-s*i)*a + (1+s*i)*b)/2).
```

A coefficient of its j-layer tensor row, indexed by a subset of size ell, is
`(1+s*i)^(j-ell) (1-s*i)^ell / 2^j`. Since `(1+i)^2=2i`, for even j every
nonzero coefficient is a Gaussian unit times 2^(-j/2). For odd j its real and
imaginary parts are each +/-2^(-(j+1)/2). Consequently:

* The exact real-component row sum is 2^ceil(j/2).
* An input grid g becomes a grid no finer than g*2^-ceil(j/2).
* A delta input witnesses the full denominator, so this **local kernel** grid
  statement is sharp. It does not prove the full decoder format is minimal.

These tensor/parity facts are prior work, notably Alejandro Zarzuelo Urdiales's
PR45 (`research/gaussian-parity-synthesis/`, including a stronger Lean execution
development). Their discovery and formal verification are not claimed here.
`independent.py` rederives the coefficients by integer Gaussian products and
binomial multiplicities for the explicitly listed test depths; no Lean is run.

For a sequential pair implementation, first form the four real sums/differences,
then their four crossed numerators, then halve. If all input components to the
complete native call are bounded by L, each such numerator after j-1 layers is
at most `4*2^ceil((j-1)/2)*L <= 4*2^k*L`. Its grid is no finer than the completed
native grid. In particular, at **even** lambda the penultimate layer already
has the final denominator; dropping one bit from the interior grid is unsound.
This is why the receipt retains the same grid for its interior envelope and
completed call, despite the interior's extra magnitude factor four.

## 3. Two-axis lowering and scalar restoration

Pairing two layers eliminates an unnecessary intermediate normalization. In
address order (00,01,10,11), write the complex inputs as (a,b,c,d). For s=+1,

```
C_+ tensor C_+(a,b,c,d)
  = (i*a+b+c-i*d, a+i*b-i*c+d,
     a-i*b+i*c+d, -i*a+b+c+i*d) / 2.
```

The implemented eight real partials are

```
u=br+cr, v=di-ai, w=bi+ci, x=ar-dr,
p=ar+dr, q=ci-bi, r=ai+di, z=br-cr.
```

The outputs are `(u+v,w+x)/2`, `(p+q,r+z)/2`,
`(p-q,r-z)/2`, `(u-v,w-x)/2`.
All eight partials are formed before overwriting any input. One ninth scratch
register holds each numerator and feeds a direct output-component HALVE.
No phase multiply, source COPY, or extra full array is needed in this scalar
register model. The negative kernel exchanges output addresses 00/11 and 01/10,
since `C_- = XOR(1) C_+`; it is implemented by the stated destinations, not
by dropping the inherited signed native wrappers from the complete invoice.

`paired_kernel.py` executes this in place, checks every arithmetic intermediate,
and meters 16 real ADD/subtract instructions, eight exact HALVEs, 16 real
array-operand reads and eight real array-component writes per four-entry block.
An unpaired layer uses eight ADDs and four HALVEs per pair. Instructions operate
on scalar registers: each ADD reads two operands and writes one result; HALVE
reads one operand and writes one result. The array traffic above identifies
the subset crossing the array/scratch boundary, not all scratch traffic.
Python tuple allocations implement this abstract register state and are **not**
a measured low-level storage implementation or runtime benchmark.

Each pair of layers has component growth at most two and loses at most one
binary grid bit. Its partials and numerators have magnitude at most 2L and 4L.
Applying these blocks and an optional unpaired layer therefore preserves the
section-2 complete and interior envelopes. All HALVEs are exact on the promised
common grid. Directions have disjoint bit supports, so their four-address
orbits partition the array; no commutation with a cover map is used.

The scratch is **dirty owned**, overwritten before use, then cleared to zero
once per native call. There are nine real scratch words when lambda>=2, five
when lambda=1. The sequential comparator needs five. The extra four clears per
call are charged below; no borrowed scalar or array is erased. This local
lowering does not eliminate an actual recursively invoked supplier boundary.

## 4. Whole-word induction and exact certificate

The verifier associates each field with a polynomial p(u) with nonnegative
rational coefficients and a maximum of affine grid exponents c+a*t. Its meaning
is that every real component is bounded by `2^P*h*p(u)` and lies on the
corresponding dyadic grid. Initially p=1 and grid=0. The rules are:

| Event | Magnitude envelope | Grid loss |
|---|---|---|
| CLEAR | 0 | none |
| unit signed ADD | p_dest + p_src | maximum of the two grids |
| quarter signed ADD | p_dest + p_src/4 | source grid + 2, then maximum |
| cover/monomial map | unchanged | unchanged |
| complete native | 2u*p | grid + 1 + t |
| native interior | 8u*p | same conservative grid as complete native |

The interior row bounds every sum/difference and crossed numerator, not only
the final halved outputs. ADD's quarter product is bounded by the resulting
nonnegative triangle envelope; its grid is included before addition. These
facts prove closure by induction over the **literal ordered** word. Arithmetic
does not reassociate query additions, remove noncommuting maps, or infer an
interior bound from endpoint equality alone.

`verify.py` checks initialization and ownership, regenerates every polynomial
and grid, then compares **every typed field** of RESULT.json and all TRACE.json
rows. The 4,032 streamed observations comprise 3,808 value-writing events and
224 native interior envelopes. The original PR2707 comparator has 4,152 rows.

For the streamed word every polynomial has degree <=3 and coefficient sum
<=171043. Its largest coefficient-sum witness is zero-based event 3797,
`W0 += -Z0`, with polynomial

```
445 + 28230*u + 96*u^2 + 142272*u^3.
```

Since u>=1, all magnitudes are at most
`2^P*h*171043*u^3 < 2^(P+18+3t)*h`.
The global grid frontier is `[9,3]`, i.e. exponent `9+3t=3k+6`.
In units of q, every arithmetic value therefore has absolute value strictly
less than `2^(P+27+6t)`. The stated `W=P+28+6t=P+6k+22` accommodates it,
including a sign bit. Owned initial dirt is discarded directly, so even the
most negative representable dirt is never negated or normalized.

The original 336-native-call word, evaluated by the **same** method, has
coefficient-sum bound 255115 and the same degree-three/global-grid envelope.
This is a controlled comparison, not a claim that either global bound is sharp
or that it supersedes PR2807's different rounded-format model.

## 5. Complete conditional cost recurrence

The frozen streamed word retains **224 native calls, 448 monomial wrappers,
352 cover maps, 1920 unit complex ADDs, 896 quarter complex ADDs and 416 array
CLEARs**. All nine hosted outputs and all 16 private arrays retain their original
source obligations. Its inherited scalar allowance is 26944, in the source's
tariff, unchanged by this numerical certificate.

Let N owners each have L complex coordinates and put D=N*L, the complete
full-cover bank length. Let A_W, H_W, Q_W and Z_W be the costs of
a signed W-bit real ADD/subtraction, exact division by two, exact division by
four, and zero write, **including their scalar operand reads and result write**.
Let s_lambda=5 at lambda=1 and 9 otherwise. Lowering all natives as above gives

```
T_dec <= D*((896*k+5632)*A_W + 448*k*H_W + 1792*Q_W)
         + (2624*D + 224*s_lambda)*Z_W
         + 448*M(D,W) + 352*C_cover(D,W)
         + E_input + E_output + E_address + E_lease + E_control.
```

The unit and quarter ADDs account for 5632 real additions per coordinate.
Quarter divisions use one scratch word, explicitly returned zero after each
real component, costing 1792D clears. This deliberately simple protocol works
also inside the owner-private sweeps without retaining a scalar across owners.
The other 832D zero writes initialize/return owned array storage. Native scratch
is reused across all owners within a call, then cleared; this contributes
224*s_lambda. No recursive child is omitted: this is the
**direct** implementation of all 224 calls. Equivalently, before lowering,
the recurrence contains `224*T_native +448*M+352*C_cover+1920*T_unit+
896*T_quarter+416*T_clear` and the same entrance/control/lease terms. Substituting
a cheap recursive supplier for the direct native bill requires a separate
proved interface and is not licensed by this result.

For the stated direct scalar protocol the array-only reads are
`D*(896*k+11264)` and array-only writes `D*(448*k+6464)`, excluding wrapper/map
traffic. These accesses are included in the scalar primitives above, not an
extra additive charge. M and C_cover must include their **whole-cover** source
access, scratch, restoration and placement costs. E_input includes bringing
borrowed inputs onto q without modifying their entry representation; E_output
includes the caller's required format/frame return. E_address, E_lease and
E_control include address generation, source selection, loop/control state,
ownership and bank/temporary allocation. These physical terms are **unpriced,
not zero**. Peak arithmetic storage is the inherited 224 full-cover owned arrays
(224D complex entries), 16 owner-private arrays (16L complex entries), and at
most nine real scalar scratch words, before any extra
storage needed to implement those unpriced transports or the caller.

The sequential direct comparator replaces k by lambda and s_lambda by 5.
Thus the arithmetic saving in unit-cost ADD/HALVE/CLEAR instructions is
`1344*D*floor(lambda/2)-896` for lambda>=2, and zero at lambda=1, with the same
input and format. It is positive for every admissible D>=2^lambda. Array
reads/writes also halve on each paired axis block. Address/control/transport
costs may dominate; **no physical speedup or new kappa follows**. This finite
comparison is not a benchmark of the selected multiplication implementation.

## 6. Evidence and unresolved implications

The independent checker imports no primary or predecessor executable. It
derives Gaussian coefficients directly and checks 65,472 complete cut bounds
at lambda=1,2,3,4,7,8,15,16. This is independent implementation structure, not
independent human review or a proof by sampling over all depths.

The integer execution checks 1,250 small signed pair cases and 13,122 small
signed two-axis cases against complex-rational multiplication. Six complete
word fixtures use two toy owners, two local axes, depths 1/2/3, and seeds
`53+10*depth+offset`, offset in {0,1}. Every native occurrence compares paired,
sequential and rational execution; all 22,848 value-writing cuts, 102,144
individual pair calls, borrowed inputs, private zero returns and primitive
invoices are checked. These are **synthetic noncommuting cover permutations**,
not an independent replay of the actual 73-axis source geometry. The actual
operator/frame proof remains the pinned source's obligation.

Controls cover inadequate grids, numerator overflow despite fitting final
outputs, an observable wrong sign, quarter indivisibility, missing first/last
clears, a borrowed write, forbidden coefficient, incorrect tensor supports,
and omitted extra scalar cleanup. Export tests rerun normal and optimized
Python without Git, with read-only file modes and unchanged-byte checks;
source/manifest/receipt/trace mutations must fail. No tests rely on assertions.

Still open: bind one real producer's physical input range and grid, implement
actual full-cover memory movement and a caller lease for all owned output
banks, price native recursion and every format/ownership return, then evaluate
both supplier caps and assembly conditions. PR3303's producer-interior proof
and PR4043's relative trace result can inform this work but do not imply those
admissions. No selected-frontier file is changed. **No new kappa.**
