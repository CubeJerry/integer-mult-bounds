# Worker B review of the global rank refinement

**Accepted.** I reconstructed T, h and P using the original worker impulse replay and endpoint inverse, without importing the root reconstruction executable. The resulting `J=[Id_7-PT | Ph]` agrees entry by entry with the root's displayed matrix. Its first row is zero. The minor in rows and columns 1 through 6 has determinant exactly one, so its rank is exactly six. The independent receipt is `output/TOTAL-RANK-REVIEW-B.json`.

The left-kernel proof is correct. For `y[Id-TP,h]=0`, setting `z=yT` gives `y=zP`, `z(Id-PT)=0` and `zPh=0`. Conversely, any such z gives an annihilator y=zP; on this constrained kernel the map is injective because zP=0 forces z=zPT=0. Hence the left nullity of the 1289-row augmented response is `7-rank(J)=1`, proving `rank[C N]=1288` over Q. One can also derive the same equality by eliminating opposite identity blocks in the matrix with block rows `[Id_n,T,h]` and `[P,Id_7,0]`.

The global rank defect is one. The separate pinned quotient defect is five because it requires five additional alignment conditions relative to the specified source controls and outside coordinates. It would be incorrect to interpret that quotient rank as five missing global information dimensions.

Keeping all surrounding forms fixed and applying only original-input block preprocessors cannot enlarge the full response column space. Allowing coefficients of each original input in arbitrary existing local outgoing or terminal forms to change is a larger surrounding-form recoding freedom; the fixed-preprocessing observation does not exclude it. A possible rank-one global repair still needs all exact endpoint, locality, stock and pricing checks.

No positive supplier or new kappa follows. Reviewed by S031 worker B, 2026-11-20.
