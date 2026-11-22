# Normalized singularity certificates for receivers54 and74

**Receivers54 and74 are excluded under the fixed-H, fixed-retained-space
hypotheses below, even with arbitrary common invertible D readout changes.**
Receiver87 remains unexcluded by the tested input-union condition. No
existence result, instruction count or complete multiplication bound follows.

Author: @CubeJerry, with substantial OpenAI assistance. The two independent
checkers import only the parent review's GF(64) arithmetic. Author solver
code is not imported or executed. The earlier alternative-receiver review
supplies the whole-source forced spaces and full30-section arguments, with
all its source pins verified on replay. Earlier packages remain unchanged.

## Hypotheses

Keep the actual H words, owners and literal retained H interface values
fixed. Retain the D input fibre subspaces for receivers6,9,48,73. Source
tuples may change as arbitrary full linear maps and the compatible D word
may change. Each retained receiver may use an arbitrary invertible readout
Q_r, common across donors. The proposed fifth receiver must isolate its
whole fibre at all native donors, and every retained section must remain
invertible.

Common readouts across donors are essential. Changed H processing, changed
literal H values, changed retained spaces, donor-dependent readouts and
nonlinear maps are outside this theorem. The proof does not require the
833-dimensional coefficient rectangle, phase restrictions or shared rows.

## The normalized necessary condition

For a candidate target t, the pinned review forces K=L W of dimension two.
Targets54,74,87 each have precisely two active retained blocks. At a tight
donor j the actual off-target map M on those two blocks has a four-dimensional
kernel equal to the direct sum of its two separate two-dimensional kernels
U_r. The checkers reconstruct these matrices from actual proper-output owner
labels and the frozen source maps.

The full30 retained H sections force the new source restriction on L_r:

\[
F_{new}(j,h)L_r=F_{old}(j,h)L_r S_{old}(j,r)S_{new}(j,r)^{-1}Q_r.
\]

Set A_r=Q_r^{-1}T'[O_r,:] and V_r=S_old(j,r)^{-1}U_r. Required isolation of
K implies

\[
A_r[:,I_j]V_r\subseteq\operatorname{im}W_r.
\]

Equivalently, Ann(W_r) A_r[:,I_j] V_r=0. Invertibility makes the two images
equal, but only inclusion is needed below.

## Physical normalization of columns4 and5

For each retained receiver, put B_r=T_old[O_r,{4,5}]. The vectors L_r B_r
belong to the retained H observation core at every donor0 D parent. The
checkers verify all sixteen H-core decompositions: four parents for each
of the four retained receivers. Their actual old proper outputs are exactly
the literal D input unit columns4 and5. Thus the D ingress on these vectors
is fixed under every allowed source change.

The retained readout identity gives

\[
T'[O_r,\{4,5\}]=Q_r B_r,
\qquad A_r[:,\{4,5\}]=B_r.
\]

This is a consequence of the literal H values and retained subspaces; it is
not an assumed fixed rectangle for the physical T'. Bridge independently
checks this physical normalization in its rebased-obstruction review.

## Receiver54: input22 forces a dependent triple

For target54 the active retained receivers are9 and48. At tight donor32,
the verifier checks exact coefficient vectors n_r such that

\[
V_r n_r=e_{I_{32}^{-1}(22)}.
\]

It also checks W_9=59 B_9 and W_48=11 B_48 over GF(64). Both factors are
nonzero, so im(W_r)=span(B_r). The normalized necessary inclusion gives

\[
A_r[:,22]\in\operatorname{im}W_r
=\operatorname{span}\{A_r[:,4],A_r[:,5]\}.
\]

Donor0 has inputs [0,3,4,5,15,19,20,22]. Its retained eight-column section
therefore contains the dependent triple4,5,22 and has rank at most7.
Multiplication by Q_r preserves rank, contradicting the required physical
section invertibility. Either retained receiver alone supplies the final
contradiction.

As a special case, with literal readouts and the original phase restriction,
W_r has early-row rank two, while input22 is late. Its image must be purely
late and lie in im(W_r), forcing the whole column22 to be zero. This explains
the literal-family universal-kernel observation without a search argument.

The checker also constructs the larger independent-row relaxation: each
A_r is an arbitrary8-by35 matrix with columns4,5,7,8 pinned and no phase or
shared-row restrictions. Each has248 free entries,72 scalar equations of
rank48 and a consistent200-dimensional affine solution set. Explicit points
are saved. Every point nevertheless has the singular donor0 section just
proved. Affine consistency does not imply determinant feasibility.

## Receiver74: input19 gives the same contradiction

Target74 uses retained receivers6 and73. The extension checker reconstructs
the actual tight donor38 off-target map. For both blocks it verifies

\[
e_{I_{38}^{-1}(19)}\in V_r,
\qquad\operatorname{im}W_r=\operatorname{span}B_r.
\]

Consequently A_r[:,19] lies in span(A_r[:,4],A_r[:,5]). Donor0 contains4,5,19,
so its retained section again has rank at most7. The certificate records
both exact input19 coefficient vectors and both W-profile changes of basis.
The proof requires neither shared rows nor phase constraints.

## Receiver87: a precise passing necessary test

For target87 the active receivers are9 and73. Embed every tight-donor V_r
into the35-dimensional global D input space, adjoin the pinned unit vectors
for4 and5, and take their span P_r. The independent checker obtains exactly

\[
P_9=P_{73}=\operatorname{span}\{e_2,e_4,e_5,e_{14},e_{16},e_{17},e_{27},e_{31}\}.
\]

For every native donor j, the intersection of this span with its coordinate
input space has dimension exactly two. Since A_r must send P_r into the
rank-two space im(W_r), a native intersection of dimension greater than two
would force a singular section. The computed dimension two produces no
obstruction from this test. It proves neither compatible matrices nor source
extensions, and receiver87 is only an unexcluded next target.

## Controls and field/lane scope

For54, the old T has an invertible donor0 section but violates the necessary
input22 relation. Thus the contradiction does not follow from the normalized
pins alone. The earlier block-projection screen remains valid: the present
argument adds cross-donor compatibility through common normalized columns.

Arithmetic is exact over GF(64), represented by x^6+x+1. The identities and
proof persist under coefficient-field extension. For k repeated lanes, the
two pinned column blocks span2k dimensions and the third lies in that span;
the donor0 section has rank at most7k. Common invertible readouts may mix lanes.
No universal conclusion is inferred from random failures.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/target54-normalized-singularity/check.py --repo . --out /tmp/s033-normalized54
python3 -B research/moonshot-005-program/results/bit-coupled-fifth-review-s033/target54-normalized-singularity/extension_check.py --repo . --out /tmp/s033-normalized74-87
```

Expected statuses:

- PASS_INDEPENDENT_NORMALIZED_RECEIVER54_SINGULARITY
- PASS_INDEPENDENT_TARGET74_OBSTRUCTION_AND_TARGET87_UNION_SCREEN

The certificate files contain literal kernel matrices, unit-vector
coefficients, profile factors, H-core normalization decompositions, relaxed
affine points and the exact receiver87 input-union census. No compiler ran.

## Open next questions

Receiver87 needs additional common-section and full-source feasibility
analysis. Targets52,85,98 were not closed by this two-block argument. Any
change to the fixed-H or retained-space hypotheses requires its own physical
interface and cost certificate. No further candidate search was run here.
