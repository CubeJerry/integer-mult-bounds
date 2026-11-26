# Independent review of the regular star-pencil lift

Disposition: **accepted in the explicitly stated scalar compression model**.
A read B's `star-pencil-regular-lift.md` and complete checker. The exact
common conjugation agrees with the independently derived SN-A10--A11
here. The occupancy/rank result is B's additional component and does not
prove that the joint star sum itself needs m separate physical queries.

The cyclic leaf permutation fixes the central coordinate and conjugates
the first star transposition to each of the m stars. Hence the diagonal
regular lift really has blocks S_1,...,S_m, and scalar embedding followed
by summation gives the weighted star sum on one arbitrary input. Its m
fibres are correlated copies of that input; they cannot be counted as
m independent useful inputs merely because the lifted operator accepts
arbitrary data on its whole domain.

I checked the operator-independence witness over an arbitrary coefficient
field. Applying the m stars to an address whose central symbol is nonzero
and whose leaf symbols are zero gives m different basis vectors. Thus
comparison of the coefficient matrix of each S_j in SL5 is legitimate
for the actual physical permutations, without an indeterminate-query
substitution or an assumption about faithful group representations.

Each compressed call contributes an outer product to that coefficient
matrix, of rank at most one. The sum of h calls must give b_j I_R, of rank
R, so h>=R. The matching R-call construction is explicit and verifies
sharpness within SL5. It follows that the full queried fibre volume is
at least hm/R>=m per independent input volume. Serial copies avoid an
m-dependent payload coefficient but do not change this volume invoice.

The same proof directly covers the actual seed-dependent numerical
coefficients: replace b_j I_R by any fixed diagonal C_j with nonzero
entries on the independent seed rows. It has rank R. More generally the
bound is h>=max_j rank(C_j) for an asserted output sum_j C_j tensor S_j.
B added this extension after review feedback, so the intended application
does not require identical coefficients on different seed rows.

The physical pair need not occupy one contiguous field. In the original
separated-half layout an ordinary whole-pair star uses two width-f swaps,
as the revised note now states. This changes only a constant in the
optimistic primitive-volume invoice. No free physical packing of those
fields is needed for the algebraic rejection. Actual controlled leaf
rotations have only been granted zero cost to strengthen this scoped
obstruction; the note does not provide their tape implementation.

The recurrence conclusion concerns the declared positive invoice. Under
the stated regular split, multiplying B(e)>=m B(f) along a logarithmically
geometric adaptive path gives the near-linear invoice after the explicit
constant-per-level loss. It is not a runtime lower bound obtained by
pricing an upper-bound oracle as a mandatory operation. Products of
lifted calls, new physical maps, direct orbit transforms and nonlinear
intermediate operations remain outside SL5.

## Isolated replay

Copied and ran the revised checker in `star-pencil-review-replay/`. It
passed 9,360 signed conjugations, 5,439 cyclic regular conjugations, ten
actual independence witnesses, 2,426 partial-lift outputs, 16,982
matching full-rate outputs, 16,982 additional varying-seed-sign outputs
and 60 volume invoices. It rejected all 256 tested one-call scalar
encodings/decodings for m=R=2 over F_2. The latter is an exhaustive finite
illustration of the rank proof, not its general proof.

Revised source SHA-256:
`9155a95b0a9b585c4ab208e049cecafc99905e24ac5ab7569bceee9df12927a7`.
An isolated receipt and result JSON are retained with the copied script.
The two requested caller-scope clarifications are incorporated. No
remaining correction requested.
