# Independent review of the representative obstruction and its volume count

Reviewer: E002 conditional review C. Gate: **PASS for the complete scoped algebraic and literal-executor counting statements**.

Reviewed Route B `query-representative-obstruction.md`, SHA-256:

`bf0edde5973aa5b29fccb163f06ceb0d644bc264acaf41170e95801793729079`.

This review includes the newly added Section 6, QR4 and QR5. It does not rely on the older Route C review, which accepted only the earlier snapshot. I read the complete current note, the pinned Fourier `kernel.tex` in full, the actual Newton recurrence in `routes/B/pairwise-newton-division.md`, and the companion `numerical-address-invoice-gate.md`.

## 1. The shared coset obstruction

The source chooses d_v with self-pairing one in its actual nondegenerate quotient. Its original distinguished value is therefore the functional `<d_v,x>`, and H is orthogonal to every source direction of a free rectangle. This functional descends to the intrinsic coset x+H. The first partial endpoint transform does not change that coset. Common representative changes identify the same coset for each source; they are not independently chosen abstract quotient relabelings.

A common distinguished coordinate preserved by all source conversions must consequently equal `<d_v,x>` for every source and every x. Nondegeneracy forces all d_v to coincide. This holds even for nonlinear auxiliary permutations, since they are prohibited from changing the distinguished coordinate. Phases also do not move a record between cosets. The distinction between equality of vector classes modulo H and equality of functionals on the quotient is correctly maintained.

For q>=3 the probe argument distinguishes the actual Gram rows for every two different labels. Choosing a letter different from both at every differing coordinate first makes their distance parities equal, and changing one such probe coordinate toggles only one parity. This proves distinctness in the radical quotient, rather than merely in a larger formal label vector space. The excluded q=2 case really can collapse labels to parity classes.

The canonical two-by-two rectangle in QR3 has distance exactly one across its sides, so its cross Gram values vanish, its free weight is nonzero, and its source directions are distinct. Evaluating at the first source vector gives the conflicting distinguished values one and zero. Thus Sections 1–5 establish the claimed obstruction to auxiliary-only conversion, with the stated limits on its scope.

## 2. Exact normalized volume in Section 6

Fixing one coordinate avoids any double count across coordinate choices. For each of q^(L-1) common assignments to the other positions, there are q/4 consecutive four-letter blocks and two orientations. Hence the selected family has exactly

`q^(L-1) (q/4) 2 = N/2`

rectangles. Both source letters in each chosen oriented rectangle have exactly that rectangle as their selected source-side occurrence. The source sides therefore partition all N labels.

These are actual canonical first-differing-bit parts at the penultimate bit, with the preceding prefix fixed. The other positions are equal, so every cross pair has distance one. Their source coefficient is `-p(1)`, and every factor `1-1/(2r)` is nonzero. There is consequently no zero-weight term that could simply be discarded from this chosen family.

For each query, QR1 forces at least one of the two source maps in every rectangle to change its distinguished value. In the literal executor, applying such a map to one source stream is charged its entire input stream volume V/N. Thus N/2 required map applications have aggregate input volume at least V/2. This is a count of applications to streams, not a claim that every record in each stream changes location. The distinction is required and is consistent with the note's definition.

The actual Newton update is

`V_h=(C-(u+h-1)I)V_(h-1)/h`,

where `C=(mI-sum_j (-1)^beta_j Q_j)/2`. Every query coefficient is therefore nonzero and has magnitude `1/(2h)`. There are D=Theta(sqrt m) such stages above the retained direct base. Their active array has the original predictor row volume; the parked accumulator is not counted as extra independent input. The executor that separately runs each source/rectangle/query conversion consequently exposes at least order `D m V = m^(3/2)V` aggregate nontrivial-map input volume. The finite repair contains the root predictor execution, so dividing by the full batch input does not remove that root contribution.

Later Newton arrays can have algebraic spectral dependencies. QR5 counts the fixed, specified executor's applications of these maps; it does not assert that an adaptive or algebraically restructured algorithm has to execute the same list. The note correctly leaves cancellation, batching, shared passes and new layouts outside its conclusion.

## 3. Relation to the conditional transfer

QR5 does not falsify RV-W in the conditional rectangle-volume theorem. RV-W allows a fixed polynomial-m ordinary address bill, and the log-free two-thirds numerical schedule explicitly pays it. QR5 instead blocks one attempted path to the stronger NI5 address invoice: merely making each individual matrix factorization cheaper while retaining a separate full-volume f-field primitive for every source/query map still pays order m^(3/2) normalized application volume.

The conditional statement attached to QR5 is essential: a compiler must actually bill at least one such full-volume primitive for every nontrivial map before the application count becomes a lower bound on that compiler's primitive-volume invoice. The argument proves no sqrt(f) physical cost per map, no unavoidable number of tape passes, no lower bound for alternative batching, and no lower bound for multiplication. It also does not prove that the surviving map family cannot be executed more cheaply by exploiting its structure.

## 4. Independent finite replay

I read the complete strengthened checker and copied it, with its exact source note, into `e002-review-c/replay-query/`. The isolated replay completed successfully at 2026-11-25T23:23:49.469036+00:00.

- Checker SHA-256: `186ebdee556ccbd21294d8e073445cf28e339cdff82299a8e01d68b7e46fe62f`.
- 135,392 distinct-label probes and 135,392 unchanged-probe controls passed.
- Fifteen canonical free-rectangle conflicts passed.
- Fifteen source-side partitions contained 14,688 source labels and 7,344 necessarily nontrivial source-stream applications.
- Seven q=2 noninjectivity controls passed.

The replay supports the exact finite Gram and partition identities. The universal obstruction uses the written nondegeneracy argument, and the asymptotic m^(3/2) count additionally uses the written Newton recurrence. The checker does not execute a Fourier algorithm or measure actual tape cost.

Credits: @CubeJerry; the pinned Fourier endpoint construction and retained rational Newton predictor; Route B's precise scoped theorem; substantial ChatGPT multi-agent assistance. No formal proof, full execution or physical lower bound is claimed.
