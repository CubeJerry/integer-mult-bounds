# Endpoint-determined histories exclude arbitrary local feedback

**Draft general proposition; no source instance is asserted here.**

Let a finite, fixed, typed linear word act on independent common public inputs
u over a field F. Fix a set of permitted intervention slots. Each slot consists
of a source event boundary and a live common role at its actual chart. Native
MOVE destinations, event order, INIT/CLEAR lifetimes and receiver observation
slots are fixed. Additional local memory and arbitrary computation may choose
interventions, but the receiver sees no additional information-bearing channel.

Index the slots by j=1,...,m. Give each an arbitrary vector-valued additive
increment w_j in F^V. For a fixed execution these increments may depend on u,
independent raw donor data q, previous common states, and local retained data.
They need not be linear, independent, or chosen in advance. Collect their
actual realized values into w. Linear superposition in the unchanged native
word gives the exact identities

    constrained common endpoints = A0 u + (A tensor I_V) w,
    complete receiver history     = F0 u + (B tensor I_V) w.

The first expression can include required zero guards as extra rows. Row
dimensions and units must be fixed consistently. The usual source response
matrices A and B are computed with formal independent increments; the same
identities hold after substituting the actual, possibly nonlinear and
feedback-dependent increments w(u,q). This is an algebraic substitution,
not an assertion of independent control availability.

## Proposition

If there is a scalar matrix L with B=L A, any permitted execution preserving
every constrained common endpoint and guard has receiver history exactly F0 u.
Consequently, if receiver side information is independent of a raw donor q_x,
no such execution can recover q_x for every u and q_x. This conclusion allows
arbitrary nonlinear decoding and arbitrary local feedback at the admitted
intervention slots.

### Proof

Preservation implies (A tensor I_V)w(u,q)=0. Therefore
(B tensor I_V)w=(L tensor I_V)(A tensor I_V)w=0. Fix u and every independently
supplied receiver-side input, and vary q_x. The receiver sees the same complete
record and side information for every q_x, so it cannot output q_x on all
inputs. The argument is coordinatewise for every positive V; it does not
assume interventions operate coordinatewise.

## Quotient certificate sufficient for a complete history factorization

Suppose the receiver history has observation matrix F0. Let d_1,...,d_s be
history coefficient rows whose baseline rows d_i F0 span row(F0), and let
z_1,...,z_t span the complete left nullspace of F0. If each d_i B factors
through A and each z_j B factors through A, then B factors through A.
Indeed every unit observation row e_k has a representation
e_k=sum_i a_i d_i+sum_j b_j z_j, obtained first by expressing e_k F0 and then
expressing the resulting zero-baseline relation. Substitute all dual
factorizations. No assumption that a zero-baseline relation is automatically
response-stable is permitted; its complete response certificate is required.

It is enough to split the d_i into already certified stable baseline
directions and a complementary history quotient. For pre-control observations
d_i B=0. For final receiver observations among the constrained endpoints,
d_i B is a literal row of A. A quotient basis plus the complete left-null
relations therefore gives a short certificate when those earlier facts have
been source-authenticated.

## Modeling limits

- A local replacement of an original scalar operation can be represented as
  its original operation followed by the actual difference in the written
  field, provided that difference occurs at an admitted slot and all native
  typing/preconditions remain valid. Merely renaming a changed operation as a
  control does not authorize a new chart or a new transport.
- Added private local records can help choose w but cannot be read by the
  receiver unless their access is part of the stated observation interface.
- A new MOVE, a changed receiver observation chart, changed processing at an
  unadmitted chart, an altered public endpoint contract or an extra correlated
  receiver-side input changes the matrices and requires a new proof.
- Free interventions constitute an overgrant. Their impossibility would apply
  to every paid implementation within the overgrant; no cost theorem is
  inferred outside it.
- This is a finite-word interface theorem. It is not a lower bound for integer
  multiplication, a native construction, or a new exponent saving.

## Source application pending

S005 is testing whether the pinned 71,261-event native admits these dual
factorizations for receiver189, first at the donor77 suffix after event29530,
then on the full five donor charts. The broader220-chart station overgrant
has nonzero gains in an exploratory computation and is not excluded.
Exact source rows, endpoint/guard matrices, complete history basis, nine
left-null relations, all-time slot coverage and independent verification
must accompany any source claim.

Prepared for @CubeJerry's persistent moonshot programme with substantial
OpenAI assistance. Standard linear superposition and factorization are used;
the possible contribution is their source-bound control/access application.
