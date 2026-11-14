# External mathematical connections

- Birmpilis, Labahn and Storjohann, *A fast algorithm for computing the Smith
  normal form with multipliers for a nonsingular integer matrix*,
  https://arxiv.org/abs/2111.09949v2. The paper constructs unimodular Smith
  multipliers and studies fractional inverse data. Rational invertibility
  versus an integral/localized module is the useful distinction here. Our
  explicit dyadic block decomposition avoids large generic Smith multipliers.
- Harvey and van der Hoeven, *Faster integer multiplication using short lattice
  vectors*, https://www.texmacs.org/joris/latticemul/latticemul.pdf,
  DOI10.2140/obs.2019.2.293. Minkowski-based representations remove specific
  prime-distribution hypotheses from an older n log n·4^(log* n) algorithm.
  This motivates representation changes but supplies no physical decoder
  or stronger complete bound for our programme.
- Li, Liu, Ma, Wan and Xing, *Encoding of algebraic geometry codes with
  quasi-linear complexity O(N log N)*, https://arxiv.org/abs/2407.04618.
  Constant-degree Galois-cover towers provide recursive encoding. Neither
  this rate nor low bilinear rank alone establishes the desired bit bound.
- Bürgisser and Lotz, *Lower Bounds on the Bounded Coefficient Complexity of
  Bilinear Maps*, https://www3.math.tu-berlin.de/algebra/work/bc.pdf.
  Their n log n lower bound concerns bounded-coefficient complex arithmetic
  circuits. It warns against replacing full encoding cost with bilinear rank;
  it is not an integer bit-complexity lower bound against this programme.

The new result is the actual source-specific preconditioner. Generic Smith
normal form, exact scalar transducers and the external algorithms retain
prior attribution and are not presented as newly proved mathematics.
