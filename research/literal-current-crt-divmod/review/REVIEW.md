# Independent review of the actual current-leaf divider

**Verdict: PASS within the stated primitive and source-substitution scope.**
Prepared independently by the complementary research agent for Jerry Chen /
@CubeJerry with substantial OpenAI assistance. This is an independent review
of the new source binding and physical implementation, not a new division
algorithm, a fully lowered CRT producer, or a new multiplication bound.

The reviewed base is `e54523517d0f03e58352e647c403a5af3e525a57`, and the retained
header/key dependency is CubeJerry commit
`4c7cee36538bb48dc2598806af2ca42554fa63c0`. Exact scientific byte pins and the
336150-location/68-role graph digest are in `RESULT.json` and `FREEZE.json`.
The final proof includes the distinction between the emitted graph and the
Python verifier's instrumentation/watchdog. No scientific correction remains.

## Independence and executed evidence

`independent_check.py` implements a separate sparse R/W/M/J/H interpreter,
translated selector windows, direct native backing access, and independent
integer quotient/remainder oracles. It imports the graph constructor and
binder only as objects under review. It does not import the new author's
hardware implementation or execute the old divider as its numerical oracle.
The retained B9 header/source implementation is explicitly an external
provider in the actual-join checks.

The source-bound comparison uses an independent allocation-only model of
the old primitive. Python integer prefix remainders decide its allocations;
the model never invokes old Word arithmetic. It then constructs the entire
64-slot live/free bijection from the observed new boundary. This is
complementary to the author's old-divider clone comparison.

Executed normal and `-O` runs agree exactly. They cover:

- All 22272 numerical instruction/slot dispatch paths, complete logical
  continuations, and all unexpanded logical instructions.
- Five complete literal divide/retire lifecycles, widths 4, 5, 7, 9 and 17,
  changing physical slots, translated descriptor origins, and old inactive
  histories up to 8193 cells. These execute 261236 instructions.
- Two actual forward/inverse source and payload roundtrips, plus a returning
  wrong-source-phase roundtrip. All six legs execute 511510 new divider
  instructions and expose twelve complete owner relations.
- Twelve core controls and a wrong-dispatch-port mutation. The controls
  include descriptor aliasing, short fields, malformed digits, divisor
  admission, missing grants, physical backing aliasing, returning stale
  operands, wrong quotients, borrowed-live corruption and incomplete erase.
- Authentication of all 65 retained inputs against their byte length,
  SHA256 and Git blob records. Remote-origin publication authentication
  remains the orchestrator's separate gate.

The wrong-phase mutation changes the initial finite phase from zero to one.
It still returns and restores the complete source/payload fixture, since
the literal divider is also mathematically correct at the earlier call.
The independent source oracle nevertheless detects all four changed call
identities: `(1,s)` was substituted for the required `(s,t)`. Thus a roundtrip
or successful halt alone does not establish this contribution's source bind.

## Universal source trigger

I checked the retained `encoded-current-crt/producer.py`, raw Word arithmetic,
NodeEntry, the actual frontend, entry lifecycle, persistent owner bank and
the one-line inverse producer specialization. The source argument is
uniform over admitted one-left/one-right leaves; it does not infer call six
from sampled slot numbers or a bounded transcript.

Initially `prefix=1` and `lower=0`. The first left modulus is `s>1`.
The raw calls are: `1 mod s`; the sole Euclidean iteration `s divmod 1`;
its quotient reduction `s mod s`; `0 mod s`; and `left_value mod s`.
After that update the prefix is exactly `s`, including the padded-coordinate
branch, which changes only `lower`. No add, modular multiply or exact
product contributes another raw division. The next raw call is therefore
`s divmod t`. The inverse specialization changes a later coordinate update,
so the same derivation applies before its sixth call.

The half counter is unary. Testing its first mark followed by RIGHT
distinguishes exactly one axis per half. The concrete read/move/test/rewind
sequence costs eight native actions and returns its head. Source widths
`u,h` give the actual guide `P=u+h+1`; `t<2^h<=2^(P-2)` supplies the primitive's
high-bit reserve. The finite phase saturates after six. Nonleaf and all
other raw divisions remain the inherited provider.

## Owner and history argument

The numerical ports are exactly eight borrowed iterator guards and 56
owned bank ports, at bank indices 3 through 58. They are not all 63 bank
ports. The separate template, guide, group streams and output keep their
own roles. Every observed replacement independently checks these actual
object identities, the complete backing bytearrays, every head, and all
incoming live bytes.

The new divider needs only two reserved output owners; the old primitive
simultaneously allocates a scan copy and two outputs and may exchange
temporary roles later. Exact allocation traces and output slot numbers are
not equal. At the primitive return, fix entry-live slots, pair old/new Q and
R, and pair the two ordered free stacks. This yields a full bijection.
All free bodies, including inactive old tails, are blank. Identity and
alias tests are preserved, and the ordered numerical operations never
branch on slot magnitude.

The final `tuple(arena.live)` cleanup is correctly treated as a weak
simulation step: disjoint erasures commute, after which free-stack positions
can be paired again while fixing surviving live objects. This argument is
about related executions; it never moves real backing or historical stock.
The final Entry lifecycle fixes the eight borrowed guards and retires the
56 actual owned ports. The smaller new peak occupancy cannot invalidate a
capacity check that succeeded on the old admitted path.

Each physical numerical owner retains its own maximum of old extent and
`P+2`. The source replay includes P=11 followed by P=6 or 7 on the same
bank. Its old tails remain blank and are not silently truncated. Standalone
cases additionally retain much longer histories and external sentinels.

Selectors reuse four actual private marker owners. Their old one-cell
extent is insufficient, so the explicit eight-cell grants and 28 additional
backing cells are essential premises. ACQUIRE clears all 32 cells and each
call returns the same four blank owners before header/key control. The
finite six-bit dispatch returns each selector head before its physical
operation; the structural projection checks every one of its 64 leaves.

## Numerical and cost review

The prefix invariant is `v_k=D*q_k+r_k`, with `0<=r_k<D`. The zero high
divisor bit ensures `2r_k+b<2D<2^P`. The low-to-high comparison retains the
most significant differing bit; subtraction cannot finish with a borrow.
The source/N and divisor/D ports are read-only, and all head returns are
literal moves. RETIRE erases both output bodies and RIGHT delimiters while
preserving LEFT and exterior cells. Malformed-entry cleanup is excluded.

The separate projection obtains eight descriptor reads, fourteen descriptor
moves and seven jumps before each numerical operation: 29 instructions.
Reads therefore cost 30 and write/move paths 31 including their return jump.
It also checks every target and the fixed physical port; a port mutation
fails independently of the arithmetic examples.

The logical invoice agrees with the loop derivation and exact execution:

`L_div = 18P^2 + 36P + 458 + (12P+9) popcount(floor(N/D))`.

The six pair checks cost 306; initialization costs `17P+27`; each digit's
base work costs `18P+19`; each quotient one costs an additional `12P+9`;
final control and return cost 125. Retirement costs `14P+131`. With
ACQUIRE=89 and each batch of four setters=124, the full standalone lifecycle
is at most `337+31(30P^2+59P+589)<2^14(P+2)^2` for P>=4.

The actual source uses its original consumers and frees, not redundant
RETIRE. Independent actual backing access increments only the arena meter;
the backing Port meter stays unchanged. Descriptor actions enter the
marker meter. The review subtracts the new numerical action count and the
unchanged header-native count from the source bill once, and subtracts the
descriptor count from the adapter bill once. The residual adapter count
is 14. The eight-action eligibility query remains in the retained source
bill. The external `C_bind=256+32I+16R+16384J` and grant cost remain separate
units. No speedup or common bit tariff is inferred from unlike meters.

## Limits and reproduction

This review accepts the explicit current-source admission, persistent-bank
and other arithmetic providers. It does not lower their acquisition,
Euclidean iteration, finite metadata binder, radix orchestration or the
whole numerical caller. It does not assert failure rollback for malformed
core inputs. Receipt/history arrays, optional observer and Python watchdog
are verification instrumentation, not physical owners or graph semantics.
All five foundational assumptions and the selected complete kappa remain.

When installed beside the reviewed package, run:

```sh
python independent_check.py
python -O independent_check.py
```

From this separate review directory, pass `--package` with the reviewed
package path. The default is read-only and prints JSON. `--write PATH` is
an explicit optional receipt output. Prior source and hardware credits are
preserved by the reviewed package's provenance; the independent review
does not claim its inherited numerical algorithms as new work.
