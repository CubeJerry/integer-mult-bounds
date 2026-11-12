# Preterminal completion of the eight coupled reverse endpoints

**Proved finite source construction, independently reviewed. No new κ.**
Prepared for @CubeJerry with substantial OpenAI assistance. Preserve the source,
E8-prefix, conditional reverse-eight, reciprocal-encoder and paired-cohort credit.

This construction replaces a dependency on already-correct forward endpoints by
an initial change of variables. Its recursive cost is still eight rank-one
messages. It does not claim a cheaper price than the earlier terminal macro.
It gives an actual word in which all eight coupled reverse outputs are correct
while the first-family forward code is still incomplete.

## 1. Exact algebra and entry contract

Let F be a field of characteristic different from two and let V be any positive
integer. All formulas apply componentwise to arbitrary vectors in F^V. A coupled
port has independent input differences x,y and desired outputs

    X_out = x-y,           Y_out = (x+y)/2.

The programme's forward endpoint interface instead preserves its input donor a
and, when its off-diagonal residual is removed, produces (a+b)/2. Apply the
invertible input map

    a = x-y,              b = 2y.

Its determinant is 2 and its inverse is y=b/2, x=a+b/2. The forward interface then
gives X_out=a=x-y and Y_out=(a+b)/2=(x+y)/2. The reverse endpoint is already
correct before any forward decoding. No second physical X bank is assigned to
the coupled coordinate.

For a simultaneous code, write x in F^104 for first-X inputs, y for first-Y
inputs, U for the eight coupled indices, and D_U for coordinate insertion.
Let C be diagonal with entries 1/2 on U and 1 elsewhere. Suppose a partial
forward word has the exact postcondition

    X = a,
    Y = C(b+a) + H a,

with H an explicitly known residual matrix. Other private inputs, common
inputs and retained observations may exist; the word must be correct on all of
them. Under

    a = x-D_U y_U,         b_H = y_H,         b_U = 2y_U,

the entire postcondition is

    X_U = x_U-y_U,         X_H = x_H,
    Y = C(y+x) + H(x-D_U y_U).

The original residual matrix has not disappeared. It acts on the changed donor
variables. In original input coordinates it has the additional columns -H D_U.
Any future aggregate acquisition must use the actual current a values; it may
not silently substitute the old x values. A row of H that was zero stays zero,
so every previously complete forward receiver remains complete.

This is a precomposition identity for an arbitrary partial word. It does not
require a diagonal or reciprocal full code, and it does not assert that all
other reverse duties have been solved. The existing hosted X2/Y2 data are
unchanged by this input substitution.

## 2. Literal source realization

The frozen source is `research/shared-wire-split-composition/data/final.json.gz`,
SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The exact parent is the admitted paired word
`results/paired-cohort/output/WORD.json.gz`, compressed SHA256
`bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17`,
with decompressed canonical payload SHA256
`bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a`.

The coupled source X roles are 17,19,30,38,40,47,52,60; their Y roles are X+112.
Each Y starts at empty chart3. The X initial lines are respectively
16,18,28,35,36,43,48,56. These are eight distinct one-dimensional subspaces.
After the parent's 400 authentic difference-formation ADDs, and before any
other operation, perform for each coupled role:

    INIT z at chart3
    z += q_Y at chart3
    MOVE z from chart3 to the actual X initial line (owned, rank1)
    q_X -= z at that line
    CLEAR z at that line

The same declared owned label1880 is reused sequentially. No owned field is
live at this entry boundary. The exact chart maps are lowered and checked by
the two retained source-pinned Clifford/signed-Pauli/global-phase engines.

Logically b_U=2q_Y is then supplied to the parent word. In the literal word,
the first parent use of each coupled Y is its SCALE by1/2, at parent clocks
3632 through3639. There is no earlier read or write of that Y. The initial
doubling therefore commutes past every intervening instruction and cancels
this first half-scale. The new word simply omits those eight SCALE instructions.
It neither reads an already-modified Y nor relies on a zero common input.

## 3. Full source composition, restoration and information

At the common-source entry, an independent-in-implementation sparse rational
interpreter checks every live field against the parent prefix under the exact
substitution on all1880 original coordinates

    v_X -> v_X-v_Y+u_Y,       v_Y -> 2v_Y-u_Y,

for the eight coupled pairs; every common coordinate and every other private
coordinate is fixed. This is the actual input change q_X->q_X-q_Y,
q_Y->2q_Y expressed before difference formation. All owned records live at the
boundary are included in the comparison. The parent common suffix is retained
byte-for-byte as an instruction list, with all physical source charts unchanged.

The common suffix therefore gives exactly the parent full map after this
invertible input change. The parent's all-input common-restoration result
applies; no common mode is dropped. Its explicit information inverse composes
with the displayed inverse of the preconditioner, so all1880 input dimensions
survive. A repeated execution of the parent's checker is not claimed as a new
independent mathematical review.

All eight coupled raw X fields equal q_X-q_Y at common entry. The exact parent
postcondition, now precomposed, keeps this raw value until the final common
recoupling; it gives the required second-native coupled X endpoint. Earlier
marks meaning “original donors restored” now mean the preconditioned originals
a. The obsolete mark is renamed and its semantics recorded in the literal word.

The eight previously complete forward receivers are still complete. The inherited
forward residual has4601 nonzero coefficients in the104-dimensional a basis.
It has4952 nonzero coefficients in the original400-difference input basis,
because351 nonzero coupled-column coefficients gain matching Y columns.
Both counts are reported explicitly. The96 hosted reverse residual remains
the same rank96 matrix I+R; no hosted reverse diagonal is completed here.

## 4. Complete incremental invoice

The emitted word has77,827 instructions, compared with the parent's77,795.
Its exact ordinary increment is

| Instruction | Increment |
| --- | ---: |
| ADD |16|
| MOVE |8, all rank1 owned|
| INIT |8|
| CLEAR |8|
| SCALE |-8|
| COPY |0|

All703 raw MOVEs and their histogram are unchanged. The new total word has
7,029 MOVEs,423 owned lifetimes and peak43 owned fields. The preload standalone
peak is one; the source word's larger peak remains43. No extra declared owner
label is needed because label1880 is dead at the insertion point. Its physical
allocation/reinitialization/erasure services remain in the eventual compiler
contract; the table is not an unbounded bit-cost tariff.

With the parent's complete provisional target histogram T4 and paid histogram
P_parent, and18 native repetitions, the changed invoice is exactly

    T_new = T4,             P_new = P_parent + 18*8 {rank1}.

The eight rank-nine E8 packets remain charged. The new caller has134586 paid
positions,27344 targets and rank surplus3616. At t=199/200 its remaining
moment per native lies in the directed rational interval

    [148577077691204038653214911433549,
     148577077691204038653214911450761] / 4500000000000000000000000000000,

approximately33.0171283758231197. This subtracts exactly8 from the parent
41.0171283758231197 allowance. Positive residual moment does not admit a
uniform supplier, price all ordinary work, or complete a new multiplication
bound. Every retained foundation and both strict complex/BIT suppliers remain.

## 5. Sharp scope of the eight-arrival entry cost

Consider the restricted entry interface in which the common native has not
started, every original X carrier remains at its distinct initial line, every
Y starts at chart3, no preexisting message contains a Y difference at an X line,
and the preconditioner must leave q_X-q_Y at each of the eight X lines. All
other raw movement is held fixed until after this entry interface. Arbitrary
linear message coding, free local scalar operations and immutable local caches
are allowed.

At each target line its demanded Y coordinate is independent of all initial
local data. Without an incoming message carrying a nonzero coefficient on that
coordinate, every obtainable local row has zero coefficient there. Thus each
of the eight different target lines requires at least one positive-rank field
arrival. Each such arrival costs at least1 at every0<t<=1. The literal entry
word attains eight rank-one arrivals, so eight is the exact minimum in this
entry class. This is not a lower bound on arbitrary later coupled completion,
shared native processing, moved raw carriers or globally changed coding.

## 6. What the construction changes

The eight coupled coordinates can now remain arbitrary primal donors without
also representing a second reverse X bank: their reverse duty is already paid
and complete. This removes the need to demand the impossible literal alias
condition at those coordinates in a future independently represented reverse
code. It does not magically extend a96-carrier reverse code to104 carriers.
An arbitrary full M/M^{-T} implementation still needs either a legitimate
rectangular reverse compiler, explicitly paid auxiliary dual carriers, or a
different current-observation representation.

The companion `NULL-PADDED-ADJOINT.md` proves a sufficient fully charged local
compiler and gives its exact information-capacity gate. Physical global
composition remains the next obligation. All future routes must use current
rows and include the costs of any auxiliary carriers they actually move.

## Verification and open next questions

Run `build_preterminal.py --repo REPO --output OUT`, then `check_charts.py`
with the same arguments. The first recreates the word, exact1880-column prefix
composition, all-source typing, invoice, inverse identities and negative controls.
The second checks all eight source chart maps and rejects a changed global phase.
Sign, wrong target chart, missing actual movement and an uncancelled half-scale
are negative controls. Independent review is required before programme admission.

The concrete next task is a global hosted reverse code on the96 genuine reverse
carriers, with the coupled first-X coordinates treated as primal-only inputs.
Try a mixed block only when its dual auxiliary route price fits the complete
33.0171283758231197 remaining allowance, or supply a smaller quotient compiler.
No new κ and no foundational assumption are claimed discharged.
