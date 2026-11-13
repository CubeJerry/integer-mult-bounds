# Independent review: one-relation gate and cache-only higher-codimension bound

## Result

The exact #7481 source reconstructs 47 owned MOVE cuts. Fourteen have a
nonzero main projection that is already in the span of strictly earlier
observations at the destination chart; each of the 47 complete target rows is
outside its full earlier destination history. The other 33 cuts therefore
cannot be supplied by a helper-only relation through that history: projecting
`x = p + u` to main coordinates would require `x_main = p_main`, which fails.
This separates the information obstruction from any helper-space budget.

For the fourteen remaining cuts, the independently reconstructed spaces

`L_E = (P_E + <x_E>) ∩ Q^H`

have total dimension 99 and joint rank 96. Exhaustive rational pair
intersections find only three shared lines:

| Site group | Shared line support | Minimum helper target rank |
| --- | --- | ---: |
| 35152, 45656 | 317, 382, 397, 756, 1344, 1346, 1347, 1393 | 4 |
| 35448, 35452 | 235, 260, 368, 381, 1130, 1131 | 4 |
| 39875, 39884 | 146, 1451 | 6 |

The three pairs are disjoint. The eight unpaired `L_E` spaces together with
the three pair sums have group dimensions adding to 96, equal to the rank of
their joint sum, so these eleven site groups form a direct sum. This proves
that the three pair relations exhaust all cross-site dependencies; it does
not infer that fact from pairwise intersections alone.

## One homogeneous helper relation

I independently enumerated all 16,383 nonempty subsets of the fourteen
`L_E` spaces. There are 16,366 zero intersections and 17 admissible
nonzero intersections: the fourteen singletons and the three shared-line
pairs above. No nonzero intersection is blocked by an old history in this
census. For any admissible intersection `L`, each old-history containment
`L ⊆ P_E` is a proper subspace. Over `Q`, their finite union cannot cover
`L`. If `h` is a coordinate in the union support of `L` with minimum helper
target rank, the coordinate hyperplane `u_h=0` is also proper. A generic
`u ∈ L` therefore simultaneously avoids every old history and uses a
cheapest-supported demotion coordinate. The price assigned to this generic
direction is an optimistic upper bound; preparation, availability and
ordinary work are free here.

At `κ = 19/5000 = 0.0038`, the best no-zero-MOVE relation is the singleton
at event 41646, with native saving `f(6)-f(4) = 1.98030291330265…` per
caller. The only other positive singleton/pair is `{39875,39884}`, with
`f(5)+f(1)-f(6) = 0.0102273551935…`. The exact 17-call complex invoice
requires `3.48481964025735…` native saving per caller. The best subset still
leaves the signed full moment at `-25.5767843582298…`.

If a one-dimensional helper relation also erases a paid MOVE, its direction
must be proportional to that MOVE's full input row. A helper-only direction
can erase only a main-free row. I rebuilt all 6,279 MOVE events from the
native word and independently recovered the same 468 nonzero main-free MOVE
rows, including owner, event, rank and exact rational vector. The complete
one-dimensional direction census (1,101 coordinate units plus 468 MOVE
directions, deduplicated) has five cache-enabling candidates and no
multisite candidate. Only direction 1424 has positive native saving: it is
the row of MOVE 76388, enables the cache at 42500, and loses helper 1498 at
target rank 4. Its native saving is `f(1)+f(3)-f(4) = 0.00851819577085…`;
the signed 17-call moment is still `-59.0971245562704…`. Every candidate's
complete moment is nonpositive.

Thus the one-relation partition is complete within the fixed-history model:
directions that erase a native MOVE are in the exact 468-row list and are
charged with event-union deduplication; directions that erase no MOVE are
covered by the arbitrary 16,383-subset intersection bound. This is a budget
screen, not a supplier construction.

## Any-codimension cache-only bound

This stronger bound grants no extra zero-MOVE credits. It assumes a
homogeneous **scalar-linear** helper relation subspace `U ⊆ Q^H`, with
`ker(U)` surjective onto retained original helper coordinates. It also keeps
the original strictly earlier same-chart histories fixed. A cache at site
`E` requires `U ∩ L_E ≠ 0`; granting a credit for every such intersection
even when the vector lies in an old history only makes the bound more
generous.

Let `T_h` be the original helper target rank and `f(r)=r^(1-κ)`. If `U` has
rank `d`, any usable funding set contains `d` helpers whose coordinate
columns form a basis of `U`. Define

`β(U) = min_J Σ_{h∈J} f(T_h)`,

where `J` ranges over coordinate bases of `U`. The actual lost helper
`f`-price is at least `β(U)`; it need not equal this linear-basis minimum.
For `W = span_E(U ∩ L_E) ⊆ U`, every coordinate basis of `U` restricts
injectively to `W`, so it contains a coordinate basis of `W`; hence
`β(U) ≥ β(W)`.

The eleven site groups above form a direct sum, and therefore
`W = ⊕_g W_g`, where `W_g` is the part in one site group. For any coordinate
basis of `W`, a nonzero determinant has a Laplace term assigning disjoint
coordinate subsets to the row blocks `W_g`, with each subset a basis for
its block. Therefore

`β(W) ≥ Σ_g β(W_g)`.

This is an additive **lower bound** on funding even when the groups overlap
in helper-coordinate support; equality is not claimed.

For an unpaired site `E`, any nonzero `W_E ⊆ L_E` costs at least
`f(c_E)`, where `c_E = min_{h in supp(L_E)} T_h`. The exact source-derived
`(MOVE rank, c_E)` pairs are:

| Site | `(r_E, c_E)` | Cache credit less minimum debit |
| ---: | ---: | --- |
| 30581 | (2, 3) | `f(2)-f(3) < 0` |
| 30593 | (1, 4) | `f(1)-f(4) < 0` |
| 36346 | (2, 2) | `0` |
| 36358 | (1, 4) | `f(1)-f(4) < 0` |
| 41646 | (6, 4) | `f(6)-f(4) > 0` |
| 42487 | (4, 4) | `0` |
| 42500 | (3, 4) | `f(3)-f(4) < 0` |
| 44253 | (1, 2) | `f(1)-f(2) < 0` |

For a paired group, let `R=L_i∩L_j` be its shared line. If `W_g` contains
`R`, any coordinate basis must have a nonzero restriction to `R`; its cost
is at least `f(c_R)`, where `c_R` is the least target rank in the support
of that line. If `R` is not contained in `W_g` and both sites are touched,
then `(U∩L_i) ⊕ (U∩L_j)` is direct and the block cost is at least
`f(c_i)+f(c_j)`. If only one site is touched, its singleton bound applies.

At κ=.0038 the two low-rank pair groups have shared-line upper bound
`f(2)+f(1)-f(4) = -0.984244717229…`; their separate-vector bounds are
smaller. The rank-5/rank-1 pair `{39875,39884}` has shared-line upper bound
`f(5)+f(1)-f(6) = +0.0102273551935…`. Here `L_39875` is exactly the shared
line, whose support target ranks are at least 6. Any second independent
direction from `L_39884` has support target ranks at least 2, so if it is
included its two-dimensional basis costs at least `f(6)+f(2)` and the pair
net is negative. The pair's maximum remains the shared-line case.

All other singleton groups contribute at most zero except 41646. Summing
the group upper bounds gives every scalar-linear helper subspace `U` the
cache-only net-saving bound

`G(U) ≤ f(6)-f(4) + f(5)+f(1)-f(6) = f(5)+f(1)-f(4)`

`= 1.99053026849617996590…` per caller.

The existing 17-call invoice needs `3.48481964025734707306…`, a gap of at
least `1.49428937176116710716…`; even granting all ordinary preparation and
cache work free, the complete signed moment is at most `-25.4029193199398…`.

## Scope limits

- The higher-codimension theorem is for homogeneous scalar-linear helper
  promises with surjective projection to retained helper coordinates. It
  does not cover arbitrary nonlinear restrictions: a nonlinear helper
  relation can expose information that has no scalar annihilator.
- The high-codimension result is cache-only. It does not add any native
  zero-MOVE credits, avoiding double funding a helper target.
- Histories are the exact original strict earlier rows in the target chart.
  Changed providers, new cross-chart imports, or altered frame histories
  are outside this theorem.
- The 33 main-projection misses are a separate information obstruction;
  they do not establish the helper-funding theorem for nonlinear relations.
- No physical word, supplier admission, unconditional theorem, or new κ is
  claimed.

## Reproduction and pins

Run from the workspace root:

```sh
python3 -I -B worker-c/combined-one-relation-review/reconstruct_arrangement.py
python3 -I -B worker-c/combined-one-relation-review/verify_one_relation.py
```

The first replay reads only the exact native word to reconstruct rows,
strict destination histories, the 47-to-14 main-projection filter and all
14 `L_E` spaces. The second script enumerates the 16,383 subsets, rechecks
the source-derived 468 main-free MOVE rows against the retained independent
row receipt, scans the 1,425 one-dimensional classes, and prices with the
pinned rational interval engine. A/B residual-space outputs are not used to
build the site spaces.

| Input / artifact | SHA256 |
| --- | --- |
| #7481 compressed WORD | `acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9` |
| #7481 canonical payload | `64fca675b91298868e12f09423b47e0c2327cba7095e35c8919c1953b4ed68b8` |
| 468-row independent receipt | `15de6d0e53a846efdd5d3f9b34beb8d57fc51534967cc464b12c305ed2cf1834` |
| exact 17-call caller bytes | `255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc` |
| exact signed caller invoice | `86f71ccbc923db5d7a6753aa971c3a9c8a572680534498ed17be072cfa2aae6b` |
| directed price engine | `527d1cb2756ac6c61bd0b08488441105b8902a20e953dce149127bebc74d32bb` |

`ARRANGEMENT-REPLAY.json` is the complete exact source-derived state
receipt. `ONE-RELATION-RECHECK.json` contains every subset and every finite
direction budget row, with exact interval values.
