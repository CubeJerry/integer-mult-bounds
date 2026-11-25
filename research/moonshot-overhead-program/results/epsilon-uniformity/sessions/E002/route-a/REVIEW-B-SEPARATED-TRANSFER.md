# Independent A review of B's separated transfer and Walsh arithmetic

Reviewer: E002 Route A, a separate agent from Route B. Status: **accepted
conditional transfer and numerical components within their stated scope**.
This is AI-assisted written review, not human refereeing or kernel proof.
It does not certify that the complete physical family satisfies all premises.

Reviewed SHA-256 snapshots:

- `separated-setup-transfer.md`:
  `e2d4aab0a74edf4acac884588728d734524e112a3e4f92ec0eeb62f572aa8ed5`
- `polynomial-walsh-precision.md`:
  `7dbc8926b2e68840e54f1ce981b5a827f53ab3f29dbe0ea7420ba25093a0ce19`
- `verify_rational_walsh.py`:
  `dee120e42ae4d4ba0637a015e1f2e331df35ac382ea2dbf0d6cfca4ae75db5f7`

## 1. Additive preparation and the complete conditional implication

S1 is valid with its stated constants. For t>=64(R+1)^2, one has
2R sqrt(t)<=t/4 and R<=t/4, while log2(1+t)<=2sqrt(t). Thus
2^R(1+t)^v<=2^(t/2) for 1<=v<=R. The use of this lemma is restricted
to additive setup, never repeated uncharged per independent input record.

F/E/N/R are independent local contracts: finite identities/call margins,
physical nonrecursive execution, numerical/shape control and reuse of
visited regions. They are stronger than the old expanded-data compiler but
are not equivalent to the desired complete runtime. E explicitly includes
interpretation, tags, sorting, coefficient access and head movement. It
forbids turning additional padded child data into free scratch.

The node-count overestimate retains the form 2^(m^C)L^(m^C), and S1
absorbs that total above log2 u>=m^{C'} after increasing an absolute exponent.
The visible poly(log L) factors are absorbed by the allocated 1/(2J)
slack with only polynomial-J prefactors, hence polynomial-m prefactors.
Geometric parked payload plus reusable intervals bounds visited cells;
the proof does not substitute a live-space estimate for the required union.

The direct selector uses integer comparison J^4 h<=q for dyadic J=2^h.
Its maximality proves J=Theta((x/log x)^(1/4)) and
Z=J^3 log(J+2)=O(x^(3/4)(log x)^(1/4))=o(x). No real oracle or uncharged
best-candidate advice is used. The large preparation profile still fits
n/16 eventually because log2 g<=2^{O(Z)}(1+x)=2^{o(x)}, whereas
log2 n=2^x-1. This also proves the applicability threshold and additive
storage fit, independently of their unknown finite cutoff.

The chunk ratio r>=8m^K gives proportional core space at most n/4 above
the cutoff. The diagonal wrapper charges r^2 chunk calls and O(nr) movement,
so log2 H<=O(log m)+x/J. The attempt clocks, visited-region caps, exact
fallback and cleanup ensure correctness and uniform linear visited space
at every input length. Eventual success makes the n^2 fallback cap irrelevant
to the asymptotic envelope; it is not ignored at finite lengths.

Thus S0 is a complete conditional theorem. It is not yet an unconditional
improvement until every stated physical contract is supplied and reviewed.
The general-profile clause correctly requires a computable inverse profile
for arbitrary real p,r; the concrete (3,1) case needs no such extra oracle.

## 2. Rational record arithmetic and on-demand tables

W1 is sound: multiplication of a long integer by an h-bit numerator takes
h shifted-addition scans. Restoring binary division uses an h+1-bit remainder
and O(h) actual steps per input bit. Signed floor correction requires the
one extra subtraction exactly when a negative product has nonzero remainder.
The output differs from the exact same-grid rational product by less than
one grid unit. This is a k*poly(h) bound, not a general fast division claim.
It avoids a precision-k coefficient-generation cost per datum.

For W2 I read the predecessor pairwise/Newton/division construction and
its polynomial source-operation audit. The actual defect set is a subset
of the Chebyshev outside-window set; hence its size is at most s. Every
selected gap is a nonzero integer, so the inverse is defined. The first
ell rows of the check matrix give a nonsingular Vandermonde matrix on
ell distinct rational nodes. Its transpose inverse produces the lift
needed by the exact repair identity. The empty-defect case is handled
without division. Fraction-free elimination and the explicit determinant/
gap denominator bound give polynomial-m coefficient height and actual
bit cost, including sequential matrix access.

A complete coefficient matrix is generated, then each k-bit data record
is processed by W1. This separation is essential: saying merely that a
symbolic table can be constructed in poly(m) arithmetic operations would
not pay the physical long-record cost. Numerical records have width Theta(k),
so reading O(k) address bits to obtain the spectral tuple is already linear
in that record's bit volume. Row alignment remains an explicit interface.

## 3. Norms and absolute O(k) precision

The selected rational table is block diagonal over spectral addresses.
Its operator norm is the maximum of block norms; counting 2^m possible
cases cannot multiply it by 2^m. Polynomial block dimensions and rational
bit heights give logarithmic local gain m^{O(1)}, including partial sums.
The source common-ancestor propagation argument then gives
2^{m^{O(1)}log(k+2)} global gain. With arity at least m and polynomial-m
branch count, the event tree has polynomial-k size of absolute degree,
up to a polynomial-m prefactor.

For k>=m^{K2} with sufficiently large absolute K2,
m^{K4}log(k+2)<=O(k). W6 therefore permits a fixed multiple of k fractional
and integer bits. The bootstrap also bounds intermediate exact products
and norms, so this is not just an output-error estimate. The remaining
irrational phase preparation retains its separate source charge.

The theorem remains conditional on the physical address/row executor and
shape interface. It does not move a spectral table across an unpaid converter
or reduce rational coefficients into the characteristic-two data field.

## 4. Finite checks and limits

The inspected W1/W2 checker was copied to `replay-walsh/` and executed in
that isolated directory. Its JSON receipt and execution log record the
actual counts. The cases check signed long/short scaling, generalized
integer binomials and the full repaired basis-vector identity, with zero-gap
and wrong-transpose controls. They use toy phase widths, explicitly not the
asymptotic source call invoice. They do not execute a fixed Turing machine,
prove a universal cost bound or verify the complete multiplier.

No unresolved objection was found in these two mathematical components.
The remaining admission gate is the complete physical composition, including
all call volumes and a compact fixed interpreter.
