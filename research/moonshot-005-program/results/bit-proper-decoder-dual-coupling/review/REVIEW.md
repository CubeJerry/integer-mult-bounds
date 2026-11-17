# Independent review: proper decoder directions force seven full-span duals

**PASS for the sharp lower bound and its block extension when b=1.** The
independent certificate enumerates all2,300 triples, proves the lower bound
without enumerating nine-subsets, and verifies the displayed tight basis and
its dual. The author's detailed two-million-subset histogram is provenance;
it is not a dependency of this review or independently certified here.

## Finite statement

Use the canonical coordinates of the frozen induced95 support certificate.
Let P be its25 binary directions with real root-support rank seven. For every
three distinct members of P, the independent checker confirms their binary
rank is three. The members of P annihilating all three span dimension at most
five. Across the2,300 triples the span-rank histogram is

    rank0:636; rank1:860; rank2:559; rank3:186; rank4:56; rank5:3.

Suppose lambda_1,...,lambda_9 form a basis drawn from P and mu_1,...,mu_9
are its dot-product dual. If three duals were proper, the other six lambda
directions would be six independent members of P annihilating those three.
That contradicts the verified maximum of five. Thus at least seven mu_j
have full real root-support span eight.

The bound is sharp. The displayed basis

    [59,87,91,199,234,248,274,367,443]

has dual

    [222,122,40,31,401,509,402,97,243].

The independent dot-product check gives the identity matrix. Exactly122 and31
are proper; the other seven duals have full support span eight.

## Arbitrary record width and noncommuting vertex gauges, b=1

Take the actual remaining95-receiver descent transcript at rank equality.
There are exactly nine whole records of width V. Let K=A C be the fitting
factorization from the open-network cut. Its rank is9V, so A and C both have
rank9V. Rigidity gives, after an invertible internal change of coordinates,

    A_i = U_i (xi_i^T tensor I_V) S,

where every U_i is invertible. Suppose every descent destination is a nonzero
allowed line. At one such line the canonical shortening is exactly
lambda tensor k^V, for a unique binary lambda in P. Therefore event e has

    A_(i,e) = (xi_i dot lambda_e) U_i G_e

for a V-by-V matrix G_e. Every event block A_e has column rank V because all
9V columns of A are independent. The stacked canonical lambda factor has
column rank V, hence G_e is invertible. No commutation of these G_e or U_i is
used.

Independence of A now forces the nine scalar lambda_e to be a basis. Any
binary scalar dependence, together with the invertible G_e, would produce a
V-dimensional dependence among its block columns. Conversely, independence
of binary lambda vectors remains independence over every characteristic-two
extension field.

Let mu_e be the binary dual basis. Uniqueness of C in A C=K then gives

    C_(e,j) = (mu_e dot xi_j) G_e^-1 U_j^-1.

Thus the actual U-projected payload block has nonzero j-component precisely
when mu_e dot xi_j=1. The noncommuting invertible gauges cannot create or
remove a support block. The finite result proves that at least seven actual
payload blocks have real root-support span eight. This proves the proposed
extension for arbitrary V; it does not assume that whole records contain
only scalar coefficients or that coordinate lanes may be split for free.

The b=1 hypothesis is material. For b>1, a width-V event can occupy a proper
V-dimensional subspace of the bV-dimensional shortening at one line. Its
factor need not be a square invertible block, and the nine-direction scalar
basis reduction does not apply. No scaled7b or analogous tariff is claimed.

## Physical scope

This statement is conditional on nine events and all nine landing on nonzero
lines. Ground arrivals do not select a one-dimensional scalar shortening and
fall outside this reduction. It also makes no claim about where full-support
payloads were formed: paid prior descents and later recoding can move their
information away from the full real span of their original input roots.
Formation and movement prices need a separate chronological argument.

Run `python -B check.py --support ../induced95-rigidity/FULL-SUPPORT-CERTIFICATE.json
--author ../../R/proper-basis-coupling --out output` from this directory.
