# Comparison with concurrent E003 star-routing work

Disposition: **useful exact normalization and a sharper next interface;
no missing contraction or stronger global bound supplied**.

This is a targeted mathematical comparison, not a full independent audit
of E003's implementation or verifiers. I read the three requested notes
in full and checked their central operator identities and support
arguments against E002 WB/SS/WC. I also read the complete retained
`routes/B/pairwise-newton-division.md` for the seed coefficients. The full
pinned Fourier kernel was read earlier during this protected route.
I did not rerun E003's checkers or independently repeat its tape audit.

Concurrent checkpoint: `8fbe12b3c76979ce11355a63bddfcdfcd4227585`.
Read snapshots, relative to the E003 session directory:

- `route-a/ROUTING-STAR-TRANSPOSE-NORMAL-FORM.md`:
  `3a912cee9d62478f04189b001b409ba096f168aa6d81ef0e5771ad43d3246ce2`.
- `route-b/STAR-SHARED-SUM-OBSTRUCTION.md`:
  `f7a992b0f438efd9521eb2ffe055a5ee3d926099ae9ca55c0fddd60c1ede3511`.
- `lead/review-star-routing.md`:
  `c991bd1059fd555135b7879444d30ed31f5081bfaa754e1b7a87168c1e2b1684`.

## 1. What the exact pair normal form adds

E003 defines the actual binary pair kernel C_f, including normalization
and quadratic phases. With P_j swapping one auxiliary pair register and
query pair j, C_0^2=I and P_j C_0=C_j P_j give exactly

    P_j C_j C_0 = C_0 P_j C_0.

The denominator in C_f is 2^f, while the pair-register alphabet is
Q=2^(2f). The distinction is correct and matters for normalization.
For any orthogonal norm-one source/destination pair, the span of their
two directions is nondegenerate. Auxiliary changes into that plane and
its perpendicular complement are independent of j. The complete pair
transfer therefore has the exact form

    O_j = L P_j R,

with common invertible auxiliary endpoints L,R, not merely the same
underlying address permutation. This is stronger than E002 SS's explicit
q=4,L=2 source witness: it absorbs the actual phases and applies to every
individual orthogonal pair. It is compatible with SS's corrected complete
composite registers and does not exchange spectator query halves.

It also extends the applicability of SS's termwise scalar-diagonalization
obstruction at this exposed cut: O_j O_1^(-1) is conjugate to P_j P_1^(-1),
so the noncommuting relative-star witness survives arbitrary common
endpoints. This is an individual-pair statement. Pair-adapted endpoints
can depend on both labels. Executing them separately on all pairs may
lose the source's rectangle sharing and is not a better complete invoice.

## 2. The support obstructions complement WB/SS/WC

A's exact m-term bound follows from one output row with m distinct input
neighbors. It excludes replacing the star sum by fewer monomial terms,
even with signed pointwise weights and common monomial gauges. It does
not exclude factorizations or shared physical movement.

B permits reuse of partial sums but restricts gates to preserve support
unions. On injective tuples, two different hub-swap neighborhoods intersect
in at most one input. Hence a partial sum involving at least two variables
cannot feed two such outputs, giving the stated (m-1)(Q)_(m+1) scalar-addition
count. The union-bound density guard Q>=m(m+1) is valid. Repeated symbols,
non-hub permutations and cancellation invalidate the proof's specific
premises, as the note expressly records.

These do not contradict WB. Its common basis uses nonmonomial one-bit
Walsh transforms and their inverses, and permits polynomial-m scalar
arithmetic. Even an Omega(m) addition count per record is compatible with
a much smaller expensive address-movement coefficient. The support bounds
must not be multiplied by sqrt(f) or summed across signed source rectangles.

Nor do these notes resolve WC's occupied-parameter contraction. They do
not supply the Q^2 broadcast state, remove WC's nonzero cross-row blocks,
or repair the explicit literal lift. The pure-SWAP bridge tests can now
be considered at E003's exact individual-pair middle cut; their remaining
scope restrictions still apply.

## 3. A cheap exact seed change gives a precise next target

The Newton query coefficient at seed t in F_2^r is a common scalar times

    chi_j(t)=(-1)^(a_j dot t),   r=ceil(log2(m+1)),

with distinct nonzero a_j. Let H_r be the unnormalized Walsh matrix on
the complete W=2^r seed rows, so H_r^(-1)=H_r/W. Character orthogonality
immediately gives

    H_r^(-1) diag(chi_j) H_r = X_(a_j),

where X_(a_j) translates the seed address by a_j. Thus the signed weighted
star middle operator is conjugate to

    S_coupled = sum_j X_(a_j)^seed tensor P_j.           (CS1)

This is a genuine basis change on all independent seed rows. No seed is
initialized to zero, no row is discarded, and there is no Q^2 parameter
contraction. The old seed identity is restored by the inverse basis change.

The seed has only O(log m) bits. Applying its transform uses that many
one-bit transforms; each is an ordinary O(V) scan/split/merge after moving
a single specified address bit. Hence the entry/exit change costs
O(V log(m+2)) ordinary tape work, O(V) reused payload space, and logarithmic
norm growth O(log m). It does not invoke a long f-field transpose.
This elementary implication does not require treating an address word as
a constant-time arithmetic object. It is not a new full routing theorem.

All Newton stages have the same character pattern; their common rational
factor and stationary term change by stage. Consequently CS1 is one fixed
nontrivial routing operator across those active updates. Other seed-row
maps must be conjugated as well if the seed basis is retained; this is
small-row algebra to be charged, not permission to omit their work.
CS1 remains a sum of m coupled permutations. The seed translations commute,
but the hub swaps do not, so this observation does not diagonalize CS1.

## 4. The physical interface that would actually advance the bound

The useful local target is an executor for CS1 (equivalently the signed
star sum) on arbitrary complete query/auxiliary pair registers and complete
seed rows, with fixed payload-array count, restored spectators, actual
head movement, and compact coefficient/precision control. Polynomial-m
scalar work is allowed and must be distinguished from long-field routing.

For the E002 NI5 target, after including all labels and shared endpoints,
one complete pencil would need a volume-normalized f-field address bill
of at most the stated subpower kernel allowance. Theta(sqrt(m)) predictor
stages would then give the allowed sqrt(m) total primitive-volume factor.
An individual-pair improvement is insufficient unless it lifts to whole
free rectangles without a new source/destination-pair multiplier.

WB currently costs a whole-active-width sqrt(a) term per rebuilt pencil,
where a=Theta(mf), not the desired sqrt(f)-scale bill. Neither E003 note
removes that distinction or proves that WB's basis survives the complete
rectangle sum. Shared routing with O(m) scalar additions per record,
or a priced cancellation-based basis for CS1, remains a coherent target
consistent with all the scoped obstructions.

The unconditional bound stays E002 V. RV-I/RV-W and the complete NI5 bridge
remain open. Credits for the general exact pair normal form and support
results belong to concurrent E003; E002 contributes this comparison and
the explicit short-seed interface calculation. No literature-priority,
full-machine execution or formal refinement is claimed.
