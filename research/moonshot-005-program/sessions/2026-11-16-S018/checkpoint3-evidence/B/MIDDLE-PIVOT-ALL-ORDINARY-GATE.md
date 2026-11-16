# A single middle first-column pivot excludes421 for every ordinary Q

**Universal fixed-template theorem, pending independent review. No caller or
new kappa.** The second interstage is unrestricted ordinary. The first
interstage's remaining blocks need not be coherent quarter controls,
triangular, monomial, commuting or in the source-square algebra.

## Statement

Use the literal four-bit a=A^tensor V, with admitted ranks1,2,3 for a,a²,a³,
and the actual natives

    L=[[a,0,0],[I,a,0],[0,0,I]],
    U=[[a,-a²,0],[0,a,0],[0,0,I]].

Let C,Q be arbitrary ordinary units with

    C=[[0,b,c],[t,d,e],[0,f,g]],
    a t a^-1 ordinary.                                    (1)

All blocks are fixed finite sums of tensor lifts of root-four monomials,
with every actual scalar phase retained. C-unit already forces t to be a
unit, because its first block column is(0,t,0). The one-block clean-forward
condition includes every unit t(D_b^tensor V), using a D_b^tensor V=D_a^tensor V a,
and the retained Boolean sign-table algebra. No transport assumption is
placed on any other block.

**Theorem.** E=L C U Q L cannot be ordinary-equivalent to independent heads
(4,2,1) at every sufficiently large faithful width. For each fixed finite
template there is a catalogue-dependent V0, and the contradiction holds at
every V>=V0 where the stipulated units and identity hold. This is not an
isolated-small-width gate.

## Proof

Literal multiplication gives

    L C U=
      [[0, a b a, a c],
       [a t a, -a t a²+b a+a d a, c+a e],
       [0, f a, g]].                                     (2)

Put j=a t a^-1, an ordinary unit. Thus a t a=j a² is a pure rank2 unit,
and a t a²=j a³ is a pure rank3 unit.

The final input block column2 is(2) times(q02,q12,q22)^T. Its only rank3
contribution is(0,-a t a² q12,0)^T. Every other word has at most two A factors,
hence support at most4, or known rank0,1,2. A rank3 Gaussian word has support8.
The target has no rank3 component, so the unit a t a² forces q12=0.

The ordinary part of this same input column is now(0,c q22,g q22)^T: the
first prefix term a t a q02 is rank2, while a c q22 and a e q22 are rank1.
The stacked operator[c;g] is injective. Indeed if c z=g z=0, then C sends
(-t^-1 e z,0,z)^T to0, so C-unit forces z=0. This argument neither divides
by sector projectors nor assumes block commutativity. The target's ordinary
component vanishes, hence q22=0.

The last block column of Q is now(q02,0,0)^T. Q-unit forces q02 to be a unit.
The entire last endpoint input column is therefore

    E[:,2]=(0,a t a q02,0)^T,                             (3)

which is pure rank2 and fills the middle output bank. Since the independent
target has rank(pi2(E))=D, the whole rank2 image is exactly that middle bank.

All rank4 contributions of E are confined to the SAME middle output bank.
The top output row in(2) has at most two A factors before Q L, so every word
in the final top output row has at most three A factors and support at most8.
The bottom output row has at most two A factors after Q L. Neither row can
contain a rank4 Gaussian word, whose one-column support is16. Ordinary
coefficients are expanded wordwise; no bound on the numerical support of
an arbitrary finite sum is asserted.

At a faithful width the target has no components except ranks1,2,4. Thus

    E=pi1(E)+pi2(E)+pi4(E).

The last two summands together have image contained in the D-dimensional
middle bank, while rank(pi1(E))=D. Consequently rank(E)<=2D. But E is a product
of units on three independent banks and has rank3D. This contradiction proves
the theorem. Equivalently the required independent rank2 and rank4 images
cannot both occupy the same output bank.

## Consequences and scope

This includes the entire residual C=R(D_b^tensor V)diag(I,h,I) class with
R first column(0,t,0), for ANY ordinary unit h, not only the old quarter
clock. Arbitrary idle coupling in the remaining first-interface blocks is
allowed, and Q can use the full ordinary algebra outside the complete
source-square normalizer. The provisional square-normalizer residual proof
is a weaker predecessor; its additional class hypotheses are unnecessary.

A source-square caller under the earlier coherent first-interface form must
use genuinely nonresidual first-column sector switching. More broadly, a
caller must change the first-column shape or its one-block clean-forward
condition, or change the native/endpoint architecture. A failed hypothesis
is not a positive caller. The complementary root stacked no-idle theorem
closes a different broad first-interface class; neither result is a full
three-native impossibility theorem.

Finite tensor separation is inherited for the complete fixed word catalogue,
including proposed ordinary endpoint encodings, at a catalogue-dependent V0.
All i^V phases and width residues are retained. The proof uses only necessary
component ranks and complete invertibility; it does not assume that those
component ranks alone would suffice for a positive endpoint factorization.

The exact Gaussian/body price remains3[1]+6[7]+3[8] against prospective target
[25]+[23]+[22]. No endpoint, saving, supplier admission or new kappa is provided.
All ordinary/compiler, precision, source/owner and recursive obligations
remain. Credit @CubeJerry and retained source/component/tensor contributors,
root's independent algebraic review, and Worker B with substantial OpenAI help.
