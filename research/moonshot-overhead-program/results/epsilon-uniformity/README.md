# Epsilon decay and quantitative uniformity

Focused companion to the square-root overhead programme. See [SESSION.json](SESSION.json)
for source pins, active routes and actual bound status, and [LOG.md](LOG.md) for
the append-only record. This directory is the scope of focused session E001;
concurrent parent session S002 is preserved separately.

The published baseline remains one fixed exact deterministic multitape machine
with time n L^(1/2+o(1)) and uniformly O(n) visited cells. No new complete
explicit overhead bound has yet been established by this focused session.

## Research files

- [CERTIFICATE.md](CERTIFICATE.md): rigorous diagnostic lemmas and explicit scope
  of the source's weighted-search upper certificate.
- [INTERCHANGE-OBSTRUCTION.md](INTERCHANGE-OBSTRUCTION.md): rational Gram rank
  forces a characteristic/window conflict in the retained tape interchanger.
  This has separate algebraic agent review and exact finite checks.
- `route-a/`: quantitative source extraction and repair/routing costs (in progress).
- `route-b/`: alternative scheduling and bounded preflight (in progress).
- [route-c/NONSTATIONARY-RECURSION.md](route-c/NONSTATIONARY-RECURSION.md):
  a complete conditional interchange endpoint, and a separate Walsh-toll
  obstruction; neither is a complete multiplication theorem.
- [route-c/SOURCE-PADDING-BARRIER.md](route-c/SOURCE-PADDING-BARRIER.md):
  literal radix padding violates common linear space for a specified natural
  variable-template selector.

Exact source revision: OpenAI `math` 3344da59991ed94f9ba711217b29c1d760badfa6.
No upstream PR is opened automatically. Proofs, partial results, scoped negative
results and finite computational checks must keep their distinct labels.

## Open next questions

Which candidate-dependent cost prevents a useful joint A_j,N_j estimate? Can
selection/generation be absorbed into a linear preparation budget while preserving
exactness and the common space cap? Does a variable-arity caller pay a summable
total excess after every local routing and precision operation is included?

Credits: @CubeJerry, OpenAI manuscripts and cited predecessors, the retained
moonshot programme and concurrent S002 work. Substantial OpenAI GPT-6 Astra Pro
assistance, including three genuinely separate task agents. No human referee or
full Lean-kernel audit is claimed.
