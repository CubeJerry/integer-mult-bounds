# Independent C review of the native nine-port modules

**Accept the explicit local causal construction and its stated local invoice.**
The partitions work at all 1,120 parent A2 planes. The V9, V18, C18 and
Hermite maps work over the specified GF(32). Their real holder assignments
and stationary caches give the claimed early/late maps, including arbitrary
original late baselines. The local bounds are 184,523,130 binary whole-record
ADDs, 627,750 INITs and the same number of dirty CLEARs, with no extra MOVE.
Global same-original-donor source gluing remains open.

## Literal geometry and every partition

The independent checker authenticates the native-root recovery, layout and
balanced factor. It compares the first 111 layout roots with the recovered
native ordering and reconstructs all 1,120 A2 triples from exact integer
Gram determinants. Plane-to-D4 containment and receiver orthogonality are
then reconstructed from the root sets.

Every submitted partition has five disjoint nine-element classes covering
exactly its plane's 45 actual D4 exits. Each of the 36 perpendicular parent
receivers sees 15 exits and exactly three per class. All 40,320 incidences
are checked. Native incidences are 29,354 at full planes, 7,549 at two-donor
planes and 360 at singletons. The inactive plane has no native donor and is
not charged as an active source module.

Every recorded predecessor reflection is also checked: it permutes actual
root lines, sends the parent plane to its successor, and transports each
actual D4 class correctly. The 1,119 predecessor edges are acyclic and reach
the verified base. Both the direct certificate and its reflection provenance
therefore pass. A negative control swaps two ports between classes while
preserving all class sizes and the full partition; a receiver then fails
the three-per-class requirement.

The source census is independently checked: 709 full planes have x=4,
84 have x=5 and 88 have x=6; 227 two-donor planes have x=6; 11 singletons
have x=12. Every native donor retains exactly 5,760 genuine early slots.
No omitted parent root is used as an additional native donor.

## Finite-field ranks and the universal C18 proof

The review implements GF(32) with carryless multiplication followed by
polynomial long division modulo z^5+z^2+1. All 31 nonzero elements have
verified inverses. It imports none of the author's implementation.

The 252 V9 donor minors are invertible. Each is a nonzero row scaling of a
three-column Vandermonde matrix at distinct nodes. Combining 120 stripes
gives rank 360 and invertible projection onto each donor's complete formal
360-dimensional quotient. The full V9 and V18 maps are invertible too.

All 168 two-donor transfer matrices have rank 12. Their early six-row block
has rank six and late six-row block has rank three. Replacing C18 by zero
gives rank exactly nine in every case, detecting the need for the crosswave
term in this design.

The written finite-grid existence argument is correct. For a fixed
constraint, the map C to LCN is onto the 3-by-3 matrices, so its determinant
polynomial is nonzero. A single C entry changes LCN by rank at most one,
so each determinant has degree at most one in that entry. The entry belongs
to one donor block and occurs in exactly 28 triples containing its output
port. The product therefore has individual degree at most 28, below 32.
The grid lemma applies even though the total degree exceeds the field size;
no common specialization of separate witnesses is assumed.

All 84 Hermite minors have rank 12. Value and formal derivative vanishing
at six distinct nodes force divisibility by their six squared linear
factors, which is impossible for a nonzero polynomial of degree below 12.
This holds in characteristic two. Omitting the derivative leaves rank six.
Only the nine odd-degree coefficients contribute to the derivative, so the
smaller cache is sufficient.

## Actual holders, permutations and chronology

The reviewer reconstructs full-plane stripes from actual labels
(donor, port, holder ordinal). For t=2,3,4,5,6 all holders occur once,
each stripe has one holder per port, and each donor contributes three
fields. These cover every phase used by x=4,5,6.

The necessary input-order permutation is compiled into literal three-ADD
binary swaps on those actual holders, then followed by the submitted V9
word. Replaying every input column gives the expected map at the fixed
physical output ports. The observed permutations use at most 90 ADDs,
below the charged bound 120. No output holder is silently relabelled.

For all six two-donor stripes, the checker separately reconstructs the
18 early holders, six genuine late donor holders and 12 direct-ground
late holders. Across the six stripes, each port uses exactly its eight
real direct-ground holders, without reuse. Both input-order permutations
are compiled and replayed; they need at most 225 ADDs, below the charged
255 per phase.

The cache copies original early coordinates before V18 acts. The complete
literal word gives early = V18 E and late = V18 Y + C18 E on all 180
independent binary early/late input columns. The cache stays unchanged and
dirty until its paid retirement. Caching the transformed early output gives
a different C18 term and is rejected by a negative control.

The singleton replay preserves every independent late baseline and adds
the derivative using only the 45 cached odd-coefficient bits. Its early
V18 map retains all 18 input fields. Every local public two-wave map is
invertible, either phase by phase or by its block-triangular form.
The cache is stationary and does not create an extra moving channel.

## Invoice and scope

The submitted binary words are checked for distinct valid ADD operands.
Their complete basis-column replay agrees with the independently expanded
field matrices. Reversing each word gives its inverse. Exact lengths are
850 ADDs for V9 and 3,554 for V18. Independent expansion gives 4,064 ADDs
for C18 and 1,878 for the derivative.

| Plane type | Count | ADD bound per plane | INIT and CLEAR per plane |
| --- | ---: | ---: | ---: |
| Three donors | 881 | 116,400 | 0 |
| Two donors | 227 | 353,160 | 2,700 each |
| Singleton | 11 | 164,310 | 1,350 each |

The totals are 184,523,130 ADDs and 627,750 each INIT and dirty CLEAR.
The five binary copies per field coordinate are included. Global source
encoding, restoration and preload inverses, later proper transport, the
return bank and recursive supplier/caller costs remain separately payable.

The unresolved constructive step is the common-original-input assignment
across every donor's 28 planes. Local target graphs with invertible donor
projections do not by themselves provide simultaneous inverse fibres,
global early injectivity or the endpoint map. The package explicitly retains
these limits. It is a verified smaller local interface, not a new complete
multiplication exponent.

Reproduce with `python3 -B check.py --repo REPOSITORY --author AUTHOR --out OUT`.
Expected marker: `PASS_INDEPENDENT_NATIVE_NINE_PORT_REVIEW`.
Exact source and author hashes are in `output/REVIEW-PINS.json`.
This is independent agent/code review, not human or formal-kernel review.
Credit the native and balanced-route authors, @CubeJerry, S026 Worker A,
and substantial OpenAI assistance.
