# Independent review of the coupled condensation gate

The proposed characteristic-zero matrix identities and exact native ranks
pass independent review. This is an information gate for an explicitly
specified complete local response, not a construction of that response. The
actual packet-cycle word still has its recorded forward and reverse debts.

## Observation contract, including mixed records

Write the current destination as `z=n+R s`, where n and s are independent,
and the desired destination as `n-J s=z-(R+J)s`. For arbitrary raw returned
observations `r=P n+Q s`, conditioning on the actually available z gives

    r-Pz = (Q-P R)s.

Hence exact linear recovery is possible precisely when

    row(R+J) is contained in row(Q-P R).

With additional existing observations `o=A n+B s`, replace their raw rows by
`B-A R` before computing a missing dimension. If the existing and newly
returned observations are already pure functions of s, this reduces to the
row-space/rank formula in the author gate. Because n is independent, z can
take any value at each fixed s; this proves necessity as well as sufficiency.
The proof holds over every field and extends to arbitrary block operators.

The author's statement that the decoder preserves each z is understood in
this conditioned, canonical form. A decoder may literally combine z with
mixed returned rows; one cannot infer that the raw returned rows themselves
are pure. In particular a raw return equal to z has a nonzero s coefficient
when R is nonzero, but supplies zero effective information. The independent
checker includes this false-credit negative control.

## Schur identity and source application

For `E=[[G,A],[T,I+S]]`, with A=GC and T=DG, right multiplication by
`[[I,-C],[0,I]]` and left multiplication by `[[I,0],[-D,I]]` give
`diag(G,I+S-DA)`. These matrices are invertible without assuming G invertible.
Thus `rank(E)=rank(G)+rank(I+S-DA)` over any field. This proves the general
identity; the following finite checks establish its pinned-source premises.

I rebuilt the 104 integer Q9 roots directly from native gzip SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`, without
importing the author's checker, Gram data, receipts, or programme helpers.
Exact Fraction elimination independently verifies:

* the actual hosted96/coupled8 partition and genuine orthonormal hosted basis;
* both cross-block containment identities and `DA=G_UU`;
* joint ranks 16,16,15,8 for the four stated proposed local responses;
* `rank(G_UU)=7` and `det(I-G_UU)=-7/64`;
* the exact invisible coupled mode `(1,-1,0,-1,1,0,0,0)` and the required
  negative-identity action on that mode;
* conditional pure-cache/Gram-return ranks 7,15,16, and the fact that one
  original y17 observation completes the information count.

The coupled roots are not an orthogonal frame. Replacing the required
`G_UU-I` self-response by `-I` leaves rank15, not8; omitting it leaves rank16.
The checker tests these wrong-response controls directly.

The cache `G_UU x_U`, local response `T=G_UH`, original y17 value and its
transport are separate physical premises. The one-dimensional remainder is
not a rank-one MOVE construction. The determinant statement is used only in
characteristic zero here; no characteristic-two BIT consequence is admitted.

## Reproduction and status

```
python3 review_coupled_condensation.py --repo REPO --output REVIEW.json
```

The JSON receipt records all exact ranks and source pins. Root proof review
and an independent source implementation corroborate the author gate, subject
to the explicit mixed-observation clarification above. No supplier admission,
physical cost saving, completed endpoint algorithm, or new κ is established.
This is AI-assisted research for @CubeJerry with predecessor credit retained.

