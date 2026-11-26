# Independent review of the certified FFT lower candidate

Status: **passes algebra, deterministic precision, fixed-tape time and
all-visited-space review**. The supplier plus the admitted amplitude
corrector is a complete exact construction with a slower invoice than
the current programme bound. No target-time improvement is admitted.

Reviewed complete author note: `route-b-work/certified-fft-lower-candidate.md`.
SHA256 `2c30552367ba4231f664ee826846c0b80a4fb58d9c77c4fa12c4201d69871498`.
Checker SHA256 `1db49c32879eea8aec97c9755f183dc53dd9c667ddc2831f70d624b347885c7c`.

## 1. Fixed precision and effective twiddles

The range 1<=a<=2b+ell implies q>=2ell+2c+20 and w=Theta(b+ell).
The same q and w apply at every stage. Since ell>=2, all square-root
arguments lie in [1/2,1], every stored next cosine is at least 1/2,
and restoring square root and ordinary division use O(q^2) time and
O(q) visited cells. The integer radicand in FFT5 produces precisely
floor(2^q sqrt((1+C2^(-q))/2)); no transcendental root oracle is hidden.
The sine quotient has the correct fixed-point scaling.

The cosine map has Lipschitz constant below 1/2 on the stated range.
Clamping to [0,1] cannot increase error. Therefore e_c<=2delta and
e_s<=5ell delta follow by induction, and epsilon=7ell delta safely
bounds primitive-root modulus error. Successive rounded powers satisfy
e_(j+1)<=(1+epsilon)e_j+epsilon+2delta. Because N epsilon<1/2,
their error is at most 16N ell delta, below the chosen eta=32N ell delta.
Conjugation preserves this bound.

The crucial smallness guard is explicit:

    eta ell =32N ell^2 delta <=2^(-ell-15)<=2^(-17).

It uses ell^2<=2^(2c) and the fixed lower bound on q. Thus the numerical
recurrence never relies on a precision that increases with stage count.

## 2. Forward, product and inverse errors

For the forward recurrence, division by 2^j bounds normalized error by
a product of factors 1+eta/2 times the sum of eta U/2 per stage and
the geometric rounding tail. The bound 4eta ell N U is conservative;
it also gives e_ell<=NU/4. The displayed pointwise-product error bound
14eta ell N^2U^2 follows from 2NU e+e^2+2delta. In particular the
quadratic error is at most eta ell N^2U^2 under eta ell<=1/16.

For the inverse transform, use exact input magnitude X=N^2U^2 and
initial error E0=14eta ell X. After normalization by 2^j, the same
recurrence gives at most 2E0+2ell eta X at the final stage, hence
30eta ell X. Rounding after division by N is covered by the stated
64eta ell X. Substitution of the actual q gives

    64eta ell N^2U^2
       =2048delta ell^2 N^3U^2
       <=2^(a-9)=M/512.

This checks FFT9 with its full N^3 rather than a missing N factor.
The exact inverse intermediate magnitude is at most N^3U^2, and its
approximation remains below twice that. The fixed w capacity contains
q fractional bits plus 2b+3ell+10 integer/sign/guard bits. Temporary
complex products use only a constant multiple of w before truncation.
There is no overflow or growing-word assumption.

## 3. Positive residual and corrector composition

Since each true coefficient c_i is integral and |z_i-c_i|<M/8,
C_i=floor(z_i-M/8) is no larger than c_i, and
0<=c_i-C_i<M/4+1<=M. The final padded zero coefficient is included.
Downward rounding of negative numbers matters: truncation toward zero
would not implement the proof. M/8 is exactly representable on the
chosen grid even when a=1 or 2.

Negative candidate coefficients are permitted by the corrector. The
candidate has O(b+ell) coefficient bits, so its own height bound and the
corrector's tau are O(b+ell). Under the amplitude interpretation one may
take B=M-1, with the corrector choosing its own strict centered modulus
(at most a+1 bits before the routine's height cap). Under the one-sided
interpretation the least-residue mass test accepts; its separate scalar
product and a<=tau budget guard remain part of that imported routine.
Neither composition silently assumes a signed modular residue verifies
an unrestricted candidate. Both occupy O(h(b+ell)) visited cells.

## 4. Physical arrays and twiddle delivery

At each radix-two stage, two monotone partner streams read the two halves
of each butterfly group, and two result streams are merged in record
order. A fixed number of complete arrays and tapes suffices. Whole-record
binary digit reversal costs ell stable partition passes. Counters have
O(ell)<=O(w) bits and their updates fit the per-record scan bill.

The twiddle supplier is sequential: scan the root table once to select
the stage stride pattern, then repeat that pattern for its groups. The
selection costs O(Nw). Repeating and rewinding a pattern of 2^(j-1)
records for N/2^j groups also costs O(Nw), including real tape travel.
There is no random-access lookup into the root table.

Short products may use a fixed set of arithmetic buffer tapes separate
from the monotone array streams. Array heads remain at their current
records while those O(w) buffers are processed, and the buffers are
reused after each call. Thus arithmetic calls do not incur repeated
traversal of a growing array prefix. The stipulated short multiplier's
O(w) visited cap applies to each reused buffer region.

Root construction uses O(w) space. All N-word arrays, twiddle streams,
patterns, counter regions and reusable buffers fit fixed marked ranges
of total O(Nw). Stages reuse those ranges; the union of all cells ever
visited is consequently O(Nw)=O(V), not merely stagewise live storage.
The stated full invoice

    O_alpha(h ell w(1+log(w+1))^alpha + ell w^2)

therefore includes root setup, twiddle generation, all butterfly movement,
short arithmetic and bit reversal. The extra repair invoice and optional
mass product are separately charged. For bounded h and large b, the root
and scalar terms have not been incorrectly absorbed into linear scans.

## 5. Independent exact replay and limits

An isolated copy of the author checker was executed in
`route-a-work/replay-certified-fft/`. The receipt reports 217 complete
candidate-plus-correction cases, 2,542 certified residual coefficients,
309 exact half-angle operations, 3,952 power-norm enclosures, 37,148
complex-rounding controls and 2,229 fixed-precision FFT stages. It also
checks all 16 binary two-digit input pairs and the negative-floor and
unpromised-alias controls. No floating-point or transcendental library
is used by that checker.

These finite calculations support the algebra and margins. They do not
execute the fixed-tape schedule; the latter is reviewed above. The
materialized-word schedule explicitly writes h ell words of width w,
so its packed-regime O(n log n (log log n)^alpha) invoice does not reach
the requested target. This is correctly scoped to this supplier and
does not assert a lower bound for all numerical multiplication methods.

No remaining blocker was found at the reviewed snapshot.

Prepared for @CubeJerry with substantial ChatGPT assistance.
