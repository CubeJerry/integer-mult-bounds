# Independent review of the eight owned-chain history gate

**PASS for each receiver separately. All eight pulse columns are hidden by its common-input history. Pooling the receivers' histories is a strictly stronger interface and extracts all eight pulses.**

This is an independent exact review of the frozen `worker-budget/OWNED-HISTORY-EXTRACT.json` gate, followed by new constructive shadow and pooled-decoder certificates. It is not an encoded-packet source construction or a transport bound. The immutable native is `research/shared-wire-split-composition/data/final.json.gz`, with compressed SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. The reviewed author report has SHA256 `ef743bb4846997bde8e066bc444af5532c3d3bc0b0c041b269ac92ad2a07e9f4`; its frozen producer has SHA256 `03e154141940265880b12df415bfd2e52881cec11a0d9dfd645f28799ca6cc61`.

## Exact observation interface

The eight independent additive pulse coordinates, in column order, are inserted immediately before source events

    28105, 30806, 32554, 34446, 36891, 30629, 38222, 40087.

Each event is a MOVE of a common-owned field. The modification adds the corresponding independent pulse to the departing value. It does not overwrite that value by an independent packet and does not supply its original payload as a separate record.

For each of the 104 raw receiver itineraries, grant all original initial common fields whose charts lie anywhere on that itinerary, and every original MOVE arrival at any of its charts, over the entire native chronology. Denote this receiver's complete granted vector by

    y_i = O_i u + B_i a,

where u consists of all 1480 independent original common inputs and a has eight independent pulse coordinates. The grant is stronger than recording only the receiver's own role. It still belongs to one receiver itinerary at a time; it is not a grant of other receivers' observations.

Our independent chart and location replay establishes that every pulse insertion chart lies outside the union of all these receiver itineraries. Thus original local processing at a receiver chart introduces no unrecorded pulse injection. Its initial values and MOVE arrivals span its subsequent source-local states. The sole source COPY at event 31737 has zero response in all eight pulse columns. Every selected first-entry response to earlier selected pulses is zero, so the eight chosen first-entry cross-effects vanish.

## Independent checks and the local obstruction

`check_owned_history.py` imports no author implementation. It reconstructs the charts, receiver routes, actual arrival versions and both the common and eight-column pulse propagation using exact rational arithmetic. Quotienting the 1046 initial input units shared by every receiver leaves 434 common columns; each receiver's further known input units are then removed separately.

The independent replay checks all 2846 arrival observations counted with receiver multiplicity, comprising 1860 distinct source arrival events. It verifies all 1486 author-supplied left-null relations against both the reconstructed common rows and all eight pulse columns. For every receiver, the supplied relations are independent and their count equals the independently computed full left-nullity. Hence they form a complete basis, not merely a list of vanishing examples.

If N_i is any full left-nullspace matrix of O_i, the exact conclusion is

    N_i B_i = 0            for every one of the 104 receivers. (1)

Equivalently, every pulse response column lies in the image of the receiver's common-input observation map. No nonzero pure linear combination of the eight independent pulses can be read from that receiver's granted histories alone. The intended first-Y pulse row is nonzero for all 104 receivers, so none can extract its whole such row in this interface. This statement does not include additional raw-signal or mixed common/signal records.

## Explicit positive common-input shadows

The new certificate supplies, for every receiver, a matrix V_i satisfying

    O_i V_i = B_i.                                      (2)

It includes the initial observations: V_i is zero on every common input initially granted to that receiver. In fact all 104 V_i can be supported solely on the 104 original common X coordinates. These are coordinates of u, not the independent raw donor signals used in a coupled construction. The maximum support is seven common X rows, with this support distribution:

| Nonzero common X rows | Number of receivers |
| --- | ---: |
| 1 | 2 |
| 2 | 24 |
| 3 | 37 |
| 4 | 28 |
| 5 | 11 |
| 6 | 1 |
| 7 | 1 |

The exact rows and eight rational coefficients are `receivers[*].X_only_shadow_rows` in `CERTIFICATE.json.gz`. The replay checks every identity (2) explicitly after solving for the shadows.

These shadows give a direct indistinguishability proof, independent of a decoder ansatz: the observed histories from input u and pulse a equal the histories from common input u+V_i a with zero pulse. More generally, changing a by t and u by -V_i t leaves this receiver's observations unchanged. Any nonzero linear target of a therefore changes along some invisible displacement. The construction tensors with the identity on a complete field volume.

## Why there is no single global common-input shadow

A single source-wide V satisfying (2) simultaneously for all receivers does not exist for these eight controls. Pooling every granted initial field and every observed arrival changes the ranks:

| Interface | Granted initial common units | Remaining common-history rank | Pure pulse rank |
| --- | ---: | ---: | ---: |
| One receiver at a time | Receiver-specific | Verified separately | 0 for all 104 |
| Union of all receiver histories | 1091 | 337 | 8 |

The union leaves 389 ungranted initial common coordinates. Even restricting attention to common X shadows and permitting unrestricted initial common X values fails to reproduce the pooled arrivals: their eight pulse columns remain independent modulo that common X image. Thus the local shadows cannot be made consistent by selecting a different common X solution for each receiver and then identifying them globally.

The certificate supplies eight explicit pooled observation combinations with zero common component and pulse gains equal to the eight standard coordinate rows. Each uses actual timed MOVE arrivals and initial common fields in the union. A separate backwards adjoint through the full native, including all 1480 common input coordinates, verifies these decoders: the only surviving common coefficients are cancelled by the listed initially granted fields, and their eight control-cut responses form the identity matrix.

| Extracted pulse | Timed arrival terms | Initial common terms |
| --- | ---: | ---: |
| 0 | 42 | 59 |
| 1 | 33 | 61 |
| 2 | 54 | 149 |
| 3 | 44 | 60 |
| 4 | 33 | 53 |
| 5 | 36 | 41 |
| 6 | 51 | 130 |
| 7 | 58 | 184 |

The exact terms are `pooled_receiver_interface.pooled_extractions`. They are finite source identities that refute an all-receiver global-shadow claim. They require data distributed across different itineraries. No acquisition, caching, route or price for collecting those terms has been constructed, and these algebraic decoders do not make pooling free.

## Connection to the joint packet-gain criterion

The programme's `results/packet-gain-reduction/GENERAL-INTERFACE.md` writes actual histories as y=Ou+Rq and gives the compatible decoder gains through the full left-nullspace contribution NR. For precompensated histories R=OVC+B, the extra zero-common gain is NB. Our result authenticates the full eight-column identity N_i B_i=0 for this fixed control family and each of these 104 specific receiver interfaces. It is stronger than checking one pulse column or a subset of left-null relations.

Thus native histories provide no additional pure packet direction from these eight additive controls beyond whatever packet or private records are separately granted. A particular decoder target must still be compared with the span of those records and with its actual baseline-compatible history gain. The new criterion does not authorize replacing the individual observation interface by its pooled union, whose NB has rank eight here.

Overwriting a helper by a packet can change the common observation matrix O, and retaining its displaced payload or a mixed raw/common value adds new observations. The additive-pulse gate cannot be applied to those changed interfaces without recomputing their common map and null relations. Likewise, additional control cuts, carrier observations or donor-station unions can change the result.

## Reproduction and evidence status

Run `python3 /workspace/scratch/6a77123a1d61/worker-review/owned-history/check_owned_history.py` in the shared workspace. The script authenticates the native and frozen author report, reconstructs the observations, checks the full local annihilator bases, derives and verifies the positive shadows, and checks the pooled decoders by a full-input adjoint. It writes the canonical mathematical certificate, a concise `REVIEW-RESULT.json`, and an additional report including elapsed time.

Canonical decompressed `CERTIFICATE.json.gz` SHA256:

    a6e6efe3e4e1df2f2f62d47796f089470bbec168a6dd5c28a2217d9b63ba5611

The local annihilator review is independently authored evidence for the budget worker's frozen gate. The explicit X-only shadows and pooled decoders are new results of this review worker; their construction and internal verification are author evidence for those additions until another worker reviews them. Substantial OpenAI assistance contributed to this work. No source supplier, full coupled private map, paid transport improvement or new kappa is claimed.
