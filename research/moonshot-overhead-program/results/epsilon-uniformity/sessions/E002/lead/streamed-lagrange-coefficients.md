# Optional streamed Lagrange repair coefficients over a small finite field

Status: complete algebraic component, independent review pending. This is
an optional alternative to grouping all small check roles into a payload
block. It is not an additional premise of the fixed-family Theorem P.

Let E be a finite field of characteristic two and order q. Fix B distinct
nodes a_0,...,a_(B-1) in E and an integer s with 0<=s<q-1. A spectral
address specifies a containing defect set J subset [B], |J|<=s, predictor
values p_j and a target z, with p_j=z outside J. Assume all discrepancies
g_j=p_j-z lie in the embedded F4, so g_j^3=1 whenever g_j is nonzero.
Set H_(i,j)=a_j^i for 0<=i<s. Input check vectors are a=HX and b=HPX.
All entries of X are arbitrary in E; zero discrepancies inside J are allowed.

## 1. Coefficients without storing a Vandermonde inverse

For j in J define

    L_j(T)= product_(t in J, t!=j) (T-a_t)/(a_j-a_t),

and set L_j=0 for j outside J. Write lambda_(j,i)=[T^i]L_j, taking
lambda_(j,i)=0 when i>=|J|. Every denominator displayed is nonzero.

**Lemma SL1.** For 0<=i<s,

    lambda_(j,i) = sum_(t in E*, t!=0) t^(q-1-i) L_j(t).       (SL1)

(The redundant t!=0 emphasizes that the sum is over the multiplicative
group.) In particular every coefficient can be computed by a polynomial
number of field operations in B+q, with a constant number of field
accumulators, O(log(B+q)) counter bits and repeated access to the membership
predicate of J. No |J|-by-|J| matrix needs to be stored.

Proof. Each L_j has degree at most s-1<q-2. For exponents r,i in [0,s-1],
character orthogonality on E* gives sum_t t^(r-i)=0 unless r=i. The only
multiple of q-1 in the interval (-(q-1),q-1) is zero. If r=i, the sum
is q-1 as a field element, which is one in characteristic two. Multiplying
by t^(q-1) changes nothing. Expand L_j and apply these identities. To
compute L_j(t), scan all B nodes, test membership, and multiply the
appropriate factors and their inverses. Finite-field inversion and powers
use polynomial bit cost in log q. Reuse the same accumulators for the
outer sum. The tests can be repeated; storage, rather than time, is being
minimized here. QED.

## 2. The whole small repair map

**Lemma SL2.** Set delta_i=b_i-z a_i for 0<=i<s and

    y_l = sum_(j in [B]) sum_(i=0 to s-1)
              lambda_(j,l) g_j^2 lambda_(j,i) delta_i,
                       0<=l<s.                              (SL2)

Then with Z=H^T y,

    PX + PZ + zZ = zX.                                    (SL3)

Proof. For ell=|J|>0 let V be the ell-by-ell submatrix of the first ell
rows of H restricted to J. The interpolation polynomials have
L_j(a_t)=1_(j=t), hence (V^-1)_(j,i)=lambda_(j,i). The entries above
ell are zero. Since (P-zI)X is supported on J,

    e_j = sum_i lambda_(j,i) delta_i = g_j X_j.

SL2 is exactly y=(V^T)^-1 diag(g_j^2) e, padded by zeros. It follows
that Z_j=g_j^3 X_j on J. If g_j!=0 this is X_j, and if g_j=0 the desired
correction is zero anyway. Thus (p_j-z)(X_j+Z_j)=0 on J and outside it.
Characteristic two turns this into SL3. If ell=0 all sums are empty and
PX=zX already. QED.

For the E002 shift construction, B=Theta(m), s=floor(B/32), and one may
choose q=4^ceil(log_4 B), so B<=q<4B. All field-operation loop counts in
SL1--SL2 are polynomial m. Field elements, role counters and count state
have O(log m) bits. This gives a low-storage evaluator even if a containing
set includes a zero gap: no discrepancy is inverted.

## 3. Physical qualification

SL1 is an algebraic/streaming-memory lemma, not an oracle for spectral bits.
To use it on tape, the source comparison scans must supply the membership
predicate at the actual converter output layout. A complete comparison
can be generated as three consecutive runs per complete target fibre,
with arbitrary spectator prefixes advanced amortizedly. A shift count is
then accumulated by sequentially repeating these scans over m pairs.
One can retain O(log m) count bits and a constant number of E accumulators
per spatial payload location, rather than the whole list of m labels.

Each role input/output is copied or accumulated by an actual aligned role
scan. All B,s,q loop ranges are polynomial m. Formula SL2 may therefore
be evaluated with polynomial-m scans and only a constant number of such
accumulator streams, provided the small role alignment is implemented and
all temporary streams are removed before paid recursive calls. The
pointwise accumulation uses bit width O(log m) and is exact. One reused
polynomial-size coefficient buffer is additive workspace, not one buffer
per spatial location.

The stronger full variable-arity space result still needs endpoint-array
storage, leading-role grouping, field encoding and recursive parking.
In particular, enumerating an arbitrarily larger common root field would
replace q=poly(m) by its larger size in SL1. Use a local subfield of
polynomial size with a supplied embedding, or the grouped-role matrix
method, if that issue arises. The present lemma does not grant a free
embedding or an unbounded field enumeration.

Credits: standard finite-field character orthogonality and Lagrange
interpolation; E002 on-demand F4 repair; Jerry Chen (@CubeJerry);
AI-assisted low-storage derivation. No full tape execution is claimed.
