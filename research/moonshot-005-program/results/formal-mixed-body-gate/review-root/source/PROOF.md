# A formal fresh-body grading obstruction

**Proved in the explicit graded algebra below. No general physical R0 exclusion and no new κ.** A mixed-slope primitive used once in each fresh body variable cannot produce only the complete-body degree when every intervening operation is invertible and body-even. Arbitrarily many body-even head queries do not change this conclusion.

## Exact premise

Let B be a unital algebra. Suppose an algebra R contains central invertible d1,...,dm and is the direct B-module sum of d1^e1...dm^em B for all binary vectors e. Assume each d_s² is an invertible central element of B. This unique parity expansion is an explicit premise, not a consequence of assigning symbols to actual matrices. Examples include independent Laurent variables over their even-power algebra, and formal independent signs d_s²=1. Over characteristic zero, the sign example is equivalently the unique Walsh expansion on all2^m sign choices.

On two k-dimensional banks let each distinct fresh primitive occur exactly once, in the form

\[
N_s=d_sE_s+C_s,\qquad E_s\in GL_{2k}(B),\quad0\ne C_s\in M_{2k}(B).
\]

The commuting mixed-slope model has diagonal(d_sI,d_s^-1I) and a nonzero cross P_s∈B. Thus E_s=diag(I,d_s^-2I) is invertible and C_s is its body-even cross block. Opposite slopes, ordinary signs, role swaps and an even body-square correction satisfy the same model.

Allow arbitrary invertible interleavings G_j∈GL_(2k)(B), including any number of head queries, even body operations and ordinary invertible role/port mixing in B. There are two fixed banks and no erasure or singular projection. The theorem does not require the head operators to commute with one another; it does require central independent body degrees as specified.

## Nonzero incomplete-body component

For the chronological product

\[
W=G_mN_mG_{m-1}\cdots N_1G_0,
\]

the coefficient of body degree(1,...,1)−e_s is nonzero for every s.

Indeed exactly one term selection has that degree: choose C_s at stage s and d_jE_j at every other stage. Its coefficient is an invertible product on the left of C_s and an invertible product on its right. It cannot vanish. The direct-sum premise prohibits cancellation against a different parity component. This proves the claim for every m and all permitted interleavings.

For m=2 the degree(0,1) coefficient is exactly G2 E2 G1 C1 G0. Hence W cannot equal d1d2 times any B-valued matrix. In particular it cannot give two independent Q^-1d1d2 targets, even after B-valued output adapters. Additional body-even queries are already included in the G_j and do not help. Over a field, a cross block of rank k gives an incomplete-body component of the same rank k.

## Scope and sharp premise controls

The independent fresh degrees and invertibility are essential. If the same body is used twice, opposite nilpotent cross terms can cancel: for C²=0 and d²=1, (dI+C)(dI−C)=I. A singular projection can kill a cross term but loses independent inputs. A homogeneous standard primitive d_s(I+C_s) has no incomplete-body component; the statement therefore does not prohibit the separately proved common-Q two-native construction.

It is also essential to justify the algebra map for actual operators. An actual finite-order matrix need not admit a sign substitution that fixes its declared even algebra. For example, over Q(i), D=diag(1,i) satisfies

\[
D=\frac{1+i}{2}I+\frac{1-i}{2}D^2.
\]

Replacing D by −D while fixing I and D² violates this relation. This example is a warning against an unproved specialization, not an assertion that the physical rank-eight body has exactly this spectrum or relation. The present theorem alone is not a physical R0 caller exclusion. A separate source-bound invariant-fibre proof can establish an appropriate sign model for a restricted actual adapter algebra.

The argument fixes two banks and uses every distinct body exactly once. Repeated body occurrences, paid idles, additional independent fields, noninvertible intermediate projections, or adapters that change the actual physical body representation require a new proof and complete accounting. No impossibility claim is made for these mechanisms.

## Reproduction and classification

`python check.py --output RESULT.json` and `python -O check.py --output RESULT-OPTIMIZED.json` independently evaluate64 rational two-stage interleavings on all four sign choices, recover the nonzero rank-one Walsh component, and check invertibility. The checker also verifies repeated-body cancellation, a homogeneous-source positive control, the information-losing projection, and the exact Gaussian-rational specialization counterexample. These finite controls illustrate the hypotheses; the displayed unique-degree argument is the universal proof.

Status: **proved in the explicit graded model**. Physical R0 applicability remains conditional on a separately established representation of that model. This package supplies no complete multiplication bound, no new supplier and **No new κ**. Worker C developed the formal obstruction in the persistent programme for @CubeJerry with OpenAI assistance; Worker A's independently developed actual Fourier-fibre bridge is a separate source-bound result.
