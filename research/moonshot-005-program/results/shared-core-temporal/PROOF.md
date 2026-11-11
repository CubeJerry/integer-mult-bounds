# Fixed-channel obstruction and temporal coding interface

Status: proved scoped linear-circuit results with exact source witness. No new kappa. No H4 native.

Source: canonical e54523517d0f03e58352e647c403a5af3e525a57, research/shared-wire-split-composition/data/final.json.gz, SHA256 2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883. This continues the unbuilt H4 route in recovery review 8bfc4e67292c6dfaf6bb1bf2037c8a7649507a75.

## Fixed-channel class

Work over Q or C in normalized chart coordinates. A finite linear word W has main fields M, arbitrary public helpers H, and zero-initialized owned fields O. Its main endpoint is an invertible E independent of helper inputs. The selected word has 400 mains (live, live+112, hosted.X2, hosted.Y2) and 1080 helpers.

Duplicate every main field with identical charts. Duplicate every main-only ADD and nonzero SCALE; pay each main MOVE separately. Retain one shared auxiliary core. Every main-to-core read uses the same nonzero row a=(a0,a1) on the copy pair. Core writes to mains may have arbitrary time-dependent broadcast weights. All auxiliary operations are homogeneous linear maps or zero INIT/CLEAR. Any gather/broadcast macro is expanded fully before the source word advances; all its positive scalar work is retained. No extra internal main-only operation is allowed. This class does not include temporally changing read rows or a new native itinerary.

Let R be the main-only skeleton, deleting scalar operations with an auxiliary operand while retaining main scalar operations and separately paid main MOVEs. Normalized MOVEs preserve rows. R is invertible because the selected skeleton has only ADDs and nonzero SCALEs, no main COPY, INIT or CLEAR.

## Kernel invariant

For nonzero v in ker(a), initialize each main pair as v*z_r and all auxiliaries as zero. Inductively all auxiliaries stay zero and every main pair equals v times its skeleton state: copied main operations preserve the form; both copies undergo the same chart map; every core read is a(v*z)=0; homogeneous auxiliary work preserves zero. Thus the final main state is v*Rz. A two-copy E endpoint is impossible if E differs from R. Zero helpers are legitimate arbitrary-helper inputs. The induction holds at every positive column multiplicity conditional on the stated chart maps.

## Boundary wrappers cannot repair the selected source

Exact source replay gives the complete main entry cohort {1,773} and exit cohort {112,882}, using equality of binary frame subspaces. These are X on port1 and Y on distinct port0. With those orders:

    R[{112,882},{1,773}] = [[-1/2,0],[0,0]],
    E[{112,882},{1,773}] = [[0,0],[0,0]].

The fixed-channel lift has a nonzero block between these doubled cohorts: its restriction to the kernel mode contains v times this rank-one block. Any invertible main-only entry/exit wrapper mixing only common-frame fields acts block-diagonally on complete frame cohorts. Invertible left/right cohort factors cannot turn a nonzero block into zero, whereas the required doubled E block is zero. This excludes arbitrary such boundary wrappers, beyond the per-port swaps of the recovered proposal.

No helper-dependent boundary encoding or new cross-chart operation is covered. The negative control role112 += role1/2 cancels the single normalized witness but is an illegal ordinary final ADD: role112 exits at a rank8 complement chart and role1 at rank9.

## One canonical temporal exchange also fails

The balanced lift uses active s=m0+m1 and silent d=m0-m1. Main-to-core reads use s and core writes are divided equally between copies. Active s plus auxiliaries follows W; silent d follows R. Insert one internal global exchange s<->d at an arbitrary source cut, leave auxiliaries unchanged, and exchange the output mode labels back. There are no additional coding changes.

Let prefix main/auxiliary responses to zero-helper input x be P*x and C*x, suffix main response be A*m+B*z, and skeleton prefix/suffix be K,L. Original correctness gives AP+BC=E and R=LK. After the exchange, outputs in original mode labels are LP*x and AK*y+BC*x. Independent E outputs require LP=E, AK=E, BC=0. Hence AP=E. Since E,K,L are invertible,

    E = AP = E K^(-1) L^(-1) E,

so E=LK=R, contradicted by the source witness. This excludes every single cut even while ignoring auxiliary restoration. It does not exclude multiple exchanges, arbitrary extra boundary matrices, or general time-dependent contact rows.

## Constructive temporal coding interface and complete budget boundary

For any linear chart operator U and any scalar 2-by-2 matrix C,

    (C tensor I)(I_2 tensor U) = (I_2 tensor U)(C tensor I).

Thus at any cut after a complete expanded source event the cloned main fields remain cochart. An invertible copy-code change is a legal ordinary operation, adds no Gaussian child, and changes no helper credit. Both original main MOVEs remain separately paid. The identity holds for every positive column multiplicity, conditional on the original chart provider.

Negating the second copy exchanges s and d. A global switch on all selected mains is exactly 400 SCALE(-1) events. A signed swap (u,v)->(v,-u) is u+=v; v-=u; u+=v, exactly 1200 ADDs globally, no scratch. Two internal global sign switches require 800 SCALEs/native, or14400 across the18-call caller. An even number returns the original mode labeling. Physical scalar/source/movement/rounding expenses remain positive and must be re-counted; no old tariff is assumed.

The recovered optimistic H4 raw margin at t=199/200 is between1771.183385 and1771.183386. Pure scalar switches leave that hypothetical T4/P4 invoice unchanged. If every other term stays fixed, a corrective paid profile above ideal H4 must have per-native t-moment below M4/18, about98.39907695. Equivalently it must save more than13.012927833 from the duplicated-owned-bank baseline111.412004783. The latter is a required saving, not an allowed total correction price. No actual native satisfying this invoice has been constructed.

## Next construction and limitations

The initial two-cut attempt is excluded by the theorem below. Find at least three global source cuts, or a small collection of role-local cuts, and legal cochart code changes whose temporal lift has two independent selected main endpoints (including both copies of all8 coupled type-B blocks), returns all1080 arbitrary helper inputs autonomously, respects all owned lifetimes, and has a completely counted corrective paid profile within the stated budget. Then recount physical constants, precision and compiler closure. No successful multi-switch word is asserted to exist.

Run python3 -B verify.py inside the repository, or pass --source PATH. Optimized mode is supported with explicit exceptions. Tests bind the immutable source, full chart chronology, complete boundary cohorts, exact full-native and skeleton blocks, forbidden correction control,49 signed-swap cases and a transport-commutation example. Written proofs establish universal statements; tests establish only their stated source facts.

Credit DreamingOfClouds' shared-native and odd-word lineage, Ali Romman's helper splitting, @CubeJerry's selected composition/recovery, and all retained source notices. Kernel/rank and tensor commutation principles are elementary; the scoped contribution is their application to the selected H4 route, one-exchange exclusion and temporal construction obligation. Prepared for @CubeJerry with substantial OpenAI assistance. All five global assumptions remain; model review is not human or proof-kernel acceptance.

## Two-switch rank theorem

Split the source into three segments, with active main/auxiliary blocks (A_j,B_j;C_j,D_j) and invertible skeleton blocks K_j. Exchange active/silent modes between segments1/2 and2/3. For zero-helper inputs x,y, final main outputs are

    active = (A3 K2 A1 + B3 D2 C1)x + B3 C2 K1 y,
    silent = K3 B2 C1 x + K3 A2 K1 y.

Independent E outputs imply B2 C1=B3 C2=0, K3 A2 K1=E, and A3 K2 A1+B3 D2 C1=E. The original endpoint is

    E=A3 A2 A1+A3 B2 C1+B3 C2 A1+B3 D2 C1.

Subtracting gives A3(A2-K2)A1=0. Since R=K3 K2 K1,

    rank(E-R)=rank(A2-K2)<=nullity(A1)+nullity(A3).

The last step is rank(LXR)>=rank(X)-nullity(L)-nullity(R) for square matrices. Prefix/suffix main blocks need not be invertible. This is a necessary condition for successful two-switch decoding, even ignoring helper restoration.

## Exact exclusion of every two-switch cut pair

The selected source has rank(E-R)>=275 over Q, witnessed by rank275 modulo prime1000003. The portable certificate computes exact modular prefix/suffix main-block ranks at52 source cuts. Every encountered rational denominator is invertible modulo that prime.

A prefix main-block rank changes only at an auxiliary-to-main ADD; a suffix main-block rank changes only at a main-to-auxiliary ADD. Each changes one row and alters rank by at most1. Main-only ADDs/nonzero SCALEs preserve rank, other events leave the corresponding block unchanged. COPY is interpreted as literal ADD on its required zero target. Its only occurrence31737 immediately follows INIT of the same owner1504; main-only switches preserve zero. Changed histories outside this class must separately establish this premise.

If d relevant events separate sampled ranks rL,rR, all intermediate ranks are at least ceil((rL+rR-d)/2): after j relevant events use max(rL-j,rR-(d-j)). No monotonicity is assumed. The52-sample certificate gives prefix/suffix rank>=270 at all71262 event boundaries. Thus every cut pair has nullity(A1)+nullity(A3)<=260<275. All canonical zero-, one-, and two-switch lifts are excluded for this frozen scalar chronology. This is an all-cut finite-source proof, not an inference from trying selected pairs.

The exploratory287-sample certificate gives stronger302/303 bounds. The smaller52-sample certificate suffices and replays cheaply. Independent review reproduced all287 original ranks with a separate implementation; that receipt may be retained separately for provenance. Rational residual rank is asserted only to be at least275, not exactly275.

`verify_two_switch.py` uses the standard library, exact Python modular integers, primality trial division, denominator guards,400-main forward/reverse endpoint checks, reconstructed E/R,104 sampled rank calculations and exact interval coverage. Its rank-loss/interpolation controls reject a monotonicity assumption. The written block proof supplies the implication from these source inequalities.

The next target must use at least three global exchanges in this canonical class, role-local switches, added internal coding, or changed source contacts/itineraries. None is ruled out. Pure scalar switches add400 SCALEs each and no Gaussian call at a synchronized cut, but arbitrary helper return, all8 coupled type-B blocks and the complete98.39907695 extra-paid-moment budget remain open. The earlier proposed two-switch search is now closed for this exact class.
