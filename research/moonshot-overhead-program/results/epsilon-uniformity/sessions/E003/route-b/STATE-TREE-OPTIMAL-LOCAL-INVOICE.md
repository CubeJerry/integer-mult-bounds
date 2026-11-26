# The optimized local tree invoice, including its second logarithm

Status: **proved scoped analytic result; independent review pending**.
This concerns the retained state-tree positive invoice, including its
unchanged highest charged term. It is not a lower bound on machine
time or on other endpoint algorithms. The same leading Psi scale
persists, but its local optimization can be quantified more precisely.

Supplier: `STATE-TREE-MOMENT-PROFILE.md`, SHA-256
`b4216256a1bd2fa16c5564390e36a2f7f9facbfd3f73f7acf07e936451656888`,
and the independently reviewed lead/A tree construction.

## 1. The declared invoice

For q=2^t, t>=2, L>=2, let D=2+L(q-2), M be the exact tree weight,
and F_tree=2D+8M. Put

```
J=1+D+F_tree+mD binom(L,floor(L/2)) q^(-ceil(L/2)),
x=log2 m,       A=log2 x,       B=log2 A,
b=log2 J.
```

Absolute multiples of this positive bill have the same result below.
At q=2 use the actual four-call exception; its retained charged term
is at least m, so it is not optimal for the bound under discussion.

**Theorem.** As x tends to infinity, the infimum of b over these integer
parameters satisfies

```
inf b=2 sqrt(x[A-B+O(1)]).                            (O1)
```

The upper direction can be attained with the exact integer profile in
the moment note, with charged-rank reserve at most 1/8 and N<=m^5.
The lower direction holds without imposing those additional guards,
so it also holds for the guarded subfamily.

## 2. Elementary constraints on a small invoice

The tree visits all lambda odd states, every tree edge has cost at least
one, and D>=q. Consequently

```
b>=t,
b>=(L-1)log2(t+1),
b>=x-Lt/2.                                          (O2)
```

The last inequality uses D>=q and
`ceil(L/2)-1<=L/2`; it does not require an estimate of the binomial
coefficient. Thus `Lt>=2(x-b)`.

It suffices to consider `b<=4sqrt(xA)`, because larger bills already
exceed the claimed lower envelope. For all sufficiently large x this
implies b<=x/2. Then Lt>=x. Since L-1>=L/2 and log2(t+1)>=1, O2
also gives L<=2b and hence

```
t>=x/(2b)>=sqrt(x)/(8sqrt(A)).
```

For A>=32 this implies `log2 t>=A/4`.

Suppose t<8L. The second inequality in O2, together with Lt>=x, gives
both

```
b>=x log2 t/(2t),       b>t log2 t/16.
```

Multiplying and taking square roots yields
`b>=sqrt(x)log2 t/sqrt(32)>=sqrt(x)A/(4sqrt(32))`.
For A>8192 this contradicts `b<=4sqrt(xA)`. Therefore every invoice
in the potentially optimal range has t>=8L once x is sufficiently
large. The deliberately large explicit cutoff A>=16384 suffices;
no assertion is made that it is sharp.

## 3. Apply the actual two-sided moment estimate

For t>=8L the moment theorem gives `M>=q kappa_L/2`, where
`kappa_L>=F_L/2` and F_L counts ordered partitions. Thus
`F_tree>=2qF_L`. Since `F_L>=L!>=(L/e)^L`,

```
b>=t+L(log2 L-log2 e).                               (O3)
```

On the other hand, Lt>=2(x-b) and t<=b imply

```
L>=2(x-b)/b>=x/b>=sqrt(x)/(4sqrt(A)),
log2 L>=A/2-B/2-2.
```

Let `R=A-B-7`, which is positive at the stated eventual cutoff. Since
`2+log2 e<7/2`, O3 implies

```
b>=2(x-b)/L+(R/2)L>=2sqrt((x-b)R).
```

Solving the resulting quadratic inequality gives the explicit lower
envelope

```
b>=2sqrt(xR+R^2)-2R>=2sqrt(xR)-2R.                   (O4)
```

This is stronger than merely reusing the D+lambda subinvoice: it uses
the actual matched moment growth of the changed tree executor.

## 4. Matching upper direction and interpretation

The moment note selects integer x_0=ceil(log2 m), then

```
a=ceil(log2 x_0),   d=floor(log2 a),   S=a-d+5,
L=2isqrt(x_0//S),   t=ceil(2x_0/L)+6.
```

It proves `log2 J<=2sqrt(x_0 S)+2S+11`, with
`S=A-B+O(1)` and x_0=x+O(1). This matches O4 up to the displayed
bounded term inside the square root. The additive O(A) remainders
can be absorbed there because `A^(3/2)/sqrt(x)` tends to zero.
This proves O1.

The minus sign of the second logarithm is a local consequence of the
new factorial state moment. It does not, by itself, improve the complete
admitted multiplication envelope, remove the positive polynomial routing
toll, or show that an older executor had a matching lower-order loss.
The theorem optimizes exactly the defined positive invoice. A different
charged decomposition, a multi-array operator representation or a cheaper
physical implementation is outside its lower-bound scope.

No new finite test is represented as proving this asymptotic argument.
The exact tree and moment identities have the separately recorded
finite receipts; the present proof is the unbounded analytic comparison.

Credits: @CubeJerry; E003 lead/A state-tree construction; Route B's
moment evaluation and local optimization; substantial ChatGPT assistance.
