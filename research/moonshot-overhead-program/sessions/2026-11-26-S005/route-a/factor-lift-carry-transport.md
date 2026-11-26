# Transporting carry maps between nearby factor lifts

Status: **exact enabling identity and affordable modulo-four setup**;
independent review requested. No fast CRT or carry supplier is constructed.
This supplements UC/KC without modifying their frozen proofs.

## 1. A full-module quotient isomorphism

Put Q=2^t, t>=1. Let g be monic of degree d over Z/(Q^2), with
squarefree reduction modulo two. For deg h<d set g_new=g+Qh. In
R_old=(Z/(Q^2))[X]/g, alpha=X mod g, choose

    delta=-h/g_dot mod (Q,g),  beta=alpha+Qdelta.       (FL1)

Here g_dot is the formal derivative. Its inverse exists modulo Q because
it is a unit modulo two; a finite geometric lift preserves that property.
Construction of the inverse is charged separately below. Taylor expansion
gives g_new(beta)=Q(delta g_dot+h)=0 modulo Q^2. Hence X -> beta
defines a homomorphism from the new quotient to the old quotient. In
their monic degree-below-d coefficient bases its matrix is I+QB, with
inverse I-QB modulo Q^2. It is an isomorphism on every independent
coefficient word, without an initialized sector or redundant payload.

## 2. Exact transport of remainders and high digits

Let E_t be their common remainder map modulo Q and let r=E_t(F) denote
the canonical degree-below-d polynomial. If r_old and r_new are the
Q^2 remainders of F in the two quotients, then

    r_new=r_old+Qdelta[E_t(F_dot)-r_dot] mod Q^2.      (FL2)

The bracket and its product with delta are reduced modulo (Q,g).
The derivative r_dot is taken on the specified polynomial representative;
there is no assumed derivative operation on the quotient ring.

Indeed, F(beta)=r_new(beta) expands to

    F(alpha)+Qdelta F_dot(alpha)
      =r_new(alpha)+Qdelta (r_new)_dot(alpha).

The final derivative may be reduced modulo Q, where r_new=r. Moving
it and expressing the result in the old monic basis proves FL2.
For canonical t-bit input coefficients, the low residue digits coincide,
so their high-digit maps satisfy

    K_new(F)=K_old(F)
      +delta[E_t(F_dot)-(E_tF)_dot] mod Q.            (FL3)

These identities hold componentwise for the entire CRT family. The
low-precision payload dimension remains exactly qt bits.

When r is already supplied, FL3 requires one additional low-precision
CRT call on F_dot. Both UC5 callers have r: forward lifting has already
computed it, and inverse lifting knows it as the low input residue.
A standalone K_new oracle using only a high-digits-only K_old oracle
must compute E_t(F) as well, hence needs two low-precision calls unless
that result is supplied.

## 3. Physical application and preparation costs

For UC's irreducible binary reductions, d_i<=b and sum d_i=q. Suppose
the factors and deltas are in the established sequential factor order.
With r supplied, the extra application invoice is

    T_CRT(q,t)+qt polylog(b+t+2).                     (FL4)

Use two T_CRT calls otherwise. The local part uses a constant number
of qt-bit streams plus reused polynomial local workspace. T_CRT must
retain its own stated time/space contract. The input derivative is a
scan multiplying the j-th coefficient by j mod Q; only a t-bit counter
is needed. Residue derivatives are another scan. Degree-d quotient
products and monic reduction use packed integers with
O(d(t+log(d+2))) bits; summing their small-arithmetic, reciprocal,
scanning and return costs gives the local term in FL4.

Given h, delta preparation is not free. In the UC irreducible case,
compute the binary inverse of g_dot by O(d) field products using
a^(2^d-2). Lift by u <- u(2-g_dot u) in the quotient ring, and multiply
by -h. Small packed arithmetic gives the safe one-time invoice

    qb polylog(b+2)+qt polylog(b+t+2),                (FL5)

with an O(qt)-bit delta directory and reused local workspace. FL5 does
not generate h. The more general squarefree hypothesis of Section 1
permits polynomial Euclid and unit lifting instead, with its actual
preparation charged; FL5 is claimed only for UC's irreducible family.

## 4. Actual modulo-four Hensel factors without a global product

Take t=1 and the literal binary g_i, with d_i dividing b and q=2^b.
In (Z/4)[X]/g_i compute

    s_i=(alpha_i^q-alpha_i)/2 mod 2.                  (FL6)

The numerator has even canonical coefficients, since its reduction
modulo two vanishes. Starting at alpha_i, b modular squarings compute
alpha_i^q. Define

    delta_i=s_i,
    h_i=s_i (g_i)_dot mod (2,g_i),
    g_i^H=g_i+2h_i mod 4.                            (FL7)

Modulo two the minus sign in FL1 disappears, so this supplies its
delta directly, without a derivative inverse. For P_0=X^q-X, its
derivative is -1 modulo two. Thus

    P_0(alpha_i+2s_i)=2s_i+2s_i(-1)=0 mod 4.

The quotient isomorphism implies that g_i^H divides P_0 modulo four.
The new factors remain monic and pairwise comaximal, with total degree q,
so their product equals X^q-X modulo four. This proves the identity
without constructing the degree-q product polynomial.

Each precision-two modular square costs d_i polylog(d_i+2) tape steps,
including monic reduction, local setup and scans. The b squarings and
one final local product per factor therefore cost

    qb polylog(b+2) time,
    O(q)+poly(b) cells ever visited.                 (FL8)

The literal input factors are generated by FS1 at the same scale plus
poly(b) preprocessing. Output lifted factors, s_i and degree tags need
O(q) bits. A constant number of sequential streams and reused local
scratch pay all movement. The additional modulo-four products have
O(b log(b+2))-bit operands; FS1's O(b^2 log(b+2)) maximum still bounds
the combined setup.

At the integer root, qH=Theta(n), H=Theta(b), so the combined setup is
n polylog(b), eventually below n sqrt(b). It must be generated once
and shared; it is not free O(q sqrt(b)) setup at every binary leaf.

## 5. Exact recurrence consequence and its limit

FL3/FL7 transfer the first carry problem between literal factors and
the factors of X^q-X modulo four. They do not remove carry. For b=2,
X+1 changes to X-1 while X and X^2+X+1 stay unchanged. At F=X the
linear factor's old carry is one and its new carry is zero, with the
nonzero correction delta(E_1(F_dot)-r_dot)=1.

The modulo-four choice alone does not select a coherent factor family
at every higher precision. Nor does it transfer the higher K_t for
UC's already fixed literal factors. Those remaining carry gates are
still open; the following comparison changes only the bottom K_1 gate.

Applying only this modulo-four conversion inside UC6 costs one extra
binary CRT at each bottom carry node. There are H/2 such nodes, so
the added binary-call cost qH B(b) is absorbed into the coefficient
of UC6's existing binary term. Retaining FL4's local work, the complete
bottom surcharge is O(qH[B(b)+polylog(b)]). D(b,1) may therefore be
O(B(b)+polylog(b)), rather than the stricter pointwise O(1) endpoint
contract. The summed endpoint implication is unchanged when
B(b)=O(sqrt(b)), since a fixed polylog(b) is eventually below sqrt(b).

No free all-precision conversion follows. One extra precision-t call
at every lifting node changes two recursive calls to three, with
normalized child-volume multiplier 3/2; UC6 would have to be replaced.
Likewise b modular squarings at precision 2t cost qt b polylog(b+t),
which need not fit the desired root budget at large t. No such general
setup or amortization is supplied here.

The concrete continuation is to test whether the binary CRT and first
carry are easier in the exact modulo-four Hensel-factor format, then
use FL3 to transport a successful supplier with the stated cost. The
unconditional frontier is unchanged.

Credits: the lead proposed the perturbation identity and modulo-four
setup; Route A independently checked and wrote the quotient,
representative-derivative and tape-cost arguments. The known-low-digit
convention and recursive extra-call obligation were clarified jointly.
Standard Hensel lifting, polynomial CRT and UC/FS's cited arithmetic
suppliers retain their provenance. Substantial ChatGPT assistance;
no priority claim.
