# Exact nonlinear rigidity for native sums over a finite abelian alphabet

Let A be a finite abelian group of order n>1. At each of the 111 native roles i, form the output

    T_i(x) = x_i + Σ_{j foreign to i} f_ij(x_j),     x ∈ A^111.

Subtract f_ij(0) from each function and translate the output by the resulting known constant. Hence suppose f_ij(0)=0. Assume only that the 221 functions on the certified bipartite tree are bijections. Other proper functions may be arbitrary. There is no field-linearity, additive-edge, or rectangular-rank assumption.

**Theorem.** If |im T| < 3n⁹/2, then A is an elementary abelian 2-group and there are additive automorphisms P_i of A for which every proper f_ij=P_i P_j⁻¹. Conversely each such map has image exactly n⁹. Thus every other tree-bijective fitting in this class has at least 3n⁹/2 output words. One-way return encoders with an identical sum-separable fitting can apply this bound when their transcript must distinguish its outputs. General nonlinear interactions among different donors at the same output remain outside this proposition.

## Two large graphs in a small sumset

If two zero-containing subsets X,Y of a finite abelian group each have size n and |X+Y|<3n/2, then H=X−X=Y−Y is a subgroup containing X,Y, with |H|<2n. For every d=x−x' in X−X, the two translates x+Y and x'+Y inside X+Y intersect in more than n/2 points. Thus |Y∩(Y+d)|>n/2. For d,e in X−X the two corresponding subsets of Y intersect, giving d−e∈Y−Y. Interchanging X and Y and using zero in each difference set gives X−X=Y−Y and H−H=H. Finally the n² ordered pairs in Y² count exactly the intersections over H. This gives |H|<2n. If one coordinate projection of X in A×A covers A, |H| is divisible by n and therefore equals n. Then X=Y=H.

## The nonlinear square on the actual ports

For every certified two-by-two proper rectangle (i,j)×(p,q), the eight specified auxiliary roles C have pairwise-zero nonself coefficients and are exterior to the four endpoints. Across each corner and each c∈C, at least one of the two links through c is absent. Restrict the native input to C,p,q and observe only outputs C,i,j. For fixed x_p,x_q each y_c can be prescribed by choosing x_c=y_c−f_cp(x_p)−f_cq(x_q), reading absent functions as zero. If f_ic is present then neither c,p nor c,q is present, so x_c=y_c in the summands contributing at i. The same holds at j. Consequently this restricted output image has exactly

    n⁸ |Γ_p+Γ_q|,     Γ_p={(f_ip(t), f_jp(t)): t∈A},

with the analogous definition for q. For each fixed y_C the exterior image is a translate of this sumset. The full image bound gives |Γ_p+Γ_q|<3n/2.

If three of the four functions on a rectangle are bijections, both graphs have size n, and one has both projections bijective. Applying the preceding lemma gives the same order-n subgroup as both graphs. This subgroup is the graph of an additive automorphism of the first copy of A onto the second. Hence the fourth function is also bijective, and

    f_jp f_ip⁻¹ = f_jq f_iq⁻¹

is an additive automorphism (composition of functions). Starting with the certified tree, the 6,249 native rectangles give these identities and bijectivity everywhere.

## A single change of coordinates per native role

Choose P_0=identity and define permutations P_i,Q_j along the tree by f_ij=P_i Q_j. The tree spans all 111 row and 111 column roles. The displayed rectangle identity propagates the same factorization through the entire transcript. For any two output rows of a certified rectangle, P_j P_i⁻¹ is additive by the common-subgroup argument. The row-pair graph consisting of these rectangles is connected on all 111 output roles, as independently testable from the witness. Thus every P_i is additive. Each Q_j is so far only a permutation fixing zero.

Parameterize input j by z_j=Q_j(x_j) and apply the additive output change P_i⁻¹ at i. This preserves image size and makes every proper contribution z_j. The only exceptional coefficient at i is its own function d_i(z)=P_i⁻¹ Q_i⁻¹(z). On the certified disjoint ten-by-ten minor there are no own terms. Its scalar integer determinant has absolute value two, so its Smith form is diag(1,…,1,2). On A its image has size n¹⁰/|A[2]|, where A[2] is the kernel of doubling. The assumed strict upper bound implies n/|A[2]|<3/2. This quotient is a positive integer, so A=A[2].

Now A is a binary vector space. For each role i use the certified disjoint nine-row, nine-column scalar core outside i with odd determinant and even bordered determinant upon adding i. Fixing the nine core outputs permits arbitrary z_i, with unique core inputs depending affinely on z_i. The remaining i-output varies by d_i(z_i)−z_i: the scalar Schur correction is one in characteristic two. That ten-block image therefore has size n⁹ times the number of distinct values of d_i(z)−z. The strict upper bound forces this integer to be one. Evaluation at zero gives d_i(z)=z and Q_i=P_i⁻¹. Conversely the canonical binary scalar matrix has rank nine; the coordinate changes preserve the cardinality n⁹.

[Geometric rectangle and scalar determinant certificate](../../bit-global-native-rank-rigidity/ADMISSION.md). Credit @CubeJerry and the native support, canonical rank and rectangle predecessors. Substantial OpenAI assistance. No new κ.
