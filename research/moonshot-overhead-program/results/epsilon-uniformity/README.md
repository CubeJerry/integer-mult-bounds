# Epsilon decay and quantitative uniformity

Focused companion to the square-root overhead programme. See [SESSION.json](SESSION.json)
for source pins, active routes and actual bound status, and [LOG.md](LOG.md) for
the append-only record. This directory is the scope of focused session E001;
concurrent parent session S002 is preserved separately.

## Admitted quantitative result

Start with [THEOREM.md](THEOREM.md). With `L=1+log_2 n`, `x=log_2 L`, and
`y=log_2 log_2(x+16)`, a specified implementation of the original construction
has the explicit upper envelope

\[
 T(n)=n\sqrt L\;2^{O(x(\log_2(y+2)/y)^{1/3})},
 \qquad\text{visited cells}=O(n).
\]

This is one fixed exact deterministic multitape machine. A weaker simple
form is `H<=2^{O(x/y^(1/4))}`. The complete finite-generator, physical
compiler, precision, all-length fallback, chunking and scheduling arguments
have passed separate AI reviews. This is a written mathematical extraction,
not a Lean certification, human referee report or execution of the enormous
templates. The square-root endpoint and poly-`x` overhead remain open.

The profile `log m=O(j³ log(j+2))` sharpens concurrent S002's earlier
sixth-power extraction. The source and both sessions' proofs and credits
are preserved; no literature-priority or practical-runtime claim is made.

## Research files

- [CERTIFICATE.md](CERTIFICATE.md): rigorous diagnostic lemmas and explicit scope
  of the source's weighted-search upper certificate.
- [route-a/elementary-tower-extraction.md](route-a/elementary-tower-extraction.md)
  and [compiler-invoice.md](route-a/compiler-invoice.md): complete quantitative
  construction and physical cost proof supporting the main theorem.
- [PARAMETER-LEDGER.md](PARAMETER-LEDGER.md): dependency and threshold ledger.
- [INTERCHANGE-OBSTRUCTION.md](INTERCHANGE-OBSTRUCTION.md): rational Gram rank
  forces a characteristic/window conflict in the retained tape interchanger.
  This has separate algebraic agent review and exact finite checks.
- [PADIC-LIFT-OBSTRUCTION.md](PADIC-LIFT-OBSTRUCTION.md): literal label transfers
  lose their small-rank advantage modulo p²; complementary to S002's more
  general supported-lift theorem.
- [route-a/README.md](route-a/README.md): additional compact binary-kernel and
  repair-table results, with their local scope and verification.
- [route-b/README.md](route-b/README.md): charged binary scheduling, bounded
  preflight, complete conditional endpoint/poly-`x` transfer, chunking and
  compiler-interface results.
- [route-c/NONSTATIONARY-RECURSION.md](route-c/NONSTATIONARY-RECURSION.md):
  a complete conditional interchange endpoint, and a separate Walsh-toll
  obstruction; neither is a complete multiplication theorem.
- [route-c/SOURCE-PADDING-BARRIER.md](route-c/SOURCE-PADDING-BARRIER.md):
  literal radix padding violates common linear space for a specified natural
  variable-template selector.
- [route-c/INPUT-DEPENDENT-RADIX.md](route-c/INPUT-DEPENDENT-RADIX.md):
  constructive repair of that padding barrier, including compatible-prime
  search, constant or summably small volume loss, and explicit preparation.
- [REVIEWS.md](REVIEWS.md): admitted proofs, actual cross-reviews, finite
  replays and their limits. Exact checker receipts sit beside their scripts.

Exact source revision: OpenAI `math` 3344da59991ed94f9ba711217b29c1d760badfa6.
No upstream PR is opened automatically. Proofs, partial results, scoped negative
results and finite computational checks must keep their distinct labels.

## Open next questions

The current joint coefficient/threshold estimate is explicit but extremely
large. The binding cost is the finite-characteristic predictor's matrix-root
representation and ensuing scalar/description work. A smaller full-rate
representation or different routing mechanism must preserve the individual
query information lost by the ordinary modular count. Preflight removes
search from the execution factor, but the current tower profiles still give
the same envelope scale. Variable-arity endpoint routes also need every
local excess and routing toll controlled, with a uniform physical compiler.

Credits: @CubeJerry, OpenAI manuscripts and cited predecessors, the retained
moonshot programme and concurrent S002 work. Substantial OpenAI GPT-6 Astra Pro
assistance, including three genuinely separate task agents. No human referee or
full Lean-kernel audit is claimed.
