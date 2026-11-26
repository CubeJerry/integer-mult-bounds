# A coupled Walsh call-loss and routing-toll invoice barrier

Status: **proved equality-invoice obstruction; independent review passed
for the abstract proof, with separately reviewed literal source supplier**.

This is a lower bound on a specified sufficient cost certificate. It is
not a running-time lower bound for a Walsh transform, interchange or
integer multiplication. It shows that a retained polynomial-arity
routing toll at the square-root active-width scale can bind the global
envelope even if interchange itself is granted a perfect square-root
bound. Improving the interchange label loss alone does not remove this
separate obstruction.

Theorem W1 below allows arbitrary arity choices at every level. It
does not presuppose the particular E003 two-scale policy. The source
application requires a separate lower bound on the **literal** binary
Walsh label/call invoice, not a reversal of a known call upper bound.

All logarithms are binary. Put

```
Psi(z)=sqrt(z log2(z+2)), z>=1,
Phi(y)=y^(2/3)[log2(y+2)]^(1/3), y>=0, Phi(0)=0.
```

## 1. The explicitly retained invoice

Let integer active widths satisfy

```
a_0>a_1>...>a_D>=1,    a_D<=E,
```

where E is a fixed base bound. At level i choose any arity `m_i>=2`,
and write `z_i=log2 m_i>=1`. Suppose

```
log2(a_i/a_(i+1)) <= z_i+c_w,                         (W1)
```

for a fixed nonnegative constant c_w. The rounded source Walsh
interface has c_w=3: its arity satisfies `2m<=A<=4m` and its even
child satisfies `a/(2A)<=f<=a/A`, so `a/f<=8m`.

Define a nonnegative equality invoice, already normalized by
`sqrt(a_i)`, by

```
U_i = tau_i + mu_i U_(i+1),
tau_i >= c_0 2^(kappa z_i),
mu_i >= 2^(c_l Psi(z_i)),
U_D >= c_0,                                         (W2)
```

where `c_0,kappa,c_l` are fixed positive constants. In unnormalized
notation this means that a local bill R_i has a routing toll at least
`c_0 sqrt(a_i) m_i^kappa` and a child coefficient lambda_i satisfying
`lambda_i sqrt(a_(i+1)/a_i)>=2^(c_l Psi(z_i))`.

The positive polynomial toll in W2 is a **retained invoice term**.
No claim is made that every implementation needs this much time. If a
coordinate-routing invoice instead charges `m^kappa0 sqrt(f)`, the
same premise follows with any suitable positive
`kappa<kappa0-1/2`, when `kappa0>1/2` and `a/f=Theta(m)`;
fixed constants can be folded into c_0. If the only retained toll is
ordinary `m^C` work per volume, without the square-root-width factor,
W2 need not hold. The theorem deliberately does not cover that case.

## 2. Every such schedule pays the two-thirds scale

**Theorem W1.** For fixed constants in W1--W2 there are constants
`c_1>0,C_1` such that every admitted chain and equality invoice obeys

```
log2(U_0/c_0) >= c_1 Phi(log2 a_0)-C_1.               (W3)
```

The choices of m_i may be nonmonotone, adaptive, asymmetric or different
at every level. Constructors, precision and other nonnegative work may
be omitted from the invoice; adding them cannot evade this bound.

### Proof

Rescale by c_0 and put

```
F_i=U_i/c_0,   H=log2 F_0,   y=log2 a_0,
Z=sum_i z_i.
```

Every `mu_i>=1`. Also `F_D>=1` and every normalized toll is at least
`2^(kappa z_i)`. Exact nonnegative unfolding therefore gives both

```
H >= kappa z_i for every i,
H >= c_l sum_i Psi(z_i).                              (W4)
```

The first bound includes the root toll and every deeper toll, because
all its prefix multipliers are at least one. The second bound retains
only the final base contribution. These are simultaneous constraints
on the same complete invoice H.

By W1, using `z_i>=1`,

```
y-log2 E
 <= sum_i log2(a_i/a_(i+1))
 <= sum_i(z_i+c_w)
 <= (1+c_w) Z.                                      (W5)
```

For a nonempty chain put `M=H/kappa`. Equation W4 gives `z_i<=M`
and `M>=1`. The function

```
Psi(z)/z = sqrt(log2(z+2)/z)
```

is decreasing on positive z: its squared derivative has the sign of
`z/(z+2)-ln(z+2)<0`. Thus

```
sum_i Psi(z_i)
 >= Z Psi(M)/M
 = Z sqrt(kappa log2(H/kappa+2)/H).                   (W6)
```

Combining W4--W6 gives the useful implicit inequality

```
H^3 >= c_l^2 kappa Z^2 log2(H/kappa+2).               (W7)
```

For sufficiently large y, W5 implies `Z>=c y` with fixed c>0.
First use `log2(H/kappa+2)>=1` in W7 to obtain
`H>=c' y^(2/3)`. Hence, after increasing a fixed initial threshold,
`log2(H/kappa+2)>=(1/2)log2(y+2)`. Substitution back into W7 proves
`H>=c_1 Phi(y)`. Empty chains and the bounded remaining roots are
covered by an additive constant C_1. This proves W3. ∎

The argument does not bound the number of recursive levels first.
It uses the total width progress, and the fact that the same budget
must pay both the largest arity toll and the accumulated local loss.
Consequently making a few very large jumps or many small jumps cannot
escape the inequality.

If a node has several children of the same successor width, their
normalized positive coefficients sum to mu_i. Allowing different future
arity policies in those children does not help: choose a child with
the least normalized remaining invoice. The parent is bounded below
by its toll plus mu_i times that minimum. Following these choices
produces a chain satisfying the proof. This extension retains the
common-successor-width interface; different child-width mechanisms
would need a separate argument.

## 3. Why a better interchanger can leave the same global scale

The numerical Walsh branch has a retained local call profile with
logarithmic excess of order Psi(log m). Its physical middle operations
also make polynomially many arity-dependent address changes. The
two-scale upper construction pays their explicit polynomial multiplier
at the interchange's square-root active-width scale.

Even if the interchange overhead were improved from
`2^(O(Phi(log a)))` to `2^(O((log a)^(2/3)))`, or all the way to an
ideal `O(sqrt(a))` per-volume invoice, the **retained** local terms
in W2 could remain. In that event W3 still forces Phi(log a) for the
numerical Walsh certificate. It would be incorrect to infer removal
of the global logarithmic factor from an interchange-only label
improvement without rechecking the Walsh toll/loss balance.

Conversely, E003's upper analysis chooses
`log m=Theta(Phi(log a))`. Its derivative potential balances
`Psi(log m)` against the decrease of Phi, while its logarithmic local
routing toll is O(log m). It attains the same order as W3 in this
invoice model. This is an analytic matching statement, not a priority
claim: remote E002 independently admitted the same global scale during
this session.

### Literal source instantiation

The E003 lead's `../lead/binary-walsh-label-invoice-barrier.md`, reviewed
separately in `REVIEW-BINARY-WALSH-INVOICE.md`, proves the required
literal local profile. For `q=2^t`, `L>=2`, `s=floor(L/2)`, put

```
D=2+L(q-2),
lambda=sum_(j odd) binom(L,j)t^j,
J=D[1+lambda+m binom(L,s)q^(-ceil(L/2))].
```

Its exact-rank, exact-free-incidence and nonzero charged-coefficient
proof gives `log2 J>=sqrt(log2 m log2 log2 m)` for `m>=2^16`.
The canonical charged count is within a factor two of its highest
degree term: successive terms `binom(L,j)q^j`, for `j<=s`, increase
by a factor at least two. Thus the nonzero highest coefficient and
the full canonical list are comparable with absolute constants.

Retain the source polynomial-dimension guard `D<=m`, its rational
Newton stage count Theta(sqrt(m)), and its finite repair. A conservative
completed call **upper invoice** may be declared as

```
lambda_m=K sqrt(m) J,
```

where K is one fixed sufficiently large constant and may be enlarged
to `K>=sqrt(8)`. This enlargement is an explicitly chosen sufficient
bill, not a lower bound on an implementation's call count. Under the
rounded source width `f>=a/(8m)`, its normalized equality coefficient
satisfies

```
mu=lambda_m sqrt(f/a) >= J.
```

For large m, the lead's theorem therefore gives
`log2 mu>=c_l Psi(log2 m)` with fixed `c_l>0`. For any retained
bounded arity range, `J>=D>=2` and bounded Psi extend the same
inequality after shrinking c_l. Alternatively one may restrict every
nonbase call to the fixed admissible large-arity guard.

The **independent routing premise** is still
`tau>=c_0 m^kappa` after square-root normalization. It is satisfied
by a declared polynomial-arity routing bill using an ideal
`I(a)=sqrt(a)` interchange upper envelope, or by a retained
`m^kappa0 sqrt(f)` bill with `kappa0>1/2`. The lead's label theorem
does not prove this premise as an actual-time lower bound. If a new
implementation changes that declared routing bill, this instantiation
does not apply until the new recurrence is analyzed.

This is consequently a matching statement about the specified positive
equality invoice. At no point is an upper bound on a call count reversed
into a lower bound on machine time.

### After the constructive destination-gauge refinement

E003 A's `ROUTING-DESTINATION-GAUGE-SHARING.md` changes the free
endpoint list. Its exact free charge becomes
`2(D-1)+2lambda+4(q-1-t)lambda'`, where the derivative denotes the
explicit incidence polynomial derivative. The older D-lambda lower
bound is not assumed to survive this change unchanged.

The lead's separately proved `rank-weighted-walsh-invoice.md`, checked
in `REVIEW-DESTINATION-GAUGE-AND-RANK.md`, uses the fresh invoice

```
J_rank=D+lambda+2(q-1-t)lambda'
       +D m binom(L,s)q^(-ceil(L/2)).
```

Its free part is smaller by Theta(t) than the old free part, with
absolute comparison constants for t>=2. Nevertheless its own proof
gives `log2 J_rank>=sqrt(log2 m log2 log2 m)/4` for m>=2^16.
Declaring the completed sufficient call invoice as
`K sqrt(m) J_rank` and repeating the rounded normalization above
therefore supplies the same local Psi premise, with different
absolute constants. Theorem W1 still applies when the **separate
positive polynomial normalized routing toll** is retained.

This records a real local sharing improvement and a fresh analysis of
its new invoice. It does not reject that improvement by appealing to
a theorem about a call list that has been replaced.

### After the prepared-basis walk and Gray refinement

E003 A's `ROUTING-STATE-WALK-SHARING.md`, independently checked in
`REVIEW-STATE-WALK-SHARING.md`, further changes both endpoint schedules.
Writing B=2^(L-1), its round-trip reflected Gray order has exact free
invoice, for t>=2,

```
F_gray=2D+4(B-1)+8(q-2)(lambda-B)/(t-1).
```

Thus `F_gray=Theta(D+(q/t)lambda)`. The prepared source and accumulated
destination arrays are changed between states; reverse visits change
bases without adding the same contribution again. This is a real
order-L improvement over the earlier rank-weighted free bill when
its nonconstant term dominates D. At q=2 all relevant subspaces are
constant and the free invoice is exactly four.

The smaller free invoice requires a new argument. For q>=4, every
distinct source-state transition has subspace distance at least two,
and all lambda source states must be visited. Boundary calls contribute
at least D. The retained call list therefore dominates

```
J_walk=D+lambda+mD binom(L,s)q^(-ceil(L/2)).
```

The fresh proof gives `log2 J_walk>=sqrt(log2 m log2 log2 m)/2`
for m>=2^16. At q=2 the D+lambda free subinvoice is unavailable;
the charged term alone is at least m and supplies the same lower scale.
This exception is not concealed by extrapolating the q>=4 transition
formula.

J_walk is a lower subinvoice, not automatically a sufficient call bill.
For the actual normalization, retain the changed executor's sufficient
positive bill, for example an absolute multiple of

```
J_actual=1+D+F_gray+mD binom(L,s)q^(-ceil(L/2)),
```

with F_gray replaced by four at q=2. The full canonical charged count
is at most twice its displayed top term. Retained Newton stage and
finite-repair factors are included in the completed bill
`K sqrt(m) J_actual` as in the earlier instantiations. After enlarging
K, the rounded width guard again gives normalized coefficient at least
J_actual, hence the fresh Psi lower profile from J_walk (or the q=2
charged term). Theorem W1 therefore applies **if the independent
positive polynomial normalized routing toll is still retained**.

This extension concerns the changed positive equality invoice. It
does not prove that a smaller shared physical routing bill is impossible,
and does not apply the obsolete D-lambda or rank-weighted lower count
to the new walk.

## 4. A general necessary tradeoff

The same proof applies to a local logarithmic loss

```
g(z)=z^alpha [log2(z+2)]^beta,
0<=alpha<1, beta>=0,
```

whenever `g(z)/z` is eventually decreasing and the bounded initial
range is given a fixed positive lower bound. Retaining
`tau_i>=c_0 2^(kappa z_i)` and `mu_i>=2^(c_l g(z_i))` gives

```
H >= c y^(1/(2-alpha))
          [log2(y+2)]^(beta/(2-alpha))-C.             (W8)
```

Indeed W4 caps z_i at H/kappa, and the analogue of W6 yields
`H^(2-alpha)>=c y [log2(H+2)]^beta`. A first estimate with the
logarithmic factor replaced by a positive constant implies a positive
power lower bound in y; inserting that estimate into the logarithm
gives W8. The hypotheses, not just a loose asymptotic upper profile,
are essential.

For `alpha=beta=1/2`, W8 is exactly W3. Even a fixed positive
logarithmic call loss (`g=1`) combined with the retained polynomial
routing toll yields an Omega(sqrt(log a)) logarithmic-certificate
barrier. Thus reaching a polynomial-in-log(a) overhead through this
same recursion would require a more favorable local interface than
merely replacing Psi by a positive constant. A call coefficient tending
to one, a smaller physical routing toll, or another recursive structure
falls outside this obstruction and remains a possible research target.

## 5. Structural negative controls

Each binding premise has a concrete failure mode if removed.

* Without the polynomial-arity normalized toll, take one large jump
  from `a=2mE` to a fixed even E and give it toll one. The invoice
  `U=1+2^(c_l Psi(log m))` has logarithm of order
  `sqrt(log a log log a)`, which is smaller than Phi(log a).
  This satisfies the source-scale width relation but violates the
  positive kappa toll premise.
* Without positive accumulated call loss, choose one fixed arity
  at every level, a fixed width reduction, and `mu_i=1`. With constant
  positive toll, the equality invoice is linear in the number of
  levels. Its logarithm is only O(log log a), smaller than W3.
* Without W1, fix `m=2` and jump from an arbitrary root directly to
  E. Constant local toll and local call coefficient then give a
  constant invoice regardless of root width. The width-volume
  interface is therefore an essential hypothesis.

These controls are mathematical examples outside the theorem's
hypotheses. They do not describe implementations of the source
transform. In particular they show why the result cannot be promoted
to an unconditional Walsh or multiplication lower bound.

## 6. Open next questions and scope

1. Determine whether the declared polynomial-arity routing bill can
   be improved enough to change the proved local invoice, rather than
   only optimizing the schedule of its existing terms.
2. Can successive middle coordinate changes share physical routing so
   that the normalized polynomial-arity toll in W2 is replaced by a
   smaller proved bound?
3. Can different finite labels or a different predictor/converter reduce
   the local logarithmic call-loss profile, while retaining full-rate
   rows and an honestly priced physical executor?

No statement here excludes such changes. No complexity conjecture,
machine-model lower bound, empirical runtime extrapolation, formal
kernel check or human review is used.

Credits: @CubeJerry; the pinned source Walsh interfaces and E003
two-scale construction; independent E003 lead work on the literal
binary-Walsh label profile; substantial ChatGPT multi-agent assistance.
