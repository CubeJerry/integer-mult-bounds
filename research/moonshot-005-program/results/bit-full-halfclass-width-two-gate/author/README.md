# Exact width-two quotient threshold in the full halfclass reservoir

The proposed theorem is stronger than the exploratory chain question:
every native width2 fitting whose canonical quotient has dimension at
most3 and whose scalar directions lie in the full36-group halfclass
reservoir has exact proper-cover charge chi>=196. No assumption about
decomposable tensors, commutativity or triangularizability remains.

The separately credited two-seven-class fitting attains chi194 with
canonical quotient dimension4 in the same reservoir. Thus4 is the exact
least quotient dimension for this reservoir to meet the retained194
support target. This is an algebraic/geometric threshold, not a physical
source, packet count, supplier or new multiplication bound.

Reproduce with Python3 standard library only:

```sh
python check.py --native /path/to/BIT-NATIVE-WORD.json.gz --output reproduced
python -O check.py --native /path/to/BIT-NATIVE-WORD.json.gz --output reproduced-optimized
```

Expected status PASS_FULL_HALFCLASS_QUOTIENT3_GATE_PREMISES. Key counts:
36 indicator groups; C+U rank39 and C intersect U rank6; maximum literal
noncoordinate local support20 and pair union34;4543 cross-family pairs;
501 common six-row spans;56 coordinate/family subcodes;270 exact quadratic
minor certificates and two nonfactorable quadratic pencils. Normal and
optimized result/evidence bytes agree.

The proof explicitly retains quotient representatives: code distance48
makes the small local intersections literal. The four noncoordinate
members of the12-port common support W are included in every relevant
count. Restricted canonical distance18 controls availability of short
representatives at coordinate receivers. These are exact source facts,
verified for the pinned word and extended to all coefficient fields by
binary rank/distance arguments.

Most new geometric obstructions have quadratic rank27 and still exact
chi2: their unique vanishing quadratic has symmetric rank7. Two rank26
cases require a full pencil argument; the explicit3-by3 minors and
Bezout identity rule out all real factorable members. The coefficient
field of the fitting is characteristic two, while this chart geometry
and its quadratic pencils are over the rationals/reals.

This explains why the separate bounded five-type GF4 chain search,
which uses only linear and quadratic rank cuts, was a necessary
relaxation rather than an exact chi solver. No claim is derived from
its timeouts. The present theorem instead has the complete written
argument and exact finite source certificates, pending independent review.

An initial outline assumed absolute absence of rank-one tensors. The
common-plane coordinate-availability argument removed that assumption
before this package was frozen. Earlier speculative notes are not part
of the proved theorem. Prepared for @CubeJerry with OpenAI assistance;
credit and exact predecessor pins are retained in SOURCES.json.
