# Existing fixed-D literal root services: bounded source audit

Audit completed 2026-11-20 against canonical main
`e54523517d0f03e58352e647c403a5af3e525a57`. The receiving rational-grid lemma
is now published at `CubeJerry/integer-mult-bounds`
`88dd72b4864665362230c56538d2bd2579c6beca`, with corrected proof SHA256
`7a4721d5e83b4138f5a918edd77881fb06c183fb41c99727f9b5973200d4e1b0`.
No frozen contribution or root artifact was edited.

## Decision

**Do not construct another fixed-D arithmetic graph.** The already published
[#6968](https://github.com/CrocSwap/integer-mult-bounds/pull/6968),
`research/current-scalar-flat-tables`, supplies exactly the required signed,
all-width literal arithmetic and successful lifecycle for each fixed nonzero
rational coefficient. Instantiate its unchanged `compile_scalar("SCALE",q)`
at `q=D` and `q=1/D`.

The reusable provider is the table **together with** its existing physical
entry/exit wrapper, not the table alone. This is an exact binding for a
complete coded Gaussian field. It is not a claim that the abstract
`c_dispatch.Tape` Python tuple representation is already that physical codec.
The remaining seam is assigning the root common format to the existing
coded-field ABI, if a literal receiving runtime is later required.

## Exact binding and corollary

Fix any positive odd integer D. Reserve signed width B>=1 for every real and
imaginary component of R>=1 complete complex records. Use the existing codec:
little-endian two's-complement B-bit components, each followed by virtual
delimiter 2; each virtual symbol has its three-bit nonblank physical code.
The public blank frontier immediately follows the last delimiter. There are
two distinct private work ports, candidate output and rewind guide. All
heads enter at their current origins, with protected left markers. Work
prefixes may be initially dirty but must be contiguous; all inactive
historical tails are already blank. Public, work, context and ancestor
segments have the original disjoint ownership assumptions.

Set

    L = 2 R (B+1),       V = 3L.

The source theorem applies to all B and R, with no decoded width, record
count, runtime arithmetic callback or input-dependent state alphabet.

* **Multiply:** the D table succeeds exactly when every D*x fits the original
  B-bit signed interval. Integrality is automatic. On that admitted domain it
  installs the entire scaled field, retaining the exact original extent.
* **Divide:** the 1/D table succeeds exactly when each x is divisible by D and
  the quotient fits. For D>=1 the quotient range condition follows from the
  input's B-bit signed range. Its finite terminal carry guard checks exact
  divisibility; this is not rounded division.
* Both positive operations preserve mathematical sign, including zero. The
  two's-complement sign bit therefore remains consistent with the unchanged
  sign; no new negative-zero convention is introduced.
* Every success restores the public and work heads. The unchanged
  `Controller.primitive` or its exact three-phase equivalent first retires old
  work, executes the finite table, then physically erases both work bodies.
  All work is blank at return, and the same physical owners are retained.
* Staging is whole-field: no target write occurs before all components pass
  the range/divisibility guards. Rejection can leave work occupied and heads
  advanced; it is not an atomic rollback interface. The root lemma uses only
  the admitted successful domain.

For both q=D and q=1/D, the source parameter
`d=v_2(denominator(q))` is zero. Its conservative initially blank-work bill
therefore specializes to

    physical cell actions + executed control rows <= 2048 (L+1).

An initially dirty work prefix of total length A adds O(A), and untouched
fixed work/context inventory Q adds O(Q), exactly as in the published theorem.
Thus the result is O_D(RB+A+Q); for clean reused work it is O_D(RB).
This is a finite-control tape bill. It is not a claim that interpreting an
arbitrarily large supplied table on a universal machine has unit lookup cost.
For fixed D that interpretation can also be charged in the D-dependent
constant, or the finite table can be taken as the machine's control.

The output work reaches at most V cells and the guide V+3, apart from fixed
origin/frontier constants. The full historical bill is the **sum of the
per-owner maxima**, for example

    max(H_out,V+O(1)) + max(H_guide,V+3+O(1)),

plus retained public, context, ancestor and controller storage. Old erased
backing is never refunded. The service does not erase an arbitrary hidden
dirty tail beyond an interior blank; that would violate its entry ABI.

The root construction has T=J*floor(log_N h) fixed-D multiplication passes and
the same number of fixed-D division passes. The rational-grid lemma supplies
the common B-bit amplitude and exact-divisibility conditions at every pass.
After each successful pass the two work bodies are empty. Reusing these same
ports therefore gives O_D(T R B) time and one retained high-water allocation,
not new tape owners or additive backing at each pass. Multiplication's
intermediate magnitudes grow monotonically toward the already bounded final
root scale; division preserves the remaining powers of D until unscaling is
complete. This is precisely the desired O_word(V log(h+2)) root contribution.

A real scalar alone can be paired with an explicit zero imaginary component,
at a constant-factor format cost. For the rational C-word caller, complete
Gaussian pairs already are the natural objects. No such padding or codec
conversion is asserted to be free.

## Why the other sources are not the best direct binding

| Source | What it already supplies | Boundary for this task |
|---|---|---|
| #7820, apoursh head `20a5532ea99b8ade78755486a6b92aa8071dc076` | Reversible adjacent-site odd division with a supplied binary modulus, returned modulus and zero scratch; unsigned magnitude plus separate sign; head movement O(m*k+S) | Its program is a uniform **length-indexed gate schedule**. Its proof explicitly leaves generating the control stream, external ferrying and a universal program counter to their own model. It is valuable circuit evidence, but not the already closed width-independent literal control interface requested here. |
| #6968, CubeJerry head `13193a22b1070a74a8580c5d3ea27470443f815a`; retained on canonical main | Fixed literal ADD/SCALE tables for every fixed rational, exact final signed range, complete staging, two work tapes, head returns and physical retirement/history | Direct reuse at D and 1/D, conditional on its explicit coded-field ABI and the root's already proved common-grid/range premises. |
| #7596, CubeJerry head `ee6005fe241ab947e511fe9f6d86f5f4fa58478b` | Actual CRT comparison/add/sub/div on unsigned P-bit Words, literal numerical graph | The documented division ceiling is `930P^2+1395P+14322`, and this package does not supply the requested fixed-divisor linear corollary. Its different Word/owner ABI also needs a signed-format join. It is unnecessary given #6968. No lower-bound claim about all possible specializations is made. |
| #6990 and #7665 | Compact/instantiated rounded scalar tables with strong current-source binding and history bills | Rounding and current-catalogue restrictions are additional machinery; #6968's exact arbitrary-fixed-rational theorem is the smaller match. |
| #7702 and #7718 | Exact row-atomic integer arithmetic or a smaller physical odd scale/rate | They do not replace the already available literal current-scalar table interface. |

#7820's reversible digit map also allows multiplication by reversing the
division schedule on an exact zero-remainder endpoint, with the same
width-indexed gate count. That observation is not needed for the chosen
binding and does not silently fill its separately excluded control-generation
and external-layout obligations.

## Constructor size and startup qualification

The #6968 generator has no hard odd-divisor cap. For these two specializations
its carry bound is D+1, d=0, and all other control components range over fixed
finite sets. Its graph is O(D) in size, with integer construction arithmetic
polynomial in log D per state. This is **not** a polynomial-in-bitlength(D)
table construction, and no such claim is needed for fixed-D runtime reuse.

Under the corrected unary-code bound, `D<=product q_i<=3^(L_code/3)`, the
O(D)-state construction is exponential in code length, not doubly exponential.
It can be absorbed in a separately proved `2^O(L_code)` cold-construction
budget, if that route is chosen and the exponent is charged. The published
rational lemma's descriptor-based construction remains a different valid
choice. This audit does not alter that lemma or silently substitute one
startup cost convention for another.

## Bounded replay and provenance

`binding_check.py` imports the **unchanged** table generator and lifecycle
executor copied from canonical main. Its only new code is a metered fixture
and independent integer oracle. It does not implement a replacement service.
The replay covers D in `{1,3,5,15,105,1125}`, multiplication and division,
B in `{1,4,9,32,129}`, and clean/dirty work with long retained backing:
120 complete calls, 1,594,740 physical actions plus executed rows. Every
success checks exact output, preserved sign, all returned heads, erased work,
unchanged origin markers and retained allocated histories. A nonmultiple
control rejects before public installation.

For D=1125, the unchanged multiplication table has 76,598 rows / 31,540
states, and the division table 45,126 rows / 22,548 states. These are finite
examples, not extrapolated proofs of the all-D or all-B statement.

Exact source bytes are bound in `SOURCE-PINS.json`. The replay receipt is
`BINDING-RESULT.json`. The universal corollary above uses #6968's published
proof. It does not rerun its complete historical controller fixture or
re-admit the selected multiplication theorem.

The bounded live overlap audit read #7820 and #6968 directly, searched
fixed-divisor, literal division/scalar and fixed-rational claims, and inspected
#7596, #6990, #7665, #7702 and #7718. Broader searches were limited to their
first 50 results; sparse and unpublished work remain coverage limitations.

Credit CubeJerry for #6968 and its unchanged table/lifecycle join; apoursh
for #7820; Jose Manuel/jmbarrancoml, Nick Petalas, Sagar Thakrar, James Chang,
Ali Romman, DreamingOfClouds, Mark/Matarener and the source notices for the
retained arithmetic and ownership lineage. This audit used substantial OpenAI
assistance and is not independent human or formal-kernel review.
