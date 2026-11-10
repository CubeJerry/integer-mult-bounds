# Independent lead review of complete coded row services

Reviewer: lead research agent, separate from the dispatcher author.
Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
Reviewed author commit: `196ba66413ecb6c9801b059e72251d6d06342824`.
The graph SHA256 is recorded in RESULT.json.
Prepared for Jerry Chen / @CubeJerry with substantial OpenAI assistance.
This is model-assisted mathematical/source review, not human or kernel acceptance.

## Outcome

**Pass for the stated homogeneous row-service interface.** I read the graph,
actual Controller and Stack/callback contracts, universal proof and complete
invoice. I independently derived the parser, transport, state count and all
four callback costs. Selected variable-rank geometry, production descriptors,
native numerical semantics, common tariff and a new kappa remain outside it.

## Independent mathematical derivation

The parser has four phase-zero states, four phase-one states, four bit-prefix
phase-two states and two separator-prefix phase-two states:14 total. Source
probes add16 states and accepted bit edges20. A scan has40 move states and a
three-state rewind, hence73 states. A blank-target probe and two target actions
on every bit edge add60, giving133 for a copying row. The two width-indexed
groups contribute266w states, final field rewinds6w, and final collector
probes w-1. The remaining fixed copies, classifier, bridge rewinds, loops and
terminals contribute126. Thus the total is exactly273w+125, independent of
B,R and depth.

For guide000, source000/001 are accepted; for guide010, only source010 after
a nonempty component is accepted. A frontier is legal only after a completed
separator. Thus data has exactly the supplied component layout. Equal total
length alone is insufficient. The finite field phase then proves the map
r -> (r mod w,floor(r/w)) and its inverse; the machine computes neither index.
The collector's final w-1 probes are necessary to reject a longer later field.

Each copied physical bit costs seven actions. The guide frontier and rewind
add2B+4, hence a copying row costs9B+4. A scan costs4B before that same end
sequence. Descriptor copying costs5B, one frontier probe and two rewinds of
2B+3, giving9B+8 including its terminal. Direct counting therefore yields:

- classify:8B+9;
- prepare:9B+8;
- install:13RB+4R+R/w+9B+3w+12;
- collect:13RB+4R+R/w+4w+4.

Each callback includes one terminal transition; all other successful graph
transitions are single raw actions. Adding the inherited administrative
formula with L_in=L_out=RB and H=B gives exactly equation(1) in PROOF.md.
This is not the complete Controller clock: emitted dispatch, RET tests,
numerical work, setup/input/format production and cleanup remain charged
separately. No ordinary-pass conversion follows from this count.

The actual Controller stages the owner and guide before push. Its outside
bridge/header survive while Stack installs new payload delimiters, so the
child guide is a distinct owned copy. Collection precedes retirement and pop;
the original parent's protected guide and every suspended owner return before
the issuing owner is replaced. For R=w^d, children have w^(d-1) rows. This
proves successful-call termination/restoration under the supplied program and
leaf contracts. It does not promise rollback after partial rejection.

The row-layout space bound is consistent. Every productive tape has a data
sum below2L_root plus path delimiters. The guide body and delimiter stack is
at most(B+1)(d+1)<=2L_root because d+1<=R and B>=1. Outside bridge/header use
at most2L_root plus endpoints. Summing roles gives the stated conservative
envelope. Numerical visits even on productive tapes, inherited PC/control,
and other private-role backing remain explicit additions. Sibling origin
reuse never frees historical blank backing.

## Separate executable evidence

`independent.py` imports only rows.py's graph constructor. A separately written
dictionary-cell interpreter and signed-component stripe/interleave oracle import
no source executor, author verifier, runner or expected receipt. The domain is
90 cases: w=2..9,17,65; three component layouts; and one, two or three batches.
Each tape has a different translated origin and mixed buried prefix. Before
collection the checker replaces every returned row independently, so returning
the saved ingress would fail. It checks all borrowed bytes, origins and prefix
boundaries. Four controls reject an extra last-field row, short middle field,
empty-component guide and a different same-length layout. The total is
1,439,496 interpreted target transitions.

Normal and optimized independent replays passed:

```sh
python3 -I -B research/coded-whole-row-services/independent-review/independent.py
python3 -I -O -B research/coded-whole-row-services/independent-review/independent.py
```

Expected: `PASS_INDEPENDENT_CODED_ROWS 90 10 4`. The working copy supports
`--package-root PATH`. Default replay is read-only and checks a typed frozen
receipt; regeneration is explicit. These are finite corroborations of the
quantified argument, not numerical-child or selected-compiler execution. The
author's actual Controller/Stack/scalar fixtures provide a distinct binding
regression, whose scope and receipt remain in the package.
