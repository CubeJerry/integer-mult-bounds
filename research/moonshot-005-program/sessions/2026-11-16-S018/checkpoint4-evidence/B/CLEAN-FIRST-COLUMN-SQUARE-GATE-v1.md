# Clean first-column transport: a necessary normal form and a full square-algebra gate

**Universal fixed-template theorem, pending independent review. No caller or new kappa.**
This uses arbitrary ordinary mixing of all three banks at the first interface.
The second theorem covers the entire admitted source-square monomial algebra,
not a finite group census or a failed search.

## Scope and component facts

Let a=A^tensor V be the literal four-bit source, D=16^V, and

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a²,0],[0,a,0],[0,0,I]],
    E=L C U Q L.

C and Q are ordinary units. Each block is a fixed finite sum of tensor lifts
of root-four monomials, with actual scalar phases, including i^V, retained.
The admitted source powers a,a²,a³ are pure Gaussian ranks1,2,3. Projection
onto a Gaussian component commutes with ordinary left/right multiplication.
Any individual word with k source factors has one-column support at most2^k.
This support observation is wordwise, not a bound on the support of a sum.

All component arguments use finite tensor separation for the complete fixed
word catalogue, including endpoint encodings. Thus each template has a V0;
the assertions hold at every V>=V0 at which its claimed units and endpoint
identity hold. They exclude a fixed finite template valid at all sufficiently
large widths, not an arbitrary isolated small-width factorization.

An ordinary-equivalent independent421 endpoint has E=E1+E2+E4, where each
Er=pi_r(E) has rankD. Since E is invertible on dimension3D, their images form
a direct sum. Indeed their image sum contains im(E), hence is the entire
3D-dimensional space; its dimension equals the sum of the three ranks.
We use this directness, not merely the three numerical rank requirements.

## 1. A necessary normal form for every ordinary Q

Write

    C=[[s,b,c],[t,d,e],[u,f,g]],
    shat=a s a^-1 ordinary, that=a t a^-1 ordinary.       (1)

Neither s nor t is assumed invertible. Define the block columns

    V=(shat,that,0)^T,  W=(0,s,u)^T,
    Z=(a b a,b a+a d a,f a)^T,
    F=(a c,c+a e,g)^T.

Literal ordered multiplication gives

    L C U=[V a²+W a, -V a³-W a²+Z, F].                 (2)

**Necessary-normal-form theorem.** If E is an independent421 endpoint up to
ordinary units, then

    c=g=0,  s and e are units,
    q02=q12=0, q22 is a unit,                           (3)

and Q's active corner Q_A=[[q00,q01],[q10,q11]] is a unit. In particular,
C=[[s,b,0],[t,d,e],[u,f,0]], with the active-to-idle block e a full unit.

Only the terms -V a³ q10 a and -V a³ q11 a can contribute rank4 in E;
every other word has at most three source factors. Consequently
im(E4) is contained in im(V). Rank(E4)=D forces V injective and
im(E4)=im(V).

The last input column is (2) times(q02,q12,q22)^T. Its only rank3 part is
-V a³ q12. Thus q12=0. Its rank2 part is now V a² q02, whose image lies
in im(E4). Directness of im(E2) and im(E4) forces V a² q02=0, hence q02=0.
Q's last column is (0,0,q22)^T, so q22 is a unit. The ordinary part of the
last endpoint column is (0,c q22,g q22)^T; it vanishes, giving c=g=0.
C's last column is now(0,e,0)^T, so e is a unit.

The complete last endpoint column is (0,a e q22,0)^T. It is pure rank1
and fills the middle output bank. Therefore im(E1) is exactly that bank.
If shat z=0, then Vz lies in the middle bank; directness of im(E4) and
im(E1) forces Vz=0, and injectivity of V forces z=0. Hence shat and s
are units. Finally Q is block lower triangular with unit q22, so Q_A
is a unit. This proves (3) without restricting Q's ordinary algebra.

## 2. The complete source-square algebra cannot supply Q

Let K be the complete class of root-four monomials J for which A² J A^-2
is monomial. The independently reviewed support/character classification
has 24*384^4=521838526464 elements. Every J in K maps the original bit pair
(a,b) to sigma(a,b), independently of(c,d), for some permutation sigma.
Let O_K be the finite linear span of their tensor lifts; this is an ordinary
algebra since K is a group. Both actual tensor scalar phases and exterior
Gaussian coefficients are retained. No finite-dimensional or commutative
specialization of O_K is imposed.

Two structural facts hold for every q in O_K:

    a² q a is pure rank3;                              (4)
    pi0(a q a)=pi1(a q a)=0.                           (5)

For (4), write a² q a=(a² q a^-2) a³. The conjugate coefficient is ordinary.
For (5), each monomial word A J A has exactly four nonzero entries in every
column. The right A branches into inputs to J with distinct original bit
pairs (b,c) and(b,c xor1). Their images under sigma are distinct. After the
left A rotates those pairs, they appear in the output spectator positions
(a,d), so the two branch sets are disjoint. The left A adds two paths in
each set. Every path amplitude has absolute value1/2 and no paths coincide.
Thus this word has support4, excluding the ordinary and rank1 classes.
No claim that every such word is a Gaussian rank2 word is needed. Expanding
finite sums and using tensor separation proves (5) at faithful widths.

**Whole-square-algebra theorem.** Under (1), no Q in GL3(O_K) can make E
ordinary-equivalent to independent421. Other C blocks are unrestricted
ordinary and may include genuine idle coupling, noncommuting controls and
arbitrary fixed clocks.

Apply the necessary normal form. The bottom row of L C U is

    [u a, -u a²+f a, 0].                              (6)

By (4), the rank3 parts in the first two endpoint columns of this row are
-u a² q10 a and -u a² q11 a. All other words have at most two A factors.
Both expressions vanish. Since the block row[q10,q11] of the unit Q_A is
surjective, their vanishing implies u a²=0, hence u=0. C's last row is now
(0,f,0), so f is a unit.

The first endpoint column in that last row is now

    f a q10 a+f a q11.                                (7)

By (5), its rank1 projection is exactly f a q11. But im(E1) is the middle
output bank, so this bottom-row projection is zero. Thus q11=0.
The rank3 part of the entire endpoint input column1 is consequently

    V a² q01 a.                                      (8)

Here (4) applies again, while the remaining W a q01 a and F q21 a have
at most two A factors. Since V is injective, (8) forces q01=0. The second
column of Q_A is now zero, contradicting invertibility. This proves the
whole-algebra exclusion.

## Consequences, surviving freedom and price

The hypotheses (1) include every coherent first interface
C=R(D_b^tensor V)diag(I,h,I), with arbitrary coherent unit R and arbitrary
ordinary unit h: its first two first-column blocks are functions of D_b,
and a D_b^tensor V=D_a^tensor V a. Therefore no such interface works with
any Q in the FULL square-normalizer algebra. This includes the diagonal,
dihedral, Boolean, spectator-switching and active-swap searches, and is
strictly broader than their finite catalogues. Nonconstant conditional
permutation first-column routing is also excluded for every ordinary Q
by (3), since s must be a unit.

The actual surviving possibilities in this native architecture are:
(a) at least one of C00,C10 fails clean forward transport; or
(b) Q uses ordinary operations outside O_K. In case(b), (3) still holds
and sharply reduces the first/second interface forms. A failed hypothesis
is not a positive caller. No claim excludes an arbitrary three-native
architecture or an arbitrary ordinary Q with a nonclean first column.

The native body remains3[1]+6[7]+3[8], against target[25]+[23]+[22]. This
negative theorem produces no endpoint, saving, new supplier or new kappa.
Any future construction still owes exact all-width endpoint gauges, paid
ordinary forward/inverse lowering, precision, source/owner and recursive
obligations. Credits include @CubeJerry, retained literal source, tensor
separation and Gaussian-component contributors, the root's square-class
proof and independent reviews, and Worker B with substantial OpenAI help.
