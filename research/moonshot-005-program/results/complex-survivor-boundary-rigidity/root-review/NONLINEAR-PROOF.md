# Nonlinear five-message rigidity up to translations

## Proposition and scope

Use the exact paid #7833 control of the authenticated #7830 word described
in the parent proof. Let K be any characteristic-zero field and let V be a
positive finite integer. Replace the payload at each of

    86, 97232, 97241, 97323, 99064

by an arbitrary function A_j:K^V -> K^V of that payload alone. No linearity,
continuity, measurability or zero-preservation is assumed. All other literal
forms, original roles and paid routes remain fixed. Independent arbitrary
bijections are allowed within each original physical input bank and each
original physical output bank, with equal-span chart aliases identified.

The changed word can represent the original endpoint up to those independent
bank bijections **if and only if each A_j is a translation**. In particular,
if all five functions preserve zero, every A_j must be identity. The parent
whole-field linear theorem is an immediate special case.

This is a restriction on these five local changes with the surrounding word
fixed. Coupled recoding of other internal forms, extra communication and
changed boundary bank partitions remain outside the claim. No price bound
for those broader architectures, complete supplier or new exponent follows.

## Exact finite identities

Write E for the invertible full 1289-field endpoint, P for the five original
payload rows, B for the five additive post-message responses at the endpoint,
and H for their responses at the pre-message payloads. The independent root
checker reconstructs the paid surgery from raw JSON; it uses reverse DAG
expansion and whole sparse elimination, without importing the author's code.
It verifies every endpoint and both complete inverse products. Put

    Q = P E^(-1),    R = E^(-1) B.

The exact identities are

    H = 0,          Q B = P R = diag(1,0,0,0,0).

Every scalar below acts on K^V by that scalar times identity. For each j there
is an input axis a and an output axis b such that the entire old inverse
block between their physical banks is zero, while

    R[a,k] Q[k,b] = 0 for k != j,
    R[a,j] Q[j,b] != 0.

The five nonzero products, in occurrence order, are

    -63/128, 1/2, -1/2, 1, 1/2.

The listed axes are (17,131), (17,150), (19,129), (17,776), (19,150).
All products and whole-bank zero assertions are checked over the complete
source. Characteristic zero keeps all five products nonzero.

## The nonlinear endpoint identity

For each occurrence, regard its departure from the original linear payload
as a separate additive perturbation. The rest of the literal DAG is linear,
so its response to any values of these five perturbations is exactly B at
the endpoint and H at the five pre-message inputs. The perturbations can
themselves be arbitrary functions of the input; linear propagation of their
values does not assume that those functions are linear.

Because H=0, every pre-message input remains exactly P_j x. Consequently

    E_A(x) = E x + B (A(P x) - P x),

where A acts separately in the five coordinates.

If E_A is bijective, A_0 must be bijective. Surjectivity follows from

    Q_0 E_A(x) = A_0(P_0 x)

and surjectivity of Q_0, since Q_0 B_0=1. To prove injectivity, use the
nonzero column r_0=R_0, for which P r_0=(1,0,0,0,0). If A_0(t)=A_0(t'),
evaluate E_A at r_0 t and r_0 t'. The other four pre-message payloads agree,
and the endpoint difference is B_0(A_0(t)-A_0(t'))=0. Injectivity of E_A
and r_0 forces t=t'. This argument does not assume zero-preservation.

Conversely, if A_0 is bijective, the whole changed endpoint is bijective
irrespective of the other four functions. Its inverse is

    E_A^(-1)(y) = E^(-1)y + R D(Q y),

with

    D_0(t) = A_0^(-1)(t)-t,
    D_j(t) = t-A_j(t)                    (j=1,2,3,4).

For verification, applying P to this formula gives A_0^(-1)(Q_0 y) in
coordinate zero and Q_j y in the other four coordinates, by P R=diag(1,0,0,0,0).
Substitution in the nonlinear endpoint identity yields y. In the reverse
order, Q E_A(x) has first coordinate A_0(P_0 x) and other coordinates P_j x,
so the inverse expression yields x. Both directions are therefore proved.

## A zero inverse-bank dependency forces a constant correction

Independent bijections at the original boundary banks preserve whether one
output bank depends on one input bank. This statement applies to arbitrary
functions: changing coordinates within a bank does not change its complete
range of possible values, and a bijection at the receiving bank cannot
identify distinct outputs. Hence if independent bank bijections turn E_A
into E, every zero bank dependency of E^(-1) must also hold for E_A^(-1).

Fix the isolating axes a,b for channel j. Vary only the single output axis
b by h in K^V. The linear E^(-1)y contribution at axis a is unchanged,
because the whole corresponding old inverse-bank block is zero. The change
in the nonlinear correction is

    sum_k R[a,k] (D_k(Q_k y + Q[k,b]h) - D_k(Q_k y)).

Every term k != j vanishes: its scalar product is zero, so either R[a,k]=0
or Q[k,b]=0. The remaining two scalars R[a,j] and Q[j,b] are nonzero.
Bank independence therefore requires

    D_j(t+q h) = D_j(t) for every h in K^V,

where q=Q[j,b] is invertible. It is enough to set y=0, so t=0; varying h
then covers all K^V. Thus D_j is constant. Applying the five witnesses gives
that all five D_j are constant, which is equivalent to all five A_j being
translations.

Conversely, if A_j(t)=t+c_j, then E_A(x)=E x+B c. Subtracting the fixed
vector B c separately within each original output bank recovers E. This is
an allowed independent output-bank bijection. The qualification 'up to
translations' is essential; arbitrary nonlinear maps need not preserve zero.

## Computational controls and review status

The checker evaluates two full literal width-two examples with genuinely
nonlinear per-message functions. A_0 is an invertible quadratic triangular
map; the other four need not be injective. For both inputs, the independently
reconstructed nonlinear endpoint identity and inverse recover all 1289
original fields. Separate controls exhibit a new inverse-bank dependency at
each isolating witness, verify the exact deletion kernel for occurrence 86,
and replay a nonzero constant-offset positive control.

These controls test the finite identities and implementation. The universal
quantifiers over fields, widths and arbitrary functions follow from the
argument above, not from sampling. Independent review of this extension is
recorded separately; the parent's finite identities and linear theorem have
been independently reconstructed by root.

Credit: parent S031 Worker B, the pinned #7830 and #7833 predecessors,
@CubeJerry, and S031 root with substantial OpenAI assistance.
