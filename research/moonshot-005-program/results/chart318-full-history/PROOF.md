# The complete receiver history closes the chart 318 swap detour

## Result

For receiver189, the entire original common-history response to arbitrary realized source-field increments on charts `{16,35,127,318}` factors through four final common endpoints:129,150,189,215. Consequently, restoring those four endpoints leaves every original receiver history unchanged. This closes the common-dependent swap and feedback extension of the proposed q17/q38 chart318 detour, under the fixed native chronology and the original receiver observation interface.

The conclusion is stronger than the earlier chart318 result about the nine original null relations. It does not assume that the common observation matrix is fixed while constructing the controls. Instead, its entire difference is proved to vanish whenever common restoration is completed. The statement includes a displaced common record physically retained at the hub and used for later hub corrections, but excludes delivering a new record to the receiver, moving the receiver through new charts, changing the native chronology, or using other source-control charts.

The frozen compressed native source has SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. Events are zero based. This is an exact scalar/whole-field source identity, not a complete supplier or a new multiplication bound. Prepared with OpenAI assistance.

## Actual changed access and retained record

Donor17 starts at chart16, line81; donor38 starts at chart35, line98. Chart318 has frame `[51,81]` and span `{0,51,81,98}`. Either donor can take the actual replacement route

\[
\text{initial donor line}\longrightarrow318\longrightarrow127
\]

with ranks1 and7. The tariff is `1+7^(199/200)`; this replaces that donor's old route and does not grant its old stops. A source swap at318 can use three cochart ADDs and a SCALE by−1 to exchange the current common payload `h(u)` with the actual raw difference `q`. The donor raw carrier then physically retains `h(u)` on the ascent to hub127. This retained record is accounted for as a function of the arbitrary common inputs, not as a second copy of `q`.

Receiver189's unchanged itinerary is `3 -> 307 -> 901 -> 198`. It contains neither318 nor127. The donor's retained record therefore does not itself enter the receiver's observations. The receiver is granted all1,046 initial common units at its itinerary charts and every one of the19 native MOVE arrivals at those charts. Initial observations are recorded before the inserted source controls. This is an overgrant of the common information available on the unchanged raw route.

## Direct single-swap screen

There are24 distinct source state intervals to consider for a single overwrite on chart318. The scan takes the state immediately before every native instruction touching a live field there, and any terminal live state. Between such touches the displaced value, suffix response, and receiver response are unchanged, so these intervals exhaust the single-swap cases on that chart.

For each interval the screen reconstructs the actual displaced row `h`, the receiver arrival response `b`, all endpoint responses, and the COPY response. It then forms the changed common matrix

\[
O'=O-bh
\]

and computes both `rank(O')` and `rank([O',b])`. The1,046 known initial common input units are quotiented as known observations, not assumed zero physical inputs. The original remaining common rank is10. This directly tests changed-matrix information rather than applying the old nine null relations to a new interface.

Exactly two cuts are individually off-hub neutral and COPY-valid:

| Before event | Common field | Native next operation | Hub response to a unit increment |
|---|---:|---|---|
| 36172 | 1048 | `ADD1048 -= 933` at318 | `2*e17 - 2*e38 + e1048` |
| 38331 | 1048 | `MOVE1048 318 -> 717` | `2*e17 - 2*e38 + e1048` |

For both, all19 receiver arrival responses are exactly zero. Thus `b=0` and `O'=O` for every displaced payload, including arbitrary common-dependent payloads. Neither swap supplies any receiver signal. The second cut is the unique chart318 departure in the admitted1,472-slot neutral-helper census.

Five nonneutral cuts do make pure `q` observable in the changed interface. This is a useful control showing that the screen does allow new null relations. In particular, replacing common215 by `q` immediately before its MOVE at40835 makes that actual arrival at901 equal `q`, drops the common quotient rank from10 to9, and exposes one pure signal direction. Its final common errors are `Delta189=Delta215=q-h`. The candidate is therefore not a restored channel. The full-history identity below proves that cancelling all common errors within the declared control charts also removes every receiver-history change.

## Exact complete-history identity

Write `DeltaH_r(t)` for the difference, from the untouched native, of common field `r` immediately after source MOVE event`t`. Write `E_r` for the difference in final common field`r`. Allow any finite sequence of realized additive increments on any live native field, at any cut where it is on one of `{16,35,127,318}`. Increments may depend on common inputs, retained records, private signals, and earlier observed values; the native instructions between them remain fixed and the original COPY guard must remain valid.

Exactly five of the receiver's19 arrival differences can be nonzero. They satisfy

\[
\begin{aligned}
\Delta H_{979}(37195)&=(E_{215}-E_{189})/2,\\
\Delta H_{215}(40835)&=-(E_{129}+E_{150})/2-E_{189}+2E_{215},\\
\Delta H_{484}(40836)&=-(E_{129}+E_{150}),\\
\Delta H_{953}(41626)&=(E_{215}-E_{189})/4,\\
\Delta H_{189}(41650)&=-E_{189}+2E_{215}.
\end{aligned}
\]

All other14 arrival differences are zero. The four endpoint charts are143,162,198,223 respectively, and all are off hub. Restoring every common datum in particular sets all four `E_r` to zero. Therefore all19 arrival differences vanish, as do all initial-observation differences.

To justify the common-dependent scope, let `delta` list the values of the realized increments, whatever causal computations produced them. Fixed source linearity gives endpoint differences `E=A delta` and arrival differences `H=B delta`. The displayed source certificate proves `B=D A` on every admissible source-control column. Thus `H=D E` holds for these actual increment values pointwise. A replacement has increment `q-current_common_value`; a swap has the same source increment plus a separately retained record. These fit the identity. Nothing in this reasoning assumes `delta` is independent of the common input.

This proves that the effective restored observation map is the original map. It avoids the invalid inference from “the old null relations vanish” to “a changed common matrix has no new null relations.” Here the entire actual history vector is unchanged after imposing common restoration. Because none of the allowed control charts is a receiver itinerary chart, the receiver's other local native states are determined by these unchanged initial values and arrivals as well.

A return from receiver198 to hub127 can only carry information already available at the receiver. It cannot make an otherwise absent target-donor signal appear there. Delivering a new q-bearing record from the hub or another chart to the receiver would change the observation interface and must be constructed and priced separately.

## Derivation, direct check, and evidence status

`full_history_factor.py` replaces the earlier screen's nine null-history outputs by all19 actual arrival outputs. Its sparse column/elimination helper is explicitly reused from the review worker's `chart318-control/derive_control_word.py`. It propagates adjoints for every off-hub endpoint, the sole pre-COPY guard, and all arrivals. It tests every changed source-field control column at the stated charts; columns are constant between those changes.

| Allowed control charts | Checked changed states | Distinct nonzero columns | Endpoint/guard rank |
|---|---:|---:|---:|
| `{318}` | 16 | 13 | 7 |
| `{16,318,127}` | 28,276 | 25 | 11 |
| `{35,318,127}` | 28,276 | 25 | 11 |
| `{16,35,318,127}` | 28,292 | 37 | 15 |

In each case, the entire arrival response factors through the endpoint/guard columns. The joint factor simplifies to the four-endpoint identity above and needs no COPY-guard term in the final displayed dual.

`check_full_dual.py` is a separate direct implementation. It initializes the19 residual functionals “arrival minus the displayed endpoint combination” and propagates them backwards through the source. It imports no column-elimination code. All residual coefficients vanish at every one of the28,292 allowed changed states. Changing the sign of the189 endpoint contribution is rejected; granting the additional receiver chart901 is also rejected. Those controls delimit the source-station scope.

The24-cut forward overwrite screen is a third calculation. It explicitly recomputes the changed common observation rank rather than borrowing the old null relations. It records the five real but nonneutral pure-signal gains, so the new exclusion is not obtained by silently forbidding changed observation matrices.

These calculations are source-coupling author evidence, with explicit code reuse as stated. They are not presented as a completed independent review. The root/review worker can authenticate the short four-endpoint dual independently. The theorem does not rule out a different donor detour that visits a receiver chart, a separately transported common record, additional receiver observations, other source-control charts, or a changed native schedule.

All three normal and optimized receipts agree byte for byte. Checks use explicit exceptions and exact rational arithmetic.
