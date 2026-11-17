# Nonregular dihedral ranges exclude both active-swap orientations

**Proved universal range theorem and source-specific ordinary-caller
obstruction. No new κ.** The previous regular-D8 hypothesis can be removed.

For unitary involutions `f,t` on dimension `d`, with `t` nonscalar and
`z=(ft)^2` a central involution, form the collective width-V projectors
`P=(I+f^tensor V)/2`, `M=I-P`, `T=(I+t^tensor V)/2`.
The two exact range projectors for `PT` and `MT` have combined rank

```
d^V - delta_V,
delta_V=(d^V+tr(z)^V-tr(t)^V-tr(zt)^V)/4.
```

Both `t` and `zt` are nonscalar involutions. Thus for even V,
`delta_V >= (d^V-2(d-2)^V)/4`, which is positive for all sufficiently large
even widths. At `d=16`, every even `V>=6` suffices for the uniform bound.
The full proof establishes the range witnesses and scalar exceptions; no
one-column rank is extrapolated.

For the retained source, when both forward conjugates of `t` required by
the first-column construction are ordinary, this gives an ordinary projector
of rank below D fixing the entire possible Gaussian4 component. Independent
Gaussian (4,2,1) endpoints require that component to have rank D and are
therefore excluded. Arbitrary remaining C entries, Q and ordinary endpoint
units are allowed in the stated fixed finite catalogue and faithful widths.

In particular `t=SWAP_ab` without the balancing `Z_c` is excluded too. Its
combined row range is `3*16^V/4+8^V/2`: it equals D at width one but is already
224 rather than 256 at width two. The old width-one control remains correct;
its missing all-width consequence is now supplied. `SWAP_ab Z_c` recovers
the earlier exact `3D/4` formula. The spectator swap has nonordinary forward
conjugates and remains outside this theorem.

See [proof and abstract group-algebra checker](../../sessions/2026-11-17-S019/checkpoint3-evidence/R/dihedral-row-range/PROOF.md)
and [independent review](../../sessions/2026-11-17-S019/checkpoint3-evidence/C/dihedral-review/REVIEW.md).
Separate exact implementations verify literal conjugates, all group traces,
range witnesses, scalar controls, and the width-one/two distinction.

Credit B's original row-range mechanism, C's independent D8 review and finite
control, root's nonregular-character extension, the retained source authors,
and @CubeJerry. Prepared with substantial OpenAI assistance. The range
projectors are analytical certificates, not free physical operations. Both
strict suppliers, the full recursive proof and all five foundations remain.
