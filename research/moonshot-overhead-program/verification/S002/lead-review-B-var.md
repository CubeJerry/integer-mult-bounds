# Independent lead review: growing-arity rational Walsh circuits

Reviewed during S002 against the complete `kernel.tex` and `binary.tex` at
OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, the completed Route B
auxiliary-cost audit, the independently reviewed Newton/division note, and
the recovered finite contraction proof. This is AI-assisted mathematical
review; it is not a formal-kernel build or an implemented full transform.

## Verdict

The stated arithmetic/indexing bound is supported by the proof chain:

    O(2^k sqrt(k+1) 2^{C sqrt(log(k+2) log log(k+4))})

for normalized Walsh transforms at even k, over Q, with the source's
unit-cost word-indexing operations. Odd normalized widths require adjoining
sqrt(2); alternatively use the unnormalized rational transform. The result
does not supply a tape-time or integer-multiplication envelope.

## Critical points checked

1. The rounded L,q choices pay for the charged rectangles: q^(L/2)>=2^L m.
   Their contribution is therefore bounded without hiding an L-dependent
   constant. At ell=2, direction rank <=1+Lq and the source/destination
   incidence counts give the displayed R_m. The logarithmic estimate has
   absolute constants when L grows.
2. Every nonrecursive map in the source kernel proof is a row-linear map,
   a binary column map, a sign accumulated over columns, or one of the
   explicitly billed child transforms. The source's free-endpoint order
   is essential: inputs are transformed once per incidence and queries
   are accumulated before the destination's final transform. The coarse
   polynomial overcount in B-poly does not replace that sharing order.
3. Prefix enumeration has O(2^(Af)) edges even though a column tuple has
   2^A possibilities. Each edge uses polynomial-m word operations; the
   2^O(m) tuple and spectral tables are setup, explicitly charged. A new
   scan of all f columns per coordinate is not necessary in this model.
4. The Newton predictor and repair introduce rational constants with
   polynomial-m bit height. The source normalization argument still
   applies to these pointwise row maps: normalized child calls supply
   the common kernel factors, and forward/inverse spectral normalizations
   cancel. No remaining numerical coefficient has uncharged f-dependent
   bit height.
5. All label, seed, rectangle and contracted-batch dimensions are
   polynomial in m beyond the explicit coarse threshold. The finite
   contraction depth is O(log m), and its expanded instruction count is
   polynomial. Gaussian elimination and the explicitly given table
   inverses therefore fit the proposed conservative polynomial bounds.
6. W_m is a power of two. Choosing k-Af>=log2 W_m gives complete batches
   exactly; extra inactive bits are spectators. The even f choice leaves
   an even remainder at even k, so normalized four-point butterflies
   suffice over Q.
7. With gamma=1/1000 and K=50, ordinary work m^K is o(sqrt(k)). The setup
   2^(Cm)m^K is o(2^k). Dividing by sqrt(k+1) leaves recursive multiplier
   at most C(R_m+1). Along a path log(k+2) contracts geometrically, so
   its cumulative log multiplier is O(sqrt(log k log log k)). The finite
   depth factor is absorbed in that envelope.

## Material limits

This is an exact rational linear-circuit/source-word-model statement.
Variable bit precision, physical head travel, fixed-tape role serialization
and the cost of column reindexing are not free in the requested multiplier
model. The source tape interchange mechanism uses another characteristic,
and its compatibility with this rational replacement is disproved for the
direct count-only and unchanged-support lifts documented elsewhere.

The numerical-growth paragraph in B's audit remains a diagnostic, not a
complete finite-precision tape proof. No claim that this rate is absent from
all prior literature is made; the relevant primary-source overlap search is
recorded separately. The full finite arithmetic construction has not been
materialized at its enormous sufficient threshold. Existing exact toy
checks validate the local identities, not a large generated circuit.
