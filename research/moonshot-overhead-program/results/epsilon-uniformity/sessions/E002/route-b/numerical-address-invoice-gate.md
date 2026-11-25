# Separate pointwise work from the numerical address-change invoice

Status: **source-specific refined invoice and conditional improvement gate;
independent review requested**. This does not improve the admitted global
envelope. It locates the physical cost that a stronger construction must
reduce, instead of treating every polynomial-m operation as equally costly.

Pins: OpenAI math 3344da59991ed94f9ba711217b29c1d760badfa6,
Fourier kernel.tex, especially endpoint transforms and sharing of queries;
tape walsh.tex and permutations.tex. Programme suppliers are the small
Newton predictor, rational finite contraction, and growing-arity circuit.
E002 supplies on-demand rational scalars and actual tape address processors.

## 1. Define the charged quantity before bounding it

Consider one completed numerical template at arity
\(A_m=2(m+D_m-1)\), on active width \(a=A_m f\), with even f.
Let C_m be the sum of the input bit volumes of all ordinary calls
to the completed exact interchanger on f-bit fields, divided by
the template's original bit volume V. Include the packed-XOR
implementations of binary coordinate shears. Keep their common
O(log k) guard factor outside C_m. These are ordinary work relative
to the numerical Walsh recursion.

Separate the bounded number of whole-half boundary exchanges, whose
field width is O(a), and all scalar/phase/row arithmetic. The latter
has polynomial-m work per volume but no square-root active-width
factor once record width and short arithmetic are paid.

If the exact interchanger has
\[
 T_I(u,V)\le V\sqrt{u+1}\,E_I(u),
\]
where E_I is monotone, the numerical local cost consequently is
\[
 V\left[m^K+C_m\sqrt{f+1}E_I(f)
           +\sqrt{a+1}E_I(a)\right]\operatorname{polylog}(k).
                                                               \tag{NI1}
\]
Direct even remainders and on-demand scalar tables belong to m^K.
Whole-half exchanges arise from equivalence of the query product
and the normalized Walsh target. Finite contraction sums their
volume coefficients geometrically, so their normalized mass is
bounded independently of m.

## 2. A finer bound in the retained source implementation

Let N=q^L be the number of numerical labels. Let lambda bound total
source or destination incidence per label, including charged rectangles,
and let N_ch be the number of charged rectangles. The source's chosen
parameters satisfy
\[
 mN_{\rm ch}/N\le C,\qquad
 R_m:=C_1 D_m(1+\lambda),\qquad
 \log R_m=O(\sqrt{\log(m+2)\log\log(m+4)}).
                                                               \tag{NI2}
\]
Changing harmless absolute constants in the definition of R_m is allowed.

For query j, the source coordinate map uses j and D_m-1 auxiliary
slots in each half. Every other distinguished slot stays in its
original order. Thus the binary coordinate matrices have dimension
at most 2D_m, not 2m. Gaussian elimination writes each invertible
such matrix as O(D_m^2) XORs and field exchanges on f-bit slots.
The same bound covers paired auxiliary bases and coset representative
changes. The complete third slot needed by bulk XOR is available
among the other occupied axes and is restored.

Once-prepared free endpoint bases contribute O(D_m^2 lambda) to
the volume-normalized count at one pencil stage. The middle
source/destination coset maps are repeated for m queries and cost
O(m D_m^2 lambda). Charged-rectangle source/destination maps are
included in the incidence bound; their common intermediate maps
cost at most O(m D_m^2 N_ch/N). Therefore one stage has
\[
 C_{\rm pencil}\le C mD_m^2(1+\lambda).              \tag{NI3}
\]
This count follows the source shared-endpoint order; it does not
recompute a Fourier endpoint separately for every query.

The rational Newton predictor uses O(sqrt m) pencils, and repair uses
two predictor evaluations. Its finite contraction has total child
mass 1/4, so ordinary work over the unrolling has a bounded geometric
sum. The direct leaves use billed numerical axis calls rather than
new uncharged full transforms. Hence the retained implementation gives
\[
 C_m\le C m^{3/2}D_m^2(1+\lambda)
        \le C m^{3/2}R_m^2.                         \tag{NI4}
\]
Together with NI1 and f<=a/(2m), the coefficient of
\(V\sqrt a E_I(a)\) is at most \(mR_m^2+O(1)\),
apart from fixed logarithmic factors. This is sharper than one
undifferentiated m^K multiplier. It still has a fixed positive
power of m, so it does not change the exponent of the optimized
variable-arity envelope.

NI4 is an upper invoice. It is not a lower bound on this execution
or on all possible implementations. In particular the assertion
that m distinct middle maps appear does not prove that their data
movement cannot be shared.

## 3. A concrete sufficient improvement gate

The following would remove the independent numerical arity obstacle:
\[
 C_m\le \sqrt m\,
 2^{C\sqrt{\log(m+2)\log\log(m+4)}}.                 \tag{NI5}
\]
It must be supplied by an actual executor for the source's
query-slot-dependent coset maps, with all temporaries removed before
numerical children. Counting them as arithmetic word maps is insufficient.

Under NI5, and the same normalized numerical child mass
\(\sqrt m\,R_m\), choose \(m(a)=\Theta(a^\gamma)\) with gamma small
enough that pointwise \(m^K/\sqrt a\) is bounded. After dividing by
V sqrt(a), NI1 becomes a local term
\[
 O(1)+E_I(a)\,
 2^{C\sqrt{\log(a+2)\log\log(a+4)}},
\]
and the recursive coefficient has the same subpower exponential.
Logarithmic widths now decrease geometrically. If E_I is of the
form \(2^{O(\chi(\log a))}\), for a monotone regular envelope chi
whose values sum along geometric arguments within O(chi at root),
iteration gives
\[
 T_W(a,V)\le V\sqrt a\,
 2^{O(\chi(\log a)+
             \sqrt{\log a\,\log\log(a+4)})}
 \operatorname{polylog}(k).                         \tag{NI6}
\]

Thus the currently admitted \(\chi=\Phi\) would remain dominant,
but a future improvement of exact interchange would no longer be
blocked by a separate slower numerical arity schedule. For example,
if chi itself had square-root-logarithmic scale, NI6 would preserve
that scale rather than return to Phi.

The analogous space premise must be checked too. The source numerical
array schedule processes rectangles sequentially, retains a constant
number of endpoint arrays, and has strict finite/spatial child-volume
contractions. At gamma sufficiently small, polynomial-m headers and
one reused rational table buffer fit the Theta(k)-bit numerical record
budget. These facts make a sharpened space invoice plausible; a proof
of NI5 must retain them and price its own additional arrays.

## 4. A tested shortcut does not meet the gate

The companion query-representative-obstruction.md proves that the
canonical common-layout schedule cannot replace every middle map
by phases and auxiliary-only reindexing while leaving the query slot
unchanged. After the first endpoint transform, that slot is the
functional \(x+H\mapsto\langle d_v,x\rangle\), which differs for
different source labels. A common unchanged slot would force all
source directions to coincide, false even in a canonical two-source
rectangle.

The gate therefore requires new physical sharing or a different
layout/kernel. It is not closed by choosing different complements
and declaring all representative changes scalar phases. This
conclusion still leaves simultaneous routing, structured batched
maps, and alternative rectangle families open.

Credits: @CubeJerry, the pinned endpoint schedule and retained Newton
construction, E002 tape processors, substantial ChatGPT multi-agent
assistance. No improved complete bound or runtime lower bound is
claimed here.
