# Discovery-route review of the S005 final report

**Decision: accepted in the reviewed mathematical scope.** The final report
accurately distinguishes the retained unconditional written frontier,
conditional transfers, proved representation/caller lemmas, and the suppliers
that remain open. No correction to a core proof is required by this review.

Reviewed report: `../FINAL-REPORT.md`

SHA-256:
`30ee75e8f25d475f42a8960792bb1d2dfd04127c675f4be4166d06c1d9f47ff2`

This review checks the lead's report against the final discovery deliverables
and their separate reviews. Route A authored the discovery proofs; this is
not presented as a second independent proof audit of those same notes.
The independent proof reviews are in route C, with a further UC precision
and KC review in route B. The present review does not attest the later
observed session completion, publication state, a new Lean rebuild, or a new
remote-source refresh. Session timing is correctly delegated to SESSION.json.

## 1. Rate and representation claims

The opening and frontier sections do not announce a new unconditional
complete multiplication bound. CT's polynomial log-log result is explicitly
conditional on both local template contracts; neither family is said to be
constructed. The exponent matches CT13,
`max(p_I+4,p_W+b_CT+1)`. The report distinguishes this fixed CT parameter
from the varying field-degree parameter in UC. The endpoint is likewise
presented only as a target or supplier implication.

RO's claim is now expressly for invertible columnwise binary reindexings in
the supplied rowspace order, with complete address fibres and wide records.
That preserves arbitrary independent payloads, rather than orbit averages.
The generic converter has the proved upper invoice
`O(V[poly(A)+a])`; the final report correctly describes its `Va` term without
discarding the polynomial-arity work or asserting a converter lower bound.

BE is scoped to common even slot width, one admissible pairing and the
supplied orbit layout. In that setting the square Bell basis preserves all
independent data. The reported local closure includes the actual quadratic
parity keys and their rational matrix-table evaluator. It does not silently
replace the evaluator by its tensor square, suppress dependent-generator
phases, or assert that arbitrary outer complex phase tables are covered.
Its explicit numerical guard supports the local fixed-width invoice; the
report does not claim that BE alone proves the global NW error theorem.

The two full-volume half-width entry/exit calls remain visible. SU's report
sentence accurately gives the total partial-Walsh width bound `a/2` per
encoder in its specified square Walsh/monomial class. The underlying proof
also yields entry-plus-exit normalized child mass at least `sqrt(2)`.
These are positive-invoice consequences for the admitted word model.
The six half-width transforms in BO describe the standard encoded outer
product schedule, not all possible bilinear implementations. The report
expressly avoids a universal time lower-bound claim.

## 2. UC's exact all-input interface and integer caller

UC1 is an isomorphism on the whole free module of `q` coefficients over
`Z/(2^H)`. Pairwise coprimality modulo two lifts to comaximality because
`1+2C` is a polynomial unit modulo `2^H`. Monicity supplies canonical
representatives, and the factor-degree sum is exactly `q`. Consequently
both coefficient and residue encodings contain exactly `qH` independent
payload bits. The report's full-rate statement does not introduce a
redundant list of `q` extension-field elements or an invariant-sector
restriction.

The packing parameters give `qH=Theta(n)`, `H=Theta(b)` and
`b=Theta(log n)` after a fixed exceptional range. The product degree is
strictly below `q`, and the ordinary convolution coefficients are below
`2^H`. Thus the actual literal lifted product polynomial `P` suffices even
though it is generally not `X^q-X` modulo four. The inverse must return
coefficient order, and the ensuing radix carry scan has the invariant
`carry <= h(2^B-1)`. These guards support the report's exact recovery and
linear final scan. They do not supply the open inverse transform.

## 3. Local costs, factor generation and the remaining gate

The two local multiplication sizes are correctly separated:

| Proved work | Aggregate time | Largest local integer operands |
| --- | --- | --- |
| UC3 residue products, reciprocal preparation and monic reduction | `O(qH log^2(b+2))` | `O(bH)=O(b^2)` |
| FS1 factor-stream construction | `q b polylog(b)+poly(b)` | `O(b^2 log(b+2))` |

UC3's reversed monic divisors have constant coefficient one, so their
Newton reciprocal step works over `Z/(2^H)` without division by two.
Summing the per-factor bounds uses the actual degree identity
`sum d_i=q`. The published integer multiplier is used only on those small
operands in the proved work, with local scratch bounded by its running time
and reused. No unproved global linear-space property of that multiplier is
needed.

FS1 imports only deterministic polynomial preprocessing for a small binary
field and normal basis. Its own schedule pays for scanned Lyndon words,
one dense basis conversion per retained orbit, sequential conjugates,
two-dimensional packing and reused local product streams. It does not
import a random-access enumeration delay as a tape bound. The factor
directory is `O(q)` bits using degree tags of `O(d)` bits per degree-`d`
factor, so it is suitable for sharing even at binary precision.

Because `H=Theta(b)`, both displayed local invoices are
`qH polylog(b)+poly(b)`. For fixed exponents this is eventually below
`qH sqrt(b)`, with a fixed cutoff. The report's statement that these bills
fit the prospective endpoint budget is therefore valid. It does not mean
that the endpoint itself has been obtained.

The global degree-`q` product, CRT cofactor inverses, factor access, layout
and return passes remain inside the transform gate. The corrected report
calls `O(qH b^2)` a product/remainder-stage invoice, before global inverse
constants and a common visited-space schedule. It also identifies the
full-size upper-level products. They are neither assigned to FS1 nor
silently paid by the desired multiplication theorem.

## 4. Precision lifting and the carry interface

UC5 uses canonical low-digit representatives. Both directions at precision
`2t` use two precision-`t` transforms and the same forward carry-remainder
map `K_t`; inversion does not require a separate inverse-carry oracle.
The normalized sum in the report retains every dyadic precision level.
The absolute space implication requires the stated local contracts,
reused child regions and a shared compact factor directory; it follows
from geometric active volumes, rather than only a live-memory estimate.

The proposed endpoint conditions are sufficient because the dyadic sum
of `sqrt(t)` is `O(sqrt(H))`, and `H=Theta(b)`. Binary CRT and the fast
carry maps remain explicitly unconstructed. The broader polynomial
log-log supplier contract likewise retains the extra precision-depth
factor.

KC's displayed first-carry formula is now labelled over `F2`, with the
integer remainder matrix distinguished from its binary reduction. A
lifted XOR circuit supplies its own integer matrix `C`; the correction
`((A-C)/2 mod 2)x` is genuinely required and charged. The report does not
infer an actual fast lift merely from a fast binary circuit. Its proposed
continuation is consistent with the exact canonical identities.

## 5. Corrections incorporated and frozen dependencies

Before acceptance, the lead incorporated the RO converter qualification,
the classical-tree invoice qualification, the complete-fibre/wide-record
and common-pairing scope, the precise SU width statement, the fixed CT
parameter name, the limitation of the outer phase theorem, and the field
of the first-carry formula. These are report precision improvements; the
accepted core proofs were not modified.

Discovery proof hashes checked during this review:

- RO: `b8c07d0cfc933636f4182555d5a41578167ebb58959be119bd5eaa5562117c40`
- BE: `840492fcefb4d7f7accf68e1591e81bdfe3070b6de26e9d38c468516858aa5d3`
- SU: `09d7fc8bd28b7309a8798732e4325b0f8c31bfaeac10bf9a9f18f6318b9da3fe`
- UC: `e451b65deb2657176e354e2b3d4ab3da6d1ecba44d75c4d7b44610ac9bb6560b`
- FS: `13be8001733a677195095abbace706db3fe86f1fcef490531c65f4c49f09be2c`
- KC: `db94d6694f7352309f021e93e41e07cfae5c7bdf9720408691b22ad213774d5d`

No new finite experiment was needed for this narrative consistency review.
The report correctly treats dense small CRTs and brute-force field searches
as checking oracles, with their exact replays recorded separately, rather
than evidence that the missing asymptotic suppliers have been constructed.
