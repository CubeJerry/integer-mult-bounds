# One source-local rank-one export cannot serve two missing receivers

**Proved source-specific linear and block obstruction, subject to independent
review. No new kappa.** The theorem is deliberately generous about source
preparation and receiver corrections. It shows that the next shared decoder
must use interacting exports, change the existing global packet space, or
change another stated premise. Choosing a different single local payload is
insufficient in this exact rank-one destination model.

## 1. Model and quantified proposition

Use either of the pinned coupled and uncoupled two-output sources from
`results/bit-coupled-singular-delivery/worker-a/two-receiver-output/`.
The recovered 111 rational root vectors are `r_i`; the original input line
is `L_i=span_Q(r_i)` and its receiver facet is `F_i=r_i^perp` in Q^8.
Let `T_0,...,T_7` be the eight actual pure-X terminal packet rows. Grant

    G = span(T_0,...,T_7,e16,e19,e38,e49,e50,e56,e57)

globally and freely to every receiver. Both variants have dimension 15.
The coupled baseline fits roles

    {16,17,19,38,49,50,56,57,59,60};

the uncoupled baseline additionally fits already-completed role 34.
After removing completed roles 17 and 34, the same 100 receivers are missing
in both variants.

The source chart `A=N^perp` is any one of the 33 distinct *named actual raw
cache charts* supporting a `DC` or `SC` record at the handoff. Their precise
normal lists, names and source-local indices are in `CERTIFICATE.json`.
The theorem does **not** assert that all their hypothetical payloads are
already physically available. In a stronger relaxation, allow a single
whole-V payload at A to be arbitrarily reprogrammed using every original
input whose line lies in A, plus arbitrary rows from G. All such preparation
is granted free. Thus, after subtracting a G contribution, its X dependence is

    Z(x) = sum_{j:L_j subset A} Z_j x_j,

where the `Z_j` are arbitrary V-by-V matrices over an arbitrary field K of
characteristic two. The V original components and the original Y baselines
are independent. Noise from independent Y variables cannot invalidate the
X-projection argument below.

Descend this one record by one physical rank to an arbitrary rational
codimension-one subspace `B subset A`. A receiver may use this record only
if `B subset F_i`. Grant that receiver all of G and all original X inputs
local to F_i with arbitrary block coefficients. This grants more access than
an actual chronological decoder. The conclusion is:

> For every characteristic-two field K and every positive integer V,
> one such rank-one export can make at most one of the 100 missing receivers
> linearly feasible at its physical destination.

This holds for both source variants. It is not an information lower bound for
multiple interacting exports, changes of G, other source charts, wider records,
nonlinear computation, or nonlocal source acquisition. An ascending receiver
can only read the exported record at B or above it, so `B subset F_i` remains
necessary throughout that trajectory. A later further descent is an additional
operation, outside the stated one-descent inventory.

## 2. Two exact preliminary facts

Let `O_i={j : r_i dot r_j != 0}` be the coordinates nonlocal to receiver i.
For a missing receiver there is a binary dual `u_i`, supported on O_i,
annihilating G, with `(u_i)_i=1`. These are exact 0/1 identities, valid after
extension to K.

Suppose a single exported V-field makes receiver i feasible. After projecting
onto original X columns, its decoder has the form

    e_i I_V = sum_a C_a g_a + M_i Z + local_i,

where `local_i` has no coefficients on O_i. Evaluating at u_i gives

    I_V = M_i Z(u_i).

Therefore **M_i is invertible**. This is derived from a missing-receiver dual;
it is not assumed because the target is a whole field. The old G fields may
already supply part of the original block, and the same dual still proves the
required conclusion.

For the geometry, `B^perp` is a one-dimensional extension of N. If it contains
any missing receiver normal outside N, then

    B^perp = span_Q(N,r_i).

Consequently two such receiver normals are reachable at the same destination
exactly when their nonzero classes in Q^8/N are proportional. Rational row
elimination partitions all 100 missing roots into these projective groups.
A normal already in N is also considered, but a source-local field is then
already receiver-local and cannot repair a missing role.

These two facts reduce all possible rational rank-one destinations and all
block decoder coefficients to a finite pinned geometric classification.

## 3. Individual receiver classification is certified by duals

Write `J_A={j:L_j subset A}`. A local payload can help receiver i only if

    e_i belongs to G + span(e_j:j in J_A) + span(e_j:j not in O_i).

Whenever this condition fails, the certificate provides an explicit binary q
such that

    support(q) subset O_i minus J_A,
    q_i=1,    g dot q=0 for every g in G.

The hypothetical new payload also annihilates q because its support lies in
J_A. Applying q to the proposed decoder gives `I_V=0`, for every K and V.
Thus each exclusion is a universal exact linear argument, not a failed scalar
search. For each individually possible role the certificate instead gives a
literal binary payload, G combination and local remainder. Those witnesses
establish only the relaxed algebraic possibility.

For each source variant there are 1,774 nonzero projective destination groups
across the 33 source charts. In the coupled case 920 groups have no possible
missing role, 853 have one, and one has two. In the uncoupled case the counts
are 918, 855 and one. The unique two-role group is identical:

    A=D4,   possible missing roles {2,13},
    B = D4 intersect F2 = D4 intersect F13.

Here `D4` is an actual dimension-seven chart (its label is a source subset
label, not its dimension). Its normal is `(0,1,1,0,-1,0,0,1)` and B has
dimension six. The certificate enumerates every group and every individual
exclusion; no untested direction of a rank-one rational descent is omitted.

## 4. The exceptional pair is universally incompatible with one payload

For the unique D4 group, use the binary duals with supports

    q2  = {2,85,89,92,94,95},
    q13 = {2,85,89,92,100,102}.

Exact pinned-source checks give:

- q2 is supported on O2, annihilates G, and `(q2)_2=1`;
- q13 is supported on O13, annihilates G, and `(q13)_13=0`;
- their restrictions to J_D4 are identical, namely `{85,89,92}`.

If the payload is source-local modulo G, then `Z(q2)=Z(q13)=S`.
Feasibility of receiver 2 gives

    M2 S = I_V.

Feasibility of receiver 13 gives

    M13 S = 0.

But M13 is invertible by Section 2, using the separately supplied missing-role
dual

    u13 = 0x5412a000000000000000002000.

Therefore S=0, contradicting the first equation. This excludes arbitrary
noncommuting block coefficients, arbitrary positive width and every
characteristic-two field. It does not divide by a scalar guessed from a
binary test.

Every other destination group has at most one individually possible missing
role. Together with Section 3 this proves the proposition.

## 5. Two-payload positive control and the next constructive question

The exceptional pair can be served in the same algebraic relaxation by **two**
separate source-local fields, each descending one rank from D4 to B:

    z2  = x11+x15+x21+x39+x41+x49+x50+x61+x85+x88+x89+x92+x93,
    z13 = x9+x14+x20+x42+x44+x51+x62+x63+x83+x87.

The certificate provides exact local correction rows l2 and l13 satisfying

    e2  = T2 + z2  + l2,    support(l2)  subset local(F2),
    e13 = T6 + z13 + l13,   support(l13) subset local(F13).

Neither single payload supplies both roles. The terminal fields T2 and T6 are
actually present at ground; the local payload/correction acquisition has not
been emitted here. This is a concrete positive control for the *relaxed
two-field interface*, not a new physical decoder. The two descents alone cost
2 movement units at t=199/200; source preparation, correction collection,
receiver fragmentation, owners and erasure are still obligations.

The next constructive task is to make several exports cooperate: two fields
can be combined with different coefficients at different receivers, a mechanism
that the one-field theorem does not constrain. Another possible escape is to
recouple the initial source so that its true terminal G changes. Neither a
favorable number of globally fitted rows nor this local gate decides the
complete 9.243842594... movement allowance.

## 6. Reproduction, verification scope and credit

Run:

```sh
python3 -B check.py --repo /absolute/path/to/integer-mult-bounds --out /tmp/single-export-check
```

The checker authenticates both complete source-word byte strings and native
root recovery, reconstructs all 222 formal original input columns, verifies
actual owner values and source restoration, classifies all projective groups
with exact rational elimination, and emits every individual dual and candidate
payload. It imports no source verifier. The predecessor's full physical source
admission remains a dependency: the reconstruction here does not claim to
repeat its complete rational MOVE audit or native gzip recovery.

Four independently meaningful rejecting controls per source variant remove
the target dual coordinate, remove the invertibility dual, break the equality
of local restrictions, and silently add receiver 2 to G. The two-field
positive control prevents the obstruction from being silently generalized to
multiple payloads. Independent review should reconstruct the source-local
mask and projective partition with a different elimination implementation,
and inspect the block invertibility step above.

Source pins are in RESULT.json and CERTIFICATE.json. The native geometry
recovery and S014 coupled/uncoupled source, static continuation and shared
reservoir authors retain their credit. The new theorem is the rank-one
destination classification under arbitrary local reprogramming and its exact
exceptional block obstruction. @CubeJerry; OpenAI-assisted S015 Worker C
research. No supplier, foundation discharge, selected-certificate change or
new complete kappa is claimed.
