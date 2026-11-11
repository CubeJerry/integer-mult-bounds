# A causal cochart criterion for coded shared storage

Status: conditionally proved constructive interface. No source-wide synthesis witness and no new kappa. The selected original-main-prefix version with only43 owned fields is excluded by the programme's capacity theorem. This interface can guide a changed-prefix construction or an explicitly funded larger storage bank.

## State and hypotheses

Run two virtual copies u,v of a fixed linear native word W, with independent main inputs, the same arbitrary helper inputs h, and zero owned initial fields. Copies of a logical role have the same current chart. Physical mains may initially store both u_r and v_r; a coded auxiliary stores

    z_r = lambda_r u_r + (1-lambda_r) v_r,
    delta_r = u_r-v_r.

A proposed implementation must exhibit every physical observation as a known linear row on the original public inputs, with its current physical chart and owner. Sidecars are real additional fields: their allocation, chart paths, capacity and retirement are charged. A coefficient-only row-span calculation is not enough; every source observation used below must be CURRENT and COCHART with the destination. Coefficients must belong to the actual scalar-service domain, with magnitude/denominator limits and finite implementation costs proved. Rational span membership by itself does not imply an admitted service.

Suppose every requested difference delta_s has a finite expression sum_j b_j o_j in available current cochart observations. Before modifying any destination, materialize that expression into a fresh zero owned field t at that chart using k nonzero ADDs, where k is the support size. This snapshot ensures that later writes cannot invalidate source versions, even if some o_j was a destination. The physical source must still permit this allocation and eventual dirty CLEAR. If a source-stable representation is used instead, its stability must be checked for the complete update macro.

## Exact event lowering

For a virtual ADD d += c s (d!=s), code weights are fixed source-controlled scalars during the complete macro. Every simultaneously live logical main/coded source and destination has a distinct physical owner, under the inherited allocation contract; no source holder aliases a destination holder. Observation expressions may still alias destinations, which is why the difference snapshot is required. With those premises:

| Destination/source | Physical update | ADD count after any snapshot |
|---|---|---:|
| main/main | u_d+=c u_s; v_d+=c v_s |2|
| coded/main | z_d+=c lambda_d u_s; z_d+=c(1-lambda_d)v_s |at most2|
| coded/coded | z_d+=c z_s; z_d+=c(lambda_d-lambda_s)t |at most2|
| main/coded | u_d+=c z_s; u_d+=c(1-lambda_s)t; v_d+=c z_s; v_d-=c lambda_s t |at most4|

For coded/coded with equal weights, no difference or snapshot is needed. Otherwise t=delta_s. For main/coded, t=delta_s is needed unless an equivalent certified direct pair of source expressions is supplied. Zero scalar coefficients are omitted. The source role is distinct from the destination role; destination-aliasing in the observation expression is handled by the snapshot.

The identity behind the coded/coded case is

    lambda_d(u_d+c u_s)+(1-lambda_d)(v_d+c v_s)
    =z_d+c z_s+c(lambda_d-lambda_s)delta_s.

The main/coded formulas use u_s=z_s+(1-lambda_s)delta_s and v_s=z_s-lambda_s delta_s. These are exact identities for arbitrary dirty helpers and arbitrary main inputs.

A nonzero SCALE is duplicated on mains and applied once to a coded field. A MOVE is paid twice for a main pair and once for a coded auxiliary; linear chart transport commutes with the scalar code. An owned INIT creates one coded zero field because both virtual values are zero. CLEAR retires the actual coded owner under the retained erasure contract. A source COPY uses the same ADD rules only after BOTH virtual destination values are established zero; code zero alone does not prove both zero.

To change a code weight from lambda to lambda', snapshot delta_r and execute

    z_r += (lambda'-lambda)t.

This costs k+1 ADDs plus INIT/CLEAR for a k-term snapshot. It introduces no Gaussian MOVE if all observations are cochart. Capturing, carrying, reusing or changing the chart of t beyond this local macro is a separate charged operation.

## Causal correctness and exact accounting

Process the finite source word in order. Induction on the events, using the displayed identities and source-safe snapshots, proves that physical rows represent the declared virtual rows after every macro. The induction assumes the supplied observation identities and chart/ownership witnesses at every event; these are the outstanding synthesis data.

If all such witnesses exist and both virtual copies of W have the selected endpoint E, then both physical main outputs have E, including the eight coupled type-B ports. At a helper endpoint the two virtual normalized values both equal its original arbitrary h, so z_h=h for every final lambda. All actual sidecars must be retired and every owned endpoint contract checked. The theorem does not produce those witnesses automatically.

For n_mm,n_am,n_aa,n_ma virtual ADDs (destination/source order: main/main, auxiliary/main, auxiliary/auxiliary, main/auxiliary), plus J code changes and snapshots with supports k_j, a conservative scalar-event bound is

    2 n_mm + 2 n_am + 2 n_aa + 4 n_ma
      + J + sum_j k_j

ADDs, plus duplicated main SCALEs, single auxiliary SCALEs, source INIT/CLEARs, and two lifecycle events per snapshot. The count overcharges omitted zero terms and equal-weight auxiliary contacts. Coefficient services, source/control movement, rounding and erasure costs remain positive and need their actual tariffs. Serial snapshots can reuse one physical role only if its previous history is retired and its next chart/initialization is legitimate; assuming one reusable role is not a storage proof.

With no extra sidecar MOVE, the base Gaussian invoice is exactly twice the original main MOVE histogram plus one original auxiliary MOVE histogram, with one credit per original helper. Extra observation/parking routes must be added. In the recovered H4 caller, permissible added per-native paid moment is less than M4/18≈98.39907695 if every other term remains fixed. Equivalently, more than13.012927833 must be saved from the doubled-owned baseline. This condition does not bound physical ordinary work or prove compiler admission.

## What the interface does and does not resolve

It identifies the precise missing causal data: for each defect, a current cochart expression, its valid scalar services, a source-version-safe schedule, and funded ownership. Static recoverability at one cut, eventual source restoration, or a favorable scalar invoice supplies none of these automatically.

The frozen original-main-prefix scheme cannot satisfy the full interface with only43 owned fields: the programme's rank deficit already requires at least62 additional full fields at the examined cut even allowing arbitrary helper coding. Thus applying this interface requires changed main-prefix rows, extra funded observations, or a new itinerary. A generalized changed-prefix row template can use the same snapshot/update principle, but must supply its own per-event target-row identities rather than claim the frozen virtual-prefix invariant.

## Negative source-version control

Let delta=old(a)+b, first destination a, second destination v, c=1 and lambda_s=1/2. Initially a=1,b=2,z_s=5,v=7, so delta=3. Correct snapshot updates give a'=15/2 and v'=21/2. If delta is recomputed after writing a, it becomes19/2, yielding v'=29/4 instead. Snapshotting the old cochart expression before either write recovers the simultaneous virtual ADD. Distinct virtual source roles may have physical expressions involving a destination; the snapshot is what preserves their original versions.

Prepared for @CubeJerry with substantial OpenAI assistance. This is an algebraic realization interface with explicit costs and premises, not a constructed H4 word. All five global assumptions remain.
