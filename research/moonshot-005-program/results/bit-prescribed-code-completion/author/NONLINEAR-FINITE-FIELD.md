# Five new symbols per record remain necessary for exact nonlinear broadcasts

**Proved in the stated fixed-information interface. No new kappa.** This is
a separate strengthening of FRAME-SATURATION.md. The lead researcher proposed
the nonlinear restriction argument; Worker C independently checked it and
implemented the finite receipt below. Earlier frozen linear proofs remain
unchanged.

## Proposition and quantifiers

Let k be any finite field of characteristic two, V a positive integer, and
let each of the 111 independent raw records lie in k^V. Supply every receiver
with the same prescribed linear S8 broadcast and, freely, any subset of the
17 raw records listed in FRAME-SATURATION.md. Receiver i may additionally
read every raw coordinate in its geometrically permitted foreign local
space L_i. Let an arbitrary deterministic encoder broadcast a further
fixed-length q-symbol message in k^q. Its encoding and every receiver's
decoding may be nonlinear.

If every receiver exactly reconstructs its own raw record for every input,
then **q >= 5V**. The bound is sharp at the abstract broadcast level: adjoining
five canonical quotient rows and repeating them across V coordinates is an
exact linear scheme. Its physical acquisition and delivery remain unproved.

No linearity of the new encoder or its decoders is used. This statement
does not assert a lower bound for a changing chronological local interface,
new nonlocal receiver information, variable-length messages, approximation,
or a different prescribed baseline.

## Proof by an injective restricted input family

Use the exact native witnesses from FRAME-SATURATION.md:

    I = {0,14,22,23,30,31,59,60},
    lambda = e0 + e24 + e32.

Choose independent u_i in k^V for the eight i in I and t in k^V, and set

    x = sum_{i in I} e_i u_i + lambda t.                       (1)

This is an injective parameterization of |k|^(9V) inputs: x24=t, x0=u0+t,
and the remaining seven frame coordinates are their corresponding u_i.
All other coordinates outside {24,32} union I vanish. All 17 freely supplied
raw point records vanish on this family, because their indices are disjoint
from that support.

Let b denote the existing baseline measurements. Every S8 row annihilates
lambda, so b is just the rank-4V restricted S8 measurement of u. Thus b has
exactly |k|^(4V) possible values. In particular, the explicit S8 row
`0xcc00cc6400097c0033000055` restricts to the unit row at 0 in I, so b
determines u0.

All frame ports are pairwise nonorthogonal in the rational native geometry.
The three lambda coordinates 0,24,32 are also nonorthogonal to receiver 0.
Consequently receiver 0's entire permitted local input is zero on (1).
Its exact decoder applied to common data (b,m), where m is the new message,
therefore yields x0=u0+t. Since b already gives u0, the common data determine
t.

For each other i in I, no frame coordinate belongs to L_i. Its only possibly
nonzero local raw records are x24 and x32, each equal to t. Once (b,m) has
determined t, it can synthesize this receiver's complete local input, invoke
its exact decoder, and recover xi=ui. It also recovers u0 from b. Hence
(b,m) determines all nine independent vectors u,t in (1).

The map (u,t) -> (b,m) is therefore injective, while its codomain has at most

    |k|^(4V) |k|^q

values. Comparing with |k|^(9V) proves q >= 5V. The matching canonical upper
bound is the rank argument already checked in FRAME-SATURATION.md. ∎

## Independent receipt and scope controls

`check_nonlinear_family.py` independently enumerates every restricted input
over F2 and F4 at V=1. The F4 representation uses two-bit labels; only field
addition occurs, which is bitwise XOR. It checks the actual baseline outputs,
the row that reveals u0, the zero local data at receiver 0, and the exact local
data at every other frame receiver. The baseline fibers have sizes 2^5 and
4^5 respectively. This finite check verifies the native witnesses and the
restricted-family calculation. The cardinality proof above supplies the
universal quantifiers; it is not an extrapolation from this enumeration.

Meaningful controls remove x32 from lambda, grant the extra raw coordinate
24 as new local information at receiver 0, and remove the distinguished
baseline measurement of u0. Each control invalidates the specific premise
it targets. None is called a disproof of a broader alternative architecture.

```sh
python3 check_nonlinear_family.py --repo REPO --seed SEED-SOURCE.json --out output
```

Expected status: `PASS_NONLINEAR_RESTRICTED_FAMILY_RECEIPT`. The source and
seed hashes are checked exactly. All five programme foundations and the
unpaid source/transport/recursive costs remain visible. **No new kappa.**
