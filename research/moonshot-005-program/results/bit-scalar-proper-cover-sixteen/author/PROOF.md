# One scalar quotient direction saves at most sixteen proper-cover charges

**Proposed all-field source-specific theorem; independent review pending. No new kappa.**

## 1. Exact charge and dependencies

Use the pinned111 real BIT source lines and their rank7 receiver facets F_i,
with characteristic-two value field k and canonical fitting K, code C=row(K).
For a foreign support S in F_i, define chi_i(S) to be0 if S is contained in
one proper linear subspace of F_i (including empty S),1 if two proper
subspaces suffice but one does not, and2 otherwise. Thus chi is capped
proper-chart coverage minus its one free predecessor. It is support monotone.

The admitted native one/two-proper-chart support bounds36/52 imply
ell_i(S)<=chi_i(S). The admitted quadratic-incidence argument gives
gamma_i(S)<=chi_i(S): a union of two proper subspaces is annihilated by a
nonzero product of linear forms. A support whose quadratic products span
Sym^2(F_i), dimension28, has chi=2. Canonical foreign supports have this
full quadratic span at all111 receivers. Consequently canonical charge222
is justified geometrically, not only by its cardinality histogram.

Dependencies, relative to the programme results directory:

- bit-quotient-direction-savings/author/PROOF.md,
  SHA2568e83d29e18e78e1b6f8e30a154b9cc84ad089c5283b2c04c807e048ffee5229b,
  and its admitted independent review: all-field gluing and complete
  cardinality case classification. Its RESULT.json has SHA256
  88a192ec4b859780b02f109fdd0172cf52c6adbab8ae782006fa72b8192716a8.
- bit-geometric-facet-charge/author/PROOF.md,
  SHA2568fed71e8698ce84e1fa0f09deb7433f3338f21f3a35b912d08e2de046426d8ab,
  and root review: real quadratic geometry and native source incidence.
- Native source SHA256
  51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78.

The scalar cardinality17 theorem remains sharp and unchanged. The charge
here is different. This theorem does not replace17 by16 in a cardinality
claim, and does not assert that gamma dominates ell.

## 2. The universal scalar theorem

**Theorem.** For any characteristic-two field k and any native scalar fitting
A with row(A) contained in C+k h for an arbitrary h in k^111,

    sum_i chi_i(supp_foreign(A_i)) >= 206.

More generally, rows in any one nonzero projective quotient direction
contribute at most16 to sum_i(2-chi_i). This latter form follows by replacing
all other rows by their canonical rows; the replacement is still a fitting
inside C+k h and the canonical rows have chi=2.

Proof. Suppose the chi saving exceeds16. Since chi>=ell, the cardinality
saving is at least17. The admitted all-field cardinality theorem bounds it
by17, so equality holds. Its complete argument is as follows. A common
glued representative g has support V of real rank r and size s; the set
J of changed receivers inside V is an orthogonal direct summand of size j.
The finite parameter bound excludes every case except
(r,s,j)=(3,5,0),(3,6,0),(4,4,3),(4,4,4). The orthogonal-four cases save at
most15. Every other parameter triple saves at most16. Therefore equality17
must occur in a rank3 flat with support size5 or6 and j=0.

The admitted exhaustive rank3 catalogue contains all74396 actual flats,
from220934 independent triples. Its11761 relevant flat/width cases have
exactly twelve maximizers with eligible count17; every one has width6.
The list in the pinned RESULT is complete, not a sample or truncated list:
the predecessor verifier records every row attaining its computed maximum.
Let P be the corresponding full flat. Every changed receiver i is
orthogonal to P, and its row has the form A_i=K_i+t_i g with t_i nonzero.
Every canonical contact outside P therefore retains coefficient1.

The new certificate checks all20 orthogonal receivers for each of these
twelve flats, including any whose cardinality cannot improve. At each,
the quadratic products of canonical contacts outside P have rank28 over Q.
This is certified by an explicit28-by28 integer minor with nonzero exact
Bareiss determinant. Thus every changed row has chi_i=2 regardless of k,
t_i or the values of g. Unchanged rows are canonical with chi=2. The chi
saving is0 in these only possible cardinality17 cases, a contradiction.
This proves the theorem for arbitrary characteristic-two fields. The
finite geometry is over Q/R and is not reduced to the value field. QED.

## 3. Positive and negative boundary controls

An indicator h of seven mutually orthogonal native lines gives a fitting
whose seven selected rows equal h and every other row is canonical. Each
selected foreign support has six independent roots and fits a proper
subspace, so chi saving is14. Thus the proved maximum lies between14 and16;
no sharpness assertion is made for16.

The old rank3 six-root witness with cardinality saving17 has chi saving0,
by the new forced-contact certificates. This is a meaningful control
against conflating cardinality and geometric costs. Replacing one certified
minor row by a duplicate destroys its determinant. Omitting the complete
extremal classification would leave the all-field theorem unproved.

## 4. Consequences and limitations

Every use of the old scalar17 capacity for a support-monotone charge may
be replaced by16 if the entire argument is explicitly formulated using
chi. In particular, a scalar cover that dominates each block row in support
also dominates it in chi. There is no such automatic transfer to gamma
via an unproved comparison gamma>=ell.

The actual source-incidence interface still has to prove chi is charged by
its nonanchor occurrences; the admitted one/two-proper-chart argument does
so in the retained native model. No complete BIT word, ordinary service,
compiler, complex supplier, kappa or foundational discharge is supplied.
Further operator-density or decomposable-code corollaries require their
own stated hypotheses and compatibility check. A possible improvement to14
remains open at this checkpoint.

Credit @CubeJerry, prior scalar gluing/census and geometric-incidence authors,
root construction, and OpenAI assistance. The predecessor finite catalogue
is reused as admitted evidence; the240 new exact minors are new checks.
