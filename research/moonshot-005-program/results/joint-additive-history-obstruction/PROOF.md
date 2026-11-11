# A complete receiver-history obstruction to joint additive controls at 220 charts

**Exact source certificate and algebraic reduction; independent review pending. No new κ.**

This packet extends the unsuccessful single-cut searches to arbitrary
joint additive controls, for one binding source pair. It does not exclude
replacement encodings whose control fields contain arbitrary common data.

## Precise interface

Use the native word with compressed SHA256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Let C be the 220 canonical chart spaces explicitly listed in the
certificate, inherited from the independently reviewed static-history
cut. Grant the independent raw difference field q77 at every chart in C
at every time, without transport, storage or ordinary cost. This is a
large relaxation of the physical programme.

Permit an arbitrary finite collection of additive controls into any live
common field at any native cut whose chart lies in C. Each added value
may be an arbitrary linear map of q77. Controls may be chosen jointly
across different cuts; no individual-neutrality condition is imposed.
The common operations outside these additions remain the original native
word. In particular, setting q77=0 recovers its original common execution
on all 1,480 arbitrary common inputs u.

Grant the raw receiver189 access to every common field initially located
on its original itinerary and every common field arriving by a native
MOVE at any chart on that itinerary, at every source time. Grant all
historical caches and arbitrary combinations of these observations.
The receiver's own raw difference and other independent differences may
be retained as side information; they can be fixed to zero when testing
the required dependence on q77. The receiver itinerary is disjoint from C.

**Within this interface, no receiver decoder can recover q77 for all
arbitrary u and q77.** This remains true without requiring the controls
to restore any final common endpoint. Consequently imposing terminal
neutrality, COPY guards or the physical budget cannot help.

The source endpoint189 contains q77 with coefficient one. Thus this
specific required contribution cannot be supplied by this additive
station-control/receiver-history interface.

## Complete observation space

There are exactly 1,065 registered receiver observations. Let O be their
coefficient matrix on the 1,480 common inputs. Exact source execution
gives rank(O)=1,056. The certificate supplies nine linearly independent
relations among the observations, with term counts

    3, 40, 12, 3, 3, 3, 42, 2, 45.

Each relation is zero on every common input. Their independence and the
rank deficit show that they form the entire left nullspace of O.

Initial values and MOVE arrivals span every available common history at
a receiver chart: intervening native ADD, COPY and SCALE operations are
linear combinations of fields already there; INIT contributes zero and
CLEAR removes a field. There is no controller at a receiver chart,
because the receiver itinerary and C are disjoint. Thus even granting
all intermediate local reads cannot enlarge this observation space beyond
the registered observations.

## Every relation is insensitive to every permitted control

For each of the nine timed history relations, propagate its adjoint
backwards through the native. Insert the specified observation weights
at their actual event cuts and field versions. The exact certificate has
the following property:

> At every native time, the adjoint on every live common field whose
> chart lies in C is zero.

Therefore adding any field value at any permitted station/time changes
none of the nine history relations. The controls may cancel jointly,
interact in time, or mix all V coordinates of a field; a zero scalar
adjoint remains zero after tensoring with the V-dimensional identity.

`verify.py` checks this exhaustive statement directly, without importing
the exploratory control-space search. Backwards, an ADD changes only
the adjoint at its source, SCALE changes its destination, COPY changes
its source and destination, MOVE changes one role's location, and
INIT/CLEAR change its lifetime. It checks every changed coefficient or
location, maintaining the all-stations-zero invariant at every cut.
Observation impulses occur outside C. Finally the initial observation
weights cancel the remaining input adjoints, independently confirming
the baseline identity.

The source COPY-zero guard is unnecessary for these nine annihilation
identities: they remain valid even in the more permissive linear
overwrite semantics. No claim is made that violating a real COPY guard
would be physically admissible.

## Indistinguishability argument

For any chosen linear additive control code, write the actual observation
vector as

\[
Ou+Bq_{77}.
\]

All nine left-null relations of O annihilate B. Hence
`im B ⊆ im O`. For any q77 there is a common input displacement v such
that `Ov=Bq77`. The receiver observations for `(u=0,q77)` are then identical
to those for `(u=v,q77=0)`. Both are permitted inputs, because the common
inputs are arbitrary and independent of the raw differences.

Thus no decoder using only this observation/access interface can recover
q77 on all inputs. This conclusion is not restricted to a linear decoder;
the two complete observation records coincide. It applies to every
admitted field volume V by the same tensor argument.

The unchanged q=0 baseline is essential. In a replacement or difference-
carrier encoding, a control such as `q−h(u)` can be nonzero even when q=0.
It changes the common-input observation map and is not excluded by this
argument. The separate103-pulse dual packet treats a different restricted
repair family. Neither numerical obstruction is added to the other.

## Controls, limitations and next obligation

Changing a displayed relation coefficient breaks its zero-baseline
identity. Granting a q77 controller at empty chart3 breaks station
insensitivity. The latter is an actual source-access/transport change:
chart3 is absent from C and is on the receiver itinerary.

The result leaves open extra common-input-dependent encodings, active
recoding of common fields outside C, extra decoder observation charts,
information delivered through repurposed owned routes, and a new native
geometry. The strongest remaining question is how to enlarge the
receiver's information or change the outside common processing while
preserving every arbitrary common input and the complete tariff.

This is a finite, exact source certificate supporting a statement for all
inputs and field volumes under its stated model. It is not an asymptotic
lower bound on multiplication. The package has not yet received an
independent mathematical/source review. Credit: @CubeJerry's persistent
programme, the native and static-cut authors, S004 joint-modulation
discussion, and construction-worker exact adjoint analysis. OpenAI
assistance disclosed.
