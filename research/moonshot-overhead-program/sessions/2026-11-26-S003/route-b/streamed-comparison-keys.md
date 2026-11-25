# Simultaneous comparison keys without per-record tags

Status: **proved scoped streaming lemma; pending independent review**. This improves the workspace implementation of C's compact repair. Its algebra and scalar table are unchanged. It is not a standalone multiplication bound.

## 1. Interface

Fix m,f>=1. The physical address is a complete lexicographic Cartesian product containing H_1,...,H_m and N_1,...,N_m in that relative order, with every H before every N. Each ranges over [Q], Q=3^f. Positive prefix, gap, suffix and reserve ranges may occur between them. Their number is polynomial in m, as in the source layout, while their values may be arbitrarily large. Let Z count records and let each raw record have b>=1 bits, so V=bZ.

Define k_j=0 at equality,1 when H_j<N_j and2 when H_j>N_j. An inverse query uses -k_j modulo3. A callback may read the m-trit key and aligned scalars, use polynomial(m) work/workspace per record and return fixed-width scalars. It need not retain every key.

**Theorem SK.** A fixed finite-alphabet multitape scanner supplies these keys in physical record order in

    V poly(m)+poly(m,log(V+2)) time,
    poly(m,log(V+2)) additional control cells.

The polynomial degrees are absolute. It creates no m-bit tag per data record and no mZ-length key stream. Thus a fixed number of aligned data arrays remains a fixed number of V-bit payload arrays, independently of m. Head travel, rewinds and counter resets are included. The theorem concerns this ordered-pair layout, not arbitrary unordered comparisons.

## 2. Nested ordered runs

Retain the current H values on a control tape; they are fixed before the N fields vary. On entry to the N_j loop read H_j and prepare three consecutive runs:

    N_j in [0,H_j): key j=2,
    N_j=H_j:        key j=0,
    N_j in (H_j,Q): key j=1.                            (SK1)

Enumerate each nonempty run with a binary down-counter, invoking suffix loops in their original order. Update position j in one m-trit key register at its at most three run boundaries. Later N positions are maintained by their nested loops. At an innermost output the complete key is available. No f-digit comparison is repeated per scalar.

Reserve and arbitrary spectator ranges use ordinary nested counters; skip unit ranges. H fields are counters whose current values remain available for later N loops. Fixed end-access stacks hold active loop state, with the innermost counter's low end at its head between outputs. A callback uses separate reusable arithmetic regions and returns each control head to its mark. This generates exactly the lexicographic key sequence. Invoke it at the completed spectral interface in original physical order; it moves no key through a coordinate map.

## 3. Long-counter and workspace accounting

Reading H_j, finding it on the control tape, preparing its boundaries and initializing its loop takes poly(m,f) work per prefix ending before N_j. That prefix has3^f N_j values and its complete suffix. Thus the total preparation cost per output record is at most

    poly(m,f)/3^f <= poly(m),                           (SK2)

uniformly in f. For every fixed c, sup_(f>=1) f^c/3^f is an absolute finite constant. Traversing the O(mf)-bit H-control region only changes the fixed polynomial. There are m controlled loops. Arbitrarily long earlier-prefix counters are not read for these operations.

Within each run, ripple decrements and head returns have aggregate linear cost, as in the source elementary-stream lemma. A range setup/reset copies its O(log(range+2))-bit descriptor once per complete range. Any fixed power of that logarithm is bounded by an absolute constant times the positive range, so long spectators pay for their own setup. The live counter frame is updated in place; a fresh f-bit frame is not pushed before every scalar.

When no later controlled N field remains, the suffix is executed directly without recopying H controls at every value. When a later N field remains, its complete3^f range pays its initialization by(SK2). Unit ranges are collapsed. Key access/reset costs O(m), allowed per record. Control state totals polynomial(m) times the actual range-bit lengths, hence poly(m,log(V+2)). There is no mV space term. These estimates prove SK.

## 4. Spectral repair composition

For each coarse input/output check-row pair run this scanner on the aligned(module,physical-address) blocks. From the current key compute SR's containing set, Vandermonde inverse and desired coefficient in polynomial m work and additive polynomial m workspace, then apply it immediately. Recompute at the next record or coarse pair instead of caching. Every module retains its order.

Labels and the module index are spectators. Reset at a complete physical-address block costs poly(m,f), paid by its controlled ranges. The current module counter has polynomial-m width. The temporary tagged arrays of SR are replaced by the key register and nested controls. Raw width stays b=2eK, so no tag stripping is needed. Containing-set correctness, S=Bw padding, phase fraction1/16 and four-child mass1/4 are unchanged.

This removes one obstacle to a parameter-independent number of payload arrays. Scalar field packing, constant-array shared pencils and a growing-arity recurrence still need their own proofs.

## 5. Provenance and limits

Single-pair ordered runs and amortized tape counters come from OpenAI math `3344da59991ed94f9ba711217b29c1d760badfa6`, tape `build/interchange.tex` and its elementary-stream references. C's S003 scalar repair is unchanged. The contribution is simultaneous key generation with additive workspace, useful when m grows with active width. Prepared for Jerry Chen (@CubeJerry) with substantial AI assistance. No full tape execution or Lean build is claimed.
