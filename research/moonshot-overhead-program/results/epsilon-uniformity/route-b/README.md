# Route B — independent uniformization and physical compilation

The distinct contribution of this route is a **linear-budget preflight
selector**. It spends `O(n)` actual steps finding and validating resource
plans, retains the best completed plan, and executes it once. For each
eligible plan, search weights affect the length at which it becomes
eligible; they do not multiply its execution time.

This is a family-specific, fixed-tape/common-visited-space adaptation of
established time-bound-search ideas, with explicit hypotheses. It does not
claim that the full source billing compiler or the exact endpoint has been
constructed.

## Results and scope

| Document | Established statement | Remaining dependency |
|---|---|---|
| [Preflight selection](preflight-selection.md) | P1 is a complete physical selection theorem; P2 gives `H=O(x^a)` under explicit family/compiler bounds, including a conditional endpoint at `a=0` | Sound bill compiler and the quantified physical plan family |
| [Binary-length schedule](binary-length-schedule.md) | Actual-step search guarantee with binary parameter weights, common space and sparse exponent indexing | Candidate constants and thresholds |
| [Linear chunk overhead](linear-chunk-overhead.md) | Alternative rowwise proof of `r^2 t(ceil(n/r))+O(rn)` and an explicit common-cap threshold | Candidate time/space constants; overlaps S002 A3–A4 |
| [Macro dispatch transfer](macro-dispatch-transfer.md) | A fixed finite primitive library makes description dispatch additive in macro events; explicit control and bill-generation bounds | Physical opcode contracts for the complete source |
| [Tower-profile comparison](tower-profile-comparison.md) | Preflight does not improve the current advertised tower envelope using only its coarse cost profiles | Better core execution/space and/or threshold growth |
| [Independent reviews](independent-reviews.md) | Lead certificate calculus and literal p-adic lift proof reviewed, with successful finite replay | No human or Lean certification |
| [Global synthesis review](global-synthesis-review.md) | Theorem E's quantifiers, complete profiles, common space and integer inversion pass a snapshot-pinned audit | The cited source/compiler proofs; no full formalization |

## Exact conditional endpoint/polylog-log theorem

Let `L=1+log_2 n`, `x=log_2 L`. Suppose one fixed sound preflight/executor
pair generates exact common-space plans with physical bill

```
U_j(n) <= C j^a n L^(1/2+1/(j+2))   (n >= N_j),
log_2(1+log_2 N_j) <= C_N j,
g_j(n) <= G_j L^v_j,
log_2 G_j <= 2^(C_G j),   v_j <= 2^(C_V j).
```

All constants are uniform, every plan's actual interpretation/movement and
data preparation are charged, and all visited cells fit common fixed
regions of `O(n)` size. Then P1 and the proved integer/threshold choice give
one exact fixed machine with `T(n)=O(n sqrt(L) x^a)` and `O(n)` visited space.
The hypotheses are not established for the original source. In particular,
`a=0` requires bounded physical execution coefficients, which literal
growing-template layouts need not have. This is a complete conditional
implication, not a new unconditional multiplication bound.

## Overlap and priority

Read alongside concurrent programme S002 at local verified predecessor
commit `2fe18c267dc76e30b98a662403ca8745d40a913f`, particularly
`routes/A/scheduler-and-chunking.md` and `routes/A/parameter-thresholds.md`.
S002 already gives sparse weighted search and linear chunk assembly, and
separates additive description storage from proportional stream space.
This route retains its different proofs with attribution; it does not count
those overlapping observations as independent new asymptotic advances.

Levin search is the source of the coding principle. Hutter (2002), Theorem 1
and Sections 2, 4–6, is prior art for replacing a multiplicative search tax
by a program-dependent cost of obtaining/evaluating time bounds. Our common
visited-space and finite-budget interface is proved directly rather than
assuming that Hutter's whole machine already has this source model.

## Verification actually performed

Run from the repository root:

```
python research/moonshot-overhead-program/results/epsilon-uniformity/route-b/verify_route_b.py
```

The reproducible final check set passed on Python 3.12.14 at
`2026-11-25T14:37:18.646676+00:00`: 22 exact simple-schedule rounds;
65,536 sharp-weight parameter pairs; 30,948 exhaustive short chunk
products; 205 seeded/boundary larger products; 2,560 space/threshold cases;
9,420 preflight-discovery cases; and 14,400 preparation-window cases.
Negative controls check omitted carries, non-summable bare weights and a
growing index whose generator outstrips preprocessing. The report is
[verification.json](verification.json).

An earlier wider run of the same invariants with 2,000 larger random products
also finished successfully at `2026-11-25T14:37:03.767199+00:00`; the saved
reproduction deliberately uses the shorter bounded check set. Neither run
implements a literal multitape machine or establishes the universal
asymptotics by finite testing.

Also independently ran the lead's `verify_padic_lift.py` and read its source;
the exact coverage and report timestamp are in the independent-review note.
No source-wide Lean build, full formal compiler or human review was run.

## Next proof obligation for the preflight route

Construct a finite macro vocabulary and its **actual physical bills** for a
specific scalable template family. Use M1–M3 to avoid scanning an entire
generated program at every primitive bit step, but retain all coefficient,
table, routing and precision work. Derive a complete time and visited-region
bill and then feed that real compiler into P1. A compiler alone will not
reach the endpoint: its plan coefficients and thresholds must also improve
beyond the literal tower profile.

Prepared for @CubeJerry with substantial OpenAI ChatGPT multi-agent
assistance. All source constructions, prior scheduling principles and
concurrent programme results retain their stated credits.
