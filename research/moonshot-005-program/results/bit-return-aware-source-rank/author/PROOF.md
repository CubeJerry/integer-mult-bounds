# Exact return-rank optimization for one source in a fixed common word

**Proved linear algebra interface. It is not a global source optimization
or a new multiplication exponent.** The previous source-mask theorem
minimizes the information rank of a proper contribution. The replacement
return depends instead on the full fitting I+B. This result optimizes
that rank when one donor's early and late source maps vary and every
other donor and every downstream operation stays fixed.

## 1. Quantified theorem

Let F be any field, let b,m,l be nonnegative integers with m<=b, and fix
matrices with a common output space Y:

    M0:Y <- F^c,  A:Y <- F^b,
    C:Y <- F^m,   D:Y <- F^l.

Choose F0:F^b->F^m of full row rank m and an arbitrary L:F^b->F^l.
The full matrix to be completed is

    M(F0,L) = [ M0 | A+C F0+D L ].                    (1)

Put W=im[M0 D], and define exact integers

    a = rank[M0 D A] - rank[M0 D],
    r = rank[M0 D C] - rank[M0 D],
    z = rank[M0 D C A] - rank[M0 D C].

Then

    min_(rank F0=m, L arbitrary) rank M(F0,L)
       = rank M0 + z + max(0,r-a).                   (2)

Every minimum in (2) is attained over the original field. A finite
Gaussian-elimination construction supplies the source maps. If m>b,
there is no admissible F0 and no minimum is asserted. Empty input, early,
late or fixed-column spaces are covered by the same formula.

In a fixed native word, M0 contains all other donor columns of I+B, A is
the unchanged identity embedding and any fixed contribution for this
donor, and C,D are its actual full-output early and late transfer maps.
All original outputs, including undesignated side outputs, belong to Y.
Completion owners whose downstream response is not zero must also be
included. Separate per-receiver C,D choices are not permitted.

## 2. Removing unrestricted late corrections legitimately

First quotient Y by im M0. The rank in (1) is rank M0 plus the rank of
the remaining b columns in that quotient. For a fixed F0, the late term
can add any column-wise vector in the image of D in this quotient.
Therefore the minimum over L equals the rank after further quotienting
by that D image.

For the upper bound, choose a linear section of the resulting quotient
restricted to the image of A+C F0. Its lifted columns have the same rank
as that quotient image. The difference from the actual columns lies in
im M0+im D; choose L to cancel the D part. The remaining im M0 part
does not affect the rank with M0 adjoined. The lower bound follows from
applying the quotient. This step preserves the actual fixed M0 columns;
it does not append D as a free return bank.

Write bars for maps into Y/W. We have reduced the problem to

    rank M0 + min_(rank F0=m) rank(Abar+Cbar F0).       (3)

Let V=im Cbar, of dimension r. As F0 ranges over the surjective maps to
F^m, the product G=Cbar F0 ranges over exactly all maps F^b->V with
image V. Necessity is immediate. Conversely, lift a surjective G through
a section of Cbar and use m-r independent source rows in ker Cbar to
complete the r independent quotient rows. This is possible because
m<=b, by the previously proved full-rank source lift; it uses no field
extension or new source dimension.

## 3. Minimum rank after adding a surjective map to V

We prove the more general elementary identity

    min_(im G=V) rank(Abar+G) = z+max(0,r-a),          (4)

where a=rank Abar and z=rank(proj_(Y/W)/V Abar).
Let K=ker(proj Abar), so dim K=b-z. The image Abar(K)=im Abar intersect V
has dimension t=a-z. For any H=Abar+G, its quotient modulo V is fixed,
so

    rank H = z+rank(H|K).

Let k=rank(H|K). The image of G|K lies in Abar(K)+H(K), of dimension at
most t+k. A complement of K has z dimensions, so all of im G has
dimension at most t+k+z=a+k. Since G is onto V, k>=r-a. Also k>=0.
This proves the lower bound in (4).

For attainment put k=max(0,r-a). Choose a basis of K whose first t vectors
map under Abar to a basis of T=im Abar intersect V and whose remaining
b-a vectors span ker Abar. Since r<=m<=b, k<=b-a. Choose k vectors in
V independent modulo T and let H send k of those kernel basis vectors
to them, sending every other vector of K to zero. Then

    G|K = H|K-Abar|K

has image of dimension t+k. Extend K by z domain vectors. The remaining
dimension needed to make G onto V is r-t-k<=z. Choose G on the complement
to fill that remaining space, setting unused complement images
arbitrarily. Now H=Abar+G has rank z+k because its restriction to K has
rank k and its quotient image has rank z. This proves (4) over every
field. The lift in section2 and late correction then attain (2).

Equivalently the contribution beyond rank M0 is max(z,r-t), with
t=dim(im Abar intersect V). The a,r,z formulation requires only ranks of
explicit concatenated matrices and avoids constructing quotient bases
merely to evaluate the screen.

## 4. What this permits in the programme

For any fixed downstream word and fixed other sources, formula (2) is an
exact best possible return rank under arbitrary full-rank early rows and
unrestricted available late parities at one donor. It is a useful
optimistic screen even if a prescribed endpoint imposes further equations:
dropping those equations enlarges the feasible set, so (2) is a lower
bound for the constrained problem. An attaining choice from this theorem
need not preserve a selected receiver target or the proposed B*.

If the quotient images of both C and D vanish modulo im M0, source
retuning cannot change this contribution to the return rank. Such
vanishing is a precise way to recognize a fixed interface with no useful
feedback through the other columns. It must be checked on the full actual
word, including residual source values on all side routes.

It is invalid to minimize each donor separately against different M0
matrices and then sum the improvements. Changing another donor changes
M0 and can change all quotient spaces. A local optimum is not a global
impossibility certificate. The statement also does not authorize arbitrary
changes to the physical transfer C,D, which must come from one common
shared H/D/K word with all causal and ownership conditions retained.

## 5. Controls and comparison with information-rank optimization

When M0=D=0 and C has full output image, (2) reduces to
min rank(A+C F0)=max(0,rank C-rank A). Taking A=0 instead gives rank C.
Thus minimizing the proper information rank and minimizing the completed
return can point in different directions. If A is invertible and C has
image dimension r, a full-rank source can cancel exactly r suitable
directions, leaving b-r. A selected proper target can forbid that choice.

More generally, with a=1,r=2,z=1 the minimum contribution is two, not
max(z,r-a)=one. The two requirements act on different parts of the domain:
the fixed quotient contributes one, and surjectivity requires a further
one on its kernel. This is a useful negative control for an incorrect
max-only formula.

The author finite checker enumerates full-rank source maps and every late
map on small binary and ternary matrices and compares the actual minima
against (2). It includes zero dimensions, rank-deficient C, nontrivial
fixed columns, and the preceding strict two-term example. Those finite
checks support the written arbitrary-field proof, not an asymptotic
algorithm claim. Independent review is recorded separately.

## 6. Cost and status

Only the source coefficients change. The inherited paid source compiler
applies if the resulting rows meet its actual source-owner interfaces;
the same field expansion, source snapshots, early inverse and genuine
late visits must be charged. Dense rank computations and coefficient
selection are finite algebraic procedures and are not a free online
oracle. Every downstream cost and complete recursive dependency remains.

This theorem does not itself lower the observed q of any native word.
Any such application needs the actual C,D,M0 and a check of all retained
target and physical constraints. No complete supplier, foundational
discharge, global rank minimum or new kappa is claimed.

Credit @CubeJerry, Worker B's fixed-transfer source-mask theorem and
minimum-information-rank proof, the actual shared-K word authors, and the
retained replacement-return interface. Root developed this return-aware
extension with substantial OpenAI assistance.
