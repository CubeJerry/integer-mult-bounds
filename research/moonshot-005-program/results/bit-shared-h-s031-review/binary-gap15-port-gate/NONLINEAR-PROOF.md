# Nonlinear bank gauges become additive on the required geometric core cosets

**Proposed strengthening, awaiting independent proof review.** Under the same
separated-source, identity-target and tight native H263 contract, arbitrary
independent bank bijections cannot repair the geometric scalar or single-gap15
source family. The argument makes no claim that a complete bank bijection is
globally additive. Its restriction to one relevant affine core coset suffices.

All finite coefficient extensions, positive admissible widths, arbitrary
gap15 matrices, nonlinear quotient-output relabelings and nonlinear H or
downstream functions are permitted. Source changes outside that family,
inter-source preprocessing, larger informative cuts and changed targets remain
outside the result. No complete kappa or new return tariff is claimed.

## 1. A finite coset-partition lemma

Let A be a nonzero finite F2-vector space. Let X be a set of nonzero vectors
of F2^r containing a binary basis. Express X in that basis. Assume every
coordinate axis occurs in at least one vector of X whose support has size at
least two. For v in X, write

    L_v={v tensor a:a in A} <= A^r.

Let W be a finite F2-vector space. Suppose f:A^r -> W is a bijection such that
for each v in X there is a fixed additive subgroup S_v<=W, and f takes every
coset of L_v onto a coset of S_v. Then f is affine-additive: f(x)+f(0) is an
additive isomorphism from A^r to W.

### Proof

Translate f so that f(0)=0, and denote the selected basis directions by
e_1,...,e_r. Put S_l=S_(e_l). Each S_l has |A| elements. Joins of equivalence
relations commute with a bijection. The join of all source axis-coset
relations has one class, A^r, and the target join has classes which are
cosets of sum_l S_l. Hence W=sum_l S_l. Since f is bijective,

    |W|=|A|^r=product_l |S_l|.

The sum is therefore direct. This cardinality argument also handles every
proper coordinate subcollection, but the full equality already suffices.

Identify W with the direct sum of the S_l. Changing x_m while holding the
other coordinates fixed changes f(x) only by an element of S_m. Thus the
projection of f(x) to S_l depends only on x_l. There are bijections
f_l:A->S_l, each taking0 to0, such that

    f(x_1,...,x_r)=sum_l f_l(x_l).                                    (1)

Take v in X with support T of size at least two. The image of L_v is S_v,
because its source coset contains0. Formula(1) gives

    S_v={sum_(l in T) f_l(t):t in A}.                                (2)

For l in T, projection pi_l:S_v->S_l is bijective, since its value at the
point in(2) is f_l(t). It is an additive isomorphism, because both S_v and
S_l are additive subgroups and projection is linear. For distinct l,m in T,
there is consequently a fixed additive isomorphism

    P_ml=pi_m composed with (pi_l|S_v)^(-1):S_l->S_m.

For any base point x and any t in A, f(x+t v)+f(x) lies in S_v. Its l,m
coordinates satisfy

    f_m(x_m+t)+f_m(x_m)
      =P_ml(f_l(x_l+t)+f_l(x_l)).                                    (3)

The two coordinates x_l,x_m can vary independently. Fix x_m=0 in(3).
The right-hand increment is then independent of x_l. Evaluating it at
x_l=0 shows

    f_l(x_l+t)+f_l(x_l)=f_l(t).

Thus f_l is additive. The same reasoning applies to every coordinate in T.
By the axis-coverage hypothesis, every f_l is additive, proving the lemma.

This is an exact finite functional-equation proof. It uses no tangent map,
smoothness, genericity, or extrapolation from a small-alphabet experiment.

### Why the native graph supplies the hypothesis

The33 native parameter directions span F2^6, so a basis can be selected from
them. Their graph joining v,w whenever v+w is also allowed is connected.
If one basis axis appeared in no mixed-support allowed vector, that basis
vector would be isolated in the graph: adding it to any other allowed vector
would introduce a mixed support containing that axis. Therefore connectedness
implies the required coverage. The checker additionally gives explicit mixed
directions covering all six selected axes.

## 2. Tight additive cuts provide the target subgroup partitions

The source and native interface are exactly those in
[BINARY-PROOF.md](BINARY-PROOF.md). Let g_j be any bijection of the full donor
bank, applied before its fixed linear source quotients. For each receiver i,
fix the fifteen off-H observations at each of the three donors. The resulting
original-input fibres are

    g_j^(-1)(u_j+L_(j,i)),

and each has size M=|F|^k. Holding all other original inputs and all external
observations fixed, the desired target varies over the sum of these three
fibres. Its only remaining informative transcript crosses the H cut of M
possible values. That sumset has at most M elements and at least M elements,
so exactly M.

For finite nonempty A,B of equal size M, equality |A+B|=M forces A and B to
be cosets of the same subgroup: all translates A+b coincide, so B-b_0 lies
in the stabilizer H of A; |H|>=M while A being a union of H-cosets gives
|H|<=M. Apply this twice to the three fibres. Holding one donor fibre fixed
while varying every fibre at another donor proves that the common subgroup
depends only on i, not on the fibre values or donor. Denote it by S_i.

Thus g_j^(-1) maps the entire partition into cosets of L_(j,i) to the entire
partition into cosets of one fixed additive subgroup S_i, common to all
three donors. This preliminary fact allows arbitrary nonlinear g_j and is
the same finite additive reduction used in the separately reviewed frozen
feedback partition gate.

## 3. Restrict each inverse gauge to one affine core coset

For the geometric/gap15 source, the reviewed universal pencil theorem gives
an injective linear core embedding

    E_j:A^6 -> F^(16k),       A=(F^k,+),

with L_(j,i)=E_j(v_(j,i) tensor A). Choose six receiver indices whose donor0
parameter vectors form a binary basis. The same receiver indices form a
basis at each other donor, because v_(j,i)=J_j v_(0,i) with J_j invertible
over F2. Use these corresponding bases to identify the three cores with A^6.
The remaining native directions then have the same binary coordinates at
all donors.

Choose arbitrary fixed source-coordinate base points u_j. The join of the
six selected source-fibre partitions has classes

    C_j=u_j+E_j(A^6).

Under g_j^(-1), these classes become cosets of the additive subgroup

    W=sum over the six selected receiver indices i of S_i.

The subgroup W is the same for all donors. The image of C_j is exactly
g_j^(-1)(u_j)+W, not merely a subset, because a bijection preserves the entire
join equivalence relation. Its cardinality is |A|^6. After translating both
base points, the restriction of g_j^(-1) is therefore a bijection

    f_j:A^6 -> W

that maps every native direction's coset partition to cosets of S_i. The
lemma proves f_j additive.

The additive isomorphism f_j^(-1) composed with f_0 preserves each native
parameter direction. Applying the connected-amplitude lemma in
BINARY-PROOF.md now gives a single invertible binary amplitude map M_j,
independent of the receiver. This conclusion is required only on these
chosen affine core cosets. The linear part may differ on other core cosets;
no global additivity of g_j is concluded or needed.

## 4. The same full H-input domain gives the port contradiction

For receiver i, fix its off-H source observations to the values at the same
chosen base point u_j. Its entire remaining source fibre is

    u_j+E_j(v_(j,i) tensor A),

which lies in the chosen core coset C_j. Its central quotient is
Q_(j,49)u_j+d_(j,i)A and therefore ranges over the full amplitude alphabet,
since d_(j,i) is nonzero. The three H inputs vary independently and exhaust
the same full product alphabet for every receiver. Their base offsets
Q_(j,49)u_j are fixed once, not changed when comparing receivers5 and76.

On the chosen core cosets, the inverse gauges are affine-additive and have
the fixed relative amplitude maps obtained above. Removing constant target
and input offsets yields exactly the binary aggregate row spaces(2) of
BINARY-PROOF.md. Different receivers embed their aggregate amplitudes into
different common uncertainty subgroups, but each embedding is injective;
recovering the full target is equivalent to recovering that aggregate.

Receivers5 and76 have derivative triples(30,18,12) and(38,18,52).
The identical second derivative18 gives the invertible difference

    D(56) M_1 D(18)^(-1).

Their aggregate row spaces have zero intersection for every invertible
binary M_1,M_2. The actual positive D108 packet, viewed as one function on
the same full H-input domain, must be a function of each aggregate by exact
capacity. It is therefore constant, contradicting its full positive alphabet.

Separate nonlinear quotient-output relabelings simply reparameterize this
full input alphabet; composing them into the arbitrary H function changes
nothing. Nonlinear H and downstream processing were allowed throughout.

## 5. Controls and exact limits

The checker supplies the literal native derivative collision, the six-axis
mixed-direction cover, the connected parameter graph and noncommuting binary
matrix controls. For the abstract coset lemma it exhausts all40,320
permutations of F2^3; exactly1,344 have the required basepoint-independent
additive increments, matching the affine group size8*7*6*4. A nonaffine
coordinate transposition fails the increment condition. These are finite
controls, not the proof of the universal lemma.

A further control deliberately makes a bank bijection globally nonlinear
while preserving every required core partition: its common additive
amplitude automorphism changes with an outside-coset coordinate. This shows
why the theorem must stop at affine restrictions on individual core cosets.
The proof does so and uses only one such coset at each donor.

The final obstruction covers the entire scalar/single-gap15 source family
under arbitrary separate bank bijections, with the stated fixed native
target and informative cuts. It does not exclude multiple-gap feedback,
other source quotient information, arbitrary coupled source preprocessing,
additional paid information paths or other target blocks. Source rank and
propagation-slack results remain valid in their original scopes. No complete
supplier, physical runtime, return-excess bound or kappa improvement is claimed.

Credit @CubeJerry and all predecessor notices. S031 Worker C developed the
derivative-collision extension and exact core-coset lemma; root independently
identified the same nonlinear extension route. Substantial OpenAI assistance.
This proposed strengthening requires a separate adversarial proof review.
