# Row-space orbit layouts: joint reindexing and the Fourier boundary

Status: **proved local compiler and exact block structure; independent
review pending**. No improved multiplication envelope is claimed. The
converter below is charged and too expensive; its improvement and the
Fourier-child interface remain open.

Pins: programme `62d9d8e917379cb2edc17c9761e12e2345bc01f4`; OpenAI math
`3344da59991ed94f9ba711217b29c1d760badfa6`. Fourier `kernel.tex`,
`binary.tex`, and tape `walsh.tex` apply an invertible binary matrix to
every address column; it may depend on a finite row/label role.

## 1. Mechanism and target budget

The admitted numerical supplier pays polynomial-arity work for repeated
address changes, each calling interchange. Grouping data by **row space
of its address matrix** makes every columnwise linear reindexing local
to one block, with an O(A^2)-bit destination key independent of slot width
f. This changes the representation, rather than retuning the old invoice.

The intended polynomial-x budget remains

    G_outer(x)<=max(G_exact(x),G_Walsh(x))+O(log(x+2)).

It requires entry/exit costs at square-root scale, real amortization,
a valid child interface, bounded normalized recursive mass, precision
and absolute visited space. Orbit cardinality proves none of these. The
current converter instead costs V times active address length. The two
discriminating questions are its improvement and closure under children.

## 2. Orbit coordinates

Let A,f>=1 and X in F2^(A by f), with A rows of f-bit address slots.
GL_A(F2) acts by X->MX. Addresses carry arbitrary independent payloads;
extra complete spectator coordinates may remain outer indices.

**RO1.** Two matrices share an orbit exactly when their row spaces agree.
For an r-dimensional row space W and its canonical nonzero-row RREF basis
B_W, every member has a unique expression

    X=C B_W, C in F2^(A by r), rank(C)=r.

The orbit has h(A,r)=product_(j=0)^(r-1)(2^A-2^j) members, with h(A,0)=1,
and the action is C->MC. Thus log2 h<=A r<=A f.

**Proof.** Invertible row operations preserve row space. Two rank-r maps
onto W differ by a domain-basis change: extend kernel bases and compatible
preimages of a basis of W. Independence of B_W gives unique full-rank C.
Its columns are an ordered independent r-tuple in F2^A, giving h. QED.

## 3. Polynomial rank/unrank without a group table

Order full-column-rank C lexicographically by columns, each read from
most to least significant bit.

**RO2.** Rank and unrank in [0,h(A,r)) cost a fixed polynomial in A actual
binary-tape steps and O(A^2) working bits, uniformly in f,W. No 2^A-vector
list or GL_A table is enumerated.

**Proof.** Suppose j fixed independent columns span U. For a prefix p of
length t on the next column, project U onto these coordinates. Elimination
gives rank rho and tests p's membership. The admissible-column count is

    2^(A-t)-indicator[p in proj_t U] 2^(j-rho).

Multiply by product_(v=j+1)^(r-1)(2^A-2^v) for subsequent columns. At each
one bit rank adds the zero-prefix completion count; unrank compares with
that count, chooses a bit and subtracts when choosing one. There are at
most A r<=A^2 stages. Counters and elimination arrays use O(A^2) bits;
schoolbook arithmetic gives polynomial work. Rank zero is empty. QED.

## 4. Actual fixed-tape orbit-order compiler

The **row-space layout** has consecutive W blocks in a canonical order.
Each has header (r,B_W) and payloads in the C order above, for all
independent row roles. Records have w bits, with w>=A f plus row-address
width, and at most polynomially many row roles. V counts encoded records
and headers. Headers have O(A f) bits and each block contains a record,
so their volume overhead is absolute. Raw one-bit records do not satisfy
this width convention; their metadata must be separately charged.

Every input fibre contains **all 2^(A f) addresses**, each once and with
independent payload. Within a W block, use role-major then C-rank order;
each role subblock is sorted separately by its destination rank. Extra
spectator indices are already outer indices of contiguous complete fibres.
Moving strided source spectators into this position is a separate charged
layout operation, not included for free in RO3 or the converter below.

**RO3.** In this layout every specified M in GL_A(F2) is executed in

    O((A+1)^12 V) steps and O(V) cells ever visited

on one fixed finite-alphabet multitape machine, with absolute constants.
The safe power 12 is nonoptimal. The statement is uniform in f,W and
payloads. Polynomially many role-dependent/successive maps retain a
fixed polynomial-A bound.

**Proof.** At each record unrank C, form MC, and append its destination
rank, of at most A r<=A f<=w bits. Key work is polynomial A per record.
Reused O(A^2) control space fits complete-array volume V>=2^(A f)A f.
Within each orbit block stable-radix-sort destination keys. A pass scans
the block into two scratch streams, rewinds them and concatenates them;
lengths are known from the header and h(A,r). At most A^2 passes each
cost O(V), including head returns. Since M is invertible, destination
ranks are exactly [0,h), each once. Drop keys by a scan. Reuse the same
original/output/split-stream intervals between blocks and passes, so only
an absolute number of payload copies is ever retained. Elementary rank
arithmetic, elimination and multiplication fit the generous power 12. QED.

Polynomially many scalar row roles can be mixed by serial role scans and
one output accumulator. For a mask depending on the ordinary address,
reconstruct X=CB_W in O(A^2 f) bit work, polynomial A times record width.
Pointwise masks preserve W blocks. Numerical arithmetic still pays its
actual coefficient preparation, precision-dependent bit cost and rounding;
this is no unit-cost product or full precision theorem.

## 5. A complete but excessive converter

From role-major ordinary lexicographic order, compute each record's B_W,C,
append (canonical W key, role, local rank), and radix sort by that
O(A f)-bit key within each already-outer spectator fibre. Equal W keys
give blocks; retain one header and drop duplicates. Inverse conversion
reconstructs X=CB_W and sorts by (role,X). The O(log roles) extra key
bits fit O(A f) for the fixed polynomial row-role bound. Elimination costs
polynomial A times f per record, and sorting costs O(A f) full passes.
Both directions therefore satisfy

    time O(V[(A+1)^12+A f]), visited cells O(V).

The V a term, a=A f, is excessive relative to V sqrt(a) with a small
overhead. This is the invoice of this implementation, not a universal
converter lower bound. No arbitrary sort is hidden in RO3.

Conversely faster converters, with RO3 between them, implement arbitrary
columnwise reindexing. At A=2 the row exchange is ordinary interchange
of two complete f-bit fields. A linear-time orbit converter would itself
give a linear-time interchanger in this model. This is a substantial
mathematical gate, not a free change of format.

## 6. Fourier children cross orbit blocks

Nonrecursive column changes and pointwise operations preserve W. An
actual selected-axis Walsh child does not.

**RO4.** Walsh transform of row 0, fixing the others, sends the basis
vector at X=0 to nonzero amplitudes in exactly 2^f orbit blocks: the zero
space and all lines in F2^f.

**Proof.** Every first-row value y receives coefficient 2^(-f/2), with
all other rows zero. Its row space is zero for y=0 and span(y) otherwise.
Over F2 different nonzero vectors give different lines. QED.

Independent blockwise execution cannot implement this child. This is
a support statement, not a runtime bound: a collective algorithm may
communicate efficiently. Charging every block separately would be an
additional accounting hypothesis. The lead's separate
`../lead/rowspace-walsh-rank-gate.md` examines the stronger possibility
of a block-preserving candidate plus a small-rank global correction.

## 7. Exact off-diagonal full-rank Fourier blocks

Let A>=2, and W!=W' be A-dimensional row spaces in F2^f. Let K be the
unnormalized child Walsh matrix between their full-rank orbit blocks,
transforming row 0 and keeping the ordered spectator rows fixed.
The ranks below are over R or C, the numerical data field; the addresses
and subspace dimensions are binary. They are not matrix ranks modulo two.

**RO5.** If dim(W intersection W')<A-1, then K=0. Otherwise U=W
intersection W' is an (A-1)-dimensional space, and K is a direct sum over
ordered bases of U in spectator rows. Each summand has rank

    2^rank(dot product restricted to U).

There are |GL_(A-1)(F2)| summands. If the restricted form is nondegenerate,

    rank K=2^(A-1)|GL_(A-1)(F2)|=h(A,A)/(2^A-1).

**Proof.** Nonzero entries require identical spectator tuples. Full row
rank makes them an independent (A-1)-tuple, proving the zero case. For
intersection U of dimension A-1, each such tuple is a basis of U.
Choose x0 in W\U, y0 in W'\U. The corresponding kernel on u,v in U is

    (-1)^((x0+u) dot (y0+v))
     =(-1)^(x0 dot y0)(-1)^(u dot y0)(-1)^(x0 dot v)(-1)^(u dot v).

The first three factors are invertible row/column scalings. A rank-t
bilinear form has character matrix equivalent by row/column basis changes
to a t-bit Walsh matrix tensored with an all-ones matrix, hence rank 2^t.
Distinct spectator tuples give disjoint blocks. Finally
h(A,A)=(2^A-1)2^(A-1)|GL_(A-1)(F2)| counts a hyperplane, its basis and a
vector outside it. QED.

This supplies a concrete Grassmann-incidence interface, not an algorithm
or a runtime lower bound. Degenerate U must retain the first rank formula.
It is not legitimate to add all block ranks as independently paid work
without an explicit restriction on the executor.

## 8. Decision, verification, and open next questions

Retain RO3 as a positive local compiler for all source columnwise linear
reindexings, with f removed from its local destination key. Retain
RO4--RO5 as exact evidence about the Fourier boundary. The priced global
converter is too expensive, and no complete H improves.

1. Can Cartesian-to-rowspace conversion improve the O(V A f) sorting bill
   with actual head movements, arbitrary independent payload and absolute
   visited space?
2. Can the Grassmann-incidence blocks be processed collectively in this
   representation, with a complete recursion and charged transitions?
3. Could a changed outer caller supply and recover a compatible layout
   without reproducing the converter cost?

The finite checker tests orbit bijections, rank/unrank, GL action, child
support and block rank, including degenerate controls. It is no full tape
execution or formal proof. Independent review is recorded separately.

Credits: Jerry Chen (@CubeJerry); OpenAI's columnwise address and Walsh
interfaces; standard finite-field row reduction and character-matrix
rank; S003/E003 star investigations motivating this changed representation;
substantial ChatGPT assistance. No priority claim is made for elementary
orbit classification or character-rank identities.
