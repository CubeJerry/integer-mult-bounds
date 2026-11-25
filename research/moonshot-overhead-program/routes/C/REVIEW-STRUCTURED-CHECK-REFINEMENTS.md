# Algebra-only review of optional structured refinements

Route C, S002, 2026-11-25. Read A's complete
`../A/power-two-degree-predictor.md` and B's complete
`../B/structured-shift-check-refinement.md`.

**Gate: PASS for finite algebra, explicit field construction and the
stated row fractions.** Neither refinement is used by the accepted Q
theorem or supplies a physical sparse executor or improved global rate.
The larger count window changes the absolute stage coefficient; Q's old
numerical call constants cannot be reused without a new invoice.

For T the least power of two at least 2b+1, T is even, so T>=2b+2.
With D=T-1 this gives floor(D/2)>=b, proving the proposed window contains
the radius-b central interval. For b=3 or 5 times ceil(sqrt(m)), the
stated m>=4096 cutoff ensures D<=m and D=O(sqrt(m)).

The full-range Lucas product is a formal distributive identity. Assigning
bit and carry i length budget 2^i makes every addition degree a power of
two. Identity-padding preserves all cyclic products, including zero
leaves. The final non-dyadic length D is formed only by concatenation.
Thus all sum twists can be one in characteristic two and all predictor
coefficients stay in F4; the row dimension is a power of two.

The bounded irreducible-polynomial enumeration over F4 is valid. Every
reducible monic degree-e polynomial has a monic factor of degree at most
e/2. A degree-e irreducible exists because the proper-subfield union in
the field of roots of X^(4^e)-X has size less than 4^e. Enumerating
4^e candidates and O(4^(e/2)) trial divisors has the claimed polynomial
cost in 4^e. No larger scalar-alphabet truth table is used.

If P=diag(p_beta) tensor I_w, the actual exceptional rows are exactly
whole shift blocks, or contained in a known union of such blocks.
For H=H0 tensor I_w, the needed left inverse and transpose right inverse
are the shift-space matrices tensored with I_w. This proves correction
for the structured sets, not arbitrary s*w defective row positions.

Nonproportional vectors in F3^r give pairwise-independent uniform dot
products. Including a basis makes the seed-to-shift map injective. The
least r gives 2m+1<=B=3^r<6m+3. Each ternary digit has mean one and
variance 2/3, so the radius 5ceil(sqrt(m)) has defect fraction at most
2/75<1/32 for every fixed frequency.

The floor guard is exact: for B>=219, 11B>=2400 gives
B/32-1>=2B/75, hence floor(B/32)>=2B/75. With v=32w, R=Bv and
s0=floor(B/32), the check budget S=R/32 leaves exactly
(B mod32)w extra rows beyond s0*v. Zero-padding those paid internal
checks does not create additional independent parent inputs. Each phase
has exactly 2S=R/16 slots and the four-child mass remains 1/4.

Only B distinct check nodes are now needed, so e=ceil(log_4 B)=O(log m)
suffices, with polynomial-B field construction. The complete 3^m
spectral table remains exponential and the independent module width w
is still large. Both notes retain those costs and expressly leave
physical module-index movement, sparse execution and growing-arity
consequences unproved. The accepted Q theorem and its constants are
unchanged by this optional algebra-only gate.
