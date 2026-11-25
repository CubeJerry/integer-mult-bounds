# Polynomial address and radix interface for the interchanger

Status: proved address/batching composition, subject to the explicit compact
scalar-row contract below. This is not a complete multiplication theorem.
The contract concerns local finite row operations, not the desired final
runtime. Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
November `build/interchange.tex`; predecessor geometry/height profile at
programme head `0607d044d1d09489580da0e5828588820e1a6775`.
Suppliers: A `HEIGHT-PRICED-AFFINE-STREAMS.md`, C `small-radix-batching.md`,
and A `SUCCINCT-ROW-EXECUTION.md`. C's masked-translation executor supplies
part of, but is not silently identified with, the complete scalar contract.

## 1. Quantified input contract

Fix m>=2 and 1/2<rho<1. All polynomial degrees below are absolute. Suppose:

1. There are at most m^C labels and rational endpoint maps/factor lists,
   reserve dimension a<=m^C, and rational bit heights <=m^C. The full list
   of required nonzero units and denominators is explicit.
2. A correct full-rate main-swap program has independent-row width W>=3,
   log2 W<=m^C and spatial call bill sigma, including converters/repair.
   Its scalar operations and row layouts on concatenated rows cost m^C V
   actual steps and visited cells using fixed tapes and a structured
   executor. It does not scan a W-by-W matrix or expanded transition list
   per datum.
3. Identical recursive address calls are grouped into polynomially many
   explicit label/query/endpoint types, using module rows as ordinary
   prefix spectators. Their child volumes sum to the invoice sigma, not
   W times that invoice. Every main group has relative volume at most a
   fixed gamma<1; in the source grouping by one label, gamma<=2/N_label
   with N_label>=3. Per-type descriptors cost m^C poly(log(2V)) of fixed
   degree.
4. One finite data algebra has at most m^C binary coordinates and
   polynomial-m arithmetic. Every recursive level uses this same encoded
   algebra. Its identities hold on arbitrary independent rows and occupied
   reserves.
5. For fixed absolute eta in (0,1] and kappa<1,

       (1+eta)*sigma/W+2a <= kappa*m^rho.             (AR1)

No external input-length runtime property is part of these local hypotheses.

## 2. Polynomial radix and height-priced maps

The full compatibility product has polynomial bit length. C's elementary
prime lemma finds an odd compatible radix b<=poly(m) in polynomial actual
bit time. It requires only nonvanishing of the listed units/denominators,
not b larger than their numeric magnitudes. All rational address maps then
specialize modulo every b^f.

HS/HA executes every lower-triangular factor in poly(m)V work and space.
The source ordered Bruhat field-permutation calls are unchanged. Inverse
scalings use reverse small-height rearrangements, not large inverse residues.
Every address field and both reserve groups contain occupied data; no zero
coordinate is assumed. Program copies are paid internal workspace.

## 3. Variable-radix digit moves on fixed tapes

The source's fixed-b digit lemmas now need an explicit polynomial-b bill.
For any prescribed two-digit permutation, iterate the b^2 input value pairs.
For one pair, scan the input and extract that class into one temporary
stream. The remaining coordinates retain the same order in its output
class. Sweep an output accumulator, filling exactly the positions of the
pair's prescribed output class and retaining all other positions. The
classes have disjoint outputs. A fixed number of tapes suffices, and each
class requires boundedly many full-volume scans, including returns/cleanup.
Initialize the accumulator explicitly. Class tests and small digit counters
cost poly(log b). This proves poly(b)V time and visited space.

A one-digit move uses the same procedure on b classes. Removing the selected
digit leaves the same order of every other coordinate, so the extraction/
fill argument applies across arbitrarily long intervening fields. This
avoids b physical tapes and random access among b parked streams. Unrelated
long prefix counters are advanced, never fully reread per datum.

## 4. Multidigit batching and the recurrence

Put ell=ceil(log_b(W/eta)), A=b^ell and q=ceil(A/W). Then

    qW/A <=1+eta,       ell<=poly(m).                  (AR2)

Use the first ell digits of the earlier active field. Pad its final group
to qW and write r=Wg+w. Regroup to rows w, keeping g and the remaining
address as spectators. Stable sorting whole blocks by the O(log W)-bit w
key costs V*poly(log W) on fixed tapes and retains increasing g within each
w. Reverse regrouping uses r=Wg+w. Alternatively process each external
prefix/group block serially and use bounded row-field moves inside it.
No unbounded spatial address is attached to each symbol. All padding is
charged and removed by its known index.

Every independent row has at most (1+eta)V/W symbols. The exact completed
program acts independently on genuine rows, so no genuine data are changed
by padding or later deletion. Padded workspace is not counted as additional
independent parent input.

For radix width e take f=floor((e-ell)/(m+2a)) when positive. Retain the
source early/late reserve geometry. After the main program restore reserves,
swap the remaining 2a reserve pairs recursively, and exchange the leading
ell digits plus fewer than m+2a remainder digits directly. All nonrecursive
work is poly(m)V. The base range e<ell+m+2a also costs poly(m)V.

Let T_m(e) be steps per encoded symbol, uniformly in prefix, gap and suffix:

    T_m(e)<=poly(m)+B_m T_m(f),
    B_m=(1+eta)sigma/W+2a<=kappa*m^rho,  f<=e/m.        (AR3)

The base width is polynomial in m. Induction with a sufficiently large
polynomial coefficient, or the geometric ratio B_m/m^rho<=kappa, gives

    T_m(e)<=poly(m)(1+e^rho).                         (AR4)

The polynomial degree is absolute. Fixed kappa and eta hide no inverse
vanishing margin. Fixed-degree descriptor work is absorbed at each type
using log^d(2V)<=C_d V. Module rows are prefix spectators for identical
calls, not separate tapes or a reason for W scans of the parent.

## 5. Visited space, data alphabet and binary input

Grouping module rows preserves the summed recursive invoice but changes
the size of one call. A main descent has the fixed relative bound gamma<1
from item 3; for the source one-label grouping this is at most
(1+eta)/N_label<=2/3, not (1+eta)/W. Its parked
arrays and returns cost poly(m) times node volume, whose sum along a path
is geometric. Before a full-volume reserve descent, merge and clear main
workspace and park only its descriptor/return instruction, as in the source.
Descriptor stacks have polynomial-m times poly(log V) size, bounded by
poly(m)V. Work regions and stack intervals are reused; this bounds all
cells ever visited without a recursion-depth multiplier.

The machine alphabet is fixed binary with fixed delimiters. An algebra
letter is a coordinate block, not a new machine symbol. Input bits embed
once; children use the same block format and algebra description, without
re-embedding each bit of a parent's block. Local row/frequency tags are
temporary parent workspace, removed or parked before a child call. They
are not passed as recursively expanding data letters.

For original binary address fields of width u, pad to the least b^e>=2^u.
Volume increases by <b^2=poly(m), and e<=O(u). The completed interchange
preserves genuine addresses; scan out the padding to obtain

    poly(m)V(1+u^rho) steps, poly(m)V visited cells.    (AR5)

## 6. Remaining bridge and credit

AR5 closes address/radix costs after the compact scalar contract is supplied.
It does not establish spectral coefficient access, numerical Walsh precision,
a candidate family or the common-cap multiplier. A dense per-symbol spectral
table scan or an expanded interpreter would violate item 2.

The next obligation is to supply every operation of the characteristic-two
main-swap/repair program under items 2--4, including unchanged paid child
volumes. Masked-translation predictors and small-field shift-only checks
are the principal positive components. Their successful composition is a
separate theorem.

Credits: Jerry Chen (@CubeJerry); OpenAI ordered streams, rational routing
and depth-first recursion; predecessor height audits; C's elementary prime,
batching and masked-translation work; the session lead's row-grouping
observation; substantial AI-assisted E002 mathematics.
