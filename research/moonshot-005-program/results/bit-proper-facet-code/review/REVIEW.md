# Independent review: BIT missing-facet packet basis

Status: independent PASS for the finite code census, all-field/block support
shortening argument, scoped unchanged-raw fresh-packet bound, literal partial
word, and exact movement price. This does not complete the missing K+I map.

## Independent checks

`check_missing_facets.py` pins the frozen author package and authenticated
BIT native, reconstructs the 111 integral norm-four roots and the actual
binary fitting matrix, and independently enumerates all 511 nonzero words
in its rank-nine row code. It uses modular rank over 1013, separate from the
author verifier's 1009 lower-rank certificates. For each of the nine rank-7
words it also computes an exact rational normal and verifies that its support
is exactly the full source contact set for that normal. Rank-8 words have a
rank-eight minor modulo 1013, so they are rank 8 over the reals.

The independently recovered proper word masks and weights are

| Mask | 38 | 44 | 223 | 241 | 254 | 296 | 314 | 367 | 419 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Support size | 56 | 60 | 59 | 58 | 58 | 59 | 58 | 56 | 59 |

Their nine rows have binary rank 9. All 36 pairwise support intersections
have size 25–34, and every pairwise union has rank 8 modulo 1013. An
independent exact reflection closure has 120 projective roots; the nine
proper facet normals are exactly the nine omitted roots. The complete
rank/weight histogram is in `RESULT.json`.

## Shortening over arbitrary characteristic-two fields and blocks

The finite census gives the stated general shortening theorem. Let \(C\) be
the binary rank-nine code and extend it to any characteristic-two field
\(k\). For a scalar \(w\in C\otimes_{\mathbb F_2} k\), write its nine code
coefficients in a finite \(\mathbb F_2\)-basis of their span in \(k\):

\[
w=\sum_a \lambda_a c_a,\qquad c_a\in C.
\]

Independence of the \(\lambda_a\) over \(\mathbb F_2\) means that
\(\operatorname{supp}(w)=\bigcup_a\operatorname{supp}(c_a)\); no coordinate
cancellation can hide a binary constituent. If that support lies in a
proper real chart, every nonzero constituent must be one of the nine proper
words. Two different proper words have a support union spanning \(\mathbb
R^8\), so all nonzero constituents must be the same proper word. Hence every
proper shortening is zero except at one of the nine facets, where it is
exactly the one-dimensional line spanned by that facet's word.

For a vector-valued word of volume \(V\), apply this scalar argument to each
of its \(V\) coordinates. A single proper chart cannot contain supports
from two different proper words, so all nonzero coordinates use the same
word \(c_a\). Therefore

\[
W(H_a)=c_a\otimes k^V,\qquad \dim_k W(H_a)=V.
\]

This proves the full-field and block support-union claim without presuming
that a general packet was a scalar tensor product.

## Fresh packet theorem and its scope

For the pinned canonical map \(K\), nine volume-\(V\) packets that implement
the update span a \(9V\)-dimensional direct sum. A nonzero packet born in a
proper chart has its \(V\)-dimensional rowspace inside a proper shortening,
so it must be exactly \(c_a\otimes k^V\) for one of the nine facets. Two
packets born at the same facet are dependent. Two born at distinct facets
have at least 25 common raw donor ports; each coefficient block on a proper
word's support is invertible, so each such unchanged donor is needed at both
facets. A single upward nested path cannot visit two incomparable
seven-dimensional facets.

Thus at most one packet can be born off the Hub **under these premises**:
nine fresh whole fields, single birth chart per packet, unchanged raw X
inputs on one upward nested path, no informative moving copies, no
multi-chart packet assembly, and no pre-existing receiver information that
helps encode the packet. This is not a bound for changed source recoding or
for additional informative copies; those need a new acquisition proof and
full route invoice.

## Literal 1-facet partial word

The independent interpreter replays `PARTIAL-WORD.json.gz` directly on the
222 independent X/Y input directions. The first delivered packet is the
mask-38 word at the rank-7 omitted-root facet; the other eight packets are
Hub-born. The exact map is

\[
X=x,\qquad Y=y+Kx,
\]

with every endpoint chart correct. The ledger is 1,307 operations: 287 MOVE,
1,002 ADD, 9 INIT, and 9 CLEAR; it has 9 retired lifetimes, peak owned count
1, and 225 distinct nested MOVE pairs. Its movement histogram is
\(\{1:56,6:56,7:167,8:8\}\). The first 56 raw X fields visit the missing
facet, remain unchanged, and then continue to the full Hub. The program does
not reuse contaminated full-native X intermediate values.

At \(t=199/200\), the old all-Hub partial profile is \(\{7:222,8:9\}\). The
new profile saves

\[
(8^t-7^t)-56(1+6^t-7^t)
=0.18625250395109168572310923188130245022\ldots .
\]

Independent directed integer-200th-root intervals give a positive saving
from `0.1862525039510916857231092318813024502217…` to
`0.1862525039510916857231092318813024505509…`. The new partial movement price
is `1610.02262098014874265715212009599434958…`; the previous partial price
is `1610.20887348409983434287522932787565203…`. These moment figures cover
MOVE rank only; ordinary operations and owned lifetimes are reported
separately above.

For the restricted acquisition interface, the minimization over support sizes
follows directly for every `0 < t <= 1`:

```text
P_w(t) - P_0(t) = -(8^t - 7^t) + w * (1 + 6^t - 7^t).
```

Since `1 + 6^t >= 7^t`, the coefficient of `w` is nonnegative. A proper
support has `w >= 56`, so its least-cost case is `w = 56`; the only remaining
alternative is no proper packet, with cost `P_0(t)`. Therefore the optimum in
this restricted interface is exactly `min(P_0(t), P_56(t))`. This statement
concerns MOVE rank only.

## Limits of the result

The literal word still outputs \(y+Kx\), not \(y+x\). All 6,470 foreign
coefficients of \(K+I\) remain. The nine-facet theorem and its one-packet
bound do not rule out a changed donor acquisition circuit that transports or
recodes X information differently. Nor does this scalar partial word by
itself establish an all-width physical compiler contract, a complete
\(Q=F\), a strict supplier, or a new \(\kappa\).

## Reproduction pins

- Frozen author manifest SHA256:
  `6ff4c619fd0f37ea016e18f6657c2b32559f25a33d88a3b4aa7019f26805ec56`.
- Native source SHA256:
  `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
- Independent checker: `check_missing_facets.py`.
- Independent exact result: `RESULT.json`.
- The checker does not import the author builder or retained replay engine.
