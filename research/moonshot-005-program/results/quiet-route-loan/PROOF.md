# A seven-ADD funded-route loan, with its exact limitation

**Proved source-bound linear routing primitive. No saved Gaussian price, full
second native action, complete supplier, or new κ is claimed.** The construction
allows actual helper and main payloads to differ temporarily from their virtual
source values, while preserving every common-source read and the common output.
The explicit raw-input example is replaceable by one earlier cochart ADD. That
limitation is part of this result, not an omitted optimization.

## 1. The quiet exchange lemma

Let H be a physical helper at chart S and Q a second-main carrier at the same
chart, containing arbitrary complete fields h and q. Suppose an already funded
helper route takes H to T now, and an already funded main itinerary takes Q to T
later. Until that later arrival H has no source read, write, MOVE or lifecycle
operation, and Q has no code operation except its declared main MOVEs. Suppose a
receiver R is cochart with H at some time between the two arrivals. The
physical holders H, Q and R are pairwise distinct, and R performs this added
shear only at a declared cochart contact.

Use the three scalar additions

    H += Q;  Q -= H;  H += Q.

The values are now H=q and Q=−h. Let H take its original route. At a cochart
receiver contact perform `R += H`. Q carries −h along its original funded main
itinerary. Upon Q's arrival at T, use

    H -= Q;  Q += H;  H -= Q.

The resulting values are exactly H=h, Q=q and R=r+q. These identities hold for
arbitrary h, q, r in every admitted complete-field dimension. No zero-helper
premise or dirty-input cancellation is hidden. Both exchanges are invertible
signed swaps, and the receiver update is an invertible elementary shear.

There are exactly seven additional ADD instructions, each with coefficient ±1.
There is no extra MOVE, INIT, CLEAR, owner or lifetime. All seven operations
require actual cochart holders; the two existing route payloads are explicitly
changed. The quiet-window premise makes the temporary common-helper change
unobservable to source instructions. It is restored before the next source use.
The positive scalar, tape and precision tariffs still belong in a complete
invoice. This is an exact linear statement, not a rounding-error theorem.

## 2. Exact source instance

The immutable source is `research/shared-wire-split-composition/data/final.json.gz`,
SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Use its exact main partition of 400 roles. Execute one full reference source
on all 1,480 arbitrary entering public values. Add a second public carrier q_r
for each main input, initially the independent second-main input minus the
corresponding first-main input. These 400 conversions cost 400 ADDs. Let each
carrier follow its corresponding source main MOVE itinerary, but do not apply
the source scalar instructions to these raw carriers.

The specific roles and times are:

| Item | Exact source event or chart |
|---|---|
| Helper H | role449, in chart3 immediately before event28048 |
| Donor Q | raw difference carrier for main907, also in chart3 |
| Funded helper route | event28048: role449, chart3→chart594 |
| Receiver R | raw difference carrier for main977, in chart594 since event27514 |
| Receiver departure | event30320: main977 leaves chart594 |
| Funded donor return | event30653: main907, chart3→chart594 |
| Next helper source use | event30837: role449 receives an ADD |

The source contains no instruction touching helper449 after its event28048 MOVE
and before event30837. The helper is thus quiet throughout the exchange. The
actual common main907 has scalar source updates in this interval, but those use
its first-copy public holder, not the independent second-main carrier. Confusing
these two holders would invalidate the construction.

Emit the first signed swap immediately before event28048, the receiver ADD just
after the helper route, and the inverse swap after the funded second-main MOVE
at event30653. Retain every original first-copy source instruction. No source
owned field is repurposed; its labels are merely shifted by 400 to avoid the
new public carrier names.

## 3. Complete literal word and exact outcome

The emitted word has 73,378 typed instructions. It includes the entire 71,261
source instructions, 1,710 funded second-main MOVEs, 400 input conversions and
seven loan ADDs. Exact replay uses all 1,880 independent entering input columns.
At the end every reference first-copy role is exactly the original source row
in the original source chart. All original owned fields are retired as before.
The difference-carrier endpoint map is exactly

    q977 ← q977 + q907,

with every other q_r unchanged. This is one invertible coded basis change. It is
not the required second native action WΔ, and it does not provide all original
input differences as individual current cochart fields after the shear.

| Operation or resource | Exact physical value |
|---|---:|
| ADD | 61,587 |
| COPY | 1 |
| SCALE | 3,662 |
| MOVE | 8,020 |
| INIT / CLEAR | 54 / 54 |
| Peak owned fields | 43 |
| Extra owned fields or lifetimes | 0 |
| Added Gaussian MOVEs beyond the funded second-main itineraries | 0 |

The original owned-MOVE histogram remains
`{1:20, 2:9, 3:2, 4:13, 5:2, 6:1}`. Thus the local primitive incurs no new
Gaussian jobs. This says nothing about the jobs needed to complete WΔ.

The temporary main907 carrier transports an arbitrary dirty common helper
value rather than its literal virtual main difference. During the loan the
current common helper need not be decodable at its virtual chart; only its
next read and final output must be correct. Consequently a theorem requiring
literal main-MOVE payloads, or every current common helper to remain available,
cannot be applied without checking those extra premises. The separate checker
`borrowed_common_check.py` proves actual unavailability just after the first
loan leg: the entering dirty helper1477 coordinate is 1 in the desired common449
row and 0 in every current physical row at chart594. That dirty information
is retained with coefficient −1 in donor carrier1806 at chart3 until return.

## 4. Why the explicit raw shear is not a target saving

Both q907 and q977 start in chart3. Their final raw shear can therefore be
implemented by the single ADD `q977 += q907` at the input, before either carrier
moves. The seven-ADD loan demonstrates a legal physical coding mechanism; this
particular transfer is not an indispensable spatial delivery and is not charged
as a saving over an optimal raw-input implementation.

`raw_contact_audit.py` independently enumerates the complete single-MOVE quiet
loan family from the source's main visit intervals and next-helper-use times.
A candidate is a non-main role moving S→T, a main donor currently in S that
arrives at T before the next helper touch, and a main receiver visiting T between
those times. The exact source has 354 such helper/donor windows and 35,921
eligible receiver contacts.

In 35,860 contacts the receiver is still at T when the donor arrives, so the
individual raw shear can instead be made directly then. The remaining 61
contacts have a receiver departure before donor return. Every one leaves the
empty chart3, and both raw donor and receiver inputs were already cochart there
at entry. Those shears can instead be made directly at entry. Each critical
case is preserved in the audit receipt; the complete deterministic witness
list is also digest-bound and reconstructed by the script. There is no funded
MOVE into chart3 anywhere in this source. Under these fixed routes and cochart
linear operations, a current zero-chart value can therefore depend only on
inputs that were already in the zero chart at entry; this follows by induction
over scalar operations, INIT and departures. A fresh independent nonzero-chart
input would require a changed route or an added charged arrival.

This is a scoped redundancy statement for individual raw-carrier shears and
this exact fixed single-MOVE quiet-window family. It does not authorize
commuting an entire interdependent coded circuit. If a donor gains a new row z
after an early contact, then an early update r←r+q differs from a later desired
update r←r+q+z. That exact algebraic counterexample is a control in the audit.
Read-active helpers, several-route loans, changed funded routes, newly arriving
coded information and full endpoint factorizations remain separate obligations.

## 5. Verification and scientific status

`build_and_verify.py` emits the complete typed word and replays it exactly on all
1,880 input columns, including arbitrary shared dirty helper inputs. It checks
live cochart ADD/COPY operands, nonzero scales, COPY-zero identities, literal
ownership flags and nested transport, exact final reference rows and the exact
400 difference-carrier output rows. It compares complete move/lifecycle bills
with the reference source. Wrong restoration sign, wrong receiver chart and a
public carrier marked owned are rejected negative controls.

The elementary signed-swap proof and the independently checked source-window
facts establish the stated finite source-bound primitive. The complete supplier
endpoint, uniform compilation, precision budget, recursive invoice and original
five foundational assumptions remain unresolved or inherited. No complete κ
improvement follows. The next useful extension must provide a needed coded row
that is unavailable at the replaceable earlier/later raw contact, while retaining
all dirty common payloads and charging every introduced operation.

Prepared for @CubeJerry by workers B and C of the persistent programme, with
substantial OpenAI assistance and retained source/predecessor credit.
