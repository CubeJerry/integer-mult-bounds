# Independent audit of the parity-weighted Fourier gate

**Verdict: pass for PW1–PW4 and the stated conditional Fourier transfer.**
OWL remains an open support-and-load hypothesis. This note supplies no
new unconditional multiplier and does not improve interchange by itself.

## Reduction and coefficient audit

The identity I-P=-O entrywise-multiplied-by P is exact: P is one on the
diagonal and vanishes at every positive even Hamming distance. Expanding
P in equality cylinders and intersecting both sides of each allowed
odd-distance rectangle gives the required weighted decomposition. A fixed
vertex has one common word for any chosen coordinate set, so the local
incidence multiplier is at most sum_j binom(L,j), with no q^j factor.
The intersections retain odd-distance cross support. The pinned source's
cross-orthogonal endpoint proof consequently applies to correlated sides;
it does not require a coordinate product or an anchor.

Allowing negative or overlapping weights does not change that support
argument, and an ordinary cover cannot substitute for the exact weighted
identity. The charged polynomial part stays unchanged. Under OWL, the
same parameter selection as the already reviewed JR Fourier transfer
therefore gives the stated square-root-logarithmic local loss.

The coefficient-height argument is valid. Choose independent incidence
columns spanning the zero-one target, then independent rows. The selected
square system and its Cramer replacements have zero-one entries, so
Hadamard bounds all numerator and denominator heights by O(R log R).
Using this solution only deletes columns from the supplied support list;
neither side load can grow. Real solvability equals rational solvability
for this rational linear system. The bound R<=N lambda follows by
counting nonempty source incidences. The Fourier parameter choice makes
N and the resulting support/height volume polynomial in m.

Odd denominator factors are allowed by the numerical rational-scaling
supplier. The draft correctly avoids claiming a Z[1/2] circuit or a
characteristic-two specialization of these weights. Coefficient norms
are priced through their bit heights. Enumerating polynomial-size
support lists and solving exact rational systems takes bounded
2^{m^C} time and polynomial-m workspace; under OWL it finds a witness,
and without OWL the bounded search still halts with failure. The search
belongs to preflight and is not repeated per data record.

## Rank obstruction and exact replay

For q>2 the two eigenvalues of 2I-J are both nonzero. On every tensor
space containing a zero-sum factor, O has the negative half of that
nonzero tensor eigenvalue. On the all-constant line the eigenvalue
[q^L-(2-q)^L]/2 is nonzero. Thus O has full rational rank N. For q=2
the constant and full-contrast lines supply exactly rank two. When some
heterogeneous alphabet equals two, the tensor term has rank equal to the
product of the other alphabet sizes and annihilates the all-constant
line, which the separate J term contributes. The heterogeneous formula
is therefore correct as well.

This rank bound excludes exact weighted representations with fewer than
N terms when q>2; it does not exclude the N lambda terms allowed by OWL.
It must not be conflated with the small binary Gram rank used for free
cross-orthogonality.

An isolated replay of `verify_parity_weighted_fourier.py`, with its two
Fourier helpers copied into `replay-parity-weighted-fourier/`, passed all
8,720 weighted identity entries, 3,176 omitted-polynomial negative
controls, and eight exact rank cases, including 256 labels. The test
families include overlaps, negative weights, odd denominators, and
binary rectangles containing multiple odd distances. These are controls
for the proved transfer, not evidence that the open OWL load bound holds.

The transfer imports the already reviewed numerical rational suppliers
and endpoint geometry. Its proper conclusion is an alternative sufficient
Fourier gate, weaker than requiring all JR partitions. Improving only
this branch leaves the current interchange loss in the complete envelope.
