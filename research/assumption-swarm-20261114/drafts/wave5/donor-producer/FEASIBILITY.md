# Actual donor1349 production before the first owned1526 subtraction

Status: source algebra and exact ABI/budget feasibility complete; no new
tape implementation has started. Canonical base remains
`e54523517d0f03e58352e647c403a5af3e525a57`. C4 is frozen separately.

## 1. Exact source and the missing implication

The authenticated selected source has:

| Index | Actual event |
|---:|---|
|28037|`INIT 1526 601`|
|28038|`ADD 212 449 1/2 3`|
|28039|`MOVE 1349 3 601 false`|
|28040|`ADD 124 212 1 3`|
|28041|`ADD 1526 1349 -1 601`|

Frame3 is empty and frame601 is`[137]`. Owner1349 is public. At INIT,
1349 is still in frame3; at the SUB it must contain its actual frame601
image. The two unrelated ADDs touch neither1349 nor1526. They remain
explicit paid continuations, with the actual source order unchanged.

C4 implements INIT and SUB but supplies the donor's post-MOVE packet at
the SUB boundary. This wave should remove exactly that post-MOVE-value
premise: begin with the actual pre-MOVE packet of1349, execute its literal
source-frame transformation on the same external HOME, restore its borrowed
work, then feed the unchanged first SUB. The pre-MOVE packet's acquisition
and the two unrelated ADDs remain caller work. This is a real source
producer-to-consumer relation, not another arbitrary provided-packet lemma.

## 2. Exact machinery and source pins

Live #7561 head is`f2f5130ec84f6a0fc81dbfec9a287909500aa80d`, branch
`research/literal-fixed-rank-positive-native-20261113`, open, based on e545.
Its proof in`research/literal-fixed-rank-positive-native/implementation`
implements positive central C on any fixed rank1..9, with joint cutoff.
It expressly does not implement surrounding monomials or a complete MOVE.
Therefore it provides the central service, not a ready-made frame137 core.

Already frozen literal kernels suffice:

| Role | Commit / source |
|---|---|
|General fixed-word CNOT emitter and transaction helpers|#7564 `caba500cefa8d1745a187e60198a97b2647e2e90`, implementation/rank2.py|
|All-column binary maps, matrix-to-fixed-word compiler|`39b40c465f7636a4bb6d70af28595fe8f70f4f3f`|
|All-column fixed quadratic phases and exact source frame engines|`172f4535ce8dcff79f626410af845f757c1563be`|
|Positive first-slot C with actual f<=cutoff guard|`1a555e469b89af70d309bc966f8f813ac11dc887`|
|C4 delivery/SUB/owner interface|Frozen protocol SHA`c324967962e04a125bbdb5f503d3d6c3cff5d7eb69343443bc6ea4338af243bd`; remote pin pending parent publication|

The source archive hash remains
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`,
canonical word hash
`91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097`.
C4's exact full interval already retains the three source gap events.
No source owner, chart, sign or index is inferred from an old recipe label.

The239 core is not reused as137. A new fixed source-specific factor sequence
will call unchanged generic kernels. No generic phase, map, affine translator
or positive-C algorithm needs to be rebuilt. The #7561 all-rank theorem and
#7559 closure remain credited predecessor work.

## 3. A direct five-factor circuit and independent kernel

Let

`G=(3,4,8,17,32,64,128,1,256)`

be its binary row list and let

`Q=(128,0,0,128,0,0,0,9,0)`.

The canonical source frame circuit is, chronologically,

`D, G^-1, C0, G, D`,

where `D|x>=(-1)^(x7(x0+x3))|x>`. D is self-adjoint, all linear alpha
coefficients and its absolute phase are0, and no affine offset occurs.
The first column of G is137. One retained matrix compiler emits21 CNOTs
for G; reversing that same word emits G^-1 in21 gates. The full fixed
map work is therefore42 CNOTs per f-column layer, not the239 maps.

The exact operator has a particularly useful direct oracle. Write
`P=X_137 Z_9`, with Z9's sign `(-1)^(x0+x3)`. Since137 has even overlap
with9, P is a Hermitian involution. Conjugating X0 through G and D gives
P, hence

`T601 = ((1+i)I + (1-i)P)/2`.

For every native basis address x its two outputs are x with coefficient
`(1+i)/2` and `x xor137` with coefficient
`(-1)^(x0+x3)(1-i)/2`. This binds absolute phase, not just Pauli action.
For f=1 packed MSB address order, the address xor is290 and the sign mask
is288. A verifier can use these direct address tuples without importing
the factor execution routine.

The feasibility derivation also computed the different conventional
rank-one lowering of the exact137 source (including its right offset1 and
global phase1). All512 basis columns of that lowering agree with the
source. The direct canonical circuit is chosen because it needs no affine
translation. The retained `analyse_quotient.py` independently checks all512
columns through both sparse and dense original source engines, the closed
two-term formula, and the G/reversed-G fixed words. This is source-algebra
feasibility evidence, not a new literal table or full packet execution.

For arbitrary encoded f, the existing phase and map kernels apply D and G
on every corresponding column. The unchanged first-slot C acts on all f
bits of the first slot, preserving the original nine-slot geometry. Tensor
functoriality proves the full source operator on every f column; no scalar
sum or ADD is tensor-powered.

## 4. Exact ABI and physical capabilities

Use C4's complete Gamma6 packet `(f,r,P,S,w,cutoff)`, same Delta, complete
`[P] x [2^f]^9 x [S]` shape and signed MSB-first w-bit components. Put
`V=2PSr2^(9f)w`, `E=|Gamma6|`, `F=V+E`.

At producer entry C4 INIT has returned. Owned1526 is the exact zero in
HOME2, with its head at its permanent origin. OLD0/CONTEXT1 stay unchanged
at their first-body heads. Private3..42 are blank at their service origins.
External bank43 contains immutable owner slots1349,728,729,730,1515 and
has its head at its origin. Slot1349 is live in frame3, with the actual
pre-MOVE value. No post-MOVE value is supplied.

The new producer can gather external slot0 to work3, use the retained
Gamma/HOME adapter and31-tape full transaction on the existing mapped
ports5..35 with guide36, then scatter back to the same slot0 and erase
work. No additional physical tape is needed. HOME2, OLD0, CONTEXT1 and
the four other external fields are unchanged. All borrowed private bodies,
temporary native guards and44 head conventions return. The returned donor
has frame601 by the source operator theorem and unchanged header/grid.

This uses C4's semantic restoration contract for external continuations.
Its stronger optional syntactic rule forbidding all private writes would
reject any borrowed-work implementation; C4 explicitly permits a more
general continuation when actual restoration is proved. No rule is changed:
the new producer must satisfy the stronger before/after capability equality
on ports0..42, with a separately paid history increase.

The unrelated ADD28038 precedes this producer and ADD28040 follows it.
They remain explicit chronological ports with complete tau/eta bills and
the required preservation contracts. After28040 returns, the unchanged
C4 SUB28041 reads the produced field, updating owned1526 to its negative.
The new result is not a claim to implement every operation of the first gap.

## 5. Numerical prefix domain

Require f<=cutoff. The two complete D phases must fit the signed width,
and every one of the actual f positive C-prefix outputs must be integral
on Delta and fit signed w bits. The final SUB additionally needs its signed
output to fit. Width, quantum, geometry and header remain unchanged. These
premises are inherited exact arithmetic conditions; the format does not
encode or itself validate the current semantic frame/grid.

For the actual zero receiver after INIT, a simple sufficient pre-MOVE
domain is: source numerators are divisible by`2^ceil(f/2)`, magnitude at
most M, and `2^ceil(f/2)M <=2^(w-1)-1`. The credited C-prefix denominator
and component norm bounds, plus monomial magnitude preservation, make
all producer prefixes and the final negation safe. A more conservative
`2^f` divisibility and `2^f M` reserve is also valid.

If one wants to use C4's separate sufficient full-lifetime domain after
this return, require enough extra pre-MOVE divisibility to leave the
produced donor divisible by2^f, or prove the actual later correlated
prefix conditions directly. That later admission is not automatic from
mere integrality of this first producer. The intended theorem stops at
the first SUB; no complete later numeric closure is silently asserted.

## 6. Complete optimistic bill

Using the unchanged per-phase, per-word and C bounds, the proposed31-tape
source core has

`2*65536(E+65V+1)`

`+1024*42*f*(V+1)+2*8192(V+E+1)`

`+65536(fV+E+1)+31V+27`.

This counts both phase scans, all42 CNOTs, physical header/guide generation,
the actual C service, the outer clone/commit and every return/retirement.
Using `f(V+1)<=2fV` and `V<=fV` gives

`8687647 fV +212992 E +213019 <=2^24(fV+E+1)`.

The C leaf itself enforces f<=cutoff. A failure before donor commit preserves
the original public donor; failure private cleanup/retry remains unclaimed.

The unchanged paid adapter adds128(F+1). C4's bank gather and scatter each
cost exactly11F+16, including full five-field traversal, source/recipient
returns and work erasure. A return edge adds1. Thus the whole producer is
bounded by

`T_producer <=2^24(fV+E+1)+150F+161`.

The unchanged first SUB adds `4096(F+1)+(19F+34)+1`. Therefore producer
plus SUB fits `2^24(fV+E+1)+8192(F+1)+128`. If literal B2 INIT is included
in the fixture, add `2^20(V_old+E_old+1)` and its41 extra shift/return steps;
the same8192 envelope remains ample. All pre-MOVE acquisition, fixed setup,
origin/window grants, ADD28038/28040 and transport are additional actual
costs; no complete first-gap or nonleaf tariff is claimed.

For incremental history, two phases contribute512(F+1), two fixed words
128(F+1), the C leaf64(F+1), and outer transaction8(F+1), totaling712(F+1).
Using the generous1024 core envelope and adding64(F+1) for the adapter,
full delivery and scalar increments fits2048(F+2). If INIT is included,
add its64(V_old+E_old+3). Earlier external/private histories and all eta
increments remain charged after cleanup. No owner or capacity is refunded.

## 7. Verification and stopping rule

Before publication: freeze the exact C4 remote pin; authenticate all retained
sources; compile the new five-factor core with fixed constants; verify the
complete port/PC relocation and absence of donor writes before successful
commit; prove all same-owner transfers/returns and the contextual handoff.

Execute a complete nonzero pre-MOVE packet through literal INIT, producer
and unchanged first SUB, with no nonzero host injection after entry. Verify
the direct xor137/sign9 oracle, original donor-owner update, unchanged
owned1526 during production, exact first SUB, every private body/head,
opaque exterior and historical union. Wrong-frame239 source binding,
actual global-phase mutation, stale unproduced donor, signed failure and
cutoff controls must be distinguished from a valid successful return.

The source-algebra and small interface review should be independent of the
new compiler. A full f=2 packet is not required for a bounded fixture; the
uniform theorem must instead invoke the actual inherited all-column kernels
and prove their exact composition. Failure cleanup, other source producers,
S011 scopes, whole dispatcher and all five assumptions remain outside scope.

Stop if an existing literal137 producer already supplies this exact
pre-value→same-owner→SUB boundary, if the actual source frame/grid or owner
contract fails, or if implementation grows into a whole dispatcher. Current
exact predecessor comparison found only generic central services and the
distinct239/owned-rank-two joins, not this producer. This is a bounded
scope comparison, not an exhaustive novelty claim.

Prepared for @CubeJerry with substantial OpenAI assistance and full
predecessor credit. Await parent review before substantial coding.
