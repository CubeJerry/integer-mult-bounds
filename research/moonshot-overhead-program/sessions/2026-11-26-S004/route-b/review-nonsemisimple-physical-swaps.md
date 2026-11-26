# Independent review: actual swap orbits in every characteristic

Reviewer: S004 Route B. Reviewed the full frozen Route C note
`nonsemisimple-physical-swap-corollary.md` and its NS1--NS4 claims.

**Verdict: the bridge passes.** The regular-rank sector proof requires
the reduced monomial basis and an invertible cyclic shift, not
diagonalizability or a spectral decomposition. The actual swap-orbit
construction supplies that basis even over characteristic two.

For any field, K[x]/(x^r-1) is free on 1,x,...,x^(r-1), and x acts
by the cyclic basis permutation. Tensoring these bases and applying the
equivariant plurality tie rule produces equal cyclic sectors exactly as
before. The kernel comparison, boundary-column rank estimate, block
completion and inverse rank identity are field-independent. Only the
previous spectral-average interpretation must be dropped.

On the actual [q]^2 basis, the q equal pairs are fixed and each unordered
unequal pair gives one independent regular two-cycle. Their total
fraction is (q-1)/q. Tensor dimensions therefore give precisely the
Poisson-binomial law and pi_0=product(1/q_j) in NS1. Every allowed query
preserves these original orbit strata; on an active coordinate it is
multiplication by x_j and on a fixed coordinate it is the identity.
An invertible query restricts invertibly to each stratum, so the inverse
is covered. Sector completion may use the enlarged comparison space;
it need not be a new physically allowed map.

Deleting arbitrary ports globally retains their actual rank cost even
if they mix strata. With those deletions the entire comparison network
preserves phases, so the telescope gives NS2. The same projection and
completion estimates prove NS3 and both orders of noncommuting
fractions, including one payment for denominator nullity in the singular
variant. No restriction of an arbitrary port network to a stratum is
silently used.

For NS4, on K_*>=mu/2>=m/4 the binomial boundary has at most 2d+1
integer levels, each with mass at most 1/sqrt(K_*+1)<=2/sqrt(m).
The complementary probability is at most 4/mu<=8/m. This proves the
displayed uniform bound; d=0 is correctly handled separately with zero
off-sector rank. The exact upper witness is valid over every field:
T-I has rank one on a two-cycle, including characteristic two, and zero
on a fixed vector. Hence its rank is exactly (D-F)/2.

The exclusions of address masks, comparisons and arbitrary payload
permutations matter. Such maps can fail to belong to the swap algebra
and are not free constant row maps. Nothing here prices their physical
execution or excludes general bit algorithms. The ordinary orbit proof
properly avoids the false characteristic-two argument that a swap's
single eigenvalue determines its rank error.

## Isolated exact replay

Copied the author checker and its three helpers into
`route-b-work/nonsemisimple-swaps-replay/` and executed it there.
All counts match: 12 regular-cycle rank identities including
characteristics dividing the cycle order; 1,461 actual swap-boundary
column checks; 14 exact identity-predictor baselines; seven actual
multiplicity mixtures; four characteristic-two inverse/strata-mixing
port controls; and 1,000 exact binomial atom bounds. The tested physical
dimensions ranged from four to 256 with unequal q_j included.
The sole-eigenvalue characteristic-two negative control passed.
Checker SHA-256:
`1365263557294e9ad6a1289a640cd07a38f9ea6d74f1cee3d38db31c3c2d3c2c`.

Prepared for @CubeJerry with substantial ChatGPT assistance.
