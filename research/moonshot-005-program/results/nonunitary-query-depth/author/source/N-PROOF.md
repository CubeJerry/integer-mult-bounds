# A sharp rank-mass obstruction for unitary normalizer circuits

**Proved for the explicit unitary circuit model below; source-specific finite premises verified. No new κ.** For b independent copies of the actual112-port service N=Q⁻¹R0Q, any all-width unitary implementation with sublinear ordinary port-mixing entropy must spend asymptotic Gaussian rank mass at least224b. The rank-mass constant is sharp in the relaxed model. Its paid moment is at least(224b)^t for0<t<1, without an ambient-rank cap. Clean zero ancillary fields do not defeat the bound. Arbitrary nonunitary arithmetic, productive helper credits and changed caller endpoints are outside this theorem.

The actual source and physical interface are the independently reviewed full112 R0 construction and physical-involution-interface package. Exact source, proof and conditional budget pins are recorded in `RESULT.json`. This is a secondary scope screen for the paid N service; it does not exclude the programme's mixed-orientation caller redesign.

## 1. Quantified circuit model

For each positive integer column multiplicity V, let one field have complex coordinate dimension K=2^(nV), with n≥9. The ambient n may vary with V. There are112b main fields and any finite number of additional fields, all of this same dimension. The latter begin at zero and must return to zero for every main input. The whole straight-line computation is unitary on the direct sum of all fields, including hypothetical nonzero ancillary inputs. This is a linear-field model, not a tensor-product quantum ancilla convention.

Allowed gates are:

1. Arbitrary coordinate monomials, including phases, field permutations and coordinate permutations. They are unitary and have no entropy change.
2. A unitary p-by-p port matrix applied identically to the coindexed coordinates of p fields, with coordinate monomials permitted before and after it. Its ordinary entropy allowance is p·log₂p. Let C_port(V) be the sum of these allowances over the circuit. This counts each actual port-mixing occurrence, including those involving ancillas or different service banks.
3. A rank-r Gaussian child on one field, possibly surrounded by coordinate monomials. Its central operation is the tensor product over V columns of an r-axis Gaussian transform. Both orientations are allowed and charged the same positive r. All these ranks are included in the paid mass S_V=Σr and moment P_V=Σr^t. No productive helper credit is subtracted.

The ordinary condition is C_port(V)=o(V). In particular it holds for a fixed finite ordinary template on a fixed finite collection of fields, regardless of its coefficients. A macro containing nonunitary arithmetic may be treated as a port gate only if its complete isolated action is exactly one of the unitary port matrices above; arbitrary nonunitary blocks interleaved with Gaussian calls are not admitted by this argument.

At completion the main action must be precisely the direct sum N^⊕b on arbitrary independent inputs, and all added zero fields must be restored. No identification of the b banks' baselines is permitted.

## 2. The source-specific target entropy

For each actual port h, let q_h be its distinct nonzero binary normal and

\[
C_q=\frac{1+i}{2}I+\frac{1-i}{2}X_q,
\qquad Q_h=C_{q_h}^{\otimes V}.
\]

The authentic R0 is a112-by112 real orthogonal matrix. Every row has exactly four nonzero entries, each±1/2, and each neighbor j has q_j≠q_h. These facts are independently checked from the pinned source. Distinct nonzero binary normals are linearly independent as a pair.

The h,j block of N is R_hj(C_qh⁻¹C_qj)^⊗V. The one-column product has precisely four translations, on span{q_h,q_j}, all with coefficient magnitude1/2. Thus each nonzero block has4^V entries per row, each of magnitude2^(−V−1) after the whole-bank coefficient R_hj is applied once. The four input ports are disjoint coordinates. Every row of N therefore has exactly4^(V+1) equal squared magnitudes4^(−V−1), and Shannon entropy2V+2 bits. Extra ambient coordinates are spectators and do not change this count.

The scalar port coefficient is not tensor-powered. `check.py` verifies every actual row at V=1,2,3 with exact Gaussian rational coefficients, alongside the universal product argument. These finite widths authenticate the source conventions; they are not the proof for unbounded V.

## 3. A full-unitary entropy potential

For a unitary matrix U on all main and ancillary coordinates define

\[
\Phi(U)=\frac1K\sum_i H\bigl((|U_{ij}|^2)_j\bigr)
=-\frac1K\sum_{i,j}|U_{ij}|^2\log_2|U_{ij}|^2,
\]

with0·log0=0. Every row is a probability distribution, so Φ≥0. At the start Φ(I)=0. Left multiplication by any coordinate monomial only permutes rows and changes their phases, leaving Φ unchanged.

**Group lemma.** Suppose a gate mixes disjoint coordinate groups B, each of size m_B, and is unitary within each group. Then

\[
|\Phi(GU)-\Phi(U)|\le\frac1K\sum_B m_B\log_2m_B.
\]

To prove this, fix one column j and one group B. Its total mass p=Σ_(i∈B)|U_ij|² is preserved. If p>0, the group's entropy contribution is−p log₂p+pH(a), where a is its conditional probability vector. Only H(a) changes, and0≤H(a)≤log₂m_B. The absolute change is at most p log₂m_B. Summing columns gives Σ_j p=m_B, because the current full matrix is unitary. Summing groups proves the lemma. The case p=0 contributes zero.

A p-port unitary has K groups of size p, hence changes Φ by at most p log₂p. A rank-r tensor Gaussian on one field partitions its K coordinates into K/2^(rV) groups of size2^(rV). It therefore changes Φ by at most rV. Other fields are singleton groups. Its ordinary monomial factors change nothing. The bound applies equally to an inverse Gaussian child.

Consequently every allowed circuit satisfies

\[
\Phi(U_{\rm final})\le V S_V+C_{\rm port}(V). \tag{1}
\]

This potential is evaluated on the full unitary operator, not only on the actual data or the currently zero ancillary values. Ignoring the latter matrix columns would invalidate the gate argument.

## 4. Clean ancillary fields and the rank-mass theorem

Write the final unitary in main/ancillary blocks. Correctness on every main input with initially zero ancillary fields forces its first block column to be(N^⊕b,0)^T. Since N^⊕b is already unitary, orthogonality to these columns forces the other upper block to vanish. Thus

\[
U_{\rm final}=N^{\oplus b}\oplus W
\]

for a unitary ancillary block W. Its entropy contribution is nonnegative. By the target row count,

\[
\Phi(U_{\rm final})\ge112b(2V+2)=224b(V+1).
\]

Combining with(1) yields the exact finite-width statement

\[
\boxed{V S_V+C_{\rm port}(V)\ge224b(V+1).} \tag{2}
\]

Therefore

\[
S_V\ge224b+\frac{224b-C_{\rm port}(V)}V,
\qquad \liminf_{V\to\infty}S_V\ge224b. \tag{3}
\]

Ranks are integers. Under C_port=o(V), inequality(3) in fact forces S_V≥224b for every sufficiently large V, even if the number, sizes and placement of Gaussian calls vary with V. For one fixed all-width Gaussian profile, S≥224b immediately by letting V grow.

This covers genuine joint unitary processing of independent service banks. Ordinary mixing across those banks or clean ancillary fields is included in C_port. There is no subtraction of a helper target rank or an unproved inference from net rank to net concave moment.

## 5. Paid moment: a cap-free consequence and a bounded-rank refinement

For0<t<1 and nonnegative x,y,

\[
x^t+y^t\ge(x+y)^t.
\]

For example, after dividing by(x+y)^t, this is a^t+(1−a)^t≥a+(1−a)=1. Iteration gives P_V=Σr^t≥S_V^t. Hence(2) implies

\[
\boxed{P_V\ge\left(\max\left\{0,224b+
\frac{224b-C_{\rm port}(V)}V\right\}\right)^t,}
\qquad
\boxed{\liminf P_V\ge(224b)^t.} \tag{4}
\]

The liminf step uses monotonicity and continuity of x^t on positive x; it does not assume fixed rank profiles or exchange a limit with an unbounded sum. The eventual integer rank bound also gives P_V≥(224b)^t eventually. No upper bound on ambient rank is needed.

If every Gaussian call additionally satisfies1≤r≤R_max, then r^t≥R_max^(t−1)r and

\[
\liminf P_V\ge224b R_{\max}^{t-1}. \tag{5}
\]

For the nine-head model at t=199/200, the latter is stronger than(4). For arbitrary extra spectator axes, the cap-free statement remains valid.

The pinned physical-interface budget permits a single-bank service moment below75.78579625756281..., or a genuinely joint two-bank moment below151.57159251512562..., before every other new expense. Exact integer-root enclosures in the receipt show that(4) exceeds each corresponding ceiling by a large margin. Thus this unitary/no-productive-credit class cannot supply the normalizer service required by that specific conditional reduction. The result does not establish a lower bound for arbitrary nonunitary source algorithms or for another caller's endpoints.

## 6. Sharpness of rank mass in the relaxed model

The direct expression Q⁻¹R0Q uses112 rank-one calls for Q and112 for Q⁻¹, so S=224 for one bank. The native halfclass decomposition expresses R0 as a field permutation followed by28 independent four-port orthogonal matrices, each with coefficients±1/2. Their total ordinary entropy allowance is28·4·log₂4=224. These exact4-by4 blocks are verified from the source, with no free physical cochart availability asserted.

Thus this relaxed unitary model has a circuit with S=224 and C_port=224. It attains equality in(2) at every width. Repeating independently gives the sharp224b mass constant for b banks. The resulting moment is224b, not necessarily the optimum moment. The weaker cap-free and capped moment bounds are not asserted sharp.

This is a positive control for the scoped rank-mass theorem, rather than a newly admitted physical source or an economical normalizer. Its service price already exceeds the conditional allowance.

## 7. Why the ordinary uniformity restriction is essential

A concrete clean-ancilla construction shows that unitarity alone is insufficient. Let X be a single-column coordinate translation involution and P_±=(I±X)/2. On one main field and one ancillary field, define

\[
J=\frac{1+i}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix},
\quad W=J^*\begin{pmatrix}I&0\\0&X\end{pmatrix}J
=\begin{pmatrix}P_+&P_-\\P_-&P_+\end{pmatrix}.
\]

J is a two-port unitary with Gaussian dyadic coefficients. Then

\[
W\begin{pmatrix}I&0\\0&iI\end{pmatrix}W
=\begin{pmatrix}P_++iP_-&0\\0&P_-+iP_+\end{pmatrix}.
\]

The first diagonal block is C_q. Starting with the ancillary field zero returns it to zero. This uses four two-port unitary occurrences, coordinate monomials and a phase, with no Gaussian child. Applying it separately to each of V columns implements C_q^⊗V with C_port=8V. Reusing the clean ancilla over all224 Q/Q⁻¹ factors and adding R0 realizes N with zero Gaussian calls but C_port=1792V+224. This does not meet o(V). It is fully consistent with(2) and demonstrates why unrestricted linear-in-V ordinary work cannot be silently granted.

The receipt checks this identity exactly, including the clean ancillary block, and rejects omission of its final W. It also checks that incorrectly tensoring the whole-bank scalar coefficient changes the actual target row norm.

## 8. Status, reproducibility and credit

The entropy and asymptotic theorems are universal mathematical arguments. The actual R0 geometry, equal support, halfclass decomposition and comparison with the retained conditional budget are source-specific exact finite premises checked by `check.py`. Normal and optimized receipts are byte-identical. No author's verifier is imported.

Run `python check.py --source <R0-minimal/WORD.json.gz> --budget <physical-involution-interface/BUDGET.json>`, and repeat under `python -O` with a separate output path. The source and budget are authenticated by their exact pins. Ordinary cost, precision and the remaining multiplication foundations are not discharged. No new κ is established.

Root proposed the entropy question and supplied the decisive cap-free concavity strengthening. Worker C developed the full-unitary potential proof, clean-ancilla argument, sharp rank-mass control, explicit ordinary-budget countercontrol and source checks. The R0 source, physical normalizer reduction, native halfclass geometry and preceding independent reviews retain their original credit. Prepared for @CubeJerry with OpenAI assistance.
