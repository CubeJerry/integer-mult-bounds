# A fully restored reversible dirty-helper coupling

**Exact finite-source construction on all 1,880 independent inputs. Independently
reviewed in review/REVIEW.md. No new kappa.**

The construction sends private difference q60 through a retained public helper
route to raw receiver213, retains the helper's displaced arbitrary common value
in the raw donor carrier, and restores every common datum. One new rank-1 owned
return transports the private signal back to the hub. This escapes the
no-retained-record premise of the single-overwrite loss theorem.

This channel was already granted by the earlier pure-source routing graph. It
does not evade that graph's54/43 packet lower bounds. Paying for its physical
restoration makes the fixed eight-packet completion more expensive. The record
mechanism and its actual source chronology are the new finite result.

## Source, domain and complete endpoint identity

The frozen native is
`research/shared-wire-split-composition/data/final.json.gz`, compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`, from canonical
commit `e54523517d0f03e58352e647c403a5af3e525a57`. It has1,480 public common
inputs,51 owned labels,71,261 instructions and6,310 MOVEs. Denote its full
public endpoint map by T. The checker derives T from every source instruction,
compares all rows with the declared native endpoint map, and checks its full
explicit inverse.

Let u contain1,480 arbitrary common inputs and v contain400 independent
second-main inputs. A separate public raw field Q_i=q_i=v_i-u_i is formed for
every main role i by a charged entry ADD. In the literal word, Q60 is1535,
Q213 is1677, common-owned labels are shifted by400, and the new owned label
is1931. No arbitrary common input is initialized to zero. The identities apply
coordinatewise to every positive complete-field volume V over a characteristic
zero field admitting the native coefficients. All extra coefficients are
dyadic, drawn from {1,-1,2,-2,4,-4,1/2,-1/2}.

The entire1,880-input endpoint identity of this partial coupling is

    common output = T u,
    second-main output i = (T u)_i + q_i + 1_{i=213} q60.

This explicitly supplies one cross-coordinate update. Receiver213 is paired
with X101 in the complete native; the remaining private-native actions are not
implemented. In particular, recoupling unchanged q_i with (T u)_i does not
normally equal the second native endpoint (T v)_i. The map on private q here
is the invertible shear I+e213 e60^T. Together with the checked inverse of T,
that proves retention of all1,880 independent inputs. All400 final recouplings
are included and charged.

## 1. Actual cochart cuts and chronology

Event numbers are zero-based indices in the original native program.

| Role | Before the swap | After the swap |
| --- | --- | --- |
| Raw Q60 | 26095:56→403;26101:403→418;30761:418→539;41727:539→962 | 42848:962→145;43151:145→127 |
| Raw Q213 | 30832:3→594;30834:594→616;40914:616→906;41720:906→221 | None;221 is its native final chart |
| Common H1024 | Actual common state at962 immediately before41779 | 41779:962→221, rank1 |

Each raw MOVE executes immediately after its corresponding common MOVE at the
original source event occurrence. All1,710 raw reservations are used exactly
once. No raw-route hoisting and no separate second-owned reservation is used.
All original common instructions retain their order, location, ownership flags
and coefficients.

Immediately before41779, Q60 and H1024 are at962, while Q213 is already at221.
The helper's actual common value is h u, with the full260-term row stored in
RESULT.json. It is not an entry input or a free acquired observation.

Execute the cochart reversible swap:

    H1024 += Q60
    Q60   -= H1024
    H1024 += Q60
    Q60   *= -1

Now (H1024,Q60)=(q60,h u). Original MOVE41779 carries the pure private signal
to221. Immediately after that MOVE and before any further native instruction:

    Q213 += H1024
    INIT A at221
    A += H1024
    MOVE A:221→127, owned, rank1

The receiver gain is exactly1. Complete chart221 has dimension8 and is properly
contained in dimension9 hub127. The new MOVE is paid. The observation occurs
before instruction41780, which adds half of common role977 into H1024.

Q60 then follows its two remaining original reservations, carrying all of h u
to127. A carries q60 to127 and remains there through common completion. These
are distinct actual records, retained until they are used.

## 2. Literal response and complete common restoration

The helper substitution injects delta=q60-h u. An independent formal unit pulse
is propagated through the entire actual suffix. Its response z has25 nonzero
public endpoints, all at hub127, and zero response at all other endpoints. The
actual COPY guard at31737 precedes this intervention and has zero response.

| Coefficient | Nonzero endpoint roles |
| --- | --- |
| -4 | 52 |
| 4 | 60 |
| -2 | 1125 |
| 2 | 571 |
| -1/2 | 619,1024 |
| -1 | 301,356,801,1168 |
| 1 | 787,796,797,804,813,817,830,842,843,849,853,868,875,1145,1206 |

At common completion the exact state is

    common = T u + z delta,
    Q60 = h u,
    A = q60,
    Q213 = q213 + q60,
    all other Q_i = q_i.

All25 affected common fields, Q60 and A are cochart at127. Reuse A as the
correction record, requiring no second owned temporary:

    A -= Q60                         # A = delta
    for every nonzero z_i: common_i -= z_i A
    Q60 += A                         # Q60 = q60
    CLEAR A

Every common datum is now exactly T u, the donor is restored and the receiver
gain remains. Finally execute all400 recouplings Q_i+=common_i at the actual
final charts. Every endpoint equation and location is checked.

The single-overwrite theorem does not apply to these retained data: its lost
common mode is physically preserved in Q60. The independent pure-q return is
also retained; omitting it would invalidate this restoration. The260-term h
is outside the span of hub-only terminal common rows, so the special q=λY
formula for hub-recoverable overwrites cannot replace that return.

## 3. Entire word and cost

SWAP-WORD.json.gz contains every physical instruction, all initial charts,
the400-role raw map,1,710 reservation bindings and the physical checkpoints.
WORD-PIN.json pins the decompressed bytes.

| Opcode | Count |
| --- | ---: |
| ADD | 62,012 |
| SCALE | 3,663 |
| COPY | 1 |
| MOVE | 8,021 |
| INIT | 55 |
| CLEAR | 55 |
| Total | 73,807 |

The comparison baseline is the complete71,261-instruction common native plus
1,710 raw MOVEs,400 entry differences and400 final recouplings:73,771 operations.
The increase is exactly32 ADDs, one SCALE, one rank-1 owned MOVE, one INIT and
one CLEAR. The32 ADDs are three swap ADDs, one receiver read, one cache copy,
one delta formation,25 corrections and one donor restoration. The extra
complete recursive moment at t=199/200 is exactly1 per native, before any
outer caller multiplicity.

The source has51 owned labels and54 lifetimes. This word declares one extra
owned label and has55 lifetimes. Its peak live owned storage remains43 because
the added lifetime begins after the source peak; final live owned count is0.
The nonzero owned erasure is charged under the inherited erasure contract.

The full8,021-MOVE rank histogram is
{1:5066,2:1188,3:916,4:353,5:453,6:25,7:14,8:6}.
All6,310 common MOVEs and1,710 raw reservations remain; only the q-return is
new. This word starts at original entry and cannot reuse reservations already
consumed by an acquisition or eight-packet prefix. No complete ordinary,
precision, storage, compiler or recursive supplier theorem follows solely from
these finite opcode counts.

## 4. Reproduction and exact controls

Run from this package with the pinned source path:

    python3 -B verify.py --source /path/to/final.json.gz --output /tmp/swap-replay
    python3 -O -B verify.py --source /path/to/final.json.gz --output /tmp/swap-replay-opt

The checker uses exact Fraction rows, no random tests and no modular-zero
inference. It authenticates the immutable source, derives the baseline and
pulse, generates the physical word, then replays every instruction on all1,880
formal input columns with cochart, proper-nesting, ownership and COPY checks.
It checks all1,480 common endpoint rows and all400 recoupled private rows.

Four changed constructions have explicit nonzero exact error witnesses:

| Change | Remaining error witness |
| --- | --- |
| Erase h instead of retaining it in Q60 | Common52 has coefficient-4 on private input1535 |
| Omit the pure-q return and use zero | Common52 has coefficient-4 on private input1535 |
| Form q60+h instead of q60-h | Common52 has coefficient-1 on common input2 |
| Omit the receiver observation | Receiver1677 misses coefficient1 on private input1535 |

The separate source-filter review finds824 hub-recoverable neutral helper
occurrences,822 arriving directly at127 and two that cannot form a direct
active-X→active-Y swap on the original itineraries. This event belongs to the
other648 occurrences and pays for its q-return. That limited classification
is not a general lower bound on changed encoders or joint records.

## Open next questions

1. Can dirty common records or common-dependent observations supply a weighted
   aggregate outside the earlier pure-coordinate routing graph? This single
   edge is already granted by that graph; scaling it does not evade54/43.
2. Can actual joint record and q-return suppliers reduce paid dimension while
   preserving every displaced datum and original raw duty? Record rank alone
   does not establish chronology, routes or cost.
3. Can a complete affordable private-native endpoint map be composed with this
   restoration, a compatible BIT supplier and all ordinary/precision/storage/
   compiler/recursive contracts? All five foundational assumptions remain.

Credit the native authors, DreamingOfClouds' shared-native lineage, Ali Romman's
helper splitting, @CubeJerry's programme, and its previous single-overwrite,
difference-carrier, active-observation and joint-restoration packages. Prepared
with substantial OpenAI assistance. Independent review is separate. No new
complete kappa or multiplication theorem is claimed.
