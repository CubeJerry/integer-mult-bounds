# Rational address changes priced by coefficient height

Status: **proved component, awaiting independent review**. This is a fixed-tape
algorithm for the ordered affine operations used by the source interchanger.
It is not, by itself, a new multiplication envelope.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, November
tape `build/interchange.tex`, and September tape
`build/sections/02-streams.tex`, Lemmas `lem:elementary-streams` and
`lem:ordered-affine-streams`. The latter proves linear-volume cost for fixed
rational coefficients by using one stream per increasing piece. The new
construction replaces that numeric-magnitude dependence by an absolute
polynomial in binary coefficient height, with a fixed number of physical tapes.

## 1. Statement and model

An array of arbitrary symbols in a fixed finite alphabet is stored in
lexicographic order on `[P] x [Q] x [B]`, with positive integer ranges and
volume `V=PQB`. The trailing coordinate includes record payload and collapsed
spectators. Descriptors and coefficients are supplied in canonical binary;
the number of formal fields is fixed. Permutations move entire suffix blocks.

**Theorem HS.** One fixed deterministic finite-alphabet multitape machine,
with an absolute integer C, implements

    (p,y,t) -> (p, c*y mod Q, t)

and its inverse for every nonzero integer c with gcd(c,Q)=1 in

    O(V (1+h)^C) actual steps and cells ever visited,       (HS1)
    h=ceil(log2(2+|c|)).

Constants are independent of P,Q,B,c. There is no polynomial-in-|c| factor,
nor a log Q factor per data symbol. The bound includes preparation, counters,
descriptors, padding, scans, rewinds and cleanup. Thus a signed rational unit
c/d has the same bound with h=ceil(log2(2+max(|c|,d))), provided d>0 and
all necessary denominators and numerators are coprime to Q.

The inverse is implemented by reversing the small-coefficient rearrangement,
not by treating the possibly large residue c^{-1} modulo Q as a coefficient.
Q=1 is trivial. A negative c is positive scaling followed by the source's
linear-volume negation, which reverses the nonzero target blocks and restores
the internal order of each block. Hence take Q>=2,c>0 below.

## 2. Exact run decomposition

Reduce c modulo Q if necessary to 1<=a<Q; its bit length is at most h.
If a=1 return the input. Otherwise write Q=a*q+s, 0<=s<a, q>=1. For
r=0,...,a-1 define

    y_r=ceil(r*Q/a),  t_r=(-r*Q) mod a,
    ell_r=y_(r+1)-y_r.

For 0<=k<ell_r,

    a*(y_r+k) mod Q = a*k+t_r.                         (HS2)

Indeed a*y_r-rQ=t_r lies in [0,a), and the whole interval
[y_r,y_(r+1)) is the increasing piece with floor(a*y/Q)=r. Since gcd(a,Q)=1,
r->t_r permutes [a]. Counting integers of residue t_r modulo a in [Q] gives

    ell_r=q+1 if t_r<s, and q otherwise.               (HS3)

All a runs are nonempty and contiguous. Their lengths differ by at most one.

## 3. Forward algorithm on a fixed number of tapes

Perform each stage for all prefix fibers, retaining their boundaries.
No step allocates a tape per run.

1. Scan runs in r order. Copy their ell_r whole B-symbol blocks and append
   one zero block when ell_r=q, so all runs have q+1 blocks. Attach the
   h_a-bit key t_r, h_a=ceil(log2 a). The recurrence
   t_(r+1)=(t_r-(Q mod a)) mod a generates keys with O(h_a) work each.

2. Sort whole run records by key with h_a stable binary LSD passes. A pass
   scans each key and its complete payload onto one of two tapes, then
   concatenates the two pieces per prefix. Per-prefix counts or delimiters
   retain boundaries. Remove keys. The shape is now
   [P] x [a] x [q+1] x [B], where row t is the run of output residue t.

3. Pad a to A=2^h_a, a<=A<2a, using zero rows. The payload volume is

       P*A*(q+1)*B < 4*P*Q*B = 4V.                   (HS4)

4. Transpose [A] x [q+1] by moving the h_a binary row digits, last digit
   first, across the entire [q+1] field, preserving their relative order.
   One such move splits on a single bit into two tapes and merges in the
   new required order. The ordinary elementary-stream proof permits an
   arbitrary intervening integer range, including [q+1]. It preserves
   suffix-block order. There are h_a scans of at most 4V symbols, including
   head returns and cleanup. The new shape is
   [P] x [q+1] x [A] x [B].

5. At each column k discard rows t>=a; at the last column k=q also discard
   t>=s. Remaining output order is k=0,...,q-1 with all t in [a], then
   k=q with t in [s]. This is precisely increasing a*k+t in [Q]. By HS2
   every original block reaches its required address.

Padding is removed by known positions, never by examining data values.
Genuine zero records are preserved just like all other records.

## 4. Inverse without a large new coefficient

Insert the same dummy slots into natural output order; undo the h_a digit
moves in reverse order; remove dummy rows t>=a. Sort the remaining run
blocks by the inverse key

    r=(-t*(Q mod a)^{-1}) mod a.

This inverse is modulo a and has only h_a bits. Compute it once by the
extended Euclidean algorithm and generate the keys. Use the same stable
whole-run radix sort. Remove the final padding block exactly when t_r>=s,
then concatenate in r order. HS2--HS3 prove that this inverts the forward
permutation, with the same kinds and numbers of physical operations.

## 5. Actual-step and visited-space accounting

Initial division Q=a*q+s, coefficient reduction and the small inverse
have fixed-polynomial cost in h+log(2Q). Initial shape preparation has
fixed-polynomial cost in h+log(2V), bounded by V(1+h)^{C0} for an absolute
C0. Reduction is performed before any enumeration of a runs.

For one prefix, a sorting pass moves O(QB+a*h) cells including headers.
Across O(h) passes the cost is O(QB*h+a*h^2)=O(QB(1+h)^2), since a<=Q.
Key generation and comparison contribute a*poly(h)<=Q*poly(h).
Padded payload is at most 4QB. Transposition takes O(QB*h) steps.

A per-run counter reset for q+1 blocks and B symbols costs
O(log(2q)+log(2B)). Even fixed-degree descriptor arithmetic fits: for
fixed d,

    log(2Q)<=h+log(2q),
    (log(2q)+log(2B))^d <= C_d*q*B.

Thus each such per-run calculation costs poly(h)*q*B, and a runs cost
O(QB poly(h)). Incrementing and returning fixed-width counters uses
amortized ripple counting, as in the source. The prefix counter is only
advanced and tested; its entire long contents are not reread per run.
Only a fixed number of collapsed formal fields is involved in a scan.

Headers occupy O(P*a*h)<=O(Vh) cells. Padded payload occupies at most 4V.
Arithmetic registers and descriptor lists use polynomial space in
h+log(2V). A fixed set of regions is reused at every pass and prefix,
so these estimates bound cells ever visited, not only live cells. This
proves HS1 with one absolute polynomial exponent. No arithmetic degree
or tape count depends on c.

To implement c/d, compose inverse scaling by d, scaling by |c| and
negation if needed. This proves the rational version.

## 6. Source lower-triangular address maps

**Corollary HA.** A rational invertible lower-triangular map on D fields
modulo Q, whose coefficients have numerator and denominator bit heights
at most H and are valid modulo Q, has local nonrecursive cost

    V * poly(D,H) actual steps and cells ever visited,      (HA1)

with an absolute polynomial, plus caller-supplied descriptor construction
of fixed polynomial degree. All fields and spectators contain occupied data.
No vacant workspace address field is assumed.

Process target fields in descending physical order. There are O(D^2)
one-control shifts and D diagonal scalings. For a shift, ordinary arithmetic
computes its offset on O(H+log Q) bits for each prefix ending before the
target. The full Q-value target fiber pays for every fixed power of log Q;
only poly(H) cost per fiber symbol remains. This is the source ordered-shift
proof with coefficient heights explicit. Long spectator counters are advanced
rather than reread. Apply HS to each diagonal scaling and inverse. A fixed
interpreter stores and scans the polynomially sized instruction list; this
adds only an absolute polynomial in D,H. No new interchange call is needed.

For a general rational matrix retain the source ordered Bruhat factorization
and its existing field-permutation call count. HA changes only the local
linear-work coefficient of the triangular factors, not the recursive-call
invoice or the cost of arbitrary field permutations.

## 7. Scope, next questions and credit

The prior physical ledger charged numeric address magnitudes 2^{poly(m)}.
HA instead gives polynomial-in-m local affine work whenever dimensions and
coefficient bit heights are polynomial in m. This is a complete improvement
to that specific source operation. It does not alone close a multiplier:
full-rate tensor row execution, spectral coefficient access, radix/batch
padding, precision and proportional space need separate composition proofs.
No endpoint, fixed-beta multiplication envelope or general lower bound is
claimed by this note.

Open next questions:

1. Combine HA with a small compatible radix and a multidigit batch block,
   including base-width and padding charges.
2. Price characteristic-two cyclic tensor factors and shift-only checks on
   actual tapes using their succinct structure.
3. Separate large one-time construction from proportional execution and
   recompute a full schedule with a common visited-space cap.

Credits: Jerry Chen (@CubeJerry), OpenAI stream lemmas, predecessor programme
height and physical-ledger audits, and substantial AI-assisted work in E002.
The new contribution is the bounded-tape run sort and short-row transpose
with explicit height dependence.
