# Exact completion through chart 3 and chart 127

## Scope

This is a conditional synthesis theorem for the fixed seven-deletion experiment. It is not a repaired word, a feasibility result for any endpoint pair, or a new multiplication exponent.

Keep the original 1,289 input roles and target matrix E of the genuine paid five-channel word. Choose two paid new routes. The current use is 27 to 3 together with either 236 to 235 or 762 to 473. The first route carries a fixed rational linear form of the two original input fields at chart 27, before any chart-3 output is sent. The other route and all non-chart-3 internal forms are fixed in a legal causal schedule. Chart 3 has no other incoming message, and chart 127 has no outgoing message in these choices. Each chart-127 incoming field is retained.

The remaining freedoms are arbitrary rational combinations of the 908 original fields and the one received field at chart 3, and an arbitrary rational final decoder on the 902 stored fields at chart 127. The multipliers by which the one received field enters the 909 chart-3 exports are treated as fixed parameters in this theorem; a surrounding search may choose them. Changing the other fixed forms or these multipliers produces a new instance of the criterion.

The theorem is scalar linear algebra over Q. It applies componentwise to complete fields whenever the actual whole-field relative chart contracts are established. It introduces no independent source field or free paid call.

## 1. The exact source pattern

Partition the input vector as x in Q^908 at chart 3 and y in Q^381 at other charts. Partition the desired output E(x,y) as a in Q^387 outside chart 127 and b in Q^902 at chart 127. The checker reconstructs E exactly from the authenticated literal source and verifies the genuine paid compensation has exactly the same endpoint.

The endpoint's bipartite components are 889 invertible singleton blocks and 200 invertible two-by-two blocks. Every two-by-two component has one x input, one y input, one a output and one b output. The singleton populations are:

| Input and output location | Population |
|---|---:|
| x to b | 532 |
| x to a | 176 |
| y to b | 170 |
| y to a | 11 |

Let R=E^(-1), in the corresponding block notation. Among the 387 columns of R_xa, exactly 376 have one nonzero entry, and those entries occupy distinct x rows. Write these columns as r_j e_(i(j)), with r_j nonzero. The other 11 columns vanish. The remaining 532 x rows of R have exactly one nonzero entry each, at distinct b coordinates, and no a entry. There are therefore 370 remaining b coordinates.

These are exact properties of this source, not generic assumptions about an arbitrary operator. The checker writes all indices and rational entries.

## 2. A basis for the 909 paid chart-3 export values

The unchanged original word has 908 chart-3 inputs, no incoming chart-3 message, no chart-3 terminal, and exactly 908 chart-3 exports. Its export matrix on those inputs is invertible: a nonzero vector in its kernel, with every other input zero, would produce a zero full endpoint, contradicting invertibility of E.

In the genuine paid five-channel word, remove export row 94019 from the 909 chart-3 export rows. The remaining rows are exactly the old 908 payload rows, permuted: new 90369 carries old 94019, new 156057 carries old 90369, and the other rows agree literally. The exact checker verifies this statement from the local forms.

Consequently the 909-by-909 matrix whose first 908 columns are the original paid word's chart-3 export payloads and whose last column is a nonzero multiple of the coordinate vector of row 94019 is invertible. Our numerical discovery uses the multiple 1/845660160 to improve scaling. This extra formal coordinate is a basis coordinate for existing export values. It is not an extra independent input. In the constructed word all formal control coordinates will be computed from the actual 908 x fields and the one already paid incoming field.

Let F be this fixed invertible export-value basis. Freeze the multiplier vector w by which the new received field m=l^t y enters the chart-3 exports. The physical export vector is

    F U x + w l^t y,

where U, of shape 909 by 908, is to be constructed. Every such choice is local at chart 3.

Execute the fixed surrounding circuit on formal export coordinates and on y. Let C, of shape 1289 by 909, be its response to F, and let M, of shape 1289 by 381, include the response to y and the fixed term w l^t y. The observed rows are the 387 outside terminal fields followed by the 902 retained chart-127 incoming fields. Before the final chart-127 decoder the circuit is therefore

    [outside outputs; stored chart-127 fields] = C U x + M y.

Write C_a, C_z and M_a, M_z for the two row blocks.

## 3. Necessary and sufficient criterion when C has full column rank

Assume rank(C)=909. The following four checks are necessary and sufficient for a completion by U and an invertible final chart-127 decoder.

1. **All external input columns are correct outside chart 127.**

       M_a = E_ay.

2. **Complete every outside coordinate involving an x input.** For each of the 376 eligible a coordinates j, the vector

       f_j = [e_j; 0] - M R_ya[:,j]

   belongs to the column space of C. Let d_j be its unique preimage, C d_j=f_j. Set column i(j) of U_0 to d_j/r_j. Set its other 532 columns initially to zero.

3. **Complete the eleven remaining outside coordinates.** For each a coordinate j with R_xa[:,j]=0, require

       M R_ya[:,j] = [e_j; 0].

4. **Complete the independent chart-127 coordinates.** Form

       S_0 = C_z U_0 R_xb + M_z R_yb.

   Let L be the 902-by-370 submatrix on the b coordinates not paired with a free singleton x input. Let W=C_z(ker C_a). Require

       rank(L)=370,    span(columns(L), W)=Q^902.

Every condition is exact rational linear algebra on finite matrices. In particular a small least-squares residual is not a passed condition, and numerical rank at a tolerance is not an exact rank certificate.

### Sufficiency

The first condition gives the correct a-output columns for every y input. For an eligible j, condition 2 yields

    r_j C_a U_0[:,i(j)] = e_j - E_ay R_ya[:,j]
                       = E_ax R_xa[:,j]
                       = r_j E_ax[:,i(j)].

Thus the 376 pinned x columns also give their correct a outputs. The other 532 x columns have zero desired a output. Their eventual choices may be any vectors in ker C_a.

Conditions 2 and 3 make the stored chart-127 fields vanish on every a coordinate when the raw inputs are expressed as R(a,b). Consequently those stored fields depend only on b.

Each free singleton x row of R_xb has one nonzero entry at its own distinct b coordinate. Changing its column of U to a vector in ker C_a changes exactly that stock column, by an arbitrary vector in W after a nonzero scalar rescaling. It changes none of the 370 columns of L.

Condition 4 allows one to extend the 370 independent columns of L by 532 vectors from W to a basis of Q^902. Choose preimages in ker C_a and divide by the corresponding nonzero entries of R_xb. Assign these vectors to the 532 free columns of U. The resulting stock matrix S on b is invertible. The final decoder S^(-1), applied locally at chart 127, returns b exactly. The outside outputs already equal a, so the entire endpoint is E on all 1,289 independent input fields.

All choices can be made by exact rational elimination. The final source-3 and chart-127 local forms may be dense, but their dimensions are fixed finite constants. They introduce no new paid route. Their scalar denominators, unsigned mass, and local implementation still require a new native precision/cost certificate before a supplier claim.

### Necessity

Any successful completion has outside output E_ax x+E_ay y. Setting x=0 gives condition 1. The final decoder takes 902 stock fields to 902 independent desired b fields. Since E is invertible, that decoder and the stock map on b must be invertible. Therefore the stock must vanish on every a coordinate in the coordinates R(a,b). This forces conditions 2 and 3.

Full column rank of C makes each pinned column of U unique. For the remaining 532 columns, the outside target is zero, so they lie in ker C_a. In the b coordinates they affect only their separate singleton columns, by vectors in W. The other 370 columns remain L. An invertible completed stock matrix forces those 370 columns to be independent and their span together with W to be all of Q^902, which is condition 4.

If C is rank deficient, pinned preimages need not be unique and this particular four-check formulation is not claimed necessary. One may retain the additional nullspace freedoms in a larger completion problem.

## 4. What this reduces

Once the surrounding circuit and the received-field multiplier vector are fixed, 908 arbitrary input-dependent coefficients at each chart-3 export need not be searched nonlinearly. The theorem either constructs their complete rational matrix and the final decoder or identifies an exact failed linear-algebra condition.

The surrounding search must still find a causal fully paid rational circuit for which these conditions hold. Neither the 120 endpoint survivors nor the present exploratory numerical fits supply one. The source-specific numerical implementation also leaves the full-rank check for L and its completion to a subsequent exact stage. This package certifies the source interface and proves the conditional reduction only.
