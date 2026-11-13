# BIT nine-packet: one-chain stationary-cache obstruction

Status: exact scalar obstruction for the clean independent X-only source and
one nested route per Y. It does not cover Y-Y coding, new X transport to an
unvisited chart, or a different source circuit.

## Claim

Take the clean independent X-only subword identified by the actual BIT source
screen. Permit a zero-owned stationary cache to copy any current X row at any
chart where that subword has such a row, retain it until the Y phase, and make
any number of local ADD fusions from the caches encountered by one Y. After
the nine global K packets are available at chart 0, each Y is required to move
along one nested chart chain to its actual final facet. With no Y-Y coding, no
receiver can obtain its correction row

\[
F_i=(K+I)_i.
\]

This failure holds even if cache count, INIT/ADD/CLEAR work, and retained
lifetimes are given no limit. Adding their real costs cannot repair the missing
coordinate.

## Exact support dual

Let \(L_j\) be the initial one-dimensional E8 chart for source \(X_j\). For
every current row \(r\) of the independent X-only circuit at chart \(C\),

\[
\operatorname{supp}(r)\subseteq\{j:L_j\subseteq C\}.
\]

The checker reconstructs all 111 X rows, all chart labels, every observed
\((C,r)\) history, and the endpoint from the authenticated native, while
omitting every non-X operand. It checks this support invariant for every one
of the 1,027 distinct history rows. The invariant follows through the actual
operations: ADD has co-charted operands, MOVE is upward and nested, and SWAP
exchanges each value together with its chart label.

For receiver \(i\), the checker independently rebuilds the native rational
root lines and verifies that \(F_i\)'s support is exactly

\[
S_i=\{j\ne i:g_i\cdot g_j=0\}.
\]

The 55–62 contact roots in each \(S_i\) span the receiver's actual
seven-dimensional final facet. Thus the pooled source-chart relaxation can
recover every \(F_i\) (as the source screen reports), but any one Y route
selects only histories from a nested chain. For every upward-terminal
continuation of every possible starting cache chart, the union of those
history-row supports omits at least one port \(j\in S_i\). Every finite
feasible cache chain is a prefix of one such continuation. The coordinate
functional \(e_j\) therefore annihilates every cache row on that chain, while
\(e_j(F_i)=1\). No linear fusion of those cache rows can produce \(F_i\).

The exact checker enumerates 33,814 upward-terminal continuations across all
111 receivers (81–550 per receiver). Every continuation has a coordinate
dual; all histories at that continuation have zero in its dual coordinate.
Every shorter nested chain inherits the same dual from an upward extension.
For the terminal continuations, no route covers more than 18 of a receiver's
55–62 required contact coordinates; each misses at least 39. Fifty-seven
receivers have at least one source history at their exact final facet. Those
endpoint histories are included in the enumeration and still do not remove
the obstruction.

### Concrete duals

- Receiver 0 has final facet chart 525 and 56 residual coordinates. On the
  actual nested cache chain `[11, 266]` of dimensions `[1, 4]`, the dual is
  \(e_3\): all source history rows at both charts have coefficient 0 at
  \(X_3\), while \(F_0\) has coefficient 1 there. Its residual bitset is
  `0x7ffffffe0007ffc00000003ffe`. Across all 94 terminal continuations for
  receiver 0, each misses at least 47 of the 56 required coordinates.
- Receiver 3's chain `[2, 126, 268, 348, 528]` reaches its exact final facet
  chart 528 (dimensions `[1, 2, 4, 6, 7]`). The dual is \(e_1\), with pairing
  0 against every cached source history on that chain and pairing 1 against
  \(F_3\). This example covers the case where the route reaches the final
  facet and uses its available source history.

## Controls and tariff

- Source pin: native SHA256
  `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`;
  packet screen SHA256 `ade07c8fdd0393f22d7a71c994af545c3d1569031b5aa617949105648ed6f77a`.
- The replay reproduces 628 X-only ADD/SWAP operations, paid profile
  `{1:289, 2:244}`, 1,027 histories, and identity X endpoint. It is a newly
  executed independent X-only circuit; contaminated full-native intermediate
  values are not reused.
- The screen's pooled all-subchart control recovers all 111 residuals, while
  a separate exact F2 row-space search over a single nested chain finds no
  witness for any of the 111 receivers. This localizes the failure to path
  compatibility. The support-coordinate duals give a shorter certificate.
- At \(t=0.995\), the requested optimistic profile pieces are:

  | Piece | Moment |
  |---|---:|
  | X source `{1:289, 2:244}` | 775.3116482599995031… |
  | Nine rank-8 packets | 71.2552792618948965… |
  | 111 direct rank-7 Y routes | 769.4767971111024689… |
  | Total with direct rank-7 routes | 1616.0437246329968685… |
  | Conditional limit | 1621.750880211152355… |
  | Remaining moment room | 5.7071555781554865… |
  | 111 all-unit Y routes instead | 1623.5669275218943996… |
  | All-unit excess | 1.8160473107420446… |

  These are optimistic movement moments only; they omit cache and ordinary
  operation costs. The direct-route profile is a comparison point, not an
  attained completion: the one-chain source rows cannot form even one required
  residual. Since no cache witness exists, there is no completed cache invoice
  to count. The impossibility is independent of the tariff because the dual
  persists with unlimited cache operations.

## Scope

The result applies to the stated scalar F2 interface: the pinned BIT fitting
rows, clean independent X-only histories at genuine visited source charts,
stationary caches copied from those rows, one nested 0-to-facet route per Y,
arbitrary fusions of encountered X caches, and no Y-Y coding. It does not
exclude using Y-Y coding, introducing new X transports to generate rows at
additional charts, or changing the source map. It is not a supplier theorem,
an all-volume completion, or a new \(\kappa\) result.

## Files

- `check_support_obstruction.py` independently replays the X-only source and
  certifies the all-receiver chain duals.
- `SUPPORT-RESULT.json` contains receiver-by-receiver geometry, path counts,
  support limits, and explicit dual examples.
- `check_chains.py` is a separate exact F2 span search over single nested
  chains; `RESULT.json` reports no chain witness for any receiver.
- `MANIFEST.json` pins the files in this review bundle.
