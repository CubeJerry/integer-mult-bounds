# Parameter and threshold ledger for the variable-parameter construction

Use with `lead/variable-profile-theorem.md` and `lead/ADMISSION-V.md`.
All constants are absolute effective constants of the described fixed
machine; they and the eventual cutoff have not been evaluated numerically.
Let Phi(y)=(y+1)^(2/3)(log_2(y+2))^(1/3).

| Quantity | Actual choice or bound | Cost or guard |
|---|---|---|
| Input scales | L=1+log_2 n; x=log_2 L | Length scan and integer bit lengths |
| Exact local arity | m=2 floor(floor(u^(1/M))/2)+1 | Fixed integer M, integer root comparisons |
| Compiler exponent | gamma=1/M, gamma K<1/4 | K covers all polynomial descriptions and local arithmetic |
| Label distance | Power of two within a fixed factor of (log m/log log m)^(1/3) | Integer comparisons; rank and dimension guards |
| Label geometry | D(1+lambda)<=2^{C Phi(log m)} | Actual endpoint and complete call invoice |
| Label count/rank | m<=N_label<=m^5; m r*/N_label<=1 | All query low-rank vectors together fit one volume |
| Complete exact call mass | <=C sqrt(m) 2^{C Phi(log m)} | Includes reserves, initial padding, child repadding |
| Unit product | Q even, complete rational pivot/inverse list | b congruent to1 modulo Q; no prime-ring assumption |
| Radix scale | H=ell(Q)+ell(W)+2ell(u+1)+4 | ell is integer bit length |
| Radix selector | e=floor(u/H), B=ceil(2^(u/e)), b=1+Q ceil((B-1)/Q) | Exact integer roots/division; e>=2 |
| Initial padding | <=1+1/(u+1) | Both fields and leading batches together |
| Child width | v=ceil(log_2 b^f), f=floor((e-1)/(m+2a)) | u/(4m)<=v<=u/m+2; lower bound tested |
| Raw-to-binary child padding | <4 for two fields | Paid separately at every child |
| Common exact data field | E=F_(2^s), even power-of-two s=O(log U) | Irreducible polynomial and omega^2+omega+1 root constructed once |
| Field encoding | s-bit records embedded once | No descendant re-embedding |
| Local exact ordinary time | C m^K s^K V | Heights, arithmetic, head movement and row scans included |
| Local exact shape | u>=m^K; u>=K log(s+2) | Otherwise direct bit base; fixed eventual success |
| Spectral metadata | One m-label mask per B>=2m+1 field-value block | O(log m) direct role moves; strip before children |
| Endpoint storage | O((1+lambda)V) | Prepared copies shared across all queries |
| Main child entry volume | <=16/N_label<=1/4, N_label>=64 | Both initial and child padding included |
| Finite exact repair child | 1/16 within current padded node | Geometric parked arrays |
| Reserve child entry volume | <=8 times parent | Main arrays cleared; descriptors parked |
| Spatial depth | O(log log(U+4)) | 8^depth is polylog U |
| Exact interchange | time V sqrt(U+1) 2^{C Phi(log(U+2))}; space V 2^{C Phi(log(U+2))} | Original binary volume V |
| Numerical local arity | y=ceil(log(a+2)), ell=ceil(log(y+2)), h^3<=y^2 ell<(h+1)^3, m=2^h+1 | log m=Theta(Phi(y)); m=a^o(1) |
| Numerical child | A=Theta(m), f largest even integer <=a/A | Remaining even width <2A handled directly |
| Numerical recursive mass | sigma/W<=C sqrt(m) 2^{C sqrt(log m log log m)} | Normalized rational template, all calls charged |
| Batch divisor | Product of W_i<=(a+2)^C, each W_i a power of two | Divides root q=2^(k-a) eventually; exact preflight test |
| Numerical local tape toll | V m^K sqrt(a+1) 2^{C Phi(log(a+2))} polylog k | Internal active slots; no repeated global k-width gather |
| Numerical norm | Path log gain <=log(k+2) 2^{C Phi(log(k+2))}=k^o(1) | Actual gain/event-count test before fixed format |
| Numerical precision | Absolute O(k) bits | Fixed source norm/error allowances and direct fallback |
| Numerical normalized recurrence | F(y)<=2^{C2 Phi(y)}+2^{C3 Psi(y)}F(y-c Phi(y)) | Psi=y^(1/3)(log y)^(2/3); inductive Phi majorant |
| Combined setup | <=2^{k^eta'}, fixed eta'<1 | Includes optional exact validation; not relabelled k^o(1) in the exponent |
| Plan access | Global cache only at polynomially many external boundaries | Local spatial chain/current descriptors carried within recursion |
| Outer digit multiplier | v sqrt(L(v)) 2^{C Phi(log L(v))}; space v 2^{C Phi(log L(v))} | CRT, occupied short Fourier, phases, exact rounding/carry |
| Chunk count | r=2^(C4 h+C5), h^3 approximately (x+1)^2 ceil(log(x+2)) | Integer comparisons; r<=n guard |
| Common cap | Setup n/16; fixed O(n) visited regions; quadratic actual-step clock | Abort before crossing marks; clear; exact schoolbook fallback |
| Final envelope | log H=O(Phi(x)) | r^2 products plus O(nr) positional assembly |

The outer short-axis primes are separate from the composite address radix.
Their existence has one fixed source cutoff and actual coprimality/shape
tests. This construction imports the source short O(k log k) multiplier;
it does not use its own claimed near-root bound as a subroutine.

Admission requires the complete proof and reviews, not this ledger alone.
No numeric practical threshold, full machine execution, formal refinement,
human refereeing or literature priority is asserted.
