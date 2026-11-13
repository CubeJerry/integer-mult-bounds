# An actual rank-nine binary private rail and the fixed-even-m sharing interface

Status: exact finite scalar source construction and conditional accounting
lemma; independent review pending. No complete Q, strict supplier or new κ.
The source is the actual111-port rational-chart BIT native, not the complex
native's96/104-port binary-chart contact graph.

## Source and fitting

The retained native gzip has SHA256
51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.
Its659 public roles comprise111 X,111 Y and437 helpers. Its scalar map over
F2 is X=x, Y=y+x, H=h, with237 explicit owned lifetimes. X_i starts on a
real one-dimensional E8 root line and ends at the full8-chart. Y_i starts
at0 and ends at the7-dimensional real orthogonal facet of that root.

Normalize the111 source roots to unit norm as g_i. Their doubled roots
v_i=2g_i have integral coordinates and norm4. Every inner product v_i.v_j
is even. Define over F2

    B_ij = (v_i.v_j/2) mod2,    K=J+B.

Exact elimination on this finite source gives rank(B)=8, rank(K)=9 and
K_ii=1. For i!=j, K_ij=1 precisely when g_i and g_j are real-orthogonal,
which is exactly the actual original line-to-facet contact relation. The
rows, a nine-row encoder basis, and all decoder masks are retained in
RAIL-RESULT.json. This is an exact source construction, not an assertion
that every E8 subset has those ranks. The odd denominator division problem
of reducing the complex Gram is absent: v_i.v_j/2 is an integer before
reduction, and no 1/2 scalar is used in the emitted binary word.

## Literal partial rail

Move all111 original X inputs directly to the full chart (111 rank7 calls).
For each of the nine actual encoder rows, initialize one owned field there,
XOR the designated current X inputs into it, move it to0 (one rank8 call),
perform every designated Y update, and retire that field under the inherited
owned-erasure contract. The same owned label is reused only after retirement.
Finally move each Y directly to its final facet (111 rank7 calls).

The1267-operation word has222 independent public inputs,231 MOVEs, nine
retired lifetimes and peak owned count1. Its exact map is

    Q(x,y)=(x,y+Kx).

The desired native main map is F(x,y)=(x,y+x). Its foreign residual K+I
has rank108 and6470 nonzero coefficients. None is waived. No unchanged
source history or helper value is consulted by this word. In particular,
the separately extracted X-only subword's clean intermediate values are
not clean values of the full native: helper contamination prevents that
identification. A new use of that subword must construct and price it as
an independent circuit.

All introduced MOVE pairs are exactly nested in the authenticated rational
geometry. This does not itself establish every all-width physical map,
compiler or precision contract. Nonzero owned erasures remain charged and
retain the framework's owned_erasure assumption.

## Fixed-m sharing lemma

For any fixed integer m>=2 and any compatible linear main map Q with the
same entrance and exit charts as F, keep one common native with its437
helpers and m-1 independent private main banks. At their initial charts,
XOR all private main banks into the common main bank. Run the common native
and each independent Q, preserving every arbitrary helper input. At final
charts XOR the resulting private banks out of the common main bank. The
result is

    common = F u_0 + sum_(k=1..m-1) (F-Q)u_k,
    private_k = Q u_k,     common_helpers = h.

This follows by linearity at the two actual cocharted coupling times. It is
valid over every characteristic-two field and for tensor block volume V
whenever the native and Q interfaces themselves hold at that V. Thus if Q=F
on the whole required interface, this implements m correct main copies while
using one helper bank. If Q is partial, the displayed errors remain in both
common and private outputs. Sharing cannot erase them.

The emitted m4 word literally instantiates this construction with the partial
nine-packet Q. It has1325 independent inputs,39270 operations,3564 MOVEs,
264 retired lifetimes and peak237. The native's three SWAP instructions
exchange whole (chart,value) role labels, as in its retained checker; they
are not assumed free value transfers between differently located fields.
All1325 input directions and final charts are replayed exactly. The common
error is the sum of three actual private residuals.

## Complete conditional E-free caller invoice

The existing E-free root caller pairs two actual111-port natives at each of
18 stages. To retain it, use a fixed even m, pair the m main copies in the
same way, and share one native per stage by the lemma. Odd m is not granted:
the inherited odd q-degree determinant obstruction remains.

Let N be the actual native paid histogram, H its437-helper target histogram,
and P2,T2 the complete existing paired caller. They are exactly

    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10},
    H={2:1,4:25,6:1,8:410},
    P2=36N+444[1]+444 sum_(j=1..8)[7j],
    T2=36H+222[127]+444 sum_(j=1..9)[1+7j].

Brackets denote rank histogram atoms, not moment powers. If and only insofar
as Q supplies the required complete main native contract, the resulting
complete profiles are

    P_m=(m/2)P2-18(m-1)N+18(m-1)Q_paid,
    T_m=(m/2)T2-18(m-1)H.

Every outer query/idle, common native, private rail and lost helper credit is
included. Added cocharted XOR work and owned storage require a fresh ordinary
compiler recount; no fixed allowance is silently inherited for arbitrary m.
Every theorem here fixes m independently of n.

At t=199/200, write M2=(T2-P2)_t<0. The complete target inequality is

    (Q_paid)_t < (N-H)_t + m*M2/(36(m-1)).

The limiting Q allowance is1621.750880211152355246... . The actual partial
Q histogram {7:222,8:9} costs1610.208873484099834342... . It leaves at most
11.542006727052520903... for completion as m grows; at fixed m4 it leaves
7.430310278604931634... . These are rigorous128-bit directed integer200th-root
intervals, stored as rational endpoints in BUDGET.json. The provisional m4
moment is positive only before paying for the missing6470 foreign
coefficients. It is not a productive-target certificate for the partial word.

For comparison, using both complete extracted X and transposed-complement
Y routes without fusion would cost
2*(289+244*2^t)+9*8^t=1621.878575781893902662...,
already above the limiting allowance by about.127695570742. That candidate
needs route fusion even if its correction map can be constructed. The latter
is open and is not established by this partial packet word.

## Verification and remaining obligations

Run build_bit_nine_rail.py --repo REPO --output OUT --multiplicity 4.
It authenticates the native, replays all659 native inputs, reconstructs K,
emits/replays the222-input Q and1325-input m4 word, checks exact nested MOVE
pairs, and computes every displayed histogram and directed rational bound.
Independent source/caller review and meaningful mutants are requested.

Needed next: an actual globally compatible current-row decoder for K+I whose
complete extra cost fits the fixed-m allowance; then full physical all-width
admission, owned/ordinary/precision recount, strict covered and ordinary BIT
bootstrap above.005, and a compatible strict complex supplier. All five
framework foundations remain. No new complete κ.

Credit: @CubeJerry programme, paired-query-only BIT and underlying native/root
authors, including DreamingOfClouds, zxv and retained predecessors; root's
binary fitting and sharing construction, worker C independent audit pending.
Substantial OpenAI-assisted research; source notices are preserved.
