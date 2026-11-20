# Minimum-price stationary width at the final native facets

For each version of the GF(64) K library there is one explicit native terminal word preserving rank 480 on every foreign donor at every receiver. At bank 480 the sum of the minimum stationary field counts is **26,565**. The captures are independent of the donor. All 480 original late fields at each receiver retain their coefficient identity. No terminal MOVE or pure-F inverse is added. This proves simultaneous foreign rank on the formal K boundaries; it requires actual full-rank H/D/source transfer to apply to a complete physical input. Its endpoint is unconstrained apart from these ranks.

## General simultaneous completion

Fix a receiver with $b$ actual late output fields and $e$ early arrival fields. For every foreign donor $j$ let $E_j$ and $Y_j$ be the respective $e$-by-$b$ and $b$-by-$b$ responses on its independent $b$ input fields. Assume the stacked response has rank $b$. Set $s=\max_j(b-\operatorname{rank}Y_j)$. In the independent-coordinate, stationary-only crossing interface, $s$ field symbols are necessary: on $\ker Y_j$ all terminal proper late inputs agree while $|F|^{b-\operatorname{rank}Y_j}$ possible inputs must be distinguished. The counting bound allows nonlinear terminal encoders, provided no extra informative path is available.

When $|F|$ exceeds the number of donors, this width suffices linearly, with identity on arbitrary late baselines. Start with $A_j=Y_j$. As long as $A_j$ is deficient, choose one common row $c$ on the early arrivals so that $cE_j$ does not vanish on $\ker A_j$ for every deficient $j$. Each failure is a proper subspace because stacking $E_j$ with $A_j$ always has full column rank. Choose one output vector $u$ outside $\operatorname{im}A_j$ for the deficient donors. For each already invertible $A_j$, exclude the affine hyperplane on which $1+cE_j A_j^{-1}u=0$. There is at most one proper affine subspace per donor and fewer than $|F|$ subspaces cannot cover the ambient space. Then $A_j+u cE_j$ gains one rank at every deficient donor and stays invertible at every full donor. This update preserves the stacked rank. After exactly $s$ steps every donor is full. It is implementable as $s$ stationary linear captures followed by additions to the actual late owners. This argument proves existence in the declared interface independently of the explicit construction below.

## Actual rows, phases and widths

Each receiver belongs to 28 K planes. At a regular receiver 24 K send 15 early and 15 late, and four send 30 late fields. At a receiver incident with a singleton these counts are 25 and two, with 45 more late fields at the singleton. Each foreign donor supports 16 K planes, with independent 30-coordinate formal cuts. On a 15+15 terminal the chosen K minor gives 30 independent rows, hence 15 independent late rows and 15 complementary early rows. An all-late terminal has rank 30, including a singleton with 45 actual outputs. The 16 independent K summands imply that $b-\operatorname{rank}Y_j$ is exactly fifteen times the number of its supported 15+15 terminals. These counts follow on actual inputs whenever the preceding source/H/D word maps the donor invertibly to its 480 chosen K inputs.

Of 6,470 ordered foreign pairs, 488, 2,010, 2,515, 1,269 and 188 require 180, 195, 210, 225 and 240 field symbols respectively. At 106 receivers the maximum is 240. At the remaining five it is 225. The largest number of native foreign donors is 62. The total 26,565 counts allocated stationary fields across disjoint facets; a simultaneous peak interpretation additionally depends on their liveness.

## Constructive minimum-width words

Number K planes by increasing pinned atlas ID. At a receiver put the 15 early fields from each mixed terminal into one column of 15 stripes, sorted by original owner ID. Split the 15 or 30 ordinary late fields, sorted by ID within each K, into columns of 15. At a singleton, the selected rows are exponents below $2n/3$ in each of the recorded K's polynomial blocks of size $n$. Sort these 30 physical owners and split them into two columns. The other 15 real late owners form a third column. There are $e=24$ or 25 early columns and exactly 32 late columns. Every physical field appears once.

Write $r=s/15$. Over $F=\mathrm{GF}(2)[z]/(z^6+z+1)$ set $C_{ab}=(a+(32+b))^{-1}$ on polynomial-basis labels, with field addition XOR. Use $V=C[0:r,0:e]$ and $U=C[0:32,0:r]$. Each of the 15 stripes stores $VE$ and adds $U\operatorname{diag}(w)VE$ to its actual late owners. The 15-by-$r$ snapshots therefore meet the lower bound. Executable coefficient vectors $w$ appear for all receivers and both K variants in WORDS.json.gz. No stationary field needs to receive a late value. The coefficients apply sequentially to early arrivals while they are present and to late arrivals at their actual receiving facet.

Here is the exact determinant reduction behind the finite witness. For a fixed donor, write $d$ for its number of supported early columns. If the singleton is absent or unsupported, the $d$ missing late columns give a $d$-square restriction of $G=U\operatorname{diag}(w)V$ on those late rows and the supported early columns. All other active late coordinates are independent. Each stripe therefore has full rank precisely when this minor is nonsingular.

If the singleton is supported, there are $d-1$ wholly missing late columns and 15 extra relations at the singleton. Independently of the other K's, compute the matrix $T=[T_0\ T_1]$ expressing the 15 extra late rows through the two 15-row selected bands. Multiply the recorded 45-by-30 incoming restriction by the inverse of its selected 30-by-30 matrix to obtain $T$ in the actual physical ordering. Restrict $G$ to the $d-1$ wholly missing rows and $d$ supported early columns. It must have full row rank. If $v$ spans its one-dimensional kernel, any undetected raw early contribution has one scalar per stripe, with column direction $v$. Let $a,b,c$ be the products of the three singleton rows of the restricted $G$ with $v$, in the selected, selected, extra order. The remaining 15 equations have coefficient matrix $cI+aT_0+bT_1$. Full rank is equivalent to its invertibility. This calculation includes the actual proper data on every extra late Y. A simple deletion of those 15 rows would change the result.

The executable selector checks these exact equations for all 6,470 pairs and both K words, including 360 pairs supported at a singleton. Every published weight vector passed. The search stopped in at most ten candidates per receiver; the theorem uses the supplied exact finite certificate, independent of search success on other atlases.

## Accounting and limits

| Item at bank 3,840 | Spread K | Mixed K |
| --- | ---: | ---: |
| Binary capture ADDs | 92,075,520 | 92,075,520 |
| Binary delivery ADDs | 124,310,760 | 124,294,440 |
| Total ADDs | 216,386,280 | 216,369,960 |
| INITs and dirty CLEARs, each | 1,275,120 | 1,275,120 |

The binary invoice expands every field multiplier in the six polynomial-basis bits. It includes all independent source and destination bit pairs appearing in the declared direct-add implementation; no XOR consolidation or unpriced constant multiplication is used. Only the F work is counted in these figures. Every original movement, H/D/K action, source operation, return action and recursive prerequisite retains its separate bill. Equality of the resulting foreign blocks to the prescribed covariant target, or a rank-$9b+b/30$ return, requires additional evidence.

Run `python -B construct.py --repo REPO --k-certs K_AUTHOR_OUTPUT --out FRESH` with NumPy. The output records exact K/source pins and the decompressed certificate digest. Credits to the native owner atlas, shareable K cuts, GF64 K libraries, previous terminal and correlated-phase work, and @CubeJerry. Constructed with OpenAI assistance. No new complete κ.
