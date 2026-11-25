# Source interface audit: a sequence of different pencils

Status: **independently checked against the pinned source**. The formula
construction may use D different affine pencils. No downstream interface
requires repetitions of one matrix.

Source pin: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`.
The cited files are in the November 24, 2026 Fourier or tape preprint's
`build/` directory.

## 1. What the predictor evaluator must deliver

Fourier `repair.tex`, Equation `repair-pencil`, defines a stage by
`A_0 tensor I + sum_(j,a) A_(j,a) tensor Q_j^a`, with arbitrary fixed row
matrices. Repetitions of a matrix root are the source's particular way
to supply P, not a hypothesis of its Full-rate Hermite repair lemma.

That lemma requires only that the **completed** operator P have the known
row multipliers p_i at each frequency, agreeing with the target outside a
known small set. Formula factorization supplies `P_beta I` on every row
of each shift block. Individual factors may mix these rows. The proof
never applies the error-support assertion to an unfinished application.

To form `P^k X`, rerun the complete ordered D-stage list k times. Do not
replace each factor by its k-th power or reorder the factors. The binary
repair's four applications then use at most 4D stages instead of 4b, with
b>=D. Check/table fractions are unchanged for the newly chosen batch.

## 2. Fourier routing is a per-stage statement

In Fourier `kernel.tex`, "Sharing the queries of a pencil" routes an
arbitrary row matrix `B_(j,a)` multiplying each query. Its endpoint proof
uses that row mixing commutes with an address transform. It never compares
the matrices of two different stages. Equation `kernel-pencil-cost` is
therefore applied D times and the resulting invoices are added.

Label directions, rectangles and endpoint layouts can be reused as finite
descriptions, while every physical execution remains charged per stage.
The scalar-basis descent in "The finite saving and recursion" applies to
any such finite program whose target has base coefficients and which
accepts arbitrary extension-valued inputs.

## 3. Tape routing is also a per-stage statement

Tape `interchange.tex`, Equation `interchange-pencil`, fixes arbitrary A_j
independent of the **label**, for one stage. Equation
`interchange-stage-cost` bounds that stage. Rectangle and low-rank delivery
apply A_j pointwise to aligned sums and never assume that the next stage
has the same matrix.

Predictor shifts belong to the internal row index. Their direct sum is
copied identically at each routing label, preserving label-independence at
every factor position. The geometry does not depend on the active factor.
The source then multiplies the per-stage bound by the number of stages
and adds the spectral-repair invoice. Replacing 4b by 4D preserves that
conservative call test. Each stage restores the reserves and ordinary
layout before the next begins.

## 4. Normalization, stability and physical data

Fourier `binary.tex`, Proposition `binary-template`, admits a finite list
of pointwise row operations. Its normalized-kernel argument absorbs
normalizations into each axis call. Its stability proof bounds each fixed
stage and telescopes their product; it does not require identical stages.

Tape `walsh.tex`, "A batch of transforms", imports a finite instruction
list and fixed finite dyadic coefficient list. Basis descent places all
the different formula stages in that interface. Their whole coefficient
list and norm bounds are charged by P_m and the compiler precision ledger.

This audit closes the repeated-pencil interface concern. It does not
replace the separate formula, generator, routing and complete-machine
proofs. Credits: OpenAI source proofs; Jerry Chen (@CubeJerry);
AI-assisted independent source audit during session S002.
