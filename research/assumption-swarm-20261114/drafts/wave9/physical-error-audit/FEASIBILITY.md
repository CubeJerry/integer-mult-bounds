# C9 source-precision audit: proposed obstruction is superseded

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
Scope: the retained same-phase-cell rounded Gaussian reference and its
coefficient precision; no claim about a current whole caller, mixed or
rectangular blocks, or a multiplication exponent.

## Decision

Stop this research objective after the bounded source audit. The proposed
premise that full-cell weights are still rounded at `P=Theta(p)` is not the
construction in the pinned fine-prime composition. Its explicit replacement
is `P_setup=Cp+64p^2 ceil(log2 p)`. This is credited prior work, not a new
repair or negative result. No additional publication is proposed.

The exact source and local reads are recorded in `SOURCE-PINS.json`.
The live PR snapshots are `PR1786.json`, `PR1797.json`, and `PR1800.json`;
the bounded recent search is in `LIVE-OVERLAP.json`. The audit does not claim
an exhaustive search of every historical or unpublished package.

## Provenance and overlap

1. `GAUGEFREE-INTERIORS.md` section 2 retains the older sufficient estimate
   `4*2^-P exp(a/(4theta))`. Its original `theta^-1=O(p^epsilon)` setting
   allowed the full-cell accuracy term to be absorbed in `Cp` bits.
2. `FINE-PRIME-PADDING.md` section 3 explicitly states that the old absolute
   precision cannot be retained at fine primes. It raises full-cell weight
   setup precision to `Cp+64p^2 ceil(log2 p)`, proves positivity and relative
   error below `2^-Cp`, and retains `Cp`-scale kernel/online precision. The
   same section explicitly directs replacing the old `Cp` weight precision
   in PR1758's comparison by this setup precision.
3. `FINE-PADDING-COMPOSITION.md` credits PR1786 for precisely these prime,
   precision, locality and normalization statements. Its section 1 table
   and section 4 do not reinstate the old weight precision.
4. The source text is byte-identical to Chafik Boukhalfa's open
   [PR1786](https://github.com/CrocSwap/integer-mult-bounds/pull/1786), head
   `c52345caa318fc6b1b6e2659c57d746317a72823`, SHA256
   `47d1b1b4df28aadda3cd6bdeb1fbc47290595e9208cd09c1a1f338520d33fdce`.
5. Merged [PR1797](https://github.com/CrocSwap/integer-mult-bounds/pull/1797)
   independently audited the explicit setup inequality and the old-precision
   underflow control. Its head is
   `4e8f77031b1a936d6739b2cd84f378dcf1eb5635`, merge
   `cad44bb9eb8f71edf3a0421f169ef168eb1a1ccd`. Its README and verifier are
   retained here from canonical main. It did not certify the whole compiler
   or the microbox layout; its finite controls are not a universal source
   theorem.
6. Open [PR1800](https://github.com/CrocSwap/integer-mult-bounds/pull/1800),
   head `46d865ab92e58098538b8c5348b6a131c99abf45`, composes the same
   mechanism. A later canonical `gmx-t74-borrow43-handoff` gauge-free note
   still quotes the historical comparison but changes absolute-scale circuit
   guards, not the fine-prime precision substitution. No incompatible
   source precision replacement was found in these targeted reads.

## The actual local implication

The original rounded reference is specified in
`LOG-A-PHASE-SCHUR-AUDIT.md` section 2: one positive downward-rounded weight
per coordinate; a single downward-rounded, truncated symmetric Toeplitz
kernel with diagonal exactly one; and, within a phase cell,

`H_ij = w_hat_i G_hat_(i-j) / w_hat_j`.

For ideal weights `w_i`, write `w_hat_i=w_i(1-e_i)` with
`0<=e_i<=eta<1`. The fine-prime setup proves `eta<2^-Cp`. At an in-band
offset `|i-j|<=W`, the exact local identity from CAPPED-GAUGE-AUDIT gives

`|log(w_i/w_j)| <= a |i-j| <= aW`.

Consequently, if `|G_hat_h-G_h|<=epsilon`, then

`|H_ij-N_ij| <= [eta |N_ij| + epsilon exp(aW)]/(1-eta)`.

This follows by adding and subtracting `(w_hat_i/w_hat_j)G_h` and using
`|(1-e_i)/(1-e_j)-1|<=eta/(1-eta)`. For the physical narrow matrix on one
matching phase cell, `|N_ij|<=1`. Thus the full-cell absolute weight range
does not multiply the local kernel error; only `exp(aW)` does. With
`a=O(log p)` and the retained `W=O(sqrt(p) polylog p)`, `aW=o(p)`.
Tail truncation must be added separately, with its own retained exponential
rate; increasing the coefficient constant does not by itself improve a
fixed truncation width. On the retained source widths the tail is
exponentially small in `p`, which is the scale needed for the A8 local
stability condition. This is an explicit unpacking of PR1786 section 3,
not a novelty claim or a new implementation of its setup.

For completeness, its weight estimate has ample slack. With
`L=ceil(log2 p)`, eventually `a<=16L` and `theta>1/(4p^2)`, hence
`a/(4theta)<16p^2L`. Since `log(2)>1/2`,

`2^(-Cp-64p^2L) exp(a/(4theta)) < 2^-Cp exp(-16p^2L)`.

The harmless factor 4 in the older comparison is absorbed for all
sufficiently large `p`, or by a fixed increase of the constant. The source
therefore does not require a cancellation that rescues underflowed weights:
it avoids underflow by paying higher setup precision.

## Complete precision and setup boundary

Full-cell weight storage/setup has `Theta(p^2 log p)` bits, not `Theta(p)`.
Online records, local kernels and local shifted/chirp pages retain
`Theta(p)` bits subject to the stated group precision guards. The source
charges polynomial coefficient/page generation per complete microbox and
axis and invokes its existing superpolynomial payload amortization. This
audit does not re-prove that layout, paid data acquisition, or whole-caller
embedding; those inherited obligations remain explicit. The later
`beta+2xi-2<1` chirp guard is essential for simultaneous online circuits.

## What remains open and what is not being claimed

The A8 theorem's actual-caller identification and actual implementation
error remain source interfaces to bind. The old displayed weight estimate,
read without its fine-prime substitution, is not itself a surviving
analytic obstruction. A further possible source-specific route is to use
the exact cancellation of rounded weights in
`H_ij H_ji/(H_ii H_jj)=G_hat_h G_hat_-h`, but that would require a new
separate claim on colored adjacency of the rounded, truncated tensor and
is not investigated or asserted here.

No new kappa, unconditional result, source modification or accepted frontier
change is claimed. Prior credit: Chafik Boukhalfa and PR1786; JosieElliston
and PR1797; Vlado Vojdanovski and PR1673; PR1758's fractional-shift lineage.
This source audit was prepared for @CubeJerry with OpenAI assistance.
