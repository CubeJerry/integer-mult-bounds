# Varying scalar stripes still cannot complete the balanced native atlas

**Claim submitted for independent review. No new κ.** The fixed balanced
routes cannot realize the full native target when each ordinary quotient
acts separately on aligned scalar stripes, even if its scalar row changes
arbitrarily with donor, plane and stripe. General array maps that mix
stripes remain outside this class.

## 1. Model and canonical input slice

Use the authenticated S022 balanced geometry, with b=5760r=16p field
coordinates per source, p=360r, over any finite characteristic-two field F.
Each source has the common actual coordinate indexing X_(j,s,t), where
1<=s<=16 and 1<=t<=p. At each ordinary donor-plane flag assume its quotient,
up to an arbitrary bijective relabelling, has coordinates

    Z_(j,H,t) = sum_s c_(j,H,t,s) X_(j,s,t).

The scalar row may vary freely in every index. There is no common row,
common kernel, common dictionary or common stripe coefficient. The common
stripe indexing in the original coordinates is a real hypothesis: arbitrary
cross-stripe donor basis changes need not preserve this class. The eleven
singleton source encoders are unrestricted within their real540r capacity.
Downstream operations and same-chart caches may be arbitrary deterministic
functions. No additional routes or raw Hub information are granted.

The balanced quotient theorem applies on the canonical-zero, zero-Y slice.
For an ordinary plane H let J_H be its native donors, m_H=2 or3, and let
I_H comprise receivers seeing H whose source cuts are tight for every j in
J_H. At any such receiver each donor's sixteen visible quotient rows form
an invertible16-by16 matrix separately at each stripe. Plane gluing forces
the inverse-coordinate lift lines to agree across the donors of H.

Thus the required p-dimensional plane target, in the independent quotient
variables Z_(j,H,t), has row space

    W_(i,H) = direct_sum_t F rho_(i,H,t),

where each rho is a nonzero row on the m_H source scalars at that stripe.
The summands use disjoint stripe coordinates. All components of each rho
are nonzero; the argument below only needs rho itself nonzero.

## 2. A port carries only stripes with a common target line

Receiver i sees fifteen actual H-to-D4 ports, with total capacity p. Fixing
the other source-plane quotients leaves every H quotient free, and the
receiver must recover its whole p-dimensional H target. Exact alphabet
capacity therefore makes the joint fifteen-port tuple a bijective
relabelling of that target. Every individual port factors through the
linear target map, even when the port encoder itself is nonlinear.

Let S_D be the receivers in I_H that see one actual H-to-D4 port D. If
S_D is nonempty, the port is invariant under the kernel of each target map.
It is consequently invariant under their kernel sum and factors through
any linear map with row space

    intersection_(i in S_D) W_(i,H).

The common-function assertion follows from additive translation invariance;
it does not assume a linear downstream code. Because the stripe summands
are aligned, this intersection is the direct sum, over stripes t, of the
intersections of the one-dimensional lines F rho_(i,H,t). At stripe t the
intersection is one-dimensional precisely when every line on S_D is the
same; otherwise it is zero.

Fix t and color each receiver i by its projective line F rho_(i,H,t).
Every receiver must lie in at least one monochromatic port neighborhood
S_D. Otherwise none of its fifteen ports depends on its stripe-t target,
and varying that source stripe while fixing all other stripes contradicts
recovery. This is a necessary condition, not a sufficient construction.

A valid coloring is therefore a partition of I_H into nonempty classes,
where each vertex belongs to an entire port neighborhood contained in its
own class. Merging classes preserves validity. In particular, absence of
a valid k-coloring excludes every coloring with at least k colors.

## 3. Exact finite coloring bounds

For each ordinary plane, let alpha_H be an upper bound on the number of
colors in a valid coloring, capped at m_H. The pinned geometry has:

| Native donors m_H | alpha_H | Number of planes |
| ---: | ---: | ---: |
| 2 | 1 | 204 |
| 2 | 2 | 23 |
| 3 | 1 | 630 |
| 3 | 2 | 249 |
| 3 | 3 | 2 |

These are complete finite partition decisions. Each color must contain a
nonempty port neighborhood. Thus k colors require k pairwise-disjoint
neighborhoods; failure of this small packing test proves nonexistence.
For remaining cases a complete deterministic search assigns vertices to
k=2 or3 colors. One fixed vertex may be assigned color0 by symmetry;
all colors must be nonempty at a successful leaf.

For partial color classes C_c, a port can have color c only if it avoids
every already assigned other color. For each vertex, list its containing
ports compatible with each color. An assigned vertex with no compatible
port is impossible. An unassigned vertex with no compatible color is
impossible; with just one color, its color is forced. If an assigned
vertex has just one compatible port, every vertex on that port is forced
to its color. Repeat these deductions. If free vertices are fewer than
unused colors, reject. Otherwise branch a free vertex over every color.
Every pruning rule is necessary. Exhausting all branches therefore proves
nonexistence; every successful assignment is checked against the original
port neighborhoods.

The computation covers all111 receivers and1108 ordinary planes, without
timeout, floating arithmetic or unknown status. Its finite decisions need
separate implementation and review before admission. Field and stripe
counts never enter the search: only fixed authenticated incidence appears.

## 4. Global information bound

At stripe t, all covered-port outputs factor through the span of their
receivers' target lines. Its dimension is at most the number of colors
and at most m_H, hence at most alpha_H. Across p stripes, the complete
covered-port tuple is a function of at most alpha_H*p field coordinates,
even with nonlinear outputs and downstream cross-stripe mixing. Grant
each uncovered port its entire p/15 capacity.

There are1436 uncovered ports. Grant the eleven singleton planes their
entire540r source alphabets. The complete plane-output alphabet is at most

    |F|^[360r*(204+2*23+630+2*249+3*2) + 24r*1436 + 11*540r]
      = |F|^(538644r).

On the canonical-zero slice, all111 native targets equal X because K=I+O.
The input dimension is(111−9)*5760r=587520r. Canonical descents are zero.
Every other varying route to receiver outputs crosses the counted plane
boundary. Correct recovery would inject this larger input space into the
smaller output alphabet, impossible. The deficit is48876r. Subject to the
source-interface hypotheses and finite geometric certificate, this proves
the exclusion at every positive r and every finite characteristic-two
extension.

## 5. Constructive boundary

The theorem excludes coordinate-varying direct sums of scalar source rows
as well as identically repeated rows. The successful four- and seven-source
fragments pay different private/shared ports and do not contradict it.
General quotient arrays can have intermediate intersections that do not
decompose into common stripe lines; they remain open. Arbitrary full-bank
donor gauges, altered capacities and new routes need separate analysis.

The deficit is not a MOVE lower bound and does not exclude every balanced
array code, discharge any foundation, or establish a new κ. The next task
is genuine cross-stripe source mixing compatible with the early-source
rank criterion and all native receivers.

Credit @CubeJerry, retained native/balanced/quotient authors, Worker A's
repeated-scalar argument, and root's stripe-varying extension and exact
partition search, with substantial OpenAI assistance.
