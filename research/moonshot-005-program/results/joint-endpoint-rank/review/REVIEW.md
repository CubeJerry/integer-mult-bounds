# Independent review of the joint Y2 endpoint gate

**PASS for the stated algebraic/source interface theorem. No new physical
encoded word, restoration algorithm, cost lower bound or kappa is admitted.**
The exact reviewed files are pinned in output/REVIEW.json. This review does
not import or execute the author's verifier or independent_engine.py.

## Algebra and the delivered-baseline distinction

For independent b,d, the encoded source outputs are b+RPd and Pd. If a baseline
Kd has actually been transported and subtracted, the errors against b-d,d are
E(P,K)=[I+RP-K;P-I]. Subtracting R times the lower block from the upper gives
[M-K;P-I], M=I+R. For a full kernel basis Z_K of M-K, the common kernel with
P-I has dimension nullity(M-K)-rank((P-I)Z_K). Therefore

    rank E(P,K)=rank(M-K)+rank((P-I)Z_K).

No invertibility of P is needed for this identity; a physical singular encoder
would have additional preservation obligations. The identity holds for arbitrary
compatible matrices and fields. Fixed rational source conclusions extend to
characteristic-zero fields. Tensoring the scalar maps with identity of field
volume V multiplies all ranks by V.

The two source conclusions are different and both correct. With K=0,
systematic B coding gives joint rank96. With an actually supplied K=G,
systematic pivots I give96-|B∩I|, whose minimum88 is attained by I=B. This
preserves rather than improves the current joint rank88. The original-Y2
errors remain among the required outputs in both cases.

Copying a coded pivot at its facet is not itself delivery of Kd. The proposed
eight facet-to-hub copies and360 hub additions factor G only when those
operations occur. This review checks that factor algebra, but neither package
emits the extra physical word. No free-K interpretation is accepted.

## Independent source reconstruction

The review reconstructs the actual rank88 word in a different input basis:
1480 common u coordinates and400 private differences q. An initial private
input v has row u+q. This is an invertible change of all1880 coordinates,
not a restriction of the input domain. A new sparse interpreter checks every
prefix operation, nested chart move, cochart read, ownership declaration and
copy-zero guard.

The hosted X2 boundary rows are exactly b+Rd, and the hosted Y2 rows exactly
d, with no other input contamination. The review derives G through the
eight-coordinate root realization normalized by8, while the author uses
the separate nine-coordinate realization normalized by18. The resulting G
and both reciprocal blocks of the current R agree exactly.

An explicit eight-column kernel with identity rows on S and a nonzero modular
88-minor prove exact current rank88. For M-G, its B columns are zero and a
nonzero88-minor gives exact rank88. Modular calculations provide lower-rank
witnesses; explicit kernels and the general proof supply the upper ranks.
No approximate numerical rank is used.

A new basis outside B∪S is [110,109,108,106,102,97,91,84], with integer root
matrix determinant768. This differs from the author's ascending-role basis
and directly certifies the needed outside spanning property. The older paired-
eight kernel follows from its block equations without root moments or I-G
invertibility, as the companion correctly explains.

For every overlap0 through8, the review chooses new pivot examples using
roots outside both B and S. It computes their rational inverses and verifies
the compressed defect8-overlap and the full joint stack. The universal theorem
follows from independence of the nonzero B\I columns of A_I^{-1}A_B; these
finite examples corroborate it without replacing its proof.

## Current rows and original-output restoration

The actual source is replayed a second time with systematic coded Y2 inputs.
Its X2 rows are b+RPd, confirming that every old read uses the encoded current
row. There are3638 nonzero coefficients in R(P-I); using stale original d
would materially change the literal source map.

All eight pivot Y2 endpoint rows remain changed: they are Pd, not d. The
entire remaining suffix was also scanned. Each of the192 hosted X2/Y2 raw
fields appears exactly once in its final literal recoupling ADD. There is
no later raw feedback or hidden restoration that removes P-I. Thus the debt
is present at the actual output interface, even when its row space overlaps
other correction duties.

The proposed counts are consistent:352 off-pivot encoder additions, eight
copy additions,360 baseline additions and eight new owned rank1 calls. These
are counts for an unadmitted proposal. Actual lifetimes, phase maps, precision,
and complete correction and erasure costs remain separate obligations.

## Negative controls and limits

A B-coordinate column is nonzero in the no-K map and becomes zero only after
subtracting G; silently crediting a baseline is detected. The coded replay
detects stale d reads. Explicit Y2 rows and the suffix audit detect dropping
restoration from the endpoint stack. These checks address three separate
interface errors rather than rerunning the author's checker.

The theorem is a rank identity for a specified correction interface. Rank
alone does not price corrections or establish a global multiplication bound.
New b-side shears, useful common history, changed supplied K, mixed current
rows, funded transport or another output representation can alter its premises.
The author keeps these limitations visible. No correction to its frozen claims
is needed.

Run:

    python3 check.py --repo REPOSITORY --author JOINT_ENDPOINT_PACKAGE --output OUTPUT

Prepared for @CubeJerry with OpenAI assistance. This is an independent agent
mathematical/source review, not a human or formal theorem-prover review.
