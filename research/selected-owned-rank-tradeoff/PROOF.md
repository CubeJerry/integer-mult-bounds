# Paid Gaussian rank versus whole-field scalar work at the 23 selected owned rises

**No new κ.** This is a source-specific obstruction for isolated replacement
of the 23 owned rises in selected #7000, not an impossibility theorem for
κ=1/200 or for joint rewrites of the native word.

## 1. Source and question

Freeze canonical `CrocSwap/integer-mult-bounds` at
`e54523517d0f03e58352e647c403a5af3e525a57`. Its selected conditional saving is
`363005817/100000000000`. The live word is
`research/shared-wire-split-composition/data/final.json.gz`, Git blob
`74563a7867d9d762b6588f65362369668841bb3e`, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The complete paid and productive profiles are those in the source package's
`FULL-RESULT.json`; the selected application review binds that invoice to
the actual caller. Neither source is changed or independently readmitted here.

Owned storage is correlated with public data. That fact might suggest that
its prescribed rank-r rise can be replaced by a cheaper rank-s job. The
question here is precise: keep every surrounding source event, return the
same actual owned field before its next use, and allow the replacement only
that field plus independent scratch, without precomputed data-dependent
side information from other public/owned fields. Can its total positive
Gaussian child tariff be strictly lower than r^t at t=199/200 while retaining
sublinear whole-field work at unbounded column multiplicity f?

## 2. Exact source reachability

At a native frame U the physical field is `T_U^(tensor f) z`, and the
normalized z is a rational linear combination of independent entering public
arrays. MOVE changes U without changing z; common-frame ADD and SCALE act on
the normalized rows with their exterior scalar coefficient unchanged.
INIT sets the owned row to zero, COPY is ADD into its declared destination,
and CLEAR drops the current row. This is the credited common-chart invariant
used in the selected application review, not a new tensor-lifting principle.

An exact source scan finds 23 owned rises with rank histogram

`{1:10, 2:4, 3:1, 4:6, 5:1, 6:1}`.

Every entrance row is nonzero. `OWNED-ROWS.json` supplies a source event,
owner, both frames and a particular nonzero public coefficient for each;
the full-row discovery also records support sizes 79 through 314. The
standalone acceptance checker recomputes all listed pivot coefficients
directly, authenticates the entire word and checks frame inclusion/ranks.
These are actual scalar rows in the common-chart interpretation, not formal
free-group rows whose physical specialization might vanish.

**Reachability lemma.** If an entrance normalized row is
`z=Σ_j c_j x_j` and some c_a≠0, then its physical owned value is surjective
onto the complete array space. For any desired y, set
`x_a=c_a^-1 (T_U^(tensor f))^-1 y` and all other entering arrays to zero.
All frame maps are invertible. Thus a replacement correct for every entering
public array must compute the prescribed complete operator on every owned
array. Other fields need not be independent of that array: their exclusion
from the replacement's input is an explicit scope restriction.

This surjectivity argument is over complex arrays. On a prescribed dyadic
grid, a rational coefficient with an odd numerator need not have a dyadic
inverse; no grid-surjectivity assertion is made. Exact equality of linear
maps only needs the reachable images of an admissible scaled basis, which
span the complex array space, not access to every unit grid point. It does
not assert that every
unit-radius owned array is reachable from unit-radius public arrays with a
source-independent constant one. If norms are needed, setting only x_a
nonzero gives scaling |c_a|, a fixed positive constant independent of f.

## 3. A paid-rank/scalar-work tradeoff

Fix integers r,f≥1. The prescribed return has form `U=L C_(rf) R`, with
unit-modulus monomial adapters L,R and complete spectator coordinates. The
selected Gaussian/Clifford convention gives exactly `2^(rf)` nonzero entries
in each row, each of modulus `2^(-rf/2)`; monomial unit phases preserve this.
This normal form is inherited from the selected application review section 2
and its checked native factors. The present dimension/inclusion and row
scans do not independently prove the full Clifford factorization or phases;
the stored binary frame bases need not be orthonormal in the ordinary Gram form.

Consider any finite linear replacement program on complete arrays with one
data input x and any number of independent scratch arrays. Permit:

- arbitrary monomial maps, including width-dependent address permutations;
- arbitrary scalar multiplication, COPY and reset/erasure;
- g binary whole-field ADDs;
- positive Gaussian children of selected dimensions `s_1 f,...,s_m f`,
  with positive integer ranks s_j and arbitrary monomial adapters.

All scratch input dependence is required to cancel at the output; giving
free independent zero scratch only enlarges this class. No operation may
read precomputed data-dependent side information from outside the replacement.
Let `s=Σ_j s_j`. Scalar and monomial work may depend on f; no bounded-coefficient
or fixed-Clifford-alphabet premise is needed for the support estimate.

**Tradeoff theorem.** The output operator A has at most `2^(g+s f)` nonzero
entries in each row of its x-input block. Consequently

`||A-U||_(2→2)^2 ≥ max(0, 1 - 2^(g-(r-s)f))`.

In particular exactness, or error strictly below `1/sqrt(2)`, implies

`g ≥ (r-s)f` whenever s<r.

**Proof.** Initially the x-input matrix is identity, with row support one;
independent scratch has zero x-input block. Monomial maps and scaling do not
increase maximum row support, COPY duplicates it and reset decreases it.
An ADD takes a union of two row supports, increasing the global maximum by
at most a factor two. A rank-s_j child mixes at most `2^(s_j f)` rows, so
increases the maximum by at most that factor. Induction gives the first bound.
For one row u of U and any row a supported on at most K positions, the
unrepresented entries contribute at least `max(0,1-K/2^(rf))` to squared
Euclidean error. Allowing a to agree exactly on its support minimizes that
row error, so arbitrary coefficients cannot improve the bound. Operator
norm dominates every row norm. Substitute K. If g<(r-s)f, integrality gives
g≤(r-s)f−1, hence squared error at least 1/2. ∎

The sparse-row projection inequality is classical and already used in
Nick Petalas's `terminal-approximation-floor` (#5111). The new result is the
paid Gaussian rank/scalar-work combination and its authenticated application
to every current selected owned rise; no priority is claimed for support
counting or sparse approximation.

## 4. Consequence under the native tariff

For 0<t≤1, subadditivity gives
`Σ_j s_j^t ≥ (Σ_j s_j)^t = s^t`.
Thus a replacement with paid child moment strictly below r^t has s<r. The
theorem forces at least f whole-field ADDs. A fixed finite native template
cannot provide this for all f. Even an f-dependent literal full-pass program
has Ω(Vf) scalar work when each complete-array ADD traverses volume V, so
cannot be charged as `O(V f^t polylog(f))` for t<1.

This last statement is conditional on the declared full-pass execution
tariff, not a general lower bound for optimized algorithms. A compiler
fusing operations into a different algorithm, partial-field implementation,
shared data-dependent side information, or a changed output contract needs
its own full accounting and is outside this result. Additional productive
helper targets could change a signed invoice even when the paid floor holds;
they are not granted by an independent owned scratch bank.

The bound is sharp in its scalar escape: `C_1=(1+i)I/2+(1-i)X/2`.
Applying this identity separately to rf binary coordinates realizes C_(rf)
using rf whole-field ADDs, monomial bit flips, scalar multiplications and
copied scratch, with no Gaussian child. This is ordinary butterfly work
Ω(Vrf), not a sublinear supplier. The finite controls check this identity
against a separate tensor-entry formula and reject omitted axes/wrong phase.

## 5. Exact κ=1/200 budget relevance

Set t=199/200 exactly. For the selected complete invoice, rational 200th-root
enclosures certify

`−567.716011 < T_t−P_t < −567.716010`.

The 23 owned rises cost per native occurrence

`R_t = 10 + 4·2^t + 3^t + 6·4^t + 5^t + 6^t`.

There are 18 native occurrences. Granting all those rises for free, while
retaining every other target and paid job, gives the favorable relaxation

`434.821363 < T_t−P_t + 18R_t < 434.821364`.

This is why the shortcut matters to the moonshot: it would flip the binding
raw complex moment. The present theorem rules out funding that free-rank
relaxation by independent lower-rank implementations with sublinear
whole-field work. It does not rule out altered native trajectories,
jointly prepared/consumed correlations, longer-rest shared wires, new
productive outputs or a different recursive interface.

A positive raw complex moment would still not prove κ=1/200. Strictification,
finite compiler reserves, ordinary BIT above the required threshold, complete
source/owner/precision/tape application and all outer inequalities would
remain. The selected ordinary BIT .00385248 is below .005. This package
changes no complete conditional saving and discharges none of the five
global assumptions: `native_all_columns`, `owned_erasure`, `compiler`,
`precision_tape`, and `analytic_recovery`.

## 6. Prior work and remaining questions

- #6914, `owned-ascent-contract`, realizes the old #6902 23 rises at their
  paid ranks. It supplies no rank-minimality theorem. The selected application
  review transfers and pays those rises in #7000.
- Matarener's #5445, `owned-centre-wire-floor`, proves a nested retiming
  floor for the older #4470 centers. Here maps may be non-nested and the
  replacement has arbitrary monomial routing and branching, but only one
  data-dependent entrance. The two scopes are not interchangeable.
- #679, `selector-batching`, retains joined-volume and monomial-support
  warnings; no selector batching saving is claimed here.
- #5111's sparse approximation method is credited; its target is the
  inverse postdecoder, whereas this target is the complete owned Gaussian
  return and its paid-rank tradeoff.

The first constructive escape to investigate is a joint replacement that
receives already prepared correlated public/owned fields and consumes them
before their source versions change. It must name those actual versions,
return every required field, and charge their acquisition and restoration.
The single-input reachability proof deliberately does not rule it out.

Prepared for @CubeJerry with substantial OpenAI assistance. Canonical native,
helper, compiler and review authors retain their credit; no independent human
or formal-kernel acceptance is represented. Apache-2.0.
