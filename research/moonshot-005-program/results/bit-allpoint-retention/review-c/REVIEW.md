# Independent all-receiver-union cut review for the no-drop point-copy prefix

**PASS for the stated necessary cut condition. No six-packet decoder or new
kappa.** Worker C independently reconstructed the native graph and core code,
enumerated all485330 nonempty native nonorthogonality cliques and checked the
62003 nontrivial cases. No author implementation or clique catalogue was
imported. This package reviews the cut reduction and exact finite algebra;
Root separately reviews the actual literal point-copy prefix.

## 1. State hypothesis and arbitrary original Y

Every original input x_j has an actual stationary copy on its native source
line L_j. Three independent pure E modes are retained at ground, where E is
the repaired rank3 halfclass gauge. Every original Y remains at ground with
value y_i+R_i x, with R_i in E. Other local halfbanks may remain; their source
support is contained in their actual charts and adds no knowledge beyond
the retained point copies already inside the same downset.

For a nonempty target set S, let D_S be the union of its receiver-facet
downsets. Write U(S) for all source indices whose lines are OUTSIDE D_S.
Every point input outside U(S) is observed inside D_S. The pure core is also
inside, and therefore the actual ground Y rows, together with the core,
span all independent original y symbols. This is an observation-space
identity for the cut proof, not permission for remote reads in a decoder.

Consequently its full-input conditional demand deficit equals the rank
deficit of the required x_i modulo E and the point copies actually inside.
All111 original y columns have been retained; no unknown Y was set to zero
to claim physical availability.

## 2. Every receiver-union cut is bounded by a clique cut

Let I(S) consist of targets i in S whose own source line is still outside
D_S. For every target in S minus I(S), x_i is already one of the in-cut point
observations, so its demand adds no rank. Distinct members of I(S) are
pairwise nonorthogonal: each is nonorthogonal to EVERY receiver in S.
Thus I(S) is a clique in the native nonorthogonality graph.

Moreover D_I is contained in D_S. Enlarging the initial observation space
can only reduce a fixed demand's conditional rank. Hence

    delta(S)=delta(I(S) demands | D_S state) <= delta(I(S)).

If I(S) is empty the deficit is zero. This proves that checking all nonempty
cliques bounds ALL2^111 receiver subsets, without enumerating all subsets.
The argument does not require a source line outside D_S to be one of S's
targets; those outside nuisance inputs remain in the rank calculation.

## 3. Exact clique formula and complete independent census

For clique I, let U be the source indices nonorthogonal to every member of
I, including self incidence. Let N=U minus I. After quotienting by the point
copies in D_I, the remaining core is E restricted to U. Adding target units
on I and then quotienting by their coordinate space gives the exact formula

    delta(I)=|I|+rank(E restricted N)-rank(E restricted U).  (1)

Every clique of size at most6 passes the six-message necessary capacity
test because its target rank is at most6. A fresh increasing-vertex recursion
enumerates ALL native cliques, using exact rational nonorthogonality. At each
step its candidate set is precisely the higher-index common neighbours of
the chosen vertices. Thus every clique occurs once and only once.

The independent counts by size1 through8 are

    111, 2870, 24689, 87601, 160810, 147246, 57630, 4373.

There are485330 nonempty cliques and no larger clique. Applying(1) to all
57630 size7 and4373 size8 cliques gives62003 exact cases. Their deficits are
4 in29026 cases,5 in30663 cases and6 in2314 cases. The maximum is therefore6.
Worker A's305073 count refers to its noncoordinate recursive enumeration,
with coordinate cases appended separately; this review enumerates all111
vertices directly. Both produce the same62003 nontrivial rank cases.

An independently found sharp witness is

    I={0,14,15,30,38,39,59},  U=I union{60}.

Here rank(E_U)=2 and rank(E_{60})=1, so delta=7+1-2=6.
Ignoring the outside nuisance column60 would incorrectly report5. This
witness supplies a negative control against examining only target columns.

## 4. Scope, controls and width lift

All relevant matrices are binary, and their ranks persist over every
characteristic-two extension field. Tensoring this fixed initial state by
I_V multiplies every conditional cut deficit by V. Thus no receiver-union
cut of this stated type demands more than6V future entrance capacity, and
some demand exactly6V. Arbitrary future operators do not change those initial
cut ranks. This is solely a passed necessary condition: it does not produce
six actual packet values, legal access to copies, or a simultaneous decoder.

Removing all pure core observations makes an eight-frame cut demand8V;
retaining only one core mode leaves at least7V. Those controls and the
outside-nuisance undercount are explicitly checked. Source and pivot bytes
are pinned. Normal and optimized executions agree.

```sh
python worker-c/review-full-point-cuts/check.py --native worker-c/block-rigidity/BIT-NATIVE-WORD.json.gz --pivots worker-a/half-class-gauge/PIVOT-SEARCH-RANK2.json --output worker-c/review-full-point-cuts/RESULT.json
python -O worker-c/review-full-point-cuts/check.py --native worker-c/block-rigidity/BIT-NATIVE-WORD.json.gz --pivots worker-a/half-class-gauge/PIVOT-SEARCH-RANK2.json --output worker-c/review-full-point-cuts/RESULT-OPTIMIZED.json
```

Credit Worker A for the no-drop full-point revision and initial cut reduction;
Worker C supplies this distinct all111-vertex reconstruction and proof review.
The native source, halfclass and conditional-rank authors retain their credit.
Prepared for @CubeJerry with OpenAI assistance. No new kappa.
