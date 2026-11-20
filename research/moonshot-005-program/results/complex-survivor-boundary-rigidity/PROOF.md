# Exact five-message operator and boundary-bank rigidity

## 1. Source and model

Let `E` be the complete 1289×1289 rational endpoint matrix of the authenticated
#7830 word at `14c74c6a67108f675ac1196a5f2415ead0920e71`. Apply the exact
#7833 construction with its genuine paid fifth observer, retaining all original
input and terminal roles. The checker verifies that this compensated word
still has exactly endpoint `E`.

Inputs and outputs are grouped by their original physical chart. Two chart
labels with equal binary span are grouped together; this gives 1102 possible
physical charts. Within an input bank or output bank, arbitrary mixing of
the fields is permitted. Distinct banks may not exchange fields through a
boundary coordinate change.

Fix any characteristic-zero field `K` and any positive finite width `V`.
Replace each scalar field by `K^V`. Every original rational coefficient acts
by that scalar times the identity on `K^V`. Number the five occurrences

\[
(e_0,e_1,e_2,e_3,e_4)=(86,97232,97241,97323,99064).
\]

At occurrence `e_j`, apply an arbitrary `K`-linear map `A_j:K^V→K^V` to
the message that the unchanged local form would produce at that time. All
other literal forms and routes are frozen. Denote the resulting endpoint by
`E_A`. Deletion is included as `A_j=0`; identity is the unmodified message.

The question is whether there can be independent bijections `U` on each
original output bank and `W` on each original input bank such that

\[
U\circ E_A\circ W=E\otimes I_V.
\tag{1}
\]

These bijections need not be linear. No free exchange between distinct banks
is hidden in (1).

## 2. Exact source identities

The checker reconstructs the complete endpoint from the literal forms.
Its bipartite coefficient support has 889 components of order one and 200
components of order two. Exact component inversion, followed by both full
matrix products, proves that `E` is invertible.

Let `p_j` be the original scalar payload row at occurrence `e_j`; let `P`
be the matrix with these five rows. Introduce independent additive messages
`z_j` immediately after the five occurrences. All subsequent literal forms
are kept fixed. Let `B` be the 1289×5 rational matrix mapping `z` to the
terminal perturbation. Let `H` be the 5×5 matrix mapping these same additive
messages to the five *pre-output* payload perturbations, before adding the
corresponding `z_j`.

Forward differentiation through the actual literal schedule gives

\[
H=0,\qquad G:=P E^{-1}B=\operatorname{diag}(1,0,0,0,0).
\tag{2}
\]

This is not an assumption that the occurrences lie in separate paths.
Exact cancellations in their literal coefficients are included. Because the
coefficients are rational scalars, each zero in `H` remains zero for arbitrary
vector-valued additive messages.

Write

\[
R=E^{-1}B,\qquad Q=P E^{-1},\qquad \Delta_j=I_V-A_j.
\]

By `H=0`, none of the five changes alters the pre-output payload at any of
the five named occurrences. Consequently, with scalar matrices tensored by
the identity and `Δ=diag(Δ_j)`, the exact changed endpoint is

\[
E_A=E\otimes I_V-(B\otimes I_V)\Delta(P\otimes I_V).
\tag{3}
\]

The checker separately replays three simultaneous scalar specializations of
(3) against every terminal coefficient, including deletion of all five.
The all-width identity follows from the linear literal perturbation argument,
not from those finite specializations.

## 3. Invertibility and the inverse formula

Let `r_0` and `b_0` be the first columns of `R` and `B`. Equation (2) gives
`P r_0=(1,0,0,0,0)^T`, so `r_0` is nonzero. If `A_0 z=0` for a nonzero
`z∈K^V`, then (3) gives

\[
E_A(r_0\otimes z)=b_0\otimes A_0z=0.
\]

Thus a singular `A_0` makes `E_A` noninjective. Equation (1) is then
impossible, because the target and both boundary changes are bijections.

Now suppose `A_0` is invertible. By (2),

\[
I-\Delta(G\otimes I_V)=\operatorname{diag}(A_0,I_V,I_V,I_V,I_V).
\]

Multiplication of (3) by the proposed inverse, using (2), gives

\[
E_A^{-1}=E^{-1}\otimes I_V+(R\otimes I_V)
\operatorname{diag}(D_0,D_1,D_2,D_3,D_4)(Q\otimes I_V),
\tag{4}
\]

where

\[
D_0=A_0^{-1}-I_V,\qquad D_j=I_V-A_j\quad(1\le j\le4).
\tag{5}
\]

For example, the first block uses
`A_0^{-1}(I_V−A_0)=A_0^{-1}−I_V`; the other four blocks use the identity
inverse. No commutativity among the five `A_j` is required. Each block acts
on its own message field, and all coefficients in `R,Q,G` are central scalars.
The same multiplication proves both sides of (4).

## 4. Five isolated inverse-bank dependencies

For the following input-axis/output-axis pairs, the entire corresponding
physical-bank block of the old inverse `E^{-1}` is zero. The checker tests
this over **every** input and output axis in each pair of physical banks,
including any equal-span chart aliases, not just at the listed entry.

At the specified entry, the five scalar products `R_{a,j}Q_{j,b}` vanish
except for the one indicated:

| Message `e_j` | Input axis `a` | Input chart | Output axis `b` | Terminal slot | Output chart | Nonzero `R_{a,j}Q_{j,b}` |
| --- | --- | --- | --- | --- | --- | --- |
| 86 | 17 | 16 | 131 | 154899 | 145 | −63/128 |
| 97232 | 17 | 16 | 150 | 154918 | 162 | 1/2 |
| 97241 | 19 | 18 | 129 | 154897 | 143 | −1/2 |
| 97323 | 17 | 16 | 776 | 155544 | 134 | 1 |
| 99064 | 19 | 18 | 150 | 154918 | 162 | 1/2 |

It follows from (4) that the changed inverse's entry at each witness is
exactly the indicated nonzero rational scalar times `D_j`. A nonzero `D_j`
therefore makes the inverse input bank depend on that output bank, whereas
the original inverse input bank was independent of it. Characteristic zero
ensures every listed scalar is nonzero in `K`.

## 5. Boundary bijections preserve bank independence

For a map between products of banks, say that output bank `a` is independent
of input bank `b` when varying only bank `b`, with all other input banks
fixed, never changes bank `a` of the output. Precomposition and postcomposition
by independent bijections at each bank preserve this property in both
directions. A bijection on bank `b` merely reparametrizes all its possible
values; bijections on the other input banks reparametrize the fixed context;
and a bijection on output bank `a` cannot identify two distinct values.

For a linear map, independence is equivalent to the corresponding whole
bank block being zero. If (1) holds, its inverse reads

\[
(E\otimes I_V)^{-1}=W^{-1}\circ E_A^{-1}\circ U^{-1}.
\]

Hence every zero inverse-bank dependency of `E` must remain zero for `E_A`.
The five witnesses in Section 4 force every `D_j=0`. Equation (5) then forces
every `A_j=I_V`. Conversely, all identity message operators recover `E`
with identity boundary maps. This proves the stated equivalence.

## 6. What the theorem leaves open

The quantifiers concern whole-field operators on these five particular
messages and arbitrary separate bijections within the original boundary
banks. The other internal forms are fixed. New local payloads involving other
stored histories, coupled recoding of surviving messages, new paid routes,
or communication between boundary banks are outside the theorem.

The earlier cut certificate allowed arbitrary internal linear recoding and
proved different graph-capacity necessities. Its remaining five deletions
cannot be called universally impossible on the basis of this narrower proof.
Additional paid communication requires either a complete coupled repair or
a new obstruction valid under those allowed internal changes.
No complex supplier construction, κ improvement, or admission of a redesigned
source by upstream native-realization proofs is asserted here.
