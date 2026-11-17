# A joint row-support capacity test for independent Gaussian endpoints

**Universal necessary endpoint condition, with an exact exclusion of one
changed Klein column. This is not a new supplier or a universal exclusion
of three-bank callers.**

## 1. Fixed-catalogue hypothesis and actual endpoint images

Work at sufficiently large faithful widths divisible by four, with the
literal four-bit source a=A^(tensor V). Ordinary coefficients, their actual
inverses, and endpoint coefficients lie in one fixed finite catalogue of
root-four monomial tensor powers. Coefficient sums are formed after lifting.
Let B=C[G], where G is the finite projective root-four monomial group on the
sixteen one-column basis states. Any smaller fixed catalogue embeds in B.
The exterior coefficients may depend on V; the catalogue itself does not.

Assume an actual independent endpoint factorization

    E=O diag(F4,F2,F1) Iin,

where O and Iin are ordinary three-bank units, with actual ordinary inverses.
Write c4,c2,c1 for the three encoder columns of O. Each im(cj) is a split
free B-module of rank one; their sum is direct. This is the endpoint
hypothesis, not a conclusion from component ranks.

Let pi select a set of output banks, and suppose pi c4=0. For any selected
input column, expand each Gaussian-r component, r=1,2, in distinct left
ordinary cosets:

    E_r[:,j]=sum_k M_r[:,k] w_rk,   M_r in Mat_(3 x k_r)(B).

Let S_r=im(M_r). Source-word separation shows S_r is contained in im(cr):
expanding F_r Iin[r,j] by the same left cosets factors every ordinary
coefficient column through cr. Enlarging the fixed finite word catalogue
and taking a faithful width justifies coefficient comparison. Analytical
class or coset projection is used only in this proof, never as an executable
operation.

For any finite-dimensional representation rho of the full ordinary group,
put d=dim(rho), and apply rho to all ordinary block coefficients. Then

    dim(S_1 intersect ker(pi)) + dim(S_2 intersect ker(pi))
       + d <= dim(ker(pi)).                              (1)

Indeed these two intersections and im(rho(c4)) are mutually disjoint,
because the full encoder O is invertible, and all three lie in ker(pi).
In the three-bank case with pi the third coordinate, dim ker(pi)=2d, so

    [rank M_1-rank(pi M_1)]
      +[rank M_2-rank(pi M_2)] <= d.                     (2)

This is a joint endpoint condition. The two weaker tests rank(M_r)<=d can
both hold while (2) fails. Direct sums of representations and multiple
selected input columns are allowed. The same argument applies to any
number of banks and any set of already-full endpoint images inside a
prescribed output subspace.

For the native word E=L C U_native Q L, Gaussian-four terms always vanish
in the third output row: that row has at most three source factors on every
literal path, including the square in U_native. Ordinary coefficients do
not turn such a fixed word into Gaussian rank four. Since the actual
quartic input row F4 Iin[4,:] is surjective, E4[2,:]=0 implies pi c4=0.
Thus (2) applies to every proposed independent (4,2,1) caller for this
native word, without choosing its endpoint basis in advance.

## 2. The changed Klein interface and the tested last column

Use s=SWAP_cd, t=X_c X_d, P_x=(I+x)/2, N_x=(I-x)/2. Retain the ordinary
Klein unit, but exchange its last two output banks:

    Calt=[[P_s,-E,-F],
          [P_st,0,I-F],
          [P_t,I-E,0]],
    E=N_s P_t, F=N_s N_t.

This is an actual ordinary unit, since the original Klein completion is
one and a bank exchange is invertible. Consider every ordinary Q whose
last column is

    (p,z,w)=(N_t,0,P_t).                                (3)

There is no failure of column completion: the controlled exchange on
banks0,2,

    Q0=[[P_t,0,N_t],[0,I,0],[N_t,0,P_t]],

is an actual unit, equals its inverse, and has this column. The other
columns of Q in the theorem are arbitrary. This family is outside the
previous original-Klein transferred-column premise.

Put U=a^2 and s1=a^-1 s a. Define the literal ordinary involutions

    h0=a t a^-1,
    h1=U t U^-1,
    h2=U s1 t s1 U^-1,
    P0=(I+h0)/2, Mj=(I-hj)/2.

The phase-sensitive one-column conjugates h0,h1,h2 are all ordinary.
The two representatives U and U s1 belong to distinct left ordinary
cosets, because U s1 U^-1 is nonordinary of Gaussian rank two.

Direct multiplication gives the complete class-one and class-two last
column, with no other Gaussian classes:

    E1[:,2] = c a,
    c=(0, P_s M0+P0, P_t M0)^T,                        (4)

    E2[:,2] = (1/2) d0 U+(1/2) d1 U s1,
    d0=(M1,M1,0)^T,
    d1=(M2,h0 M2,0)^T.                                (5)

These are collective word identities. They use t commuting with s,
U t1 U^-1=h0, and the literal ordinary conjugates above. In particular,
the two cosets in (5) cannot be combined merely because a one-width
numerical matrix happens to have smaller rank.

## 3. An exact fifteen-dimensional witness

Use the standard permutation representation of G: discard each monomial's
phases, act on the sixteen coordinate labels, and restrict to the
sum-zero subspace with basis e_j-e_15, 0<=j<15. This is a representation of
the full ordinary group, so enlarging the endpoint catalogue cannot evade
it. It is not the physical sixteen-dimensional source representation.

Exact rational row reduction gives

| Ordinary coefficient module | Whole rank | Third-row rank | Kernel of third row |
|---|---:|---:|---:|
| M1=c from (4) | 15 | 4 | 11 |
| M2=[d0 d1] from (5) | 13 | 0 | 13 |

The necessary inequality (2) would require 11+13<=15. Its actual left side
is24. Therefore no completion retaining (3) has actual independent
(4,2,1) endpoints in the fixed finite ordinary catalogue model. Right
basis changes of this last column are also covered, because an ordinary
unit acting only on input3 commutes with the final L and can be absorbed
by the ordinary input endpoint.

The individual inequalities 15<=15 and13<=15 pass. This is why testing only
one component at a time did not reveal the obstruction.

## 4. Exact checking and scope

The checker reconstructs the literal source and all phase-sensitive tables
from the pinned Gaussian-dyadic engine, verifies the conjugacy and coset
facts, checks the two collective identities by their literal factors, and
reconstructs the fifteen-dimensional representation independently of the
exploratory module code. All four ranks are computed over the rationals,
not inferred from modular sampling. The controlled-exchange completion
and its inverse are checked on every bank input. Negative controls detect
an omitted coefficient term and an altered endpoint-support premise.

The argument excludes this entire fixed-last-column family, not all Calt
columns. In particular, it makes the nonzero z channel materially relevant:
its class-two contribution can occupy the third output bank and change
the left side of (2). The Z_c Z_d spectator changes the transported
involution algebra and is a separate construction. No conclusion about
its complete caller is claimed here.

## Open next question

Construct a column with nonzero z and w that satisfies the joint condition,
then give the remaining ordinary Q and endpoint units with all source
classes canceled and every input retained. Passing (2) is necessary and
is not an endpoint construction.

Credit @CubeJerry, the retained literal source and native contract, the
Klein completion, C's ordinary-capacity analysis, and substantial OpenAI
assistance. This package supplies no new kappa or foundational discharge.
