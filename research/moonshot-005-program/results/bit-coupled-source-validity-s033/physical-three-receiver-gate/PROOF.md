# A sharper physical gate from three actual receiver row sets

**Necessary conditions, with exact abstract sharpness models. No native
construction, sufficient admission criterion, supplier or new κ is inferred
from the gate alone.**

## 1. Actual physical incidence

The pinned35-owner D word has output sets

    O48 = {0,8,10,11,21,22,30,34},
    O73 = {4,10,15,17,20,23,25,30},
    O95 = {10,13,16,18,30,31,32,33}.

Every pair intersects in exactly the two actual rows{10,30}. Each pair union
has14 rows and the triple union has20. The native donor input union V has32
coordinates; only columns24,29,33 are absent. `check.py` obtains these sets
from the source-pinned physical readout records and checks their consistency
at every donor/receiver occurrence.

Let T be any invertible35-by35 word, with each displayed receiver restriction
T[O_r,V] of row rank8. The latter follows from any required invertible native
eight-column section. Write R_r for its native row space, S=R48+R73,
I=R48 intersect R73 and d=dim I. Let M=R95. Since the two shared native rows
are independent, d>=2. Full T invertibility makes each set of distinct rows
independent before restriction. Deleting three columns drops row rank by at
most three. Consequently

    dim S >= 14-3 = 11,             2 <= d <= 5,
    dim(S+M) >= 20-3 = 17.

## 2. The actual receiver cannot reuse every common row

Put e=dim(M intersect I). The two shared rows lie in M intersect I, so e>=2.
Since I is contained in S,

    e <= dim(M intersect S)
      = dim M + dim S - dim(M+S)
      <= 8+(16-d)-17 = 7-d.

Also e<=d. Therefore

    2 <= e <= min(d,7-d),
    dim(M/(M intersect I)) >= 8-min(d,7-d).

At maximal overlap d=5, exactly two dimensions of the actual receiver can
belong to I. Six actual receiver directions must lie outside I. The earlier
coarser observation that at most five receiver rows can come from I misses
the additional independence forced by the20 actual physical rows.

## 3. Refined contrast gate and its essential premise

Let Z be a donor-contrast matrix supported on V, and let A=Ann_row(Z[V]).
Assume **I is contained in A**. This premise is supplied in the fixed-rectangle
source/D family by the projection identity in
`../../bit-coupled-fifth-review-s033/PROOF.md`, section3: any row represented
at both48 and73 has the same forced-K response at every donor. It is not an
automatic statement about arbitrary contrast matrices or arbitrary source
modifications.

Equal actual receiver95 responses on K require M to be contained in A.
Hence

    dim A >= dim(I+M) = d+8-e >= d+8-min(d,7-d),
    rank Z <= 32-d-8+min(d,7-d).

| d | Maximum e | Actual receiver directions outside I, at least | dim Ann Z, at least | rank Z, at most |
| --- | --- | --- | --- | --- |
| 2 | 2 | 6 | 8 | 24 |
| 3 | 3 | 5 | 8 | 24 |
| 4 | 3 | 5 | 9 | 23 |
| 5 | 2 | 6 | 11 | 21 |

In particular, the three-overlap candidate has d=5 and rank Z=27. While d=5
is retained, its necessary actual-receiver target is rank Z<=21, not merely24.
Six extra annihilator dimensions outside its five-dimensional overlap are
required. This is a conditional gate for successful receiver95 equality;
it does not impose rank Z<=21 on every valid local word.

Allowing d to change matters. The later pencil candidate has d=2, so the
refined gate permits rank Z=24. Its separately reviewed actual common readout
is consistent with this theorem. The gate does not favor maximizing d.

## 4. Repetition and field extensions

The dimension proof holds over any field. With k-fold owner blocks, replace
35,32,20,17,14,8,3,2 by their multiples of k. If d is the overlap dimension,
2k<=d<=5k, and

    e <= min(d,7k-d),
    dim Ann Z >= d+8k-min(d,7k-d),
    rank Z <= 24k-d+min(d,7k-d).

At d=5k this gives rank Z<=21k and requires6k actual receiver directions
outside the overlap. Arbitrary linear mixing within the blocks does not
change the dimension argument. No physical implementation cost follows from
these inequalities.

## 5. Exact abstract sharpness and negative controls

For each d=2,3,4,5, the checker constructs an invertible35-by35 matrix using
these exact physical row sets and these three deleted columns. Its20-row
native restriction has rank17. Start with two shared native basis rows,
make d-2 further native coincidences between48 and73, and make5-d further
coincidences when adding95. Lift the total three dependencies using the three
absent columns; the20 full physical rows are then independent. Complete the
remaining15 rows by unused native basis vectors.

Choose the95 overlap with I as large as min(d,7-d), and take A=I+M. A contrast
basis for ker A attains exactly the four listed rank bounds. Four independent
columns seen by M give a common rank-four response; eleven donor images can
all remain rank four. The full matrices and contrasts are saved in
`output/ABSTRACT-MODELS.json.gz`.

These models establish sharpness for the stated row-incidence and annihilator
premises only. They do not satisfy or purport to satisfy the frozen rectangle,
all144 native/geometric section contracts, source interpolation, whole fibres,
phase chronology or supplier billing. Native attainability for d=3,4,5 is not
asserted.

Two controls delimit the proof. First, keep the invertible d=5 physical model
but set A=M. Then rank Z=24 and actual95 equality holds, while I Z has rank3.
The refined rank21 conclusion fails because I subset Ann Z was omitted.
Second, make M contain I with dim A=8 at d=5. The resulting model loses full
physical-word rank and its triple native union rank drops below17. The
ordinary eight-row test alone would miss that loss.

## 6. Reproduction and scope

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-source-validity-s033/physical-three-receiver-gate/check.py --repo . --out /tmp/s033-three-receiver-gate
```

Expected: `PASS_PHYSICAL_THREE_RECEIVER_REFINED_GATE`, followed by the pairs
(2,24),(3,24),(4,23),(5,21). Optional repeated `--candidate` arguments inspect
a literal candidate's physical overlap and conditional bound. No constructor
executable is imported. The source pins and full abstract witnesses accompany
the result. All five foundational assumptions remain explicit.

Credit @CubeJerry, the root's refined gate proposal, S033 adversarial projection
identity and overlap ceiling, and retained S031/S032 physical interfaces.
Substantial OpenAI assistance; exact arithmetic and proof review, not a
formal-kernel theorem or independent human review. Apache-2.0.
