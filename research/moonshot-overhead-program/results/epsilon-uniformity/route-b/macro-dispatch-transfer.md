# A finite macro executor can make description traversal additive

Status: **proved conditional compiler lemma**. The complete library of
physical primitive bills for the OpenAI source has not been implemented or
verified here. This lemma isolates the specific interpreter expense that can
be removed and the semantic expenses that cannot be removed by dispatch.

## 1. Resource contracts

Fix a finite list of primitive opcodes and a finite-alphabet, fixed-tape
implementation for each opcode. An opcode receives a finite binary header
`z` and streams in declared regions. Its proven contract specifies:

- the exact map on its data, including error allowances if it is a numerical
  primitive;
- a bound `Q(z)` on **actual** head movements and steps, including reading
  coefficients/tables, input/output positioning, arithmetic and cleanup;
- the intervals it may visit, its final head positions and its region-reuse
  behavior.

The functions producing/checking these bounds are fixed algorithms. An
uninterpreted gate with unit cost, an arbitrary program advertised as an
opcode, or a table lookup with no physical implementation is not a legal
primitive. The finite opcode list does not grow with the template.

A template `D` is data of length `d` in a fixed grammar. It specifies a finite
sequence of these opcodes, well-founded child calls, and sequential bounded
loops. Descriptors are binary. It is permissible to keep a coefficient table
as data, but its accesses remain in the primitive's `Q` bill. Let `J` be the
number of executed macro instructions and child transitions, after expanding
the template recursion but **not** its primitives' per-record loops. Let
`h` bound the bit length of one live descriptor and return frame.

## 2. Dispatch theorem

**Theorem M1.** One fixed multitape machine can execute every legal template
with total time

```
sum_over_executed_primitives Q(z) + O(J poly(d+h+1)),             (M1)
```

and, in addition to the primitive/live-stream regions,

```
O(poly(d+h+1) + depth * poly(h+log(d+2)))                        (M2)
```

control cells. The polynomial degrees and outer constants are absolute,
depending only on the fixed grammar and opcode library. Fixed tape count
and alphabet are preserved. If primitive region contracts and the caller's
stack discipline give a uniform `O(n)` visited-cell invoice, (M2) is the
only additional control region that must fit the same bound.

### Proof

Store `D` on a fixed description tape. A fixed parser scans at most its
whole `d`-bit region to find the next instruction and its binary operands.
It uses standard polynomial-time binary arithmetic to derive the header
from the current descriptor. A finite control branch dispatches to one of
the finitely many primitive implementations. That primitive's machine is
part of the executor's fixed finite program; it is not simulated by scanning
`D` at every one of its raw bit operations. Its description-tape head can
remain parked, except for accesses explicitly included in `Q`.

On a child call, push the return instruction index and parent descriptor to
the end of a control stack. On return, pop them, rescan `D` to the indicated
instruction, and continue. There is no uncharged random-access jump:
every rescan costs at most polynomial in `d+h`. The same parser/interpreter
handles all recursion levels, so there is no tower of nested universal
interpreters. Binary loop counters and their head returns are part of this
control charge or of the primitive charge, according to the fixed grammar.

Summing this actual per-event cost over `J` proves (M1). `D` is retained once;
the parser's polynomial work region is reused, and only the depth-first
return stack is simultaneously live. These regions
start at fixed marked origins and are reused, so their maximum extents
bound their entire visited-cell union, giving (M2). The primitive library,
parser and a constant number of stack/description streams use one fixed
number of tapes. ∎

### What the theorem does not say

A primitive might itself scan a `d`-bit coefficient list for every record.
Then `Q(z)` contains that cost. A dense row map may use a number of arithmetic
operations proportional to its dimension squared. That cost also remains.
M1 removes generic *whole-program dispatch* at every primitive bit step; it
does not imply that templates of arbitrarily large arity have bounded
execution constants.

## 3. An explicit polylogarithmic control bound for shrinking templates

Suppose a template of length `d>=2` has at most `d^c` macro instructions or
children per node, recursion depth at most `c log_2(k+2)`, and at most
`d^c(k+2)^c` top-level pieces, for one absolute constant `c`. Suppose every
descriptor has length at most `poly(d+k)` with an absolute degree. Then

```
J <= d^C (k+2)^(C log_2(d+2)),
dispatch work <= d^C (k+2)^(C log_2(d+2))                      (M3)
```

after enlarging an absolute `C`.

Indeed a tree of branching `B<=d^c` and depth `t<=c log_2(k+2)` has at most
`(B+1)^(t+1)` nodes. Multiplying by the top-level pieces and per-node parsing
polynomial preserves the form (M3). A fixed number of nested families, each
with this property, multiplies finitely many such bounds and only enlarges
`C`. The proof handles integer floors by replacing bounds with `k+2` and
`d+2`; it does not assume exact powers at every input length.

If `k=Theta(log n)` and `d` is fixed for a chosen template, this control is
`poly_d(log n)`, hence eligible to be an additive setup/control expense at
large enough `n`. When `d=d(n)` grows, it must pass an explicit inequality
such as (P1) in `preflight-selection.md`; calling it “polylogarithmic” is
not a uniform estimate.

## 4. Computing bills from the same grammar

Suppose, additionally, the primitive bills and shape/region bounds can be
computed in `poly(d+k)` actual steps per macro node, with integer output
length `poly(d+k)`. A fixed compiler can enumerate the expanded macro tree,
sum its time bills, and combine its visited-region bounds in time of the
form (M3). Per-record loops remain compressed in the primitive bill; a
stream of volume `2^k` is described by an `O(k)`-bit length, not enumerated
by the preflight.

The space rules must distinguish sequential region reuse, parked parent
frames, and fresh stacks. Summing or maximizing arbitrary “live memory”
numbers without a common location/reuse contract would not bound all
visited cells. With the declared fixed-origin regions, a complete bill is
a sound finite derivation in the plan interface of `preflight-selection.md`.
The checker can recompute that derivation with the same resource order.

This gives a concrete sufficient route to a fast preflight; it does not
assume access to the best candidate or to its future observed runtime.

## 5. Source applicability and remaining work

At `openai/math@3344da59991ed94f9ba711217b29c1d760badfa6`, the tape
`uniformity.tex` serialization already describes sequential track scans,
splits, merges and depth-first parking. `walsh.tex` and `interchange.tex`
have fixed-branching, logarithmic-depth recursion for a fixed template.
These are compatible high-level shapes for M1–M3. The source's original
transition-list interpreter instead allows a candidate-dependent constant
for scanning a whole list on every simulated step.

To apply M1 as an actual replacement, one still must supply and audit the
finite primitive library, particularly dynamic rational/radix address maps,
finite-field/extension coefficients, data-dependent control tables and
their numerical bounds. Proving a finite vocabulary at the mathematical
level is not enough; its algorithms and head/region contracts must work
over one fixed physical alphabet as their headers grow.

Route A's coarse tower compiler already prices these expenses by fixed
powers of a very large `S_j`. The dispatch lemma explains a possible finer
separation of setup from semantic execution. It does not, by itself,
improve that tower-height envelope or establish the bounded physical bill
needed for the exact endpoint.

Open next question: implement one complete nontrivial interchange template
in this grammar, compute its exact time/region bill and compare the bill to
the source's recurrence, preserving every child volume. A failed resource
contract should identify the specific primitive that requires a stronger
invoice or a different representation.

Credits: @CubeJerry; the OpenAI tape source's stream serialization and
parking discipline; concurrent S002's distinction between additive
description space and proportional stream space; classical interpreter
and resource-analysis methods. Developed with ChatGPT multi-agent assistance.
