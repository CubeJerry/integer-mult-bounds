# Joint response injectivity for 58 prescribed helper departures

**Status:** exact finite-source linear theorem for a stated intervention family. No new kappa. This closes a proposed low-dimensional compression of these particular simultaneous debts; it is not a lower bound on every side-informed repair protocol.

## Pinned family

Use native `research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`, canonical `e54523517d0f03e58352e647c403a5af3e525a57`.

The predecessor `results/itinerary-control-obstruction/CERTIFICATE.json` lists 103 donor/departure pairs at 58 distinct `(event,helper)` cuts. The theorem concerns exactly those 58 cuts, ordered chronologically. It is not a completeness claim about all native helper departures. `results/active-helper-observation/OBSERVATIONS.json` supplies 31 independently admitted single-pulse historical decoders, at distinct cuts and for distinct first-X donors. Both predecessor byte hashes are recorded in the receipt.

Immediately before cut k's helper MOVE, add an arbitrary field a_k to that helper. The rest of the common word is unchanged. All common inputs u are arbitrary. Define H_k u as the unperturbed pre-cut payload. Let L_kj be the contribution of unit impulse j to that payload just before cut k, and let Z contain the final public common responses outside hub127. Then L is strictly lower triangular and

    current pre-cut payload_k = H_k u + sum_{j<k} L_kj a_j,
    final offhub common error = Z a.

The columns of Z include all 458 offhub public endpoints. The native COPY guard has zero response to every one of the 58 impulses. All statements tensor with the identity on every positive field volume V over Q or C.

## 1. Exact source result

The source certificate gives:

| Selected columns | Number | Offhub rank |
| --- | ---: | ---: |
| All prescribed departure events |58|58|
| Admitted historical-observer events |31|31|
| Prescribed events whose baseline payload is exactly u_Xj |30|30|
| Admitted historical events with that unit payload |17|17|

All 30 unit-payload donors are distinct and have actual donor access at the selected source chart. The 31 admitted observers also have distinct donors. The entire 58-event family has multiple possible donors at two cuts and repeated donor choices at other cuts; 58 independent private donor channels are **not** inferred from 58 independent impulse slots.

The exact verifier reconstructs each H_k independently by propagating one row backward through its source prefix. It then propagates all 58 formal impulses forward through the full native word, recording L and Z. It reproduces every stored H row and offhub response from the 31 predecessor modules. Rational elimination produces explicit pivot-output lists and nonzero pivot coefficients. In particular the 58 selected pivot rows give a nonsingular 58-by-58 submatrix of Z. These finite identities, together with the following argument, establish the all-volume statements.

**Injectivity theorem.** If a controller changes the common word only through these 58 additive intervention slots and through arbitrary final hub-only corrections, then all common endpoints outside the hub are restored if and only if a=0.

**Proof.** Z has full column rank, so Z tensor I_V has trivial kernel. Offhub restoration means `(Z tensor I_V)a=0`, hence every a_k is zero. Conversely zero interventions leave the native common output unchanged. This argument applies to realized amplitudes of feedback controllers: they may depend on arbitrary common values, private inputs and earlier controls, and need not be linear functions of those inputs. Their effects still enter the fixed native word through the displayed linear impulse map. QED.

The result allows jointly chosen impulses, rather than checking neutrality one pulse at a time. It does not allow additional correction slots at other positions, changed native operations away from those cuts, or final offhub correction using other fields. Those are genuine ways to change the interface.

## 2. Causal encoders and the debt-rank invariant

For selected cuts with nonzero gains g_i, a current-payload encoder installing the local desired value x_i with gain g_i satisfies

    a_i = g_i (x_i − H_i u − sum_{j<i} L_ij a_j).

Writing `T=diag(1/g_i)+L` on that selected subfamily gives

    T a = x−H u.

T is lower triangular with nonzero diagonal and is therefore invertible. If the selected x_i are independent supplied private values, the q-dependent error map has the same rank as Z: multiplication by T inverse and by nonzero diagonal gain matrices cannot lower it. In the unit-payload actual-input version, x_i=v_Xi=u_Xi+q_Xi and H_i u=u_Xi, so a=T inverse q and the same conclusion applies directly.

Thus the complete 17-,30- or31-dimensional independent debt vector cannot be represented as a function of only eight common field-valued linear packets. In formal terms, an identity

    Z T inverse = D C

with C having at most eight rows is impossible for those respective subfamilies. This is a rank statement about factorizing the entire debt through shared values. It is **not** a claim that every physical repair needs 17,30 or31 new messages: receivers may already have useful local side information, and other funded operations can alter what must be transmitted.

## 3. The old 31 decoders do not compose unchanged

Let Phi_i be predecessor i's actual historical decoder. Baseline correctness is `Phi_i(F0 u)=H_i u`. Define B_ij as its response to impulse j, using all recorded source times and fields. Under joint intervention, the decoder therefore returns

    Phi_i = H_i u + (B a)_i.

The predecessor gains are essential: five decoders have sensitivity1,24 have sensitivity1/2 and two have sensitivity−1/2. Their gains are respectively1,2,−2. Exact replay verifies B_ii=1/g_i.

For current-payload encoding, desired x equals H u+T a. Hence the simultaneous decoder error is exactly

    decoded−desired = (B−T)a.

On the 31 admitted cuts, the source has rank(B−T)=30. All 31 rows have a nonzero mismatch. Therefore individual single-pulse correctness cannot be reused as a proof of simultaneous correctness. This does not exclude a different decoder using the complete local history, added initial corrections, or additional physically supplied information.

For the 17 unit-payload admitted modules, a separate continuation calculation finds rank(B17)=14 and rank(I−B17 T17 inverse)=16. Every unit17 encoder lies on its donor's initial rank1 chart. Every offhub unit17 response is supported on outputs whose original common input is at chart3. This supports a conditional initial-precorrection interface, but its full independent common debt still has rank17. That continuation is separate from the 58-slot theorem and needs its own physical cost accounting.

## Verification and limitations

`verify.py` uses exact Fraction arithmetic, explicit exceptions rather than assertions, all source instructions and all 1480 public input variables. The source hash and two predecessor hashes are retained. Exact backward payload reconstruction and simultaneous forward response reconstruction use different directions; this alone is not independent review. The separately authored review reconstructs H forward and L/B/Z by backward adjoints.

The source proof uses the literal 58 cuts and the supplied 31 history modules. No asymptotic optimality, generic impossibility or lower bound for all helper encoders is claimed. Neither common restoration nor a new complete multiplication exponent has been constructed. All five programme assumptions remain.

Credit the selected native's authors, @CubeJerry's persistent programme, and the S004 active-observation and itinerary-control packages. This contribution is the exact joint source matrix, its injective-response consequence, and the corrected causal gain accounting. Prepared with substantial OpenAI assistance.
