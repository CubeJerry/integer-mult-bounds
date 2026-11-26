# Independent audit of nested Fourier source reuse

**Verdict: pass for NR1–NR7 and their local compiler interface.** This
review concerns the frozen source-only construction. Any later destination
accumulation extension is a separate gate. The unchanged destination
bill and unchanged complete asymptotic envelope are correctly retained.

## Geometry and common frequency slots

The projection pi_v(z)=z+<d_v,z>d_v is essential. For a label u differing
from v in one coordinate, <d_v,d_u>=0, so projecting the affine
difference d_u+d_v gives d_u. Its unprojected form is not auxiliary.
The proper-product rank lemma makes the affine differences independent,
and projection is injective on their span: every such difference has
self-pairing zero, whereas d_v has self-pairing one. Thus the projected
generators in NR2 are independent across coordinate flags as claimed.

Their spans give span(I)=<d_v> direct-sum W(s). A basis adapted to all
nested W_i(s) exists because the largest flag spaces form a direct sum.
The flags need not be orthogonal or nondegenerate. In the full Fourier
frequency coordinates, W(s) is the annihilator of H=span(I)^perp inside
the nondegenerate auxiliary space. Using a frequency basis adapted to
W(s) and its paired ordinary basis, inverse transforms in precisely those
slots recover the desired H-partial transform.

This supplies one compatible coordinate system for every requested state.
Previously inverted slots stay ordinary while the other slots stay in
frequency coordinates; inverse transforms on distinct slots commute.
The rectangle-dependent final conversion to common representatives remains
in the paid middle maps. Initial auxiliary phases precede preconditioning,
and query-dependent phases stay in their original middle terms.

## Tree and invoice

A positive state coordinate forces an unequal position. Since L is even,
all-positive states cannot occur in the odd-distance partition. Any state
with a zero occurs, because that zero may be declared equal or unequal
at level zero to select the required parity. This proves the state set Q.

Decrementing a smallest positive coordinate preserves Q and decreases its
coordinate sum, giving a rooted tree. The added flag dimension is exactly
2^(s_i-1). Copying the cached parent before this inverse transform is
necessary and sufficient. Each resulting array equals the separate
direct partial transform by induction on the tree.

The second difference in NR6 counts states with a zero and smallest
positive entry ell: include coordinates from {0,ell,...,t-1}, exclude
the cases with no zero or no ell, and add back their intersection.
Every state occurs in the original incidence list, so charging its
incoming edge by at most its full rank proves S<=A. Consequently NR7
lies between half and all of the previous preconditioned bill. The
finite 306-to-230 example and unchanged logarithmic scale follow.

## Physical and numerical interface

There are at most lambda cached states and lambda incidence copies per
source. This is an absolute-factor enlargement of the already admitted
incidence storage. Tree routing, complete-row copies, common-basis maps
and distribution remain charged polynomial ordinary operations. They
are not extra free axis calls or word-RAM accesses. Every expensive
edge operation is an existing normalized f-bit axis child.

An error introduced at any cache node reaches at most lambda descendants
through unitary branch maps. Its combined copying norm is therefore at
most sqrt(lambda), before the existing row/distribution factors. This
gives the stated polynomial numerical gain and precision enlargement,
without multiplying an unnecessarily coarse fan-out estimate separately
at each depth. No per-bit metadata or altered common-root assumption is
needed. The result is a local call-list replacement inside the admitted
compiler, not a new standalone global visited-space theorem.

## Isolated replay

The copy in `replay-nested-fourier-source/` passes all 15,618 direct
transform entries, 39 projected-side ranks, 20 degenerate flag spaces,
4,368 states, 10,320 incidences and 300 invoice profiles. It rejects
15,401 wrong-dual entries, 9,226 mutated-parent entries and 16 unprojected
affine differences. The dimension-13 case checks 32 deterministic
positions per state; lower dimensions check every output, as the draft
explicitly reports. These are exact finite controls, not a tape simulation.
