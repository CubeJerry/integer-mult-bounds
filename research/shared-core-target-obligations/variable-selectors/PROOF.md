# Exact exclusion of 19,600 named time-varying selector schemes

**Finite-family endpoint theorem. No new κ.** Every member of the family
below fails the required rational normalized endpoint on one explicitly
generated integer input. No claim concerns all selectors, all shared cores,
all K4 constructions, or the feasibility of κ=1/200 in another architecture.
Optimistic invoice and ordinary-cost estimates are not used or asserted here.

Base: `e54523517d0f03e58352e647c403a5af3e525a57`. Source is
`research/shared-wire-split-composition/data/final.json.gz`, Git blob
`74563a7867d9d762b6588f65362369668841bb3e`, SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.

## Exact finite family

Duplicate all 400 actual main fields and their MOVE, SCALE and main-main ADD
events. Keep one copy of all 1,080 arbitrary public helpers and 51 owned
labels, including every core MOVE/INIT/CLEAR. Core-core operations remain.
For a core←main ADD with coefficient q, use q(w0*x0+w1*x1). For main←core,
add q*v0 times that core value to copy0 and q*v1 times it to copy1. Each
nonzero summand is a literal same-chart ADD. Main copies follow identical
source charts; no source version, contact time or MOVE is relaxed.

For loads and reads independently, select one of the following 14 bits and
optionally complement it. Indices begin at zero. Here c,n describe that
role's directional contacts; k,m describe its combined load/read contacts.

| Index | Bit |
|---:|---|
|0,1|Constant 0 or 1|
|2|c modulo 2|
|3,4|c is first or last|
|5|2c>=n|
|6|k modulo 2|
|7,8|k is first or last|
|9|2k>=m|
|10|Current source-frame dimension modulo 2|
|11|Original event lies in second half of the full word|
|12|Sorted main-role index modulo 2|
|13|c is divisible by 3|

For bit b and s=(-1)^b, independently choose load/read weights among
`(1-b,b)`, `(1,s)`, `(1/2,s/2)`, `(s,1)`, `(s/2,1/2)`.
The parameter domain has exactly 14²×5²×2²=19,600 elements. Different
parameter tuples may denote identical programs; no distinct-word count is
claimed. Data-dependent or arbitrary contact-specific weights are excluded.

The target is two independent copies of the actual selected main map, plus
autonomous original helper returns. The eight coupled ports retain
`(X,Y)->(X-Y,(X+Y)/2)`. The other 96 first-family ports have Y←Y+X, and the
96 second-family ports have X←X-Y, as specified by the pinned source.
None of the public helper inputs is specialized to owned zero.

## Exact counterexample proof and independent verification

Take p=1,000,000,007 and the 1,880 public values generated successively by
Python `random.Random(20261111).randrange(p)`: 400 mains per copy, then all
1,080 helpers. Owned values begin zero and obey the literal source resets.
The full input and target vectors are regenerated and byte-pinned; no
probabilistic correctness claim is needed. One fixed counterexample per
program suffices.

Independent preparation proves p prime by trial division through floor√p,
checks every source denominator nonzero modulo p, and accounts for the new
factor 2 in the weights. Hence reduction defines a homomorphism on all
rational coefficients and input values used. If the rational linear maps
agreed, their reductions would agree on this input. A nonzero modular
residual therefore proves rational inequality. A zero residual would not
prove equality; no case relies on that converse.

The author's C++ interpreter generates the full 19,600-row counterexample
table. An independent implementation then prepares instructions directly
from the authenticated raw word, using a unified register layout, original
frame chronology and independent contact masks. Its C++ interpreter replays
every tuple and checks both the recorded nonzero witness and every complete
main/helper mismatch count. It also verifies all owned outputs are cleared.
No author scientific code is imported into the independent implementation.

Independent preparation checks all binary source frames, every nested MOVE,
every same-chart contact and source version. The sole COPY immediately
follows its destination's INIT; the independent runtime checks its zero
destination in every scheme. The coupled-port targets are rederived from
the source metadata. Every arithmetic product and sum is bounded by
`2(p-1)^2+(p-1)<2^64`; acceptance uses no floating point.

The complete result is 19,600 rejected tuples, zero survivors, 296 schemes
whose helpers happen to return correctly on this input, and minimum 286
incorrect public fields. The fixed selector control has zero active/helper
errors and 286 passive errors. A deliberately altered witness must be
rejected with exit3. The generated witness table's SHA256 is
`5c774b5db931cad2379307b1a97496d96d3501234bd31a77d83a758f61d0746a`;
the original generated screen input's SHA256 is
`de0e0fc24c0b816e3c1ca1aa6de1259ecd0725c2835b64c762b3cc49eb974d65`.

All source compilation, storage, tapes, precision and five foundational
assumptions remain outside this finite rejection theorem. It does not
establish a supplier or rule out finer contact weights, changed charts,
different words, temporal owned storage or other representations. Its
κ=1/200 relevance is limited to rejecting these proposed endpoint mechanisms
before their optimistic price can legitimately be credited.

The family and first screen were prepared by one OpenAI Codex research agent;
the full-domain independent preparation/interpreter and review were produced
by a separate OpenAI Codex agent. This is not independent human or formal
kernel review. Credit the selected #7000 source, DreamingOfClouds, @CubeJerry
and all retained native/caller authors. No novelty claim is made for selector
or signed-copy coding itself. Apache-2.0.
