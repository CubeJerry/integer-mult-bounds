# Independent review: pure-prefix image gate and a complete aligned rank-four component

Root independently accepts the scoped universal proof in
`B/PURE-PREFIX-IMAGE-GATE-v2.md`. This review uses the retained source and
inverse-cut tensor-word framework. It does not infer an all-width theorem
from a numerical rank test or from an unsuccessful caller search.

For C=[[s,b,c],[t,d,e],[u,f,g]], literal noncommuting multiplication gives
LCU=[K+Wa,-Ka-Wa²+Z,F], with K=(asa,ata,0), W=(0,s,u),
Z=(aba,ba+ada,fa), F=(ac,c+ae,g). Assume K is pure Gaussian rank2,
Ka is pure rank3, and Ka[q10a,q11a,0] is pure rank4 in the fixed faithful
catalogue. Every other term contains at most three source factors. A required
rank-D fourth component therefore has image exactly im(K), and K is injective.
The last input column has rank3 part -Ka q12, forcing q12=0. Its rank2 part
Kq02 lies in im(K); direct rank2/rank4 images force q02=0. Q is a unit, so
q22 is a unit. Its ordinary last-column part then forces c=g=0, and C-unit
forces e to be a unit. The last endpoint column fills the middle bank with
the rank1 image. Directness makes asa, hence s, injective and invertible:
a kernel vector would give a nonzero K-image in that middle bank. This
argument permits singular individual entries and noncommuting coefficients.

The top/bottom projection is [M,0], with
M=diag(a,I) B U_A Q_A L_A and B=[[s,b],[u,f]] a unit. The fourth-rank output
image projects onto the entire top bank and zero bottom. Choose its ordinary
endpoint column v. Applying the inverse two-source prefix gives the retained
F2/F1 cut contradiction: the left terms before the rank4 Gaussian have inverse
degree at most2 and hence source support at least4; the right lies in F1.
Faithful tensor separation prohibits a nonzero selected column. Ordinary
coefficient inverses remain inside the finite-dimensional unital algebra
when ambient-invertible, by injectivity/surjectivity of left multiplication;
this algebraic fact is not an uncharged physical inverse recipe. The result
is confined to the stated template and pure-prefix assumptions.

The separate bounded Gaussian-integer engine checks all2048 words
A Dc^j A² g A, j=0,1,2,3 and g in the actual512 group, as rank4, and all
eight associated rank2/rank3 prefixes. It checks the literal Db-to-Da
transport. This exhausts the generator hypotheses of the coefficient-algebra
instance; the preceding proof supplies arbitrary coefficients and all widths.

## Positive aligned component, followed by a scoped completion obstruction

Set F=Da², H=A^-2 F A², P=(I+F)/2, T=(I+H)/2, S=SWAP_ab,
Fhat=A F A^-1, Fback=A^-1 H A, Phat=(I+Fhat)/2,
Pback=(I+Fback)/2. All three displayed involutions are literal monomials.
Let K=A J A² S A^-3. Independently reconstructed exact tables give
K:(a,b,c,d)->(a,b xor ad,c xor ad,d) with phase(-1)^(ad),
and K commutes with Fhat. With B2=A³ S A, exact multiplicative identities are
A J A³=K B2, B2 Fback=Fhat B2 and A4 Fback=Fhat A4; B2 has rank2.
These literal one-column product identities tensor at every width.

Choose ordinary units C=diag(I,J,I) S_P and
Q=diag(I,S,I) S_T diag(I,S^-1,I), where S_P is the controlled swap of banks0/1.
Their first column/second row are respectively(I-P,JP,0)^T and(ST,I-T,0).
The entire quartic prefix has only two nonzero blocks:
(0,1)=-(I-Phat) A4 and(1,0)=-Phat K A4. The putative rank2 cross channels
vanish by the two intertwiners. The output unit
S_Phat diag(I,K^-1,I) and input unit S_Pback reduce this to the single
(0,1) block -A4, of full dimension D. Thus this is a real exact aligned
rank-four component; it is not an independent421 endpoint. Its K-column is
pure rank2, its next prefix pure rank3, and its quartic term pure rank4,
so the universal pure-prefix gate excludes every independent421 completion
with this fixed first column and active second-interface row.

## Actual ordinary controls and their charges

For an involution F and P=(I+F)/2,
S_P=diag(I,-F) E01(P) E10(-P) E01(P). The JSON lists actual execution
order. Each shear ±P uses SCALE(source,±1/2), ADD, MONO(F), ADD,
MONO(F^-1), SCALE(source,±2), restoring the source. The final -F is a MONO(F)
followed by external SCALE(-1). External signs and halves are never absorbed
into a one-column phase: doing that would tensor an unwanted width-dependent
sign. All monomial tables, their destinations and quarter phases are explicit.

`ORDINARY-WORDS.json` contains C,C^-1,Q,Q^-1 and the two decoders and their
inverses. Every word uses6 ADD and7 SCALE; C and its inverse use8 MONO,
Q and its inverse9, the output decoder/inverse8, the input decoder/inverse7.
All have maximum-bank prefix norm bounded by5 through a direct triangle
bound. Both inverse identities are verified exactly;48 single-ADD omissions
change the advertised operator. No owned auxiliary field is introduced.
Each operation acts on a complete field and remains charged. These limited
ordinary controls do not discharge native all-columns, compiler, erasure,
precision, analytic recovery, supplier or recursive accounting obligations.

All-width validity of these controls follows from the involution/projector
algebra and the exact multiplicative identities, not by tensoring a sum of
one-column matrices. The exact one-column replay is an independent error
control. Credit @CubeJerry, the retained native and tensor-word frameworks,
B's pure-prefix theorem and selective alignment, and OpenAI-assisted root
review and literal primitive lowering. No new kappa.
