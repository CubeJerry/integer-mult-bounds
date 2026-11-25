# Whole-identity packing over arbitrary finite coefficient alphabets

Status: **proved scoped encoding bridge; independent review requested**. This does not improve AQ or its geometric invoice. It extends the uniform-payload interface beyond binary field coordinates and identifies precisely where linear basis descent is unnecessary. The elementary encoding principle is not claimed as a new general coding theorem; the contribution here is the occupied-row, fixed-tape and recursive-call accounting for this programme.

## 1. Algebraic boundary and explicit representation

Let A be a finite coefficient algebra of cardinality Q>=2, with an explicit canonical enumeration by integers0,...,Q-1. Arithmetic and conversion to that enumeration must have a paid fixed algorithm. In the intended parameterized application, log₂Q and all operation/description bounds are polynomial in the finite parameter m, with absolute degrees. Listing Q elements is not assumed or permitted merely because A is finite.

Examples include a finite field, or a finite free quotient F_p[T]/(f) for monic f of degree d. The latter has Q=p^d regardless of whether f is irreducible. The base-p coefficient vector gives a canonical index in[Q]. Conversion and ordinary polynomial arithmetic have polynomial bit cost in d and log p, without enumerating the p^d elements. The lemma assumes the scalar program is already correct over its chosen algebra; it supplies no missing inverses or specialization theorem.

Suppose a completed program on W arbitrary independent A-valued rows and a complete physical range Omega has the identity

    P(X)_(r,omega)=X_(r,pi^(-1)(omega)),                (FP-A1)

where pi is the desired spatial permutation and r in[W] is unchanged. The internal operations may mix rows and use arbitrary coefficients in A. Only the completed whole-row identity is required.

Put b=floor(log₂Q), s=ceil(log₂Q). Thus b>=1 and

    1<=s/b<=2.                                         (FP-A2)

Q a power of two gives equality1. Otherwise s=b+1. Both integers are computed from Q's binary description.

## 2. Occupied binary rows and correctness

For each r and omega, pack b independent bits x_(r,c,omega), c in[b], into the coefficient symbol with canonical index

    index=sum_(c=0)^(b-1) 2^c x_(r,c,omega) <2^b<=Q.

Store its canonical index in s bits. This is an injective map from all2^b bit patterns. No binary input row is zero-initialized, fixed, ignored or discarded. The scalar program may leave this subset during execution.

**Lemma FP-A.** Applying the complete program FP-A1 and decoding the final canonical indices applies pi independently to all bW binary rows. Encoded bit volume is exactly(s/b)V, where V=bW|Omega| is the original binary volume.

**Proof.** FP-A1 moves each complete coefficient value unchanged from pi^(-1)(omega). Therefore its final index is again below2^b and its b binary digits are exactly the corresponding input bits. This is valid for every independent bit input. No additivity, F2-linearity, subfield embedding or coordinatewise action of intermediate maps is used. QED.

The distinction from basis descent is substantive. Addition in an odd-characteristic algebra need not implement XOR on the packed bits. This lemma transfers a completed spatial permutation, not an arbitrary coefficient-linear transform. Decoding before the whole identity completes may lose information: intermediate values can have canonical index at least2^b.

## 3. Actual fixed-tape packing for arbitrary b

The input order is `(outer prefix,row[W],coordinate[b],physical address)` and the encoded order is `(outer prefix,row[W],physical address,record bit[s])`. An arbitrary positive outer prefix and additional physical spectators are allowed. Unlike binary basis packing, b need not be a power of two.

Initialize an encoded output region of volume(s/b)V to zero. For c=0,...,b-1, make a complete input scan and extract the c-th coordinate stream in(row,physical-address) order. In a second aligned scan, copy the current encoded region to an alternate region, replacing bit c of each s-bit record by the extracted bit. Preserve all other record bits. Reuse the two encoded regions and one extraction region. After b passes the desired index records have been written. Their unused high bit, when present, is zero.

Each pass costs O(V+(s/b)V), including reads, writes, rewinds and clearing. The total is O(bV+sV)=O(sV). Only an absolute number of regions of size at most2V coexist. The coordinate and within-record counters have O(log s) bits. Long outer/row/physical counters advance amortized; the scanner does not read a full physical address per bit. Descriptor preparation has its separately paid fixed polynomial degree in log(V+2) and the finite parameter. A fixed number of ordinary tapes suffices.

More explicitly, the input scan for a fixed c uses three consecutive runs in each row: skip c|Omega| bits, copy |Omega| bits, then skip(b-1-c)|Omega| bits. Output records similarly have three known runs around bit c. Initializing a positive run counter costs at most a constant times the run it controls, since log(r+2)=O(r) for r>=1; zero runs are omitted. Thus a log s comparison is not repeated for every input bit. The arbitrary outer prefix simply repeats this schedule and multiplies both volumes by its size.

Unpacking reverses the layout using the same b complete scans and reusable regions, taking the low b bits of each final index. FP-A1 guarantees the discarded extra high bit is zero at this boundary. The output is restored to the original b independent rows and original volume.

Consequently if s<=poly(m), packing and unpacking cost poly(m)V plus additive descriptor work, with an absolute O(V) payload-space coefficient. This bound does not expand a non-power-of-two coordinate index to the next power of two or request b tape heads.

## 4. Spatial recursion and the honest volume price

A scalar program may call a binary spatial interchanger on its encoded records, treating the s-bit coordinate as a suffix spectator. The child's own codec may use another finite algebra. Its completed operation returns exactly the requested permutation of those bits, so the parent's canonical scalar records are restored correctly. Intermediate child bits need no interpretation in the parent algebra.

To expose W scalar rows, a leading-row batch must supply bW independent binary rows. Set ell=ceil(log₃(bW)). Pad3^ell leading rows to the least multiple of bW. The leading-range factor beta is less than two, and log(bW) remains polynomial(m) when log W and s do. This is the same paid packed-leading construction as PB, with a different finite row count.

Let alpha=s/b<=2. If the scalar template's normalized recursive call price is Q_m, its binary-input price becomes alpha beta Q_m<4Q_m. The factor alpha is real and must be charged; this lemma does not claim exact volume equality for odd Q. Ordinary work and local payload space also acquire only an absolute factor. No per-level factor depending on log Q remains.

If each scalar main child has volume at most gamma of the scalar main parent and gamma<=1/16, its incoming binary volume is at most alpha beta gamma V<=V/4. Thus constant-array local work still has an absolute geometric parked-volume sum. A finite repair tree keeps its scalar algebra fixed and retains its existing relative child fractions; it does not repack at each repair phase.

For any full-volume reserve descent, decode at the completed permutation boundary and clear main scratch before handing over the original V-bit region. This condition is necessary: leaving an expanded parent representation parked across a full-volume chain would require separate accounting. The current source main/reserve decomposition has a complete ordinary main-field permutation at that boundary, so decoding is legal there. The lemma does not assert this property for an arbitrary unfinished scalar circuit.

The absolute factor four in the recursive main-call invoice changes constants in an adaptive bound whose logarithmic widths contract geometrically; it contributes only O(number of levels) to the logarithmic product. It also changes a fixed-exponent acceptance margin and must be included in that margin. It is not silently ignored as a data-field constant.

## 5. What the bridge does and does not supply

The whole-identity permutation boundary, explicit canonical arithmetic and small bit-width assumptions are the actual requirements. The coefficient characteristic need not be two; a finite free algebra need not even be a field. This removes an encoding obstacle for future odd-characteristic or quotient-algebra executions without licensing factorial division, nonexistent scalar inverses, false low-rank label claims, or a numerical circuit specialized into an incompatible characteristic.

This bridge does not construct a new scalar predictor, label family or cheaper delivery schedule. In particular it does not evade the current literal-invoice obstruction and does not improve AQ. Binary field basis packing remains preferable for the admitted construction because it has exact volume equality and fewer digit passes. The present result is a wider, independently checkable interface for later constructions.

`verify_finite_alphabet_packing.py` tests literal coordinate-pass packing, independent bits, a complete mixing/permutation/unmixing program over odd prime fields and a ring with nilpotents, and two different codecs in nested spatial calls. It includes premature truncation and incomplete-identity controls. These tests illustrate the boundary conditions; the general statement is proved above. No full multiplier or formal-kernel proof is claimed.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance. This extends the session's B full-rate field-packing interface using ordinary injective coding and complete-row permutation identities. The source elementary-stream and packed-batch credits are retained. General binary encoding is standard; no broad novelty claim is made.
