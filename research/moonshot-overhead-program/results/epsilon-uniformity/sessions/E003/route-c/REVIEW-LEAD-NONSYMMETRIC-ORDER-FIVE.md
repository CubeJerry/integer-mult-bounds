# Independent review of the nonsymmetric order-five extension

Status: **accepted within the stated converter-word model**. This review
checks `../lead/order-five-nonsymmetric-extension.md`, SHA-256
`7e9656f5b901f5d7b4fd2da91e9792176c969c8e0d9611f2c90ac7c0cbd71a00`.
It does not assert a classification of other words, larger gates or global
running times.

The proof correctly handles the zero-pattern boundary before using the
cross ratio. A triangular invertible gate and diagonal factors remain
triangular, so they cannot produce the swap. Triangular gates can satisfy
the converter condition alone and are not incorrectly excluded from that
condition. Once `bc != 0`, both normalized eigenvectors are dense; diagonal
equivalence to their eigenbasis therefore requires `a,d != 0`.

Writing `z=bc`, the cross-ratio equation gives
`(1+z)(lambda+a)=z(mu+a)`, hence `a=lambda+tau*z`.
Substitution in the determinant condition yields
`z*(1+tau^2+tau^2*z)=0`. Thus the nontriangular converter forces
`z=(tau^2+1)/tau^2`, `a=mu^2/tau`, and `d=lambda^2/tau`.
The converse follows from the same nonzero-entry cross-ratio criterion.
In particular the proposed symmetrization uses the explicitly available
element `(tau+1)/tau`; it needs neither a perfect field nor an additional
square-root hypothesis.

I independently expanded the determinant of the two diagonal equations
for `C D C^2`. Since `ad=1+z`, it is
`(1+z)*(tau^2*z+1)+tau^2*z^2 = 1+z*(tau^2+1)`.
The off-diagonal entries of this two-by-two equation matrix are nonzero,
so singularity supplies a kernel vector with both entries nonzero. The
resulting word is invertible and has zero diagonal, and the final left
diagonal scales its two nonzero entries to the swap. Combining the
determinant condition with the converter condition gives
`(tau^2+tau+1)^2=0`, and then the fifth cyclotomic equation for `lambda`.
Both directions and the claimed diagonal-conjugation equivalence follow.

The unchanged finite verifier was copied into
`review-o5-nonsymmetric-replay/` and replayed there. It passed all 4,280
ordered split gates across F4, F8 and F16, including triangular gates;
found respectively 0, 42 and 180 nontriangular converters; and found
exactly 60 joint gates, all in F16, of which 56 are nonsymmetric. Its
144,744 diagonal-word trials and four negative controls passed. These
finite checks corroborate the universal algebraic proof rather than
substitute for it.

This extension closes the symmetry assumption for the exact pair
`S=A C B`, `Q=E C D C^2`, with distinct reciprocal split eigenvalues and
determinant one in characteristic two. It does not restrict other powers,
other word shapes, non-diagonal conversions or the full multiplication
machine, and it supplies no additional asymptotic improvement.

Review: E003 route C, 2026-11-25; substantial AI assistance.
