# Attribution and license

New contribution: copyright 2026 Jerry Chen / @CubeJerry. Apache-2.0,
under the repository LICENSE. Substantial OpenAI ChatGPT (GPT-6 Astra Pro)
assistance was used for derivation, implementation, execution, self-review
and writing. No independent human review or proof-assistant certification
is claimed.

## Predecessor notice retained

Copyright 2026 DominikScholz. Apache-2.0. The original PR598 package was
prepared for DominikScholz with OpenAI GPT-6 Astra assistance in T3 Code.
Credit that work for the Leech geometry and line order, norm-six source
recipe and support bound, integer-valued cubic factorization, and optimistic
cost model. `reproduce_directions.py` adapts its direction-generation recipe;
`model.py` independently implements its coordinate data and ordering;
`budget.py` specializes its explicitly conditional cost screen. These
predecessor constructions are not attributed to this contribution.

The new work is the explicit mod-five separating certificate for the frozen
2,600-direction prefix, the one-row escape, the direct cubic-injectivity
argument, independent exact Boolean rank implementation, and scoped replay.
The two arithmetic implementations belong to the same AI-assisted author.

The predecessor's mathematical attribution is retained:
R. J. Turyn for Hamming/Golay gluing; J. H. Conway and N. J. A. Sloane for
Leech constructions and coset decoding; E. Bannai and N. J. A. Sloane for
the minimal-shell description; Gabriele Nebe for polarization and generalized
Turyn construction; Vincent Corlay, Joseph J. Boutros, Philippe Ciblat and
Loic Brunel for the explicit three-block formulation; SageMath contributors
for the published Golay generator matrix. No Sage implementation is copied.

Primary source pointers retained from PR598:
- Bannai and Sloane, *Uniqueness of Certain Spherical Codes*, Canadian Journal
  of Mathematics 33 (1981), 437-449, p.443 equation (12):
  https://neilsloane.com/doc/Me71.pdf
- SageMath Golay generator example:
  https://doc.sagemath.org/html/en/reference/coding/sage/coding/golay_code.html

Credit Cinna Davis / @1337isnot1337's PR2222 for the distinct 48-dimensional
norm-six lattice construction inspected for overlap, not a proof dependency.

The inherited supplier framework is maintained by Douglas Colkitt / CrocSwap,
conditional on OpenAI #109. Predecessor notices credit Avi Eisenberg, Henry
Grant, Jacob Sussman, Evan McKinney, Rohan Arun, Chafik Boukhalfa,
DreamingOfClouds, Dugongue, eumemic, icekylinx and earlier community authors.
No supplier implementation or selected proof is replaced by this package.
