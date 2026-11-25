# E003 admission of the fixed-machine two-scale construction

Disposition: **accepted written complete algorithm/profile construction**
in the pinned finite-alphabet multitape model. The local executor gates
P-I/P-W/P-O of Route B's conditional transfer are supplied by the separately
reviewed components identified below. No unproved efficiency-family
hypothesis remains in this composition.

This is an AI-assisted mathematical construction and review. It is not
human refereeing, a formal machine refinement, an executed full multiplier,
a practical implementation, or a certified literature-priority result.

## Result and concurrent provenance

Put L(n)=1+log2 n, x=log2 L(n), Phi(x)=x^(2/3)(log2(x+2))^(1/3).
There is one fixed exact deterministic finite-alphabet multitape machine
computing the full product at every input length, with

    T(n)=O(n sqrt(L(n)) 2^(O(Phi(x)))),
    total cells ever visited=O(n).

The constants and eventual cutoff are absolute but have not been
numerically optimized or evaluated. All-length correctness uses explicit
shape/numerical/space/time guards and exact fallback. The actual fast
construction can have an enormous initial range where fallback is used.

Concurrent E002 admitted this same explicit asymptotic scale at 8af1911b,
and S003 at 2fde2b0c. E003 independently derived and reviewed a two-scale
composition using S003's fixed-three geometry and E003's local storage
suppliers. This admission is an additional proof chain, not a new
programme-best rate or a claim of priority over those sessions.

The bound implies every pure envelope 2^(O(x^beta)) with beta>2/3.
It retains the logarithmic factor at beta=2/3. Polynomial-x overhead,
bounded H and the square-root endpoint remain open; kappa_ov is not
assigned. No lower bound on actual runtime is inferred from a growing
upper-bound certificate.

## Exact proof objects

The analytic composition is `../route-b/TWO-SCALE-RECURSION.md`, reviewed
at SHA-256

    d3dbaec51328645cc2431f7dcccbb654bf62f2fd20e91cea17ab9d04658e5cdc.

Its modular statement remains conditional as written; this admission
supplies its contracts. A's physical/analytic review is
`../route-a/REVIEW-TWO-SCALE-PHYSICAL-CLOSURE.md`; C's independent
analytic/source review is `../route-c/REVIEW-B-TWO-SCALE.md`.
The lead read both in full, the complete transfer, all new local
suppliers and the complete primary caller files listed in
`review-source-composition.md`.

The consequential new P-W supplier is
`../route-a/RATIONAL-WALSH-CONSTANT-SPACE.md`, SHA-256

    11cfd491f2f1153ab9a534e8625308f45577093b31a25a6ae641bd74a3b8e9b2.

It is independently accepted in
`../route-b/REVIEW-RATIONAL-WALSH-SPACE.md`, and the lead also read and
checked the full schedule against source `kernel.tex`, `binary.tex`,
`walsh.tex` and `permutations.tex`. A's review does not count as an
independent review of A's own new supplier. Exact component/review
hashes are recorded in `two-scale-admission-manifest.json`.

## Closing P-I: local exact interchange

The all-arity rule in `ALL-ARITY-LABEL-PROFILE.md` is an integer
constructor for every sufficiently large arity, with an explicit
conservative guard. It supplies the rank budget, polynomial label
dimensions, sublinear reserves and the Phi call-loss profile. It does
not rely on substituting a changing exponent into a fixed-J trial.

The local physical executor uses the predecessor compact cyclic and
small check-space processors. E003's shared-pencil schedule stores all
query rank intermediates together inside one input volume because
m r*/N<=1. It retains raw pre-A_j sums, and direct/low-rank delivery
meets at exactly the same ordinary address. Comparison labels use one
current control tuple. Guarded stream primitives or the independently
reviewed HFS scaler provide an absolute payload-space coefficient.

S003's explicit dyadic geometry permits address radix three at every
node. Its doubled dimension and elementary-map constant are charged
afresh. Full-rate field packing preserves arbitrary binary input bits
and every normalized child volume. A new coefficient field is permitted
only at a completed spatial permutation; finite repair descendants
retain the local field and template.

Grouped main payload descents contract by at most 2/N<=2/3. Finite
repair descents contract by 1/16. Before a full-volume reserve child,
the main arrays and workspace are cleared and only descriptors are
parked. Region reuse bounds all visited cells. The constructor is
absorbed at each node using the complete two-field volume; no global
archive is scanned at a small descendant. These are the complete P-I
time/volume/storage contracts reviewed by A, B and the lead.

## Closing P-W: numerical Walsh with fixed arrays

An older polynomial-m proportional-space estimate is insufficient for
the variable Walsh arity. The new RW schedule closes that specific gap.
Small rational row maps are serialized over role pairs with source,
accumulator and reusable term streams. Rectangles run sequentially;
each source endpoint is prepared once, all middle-query contributions
are added to one prepared destination collection, and its final partial
transform is performed once. The original recursive Fourier invoice
is preserved while ordinary work remains explicitly polynomial in m.

The rational Newton predictor and division repair use a fixed number
of arrays. Finite repair has two sequential children of volume 1/8;
its height O(log m) gives only polynomially many actual occurrences.
Completed numerical spatial children have volume V/W_m. Binary
coordinate maps retain their packed-XOR guards, exact destination tags,
paid interchanges and tag removal before children.

Exact short-rational arithmetic, coefficient heights and on-demand
spectral matrices are charged per encoded volume. Every local
input-to-intermediate and fault-to-later numerical gain has polynomial-m
logarithm. The statement covers physical partial sums and parked arrays,
not only the completed unitary target. Exact bit permutations create no
rounding events; their intermediate bit encodings are not interpreted
as approximate numerical values. This supplies every part of P-W.

## Closing P-O and the global guards

The lead and B read the complete primary outer caller independently.
Its guarded record permutations depend on the interchanger through an
explicit call interface, so the monotone new cost envelope can be used
directly. The CRT/short-Fourier/phase/carry grammar, absolute precision
requests and exact recovery proof are unchanged. See the lead source
review and B's `OUTER-REDUCTION-TRANSFER.md` for the operation-by-operation
mapping. The fixed short-word arithmetic primitive is not circularly
derived from the new multiplication theorem.

The exact interchanger uses a small fixed power of active width as its
arity. The numerical Walsh routine uses log arity of order Phi(log a),
so its real polynomial routing toll and accumulated recursive loss both
fit the same envelope. Leading numerical rows are padded once to a
product of the known batch divisors; deeper divisions are exact.

The Walsh-only finite preparation is 2^(k^o(1)). The different exact
interchanger preparation is paid locally and is not included in that
stronger numerical setup assertion. Actual numerical operation count
is polynomial in k. An explicit numerical guard k>=m_max^K2, with a
fixed sufficiently large exponent, pays the gain/event/coefficient
budgets before choosing an absolute O(k)-bit format. Time and space
caps alone would not establish numerical correctness.

The first digit routine has a stated poly(log L) space coefficient.
The exact rowwise chunk wrapper reduces it to one absolute O(n) visited
cap, at only a polynomial-x time penalty. Each chunk product is executed
sequentially, and rowwise carry assembly costs O(nr), not a whole-output
scan per chunk pair. The r>n branch and every failed shape/numerical/cap
test use exact schoolbook. Eventual success proves the displayed
asymptotic bound while every input length remains correct.

## Evidence and continuing research

Independent finite replays cover full-rate bit packing, exact dyadic
geometry, shared-pencil bookkeeping, discrete arity guards, rational
rounding/repair and integer recursion/padding. Their receipts retain
their limited scopes. They do not execute the astronomical full template
or certify actual asymptotic tape timing. No fresh Lean build was run.

The order-five construction, matrix/port obstructions, and binary-Walsh
invoice work are separate components, not needed premises of this
admission. They must not be converted into a smaller global H without
another complete cost proof. The active research direction is a changed
physical query-delivery or label mechanism; parameter retuning inside
the retained invoice is not an established route to a better scale.

Credits: Jerry Chen (@CubeJerry), pinned OpenAI source authors and their
predecessors, S002/E001/E002/S003 components, the E003 lead and A/B/C
workers, and substantial ChatGPT assistance. Concurrent contributions
retain their own provenance and claim limits.
