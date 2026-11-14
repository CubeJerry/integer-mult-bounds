# Wave12 feasibility: combined current raw arithmetic closure

2026-11-14. Canonical base `e54523517d0f03e58352e647c403a5af3e525a57`.
This is a proposal and source audit, not an implemented or verified theorem.
Verdict: **GO, subject to lead approval and the stopping rules below.**

## Precise new claim

At every admitted invocation of the exact forward or inverse current CRT
numerical producer, replace every actual call to `Unsigned.compare`,
`Unsigned.add`, `Unsigned.subtract` and `Unsigned.divmod` by a single fixed
literal R/W/M/J/H instruction graph on the existing64 physical Word roles
and four eight-cell selector owners. `subtract_exact` remains its finite
borrow check and delegates to the new subtraction entry. No old arithmetic
provider is available during actual source execution. The existing B10
division graph is retained byte for byte as an unchanged initial segment.

The result preserves all incoming live Word contents, operand heads and
unrelated physical owners; returns a fresh complete output Word for add or
subtract together with its finite carry/borrow; returns one of three finite
comparison states; and returns the same numerical source outputs as before.
All four selector bodies are blank and their heads returned after each call.
One-output reservations and the existing two-output weak division relation
compose through the actual source and its final cleanup. Every physical
history and every new literal action is charged. Other Word operations,
finite live/free control, source framing and grant acquisition remain external.
There is no full literal numerical-producer controller or global compiler
claim and no new kappa.

## Exact dependencies and overlap

- #5053, head `ef9da0a9ac29cf86610a52e3a183bdb28508aa74`,
  `research/encoded-current-crt/producer.py`, blob
  `a327b0161eca57a1cc44ec2aa8e3defed2167ddc`.
- Exact `words.py` blob `8d4ba37e2778acb35b34e0719df2caf138fbeb50`,
  retained in that source lineage, defines the primitive semantics.
- #7388, head `d6f4a69202ad0bba4a915f4d4f3eaba1fe431c86`, retains the
  inverse specialization and actual current leaf source/payload caller.
- #5219/#5353 supply the eager Entry and row boundary. They bind exactly8
  protected guard Words and56 owned Word roles; this is not an arbitrary
  Arena with fewer physical guard ports.
- Published B10 `c4ab5dab6914a04cb86d1fe54eb763b35cc7eeb1` supplies the
  literal divider, dispatcher, grants and weak owner relation.
- B11 frozen package `worker-b/wave11/all-current-divmod`, binding SHA256
  `1b62577836ffc5906bd749b3705cfb3873cf9b15380224648fff924315efc8c9`,
  supplies all-source division scope and its loop-count proof. It has passed
  author and separate independent checks; remote publication is pending.

`SOURCE-AUDIT.json` records exact bytes, blob hashes and all16 forward and
inverse raw call sites. The only method names are add, compare, divmod and
subtract_exact. `subtract_exact` invokes subtract. The obsolete division
body's shift_add_bit is unreachable after B11 replaces all divisions;
times_small and increment_in_place have no call path from this producer.
The inverse file differs scientifically only by using modular subtraction
instead of addition for a valid right coordinate.

The bounded live searches for `Unsigned.add` and `Unsigned.compare` returned
no PR; `encoded-current-crt` with `literal` returned #5053 and #5219. Broader
arithmetic searches mostly found unrelated scalar/connector work. Canonical
tree names exposed no matching source-bound arithmetic closure. This does
not certify novelty against every diff or unpublished claim. #5053 already
proves the arithmetic algorithms and their ranges. #7565 supplies a generic
dispatcher. Neither is claimed anew: the proposed result is one combined
actual-source provider elimination with alias/flag/allocation interfaces.

## ABI and substantive obstacles

The numerical port alphabet, P-bit extent, LEFT at0, RIGHT atP+1, head1,
physical backing identities and native meter are unchanged. P>=4.
All four selector frames are populated on every invocation using unchanged
B10 setters: compare `(a,b,a,b)`; add/subtract `(a,b,out,out)`; divide keeps
its existing four distinct roles. Duplicate descriptor values are legal
only at the new entries; all physical port objects remain distinct.

`a is b` genuinely occurs in doubling at producer lines45 and74. A literal
six-bit descriptor equality scan must choose an alias path which advances
the shared operand once, rather than twice. Compare on equal descriptors
returns0 with no numerical allocation; add/subtract read and scan one
shared input and the fresh output. For distinct inputs the ordinary two
head path applies. The graph validates output-distinctness and complete
typed extents and preserves all input bytes. Neither host object identity
nor decoded operand values choose the arithmetic path.

The new add/subtract entry writes directly into an inactive blank output
body after reserving one owner. It scans every output cell, verifies its
blank entry state, writes all P digits and RIGHT, and returns every head.
Original `Arena.zero` would have allocated that same one output and first
zeroed it via the template. Its complete actions are part of the old raw
provider bill and will be removed exactly once. The graph's direct write
does not leave a hidden initialization service. The existing grants supply
the body capacity; no growable-tape inference is allowed.

Addition returns `ADD_C0` or `ADD_C1`, subtraction `SUB_B0` or `SUB_B1`, and
comparison `CMP_NEG`, `CMP_EQ` or `CMP_POS` as finite halt states after
literal cleanup. The retained source binder maps these fixed tags to its
finite carry/borrow/comparison control. This finite delivery is separately
charged. It is not an encoded-word decoding or an unbounded dispatch.

One-output reservation is a new finite binder method, validating the exact
64-slot live/free partition and incoming backing identities before one pop.
For compare and add/subtract the old and new allocation traces match under
the current slot bijection. Aliasing is preserved because a bijection is
injective. The B11 division relation is composed unchanged. No new live
Word scratch is required, so the prior32-live bound remains applicable.
Actual physical history unions are recomputed; old per-slot profiles are
never transferred by permutation. The four selector grants remain explicit
eight-cell windows and all retired private extents remain preserved.

## Optimistic complete bill

Let n=m+t, E be the sum of the Euclidean iteration counts, and let H count
all actual compare/add/subtract calls outside the replaced division body.
Each modular multiplication performs P doublings and at most P further
modular additions, each costing at most three of these raw calls. A modular
subtraction costs at most three; a full product costs at most2P raw adds.
Directly from the exact source, for either direction,

    H <= (6P+3)E + m(10P+7) + t(8P+6)
      <= (P-2)(12P²+22P+10) < 12(P+2)³.

The first term counts every inverse's modular product and subtraction;
the left term includes scaled multiplication, adjustment, both full
products, the reconstruction add, admit/value/unit comparisons; the right
term includes offset multiplication, valid coordinate update, its full
product and all three comparisons. Short-circuit left validity can only
reduce this count. The inherited source proof gives E<=n(2P+1), n<=P-2.

The planned literal primitive uses one digit scan, returns over the exact
P-bit extent, and only fixed-size descriptor/alias/owner checks. A generous
construction target including four31-instruction setters, all header reads,
output initialization, complete source extent, head returns, finite flag
delivery and selector retirement is at most8192(P+2) instructions per call.
The emitted graph must prove an actual count below this target; it is not
yet a measured or established bound. Thus the optimistic combined subset is

    T <= 89 + J(930P²+1395P+14322) + 8192(P+2)H
      < 2^18(P+2)^4,

where J is the already established B11 division count. A conservative
publication ceiling of2^20(P+2)^4 leaves room for precise new graph constants.
ACQUIRE is charged once per descriptor lifetime, not once per primitive.

The complete invoice remains a vector: new literal actions, residual exact
source-tape/controller actions, finite metadata and finite returned-flag
actions, plus grant acquisition. For each old source leg, spy only the
outermost call among the four replaced providers: the old divmod contains
its own compare/subtract calls, which must not be subtracted again. In the
new source no provider invokes another host arithmetic provider. Direct
numeric actions charge arena.meter exactly once; selector actions charge
their marker ports exactly once. Retained Word.zero/copy/free/control costs
stay in the residual source bill. In particular an add/subtract output is
returned live, not numerically erased at primitive return: its later actual
Word.free scans and erasure remain charged in that residual source bill.
Only the four selector frames are retired by the arithmetic entry itself.
The old source bound also prices every such lifecycle action. No common
tariff, speedup or kappa follows.

## Implementation and verification plan; stopping rule

Build the three new primitive entries offline with the fixed alphabet;
append their compiled graph to the unchanged B10 graph and independently
check every relocated branch and old instruction. Reuse the same68 owners
and old setters. Prove all-P loop and carry/borrow invariants, strict output
separation, alias correctness, finite return semantics and the count above.
Use exact integer oracles for sums, differences, wraparound flags and
comparisons, including equal inputs and maximal values. Negative controls
must return cleanly but alter a carry, alias head step, comparison state or
live input, so the semantic oracle detects more than exceptions.

Then execute the exact current source in both directions, including a
nonleaf group, with all four old providers and shift_add_bit unavailable.
Check the direct current CRT oracle, full source/payload restoration,
composed live/free relations, reused histories and exact outermost-provider
meter subtraction. Include out-of-producer/foreign-arena and fallback
controls. Test instrumentation is excluded from the machine theorem.

Stop if the exact source has another reachable numerical provider, if the
alias/finite-flag interface requires unbounded host arithmetic, if a fresh
one-output relation fails, or if complete costs exceed the declared subset
budget. Do not publish a standalone generic arithmetic library or a claim
that Word lifecycle/control, the finite allocator or compiler is now literal.
No construction starts before lead approval; no new speculative start after
09:57 UTC.
