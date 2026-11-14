# Acyclic acquisition filtration for arbitrary local block decoders

**Proved universal matrix theorem and scoped physical consequences; independently
reviewed. No new complete kappa.** This adapts established acyclic index-coding
reasoning to the programme's actual acquisition/decoder interface; no global
literature novelty claim is made.

Partition n whole-V source blocks into cohorts. Let P have zero own-cohort
blocks, with acquisition row j supported on s_j other cohorts, and let U be
cohort block diagonal, possibly singular and internally noncommuting. For
A=I-UP, a kernel filtration proves

    rank A >= V max_order(good acquisition rows)
           >= V ceil(sum_j 1/(s_j+1)).

A row is good when its target cohort precedes every source cohort it reads.
If all s_j<=k, rank A>=V ceil(n/(k+1)), sharp algebraically over every field.
Rectangular b-row acquisition gives V(n-b+max_order good). Thus extra helper
observations change the interface and cannot be inserted into the square case.

With n111 and q8/9/10 FIXED global X modes, maximum support is at least13/12/11,
and total input-cohort incidences at least1430/1258/1122. In particular, one
foreign source cohort per row requires56 modes even with singular decoding.
The transpose version applies to actual input-column supports. Pure one-stop
104-input complex collectors need at least52 fixed modes; the parity pairing's
optimized order recovers its sharper56 gate. Actual X pre-encoders can spread
input coefficients, and moving packets can have more historical modes than
packet identities. Neither escape is excluded without proving its own premise.

[Proof](author/PROOF.md), [corollaries](author/COROLLARIES.md),
[independent review](review-c/REVIEW.md), [literature credit](author/LITERATURE.md).
Root controls cover324 matrix cases and9288 filtration increments; C's separate
exhaustive-kernel checker covers648 cases,579 singular U and12976 increments,
plus234 sharpness controls. These support the universal argument, not replace it.

```bash
python3 -I -B research/moonshot-005-program/results/cohort-acquisition-rank/author/check.py --output /tmp/cohort-author.json
python3 -I -B research/moonshot-005-program/results/cohort-acquisition-rank/review-c/check.py --package research/moonshot-005-program/results/cohort-acquisition-rank/author --output /tmp/cohort-review.json
```

Credit C's acquisition question, root's stronger filtration and rectangular
extension, C's independent review, the cited Bar-Yossef/Birk/Jayram/Kol acyclic
method, native predecessors and @CubeJerry. OpenAI assistance. All supplier,
physical/compiler, ownership, precision and recursive obligations remain.
Baseline5a9ddf74c3aff42df5617e594c6ac3b85b1881d4.
