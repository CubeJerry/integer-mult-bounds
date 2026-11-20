# Exact gates for the frozen seven-deletion baseline

## Scope and observation coordinates

Start from the genuine paid word and set the seven D1 message forms to zero, leaving all other forms fixed. The order is

    D = (86, 89777, 97232, 97241, 97320, 97323, 99064).

Neither proposed second route, 236 to 235 or 762 to 473, is present in this baseline. The exact gate permits arbitrary encoding into the 909 existing chart-3 exports and an arbitrary final decoder at chart 127. It does not permit surrounding form changes in the baseline itself. Its failure is not an exclusion of the endpoint pairs after such changes.

The original chart-127 decoder is invertible: its 902 independent target rows factor through exactly 902 stored fields. Apply that original decoder to the observation stock only as an invertible choice of observation coordinates. This leaves every outside coordinate unchanged, and preserves all column-space membership tests. In these coordinates the full original endpoint is E, its inverse is R, and the frozen endpoint is E0.

## The outside external defect

Partition inputs into the 908 chart-3 coordinates I and the 381 other coordinates Y. Direct rational replay gives

    Delta = E[a,Y] - E0[a,Y].

Exactly 75 outside terminal rows and 73 external input columns are nonzero. The result lists every affected input and output, both basis columns, and the exact coefficients expressing every column through input columns 0 and 4. The minor on terminal rows 154880 and 154885 and input columns 0 and 4 is

    [[1/2, 1/2],
     [1/2,   0]],

with determinant -1/4. This proves rank exactly two. Only input 29 in this support is at chart 27; its other original input 691 has zero defect. In particular 72 affected external columns are unavailable to an incoming form of chart 27's two initial fields. The same displayed minor avoids both chart-27 columns, so the defect restricted to those other columns still has rank two.

Consequently a fixed surrounding circuit cannot pass the outside equality merely by changing the chart-3 received-field multipliers. More generally, keeping old scalar coefficients fixed and adding only one scalar correction channel for the other external columns cannot cancel this rank-two defect. This statement does not cover changes to the surrounding old forms.

## An eight-variable exact pinned test

Let P be the 7-by-1289 matrix of the original payloads at D. Let B be the response to seven additive impulses at those slots in the frozen circuit, with all other deleted slots held at zero. A local induction gives

    E0 = E - B P.

Indeed, at each deleted slot the original-minus-frozen difference is its original payload; at each retained slot the difference propagates by the unchanged local linear form. Let v be the frozen response to an additive impulse at the existing chart-3 export 94019, and put

    T = R B,    h = R v.

The natural 909-column export basis has 908 original source-input columns and the extra 94019 impulse. After applying R, the corresponding control matrix is

    C' = [ (Id-T P)[:,I] | h ].

The full-column-rank question and all pinned memberships can therefore be tested through seven payload variables and one extra export variable. Write

    K0 = [ T_Y | -h_Y ],
    Z  = [ Id_7-P_I T_I | P_I h_I ].

For a control vector (u,k), put t=P_I u. The equation C'(u,k)=0 is equivalent to

    K0(t,k)=0,    Z(t,k)=0,

with u=T_I t-h_I k. Hence

    nullity(C') = dim ker(K0) - rank(Z restricted to ker(K0)).

The checker obtains the exact one-dimensional kernel

    ker(K0) = span{(0,0,0,0,1/4,1,0,0)}

and Z sends its displayed generator to (0,0,0,0,1/4,0,0). A nonzero rational 7-by-7 minor of K0 is retained in the result. Thus C and C' have full column rank 909.

For an eligible outside coordinate j, put q_j=P R[:,j]. Subtracting the control contribution of R_xa[:,j] from the pinned right-hand side reduces membership to B q_j in col(C), or T q_j in col(C'). In the equation C'(u,k)=T q_j put s=P_I u+q_j. The equation is equivalent to

    K0(s,k)=0,    Z(s,k)=q_j.

Therefore the pinned membership holds exactly when q_j lies in

    G = Z(ker K0) = span{e_4},

where index 4 denotes deleted slot 97320 in the displayed seven-slot order. This reduction is over Q; it is not a modular or numerical rank calculation.

Project all 376 q_j columns modulo G. The resulting matrix has exact rank five. The checker retains a nonzero 5-by-5 rational minor and the exact left-kernel relation establishing the upper bound. Exactly 103 individual columns are nonzero in that quotient. For example terminal 154897 has

    q_j = (0,0,-1/4,1/4,0,0,0),

so the coordinate functional at deleted slot 97232 isolates a nonzero value -1/4 and proves its pinned membership fails.

Among the 376 eligible coordinates, 272 have R_ya[:,j]=0. Their right-hand sides are pure outside units, independent of every external-source encoding. On this subset the quotient rank is one and the sole failed coordinate is terminal 155100. The other four independent failures belong to coordinates involving an external input. All eleven fixed outside coordinates have P R[:,j]=0, so this particular frozen deletion does not violate their separate fixed-coordinate equations.

## A precise lower bound on surrounding scalar-form edits

This paragraph concerns one fixed acyclic supergraph, one fixed export-control basis and one fixed observation stock. Extend the frozen baseline by any additional internal nodes with zero forms and zero coefficients in old uses. Keep the 909 chart-3 exports as free controls and the final chart-127 decoder free. Count changes to individual scalar forms elsewhere; a local form may have arbitrarily many rational coefficients.

Changing one scalar form changes the complete response matrix [C N] by rank at most one. Its changed scalar value is one linear functional of the independent controls and external inputs, and the rest of the fixed causal circuit propagates that value along one response column. Telescoping s such changes shows that all columns of the total response difference lie in a subspace D of dimension at most s.

Let F(N) consist of the 376 pinned right-hand sides. If the changed surrounding circuit passes the pinned test, then

    col(F(N_old)) is contained in col(C_old) + D.

This follows from F(N_old)-F(N_new)=(N_new-N_old)R_ya and col(C_new) contained in col(C_old)+D. The frozen quotient has dimension five, so necessarily s>=5. A chart-3 incoming contribution remains inside the changed col(C) and does not evade the gate.

This is a count of changed scalar forms in a common causal model. It is not a paid-call lower bound: five or more existing local forms may be changed at no additional communication charge. It does not cover arbitrary retimings whose union has no common acyclic supergraph. It does not assert that adding a new route and freely changing many of its uses counts as only one scalar-form edit. Neither proposed second route is already included in the baseline rank-five certificate.

No repaired word, complete supplier, or new multiplication exponent follows from these gates.
