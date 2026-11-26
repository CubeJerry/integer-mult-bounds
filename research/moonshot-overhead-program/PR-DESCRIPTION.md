# Quantitative overhead for exact integer multiplication on fixed tapes

## Result

One deterministic finite-alphabet multitape machine multiplies two arbitrary \(n\)-bit strings and writes exactly \(2n\) bits. Set \(L=1+\log_2 n,\ x=\log_2 L,\ \Phi(x)=(x^2\log_2(x+2))^{1/3}\). Its written time bound is \(n\sqrt L\,2^{63\Phi(x)}\) for every \(n\ge2\); \(n=1\) takes at most 4096 transitions. At most \(2^{32}n\) physical tape cells are visited through halt. [All-length proof](sessions/2026-11-26-S008/all-lengths.md) · [Space proof](sessions/2026-11-26-S008/routing-outer-space.md)

Whenever \(\log_2\log_2 n\ge7{,}519{,}517{,}465{,}920{,}988\), the worst case is at most \(n(\ln n)^{501/1000}\), with coefficient one. This is a sufficient length. The construction quantifies the fork's earlier cube-root rate for the excess. The square-root endpoint and a faster functional order remain open. [Threshold proof](sessions/2026-11-26-S008/routing-label-walsh.md) · [Independent certificate](sessions/2026-11-26-S008/recount-label-cutoff.lean)

For \(t=\log_2\log_2 n\), the proven coefficient in front of \(\Phi(t)\) falls to 60 throughout \(t\ge1{,}572{,}864{,}480\), and to 53 throughout \(t\ge2^{69110}\). The latter proof uses the actual number of bits per label. Both estimates include an extra factor of two on the time side and use the same fixed machine. [Coefficient 60](sessions/2026-11-26-S008/profile-limit.md) · [Effective coefficient 53](sessions/2026-11-26-S008/coefficient-53.md) · [Fixed-exponent cutoffs](sessions/2026-11-26-S008/all-exponents.md)

## Construction for review

* The native ternary interchange includes ordinary steps, all grouped children, returns, binary adaptation and the finite compiler. The full proof fixes \(R=240\). [Numerical interchange](sessions/2026-11-26-S008/node-root-parameter.md)
* The Walsh calculation charges the common denominator, each true slot width, actual child volumes, bounded precision and reusable banks. [Walsh proof](sessions/2026-11-26-S008/walsh-node.md)
* The two forward transforms and adjoint include phase generation, guarded permutations, CRT, exact recovery and fresh output. Earlier lengths use a direct dyadic transform or the raw grade-school machine. [Outer caller](sessions/2026-11-26-S008/outer-layers.md) · [Dyadic caller](sessions/2026-11-26-S008/address-dyadic-caller.md)

* The cross-anchor partition reduces endpoint occurrences within a stated routing model. The remaining local and Walsh costs keep the previous asymptotic rate. Fixed-precision ordered factor transforms remain a separate result in this contribution. [Routing assessment](sessions/2026-11-26-S008/address-review-cross.md) · [Earlier fixed-precision transform](sessions/2026-11-26-S007/fixed-witt-precision.md)

## Verification

Independent AI reviews reconstructed the numerical joins and port conventions. Component Lean proofs cover selected tape rules, interpolation, real-variable bounds and numerical cutoffs. A small-box full-grid replay recovered all 210 coefficients and a 2,000-bit product. The written whole-machine time theorem awaits independent human review and end-to-end formalization. [Verification record](sessions/2026-11-26-S008/VERIFICATION.md)

## Credits

Jerry Chen (@CubeJerry) directed the programme with substantial ChatGPT research and multi-agent assistance. OpenAI's source authors supplied the 2026 tape and Fourier constructions. S002/E001, E002, S003/E003 and S004–S007 supplied the preceding credited proofs, conditional transfers and negative results. The cited authors retain credit for combinatorial sieves, fast multiplication, Toom–Cook interpolation, Frobenius partitions, Fourier transforms and normal-basis theory. Cantor and Kaltofen supplied the cyclotomic decomposition, Yann Tal the fixed-tape sorting theorem, Harvey and van der Hoeven the short products, and Swapnil Jain the verified finite residue word.
