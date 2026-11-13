# Independent review: BIT rank-nine partial rail

Status: independent exact replay passes for the pinned partial rail, the
four-bank shared-native partial word, source contact geometry, and conditional
even-m profile arithmetic. The 6,470-entry residual is still unpaid. This is
not a completed Q or supplier.

## Source geometry and fitting

I verified the frozen author manifest and independently read the pinned BIT
native (`51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`).
All 636 listed frames have exact complementary A/B bases of the declared
dimension. Native replay preserves all659 public endpoint rows and all
237 owned lifetimes.

The first111 X inputs start on 111 distinct rational lines. Their source
representatives have squared norms `1` for8 rows and `4` for103; doubling the
norm-one representatives gives integral vectors `v_i` all of squared norm4.
Their pairwise products are `0` or `±2` off diagonal, and the111 lines span
rank8. Exact reflection closure from these source lines contains120
projective lines and is stable under every root reflection, confirming the
full E8 line geometry from the actual source.

For each Y receiver `i`, its actual final chart is rank7 and is orthogonal to
`v_i`. I checked membership of every source line `v_j` in that actual facet:
for `i != j`, membership holds exactly when `v_i·v_j=0`. Thus

```text
B_ij = (v_i·v_j/2) mod 2
K    = J + B over F2
```

has `rank(B)=8`, `rank(K)=9`, `K_ii=1`, and off-diagonal ones exactly at the
actual line-to-facet contacts. The diagonal is the added identity term: a
root is not orthogonal to itself. The nine encoder rows selected from K are
source rows `[0,1,2,4,8,9,14,30,59]`; I independently solved and checked every
decoder row against them.

The partial rail's map is exactly `X=x, Y=y+Kx`. The desired native shear is
`Y=y+x`, so the outstanding map is `K+I`: exact binary rank108, 6,470 ones,
and nonzero in all111 receiver rows. The K diagonal must be removed before
calling this the residual.

## Literal rail and m=4 word

I replayed both frozen words with a separate interpreter and exact rational
chart checks. The222-input rail has1,267 operations, 231 paid moves with
profile `{7:222, 8:9}`, nine retired one-slot lifetimes, and peak owned count1.
It has the claimed map on all222 independent inputs and all moves are nested.
The rail receipt's fitting rows, encoders, decoder masks, residual rank and
residual weight match my reconstruction.

The m=4 word has1,325 independent public inputs,39,270 operations,3,564 paid
moves,264 retired lifetimes and peak owned count237. Its exact endpoint is

```text
common main = F(u0) + (F-Q)(u1) + (F-Q)(u2) + (F-Q)(u3)
private k   = Q(uk)
common helper outputs = h
```

where `Q(x,y)=(x,y+Kx)` and `F(x,y)=(x,y+x)`. Thus its common error is exactly
the sum of three actual private residuals. The word retains all common helper
input/output rows. It is a literal **partial** map: the displayed errors are
present in the independently replayed endpoint, so the map is not silently
treated as the native product.

The native has three SWAPs at events34127,34131,34136, between chart dimensions
8 and4,8 and4, and8 and6. Treating these as value swaps while keeping charts
fixed preserves the scalar endpoint rows in this source, but misses six final
chart assignments. The accepted replay exchanges the complete `(chart,value)`
role pair, matching the retained BIT operation semantics. This is not a free
same-chart ADD between those fields.

## Even-m profile formulas

Let `N` be the per-native paid MOVE profile and `H` the437-helper target
profile. I rederived them from the native as

```text
N = {1:1386, 2:1253, 3:62, 4:47, 5:9, 6:104, 7:10}
H = {2:1, 4:25, 6:1, 8:410}
```

The paired caller has two native calls at each of18 stages. Its full profiles
match the independently reviewed, hash-pinned `bit-query-budget/RESULT.json`
(SHA256 `3fb13f8072e0d8b2ff9cead7754533cf95fe5079f144857e558da719d3a533f0`):

```text
P2 = 36N + 444[1] + 444 sum(j=1..8) [7j]
T2 = 36H + 222[127] + 444 sum(j=1..9) [1+7j]
```

For fixed even `m`, the replicated paired caller starts with `m/2` copies of
these profiles. Across its18 stages, replace `m-1` of the `m` native paid
profiles by one Q rail each, and retain only one native helper target profile.
This gives, profile by profile,

```text
P_m = (m/2)P2 - 18(m-1)N + 18(m-1)Q_paid
T_m = (m/2)T2 - 18(m-1)H
```

The paid formula removes only native calls replaced by Q and adds each Q's
actual MOVE profile. The target formula removes helper target credit for the
`m-1` omitted native helper copies. Independent recomputation of both formulas
matches the frozen m4 profiles exactly. The m=4 literal word is one stage's
native-plus-three-Q instance; the18-stage caller scaling is accounted for in
the profile formulas.

At `t=199/200`, the exact directed 128-bit integer-root intervals give:

| Quantity | Independently recomputed value |
|---|---:|
| Original paired margin `(T2-P2)_t` | `-444.06321643233964...` |
| Partial rail price `(Q_paid)_t` | `1610.20887348409983...` |
| Limiting Q allowance | `1621.75088021115235...` |
| Limiting room after this partial rail | `11.54200672705252...` |
| Fixed m=2 room | `-0.79308261829024...` |
| Fixed m=4 room | `7.43031027860493...` |
| Conditional m=4 margin before Q completion | `401.23675504466630...` |

My exact rational interval endpoints match `BUDGET.json` byte-for-byte. The
positive provisional m4 margin is only the allowance before correcting
`K+I`; the missing coefficients must fit strictly inside the7.43031 room
per repeated Q rail, and no such correction is in this package. The all-even-m
formula is valid for the stated repeated paired caller and one-common-native
architecture. Odd m and any changed caller remain outside this check.

## Negative controls and scope

The original native contains1,702 ADDs from non-X fields into X destinations.
Replaying all659 public inputs at the exact source cuts shows the pure-X screen
is a valid extracted subword only when run as its own fresh circuit. Among its
1,027 deduplicated `(chart,row)` histories,670 rows differ from the actual
native field's X component and914 have contamination from other public input
directions; only the111 initial histories are both clean and equal. This
confirms the screen histories cannot be credited as actual native payloads.
The emitted rail does not reuse those histories; it forms packets from its own
independent X inputs and pays its own moves.

The exact `EFREE-CALLER.json.gz` and `EFREE-RESULT.json` payloads referenced by
the prior caller receipt are not present in this checkout, so I did not rerun
the event-level caller derivation. I did rederive `N` and `H` from the pinned
native, verify the paired-profile identities exactly against the reviewed
receipt, and independently recompute every bound in the new budget.

The remaining K+I correction, ordinary scalar and storage work, all-width
physical/compiler/precision contracts, strict supplier steps and a compatible
complex supplier remain open. No new kappa is established.

## Reproduction

From the workspace root:

```sh
python3 -I -B worker-c/check_bit_nine.py --repo . \
  --output worker-c/bit-nine-review/RESULT.json
```

The checker imports no root-work builder or source screen.
