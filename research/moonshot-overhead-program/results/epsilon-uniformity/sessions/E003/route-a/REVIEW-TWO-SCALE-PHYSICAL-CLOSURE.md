# Independent audit of the two-scale physical transfer

Reviewer: E003 Route A. Result: **pass for the analytic implication and
for the source-specific P-I/P-W composition, with the explicit fixed-array
Walsh supplier recorded below**. This is a written mathematical and
machine-model review with finite supporting replays. It is not a full
multiplier execution, a formal-kernel verification, or human refereeing.

The reviewed Route B note initially left P-I and P-W as admission gates.
The main additional obligation found in this audit was real: importing
E002's `m^C V` Walsh-space estimate would not imply the required
`V poly(log k)` estimate at `m=2^(Theta(Phi(log a)))`. The separate
`RATIONAL-WALSH-CONSTANT-SPACE.md` supplies the needed fixed-array
schedule. That component is authored by this reviewer and must receive
its own independent review; this document does not certify its own
authorship as independent evidence.

Remote E002 has independently reached the same 2/3 logarithmic scale
during this session. This review makes no priority or new-programme-best
claim. It checks this E003 proof chain and its specific storage mechanisms.

## 1. Exact reviewed objects and reading scope

The principal reviewed object is Route B's `TWO-SCALE-RECURSION.md`,
SHA-256

```
d3dbaec51328645cc2431f7dcccbb654bf62f2fd20e91cea17ab9d04658e5cdc
```

It includes the all-arity construction, the binary versus field-row
distinction, finite-repair field scope, the full intermediate-gain
condition, and the explicit numerical eligibility guard. The accompanying
`physical-closure-review-manifest.json` records exact hashes of the
component files and primary source bytes read. A later text change is not
silently covered by the principal hash; a delta review may extend it.
The initial complete review used
`ad7df694ff57da4ce40a3593451517b2293c47b5cabe90c4bf23ad2470c951d7`.
The reviewed delta to the displayed hash adds remote attribution, the
opaque exact-bit/numerical-boundary distinction, and an explicit restriction
of the `2^(k^o(1))` setup formula to Walsh. Those clarifications pass;
the different power-arity interchange constructor is paid locally in
Section 4 and was never part of that numerical setup formula.

Primary source pin is OpenAI
`math@3344da59991ed94f9ba711217b29c1d760badfa6`. Read the actual tape
`walsh.tex` and `permutations.tex` in full; Fourier `kernel.tex` and
`binary.tex` in full; the label, rectangle, low-rank, spectral and full
recursive-space proof portions of tape `interchange.tex`; and the
construction, precision, serialization and scheduling portions of tape
`uniformity.tex`. The arithmetic-applications corollary in the latter
is outside this review. Root independently audits `integers.tex` and
the outer reduction; this reviewer does not claim an independent full
reading of that outer proof.

Read the actual programme rational Newton/division construction, its
polynomial operation audit, the exact binary rectangle invoice S7--S8,
fixed-field Q2--Q5, E002's complete polynomial-interchange invoice,
cyclic executor, on-demand spectral repair, multidigit batching and
rational precision supplier. Read and independently audited S003's
explicit dyadic address construction. The four E003 space/packing
suppliers are this reviewer's work, already independently reviewed by
Route B; full-rate packing also has a separate Route C review.

Predecessor finite algebraic identities remain imports with their
recorded claim status. This audit verifies their stated physical
interfaces and quantitative composition, not every predecessor finite
identity from scratch.

## 2. All-arity label admission and the interchange invoice

The earlier fixed-J trial subsequence alone would not justify selecting
an arbitrary `m(e)` at each level. Route A's new all-arity supplier
removes this problem. For `x=ceil(log2 m)`,

```
v=ceil(log2(x+2)),
d=least power of two >=2 with d^3 v>=x,
t=2+ceil(x/d^2), q=2^t, h=2d-1,
N=q^(h^2), D=2(2+h q^h),
lambda=binom(h,d)^(d+1)(q-1)^d t^(d(d-1)).
```

The exact rank bound is particularly useful:

```
m r*/N <= m 2^(2d^2-2) q^(-d^2) <= 1/4.
```

It uses the integer reserve +2 in t. The same explicit formula gives
`N<=m^5`, `D<=sqrt(m)` and the logarithmic incidence bound for every
`x>=2^40`. Thus all sufficiently large odd arities chosen by B are
actually admissible. The enormous cutoff is finite and effective; it
is not presented as a practical parameter range.

The rank inequality also pays the critical simultaneous storage:
all query-indexed rank accumulators together have volume
`(m r*/N)V<=V/4`. Their query-specific common layouts are kept separate.
The two-pass pencil first accumulates the **raw pre-A_j** source sums,
then applies the central rank map and A_j, and finally delivers the
low-rank terms in a second destination pass. Direct and low-rank
contributions meet in the same ordinary output layout. Repeating a
destination endpoint only an absolute number of times preserves an
absolute multiple of the source invoice. Repeating it for every query
would not have done so.

S003's address space is doubled and its endpoint factor lists differ
from the predecessor's generic lists. B correctly retains a new
absolute geometric factor inside C_I. The old literal `2^19` schedule
allowance is not asserted to be the entire dyadic coefficient. No exact
numerical fixed-exponent admission certificate is supplied by this
asymptotic proof, and none is needed for its scale conclusion.

## 3. P-I: every actual local operation and its storage

The local compiler has the following complete coverage.

| Operation | Paid implementation | Uniform payload storage |
|---|---|---|
| Formula coefficient factors | E002's polynomial list of input masks and cyclic coordinate translations | Input, one translated term, accumulator |
| Small shift/check maps | Serial source/destination-role scans and exact represented-field arithmetic | A fixed number of input/check/output regions |
| Spectral coefficient selection | Current m comparison labels, on-demand small Vandermonde computation | One flag tuple and reused polynomial-m registers |
| Ordered affine maps | S003 dyadic elementary lists and the height-priced/HFS stream primitives | Fixed scan/sort regions; no coefficient-sized tape alphabet |
| Shared label pencil | The rank-budgeted two-pass schedule | All query rank arrays together at most V; one rectangle at a time |
| Leading-row batching | The whole `ell=ceil(log_3 W_bin)` occupied prefix, padded by less than two | The padding is charged before child volumes are computed |
| Binary field packing | Full-rate vector-space packing and unpacking | Same encoded volume; an absolute number of streams |
| Finite repair | Four sequential phases of volume V/16 | Geometric parked arrays |
| Main spatial descent | Group identical module-row calls within one label | Child fraction at most 2/N<=2/3 |
| Reserve descent | Merge and clear the main workspace before passing the whole stream | Only descriptors are parked |

The compact cyclic executor is essential. Its module dimension can be
exponential in polynomial m, while its path list and row-index routines
have polynomial size. Replacing those paths by a dense row matrix or
one tape per module row would invalidate P-I. The actual proof does
neither. Every spatial call repeated across the same module coordinate
is grouped within one physical label; this preserves its sum-of-volume
invoice and avoids exponentially many separate dispatches.

The comparison stream uses the actual ordinary layout in which H_j
precedes N_j. Its three consecutive runs supply a current ternary flag.
Keeping one tuple replaces the predecessor's m full-volume mask tracks.
The finite spectral repair is still sandwiched between its paid
converters; no spectral condition is applied to a premixed ordinary row.

The primary address construction is compatible with radix three at
every node. Binary-to-ternary full-grid padding is less than nine once
per binary interchange call; no variable prime selector is required.
The leading **binary** row count is `W_bin=d_m W_E,m`. Full-rate packing
makes this many arbitrary binary rows into W_E,m coefficient-field rows
and does not multiply encoded bit volume. The numerator and denominator
of every child-volume fraction both contain d_m, so it cancels. Only
completed spatial permutations may choose a new m and a new field.
The local order-three F/F-inverse repair tree retains its parent's
algebra and row coordinates through its whole finite unrolling.

For one sufficiently large absolute C, `e>=m^(C+2)` also implies the
stronger affine/row-key guard: the actual child field
`f=floor((e-ell)/(m+2a))` is at least twice every polynomial-m height
after enlarging C. HFS removes the affine header restriction entirely;
the guarded version already suffices. General row-sort keys are attached
to whole rows with a complete spatial suffix, not to individual tiny
field symbols. Cyclic translations need no such keys.

All recurring work is `V poly(m)` with the permitted root-logarithmic
factor. Polynomial-in-log V calculations are genuine descriptor setup,
not an uncharged per-datum action. Additive construction may be bounded
by `2^(C m^C)`. This verifies P2's intended distinction between a compact
streaming instruction and an optional large construction artifact.

The source parked-payload proof remains uniform. Main descents contract,
finite-repair descents contract, and full-volume reserve descents retain
no parent payload. Siblings reuse the same marked intervals. Descriptor
space along noncontracting reserves may be bounded by a fixed polynomial
in log V times logarithmic width depth; it fits the deliberately loose
`V poly(log u)` envelope. This review does not silently call that last
envelope an absolute linear-space bound before the final wrapper.

## 4. Interchange recurrence and additive setup

For fixed `r>8(C+2)` and `beta=1/r`, B's integer choice obeys
`e^beta/3<=m(e)<=e^beta` above a fixed base. Since `a=o(m)` and
`ell<=1+C m^C=o(e)`, the exact floor gives

```
e/(8m) <= f <= e/m.
```

Consequently the logarithmic widths contract between two fixed ratios
strictly between zero and one. Normalizing by sqrt(e), the child
coefficient is at most `2^(C Phi(log m))`; its cumulative logarithm is
a geometric sum bounded by `O(Phi(log e))`. The local time normalized
by sqrt(e) is bounded by `poly(log u) e^(-eta)` with
`eta=1/2-beta C>0`. Its sum is uniformly finite because successive
nonbase logarithmic widths have a fixed positive separation. Terminal
direct costs have an absolute bound after the fixed cutoff is chosen.

The constructor exponent is at most e/2 eventually because beta C<1.
Every local two-field stream has volume at least `3^(2e)`, even before
counting spectators. Thus its additive construction bill is absorbed
locally. This remains true when construction is repeated at each node;
the same local-volume charge is used in the recurrence. No giant root
description is scanned at the smaller node.

These facts justify the claimed interchange envelope. I found no
remaining quantitative obstruction in its recurrence or P-I composition.

## 5. P-W: the important space repair

E002's scalar precision note states a polynomial-m proportional-space
bound. For the current arity,

```
m^C = 2^(Theta(Phi(log a))),
```

which is larger than every fixed power of log k when a is comparable
with k. That predecessor sentence alone therefore does not supply P-W.
This is the principal issue resolved by the accompanying RW theorem.

The actual rational template has only polynomially many independent
row roles. Its dense row operations can be serialized over ordered
role pairs, retaining input, output accumulator and one term stream.
The on-demand spectral matrix occupies polynomial-m additive registers,
not a new matrix at every record. For every free rectangle, the first
source endpoint is prepared once and retained in a collection of
volume at most V. A destination collection of volume at most V sums
all query contributions before its shared final endpoint. Middle
coordinate maps and rational row arithmetic are genuinely paid
`m^C` local work. The source proof permits this sharing order even
when the intermediate subspace is degenerate, since it uses a paired
dual basis for the full nondegenerate form.

Binary elimination has polynomially many slot additions/exchanges.
The source packed-XOR controls and rank computations have polynomial
bit complexity in m and k with absolute degrees. Since m<=k, a single
fixed `G=C0 log k` guard pays the sparse exceptional sort. Its O(k)-bit
destination tags fit a Theta(k)-bit numerical record by an absolute
factor. They are removed before numerical children. Narrow fields
use direct bit moves. The use of an interchange envelope is linear
in its cost, as is explicit in the source proof.

Exact rational scaling costs `O((k+h+1)(h+1))`, for coefficient height
h<=poly(m), on actual fixed tapes. The guard k>=poly(m) places its
temporaries inside O(k) bits. W2 computes actual defects and the
Vandermonde/transpose-inverse table in polynomial-m bit work without
an exponential lookup. All field changes in the underlying exact bit
interchanger are opaque to this numerical layer: the completed child
returns the exact bit permutation and makes no rounding fault.

With RW's fixed-array schedule and the proved interchange supplier,
P-W has `V poly(log k)` visited space plus the allowed additive setup.
The changed schedule preserves the source Fourier endpoint count;
it does not add an m factor to the recursive numerical invoice.

## 6. Finite unrolling, actual nodes and numerical growth

The rational finite repair has two sequential phase children, each of
volume V/8, at height `h=ceil(log2(m)/4)`. Its full binary unrolling
tree has at most `2^(h+1)-1<=4m^(1/4)` vertices. Newton stages,
labels, rectangles, role pairs and coordinate matrix entries are all
polynomial in m. Therefore the fully completed finite local program
has polynomially many actual array operations and numerical children,
not merely a polynomial weighted call ratio. This is needed for the
global setup and rounding-event counts.

The logarithmic norm bound must apply to input-to-intermediate and
arbitrary-fault-to-later maps, including partial sums and parked
registers. The latest principal hash states exactly that condition.
Each elementary numerical row block has polynomial dimension and
polynomial coefficient bit height; the number of blocks/stages is
polynomial. Their product gives a polynomial-m logarithmic gain.
Spectral selection is a direct sum of small blocks, so `2^m` possible
keys does not multiply the norm. Completed child transforms are
normalized unitaries. This supplies the stronger gain condition,
not just a bound on the completed predictor.

The local coefficient field and arity stay fixed inside finite repair.
Changing parameters occurs only at the smaller spatial width. Hence
the finite exact identities remain intact during this node count.

## 7. Variable Walsh arity and leading rows

The integer choice
`z=ceil(cuberoot(y^2 ceil(log2(y+2))))`,
`y=ceil(log2(a+2))`, `m=2^z+1`
is odd and satisfies `z=Theta(Phi(log a))=o(log a)`.
The even floor `f=2 floor(a/(2A))` gives
`a/(2A)<=f<=a/A` above the checked base range and changes log width
by `z+O(1)`. Fewer than 2A leftover bits are transformed directly;
their cost is polynomial in m and is present in the local toll.

B's leading-row product is valid: for the entire deterministic width
chain, `sum log m_i<=log a_0`, so
`B=product W_i<=a_0^C`. The source selected-bit width is at most
`c k/log(2+k)`, leaving at least `2^(k/2)` spectator rows eventually.
Padding once to a multiple of B has factor less than two. At every
later numerical split the remaining leading count has exactly the
necessary divisibility. No padding loss compounds with recursion.
The rational W_i are in fact powers of two, although the weaker
divisibility argument is sufficient.

For `Y=log a`, the derivative of Phi on `[Y/2,Y]` is bounded below
by a constant times `Y^(-1/3)(log Y)^(1/3)`. Multiplying by the
width decrease `Theta(Phi(Y))` gives
`Theta(Y^(1/3)(log Y)^(2/3))`, which dominates
`Psi(z+O(1))`. Thus the logarithms of all normalized child
coefficients telescope to `O(Phi(Y_0))`.

The local routing term is also correctly charged:

```
m^C I(a,k)/sqrt(a)
 <= poly(log k) 2^(O(Phi(log a))).
```

This is where the different arity schedules matter. Using the
interchanger's power arity for Walsh would leave a positive power
of a here. The current proof retains this real cost and chooses
parameters that pay it. Depth and root-logarithmic factors are
absorbed by the claimed exponential envelope.

## 8. Global setup, precision and the common-space wrapper

Along a Walsh path `sum log m_i<=log a_0<=log k`. With polynomial
local branching and operation counts this bounds the actual whole
tree by `k^C'` array operations for an absolute exponent. The maximum
arity is `k^o(1)`, so even repeated setup has total cost/storage

```
k^C' 2^(C m_max^C) (1+k)^(m_max^C)
 = 2^(k^o(1)) = o(2^k).
```

This is an additive construction allowance. An entire exponential
table scan per record would violate it and is expressly excluded.
The compact and on-demand processors examined above meet that rule.

The explicit numerical guard `k>=m_max^K2` is necessary for all-length
correctness. It can be enlarged so that the logarithmic gain along
two ancestor paths, the event count and all coefficient widths fit
an absolute multiple of k. A failure selects exact schoolbook before
the numerical fast path is trusted. A time/space cap alone would not
detect inaccurate numerical output; the reviewed version does not
make that mistake.

The source fault-freezing argument then bounds all accumulated errors
by `2^(-p+O(k)+k^o(1))`. Choosing one absolute `p=C0 k` supplies the
caller's fixed desired error exponent and O(k) signed integer width.
Input-to-intermediate ideal norms satisfy the same bound. The local
exact rational primitive needs no coefficient approximation; the
remaining source irrational coefficients retain their charged
preparation and error terms.

The resulting digit routine has the explicitly nonconstant space
coefficient `C n(1+x)^C`. The final wrapper takes a power-of-two
chunk count r comparable to that coefficient, with an explicit
schoolbook branch when r>n. Each core uses at most a fixed fraction
of the global n-sized regions. Chunk products run sequentially;
rowwise assembly costs O(nr), and the r^2 calls cost at most rn
times the core per-bit envelope. Since r is polynomial in x,
the added logarithmic time is `O(log x)=o(Phi(x))`. This establishes
the conditional common-space conclusion without discarding the
proportional-space surcharge.

The precise outer CRT/short-axis/carry replacement is root's P-O
audit. This review's acceptance of the whole displayed multiplier
therefore retains that explicit source dependency. It verifies the
two-scale analytic implication and both physical local premises.

## 9. Finite replay, changes required, and remaining limits

Copied E002's rational checker without modification into the isolated
`rational-walsh-review-replay/` directory and ran

```
python3 -B research/moonshot-overhead-program/results/epsilon-uniformity/sessions/E003/route-a/rational-walsh-review-replay/verify_rational_walsh.py
```

It passed 203,949 exact signed scaling cases, 611,847 grid-rounding
checks, 630 negative-binomial cases, 200 predictor cases and 1,440
full-basis repair identities. It rejected 184 zero-gap divisions and
128 wrong-transpose controls. Toy windows use `s=|J|`; this replay
does not verify the asymptotic phase invoice or the tape schedule.
The other route-a receipts test the independent HFS, dyadic geometry,
full-rate packing, rank-pencil schedule and all-arity inequalities,
with their own exact stated finite scopes.

Required integration actions are narrow:

1. Bind P-W explicitly to `RATIONAL-WALSH-CONSTANT-SPACE.md` after
   independent review. The old polynomial-m proportional-space estimate
   is insufficient by itself.
2. Retain the binary-row count, finite-repair algebra scope, new geometric
   constant, intermediate-gain condition and numerical eligibility guard
   already present in the reviewed hash.
3. Record root's independent P-O review and the exact final proof hash;
   do not translate these written/finite checks into a claim that the
   full fixed-tape multiplier has been executed.

No unresolved algebraic or quantitative counterexample was found in
the scoped composition after these fixes. Further independent review
of the source finite identities and of the complete formal machine
remains valuable; this document does not erase those claim boundaries.

Credits: @CubeJerry; pinned OpenAI source proofs and their predecessors;
S002/E002 rational and characteristic-two suppliers; S003's explicit
dyadic realization; E003 Route B's two-scale analysis and Route C's
packing review; substantial AI-assisted derivation and adversarial review.
