# A paid pre-F2 rotation retains the first QQ16 cut

This is an ordered logical construction for **pair 0 only**, conditional on
Ali Romman's retained QQ16 maps. It closes the recorded-cut-to-final-record
implication left open by commdata2338's PR2174 for one explicitly changed
selected schedule. It does not restore all four banks, implement the native
reads, or establish a favorable supplier invoice. **No new κ.**

## 1. Contract

Use the actual eight-port sets A and T and the 96 ordinary ports U in
`research/joint-query/evidence/CONSERVED-QQ16.md`. At chart s write

    B_s = R_s iota_U,     K_s = K_(s,U),     B_s K_s = 12 I.

The selected sections P_(s,A), P_(s,T) have two-sided selected inverses
ell_(s,A), ell_(s,T). They are maps between an eight-coordinate query block
and its indicated selected block. Products below are ordered; different
chart operators need not commute. This includes the retained cover/tensor
operators, not just a common-chart scalar specialization.

Keep all nine local maps and all nine **ordinary-only** bridges of the
source-pinned 19-event recipe. The local bank sequence is
`0,0,0,1,1,2,2,3,3`. A bridge (i,j,c) performs

    X_(j,U) += c X_(i,U),       Y_(i,U) -= c Y_(j,U).

Apply the signed terminal `(X,Y) -> (Y,-X)` on ordinary **and selected**
fields. In particular named final Y_U has the completed-X type; named
final X_U has the former-Y type. These types cannot be interchanged.

Insert the adapter in §2 immediately before F2 on pair 0, after the first
positive ordinary bridge. There are no other selected interventions.
There is no canonical selected-state observer inside the adapter or
between it and F2. The ordinary bridge does not change its selected inputs.
All original X/Y inputs of all four banks are arbitrary, including their
selected entries. The retained local helper contract is inherited.

The decoder may observe exactly:

1. `q0=B0 X_(0,U)^initial`, `q2=B2 X_(0,U)^initial`, and the actual F0
   query f0. These are three retained eight-coordinate query blocks.
2. Pair 0's four final selected blocks, denoted XA, XT, YA, YT.
3. `C=Y_(0,U)^final`, its completed-X ordinary descendant.

There is no post-B1 checkpoint in this observation set, no separately
retained f2, no later forward histories, and no former-Y ordinary read.
Capturing, retaining and accessing these logical observations are paid
obligations, not an assertion of free or automatically clean storage.

## 2. Three paired shears

Set `H=P_(2,A) ell_(2,T)` and `J=P_(2,T) ell_(2,A)`. Two-sided section
identities give `HJ=I_A` and `JH=I_T`. On pair 0 execute in order

    X_A += H X_T;       Y_A -= H X_T;
    X_T -= J X_A;       Y_T += J X_A;
    X_A += H X_T;       Y_A -= H X_T.

Each pair of updates has an unchanged source, so its two ADDs can run
sequentially. Every X_p+Y_p sum on A or T remains invariant. If the entry
values are `(a,t,b,d)=(X_A,X_T,Y_A,Y_T)`, the exact exit is

    (H t, -J a, b+a-H t, d+t+J a).                 (1)

This is a conserved quarter-turn, not an unpriced renaming of fields.
The inverse reverses the six ADDs and negates their signs. Formula (1)
and its inverse hold for arbitrary dirty values of all four blocks.

F2 next writes `X_A^F2=P_(2,A) ell_(2,T) X_T^entry`, hence

    X_A^F2 = H(-J a) = -a.                        (2)

It writes `X_T^F2=P_(2,T) f2`. No later local call or selected operation
touches pair 0 until the signed terminal. Therefore

    YA = a = X_A^B1,       YT = -P_(2,T) f2.       (3)

The pair sums are conserved until that terminal. Thus, using only final
selected values, recover

    p_A = XA-YA,               p_T = XT-YT,
    d_A = Y_A^B1 = p_A-YA,     f2 = -ell_(2,T) YT. (4)

This proves the new retention implication. In particular d_A is
`XA-2 YA`, with the signs dictated by the specified terminal. Moving
the adapter after F2, changing its chart, or omitting its Y corrections
does not have this contract.

## 3. Reconstruct the original selected inputs

Write `z=X_(0,U)^initial` and `w=Y_(0,U)^initial`. After F0 the ordinary
pair is `(z-K0 f0, w+z-K0 f0)`. B1 subtracts these and leaves X_U=-w.
The positive bridge, F2 and negative bridge change X_(0,U) in total by
`-K2 f2`; the other bank's contribution cancels. No later event writes
X_(0,U) before the terminal. Consequently

    C = w + K2 f2,       B2 w = B2 C - 12 f2.      (5)

The adapter changes the actual f2; (5) uses that changed value. The
symbolic tail checker treats all forward histories and backward drivers
as independent symbols, and binds the **entire** recipe to its archive.
This is not the invalid shortcut assigning F2 to bank 1 or F8 to bank 0.

Let t be the transient F0 A output, not an observation. The retained F0
and B_(1,2) future logger imply

    t = p_A-d_A + P_(2,A) [
          B2 C + q2 - 12 f2 - B2 K0 f0
          + ell_(2,T)(p_T-P_(0,T) f0) ].           (6)

For completeness, before B1 its Y source is
`Y_U=w+z-K0 f0`, `Y_A=p_A-t`, `Y_T=p_T-P_(0,T) f0`.
The future logger adds `P_(2,A)(B2 Y_U+ell_(2,T)Y_T)` to Y_A.
Solving for t, substituting q2=B2 z and (5), gives (6).
This is the credited PR2174 decoder with the new final-record inputs
(4), and B2K2=12I applied before materializing an ordinary workspace row.

Now recover all four original selected blocks of pair 0:

    X_T^initial = P_(0,T) ell_(0,A) t,
    X_A^initial = P_(0,A) [f0-q0-ell_(0,T) X_T^initial],
    Y_A^initial = p_A-X_A^initial,
    Y_T^initial = p_T-X_T^initial.                 (7)

The first equation uses F0's old-T-to-A transfer. The second uses its
full query `f0=q0+ell_(0,A)X_A^initial+ell_(0,T)X_T^initial`.
No ordinary query or cross-chart response is inverted. Equations (1)--(7)
give a linear decoder D with `D O=J0`, where O is precisely §1's
observation operator and J0 selects pair 0's original selected entries.
Thus `ker O` is contained in `ker J0` for all admissible inputs.
This is a written ordered proof, not a finite-rank inference or a
proof-assistant theorem.

## 4. Relationship to the final-only obstruction

PR2346's unchanged schedule has an actual-cover family with post-B1
selected pair `(X_A,Y_A)=(-d,d)`, `X_T=Y_T=0`, and d nonzero.
Its subsequent F2 erases that visible selected state. In our changed
schedule (3) gives `YA=-d`, so the family is detected. This does not
contradict the predecessor's theorem: its explicit hypothesis excludes
interventions before F2. Its common-chart finite fixture is also replayed
here: old allowed observations all vanish, initial X_A=-1, whereas the
repair produces final YA=1 and f2=-2.

This is also outside PR2306's selected-only obstruction without the
extra input records. We **retain** the q0/q2/f0 observations; no claim is
made that the quarter-turn alone restores the QQ16 controller. We do not
identify this word with the separately mentioned historical first-six-swap
controller, whose full selected program is not a dependency here.

## 5. Complete conditional cost and dirty scratch

Let one query block have eight length-L fields. For every fixed-port
additive operation F, let C_F(L) be a complete price including source
and coefficient access, recursive descendants, target updates, scratch
restoration, frame/cover conversion, routing, head returns and dispatch.
Use an upper price over every actual sign, port and incoming frame in
this word; exact port-dependent invoices must sum the actual invocation
prices instead. A logical map name does not equate X and Y native costs.

The adapter makes **four H ADDs and two J ADDs**. If these compound maps
are unavailable, each can be implemented conditionally from additive
selected-section/readout children. For F=P ell, with a distinct borrowed
dirty query block z, use

    z += ell(source); target += sign*P(z);
    z -= ell(source); target -= sign*P(z).

The unchanged source and linearity cancel every coefficient of initial
z. The net effect is `target += sign*P ell(source)`. All child-private
scratch must exclude these ports and restore on return. Reuse z only
after the complete echo. This construction needs **one borrowed dirty
query block (8L entries), not a clean block**. It does not require an
additional persistent d_A snapshot. Its six echoes contain exactly

    8 ell_(2,T) + 8 P_(2,A) + 4 ell_(2,A) + 4 P_(2,T)

complete additive children, **24 calls**, including every inverse and
scratch restoration. This is a call count, **not 24 native rank units**.
The 40-column check on the actual scalar minors verifies the entire
adapter, its scratch output and both inverse orders. It does not execute
the cover maps inside these operator-valued children.

A complete conditional recurrence for this modified 19-event controller
and the pair-0 reconstruction is

    T(L) <= I(L) + P(L) + Program(L)
          + sum_(9 local events) T_local(L)
          + sum_(9 ordinary bridges) T_bridge(L) + T_terminal(L)
          + 8 C_ell2T(L) + 8 C_P2A(L)
          + 4 C_ell2A(L) + 4 C_P2T(L)
          + Capture_q0(L) + Capture_q2(L) + Capture_f0(L)
          + Retain(L) + Read_B2C(L) + Decode_small(L)
          + Release(L) + Extra_control(L).                         (8)

I admits all data, the borrowed block and child workspace; P prepares
operators/constants; Program pays instruction construction, storage and
reads. Capture and Retain pay the three input/history records and their
actual lifetimes. Owned record buffers need paid initialization/clear;
borrowed buffers require a separately proved reversible logging contract.
Read_B2C pays the one ordinary query from the completed-X endpoint.
Decode_small executes precisely (4), (6), (7), paying every selected
map, ADD, scaling and output write. Its ordinary map B2K0 may be executed
as two complete maps, never a free precomputed product. Its temporary
storage, old input preservation and cleanup belong in Decode_small and
Release. There is no separate f2 capture. Extra_control includes any
additional reservation, frame, precision or tape work not already charged.
Each child cost in (8) recursively expands under that child's actual
contract; no parent expense is removed by changing notation.

Relative to a controller that physically saves and later retrieves d_A,
this trades that checkpoint's capture/retention/cleanup cost for the
adapter, its borrowed-block lifetime and final-record decoding/access.
The common q0/q2/f0 captures, local calls and ordinary tail remain paid.
Any useful supplier substitution additionally needs the intended full
data map, not just recovery of selected inputs: f2 and ordinary endpoints
can change here. It also needs the **complete** added costs to be smaller
than eliminated checkpoint costs. Neither condition is established for
the selected supplier. In particular neither q0/q2 retention, arbitrary
P/ell child availability nor access across the X/Y native frame mismatch
is supplied by the logical identities. All-size hosting, precision/tape,
native realization and the other three banks' recovery remain open.
This stops at a verified retention lemma rather than installing an
unpriced exponent improvement.

### A literal, fully inventoried decoder

The executable does not hide the algebraic decoder in an unpriced inverse.
It also emits an out-of-place decoder, with readonly observations and
four **owned** output query blocks. These outputs may be initialized by
paid CLEAR; their previous contents are not borrowed state to restore.
It uses two owned query temporaries m,v and one owned ordinary temporary u.
For the actual geometry these occupy `2*8+96=112` coordinates per owner,
in addition to `4*8=32` output coordinates. All three temporaries finish
zero, after paid clears. This deliberately simple implementation is not
a low-memory claim and may be unsuitable for a supplier.

Eliminating d_A and f2 in (6) yields

    t = YA + P_(2,A)[B2 C + q2 - B2 K0 f0
                    + ell_(2,T)(XT+11 YT-P_(0,T) f0)].       (9)

`algebra.py:decoder_program` executes (9), then (7), as 35 events:

| Complete operation | Calls |
| --- | ---: |
| B2 additive query | 2 |
| K0 additive injection | 1 |
| P_(0,T) additive map | 2 |
| ell_(2,T), P_(2,A), ell_(0,A), ell_(0,T), P_(0,A) | 1 each |
| Plain query-block ADD | 11 |
| Query-block ADD with coefficient -11 | 1 |
| CLEAR of an owned query block | 11 |
| CLEAR of the owned ordinary block | 2 |

Thus Read_B2C + Decode_small in (8) can be instantiated by these **10 mapped ADDs,
12 scalar-block ADDs and 13 CLEARs**, plus admission of all 144 owned
scratch/output coordinates, coefficient access, dispatch, frame/routing,
precision and output delivery costs. The coefficient -11 is charged,
not treated as a unit ADD. No intermediate B2K0 product is precomputed.
The capture/retention costs of q0/q2/f0 remain separate. The exact finite
models check all 240 bank-input columns plus 54 independent owned-dirt
columns across the three models. Every one of the 35 event omissions
violates either recovery or a declared zero scratch endpoint.

## Credit

Ali Romman / PR1969: QQ16 local words, ordered maps and native contract.
commdata2338 / PR2174: two-query recorded-cut decoder and ordinary tail.
alephnan / PR2346: actual-cover final-record obstruction and pre-F2 handoff;
Philippe Van Velzen: its credited earlier four-bank finite-model failure.
Adam Gall / PR2093, Ross Richardson / PR2104, Cinna Davis / PR2216 and
the PR2306/2326/2350/2354 lines retain credit for adjacent kernel, shear,
tap and audit work. The four-child dirty echo is established repository
machinery, not new algebra here. The retained compiler, owner schedule,
selected suppliers and their contributors retain their existing notices.

New contribution by @CubeJerry with substantial OpenAI Codex assistance
in derivation, implementation, verification and writing. Apache-2.0.
No independent human or formal-kernel review is claimed.
