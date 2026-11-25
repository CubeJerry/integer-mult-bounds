# Independent audit of dense recurrence residual correction

**Verdict: pass for Theorems H1 and H2 as promised-component results.**
Reviewed the complete B draft, including the lead's zero-faithful
integer-encoding extension. The construction neither certifies the
recurrence promise nor supplies a fast candidate.

## Reconstruction and arithmetic

The normalized forward convention is essential. A length-D sequence
obeying an order-s recurrence from index s has generating series P/Q
modulo X^D, with deg P<s, deg Q<=s, Q(0)=1. The difference of two such
series has numerator degree below 2s. Thus agreement on the first 2s
coefficients proves equality in the promised prefix. This validates any
consistent solution of H5: extend it using the first s terms, compare
its first 2s terms with the true sequence, and invoke uniqueness.

A nonsingular rank minor with free variables zero gives one common
determinant denominator of height O(s(tau+log s)). Fraction-free
preparation has polynomial entry heights and fits O(K^6) time and O(K)
storage. There is no product of independently formed denominators.

The small-prime proof is valid. Each binomial coefficient in row L-1
divides lcm(1,...,L), since each prime valuation is a sum of at most
floor(log_p L) zero-one terms. The largest coefficient is at least
2^(L-1)/L and the lcm at most L^pi(L). At L=8(B+2)^2 this forces more
than B primes, one avoiding the nonzero B-bit denominator. Trial
division has polynomial cost in B. The selected prime power exceeds
2Emax, has O(tau) bits, and makes q_0 a unit. The coefficient ring need
not be a field.

H10 correctly advances a block: degree(Q)<=s means only the immediately
preceding block contributes to the next block's earlier positions. The
high half of Q times that preceding block supplies the inhomogeneous
term, and Q^-1 modulo X^s solves the current block. This includes q_s
and a final partial block. Centered residues uniquely recover all
bounded integer terms.

## Physical invoice and promise boundary

The first 2s product terms require one guarded short packed product.
Each emitted block uses two O(s tau)-bit products. Since log s=O(tau),
each decoded coefficient has O(tau) bits; reciprocal reduction uses a
fixed number of charged O(tau)-bit multiplications. Summing these costs
gives H11. Candidate scans, output and carries have O(V) bit volume.
The retained recurrence and reused work regions have O(K) volume.

The K>V branch is necessary for uniform O(V) visited space. It skips
reconstruction and uses packed schoolbook multiplication, whose O(V^2)
cost fits O(K^6). When K<=V all regions can be reused. Neither tape
count nor alphabet depends on s. The stated polylogarithmic and
subexponential-order substitutions follow directly from the bound on K.

The X^(2s) control correctly rejects an unrestricted prefix certificate.
The terminal-spike example correctly separates finite Hankel rank from
normalized forward recurrence. Fingerprints and boundary-degenerate
rank cannot replace H1 without a new proof.

## Supplier obstruction

Projection to the first s terms is injective on a linear subspace all
of whose vectors have their own order-at-most-s normalized recurrence.
A kernel vector has s initial zeroes, and its own recurrence forces
all later terms to vanish. Recurrence coefficients need not be shared
or input independent. Applying the same projection on W rows gives
rank at most Ws.

The zero-faithful integer encoding extension also passes. A field
vector in the prefix kernel encodes to an integer zero prefix; its own
rational recurrence forces the entire encoded sequence to vanish;
zero faithfulness forces the original vector to vanish. The linear
prefix map and dimension count stay over the original field, without
reducing recurrence denominators into it. A changed order, bit stream,
or nonlinear residual needs a separate interface. A spectral-average
rank premise additionally requires the regular representation or an
actual multiplicity check, as the draft now states.

## Isolated exact replay

An isolated copy of the self-contained checker passed 36 complete
integer recovery cases, 37 rational reconstructions, 697 packed products,
330 emitted blocks, 80 small-prime bounds and 72 finite-field prefix
gates. Negative controls reject three nonunit denominator choices, ten
finite-Hankel boundary examples, and an unrestricted prefix certificate.
Cases include dense periodic, polynomial, Fibonacci and rational
dyadic-decay sequences. This is exact algebra and packing verification,
not a fixed-tape runtime simulation. The final copied checker uses
integer square roots in primality bounds.
