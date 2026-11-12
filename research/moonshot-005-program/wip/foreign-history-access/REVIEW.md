# Independent review of the null-route E8 packet vector

**Exact vector and source-access facts independently checked. The proposed
foreign-history mechanism remains WIP. No new κ.**

The review used a separate inline Python calculation, without importing or
executing `prepare.py`. It loaded the pinned native word, reconstructed complete
binary chart spaces, and independently formed all 104 integer packet rows from
the nine-dimensional roots `1_S−ones/3` and `e_i−e_j`, using
`a_k=2r_k+r_9`. Those rows exactly equal the actual `eight-packet-prefix` word's
rows in the same donor order.

## Verified facts

Let d have entries

\[
 d_{77}=1,\quad d_{10}=-1,\quad d_{16}=-1,\quad
 d_{20}=1,\quad d_{26}=1,
\]

and all other entries zero. For the actual eight-packet matrix C, all eight
coordinates of Cd are exactly zero. In particular, this is an exact packet
kernel vector with `e77 d=1`, not a numerical near-null vector.

Each supporting donor's entire original raw itinerary lies in receiver189's
admitted 220-station null set. The checked literal routes are:

| Donor | Original route charts |
| --- | --- |
| 77 | 71, 312, 324, 232, 127 |
| 10 | 10, 270, 285, 851, 980, 133, 127 |
| 16 | 15, 479, 497, 498, 127 |
| 20 | 19, 500, 515, 516, 477, 127 |
| 26 | 24, 426, 436, 243, 127 |

Membership was tested by complete binary spaces, not integer labels. The
independent census also reproduces all 46 null-route donors, all 48 nonzero
foreign correction coordinates, and the 27 coordinates having at least one
original route station outside the null set. The entire `INVENTORY.json`
coordinate list agrees. The separately claimed eight-row basis rank in
`NULL-ROUTE-PACKET-TEST.json` was not needed and is not admitted by this review.

## Sharply scoped consequence

Consider the fixed native common word with linear, common-input-independent
private additions. For each donor j, the q_j-dependent control column may act
only at stations on that donor's original raw itinerary. Grant all such access
and caches freely, but no new stations, new carrier observations, or additional
private S information. Allow initial common correction `VCq`, grant the receiver
the eight packets Cq, and require common endpoint189 to be restored to its
original value. The receiver's records are the declared native initial and
MOVE-arrival histories and those packets.

Under these restrictions, receiver189 cannot recover `u77+q77` for every
independent common and private input, even with a nonlinear decoder of those
records.

Here is the exact restricted-displacement argument. Write the histories as
`Ou+(OVC+B)q`. Along d, the precompensation vanishes because Cd=0. Every
potentially nonzero control variation is confined to the 220 null stations,
since every supporting donor route is inside them. The admitted complete
history-nullspace certificate therefore gives `NBd=0`, even if foreign control
columns outside this support have nonzero NB. Hence `Bd` lies in `im O`;
choose v with `Ov=Bd`.

On this particular displacement, all control variations are also disjoint
from the receiver itinerary. The actual endpoint-minus-initial history
functional D0 remains valid. Endpoint restoration and Cd=0 give `D0Bd=0`,
so `e77 v=0`. The two inputs `(u=0,q=d)` and `(u=v,q=0)` have identical native
history and packet records, but their target values differ by `e77 d=1`.

This is the packet-gain reduction applied to a specific supported kernel
direction. It does **not** set the full foreign matrix NB to zero. The 27
outside-null foreign coordinates cannot eliminate this particular ambiguity
under the stipulated per-donor access, because their coordinates in d are zero.

## Limitations

The argument changes if extra private information Sd is nonzero, if further
packets distinguish d, or if q-dependent writes can leave a donor's original
stations. In particular, common-dependent cross-donor feedback may propagate
dependence to other stations and is excluded here. New carrier histories,
changed common processing, or common-dependent replacement changing O also
require a new analysis. The direct-17 construction supplies additional private
information and is not contradicted. A different packet matrix need not have
this kernel vector.

This review does not supply a positive history-gain witness, a physical cache
schedule, complete restoration for a new code, or a price improvement. The WIP
inventory remains exploratory. The scoped indistinguishability deduction
retains the previously admitted complete-history and endpoint-representation
theorems; their source checks were not rerun during this short review.

## Exact files checked

All paths below are relative to `research/moonshot-005-program/`, except the
native source. SHA256 values bind the examined bytes.

| File | SHA256 |
| --- | --- |
| `wip/foreign-history-access/prepare.py` | `fd623f13b8c0bcb2d59d082fbf23a20ff0c775dbc646f300ec5e5882010e26ae` |
| `wip/foreign-history-access/INVENTORY.json` | `87197ab352408bc40231df54ac749241bdb36ba7da12b3e3ca6b4f1d300dbeb8` |
| `wip/foreign-history-access/NULL-ROUTE-PACKET-TEST.json` | `5f8c4fe8849f0343007f8dd57ec34aecf7830ec01fba8a24664a2d2e46da52f2` |
| `results/joint-additive-history-obstruction/CERTIFICATE.json` | `168fee8f09cdf0f33bcf5989630d244141d3c570808b7ccb553f6ad7be098dd7` |
| `results/eight-packet-prefix/PREFIX.json.gz` | `e0756b92f7507499cc271411beb08c4b8b1070c45efbf49036f3d5fd360022b5` |
| `results/packet-gain-reduction/PROOF.md` | `51bed76021f5007d39b09cc31ebf5c4cafa3f67290b78947a4e915e3a4d8827e` |
| `results/packet-gain-reduction/GENERAL-INTERFACE.md` | `455b94859d24c5ef2367bd40ca68fc7e60413680a2a4e908d318f63c4e525dd2` |

The compressed native source SHA256 is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The inherited joint-history admission SHA256 is
`1d9d2047a3dbc3b20225e0ee490347b69f03757de8747ed05f932ffb52e78097`.

Prepared by the independent S006 adversarial worker; no author code imports.

## Final pin correction

The author corrected `outside_initial_station` from integer-label membership
to full binary-space membership, `C[w["initial"][x]] not in null`, during
publication. I inspected this one-line semantic correction and independently
rechecked every regenerated inventory route, outside-station list and initial
station flag using complete spaces; all 48 rows and the 27-outside count pass.
The hashes in the table above now bind that corrected author version. The old
prepare.py hash was `544bb93d0fcb92427016dd566941909f70e50812e8125d9f72717e1fc64f6736`;
the previously recorded inventory hash was
`87197ab352408bc40231df54ac749241bdb36ba7da12b3e3ca6b4f1d300dbeb8`.
The independent scientific check already used full-space semantics, so the
packet-null vector, route inclusion and scoped deduction are unchanged.
