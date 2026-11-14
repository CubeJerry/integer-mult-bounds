# Independent mathematical review: union cuts seven, chronological rank eight

**Independent mathematical review and literal-state replay passed. No new
kappa.**

The two claims are compatible. Every receiver-union downset has at most
seven widths of missing demanded information at the purified checkpoint,
while the complete future monotone network still needs at least eight
widths of downward information-transfer capacity. Neither claim says
that seven or eight packet lifetimes suffice.

## 1. Source-state hypotheses

After the actual paid helper, original X inputs are restored at Hub;
all111 genuine point copies x_j remain at their source lines. Y92 is
complete at F92, every other Y is unchanged at ground. The only live
nonlocal X information with monotone access to arbitrary future
receivers is ell=K92 star K54 at ground. A pure K92 cache remains at
C=F92 intersect F54. The helper carrying the copied completed Y92 is
cleared at C and charged. These hypotheses must be established from
the literal word, not from an idealized projected-X state.

## 2. The finite-quadric facts needed for all union cuts

Use the binary eight-dimensional quadric q=1 from the authenticated
source; K_uv=1+B(u,v). In a set of eight pairwise nonorthogonal real
roots, the polar Gram matrix is I+J over F2 and is invertible. The eight
points t_1,...,t_8 are a basis and

    q(sum z_j t_j)=wt(z)(wt(z)+1)/2 mod2.

There cannot be nine pairwise nonorthogonal points. For such nine, their
sum is polar-orthogonal to each, hence zero since any eight span. But
the quadratic value of that sum would be9+36=1, a contradiction.

For an anisotropic point r with coordinates z in an eight-frame, write
s=sum z_j. Its restricted canonical row is

    w_j=1+B(r,t_j)=z_j+1+s.

This affine involution preserves the displayed quadratic form. Thus
wt(w) belongs to{1,2,5,6}. Weight1 means w=e_j and, since s=1, z=e_j,
so r=t_j. Every root outside the frame therefore has restricted weight
in{2,5,6}. This is a proof for every frame, not a census of selected ones.

The native A2 triple satisfies r84=r92-r54 in norm4 representatives,
and its binary labels add. Hence

    K92+K54+K84=1,     C subset F92,F54,F84.

The chart C lies in no other native receiver facet; this can be checked
directly from its exact rational basis.

## 3. Every receiver-union deficit is at most seven widths

Let S be any set of unfinished receivers and D the union of their
facet downsets. Every input x_j for which j is orthogonal to at least
one receiver in S is already observed through its genuine point copy.
Let U be the remaining unknown X indices and T=U intersect S the
demanded unknown indices. Then T is pairwise nonorthogonal, so |T|<=8.
Every original y_t for t in S is already at ground, hence known in D.

If |T|<=7, the bound is immediate, irrespective of nuisance sources.
If |T|=8, there can be no unknown index outside T: it would be
nonorthogonal to all eight and create a forbidden nine-frame. Thus
U=T. This step is essential: only now can a nonzero restriction of
ell be used as one clean demanded equation without nuisance columns.

If ell restricted to T is nonzero, that ground equation reduces the
deficit to at most7. If it is zero, put u=K92|T,v=K54|T,w=K84|T.
Then uv=0 coordinatewise and u+v+w=1, so these three binary supports
partition the eight coordinates. The completed receiver92 is not in T.
If54 and84 were also outside T, all three weights would be in{2,5,6},
and three such numbers cannot sum to8. Hence54 or84 belongs to T.
The actual K92 cache at C is therefore inside D. Its restriction to T
is nonzero because92 is outside the eight-frame. It supplies the missing
equation and again leaves deficit at most7.

If a union also includes the already completed receiver92, dropping it
leaves the same unfinished demands and only removes observations, so
the bound for unfinished-receiver unions still implies the bound for
that larger union.

The seven-set {2,8,9,14,15,60,93} attains deficit7. It is independent,
avoids J92 and the A2 triple, so C is outside its union and ell vanishes
on the seven demanded unknowns. Its original Y values are observed,
but no initial record supplies a nonzero demanded-X combination.

## 4. The stronger chronological rank constraint

The admitted rank-nine certificate uses nine nonorthogonal eight-frames
on26 roles, each role with even multiplicity. All26 avoid92,54,84.
Thus none of their receiver facets contains C, and none equals F92.

Restrict inputs and outputs to these26 roles, setting other independent
inputs to zero for the lower bound. Cut every future non-monotone
information transfer in the time-unrolled network. After those cut
outputs are replaced by independent formal variables, the initial
point copies can reach an output only along allowed line-to-facet
containments. The Hub originals, completed Y92 at F92, and K92 at C
cannot reach any of these26 outputs by monotone paths. The one
exception is the width-V ground value ell.

Consequently the final identity has the form

    I-M0 = A_ell ell + sum_e A_e C_e,

where M0 has zero own blocks and zero forbidden off-diagonal blocks.
The left side is a fitting on the26-role witness graph. The existing
parity-frame argument, applied solely to these26 roles, gives rank at
least9V. The initial ground term has rank at mostV. Therefore

    sum_e width(e) >=8V.

Later transfers may depend on earlier ones. The matrices C_e are their
complete actual input dependence, so no independence is assumed and
each transfer is counted once. This is exactly the admitted
time-unrolled argument with one paid initial nonlocal width retained.

This excludes seven future transfers of width V as the only incoming
capacity. It does not exclude seven lifetimes that create additional
independent intermediate transfer histories; each such transfer must
be listed and priced. Union-cut feasibility is therefore strictly
weaker here than the chronological rank requirement.

## 5. Review conclusion and retained scope

Both mathematical arguments pass independent review under the stated
literal checkpoint. The important qualifications are the nuisance-free
step at |T|=8, exclusion of all three A2 facets from the26-role witness,
and counting future transfer dimensions rather than packet lifetimes.
No complete source, price theorem, strict supplier, or new kappa follows.
The independent replay is in `check.py` and `RESULT.json`. It imports
no author construction engine and represents symbolic values as sets of
original input indices, preserving all222 independent columns. It checks
native frames are unchanged, new frame basis/annihilator ranks, every
actual nested move and same-chart addition, complete retained public and
owned state, and both seven-deficit cuts. It reconstructs the quadric
using a different eight-frame from the author's coordinate choice.

The reviewed literal prefix gzip has SHA256
`074bdf752f03f6060ebf7e9fb548d78a94f866c4425395693388dc43e7c30f47`.
The26-role parity certificate has SHA256
`977eedcdd197d36967f646385fe07f32bae06b37a08f06dd986d8fbccccba001`.
Deleting the complete five-operation purification helper restores the
old region's deficit8, a meaningful negative control. No author price
routine was rerun or represented as independent cost certification.

Reproduction:

```sh
python check.py --repo /path/to/integer-mult-bounds --prefix /path/to/PREFIX.json.gz --output RESULT.json
```

Expected status: `PASS_INDEPENDENT_PURIFIED_PIVOT_CUT_REVIEW`.
Credit the construction worker and root for the source and purification,
the admitted rank-nine source certificate, @CubeJerry, and AI assistance.
