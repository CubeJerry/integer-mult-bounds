# Two common-Q native calls and two nonself queries on four arbitrary roles

**Proved formal positive control. No new κ and no R0 admission.** Two complete standard common-Q HOST2 calls, at two distinct fresh stages, together with two literal nonself QUERY(-1) calls produce four independent Q^-1 D1D2 targets. There are no paid idles, extra role fields, zero-input promises or productive-helper credits. The existing ordinary LAMBDA service is retained and every occurrence is listed. A three-native/zero-query version is also supplied.

The actual R0 sources have different, noncentral stage couplings. This theorem does not replace those couplings by Q. It supplies a constructive common-Q control for the ongoing mixed-orientation caller problem.

## 1. Exact model and ordinary premises

Let Q,D1,D2,D3 be commuting endomorphisms of any complex vector space, with Q^4=I. The D variables are unrestricted and need not be invertible. Standard HOST2 at stage s, on four distinct roles(X,Y,U,V), is

\[
(X,Y,U,V)\longmapsto
\bigl(D_sX,\ D_s(Y+Q^{-1}X),\ D_s(U-QV),\ D_sV\bigr).
\]

QUERY(-1) updates a destination by Q^-1 times a distinct source. It is not a self-query and does not change its source.

Retain the established ordinary phase units

\[
\lambda_\pm=\frac{(1\pm i)I+(1\mp i)Q^2}{2},
\quad \lambda_+\lambda_-=I,
\quad \lambda_+^2=Q^2.
\]

Define S=λ_+Q^-1=Qλ_-. Then S²=I and S commutes with every D_s. In the intended Gaussian common-Q interface, Q² is an ordinary whole-field translation and these are the existing LAMBDA macros. This ordinary implementation premise is explicit; the abstract relation Q^4=I alone is not a claim that λ is costless or physically available. The listed LAMBDA, SCALE and SWAP scans retain their ordinary tape and precision costs.

Preapplying λ_- on Y,V and postapplying λ_+ on Y,V normalizes one HOST2 to

\[
(X,Y,U,V)\mapsto D_s(X,Y+SX,U-SV,V).
\]

No D inverse occurs in this normalization.

## 2. Two parallel lower and upper shears

On logical role pairs(a,b) and(c,d), write

\[
L(S)=\begin{pmatrix}1&0\\S&1\end{pmatrix},
\qquad U(-S)=\begin{pmatrix}1&-S\\0&1\end{pmatrix}.
\]

A normalized HOST2 with native roles(X,Y,U,V)=(a,b,d,c), and a sign conjugation on d, gives L(S) on both pairs while applying D_s to all four roles. The literal seven events are:

```
LAMBDA(b,-1); LAMBDA(c,-1); SCALE(d,-1);
HOST2(s; a,b,d,c);
SCALE(d,-1); LAMBDA(b,+1); LAMBDA(c,+1).
```

A normalized HOST2 with native roles(X,Y,U,V)=(b,a,c,d), and a sign conjugation on a, gives U(-S) on both pairs. Its seven events are:

```
LAMBDA(a,-1); LAMBDA(d,-1); SCALE(a,-1);
HOST2(s; b,a,c,d);
SCALE(a,-1); LAMBDA(a,+1); LAMBDA(d,+1).
```

These are invertible changes on arbitrary baselines; signs do not specialize or discard any input. Use the first block at stage1 and the second at stage2. Because Q,λ and D1,D2 commute, their body factors multiply to D1D2 on every role without an idle or correction.

## 3. Two actual queries finish all four targets

For a distinct pair(a,b), the three events

```
LAMBDA(a,+1); QUERY(-1; destination=b, source=a); LAMBDA(a,-1)
```

perform exactly b←b+Sa and restore a. Apply this once to(a,b) and once to(c,d). The sources are literal other public roles throughout; no query is a self update and no hidden auxiliary input is used.

The chronological sequence on either pair is L(S), U(-S), L(S). Later operations multiply on the left, and direct multiplication gives

\[
L(S)U(-S)L(S)=\begin{pmatrix}0&-S\\S&0\end{pmatrix}.
\]

Thus the two-role output is(−SD1D2 b, SD1D2 a). Swap the two roles and negate the second. This returns(SD1D2 a, SD1D2 b). Do the same for(c,d), and finally apply λ_- to all four roles. Since λ_-S=Q^-1, the result is exactly

\[
\boxed{(Q^{-1}D_1D_2a,\ Q^{-1}D_1D_2b,\ Q^{-1}D_1D_2c,\ Q^{-1}D_1D_2d).}
\]

Every variable a,b,c,d is arbitrary and independent. Every field participates in both natives. The complete emitted word `two_native_two_query.json` has28 events:2 HOST2,2 QUERY,16 LAMBDA,6 SCALE and2 SWAP. It has no IDLE, no additional role, no source retirement and no additional paid operation type. Its paid Gaussian profile is two full native calls and two full queries under the stipulated common-Q service. The ordinary work is finite but retained.

## 4. Three natives and no queries

Replace the last two query shears by the seven-event lower-native block at stage3. It acts on both pairs together and supplies the same last L(S), now with the common additional D3 on every role. The same signed swaps and λ_- postprocessing give four independent Q^-1D1D2D3 targets.

The emitted `three_native_zero_query.json` has29 events:3 HOST2,16 LAMBDA,8 SCALE and2 SWAP. It has no QUERY, IDLE or new role. This is a useful scalar positive control; it is not a physical R0 caller.

## 5. Complete algebraic certificate and controls

`check.py` starts four independent input symbols and replays every literal event over

\[
\mathbb Q(i)[q,D_1,D_2,D_3]/(q^4-1).
\]

Only the q exponent is reduced modulo4. All D exponents remain unrestricted; no inverse, idempotence or special value is introduced. Exact Gaussian rational coefficients are preserved. Each result has exactly one nonzero coefficient in each output: its own arbitrary input multiplied by q^3 and the intended product of distinct body variables. Thus the finite symbolic certificate proves an identity in the stated universal ring, rather than extrapolating from samples of Q or D.

The checker rejects deleting one query, changing the second native's sign conjugation, failing to restore a query source's λ scaling, reversing a query's Q orientation, repeating the first body stage instead of the second, and making a query self-referential. Normal and optimized receipts are identical. These controls include the q²=−1 sector, which would be lost by incorrectly assuming q²=1.

Run `python check.py` and `python -O check.py --receipt RESULT-OPTIMIZED.json` in this directory. The literal programs, all-column endpoint certificates and exact census are committed together.

## 6. Programme relevance and limits

The scalar/common-Q task has a positive solution with fewer queries than the proposed two-native/three-query allowance. Its usefulness is to identify a concrete algebraic objective for the actual R0 mixed-orientation interface. To transfer it, the programme must establish the corresponding genuine stage couplings and ordinary transports, preserve all independent output targets, and charge every query, body correction, native source and ordinary pass. The present theorem does none of that transfer by assumption. The foundational compiler, source, ordinary-tape, precision and outer multiplication obligations remain.

Root and Worker C independently identified the simultaneous three-shear construction; Worker A posed the complementary scalar synthesis problem. Worker C emitted the complete chronology, universal proof and exact polynomial certificate. The standard HOST2, LAMBDA normalization and QUERY semantics retain their predecessor credit. Prepared for @CubeJerry with OpenAI assistance. **No new κ.**
