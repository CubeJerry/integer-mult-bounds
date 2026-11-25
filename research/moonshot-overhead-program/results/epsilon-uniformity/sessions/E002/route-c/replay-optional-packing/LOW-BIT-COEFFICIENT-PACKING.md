# Packing a low address block into coefficient coordinates

Status: **proved wrapper, conditional only on the declared arbitrary-E
high-field interchange**. This is the E002 lead's proposed low-bit wrapper,
written and independently checked by Route A. Its vector-space principle
is the same full-rate scalar descent already explicit in concurrent E003
`route-a/FULL-RATE-BINARY-FIELD-PACKING.md` (SHA256
`a2ee7273eb75e258e5e63bb7f85db998a185173c2012239c905a367fdee8da09`).
That general changing-field component retains E003 provenance. The present
wrapper specializes it to peeled low address bits and a common root field.
It is optional and does not alter admitted V's existing encoding proof.

## 1. Exact interface and statement

Let an arbitrary bit array occupy

    [P] x [2^U]_X x [G] x [2^U]_Y x [B],

with volume V=P G B 2^(2U), where all ranges are complete and positive.
Let d=2^t with 0<=t<=U, and let E=F_(2^d) be given in an explicit d-bit
F2 basis. Assume a fixed-tape routine interchanges two (U-t)-bit address
fields on arbitrary E-valued input, retaining every coefficient coordinate
and arbitrary spectator ranges. Its input bit volume is used in its cost.

**Lemma LP.** The full U-bit X/Y swap is obtained from one invocation of
that routine, O(tV) ordinary bit moves, and the separately charged field
preparation. The routine receives exactly V encoded bits, with no zero
extension or input-volume inflation. The additional payload workspace is
O(V), with an absolute tape count and marked-region reuse.

The high-field routine may use the same root E at every internal depth.
This is the arbitrary-E internal processor already used before the final
initial-bit embedding in V. Calling the public bit-embedding wrapper again
would not satisfy the stated no-expansion contract.

## 2. Packing and the high swap

Write X=(X_H,X_L), Y=(Y_H,Y_L), where each low field has t bits and
therefore d values. The physical layout is

    [P] [X_H] [X_L] [G] [Y_H] [Y_L] [B].

For each fixed (p,x_H,x_L,g,y_H,b), pack its d independent Y_L bits as
one E value in the supplied basis. First move the complete d-valued Y_L
coordinate past the trailing B range. Since d is a power of two, this is
t ordinary binary coordinate moves, costing O(tV) time and O(V) visited
payload cells. The resulting physical layout is

    [P] [X_H] [X_L] [G] [Y_H] [B] [coefficient_d].

There are V/d E elements and exactly V binary coordinates. Every basis
coordinate was occupied by an independent original input bit. With X_L
and G collapsed into the arbitrary gap range, invoke the high-field routine
on X_H and Y_H. Its output layout is

    [P] [Y_H] [X_L] [G] [X_H] [B] [coefficient_d].

Its completed target is the high-coordinate permutation tensored with the
identity on E. Consequently the coefficient index still represents the
original Y_L value, independently for each original trailing payload bit.
No premise of a zero coordinate or initialized module row is used.

## 3. Unpacking and the low swap

Move the d-valued coefficient coordinate back across B, now interpreting
its basis bits as the original Y_L coordinate. This gives

    [P] [Y_H] [X_L] [G] [X_H] [Y_L] [B].

Directly interchange the t-bit fields X_L and Y_L across the intervening
G and X_H ranges. At most a constant times t elementary binary coordinate
moves suffice, giving

    [P] [Y_H] [Y_L] [G] [X_H] [X_L] [B].

This is exactly the desired full swap, including the order of both low
fields and all trailing payload bits. Every operation is a permutation
of the original V bit positions except the reversible interpretation as
field coordinates. Successive binary moves reuse marked buffers, so
the wrapper visits only O(V) additional payload cells. No number of
prefixes is converted into a number of tapes. This proves Lemma LP.

## 4. Choosing the common field

Suppose the high routine needs at most B_max distinct check nodes, with
B_max polynomial in the root width U. Choose d to be the least power of
two at least max(2,ceil(log2 B_max)); then d=O(log(U+2)) and
`t=log2 d=O(log log(U+4))`. The finite guard t<=U is checked before this
wrapper; failing inputs use the existing direct routine. A sufficiently
large U has U-t comparable to U, so a root upper bound for all node
requirements continues to cover the reduced high fields.

Root field preparation is charged separately. Even an exhaustive
construction taking polynomial in 2^d operations costs U to an absolute
constant power, and is absorbed by the ordinary input-volume allowance
V>=2^(2U) for sufficiently large U. Polynomial-time basis arithmetic
is charged in the high routine, rather than treated as a unit-cost oracle.

This wrapper removes the initial degree-d zero embedding. It does not
by itself remove any remaining incidence reserves, scalar arithmetic,
spatial padding, or coefficient-selection cost inside its supplier.
In particular its O(V) extra space is not a claim that an arbitrary
supplier has O(V) total space. The admitted V theorem is unchanged.

## 5. Verification scope

A finite checker accompanies this note. It gives every original position
a distinct token, executes the stated packing, high-field permutation,
unpacking and low-field permutation, and compares the complete output
with the full-coordinate-swap specification. This tests the layout
identity for all basis coordinates, not just zero-embedded input.
The tape-time and all-width assertions follow from the written primitive
composition; a finite layout test is not their proof.

Credits: E002 lead for this proposed wrapper; concurrent E003 Route A
for the general full-rate binary field-packing component; the pinned
source's exact spatial permutations; @CubeJerry and substantial ChatGPT
multi-agent assistance.

Finite replay result: 360 complete layouts and 835,488 position checks passed,
including 270 nontrivial packings. Omitting the low swap and reversing the
coefficient basis each failed in all 270 applicable negative controls.
See `verify_low_bit_packing.py` and `low-bit-packing-verification.json`.
