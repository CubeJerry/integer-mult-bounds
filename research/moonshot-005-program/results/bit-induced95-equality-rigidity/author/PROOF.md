# Rigidity at the remaining95 fitting floor, with the correct support exceptions

**Proved algebraic and source-specific equality consequences, pending independent
review. No source-formation tariff or complete supplier is asserted.**

The induced95-port graph has a unique minimum-rank block fitting up to vertex
gauges. Its canonical code has **486 full-span words and25 rank-seven words**,
not511 full-span words. At exact minimum transcript dimension this forces
future receiver-downset destinations to have rank at most one. A nonzero
destination must lie on one of25 explicitly listed lines. The claim that all
such packets must be born at Hub and arrive at ground is not justified.

## 1. Native and remaining domain

Use the authenticated actual native roots, SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
Their line/facet convention is L_i=span(R_i), F_i=R_i^perp, and the binary
canonical fitting is

    K0_ij = 1 if i=j or R_i dot R_j=0, and 0 otherwise.

Let

    T={14,17,19,20,96,99,101,102},
    U={8,...,110}\T,     |U|=95.

The preceding private-region/transcript package proved the exact minimum
fitting rank9d on U, for every characteristic-two field k and positive block
width d, using a new nine-frame parity witness entirely inside U. That floor
must not be inferred merely by deleting vertices from the full111 theorem.
The present package proves its equality classification independently of the
full111 anchor list.

## 2. A new saturated star and complete ordered propagation

The point frame is

    F=[27,16,11,39,36,57,68,72].

Its point-point fitting blocks are the eight-coordinate identity mask.
There are21 retained edge roles with the exact two-point contact patterns
recorded in STAR-CERTIFICATE.json. The underlying eight-point graph has degrees

    [5,5,5,5,5,5,7,5].

Every two edge roles sharing an endpoint are actual noncontacts. Hence the
abstract saturated-star argument applies, but this is a newly checked star
on U. None of its points or edges is an axis or one of the eight removed
raised targets.

Here is the needed argument in its exact block form. Let K=CR have rank9d.
Normalize the point frame to eight coordinate d-blocks, with a remaining
ambient d-block. An edge e={a,b} then has factors supported only at a,b and
the last block. Write

    S_e=C_e,* R_e,*,
    gamma_e(a)=C_e,a R_e,a+S_e,
    g_e(a)=rank gamma_e(a),
    G_a=sum_(e incident a) g_e(a).

The credited star rank inequality is

    G_a+d <= d+2(g_e(a)+g_e(b)).

It follows by stacking the restricted edge factors at a and the final block,
using the actual zero off-diagonal edge products, and applying Sylvester's
rank inequality. The complete derivation is retained in the admitted
`results/bit-saturated-star-rigidity/author/PROOF.md`, Sections2–3, crediting
DreamingOfClouds's #7114 inequality. Summing over edge endpoints yields

    sum_a (deg(a)-4) G_a <= 0.

Every degree is at least five, so all G_a and all gamma_e(a) vanish. The edge
diagonal identity then forces S_e=-I=I in characteristic two. Both factors
of each S_e are invertible. The ordered star gauges make all point and edge
factors canonical without commuting any matrices. Degree at least three,
already satisfied here, gives a common point gauge from the shared-edge zeros.

This normalizes29 actual roles: eight points and21 edges. The new certificate
then supplies66 ordered propagation steps. At each step the new role has
eight previously normalized noncontact anchors whose canonical binary vectors
have rank eight. Their common annihilator is exactly the new role's canonical
one-dimensional vector. The two-sided noncontact constraints therefore force

    C_i=U_i (xi_i^T tensor I_d),
    R_i=(xi_i tensor I_d) V_i.

Since xi_i dot xi_i=1, the diagonal condition gives U_i V_i=I_d. Both are
square and hence invertible. Applying the vertex gauge normalizes that role.
All95 roles are reached in order.

**Rigidity theorem.** Every fitting K on U of rank exactly9d over any
characteristic-two field has

    K_ij=U_i (K0_ij I_d) U_j^-1

for invertible U_i. Nonsymmetry, arbitrary noncommuting blocks and initially
singular edge factors are included. No scalar-tensor restriction is imposed.
The explicit K0 tensor I_d attains the rank. No physical encoding or decoding
schedule is supplied by this algebraic theorem.

## 3. Exact canonical support classification

The checker derives canonical vectors xi_i in F2^9 directly from the new star:
the first eight coordinates are the contacts to F; the last is obtained from
one actual star edge. It verifies every one of the95² Gram entries

    xi_i dot xi_j = K0_ij.

For each nonzero binary coefficient lambda in F2^9, form the support

    S_lambda={i in U: xi_i dot lambda=1}.

All511 supports are explicitly enumerated. For each, the certificate gives
an integer nonzero minor from its actual root vectors. The486 rank-eight
cases have exact eight-root, eight-column determinants. Each of25 rank-seven
cases has a nonzero seven-root minor and an exact annihilating normal that
kills every root in its support. There are no supports of rank below seven.
The finite geometric result is

    rank_R span{R_i:i in S_lambda} = 8, for486 lambda;
    rank_R span{R_i:i in S_lambda} = 7, for25 lambda.

The25 normal lines are all distinct. Sixteen are the native lines of the
eight deleted axes and eight deleted raised roles. Nine are lines absent
from the actual111-port native. None is a remaining role in U. The exact
mask, support, determinant and line list is retained; it is not inferred
from a root-system name or an unverified symmetry claim.

### Explicit counterexample to the all511-full-span claim

In the new coordinate convention, lambda has mask31 (bits0 through4). Its
52-role support is

    9,11,16,18,22,24,27,29,30,31,36,37,39,41,42,44,46,47,
    48,52,54,56,58,59,60,64,65,66,67,70,71,73,74,77,78,
    83,85,87,90,91,94,95,98,100,103,104,105,106,107,108,109,110.

Every listed native root is orthogonal to

    n=(0,-1,1,0,1,0,0,1).

The saved seven-root minor is nonzero. Its real support rank is therefore
exactly seven. This is a counterexample, not a failed search for an eighth
root. It prevents a false Hub/ground conclusion.

## 4. Extension to arbitrary fields, blocks and vertex gauges

The binary support check is enough to obtain the appropriate universal
lower bound. Consider any nonzero vector-valued combination

    f_i=sum_(a=1)^9 xi_(i,a) w_a,    w_a in k^d.

Choose one scalar component on which some w_a is nonzero. Its nine scalar
coefficients span a finite-dimensional F2-space, even when k is infinite.
An F2-linear functional to F2 can be chosen to be nonzero on that component.
Applying it produces a nonzero binary lambda with

    S_lambda subset {i:f_i is nonzero}.

Thus the real roots on the support of f span at least seven dimensions.
Multiplication by the individual invertible U_i does not change which f_i
vanish. The conclusion therefore applies to every column of a vertex-gauged
canonical decoder factor and every row block of a canonical payload factor.
It is not restricted to binary scalar coefficients.

If the support annihilates a nonzero real line, its binary sub-support must
be one of the25 rank-seven cases, and that line must be its listed normal.
At each such line the scalar canonical shortening has dimension exactly one:
its only nonzero binary vector is the listed lambda. Binary rank remains the
same over every characteristic-two extension field. Hence the vector-valued
shortening is lambda tensor k^d.

## 5. What exact9b remaining-downset descents force

Apply the preceding theorem to either actual source in the private-region
package, or to the separately audited two-copy source. Each copy record has
width V; set d=bV. Cut all future downward owned MOVEs whose destination lies
in the union D_U of remaining receiver facets. The actual all-field source
locality audit gives

    K=I-M0=A C,

where K is a fitting on U and C stacks each cut record's full dependence on
the remaining input blocks. This is the time-unrolled cut construction;
later cut values may depend on earlier cuts.

Suppose there are **exactly9b** such whole-record events. Then C has9bV=9d
rows, and K has rank at least9d. Equality follows. Both A and C have full
rank9d. Rigidity therefore puts A, after one invertible factor-basis change,
in the form

    A_i=U_i (xi_i^T tensor I_d) S.

For event e with actual destination chart B_e, the open network's response
A_ie can be nonzero only if B_e is contained in F_i. Indeed, the response
from the independent cut variable z_e can propagate afterward only along
uncut local and upward paths; any later downward entry into D_U is itself
cut and replaced by a fresh variable. A_e has a nonzero column since A has
full column rank. By Section4, the normals R_i on that column's support span
at least seven dimensions. All annihilate B_e, so

    dim B_e <= 1.

If dim B_e=1, it is one of the25 normal lines in Section3. More sharply, all
independent decoder columns for events landing at the same line lie in the
same d-dimensional shortening lambda tensor k^d. Since A's full collection
of columns is independent, at most b whole-V events can land at any one such
line at equality. Ground arrivals have no analogous one-line restriction.

This is a conditional equality theorem. A continuation with more than9b
remaining-downset descents changes its premise. The theorem does not price
formation of the payloads, constrain unrelated descents outside D_U, or
conclude that the b-fold caller is complete.

## 6. Ground-only and Hub-birth conclusions do not follow

The correct destination conclusion is rank at most one, with25 explicit
nonzero-line exceptions. The listed proper code directions even span all
nine binary canonical dimensions. The certificate gives an invertible
nine-direction decoder basis using only these rank-seven directions:

    [31,59,87,91,122,199,217,265,367].

Its inverse supplies the corresponding payload basis. This is a valid
algebraic fitting factorization with possible nonzero-line supports; it does
not by itself supply a cheap physical schedule. In particular, this package
does not silently turn that factorization into a target-budget construction.

A universal Hub-birth claim is also unjustified in the admitted model that
permits paid owned ascents. For the mask31 word, all52 actual raw native
copies exist at their own source lines. Those lines lie in the proper
rank-seven hyperplane n^perp. Paid ascents can gather copies there, where
local ADDs form this canonical codeword without visiting Hub. The gathering
is expensive; no free movement, target-budget feasibility, or source-price
improvement is claimed. This explicit possibility shows why real support
rank alone is not a source-location theorem.

The current proper half reservoirs make the distinction even more important:
their payload support need not be contained in their own chart after earlier
paid descents. A complete cost obstruction must audit actual source
availability, earlier paid crossings, aggregation, and future routes. It
cannot replace those duties by an unsupported statement that every
canonical payload is born at Hub.

## 7. Verification and next obligation

Run `python -B check.py --repo REPO --star STAR-CERTIFICATE.json --support
FULL-SUPPORT-CERTIFICATE.json --out OUTPUT`. The checker authenticates the
native, reconstructs the entire95-role canonical factorization, verifies the
new21-edge star and all66 ordered anchor steps, and checks every511 support
using exact integer minors and annihilators. It verifies the25 distinct
normal lines and the displayed nine-direction basis and inverse. Search
scripts are discovery provenance, not proof dependencies.

The remaining physical question is whether payloads entering those25 lines
or ground can actually be formed and delivered within the source's residual
movement budget. This package establishes the exact algebraic and geometric
equality constraints and removes the false all-Hub/all-ground shortcut. It
does not grant any formation expense or prove that equality is attainable
at the target tariff. More than9b descents also remain possible, with their
honest additional cost.

Credit the admitted parity theorem, DreamingOfClouds's star rank inequality
and the programme's saturated-star argument, the previous ordered-anchor
method, S021 C's new induced95 certificate and support classification,
root's equality/formation challenge, @CubeJerry, and substantial OpenAI
research assistance. No new complete kappa or foundational discharge.
