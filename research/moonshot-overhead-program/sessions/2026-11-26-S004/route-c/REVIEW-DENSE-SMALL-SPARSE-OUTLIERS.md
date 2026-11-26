# Independent audit of dense-small plus sparse-outlier correction

**Verdict: pass for Hyb1–Hyb5 in their signed-promise and one-sided
certification scopes.** This combines already reviewed engines and
supplies no approximate candidate.

For signed errors, centered residues equal E_i whenever |E_i|<M/2.
The residual E-r is supported only at the promised outliers, including
the correctly handled half-open endpoint. Its height and the height
of C+r grow by only O(1) bits because a<=tau. The signed sparse
corrector therefore applies to C+r under the mixed promise. Its own
verification does not certify arbitrary signed residuals outside that
class, as the note explicitly states.

For one-sided errors, least nonnegative residues yield
F_i=M floor(E_i/M)>=0. The new candidate remains coefficientwise below
the exact product. The dense-safe three-moment certificate keeps sound
acceptance when the supplied outlier budget is false; its mass test
checks that no positive residual remains. The zero-outlier branch is
the separately charged amplitude mass test. A fallback after an
incomplete budget is additional unless the large-k branch pays for it.

Both beta and beta_+ are Theta(tau): tau dominates log D, S<=D, and
M<=2^tau changes heights by only a constant number of bits. The sparse
stream volume is therefore Theta(V). Retaining C' while reusing the
modular regions requires a fixed number of O(V) streams. The k>V
branch preserves the uniform-space schoolbook fallback. The time is
the sum of the actual component invoices, with the scalar mass product
displayed separately. The stated regimes follow from
log k=O(log tau+log S+log log D) and the declared k^6=n^o(1) range.

An isolated replay in `replay-hybrid-residual/` passes 24 full signed
mixed repairs with height/carry checks, 24 one-sided attempts (18
accepted, six incomplete), 12 false outlier guesses and the centered
endpoint. It also rejects a dense positive false budget, tests two
zero-outlier mass outcomes, and retains the signed missing-promise
false-certificate control. The receipt hashes all three component
checkers. These are exact two-stage arithmetic and certificate checks,
not an executed tape-time claim.
