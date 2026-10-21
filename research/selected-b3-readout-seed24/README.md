# A shorter readout in the selected complex supplier

**Finite local circuit result. No new κ.** The selected #1094 gauge44 word's
zero-based, half-open `B[201:235]` block has an exact 27-ADD replacement for its
34 ADDs. Both orientations save **108 real-component primitive operations per
provider invocation**, including coefficient work, preparation and restoration.
The recursive profile is unchanged. This package does not install the candidate
in the selected construction or establish a new complete supplier.

Base: `12fa8c5c844be21bfefb38a19503fbd867a11244` (canonical main, priority
revision 7). At this base the selected conditional result is
κ = 0.001672660197076918, reached through
[`selected-result.json`](../../certificates/selected-result.json), its
[#1094 source manifest](../community-frontier1094-audit/SELECTED-SOURCE.json),
and the [maintainer review](../../docs/research/community-batch1099-review.md).
Historical frontiers and pending PR titles are not used as accepted results.

## Reproduce

From a full repository checkout, using Python 3.12 (standard library only):

```sh
python3.12 -B scripts/research_package.py --package research/selected-b3-readout-seed24
```

Expected: `PASS_SELECTED_B3_READOUT gates=34->27
block_component_primitives=170->116 full_columns=712 orientations=2 controls=12
no_new_kappa`, followed by `PASS_REGISTERED_RESEARCH_PACKAGE`.
The registered commands run the exact checks both normally and under `-O`,
with warnings treated as errors. Checks use explicit exceptions, not assertions.
Local verification used CPython 3.12.14 on Linux, with no external packages.
`RESULT.json` contains both gate lists, exact counts and prefix bounds, all
source/member pins, the selected block domain, and candidate program hashes.
The verifier compares every certificate field, not only the success marker.

For an optional handoff of both complete candidate event streams,
use a directory that does not already exist:

```sh
python3.12 -I -B research/selected-b3-readout-seed24/verify.py --emit /tmp/selected-b3-candidate
```

The emitted `LOCAL-PROGRAMS.json` is a candidate input for subsequent admission;
it is not an already admitted provider. The exporter first runs all checks and
compares the committed receipt. It refuses to overwrite an existing directory.

## Identity and complete local bill

There are two readout groups, with the following register order:

| Group | Targets `(y1,y2,y3,y4)` | Sources `(a,b,c,d)` |
|---|---|---|
| First | `(179,115,120,138)` | `(664,665,666,668)` |
| Second | `(117,181,208,177)` | `(672,673,674,676)` |

All operands have frame 3, whose retained basis is `[51]`. Each group's desired
target increment is `M * (a,b,c,d)`, where

```text
        [ -1 -1 -1 -1 ]
M = 1/2 [  1 -1 -1  1 ]
        [ -1 -1 -1  1 ]
        [  1 -1  1  1 ]
```

Use this restored target chain, in the stated order:

```text
prepare:  y4 -= y2;  y2 -= y3;  y3 -= y1
inject:   y1 -= a/2; y1 -= b/2; y1 -= c/2; y1 -= d/2
          y3 += d;   y2 += a;   y4 += c
restore:  y3 += y1;  y2 += y3;  y4 += y2
```

Preparation stores the successive differences along `y1 -> y3 -> y2 -> y4`;
restoration takes their cumulative sums. Their product is the identity on the
four arbitrary initial target values. The injected increments become, in that
chain order, `-(a+b+c+d)/2`, then add `d`, then `a`, then `c`, giving precisely
the four rows of M in the table's order. The sources remain unchanged.

The second old group additionally has a restored pulse
`L676 += 2*L566; L181 += L676/2; L676 -= 2*L566`.
Relative to its ordinary `L181 += L676/2` readout this contributes exactly
`L181 += L566`, with L676 restored. Add that one unit ADD after the two chains.
This establishes the full forward block on all 17 logical input columns.
It is a shear `I+N` with `N^2=0`; its inverse transpose is `I-N^T`.
Swapping the operands and negating each coefficient, in the same gate order,
therefore gives the inherited backward orientation. The verifier separately
checks both against the closed-form matrix, without deriving that matrix from
either gate list.

Under the retained cleared-work binary-Horner convention, one unit ADD costs
four primitives per real component: clear W, add source into W, signed add W
into target, clear W. A half ADD adds one halving; a double ADD adds one doubling.
Each old gate costs five, including the two donor-pulse gates. Each new group
has four half ADDs and nine unit ADDs; the donor correction costs four:

| Charge per real component | Old | New |
|---|---:|---:|
| Two groups and restored pulse | `34*5 = 170` | `2*(4*5+9*4)+4 = 116` |
| Both real components | 340 | 232 |
| Extra helpers, copies, scales, child calls | 0 | 0 |

W is the existing private coefficient workspace. It is cleared on entry and
exit, even from arbitrary initial contents; it is **not** an arbitrary helper
whose initial value must be restored. This is the inherited CLEAR contract.
No unpriced source access or intermediate arithmetic is hidden in a coefficient.

Five existing rank-one B climbs are moved to the front of the replaced event
window `[13021:13060]`. The checker verifies that each was before the first
scalar touch of its own register, and that every new operand is then in frame 3.
Under the inherited register-local climb interface, these climbs commute past
the preceding scalar operations on other logical registers. Each scalar ADD
returns its private coefficient work to zero. There are no centers, adapters,
phases, or other native events inside the window. The ordered list of **all**
non-scalar events is identical before and after the splice; no climb or recursive
child is omitted. Actual hosting and shared-work realization remain admission
obligations below. The old cleanup remains literal and unchanged; this package
does not regenerate the canonical word or claim a second saving in cleanup.

## Verification and observed results

The exact sparse macro replay checks 17 arbitrary logical columns locally.
A separate dense rational interpreter checks the actual primitive instructions
on those columns plus arbitrary W, including W's erasure. The whole scalar
projection is checked on 704 logical and 8 private-center columns: both versions
give the expected data shear and return every arbitrary logical helper, with
private centers erased. This projection deliberately omits native actions;
it is not a finite replay of the complete physical supplier.

| Complete scalar-program charge | Old | New |
|---|---:|---:|
| Macros, either orientation | 19,693 | 19,686 |
| Real-component primitives, forward | 198,766 | 198,658 |
| Real-component primitives, backward | 198,814 | 198,706 |
| Positive-prefix bits, forward/backward | 52 / 68 | 52 / 68 |

The baseline counts and exact positive-prefix receipts match the retained
independent replay. The backward positive majorant increases slightly, from
`14824960514781440791821/64` to `14824971130054817125485/64`; both are below the
inherited 192-bit scalar charge. The forward majorant stays
`2765345294379392599/1024`. These are scalar/Horner majorants, not newly proved
global precision bounds. The paid profile in both orientations stays
`{1:2412, 2:418, 3:432, 4:142, 5:82, 8:8}`.

All 12 negative controls must reject: in each orientation, omit a target
preparation, omit a restoration, omit the donor correction, reverse its sign,
use a wrong frame, or omit the final coefficient-work clear. The preparation
control exercises arbitrary initial targets that a zero-target-only test could
miss. No floating-point tolerance, random evaluation, or finite field is used.

The registered replay, metadata validation, candidate-stream export, selected
baseline binding check, and committed-byte/source-history preflight are the
relevant checks for this isolated package. The full selected
`make frontier1094-verify` cold replay is **not run**: no selected artifact is
changed, and no new full-provider admission is claimed.

## Scope, selection and predecessor credit

OS seed **24** assigns the complex-supplier track. Among the 20 maximal
same-frame B runs of at least ten gates, index `24 mod 20 = 4` selects this
block; the complete selection domain is in `RESULT.json`. This was a bounded
constructive experiment, not an exhaustive synthesis search: inspect this
block, apply one restored target-chain mechanism, and stop at the first useful
verified replacement. No minimality or impossibility claim is made.
The three candidate tasks, overlap coverage and local coordination fallback
are in [CLAIM.md](CLAIM.md). [TASK.json](TASK.json) explicitly changes the
rank-shape card's scope to a scalar side result. The recursive profile ceiling
cannot improve from this change alone; it does not pass the card's five-percent
gate or justify further construction rounds.

Target-basis compensation is predecessor work: Sricharan Vagvala / @theon199
[#749](https://github.com/CrocSwap/integer-mult-bounds/pull/749), ToikY
[#901](https://github.com/CrocSwap/integer-mult-bounds/pull/901), and Ross
Richardson [#932](https://github.com/CrocSwap/integer-mult-bounds/pull/932),
with Oscar Fennell and dd-hemant's antecedents credited in the repository.
The contribution here is its source-specific application to this selected
nonzero-frame B readout, including its donor pulse, dual, primitive bill and
reproducible splice. Concurrent thu-nmrc
[#4218](https://github.com/CrocSwap/integer-mult-bounds/pull/4218), inspected at
`81f5cccf92cde2a55fcac298b9d204526a31a409`, resynthesizes historical #799 A-prefix
blocks; it is credited as adjacent work and is not a dependency.

The selected source retains Rohan Arun's #1094, Jeremy Kothe's #1087/#799,
icekylinx's gauge44, Chafik Boukhalfa's #741, and their recorded predecessors.
Primitive charging follows the retained #558 (eumemic) -> #552 (Dugongue) ->
#531 (icekylinx) invoice convention. No predecessor implementation is imported.
[SOURCES.json](SOURCES.json) records base Git blobs and SHA256 pins. The sole
live input is the unchanged selected replay archive, SHA256
`f1da80610bf33c58527f18ad63b4350d0b864e1d4486141ee17ac9bed4d529d6`;
its four consumed members have separate byte pins in `verify.py` and `RESULT.json`.

Prepared for and attributed to **@CubeJerry**, with substantial OpenAI Codex
assistance in selection, derivation, implementation, verification and writing.
New work is Apache-2.0; retained sources and their attribution are unchanged.

## Open next questions

Can this exact exported event stream pass the existing complete native
frame/phase/normalization admission and then the actual mixed-provider invoice?
The first step is to feed it into the retained local admission checker in an
isolated candidate directory, explicitly accommodating the five commuting
climbs. This would determine whether the scalar saving is usable under the
compiler's accepted grammar. It remains unperformed; the current package
certifies the local identity, scalar bill and stated frame conditions only.

Even successful admission would leave the unchanged recursive profile and
other supplier/assembly constraints binding. The inherited all-size compiler,
common-label and mutable-source realization, whole-call hosting,
precision/tape/recovery, analytic transfer, and bit H1-H5 assumptions remain.
There is no claim of an unconditional multiplication theorem, global optimality,
or a larger κ. The structured handoff is in `TASK.json`.
