# A characteristic/reserve obstruction in the published interchanger

Status: **proved within the specified source construction**. This is not a
lower bound on arbitrary interchangers, Walsh transforms or multiplication.
It explains why the compact characteristic-zero count predictor cannot be
ported to the source interchanger merely by choosing a larger data characteristic.

Source pin: OpenAI `math` `3344da59991ed94f9ba711217b29c1d760badfa6`.
The relevant tape file is `build/interchange.tex`: the label family,
Equation `eq:interchange-gram`, Section `subsec:swap-spectrum`, and
Equation `eq:interchange-contraction`. The count window is in the Fourier
file `build/repair.tex`, Section `sec:repair`, Lemma `lem:count-predict`.
The concurrent programme's characteristic-zero alternative is
`routes/A/compact-complex-predictor.md` at `bbfd1086b7e629375f9891998e4602270d8801cd`.

## 1. Precise statement

Let p>=3 be an odd prime, q>=2, h=2p-1. Retain the source's labels
V=([q]^h)^h. For labels v,w, let k(v,w) count outer coordinates whose
inner words have Hamming distance exactly p. Let G be the rational symmetric
matrix with a two-by-two block for each ordered label pair,

    G[v,w]=(1-k(v,w)/p) I_2 + (k(v,w)/p) S,
    S=[[0,1],[1,0]],

and let D=rank_Q(G), the dimension after quotienting by the radical.
Then

    D >= 2^(2p-1)+1.                                         (1)

Consequently, with a=D-2, if the source's strict recursive inequality

    2 m^gamma + 2a < m^alpha,     1/2<gamma<alpha<=1           (2)

holds, then

    2^(2p)-2 < m^alpha <= m,      p < sqrt(m).                (3)

For the binary repair window of the source, intersected with counts 0,...,m,
its integer width is at least sqrt(m). Therefore it contains two counts
c and c+p. They have the same value in every field of characteristic p but
opposite parity. No scalar predictor depending only on the field-valued
count can agree with the required parity throughout the source window.

This includes polynomial and everywhere-defined rational functions of that
count, and scalar expressions over any finite extension of F_p. It does not
include the source's multivariate integral predictor, which retains the
individual query indicators, or arbitrary row-mixing matrix pencils.

## 2. A full-rank binary submatrix of the address Gram form

Choose two letters in [q]. For x in {0,1}^h let v_x be the label whose first
inner word is x and whose other h-1 inner words are one fixed word. Thus
k(v_x,v_y) is the indicator of d_H(x,y)=p. Let A be the adjacency matrix of
the distance-p graph on {0,1}^h, of order M=2^h. The corresponding principal
block submatrix of G becomes, after the invertible change from each pair to
its sum and difference coordinates,

    J_M  direct-sum  (J_M-(2/p)A),                            (4)

up to nonzero scalar factors. Here J_M is the all-ones matrix. It remains
to show that B=J_M-(2/p)A is invertible over Q. Then (4) has rank M+1,
and the full G has at least this rank.

For S subset {1,...,h}, the character chi_S(x)=(-1)^(sum_{i in S} x_i)
is an eigenvector of A. Its eigenvalue depends only on t=|S| and is

    K_p(t) = sum_r (-1)^r binom(t,r) binom(h-t,p-r).

Double-counting the intersection of a t-set and a p-set gives

    binom(h,t) K_p(t) = binom(h,p) K_t(p).                    (5)

Since h=2p-1, the generating polynomial for the right-hand factor is

    sum_t K_t(p) z^t
       = (1-z)^p(1+z)^(p-1)
       = (1-z)(1-z^2)^(p-1).

Hence, for 0<=r<=p-1,

    K_(2r)(p)   = (-1)^r binom(p-1,r),
    K_(2r+1)(p) = (-1)^(r+1) binom(p-1,r).

Every coefficient is nonzero, so every K_p(t) is nonzero by (5).
The characters form a rational basis: their matrix has product with its
transpose equal to M I_M. On nonconstant characters, B has eigenvalue
-(2/p)K_p(t), which is nonzero. On the constant character its eigenvalue is

    M-(2/p)binom(h,p) > 0,

because binom(h,p)<=M and 2/p<1. Thus B is invertible. This proves (1).
No estimate of the source's unspecified O_p constants was used.

## 3. The characteristic cannot be raised past the window

Equation (1) gives a>=2^(2p-1)-1. Dropping the positive first term in (2)
yields 2^(2p)-2<m^alpha<=m. For p>=3, 4^p-2>p^2, so p<sqrt(m).
The stronger direct restriction is

    p < (1/2) log2(m^alpha+2).                              (6)

The source's binary window has r=ceil(log2(2m)),
B0=ceil(sqrt(2mr)), u=floor(m/2-B0), v=ceil(m/2+B0).
Let I=[max(0,u),min(m,v)] intersect Z, with integer width w.
If m is even, w=min(m,2B0); if m is odd, w=min(m,2B0+1).
Thus w>=min(m,2sqrt(2mr))>=sqrt(m)>p. There are integers c,c+p in I.

On a row with shift beta, set

    C_beta=(m I-sum_j (-1)^beta_j Q_j)/2.

At a common frequency its eigenvalue is the Hamming count c, reduced
modulo p. The desired product multiplier is (-1)^(c-|beta|).
The source spectral-conversion paragraph explicitly supplies every sign
pattern, so both relevant counts occur. Since p is odd,

    c = c+p in F_p,        (-1)^(c+p)=-(-1)^c.

The two required values are distinct in characteristic p. Any scalar
function of C_beta alone assigns them the same value, a contradiction.
Extending the field does not separate equal prime-field elements.

The same conclusion holds for any alternative centered count window whose
effective integer width is at least sqrt(m), including the concurrent S002
t-wise-independent compact window. Reducing the window enough to avoid this
argument would change the exceptional-fraction and repair budget and needs a
new analysis; it is not covered by the existing rare-exception guarantee.

## 4. Consequence for quantitative research

The characteristic-zero Newton polynomial can be evaluated from one rational
count because it distinguishes all integer counts in its window. Its factorial
denominators cannot simply be reduced modulo p when the window reaches p.
The obstruction is stronger than this denominator observation: no replacement
scalar function of the reduced count can work under (2).

The original integral interpolation avoids the obstruction by constructing
binomial-count data from separate query indicators before specialization.
Those multivariate values need not be functions of c modulo p. They retain
information which a single field count loses.

Therefore a small characteristic-zero predictor for the numerical Walsh part
does not by itself remove the interchanger's template cost. A successful
transfer must change at least one of: the count representation, the label/Gram
construction and reserve recursion, the rare-exception contract, or the actual
tape mechanism. This is a concrete reason to preserve the independent routes.

## Verification and open next questions

The proof above is algebraic and applies for all stated parameters. A finite
verifier separately checks spectral identities, complete finite cube spectra,
window formulas and aliasing witnesses; these checks do not prove the theorem.
Independent Route C algebraic re-derivation found no blocking issue; see
[review](route-c/ROOT-OBSTRUCTION-REVIEW.md). The exact finite checks passed;
see [receipt](verification-obstruction.json) and run
`python3 -I -B research/moonshot-overhead-program/results/epsilon-uniformity/verify_obstruction.py`.
No Lean build
or full source-kernel replay is claimed.

Can a compact representation of higher integer count digits or divided powers
preserve the information required in characteristic p without the source's
large Clifford enlargement? Can the label construction achieve a smaller
rational Gram rank while retaining the required rectangle and rank fractions?
These are distinct, falsifiable next obligations; neither is assumed here.

Credits: OpenAI source construction and its cited intersection/Clifford lineage;
standard Fourier characters of the binary cube and Krawtchouk identities;
@CubeJerry's programme and concurrent S002 predictor. Proof developed with
OpenAI GPT-6 Astra Pro assistance. Novelty beyond this specific source
application has not been established by a comprehensive literature search.
