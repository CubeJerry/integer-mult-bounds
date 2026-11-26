# Independent review of the odd-characteristic order-four closure

Disposition: **accepted finite algebraic component and conditional
shared-swap call interface**. A read C's complete
`ODD-CHARACTERISTIC-ORDER-FOUR-CLOSURE.md`, its checker, the source tape
`interchange.tex` shared-pencil and spectral-conversion sections, and
the already reviewed p-power-only compiler. No whole odd-characteristic
adaptive interchanger or multiplication theorem is admitted by this review.

## 1. Matrices and required units, including characteristic three

Every nonzero element of F_p is a square in F_(p^2), since p-1 divides
(p^2-1)/2 for odd p. Thus both r and i exist. Their values and r+1,r-1
are nonzero: r^2=2 and r^2-1=1. With R=i(r+1), the identity
`R^2-1=-2r(r+1)` shows R and R+1,R-1 are nonzero. Every displayed
diagonal and all denominators in O4-1--O4-3 are therefore units for every
odd p. There is no hidden exception at p=3.

I independently multiplied the factors:

    H B H = [[R,1],[1,R]],
    A C B C J = [[1,1],[i/R,iR]]
              = [[1,1],[r-1,-r-1]].

The columns have H eigenvalues r and -r. The displayed inverse follows
from det(S)=-2r and `1/(2r)=r/4`. Hence T C S=diag(i,-i), with the
inverse word in the stated reverse order. Also H E H=2Q and a^2=-1/2,
so C E C=-Q exactly. These are identities over the field, not assertions
inferred solely from a finite list of tested primes.

## 2. Actual single-swap pencil contract

On a nontrivial physical orbit, C=a(Q+U-L). On a fixed point its separate
definition is C=1, giving O4-4's `(1-a)K` adjustment. The conventions for
**every** individual diagonal factor at equality are essential: evaluating
an off-diagonal-orbit scalar there would invalidate the global words.

The pencil reduction has constant spatial coefficients in the expensive
part. Writing B_j=A_(j,1)-A_(j,3), its shared-swap part is

    A_0-sum_j A_(j,2) + sum_j a B_j Q_j.

Its remaining terms are precisely

    sum_j [a B_j(U_j-L_j)
       +((1-a)B_j+2A_(j,2)+2A_(j,3))K_j].

This matches direct expansion of C^2=-I+2K and C^3=-C+2K. Crucially,
the comparison projectors occur only in the separately applied pointwise
summands. The original input can be retained while the shared Q pencil
returns in original physical order, then those pointwise summands added.
Scalar row maps commute with spatial projectors. Therefore no mask must
be evaluated after, or transported through, a label-dependent endpoint
map. This meets the source's fixed-row-coefficient shared-pencil
contract; it is not the invalid substitution of address-dependent
coefficients into that contract.

The ordered comparison runs are exactly the source's earlier-field / full
later-field scans, with arbitrary prefixes and suffixes. Their physical
control cost is still charged. A polynomial number of pointwise passes
and a constant number of retained payload arrays suffice for this
reduction; the nontrivial row-program description and arithmetic costs
remain whatever the separately supplied compiler proves.

## 3. Full converter words and finite repair

Different coordinate pairs are disjoint, so their operators commute.
This justifies regrouping the product of local S words into
`A_all F B_all F J_all`, and the product of inverse words into the
stated two F^(-1) phases. No diagonal factor has been commuted past its
same-pair C. At the completed forward interface, the address ordering
places eigenvalue i at the smaller orbit member, -i at the larger, and
1 at equality. Inverse-query exponents are obtained by negation modulo
four. The repair table belongs between the complete words.

The F^(-1) children use a separately constructed predictor for the
commuting queries C_j^(-1)=C_j^3. Its spectral exponent is -k_j modulo
four. The same shift family, degree window and padded length apply;
its affine query powers are just the four original powers in reversed
order. Thus O4-4a supplies the same single-swap price. These children
are not implemented by three completed F calls, and no inverse execution
is declared free. The finite unrolling is a simultaneous induction for
the two target families F and F^(-1), with the same upper call invoice
at depth h and the direct m-swap base for each. Every converter child
has depth h-1, so this mutual closure is terminating, not circular.

For the checks, V is the square Vandermonde on the actual containing set.
Its inverse exists because nodes are distinct. Predictor values and the
target multiplier lie in the F_(p^2) subfield, so h(g)=g^(p^2-2) is inverse
on nonzero gaps and zero at zero. The transpose-lift restriction on the
containing set is exactly `diag(h(g))e`, hence equals X on every nonzero
gap and need not equal X elsewhere. Outside the containing set the
original gap is zero. Consequently PX-PZ+FZ=FX on every independent row,
including containing-set rows with accidentally zero gap.

Each of the two check families has s w rows, with s=B/32 exactly. Every
completed converter has two target phases. Forward and inverse together
therefore give four sequential children, each on `2s w=Bw/16` raw rows.
Their total volume is one quarter of the parent. The independent module
w is tensor-preserved and is never counted as initialized workspace.
Finite unrolling multiplies stage mass by the geometric series
`sum 4^(-ell)` and leaves the direct m-query term `m 4^(-h)`. A direct
C or C^(-1) uses one copied swap and pointwise maps, so the leaf price is
correct. The final extraction `M_all F E_all F` has two full target
calls and returns the complete physical swap on all occupied fields.

## 4. Count syntax, field construction and limits

Mapping pairwise independent F_4 linear values bijectively to four
ordinary digits preserves uniformity and pairwise independence. Addition
of a fixed spectral exponent modulo four preserves them again. Thus the
count has mean 3m/2 and variance 5m/4. The stated window has outside
fraction at most 5/196<1/32, and its degree D is at most 14sqrt(m)+3.
For sufficiently large m this meets D<=m. A minimal projective-direction
seed family has B=4^r=O(m), and B is divisible by 32 for r>=3.

The four projectors are affine in the four powers of C, using 1/4.
These powers can be treated as commuting affine query symbols by the
formal count compiler and then substituted by the physical operators.
At p=3, the initial digit representing shifted value 3 must have a high
digit equal to its projector. This detail is explicitly included; merely
reducing the value modulo three would be false. Both initial digit
functions have constant-size affine formulas, so the balanced carry
recurrence and actual padded p-power budgets retain the same size bound.
Generalized Lucas handles negative offsets as in the p-power review.

On the central interval the ordinary binomial identity evaluates O4-7
to `i^(u-sum beta+c-u)=i^(sum k)`. Outside it, arbitrary predictor values
are permitted and are covered by repair. The root length L is the least
p-power at least D, not D without padding; its factor-p inflation and
`m^{O(1+log p)}` formula syntax are both retained. The addition compiler
works over the characteristic-p coefficient field containing i without
adjoining prime-to-p roots for its sum gates.

For 3<=p<=m, the least positive even e with p^e>=B satisfies
`p^e<p^2 B=O(m^3)`. Exhaustive enumeration of monic defining polynomials
and trial factors is consequently bounded by a fixed polynomial in m;
elementary field operations and searching for the two roots have the
same kind of bound. The even extension contains the unique F_(p^2)
subfield and has enough distinct nodes. Thus this is an effective finite
field choice, rather than an unpriced irreducibility oracle. The claim
does not require a polynomial-m bound independent of p when p>m.

The theorem remains a finite component. A growing odd-characteristic
geometry, actual endpoint/row compiler, batching, numeric address units,
payload encoding and common visited-space coefficient still need their
own uniform bounds. The finite-alphabet packing lemma applies only at
completed physical permutation boundaries. It does not authorize
repacking arbitrary intermediate values inside an unfinished F word.

## 5. Final isolated verification

Read the final added projector, Newton/Lucas and repair tests, then copied
and ran the stable checker in `order-four-review-replay/`. Its SHA-256 is
`a8fb4c5d98a1dec843294438fdf751aa9eb0ce7f520551b1ecd98272739575b8`.
The isolated receipt and result JSON are retained beside the copy.

The replay passed 192 matrix identities over p=3,5,7,11,13,17,19,31,
testing every root pair. On complete physical orbits it passed 251,136
global-word outputs and 62,784 arbitrary two-row pencil outputs, with
both equality and nonequality, suffix spectators and a complete basis
check for the smallest shape. Forty-eight controls detect missing signs
and wrong fixed-point treatment.

The additions passed 28,600 count/offset/Newton/Lucas cases, 32 spectral
projectors and the omitted base-three high-digit control. Exact repair
tests passed 6,912 corrected output entries, 96 containing sets with a
zero actual gap, 288 examples where the lift is nonzero outside the
containing set, and 288 wrong-transpose rejections. Those last two tests
check the correct support argument: it is the original gap that vanishes
outside the set, not necessarily the lift.

The finite tests do not implement the asymptotic 1/16-volume repair
schedule or a complete tape compiler. Those are the algebraic ledger
and explicitly conditional physical interface reviewed above. No
remaining correction requested; the finite closure and its scope are
accepted.
