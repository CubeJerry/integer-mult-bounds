# Return ranks under arbitrary final-facet words

The actual GF(64) source, two-component H word and Cauchy D word admit two right K words, a 9+36 spread word and a 45-port mixed word. For either K word, no choice of linear operations at the final facets can bring the one-way replacement bank below **41,880 GF(64) symbols** at bank 3,840. This permits singular foreign endpoint blocks, arbitrary invertible local changes of coordinates and the use of every early arrival at each facet. At the price 0.005 the limiting admissible bank is at most 34,694. At the S028 multiplicity 870 it is at most 34,688.

The assertion concerns these fixed earlier words. It leaves earlier reweightings and other suppliers open. The computation also reviews the two previously explicit final-facet choices individually.

## The eight diagonal pivots

Write the proper response as B and the complete native fitting as I+B on 111 independent banks. Work first in one 480-coordinate stripe. Split its rows and columns into the following three consecutive groups.

| Group | Rows | Columns |
|---|---|---|
| First five | 71, 4, 52, 9, 66 | Same five native roles |
| Center | 73, 12, 56 | 15, 20, 33, 34, 39, 44 |
| Last three | 13, 54, 88 | Same three native roles |

Different roles among the eight outer indices are all nonorthogonal in the native root table. Each center row is nonorthogonal to each first index. Each last index is nonorthogonal to each center donor. Proper containment makes every such block zero for every local endpoint reweighting. The center rows and columns are disjoint. The other diagonal blocks are the self-identities of the fitting. Gaussian elimination at the eight outer blocks leaves the central rectangular matrix unchanged. Its rank adds to eight whole banks. Independent left and right basis changes may replace the eight pivots by arbitrary invertible diagonal blocks. The conclusion still holds.

Let E and Y be the stacked actual early and late fields at the three central receivers, restricted to the six independent donors. Each receiver receives all 480 genuine late owners. On these inputs every local linear final word can be written as W Y+T E with W block diagonal and invertible. Invertibility is necessary on arbitrary late baselines. The evaluation allows arbitrary T and every actual early input, including a larger stationary store than the constructed words use. Restrict to ker E. The output rank there equals

    rank(Y restricted to ker E) = rank([E;Y]) − rank(E).

The standard identity follows by applying the projection onto E to the image of the stacked map. The projected kernel is precisely the image of Y on ker E. The pinned calculation gives 1,035 and 2,430 for rank(E) and rank([E;Y]), respectively, with each of the two K words. Thus the center contributes at least 1,395. The fixed earlier words are eight copies of these maps after the role-wise coordinate orderings in their source and facet definitions. Hence the full fitting has rank at least

    8 · (8 · 480 + 1,395) = 41,880,
    h ≥ 41,880 − 9 · 3,840 = 7,320.

The proof still applies when W,T or independent endpoint gauges mix the eight copies or all six bits of each field. Restrict to the kernel of all repeated E coordinates before applying the new maps. Restriction of scalars multiplies the stated field ranks by six. In this case the lower bound is 251,280 independent binary return records. A general deterministic return transcript in the fixed linear fitting interface must distinguish at least this many independent bits.

## Changing the earlier word or adding satellites

Let the true earlier stages produce E',Y' in place of E,Y, in the same physical presentation. On the kernel of the stacked difference [E'−E;Y'−Y], the two pairs agree. Intersecting that kernel with ker E can lose at most the rank of the difference from the 1,395-dimensional image. The identical conclusion applies to an additional arbitrary linear side input by intersecting its kernel. With the unchanged support and the eight guaranteed self pivots, at width 3,840, reaching the 870-multiplicity cap requires a change or combined extra data of rank at least **7,192 field coordinates** on this slice. The limiting cap requires at least 7,186. These are ranks of information. A particular altered native gate may influence many arrivals. Its actual operation and movement prices require its own physical word.

## Four explicit endpoint combinations

A second triangular restriction uses leading foreign pivots (49,39), (87,107), (85,0), (60,43) and trailing foreign pivots (23,98), (34,94), (108,31), (36,79). The center has rows 27,30 and columns 28,48. These twenty roles are distinct, every diagonal foreign pair is orthogonal, and every block below the diagonal groups is geometrically zero. The earlier full-foreign-rank proofs give invertible pivots for either constructed facet word. The four actual central blocks form a 960-square matrix of rank 960 in each combination.

| Actual K | Actual facet | Central rank | One-body return lower bound |
|---|---|---:|---:|
| Spread 9+36 | Transposed Reed–Solomon | 960 | 38,400 |
| Spread 9+36 | Minimum-width captures | 960 | 38,400 |
| Mixed 45 | Transposed Reed–Solomon | 960 | 38,400 |
| Mixed 45 | Minimum-width captures | 960 | 38,400 |

In particular, the four-block holonomy on the two input roles has 480-dimensional defect from the identity. This follows by block elimination using any of the four invertible pivots. Allowing the two extra center donors 50 and 99 gives rank(E)=630, rank([E;Y])=1,500 and the independently checkable 870-dimensional quotient. The self-diagonal argument above removes any external foreign-rank premise.

## Conditional synthesis for a proposed common return space

Write all donor coordinates as x and let π_i select its i-th native block. Fix the actual incoming E_i,Y_i before each facet. Permit arbitrary invertible local ground-side factors and arbitrary linear early captures. A candidate row space U of return messages with dimension q is sufficient exactly when invertible native S_i exist such that

    row(Y_i + S_i π_i) is contained in row(E_i) + U  for every i.

Indeed multiplication of each output by the inverse of its late coefficient changes the native diagonal to S_i and normalizes its late response to Y_i. Addition of a matrix times E_i realizes precisely the row corrections in row(E_i). The final residual then factors through the q rows of U. The converse follows by reversing these operations. Independent input gauges are absorbed by a global blockwise change of variables and new S_i. The application still has to pay to realize any witness.

For fixed U this gives a finite test for the diagonal matrices. Put K_i=ker E_i intersect ker U. There exists an invertible S_i with Y_i=S_iπ_i on K_i exactly when the kernels of Y_i and π_i restricted to K_i agree. In that event the two images are isomorphic via π_i x mapping to Y_i x. Extend that isomorphism to the full native output bank.

For fixed U,S_i satisfying the inclusion, the minimum number of independent linear early captures at facet i is

    d_i = dim(row(Y_i+S_iπ_i)+U) − dim U.

Take d_i linearly independent early row combinations whose classes modulo U span the residual classes. Capturing these and delivering their required output combinations constructs a facet with exactly d_i stored field symbols. Any other correction must span those d_i independent classes. This characterizes the possible stationary-width improvement for a proposed return bank even when the desired native proper fitting has some singular foreign cells. Dense capture and delivery operations, records and return movements still require the usual charges.

## Arithmetic, source and replay

The parameterized paid rank-eight coefficient is 9+h/3840 in Q. Substitution into the retained paired histogram at t=199/200 yields a strict affine inequality in h. Using integer 200th roots to bound each r^t to absolute error 10^−14 gives cutoffs inside (128.00188874,128.00188876) at m=870 and (134.88649663,134.88649665) in the slope. The cutoff is a constant plus a multiple of 1/(m−1), since the gap is affine in m. The 870 value is below the slope value, so every finite multiplicity has a smaller cutoff than the limit. The native counts and the 18(m−1) multiplier are shared with the S028 return-bank and single-grade invoices. Ordinary operations and outer recurrence charges are additional. Neither endpoint combination supplies this tariff at 0.005.

The forward simulator assigns real source polynomial values or scaled derivatives to their actual H slots, applies the pinned H Vandermonde and same-chart delayed derivative, sends the resulting owners through the exact selected D weights, applies each true K stripe and its delayed pairs and reads the actual F owners. Its direct propagation uses every input basis vector. The output contains original field-payload hashes for E, Y and each literal endpoint. The optional independent arrays also compare the spread matrices cell by cell with the separately assembled D-cut contraction.

Run with NumPy and Python using `python -I -B check.py --repo REPO --h-words H_OUTPUT --d-words D_OUTPUT --k-words K_OUTPUT --f-words MINIMUM_F_OUTPUT --out FRESH`. The result includes the pinned native geometry, routes, spread, phase, H, D, K and minimum-facet payloads. The source and terminal definitions are the degree-15 true H source and true K-adjoint maps of the spread-H package. Credit @CubeJerry, the native atlas, the balanced replacement-bank theorem and the participating source, H, D, K and F teams. OpenAI assistance was used. No new complete κ.
