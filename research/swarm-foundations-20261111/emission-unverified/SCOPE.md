# Wave 5 emitted-word bound: unverified scope

Base e54523517d0f03e58352e647c403a5af3e525a57; tracks 54/81.
No implementation or new theorem is claimed at this checkpoint.
Published count dependency: CubeJerry commit
022461f115369efd988ef8c459907f5544bb8bb3,
research/quantitative-rank-library. library.py SHA256
06e3b44704048461de0ff0ab55fe158b95df412688324b88fd3d81b929ef0d92;
PROOF.md 05a04e5ba1db71b9e40397e3220f047411906a5e8a70609c7a879499e6325e88.

## Exact proposed implication and optimistic budget

Work on the common domain m=A=max target rank, strict r_max<k_min,
default height and least chronological replication. The published evaluator
does not yet cover a larger ambient A; do not transfer it silently.

Candidate structural lemma: the fully expanded rank-induction tree has at
most P_N+O_N activations. Moreover, the sum of productive widths B_q over
all those activations is at most P_N+W*O_N. A nonbase activation contributes
local a_q*U_q>=1 raw units and B_q=a_q*S_q<=W*a_q*U_q. A base activation
has width one and contributes at least one rank-one leaf. These local
charges partition O_N and P_N. No rank surplus is needed.

This does not yet bound actual code. With a fixed concrete native word of
input length L_raw, set Q=1+max_(q<=N)(P_q+O_q) and
H=1+L_raw+bit_length(N+Q+1). Investigate a conservative skeleton with
O_raw(Q^2) field/call sites and O_raw(N^2*Q^2*H) descriptor bits. If a
source-bound adapter producer emits A(N,H) bits in F(N,H) paid bit work
per site, target the explicit reduction

    code <= O_raw(N^2*Q^2*H + Q^2*A(N,H));
    construction <= poly(N,Q,H) + O_raw(Q^2*F(N,H)).

These envelopes remain unverified pending an actual emitter grammar.
Polynomial A,F would imply quasipolynomial code/construction using the
published count theorem. Semantic existence of finite adapters alone does
not imply polynomial A,F. Full copying, matching, sorting, owner IDs,
constants, inverse returns and written output must be included.

## Source findings and remaining boundary

FINITE-PRECOMPILATION sections 1,4,6 explicitly requires whole-job adapters
and finite closure (blob 4badb40f0919c515823cb07e44c6470d4d6469ca).
#6878 constructs order(A,N), complete complements, at most N-1 swaps,
inverse returns and occurrence-specific field conjugations (PROOF blob
152fcd41486dc8d078ae2a77cb3e6a26c37e8e10). Its COST blob
4f811a465093c5e489d8c2b67025e99810919c2c pays fixed-template runtime,
not uniform-in-N word generation. Raw whole-job normalizers remain inputs.
The current #7000 review bounds binary-monomial decomposition by
4(n+1)^2 elementary records; data production still must be bound.
#4638 and #4586 explicitly leave actual emitted-word/caller consequences
outside their width result.

Next inspect whether a fixed literal native scalar word supplies explicit
matrix/phase/scalar and normalizer records supporting a uniformly priced
tensor/relocation producer. A one-column word, an abstract all-column
service and an explicit all-column record schema are different inputs.
Do not tensor ADD/matrix sums or materialize a 2^N-dimensional operator.

## Overlap and stopping rule

Read #6878, #4638/#4586, #6743, expanded-count audit, selected source and
visitation bridge audits, physical-compiler-correspondence, production-low-
code compiler, coded/compact compiler parameter packages and canonical
directory metadata. Targeted live searches cover compiler construction
time, word size, emitted/quasipolynomial and owner/code size. No same
uniform encoded-word theorem found in those bounded reads; this is not an
exhaustive novelty claim. No duplicate generic routing implementation.
If source evidence does not supply the producer, finish a precise
conditional reduction/checkpoint. No new kappa or assumption discharge.
