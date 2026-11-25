# One compatible radix for a changing template menu

Status: **proved arithmetic and fixed-tape preparation component; independent
review pending**. This is not a complete multiplication theorem. The new
point is to combine E001's narrow-interval prime selector with E002's
multidigit batching. The radix need not exceed the completed batch width.
A single radix can serve an entire nonstationary recursion, with bounded
initial binary-range padding and only logarithmic radix-digit cost.

Sources: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`; programme predecessor
`a2d9c4b00c02dadf7bdc970acf9190dfabf9ec32`; focused E001
`route-c/INPUT-DEPENDENT-RADIX.md`, R1; E002
`route-c/small-radix-batching.md`, R3--R5. The external number-theory
input is the eventual Baker--Harman--Pintz short-prime interval theorem
already invoked in the tape manuscript. Its analytic proof is imported,
not reverified here, and no numerical absolute cutoff is asserted.

All logarithms are binary. Input width `u` is a binary address-field
width, not the integer-multiplication input length.

## 1. Finite menu hypothesis

For every integer `M>=2`, a fixed constructor emits the rational address
maps for all templates in a finite menu `F_M`, containing every template
which the subsequent recursion may use. Suppose absolute `C,c>=1` give:

1. Every nonzero numerator/denominator which must be invertible appears
   in a list. Its absolute product, multiplied by two, is `Q_bad`.
   Its **binary bit length** is `S<=C M^c`.
2. Full menu construction, including that product, costs at most
   `2^(C M^c)` actual binary-tape steps and visited cells. Compact local
   descriptions can be regenerated without scanning the entire menu
   during every data operation.
3. A template of arity `m<=M` has completed batch width `W_m` with
   `log W_m<=C m^c`. Its address maps are valid over every modulus
   `b^f` whenever the odd prime `b` avoids `Q_bad`.

The menu may contain all odd `m<=M` or a smaller explicit set.
Polynomially many rational maps of polynomial bit height per `m` give
the first bound after one polynomial enlargement. The scalar data field
is separate from this rational-address compatibility list.

## 2. Selector and integer tests

Choose a fixed integer `r>4c` and put `M=floor(u^(1/r))` by integer
root extraction. Construct the menu, and set

```
t = 3 bitlength(S) + 3 bitlength(u) + 13,
e = floor(u/t),
B = ceil((2^u)^(1/e)),
H = floor(B/(2e)).                                      (R1)
```

If `M<2` or `u<4t`, use the direct binary fallback. Find `B` by binary
search and exact power comparisons. Search `[B,B+H]`, test primality
by trial division, and for primes test `gcd(b,Q_bad)=1`. Return a found
prime, or report failure. These are finite exact tests; failure permits
the caller's exact fallback.

**Theorem R.** For all sufficiently large `u`, uniformly over menus with
these bounds, the selector succeeds and returns an odd prime with

```
2^u <= b^e < 3*2^u,      log b = O(log(u+2)).            (R2)
```

Every selected template is valid over every `b^f`. Total selector time
and visited space are at most `2^(C' u^(c/r))+poly(u)=o(2^u)` for an
absolute `C'`. Padding two binary address fields to these radix fields
has volume factor less than nine, uniformly in `u`.

### Proof

`S<=C u^(c/r)` implies `t=O(log(u+2))`, so `u>=4t` eventually.
We have `e>=4`, `e<=u`, and

```
2^t >= 8192 (S+1)^3 (u+1)^3.
```

Since `u/e>=t`, `B>=2^t`. Thus `B>=4e+4`, and

```
B^2 >= [16(S+1)e]^5.                                  (R3)
```

Indeed the lower bound for `B^2` has coefficient `2^26`, versus
`16^5=2^20`, and powers `(S+1)^6(u+1)^6` dominate `(S+1)^5 e^5`.
At most `S` distinct primes divide `Q_bad`.

Put `D=ceil((2B)^(3/5))+1<=4B^(3/5)`. Since `H>=B/(4e)`, (R3)
gives `(S+1)D<=H`. The `S+1` right endpoints `y_j=B+jD` lie in
`[B,B+H]`. Their disjoint intervals `[y_j-y_j^(3/5),y_j]` also lie
there. Beyond the fixed absolute prime cutoff, each contains a prime.
One of the `S+1` primes avoids `Q_bad`; it is odd since two divides
that product.

Writing `R=2^(u/e)`, `R<=B<R+1` and `B>=4e+4` imply

```
b <= B+B/(2e) < R(1+1/e).
```

Hence `b^e<2^u(1+1/e)^e<3*2^u`. There is no condition on `W_m`:
the multidigit prefix below supplies that batching capacity.

For `u>=4t`, `e=floor(u/t)>=3u/(4t)`, so `B<=2^(4t/3)+1=poly(u)`.
Trial division, compatibility remainders, root extraction and control
therefore cost `poly(u)` actual steps and space. Add the menu constructor.
Since `c/r<1`, the logarithm of its bound is `o(u)`. Finite guarded
failures cover the unknown absolute prime cutoff. ∎

## 3. Batch capacity and recursive consistency

For any selected template and current radix width `v`, use

```
ell_m = min { ell>=0 : b^ell >= W_m }.
```

Compute it by exact repeated multiplication or power comparisons. Since
`b>=2`,

```
ell_m <= 1+log W_m <= 1+C m^c.                         (R4)
```

E002's multidigit split has row-padding factor at most two and child width

```
f = floor((v-ell_m)/(m+2a_m)).                          (R5)
```

If `m<=v^beta` and `beta c<1`, the prefix consumes `o(v)` digits.
The radix is chosen once at the binary root. Children never convert
to a different radix; the root menu guarantees all their maps are valid.
The factor-two batch loss remains in the recursive call invoice.

## 4. Digit swaps cost bit length, not numeric radix

**Lemma D.** A fixed binary multitape machine interchanges two `[b]`
address fields with arbitrary prefix, gap and suffix ranges and payload
volume `V`, in

```
O(V(1+log b)) + poly(log(2V))
```

steps and `O(V)+poly(log(2V))` visited cells. Constants and tape count
are independent of `b`.

**Proof.** Pad both fields to `[2^h]`, `h=ceil(log b)`, by sequential
scans. Combined volume increases by less than four. Exchange the two
`h`-bit fields by `h` elementary single-bit field swaps, each using a
constant number of full-payload copies, amortized counters and charged
returns. Remove padding by its positions. The swap preserves the subset
where both original field values are below `b`. Reuse the same regions
in every pass. No faster interchanger or one tape per digit class is
assumed. ∎

For Theorem R's radix, leading/remainder digit exchanges cost
`poly(m) V log(u+2)`, rather than `poly(b) V`.

## 5. Scope and next question

This is a common-radix preparation/padding bridge. The nonstationary
algorithm still requires full-rate local identities, their call bound,
uniform workspace and local generation charged at every scale. A giant
alphabet or a complete-menu scan per record remains inadmissible.

The next gate is the guarded local executor: spatial payload must absorb
temporary metadata, and full-volume reserve descents must clear parent
arrays before recursion. The coupled recurrence note retains these as
explicit physical premises.

Credits: @CubeJerry; OpenAI tape/Fourier constructions; E001's
input-dependent prime lemma; E002 multidigit batching; Baker, Harman
and Pintz; substantial ChatGPT multi-agent assistance. No human
refereeing or Lean verification is claimed.
