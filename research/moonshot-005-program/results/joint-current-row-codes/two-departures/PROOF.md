# Two compatible paired quotient departures through a shared lower code

**Proved algebraic lemma and exact finite source construction; independent source review pending. No new κ.** Prepared for @CubeJerry with OpenAI assistance. Existing source, E8, paired-cohort, two-frame, reversible-encoder and coupled-precondition contributions retain their credit.

## 1. Result and exact scope

The actual 78,145-instruction word is a literal extension of the combined two-frame/eight-coupled word. It replaces the old primal and dual blocks of one B cohort by a single jointly encoded schedule. Its all-1880-coordinate prefix differs in exactly four rows:

- first Y112 changes by −q_X90/2;
- hosted X2_90 (role 860) changes by +q_Y2_0/2;
- first Y119 changes by +q_X43/2;
- hosted X2_43 (role 815) changes by −q_Y2_7/2.

Every other live prefix row is identical to the parent. The common suffix is identical, and these four changed rows have no later uses except their own final common recoupling. All eight complete B forward receivers and all eight complete coupled reverse outputs are retained. The hosted reverse residual still has exact rank 88. The forward residual has 4567 nonzero coefficients in the changed donor basis, or 4918 in original difference coordinates. The second-frame debt becomes 350 forward coefficients, of which 318 are hosted reciprocal coefficients and 32 are unchanged coupled-coordinate forward coefficients.

This is a construction of two compatible departures from authentic current carriers. It does not assemble a complete receiver, new supplier, uniform compiler or exponent improvement.

The immutable source SHA256 is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
The combined parent compressed SHA256 is
`54b268f4e67e696b6e7e1bdbabb8fd136a434d312f2e305bd714e1f245e2473a`.
The resulting compressed SHA256 is
`8679471f82cbb0fa850dd7b1f450e8c5d25b9f54b42f4df22bc9f7bac6a1e45d`;
its canonical JSON payload SHA256 is
`a2da2e71223578e69a129eee93e5023cd30aea099c51950b8d515df5a42d4d15`.

## 2. General compatible-departure lemma

Let A be an m-by-p matrix over a field. Let T be an invertible change of coordinates supported on non-exit carriers. For an exit set E, suppose vectors u_j are supported outside E and satisfy `(A T^{-1}) u_j = A_j` for every j in E. Put

    N = I + sum_(j in E) u_j e_j^T,     P = N T.

Because every u_j has zero entries on E, all products `(u_j e_j^T)(u_k e_k^T)` vanish. Thus `N^{-1}=I−sum u_j e_j^T`, and `A P^{-1}` has zero columns on E. Encode the real primal and dual banks by `P` and `P^{-T}`. The original A duties can then be performed from the remaining real coordinates, subject to their actual rank, routing and cochart conditions.

At a new receiver j, an exit pair can perform `c_j += alpha_j a'_j` and `b'_j -= alpha_j d_j`. Since T fixes E and N does not change its exit rows, `a'_j=a_j`. After the remaining original reciprocal duties and actual decoding by `P^{-1}` and `P^T`, the original forward map and transpose are restored, with precisely the additional isolated terms

    c_j += alpha_j a_j,        b_j -= alpha_j d_j.

Indeed `P^T(A P^{-1})^T=A^T` and `P^T e_j=e_j`. This proves the algebra for arbitrary inputs, with all original and temporary fields treated as actual records. It grants no physical reconstruction at separated charts.

A branched physical implementation needs a real shared cochart for each T block, nested branch charts for the portions of N, retained routes for the reduced original duties, and a real common decode chart. Different branches must receive distinct output records of the shared code. They cannot each assume their old unmixed inputs remain available. The construction below verifies these conditions on the pinned finite complex source. Its scalar algebra holds in any field of characteristic other than 2; the physical Clifford realization remains the given complex-field one.

## 3. Shared code and exact source geometry

The existing cohort has chart C=1097 of dimension 6, donor order
`[11,24,30,43,78,83,85,90]`, and old forward rows `[117,168,189,208]`.
Its original matrix A is

```
[-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,-1/2]
[-1/2,-1/2,-1/2,-1/2, 1/2, 1/2, 1/2, 1/2]
[-1/2,-1/2, 1/2, 1/2,-1/2,-1/2, 1/2, 1/2]
[-1/2, 1/2,-1/2, 1/2, 1/2,-1/2, 1/2,-1/2]
```

Write `u=A83`, `v=A85`, `x=A78`, and `y=A11`. The exact relations are
`A90=−x+u+v` and `A43=y−u+v`. The shared donor lines 83 and 85 span D0=1111, dimension 2. Their true original primal and dual fields first move to D0. On their ordered primal pair execute

    a85 -= a83;  a83 += a85/2;  a85 *= 1/2.

The resulting matrix is `T=(1/2)[[1,1],[-1,1]]`. On their true dual pair execute

    b85 -= b83;  b83 *= 2;  b83 += b85.

This is exactly `T^{-T}=[[1,1],[-1,1]]`. There are no duplicate source banks.

The branch charts are D1=1112, the dimension-3 binary span of donor lines `[78,83,85,90]`, and D2=1113, the dimension-3 span of `[11,43,83,85]`. Exact binary containment gives

    D0 < D1 < C,       D1 < actual facet of S0,
    D0 < D2 < C,       D2 < actual facet of S7.

The two branch charts are distinct. They receive different encoded carriers: the plus coordinate 83 goes to D1, the minus coordinate 85 goes to D2. The real pairs 78,90 enter D1 from their original lines; the real pairs 11,43 enter D2. All six source donors are hosted, so all twelve input records are independent actual fields. Coupled donor 30 is not used by this shared transform.

At D1 perform

    a78 -= a90;  a83 += a90;  b90 += b78−b83.

At D2 perform

    a11 += a43;  a85 += a43;  b43 -= b11+b85.

These are the two commuting N shears. The current coefficient columns on surviving carriers 83 and 85 are respectively `u+v` and `−u+v`; those are the columns used by every subsequent old-cohort operation.

The actual pair 90 visits the S0 facet, changes its stationary forward collector by `−a90/2`, changes its own dual by `+d0/2`, and proceeds to hub 127. The actual pair 43 similarly visits S7, adding `+a43/2` to its stationary collector and `−d7/2` to its dual, then proceeds to the hub. The all-1880-coordinate entry replay confirms that both collectors and both unmodified Y2 receiver fields are already at these facets and that the twelve incoming branch fields have not been spent or changed. The existing collectors are reused without new owned lifetimes or moves.

## 4. Full old duties and true inverse

The remaining six primal coordinates are `[11,24,30,78,83,85]`. The original primal pivots `[11,24,30,78]` and their original nonsingular 4-by-4 minor are unchanged. The two surviving nonpivots use the new sum/difference columns. The original accumulator, snapshot, four receiver-delivery and inverse-minor pattern is rebuilt with exactly these current coefficients and actual locations. All four old B output rows are preserved.

The remaining five hosted dual coordinates are `[11,24,78,83,85]`. Their restricted matrix retains row rank 4. The selected pivot minor uses `[11,24,78,83]`. The emitted 5-by-5 invertible matrix places the four desired old rows at these pivots and preserves the other coordinate. Its literal inverse-transpose is used before the four authentic receiver reads; its transpose decodes at the hub. No original column or route is silently restored before its actual inverse runs.

After that reciprocal decode, undo the N dual shears at the hub:

    b90 += −b78+b83;        b43 += b11+b85.

Then undo the shared dual transform by its transpose:

    b83 -= b85;  b83 *= 1/2;  b85 += b83.

After the original primal decode, undo N at the hub:

    a78 += a90;  a83 -= a90;  a11 -= a43;  a85 -= a43.

Finally undo T:

    a83 -= a85;  a85 *= 2;  a85 += a83.

Every first-X carrier is thus restored to its combined-parent current/preconditioned donor value before the later E8 packet formation (the involved hosted donors to original q_X, and the eight coupled carriers to their preconditioned x−y values), and every old hosted-dual duty is restored with only the two declared new reciprocal terms. The source checker compares every live row on all 1880 independent common/private coordinates, not just zero-common or initialized toy inputs. Its information inverse subtracts the four declared new terms using the restored authentic inputs. Both changed first-Y fields and both changed X2 fields have no later feedback into any other field.

## 5. Reverse rank and exact paid invoice

Let K=B union S be the parent's closed sixteen-port principal Gram block. Both new residual row indices 90,43 are outside K; both new column indices 0,7 lie in S. The eight old left-kernel vectors are supported on K and remain in the left kernel. The parent's nonsingular 88-by-88 minor obtained by deleting S is unchanged. Thus the rank stays exactly 88. The checker independently extracts the actual 96-by-96 rational residual from the interpreted rows and obtains this same rank. Neither new diagonal is completed.

Relative to the 78,155-instruction combined parent, the entire new word has:

| Quantity | Increment | Final value |
|---|---:|---:|
| MOVE instructions, all raw | +16 | 7077 total; 751 raw |
| ADD instructions | −22 | 66483 |
| SCALE instructions | +4 | 3666 |
| INIT instructions | −4 | 459 |
| CLEAR instructions | −4 | 459 |
| COPY instructions | 0 | 1 |
| Owned peak | 0 | 43 |
| Instructions | −10 | 78145 |

Every newly introduced MOVE is a raw route refinement; the owned MOVE histogram is identical at every rank. The exact raw signed rank histogram is

    +12{rank 1} +8{rank 2} +4{rank 3} −8{rank 5}.

Total raw rank mass stays 3200. Consequently, at t=199/200 the extra paid moment per native instance is exactly

    12 + 8*2^t + 4*3^t − 8*5^t.

The complete provisional caller adds 18 times this signed histogram to the parent paid profile and retains the entire T4 target. It still charges all eight rank-9 E8 calls, all eight rank-1 coupled-precondition calls, every inherited raw move and every inherited owned call. There are 135450 paid positions and 27344 targets; the rank surplus remains 3616. Exact dyadic bounds, using integer 200th roots, give remaining moment per native instance

    32.24557971165029...

The remaining moment is positive, but it is available only for the still missing source operations under the inherited conditional model. This result supplies neither the entire remaining forward/reverse matrix nor an all-size uniform compiler. Scalar coefficient work, allocation/erasure, precision/tape handling and the five foundational contracts remain explicitly retained.

## 6. Verification and reproducibility

From the programme checkout, with scratch package path substituted as needed:

```sh
python3 -I -B build_two_departures.py --repo REPO --combined combined --output two-departures
python3 -I -B check_departure_charts.py --repo REPO --parent combined --output two-departures
```

The builder pins the immutable source and exact combined parent, finds each original replaced block as a unique literal substring, and records actual chronological indices and parent lineage. No native-source instruction is replaced. It reconstructs the true 1880-coordinate entry state, checks every output row, checks exact final location and typed ownership invariants, extracts the actual reverse matrix and computes its rational rank, checks the unchanged common suffix and its absence of feedback from changed rows, and derives all paid/ordinary counts from the emitted operations. A wrong shared-code coefficient is rejected because it changes the actual source map.

The separate chart checker validates all twelve introduced distinct source-to-target maps with the pinned Clifford lowering and signed-Pauli/global-phase engine. It checks exact ascending rank and rejects a wrong global phase. These are finite source checks and supporting algebraic verification. Reusing a previous independent interpreter does not constitute an independent review of this new construction. Admission still requires a separate mathematical and source review.

## 7. Programme implication

This resolves the compatibility issue left by the single-departure witness: two lower-span relations sharing original donors can be realized without giving both branches fresh copies. A real shared prefix sends distinct encoded records into the branches; all later old duties are recomputed against the current matrix, and both inverse maps are paid and emitted.

The result does not license arbitrary simultaneous choices from the 38 initial four-donor circuits. Each further branch must satisfy an actual compatible shared-code and routing construction. The old restricted 34-coordinate-nullity bound remains relevant to pure coordinate departures. The nearest rank-lowering target is instead the twelve-entry principal extension of K by one hosted t: four missing t-from-S entries and eight K-from-t entries. These two new contacts lie in different such extensions and therefore do not complete either extension. The separately developed principal-extension construction is the appropriate source of a rank-87 claim if and when its whole word passes verification.
