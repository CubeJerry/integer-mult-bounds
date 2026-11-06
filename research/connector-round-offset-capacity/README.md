# Sharp dirty-connector capacity from round-offset cancellation

**N(c)=(1+o(1))c log₂c in the unchanged unsigned floor-word interface. No new κ.**
One ordinary boundary read cancels the common offset of several group-subset
reads. This gives a deterministic construction matching the known upper
leading constant of one, improving the preceding lower constant one half.
It also attains the leading block-size upper bound at every fixed depth.

```sh
python3 -B scripts/research_package.py --package research/connector-round-offset-capacity
```

Expected: `PASS_ROUND_OFFSET_CAPACITY`, `PASS_INDEPENDENT_ROUND_OFFSET`,
`PASS_CHAIN_ROUND_REFINEMENT`, and `PASS_INDEPENDENT_CHAIN_COVER_REFINEMENT`,
each in normal and optimized Python. Standard library only, tested with
Python 3.12.14. Eight commands are registered.

## Exact result

For integers D,b>=1, c>=D+1, and D(2^b-1)<=c, there is an explicit
unsigned depth-(D+1) block on Db sources. Therefore

    N(c) >= Db floor(c/(D+1)).

Choosing D=floor(log₂c), b=floor(log₂(1+c/D)) gives, for every c>=16,

    N(c) >= c log₂c-c log₂(log₂c)-3c.

The inherited counting upper bound is c log₂c+O(c log log c), proving
N(c)/(c log₂c) tends to one. At fixed depth d=D+1 the block has
(d-1)log₂c-O_d(1) sources, matching #6107's leading upper term.
See [PROOF.md](PROOF.md) for the complete proof and exact interface.

The [symmetric-chain refinement](CHAIN_COVER.md) reduces the round budget to
D binom(b,floor(b/2))<=c. This is the exact minimum within the stated
literal pure-group prefix-cover class. It improves the bound, for all c>=16, to

    N(c) >= c log₂c-(1/2)c log₂(log₂c)-4c.

It also gives fixed-depth block size
(d-1)log₂c+((d-1)/2)log₂log₂c+O_d(1). The refinement uses the same
one-read correction and does not change the alphabet or complete abstract bill.

The construction reserves one source-permutation round per nonempty subset
of each small group. A selected prefix has vector r·1+1_S. Splitting a mask
across groups produces the desired mask plus a scalar multiple of 1. A read
at a suitable round start cancels that scalar modulo c. Each source still
appears exactly c times, and padding each output to c reads cancels arbitrary
dirty contents. No inverse, negative call, extra oracle, or random search is
used. Composite characteristics and repeated read boundaries are covered.

This resolves the leading-constant questions in the merged
`research/connector-bounded-depth-cap/README.md` (#6107, Open Questions 1--2)
and the general-constant question in `research/connector-gray-growth/README.md`
(#6071). It does not claim pointwise optimality at small c or replace sharper
finite blocks. The exact finite capacity and second-order term remain open.

## Verified evidence

- The primary constructor is compared exactly against independently prepared
  six finite schedule fixtures, then checked on 131 schedule cases and
  3,847 mask executions, including concatenated blocks. Literal source
  counts and actual prefix sums are recomputed.
- The separately written checker imports no primary construction code.
  It regenerates all six fixtures, executes all 410 masks and 3,389 complete
  calls over formal dirty/source/output coefficients, and tests correction
  boundaries before, after, between and in productive rounds. It includes
  two-block concatenation and rejects 51 semantic or parameter mutations.
- The primary check rejects ten additional faults, including drift of all
  three live source inputs, lost source calls, a missing offset correction,
  an incorrect boundary, and insufficient round/read budgets. It checks
  the exact capacity formula for c=2,...,65,536 and selected powers through
  2^4096. These arithmetic checks are not proofs of asymptotic quantifiers.
- The chain refinement checks 8,190 located subsets and 1,911 covering
  permutations at b=1..12, plus 4,739 output masks and 30,180 complete calls
  in five literal fixtures. Primary and independently authored checkers
  reject 69 and 89 mutations, respectively. Exact integer arithmetic checks
  2,048 binomial estimates and 16,383 consecutive capacities, with additional
  powers through 2^4096; an independent binary-search oracle confirms every
  capacity entry. [CHAIN_REVIEW.md](CHAIN_REVIEW.md) and
  [CHAIN_LITERAL_REVIEW.md](CHAIN_LITERAL_REVIEW.md) record the two reviews.
- All four programs pass with normal Python and `-O`; failure detection does
  not depend on Python assertions. The task-card orientation control also
  passed: `python3 -B research/universal-connector-boundary/verify.py`,
  `PASS_UNIVERSAL_CONNECTOR_BOUNDARY pairings=945 max_coverage=31 queries=74 leaves=182`.
- Two separately assigned mathematical reviews checked the universal
  correction identity, chronology, arbitrary dirty/noncommuting-map model,
  all-characteristic quantifiers, explicit lower estimate, and matching
  inherited upper bound. Their notes pin the exact proof bytes:
  [MATHEMATICAL_REVIEW.md](MATHEMATICAL_REVIEW.md) and
  [INTERFACE_REVIEW.md](INTERFACE_REVIEW.md).

The fixture domains and rejection controls are explicit in `independent.py`.
The chain fixture generator deliberately caps b and total source count at 12;
the universal construction is proved separately in CHAIN_COVER.md.
Construction is deterministic; no seed or unsuccessful-search inference is
used. These are exact finite checks and independent AI mathematical reviews,
not proof-kernel formalization or independent human acceptance.

## Sources, complete costs, and limitations

Canonical base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.
`SOURCES.json` records exact Git blobs and SHA256s for the three merged
interface/proof inputs and the selected/task provenance. The runner verifies
pins, and the primary verifier checks live input hashes with mutations.
No unmerged code, large artifact, or predecessor full scientific replay is
required. Full Git-history preflight was not run in this shallow checkout;
committed-byte and export checks are separate from historical ancestry.

The complete abstract call bill is cn source calls and c(2^n-1) output
calls. Schedule generation is explicit, but there are exponentially many
outputs. A physical consumer must retain input admission/layout, coefficient
preparation, source/coefficient access, target updates, complete-call scratch
restoration and head returns, instruction construction/storage/read/dispatch,
helper/frame work, decoding, workspace, precision, routing and outer costs.
Equivalently, I+sum P_F+D_W+c sum cost(B_j)+c sum cost(A_M), with every
applicable inherited obligation retained. Unknown physical costs are not zero.
No favorable complete physical consumer is supplied. The selected
κ=0.003125804 and its five assumptions remain unchanged.

The bounded research decision was to resolve this one structural interface
question and verify its legal calls, then stop. Physical adoption requires
a named caller and a favorable full invoice before implementation expansion.

## Credit and open work

Prepared for and contributed by @CubeJerry with substantial OpenAI Codex
assistance in construction, proofs, implementation and separate AI review.
Credit Nick Petalas for #4231/#4248's interface, floor criterion,
concatenation and count; apoursh/Armin Pourshafeie for #6071's Gray growth;
JosieElliston for #6107's depth cap and open questions; and the retained
Ross Richardson/Riquelme Soares connector lineage. Earlier palette/block
ideas in #4256 and conorholds's #2208 concern different coefficient demands
or signed/two-root alphabets and retain their conceptual credit. Partitioning
subsets and modular arithmetic are classical; the new step is their
exact-floor realization through the round-start correction. The refinement
credits the classical symmetric-chain decomposition of de Bruijn, van
Ebbenhorst Tengbergen and Kruyswijk (1951); its proof and source are recorded
in CHAIN_COVER.md. The bounded
[provenance review](PROVENANCE_REVIEW.md) records what was checked and its
coverage limits. Apache-2.0. No predecessor file or selected record changes.

## Open next questions

1. What is the sharp second-order term? The lower and upper bounds differ
   at order c log log c. First compare the explicit grouped-round lower
   bound with a sharper multiset count; the current count is too coarse.
2. What are exact finite capacities and useful finite improvements? First
   compare this formula with existing small blocks at a named characteristic;
   the asymptotic construction is not pointwise optimal.
3. Can a physical consumer benefit? First name a caller and retain its full
   complete-call, instruction, workspace, restoration and outer bill. No
   favorable consumer is supplied; this is the gate before implementation.

A component theorem does not by itself improve the multiplication exponent.
