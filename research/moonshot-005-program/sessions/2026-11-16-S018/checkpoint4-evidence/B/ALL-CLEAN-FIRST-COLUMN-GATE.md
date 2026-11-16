# Every clean first-column block excludes421 for arbitrary ordinary Q

**Universal fixed-template extension, pending independent review. No caller.**
Use the scope, literal natives and component-image normal-form theorem in
CLEAN-FIRST-COLUMN-SQUARE-GATE-v1.md. This extension places NO restriction
on Q's ordinary algebra. It instead adds clean forward transport of C20.

## Theorem

Let C=[[s,b,c],[t,d,e],[u,f,g]] and Q be arbitrary ordinary units. Assume

    a s a^-1, a t a^-1, a u a^-1 are ordinary.           (1)

Then L C U Q L cannot be ordinary-equivalent to independent Gaussian
heads(4,2,1), for a fixed finite template valid at all sufficiently large
faithful widths. The threshold V0 depends on the complete finite word
catalogue. No isolated small-width assertion is made. All actual phases
and width residues are retained.

In particular this excludes EVERY coherent first interface
R(D_b^tensor V)diag(I,h,I), for every ordinary unit h and every ordinary
second interface Q. There is no diagonal, square-normalizer, commutativity,
monomiality, triangularity or no-idle assumption on Q or the remaining
first-interface blocks.

## Proof

Write shat=a s a^-1, that=a t a^-1, uhat=a u a^-1. The already proved
necessary normal form gives

    c=g=q02=q12=0; s,e,q22 and Q_A are units,
    V=(shat,that,0)^T,
    im(pi4(E))=im(V), im(pi1(E))=middle output bank.      (2)

The last output row E_bottom consequently has ONLY rank2: neither the
rank1 nor the rank4 image has a bottom component, and the endpoint has no
other components. Hence a E_bottom has support filtration degree at most3,
so pi4(a E_bottom)=0. This follows by writing the pure rank2 component
in its ordinary Gaussian bimodule; multiplication by a rank1 word raises
its support degree by at most1. It does not assume that all degree3 words
are Gaussian.

From the exact bottom prefix [u a,-u a²+f a,0], the ONLY rank4-capable terms
in a E_bottom are

    -a u a² [q10,q11] diag(a,a)
       =-uhat a³ [q10,q11] diag(a,a).                   (3)

All remaining terms have at most three A factors. Define

    X=[pi4(a³ q10 a),pi4(a³ q11 a)].

Since uhat is ordinary, (3) implies uhat X=0. The top row of pi4(E) is
-shat X. Rank(pi4(E))=D and the unit shat imply rank(X)=D; thus X is
surjective and uhat=0, hence u=0. C's bottom row is now(0,f,0), so f is a unit.

The first endpoint column in the bottom row becomes

    f a q10 a+f a q11.                                (4)

Its rank1 projection vanishes. Ordinary multiplication commutes with that
projection and f is invertible, hence

    pi1(a q10 a)+a q11=0.                             (5)

The finite projective word sets a H a and a H are disjoint: an equality
a h a=lambda a k with ordinary monomials h,k would make a=lambda h^-1 k
monomial. Therefore projection onto the ordinary left coset a O annihilates
every selected word in pi1(a q10 a), and fixes a q11. Finite tensor
separation with all phases retained applies to this coset projection just
as in the admitted two-native ordinary-coset proof. Equation(5) forces
q11=0. No source-square property was used.

The entire endpoint input column1 is now

    E[:,1]=(V a²+W a)q01 a+F q21 a,
    W=(0,s,0)^T, F=(0,a e,0)^T.                       (6)

Its bottom component is zero, and its top component is shat a² q01 a.
Every word in(6) has at most three A factors, so its rank4 projection is
zero. The top and middle output banks together equal
im(pi4(E)) plus im(pi1(E)), because shat is a unit. Since the three
component images form a direct sum, the rank2 part of(6), which also has
zero bottom component, must vanish. Thus(6) has only rank1 image, entirely
in the middle bank. Its top component is zero; the units shat and a force
q01=0. Together q01=q11=0 contradict the unit Q_A. This proves the theorem.

## Surviving construction freedom

The complete-square-algebra gate still allows C20 to be nonclean, whereas
this extension allows Q to be arbitrary but requires all three first-column
blocks to be clean. Their union is useful: within the normal form having
clean C00,C10, any candidate must have nonclean C20 AND Q outside the entire
source-square algebra. A minimal still-open shape is

    C=[[I,0,0],[0,0,I],[h,I,0]],

with h an ordinary clock whose a h a^-1 is nonordinary, together with an
ordinary Q outside the square algebra. This is an invertible genuinely
idle-coupled interface. Its existence is not a caller or a saving.

The body price and all positive construction obligations remain unchanged:
3[1]+6[7]+3[8] against[25]+[23]+[22], exact independent endpoint gauges,
all-width phases, paid forward/inverse ordinary lowering, precision,
source/owner and recursive foundations. Credit @CubeJerry and retained
source, tensor separation, ordinary-coset and component arguments, the
root's independent contributions, and Worker B with substantial OpenAI help.
