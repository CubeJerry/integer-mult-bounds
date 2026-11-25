# Refined space for a variable-parameter structured interchanger

Status: **proposed complete component proof; independent review requested**.
The previous polynomial-in-m space bound alone does not imply this result.

Pins: OpenAI math at 3344da59991ed94f9ba711217b29c1d760badfa6,
November tape interchange.tex, shared-pencil delivery and spatial
partition proofs. E002 suppliers: the polynomial interchanger invoice,
succinct row execution, height-priced affine streams, on-demand spectral
repair, and the composite-radix note in this directory.

Write \(\Phi(y)=(y+1)^{2/3}(\log_2(y+2))^{1/3}\).
The accepted label inequalities give, for every sufficiently large odd m,
an integer-selected power-of-two distance with
\[
 D_m(1+\lambda_m)\le2^{C\Phi(\log_2 m)},\quad
 mr_m/N_m\le1,\quad m\le N_m\le m^5.                 \tag{VS1}
\]
Here \(\lambda_m\) is maximum endpoint incidence, \(r_m\) scalar rank,
and \(N_m\) label count. Finite descriptions and rational heights are
polynomial in m. Select the distance within an absolute factor of
\((\log m/\log\log m)^{1/3}\) using integer comparisons.

## 1. Keep one data field

At root width U choose an even power-of-two extension degree s with
\(2^s\ge B(m(U))\) and \(s=O(\log(m(U)+2))\). Keep
\(E_*=\mathbb F_{2^s}\) throughout the entire interchange invocation.
It contains \(\mathbb F_4\), and has enough distinct check nodes for
every descendant because m never increases. A descendant uses the first
B(m) distinct coordinate strings as nodes. Its Vandermonde determinant
is nonzero. Gaussian elimination and inversion by exponentiation cost
polynomial(m,s) bit operations; no enumeration of all \(2^s\) elements
is needed per coefficient.

Embed each initial bit once into one s-bit E-symbol. This multiplies
original bit volume by s once. Recursive calls retain exactly those
s-bit records. The completed swap is the identity on coefficient
coordinates, so decoding recovers the input symbols. Restricting the
arbitrary E-input identity to these embedded inputs is valid; no
independent input row has been declared initialized workspace.

Construct E once by bounded polynomial enumeration and irreducibility
tests, in polynomial(\(2^s\)) work, hence polynomial(root m) work.
Find a nontrivial F4 generator once by testing
\(\omega^2+\omega+1=0\) through the root field; its even degree
guarantees a root, and the same polynomial(root m) bound covers it.
Discard any optional expanded validation archive before data execution.

## 2. Amortize metadata by complete payloads

Fix a sufficiently large absolute integer K covering every polynomial
description, height, local scratch and field-operation bound in the
suppliers. Impose the node guards
\[
 u\ge m^K,\qquad u\ge K\log_2(s+2).                 \tag{VS2}
\]
The caller uses direct bit moves if a guard fails.

**Whole module rows.** A tagged row contains complete spatial ranges.
The completed batch and controls can be exponentially large in a
polynomial of m, but consume at most polynomial(m) address bits.
Thus the remaining row payload is at least \(2^{2u-m^{C_0}}\),
and at least \(2^u\) after enlarging the guard exponent in VS2.
Its polynomial(m) index header and polynomial(m,s) descriptor
fit inside its payload budget under VS2. Stable binary radix sorting
uses only a fixed number of arrays. Serialize every monomial term:
retain original input and output accumulator, and reuse one temporary
permutation array. The number of simultaneous arrays does not equal the
polynomial number of monomial terms.

**Rational address runs.** In the height-priced affine algorithm, a
reduced coefficient a has height polynomial(m), while the target field
has \(\log_2 Q=\Omega(u/m)\). Increasing K in VS2 makes
\(Q/a\ge m^K\). Each of the a headers has polynomial(m) bits and its
run has at least \(\lfloor Q/a\rfloor\) complete payload blocks. All
headers therefore fit in a constant times the payload. The padded
transpose grid has at most four times that volume. Inverse scaling
reverses this same short-coefficient construction, rather than treating
a large modular inverse as a new coefficient. Triangular maps serialize
their elementary operations and reuse the same regions.

**Group spectral roles before appending labels.** Predictor and padded
check row counts are R=32Bw and S=Bw, with \(2m+1\le B<6m+3\).
Move the O(log m) bits of the finite role coordinate across the following
module/spatial range by ordinary binary split/merge scans, padding the
role coordinate to a power of two and deleting the known padding only
after the complete move. This costs O(V log(m+2)) nonrecursive time and
constant-volume space, and invokes no large interchange.

Each (module,address) block then contains B E-elements for a check
stream, or 32B for a predictor stream. Append the m ternary comparison
labels once per block. Their 2m bits fit within the existing B s payload.
The source comparison construction still applies to these larger
records in the same spatial address order: a later-field fibre has
three consecutive comparison runs, and its counter arithmetic is
amortized over that complete fibre.

Form the entire small spectral matrix from this block's labels in
one reused polynomial(m,s)-bit buffer, apply it to the block by actual
sequential loops, then reuse the buffer. A matrix is never stored for
every address simultaneously. VS2 and the complete spatial volume
absorb the buffer. Flattening (check,duplicate32) and zero-padding
gives exactly B check roles per unchanged w-coordinate, including the
small true-check case. Output, original, mask and accumulator arrays
have constant total volume. Remove labels and undo role grouping
before every spatial or converter child. Child invoices are unchanged.

## 3. Endpoint and low-rank arrays

Retain the source's prepared endpoint layout for every incidence through
all queries. At most \(1+\lambda_m\) copies occur per input label, so
all prepared endpoints and their destination accumulators occupy
\[
 O((1+\lambda_m)V).                                 \tag{VS3}
\]
Keep this estimate as written; replacing it by polynomial(m)V would
lose useful information. By VS1 its logarithm has the required Phi size.

For low-rank delivery, retaining the r_m intermediate vectors for every
query j occupies
\[
 O((m r_m/N_m)V)=O(V).                              \tag{VS4}
\]
Thus each rectangle sum can be gathered when generated without redoing
its source endpoint change. Destination endpoint arrays retain direct
and low-rank contributions until they can all be returned to physical
order. Apply the rank matrix row by row with one output accumulator.
Its polynomial-m coefficient table is one buffer, not a copy per address.
This is the source schedule with its space exposed; it adds no recursive
field permutation for each query.

Predictor stages execute sequentially with ping-pong arrays. Finite
repair has its existing 1/16 child-volume ratio; its parked arrays
sum geometrically. The polynomial finite unrolling changes the batch's
independent row count, rather than requiring a full array per unrolling
node. All such children use one fixed set of reusable work intervals.

## 4. Spatial stack and visited regions

Use the composite-radix preparation at each spatial node. Its initial
two-field and leading padding is at most \(1+1/(u+1)\). To pass to a
new binary-width node, pad each raw child field \(b^f\) to
\(2^{\lceil\log_2 b^f\rceil}\). This two-field factor is less than four
and is charged at every child.

Measure parent volume at binary entry to a spatial node. Its padded
radix/leading layout has at most twice that volume. Including this
factor, grouped main children have at most \(16/N_m\) of their parent's
payload. Increase the fixed base threshold so \(N_m\ge64\); parked
arrays of such children sum geometrically. Finite repair retains
its 1/16 ratio within the already padded local layout. Reserve children
can have eight times their binary-entry
parent's payload, but all other arrays are merged and cleared first,
leaving only descriptors, as in the source reserve schedule.

Take \(m(u)=\Theta(u^\gamma)\) for a sufficiently small fixed rational
\(\gamma>0\). The child width is
\[
 v\le u/m+2\le u^{1-\gamma/2}
\]
above the base threshold. There are O(log log(U+4)) spatial levels.
Even eightfold inflation at every reserve level contributes only
\((\log(U+4))^{O(1)}\). VS1 bounds every endpoint factor by the
monotone envelope \(2^{C\Phi(\log_2(U+2))}\). The root field embedding
contributes only O(log(U+2)).

The deterministic widths and parameters at each spatial depth can be
prepared once at the root and reused: every main and reserve call from
one level has the same raw field width and hence the same padded binary
width. The complete O(log log(U+4))-entry chain retains only compact
executable plans. Discard optional expanded archives after validation.
For sufficiently small gamma, whole-chain construction has cost
2^(U^eta) times a fixed polynomial in log(2V), with a fixed eta<1;
the root's two complete U-bit fields absorb this additive bill.
A deliberately coarse stack estimate
also suffices: with depth d, every active payload is at most 8^d times
the root payload, and there are O(log log(U+4)) spatial ancestors.
Their whole parked arrays, compact plans and construction regions fit
in the maximum local endpoint factor times a polynomial in log(U+4).
Thus no extra regeneration-per-child assumption is needed. The source
end-access stacks, copying, erasure, and head returns are charged in
time. Sibling calls always reuse the same marked intervals.

The resulting proposed bound is therefore
\[
 \operatorname{Space}_I(U,V_0)
 \le V_0\,2^{C'\Phi(\log_2(U+2))},                    \tag{VS5}
\]
for original binary volume \(V_0\). This bounds the union of visited
regions. Direct base calls when \(u<K\log_2(s+2)\) use O(V) space and
polynomial(log U) time, which fits the same envelope.

## 5. Falsifiers and scope

The proof fails if some factor requires polynomially many simultaneous
full-volume arrays that cannot be serialized without increasing its
recursive invoice; if grouping the O(m) roles calls the recursive
interchanger; if masks attach m labels to each scalar rather than
each grouped block; if endpoint multiplicity exceeds the incidence
bound; or if field coordinates are embedded anew at each depth.

The time bound is separate. All polynomial(m,s) scans remain charged,
and the numerical Walsh/outer multiplier must be composed separately.
No complete multiplier envelope follows from this component alone.

Credits: @CubeJerry, the pinned source endpoint schedule, E002 component
authors, and substantial ChatGPT multi-agent assistance. This is a
written proof proposal, not an executed full machine or formal certificate.
