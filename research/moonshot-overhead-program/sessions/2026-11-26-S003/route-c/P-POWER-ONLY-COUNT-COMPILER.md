# Prime-power addition budgets without auxiliary roots

Status: **proved finite compiler component; independently accepted by Route A** in `../route-a/review-p-power-count-compiler.md`. This refines prime-characteristic count formulas PC1–PC8. It does not supply a new complete interchanger or multiplication bound and is separate from the admitted characteristic-two route.

**Subsequent finite improvement:** `TELESCOPING-PRIME-ARY-CARRY.md` supplies a polynomial-p p-ary carry formula. Combined with A's p-ary recurrence, it improves this note's binary-tree grammar bound m^{O(log p)} to m^K with an absolute K for 3<=p<=m. The present binary-tree proof and its evidence are preserved as the earlier construction. The top length L<=pD and all separate physical-compiler obligations remain.

Let m>=2, 1<=D<=m, and let p be prime. For 0<=a<p write B_a(X)=X(X-1)...(X-a+1)/a! over F_p, including B_0=1. These factorials are units. The old digit carry uses

    G_p(X,Y)=sum_(a=1)^(p-1) B_a(X)B_(p-a)(Y),
    H_p(X,Y)=1-(X+Y+1)^(p-1).

On ordinary base-p digits, G_p is the carry of X+Y, and H_p indicates X+Y=p-1. Rewrite its exact update as

    c_next=G_p(X,Y)+c-(X+Y+1)^(p-1)c.                 (PP-C1)

Do not first construct H_p and then multiply it by c.

## 1. Every addition has a p-power factor budget

Give the i-th digits and incoming carry budget p^i. Each factor X-r in B_a(X) has addition budget p^i; its product has budget a p^i. A summand of G_p therefore has budget p^(i+1), and its flattened binary sum can use that same p-power budget.

The inner sum X+Y+1 has budget p^i. Its(p-1)-st power times c has budget(p-1)p^i+p^i=p^(i+1). PP-C1 consequently has budget p^(i+1), while the output digit X+Y+c has budget p^i. These are lengths of actual padded factor families, not merely reduced formal polynomial degrees.

Constants are folded; scalar multiplication preserves a nonconstant budget. A constant has an explicit cyclic family at any requested positive budget. Products concatenate nonconstant budgets. Thus no nontrivial zero-degree scalar is mistaken for an empty factor product.

For p>2, separately forming H_p gives natural budget(p-1)p^i, which is not a p-power. Rounding H_p itself to p^(i+1) before multiplying by c exceeds the carry budget. Moving that multiplication inside the top sum avoids this obstruction.

## 2. The unfolded size bound

PP-C1 duplicates the predecessor carry twice instead of once. If input digit-i formulas have size at most S_i, a safe bound is

    |z_k|<=A_p sum_(i=0)^k 2^(k-i)S_i,
    A_p=128p².                                        (PP-C2)

The digit's binomial products and repeated X+Y+1 use O(p²) input copies; only the prior carry has the recursive factor two. Affine query indicators may be counted as leaves, or their absolute constant size can be included in the initial bound. For a balanced tree of r additions,

    S_(r,k)<=A_p^r 2^k binom(r+k,k).                   (PP-C3)

Substitution cancels2^i against2^(k-i), leaving the hockey-stick binomial sum. A fresh2^k loss is not multiplied at every tree level. With r=ceil(log₂m), k<=r, this is m^{O(1+log p)}. Adding a fixed residue offset requires one further digit-addition stage.

Take t=ceil(log_p(D+1)) digits, so the largest needed digit index is at most r. The unused carry beyond digit t-1 is not included in the formula. Generalized Lucas evaluation, including negative offsets, expresses binom(c-u,h) mod p as product_i B_(h_i)((c-u)_i). Its factors have total budget sum_i h_i p^i=h. Give the truncated Newton sum over0<=h<=D the least p-power budget L>=max(1,D). Then

    S=m^{O(1+log p)}, L<=p max(1,D),                  (PP-C4)

and every addition budget is a p-power at most L. For odd p the binary query indicators(1-(-1)^beta Q_j)/2 are valid affine substitutions. No factorial at least p is inverted; higher count digits are retained.

## 3. Frobenius cyclic lifting

Suppose two cyclic affine families of common length d=p^v have every cyclic product equal to P I and Q I. On their graded modules define operators A and B that advance their own grade and apply their own factor. They act on different tensor components and commute. Their d-th powers are P I and Q I. Frobenius gives

    (A+B)^d=A^d+B^d=(P+Q)I.                           (PP-C5)

Successive restrictions to total-grade slices yield d affine pencils. Every slice has d times the product of the child row dimensions; the product starting at any slice is(P+Q)I. This is a whole-row identity, not a claim about one output coordinate.

Products concatenate tensor-extended cyclic families. Inserting identity factors pads a family and preserves every cyclic product. These operations need no auxiliary roots. Since every sum gate in section1 has a p-power budget, the complete factorization is defined over F_p itself: its sum gates do not need prime-to-p cyclotomic roots.

For a formula of size S and maximum budget L, the independent width is at most L^S after harmless constant conventions. Hence its logarithm and explicit grade grammar have size m^{O(1+log p)}. The factor list has L stages. This is not polynomial in m with an absolute exponent when p grows.

The scalar slices also have a succinct execution in the same sense as B1. At an addition phase t, a grade-i input uses the first child's i-th factor and the second child's(t-i mod d)-th factor. The first changes the grade to i+1; the second leaves it at i. Both masks read the input grade. A formula traversal yields only polynomially many masked cyclic grade rotations in S,L and the scalar bit width. A cyclic rotation of d equal complete row blocks is a fixed-tape split/concatenate scan even when d is not a power of two. No d-by-d matrix or L^S-row instruction table is needed. This observation is a scalar-slice interface, not the physical shared-pencil theorem.

## 4. Consequence and remaining obligations

The earlier PC construction allowed arbitrary sum budgets and adjoined roots for their prime-to-p parts. PP-C1 removes that requirement for the actual count formulas at a factor at most p in the top pencil length. Its formula-size exponent O(1+log p) remains explicit.

This does not remove auxiliary algebra required by a separate spectral converter, supply a smaller scalar rank certificate, or justify all odd-characteristic endpoint maps. Shift-only check matrices could keep interpolation nodes independent of the exponential module; that is a separate repair interface. The new finite-alphabet packing lemma permits an explicit odd-characteristic finite algebra to be used with constant payload inflation once a completed whole-identity permutation exists, but it does not prove those missing identities.

No complete odd-characteristic adaptive cost is admitted here. In particular the quasipolynomial formula grammar cannot be assigned an absolute polynomial-m cost, and the factor-p pencil inflation must be included in any later invoice. The result is a concrete finite compiler simplification for the backup route.

## 5. Evidence and credit

`verify_p_power_count_compiler.py` passed 504 formula constructions, 47,544 count-digit and 47,544 offset-digit values, 24,924 Newton values, and 30,244 addition-budget checks. Its expression objects share references to keep the checker small; their stored size counts the full formula unfolding, reaching 1,311,481 nodes. The checks include higher base-3 and base-5 digits and negative offsets, not just one-digit residues.

The checker also passed 936 unfolded-size majorants, 754 primitive carry cases, 192 child and 96 sum cyclic matrix products, and 21 formal bivariate polynomial cyclic products across 3,225 matrix entries. The polynomial tests compare coefficients exactly, so they do not confuse equality on a finite field with a formal identity. Ten old-budget controls, twelve wrong-phase controls, and four non-p-power Frobenius controls rejected the incorrect constructions. The result is saved in `p-power-count-compiler-verification.json`. These are finite checks of the written component, not a full tape multiplier or formal-kernel proof.

Source: predecessor `routes/A/prime-characteristic-count-formulas.md` and its accepted review, the cyclic formula factorization, and S003 B1's succinct scalar slices. Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. The general Frobenius and Lucas identities are standard; no broad novelty claim is made. This note identifies and verifies the p-power-only syntax of this particular count compiler.
