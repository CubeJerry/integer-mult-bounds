# Complete fixed-history census for the single public-cache promise

On exact #7481, impose only

    u=-e1459-e705+e885=0,

with all remaining helper inputs and all 400 main inputs arbitrary. Retain
every original operation, chronology and coframe. The complete census gives
**no identically zero MOVE and exactly one newly history-reconstructible
whole MOVE target: event 40710, rank 8**. Thus reuse at another original
coframe does not improve this promise's budget.

The sole primary source is WORD.json.gz, SHA256
acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9,
canonical payload64fca675b91298868e12f09423b47e0c2327cba7095e35c8919c1953b4ed68b8.
SOURCES.json pins the unchanged preparation-bound provenance and exact
17-call signed caller separately. No old target/history receipt supplies
the rows in this census.

## Fresh source and complete coframe histories

The checker freshly replays all 76,475 instructions in exact sparse rational
rows. It checks current coframes, strict public/owned nesting, ownership,
coframed scalar operations, COPY into zero and complete lifetimes/endpoints.
MOVE changes the current frame but preserves its normalized latent row.

For every coframe, form B from all original public initial observations at
that coframe and every MOVE arrival, in chronological order. There are 7,780
observations: 1,501 initials and 6,279 arrivals, in 979 nonempty classes. Every
used class has exactly one actual frame ID; no used nonidentical phase/frame
alias is silently pooled. A target's own arrival is excluded from its strict
earlier history. Every original scalar same-coframe value lies in the span
of that accumulated history. Giving the whole historical span grants free
storage and arbitrary processing, so it is an optimistic information model.

The original matrices B are all full ROW rank. The fresh checker certifies
this with sparse COLUMN elimination modulo prime 1000033. It verifies
primality and invertibility of every encountered rational denominator. Each
certificate reaches its literal row-count upper bound m. Its nonzero minor
therefore proves rank_Q(B)>=m, while the row count proves rank_Q(B)<=m.
Every original chronological prefix is consequently independent.

The full-original-history innovation theorem and its classical mechanism
are credited to the earlier all-history-innovation work. Here they are
freshly recertified by an own maximum-row-pivot implementation and applied
to this one non-coordinate promise. No neutral-set restriction or broad
relation search is used.

## One relation creates at most one new arrival per coframe

Append u to B. For 978 coframes the modular augmented rank reaches m+1,
again equal to the literal rational row-count upper bound. Therefore their
exact rational augmented rank is m+1 and u is outside span_Q(B). This is
not bare modular nonmembership: the full rank and exact upper bound are
both explicit. All chronological histories at such a coframe stay independent
modulo u, so no target there becomes reconstructible or zero.

Only actual frame 189 contains u in its final row span. Its original matrix
has 16 independent rows. The checker derives the unique expression over Q
and directly verifies every coefficient. In an independent family B,
the quotient by span(u) has a single dependency, whose support is precisely
the nonzero coefficients in that expression. An arrival row becomes a
combination of strictly earlier rows modulo u if and only if it is the
latest member of that support. Any earlier member still has a nonzero
coefficient on a later independent observation. A row vanishes individually
only when the support is a singleton.

The exact frame 189 dependency is

    u = r40710 - r40708 - r_initial1459,
    r_initial1459 = e1459,
    r40708 = e705+e943,
    r40710 = e885+e943.

The latest support member is 40710. Hence it is the only eligible arrival.
It is the actual public instruction

    ["MOVE",885,3,189,false].

At that cut, both providers precede the target and have actual frame 189:
the original initial observation on owner1459 and the MOVE 40708 arrival
on owner705. Under u=0, their sum is exactly the complete target row. The
initial value of demoted 1459 is granted only in the information screen;
its physical preparation remains paid below. The dependency has three
members, so no row in this frame is zero. A separate exact quotient scan
of all 6,279 MOVE rows independently confirms that no MOVE vanishes.

On the linear promise, deterministic recovery from linear observations is
equivalent to this row-span test by finite-dimensional kernel duality.
A missed target has an input direction satisfying u=0, annihilating its
strict observations but not the target. This also excludes arbitrary
deterministic processing of those same observations on the stated linear
domain. Whole-array identities follow componentwise as source algebra;
all physical all-column and provider assumptions remain explicit.

## Optimistic complete budget and stopping gate

Actual target ranks are R1459=1, R705=R885=8. Demote only 1459, retaining
the other two inputs as arbitrary productive originals. The separate,
source-bound fixed-history preparation probe requires a new whole-field
dependency path from empty frame 3 to dimension-eight frame 189. Its total
rank variation is at least 8. For f(r)=r^(1-kappa), f(0)=0 and
0<=kappa<1, increasing subadditivity gives path price at least f(8).
Sharing that preparation cannot make the total added bill smaller than
this one compulsory path. The scope of that preparation result remains
the unchanged original carriers/histories; changed-carrier mechanisms are
not excluded by this census.

Grant every candidate credit, all ordinary work, cache storage, source
cleanup, private erasure, return and unpriced preparation overhead free.
The only native credit is f(8), and there is no zero-MOVE credit. Therefore

    native gain <= f(8)-f(1)-f(8)=-1.

The exact .0038 per-call requirement supplied for this task is
3.48481964025734707307, so the gap is 4.48481964025734707307. No floating sign
or transcendental pricing is involved: f(8) cancels and f(1)=1 exactly.
The unchanged exact Git caller has 17 native invocations, so its modification
gain is at most -17 under this repeated per-call preparation model; its
complete moment is at most the existing baseline minus 17. BUDGET.json records
this exact cancellation and caller pin. This route is stopped at that gate.

## Reproduction, controls and limits

```sh
python3 -B worker-b/public-relation885/check.py
python3 -O -B worker-b/public-relation885/check.py --output worker-b/public-relation885/RESULT-O.json
python3 -B worker-b/public-relation885/budget.py
```

An explicit --source path can replace the default pinned source location;
any source-byte change is rejected. The research CLI writes only its selected
output. RESULT.json retains exact coframe matrix hashes, modular full-size
minor pivots, the exact rational dependency and all eligible witnesses.

Controls reject treating the relation as independent coordinate zeroing,
crediting an earlier circuit member, a wrong provider coefficient sign,
and a bare modular miss whose history loses rank at the prime. The last
control has rational history rows (1,0),(1,p) and target(0,1): the target is
in their Q span but outside the modular history. It does not reach the
three-row augmented upper bound, so the full-rank validator rejects it.
Normal and optimized results agree after omitting timings. Finite controls
support the source/rank proof; they are not physical cache constructions.

No original source, frozen interface package or published artifact is
modified. No changed word, new productive type, fast preparation, broad
correlation barrier or new kappa is claimed. All five foundations remain.
Prepared for Jerry Chen / CubeJerry with substantial OpenAI assistance;
earlier history-innovation and fixed-history import authors retain credit.
