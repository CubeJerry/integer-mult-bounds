# Quantitative error of a count-only predictor in odd characteristic

Status: **proved restricted obstruction**, not a lower bound on general
predictors, the source's integral multivariate predictor, or multiplication.
Source: OpenAI `math` at `3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/repair.tex` (`lem:count-predict`, `cor:swap-repair`) and tape
`build/interchange.tex` (`subsec:swap-spectrum`).

## Theorem

Let `p` be odd and `C~Binomial(m,1/2)`. Any predictor whose only count
information is `C mod p` has error probability at least

\[
 \frac{1-(p-1)\cos(\pi/(2p))^m}{2}
\]

when predicting `(-1)^C`. Values other than `+1,-1` cannot improve success.
If `m >= (8p^2/pi^2) log(2(p-1))`, the error is at least `1/4`, and hence
cannot meet the source's `1/(2m^3)` error budget for `m>=2`.

### Proof

Write

\[
 S_a=2^{-m}\sum_{c\equiv a\pmod p}(-1)^c{m\choose c}.
\]

Choosing the more likely parity separately in each residue class gives
optimal success `(1+sum_a |S_a|)/2`. For a complex primitive `p`th root
`omega`, root-of-unity filtering yields

\[
 S_a=\frac1p\sum_{r=0}^{p-1}\omega^{-ar}
       \left(\frac{1-\omega^r}{2}\right)^m.
\]

The `r=0` term vanishes, and oddness of `p` gives
`|1-omega^r|/2 <= cos(pi/(2p))`. Summing the triangle inequality over
`a` proves the stated error bound. Finally `cos t<=exp(-t^2/2)` on
`[0,pi/2)` because the derivative of `log cos t+t^2/2` is
`t-tan t<=0`. This proves the threshold.

## Exact window collision and scope

The characteristic-`p` count operator
`C_beta=(mI-sum_j(-1)^beta_j Q_j)/2` has eigenvalue `c mod p`.
On an integer interval `[u,v]` of width at least `p` inside `[0,m]`,
the counts `u,u+p` have identical field image and opposite parity.
No function of the field count alone can predict both. The source's
integral multivariate predictor keeps individual query information and is
not generally a polynomial in this field-valued count alone.

At each fixed frequency the source uses all `2^m` translated shifts
equally often, so their count distribution is exactly binomial. The
theorem therefore applies at every frequency to a count-only replacement
of that source predictor. A smaller bounded-independence multiset does
not automatically have this residue law; it needs a separate argument.

The root agent separately establishes a Gram-rank/reserve obstruction
connecting the source's admissible `m,p` to the exact collision. This note
adds a quantitative error floor once `m` exceeds `O(p^2 log p)`.

### Open next questions

Find a full-rate representation of higher count digits or individual-query
information that avoids the original large Clifford representation, or
replace the finite-characteristic interchange architecture.

Credits: @CubeJerry, the cited OpenAI manuscripts, and S002's compact
characteristic-zero predictor. Derivation used GPT-6 Astra Pro assistance.
