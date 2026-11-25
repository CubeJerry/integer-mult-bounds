# Independent review of the literal-label certificate barrier

Gate: **PASS for the precisely restricted certificate model** in Route A
`LITERAL-LABEL-PROFILE-BARRIER.md`. This is not a runtime lower bound.

The binomial product is correct:
`binom(2d-1,d)=product_(i=1)^(d-1)(d+i)/i`, and each factor is at
least two. Therefore the incidence majorant has logarithm at least
`d^2-1+d(t-1)+d(d-1)log_2 t`. The rank guard gives
`t>=x/d^2+2-2/d^2`, whence `d(t-1)>=x/d`. Combining with
`log_2 lambda<=x/(2J)` gives `d>=2J`.

The other nonnegative terms yield `d^2<=2x/(3J)` and hence
`t>=3J/2`. Since `d(d-1)>=d^2/2>=2J^2`, the last term gives
`x>=4J^3 log_2(3J/2)`. No minimal-t or power-of-two-d assumption
is used, so the original construction's additional restrictions cannot
evade this necessary inequality.

The overhead corollary is valid under the additional **lower charge**
`F_J(X)>=c log_2 m_J+X/J`. With
`Y=(X/log_2(X+2))^(1/4)`, J<=Y is bounded by X/J and J>Y by the
arity charge. This produces the stated 3/4 scale with its logarithmic
factor. An upper bound `D_J<=m_J^K` alone would not imply the lower
charge; the reviewed note explicitly avoids that inference.

The lemma rules out improving this single-template upper-bound certificate
only by optimizing d, q or search weights. It does not exclude a smaller
actual incidence bound, a sharper charged prefactor, another label family,
a variable-arity recursion, or another multiplication algorithm. Its
exact-square-root disclaimer is appropriate.

This is a written algebraic review of the universal scoped theorem, not
finite-test evidence. Credits: @CubeJerry, the pinned label construction,
prior programme bounds, Route A's proof, and substantial ChatGPT
multi-agent assistance.

Reviewed SHA-256:
`4f486788baf7b1a9ce64a29e3303e73f97273dc868cbaef28eac0ff5307cb5c5`.
