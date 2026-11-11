# Independent adversarial review: target BIT bootstrap

Verdict: PASS for the stated strict three-cost interface, subject to its
explicit retained physical/compiler/stock premises. No supplier, new kappa,
or unconditional multiplication theorem is established. Reviewed sources and
author artifacts are pinned separately in REVIEWED-FILES.json.

## Independent derivation

Set d=C-b>0. The main saving is A=C-rho*d. The full root bill also includes
the linear adapter (saving rho) and stock exchange (saving1-rho). Thus the
maximum of min(rho,A,1-rho) is at the crossing rho=C/(1+d): the first two
terms bound every other rho. Because C<1/2 and b<C, this crossing lies below
1/2; stock does not lower the optimum. Strict source separators make it a
supremum. The directly solved rho interval is

    C/(1+C-b) < rho < min((C-B)/(C-b),(1-C)/(1-C+b)).

It is nonempty exactly for b<B<C/(1+C-b). This independently reproduces
the one-stage result and its strict inverse C>B(1-b)/(1-B).

For depth, apply the rational matrix [[0,C],[-1,1+C]] to the numerator and
denominator of the old saving. Its projective action is the one-stage
supremum. Its eigenvalues are1 andC; equivalently it multiplies the cross
ratio (C-x)/(1-x) byC. This gives the proposed exact finite-depth law,
including h=0 as the existing backend. Monotonicity and density of rational
strict witnesses prove supremum attainability from below at every fixed depth.
No input-dependent number of stages is used.

The portfolio bound follows by induction on a finite acyclic tree: every
eligible covered C_j<=C_max and predecessor b_j is bounded by the monotone
one-step map at C_max. This says nothing about a new coupled recurrence.

## Source and cost correspondence

DELAYED-COVER-BRIDGE section8 explicitly pays all three powers and uses
rho>A and rho<1-A. It does not require rho>C; later source receipts use that
as a sufficient choice. The stock count remains O_fixed(e^rho log e)=o(e).
The remainder toll is bounded by the paid stock term. Each changed fixed rho
still requires the source primitive/stock contracts and a fresh finite cutoff.
The reviewed theorem correctly treats these as premises, not a constructed
all-width implementation. The ordinary backend must be completed, preserve
spectators and restore its own ROW stock; an exponent alone is insufficient.

## Target checks and independent lift proof

From selected b=.00385248, one stage at target1/200 requires
C>3112961/621875000. Covered C=.0050001 is below that threshold, but two
matrix steps exceed target. The proposed rho=.0051 witnesses have all four
strict gaps positive. Frozen selected covered .0038525298 cannot reach target
at any finite depth; fixed rho=.004 separately cannot pay the adapter at target.
These are source-interface limitations, not universal BIT lower bounds.

For L(k)=7^(1-k)+3^(1-k)+5^(1-k)-9^(1-k)-4^(1-k)-2, L(0)=0.
Uniformly on 0<=k<=K=.0051, use exp(-k log r)>=1-k log r on positive
derivative terms r=9,4, and r^(1-k)<=r on negative terms r=7,3,5. This gives

    L'(k) >= sum_(r=9,4) r(1-K log r)log r
             -sum_(r=7,3,5) r log r >19/200.

Independent range-reduced rational atanh enclosures prove the final bound;
its approximate value is .0950003738. Therefore L(k)>(19/200)k for k>0.
This avoids the author's exponential Taylor code and repairs the old coarse
guard without claiming new supplier admission.

## Tests actually run

check_independent.py imports no author scientific code. It checks450 exact
matrix/cross-ratio cases,5,000 rational full-cost comparisons, the exact target
inverse and both strict witness stages, plus eight source Git/SHA256 pins.
Normal and -O runs produced byte-identical receipts. The author verifier also
completed separately; that rerun is supporting evidence, not the independent
mathematical argument. Controls isolate omission of the adapter, zero strict
slack, omission of stock, and substitution of the older tied affine recurrence.
An initial adapter-control fixture used too-small C and was corrected to .00501
so it actually isolates the missing adapter rather than failing the main term.

## Novelty and limitations

BagMan9's #768 bootstrap-depth-audit already establishes finite-depth envelope
and inverse-budget reasoning for a tied covered/atom recurrence. The T37 audit
reuses it. The author added explicit credit after review. The distinct result
here is the decoupled covered-C/atom-rho optimum and current .005 target binding.
No exhaustive literature-priority claim is made. Native, owned-erasure,
compiler, precision/tape and analytic-recovery hypotheses all remain.

Prepared by a separate OpenAI-assisted reviewer for @CubeJerry. This is
independent model-assisted reasoning, not independent human or kernel review.
