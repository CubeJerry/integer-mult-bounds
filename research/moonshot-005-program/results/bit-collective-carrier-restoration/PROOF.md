# Simultaneous restoration of released original carriers

**Working proof, not yet admitted.** This is an exact restoration interface,
not a movement saving or a complete BIT supplier.

## Proposition and proof

Let k be a field and x in k^h, r in k^m be independent original inputs.
At one actual chart, the h original records to be restored contain
z=A x+B r; other original records contain raw r; and q retained records
contain s=C x+D r. These are current co-located values, not historical or
remotely granted information. There is an invertible co-located linear update
restoring z to x while preserving r and s if and only if [A;C] has column
rank h, equivalently ker A intersect ker C={0}. No new record or movement is
needed, but every ordinary operation and later retirement remains charged.

Necessity holds even for arbitrary deterministic subsequent computation
restricted to these observations: a nonzero v in both kernels makes (x,r)
and (x+v,r) observationally identical, while their required endpoints differ.

For sufficiency put K=ker C. A is injective on K. Choose an invertible U
whose restriction to A(K) is the inverse of A restricted to K, by extending
the independent lists (A k_j) and (k_j) to bases. Then E=I-UA annihilates K,
so its rows lie in row(C). Choose V with VC=I-UA, and put W=-UB-VD.
The actual update z <- U z+V s+W r equals x. Apply U through elementary
invertible operations on the original destinations, then add actual side
and raw terms. The full triangular update on (z,s,r) is invertible because
U is, and r and s are unchanged. No side record is implicitly erased.

If A is invertible, U=A^{-1}, V=0, W=-A^{-1}B suffice. Mutually dependent
carrier masks therefore need an actual invertibility check, not an assertion
that every original can be unmasked using others which are still altered.

## Exact side-information deficit

For fixed A, restoration requires C restricted to ker A to be injective.
Thus q>=h-rank A; equality is attainable by separating a basis of ker A.
This is a bound on side information actually available at the restoration
chart. It grants neither that information nor its delivery for free.

Over a finite field, the same number of fixed-length arbitrary side-message
symbols is necessary by counting the |k|^(h-rank A) members of a fiber of A.
A linear separating C attains it. No variable-length or error-tolerant claim
is made.

## Width and implementation

The criterion extends to arbitrary finite block matrices by using total scalar
dimension; this alone does not supply a width-uniform implementation. For a
fixed binary carrier template A,B,C,D tensored with I_V, choose U,V,W over F2
and tensor one fixed finite ADD word with I_V. The word works for every
characteristic-two field and positive whole-record width. Swaps cost three
ADDs; no fractional record or unpriced block operation is admitted.

Gaussian elimination gives a conservative bound h(h-1)+3h ADDs for U, plus
at most h(q+m) side/raw ADDs. Emit and count the actual word in an application;
this bound is not a complete supplier ordinary tariff. Nonbinary scalars
retain their own implementation and charging obligations.

## Essential control

If both carriers equal x0+x1 then A=[[1,1],[1,1]] is singular. A raw x0 copy
at ground does not restore them at Hub without actual delivery. A raw x0
copy at Hub does: ADD z1 to z0; ADD the copy to z0; ADD z0 to z1. The result
is x0,x1 and the side copy stays unchanged. This three-ADD positive control
isolates the physical availability requirement.

## Application still required

Independently reconstruct current Hub rows and charts of the new released
carriers, compute this criterion, emit the actual restoration and count it.
The next construction should choose masks that serve many receivers while
making A invertible, or explicitly paying its side-information deficit.
All111 endpoints, full invoices, strict suppliers, recursion and the five
foundations remain open.

Prepared for @CubeJerry with substantial OpenAI assistance. The extension
argument is elementary linear algebra; the contribution here is its precise
simultaneous physical restoration interface, not novelty for matrix inversion.
