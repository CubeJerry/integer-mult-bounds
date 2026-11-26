# Lead independent review of the spectator-span Fourier lift

Decision: **accept SF1–SF10 as exact full-rate algebra and SF11–SF17 as
the stated conditional physical transfer**. FC is open; no unconditional
improvement follows. Reviewed proof SHA-256:
b1ae83efcc202e289131ae96024735ac6dc6df33667c39f883abe55fdf29d2ff.

The lead read the complete proof, compared it with the already read RO
compiler and source interfaces, and replayed the author checker in a
fresh directory. The replay is not a second checker implementation.

## Algebra and full-rate accounting

For each ordered spectator matrix B, its RREF basis [I R] with standard
nonpivot complement is invertible even when the restricted dot product
on U=span(B) is degenerate. The number of B of rank r is the number of
subspaces times h(A-1,r) full-column-rank coefficient matrices. Multiplying
by all 2^f first rows and summing over r recovers all 2^(Af) independent
entries. No invariant quotient is substituted for arbitrary data.

Input coordinates obey x_p=alpha, x_nonpivot=R^T alpha+beta. The Fourier
character is alpha·gamma+beta·delta, with y_p=gamma+R delta and
y_nonpivot=delta. Output primal coordinates are gamma+R delta and
delta+R^T(gamma+R delta), exactly SF8. This proves normalized H_r then
H_(f-r), including r=0 and r=f. Both transforms act on the complete
fibre volume. The isotropic U=<11> example correctly rejects reading
delta alone as the output rowspace.

Translations in a coset block contribute only invertible sign diagonals.
Restricted rank r-d gives a Walsh factor tensored with J_(2^d), hence
nonzero normalized singular values 2^((r+d-f)/2), multiplicity 2^(r-d).
As a consistency check d<=f-r makes these values at most one. This is
rank over R or C, not binary rank. It does not lower-bound tape time.

## Physical implication and limits

FC requires actual bijections for every rank and ordered spectator frame
at V[m^K+D_m(1+J(f))] times the displayed root logarithms, with all head
travel, roles, metadata, erasure and a fixed payload coefficient charged.
A polynomial-m multiplier on J(f) does not meet its subpower threshold.
Computing an address formula alone proves no such supplier.

In the complete local template, pointwise masks and columnwise linear
maps use RO. Every completed Fourier child still needs two conversions
on its full work-row address range. The volume factor is exactly
2+2 sigma_m/W_m, giving V sqrt(m) R_m D_m J(f). With f<=a/A_m and a
completed monotone exact envelope, this is bounded by
V sqrt(a+1) R_m D_m E_I(a), plus paid ordinary work.

Fixed-power arity geometrically contracts log width. In the expanded
positive recurrence, monotonicity bounds all local E_I(a_i) by
E_I(a_root); pay it once in the largest local term. Only the psi terms
in recursive multipliers need summing along the path, and their geometric
sum plus the logarithm of path length is O(psi). Thus SF16 does not
need geometric summability of chi. Ordinary work, finite bases, setup,
occupied batching and outer logarithms remain included. Exact FC
permutations add no rounding error; existing coefficient/gain bounds
are retained, with the same common-cap requirements.

The source caller gives conditional SF17. Current chi dominates psi,
so there is no improvement to the admitted complete bound. A future
polynomial-log-log exact supplier would still leave the retained psi
numerical mass. This identifies a concrete representation-change gate;
it does not construct CT-I or CT-W.

## Corrections and evidence boundary

Before acceptance the author removed wording that incorrectly treated
the upper envelope J(f) as a lower cost bound, and revised the recurrence
to pull the monotone exact envelope out once. No other blocking issue
was found. Exact replay is in spectator-span-replay.json. No Lean proof
of SF/FC, full tape execution, human refereeing or priority claim is made.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance.
