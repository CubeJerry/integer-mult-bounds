# Reusing nested source transforms in the canonical Fourier rectangles

Status: **proved local execution draft; independent review requested**.
This continues the admitted endpoint-preconditioning component. It saves
additional source-axis calls by an actual copying computation graph. The
destination endpoint bill remains explicit, and the complete multiplication
envelope is unchanged.

The independently concurrent E003 `lead/rank-weighted-walsh-invoice.md`
derives the same earlier span-weighted formula. The present note concerns
additional reuse between different rectangles after preconditioning. It
does not claim priority for the earlier formula or use E003's separate
executor gate as a proved premise.

## 1. The auxiliary subspaces really form compatible flags

Use the binary label geometry with q=2^t, even L>=2, N=q^L and
D=2+L(q-2). Fix a source label v. Its direction d_v has self-pairing one,
so the auxiliary space A_v=d_v^perp is nondegenerate of dimension D-1.
The orthogonal projection onto it is

    pi_v(z)=z+<d_v,z>d_v.                                 (NR1)

For a first-difference side containing v, coordinate i is either the
singleton {v_i}, or the binary prefix block B_i(s) containing v_i with
size 2^s, where 0<=s<=t-1. The blocks B_i(s) are nested. Let

    W_i(s)=span{d_(v with coordinate i changed to a):
                 a in B_i(s), a!=v_i}.                    (NR2)

Every generator is orthogonal to d_v, since it differs from v in exactly
one coordinate. Their number is 2^s-1. The exact proper-product-side rank
lemma EP4 proves that these generators, over all coordinates, are linearly
independent. Therefore W_i(0)=0, the W_i(s) form nested flags, and sums
across the i are direct.

If I is the source side corresponding to the state s=(s_1,...,s_L), then

    span(I)=<d_v> direct-sum W(s),
    W(s)=direct-sum_i W_i(s_i),
    dim W(s)=sum_i(2^s_i-1).                              (NR3)

For clarity, the vectors d_u+d_v are not in general auxiliary vectors.
For a one-coordinate change they have pairing one with d_v. Projection
NR1, which yields d_u in that case, is essential. The claim does not
assume that the flags are mutually orthogonal or nondegenerate.

Choose one basis B_v of A_v adapted to every W_i(s). This is possible
because the flags' largest subspaces are independent. List the increments
of each flag in order and extend to a basis by binary elimination. This
single basis depends on v, but neither on the rectangle nor on query j.
Use its paired dual where ordinary coordinates require it.

For the preconditioning choice H=span(I)^perp, the complement of H inside
A_v is dual to W(s). Thus a full auxiliary Fourier transform, expressed
in the fixed frequency basis B_v, followed by inverse transforms in the
coordinate slots belonging to W(s), supplies the source partial transform.
All states now use compatible coordinate slots. No new coordinate change
is needed between two states. The rectangle's final ordinary middle maps
still convert its resulting mixed coordinates to the common representative.

## 2. Which states must be generated

Each unequal coordinate chooses one of the t first-difference levels.
An equal coordinate and an unequal coordinate of level zero both have
the singleton source side and therefore contribute state coordinate zero.
Only odd sets of unequal coordinates occur. Since L is even, a state
with every coordinate positive is impossible; every state with at least
one zero is possible, by choosing the parity among its zero coordinates.

The distinct source states are consequently the downwards-closed set

    Q={0,...,t-1}^L \ {1,...,t-1}^L,
    |Q|=t^L-(t-1)^L.                                    (NR4)

The all-zero state is already available as the fully preconditioned array.
Several rectangles may use the same state; they receive copies of that
one computed array. The number of distinct states does not exceed the
source's original incidence load

    lambda(t)=sum_(k odd) binom(L,k)t^k.

## 3. An explicit transform tree

For every nonzero state s in Q, select a coordinate having the smallest
positive s_i, breaking ties by index, and define p(s)=s-e_i. The parent
lies in Q, and the sum of coordinates decreases. These edges therefore
form a rooted tree spanning all requested states.

To compute state s, copy the cached parent array and inverse-transform
only the newly added flag slots. Their number is

    dim W_i(s_i)-dim W_i(s_i-1)=2^(s_i-1).                 (NR5)

All inverse coordinate transforms commute because they act on fixed
distinct slots. Induction on the tree proves that the cached array at s
is exactly the same as separately inverse-transforming all of W(s) from
the fully preconditioned input. The copies are necessary: mutating the
only parent array would destroy inputs for its other children.

Write S(L,t) for the resulting axis bill per half. Counting states by
their smallest positive coordinate gives the exact finite formula

    S(L,t)=sum_(ell=1)^(t-1) 2^(ell-1)
       [(t-ell+1)^L-2(t-ell)^L+(t-ell-1)^L].              (NR6)

The second difference counts states with at least one zero and minimum
positive entry exactly ell. At t=1 the sum is zero. An equivalent formula
is obtained by choosing the number k in {1,...,L-1} of positive entries
and summing binom(L,k)[(t-ell)^k-(t-ell-1)^k].

This count refers to the specified copying tree. No optimality over
general linear circuits, shared bases or other rectangle partitions is
claimed. In particular it is not a lower bound on the actual algorithm.

## 4. The revised complete free-endpoint invoice

Put A=(q-1-t)lambda'(t). The previous independently performed source
inverse transforms cost A axes per half; the unchanged destination
transforms cost lambda+A. The new source computation costs S(L,t).
Including the once-per-label full preconditioning gives

    F_nested=2(D-1)+2S(L,t)+2lambda+2A.                    (NR7)

The earlier admitted bill was 2(D-1)+2lambda+4A. The saving is exactly
2[A-S(L,t)], which is nonnegative: each nonroot state is charged at most
its full rank, and it occurs at least once in the original incidence sum.

For q=4,L=4, D=10, lambda=40, A=52 and S=14. The new free call invoice
is 230, compared with 306 after independent endpoint preconditioning and
800 in the original literal endpoint count. For q=8,L=4 it is 1,342,
compared with 2,082 and 6,240 respectively. These are exact axis counts,
not measured full-machine runtimes.

The new source sum satisfies S(L,t)<=2^t(C L)^L for an absolute C.
Indeed write u=t-ell in NR6, bound its second difference by (u+1)^L,
and sum 2^(-u)(u+1)^L. A geometric-exponential moment bound gives the
stated estimate. For fixed L>=4 and growing t, this reduces the source
component from order_L(2^t t^(L-2)) to O_L(2^t).

The destination term A is still present in NR7. In fact NR7 lies between
one half of and the whole earlier preconditioned bill. Thus its logarithmic
local scale and the admitted complete asymptotic envelope do not change.
This conclusion is explicit; source reuse is not silently attributed to
destination arrays carrying different independent rectangle contributions.

## 5. Copies, tape layout, precision and common parameters

One common basis is computed per label in polynomial local-arity work.
The fully preconditioned source array is reindexed into it once. Each
tree edge copies a complete source row and applies the specified ordinary
normalized Fourier children in its existing f-bit coordinate slots.
The same construction is used on both auxiliary halves. The initial
auxiliary phase remains before preconditioning, as in EP9, and every
query-dependent phase remains in its original middle map.

All cached arrays can be stored in the same source-incidence row format.
There are at most lambda cached states and lambda incidence copies per
source, an absolute-factor enlargement of the admitted O((1+lambda)V)
local storage envelope. Metadata consist of polynomial-size preflight
lists; no O(log m) tag is appended to every data bit. Within one row block,
the parent and child are brought together by the existing charged row
routing/copy supplier. Each complete copy or leaf distribution is charged
to polynomial ordinary work, not omitted as an address-word operation.
Since the parameters and lists are polynomial in local arity, this does
not change that supplier's fixed polynomial exponent type.

Every additional expensive operation is one of the original normalized
axis children. A child result may be copied for several uses, but the
linear duplication map's norm is at most the square root of the number
of copies. Its logarithmic growth is O(log lambda), already polynomially
bounded in the template size. The existing path/event-count precision
guard can be enlarged by this explicit duplication count. No unchecked
commutation of a diagonal phase through a Fourier transform occurs.

The tree is a finite local template. The common root field, divisor
alignment, variable-arity scheduling and all-visited outer cap continue
to be supplied by the admitted compiler; this note does not independently
prove a new global machine. It changes a concrete local call list while
retaining all original ordinary maps and copies with their charges.

## 6. Exact finite controls

`verify_nested_fourier_source_reuse.py` reconstructs the actual binary Gram
row quotient and its source auxiliary projection. It verifies 39 exact
product-side projections/ranks, including 20 degenerate requested flag
spaces. It then compares 15,618 exact output entries from the copying tree
against direct partial-transform sums. Negative controls reject 15,401
entries with a wrong dual-basis change, 9,226 entries after mutating a
shared parent, and 16 unprojected affine-difference directions.

The independent combinatorial enumeration covers 12 families, 4,368
distinct states and 10,320 original source incidences. All exact edge sums
match NR6. A further 300 integer parameter profiles verify the revised
invoice inequalities. At auxiliary dimension 13 the transform check uses
32 deterministic output positions per state; dimensions at most nine
are checked at every output position. All arithmetic is exact. The JSON
receipt is `nested-fourier-source-verification.json`; no full tape
simulation or formal verification is claimed.

## 7. Next unresolved reuse interface

At a fixed destination the source sides encountered across first-difference
levels are sibling blocks rather than nested blocks. Their incoming data
also differ by rectangle. A valid improvement there would require an
adjoint accumulation graph with compatible endpoint coordinates and
phases, or a different geometry. The present source tree alone does not
give that graph. E002's common Weyl-star basis does not automatically
apply to these rectangle-dependent middle maps either.

Credits: the pinned OpenAI endpoint kernel and proper-product geometry;
S004 endpoint preconditioning and the lead's request to investigate nested
reuse; concurrent E003 rank-weighted calculation; E002 physical suppliers;
@CubeJerry; substantial ChatGPT assistance.
