# Source-aware lowering of an orthogonal triple code

## Proposition and computational model

Let F be any field of characteristic two, let V be any positive whole-record width, and let X_a,X_b,X_c be arbitrary independent records in F^V. Let L_a,L_b,L_c be distinct native real lines with pairwise zero real inner products, and let F_a,F_b,F_c be their native orthogonal receiver facets in an ambient D-dimensional real chart. Thus each native line is contained in each of the other two receiver facets, but not in its own facet.

Assume a legal source prefix and the following **actual** source/geometry conditions:

1. A descending owned principal P is at an m-dimensional chart M with value X_b+X_c. Its acquisition cost is already explicitly present in the source prefix. No abstract span or unavailable past value is substituted for this record.
2. A chart E contains L_c, is contained in F_a and F_b, and is contained in M. Let e=dim(E). The actual source X_c visits E while still raw, so a scratch record R_c at E may capture X_c there.
3. K=L_a+L_b, J_a=E+L_b, and J_b=E+L_a are contained in M. The source X_b has a legal ascending visit to J_a while still raw, and source X_c has a legal ascending visit to J_b after E while still raw. All old source reads/restoration obligations are preserved. This condition is a source theorem to prove, not a consequence of chart containment alone.
4. Raw X_a and X_b can be captured at their native births in stationary records R_a at L_a and R_b at L_b. The source visits in conditions 1–3 precede P's descent and the final Y decoders. All required scratch records remain live through their final readers.
5. All old readers of the principal's former terminal have been protected or reencoded explicitly. Replacing that terminal by a+b+c is not automatically safe.

Suppose m>2 and e+1<D-1 for the nondegenerate displayed routes; equality cases omit zero-length moves. In the retained instruction model, there is then a literal construction that produces actual common code X_a+X_b+X_c and correctly increments Y_a,Y_b,Y_c, with all new storage, queries, movement, and retirements counted. It applies to every F and V above.

### Geometry implied by the assumptions

Pairwise orthogonality gives dim(K)=2, K contained in F_c, and L_a contained in K. Because E is contained in F_a and F_b, neither L_a nor L_b lies in E. Hence dim(J_a)=dim(J_b)=e+1. Moreover J_a is contained in F_a and J_b is contained in F_b. These prove the receiver paths below are nested; their source paths still require condition 3.

## Literal source and decoder word

Create the stationary captures R_a=X_a at L_a, R_b=X_b at L_b, and R_c=X_c at E. Create S_b=X_b at J_a and S_c=X_c at J_b by the actual source visits. Initialize Q=0 at K. The principal executes

1. MOVE P from M to K; ADD P into Q. Now Q=X_b+X_c.
2. MOVE P from K to L_a; ADD R_a into P.
3. MOVE P from L_a to ground. Now P=X_a+X_b+X_c.

P is **not reset after the retained partial sum**. This retained/common pairing is the mechanism.

The actual Y decoders are:

| Receiver | Ground read | Nested ascending route and reads | Resulting increment |
|---|---|---|---|
| Y_a | P | E: read R_c; J_a: read S_b; F_a | X_a |
| Y_b | P | L_a: read R_a; J_b: read S_c; F_b | X_b |
| Y_c | none | L_b: read R_b; K: read Q; F_c | X_c |

The equations follow by cancellation in characteristic two. All original-Y values remain arbitrary and occur with coefficient one only in their own records. Every original X is only read by the new instructions; its retained source restoration proof remains applicable when condition 3 is met. Retire all newly created owners after their last readers.

If the actual source value is X_b+X_c+g for a fixed recipe g of actual common records, the same construction works: the common principal has a+b+c+g; Y_a and Y_b also read g at ground; Y_c reads g at ground before its local path. The number of ADDs in the recipe for g is charged at every use. This is the masked version used for P5, where g=X0+X44. Existing ground E75/E79 adjustments are separate real reads with their own cost.

## Complete new primitive accounting

With none of the six scratch records already present, the construction uses exactly six INIT and six CLEAR calls for R_a,R_b,R_c,S_b,S_c,Q. It performs five source-capture ADDs, two carrier ADDs, and eight decoder ADDs, for 15 ADDs total, before any common-mask reads and before acquiring X_b+X_c at M. All six values are arbitrary; dirty-erasure applicability is not assumed away. No scratch record other than the principal performs a MOVE.

These are the local construction's full counts, not automatically its marginal counts in an assembled caller. An actual application may reuse existing stationary records, replace old decoders or delete obsolete owners. Its net INIT/ADD/CLEAR invoice must be computed from that exact word. Reuse is permitted only with verified value, chart, chronology, ownership and remaining-reader compatibility.

### Exact movement increment against a specified pair-code baseline

Write [r]=r^t, with [0]=0 and zero-length segments omitted. Assume the baseline already delivers X_b+X_c directly M→ground, decodes b and c by visiting the other native line, and sends the otherwise unchanged Y_a directly from ground to F_a. Suppose original X_b's available segment is L_b→U_b with dim(U_b)=r_b and J_a contained in U_b. Suppose original X_c already visits E and has segment E→U_c with dim(U_c)=r_c and J_b contained in U_c. Replacing only these segments and decoders gives the following **complete signed increment**:

| Part | Exact movement increment |
|---|---|
| Principal M→K→L_a→0 | [m−2]+2[1]−[m] |
| X_b visits J_a | [e]+[r_b−e−1]−[r_b−1] |
| X_c visits J_b after E | [1]+[r_c−e−1]−[r_c−e] |
| New Y_a decoder | [e]+[1]+[D−e−2]−[D−1] |
| Changed Y_b decoder | [e]+[D−e−2]−[D−2] |
| Changed Y_c decoder | [1]+[D−3]−[D−2] |

All changed segments are nested, so their rank-volume is unchanged at t=1. The sum has zero value at t=1. For 0<t<1 its concave-moment overhead remains real and must be charged; zero linear volume does not imply zero movement cost.

If E itself is a new stop in X_c's former L_c→U_c segment, use the complete source increment

\[
[e-1]+[1]+[r_c-e-1]-[r_c-1]
\]

instead of the third row. If old source obligations need relocation, add their exact changes as well. A paid helper transfer, altered raw capture, or old-reader repair is never hidden in the lemma's hypotheses or ignored in the invoice.

## Exact applications in the current 41-output source

For the last two triples, D=8,m=5,E=L_c,e=1,r_b=r_c=5. The displayed baseline sum becomes

\[
8[1]+3[3]-2[4]+2[5]-2[6]-[7].
\]

This is exactly the third pair-to-triple conversion, (a,b,c)=(49,45,48), in `build_clique41.py`. Every source visit is independently checked against the actual preceding word. The source carries the actual mask g=X0+X44; that mask's ordinary ADDs remain included in the final word.

For (a,b,c)=(40,29,42), original X29 already had a rank-two Jnew2 stop that became obsolete only after Y2 was repaired to read its raw29 correction at native L29. Replacing that old rank-two stop by J_a has zero movement difference, rather than the second-row increment. The additional Y2 split costs 2[1]−[2]. Therefore its actual increment is

\[
9[1]-[2]+2[3]-[4]+2[5]-2[6]-[7].
\]

The sum of the two actual increments is

\[
17[1]-[2]+5[3]-3[4]+4[5]-4[6]-2[7],
\]

matching the literal profile difference of the pinned 39 and 41 words. This equality is checked directly by the builder; it is not inferred from an optimistic schematic.

The first triple, (41,43,46), uses the same source-aware word with e=2, but its comparator is a different predecessor with a paid raw43 ground grant and a protected leaf source. Its exact signed profile is given in `clique39/PROOF.md`; it must not be priced as the pair-code comparator above.

## Scope and remaining obligation

The lemma lowers a source-compatible orthogonal triple code to actual instructions. It proves neither that every clique has the required source paths nor that enough such codes complete the 111-role native within budget. It does not supersede the independent Extra6 source-dimension cut, whose missing E directions must first be acquired outside its frozen one-channel interface. All global supplier, recursion, compilation, precision, ownership/erasure and recovery assumptions remain explicit.

Prepared by `/root/coded_construction` in @CubeJerry's persistent programme with substantial OpenAI assistance. The theorem abstracts the literal 39/41 constructions; independent review is required before programme admission.
