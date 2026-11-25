# Joint rectangle partitions and the routing logarithm

Checkpoint disposition: Section 9 conditional JR transfer admitted after A/lead review; JR remains open. See `lead/FIRST-WAVE-ADMISSION.md` relative to the session root.

Status: **expanded-profile transfer independently reviewed; compact-profile
extension below under review**.
The partition hypothesis is open. A cheap cover does not establish it.

## 1. Finite hypothesis

For q>=2 and k>=1, let C(q,k) have left and right copies of [q]^k,
with an edge (x,y) exactly when x_i != y_i in every coordinate.
A rectangle is A x B contained in the edge set; its sides need not be
coordinate products. Count incidences separately on the two sides.

**JR.** There is an absolute integer c>=2 such that, for every t>=1,
q=2^t and k>=1, C(q,k) admits a disjoint rectangle partition with each
word in at most c^k(t+1)^c rectangles on each specified side.

This is a finite graph statement, not a time-bound assumption. Nonempty
rectangles number at most q^k c^k(t+1)^c. No efficient constructor is
assumed; bounded exhaustive search will suffice for the expanded profile.

## 2. Cover versus exact transfer

**J1.** C(q,k) has a rectangle cover with at most
ceil(4^k(2k ln q+1)) rectangles. Independently assign every alphabet symbol
in each coordinate a fair bit, taking products of the zero and one sets
as the two sides. A fixed edge is covered with probability 4^-k. For R
trials, the union bound on uncovered edges is at most
q^(2k) exp(-R 4^-k), which is below one at the displayed R.

This cover does not give exact edge multiplicity one. Over F2 an edge
covered twice vanishes; over Q it has coefficient two.

**J2.** In any field whose characteristic divides q, C(q,k)'s adjacency
matrix has rank q^k. Indeed J_q^2=0, so I_q-J_q is invertible with
inverse I_q+J_q; tensor powers are invertible. Thus any exact weighted
sum of rank-one rectangle matrices needs at least q^k nonzero summands.
The short random-cover list cannot be made exact just by weights when
it has fewer than q^k rectangles. This does not disprove JR, which permits
many more smaller rectangles. If every summand's source side has at least
S vertices, its maximum source load is at least S by counting incidences.
The destination statement is identical.

## 3. Distance-label rectangles

Retain d=2^r>=2, h=2d-1, U=[q]^h, with far inner pairs at Hamming
distance d. Outer labels are V=U^h, N=q^(h^2). The matrix P* marks the
diagonal and pairs differing in d outer coordinates, all changed inner
pairs far. For a far inner pair fix its d changed positions and common
letters elsewhere; fix both ordered letters at the first changed position.
Apply JR with k=d-1 to the remaining positions. The resulting disjoint
partition has per-side load

    lambda0 <= binom(h,d)(q-1)c^(d-1)(t+1)^c.

Each side varies in at most d-1 positions, hence has no internal far pair.
The source outer product then has load

    lambda <= binom(h,d) lambda0^d.

The far-inner count is zero within a side and d across sides. These are
exactly the Gram values needed by the source endpoint-layout proof.
Its low-rank singleton and rectangle deliveries remain valid. The scalar
matrix, rational Gram form and target permutation are unchanged, with

    rank_F2(P*)/N <= 2^(2d^2-2)q^(-d^2),
    D <= 2+h q^h.

## 4. Smaller arity under JR

Put x=log2 m and take the least power of two q with
q^(d^2)>=2^(2d^2-2)m. Then t<=3+x/d^2 and m rank(P*)/N<=1.
The previous bounds and binom(h,d)<=2^h give

    log2[D(1+lambda)]
      <= (3d-1)t + O_c(d^2+d log2(t+1))
      <= 3x/d + O_c(d^2+d log2(4+x/d^2)).                 (J6)

The old product partition had d(d-1) log2 t instead of the new
O_c(d log2(t+1)) term. For J>=3 choose the least power of two d>=100J.
There is an absolute K_c such that x>=K_c J^3 supplies the full call
margin at rho_J=1/2+1/(2J). The first term of J6 is at most 3x/(100J).
The rest is at most C_c[J^2+J log2(4+x/J^2)], which fits x/(4J)
at x=K_c J^3 after enlarging K_c. Its ratio to x decreases thereafter.
Absolute factors in the full call bill and reserve restoration fit the
remaining margin. All geometric guards, including N<=m^5, hold eventually.

The numerical Walsh branch is unchanged. Its distance parameter is of
order J and its extra loss is O(x/J+J log(3x)); at x=K_c J^3 the second
term is smaller than the available order-J^2 margin. Both interfaces thus
pass the actual acceptance inequalities with

    log2 m_J = O_c(J^3).                                  (J7)

Search m=2^u+1 with u a power of two; the first guaranteed trial is within
twice this log-arity scale. S003's nested-label obstruction assumes the
old literal partition, so it does not contradict J7.

## 5. Bounded construction

The JR universe has n0=q^(d-1)<=m^5 elements under these guards, and
the allowed load B=ceil(c^(d-1)(t+1)^c) is polynomial in m. A partition
has at most n0 B nonempty rectangles. Encode each side by n0 bits and
enumerate lists up to this length, checking support, multiplicity and
both loads by integer arithmetic. The entire search has time and space
at most 2^{m^{C_c}}. JR guarantees a successful list. Each trial search
has this explicit finite cap, so even unsuccessful earlier trials halt.

Then form the actual endpoint maps, rational bases, rank factors and
scalar instructions with the accepted source compiler. All dimensions,
incidence counts and rational bit heights are polynomial in m before
expansion. Numeric address magnitudes, radix search, predictor matrices,
finite algebra and numerical Walsh data fit

    P_m <= 2^{m^{C'_c}}.                                  (J8)

This is an actual constructor bound. No arbitrary effective generator
is assigned a convenient runtime. The coefficient algebras remain separate.

## 6. Complete conditional expanded-profile envelope

**Theorem J3.** JR and the programme's already proved fixed-field
construction and physical compiler imply one fixed exact deterministic
finite-alphabet multitape full-product machine with O(n) visited cells and

    T(n)=O(n sqrt(L(n)) 2^{O(s(n)/(log2 s(n))^(1/3))}),
    L(n)=1+log2 n, s(n)=log2 L(n).                         (J9)

JR is the sole additional mathematical hypothesis. The source and local
compiler proofs remain named unconditional dependencies, with their stated
written-proof and formalization limits.

Proof. The unchanged numerical preparation, physical compiler, common-cap
chunk convolution and prefix-weight schedule give candidates of exponent
1/2+1/J with

    log2 D_J, log2 L(N_J) <= 2^{C_c J^3}.                 (J10)

J7 and J8 are exactly the changed growth estimates. As in the accepted
fixed-field theorem, the bill includes generation, numeric addresses,
scalar operations, precision, head movement, reserves, padding, retained
descriptions, erasure and unsuccessful attempts. The chunk wrapper uses
one O(n) visited cap. A correct fallback handles all excluded lengths.
Take Y=(log2 s/(2C_c))^(1/3) and the largest sparse power of two J<=Y.
For sufficiently large s, J>Y/2 and 2^{C_c J^3}<=sqrt(s)<s, so the
candidate is eligible. Then

    log2 H <= O(1)+sqrt(s)+s/J = O_c(s/(log2 s)^(1/3)).

This candidate choice only bounds the fixed scheduler's performance; it
is not nonuniform advice. QED.

Against the preceding explicit programme envelope, the displayed upper
scale for log H improves by (log2 log2 s)^(-1/3). This compares explicit
envelopes conditionally, not actual runtimes or an unspecified published
o(1). It does not reach a fixed-beta 2^{O(s^beta)} envelope, polynomial
overhead in s or the constant endpoint.

## 7. Positive control and its asymptotic limitation

For C(4,2), the 16 rectangles indexed by (a,b) in [4]^2,

    A=([4] minus {a}) x {b}, B={a} x ([4] minus {b}),

partition all 144 edges and have load three on either side. Their number
is minimal by J2. The binary product partition has load four. The finite
MILP experiment rediscovered this simple opposing-star product; its
rounded certificate was checked by exact integer counts.

For q=4^u, first-difference base-four partitions with opposite star
orientations on pairs of coordinates give load 3^{k/2} u^k for even k.
This improves the binary product load (2u)^k by (sqrt(3)/2)^k, while
retaining the power u^k. In the two-level label invoice it changes only
an O(d^2) term, not the binding d^2 log t term. Further constant tuning
inside this family is therefore not a route to J9.

## 8. Sources and next gate

OpenAI math pin: 3344da59991ed94f9ba711217b29c1d760badfa6, complete tape
build/interchange.tex read. Programme pin: a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32.
Dependencies read: routes/B/characteristic-two-label-geometry.md,
routes/A/fixed-field-extraction-theorem.md, routes/A/physical-compiler-ledger.md,
and S003 route-a/nested-label-invoice-barrier.md.

Trevor Pinto, *Biclique Covers and Partitions*, EJC 21(1), P1.19 (2014),
distinguishes local covers from partitions and proves that bounded local
cover number does not bound local partition number for arbitrary graphs.
The primary definitions and introductory theorem statements were read:
https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i1p19/pdf/
That result does not resolve JR.

Ghosal and Karrenbauer, *Engineering Insights into Biclique Partitions and
Fractional Binary Ranks of Matrices*, SEA 2025,
https://doi.org/10.4230/LIPIcs.SEA.2025.18, studies Kronecker powers and
fractional partition parameters. Its introduction and definitions were
read; no fractional or Boolean result is imported as an exact partition.

The decisive next question is JR or an exact replacement with load
exp(O(k)) poly(log q). A cheaper cover is insufficient; every conversion
must expose its added load. Finite feasibility is not an unbounded family
proof. No claim of priority, formal build or human review is made.

Credits: the OpenAI sources and rectangle/index-coding predecessors;
S002 labels and S003 invoice obstruction; the cited graph literature;
@CubeJerry; substantial ChatGPT research assistance.

## 9. Compact-profile update after the concurrent result

At remote `c65aac1156a46d10c0ef2aa36fd846c7a93518e1`, S003 and E002 have admitted a polynomial-m
physical profile. Their unconditional envelope is
`H<=2^{O(s^(3/4)(log2(s+2))^(1/4))}`. Section 6's expanded-profile bound
is therefore no longer a useful improvement over the current programme
baseline. It remains a valid conditional historical derivation.

The new construction permits a stronger transfer under exactly JR:

    H(n)<=2^{O(s(n)^(3/4))}.                              (J12)

Here is the additional dependency check, rather than silently replacing
one compiler by another. S003's explicit-dyadic-geometry theorem, Section4,
requires outer rectangles L=product L_a, K=product K_a, with disjoint
inner sides in each changed coordinate. It does not require those inner
sides to be Cartesian products of alphabet subsets. Our first-coordinate
anchor makes the JR sides disjoint, and the outer construction is a product.
The same explicit star bases, small dyadic elementary maps, reserve-only
preparations and fixed address radix3 therefore apply. The doubled address
dimension changes only absolute constants in J6.

All lists for a returned JR partition have polynomial-m size. Compact
scalar-factor execution, check-space repair, packed batching and numerical
Walsh are unchanged. Their local work and proportional space remain
polynomial in m. The only lost polynomial-time premise is the search for
the partition. This can be separated honestly: enumeration stores only one
polynomial-length candidate, its counter and polynomial-size verification
data. Its **time** is at most g_J=2^{m_J^C}, but its workspace and retained
description are at most m_J^C. Rejected bounded trial searches fit the same
profile after enlarging an absolute C depending on c.

Run the same fixed prefix-weight schedule. For a successful candidate,
add n>=g_J to its eligibility threshold. Actual generation then costs
at most n. The chunked execution still has coefficient m_J^{O(1)} and
one common O(n) visited cap. Increasing N_J to max(N_J,g_J) costs only
O(log2 m_J) in log2 L(N_J), since log2 log2 g_J=O(log2 m_J).
Consequently the actual successful attempts satisfy

    log2 D_J, log2 L(N_J) <= C_c J^3.                    (J13)

This does not assume generation is cheap per data item or omit it from
the schedule; it charges one bounded initial search and includes its
threshold. Take a dyadic J within a constant factor of s^(1/4). Then
J^3=o(s), giving eligibility for all sufficiently large n, and

    log2 H <= O(1)+C_c J^3+s/J = O_c(s^(3/4)).

The derivation yields J12, conditional solely on JR relative to the named
compact physical construction. Compared with the current unconditional
upper scale, its log-overhead is smaller by (log2(s+2))^(-1/4).
JR remains open, and J12 is not an unconditional improvement, endpoint
result or polynomial-s overhead. Independent review of this updated
composition is required before its admission.
