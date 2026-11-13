# A standalone cyclic rail and its finite-multiplicity sharing theorem

**Exact finite source construction and conditional composition theorem. No new kappa.**
Prepared for @CubeJerry with OpenAI assistance. The native shared-wire source,
the H4 invoice, the E8 and cyclic-dual source constructions retain their credit.
The programme baseline is `cbc210ca0eb82c74a021b4f1b744e2e07e07e00b`.
Independent review is recorded separately; it must not be inferred from this
author's replay. This package continues the same current-row construction.

## 1. Precise source and domain

Let W be the pinned 71,261-operation native word on 1,480 public inputs,
including the 400 original main inputs and 1,080 arbitrary public helpers.
Its gzip SHA256 is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Let C be the pinned 78,011-operation cyclic partial lift on those inputs plus
400 private main inputs. Its gzip SHA256 is
`ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2`.
No other historical source is silently substituted.

The scalar identities here hold over Q, and hence componentwise on every
allowed positive whole-field volume under the retained chart semantics.
The standalone rail uses only dyadic coefficients and nonzero scalings +/-2,
so its rational identities also specialize to characteristic different from
two. This does not supply the separate characteristic-two BIT source or its
uniform compiler. The native W's own scalar and physical contracts remain.

Write u for all original common inputs, v for the private main inputs,
and q=v-u_main. Let E be W's main target operator under its retained endpoint
contract. The old cyclic private endpoint is E u_main + L q, where L is
incomplete: forward debt is 4,569 terms in its changed donor basis, or 4,920
in original coordinates; hosted reverse residual rank is 82. All eight
coupled reverse outputs and the previously completed forward outputs remain.
The statement below constructs L, not E.

## 2. Removing the common-history interface

Remove precisely the original native instructions, identified by C's frozen
native-event map, and the remaining scalar instructions touching a common
public role. Retain every other instruction in its literal order. Renumber
the 400 private fields to 0..399 and its 93 declared owned labels accordingly.
This gives a 4,748-operation standalone base rail. Every local read, location,
ownership predicate, initialization, retirement and nested MOVE is checked.

This deletion changes exactly six private final rows. They can all be repaired
from actual current first-X values already at Hub127:

| Original receiver role | Standalone destination | Final facet | Required actual Hub combination |
|---|---:|---:|---|
|116|107|131|q110/2|
|144|133|157|-q111/2|
|145|134|158|-q36/2|
|160|147|171|-q111/2|
|161|148|172|-q36/2|
|172|159|183|-(q37+(q47-q159))/4|

Here q47-q159 is the actual preconditioned donor row, not an unavailable
original q47. The standalone current fields realizing these combinations
are explicitly listed in PURE-RAIL-RESULT.json. Each repair initializes
one owned zero at the Hub, forms the indicated combination by actual ADDs,
moves it down to the destination facet for one rank-one call, adds it to
that receiver and clears it. Each lifetime ends before the next begins.
There are six new calls, not seven; the last packet carries one combination.

The six downward chart pairs do not occur in the frozen parent. Their exact
Clifford recipes, rank and global phase are independently compared with the
pinned signed-Pauli engine in CHART-MAPS.json. All other rail pairs inherit
the exact parent maps. A deliberately wrong global phase is rejected.

Two distinct coefficient checks establish the endpoint statement. First,
the old cyclic source and the new standalone rail are replayed on all 400
independent private q coordinates with the common coordinates zero. Their
entire 400-row private maps and final charts agree. Second, at the old cut
after q formation, mark every common input as possibly relevant and every q
as independent. Boolean dependency propagation leaves only six potentially
common-dependent private endpoints. Exact backward row propagation on each
proves that all 1,480 common derivatives vanish before final recoupling.
Every other private endpoint was already excluded by the conservative
dependency calculation. Thus equality for q with u=0 extends to arbitrary
independent (u,q); it is not an unproved zero-helper assumption.

Changing the sign of any one of the six repair contributions changes the
exact 400-input endpoint map. The zero-derivative check, complete comparisons,
locations and phase checks are separate from these mutation controls.

## 3. Exact standalone interface

The repaired Q has 4,779 operations: 3,226 ADD, 809 MOVE, 371 INIT,
371 CLEAR and two SCALE. All 371 lifetimes retire. The live owned peak is
29; 93 labels are declared, and unused labels are not extra live capacity.
Its paid MOVE profile is

    Qpaid = {1:177, 2:132, 3:96, 4:20, 5:199, 6:1, 7:4, 8:172, 9:8}.

It reads only its 400 arbitrary public inputs. Its initial charts match the
original main initial charts, its final charts match the original main final
charts, and it implements exactly L. This is a reusable, independent private
rail, with every common-history replacement included in its bill. It is
not an implementation of the full target E.

## 4. Universal fixed-m sharing theorem

For every fixed integer m>=2, suppose Q implements a linear map L on the
main domain with the initial/final chart interface above, and retires every
owned field. Then one execution of W and m-1 sequential executions of Q
implement

    common output = W u,
    private output j = E u_main + L(v_j-u_main),  1<=j<m.

Proof: while common main fields still equal their original inputs, perform
400 cocharted difference ADDs v_j<-v_j-u_main and run Q on bank j. Q neither
reads nor writes the common bank or any other private bank. Repeat for each
j. Then run W once, with its actual arbitrary helper inputs. Finally add
each matching common main output into each private output by 400 real
cocharted ADDs. Linearity gives the displayed formula. These are genuine
source operations; there is no abstract decoder or uncharged intermediate
return. Owned labels may be reused because each Q has already retired all
its owned fields before the next Q or W starts.

If L=E, every private output equals E v_j, so the main target is replicated
m times while the helper target is realized and credited once. If L differs
from E, the error is exactly (L-E)(v_j-u_main) in each private bank. Increasing
m does not cancel it. Every remaining endpoint obligation survives.

For a Q with a operations, h lifetimes and peak p, the actual source word
has 71,261+(m-1)(a+800) operations, 54+(m-1)h lifetimes, and peak max(43,p).
This is a literal scalar/lifetime count, not a complete physical tape bill.
Public storage is 1,480+400(m-1). Addressing, setup, precision, retained
records, allocation and erasure must be compiled for that fixed source.
The theorem permits fixed m; it grants no growing m(n) schedule.

The emitted m=2 word has 76,840 operations on 1,880 independent inputs,
425 lifetimes and peak43. The m=3 word has 82,419 operations on 2,280
independent inputs, 796 lifetimes and peak43. Their complete exact replays
agree with the separately composed formula on every coordinate. Their
full ordinary and MOVE profiles are in the respective RESULT.json files.

## 5. Full conditional caller moment and finite ceiling

Let T,P be the complete selected caller profiles, H the per-native helper
target profile, N the whole native paid profile, R the old main raw profile,
and G=N-R. All are pinned by FULL-RESULT.json, SHA256
`d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.
All ordinary outer/main/QUERY/IDLE/LAMBDA terms are duplicated m times;
only one common native is shared. For a complete Q, the conditional profiles
are exactly

    T_m = m T - 18(m-1)H,
    P_m = m P - 18(m-1)G + 18(m-1)(Qpaid-R)
        = m(P-18N) + 18N + 18(m-1)Qpaid.

The same formal invoice is a remaining allowance for an incomplete Q, with
all missing endpoint and physical work still owed. In particular, m copies
do not retain m copies of the shared helper target credit. Omitting the H
term is an explicit overcredit control in the arithmetic checker.

For t=199/200 define M0=sum_r(T_r-P_r)r^t, d=-M0/18>0,
g=sum_r(G_r-H_r)r^t and c=sum_r(Qpaid_r-R_r)r^t. Then

    (T_m-P_m)_t / (18(m-1)) = (g-d)-d/(m-1)-c.

Exact integer 200th-root enclosures give

    d = 31.5397783670854135...,
    A_infinity = g-d = 129.9388553172829489...,
    A_m = A_infinity-d/(m-1).

These are rigorous bounded quantities; decimals are explanatory. For this
invoice, a finite m with strict positive moment exists if and only if
c<A_infinity. When so, the exact condition is
m-1>d/(A_infinity-c), and the least integer m is
floor(d/(A_infinity-c))+2. Equality at the limiting ceiling is insufficient
for every finite m. This is necessary and sufficient for this moment test,
not for source construction or supplier admission.

|m|Allowed extra moment c, strictly below|Remaining allowance for current Q|
|---:|---:|---:|
|2|98.3990769501975...|25.5565619013565...|
|3|114.1689661337402...|41.3264510848992...|
|4|119.4255958615878...|46.5830808127468...|
|8|125.4331726934136...|52.5906576445726...|
|limit|129.9388553172829...|57.0963402684419...|

The current Q's c is72.8425150488410..., including its six repairs. A later
actual consumer must be added to Q and its whole profile recomputed. Prior
two-copy obstructions keep their stated scopes; a larger invoice neither
invalidates their proofs nor constructs an interface they excluded.

## 6. Reproduction, limits and next construction

Run, without Python -O (the rational replay explicitly rejects it):

    python -I -B extract_rail.py --repo REPO --output OUT
    python -I -B complete_extraction.py --repo REPO --output OUT
    python -I -B check_rail_charts.py --repo REPO --output OUT
    python -I -B check_budget.py --repo REPO --output OUT
    python -I -B build_mcopy.py --repo REPO --rail OUT --copies 2 --output OUT/m2
    python -I -B build_mcopy.py --repo REPO --rail OUT --copies 3 --output OUT/m3

Neither emitted lift is a complete native, a uniform complex supplier, a
covered or ordinary BIT supplier, or a complete multiplication theorem.
The outer target still needs compatible strict U>.005 and B>.005. All five
foundations remain: native_all_columns, owned_erasure, compiler,
precision_tape and analytic_recovery. The next construction must complete
the current forward and reverse maps within the finite allowance above,
or replace Q with a stronger source-valid interface and recompute its bill.
