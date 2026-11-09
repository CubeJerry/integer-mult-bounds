# Current native header for the first caller-local helper

This implements the missing encoded header handoff at the first normalized
caller-local right-monomial cut of selected raw MOVE 9896. The actual source
maps raw helper 236 to owner **3356** and wraps its token in a nested
`caller-local` tuple. A typed binder accepts exactly that source cut. Literal
physical tables construct the nine-vector descriptor required by the
published current-format phase provider, preserve the full parent header,
and retire the temporary view.

The scope is fixed ambient **N=145, gamma=1**, under the established helper
placement/contact geometry and a valid ordinary parent header. The new program
does not generalize product/compiler multiplicities, execute a full selected
Fourier caller, or supply a new phase theorem. The selected #6030 kappa and
**all five assumptions remain unchanged**.

## Result

An ordinary parent has `e=145*f+r`, `0<=r<145`, and active origin
`z=entry_start+r*K`. The existing normalized first-helper placement exposes
its nine vectors at `z+(i*f+j)*K+rho`, for `i<9`, `j<f`.

The native view changes exactly three of the 23 encoded values:

| Field | Native view |
|---|---|
| selected_axes | `9*f` |
| entry_start | existing `active_start` |
| remainder | `0` |

The other **20 values**, including f, remain unchanged. Complete row extent,
within-row address width, numeric record width, outer/row multiplicity, stock,
precision/reservation parameters, current selected residue, back origin and
cutoff are preserved. The ordinary remainder remains a spectator before z;
the other 136f active chunks remain spectators after the nine-vector span.
Every numeric coefficient stays present through the predecessor's existing
paid suffix-folding mechanism.

The temporary view is a separate read-only raw-binary descriptor. The parent
remains the header for ordinary recursion and global selected-XOR routes.
Accepting a route record does not by itself prove field placement: this exact
placement is inherited from [#6878](https://github.com/CrocSwap/integer-mult-bounds/pull/6878).
No new route is needed at the chosen first helper; broader occurrences are
excluded.

`header_view.py` emits 2,742 PREPARE and 475 RELEASE instructions over fixed
local reads, writes, unit moves, jumps and terminal states. It has 39 private
ports plus the borrowed parent. Runtime lengths and values stay on encoded
tapes. There is no shape integer decoded into host control, dynamic tape
allocation, numerical payload callback, or scan to an old high-water address.

For parent-header body length E, the complete prepare/retire charge is at most
**1000E+10000 local instructions**. [PROOF.md](PROOF.md), section 5, derives
this bound from individual decoder, multiplier, copy, encoder, rewind and
clear scans. Historical backing is retained: with M the largest prior E,
the added bank uses at most its supplied initial prefixes plus `39*(2*M+1)`
cells. Fixed source/table/native construction has separate template constants.
The complete relative invoice remains

`C0 + T_source_routes + T_native + 1000E + 10000`.

The predecessor's native setup, format/cleanup cost, ordinary tariff and
retained backing remain fully charged. The new metadata interface does not
improve a native exponent or meet the selected tariff by itself.

## Exact source binding

The witness executes the authentic current caller constructor until it
computes this event:

```python
Event('SERVICE', (3356,),
      ('caller-local',0,0,
       ('move-in','local',9896,('MOVE',236,3,7,False))), 0)
```

The raw helper is ordinal 28, giving `32*104+28=3356`. Its initial frame is
empty frame 3; its target is rank-nine frame 127. The selected native monomial
has nine address variables, distinct from the intervening paid rank-one job.
The typed adapter preserves the actual owner and passes the established raw
token to the unchanged selected phase service. Other owners, cuts, nesting,
boolean/integer substitutions, routes or gamma values reject.

The source-prefix and ordinary-header witnesses are concrete current-source
bindings. Their finite execution is not presented as a complete caller replay.
All-size correctness follows from the encoded-program argument and the stated
parent/native premises in [PROOF.md](PROOF.md).

## Executed evidence

[DESCRIPTOR-RESULT.json](DESCRIPTOR-RESULT.json) records:

- 18 physical descriptor cases with f=1,2,5 and remainders 0,1,8,9,13,144;
  complete 23-value and byte comparisons, nontrivial outer/row/stock values,
  trailing spectators, translated origins and private cleanup.
- Four long encoded shape descriptions, plus a large-then-small history.
  Reused and fresh small calls both cost **47,819 physical actions**, while
  retaining **37,987 versus 2,973 private cells**.
- An actual ordinary-source geometry table whose output port is borrowed
  directly by the new producer, with no intervening decode/reload/converter.
- Thirteen typed source/route controls and a rejected f=0 header followed by
  a valid retry on the same physical bank.

[PHASE-RESULT.json](PHASE-RESULT.json) records two actual selected phase-control
calls through the produced view, both at f=2. Their phases are 2 and 1, and
their complete measured physical actions are 24,210,731 and 73,878,991. The
checks exercise inverse phase, the repeated scalar constant and a
discriminating wrong-residue input.

These phase fixtures use locally sufficient `H=f-1` reservations. They retain
the ordinary `e=145*f+r` metadata and its complete trailing spectators, but
they are **not full global root reservation/precision admissions**. No numeric
parent packet or Fourier child is executed. `full_native_invocations=0` and
`full_global_reservation_admission=false` are explicit receipt fields. Every
phase value comes from the unchanged real encoded phase accumulator; no
synthetic numerical service provides a result.

The [independent review](review/REVIEW.md) uses a separate sparse physical
tape model, interpreter, header encoder and mathematical oracle. Its normal
and optimized receipts agree byte-for-byte. Eight successful cases, a
history case, three mutated instruction graphs, three malformed binary
controls and fourteen typed source/route controls are included. This is an
independent implementation by an OpenAI-assisted collaborator, not independent
human or proof-kernel acceptance.

The metadata fixtures establish syntax, local-layout transformation, source
binding and literal execution. They do not certify every upstream global
qF/qB, stock, precision or native-supplier admission from their supplied
numbers. The complete native source-level implementation also retains its
own endpoint/error contracts; only the new header graphs are exported as
literal tables here.

## Reproduction and source integrity

From the repository root:

```sh
python3 scripts/research_package.py --package research/current-native-header-view --check-only
python3 scripts/research_package.py --package research/current-native-header-view
```

The four registered commands run the author replay and independent checker,
each in normal and optimized Python. Direct author replay is:

```sh
python3 -I -B research/current-native-header-view/verify.py
python3 -I -O -B research/current-native-header-view/verify.py
```

Every direct checker uses a fresh bytecode-cache namespace. Both author modes
compare the exact committed descriptor and phase receipts; the independent
wrapper compares the exact frozen review receipt. The finite table hash is
`3e8bdb02323df791291cd7dd002483ebcdd8b02874b4ae53092bcb6860e08b1e`.

[DEPENDENCIES.json](DEPENDENCIES.json) pins all 109 retained files by public
repository/commit/path, Git blob and SHA256. The current phase closure is
vendored unchanged from
`CubeJerry/integer-mult-bounds@7d1ff23714e6f9182c1d0ff9214f65def2f30e04`.
The current row Builder lineage is pinned at
`5c59d247d51c6e1fca0dead3ed2139b6802b3a15`; the placement proof at
`41febf890fbbb852c6059d4c0cc8c593ae9dfa5c`. Authentication precedes imports.
[VERIFICATION.md](VERIFICATION.md) records the exact completed gates and limits.

## Open next questions

1. Consume a completed route certificate for one additional product/compiler
   occurrence, including its actual owner, multiplicity, entry and inverse
   normalizers. Another token wrapper alone is insufficient.
2. Join a reviewed complete MOVE service on this same complete owner field,
   common grid and signed headroom. The numerical Fourier-child/width
   contracts remain separate blockers.
3. Bind a native supplier with a complete tariff matching the selected node
   bound. Include setup, stock, return and historical backing; no exponent
   improvement follows from this metadata change.

The structured scope and next steps are in [TASK.json](TASK.json). The local
overlap claim records the distinct concurrent raw-owner atomic MOVE work;
its provisional code is neither imported nor assumed verified here.

## Credit

Prepared for @CubeJerry with substantial OpenAI assistance in source analysis,
proof, implementation, testing and documentation. Apache-2.0. Credit remains
with the P104/current lifecycle and row-dispatch contributors, JoyboyBrian's
retained row Builder and its cited source semantics, #6878's compiler/layout
lineage, and the authors of #3087, #6293, #6930 and the published current-format
phase adapter. Their computational bodies and notices are unchanged. No new
phase algebra or full selected-assumption admission is claimed.
