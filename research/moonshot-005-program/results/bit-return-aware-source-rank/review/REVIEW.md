# Independent review of the one-source return-rank formula

**Verdict: accepted as an arbitrary-field linear algebra theorem with the
stated fixed-word, fixed-other-sources interface.** This review imports and
executes no author checker. The attached finite verification uses GF(4),
whereas the author checked binary and ternary cases.

The precise statement is the minimum of
`rank[M0, A+C F+D L]`, with `rank F=m<=b`, for fixed matrices M0,A,C,D. All
output coordinates must be present in those matrices. No selected receiver
constraint is retained unless separately imposed; no global optimization
across changing donor interfaces follows.

## Proof checks

1. Quotienting by `im M0` is exact for rank with the actual M0 columns
adjoined. Optimizing the unrestricted L then permits a second quotient by
`im D` in that quotient. A section of the resulting image attains the
quotient rank, because each unwanted D component can be removed column by
column. The cost is `rank M0`, **not** `rank[M0 D]`: this argument does not
supply D as a free bank of return columns.

2. Set W=`im[M0 D]` and V=`im Cbar`. A full-rank source F makes Cbar F
surjective onto V. Conversely every such surjection lifts to a full-rank
F: lift its r independent quotient rows and extend them by m-r rows in the
kernel coordinates of Cbar. The needed source dimension is exactly m<=b.
Rank-deficient C and zero dimensions cause no exception.

3. For a map G onto V, let H=Abar+G, z=`rank(Abar mod V)`, and
K=`ker(Abar mod V)`. The image of H outside V has rank z, while the part
inside V is precisely H(K). Thus `rank H=z+rank(H|K)`. The restriction
Abar(K) has dimension a-z. If H(K) has dimension k, G(K) has dimension
at most a-z+k, and the z complementary input directions contribute at
most z further dimensions. Surjectivity therefore requires r<=a+k.
This proves the additive lower bound `z+max(0,r-a)`.

4. Attainment is valid over the original field. Write K as t=a-z directions
mapped independently by Abar and b-a directions in its kernel. Use
k=max(0,r-a) of the kernel directions to supply k new V directions modulo
Abar(K), make H zero on the other K directions, and choose G on a complement
of K to fill V. The needed inequalities are k<=b-a and r-(a-z+k)<=z;
both follow directly from r<=m<=b. This constructs H of rank z+k.
No genericity argument or field-size assumption is being hidden.

5. The native interpretation correctly insists on full actual transfer
maps. In particular, unused basis-completion source owners or residual H
holders can have downstream effects. Omitting such columns changes C and
can invalidate an application. Matching the source inverse at Hub changes
no Y transfer only after the actual chronology has been verified. The
formula alone does not establish that a proposed interface meets those
conditions, nor does it make source-selection or compilation costs free.

## Independent finite checks and controls

`check.py` implements GF(4)=F2[t]/(t^2+t+1), row elimination, matrix products,
and direct enumeration of admissible full-rank F and late L. It checks an
exhaustive scalar-output family, an exhaustive two-output/one-input family,
and additional fully enumerated completion problems for reproducibly
sampled boundaries with deficient C, nontrivial M0 and D, empty dimensions,
and wider inputs. Enumeration may stop when the universal lower bound
`rank M0` is reached; that stopping rule does not use the proposed formula.
The exact counts and proof hash are in `output/RESULT.json`.

The controls distinguish addition from an incorrect maximum of the two
terms, show that dropping full-rank F changes the answer, and exhibit a
selected target that forbids the unconstrained optimizer. Finite checks
support the written proof; they are not its universal justification.

```sh
python check.py --proof /path/to/return-aware-source/PROOF.md --out output
```

This theorem may identify an exact marginal improvement for a fixed native
word, once C,D,M0 are independently built. Such a result cannot be summed
over donors without recomputing M0 after each change. A marginal obstruction
would not be a global source impossibility theorem. No new kappa is proved.

Independent review: Worker B, with substantial OpenAI assistance.
