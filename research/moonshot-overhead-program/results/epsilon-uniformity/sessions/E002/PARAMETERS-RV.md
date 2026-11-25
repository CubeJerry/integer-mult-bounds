# Conditional rectangle-volume parameter and threshold ledger

Status: complete reviewed implication; **RV-I and RV-W remain open**.
See [proof](lead/rectangle-volume-conditional-transfer.md) and
[admission](lead/ADMISSION-RV.md). Every K and C below is an absolute
constant, chosen once for one interpreter. No unknown fixed-parameter
threshold may replace the sufficient tested polynomial guards.

| Layer | Selected parameters | Charged consequence or obligation |
|---|---|---|
| Exact local geometry | z=log2 m; power-of-two d=Theta(z^(1/3)); h=2d−1; least t with td²>=2d²−2+z; q=2^t | N=q^(h²)<=m^(4+o(1)), mr*/N<=1; D^K(1+R/N)<=2^(Cz^(2/3)) |
| RV-I delivery | Complete free and low-rank pencil, occupied reserves and arbitrary spectators | Actual child volume RV1 and union of visited cells RV2; ordinary work m^K s^K V; main child<=16V/N, N>=64; reserve inflation<=8; finite repair<=1/16 |
| Exact recursive arity | Odd m(u)=Theta(u^gamma), fixed sufficiently small gamma>0 | All polynomial-m guards and ordinary work subcritical; actual child u/(4m)<=v<=u/m+2; time V sqrt(U) 2^(C(log U)^(2/3)), matching space envelope without sqrt(U) |
| Root field and compatible radix | Same explicit even power-of-two root degree and tested compatible radix as V | No repeated embedding; actual initial/child padding paid; no fixed-radix assumption |
| Numerical geometry | z=log2 m; even L=Theta(sqrt z); least dyadic q with q^(L/2)>=2^L m | R_f/N<=3^L; mR_c/N<=1; D_F<=1+Lq; pencil excess 2^(C sqrt z) |
| RV-W delivery | Completed physical shared endpoints and exact source cancellation | Actual normalized Fourier call count RV3; ordinary scalar/address work and coefficient height m^K; marked reused array regions; exact power-of-two batch and repair contraction |
| Numerical recursive arity | y=ceil(log2(a+2)); h=floor(cuberoot(y²)); m=2^h+1 | Child log-width falls by c y^(2/3); local normalized cost 2^(C y^(2/3)); recursive coefficient 2^(C y^(1/3)); strict majorant closes |
| Batching | Product of polynomial-m power-of-two divisors along actual path | Product polynomial in root active width; test exact spectator divisibility; no repeated padding coefficient |
| Accuracy | Actual compiled height/gain/event majorant | Log path gain k^o(1), polynomial-k branch count; one absolute O(k)-bit format and the existing source recovery margins |
| Preparation and cache | Fixed interpreter, compact parameter descriptions; total optional setup<=2^(k^eta'), eta'<1 | External-boundary global cache scans only; descendants carry local plans; ordinary data movement always charged |
| Outer common cap | r=2^(C4 ceil(cuberoot((x+O(1))²))+C5), v=ceil(n/r), r<=n tested | r² exact digit products and O(nr) assembly; fixed marked O(n) visited cells, n/16 preflight allowance and actual quadratic time clock |
| All finite exceptions | Failed shape, numerical, preparation, clock or visited-bound tests | Abort before forbidden head movement, clear scratch and exact schoolbook fallback; eventual success proved under the two local hypotheses |

The finite list of source short-axis cutoff conditions is tested by actual
integer comparisons and shape checks. The proof establishes an absolute
eventual cutoff, but does not numerically evaluate it. The logarithmic
factors inside the displayed big-O envelopes are mathematical majorants;
parameter selection uses integer bit lengths, powers and root comparisons.

Dependencies flow in this order: reviewed algebra/radix/field suppliers +
**RV-I** -> completed exact interchange -> physical address wrappers;
reviewed numerical suppliers + **RV-W** + those wrappers -> numerical Walsh;
then source outer transform/recovery and the common capped chunk wrapper ->
conditional full multiplication. The short O(k log k) multiplier is retained.
There is no circular invocation of the desired near-root multiplier.
