# Native nine-port modules over one common GF(32)

## Positive theorem and scope

Every A2 plane of the pinned 120-root completion admits a partition of
its 45 actual D4 exits into five classes of nine. Each of its 36
perpendicular parent receivers sees exactly three exits in every class.
This supplies smaller explicit causal local interfaces at all 1,119
active native planes, over F=F2[z]/(z^5+z^2+1). Full three-donor planes
use 9-by-9 maps, two-donor planes use one universal 18-by-18 two-wave
design, and singletons use an 18-by-18 Hermite design.

The original formal quotient dimensions and physical holder counts
are unchanged. Every ordinary receiver target has dimension 360 and
projects invertibly onto each donor quotient. At a singleton, the
receiver gets rank 360 in the real 540-dimensional source input.

The complete local construction costs at most 184,523,130 binary
whole-record ADDs, 627,750 stationary INITs and the same number of dirty
CLEARs, with no additional MOVE. One field copy is five binary native
copies. These local figures do not replace the complete supplier invoice.

This constructs local modules for source gluing, not a glued native
source atlas. Same-original-input compatibility, global early inverse,
later proper transport, return bank and recursive costs remain open.
No new kappa is claimed. A low-rank endpoint target does not by itself
give a physical realization through these modules.

## Exact native partition

At base plane H=3, number its 45 exits by increasing global D4 index.
The five classes of local ordinals are:

    0,8,13,14,20,24,27,34,44
    5,12,15,22,23,28,31,36,43
    1,9,17,21,25,26,32,37,41
    3,4,11,16,19,29,33,39,40
    2,6,7,10,18,30,35,38,42

`BASE-PARTITION.json` records their global port indices and the 36
receivers. A binary integer search discovered this positive witness;
validation uses only exact integer root incidence.

For roots of squared norm four, reflections have formula

    r_s(v) = v - (v dot s)/2 * s.

All relevant dots are even. Identify each reflected root up to sign
in the pinned table. The checker verifies the permutations of 120 root
lines and traverses their A2 orbit. It reaches all 1,120 planes,
transporting the classes. Predecessor reflections and all transported
partitions appear in `output/PARTITIONS.json.gz`.

For each plane, a separate direct check verifies its classes partition
its actual 45 exits and all 36 receivers see three ports in every class.
This covers all 40,320 parent receiver-plane incidences. Native counts
are 29,354 at full planes, 7,549 at two-donor planes, and 360 at
singletons. No missing parent root is used as a genuine native donor.
No novelty is claimed for the abstract finite geometry behind the
finite partition certificate.

## Full three-donor module

Within a class, number the nine ports p=0,...,8 and put

    V9[p,t]=(p+1)^t, 0<=p,t<9.

The nodes are distinct and nonzero in F. Donor j owns columns
3j,3j+1,3j+2. V9 is invertible. For any three-row set S its donor-j
projection is diag(alpha_p^(3j)) times the three-node Vandermonde,
so is invertible. The checker directly verifies all 252 such minors.

At a full plane the balanced early factor is x=4,5,6. Each physical
port has x early holders and 8-x late holders from each donor. For a
phase with t holders per donor per port, assign holder s at donor j
and local port p to stripe

    s+t*((j+p) mod3), 0<=s<t.

Each of the 3t stripes has one real holder per port and three symbols
from each donor. Every holder occurs exactly once. Apply V9 to each
stripe, paying an input-order permutation. Thus each class uses 3x
early stripes and 24-3x late stripes, with 24 total. The five classes
give 120 V9 modules and 360 source symbols per donor. Both phases
separately preserve all their inputs; late data is not used early.

Every receiver gets three outputs in each module, hence rank 360
with invertible projection onto all three complete donor quotients.
All 1,080 local source dimensions are retained. The five classes have
different receiver port patterns. This is not one fixed width-two
base map repeated on every source coordinate.

## Universal two-donor crosswave

At a two-donor plane x=6. Each port has six early holders per donor,
two late holders per donor and eight genuine direct-ground late
holders. In each nine-port class form six early stripes, each with
one holder per donor per port. A stripe's early source is
E=(E0,E1), with E_j in F^9.

Use the displayed stripe formula with t=2 and j=0,1 for late source
holders. Every stripe gets three from each donor. Fill its two
holders per port using the actual direct-ground holders. This uses
exactly eight direct-ground holders at each port. In source-column
order the late input is Y=(L0,L1,Z), with L_j in F^3 and Z in F^12.
Every one of the 18 late fields has an independent arbitrary baseline;
the first six also contain the native donor additions.

Define V18[r,t]=(r+1)^t for 0<=r,t<18. The causal map is

    early output = V18 E,
    late output = V18 Y + C E.

Cache the 18 actual early input fields before applying the early map.
`UNIVERSAL-C.json` gives one fixed 18-by-18 C used everywhere. Put
output rows 2p,2p+1 at port p. A receiver sees three ports, giving a
six-row set S in each phase. Its source transfer on donor j is

    [ V18[S,9j..9j+8]                0 ]
    [ C[S,9j..9j+8]    V18[S,3j..3j+2] ].

All 168 such 12-by-12 matrices, for all 84 port triples and both
donors, are directly checked invertible. With C=0 all their ranks
are exactly nine. The universal matrix was found at trial 395 of
the deterministic generator; that search count has no proof role.

An existence proof also works at field size 32. Let N be a 9-by-3
right-kernel basis for the early block and L a 3-by-6 left-kernel
basis for the late block. Vandermonde minors give the stated ranks.
The full matrix is invertible iff det(L C[S,9j..9j+8] N) is nonzero.
For any one constraint, the linear map C to LCN is surjective, so
this determinant polynomial is nonzero. Their product is nonzero.
Each C entry belongs to one donor block, affects a determinant with
rank at most one, and occurs only when its output port is selected.
There are binomial(8,2)=28 such triples. Its individual degree in
the product is therefore at most 28, below 32. The elementary finite
grid lemma guarantees a nonzero assignment in F.

Thirty stripes per plane give 30*(9+3)=360 source symbols per donor.
Every receiver obtains 30*12=360 dimensions with both projections
invertible. The early map and the late baseline map are invertible,
so the whole public map is invertible for arbitrary original late
baselines. The cache is stationary and used only after late arrival.

## Singleton Hermite module

Singleton ports have twelve early source fields and twelve genuine
direct-ground late fields. In each class use six stripes of two
holders per port. A stripe's 18 early inputs are the coefficients
of a polynomial f of degree at most 17. Output its evaluations at
the nodes 1,...,18 early. Output each original late baseline plus
the corresponding formal derivative value late. Cache only the
nine odd-degree coefficients.

A receiver sees six nodes, so twelve value/derivative observations.
On polynomials of degree below twelve these observations are
injective: simultaneous vanishing would make the product of six
distinct squared linear factors divide f. All 84 corresponding
twelve-by-twelve minors are checked. Thirty stripes give receiver
rank 360 in the real 540-dimensional source, and the invertible
early evaluation map retains all 540 dimensions.

## Literal ordinary implementation and accounting

Expand F in its five-bit polynomial basis. V9 and V18 become 45-by-45
and 90-by-90 invertible binary matrices. Reversed exact binary row
reduction gives the literal words in `output/ADD-WORDS.json.gz`.
Every ADD has distinct co-located source and target records. The
checker replays every independent input column. The counts are
850 ADDs for V9 and 3,554 for V18. An n-field holder permutation
costs at most 15(n-1) ADDs, without helpers or movement.

The C18 term costs 4,064 binary ADDs per stripe; the derivative
costs 1,878. Each binary cache owner pays INIT, one copy ADD and
dirty CLEAR. Full two-wave replays include all 180 independent
early and late input columns and preserve dirty cache contents.

| Local type | Planes | ADD bound per plane | INIT per plane | CLEAR per plane |
| --- | ---: | ---: | ---: | ---: |
| Three donors | 881 | 116,400 | 0 | 0 |
| Two donors | 227 | 353,160 | 2,700 | 2,700 |
| Singleton | 11 | 164,310 | 1,350 | 1,350 |

Totals are 184,523,130 ADDs and 627,750 each INIT and dirty CLEAR.
No additional MOVE occurs. These fixed finite words tensor with any
body identity. All source, global inverse, preload, subsequent
proper maps, field-extension native copies, and recursive costs
remain separately payable.

## Reproduction and remaining task

    python3 -B author/check.py --repo PATH_TO_REPO --out OUTPUT_DIRECTORY

The decompressed layout SHA256 is
`9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72`.
The factor raw SHA256 is
`346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7`.
The layout attributes native source SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.

The predecessor `bit-all-plane-causal-arrays` packages supply the
Vandermonde, crosswave and Hermite patterns. New constructive content
here is the native partition, the smaller universal maps over GF(32),
the all-triple C18 certificate, and the actual holder compilation.

The immediate next task is a same-original-donor source representation
whose inverse fibres agree with these actual receiver graph maps.
One can now use width-three modules at full planes, but they must
remain coupled across every donor's 28 planes. The smaller matrices
make a source-cycle solver more tractable; they do not solve its
equations. Changed return banks require their own endpoint contract
and cannot inherit exact canonical saturation without proof.

Credit @CubeJerry, the native root/route and balanced factor authors,
the retained local causal array authors, and S026 Worker A with
substantial OpenAI assistance. No new kappa.
