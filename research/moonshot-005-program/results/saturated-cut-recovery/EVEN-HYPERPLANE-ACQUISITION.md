# Acquisition cost at the universal even-hyperplane exit

## Proposition and scope

Keep the exact source model and the upward region D of
`E8-SATURATED-CUT.md`. Retain the native common MOVE endpoint multiset, the
eight original E8 hub-to-zero packet legs, and the 400 raw endpoint pairs.
Raw paths may be changed arbitrarily but must remain monotone. All other
MOVEs are additional, newly charged calls. Initial owned fields are zero;
the normalized cochart field operations are linear, and all private and
common endpoint obligations are retained.

Let E be the even-parity hyperplane. Let h be the number of additional
MOVEs entering D whose source chart is **not** E. Let e be the number of
additional E-to-hub MOVEs, and let g be the number of additional MOVEs
entering E from a chart outside D. All counts are whole-field counts; for
volume V, information dimensions and capacities scale by V.

Then every complete implementation in this interface satisfies

\[
e\ge(8-h)_+,\qquad g\ge(8-h)_+.
\]

Consequently its newly charged MOVE moment, at any exponent t>0 for which
positive integer rank costs at least one, is at least

\[
h+2(8-h)_+.
\]

In particular, if all additional inward information is routed through the
universal E-to-hub edge, at least eight fields must first be acquired at E
and at least eight must then leave E. **This architecture needs at least
16 added moment units, not eight.** This is a scoped acquisition bound;
it is not a general 16-field lower bound for arbitrary new routes.

## Source availability premise

The fresh exact source audit establishes:

1. E is absent from the complete native chart list. No original public
   input, native owned lifetime, or retained native MOVE endpoint is at E.
2. A line-origin raw field begins at an odd active line, which is not
   contained in E. It cannot ascend to E.
3. A zero-origin raw field ends at an actual first-Y or second-Y facet.
   Every such facet has dimension eight and differs from E. A monotone
   path through E therefore cannot reach its prescribed endpoint.
4. The retained E8 packet legs go directly from the hub to zero. They do
   not visit E.

Thus no retained field carries information into E or starts there. New
stationary INIT fields at E are zero. Every nonzero current observation
at E must descend causally from newly charged ingress into E. The proof
uses field-level access at the declared chart endpoints; access to
unrecorded microstates of a transform is a different interface.

The actual selected receiver facets provide a useful scope control: each
can have its own first-Y and second-Y raw field. The no-holder premise is
specific to E, not a statement about every dimension-eight chart.

## Proof with arbitrary feedback and mixed payloads

Condition on all original inputs whose initial charts lie inside D. Let F
be the complete retained inward transcript: the 1,255 common entries and
368 forced monotone raw entries. It contains at most 1,623V scalar
dimensions. The desired inside outputs have conditional rank 1,631V.
The transcript of the h other new inward calls contributes at most hV,
and the e new E-to-hub calls contribute at most eV. The ordinary cut bound
therefore gives

\[
1631V\le(1623+h+e)V,
\]

which proves e>=8-h when h<8.

For the acquisition inequality, grant the inside decoder **all** values in
F, all h other new inward values, and all g new values entering E from
outside D. Denote these lists by F,H,G. Every extra ingress into E from
inside D is feedback from the inside computation. Starting with zero
information at E and conditioned known inputs inside D, induction through
the actual chronological instruction sequence proves:

- Every inside field and every inside-to-E feedback message lies in the
  span of the known inside inputs and the already realized F,H,G values.
- Every E field and every E-to-hub message lies in that same span.

An outside-to-E arrival is precisely a G event and may enlarge the span by
at most V. A retained inward arrival is an F event; another new inward
arrival is an H event. Local arithmetic and erasure do not enlarge the
span. Inside feedback has no independent source beyond that span. These
facts remain valid when F or H values themselves depend on earlier
E-to-hub values: the induction is causal and does not assume statistical
or algebraic independence of whole transcripts.

Hence the entire final inside observation space lies in the span of the
conditioned inputs and F,H,G. It follows that

\[
1631V\le(1623+h+g)V,
\]

so g>=8-h when h<8. Each G call and each E-to-hub call is distinct: the
former terminates outside D at E, while the latter enters D. Both classes
are disjoint from H. All have positive rank. This proves the stated
moment floor.

Since E has dimension eight and the hub is the only strictly larger
ambient subspace, every legal nested E-to-inside MOVE is its rank-one
hub exit. An outside-D chart sending into E must be a proper subspace of
E, so its acquisition MOVE has positive rank as well.

## Limits and constructive implication

Eight extra rank-one calls from the eight actual selected second-Y facets
to the hub would have h=8 and e=g=0. They fill this cut's capacity deficit
and satisfy the lower bound of eight; this does not complete all source
duties. Thus the argument cannot be promoted to an unrestricted 16-call
obstruction. Other acquisition charts can avoid the E-specific doubling.

Likewise, supplying independent data initially at E, routing retained
common fields through E, replacing the E8 packet geometry, permitting raw
descents, or granting uncharged transported records changes an explicit
premise. Such changes must be priced and analysed directly.

The recovered cut dual's universal cheap edge remains a mathematically
valid normalization constraint. The present result prices its previously
unfunded acquisition in one concrete implementation class. It admits
arbitrary coded and mixed common/private payloads and causal feedback; it
does not require each packet to be a pure Gram mode. The pure-mode
acquisition/distribution obstruction is a different, stronger bound under
different restrictions.

The optimistic E8 source allowance is approximately 47.0797427, so even
this 16-unit gate does not exclude the target. A construction using E must
provide its incoming innovations and include both transport legs, or must
change the interface with a justified source of useful records. No
supplier, full source map, foundational assumption, or new kappa follows.

The source availability facts and recovered rank/capacity data are
reproducible with `e8_saturated_cut.py`. The proposition above is the
mathematical causal-span proof, rather than an inference from a finite
search. Prepared by the adversarial worker with OpenAI assistance for
@CubeJerry; credit the recovered odd-eight cut and its independent review.
