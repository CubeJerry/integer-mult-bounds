# Independent review of the power-of-two predictor refinement

Result: **PASS for the stated finite representation interfaces**.
Read `../A/power-two-degree-predictor.md` in full during S002. This
review does not change the accepted global theorem or its call constants.

The choice T>=2b+1 and D=T-1 gives an odd D with
floor(D/2)>=b, so the recentered window contains both count tails used
by the original estimate. Its degree remains O(sqrt m). The factorization
of the complete truncated sum into

    product_(i<t)(1+(omega-1)^(2^i) B_i)

is a formal distributive identity, not merely an identity on Boolean
inputs. Each B_i has budget 2^i. Its carry recursion uses products of
two equal budgets and additions at that doubled power of two; bit outputs
and constant offset additions retain power-of-two budgets. The displayed
outer factors also add at power-of-two budgets. Concatenating them gives
length D without any degree-D addition. The scalar prefactor is absorbed
in one factor.

At a sum gate the two tensor operators commute when xi=1. Frobenius in
characteristic two therefore gives their sum's required 2^i-th power.
The total-grade restriction and cyclic identity are unchanged. All
predictor coefficients lie in F4; every sum multiplies width by a power
of two, so the completed module width is also a power of two. No odd-order
root is being assumed to exist for this step.

For repair, e=ceil(log_4 R) gives 4^e>=R and 4^e<4R. Enumerating monic
degree-e polynomials and dividing by every monic polynomial of degree
at most e/2 detects reducibility and costs R^{O(1)} work. The stated
existence proof through X^(4^e)-X is valid, including the proper-subfield
count; degree one is handled separately. Thus this is a bounded actual
constructor, not an irreducibility oracle. Distinct coordinate nodes have
unit differences in the resulting field, and every scalar operation has
ordinary polynomial-e coordinate cost. No field-element truth table is
needed.

The extension degree is polynomial in m because log R is polynomial in m.
This reduces scalar-coordinate size but leaves the exponential row module,
expanded finite operations and existing physical-profile bottlenecks.
The larger window changes the absolute stage coefficient, so the old Q3
constant is correctly left untouched. No additional whole-input rate is
claimed or inferred.

Credits: A's refinement; the previously reviewed cyclic and repair
interfaces; Jerry Chen (@CubeJerry); AI-assisted independent review.
