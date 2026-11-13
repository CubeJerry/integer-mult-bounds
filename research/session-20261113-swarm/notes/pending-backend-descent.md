# Compact CNOT / ordinary BIT descent audit checkpoint

Started 2026-11-13 11:09:24 UTC; bounded gate ends by 11:54:24 UTC.
Canonical main: e54523517d0f03e58352e647c403a5af3e525a57.
No graph implementation or publication is authorized in this gate.

Named first call: one width-u=(f-1)G dirty-control shuttle inside the
earlier-source compact CNOT, G=4 ceil(log2 p)+6. Its caller has complete
arbitrary fields and arbitrary spectator/payload dimensions. f=1 is the
elementary no-shuttle case. f>=2 has u>=1.

Preliminary source finding: current #7001 binding explicitly freezes the
ordinary backend chain .0034 -> .0038507 -> .00385248. Cover transports
and stopped atom leaves use the completed predecessor, not the current
ordinary backend. Same-stage weighted children have atom width at most
floor(n/N_B)<n. No source edge read so far calls the complex compact CNOT
again. This supports a backend-stage / service-kind / atom-count induction,
relative to the source-bound completed .0034 backend premise.

Important outstanding distinctions: (1) fG can exceed f and is not a
descent measure; (2) the current conservative BIT carrier is
N_B=2^296630000000000, not the archived 127-axis certificate's earlier
2^293160000000000; (3) a batched BIT child retains the whole high-matrix
cover as an ancestor spectator, so its physical volume is V/W0 for fixed
low-type role count W0, not V/W(w); (4) arithmetic uses exact local-ring
address words, not the complex coefficient precision; (5) all physical
implementation/old-backend premises remain explicit.

Sources already read: compact-control-movement.tex, three-stage-cover-bit.tex,
upstream04 arbitrary-width interchange, DELAYED-COVER-BRIDGE.md, #7001
paired-query-only-bit/{README,PROOF,INPUT-PINS,EFREE-RESULT}, and both current
#7000 admission/application reviews. Exact pins and final dependency table
will be written before the bounded gate ends.
