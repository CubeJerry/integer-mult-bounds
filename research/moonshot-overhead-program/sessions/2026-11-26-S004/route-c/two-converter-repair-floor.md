# Two-converter repair trees retain a positive normalized floor

Status: **proved restricted invoice theorem; independent review requested**.
This extends the concurrent E003 matrix-rank and recursive-port arguments
to its new order-five converter. It is not a lower bound for multitape
movement, interchange, or integer multiplication.

## 1. Provenance and the changed question

E003's `MATRIX-PREDICTION-RANK-BARRIER.md` proves the two-point matrix-rank
tail used below. Its `RECURSIVE-PORT-COST-FLOOR.md` treats repair ports
requiring q>2 target-transform calls; the order-three converter has q=4.
Its new `ORDER-FIVE-ONE-TRANSFORM-CONVERTER.md` constructs a converter with
q=2. These files were read at published programme commit
`df91e4c8e31b1020e05056db5b0eb16169ef3421`.

Simply substituting q=2 in the q>2 proof leaves a problem: the limiting
potential's infimum occurs at zero scaled predictor degree, where the
original even-m rank tail has a finite parity loss. Fixing one coordinate
when necessary removes that loss and gives an exact finite constant.

## 2. Exact invoice model

Fix m independent spectral coordinates, each with at least two distinct
nonzero field values. An exact node applies their product f, or its
inverse, to W independent rows. On every product of two-point local
restrictions, replacing its spectral-table ports by query-independent
reference maps gives an input-output matrix of Boolean degree at most t.
The node is charged at least Wt ordinary row-stages. This is E003's
explicit full-batch pricing premise; it does not price gates on smaller
subsets as full-batch stages.

If the port dimensions are h_1,...,h_s, each port is charged for two
sequential exact child calls on h_i rows with the same m coordinates.
Children may target f or its inverse. Degrees, widths, port counts and
finite branch depths may vary arbitrarily. Leaves have no ports and
cost at least m stages per row. Other costs are nonnegative. Intermediate
workspace may change size. The full-rate interface requires correctness
on arbitrary input rows even when the actual child inputs are correlated.

Write C_m(W) for the total row-stage invoice. This invoice is not equated
with tape running time or a lower bound on actual shared-pencil swap calls.

## 3. Parity-corrected rank tail

For n>=1 and 0<=t<n put

    delta_n(t)=2^-n sum_(j<=floor((n-t-1)/2)) binom(n,j).

E003 M1--M3 give total port width at least W delta_m(t). Fixing m-n
coordinates, applying that theorem to the remaining n, and averaging
the fixed values gives the stronger family

    sum_i h_i / W >= delta_n(t)             for every t<n<=m.  (T1)

Restriction cannot increase Boolean degree; fixed target factors are
nonzero scalars. For larger alphabets use E003's random two-point
restriction and endpoint averaging. The degree premise must hold on
these pair restrictions; affine-query constructions and support degree
supply it. Inverse targets also qualify.

Set v=floor(m/2) and define

    M*_m=binom(2v,v)/4^v,       A_m=1/M*_m.                    (T2)

For 0<=t<m choose n=m when m-t is odd, and n=m-1 otherwise. Always n>t
and n-t is odd. If M_n is the largest Bin(n,1/2) atom, symmetry gives

    delta_n(t)>=1/2-t M_n/2 >=1/2-t M*_m/2.                   (T3)

Indeed, for odd n, t is even and precisely t/2 whole atoms are removed
from the lower half. For even n, t is odd and the removed mass is half
the central atom plus (t-1)/2 whole atoms. Every such atom is at most
M_n. For even m, M_m=M_(m-1)=M*_m; for odd m>=3 both possible M_n are
at most M_(m-1)=M*_m. The case m=1 is immediate. Thus

    sum_i h_i / W >=1/2-t M*_m/2.                             (T4)

The zero-stage bound is W/2 exactly. The unrevised even-m tail gives
only `(1-M*_m)W/2`, insufficient at q=2.

## 4. Exact finite tree theorem

**Theorem T.** Every finite tree in Section 2 satisfies

    C_m(W)>=A_m W.                                            (T5)

The same holds for q>=2 children per port with the remaining interface
unchanged.

For m>=2, M*_m is the largest atom of Bin(m-1,1/2), a distribution on m
outcomes. Thus A_m<=m; also A_1=1. Leaves obey T5. Assuming the bound
for all children, an internal node costs at least

    Wt+2 A_m sum_i h_i.

For t>=m the local cost suffices. Otherwise T4 makes this at least

    W[t+2 A_m(1/2-t M*_m/2)]=A_m W.

Finite structural induction proves T5; no common depth or predictor is
required. Extra child calls and nonnegative costs preserve the bound.

Stirling gives

    A_m=[sqrt(pi/2)+o(1)] sqrt(m).

The normalized stage invoice therefore retains the constant
`sqrt(pi/2)=1.253314...` with two converter calls. E003's elementary
central-atom estimate also gives A_m>=sqrt(3(m-1)/2), hence

    C_m(W)>=(6/5) W sqrt(m)                  for every m>=25.  (T6)

The decimal is diagnostic; T2 and T5 are exact.

## 5. Sharpness of this scalar relaxation

For m>=2 and t=1, choose n to be the largest even integer at most m.
Then delta_n(1)=(1-M*_m)/2. A relaxed degree-one node costing one stage
per row and having two children with total mass 1-M*_m gives at depth d

    sum_(j=0)^(d-1)(1-M*_m)^j + m(1-M*_m)^d,

which tends to A_m. Sufficiently divisible root batch sizes make every
finite relaxed child width integral. Thus A_m is the best scalar
potential from these displayed corrected constraints. This does not
construct a predictor or physical caller attaining it.

The parity fix is essential: for even m, the original t=0 tail permits
false relaxed child mass 1-M*_m<1. Arbitrarily deep zero-cost internal
nodes would make the leaf invoice tend to zero. Restricting to m-1
coordinates rules out that escape.

The theorem answers the q=2 endpoint of E003's invoice model. It does not
rule out the order-five construction, smaller active-row pricing, changing
m during repair, sharing work across nodes, or a different converter
interface. Those mechanisms need their own accounting.

## 6. Lead composition: active-row pricing and inverse gates

The S004 lead derived the following distinct composition of Route C's
commutator theorem. It has a weaker constant but removes the full-batch
stage-pricing and polynomial-output requirements.

At each exact repair node use `inverse-query-commutator.md`'s network:
constant linear row maps, affine one-coordinate query matrices, their
everywhere-defined inverses, and spectral table ports. All gates preserve
one common spectral decomposition. Charge Q=sum h_j for actual active
query-row volume, counting every occurrence. If total port dimension is H,
charge two exact child target or inverse-target calls per port. Keep m
fixed throughout the finite tree. Arbitrary physical address permutations
are not granted as free constant row maps.

Let n be the largest odd integer at most m, and set

    kappa_n=2 binom(n,(n-1)/2)/2^n,    B_m=1/kappa_n.            (T7)

Fix one coordinate when m is even, apply the weighted two-point
commutator cut on n coordinates, and average all restrictions. Exactness
makes final error zero, and gives at each node

    kappa_n Q/W+2H/W>=1.                                     (T8)

Replacing a table's average rank by its port dimension only increases
the left side. Affine gates remain affine after restriction, and their
pointwise inverses stay defined. Inverse targets obey the same cut since
inverse local values are distinct and nonzero.

A leaf has Q>=B_m W. If all children obey this bound, their parent costs
at least Q+2 B_m H>=B_m W. Finite tree induction proves

    total active query-row volume >=B_m W,
    B_m=[sqrt(pi/8)+o(1)] sqrt(m).                            (T9)

For even m, B_m=A_m/2; for odd m, B_m=(m+1)A_m/(2m). This floor permits
inverse-affine gates and varying active subsets, unlike Theorem T's
polynomial full-batch premise. Its constant does not prove a normalized
loss above one. Neither invoice is a general tape-time lower bound.
Changing the common spectrum or sharing work across repair nodes changes
the model.

Attribution: the S004 lead proposed this recursive active-volume
composition; Route C independently checked it. The commutator premise
and weighted-basis provenance are in the companion note.

Credits: E003's weighted rank theorem, port telescoping, recursive potential
and order-five construction; the S004 parity-restriction extension and
finite q=2 induction; the OpenAI source; Jerry Chen (@CubeJerry);
substantial ChatGPT mathematical assistance. No priority claim is made.
