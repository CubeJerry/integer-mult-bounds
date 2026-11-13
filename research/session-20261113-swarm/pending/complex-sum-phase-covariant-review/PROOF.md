# Exact-sum, phase-covariant complex-pair review

## Operator and candidate

For Gaussian integers \(u,v\), put
\[
s=u+v,\qquad d=u-v.
\]
The ideal map from #6509 with \(\sigma=+1\) is
\[
C_+(u,v)=\left(\frac{s+i d}{2},\frac{s-i d}{2}\right).
\]
In real coordinates \(z=(\Re z,\Im z)\), write
\[
H=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\quad
T=H/2,\quad
J(a,b)=(-b,a),\quad Q=-J.
\]
Thus multiplication by \(i\) is \(J\), \(T^2=I/2\), and \(HT=I\).

The candidate preserves \(s\) and selects an integer difference \(d'\):

- If the two real-coordinate parities of \(s\) agree, set \(d'=Jd\).
- Otherwise let \(p=\Re(s)\bmod2\), set \(t=TJd\), apply the two-axis
  half-integer pairing \(M_p\) below to get \(m=M_p(t)\), and set \(d'=Hm\).

Return \(u'=(s+d')/2,\ v'=(s-d')/2\). For \(p=0\), axis 0 uses type 0
and axis 1 type 1; for \(p=1\), the types are swapped.

Type 0 pairs, separately on each sign, magnitudes
\((\tfrac12+2k,\tfrac32+2k)\) for \(k\ge0\). Type 1 pairs
\(-\tfrac12\) with \(+\tfrac12\), then pairs, separately on each sign,
\((\tfrac32+2k,\tfrac52+2k)\). A coordinate's score is the lower
absolute magnitude of its pair, except the central pair has score zero.
Choose the coordinate of least (score, index) and toggle its pair.

## Integral outputs, exact sum, and inverse

Input Gaussian integrality is exactly \(d\equiv s\pmod2\) componentwise.
In the equal-parity branch, \(Jd\equiv s\pmod2\). In the mixed branch,
write \(d=(2a+p,2b+1-p)\), where \(p=\Re(s)\bmod2\). Then
\[
t=TJd=(a-b+p-\tfrac12,\ -a-b-\tfrac12),
\]
so \(t\) is half-integral and its coordinate sum has parity \(1-p\).
The pairing M toggles one coordinate by one, so \(m=M_p(t)\) has
half-integral coordinates and sum parity \(p\). For any such
\(m=(r+\tfrac12,q+\tfrac12)\),
\[
Hm=(r+q+1,\ r-q)
\]
is integral with coordinate parities \((p,1-p)\). These are the parities
of \(s\), so \(s\pm d'\) are both even coordinatewise. The returned
outputs are Gaussian integers and sum exactly to \(s\).

For fixed \(p\), M is an involution: a toggle leaves every score
unchanged, hence it selects the same coordinate and toggles the pair back.
The score classes on the two types are disjoint: type 0 scores are
\(\tfrac12+2\mathbb Z_{\ge0}\), while type 1 scores are zero or
\(\tfrac32+2\mathbb Z_{\ge0}\). Thus the selected coordinate is unique.
The map \(d\mapsto t=TJd\), followed by M and H, is a bijection from
the input difference parity class \(d\equiv s\pmod2\) onto that same
output parity class: \(T J\) is invertible, M bijects the two half-grid
sum-parity classes, and H bijects the half-grid class of sum parity p
with integer vectors of parity \((p,1-p)\). The equal-parity branch is
the bijection \(d\mapsto Jd\). Therefore the full map is bijective on the
Gaussian pair lattice, fiberwise at each exact sum.

The inverse difference is
\[
d=
\begin{cases}
-Jd',&\text{equal-parity branch},\\
-JH\,M_p(Td'),&\text{mixed-parity branch}.
\end{cases}
\]
The second formula follows from \(Td'=M_p(t)\), applying M again to
recover \(t=TJd\), and then using \(d=-JHt\). Reconstruct the inverse
pair from \(s,d\) using \((s\pm d)/2\).

## Accuracy and exact radial upper bound

In the equal-parity branch \(d'=Jd\), so the pair is exact. In the mixed
branch \(m-t=\delta\) is one signed coordinate unit vector and
\[
d'-Jd=H\delta.
\]
Each column of H has squared norm 2. The two output errors are
\((d'-Jd)/2\) and its negative, so their combined squared Euclidean norm
is \(\|H\delta\|^2/2=1\). Thus every pair has error at most one.

The pair norm satisfies
\[
\|u\|^2+\|v\|^2=\frac{\|s\|^2+\|d\|^2}{2}.
\]
In the mixed branch, \(\|t\|^2=\|d\|^2/2\) and
\(\|Hm\|^2=2\|m\|^2\). If M selects a central type-1 pair, it only
changes \(-\tfrac12\) to \(+\tfrac12\) or conversely, so the norm does
not change.

Otherwise let \(a>0\) be the selected lower magnitude and \(q=2a+1\).
Because there are two axes with opposite score phases, minimality of a
forces the other axis's pair score to be at least \(a+1\). The lower
endpoint in the two-dimensional t-plane therefore has
\[
\|t_{\rm low}\|^2\ge a^2+(a+1)^2.
\]
The squared t-norm jump is q. Consequently
\[
\|d_{\rm low}\|^2=2\|t_{\rm low}\|^2
\ge 2a^2+2(a+1)^2=q^2+1.
\]
The pair's squared norm changes by q. If \(R,R'\) are its lower and
higher endpoint norms, then
\[
R^2=\frac{\|s\|^2+\|d_{\rm low}\|^2}{2}
\ge\frac{q^2+1}{2},\qquad R'>R.
\]
Thus \(R,R'>q/\sqrt2\), and
\[
|R'-R|=\frac{q}{R'+R}<\frac1{\sqrt2}.
\]
The map's global supremum is at most \(1/\sqrt2\).

## Sharp universal lower bound at fixed exact sum

Consider any exact-sum Gaussian pair map whose combined error relative
to \(C_+\) is at most one. Fix \(s=(1,0)\), and for each positive integer
a use \(d=(2a+1,0)\), corresponding to Gaussian integer inputs
\[
u=(a+1,0),\qquad v=(-a,0).
\]
The ideal difference is \(Jd=(0,2a+1)\). Exact-sum integrality forces
\(d'\equiv s\pmod2\). Pair error at most one is equivalent to
\(\|d'-Jd\|^2\le2\). Both coordinate differences are odd, so each must
be \(\pm1\). Therefore the only possible output differences are
\[
d'=(\pm1,2a)\quad\text{or}\quad d'=(\pm1,2a+2).
\]
The input pair norm squared is \(n=2a^2+2a+1\); the two possible output
norm squares are \(m_-=2a^2+1\) and \(m_+=2a^2+4a+3\). The corresponding
radial gaps are
\[
\frac{2a}{\sqrt n+\sqrt{m_-}},\qquad
\frac{2a+2}{\sqrt{m_+}+\sqrt n}.
\]
Both tend to \(1/\sqrt2\). At every a, any legal output must choose one
of these gaps, so every exact-sum error-one map has worst-case bilateral
radial slack at least \(1/\sqrt2\). Combined with the upper bound, this
candidate is sharp in the stated class.

## Symmetries and non-symmetries

Global multiplication by i sends \(s,d\) to \(Js,Jd\). In the mixed
branch \(p\) changes to \(1-p\), and
\[
t'=TJ(Jd)=-Td=Qt,\qquad Q=-J.
\]
The phase-swapped pairings obey \(M_{1-p}(Qt)=QM_p(t)\): Q swaps the
axes and changes one sign, while p swaps the two type assignments. Also
\(HQ=JH\), so the output difference transforms by J. The equal-parity
branch is linear and has the same covariance. Hence the global map is
Gaussian-unit phase covariant.

Wire swap fixes s and sends d to -d. M is odd under sign reversal, so
d' changes to -d'; the output pair is swapped. Thus this map commutes
with wire swap.

Let C be complex conjugation, \(C(a,b)=(a,-b)\). M commutes with C
because its pair rules are sign-symmetric. In the equal-parity branch
\(CJC=-J\). In the mixed branch \(TJC H=C\) and \(CHC=-JH\).
Together these identities give
\[
F^{-1}=CFC.
\]
The candidate is generally not forward conjugation-equivariant:
\(F(Cx)\ne C F(x)\). The exhaustive receipt records this distinction.

No fourth-power property follows. The exact checked counterexample in
RESULT.json has input \((-2-2i,-2+i)\), first image
\((-1-i,-3)\), and fourth iterate \((-3,-1-i)\), which differs from
the input and even differs from the first image. The phase pairings
themselves do not commute: on doubled half-grid input \((-9,-9)\), the
orders (M_1M_0) and (M_0M_1) return \((-9,-5)\) and \((-5,-9)\),
respectively. The executable receipt stores the two orders explicitly.

## Exact computational challenges and limits

The separate integer checker examines all 625 pairs whose four real
coordinates lie in \([-2,2]\), plus 20 explicit large cases through
coordinate scale \(2^{512}\). It checks exact sum, integrality, inverse,
error, the exact integer \(1/\sqrt2\)-slack criterion, global i covariance,
wire swap, and conjugation-as-inverse. It also records the failure of
forward conjugation equivariance, detects a mutant that fails to swap
the p-dependent types, and finds the fourth-power counterexample.

These computations corroborate the all-input algebra; the universal
claims above do not follow from the finite sample. The task is a
mathematical supplement to the #6509 exact-sum branch. It makes no
physical-tariff or multiplication-frontier claim.
