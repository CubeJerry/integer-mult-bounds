# Same-original-donor gluing on a native three-plane cycle

## Positive result and scope

Use the pinned 111-role geometry and the checked five nine-port classes.
There is an explicit source-to-visible-port code over GF(32) on this
genuine native cycle:

| Shared plane | Native lines | Varying donors |
| --- | --- | --- |
| H249 | 29,36,58 | 29,36 |
| H339 | 29,70,77 | 29,77 |
| H791 | 36,77,107 | 36,77 |

The receivers are 10,33,80,95. Each is perpendicular to all three
varying donors. The other 108 original donors are held zero in this
fragment. The third donor on each displayed plane is genuine but has
zero varying input. All sixteen planes visible to each receiver at
each varying donor are full three-native-donor planes.

For each of the five actual nine-port classes, each donor has one
common 48-dimensional original input and 28 rank-three maps of that
same input. The actual V9 array is used at every relevant plane.
All three shared planes are compatible simultaneously: one receiver
tuple at a shared plane serves both active donors. Decoders from the
visible plane-port values recover the sum of the original inputs at
every receiver.

The exact certificate verifies 420 rank-three source maps, 120 common
lift identities, and 60 receiver/donor identity blocks. At all fifteen
shared-plane/class pairs the two source row spaces have stacked rank
six. Fourteen of fifteen tested pairs of transitions at receivers
10 and 33 fail to commute.

This is a common-original-source compatibility result on a native
cycle, not a collection of independent local formal inputs. It is not
the full 111-donor code. The theorem's decoder reads actual visible
H-to-D values; their common D-to-K-to-F transport remains open. This
coefficient package does not itself certify the balanced early quotas.
Those need a separate phase assignment, discussed below. No new kappa.

## Common lift coordinates

Fix a class c. Write G=F^48 as sixteen three-dimensional blocks. Assign
blocks 0,...,11 to the twelve pairs (i,H), with i one of the four
receivers and H one of the three cycle planes. There are four
consecutive blocks per plane. Let E_(i,H):F^3->G be the corresponding
coordinate inclusion. Four blocks remain as completion coordinates.

Let A_(c,i,H,j) be the three-by-three minor of V9 on the three actual
ports of class c visible to i and the three source columns for native
donor j. Every A is invertible by the nine-port theorem. For an active
donor j on a cycle plane H, define its single source map by

    F_(c,j,H) E_(i,H) = A_(c,i,H,j)^(-1)

for all four i, and make it zero on every other block. In particular,
it annihilates all E_(i,Q) for the other cycle plane Q incident to j.
The map is defined on the same original 48 coordinates as all other
source maps of j.

This construction is performed separately for every actual class.
Its shared-plane matrices use that class's own receiver triples and
V9 minors. No agreement between the triples of different classes is
assumed.

## Private-plane linear completion

Every other plane through an active donor has just one active donor.
Call it private for this fragment; it retains its actual native ports.
At a private P choose a scalar row a_(j,P) in F^16 and put

    F_(c,j,P) = a_(j,P) tensor I3.

This row is shared by all five classes. If P is visible to i, make
its entries at the two blocks (i,H) incident to j zero. This is one
fixed source row, not a receiver-specific emission.

At receiver i remove those two coordinate columns. The fourteen
private visible planes give a fourteen-by-fourteen matrix D_(i,j).
The certificate makes all twelve D matrices invertible and supplies
a nonzero perfect matching for each.

More generally, this zero-pattern completion exists whenever every
required D pattern has a perfect matching, over any field with more
than four elements. The matching gives a nonzero determinant
polynomial. The product of the twelve determinant polynomials is
nonzero. Each allowed row-entry variable appears in at most four
determinants, with degree one in each, so its individual product
degree is at most four. The finite-grid lemma gives a simultaneous
assignment. The stored exact witness is checked directly; its search
success is not used as a proof.

## Simultaneous compatibility around the cycle

Stack the sixteen visible maps at i,j into M_(c,i,j), a 48-by-48
matrix in actual plane order. Split G into the two shared blocks
E_(i,H) and the other fourteen blocks. Private rows vanish on the
first two and form D_(i,j) tensor I3 on the others. Shared rows
restrict to the first two as the two diagonal invertible blocks
A_(c,i,H,j)^(-1). Thus M is invertible, and its inverse lift of
the H source coordinate is exactly

    M_(c,i,j)^(-1) at coordinate H = E_(i,H) A_(c,i,H,j).

The actual three visible outputs at a shared plane are

    T_(c,i,H) = sum_(active j in H)
                  A_(c,i,H,j) F_(c,j,H) X_(c,j).

Apply the single common inclusion E_(i,H). It produces the sum of
the inverse-source contributions for both donors. There is one
shared tuple, with one common decoder, rather than a private tuple
for each donor.

At private P, its V9 minor is invertible and only one donor varies.
Invert that minor and apply the relevant inverse block of M. Summing
the shared and private contributions gives the sum of all three
original donor inputs. Explicit matrix multiplication gives I48
for all sixty class/receiver/donor blocks.

The different H-fibres are not identified with one common three-space
carrying a flat scalar gauge around the cycle. Their distinct common
coordinate inclusions are part of this source representation. The
prescribed noncommuting minors fit these inclusions and the private
rows complete each donor's source basis. This reduces this genuine
native cycle to a constructive zero-pattern completion.

## Balanced early timing is a separate statement

Receiver 10's source stack is invertible, so its sixteen planes give
an abstract source basis. This fact alone does not meet the actual
quota 45*x_H at every H. An ordinary quotient has 360 fields with
fraction x_H/8 early, and donor 77 also has its singleton quota.

A concrete lift uses eight copies of each 48-dimensional class bank,
then three repetitions. At each ordinary H choose x_H of the eight
copies early. The choices at a shared H must agree for both active
donors. If every copy's early maps are a basis, three repetitions
give exactly 3*x_H early V9 stripes per class. Five classes then
give donor bank 5*8*3*48=5760 and ordinary quotient 5*8*3*3=360.

Donor 77's singleton H1008 is invisible to all four receivers.
Eight basic rank-three copies plus four extra rank-three blocks,
then three repetitions and five classes, give its actual 540 early
fields. The extra rows can complete early bases without changing
the receiver identities. Exact schedules, rank checks, singleton
complements and physical holder assignment must certify this step.
They are deliberately not inferred from dimension counts here.

The separate S026 triangle-early package was being prepared when
this coefficient package was frozen. Its result must be assessed
and cited separately before claiming the balanced causal lift.

## Reproduction and pins

    python3 -B author/check.py --repo PATH_TO_REPO \
      --nine-author PATH_TO_NINE_PORT_AUTHOR --out OUTPUT_DIRECTORY

The checker reads the frozen witness, reconstructs root incidence,
all visibility sets and local port minors, and recomputes all inverse
source and decoder matrices. It does not rerun a random search.

The layout decompressed SHA256 is
`9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72`.
The nine-port partition certificate SHA256 is
`2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25`.
The five-class source witness decompressed SHA256 is
`362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af`.

The first class-zero discovery is retained as
`output/SOURCE-CERTIFICATE.json.gz`. The builder reconstructs all
five classes from it and the actual V9 minors. Exact field arithmetic
is included in `field.py`.

## Open next questions

First certify the balanced phase lift and then provide actual common
downstream transport. The larger source question is how to replace
the twelve independent common fibre blocks by overlapping compatible
fibres when many more planes and receivers are active. The present
construction uses twelve of sixteen available blocks. The full atlas
cannot assign an independent block to every shared incidence. This
identifies the limitation of this construction; it does not exclude
a compact overlapping arrangement.

Credit @CubeJerry, the native and balanced-source authors, the checked
nine-port construction, and S026 Worker A with substantial OpenAI
assistance. No new kappa.
