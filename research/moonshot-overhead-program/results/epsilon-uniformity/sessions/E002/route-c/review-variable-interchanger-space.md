# Independent review of the variable-interchanger space ledger

Gate: **PASS for the proposed space component**, under its node guards and
complete-unit-list contract. This does not establish its time recurrence
or a complete multiplier. Reviewed: Route B `variable-interchanger-space.md`.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`interchange.tex`, especially endpoint preparation, rectangle/low-rank
delivery, and spatial partition/parking. E002 suppliers are the reviewed
fixed-template physical components and composite-radix selector.

## 1. Label and field bounds

The retained estimate

\[
\log_2[D_m(1+\lambda_m)]\le3y/d+10d^2\log_2(4y),\quad y=\log_2 m,
\]

with a power-of-two d within an absolute factor of
`(y/log(y+2))^(1/3)`, gives `D_m(1+lambda_m)<=2^{C Phi(y)}`.
The exact rank guard is unchanged. The label lower bound follows from
`q^(d^2)>=C_r m` and `(2d-1)^2>=d^2`; the upper guard
`y>=12d^2` holds eventually, giving `m<=N_m<=m^5`. Rational dimensions,
counts and heights stay polynomial m, uniformly in this distance choice.

An even power-of-two s with `2^s>=B(m(U))` and
`s=O(log(m(U)+2))` supplies one field `F_(2^s)` with enough distinct
nodes for every descendant. An explicit constructor can find its F4
generator by testing `omega^2+omega+1=0`; enumeration over at most
`2^s` elements is polynomial root-m work done once. Retain this generator
and the irreducible polynomial.

Initial bit embedding expands volume by s only once. Internal calls keep
the same s-bit records. Their arbitrary-E-input identity therefore applies
to the embedded input bits with no repeated extension. The s factor is
polylog(U), within the proposed envelope. The guard
`u>=K log(s+2)` makes a complete two-field payload large enough for every
fixed polynomial-in-s coefficient buffer. A direct small-u base moves
opaque records and needs no new field-arithmetic workspace.

## 2. Headers and spectral labels fit in their payloads

Whole-row keys are headers, not tags appended to each scalar. Under
`u>=m^K`, complete spatial rows dominate polynomial-size module-index
headers and descriptors. Stable row sorting uses constant-volume arrays.
Monomial terms are serialized with one input, one accumulator and one
work stream; their polynomial number does not count live arrays.

A rational coefficient of height `m^C` can be numerically enormous.
However `log_2 Q=Omega(u/m)` for the target field. With a sufficiently
large guard exponent and sufficiently small gamma, `Q/a>=m^K`.
Every increasing run then pays its polynomial-size header, so all a
headers fit in total payload volume. The padded grid is at most fourfold.
Inverse scaling reverses this same construction rather than using a large
modular inverse as a fresh coefficient. This strengthens the earlier
polynomial-space HS bound in exactly the needed regime.

Moving a finite shift/check role to the fast position costs `O(log m)`
elementary binary moves and constant temporary volume; it is not a call
to the recursive interchanger. Remove padding after the complete role
move. The resulting record has B or 32B E-elements, whose `B s` bits
pay for one m-label list. Spatial addresses remain in the source order,
so its comparison-run generator applies to these larger records.
One reused polynomial-size buffer holds the selected spectral matrix.
No such buffer is retained for every address simultaneously.

Real check outputs have indices
`(check<floor(B/32),duplicate<32,module)`. Flatten the first two and
append the remaining `B-32 floor(B/32)` zero roles. Each module/address
block has exactly B roles. Remove comparison labels and restore role order
before paid children, so their volume invoice is unchanged.

## 3. The source endpoint schedule gives the claimed storage

Each label occurs in at most lambda rectangles on either side. All
once-prepared source endpoint copies and destination accumulators occupy
`O((1+lambda)V)`, rather than one parent array per rectangle. This
retained factor has the Phi bound and should not be replaced by a coarse
polynomial-m factor.

All `m r_m` low-rank vectors together have volume
`(m r_m/N_m)V<=V`. For each prepared rectangle and query j, form its sum,
deliver its direct contribution, and immediately accumulate its converted
contributions in the relevant basis-row vectors for j. Then discard that
sum. The prepared source copies remain for later queries. Once the basis
vectors are complete, apply the small rank matrix and module coefficient
map with reused input/output arrays, and distribute to the prepared
destination endpoints. Finally return those endpoints to physical order.

This schedule uses the original source conversions counted by
`r_m(1+lambda_m)` for each query. It does not repeat the reserve endpoint
change per query. Keeping all query accumulators is exactly what the rank
fraction pays for. Predictor stages use ping-pong storage; finite repair
has its existing geometric 1/16 children.

## 4. Reserve inflation and visited regions

Composite initial padding is at most `1+1/(u+1)`. Child re-encoding from
two `b^f` fields to binary costs a separate factor less than four. For
`m=Theta(u^gamma)`, above the base cutoff,

\[
v\le u/m+2\le u^{1-\gamma/2}.
\]

Thus spatial depth is `O(log log(U+4))`. With the latest conservative
binary-entry convention, grouped main children have fraction at most
`16/N_m<=1/4` once `N_m>=64`. Reserve children can have eightfold
payload including entry padding, but the source has cleared its main arrays and
parks only descriptors before these calls.

Along a path raw payload inflation is at most `8^d`, hence polylog(U).
Endpoint factors are bounded by the monotone root Phi envelope. Summing
parked spatial arrays adds another polylog(U) factor. Finite-contraction
ancestors at a fixed spatial scale have geometric 1/16 payload; even
counting their depth explicitly would add only a polylog(U) factor.
Compact construction and coefficient buffers fit the complete payload
under the guards. Siblings reuse marked regions. This bounds the union
of visited cells by

\[
V_0\,2^{C'\Phi(\log_2(U+2))}.
\]

The guard `u>=m^K` is eventually automatic for small enough gamma.
The base `u<K log(s+2)` uses O(V) space and polylog(U)-coefficient
direct time. Every other failed shape guard must remain an explicit base
branch in the later time proof.

## Scope

The ledger avoids repeated field embeddings, m labels per scalar, a live
array per monomial term, and all rectangle-query sums retained together.
Its endpoint-incidence arrays are explicitly priced. The numerical Walsh
recurrence and final common-space selector remain separate obligations.

Credits: @CubeJerry; the pinned source schedule; E002 component authors;
substantial ChatGPT multi-agent assistance. This is a written mathematical
review, not a full tape execution or formal certificate.

The initially reviewed source snapshot was
`71cf477715f4991a0c67ccf25df0ee3ad6669a1eea7ac29658faf01b7d96c300`.
The final reviewed snapshot is
`b4a710a1d2160d07ff2aab206bec9be8d3521fa7d5090c8f7cbe138640e6a97c`.
Its explicit F4-generator search, one-time compact width-chain preparation,
`2^{2u-poly(m)}` row-payload estimate and conservative 8^d entry-padding
convention have all been checked. They preserve the stated space envelope.
