# Finite native tape programs in the released machine model

The [finite-table translator](node-source-tables.py) exports twelve actual static programs to the published Lean type `TM.Rule`. Together they contain 1,312 program states and 2,432 table alternatives. The true multitape program-counter type, tape-index type and alphabet are finite. An instruction consults one local probe, uses the complete old read tuple for any copies or XORs, writes simultaneously, and moves each head by at most one. The fixed transition table is compiled before any data are supplied. The alphabet has separate symbols for marks, boundaries, binary digits and the blank.

| Program | States | Alternatives | Tapes |
| --- | ---: | ---: | ---: |
| Native direct ternary interchange | 169 | 313 | 17 |
| Packed source-to-destination copy and XOR, each | 138 | 258 | 15 |
| Public schoolbook multiplier | 19 | 53 | 5 |
| Pack and unpack binary leading rows | 79 and 97 | 146 and 178 | 9 |
| Pad and trim ternary leading rows, each | 81 | 149 | 9 |
| Append either signed comparison trit, each | 120 | 212 | 11 |
| External binary/ternary padding and trimming, each | 135 | 252 | 15 |

## Exact machine, address and installation statements

The [bridge](node-source-bridge.lean) proves that a finite zipper step implements the original `TM.advance` for every fixed table and every runtime configuration. An accepted complete-window check proves an exact-length original trace, halting, equality of every entire output tape including its final head, and an upper bound for all physical cells visited. Final equality uses blank-trimmed half-tapes and therefore checks every address of the bi-infinite tape.

The [exact interval proof](node-exact-cells.lean) establishes a stronger conclusion. Starting each recorded lower and upper bound at its actual head, physical cell \((i,z)\) belongs to the original visited set **if and only if** the final recorded extrema satisfy \(l_i\le z\le h_i\). Inductively the new head lies at distance at most one from the preceding head. Any integer cell newly included in its interval has just been reached. The visited-set cardinality is exactly \(\sum_i(h_i+1-l_i)\), including cells erased later.

The [caller-context proof](node-locality.lean) permits independent relocation of each tape and arbitrary occupied data beyond each checked interval. Taking a physical step commutes with overlaying this ambient data whenever the old head remains inside the retained interval. Induction on the actual trace preserves every external position, the exact transition clock and halting. Its exact visited set translates by the independent tape offsets. This applies even when different caller heads start at different absolute addresses.

The [multitape composition theorem](node-composition.lean) installs an arbitrary subroutine on its active tapes with any finite family of fully occupied parked tapes. The exact trace and halting persist; each parked tape adds exactly one visited cell at its stationary head. A second theorem gives the composite clock of two subroutines as the sum of their two actual clocks plus one stationary return transition. Its visited set is precisely the union of the two original visited sets, retaining the same scratch addresses.

The actual zero-width native branch has its own [unbounded physical theorem](node-direct-zero.lean). Supply *arbitrary countable contents and arbitrary starting heads on all seventeen tapes*, place a blank in the cell immediately to the left of each head, and put a zero bit under the width head. The true 169-state table executes exactly five transitions, restores every head and every input cell, and visits the two positions at and just left of every head. Its payload and all metadata sizes are otherwise unrestricted.

## Data-independent control at every size

The [layout theorem](node-data-oblivious.lean) checks the actual direct table, both packed-role tables, the two packed-row conversions, the native pad/trim pair, and the [external binary/ternary range adapters](address-range.md), through all 1,053 nonhalting states. Replace every bit cell of the payload tapes by zero while retaining all head positions, program counters, nonbinary end/mark symbols and complete metadata. Every transition, including a possible halt, commutes with this replacement. Two original configurations with equal projected layouts consequently have matching traces at every length, identical halting times and exactly the same original visited set. This theorem permits arbitrarily many independent data bits, arbitrary physical tape contents and every legal width, prefix, gap and suffix. Its proof checks the branch table, the source/destination classes of each copy, the three classes of every XOR and each constant write. Each actual payload probe takes the same alternative for zero and one.

The [superposition proof](node-linear-tapes.lean) takes two original inputs with a shared layout and forms their pointwise binary XOR on data cells. At every time for which the first input has a physical trace, the second and the combined input have traces of that exact length. Their endpoints combine in the same way, including all writes, heads and metadata. Thus the nine checked programs compute linear maps over the binary field on their occupied data, at every admissible layout and width. The basis theorem consequently reduces any proposed additive output map on \(v\) independent data bits to its zero-word and \(v\) singleton physical traces. This uniform claim uses the actual instructions and does not presuppose which coordinate map they implement.

The two [signed tag appenders](node-affine-tags.lean) use the same branch geometry and append fixed digits that can equal one. Replace every data-writing constant one by a read from an added unit bit; this makes both 120-state tables linear on their extended inputs. Setting the unit bit to one gives the exact original eleven-tape trace in both directions of the correspondence. Three-way XOR leaves that unit bit equal to one. The original tagged result on the XOR of any three inputs is therefore their three outputs XORed cellwise, with the same head positions, time and metadata. This proves the affine property and exact data-independent visited set on every width and layout. The nine linear and two affine classifications cover all 1,293 states of the translated data-movement programs. The public schoolbook program supplies the remaining nineteen states.

## Arbitrary bit assignments at a fixed geometry

The [symbolic interpreter](node-symbolic.lean) gives every physical input bit its own variable. It carries copies and binary XOR formulas through the real table. It accepts a probe of an unassigned bit only when both of its possible values take the default branch. Induction on the accepted symbolic trace proves the original concrete trace, its complete outputs and its exact visited-set size for every Boolean assignment at once.

The [coordinate oracle](node-symbolic-cases.lean) calculates the expected row by interchanging the two actual ternary fields with prefix, gap and suffix in place. Its packed-role oracle addresses an independent source and destination word and changes exactly the named destination role in each outer prefix. Five original-program symbolic checks cover the geometries below. The [proof-object generator](node-certified-traces.py) emits explicit intermediate states in pieces of at most four transitions. Lean can compare each piece with the source interpreter by definitional reduction and join its exact subtraces using the proved composition theorem. An incorrect intermediate symbol, head or interval makes the corresponding proof fail.

| Shape | Independent input bits | Exact steps | Exact visited cells | Verification completed |
| --- | ---: | ---: | ---: | --- |
| One 3 × 3 trit exchange | 9 | 296 | 59 | Executable and ground kernel proof |
| Two prefixes, width-one fields, gap two, suffix two | 72 | 1,086 | 190 | Executable and ground kernel proof |
| Width-two ternary fields, unit prefix/gap/suffix | 81 | 2,521 | 211 | Executable symbolic check |
| Copy one of three source roles to one of four destinations, over two prefixes and suffix two | 28 | 490 | 86 | Executable and ground kernel proof |
| XOR on the same geometry | 28 | 490 | 86 | Executable and ground kernel proof |

For example, the nine-bit result proves the transposed source indices are \(0,3,6,1,4,7,2,5,8\) on all 512 fillings. The twenty-eight-bit XOR result quantifies over \(2^{28}\) independently occupied joint inputs. Its four changed bits are computed from their own source/destination pairs. All unselected destination, source, and descriptor data are restored. The 22 concrete complete-tape fixtures separately replay 19,768 transitions across the twelve programs, covering exact return positions even for the schoolbook output whose head ends after its last bit.

## Reproduction and scope

Use Lean 4.34.1, the original OpenAI math commit `3344da59991ed94f9ba711217b29c1d760badfa6`, and its mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. The [reproduction script](node-check-lean.sh) checks the four original module blobs, builds in a temporary directory with one Lean worker, and audits the source theorem's axiom list. Its third argument selects the module family.

```sh
bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_MATHLIB width
bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_MATHLIB tables
bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_MATHLIB nine
bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_MATHLIB xor
bash node-check-lean.sh PATH_TO_OPENAI_MATH PATH_TO_MATHLIB eightyone
```

The compiler-generated intermediate modules reside inside the temporary build tree. The modes `copy`, `seventytwo`, and `eightyone` request the other independent kernel certificates. Set `S008_NODE_FRESH=1` to replay the chosen module's full transitive dependency closure, and run such jobs serially. The width-only mode uses a transitive replay by default. The structural `tables` mode has been rebuilt from the pinned source and checked with the module-local `leanchecker`. Its reported axioms are a subset of `propext`, `Classical.choice` and `Quot.sound`. A separate joint import checked both the original-tape trace and the exact visited-cardinality theorem for each of the four completed positive certificates. All eight declarations reported exactly these three axioms. The previously completed width-only run also checked its full transitive closure.

The width-two executable check uses the same symbolic interpreter and checks the entire body on 81 variables. The optional ground kernel run for this fifth positive fixture was stopped before completion. The all-width positive-coordinate permutation and the assembly of the complete adaptive multiplier into the original numerical goal retain the written arguments linked from the [native ledger](node-integrated.md).

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance. The upstream machine and visited predicates, and the reusable two-sided window proof in [the recursive handoff](recount-handoff.lean), retain their original attributions.
