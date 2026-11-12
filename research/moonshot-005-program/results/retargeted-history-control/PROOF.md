# Chart 318 cannot give receiver 189 an endpoint-neutral history gain

**Exact result for common-input-independent controls:** fixed linear combinations of the independent raw signals, inserted at charts 16, 35, 127 and 318, cannot supply receiver189 with pure signal information while the off-hub common endpoints are restored. This includes the proposed q17 and q38 detours and their joint use under the larger grant of both signals at all four charts. The underlying two-endpoint identity holds for more general realized increments, but that alone is not an information exclusion for common-dependent feedback or replacement.

## 1. Authenticated source and interface

The native is `research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. The receiver's nine complete common-history null relations are those in `results/joint-additive-history-obstruction/CERTIFICATE.json`, SHA256 `168fee8f09cdf0f33bcf5989630d244141d3c570808b7ccb553f6ad7be098dd7`.

Receiver 189 is granted all initial common values at its original itinerary charts and all native MOVE arrivals to those charts, for the full chronology. Independently reconstructed counts are 1046 initial units and 19 arrivals. After quotienting the initial units, the common rank is 10; hence the full common-history rank is 1056 and the nullity is nine. The nine supplied relations are independent. A fresh full-input adjoint checks that each relation annihilates all 1480 original common inputs exactly.

Write nu_j for the value of null relation j on the changed history, using the certificate's zero-based relation order. Write Delta_r for the change in final common public field r. Allow additive increments on any live native field at any cut where that field is at one of the four charts

    16, 35, 127, 318.

These can be arbitrary fixed linear combinations of independently retained raw signals, whose coefficients are independent of the common inputs u. In the independent coordinates (u,q), the increments depend only on q, so the original common observation matrix is unchanged. No restriction on the number of such controls is imposed. The native chronology remains fixed, its COPY guard must remain valid, and observations are taken at the original declared initial and after-MOVE cuts. A control inserted before source event t affects that event and later events, not observations already recorded before it.

## 2. Two-endpoint identity

For every such control word, exact source propagation gives

    nu_5 = (Delta_215-Delta_189)/2,
    nu_7 = (Delta_215-Delta_189)/4,
    nu_j = 0 for j outside {5,7}.                     (1)

The endpoints are at charts 223 and 198 respectively; both lie outside hub127. Therefore preserving all off-hub common endpoints implies nu=0. In fact preserving just these two endpoints is sufficient for that conclusion. Any remaining hub-only changes can be repaired using the retained raw signal at the hub, but such repairs cannot make the vanished history gain nonzero.

For the stated controls the histories have the form y=Ou+Bq with the original common matrix O unchanged. These nine relations span its complete left nullspace, so nu=0 means NB=0 and excludes every nonzero pure signal combination obtainable from these histories. Adding raw records to the receiver, or allowing common-dependent controls that change O, changes this information interface and must be analyzed separately.

## 3. Exact derivation and direct source verification

`derive_control_word.py` initializes the adjoints for all 458 off-hub public endpoints, the sole pre-COPY guard and all nine history relations. It follows all native fields backwards, inserting each history observation at its actual cut. It records each possible control column when its adjoint or chart changes. Between such changes the column is constant, so this enumerates all cuts without treating unchanged time intervals as new directions.

For donor17's chart set {16,127,318}, and separately donor38's {35,127,318}, the scan checks 28276 relevant changed states. Each has 25 distinct nonzero endpoint/guard/history columns, and the endpoint-plus-guard rank is 11. Exact elimination finds no endpoint/guard-neutral column combination with nonzero history response. Its resulting dual uses only final fields189 and215 and simplifies to (1).

`check_dual.py` is a separate direct implementation of that final two-endpoint identity. It does not import the span derivation. It initializes the residuals

    nu_5 + Delta_189/2 - Delta_215/2,
    nu_7 + Delta_189/4 - Delta_215/4,

and the seven other nu rows, then propagates those adjoints backwards through the native. At every relevant cut and native live field in the union {16,35,127,318}, all nine coefficients vanish. It checks 28292 changed states. A finite linear combination of source control columns therefore also has zero residual, proving (1). Identity (1) also applies to realized increments chosen causally from earlier records, since the fixed native response to the increment values is linear. This extension proves only the identity for the original nine history functionals. If the increments depend on u, the effective common matrix can change from O to O-prime, whose new null relations need not be among those nine. It therefore does not extend the no-information conclusion to common-dependent feedback or overwrites. For example, an original observation y=u has no left-null relation, but replacing it by q makes q observable despite every original null relation still vanishing. New observation access or a changed native chronology is also outside the tested interface.

The direct checker separately reconstructs the 1065 baseline observations, proves their exact rank1056 and the independence of the nine supplied relations, and verifies all nine original null identities on the full input space. Thus the conclusion uses the complete receiver-history quotient.

## 4. The tempting pulse and negative controls

Immediately before source MOVE event37195, field979 is at chart318. A unit additive control there gives the exact off-hub response

| Common endpoint | Change |
| --- | ---: |
| 189 | -4 |
| 215 | -2 |
| 449 | -1 |
| 484 | 1/2 |
| 953 | 1/2 |
| 979 | 1/2 |

The COPY guard response is zero. Its history responses are nu_5=1 and nu_7=1/2. They satisfy (1): the endpoint difference is -2-(-4)=2. Other allowed controls can alter and cancel endpoint errors, but any cancellation of this endpoint difference cancels these gains in the same proportion. A search limited to individual controls or proportional pairs would not establish this; the full control-space factorization does.

The checker rejects changing the sign of the endpoint dual. That mutant first fails in reverse order at the displayed control cut, with residuals2 and1. It also rejects silently granting the additional chart198: a terminal control on common189 there gives residuals1/2 and1/4. These controls delimit the exact station scope; (1) is not a source-wide identity for arbitrary new charts.

## 5. Actual rerouting ranks

The proposed raw routes are geometrically valid. Chart318 has frame [51,81] and span {0,51,81,98}. Donor17 starts at chart16 with line81; donor38 starts at chart35 with line98. Each line is contained in chart318, which is contained in the rank-nine hub chart127. Thus either route

    original donor line -> chart318 -> hub127

has newly charged ranks [1,7]. Their original source-route rank profiles, independently reconstructed from the frames, are:

| Raw donor | Original route charts | Original ranks | Proposed ranks |
| --- | --- | --- | --- |
| 17 | 16,308,326,232,127 | 1,1,1,5 | 1,7 |
| 38 | 35,309,324,854,982,153,127 | 1,1,3,1,1,1 | 1,7 |

For a rank tariff r^t with 0<t<1, the proposed moment 1+7^t is strictly below 3+5^t and below 5+3^t respectively; this follows by merging positive rank summands under the strictly subadditive power. All three total rank sums are eight. These are actual replacement routes, not uses of the donors' old MOVE reservations. A construction would also have to count the raw caches, retention, scalar operations and receiver recording. This geometric saving does not change the zero-gain conclusion under the fixed control interface.

## 6. Scope and provenance

The arithmetic above is exact over the rational source scalar model. It does not authorize coefficients in a scalar service that the source model excludes. No finite control word with fixed common-input-independent raw increments can reveal a nonzero pure signal combination through these receiver189 histories while the common endpoints are restored. Common-dependent replacements are excluded from this information claim, even if their endpoint errors are later restored; the original-functional identity (1) remains valid on their realized increments. Other charts, additional packet or mixed records, changes to the observation family or native chronology, and a joint source using other receiver histories remain outside this statement.

Both `derive_control_word.py` and `check_dual.py` were authored by the review worker in response to the root worker's chart318 proposal, with substantial OpenAI assistance. The nine original history relations and the candidate cut came from the programme and budget worker. The direct checker is separate implementation evidence for this new result, not a claim that another author has independently reviewed the new proof. Root review is pending. No supplier, full private native or new kappa is supplied.
