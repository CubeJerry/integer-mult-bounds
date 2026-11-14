# Wave 10: actual current-producer divmod with paid owner binding

Approved phase1 route; no divider construction yet. Base e54523517d0f03e58352e647c403a5af3e525a57.
Immediate exact current caller is frozen B9; its B7 dependency is published
f789e7318ef89b26c2e358c4c1eb09ce93d21f73.

## Actual call and nonconstant incoming owners

Use the sixth raw divmod of one actual one-left/one-right current leaf.
The first five are left-base, the single Euclid division for inverse of1,
that step's qmod, left-local and left-digit. The sixth computes the genuine
left-modulus/right-modulus quotient and remainder. Actual p=u+h+1>=4,
right modulus>1 and h-bit encoding give 0<D<2^h<=2^(p-2), hence the original
zero-high-bit division margin. N/D are distinct live words returned to
first-body heads; every other live/protected word must remain unchanged.

Exact code: merged #5053 head ef9da0a9ac29cf86610a52e3a183bdb28508aa74,
producer blob a327b0161eca57a1cc44ec2aa8e3defed2167ddc; actual Word module
blob8d4ba37e2778acb35b34e0719df2caf138fbeb50, SHA256
5c37f57708ba3131bdcb03139f9dbc29886bee44569c09cbba51b68f75acd7f9,
Unsigned.divmod lines253--279. Entry #5219 head15edd6b658f14ae981cedf24507bb957a9e4e174;
RowEntry #5353 head07a135eee3a8da9392c4a1e01d4b89db05b4ac03;
actual source frontend/leaf #7352/#7388 at their frozen B9 pins.

The bounded trace_call.py executed40 actual selected NodeEntry leaves,
varying coprime moduli and valid/padded left coordinates. It found8 incoming
slot/free-stack fingerprints already, with numerator slots18/19/23 and
denominator9. CALL-TRACE.json is observational evidence, not an exhaustive
state theorem. Hard-wiring a fixture's slot tuple is excluded.

## One fixed literal graph and an explicit finite-source binder

Physical graph roles are the64 genuine numerical Words plus four six-bit
N/D/Q/R descriptors. Every actual Word read/write/move goes through a
literal64-way dispatcher; each leaf names a fixed physical port. The
descriptors are parsed and physically returned on every action. No Python
runtime tape lookup performs a numerical operation.

The source binder remains retained finite64-slot control: check ownership,
reserve two free roles without initialization, and choose four fixed setter
entries from existing slot identities0..63. A setter's six digits are
compile-time constants, all written by the graph. The selection is a fixed
finite choice, not P/value decoding. Explicitly charge comparisons, pool
updates, binding and setter instructions; keep finite-source and literal
counts separate unless a common tariff is proved. This does not pretend
that the entire numerical controller has been lowered.

Four descriptor owners can reuse the actual direct caller's first four
blank private marker owners: all14 are acquired before numerical production,
and none is used by header/key control until the current result exists.
Return all four blank at their origins after every division. Their eight-cell
history unions must be charged; old private-key bounds do not transfer
unchanged. No new physical owner is acquired per division. Standalone
entry must separately supply and price these four persistent windows.

Core entry has live same-p N/D, 0<=N<2^p,0<D<2^(p-1), distinct newly reserved
Q/R and blank owned bodies with their existing LEFT guards. It validates
matching extents, p>=4 and divisor margin/nonzero; initializes every Q/R
cell; scans N high-to-low; shifts R<-2R+bit, compares/subtracts D in place,
and writes Q. It returns floor(N/D), N mod D, borrowed bytes/heads and
blank descriptor owners. The new two outputs replace old scan/shift scratch,
so no additional p-size physical role is needed.

## A replacement for exact allocation-event coupling

Identical old/new allocator event traces are not claimed. At primitive
boundaries relate contexts by a bijection of64 slot labels: incoming live
words/values/heads and protected roles correspond, ordered free stacks map
positionwise, and every free body is blank. After division map old returned
Q/R to new Q/R and remaining free stacks positionwise, preserving the
relation on incoming live objects. Both sides leave exactly two fresh
outputs and every other entry-free word blank, so this bijection exists.
It is a proof relation, not a free physical tape permutation.

Audit each retained use of slot/identity: arena identity, available pop,
live membership, word.slot, words[slot], protected/keep and alias branches.
Ordered zero/free/copy/free_many/arithmetic calls are equivariant. Numerical
code never branches on the magnitude of a slot or allocator metrics.

Important qualification: producer finally iterates tuple(arena.live), whose
order can change under a label permutation. Thus the argument is a weak
simulation at structured boundaries, not an identical individual-step
bisimulation. Final cleanup erases disjoint non-kept words in either order;
then refresh the free-stack bijection while fixing protected and returned
words. Prove its effects, head returns, peak live count and all failure
checks explicitly. Do not silently apply #5219's stronger unchanged-event
coupling to the replacement.

Old numerical capacities do not move under the proof permutation. Each
actual physical Word retains its own old history; active arithmetic stays
inside its current p+2 frame. The persistent-owner proof supplies delimiter
semantics for larger blank tails. New numerical writes stay within these
same actual frames. Descriptor history is additional on the actual four
reused private ports. Peak new live numerical count is at most old peak:
two output reservations replace a call that simultaneously owns at least
scan/Q/R before further scratch.

## Optimistic bill and complete scope

P iterations, each with full shift, compare, optional subtraction and every
return, give O(P^2) logical actions. Fixed six-bit dispatch gives constant
overhead per action, with all selectors restored. Four setters and final
descriptor disposal are paid. Initial conservative target:
2^14(P+2)^2+O(1) literal instructions, plus at most16384 explicitly retained
finite-slot binder operations after exact inspection. Derive the actual
invoice before claiming it. All source-field production, preceding/later
arithmetic, output serialization, source commit and radix stay charged
external providers. No new kappa or whole numerical/multiplier claim.

Use exact integer oracles and a separate sparse interpreter; test numerator
less than divisor, divisor1, full numerator, high margin, padding, slot
choices and retained larger histories. Controls must catch descriptor drift,
aliases, live-word corruption, wrong returning Q/R and missing retirement.
Execute complete current source-offset/payload joins at several different
allocator fingerprints, preserving all incoming/protected data and final
source/owner retirement.

Overlap: #5053 already proves CRT/Euclid/word semantics and source-operation
costs; #5219/#5353 and persistent owner already prove entry/lifecycle. The
complete PR5105 binary refinement is a different fixed program/geometry.
Prior bounded searches found no exact current divmod plus this owner join.
Stop if the physical dispatcher hides numerical work externally, if the
slot relation fails a real use, if private-owner reuse is live-conflicting,
or if only generic standalone division remains. One evidence-driven pivot
is allowed within this boundary;75-minute initial budget including review.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit exact
Word/record authors, JoyboyBrian #5053/#5219/persistent-owner, Ali Romman
#5353 and current #7352/#7388/B4--B9 source lineage. B9 remains frozen.
