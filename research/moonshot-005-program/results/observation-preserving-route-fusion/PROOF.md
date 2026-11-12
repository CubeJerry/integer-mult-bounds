# Preserve every actual observation while shortening private transport

**Exact finite-word construction under the retained chart-transport contracts.
No complete supplier and no new kappa.**

The previously admitted unit17 word restores all 1,480 common outputs and
performs 17 of the 208 required private cross dependencies on 1,880 independent
inputs. Its raw carriers copied all 1,710 original main MOVEs even when nobody
read a carrier at the intermediate stops. This construction removes precisely
those unused stops, retaining every actual scalar use and every recorded value.

## 1. The rewrite and its universal correctness

Fix a private public carrier a in a well-typed finite word. Consider a maximal
sequence of its MOVEs

    U0 -> U1 -> ... -> Um,

with strictly nested spaces U0 < U1 < ... < Um, such that no non-MOVE instruction
between the first and last MOVE reads, writes, scales, copies, allocates or
retires a. Instructions on other carriers may be interleaved. Replace the
whole sequence by one MOVE U0 -> Um at the last old MOVE position.

Every intervening instruction is independent of a. Thus its value, physical
chart tests and ownership state are unchanged. The raw carrier stays at U0
until the final replacement, then reaches Um. At every non-MOVE instruction
that actually touches a, its location and logical payload agree with the old
execution. This proves preservation by induction, simultaneously for every
independent input and every admitted complete field volume V. Different raw
carriers can be rewritten together because any instruction touching either
carrier ends that carrier's segment.

This argument uses the source's actual chart-transport convention: in logical
coordinates MOVE c -> d carries the same field from representation C_c to
representation C_d. Physical transports compose as
C_d C_c^{-1}. Hence the nested chain and the direct transport both represent
C_Um C_U0^{-1}. The direct rank is dim(Um)-dim(U0), and its complete recursive
call, scalar normalization and layout services remain subject to the native,
compiler and precision foundations. This is not an assumption that an arbitrary
physical network transmission can be shortened without changing its interface.
Every emitted rank-eight transport is a proper nested source-frame call in the
same ambient chart model.

For 0 < t <= 1, write r_i=dim(U_i)-dim(U_(i-1)). Concavity/subadditivity gives

    (sum_i r_i)^t <= sum_i r_i^t.

The direct replacement therefore has no larger Gaussian t-moment, while its
total rank is exactly unchanged. Within the old monotone route and the exact
set of retained non-MOVE access occurrences, deleting every unused intermediate
stop attains the least moment among route subsequences. This does not optimize
over different scalar computations, changed access sets or networks mixing
several fields.

No source reservation is duplicated. Removed raw calls are absent from the new
paid profile. Their old intermediate stops are likewise absent from the new
access contract. A later controller that needs one of those stops must restore
that visit, or exhibit and price another route. The old side-information graph
is not automatically available to the rewritten word.

## 2. Actual frozen construction

Native source compressed SHA256:
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

Parent unit17 word compressed SHA256:
`c75f595393d32f0ddefed906e9dab02e6e09b764730684541375d6979c6c349c`.

The builder identifies the 400 raw carriers, computes their actual read/write
barriers from the entire parent word, verifies every original raw MOVE is a
strict upward nesting, and emits the fused segments. The new word retains a
complete parent-event map and the exact parent MOVE list of every replacement.
The original common native subsequence and all non-MOVE instructions are
unchanged. No historical read is dropped or retimed.

| Quantity | Admitted parent | Rewritten word |
|---|---:|---:|
| All instructions | 80,774 | 79,469 |
| Common MOVEs | 6,310 | 6,310 |
| Raw MOVEs | 1,710 | 405 |
| Extra owned rank-one packet MOVEs | 17 | 17 |
| Total MOVEs | 8,037 | 6,732 |
| Raw rank sum | 3,200 | 3,200 |
| ADD | 68,642 | 68,642 |
| SCALE | 3,662 | 3,662 |
| COPY | 1 | 1 |
| INIT / CLEAR | 216 / 216 | 216 / 216 |
| Peak owned fields | 121 | 121 |

The exact raw histograms are

    R_old = {1:990, 2:360, 3:105, 4:112, 5:133, 6:8, 7:2},
    R_new = {1:3, 2:1, 3:2, 5:1, 8:398}.

The output contract is unchanged: every common field equals the original native
map; the 17 declared ordinary private Y fields equal vY+vX; the other 383 private
input values are unchanged; every public field is at its required final chart;
all owned lifetimes close. The construction does not complete the remaining
191 cross dependencies. In particular, shortening an identity carrier is not
a proof that its still-missing native operation has been implemented.

The root replay uses the inherited S006 author interpreter on all 1,880 formal
input directions and checks every final row and chart. It is explicitly labelled
as an integration replay, not a new independent review. A separate review of
the frozen rewrite and its proof is required before admission.

## 3. Exact changed invoice

At t=199/200 the per-native saved moment is

    Delta = sum_r (R_old[r]-R_new[r]) r^t
          = 19.8083625716245272... .

RESULT.json encloses it with integer 200th-root brackets; the displayed decimal
is only explanatory. This is an actual reduction of emitted recursive calls,
not a relabeling of funded work or an erasure credit.

Keeping the H4 outer target T4 and all other caller contributions fixed, the
rewritten partial word has the explicit provisional paid histogram

    P_partial = P4 + 18(R_new-R_old) + 18*17*{rank1}.

It has 27,344 target positions, 129,240 paid positions and rank surplus 4,750.
Its remaining moment per native is exactly

    H_partial = H4 + Delta - 17
              = 101.20743952182206... .

The 17 newly paid packet calls are included. Thus the actual partial word has
smaller Gaussian moment than the older blank H4 route ledger by Delta-17,
approximately 2.80836 per native. This statement compares paid profiles; the old
blank ledger was not a completed algorithm, and neither is the rewritten word.
The entire remaining 191-dependency construction, scalar and history services,
precision, compiler, ownership, compatible BIT/complex suppliers and recursive
outer costs remain to be established. Positive provisional margin establishes
none of them by itself.

All non-MOVE instruction counts and scalar coefficients are unchanged. In
particular, the parent's unresolved non-dyadic scalar services and peak-121
owned storage remain real obligations. Paid ranks and the number of route calls
change, so an eventual physical compiler invoice must be regenerated from the
emitted word, including its actual rank-eight calls.

## 4. Consequence for the next construction

The price of a raw route should be tied to its actual required observation and
control stops. A source route with many unused intermediate charts is not an
unavoidable paid cost. Conversely, the cheapest endpoint route does not grant
the missing source's entire access history.

The next mechanism can choose a few useful nested control/decoder stops, build
its real cochart word, and apply this same exact rewrite around those stops.
This offers more budget than the frozen 1,710-call calendar, without weakening
any field-input, endpoint, observation or ownership contract. It does not
invalidate earlier exclusions within that frozen calendar.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the original
native, H4 invoice, S006 unit17 precompensation construction and its independent
review. All five foundational assumptions are retained. No new kappa.
