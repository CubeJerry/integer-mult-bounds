# Independent review of sharp terminal alignment by reseeding

**Verdict: accept the general sharp quotient theorem and its literal serial
source equality construction.** The canonical intersection bound is5V under
the stated full-W history contract. The emitted equality word has unchanged
movement,121 additional ordinary ADDs and the same three actual outputs.
No complete decoder, supplier or new kappa follows.

The reviewed root package is `root/point-source-interface/`. Exact proof,
emitter, result and word hashes are in `MANIFEST.json`. Its baseline serial
source was independently reviewed in `review-serial-point/`; that review's
manifest is pinned. No root emitter or author checker was imported or executed.

## 1. Universal sharp quotient theorem

Work in any finite-dimensional ambient vector space over any field. Assume
N is contained in D. Define

    n=dim N, r=dim((D+W)/D), k=dim(N∩E),
    z=dim(E∩(D+W))−dim(E∩D).

The desired T obeys `N⊂T`, `dim T≤q`, `W⊂D+T`. Such a T exists exactly when
`q≥n+r`. If it exists, its maximum E intersection is

    min(dim E, k+z+q−n−r).

The statement does not require N to be in W, D to be disjoint from E, or
ordinary coefficients to be invertible. The proof uses only linear-space
quotients and bases, and is valid in every characteristic.

### Necessity and the two independent contributions

Projection modulo D sends T onto a space containing the r-dimensional image
of W. The kernel contains N, so `dim T≥n+r`. For the sharper objective, the
linear map

    T/(T∩E) -> ambient/(D+E)

is well-defined. Its kernel contains the image of N, whose dimension is
`n−k`. Its image contains the image of W modulo D+E. That image has dimension
`r−z`: z is exactly the dimension of the intersection of the quotient images
of E and W modulo D. Rank-nullity therefore gives

    dim T−dim(T∩E) ≥ n−k+r−z.

The two terms are a kernel contribution and an image contribution; they do
not assume that arbitrary representatives in the ambient space are disjoint.
Combining with `dim T≤q` and `dim(T∩E)≤dim E` gives the stated upper bound.

### Attainment

Choose z independent vectors in E whose images form a basis of the
intersection of the quotient images. Extend those images to a basis of the
r-dimensional image of W, choosing the remaining representatives in W. Add
a basis of N. The resulting T0 has dimension n+r: all r chosen lifts are
independent modulo D, and N is inside D. It supplies W modulo D.

Only the first z lifts can contribute an E vector modulo D. The remaining
lifts are independent modulo the quotient image of E. Consequently
`dim(T0∩E)=k+z`. Adjoin E vectors independent of T0 until either E is contained
or the q budget is reached. Every such vector increases both dimensions by
one. This attains the formula, including unsaturated q and nontrivial N∩E.

When `q=n+r`, every admissible T has `T∩D=N` and the same quotient image as W.
Those saturation statements follow from equalities in the size argument.
There is no unproved genericity or favorable basis-position assumption.

## 2. Fixed-source identity and block extension

The seven free serial packets add only fixed actual source rows after their
Hub seed. Their terminal is `t_i=s_i+m_i`. Neither their values nor their new
seed reads affect an original receiver, a source cache, another packet or the
fixed P4 serial interactions. Every intermediate free-packet state minus its
terminal is therefore a fixed suffix increment. Keep all fixed P4 states.

Their span D is independent of reseeding. Terminals are actual history states,
so subtraction proves both inclusions in

    H(T)=D+T.

This statement is about a span of historical observations. It does not imply
that all its vectors coexist at one chart or at one time.

At width V, interpret the fixed binary spaces as tensor products with F^V.
Every binary rank and intersection dimension scales by V. A free packet may
use arbitrary linear block seed coefficients; its terminal contributes at
most V row dimensions. No commutation between coefficient blocks is needed,
because the theorem concerns ordinary vector subspaces in the222V-column
space. The scalar equality construction tensors with `I_V`.

The attainment argument remains physically relevant as a *seed interface*:
the chosen W, C and N vectors are pure X, and each corresponding seed
`s_i=t_i−m_i` is a linear combination of actual restored Hub X originals.
This does not assert that arbitrary block coefficients have a free uniform
implementation. The emitted scalar word instead lists every actual XOR ADD.

## 3. Independently verified source dimensions

The checker forms D directly from its own actual packet history by subtracting
the terminal of every free packet and retaining the fixed P4 history. It does
not import the root's D basis. The resulting dimensions are:

| Quantity | Dimension |
|---|---:|
| D | 27 |
| Public-y projection of D | 2 |
| D∩W | 8 |
| D∩C | 3 |
| D∩C_s | 3 |
| (D+C)∩W | 13 |
| (D+W)∩C | 8 |
| D+W | 34 |

N is the line spanned by e9, lies in D and is disjoint from both C and W.
Hence the source has `q=8`, `n=1`, `r=7`, `k=0`, `z=5` for E=C. The retained
full-W requirement saturates the available quotient dimension. It follows
for all fields of characteristic two and all widths that

    dim(T∩C_V)≤5V,       dim(T∩W_V)≤7V.

A useful equivalent check is that saturation forces `T∩D=N`. The canonical
part of T meets D trivially, and injects into
`((D+W)∩C)/(D∩C)`, which has dimension5V. This separately recovers the
canonical upper bound without the unsaturated formula.

W15 is an explicit sufficient historical target for the programme's current
low-charge construction. The theorem does not impose W15 on every possible
integer multiplication algorithm. Dropping it changes the question and
requires a compatible fitting, decoder and complete accounting.

## 4. Literal equality word and full operation comparison

The actual terminal rows are

    P0=K1, P1=K3, P2=K10, P3=K11, P4=e9,
    P5=K61, P6=W0, P7=W1.

The independent replay checks these rows, all222 original columns, every
rational chart and chronological read, all original endpoints and ownership.
It separately derives111 W-history identities. It verifies

    dim T=8, T∩C=5, T∩W=7, T∩D=1,
    H=D+T=D+W, dim H=34.

Comparison against the frozen serial baseline is stronger than equal movement
counts: after deleting only contiguous Hub seed ADDs of the seven free
packets, the complete operation sequences are identical. Every non-ADD
instruction is unchanged. The extra121 ADDs are all explicit restored-X
Hub reads. The resulting closed counts are150 INIT,750 ADD,394 MOVE and150
CLEAR, including145 dirty CLEARs.

The movement profile remains

    105[1]+39[2]+23[3]+29[4]+53[5]+29[6]+115[7]+[8],

with rank length1620. Independent directed integer200th-root arithmetic again
gives moment1606.998014987781958... and limiting movement room14.752865223370397....
The extra121 ADDs are a material ordinary/physical expense. This variant is
not automatically preferable to the lower-ADD source.

The free-terminal/free-local-correction fitting list is exactly
`0,1,3,9,10,11,17,18,61,64,65,68,72`. Only9,17,34 are physically delivered.
Adjoining all of C would need four additional independent whole-width
directions. That is a code-dimension statement, not a free physical export,
not a decoder and not a claim that canonical-only cover charge meets the
marked q8/q9 bounds. The source's two noncanonical W directions remain part
of its actual terminal interface.

## 5. Independent controls

The literal source review includes ten rejecting semantic controls for public-y
prefixes, point captures, feedback, unmasking, dirty retirement, output delivery
and false chart access. They are rerun on the reseeded words.

`lemma_controls.py` independently enumerates all16 subspaces of F2^3 and all
67,584 valid D,W,N,E,q cases, with N⊂D and q from0 through3. It checks actual
feasibility and the exact optimum over every candidate T;39,888 cases are
feasible. Omitting the `n−k` kernel term is rejected, for example with
`D=N=span(e1)`, `W=0`, `E=span(e2)`, `q=1`: the actual maximum is0, whereas the
incorrect formula gives1. This is a finite control of the separately reviewed
universal proof.

A further actual-word control replaces terminal P6=W0 by a sixth independent
canonical row K5 and changes its Hub seed consistently. All three original
output endpoints remain correct, and terminal canonical intersection rises
to6, but historical W intersection falls to14. The retained-W checker rejects
that exact loss. The control is not called a physically impossible source;
it fails the particular W15 theorem premise.

## 6. Reproduction and remaining obligation

```sh
python3 -B check_independent.py \
  --repo /absolute/path/to/integer-mult-bounds \
  --package /absolute/path/to/point-source-interface/output \
  --baseline /absolute/path/to/serial-point-source/output \
  --out /absolute/path/to/review-output
python3 -B lemma_controls.py \
  --repo /absolute/path/to/integer-mult-bounds \
  --package /absolute/path/to/point-source-interface/output \
  --out /absolute/path/to/LEMMA-CONTROLS.json
```

Expected statuses are `PASS_INDEPENDENT_CANONICAL_RESEED_REVIEW` and
`PASS_INDEPENDENT_SATURATED_QUOTIENT_CONTROLS`.

The next obligation is actual joint receiver delivery with a verified
proper-cover charge and complete costs. Neither the13 algebraic fits nor the
four-direction canonical extension count supplies that delivery. All five
foundations, both strict supplier requirements and the complete recursive
assembly remain. No new kappa.

Credit: independent S015 Worker C review of Root's quotient theorem and
reseeding, Worker A's serial source, and all frozen canonical/W/native and
orthogonal-staircase predecessors; @CubeJerry attribution retained.
Substantial OpenAI assistance.
