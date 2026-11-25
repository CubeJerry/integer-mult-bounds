# Lead admission of the complete polynomial-profile theorem

Admitted during the live E002 session, 26 November 2026 Melbourne.
Status: **complete written unconditional algorithm/profile construction**
within the pinned source model. This is a mathematical review result with
finite exact supporting checks. It is not human refereeing, full execution,
a Lean refinement or a claim of literature priority.

## Result

With L=1+log2 n and x=log2 L, Theorem P gives

    T(n)=O(n sqrt(L) 2^{O(x^(3/4)(log2(x+2))^(1/4))}),
    cells ever visited=O(n),

for one fixed deterministic finite-alphabet multitape machine computing
the exact full product at every length. It implies every fixed-beta
benchmark beta>3/4, for example beta=4/5. The logarithmic factor remains;
no beta=3/4 log-free, polynomial-x or constant overhead is admitted.
No value of kappa_ov is assigned because this is not the x^alpha scale.

## Review chain

The lead read the complete component proofs and all independent receipts.
A and C separately read the global theorem and accepted P2--P11 at SHA256
`319601f989b4696d5328fbe42673bcce2b9f026e30b9b1d29a16f5d3d18274dd`.
Their reviews are `../route-a/REVIEW-GLOBAL-POLYNOMIAL-PROFILE.md` and
`../route-c/review-polynomial-profile.md`. Subsequent changes to the theorem
at this gate alter status wording only; the mathematical statements and
proof of P2--P11 are unchanged.

The lead's checks included: exact rational height dependence; signed and
ragged affine runs; fixed-tape row ordering; cyclic path masks on input
grades; power-two signed-count truncation; F4 discrepancy repair with a
transpose inverse and containing zero gaps; true independent module
occupancy; small compatible radix; finite-control regrouping; exact full
call margins; numerical rational selection and scaling; fixed precision;
source guarded permutations; outer integer rounding/carries; additive
setup absorption; dyadic candidate admissibility; and one visited-cell cap.

The principal composition corrections were substantive and are retained:

1. Grouping module rows preserves the summed time invoice but changes the
   largest individual child fraction to at most 2/N_label<=2/3. The old
   2/W single-row fraction is not used after grouping.
2. The numerical Walsh toll includes active width a^rho from its calls to
   the independently proved interchanger. B amended E/S2 to a two-tier
   contract. The whole theorem already used the correct P6 recurrence.
3. Metadata is stripped before children, and the exact interchange field
   encoding is unchanged across its internal recursion.
4. The numerical leading spectator padding is global to W_F^j, so internal
   child volumes are exactly V/W_F. If local padding were used instead,
   its extra factor would need its own recursive invoice.
5. Polynomial-time coefficient emission is distinct from applying a
   coefficient to a k-bit numerical payload; W1 prices the latter.

The corrected B transfer snapshot has SHA256
`0290ece9913c8398fbe1342d2171f627fcb2f8f9fee037f492296a4acd732970`.
All global reviewers explicitly used the amended version. The earlier
checkpoint remains historical evidence of the correction, not the admitted
premise set.

## Finite and source evidence

The lead ran the five component checkers in fresh temporary directories.
Their copied-source hashes, JSON receipts, exit statuses and captured output
are in `../lead-component-replays.json`. They cover rational affine stream
permutations, compatible radix batching, succinct cyclic factors, rational
Walsh repair/rounding, and the characteristic-two spectral repair. Negative
controls detect sign, padding, grade, transpose and coefficient-domain
errors. These finite checks do not prove the universal asymptotic theorem;
the written proofs and their composition supply it.

Fresh source reading included the complete tape interchange, permutations,
Walsh and single-machine argument; integer packing/CRT/final error sections;
the source introduction and formalization scope; Fourier binary normalization
and kernel endpoint/saving sections; and the detailed predecessor finite
construction, height and compiler interfaces. A independently read the whole
outer integer proof. The imported source theorem on synchronized occupied
short Fourier transforms is retained as a proved source input, rather than
claimed to have a new independent derivation here.

The OpenAI formalization scope note and actual NearSquareRoot Main.lean
were read, as were the independent comparator statement and its instructions.
No fresh Lean build or transitive formal-dependency audit was performed.
The new E002 operations have not been formally connected to that development.

## What remains

The expanded proportional-cost bottleneck has been replaced by polynomial
compact execution. The retained geometry still has log m=O(J^3 log J).
Balancing its polynomial-m prefactor with x/J gives the admitted 3/4 power.
A's literal-invoice obstruction explains why merely retuning that sufficient
fixed-family invoice has the same scale; it is not a machine lower bound.

The protected variable-arity route is separate. It must establish charged
changing-radix interfaces, sufficiently small proportional workspace,
compatible field encoding and the numerical Walsh toll before a stronger
global envelope can be admitted. Its prospective 2/3 scale is not used here.
The endpoint, polynomial-x overhead and all general runtime lower bounds
remain open in this session.

Credits: Jerry Chen (@CubeJerry), OpenAI source authors and cited earlier
work, the preceding S002/E001 programme proofs, E002 Routes A/B/C and lead,
and substantial ChatGPT multi-agent mathematical assistance. Concurrent
S003 checkpoint `a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32` is preserved;
its parallel compact-factor/batching work has separate provenance and is
not claimed as an E002 discovery.
