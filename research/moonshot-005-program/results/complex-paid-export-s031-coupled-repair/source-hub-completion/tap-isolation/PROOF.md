# An exact one-column tap repair

## Scope

This is a literal partial recoding on the D1 deletion topology. It uses no new paid route. It restores one complete target input column and repairs all source-only outside membership tests. The five-dimensional pinned obstruction and the one-dimensional global rank defect remain. This is not a repaired supplier.

## The physical change

The retained export 48 is sent from chart 3 to chart 117 with the exact original form

    field_48 = -3072 * input_332.

The outside terminal 155100 at chart 117 has the form

    output_155100 = -field_48 / 3072.

In the frozen D1 word, field 48 is also used by eleven retained scalar forms at chart 117. Remove its coefficient from those eleven forms and keep the terminal form unchanged. In the six other chart-3 exports containing original input 332, remove that input coefficient. Keep every other coefficient fixed, apart from removing all references to the seven retired D1 messages, whose frozen values are zero.

The exact patch records each affected slot, removed operand and original rational coefficient. The checker constructs a new `Literal` with the seven paid routes actually absent, and checks causal locality through the literal constructor. It then propagates every original input symbol exactly.

After the change, input 332 appears only in export 48, and that field is used only in terminal 155100. Its entire output column is therefore its original target unit column. All other input columns remain exactly equal to the frozen D1 endpoint. The checker verifies both claims on all 1,289 outputs. In this example the outside rows were already correct on input 332, so every outside endpoint row, including the 73-column external defect, remains unchanged.

There are eleven changed non-source forms and six changed source-export forms. No new owner, paid route, independent input or final decoder is introduced by this patch. A complete native precision and local arithmetic certificate would still be needed for any finished supplier containing the patch.

## What the source-control gate gains

Use the 909 actual chart-3 export values as independent control coordinates. Before the change, terminal 155100 reads only control 48. Thus every representation of another pure outside unit has coefficient zero on that control. The eleven use removals change only column 48 of the control response. That column becomes exactly the nonzero multiple `-e_155100/3072`, while every other control column stays unchanged.

The frozen control matrix has full column rank 909, and `e_155100` is the sole failed member among its 272 pure outside units. Its other 908 columns are independent. Since `e_155100` was not in the old column space, replacing column 48 by its nonzero multiple preserves rank 909. Every other pure outside unit retains its old representation using zero coefficient on column 48. The newly isolated column supplies the missing unit. Therefore all 272 source-only outside memberships now pass.

This statement permits the usual subsequent free source encoding; the concrete patch separately gives the stated one-column endpoint repair.

## What remains unchanged

Let T, h and P be the exact eight-variable reduction of the adjacent frozen-gates package. The patched endpoint is `E-B P1`, where P1 is P with input column 332 set to zero. The checker verifies the full endpoint statement directly. It also checks

    T[332,:] = 0,    h[332] = 0.

Consequently the reduced matrix `Z=[Id-P_I T_I | P_I h_I]` is unchanged by the replacement P to P1. The kernel K0 and its image G are unchanged as well. The natural source-export basis remains invertible: its other 908 columns have coordinate 48 equal to zero and form a basis of that hyperplane, while the replaced input-332 column still has coordinate 48 equal to -3072.

The pinned right-hand sides change only at terminal 155100. Exact rational replay gives 102 remaining failed memberships, with quotient rank still five. The global augmented response still has rank 1288, from the same rank-six seven-by-eight left-kernel matrix. Thus correcting this individual source-only condition does not remove an independent pinned defect, and it does not restore global invertibility.

These exact residual statements prevent the partial construction from being mistaken for progress on the whole target count. The separate all-source-encoder numerical and modular experiments are discovery tools only; they are not used in this proof.
