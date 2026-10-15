# A complementary-frame backward shear for the completed P104 word

**Finite construction. No new κ.** The completed forward word from
[PR2305](https://github.com/CrocSwap/integer-mult-bounds/pull/2305) now has an
explicit companion implementing `X <- X - Y`, with all 527 ordinary dirty
helpers restored. Both words act on 735 independent public inputs. Every
positive-rank transport, all scratch lifetimes and the complete native
operators of the companion are checked.

This addresses one finite orientation obligation explicitly left open by
PR2152/PR2305. It does not admit their global supplier. In particular, the
predecessor's actual conditional owner invoice already misses the selected
κ; this construction does not improve that invoice or the selected result
`836330098538459/500000000000000000`.

## Exact result and bill

The scientific base is canonical main
`0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`, priority revision 4.
The input is Gareth Davidson's PR2305 at
`335e78619a17b7c418e11306f86a72fd366de35b`, built from David Arias's PR2152 at
`05f7aad0f08992ee48ec2dd93e896d9a4567847d`. Cinna Davis's PR2219 private-reuse
mechanism is inherited through that input, not newly claimed.

The companion reverses the scalar event order, transposes additions,
complements every binary frame and applies a fixed sign gauge. It retains
every public register's lifetime width. The full paid profile in each
orientation is

```text
2429 H1 + 557 H2 + 389 H3 + 112 H4 + 108 H5 + 16 H6 + 13 H7 + H9.
```

| Quantity | Forward input | New companion |
| --- | ---: | ---: |
| Public inputs / ordinary dirty helpers | 735 / 527 | 735 / 527 |
| Public / private rank mass | 5838 / 56 | 5838 / 56 |
| Positive-rank transports | 3625 | 3625 |
| Scalar additions | 20947 | 20955 |
| COPY-to-zero assignments | 8 | 0 |
| Nonzero scalar scales | 715 | 715 |
| Owned scratch initializations / discards | 8 / 8 | 8 / 8 |
| Maximum simultaneous private registers | 1 | 1 |
| Total events | 25311 | 25311 |

The eight forward COPY assignments become eight add-back operations. They
are counted as additions; they are not omitted or charged as free copies.
The companion uses a zeroed owned **accumulator**, followed by its paid
descent and add-back, rather than a single-source-copy interface. Its private
profile is `2 H1 + H2 + H3 + 7 H7`, still mass 56. All public restoration,
including the unused helper's rank-nine boundary transport, is retained.
These are finite program counts; bit/tape costs and recursive work constants
are not certified.

There is no change in the recursive rank moment. Recomputing the predecessor's
favorable hypothetical model (`m=73`, `w=832/9`, centre mass 56, and 818 idle
ranks all placed fractionally at rank 51) gives a moment about
`0.99999585229209` at `a=κ_selected/(1-κ_selected)`, and the same κ upper cap
about `0.00167393973105`. This is an upper ceiling, not an attained saving.
The exact rational enclosures are in [RESULT.json](RESULT.json).
PR2305's actual forward owner invoice was about `1.00006553178737` at that
threshold. That number is credited context, not a newly checked backward
owner assignment: equal widths do not imply compatible chronological windows.

## Why the construction works

Let `M=I+N` be the forward logical matrix, where `N` sends the 104 live X
coordinates to their corresponding Y coordinates and is zero elsewhere.
Thus `N²=0`. Ordinary transposition of a finite linear straight-line program
reverses its operation order, swaps the operands of each addition, and keeps
each scalar multiplier unchanged. It gives `Mᵀ`, not a program obtained by
reciprocating the scalar scales.

Private storage fits this argument explicitly. Initialization is the linear
embedding `z -> (z,0)` and discard is projection `(z,c) -> z`; transposition
exchanges these two maps. A COPY with a proved zero destination is an addition
on that extended space. Its transpose adds the accumulated private row back
to the original source. Each original discard therefore becomes a zeroed
accumulator at the beginning of the reversed lifetime. Its final content may
be nonzero when discarded, as permitted by the inherited owned-private
storage contract. Arbitrary *public* dirty inputs are never reset or discarded.

Let `S` negate the original 104 live X coordinates and fix every other public
coordinate and every scratch coordinate. Conjugate every transposed scalar
operation by this fixed diagonal sign matrix. An addition coefficient is
multiplied by `s_destination*s_source`; scales stay unchanged. There are no
extra boundary NEG operations. Since `S Nᵀ S = -Nᵀ`, the resulting logical
boundary map is

```text
S Mᵀ S = I - Nᵀ = M^(-ᵀ).
```

This reasoning is independently checked by exact rational replay on all 735
input columns. Applying the generator's dual transformation twice reproduces
every forward event, with the eight zero-destination COPY operations written
as additions. The checker also compares all 25,311 individual event
correspondences, so endpoint equality alone cannot conceal added work.

For the frames, an original public step `A ⊂ B` becomes
`B⊥ ⊂ A⊥` under reversal. A private descending step becomes another descending
step. Nondegeneracy of the ordinary binary dot product gives
`dim(A⊥)=9-dim(A)` and preserves each jump rank. This uses orthogonal
complements, not set complements or a direct-sum assumption; isotropic
subspaces cause no exception. The generator uses binary elimination, whereas
the checker reconstructs complements by testing all 512 binary labels.
All operands of an original scalar operation shared one frame, so their
companions also share one complementary frame.

For an odd physical port `q`, the forward X boundary `⟨q⟩ -> FULL` becomes
the backward target boundary `ZERO -> q⊥`. The forward Y boundary
`ZERO -> q⊥` becomes the backward source boundary `⟨q⟩ -> FULL`.
Helper entries and exits are also complemented and reversed, with equal
lifetime widths. They are restored in these new frames, not silently assigned
their old endpoint charts.

The finite physical invariant is: register `r` contains `Γ_frame(r)` applied
to its exact logical row. Common-chart additions and verified native
transports preserve this invariant. The inherited exact compiler lowers each
new transport; the separate Gaussian interpreter checks signed Pauli actions
and a nonzero state column to fix global phase. It also checks all 512 columns
of each of the eight complete private paths. The 208 intrinsic data endpoint
adapters have rank zero. The new native recipe payload digest is
`4b0afd36e284079413716d69fd03a86761697552838031a18fccf097ac728b06`.

“Inverse transpose” here describes the logical shear. The physical operators
are compiled in complementary charts. Binding these charts, the private
accumulator interface and helper endpoints to an actual caller remains open.

## Reproduce

From the repository root, using standard-library Python 3.12:

```sh
python3.12 scripts/research_package.py --package research/p104-complementary-dual
```

Expected: `PASS_P104_COMPLEMENTARY_DUAL` followed by
`PASS_REGISTERED_RESEARCH_PACKAGE`. The registered replay took 90.433 seconds;
a normal-mode Git-free export took 186.136 seconds on Linux x86_64 with
CPython 3.12.14. Both produced receipt
`e22a689627498131323fa18cbdfa73b48bafe8c4d81c4029897f3e4426426f92`.
The registered command uses
`-I -O -B`; all checks remain active with assertions disabled.

The direct command also passed from an export containing this package and its
six declared input files, without Git or network. All 17 files stayed unchanged,
including two deliberately recompressed word containers with identical payloads:

```sh
python3 -I -O -B research/p104-complementary-dual/verify.py
```

Default replay regenerates both complete words in temporary storage, compares
their canonical decompressed payloads, checks both 735-column maps, checks the
new native operators, and compares the complete receipt. It writes no source
files. `--out NEW_FILE` writes only to a new caller-selected path;
`--write-result` explicitly regenerates the receipt. `--scalar-only` is a
development diagnostic whose status explicitly says native checks were not run;
it cannot replace the full receipt. The generator's optional `--out-dir`
likewise requires a new directory.

Ten actual mutations reject: missing private accumulation, wrong private
scatter sign, reciprocal private scale, missing dirty-helper cleanup, wrong
common chart, an undercharged transport, omitted unused-helper boundary,
missing private initialization, public reset disguised as private
initialization, and the positive transpose in place of the inverse transpose.
The dirty-helper control leaves every data endpoint correct and is rejected
for helper corruption. The native checker separately rejects a wrong global
phase. Five additional controls reject changed external source bytes, a changed
word payload, changed producer-archive bytes, an occupied output path and an
attempt to overwrite the full receipt with a scalar-only run. They are recorded
in the task's validation receipt.

## Scope and overlap

This is a finite local construction under the owned-private storage contract.
It supplies no global emitter, caller wrappers, chronological backward owners,
recursive precision/reserve or all-size proof, outer assembly, selected
cold replay, or new κ. No human independent review or proof assistant is claimed.
The scalar/frame interpreter was written separately from the predecessor
constructor; the compiler, native interpreter and interval engine are inherited.

The OS assignment seed was **32** (complex supplier). The chosen card was
`p104-side-correction`, with an explicit scope change after live review of
completed forward work. PR2337's independent forward corroboration is credited;
the active pooled-prefix and causal-contact investigations address different
questions. [TASK.json](TASK.json) records the candidate comparison, local claim,
partial public-web overlap coverage and freshness limits. GitHub API posting
was not attempted under the user's publication restriction.

## Open next questions

First bind one complete invocation's caller to these
new helper/data endpoints and accumulator lifetimes, including every native
wrapper and charge. A second useful step is a cheaper local mechanism or
actual owner packing that survives the full moment test; the present dual
preserves the existing cost warning. Stop a proposed realization when its
frame/dirty contract fails or its favorable completed budget cannot help.
Structured first steps and blockers are in [TASK.json](TASK.json).

## Attribution

Prepared for **@CubeJerry** with substantial OpenAI Codex assistance in the
construction, proof, implementation, verification and writing. No subagents
were used. New work is Apache-2.0. The linear-program transposition principle
is standard; this contribution is its explicit, source-bound application to
the completed P104 word and its scratch/frame contracts.

Credit Gareth Davidson / @bitplane (PR2305), David Arias / @DavidAriasC
(PR2152), Cinna Davis / @1337isnot1337 (PR2219), and the independent forward
corroboration by SHIN09-git (PR2337). The frozen producer archive retains
the predecessor READMEs and source attribution verbatim.

The retained lineage includes Rohan Arun's scalar channel and T16 schedule,
Chafik Boukhalfa's native realization, Adam Gall's schedule, Josie Elliston's
and Ali Romman's P104 geometry/decoder work, icekylinx's frame-sa504 work,
the PR1042/PR1094 supplier/controller lineage, and Douglas Colkitt's exact
ceiling engine. The unchanged compiler and Gaussian interpreter retain the
repository's frame-sa504 and PR1862 notices. [SOURCES.json](SOURCES.json)
records every archive member's commit, Git blob and SHA-256, the external
input pins, and canonical word-payload hashes.
