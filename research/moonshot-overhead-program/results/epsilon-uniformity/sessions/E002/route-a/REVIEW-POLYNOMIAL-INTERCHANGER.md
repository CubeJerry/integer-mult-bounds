# Independent A review of the polynomial interchanger and spectral supplier

Reviewer: E002 Route A. Status: **accepted written component composition**,
with the grouping-volume correction incorporated. This is not acceptance
of a full multiplication theorem. No human or kernel review is claimed.

Snapshots read in full (SHA-256):

- C `polynomial-interchange-invoice.md`:
  `311c0d4987fde89502183bf2fb860c2462675667c6ff8e29ce59769d154aa5d1`
- lead `on-demand-spectral-repair.md`:
  `e2b9a20b1d177efe7cab8f76d0aadfcbd9b226242c53c0b1e090290aee217e2b`

I also read the predecessor order-three group identities, spectral labels,
pencil decomposition and four-element discrepancy repair, plus C's
small-radix and masked-translation suppliers. Separate review/replay records
cover the latter two components. HS/HA is this reviewer's own supplier,
independently reviewed by B/C and the lead; this review does not count as
an independent review of HS/HA itself.

## 1. On-demand spectral table

The signed-count identity is valid even for negative c_beta-u. In formal
characteristic-two series, writing a=qT+r with 0<=r<T gives
(1+X)^a=(1+X^T)^q(1+X)^r, whose degree-below-T truncation is (1+X)^r.
Negative q is allowed because 1+X^T is a unit. Evaluation then occurs only
on the finite retained polynomial. This proves the phase formula and the
actual gap condition without expanding 3^m cases.

The containing exception set has at most floor(B/32) shifts by the stated
pairwise-variance calculation and the B>=219 rounding guard. It may contain
zero gaps, which is safe: the table multiplies by the gap squared and never
divides by it. Vandermonde inversion recovers the supported error; transpose
inversion makes the lifted coordinates equal to the desired correction.
Each nonzero gap belongs to the embedded F4 and has cube one, even though
the data are arbitrary in the larger check field E. Therefore the repaired
output is exactly zX on every independent module row. General E-valued gaps
would invalidate this argument, but they are explicitly excluded by the
computed F4 predictor/target phases.

All coefficient computation is polynomial m over a field of O(log m) bits.
Even fully sequential access to the small matrix leaves polynomial bit
complexity. The physical mask scans follow the source comparison construction:
no full long prefix is reread per symbol. The label/role counts are polynomial,
while the module coordinate is an unchanged tensor spectator. Temporary
metadata is paid parent scratch and stripped before recursive calls.
The paid forward/inverse conversions and their R/16 phase sizes remain.

## 2. Scalar execution and finite regrouping

The power-two window has D_pred<=24sqrt(m) and <=m above the explicit
m>=4096 guard. All shifts retain a common unpruned copied formula and module
width. C's static path expansion supplies polynomially many masked module
translations per affine coefficient. These act after the existing shared
routing and do not introduce one spatial Q_j call per path.

The check coordinates before child conversion are
(copy16,half2,checkB,module_w). The bijection dup32=2*copy16+half2 followed
by the finite control permutation supplies exactly the next child's
(shiftB,dup32,module_w) independent rows. The module is neither dropped nor
identified, and internal check padding remains paid. Only polynomial-sized
control ranges are moved; a log w procedure would also be polynomial m.
Four child phases of relative volume 1/16 give mass 1/4 and geometric parked
volume. Their finite depth h has 16^h<=16m and 4^h<=4sqrt(m), so explicitly
unrolling control types remains polynomial in m.

## 3. Complete recursive invoice and the important space distinction

The larger predictor window is charged in I3. Its leading term is at most
8*24*64=12,288 times sqrt(m) D_I(1+lambda). The direct leaf term fits the
stated 2^14 bound. Padding by at most two and reserve restoration then fit
2^17 in I4. The predecessor label estimate, at the enlarged absolute
2^42 J^3 log2 J threshold, provides the same strict 1/2 contraction and
log2 m=O(J^3 log J). None of these claims relies on a smaller old window.

Grouping many identical module-row calls preserves their **summed** child
volume and hence the time recurrence, but changes the maximum size of one
child. The correct one-label grouped bound is 2/N_label<=2/3, not 2/W.
The reviewed C note explicitly uses the correct bound. A's related
ADDRESS-RADIX-INTERFACE.md was corrected in the same way. This fixed strict
volume contraction suffices for the geometric stack argument; the erroneous
stronger fraction is unnecessary.

The base range ell+m+2a, small radix b, exact scalar blocks and affine
bit heights all have polynomial-m bounds. Digit moves now charge polynomial
b on a fixed number of tapes. Metadata is removed before child calls.
Full-volume reserve children run after main workspace is cleared and park
only descriptors. Thus actual visited regions, as well as live arrays, have
polynomial-m volume. The data field is embedded once and its binary block
encoding is reused at all depths; no per-level alphabet expansion occurs.

I6--I7 therefore follow from their stated source recurrence and supplied
local operations. This is a genuine polynomial-coefficient interchanger
component, not yet the rational numerical Walsh/outer integer assembly.

## 4. Remaining global gate

A whole multiplication result still needs the distinct rational Walsh
processor, its numerical precision, outer bit permutations, exact assembly,
and a fixed single-machine common-space selector. Those cannot be supplied
by silently substituting the exact characteristic-two processor for numerical
coefficients. B's conditional transfer isolates the required interfaces;
its hypotheses must be matched to the complete assembled caller.
