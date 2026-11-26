# Independent review of the adaptive command-interface bridge

Decision: **accept AS as a written conditional theorem about the exact
source Certified predicate, and accept ResourcePotential as checked
natural-number arithmetic**. This does not instantiate the adaptive
supplier or prove its tape implementation. The distinction between
the written interface theorem and the compiled arithmetic is essential.

Reviewed files:

- lead/adaptive-source-interface.md, SHA-256
  203245a355c5950ffa49e1b4ce2873d8c06d6d9e819e1ff6b27257cd05231903.
- lead/formal/ResourcePotential.lean, SHA-256
  e6bf8cfe8a0df6b4b5c61db193343036ff920bdf6442c1550cb88cc20c33c0df.

The primary source was read independently at OpenAI math
3344da59991ed94f9ba711217b29c1d760badfa6:
InterchangeROMRecursion, InterchangeBQuestClock,
InterchangeBQuestResolve, InterchangeBQuestMixedResolve and
InterchangeBQuestCore, under lean/OAI/Computability/NearSquareRoot.
The actual definitions and proofs support the review below.

## 1. The source already has the general clock

The source resolve_controller takes an arbitrary fare \(X\to\mathbb R\).
Its width-power theorem is a specialization. The general clock theorem
exists_floor_clock also takes an arbitrary natural-valued local allowance
\(w\), a repeated child list and a nonnegative fare.

The new bridge therefore need not formalize real-to-integer rounding
again or infer a variable fare from a fixed-exponent theorem.
AS correctly reuses the stronger existing theorem.

Certified is existential in one natural constant \(K\), followed by
all requests, environments, decks and base caps. Its bounds are
\(K(\mathrm{time}(x)+1)\),
\(\mathrm{base}+K(\mathrm{space}(x)+1)\), and
\(K(\mathrm{space}(x)+1)\). A selected width-exponent theorem does not
by itself give a leading constant uniform over a changing selection
parameter. A common register cutoff does not remove that quantifier issue.

## 2. The mismatch is correctly identified

Sharp uses the same \(CV\) for local running time and payload retained
above a contracted child. Its full-volume branch retains only the
specified logarithmic header. Inflating \(V\) to pay \(Vm(h)^K\) work
also inflates the payload budget, defeating the common linear cap.

The source Body and prepared batch rules demonstrate the danger:
generic time-to-space conversions can charge the full preparation clock
as temporary stack growth. A slower computation that actually uses
small workspace needs a direct BoundedFits workspace proof.

The separated contract explicitly assumes that stronger physical fact.
It keeps one fixed command \(c\), actual local time \(w(x)\), fixed
payload coefficient \(C\), and descriptor allowance \(B(V)\).
It therefore identifies a missing implementation interface instead
of silently changing the meaning of the source volume.

## 3. Exact command, environment and multiplicity

The revised text states BoundedFits \((c::env)\ c\) for both the
body and inductively supplied child executions. The command .tie c
appears only after closure. This matches resolve_tie_exact literally;
a different command selected at each input width would not qualify.

All deck and base-cap quantifiers remain present. The body contract
uses the actual query/reply trees, and children are finite lists.
Repeated requests remain repeated time summands. Space uses their
peak, with zero for an empty list. The local \(w(x)\) includes recursive
jumps, decoding, preparation, returns and cleanup. These details are
necessary for the exact-command conclusion.

## 4. Time closure has no omitted rounding loss

AS2 is the hypothesis of exists_floor_clock after coercing \(w\) to
the reals. For one fixed natural \(K_0\),

\[
 w(x)+1+\sum_y\lfloor K_0P(y)\rfloor
   \le \lfloor K_0P(x)\rfloor.
\]

Flooring each child is crucial. Ceilings would add an error proportional
to the number of occurrences. The source theorem sums the individual
floor upper bounds and needs no bounded child count for this step.

Set \(t(x)=\lfloor K_0P(x)\rfloor\). The body fits that clock.
resolve_tie_exact adds its single outer tie transition.
The source floor_clock_le_mul_ceil bounds \(t(x)\) by
\(K_0\lceil P(x)\rceil\), so \(K_0+1\) pays the final time expression.
The algorithm does not evaluate the analytic fare.

## 5. Potential, empty lists and common constants

For

\[
 Q(x)=3CV(x)+(h(x)+1)B(V(x)),
\]

a small child satisfies

\[
 CV(x)+3CV(y)\le3CV(x),\qquad
 (h(y)+1)B(V(y))\le h(x)B(V(x)).
\]

The first inequality uses \(3V(y)\le2V(x)\); the second uses strict
height descent and descriptor monotonicity. They prove the
small-child potential inequality. For a full-volume child,
volume monotonicity pays the payload and the height decrement
pays one parked \(B(V(x))\).

For empty lists the cap must still cover its local term.
The checked payload_le and descriptor_le supply exactly these cases.
Taking the source childPeak maximum therefore bounds both data
and return stacks. Sibling reuse is a maximum, not a sum of separate
workspace allocations.

AS1 gives \(Q(x)\le(3C+D)V(x)\). A final constant at least
\(\max(K_0+1,3C+D)\) converts the exact bounds into Certified while
leaving the ambient base cap unscaled. This establishes the stated
conditional command-level result.

The revised application paragraph now specifies
\(B(V)=O((1+\log V)^d)\) for a fixed degree \(d\).
Together with \(h=O(\log V)\), this yields AS1 by exponential
domination and finite initial adjustment. An arbitrary polynomial
in \(V\) would not justify that assertion. AS itself takes the
descriptor budget as a separate hypothesis.

## 6. Independent kernel check and remaining obligations

ResourcePotential was read, copied byte-for-byte into a fresh
temporary directory, and compiled with an isolated import path and

    lean -DwarningAsError=true ResourcePotential.lean

under Lean 4.35.0, commit
eb6cafb7290e8bd5f2937522d8d804f58f02bafc.
Both hashes were e6bf8cfe8a0df6b4b5c61db193343036ff920bdf6442c1550cb88cc20c33c0df.
It passed without warnings. The six printed dependencies are subsets
of propext and Quot.sound. The receipt is
resource-potential-independent-verification.json.

This check proves the small/full/local/max/linear-cap arithmetic.
The file imports only Std. It does not import the OpenAI request
machinery or kernel-check AS's instantiation of it.

A formal adaptive supplier still requires one actual request-decoding
command, separately bounded preparation and workspace, the literal
query/reply contract, and refinement through the interpreter and
visited-tape-cell theorems. A recurrence, a live-array count or
input-dependent code selection would leave those obligations open.
Numerical error and the outer integer caller remain outside AS.

The reuse decision is sound: the general analytic fare and
exact-command clock already exist. The next proof should concentrate
on the separated physical body and actual machine refinement.

Prepared independently by S005 Route C for @CubeJerry, with substantial
ChatGPT assistance. No upstream OAI build, comparator run, full supplier
formalization or new unconditional multiplication bound is claimed.

