# Sharp 416-field terminal completion of the two-direction code

## Precise theorem and scope

Fix the reconstructed 6,952-event two-direction endpoint word and its exact terminal state. Let each normalized field have V>=1 coordinates over a characteristic-zero field. Consider an appended field-linear programme with arbitrary local linear recoding, free local history retention, arbitrary interbank feedback and newly initialized zero owned records. Ordinary interactions require the same actual chart. Information between charts travels only in charged MOVEs; a full V-field arrival carries at most V independent dimensions. All original public target values must be produced at their source-prescribed final charts. There are no undeclared retained histories, unexecuted funded routes or external input oracles at this boundary.

Then any such completion needs at least 416 newly arriving full-field units: 208 at the hub and 208 across the 104 distinct receiver facets. Therefore its additional recursive moment is at least 416 for every 0<t<=1. A literal suffix with exactly 416 rank-one MOVEs attains this recursive minimum under the retained normalized transport and owned-erasure contracts.

This is an append-only theorem for one terminal interface. It does not exclude changing earlier common or raw routes, keeping new records before the boundary, changing the endpoint code, or changing the required native/caller interface. It does not establish a physical all-width supplier or a new kappa.

## 1. Local arrival lemma

For a chart C, let L_C be the row span of all fields available there at the initial boundary, as linear forms in all original inputs. Let D_C contain the rows that must eventually be output there. Suppose k complete V-field units arrive at C.

Local linear operations, zero initialization and retirement cannot enlarge the span beyond L_C and the arriving messages. Keeping every earlier local value for free only strengthens the programme. Therefore

    k*V >= dim((L_C + D_C)/L_C).

This remains true when messages depend on earlier outgoing messages and feedback: each actual arrival introduces at most V dimensions. Inter-coordinate field-linear maps are included. Replacing one V-field by a larger volume charges the corresponding number of field units.

The same argument applies to distinct exact chart subspaces. Each MOVE has only one destination, so its arrival can be charged to only one of these local inequalities. Summing the bounds does not double-count a MOVE. New role names or local permutations do not change a required output's chart. An uncharged change of chart would violate the declared transport model.

## 2. The residual matrix is invertible

The source-bound predecessor tight-frame identity is A^T A=104 I_8, with A the 104-by-8 root matrix. This is credited reuse from eight-packet-prefix/review-algebra/CORRECTION-STRUCTURE.md, freshly corroborated here.

For P=A A^T/8,

    P^2=13P,
    (P-I)^(-1)=-I+P/12.

The product identity is immediate by multiplication. In particular E=P-I has rank104. Each of its rows is nonzero. The exact source has48 nonzero entries per row, all off diagonal.

## 3. Hub deficit: 104 per copy

In one independent main copy, write X_H for the96 hosted first X coordinates, R for all104 reverse X coordinates and S for their104 reverse Y coordinates. X_H and R are disjoint sets of original input coordinates. At the terminal hub the available main rows are

    X_H,  R-P S.

The required source main rows there are

    X_H,  R-S.

Both collections have rank200. If a linear combination of the second reverse family belongs to the current hub span, matching the independent R coefficients forces the same coefficient vector alpha on R-P S. The remaining condition is alpha*(P-I)=0, hence alpha=0. Their intersection therefore has rank96, exactly the X_H span; their union has rank304.

The missing dimension per copy is304-200=104. After physical recoupling, the common and second-copy maps depend on disjoint independent inputs, so cross-copy combinations cannot reduce their direct-sum deficit: joint current rank400, joint union rank608, missing208.

The822 common helpers currently at the hub are independent unchanged original helper coordinates. Their span is disjoint from the main input coordinates and adds equally to both ranks. Other helper coordinates do not appear at the hub without a newly charged arrival. Thus the hub needs at least208 complete field units.

## 4. Receiver deficit: one per facet per copy

Receiver facet F_i contains the first-Y row

    c_i*(Y_i+P_i X),

and, for hosted i, the unchanged corresponding second Y value S_i. Coupled i has no separate hosted S_i. Common helper rows at that facet are independent original helper inputs.

The required first-Y row is

    c_i*(Y_i+X_i).

Its independent Y_i coefficient forces coefficient one on the existing first-Y row in any local expression. Every hosted second-Y and helper coefficient must vanish, as those input coordinates do not occur in the target. The remaining discrepancy c_i*(P-I)_i X is nonzero. Thus this target adds exactly one missing scalar dimension per copy, or V complete dimensions for arbitrary coordinate volume. The two independent copies jointly add two field units.

The104 facets are pairwise different binary subspaces and all differ from the nine-dimensional hub. This is checked using actual spans, not chart identifier inequality. Each has dimension8. Summing their deficits gives208 field arrivals to the facets. Along with208 hub arrivals, every appended completion costs at least416 positive-rank full-field units. Positive rank r has r^t>=1, so the paid-moment floor is416.

## 5. Attaining word with actual accesses

Process the common and second-copy banks in sequence. Their terminal values are independent; modifying one does not alter the other. For one bank:

1. At each receiver facet, copy its current reverse Y value S_i' into a genuine zero owned record. Move the104 records to the hub by rank-one ascents. Their source charts and live values are actual, not ideal originals granted for free.
2. The96 hosted S_i records already equal original S_i. For the eight coupled indices U, recover original Y_U at the hub using the earlier exact coupled inverse:
   
       a = X_U' + P_UH S_H,
       b = 2Y_U' - P_UH X_H,
       Y_U = (I+P_UU^2)^(-1)*(b-P_UU a).

   Every operand is now physically at the hub: X values were already there; Y_U' and S_H were just carried in. Eight additional stationary owned records store these original Y_U values. The determinant is1384497/4096, and every actual rational coefficient and ADD appears in the word.
3. For each reverse X, add (P-I)_i S using the available original S records. This changes R_i-P_i S into R_i-S_i, the required source output.
4. Original forward X is now available at the hub. Hosted X is untouched. A coupled original X is its corrected current value X_i-Y_i plus the stationary original Y_i record.
5. For each first Y_i, encode c_i*(I-P)_i X in one owned packet at the hub. Move it by one rank-one descent to its actual facet, add it to Y_i', then retire the packet. These104 packets correct every first-Y output.
6. Retire the104 incoming records and eight stationary inverse records at the hub.

All sources for acquisition and correction are current cocharted fields. There is no assumed ideal-Y oracle and no uncharged original-X restoration. Each bank uses104 inward and104 outward rank-one MOVEs, hence416 over both copies. All helpers are untouched and the final map equals both copies of the authentic source target on all1,880 inputs.

The suffix has25,760 instructions:24,480 ADD,416 MOVE,432 INIT and432 CLEAR. Its peak owned count is113. Together with the reconstructed prefix, the full normalized word has32,712 events:29,440 ADD,16 SCALE,2,328 MOVE,464 INIT and464 CLEAR. All owned lifetimes close.

The attaining claim concerns recursive movement only. No claim of minimum ordinary work or minimum storage is made. The rational inverse introduces additional scalar and precision obligations; they are explicit operations and cannot improve the already failing recursive budget.

## 6. Complete invoice and programme consequence

The partial code's exact remaining paid moment per native at t=199/200 is approximately14.812385620139944. The sharp terminal completion consumes416:

    remaining moment = 14.812385620139944... - 416
                     = -401.187614379860055... .

The complete caller has49,968 paid positions,27,344 targets and rank surplus -5,600. The full directed rational bounds are in RESULT.json. This excludes every appended completion in the stated field-linear interface, even with ordinary, storage, scalar, precision and compiler costs granted free.

The useful continuation is therefore before this terminal boundary. A successor must preserve or deliver the missing receiver/hub information earlier, change the direct common transport, or replace the code and its full invoice. The sharp floor does not transfer to that changed problem.

## Verification and credit

complete.py independently derives the local quotient ranks from the actual candidate rows, checks all105 distinct chart subspaces, emits the explicit suffix and reuses the disclosed S008 interpreter for all1,880 source targets. This is author verification, not a second independent mathematical audit. Root review must supply the independent gate.

The suffix adds207 distinct chart-map pairs relative to the candidate. Each is checked by the retained exact Clifford compiler and separate signed-Pauli/global-phase engine; the reverse pair already present is not counted again. Four actual mutants fail: missing inbound MOVE, omitted forward correction, wrong reverse correction and broken coupled inverse.

The mathematical lower bound follows from Sections1–4, not from failed finite search. The exact source and finite word checks authenticate its application. All five foundational assumptions remain; no new complete kappa.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the S007 endpoint recipe, S008 reconstruction, source E8 tight-frame proof, common/raw native source and all retained chart/compiler lineage. Apache-2.0.

