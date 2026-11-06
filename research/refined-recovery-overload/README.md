# Sharp recovery at the first overloaded depth

For the literal 112-dimensional rounded native map, **696 bits are necessary
and sufficient for a fixed exact-recovery tag after 27 mode-preserving
stages**. We also prove and attain the exact minimum zero-output fiber

    A^27 + 3 A B^26 + 12 A^2 B^25,
    A=51008161, B=50979600.

The same explicit integer-frame construction has at most 16 A^27 preimages
at every output. **The exact minimum worst-output cardinality remains open.**
This distinction is essential: sharp zero-output counts and sharp packed
bits do not establish a sharp maximum cardinality. **No new κ.**

[Proof](PROOF.md) · [actual lattice lift and full-output bound](LIFT_PROOF.md) ·
[source pins](SOURCES.json) · [scope](TASK.json) · [validation](VALIDATION.md).

## What is new

Merged [#6327](https://github.com/CrocSwap/integer-mult-bounds/pull/6327)
(`research/refined-native-recovery`) established optimal two-step refined
recovery. Nick Petalas's pending
[#6660](https://github.com/CrocSwap/integer-mult-bounds/pull/6660), head
`b6de532eff668a7daf8f2f98668f97af5af41338`, resolves depths through 26 and
leaves the first overloaded depth open. This package settles its zero-fiber
and packed-bit questions at depth 27.

The new lower bound reduces every four-dimensional relation subspace to
30 linear-map types, then certifies the exact optimum. The construction
uses a balanced relation with rank-three even-syndrome projections, rather
than repeating a previously independent image. A separate exact lattice
lift realizes that relation by actual integer unimodular frames preserving
all eight source modes. Neither an abstract binary configuration nor a
zero-output calculation is substituted for a full-output argument.

## Reproduce

From repository root, CPython 3.12 and the standard library:

```sh
python3 -B scripts/research_package.py --package research/refined-recovery-overload
```

Expected final marker: `PASS_REGISTERED_RESEARCH_PACKAGE`. The eight
registered commands run both normal and optimized modes. They cover:

- Literal source Gram/code identities, all 65,536 four-by-four binary maps,
  all 816 small functional multisets, exact AM-GM and 696-bit inequalities.
- An independently authored integer dynamic program over all allocations,
  importing no primary checker.
- The actual integer kernel/complement split, all 3,024 frame columns,
  every lifted source column, and 121 complete 27-stage forward/inverse
  samples with seven semantic controls.
- Eight actual private-copy source or program corruptions, rejected for
  their intended reasons in both execution modes.

The quantified proofs establish the all-frame and all-input statements;
finite samples alone do not. The search domains above are complete and
fixed, with no heuristic optimum or random-search exclusion. The eight
signed chain samples use a disclosed deterministic seed in the checker.

## Scope and costs

Inputs are arbitrary exact integer vectors. Frames are fixed and known;
there is one relative refinement bit before the first call. The output
function changes with the frames. The tag is an abstract fiber index;
no efficient codec or physical memory saving is supplied. Frame swaps and
shears, input range, source access, workspace, routing, restoration and
cleanup remain payable. No selected caller, complete paid invoice,
supplier admission or full multiplication theorem follows.

The base is `7c49fe32c55de02c2c873655c804b16e4c3fef0a`; selected
κ=0.003125804 and all five framework assumptions remain unchanged. No
selected cold replay, human review or formal proof-kernel acceptance is
claimed. Exact source identities and predecessor provenance are retained.

## Open next questions

1. Determine the exact minimum maximum-fiber cardinality at depth 27.
   Start with nonzero-output fibers of the emitted frames; the obstacle is
   the dependence of backward interval starts on later quotients.
2. Determine the optimum at depth 28 and beyond, when relation dimension
   exceeds four. The present 30-type classification does not directly apply.
3. Bind a physical caller accepting the framed output and price all frame,
   codec and cleanup work. No favorable physical invoice is presently known.

## Credit

Prepared for **@CubeJerry** with substantial **OpenAI Codex assistance** in
separate mathematical, constructive, independent-checking and review roles.
Credit @CubeJerry/#6327, zxv/#5444, Ali Romman/#5323, Brian/#5035 and the
retained native/recovery lineage; Nick Petalas/#6660 supplied the longer
chain formulation, dimensional limit and explicit open question. Binary
code duality, AM-GM, discrete convex optimization and unimodular lifting are
classical. New work is Apache-2.0; frozen predecessors are unchanged.
