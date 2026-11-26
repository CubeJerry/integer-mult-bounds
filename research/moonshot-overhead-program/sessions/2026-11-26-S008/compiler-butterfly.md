# A kernel-certified modular butterfly on one pair and on a complete stream

Two explicit deterministic machines use the same five physical tapes, six symbols and OpenAI `TM.advance` transition semantics. The first maps canonical $w$-bit residues $a,b$ to $(a+b)\bmod M$ and $(a-b)\bmod M$. The second applies it independently to every aligned pair in two streams, retaining one physical copy of $M$. Both accept every positive representable modulus, and both preserve their input and modulus banks and restore every head to its own entry origin. An external position permutation or stable split supplies paired streams when a Walsh call selects nonadjacent logical addresses. Those movements have separate prices in the full construction. [Original tape model](https://github.com/openai/math/blob/3344da59991ed94f9ba711217b29c1d760badfa6/lean/OAI/Computability/IntegerMultiplication/TMModel.lean) · [Complete Walsh caller](walsh-node.md)

## One independently occupied pair

The five tapes hold $a,b,M$, the sum destination and the difference destination. A data word is least-significant-bit first with the three source delimiters aligned at their own offsets $w$. The first operand has one home marker just before its low bit. The two other source and destination exteriors may contain arbitrary symbols, and all five origins are independently chosen signed positions. The machine accepts arbitrary existing destination contents.

During a forward pass four carry or borrow bits reside in control. The machine computes both the uncorrected low sum and its difference with $M$, the uncorrected low difference and its sum with $M$. Two candidate bits fit in one of four symbols already in the common alphabet. A simultaneous transition writes one candidate pair per destination. At the right-hand terminators, the forward carry and the subtraction borrow decide whether to subtract $M$ from the sum. The borrow from $a-b$ decides whether to add $M$ to the difference. No read of the discarded high candidates is needed. A backward pass selects the final bits destructively in the same cells. The first operand's home marker moves all five heads back to their original positions and halts.

The 21-state machine takes **exactly $2w+2$ transitions**. The original `visitedCells` has cardinality **exactly $5(w+2)$**, the five intervals from one cell before the word to its right delimiter. The named theorem `Butterfly.resources` combines the uninterrupted transition trace, halt, five head postconditions, the finite-cover space bound and the actual natural numbers decoded from both final tapes. `Butterfly.exact_space` proves the cardinality equality. `Butterfly.retained` and `Butterfly.exterior` give the full arbitrary-data preservation statements. [Lean rule and proof](compiler-butterfly.lean)

The arithmetic invariant after $i$ bits has four equations. Write $A,B,M_i$ for the low $i$ bits and $S,D,R,C$ for the accumulated unconstrained sum, difference, sum-minus-modulus and difference-plus-modulus candidates. The carry and borrow bits, respectively $c,d,r,e$, satisfy

$$S+2^ic=A+B,\qquad D+B=A+2^id,\qquad R+M_i=S+2^ir,\qquad C+2^ie=D+M_i.$$

All candidates are below $2^i$. At $i=w$ these equations give both canonical residual values even when addition overflows the binary width, when $a<b$, when $M=1$, and when $M$ is even. The kernel proof derives the four equalities from the finite full-adder and full-subtractor truth tables and links the selected digits to the absolute tape cells of the halting configuration.

## A complete file of pairs

The stream wrapper has **27 states** and uses the same five tapes. There are $N$ marked records in each of four equally aligned moving streams. The modulus stays at its own origin between word calls. Each moving record occupies $w+2$ cells, comprising the digits and two boundary cells. Only the documented control markers on the first input and the physical source terminators are inspected. The two input streams and output destinations may be independently occupied. The record stride is present in the file, so it is never charged as a constant-time random seek.

One row uses one issue transition, $2w+2$ transitions of the literal five-tape word program, one transition to recover caller control, $w$ forward digit moves, one delimiter transition and one move over the row marker. Dispatch, evaluation and advancement thus cost $3w+6$ per row. After the last record, the controller traverses the four moving streams back to their common relative start. It spends $N(w+2)+4$ transitions including both end turns. The full bank price is exactly

$$N(4w+8)+4.$$

`ButterflyStream.batch` gives that exact source trace. `batch_numbers` identifies both modular results of every row in the *same final configuration*. `batch_sources`, `batch_exterior`, `batch_homes` and `batch_halts` give the raw tape and head conditions. The two coordinates of one row keep their separate absolute locations after all subsequent rows have run. The empty file has four transitions, while a legal zero-width file has its structural trace even though its positive-modulus arithmetic domain is empty. [Full-stream rule and proof](compiler-butterfly-stream.lean)

For each of the four moving heads the union of visited positions is its own interval from offset $-2$ through $N(w+2)$. The modulus head visits offsets $-1$ through $w$ once a word is processed. In an empty file it remains at offset zero. Consequently the exact count is

$$4\bigl(N(w+2)+3\bigr)+\begin{cases}1 & N=0,\\w+2 & N>0.\end{cases}$$

The word calls stay in their own row's intervals, and the only movements between calls are the bounded row-advance, return and end-marker scans above. Repeated visits to the single modulus copy do not accrue fresh positions. `ButterflyStream.batch_visited_iff` identifies each reachable pair of a tape and an absolute position. `ButterflyStream.sharp_visits` gives the original finite-cover guarantee and `ButterflyStream.batch_exact_space` proves the cardinality equality. The finite replay also counts the union through halt on every fixture. [Precise stream-space proof](compiler-butterfly-stream-space.lean)

## Verification

The [source runner](compiler-check-lean.sh) builds the original pinned model and the new proof modules with warning-as-error Lean 4.34.1. The [table exporter](compiler-butterfly-export.lean) emits all rule rows, including malformed reads and halting states. The [independent simulator](compiler-butterfly.py) computes full-adder and subtractor decisions with signed integer arithmetic, compares every exported byte, and checks final contents, displacement, elapsed transitions and the exact visited set size. Reproducible results are as follows.

| Program | Complete rule rows | SHA-256 of table | Tested executions | Physical transitions |
|---|---:|---|---:|---:|
| One modular pair | 163,296 | `84b8de66434cb2c0f1c51e1c3433a53e0536ba4d18f8b02c403377daca5d7fcf` | 97,555 | 1,448,816 |
| Complete stream | 209,952 | `47a557d85f5c74a2868abfb55fe4dda16a1e778d003390f426df5fa7507387f5` | 284 | 375,240 |

The extended scalar suite exhausts all reduced input pairs and moduli through six-bit words, then tests wider operands through 1,024 bits. The stream suite includes empty files, empty-width structural calls, dense operands, independent nonzero destinations and separate signed origins. The numerical whole-integer clocks retain their original paid routing allowances. These two arithmetic machines are additional verified realizations of the paired-word operation at its actual width.

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance.
