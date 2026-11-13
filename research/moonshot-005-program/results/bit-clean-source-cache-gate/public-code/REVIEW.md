# BIT nine-packet: public-Y last-interaction gate

Status: exact support obstruction to arbitrary acyclic ADD/SWAP coding among
the 111 public Y rows under the same clean stationary-X-cache interface. This
is a follow-on to the one-chain cache obstruction. Extra Y-bearing owned
copies are outside this gate.

## Result

Fix the nine-packet partial map first: at chart 0 the public rows are exactly
\(Y=y+Kx\). Then allow any sequence of public-row ADDs and whole-label SWAPs,
arbitrary stationary X-cache fusions on every path, and exact restoration of
all public y coefficients at their endpoints. This still cannot complete the
residual map.

For receiver \(i\), let \(S_i=\operatorname{supp}(F_i)\), where
\(F_i=(K+I)_i\). On every receiver pair, the private support size
\(|S_i\setminus S_h|\) is at least 21. For the same receiver, the exact X
history support replay shows that any single nested cache chain inside its
facet covers at most 18 coordinates of \(S_i\). Receiver-by-receiver, the
minimum private support over all possible partners is strictly greater than
the maximum cache support of any one suffix chain; the minimum strict gap is
4.

For arbitrary acyclic public-row coding, follow each final output value
through whole-label SWAPs and choose its last incoming \(Y\leftarrow Y\) ADD.
After that ADD, its y row must already be \(e_i\): later source-only uses do
not change the row, and exact endpoint restoration leaves no further incoming
Y operation. If output \(i\) has no incoming Y-Y ADD, its whole correction
uses one chain and fails the predecessor result.

Otherwise consider the donor row at the last ADD. The 111 public y rows remain
a full-rank basis under ADD and SWAP, so modulo \(e_i\) this donor has a
nonzero y component. The remaining public rows are an invertible basis modulo
\(e_i\); the donor's quotient information must influence at least one other
final output \(h\ne i\). Track that nonzero dependency through row
operations, SWAPs, and monotone field routes. The interaction chart \(C\) is
nested in both final facets \(F_i\) and \(F_h\). Every X-cache increment
added on the paths before that interaction is supported on source lines
inside \(C\), hence in \(S_i\cap S_h\). It cannot change any coordinate in
\(S_i\setminus S_h\). After its last incoming Y-Y ADD, output \(i\) has one
suffix path, and that path cannot source all the at-least-21 private
coordinates because any single chain exposes at most 18 contact coordinates
in total. This covers arbitrary sequences of public Y ADD/SWAP operations,
not just one fixed encoding matrix and demix.

The premise is that the nine global packets establish \(Y=y+Kx\) at chart 0
before this path code, or that the packet updates are transported through
exactly the same public-row operations so that the net pre-correction map is
still \(K\). Restoring the y identity then restores the Kx contribution as
well; the required local correction remains \(F=K+I\). If a different
rank-nine packet placement gives \(Y=y+Mx\), this gate does not apply; the
residual \(I+M\) and its contact geometry must be recomputed. The obstruction
is a support argument, before movement or ordinary operation costs.

## Exact controls

- `check_receiver_mixing.py` verifies the support-result and actual BIT screen
  hashes, checks every residual support against the exact contact sets, and
  proves `min_h |S_i\S_h| > max_chain_support_i` for all 111 receivers.
- Result range: contact weights 55–62; minimum private difference 21; maximum
  any one-chain support 18; minimum per-receiver deficit 4.
- Tight output: receiver 3, closest partner 76, 22 private contact ports, and
  at most 18 source-contact ports on any suffix chain.
- The preceding support checker reconstructs the clean independent X-only
  subword and its histories from the pinned native. No contaminated full-native
  X intermediates are credited.

## Scope

This gate covers arbitrary public-only acyclic Y ADD/SWAP operations with
exact endpoint restoration of y, after the fixed \(K\) packet map, and one
monotone physical output path per public row. It does not cover Y-bearing
copies in owned fields that can take separate routes and later form pure-X
packets, a different rank-nine packet map, new X transports, or a different X
source word. It is a scalar F2 statement and gives no supplier, all-volume
completion, or new \(\kappa\).
