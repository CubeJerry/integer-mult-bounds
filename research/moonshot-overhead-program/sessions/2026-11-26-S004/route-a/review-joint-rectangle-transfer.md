# Route A review of the joint-rectangle conditional transfer

Reviewed: lead draft `lead-work/joint-rectangle-transfer.md`, S004.
Source pins: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6` and
programme `a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`.

**Verdict: passes as a complete conditional transfer, relative to the
named existing fixed-field construction and expanded physical compiler.
JR remains open.** This review does not independently reprove every
predecessor theorem or certify a physical multiplier implementation.

## Finite graph and layout interface

The random-cover union bound is correct: each fixed unequal-coordinate
edge occurs in a random directed product cut with probability 4^-k, and
R>=4^k(2k ln q+1) makes the missing-edge probability strictly less than 1.
The distinction between a cover and an exact disjoint partition is
essential and preserved. Over characteristic dividing q, J_q^2=0 and
(I-J_q)(I+J_q)=I; tensoring gives adjacency rank q^k. Therefore a weighted
rank-one realization needs at least q^k nonzero terms, independently of
the signs or coefficients. This is not an obstruction to JR's allowed
number of small rectangles.

The JR substitution preserves all source Gram contracts. Fixing the first
changed coordinate and both of its letters means that each side of a new
inner rectangle varies in at most d-1 positions. Internal far distance d
is impossible, while every cross pair differs in exactly the chosen d
positions. Taking products over the chosen outer positions gives k=0
within each side and k=d across sides. The new rectangles are disjoint
because the difference support, common letters and fixed first ordered
pair are unique, and the JR pieces partition the remaining edges.

For a fixed vertex on either side, choose the d positions, the opposite
letter at the first position, then one of the JR incidences on its suffix.
This gives precisely the claimed lambda0 bound. Applying the independent
inner partition in each of the d changed outer coordinates gives
binom(h,d)*lambda0^d. No additional q or t factor has been omitted.

## Parameter growth and both transform branches

Expanding the displayed load yields

    log lambda <= h(d+1) + d t + d(d-1) log c + c d log(t+1).

Together with log D <= h t + O(log h), this proves J6 with constants
depending only on c. The former d(d-1)log t term really is replaced by
O_c(d log(t+1)); no other occurrence of the old product partition remains
in the source call invoice.

At d in [100J,200J), t<=3+x/d^2, x=K_c J^3, the excess is at most

    .03 x/J + O_c(J^2 + J log(4+K_c J)).

An absolute K_c depending only on c makes the latter at most x/(4J),
uniformly for J>=3. The log(x)/x ratio decreases after a fixed initial
range, so the same holds for all larger x. Absolute call constants,
leading padding and the reserve term fit the retained strict margin.
N<=m^5 follows once x>=12d^2 and creates no J^3 log J requirement.

The rational Walsh branch uses its separate binary-label distance L of
order J. At x=K_c J^3 its extra routing logarithm is
O(x/J + J log x). The second term is O(J log J), below the order-J^2
margin. Increasing the fixed Fourier-distance constant reduces the first
term's coefficient. Thus that branch does not restore the lost log J.
Its rational coefficients are not specialized into characteristic two.

## Constructor, physical profile and inversion

The finite universe has n0=q^(d-1)<=m^5, and the permitted side load B has
log B=O_c(d+log(t+1)), hence B<=m^{C_c}. At most n0 B nonempty rectangles
occur. Encoding both sides of every candidate rectangle and the whole
candidate list uses polynomially many bits in m. Exhaustive list search
therefore costs at most 2^{m^{C_c}} actual operations and cells, including
support, disjointness, coverage and load checks. This is an explicit finite
search bound, not an appeal to mere computability. Under JR, one fixed c
can be hardcoded into the conditional machine; constants need not be
uniform over all possible witnessing c.

The new partition changes neither the finite count formula nor the
coefficient algebras. Polynomially many endpoint maps of polynomial bit
height, followed by the prior expanded compiler, fit the same singly
exponential finite profile P_m<=2^{m^{C'_c}}. Substituting log m=O_c(J^3)
into the already proved common-cap profile gives

    log D_J, log L(N_J) <= 2^{C_c J^3}.

Sparse inversion with J within a factor two of
(log s/(2C_c))^(1/3) proves eligibility and leaves log H=O_c(s/(log s)^(1/3)).
The fixed scheduler supplies the actual machine; the analysis does not
provide the candidate index as nonuniform advice. Common visited-space
caps, failed attempts, fallback and numerical precision are inherited
unchanged from the specifically named predecessor transfer.

## Limits

No proof of JR is supplied by the cover, finite C(4,2) example or rank
calculation. The conditional envelope improves the preceding explicit
upper scale only when JR holds. This review does not claim a practical
cutoff, formal build, human refereeing or priority for the graph hypothesis.
The competing E002/S003 physical-profile work may supply a stronger
unconditional bound; that does not invalidate this exact finite-graph-to-
template transfer or make it an unconditional improvement.

## Update: Section 9 and the compact profile at c65aac1156a46d10c0ef2aa36fd846c7a93518e1

The new E002/S003 complete profile supplies the unconditional benchmark
`H<=2^{O(s^(3/4)(log(s+2))^(1/4))}`. The older conditional expanded-profile
envelope reviewed above is therefore no longer a frontier improvement.

I read the lead's complete new Section 9, S003
`route-b/explicit-dyadic-geometry.md`, the E002
`lead/polynomial-profile-theorem.md` composition chain, and S003's complete
independent polynomial-profile review. **The stronger JR conditional
implication H<=2^{O_c(s^(3/4))} passes.**

The dyadic star geometry needs each outer rectangle to be a product of
inner subsets L_a,K_a, with disjoint sides on changed outer coordinates.
JR changes the inner subsets but retains both requirements: the source's
outer product is unchanged, and the fixed first unequal letter makes
L_a and K_a disjoint. Their arbitrary internal correlations are harmless;
the star basis uses one feature per whole inner word and does not require
each inner subset itself to be a coordinate product. The cross/within
Gram values remain exactly d/0. Thus the small-dyadic reserve-only lists,
fixed radix 3, succinct coefficient executor and recursive bill remain
valid for the JR partitions.

The partition has polynomially many bits in m. Exhaustive search reuses
one candidate-list buffer, one counter and polynomial-size graph checks,
so its workspace is polynomial m while time is at most 2^{m^{C_c}}.
The resulting endpoint certificates and runtime descriptions have
polynomial size. Search is additive setup, never repeated per input
record or represented as a polynomial-time constructor.

For a successful scheduled attempt, impose the analytical eligibility
condition n>=g_J in addition to the previous chunk/shape guards. Then
the actual generator costs at most n and its polynomial workspace fits
the marked regions after the existing guard enlargement. Neither the
machine nor the schedule needs to know the eventual cutoff to run: time
and visited-space caps still abort incomplete attempts safely.

The chunk count remains r=m^{O_c(1)} because retained data and proportional
execution space, unlike total search time, are polynomial in m. The
prefix-code penalty depends polynomially on the diagonal index of
(h,log r), hence only polynomially on log m and h. It does not encode
the elapsed generation time into the successful attempt's index. The
completed attempt therefore has coefficient D_J=m^{O_c(1)}, with
generation absorbed as one initial O(n) cost.

Since log m=O_c(J^3) and g_J<=2^{m^{C_c}},

    log D_J=O_c(J^3),
    log L(max(N_J,g_J))=O_c(log m)=O_c(J^3).

Taking dyadic J within a constant factor of s^(1/4) makes this threshold
strictly smaller than s eventually and gives

    log H <= O_c(J^3)+s/J=O_c(s^(3/4)).

Thus Section 9 preserves the fixed prefix schedule and common O(n)
visited cap. It conditionally removes the (log s)^(1/4) factor from the
new displayed logarithmic-overhead scale. It does not prove JR or the
endpoint. The accepted compact physical profiles remain named written-
proof dependencies; no full tape execution, formal build or human review
is asserted by this independent composition check.
