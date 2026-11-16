# The changed eight-seed code needs exactly four further directions

**Proved fixed-source algebraic result. Independent review pending. No new
kappa.** Replacing both inactive S8 directions by the specified canonical
pair reduces the exact completion requirement from five to four. This is a
statement about the new code, with its source implementation verified
separately. It does not turn distributed histories into free ground fields.

## 1. Exact code and local-information interface

Keep the active six singular fitting rows

    A3, A76, A80, A4, A74, A78

of the pinned 111-root source and adjoin these canonical rows:

    g0 = 0x55cc5798cf1d51e94f294f3596,
    g1 = 0x663399ff98643f8d0ce5bc331b33.

Write U8 for their eight-dimensional binary span. SOURCE.json records every
literal row and native source hash. The pair has quotient masks [24,45,53]
in the construction worker's six-dimensional canonical quotient screen.
The present proof uses the literal rows, not that screen's completeness.

Let P be any subset of

    T24 = {1,3,4,6,21,26,51,55,64,65,67,71,73,74,75,76,77,78,
           79,80,90,94,98,102},

and let B0=U8+span{e_p:p in P}. This includes the actual six early point grants
E6={1,6,73,75,77,79}. Allow every receiver all foreign raw coordinates lying
in its rational native facet, whether or not the source has delivered them.
The theorem therefore uses an optimistic static local-information interface.
No claim that all T24 points are physically delivered is required.

## 2. Four-direction lower bound

Use the witnesses

    I={0,14,16,22,38,40,59,60},
    s=0xcc00cc6400097c0033000055,
    lambda=e0+e17+e24.

All 64 ordered pairs of native roots indexed by I have nonzero real inner
product. A complete fitting must restrict on this frame to the identity.
The restriction of U8 to I has rank five, and s belongs to the active S6
already: s=A4+A74+A78. Its restriction is the unit row at receiver 0.

The functional lambda annihilates all eight U8 rows. Its support is disjoint
from T24, as is I, so the same statements hold after any permitted point
grants. The native products with receiver 0 are

    r0 dot r0=4, r0 dot r17=2, r0 dot r24=2.

Thus lambda kills receiver 0's entire foreign local space and takes value
one on e0. The saturated-frame lemma of FRAME-SATURATION.md applies with
m=8 and r=5. For every characteristic-two field, every record width V>=1,
and every complete linear block fitting inside a row space T containing
B0 tensor k^V,

    dim T - dim(B0 tensor k^V) >= (8-5+1)V = 4V.               (1)

New rows may use arbitrary block operators and need not belong to the
canonical code, W15, or their joint span. The geometry remains rational;
only the record coefficients are in characteristic two.

## 3. Matching abstract canonical completion

The pinned canonical fitting code C9 has dimension nine, and exact ranks give

    dim(C9 intersect U8)=5,
    dim(C9 intersect (U8+span T24))=5.

By monotonicity every intermediate P has the same intersection dimension.
Hence adjoining C9 adds exactly four scalar directions and supplies all 111
fitting rows. Explicit independent quotient representatives, including all
111 decoding coefficients, are recorded in RESULT.json. Tensoring gives the
matching 4V upper bound. Therefore the exact additional linear dimension is
4V for every permitted P, field and width.

The previous S8 minimum was 5V. U8 preserves only the active S6 portion of
the original ground preloads; its two other directions have actually been
changed. The two statements are compatible and the improvement has a real
algebraic cause.

## 4. Exact nonlinear finite-field version

Over any finite field k of characteristic two, even an arbitrary deterministic
nonlinear common message of fixed length q needs q>=4V under this same
baseline and local-information interface. Take independent u_i in k^V for
i in I and t in k^V and restrict inputs to

    x=sum_{i in I}e_i u_i + lambda t.

This family has |k|^(9V) members. Existing baseline measurements have rank
5V on it, annihilate lambda, and reveal u0 through the displayed s. All
point grants vanish. Receiver 0 has zero local input and exactly recovers
x0=u0+t, so the common data determine t. Every other frame receiver's local
input depends only on t, because it contains no frame coordinates. The
common data therefore synthesize all their local inputs and recover every
u_i. Consequently the common baseline and new message jointly distinguish
all |k|^(9V) inputs but have at most |k|^(5V+q) values; q>=4V follows. The
canonical construction shows equality at this abstract message level.

This is the lead researcher's earlier nonlinear restriction argument applied
to the newly certified native witnesses. It does not concern changing local
histories, interactive receiver exchanges, or a different ground code.

## 5. Verification and the outstanding physical bridge

`certify.py` independently recomputes U8, native frame products, the explicit
row and annihilator, both canonical intersections, and all 111 complete
fitting equations. It checks that omitting any one of the four displayed
completion directions leaves an unfitted receiver. Other controls invalidate
the annihilator, unit-row or allowed-point premise. A small exhaustive F2
restricted-family check confirms 512 inputs and 32 baseline values, each
having 16 preimages; the written proof gives the universal nonlinear result.

```sh
python3 certify.py --repo REPO --source SOURCE.json --out output
```

Expected status: `PASS_CHANGED_EIGHT_SEED_EXACT_FOUR_COMPLETION`.

The physical source currently retains the canonical directions in actual
histories. Four extra Hub-to-ground fields would cost 4[8], far more than
the remaining movement room. The useful next step is to acquire and deliver
the missing quotient through inexpensive proper charts or chronological
reuse, with real ownership and restoration. Equation(1) is a dimension
requirement, not a tariff or a construction of that bridge. **No new kappa.**
