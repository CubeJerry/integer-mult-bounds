# One-receiver packet and gain reduction after initial precompensation

**Derived linear-interface theorem, using admitted pinned source facts. No new kappa.**

## Precise interface

Let `u` be the 1480 independent common inputs and let `q` contain all independent raw differences used by a proposed code. The row `e` selects q77; the common-input row `h` selects u77. Fix the pinned native source and receiver189. Let `O` be its complete initial/MOVE-arrival history matrix, of size1065 by1480 and rank1056. Let `C` denote a packet matrix, so the receiver is granted the full packet vector `p=Cq`, and let `S q` be all further private, common-input-independent linear information granted to that receiver. These grants do not establish physical delivery or its price.

Before native execution, allow any common-input precompensation `u'=u+V Cq`. Its physically proposed specialization uses only public inputs initially at empty chart3. During execution allow arbitrary additive q-dependent controls, at arbitrary times, at the220 canonical station charts of the admitted joint-additive-history obstruction. Write their response on registered histories as `Bq`. No additional common-dependent replacement is permitted. The native operations, routes, observation times and field lifetimes otherwise remain unchanged. Controls may depend linearly on all q coordinates, not just q77; the source zero-adjoint identities apply separately to every coordinate.

Require final common role189, as produced by this execution, to equal its original baseline value `u189+u77`. Hub-only subsequent corrections cannot change this off-hub field. The receiver sees only the declared native histories, `Cq`, and `Sq`. Unmodelled new raw carrier histories or common-dependent records are not included. It is granted arbitrary local linear combinations and free storage. All statements hold over Q and, by tensoring, for every admitted field volume with scalar-matrix controls; arbitrary coordinate-linear controls require the corresponding block-row interpretation.

## Theorem

Under this interface, a linear receiver decoder can recover `u77+q77` for every independent `(u,q)` if and only if

`e in row(C,S)`.

Equivalently, the controlled native common history supplies no additional q77 information beyond the packet and private-information span once this endpoint has been restored. This is a necessary interface condition, not a source delivery construction or tariff lower bound.

## Proof with the modified initial history retained

Every zero-baseline relation `dO=0` satisfies `dB=0`, by the admitted complete nine-relation source certificate. Thus all decoders `D` with `DO=h` have the same q-response `DB`. The histories actually read are

`y=Ou+(OVC+B)q`.

The native final role189 is a linear combination of the registered histories with the same coefficients in the perturbed execution. This last assertion uses the disjointness of the220 control stations and the receiver itinerary: native local ADD/COPY/SCALE combine previously present fields; INIT adds zero; every MOVE arrival is recorded; no unrecorded control is inserted at a receiver chart. The independently checked stable-history source packet gives the baseline identity

`h = final189 - initial189`.

Let `D0` be that actual endpoint-minus-initial history decoder. The modified initial observation is `u189+(e189 V)Cq`; it must not be silently treated as the original u189. Since the actual final endpoint is restored,

`D0 y = u77-(e189 V)Cq`.

For any other `D` satisfying `DO=h`, the difference `D-D0` annihilates O and therefore B, as well as OVC. Consequently

`D y = u77-(e189 V)Cq`.

Any full linear decoder for the target must have a history coefficient D with DO=h, because the packet/private records contain no u. Its remaining q coefficient can therefore be changed only by rows of C and S. The equality to `u77+q77` is possible exactly when e lies in row(C,S). Sufficiency is explicit: use D0, add `(e189 V)Cq`, then recover q77 from Cq and Sq.

## A full indistinguishability strengthening within this exact interface

The same necessity also applies to nonlinear decoders of these particular records. If `e` is outside row(C,S), choose q0 with `Cq0=Sq0=0` but `e q0 != 0`. Complete left-null annihilation implies `Bq0` belongs to im(O), so choose v with `Ov=Bq0`. The records for `(u=0,q=q0)` and `(u=v,q=0)` coincide. Moreover `h v=D0 Ov=D0 Bq0=0`, since Cq0=0 and endpoint restoration gives the displayed D0 identity. Their target values differ by `e q0`. This proves indistinguishability, not merely a linear-rank heuristic. It does not claim impossibility after adding different records.

## Scope and escapes

This is a one-receiver statement for77 to189. Donor77 is already among the17 directly repaired channels in the new physical partial word, so this theorem alone does not obstruct completing the other87 first-pair channels or the remaining191 total dependencies.

A donor raw input v77 itself is a common-dependent private record and is outside the stated Sq-only model. A receiver's own raw input can be converted to its own q coordinate using the initial common observation and known packet correction; if used, that coordinate must be included in S. More general correlated common/raw side information must be modelled jointly and can escape the conclusion. So can common-dependent payload replacement, new observation/carrier histories, controls at receiver charts or other charts outside the220 set, a different native word, or additional packet/private rows containing the missing direction. Pure packet-dependent initial corrections alone do not escape, because their full effect has been retained above.

In particular, matching the desired E8 Gram column at off-hub endpoints does not by itself establish the required donor gain. If a candidate uses only this interface, its actual local private S must also make e lie in row(C,S). This is not a claim that E8 packets fail every possible completed architecture.

## Provenance and admission

Source: `research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

Dependencies: `results/joint-additive-history-obstruction/PROOF.md`, `CERTIFICATE.json`, `ADMISSION.md`, and independent `review/REVIEW.md`; `results/stable-history-encoder/source/PROOF.md`, exact `RESULT.json`, and independent stable-gate/source reviews. They establish the complete history dimension, all220-station zero adjoints, disjoint receiver itinerary and actual stable endpoint representation. The source facts were established previously; the contribution here is the exact packet/private-information reduction after precompensation, including the modified initial observation and its indistinguishability proof.

Credit: @CubeJerry's persistent programme, predecessor source and obstruction authors, S006 root's packet/gain question, and OpenAI-assisted construction-worker proof. Independent review of this new reduction is requested separately. No new multiplication bound or scalar/precision admission is claimed.
