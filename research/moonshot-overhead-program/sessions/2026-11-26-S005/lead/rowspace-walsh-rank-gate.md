# A Walsh child needs a constant fraction of cross-orbit rank

Status: **new written scoped theorem; independent review requested**.
This is a test of the row-space layout proposal, not a lower bound on tape
time or multiplication. The numerical data field is the real or complex
numbers; binary vectors below are addresses. No complete overhead bound
changes.

## 1. The proposed representation and its missing operation

Write an address as an A-by-f binary matrix X, with A complete registers
of f bits each. A source column reindexing applies the same invertible
binary matrix g to every column: X maps to gX. Its orbits are exactly the
row spaces W of X. Thus an orbit layout can place all such address changes
inside blocks of size at most 2^(A^2), independent of f. Discovery's separate
orbit compiler investigates that useful observation and prices its missing
layout conversion.

A recursive numerical child applies a normalized f-bit Walsh transform to
one register while leaving the other registers fixed. It does not preserve
these row-space blocks. The question here is stronger than whether there is
one escaping entry: can an arbitrary orbit-preserving processor perform the
child up to a low-rank correction?

The answer is no for any correction of rank below a fixed positive fraction
of the entire input dimension. This rules out an exceptional small-rank
repair of this operation in the proposed layout. It does not rule out a
fully priced cross-orbit transform.

## 2. Precise statement

Let 2 <= A <= f, N=2^(Af), and R>=1. The physical array contains R
independent copies of every matrix X in F2^(A by f). Let H act on the first
row x of X by

    (H z)(y,B)=2^(-f/2) sum_x (-1)^(x dot y) z(x,B),       (RG1)

where B denotes the other A-1 rows. The operator on all copies is I_R
tensor H. Write it simply as H below.

For every binary row space W, let E_W contain all records with row space W,
including all R copies. Let D be any linear operator satisfying
D(E_W) subset E_W for every W. It may be dense and singular, and may mix
the independent copies without restriction inside each block.

Define

    alpha_A = product_(j=2)^A (1-2^(-j)),
    beta_A  = alpha_A (3*2^(A-1)-1)/(4*(2^A-1)).          (RG2)

**Theorem RG.** If E is any linear operator of rank less than
R N beta_A, then

    ||H-D-E||_2 >= 1/sqrt(2).                           (RG3)

In particular an exact representation H=D+E requires

    rank E >= R N beta_A > 3 R N / 16.                  (RG4)

The integer R N beta_A is the exact rank of the cross-block matrix used
in the proof. For A=2,3 it equals respectively 5 R N/16 and 33 R N/128.
The bound is uniform in f and in the number of independent rows R.

This theorem allows every orbit-local linear algorithm for free. It is
therefore stronger than a statement about a specified list of register
permutations. It still has the essential orbit-local plus low-rank premise.

## 3. An orbit-invariant separator

Let P_1 project onto addresses for which the first A columns of X have
determinant 1 over F2, and put P_0=I-P_1. For any g in GL_A(F2),

    det((gX)_[first A columns])=det(g)det(X_[first A columns])
                              =det(X_[first A columns]), (RG5)

since every nonzero binary determinant equals 1. This predicate is
constant on each row-space orbit. Hence P_0 D P_1=0 for every permitted D.

Fix B. Let B_0 be its (A-1)-by-A restriction to the first A columns. If
rank B_0<A-1, the determinant is zero for every first row, so this fibre
contributes nothing to P_0 H P_1. Otherwise there is a unique nonzero
cofactor vector c in F2^A such that the determinant is c dot x_[first A].
Extend c by zero to F2^f. On this fibre, the cross-block operator is the
normalized character matrix with rows c dot y=0 and columns c dot x=1.

## 4. Exact rank and singular values of the halfspace block

Put Q=2^f and U=c^perp. Its size is Q/2. Pick v with c dot v=1; the
column set is v+U. After a diagonal row sign, the unnormalized cross-block
matrix is

    M_(y,h)=(-1)^(y dot h),  y,h in U.                   (RG6)

The radical of the dot product restricted to U is U intersect span(c).
It has size t=1 if c dot c=1 and t=2 if c dot c=0. Character orthogonality
gives

    (M M^*)_(y,z) = |U| [y+z lies in rad(U)].            (RG7)

Each radical coset contributes one nonzero singular value squared equal
to |U| t. Therefore

    rank M = |U|/t;
    all nonzero singular values of Q^(-1/2)M are sqrt(t/2).
                                                               (RG8)

They are 1/sqrt(2) in the nonisotropic case and 1 in the isotropic case.
The rank is respectively Q/2 or Q/4. This calculation also accounts for
the possible degeneracy of the binary dot product on the hyperplane.

## 5. Count all full physical fibres

There are

    product_(i=0)^(A-2) (2^A-2^i)

ordered independent (A-1)-tuples in F2^A. The remaining columns of B are
arbitrary. Thus a fraction alpha_A of all B have rank B_0=A-1.
For these tuples, the cofactor vector is uniformly distributed over the
2^A-1 nonzero vectors: every hyperplane has the same number of ordered
bases. Exactly 2^(A-1) nonzero c have c dot c=1, and 2^(A-1)-1 have
c dot c=0.

Summing the direct-sum fibre ranks from RG8, then including all R copies,
gives

    rank(P_0 H P_1)
      = R 2^((A-1)f) alpha_A
          [2^(A-1) Q/2 + (2^(A-1)-1) Q/4]/(2^A-1)
      = R N beta_A.                                    (RG9)

Every nonzero singular value is at least 1/sqrt(2), because the fibres
are mutually orthogonal coordinate subspaces. Also

    alpha_A >= 1-sum_(j=2)^A 2^(-j) = 1/2+2^(-A)>1/2,
    (3*2^(A-1)-1)/(4*(2^A-1))>3/8.

Consequently beta_A>3/16. These loose uniform constants are sufficient
for the representation decision; no optimality is claimed.

## 6. Low-rank repair and approximation

Set M=P_0 H P_1 and E'=P_0 E P_1. Its rank is at most rank E. If this
is smaller than rank M, the nonzero right singular subspace of M contains
a unit vector v killed by E'. On that subspace, RG8--RG9 imply
||M v||>=1/sqrt(2). Therefore

    ||H-D-E|| >= ||P_0(H-D-E)P_1||
                = ||M-E'|| >= 1/sqrt(2).

This proves RG3 and RG4 with no assumption about the norm or conditioning
of D or E. For a differently scaled Walsh target, both sides scale by
that normalization. The source child is normalized as in RG1.

## 7. Consequence for the programme and open questions

The finite column-reindexing compiler and this obstruction concern
different operations. Orbit layouts can make the former local, while a
single actual Fourier child requires substantial interaction between
orbits. The missing interaction cannot be relegated to a correction of
vanishing relative rank. A complete improved numerical recurrence must
charge it as productive work.

This does not lower-bound the time of that interaction, forbid a new
orbit-aware Fourier algorithm, or contradict the source's different
spectral repair mechanism. A rank fraction is not a bit-volume invoice.
It does not rule out joint cancellation across a whole pencil that never
isolates this child. Arbitrary initialized workspace or a change of layout
may be useful, but must be included in the actual supplier contract.

The next constructive question is a full-rate transform between adjacent
row-space fibres, with charged forward and inverse layout maps. For a
fixed B of rank r, replacing its first row traverses the one-dimensional
extensions of span(B); this suggests an incidence/fibre algorithm, rather
than an exceptional-error correction. No such fast physical algorithm is
asserted here.

## Verification and credit

`verify_rowspace_walsh_rank.py` supplies exact finite checks of the
determinant separator, character Gram identity, cofactor counts, rank
fraction and omitted-premise controls. The written proof above establishes
the unbounded family. A numerical singular-value computation is unnecessary.
Independent review and the actual replay receipt are recorded separately.

Source context: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`,
Fourier `build/binary.tex` and tape `build/walsh.tex`; AQ/NW's complete
spectator/selected-bit interface. The new row-space compiler is S005
Route A's protected discovery. This rank test was developed independently
by the S005 lead for Jerry Chen (@CubeJerry), with substantial ChatGPT
assistance. The determinant and character-orthogonality ingredients are
standard; no broad literature-priority, formal-kernel or runtime claim.
