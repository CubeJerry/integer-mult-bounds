# Independent audit of the certified FFT lower candidate

**Verdict: pass for the all-input positive-residual supplier and the
explicit slower complete supplier-plus-modular-repair construction.**
The proof escapes the restricted monotone and missing-coordinate models,
but its full-word stage invoice is above the research target.

## Effective roots and numerical constants

The half-angle square-root derivative is at most one half on the stated
interval, so e_c'<=e_c/2+delta. Both exact and stored new cosines are
at least one half; comparing the sine quotients gives
e_s'<=e_s+2e_c'+delta. The integer square-root numerator FFT5 and the
sine quotient implement the intended downward grid rounding exactly.
Clamping cannot enlarge these component errors.

The primitive-root bound epsilon=7ell delta follows. Successive complex
products satisfy the stated power-error recurrence; N epsilon<1/2
makes its geometric factor below two. The 16Nell delta power bound
and retained eta=32Nell delta therefore hold. From the minimum q,
eta ell<=2^-17 and delta<=eta. No transcendental oracle or growing
precision is used.

The forward butterfly error recurrence correctly includes both input
errors, twiddle error times the true stage magnitude and one complex
rounding error. Dividing by the stage scale and summing gives FFT7
with ample margin. The pointwise product error includes the cross term,
quadratic error and rounding, proving FFT8. Applying the same normalized
recurrence to the inverse gives at most 30eta ell N^2 U^2 before the
last harmless grid rounding; the retained factor 64 is safe.

Substitution of q into 2048delta ell^2 N^3 U^2 gives at most M/512,
using ell^2<=2^(2c) and U<2^b. The integer-part guard in w covers
twice the N^3 U^2 inverse magnitude. Temporary complex products need
only a constant multiple of w bits, with their actual integer arithmetic
charged.

## One-sided rounding and exact repair

With C_i=floor(z_i-M/8), the proved real-part error gives C_i<=c_i
and 0<=c_i-C_i<M/4+1<=M. The half-open residual range is strict,
including M=2 and true zero coefficients; negative candidate coefficients
are allowed by the corrector. Coefficient heights stay O(b+ell).

The clean complete composition uses least nonnegative residues modulo
M: FFT1 already proves 0<=E_i<M, so those residues recover E directly.
The optional positive mass test is also sound and has its separately
charged scalar product. If using the centered amplitude theorem instead,
its own modulus must exceed twice the chosen residual bound; B=M-1
and modulus at most 2M suffice. One must not silently use centered
lifting modulo M at M=2, where the constructed residual can equal one.
The actual integration checker uses the valid nonnegative-residue path.

## Physical invoice and limiting conclusion

Each full butterfly stage has monotone partner streams and reusable
outputs. Digit reversal uses a fixed number of streams and ell stable
whole-record passes. A stage's twiddle pattern is selected by one root
table scan and repeated sequentially, costing O(Nw), rather than random
lookup. Counters fit the word bound. The fixed short multiplier's work
can remain on its own fixed scratch tapes, so word products do not
require crossing a parked full array per call.

All arrays and stage regions occupy O(Nw)=O(h(b+ell)) cells, reused
across stages. Root construction adds O(w) workspace and O(ell w^2)
time. Complex operations give O(h ell w(1+log(w+1))^alpha), with
separate mass-product charges retained when needed. The fixed tape
count and union-of-visited-cells conclusion follow from these explicit
stream regions.

In the declared packed regime, the supplier materializes Theta(n) bits
at every one of Theta(log n) stages, so this schedule already spends
Omega(n log n) on writes. Its complete upper invoice is the stated
O_alpha(n log n (log log n)^alpha). The result is a genuine paid
nonlinear/rounded supplier bridge, but no competitive upper bound or
lower bound for other numerical architectures follows.

## Isolated arithmetic and end-to-end replay

The copy in `replay-certified-fft/` passes 217 complete supplier cases,
2,542 positive residual coefficients, 2,229 fixed-precision stages,
3,952 root-power enclosures, 37,148 rounding controls and 309 half-angle
steps. Word capacities and floor/alias negative controls also pass.
The second checker combines the actual dyadic supplier with the actual
triadic modular engine in 18 cases, recovering 336 coefficients and
checking both the exact mass and base-2^b carried product. This is
exact finite arithmetic; tape pricing is established by the audited
stream schedule rather than measured by these tests.
