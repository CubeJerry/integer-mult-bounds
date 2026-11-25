# A matching obstruction for the retained nonstationary label invoice

Status: **proved scoped certificate obstruction; independent review pending**.
This is not a running-time lower bound for the source machine or integer
multiplication. It shows that changing arities at every recursive level,
allowing unequal distance parameters, and adding label levels cannot make
the retained shared-pencil *invoice* beat the two-thirds logarithmic-loss
scale. A different physical analysis may charge less than that invoice.

Predecessor: S003 A's `nested-label-invoice-barrier.md`, Theorem N, at
programme `c65aac1156a46d10c0ef2aa36fd846c7a93518e1`; OpenAI source
`math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`. The predecessor's exact-rank proof is imported
and was read in full. The additional result here is its inversion into
a per-level loss and its accumulation for arbitrary nonstationary
integer-width chains.

All logarithms are binary. Put

```
Phi(y)=y^(2/3)[log2(y+2)]^(1/3),   y>=0, Phi(0)=0.
```

## 1. The exact restricted invoice

At any level choose arity `m>=2`, label depth `ell>=2`, arbitrary
power-of-two distances `d_1,...,d_ell>=2` and alphabet size `q=2^t`.
Use exactly the predecessor's nested far relation and first-differing-bit
rectangle partition. Let

```
I_m = D(1+lambda)(1+m a),
D = rank_Q(source Gram matrix),
a = rank_F2(P_ell)/N_ell.
```

Theorem N says, uniformly over all these choices, that for real `J>=64`,

```
I_m<=m^(1/J)  implies  log2 m>=J^3 log2 J/128.          (B1)
```

We dropped its additional factor `2^(ell-2)>=1`, which only strengthens
the result. A nonminimal address realization, including S003's doubled
hyperbolic realization, has dimension at least D; its analogous invoice
is therefore at least I_m.

## 2. Inverting the necessary scale

**Lemma B1.** There is an absolute `c>0` such that every admitted local
label invoice satisfies

```
log2 I_m >= c Phi(log2 m).                              (B2)
```

For `x=log2 m>=2^16`, one may take `c=1/16`.

**Proof.** Write `b=log2 I_m`. If `b>=x/64`, then
`x>=64 log2(x+2)` for `x>=2^16` gives `b>=Phi(x)/16`.
Suppose `b<x/64` and set `J=x/b>64`. Since `I_m=m^(1/J)`, (B1) gives

```
b^3 >= x^2 log2(x/b)/128.                              (B3)
```

If `b>=x^(3/4)`, the claimed weaker lower bound follows because
`x^(1/4)>=log2(x+2)/4096` on this range. Otherwise
`log2(x/b)>(1/4)log2 x`, so B3 implies

```
b >= (1/8) x^(2/3)(log2 x)^(1/3) >= Phi(x)/16.
```

For `1<=x<2^16`, the elementary bounds `D>=2`, `lambda>=1` give
`b>=2`. Since Phi is increasing and bounded on that interval, taking
the minimum of `1/16` and `2/Phi(2^16)` proves B2 for every m. This
constant is absolute and does not depend on depth or distance choices. ∎

This inversion uses a lower bound on the **actual scalar rank** already
proved in Theorem N. Replacing a coarse upper rank certificate by the
exact rank was therefore allowed before B2 was derived.

## 3. Arbitrary rounded nonstationary chains

Consider integer widths

```
e_0>e_1>...>e_D>=1
```

with terminal `e_D<=E` for one fixed E. At level i choose any admitted
arity and label parameters. Suppose the geometric interface obeys

```
e_i/(8m_i) <= e_(i+1) <= e_i/m_i.                     (B4)
```

This is exactly the rounded guarded range I3 in the two-scale theorem.
It allows different arities, distances and nesting depth at every level.

Define the nonnegative equality invoice

```
R_i = t_i + C_i sqrt(m_i) I_(m_i) R_(i+1),
t_i>=0,   C_i>=sqrt(8),
R_D/sqrt(e_D)>=c_0>0,                                 (B5)
```

where `c_0` is fixed. The chosen normalization covers any larger
conservative source bill with its explicit absolute endpoint constant.
It is a definition of a certificate; it is not assumed equal to the
physical runtime.

**Theorem B2.** Uniformly over every chain and every choice in B4--B5,

```
log2(R_0/sqrt(e_0)) >= c_1 Phi(log2 e_0)-C_0           (B6)
```

for absolute positive `c_1,C_0` depending only on E and `c_0`.

### Proof

Normalize each R_i by `sqrt(e_i)`. The multiplicative factor becomes

```
mu_i=C_i I_(m_i) sqrt(m_i e_(i+1)/e_i) >= I_(m_i),
```

by B4 and `C_i>=sqrt(8)`. Dropping the nonnegative tolls therefore gives

```
log2(R_0/sqrt(e_0))
 >= log2 c_0 + sum_i log2 I_(m_i)
 >= log2 c_0 + c sum_i Phi(z_i),   z_i=log2 m_i>=1.    (B7)
```

Let `Z=sum_i z_i`, `y_i=log2 e_i`. The other side of B4 gives
`y_i-y_(i+1)<=z_i+3<=4z_i`. Consequently

```
Z >= (y_0-y_D)/4 >= (y_0-log2 E)/4.                   (B8)
```

The function `Phi(z)/z=[log2(z+2)/z]^(1/3)` decreases for positive z:
the sign of its cubed derivative is that of
`z/(z+2)-ln(z+2)<0`. Since `z_i<=Z`,

```
sum_i Phi(z_i)
 = sum_i z_i [Phi(z_i)/z_i]
 >= Z [Phi(Z)/Z] = Phi(Z).                            (B9)
```

For sufficiently large `y_0`, B8 gives `Z>=y_0/8`, and
`Phi(y_0/8)>=c_2 Phi(y_0)` for a fixed positive `c_2`.
Substitute into B7 and enlarge an additive constant for the bounded
remaining roots. This proves B6. ∎

The proof does not require the m_i to follow a power law, or even to be
monotone. Its use of B4 is explicit. If a different interface makes
the next width much smaller than `e/(8m)`, its volume, reserves, setup
and local toll must be proved afresh; that mechanism lies outside B2.

## 4. Consequence for the programme

The two-scale theorem's interchanger supplies a conditional upper bound
whose logarithmic certificate scale is `O(Phi(log e))`. B2 gives the
matching lower scale for the specified local label/invoice model, even
after arbitrary nonstationary parameter selection. The result does not
lower-bound the actual interchanger, because its observed runtime could
be smaller than a sufficient equality invoice.

Within this invoice, attaining a polynomial-in-`log e` overhead would
require logarithmic overhead `O(log log e)`, which is asymptotically
smaller than Phi(log e). Thus merely optimizing arity schedules, exact
rank estimates, asymmetric distances or label nesting cannot reach that
target. The explicit dyadic basis and compact executor remove unrelated
costs, but retain the rank/incidence/dimension structure to which B2
applies.

The next consequential route must change at least one binding interface:
reduce actual endpoint work below the `D(1+lambda)` accounting by new
sharing, construct a different rank/rectangle geometry, or replace the
prediction/shared-pencil architecture. These are open possibilities,
not excluded by the theorem. Neither Weak ETH nor any global lower-bound
assumption is used.

Credits: @CubeJerry; S003 A's actual-rank nested-label obstruction and
its independently overlapping Route C work; OpenAI source label/routing
construction; E003 two-scale recursion; substantial ChatGPT multi-agent
assistance. Finite checks of supporting inequalities do not replace the
unbounded proofs. No human or formal-kernel certification is claimed.
