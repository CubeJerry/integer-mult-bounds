# The prescribed S8 completion minimum is exactly five full-width directions

**Proved fixed-source algebraic theorem. Independent review pending. No new
kappa.** This sharpens the valid but nonsharp four-versus-five interval in the
earlier frozen PROOF.md. The active S6 five-versus-six interval remains open.
All actual source, acquisition, locality, cost and chronological-interface
qualifications from that document remain.

## 1. Refinement when a frame bound is saturated

Let k be any field, with V-wide raw records at n ports. A baseline scalar
code B0 gives `B=B0 tensor k^V`. Let I be m ports whose fitting principal
block must be the identity, with `rank(B0 restricted to I)=r`. Let T contain
B and the rows of a complete block fitting. Restriction to I maps T onto
`k^(mV)`.

Suppose i in I has both properties:

1. A baseline row s restricts on I to the unit row e_i.
2. A scalar coordinate functional lambda annihilates B0 and the permitted
   foreign local space L_i, and lambda(e_i)=1.

Then

    dim T - dim B >= (m-r+1)V.                                  (1)

**Proof.** Let K_T and K_B be the kernels of restriction to I in T and B.
For each v in k^V, a fitting row a_v for receiver i restricts to
`e_i tensor v`, as does `s tensor v`. Their difference lies in K_T.
Applying lambda blockwise sends this difference to v: its local fitting
part and baseline row are annihilated. Thus lambda maps K_T onto k^V and
annihilates K_B. Consequently `dim(K_T/K_B)>=V`. Rank-nullity gives

    dim T-dim B = (m-r)V + dim K_T-dim K_B >= (m-r+1)V.

Arbitrary additional rows and block operators are allowed. Their scalar
separability, commutativity and membership in any earlier fitting code are
not assumed. The two stated baseline/functional conditions are essential.
This remains a linear fixed-code theorem. ∎

At V=1, equality in the ordinary frame bound would leave no new restriction-
kernel direction. A receiver whose unit frame row is already in the old code
would then have to use an old-code fitting row. The functional certifies that
no such old-code fitting row exists.

## 2. Three small native witnesses close the S8 gap

Let S8 and T17 be the source code and17-point set of the earlier proof, and
let P be ANY subset of T17. Put `B0=S8+span{e_p:p in P}`. Literal witnesses
on the pinned native source are

    I={0,14,22,23,30,31,59,60},
    s=0xcc00cc6400097c0033000055,
    lambda=e0+e24+e32.

I is an eight-element clique for REAL nonorthogonality, so its fitting
principal block is identity. It is disjoint from T17. The S8 restriction has
rank4. The displayed s is exactly seed-basis row7 in SEED-SOURCE.json and
restricts on I to receiver0's unit row. Every P grant vanishes on I, leaving
the same baseline restriction rank4.

Lambda annihilates every S8 row and every P grant. Its support is disjoint
from T17. The actual native inner products are

    r0 dot r0=4, r0 dot r24=2, r0 dot r32=2.

Thus none of lambda's support is in L0, while lambda(e0)=1. Equation(1) gives

    dim T - dim(B0 tensor k^V) >=5V                             (2)

for every characteristic-two field, every V>=1, every P subset T17 and every
complete block fitting inside T. There is no canonical, W15, vertex-gauge
or small-field restriction on the new directions. Binary annihilation and
rank identities survive characteristic-two extension; the real chart
geometry remains the fixed rational geometry and is not reduced modulo two.

## 3. Matching abstract upper bound

The canonical fitting code C9 supplies a complete fitting, and

    dim(C9 intersect S8)=4,
    dim(C9 intersect (S8+span T17))=4.

Monotonicity gives the same intersection dimension for every intermediate
P. Adjoining C9 therefore adds exactly5 scalar directions. Tensoring gives
a complete block fitting with5V new dimensions. Together with(2):

**Theorem.** The minimum additional row-space dimension for a complete native
fitting from the prescribed S8 ground code, even granting any subset of the17
raw feedback coordinates freely, is exactly5V at width V, over every
characteristic-two field.

This is an abstract completion theorem, not a five-field physical source.
Canonical acquisition and receiver-correction costs are not paid by the
matching rank upper bound. Current W15 histories remain distributed in time
and chart; none is converted to a free ground code by this theorem.

## 4. Verification and limits

`certify_saturation.py` checks the exact seed/native pins, all64 ordered frame
inner products, rank4 restriction, displayed source row and three-coordinate
lambda identity. It verifies both canonical intersections for the upper
bound. Negative controls remove lambda's own coefficient, duplicate a frame
port, substitute a wrong baseline row, or grant e24 under the unchanged
annihilator premise. The last control exposes the precise boundary: free
coordinates outside T17 are not included in this theorem's feedback clause.

```sh
python3 certify_saturation.py --repo REPO --seed SEED-SOURCE.json --out output
```

Expected status: `PASS_EXACT_FIVE_DIRECTION_COMPLETION_MINIMUM`. The exploratory
normalized-frame solver first found inconsistent forbidden equations(0,24)
and(0,32); the final proof does not rely on a failed search.

The proposed four-direction completion of unchanged S8 is excluded, including
operator-width and extension-field variants. A repair must price five actual
directions, change required ground preloads, or change the chronology/local
interface so this prescribed-code hypothesis no longer applies. For active
S6, only the earlier interval5..6 is established; its first extremal-frame
equations were consistent and no sharper lower bound is claimed.

All literal partial words and their histories remain valid. All five
foundations, strict suppliers and complete compiler/precision/recursive costs
remain. **No new kappa.**
