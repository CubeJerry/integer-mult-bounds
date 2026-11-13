# Independent review of the mixed cache budget relaxation

## Source-union certificate

I rebuilt the fourteen helper-extension spaces from the exact #7481 native
word with the Wave31 source replay. I used those fresh `L_E` basis rows and
the 468 source-derived nonzero main-free MOVE rows; A's residual bases and the
root's exploratory component output were not used to build the union. The
fresh MOVE rows were compared event by event against the independently pinned
row receipt as a separate cross-check.

The exact-rational union has 567 labeled row occurrences: 468 main-free MOVE
rows and 99 `L_E` basis rows. Its rank is 525 and nullity is 42. A greedy
exact-Q row basis supplies 42 fundamental circuits; joining rows in each
fundamental circuit gives the row-matroid components. I then forced every
basis row of a given cache space into one component and recomputed each
component rank. The result is 418 components in total:

- 11 cache-containing components, with combined rank 101;
- 407 zero-only components, with combined rank 424;
- component ranks sum to 525, confirming a direct-sum decomposition.

The 11 cache-containing groups match the root's exploratory event/site
partition exactly after my source-derived construction. Ten contain both
cache rows and zero MOVE rows; event 41646 is cache-only. The largest mixed
block contains fourteen zero MOVE events and the two cache spaces 35152 and
45656. Every other mixed block contains at most six zero MOVE events and at
most two cache spaces.

| Cache site group | Zero MOVE events | Row-union rank |
| --- | --- | ---: |
| 35152, 45656 | 32681, 39855, 39857, 39859, 45659, 45661, 45663, 45698, 45701, 45706, 51637, 57989, 58936, 76469 | 22 |
| 42487 | 31351, 35683, 43283, 43285, 46810, 47178 | 19 |
| 35448, 35452 | 34154, 34156, 46841, 47000, 48515, 49195 | 15 |
| 30593 | 29930, 46676, 49095, 49520 | 18 |
| 36358 | 40226, 47235, 47444, 51716 | 11 |
| 30581 | 30540 | 2 |
| 36346 | 36333 | 2 |
| 39875, 39884 | 47227 | 6 |
| 44253 | 48894 | 3 |
| 42500 | 76388 | 1 |
| 41646 | — | 2 |

The zero-only component rank histogram is 403 components of one row/rank one,
three components of five rows/rank four, and one component of eleven rows/rank
nine. This establishes the source decomposition needed to price mixed blocks
separately from zero-only blocks. It does not compute a local mixed price or
assert a gain.

## Fixed-subset two-case bound

For the restricted homogeneous scalar-linear promise, let `U` be the full
helper-relation row space. A native zero MOVE row vanishes on `ker U` exactly
when it belongs to `U`. Thus the actual set `S` of deleted zero moves has
`Z=span(S) ⊆ U`. Surjectivity onto retained coordinates makes projection from
`U` to the debited helper coordinates injective. The same is true on any
subspace `V ⊆ U`, so the lost helper price is at least the minimum
coordinate-basis price `β_f(V)`. This is a lower bound, not an equality.

For a cache target row `c_E` and unchanged earlier history row space `P_E`,
linear recoverability on `ker U` is equivalent to `c_E∈P_E+U`. A witness
`u_E=c_E-p_E` lies in `U∩L_E`, where `L_E=(P_E+<c_E>)∩H`. Define
`A(S)={E:c_E∈P_E+Z}`.

There are two exhaustive cases in a coarsened component:

1. If `U` enables no cache outside `A(S)`, the gross credit is at most the
   zero-MOVE price `z=Σ_{e∈S} f(r_e)` plus `Σ_{E∈A(S)}f(r_E)`. Since
   `Z⊆U`, actual helper debit is at least `β_f(Z)`.
2. Otherwise some enabled cache outside `A(S)` supplies `u∈L_E\Z`. Then
   `Z+<u>⊆U`. Granting every cache in the component for this one added
   direction only increases the credit. The debit is at least
   `γ_f(Z,L)=min_{u∈L\Z} β_f(Z+<u>)`, where `L` is the sum of the cache
   spaces in this component. If `L⊆Z`, this case is impossible.

The actual proposal's complete zero-MOVE set is one of the enumerated subsets
`S`; additional unused constraints can only increase the row space and the
minimum funding requirement. This makes both cases upper bounds for any
actual scalar-linear `U`, including `U` with further mixed constraints.

## Generic appended row and prefix pricing

For a fixed `Z` and cache sum `L`, append `u=Σ_j α_j l_j`, with `l_j` a basis
of `L`. For any helper-coordinate set `J`, the rank can increase over `Z|J`
by at most one. It increases exactly when `L|J` is not contained in `Z|J`.
In that case the bad coefficients form a proper linear subspace in the
finite-dimensional coefficient space. There are finitely many column sets
`J`; the union of these bad subspaces, together with `u∈Z`, is a finite union
of proper subspaces. Over infinite `Q`, a rational coefficient tuple outside
that union exists. It simultaneously attains

`r_generic(J)=min(rank(Z|J)+1, rank((Z+L)|J))`

for every `J`, and has `u∉Z` when `L⊄Z`.

Any special `u∈L\Z` has the same whole-space rank as the generic row and no
larger rank on any column subset. Every special column basis is therefore
independent for the generic row too. The generic minimum basis price is no
larger than any special `u` price, so it is a valid optimistic lower debit
for the second case. A rational generic row exists, but this does not give a
bounded-height witness or a physically available preparation schedule.

All helper target ranks in this source are 1 through 9, and
`f(r)=r^(1-κ)` is increasing for the stated κ. With `C_k` the columns of
target rank at most `k`, the minimum basis contains
`rank(C_k)-rank(C_{k-1})` columns of rank `k`. Thus both `β_f(Z)` and the
generic `γ_f(Z,L)` follow from exact rational prefix ranks. Modular rank
lower bounds alone do not determine these minimum basis weights, so the
prefix ranks need exact-Q computation before directed `f(k)` intervals are
applied.

## Composition across components

The coarsened row spaces form a direct sum, certified by exact component
ranks summing to the 525-row-union rank. If `V=⊕V_g` is the span of the
actual zero rows and cache witnesses in the relevant components, take any
nonzero global column-basis determinant for `V`. Laplace expansion by the
row blocks has a nonzero term assigning disjoint column subsets `J_g` to
the blocks, each a column basis for `V_g`. Therefore the cost of that global
basis is at least `Σ_g β_f(V_g)`, even when different blocks use overlapping
helper-coordinate supports. Taking the minimum over global bases gives

`β_f(V) ≥ Σ_g β_f(V_g)`.

This is only a lower bound; it is generally not equality. Any additional
constraints in `U` do not evade it: `V⊆U`, and a column basis for `U` restricts
injectively to `V`, so `β_f(U)≥β_f(V)`. The zero-only groups can be charged by
the separately verified helper-funding theorem; the mixed blocks use the
two-case relaxation. No zero MOVE is counted in both places.

## Scope and wording correction

The proof is valid for homogeneous scalar-linear helper promises with
surjective projection onto retained coordinates, unchanged native
same-chart histories, and no imported cross-chart cache information. It does
not apply to nonlinear helper restrictions or changed providers. The
source-union certificate proves the partition and ranks, not the mixed
subset prices. No actual relation vector, schedule, supplier, or κ is
established.

The draft calls these “eleven mixed components.” The exact partition has
eleven cache-containing groups, of which ten are mixed with zero MOVE rows
and one is cache-only (site 41646). I recommend that wording correction.

## Reproduction

From the workspace root:

```sh
python3 -I -B worker-c/combined-one-relation-review/reconstruct_arrangement.py
python3 -I -B worker-c/mixed-cache-budget-review/certify_union.py
```

The second script rebuilds all 567 row occurrences from the first script's
fresh exact native receipt, validates the independent 468-row snapshot, then
does exact-Q rank elimination and fundamental-circuit coarsening.

| Input | SHA256 |
| --- | --- |
| #7481 WORD gzip | `acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9` |
| canonical source payload | `64fca675b91298868e12f09423b47e0c2327cba7095e35c8919c1953b4ed68b8` |
| independent 468-row snapshot cross-check | `15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834` |
| fresh 14-site source receipt | `88ea4b3ebd50f2ec93739967780b53b20444043a89b49c85b854f8a91825b7b2` |

The machine-readable component certificate is `UNION-CERTIFICATE.json`.
