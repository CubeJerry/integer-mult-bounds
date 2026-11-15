# Exact closure gaps for the frozen eight-packet history

**Proved, source-specific information statements. No completed source,
decoder, supplier or new kappa is asserted by the algebraic completions.**

The source is the frozen actual eight-packet word independently reviewed in
`EIGHT-REVIEW.md`. The later three-output continuation retains the same
packet values, but its seven new D8 caches are additional observations and
must not be silently excluded when applying this result to that continuation.

## 1. Fixed spaces and exact conclusion

Work on the authenticated 111 native real roots r_i. Write

- F_i = r_i-perp for the real receiver facet;
- L_i = span over F2 of e_j with r_i dot r_j = 0 for its freely granted local
  original-input information;
- K_i = e_i + sum_{j != i, r_i dot r_j = 0} e_j;
- C = span{K_i}, the rank-nine canonical code;
- W for the rank-fifteen singular split code at pivot 38;
- G for the span of all actual packet values after departure from Hub;
- T for the span of the eight actual terminal ground packet values.

Independent replay gives dim G=18, dim T=8, dim(G intersection W)=11 and
dim(G intersection C)=7. In fact

    G intersection C = span{K1,K3,K5,K10,K11,K15,K30}.

These are exactly the seven original canonical seed rows. The masked
historical values create **no further canonical dimension**. Also
dim(T intersection C)=4.

The following table grants the entire base space globally and grants every
local L_i freely to receiver i. This is a relaxation of actual routing.

| Base information | Receivers already fitting | Allowed enlargement | Necessary and sufficient added dimension at width V |
|---|---:|---|---:|
| G | 38 of 111 | G+W | 4V |
| G | 38 of 111 | G+C | 2V |
| T | 14 of 111 | T+C | 5V |

The last column is the dimension of additional **global linear information
modulo the base**, not the number of physical packet lifetimes. A packet
may export a value and later change; history and terminal rank differ.
Conversely, granting history globally does not provide a time-respecting
way for a receiver to read it. Each enlargement restriction is essential:
the 4V bound inside G+W does not constrain additions outside that space.

The statements hold for every characteristic-two field K, every positive
width V and arbitrary matrix coefficients on K^V. No commutativity of block
coefficients is used. Any nonlinear decoder of the same linear observations
is subject to the same information obstruction.

## 2. Full-history impossibility certificate

A receiver can recover x_i from globally known rows B and all its local
inputs precisely when some b in B agrees with e_i on the complement of F_i.
This is a finite exact binary linear equation. All 111 equations are checked
with either an explicit fitting-row coefficient mask or a dual input vector.

For example, for receiver 8, put the same arbitrary nonzero v in K^V at
original input indices

    {8,29,69,72,84,86},

and zero elsewhere. The corresponding binary dual vector is
`0x5001200000000020000100`. Its support contains no local input of F8, every
row of G vanishes on it, and x8=v. Thus even a decoder granted all historical
G and all local originals cannot recover x8. The receipt contains analogous
certificates for all 73 failures. These are genuine all-field counterinputs,
not a failed numerical search.

With T in place of G, 97 receivers fail the same test. For the frozen live
handoff, records already located inside a receiver's downset carry only
local input combinations, apart from the globally granted terminal packets.
Thus the T test also obstructs completion without additional nonlocal
observations entering that downset. Descending a new cache, loading another
packet, introducing a Y relay or changing the source can supply new
observations and is not excluded.

## 3. Quotient proof, including arbitrary block coefficients

Let B be G or T, let H be one of the stated enlargements, and let Q=H/B.
Choose a known fitting row a_i in H: the singular A_i for H=G+W and the
canonical K_i for the other two cases. Its quotient class is q_i. Define

    J_i = image in Q of H intersection L_i.

Every fitting row in H lies in the affine space a_i+(H intersection L_i).
Consequently, if E is the quotient of added global observations, receiver i
requires

    q_i in E+J_i.

At width V this becomes q_i tensor K^V contained in
E+(J_i tensor K^V). A binary kernel and image scalar extend exactly to K,
so the same quotient description holds over every characteristic-two field.
For arbitrary block observations, E is simply their full row space in
Q tensor K^V; this includes noncommuting V-by-V coefficients.

Start with F=0, a subspace already known to be contained in E. Whenever
J_i is contained in F, the receiver equation forces q_i tensor K^V into E.
Add q_i to F and repeat. The receipt stores each step, its previous forced
basis and its local ambiguity basis. This procedure forces the whole Q in
all three cases. It proves the lower bounds without enumerating only binary
candidate decoders. Supplying a basis of Q globally is algebraically
sufficient, proving exactness of the information gaps.

For G+W, the quotient has dimension four. Receivers 8,32,59 have no quotient
local freedom and force independent classes 1,2,4. Receiver 61 requires
class 8 with local ambiguity span{4}; that ambiguity has already been
forced, so class 8 is compulsory too. Thus every completion remaining inside
G+W adds four dimensions per width. The explicit sufficient proper modes are
hK10,hK30,hK61,K_b, where b=(0,0,1,1,0,0,1,-1).

For G+C, receivers 8 and 59 force independent quotient classes, giving 2V.
For T+C, the stored receiver sequence forces all five quotient dimensions,
giving 5V. The terminal result prevents replacing the two historical
directions by two fresh ground directions while ignoring lost seed values.

An arbitrary decoder cannot bypass these statements: if a required linear
output is not in the observation row space, a vector in the observation
kernel changes that output. Equal observations on two different required
outputs exclude every deterministic decoder, linear or otherwise.

## 4. Proper canonical additions and their exact limits

Exhausting all 511 nonzero binary words of C gives exactly nine properly
real-supported words. Each has rank-seven support and equals the contact
mode K_c of one of the nine omitted root normals. The other 502 words have
real rank eight. Rank-eight claims have exact mod-107 lower certificates;
the nine rank-seven claims have matching rational normal upper certificates.

This finite classification is exhaustive for the fixed code. It extends to
arbitrary characteristic-two fields: expand any coefficient tuple in a
finite F2-basis of its scalar span. Its binary component words have support
contained in the same real chart. Each proper chart therefore has the scalar
extension of its binary local code, not new hidden field-dependent modes.

The nine words map to all three nonzero classes of (G+C)/G, as well as zero.
One concrete independent pair is

    b = (0,0,1,1,0,0,1,-1),
    c = (1,0,0,1,1,0,0,1).

Their source supports have sizes 56 and 59. Their exact row encodings are

    K_b = 0x2d25f094b54994c6a97fe6569133,
    K_c = 0x785a3c5878d2b55feab32ab33266.

G+K_b fits 60 receivers; G+K_c fits 68; G+K_b+K_c contains all 111 canonical
fitting rows. The receipt supplies a coefficient mask for every one of those
rows in the stated 20-row basis. Neither single addition is sufficient.
Replacing G by T is a further negative control and does not give complete
fitting. These two modes are an algebraic alternative completion target;
their physical acquisition and historical delivery are wholly open here.

Among the 69 properly supported singular W words, K_b is the strongest
single addition to this frozen G: it increases the relaxed fitted-receiver
count from 38 to 60. This is a finite source-specific selection criterion,
not evidence that acquiring K_b is cheap or that a greedy strategy completes
the programme. The existing first-exit gate constrains a particular pure
facet acquisition basis; recoded multi-chart histories and changed bases
remain available.

## 5. Verification, scope and next use

`history_bridge_check.py` replays the frozen word using Worker C's independent
engine, constructs all spaces from root coordinates, proves the rank and
quotient certificates, enumerates the whole canonical code and checks the
111 complete algebraic fitting representations. Its only imports are the
independent Worker C utilities. It does not execute the author's verifier.

```sh
python research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-c/review-a/history_bridge_check.py --source research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json --word research/moonshot-005-program/work-in-progress/2026-11-15-S014/worker-a/eight-output/WORD.json --output /tmp/history-bridge-independent.json
```

Expected status: `PASS_EXACT_HISTORICAL_TERMINAL_BRIDGE`. The proof concerns
the pinned root source and frozen literal packet history. New cache
acquisitions or receiver side information require recomputing it. The next
construction must either acquire and deliver the remaining singular modes,
or provide actual canonical historical observations and the necessary
receiver contacts. Full recursive cost and all retained foundational
assumptions remain unresolved. **No new kappa.**
