# Streaming key batching with reversible stable partitions

Status: **proved elementary fixed-tape component; independent review pending**.
This is a physical interface for sharing coefficient preparation. Stable
radix partitioning is standard; the contribution is its explicit use and
invoice in the proposed compact numerical-template compiler. It is not a
new sorting algorithm or a complete multiplication theorem.

## Statement

An input is M fixed-length records in one stream. Each contains a q-bit key
and a b-bit payload, with b>=1. Keys may repeat and are preserved by the
following computation. Assume a fixed procedure, given one key and declared
parameters, prepares a coefficient/state of at most S bits in at most G
actual tape steps. Assume a fixed record processor, with that state, maps a
b-bit payload to a b-bit payload in at most R actual steps. Its semantics
are pointwise on records; it does not exchange different keys' payloads.
The bounds G,S,R include all interpretation, arithmetic, return and clearing
costs required by those procedures.

One fixed finite-alphabet multitape machine applies this processor using
one preparation per **distinct occurring key**, restores the original record
order, and has time

    O(q M(b+q) + M R + min(M,2^q) G)
      + poly(log(M+2),q,log(b+2)),                      (KB1)

and visited space

    O(M(b+q)+S) + poly(log(M+2),q,log(b+2)).             (KB2)

The fixed number of tapes is independent of M,q,b. If state preparation
temporarily needs more space than S, that workspace must be added to S.
Keys can be supplied by a preceding paid source scan; their computation
is not free or part of this theorem unless included explicitly.

## Forward sort and recorded inverse

Perform q least-significant-bit-first stable binary partitions. In a pass,
read each complete record and copy it to a zero stream or a one stream
according to its selected key bit. Append that routing bit to a mask stack
in **the input order of this pass**. Count zero/one records. Concatenate the
zero and one streams into the next input, and clear the two temporary
streams. A complete pass uses O(M(b+q)) steps, including rewinds and the
amortized binary counters. The mask adds M bits per pass; all q masks use
qM cells, already included in M(b+q).

Keep each pass's count and fixed mask length on an end-access descriptor
stack. Metadata uses O(q log(M+2)) bits and preparation work. For q>=1,
this is bounded by the displayed volume or additive polynomial: log(M+2)
is O(M), and for q=0 there is only one possible key and no partition.
The sorted stream is ordered by the complete key. No log M-bit destination
tag is attached to each payload. The saved one-bit masks are sufficient.

Scan the sorted stream by key runs. For each occurring key prepare its
state once, process the run sequentially, and erase/reuse the state before
the next key. A fresh key is detected by comparing its q bits with the
previous key, at O(q) cost per record, already charged in the partition
term when q>=1. When q=0, use O(Mb+MR+G) as the bound. The number of runs is
at most min(M,2^q), proving the preparation term in (KB1).

Now undo the q partitions in reverse order. For the current pass, split
the first recorded zero-count records and the remaining one-count records
into two streams. Read that pass's saved mask in its original forward
order; a zero takes the next record from the zero stream, a one the next
from the one stream. Stability makes this the exact inverse permutation.
Changes to payloads do not matter because routing depends on the retained
mask and record length, not on payload values.

To access the newest mask forward on a tape, retreat by its known M-bit
length to its beginning, scan it forward, then clear and retreat over that
block before accessing the preceding block. Each mask is traversed only a
constant number of times. Temporary streams and earlier masks occupy fixed
reusable regions or the one stack; no tape is allocated per pass. Each
inverse costs O(M(b+q)), proving (KB1). The original record permutation is
restored exactly.

All work tapes are reused between passes and key runs. The mask stack has
qM bits; payload copies occupy a fixed number of M(b+q)-bit regions. The
state and descriptors give (KB2), including cells visited and then erased.

## Numerical-template consequence and limits

Suppose a numerical record has b=Theta(k) bits, its key has
q<=m^C bits, its per-key rational/dyadic preparation costs poly(m,k), and
prepared coefficients are used with the source short O(k log(2+k)) integer
multiplier. Then key grouping and restoration cost `poly(m) V`, where
V=M b, after enlarging the polynomial to include q/b. Record products cost
`poly(m) V log(2+k)`. Per-key preparation costs at most

    2^(m^C) poly(m,k).                                 (KB3)

This can be treated as setup, rather than multiplication by an exponential
constant at every record. For fixed absolute polynomial degree and a large
enough fixed C', k>=m^C' implies (KB3)<=2^(k/2), up to an absolute eventual
cutoff. A caller with at least 2^k records can absorb it. This last shape
condition must be checked at the actual recursive node; a root-volume
argument cannot silently pay every small child setup. Alternatively the
total number of nodes and their setup must be bounded globally.

The state may contain a whole polynomial-size row-tuple matrix, provided the
records really contain the corresponding aligned tuple and every tuple
copy, access and bit product is included in R. The theorem gives no free
gathering of scattered tuple operands and no free controlled permutation.
If the numerical operation changes a key or requires communication between
different key groups, a separate proof is required.

This lemma is intended for the rational Walsh template's finite spectral
tables. Its complete application still needs actual key-generation scans,
the exact number/height of coefficients, one uniform setup-degree bound,
the recursive-node count, precision and visited-space accounting. It does
not turn an arithmetic/indexing circuit into a tape theorem by itself.

Credits: standard stable radix sort and inverse merge; source fixed-tape
streaming/short multiplication interfaces; Jerry Chen (@CubeJerry);
AI-assisted S003 physical billing and application.
