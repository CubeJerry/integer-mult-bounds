# Three-receiver partition obstruction for the frozen feedback source

**Source-specific theorem under the native identity-target and tight-cut contract.
Arbitrary separate nonlinear bank gauges are allowed. No new complete kappa.**

The S030 state mentioned an unfinished binary-gauge obstruction but retained no
proof or certificate for it. This package reconstructs the literal source from
the committed parameters and proves a stronger obstruction. It does not treat
the missing S030 artifact as evidence.

## 1. Exact source and quantifiers

Let F be GF(64), with modulus z^6+z+1, and let K be any finite extension of F.
Use the literal shared node table and the seed-zero width-three polynomial
feedback maps of
[the admitted source](../../bit-coupled-native-polynomial-feedback/ADMISSION.md).
For donor j in {0,61,62}, the input is x in K^48 and the quotient at plane h is

    Q_(j,h)x = ([1,a_h,...,a_h^15] tensor I_3)x
                  + (a_h^16+1)V_j x.

The nine feedback blocks are at positions 3,6,7,9,10,11,12,13,15. Their exact
SHAKE256 tags, fixed three-cycle at position3, and E_00 at position6 are rebuilt
by the new checker. The resulting complete donor coefficient hashes equal the
three hashes in the frozen S030 receipt. No author constructor or predecessor
executable code is imported.

Fix H263={0,61,62}. Its common node is49. Let I be its33 actual native receivers.
For i in I, let

    L_(j,i) = intersection over the15 visible h != H263 of ker Q_(j,h).

Each L_(j,i) has dimension3. The central quotient restricts to an isomorphism
on it, since the full sixteen-quotient source view is invertible. The checker
reconstructs these kernels from the actual 45 by48 off-H matrices, using fresh
nullspaces rather than the feedback inverse formula. All99 relevant source
cuts are checked exactly.

The target on these donor/receiver pairs is the identity proper block of the
specified S028 endpoint. Receiver80 and donor10, its exceptional stars, are
absent. The retained native route stream has720 genuine early X fields at
H263,45 exits of16 fields, and240 visible fields at each relevant receiver at
bank3840. There is no informative bypass under the stated contract. These
counts and the original source owners are independently reconstructed.

The theorem excludes completing these exact quotient information systems under
that tight cut after any independent bijection of each entire donor bank and
any separate bijection of a quotient output. H processing and downstream
decoders may be arbitrary deterministic functions. Repetitions and certain
balanced companions are specified below. No claim is made about arbitrary
changed source quotients, inter-source preprocessing, an enlarged informative
cut, a changed target, or arbitrary other companions.

## 2. Why arbitrary bank bijections must preserve the partition joins

We give the finite additive argument explicitly. Let G be a finite abelian
group, and let A,B be nonempty subsets of equal size M. If |A+B|=M, then A and
B are cosets of the same subgroup of size M. Indeed, for every b in B the
translate A+b must equal A+B. Thus B-b_0 lies in the stabilizer H of A, so
|H|>=M. Since A is a nonempty union of H-cosets, |H|<=|A|=M. Equality follows,
and both A and B are single cosets. Applying this argument twice proves the
same assertion for three sets A,B,C of size M whose sumset has size M.

Now allow an arbitrary separate input bijection g_j at each source. For a fixed
receiver i, fixing a donor's fifteen off-H observations leaves a fibre

    A_j = g_j^(-1)(u_j + L_(j,i)),

of size M=|K|^3, or the corresponding total quotient size after direct sums.
Fix the other original sources and all off-H observations. The desired output
variation is exactly A_0+A_61+A_62. The only remaining varying transcript
crosses the common H cut of M possible values. Exact recovery implies that the
sumset has at most M elements. It has at least M by fixing two summands, so it
has exactly M elements. All three fibres are therefore cosets of one common
additive subgroup.

This subgroup is independent of which fibre is chosen. Hold a fibre at one
other donor fixed and vary the selected donor's off-H observations. Every
resulting fibre must be a coset of the fixed fibre's unique stabilizer. Repeating
the argument across donors gives one subgroup S_i common to every fibre at
every donor, for this receiver i.

Consequently g_l composed with g_j^(-1) is an isomorphism between the entire
coset partition of L_(j,i) and that of L_(l,i), simultaneously for every i.
No linearity of g_j or g_l was assumed. Output bijections do not change these
partitions. This is the necessary source-compatibility step underlying the
previous tight-cut results, proved here for the exact claimed nonlinear scope.

For any receiver subset J, the join of the coset equivalence relations

    x ~_i y iff x-y lies in L_(j,i),  i in J,

has classes equal to the cosets of sum_(i in J) L_(j,i). A partition
isomorphism preserves the cardinalities of the join classes. Thus a necessary
condition, even for arbitrary nonlinear bank gauges, is

    dim_K sum_(i in J) L_(j,i)
        = dim_K sum_(i in J) L_(l,i)       for every J and every donor pair. (1)

Only finite cardinality and the additive target are used. In particular, the
argument does not assume a linear H encoder or invoke an unsupported
linearization of an arbitrary bank bijection.

## 3. Three minimal witnesses and a combined rank gap

The new checker exhausts all528 receiver pairs and all5,456 receiver triples.
Every pair has rank6 at all three donors. Every singleton has rank3. Exactly
three triples have unequal join ranks:

| Receiver subset | Donor0 | Donor61 | Donor62 |
| --- | ---: | ---: | ---: |
| {52,73,98} | 9 | 8 | 8 |
| {53,75,96} | 9 | 8 | 9 |
| {54,74,98} | 9 | 8 | 9 |

The other5,453 triples have rank9 at every donor. Three receivers are therefore
the smallest possible support for this join-rank obstruction within the33
native H263 receivers. This is a complete finite census, not a failed search
being interpreted as a universal theorem.

Their eight-receiver union

    J8={52,53,54,73,74,75,96,98}

has rank profile(24,21,23). All four displayed witnesses have explicit exact
upper and lower rank certificates: independent kernel columns and a nonzero
maximal minor. `JOIN-CERTIFICATES.json` records their rows, columns,
determinants, kernel vectors and coefficient hashes.

Each triple already contradicts(1). Hence the literal frozen feedback source
cannot complete this H interface after arbitrary independent nonlinear bank
gauges under the stated target and routes.

The rank-gap3 on J8 is an exact statement about source partition joins. It is
**not** a proof that a repaired complete word requires three additional return
fields per component. That conclusion needs a separate stability/repair-cost
argument, and none is asserted here.

## 4. Repetitions, finite extensions and companions

For r positive identical copies, the inverse fibres are L_(j,i) tensor K^r.
Their join ranks multiply by r. Any whole-bank bijection may mix the copies
arbitrarily; it still must preserve the join-class cardinalities. The triple
gap becomes r and the J8 gap becomes3r. The obstruction therefore survives all
positive repetitions and all finite extensions, as well as Frobenius-conjugate
copies, whose rank functions are unchanged.

For example,80 copies give quotient width240 and bank3840. Their J8 profile is
(1920,1680,1840), so this proposed full-bank repetition is excluded. This is a
hypothetical completion test; S030 did not publish a full-bank physical
feedback word or a paid invoice.

For direct sums of heterogeneous components, the necessary condition is more
generally equality of the sums of their receiver-join rank functions:

    sum_t rank_j,t(J) = sum_t rank_l,t(J), for all J.                  (2)

Thus arbitrary other components cannot be dismissed: unequal companion ranks
might compensate an existing discrepancy. In particular, no theorem here
excludes every possible3+12 source extension.

The literal shared-node geometric tensor source and the standard Hermite3 and
Hermite12 sources do have balanced profiles on all four witnesses:

| Companion diagram | Each displayed triple, all donors | J8, all donors |
| --- | ---: | ---: |
| Geometric tensor, width3 | 6 | 15 |
| Shared-node Hermite3 | 9 | 24 |
| Shared-node Hermite12 | 36 | 96 |

These are checked from the literal polynomial kernels. For Hermite width k,
the kernel is g(z)^k times the polynomials of degree below k, where g is the
product of the15 off-H node factors. This follows directly from the Hasse
vanishing conditions. It also proves the full16-node source invertibility by
degree and multiplicity counting. Scalar tensor widths and repetitions scale
the listed geometric profile. Consequently adding any combination of these
balanced companions cannot cancel a nonzero number of frozen feedback
components. Even arbitrary nonlinear whole-bank mixing after source emission
cannot change(2).

For a general companion added to r frozen feedback components, its J8 ranks
c_0,c_61,c_62 would necessarily satisfy

    c_61-c_0=3r,     c_62-c_0=r.

The three triple constraints impose their corresponding rank differences as
well. These are useful exact repair requirements, not sufficient conditions
for a common H word.

## 5. A separate six-twist transport certificate

The package also reconstructs the stronger linear algebra system mentioned
in S030, without relying on any missing artifact. Choose the twelve receivers

    {84,85,86,87,92,93,94,95,96,97,98,99}.

Concatenating their donor0 kernel bases gives a48 by36 matrix A of rank30.
Let R be a36 by6 full relation basis. A field-linear map carrying each source
fibre into its target fibre must have independently chosen3 by3 matrices M_i
with

    [B_1 M_1 ... B_12 M_12] R=0.                                    (3)

Conversely, respecting all source relations is sufficient to define the map
on the30-dimensional source span. There is no requirement that the M_i agree
or be diagonal. For each relative Frobenius power0 through5, substitute the
coefficientwise conjugate of each B_i in(3). Each resulting288 by108 system
has full column rank108. Six independently selected108-square nonzero minors
are recorded in `TRANSPORT-MINORS.json`.

Every F2-linear map on F^48 is uniquely a sum of six Frobenius-semilinear maps.
If it maps every F-linear source fibre into its target fibre, applying it to
lambda*x for all lambda in F and projecting modulo the target fibre separates
the six semilinear terms. The resulting vector polynomial has degree at most32
and vanishes on all64 values. Thus every term separately transports the
corresponding twisted diagrams. The six systems force all such terms to
vanish on the nonzero source core. No invertible binary-linear bank transport
can therefore align these twelve fibres. Copy-block and finite-extension
arguments give the corresponding arbitrary-copy mixing statement.

This six-twist result is independently useful as an exact system for choosing
future correlated feedback parameters. It is not necessary for the simpler
nonlinear partition contradiction of Sections2–4. Neither result excludes the
entire universal feedback family: the literal seed-zero coefficients matter.

## 6. Verification, controls and next question

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 python -I -B research/moonshot-005-program/results/bit-shared-h-s031-review/feedback-partition-gate/check.py --repo . --out FRESH
```

Expected output:

```text
PASS_FROZEN_FEEDBACK_NATIVE_PARTITION_OBSTRUCTION 99 528 5456 [24, 21, 23] 6 108
```

The checker authenticates all used source bytes; reconstructs actual roots,
planes, source quotient matrices and owner routes; obtains fresh full off-H
nullspaces; checks all pairs and triples; emits both sides of each rank
certificate; and checks the six-twist systems. It includes a positive identity
transport, balanced geometric/Hermite companion controls, the disappearance
of each triple discrepancy when any one receiver is removed, and a duplicate
minor row that lowers the transport certificate rank from108 to107.

The next constructive problem is to choose correlated feedback parameters
and shared source coordinates satisfying the same native partition diagram
at all centres. Matching the rank functions in(1) is necessary and may be
tested early; it is not sufficient for a simultaneous transport or physical
H word. The full H/D/K/facet endpoint, near-nine-bank return, paid physical
word, compatible strict suppliers and complete recursive theorem remain
separate obligations. This package discharges no foundational assumption and
establishes no new complete kappa.

Credit @CubeJerry and the retained native-atlas, shared-node, polynomial
feedback and tight-cut authors. The finite-field and exact root-coordinate
methods follow the independent Hermite review, with fresh source nullspaces,
different pivot choices and no executable imports. S031 Worker C developed
the nonlinear partition-join obstruction and the new exact certificates with
substantial OpenAI assistance. Independent review is recorded separately.
