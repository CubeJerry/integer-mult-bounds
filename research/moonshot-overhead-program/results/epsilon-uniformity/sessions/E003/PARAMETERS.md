# E003 parameter and threshold ledger

Notation: `L=1+log2 n`, `x=log2 L`,
`Phi(y)=y^(2/3)(log2(y+2))^(1/3)`,
`Psi(y)=sqrt(y log2(y+2))`. All profile constants must be absolute.

| Quantity | Bound / choice | Scope and remaining dependency |
|---|---|---|
| Header-free modular scaling | time V poly(h); space O(V)+poly(h,log V) | Proved HFS; no coefficient-height multiplier on payload storage. |
| Local label geometry | log[D(1+lambda)] <= 3 log(m)/d + O(d^2 log log(m)) | Source-specific family; choose power-two d to get O(Phi(log m)). |
| Interchange child coefficient | <=sqrt(m) 2^{O(Phi(log m))} | Completed finite repair and exact volume invoice must be preserved. |
| Interchange arity | largest odd m<=floor(e^(1/r)) | Fixed sufficiently large r absorbs polynomial local work and construction. |
| Interchange width descent | e/(8m)<=f<=e/m eventually | Prefix, reserves, rounding and direct base charged. |
| Rational Walsh child coefficient | <=sqrt(A) 2^{O(Psi(log m))}, A=Theta(m) | Predecessor rational predictor and source kernel. |
| Walsh arity | log m=Theta(Phi(log a)) | Smaller than power-size interchange arity; prices its polynomial routing toll. |
| Walsh row padding | product_i W_i <= a^C | Global padding against exponential leading spectator count, not per-node inflation. |
| Numerical local height / log gain | <=m^C | Scalar generation and actual k-bit record arithmetic remain separate. |
| Whole numerical preparation | <=2^{k^{o(1)}} | Walsh setup only, including repeated setup at polynomially many nodes; interchange setup is paid locally. |
| Numerical precision | C0 k bits | Admitted after explicit k>=m_max^K2 guard; counts ancestor-path gains, completed unitary children and faults. |
| Preliminary visited space | n poly(1+x) | Sequential chunk wrapper proves one absolute O(n) cap, with O(nr) rowwise assembly. |
| Admitted final envelope | H<=2^{O(Phi(x))} | Complete written admission in lead/ADMISSION-TWO-SCALE.md; matches earlier E002/S003 rate. |
| Canonical binary-Walsh invoice | log J>=sqrt(log m log log m) | Exact rank and incidence lower bound on specified positive invoice; no runtime inference. |
| Crown-product laminar load | >=ceil[(1+(q-2)/q^k)(q-1)^(k-1)] | One common laminar endpoint family; arbitrary nonlaminar partitions remain open. |

The existing weighted-search certificate and its growing-index obstruction
remain recorded in E001. No claim here turns that sufficient certificate
into a lower bound on actual scheduler time. The new construction seeks a
direct input-length-aware fixed program.
