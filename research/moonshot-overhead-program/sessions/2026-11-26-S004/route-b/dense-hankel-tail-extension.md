# Draft extension: a tall Hankel promise with a short tail

Status: **proved draft, not independently reviewed or admitted**. This is
a short closure of the preceding recurrence route. It does not replace
the protected amplitude investigation and supplies no new candidate.

Fix a length-D sequence E and `1<=s<=D/3`. Define the explicit tall
Hankel matrix

    H_s(E)=(E_(i+j))_(0<=i<D-s, 0<=j<=s).

This precise rectangular convention is part of the promise. No
equivalence with a differently shaped central Hankel rank is assumed.

If `rank H_s(E)<=s` over Q, choose a nonzero kernel vector
`(q_0,...,q_s)` and let r be its highest nonzero index. Then

    sum_(j=0)^r q_j E_(i+j)=0     for 0<=i<D-s.

If r=0, the first D-s terms are zero. If r>0, divide by q_r and solve
for E_(i+r). This is a normalized forward recurrence of order r on the
prefix of length D-s+r. In particular, the first D-s terms have forward
recurrence order at most s. This proves the prefix recurrence assertion;
there is no assumption about a nonsingular leading Hankel minor.

Since D-s>=2s, the first 2s terms determine that prefix by Theorem H1's
uniqueness argument. Reconstruct and emit only this prefix. Compute the
last s coefficients of AB by one short product of reversed input
prefixes, and subtract the corresponding candidate suffix. When A and B
have padded degree bounds below h and D=2h, coefficient D-1 is zero;
the reversal of AB has formal degree D-2. This boundary is handled
explicitly rather than shifted by one.

Reversing coefficient order on fixed tapes costs O(V): reverse the
whole bit string, then reverse the bits within each fixed-width record
using the reusable record buffer. The additional product uses O(s tau)
bits. Therefore the repair time and uniform visited-space bound of H1
remain unchanged. When D<3s, its parameter K is already larger than V
up to fixed constants, and the direct packed fallback fits K^6.

For a field-linear image all of whose vectors obey this tall-Hankel
rank promise, projection to the first s and last s coordinates is
injective. A kernel vector has a zero initial s-prefix and its own
forward recurrence on the first D-s coordinates, so that entire prefix
vanishes; its final s coordinates vanish as well. Thus the image
dimension is at most 2s. The W-row form is rank at most 2Ws. The same
argument survives coordinatewise zero-faithful integer encoding when
the Hankel promise holds over Q for the encoded sequence.

Unlike a prefix-only recurrence algorithm, this extension recovers the
last-coordinate impulse whose finite Hankel rank is one. It still needs
the explicit rank promise; neither a short prefix nor its combination
with a short suffix certifies an arbitrary dense residual.

Prepared for @CubeJerry with substantial ChatGPT assistance.
