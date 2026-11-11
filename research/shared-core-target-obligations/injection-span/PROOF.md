# Core-write span is necessary for independent copied-main endpoints

**Optional elementary interface lemma; no new κ.** This is a quotient-space
invariant, not a new lower bound for general multiplication or priority claim
for linear control theory. Its useful strengthening of the fixed-selector
calculation is that the load weights and the entire shared-core dynamics may
vary arbitrarily. Changing only how the core reads copies cannot repair a
missing main mode when all writes remain in a proper fixed bank subspace.

## 1. Statement without bank mixing

Let F be a field, U a nonzero F-vector space, and m≥1. There are m main
banks x_1,...,x_m in U with arbitrary independent entering values. A fixed
finite chronological program alternates:

1. An F-linear main operation A on U, applied identically to every bank.
2. Shared-core operations and loads, whose internal behavior is unrestricted
   for this argument and which change mains only through the writes below.
3. Writes adding sums of vectors `v⊗z` to the bank vector, where v∈F^m and
   z∈U. All banks in one such term receive the same z with coefficients v.

Different writes may use different z and different v; z may depend on the
whole past and on dirty helpers. If sequential writes use different core
values, they are separate terms. Let M0 be the chronological product of the
identical main operations, excluding core writes. Fix a subspace R≤F^m
containing every write vector v. There are no other main modifications.

**Lemma.** For every row λ annihilating R, at every prefix

`Σ_c λ_c x_c(prefix) = M0_prefix(Σ_c λ_c x_c(entrance))`.

Consequently, if the required main endpoint is x'_c=E x_c for every c and
every independent entering bank, where E is F-linear, then E≠M0 implies
R=F^m. This necessity is independent of all load weights and core dynamics.

**Proof.** An identical main operation sends the left combination through
the same A. A write contributes `(λv)z=0`; core-only operations contribute
nothing. Induction gives the prefix identity. If R is proper, choose nonzero
λ in its annihilator. Under independent inputs, Σλ_c x_c ranges over all U:
choose a bank with λ_c≠0 and set only that bank to λ_c^-1 u. Correctness
therefore forces E u=M0 u for all u∈U, a contradiction. ∎

Full write span is necessary, not sufficient. It establishes no helper
restoration, chronology, paid saving, precision bound or construction.
Independence is essential: on the constrained diagonal x_1=...=x_m a fixed
selector can already give the desired repeated output without computing
every deviation mode. That constrained contract is not the selected supplier.

## 2. Uniform bank basis changes

Allow additional fixed, input-independent invertible scalar bank matrices
B∈GL_m(F), each applied
uniformly to all coordinates/roles of U. These are distinct from main
operations: they map x to `(B⊗I_U)x`. They commute with identical main
operations. Let B_total be their chronological product. For each write e
with vector v_e, let B_after,e be the product of bank matrices AFTER that
write, in their chronological operator order. Define

`R_eff = span{ B_after,e v_e : all write terms e }`.

The written scalar bank vectors are fixed program coefficients. If a larger
class permits input-dependent write vectors, R_eff must instead contain all
their possible transported values, so that its annihilator is fixed across
the input quantifier. Input-dependent bank basis matrices are not included.

Unrolling the program, its main return equals

`(B_total⊗M0)x + Σ_e (B_after,e v_e)⊗z'_e`,

where z'_e includes the subsequent identical main operations and may depend
on the entire original computation. No linearity assumption about that
dependence is needed to annihilate its bank factor.

**Effective-span lemma.** If E and M0 are linearly independent as operators
over F, a correct independent endpoint I_m⊗E requires R_eff=F^m.

**Proof.** Let μ annihilate R_eff. Applying μ to the displayed identity and
to the desired return, and varying one entering bank at a time, gives

`μ_c E = (μ B_total)_c M0` for each c.

Operator independence forces μ_c=0 for every c. Hence the annihilator of
R_eff is zero and R_eff=F^m. ∎

The independence premise cannot be weakened to E≠M0 when arbitrary basis
changes are allowed: if E=a M0 with a≠0, the scalar bank matrix aI can supply
that factor without a core. The selected complex source has a stronger
witness: C=E M0^-1 has off-diagonal entry C[17,129]=−3, so E is not a scalar
multiple of M0. Both are nonzero/invertible in that source.

In particular, arbitrary uniform bank matrices only at the entrance and
exit cannot rescue a proper original write span: then R_eff=B_exit R has
the same dimension as R. This covers noninverse pre/post matrices as well
as conjugating wrappers. It does NOT cover bank changes chosen separately
for different main roles; those do not generally commute with the main-only
sequence. Nor may raw span replace R_eff with interleaving. A bank swap
between two writes in the same raw direction can give two independent
effective output directions. The controls exhibit this escape explicitly.

## 3. Application, cost and research significance

Use the same exact selected complex source as the shared-core package:
canonical e54523517d0f03e58352e647c403a5af3e525a57,
`research/shared-wire-split-composition/data/final.json.gz`, Git blob
74563a7867d9d762b6588f65362369668841bb3e, SHA256
2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883.
Take U to be the400-main role vector tensored with complete array space.
Main copies have identical chart trajectories. Each allowed bank change
acts only between co-charted corresponding fields, at a cut after all
replicated MOVEs complete. All scalar coefficients stay exterior to tensor
powers. The existing exact counterexample C[17,129]=−3 establishes the
operator independence needed above; this note does not re-admit its source.

Thus an arbitrary redesign of shared-core loads, with all main writes still
collinear in the two-bank space, cannot give two independent selected main
endpoints. For example, loading changing sums/differences while always
broadcasting in direction (1,1) cannot work, even with arbitrary new core
logic and uniform bank matrices at its boundaries. A viable switching
construction must change write directions, or rotate their effective span
through interleaved bank changes, or change another stated interface premise.
This is a useful filter beyond the finite19600-family experiment; it is not
a proof that a full-span choice exists or fits the target budget.

No bank mixing is free in a proposed supplier. If a fixed matrix is factored
into a ADDs and s SCALEs on an m-component bank vector, applying it uniformly
to the400 roles costs400a whole-field ADDs and400s SCALEs at that cut; repeat
for every actual matrix and native occurrence. Coefficients, full volume,
routing/field identity and a new precision envelope must be charged under
the actual physical service tariffs. There is no new productive helper
credit or omitted Gaussian job. The impossibility statement grants these
bank changes without cost, so charging them cannot invalidate it.

The argument is mathematically immediate from an annihilating linear
functional. It is recommended as an optional refinement/search condition
inside the shared-core package, not a standalone research claim or PR.
The actual high-upside obligation remains a fully paid changing-write
itinerary with enough effective directions, arbitrary helper restoration,
the coupled-port endpoints and sufficient joint owned savings. No κ is
changed and all five foundational assumptions remain unchanged.

Prepared for @CubeJerry with substantial OpenAI assistance. Existing native,
fixed-selector and BIT authors retain their credit. No human or formal-kernel
acceptance or novelty priority for the underlying linear algebra is claimed.
