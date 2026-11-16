# Independent review of the finite cyclic conjugacy criterion

**Accepted as a necessary and sufficient construction theorem for the stated
cyclic P and bi-cyclic a-channel T interface.** The theorem does not decide
conjugacy in the full ordinary algebra, ordinary membership of the reconstructed
C, or existence of a profitable independent (4,2,1) endpoint.

## Universal source separation

For the literal A=C_b D_acd P, each input (a,b,c,d) has two nonzero outputs
(b,c xor epsilon,d,a), including their nonzero dyadic Gaussian coefficients.
For each of the four specified phase tables, the output/input phase-bit pair
takes all four values. Three tensor columns therefore realize every ordered
pair of counts s,t in {0,1,2,3}. Additional columns use the (0,0) witness.
Thus Pi_s a Pi_t is nonzero for every pair at every V>=3. Different ordered
blocks have disjoint input/output support. Their fixed scalar matrix
coefficients can be compared independently; no general tensor-word separation
theorem or finite-width extrapolation is needed for this particular step.

## Necessity and sufficiency

If Q=sum q_s tensor Pi_s is an ordinary cyclic unit with the required
conjugacies, then P_s=q_s^-1 E22 q_s and
M_st=-(q_s^-1 e0)(e1^T q_t). Stacking the four left and four right factors gives
one nonzero rank-one 12-by-12 matrix. Every block is nonzero. The kernel/image
relations and v_s u_s=0 follow from E22 e0=0, e1^T E22=0 and e1^T e0=0.

Conversely, a global factorization M=-u v with every block nonzero gives
nonzero u_s,v_s. The asserted flags put u_s in ker(P_s), v_s in the annihilator
of im(P_s), and v_s u_s=0. Choose a nonzero image vector w_s and a coordinate
with v_s e_j nonzero. Then z_s=(I-P_s)e_j/(v_s e_j) is in ker(P_s) and has
v_s z_s=1. Hence u_s,z_s are independent in that two-dimensional kernel and
w_s completes a basis. The matrix R_s with these columns is invertible and
q_s=R_s^-1 has exactly the required two conjugacy identities. Global rescaling
of u,v does not affect the existence conditions. Fourier interpolation supplies
fixed finite coefficients and an explicit inverse in the previously reviewed
cyclic ordinary family. The resulting spectral identities hold at every
positive width; V>=3 is used only to establish necessary coefficient equality.

The double Fourier transform of h_V^j a h_V^k has coefficient
i^(sj+tk) on channel (s,t); no negative sign or conjugation is missing. The
inverse transform has the factor 1/16 and the two negative exponents.

## False positives and physical boundary

With P_s=E22 and M_st=-c_st E01, where c is all ones except c33=3/2, each block
has rank one but the joint matrix has rank two. It cannot admit a cyclic Q.
The physical nonzero block a+(1/2)Pi3 a Pi3 is invertible: after factoring out
the unitary a, the perturbation norm is at most 1/2. Thus T still has rank D,
is square-zero and annihilates P in both orders. Those old operator tests do
not imply cyclic conjugacy. This does not exclude a noncyclic ordinary Q.

Likewise physical rank D of a cyclic projector does not force sector rank one.
For the balanced Boolean controls trace(h_V^2)=0 for every V>0, so the sum of
the even-sector dimensions equals the sum of the odd-sector dimensions.
Projector ranks (2,0,2,0) give physical rank D at every width while violating
the sectorwise conjugacy condition. This is an all-width counterexample.

## Independent evidence and remaining obligation

The root checker imports no author code. It independently factors the joint
matrix with a different normalization, constructs the basis and inverse,
checks all sixteen cross-sector equations for the author family and a separate
nontriangular complex family, and verifies both polynomial inverse products.
It reconstructs the literal 16-address source with all 32 nonzero coefficients
and all 64 width-three channel witnesses. Four deliberate invalid cases are
rejected. Exact finite checks accompany the universal argument above.

For an actual desired endpoint, one must still derive P,T in this restricted
form, satisfy the criterion, and prove C=F Q^-1 diag(a^-1,a^-1,I) ordinary with
its actual finite recipe and complete invoice. The C4 implementation gives Q
nonzero ordinary, scalar, precision and tape expenses; algebraic peeling does
not remove native/body/endpoint services. No complete supplier, global
foundation or new kappa is claimed. Source/proof pins appear in the package
dependency record and RESULT.json. Credit @CubeJerry, retained contributors,
Worker B and independent root review, with substantial OpenAI assistance.
