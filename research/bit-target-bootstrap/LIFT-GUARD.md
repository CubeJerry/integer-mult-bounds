# Retained input-lift gain through the moonshot interval

**Source-bound guard repair; no new native construction or κ.** The selected
`research/shared-wire-split-composition/interval_gate.py` retains the local
input-lift signed gain

`H(k)=7^(1-k)+3^(1-k)+5^(1-k)-9^(1-k)-4^(1-k)-2`.

The physical input-lift construction and these ranks are predecessor work,
including DreamingOfClouds' shared-carrier input lift; this note changes only
the sufficient interval proof used when considering a stronger target.
For the old range, the source bounds `g'(1)+k*M<0` using the sum of absolute
second-derivative terms. That sufficient test becomes positive at k=1/200.
Its failure does not show that the lift ceases to help.

**Lemma.** For every real `0<k<=51/10000`, `H(k)>(9/100)k>0`.

**Proof.** H(0)=0. Each `r^(1-k)` decreases in k. Therefore, on this
whole interval,

```
H'(k) >= 9^(1-51/10000) log 9 + 4^(1-51/10000) log 4
          -7 log 7 -3 log 3 -5 log 5 > 9/100.
```

The final strict rational enclosure is checked by `verify.py` with the
following complete bounds, independent of the source interval engine.
For integer r>=1 put y=(r-1)/(r+1), n=128. Then

```
L=2 sum(j=0..n-1) y^(2j+1)/(2j+1),
0<=log(r)-L<=2 y^(2n+1)/((2n+1)(1-y^2)).
```

For the ranks in the display, the remainder is positive and bounded as
written by replacing each remaining denominator with 2n+1 and summing a
geometric series. Put x=k log(r); all interval endpoints satisfy 0<=x<1.
The alternating Taylor polynomial of degree 15 at the upper x endpoint
is a lower bound for exp(-x); degree 14 at the lower endpoint is an upper
bound. Multiplying by r gives a bound on r^(1-k). All comparisons use
Fractions and explicit directions. The resulting derivative lower bound
strictly exceeds 9/100. Integrate from 0 to k to obtain the lemma. ∎

For clarity the verifier also proves that the **old sufficient test**
`g'(1)+(1/200)*M` exceeds 11/100, using a directed rational lower bound.
Thus the repair is necessary if reusing that particular guard at the target;
it does not establish the target's complete signed moment. The native word,
operator, arrays, fees, and all five foundational assumptions are unchanged.

The interval 51/10000 includes κ★=1/200 plus the strict raw, compiler and
outer slacks in the hypothetical target blueprint. It is not advertised as
the largest positivity domain or a physical supplier admission.
