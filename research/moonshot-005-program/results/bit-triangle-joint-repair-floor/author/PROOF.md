# A joint middle cut excludes inexpensive repairs of the frozen triangle source

**Proved on the stated fixed-source interface, subject to independent review.
No new kappa.** The result strengthens the prior one-middle obstruction. It
does not exclude redesigned source maps or a replacement return bank solely
because its fitting-rank excess is small.

## 1. A cut theorem with arbitrary deterministic helper information

Let F be a finite field, let X range freely over a finite-dimensional F-space,
and let L:X -> direct_sum(D in A) Z_D be a surjective linear boundary map.
Assume the required output is T X = sum_D C_D (L X)_D, where each C_D is
linear. The boundary variables therefore range independently. Their original
input representation need not use independent input variables for each D.

Retain a downstream directed network in which information initially at D can
reach the chosen output only through a listed outgoing transcript with at most
c_D F-symbols. Transcripts may be arbitrary deterministic functions. Give the
downstream computation any additional helper transcript of at most r F-symbols,
which may be a function of the complete original input. No other varying input
or uncounted informative bypass is allowed. In particular the helper does not
change the fixed boundary map L or the original outgoing capacities.

For every subset S of boundary locations,

    r >= rank([C_D : D in S]) - sum(D in S) c_D.       (1)

To prove (1), fix the boundary variables outside S. Surjectivity of L permits
all values of the variables in S. The required output takes exactly
|F|^rank([C_D:D in S]) values. All varying information reaching it is carried
by the helper and the listed outgoing transcripts, with joint alphabet at most
|F|^(r+sum c_D). Even nonlinear, jointly correlated coding cannot distinguish
more possibilities. This is a cardinality argument, not an assumption that
one cut's dimension can always be added to another cut's dimension.

If the images R_D=im C_D for D in S form a direct sum, the right side of (1)
is sum_D(dim R_D-c_D). The bound is sharp for the abstract cut relaxation
when 0<=c_D<=dim R_D: choose a basis of each R_D, send c_D coordinates through
its local channel, and send the other coordinates through the shared helper.
This sufficiency claim concerns that abstract relaxation only. It does not
construct the programme's shared K/F network or its causal early/late phases.

The proof remains valid for any positive number rho of independent repeated
stripes, even when all subsequent maps mix stripes arbitrarily. Both rank and
listed capacity scale by rho. It also holds over every finite extension of F.

## 2. Fixed native source and its independent boundary variables

Use the S026 five-class triangle source on original donors29,36,77 and choose
receiver10. Its uncompressed source certificate has SHA-256
`362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af`.
The coefficient field is GF(32), represented by t^5+t^2+1. The native layout
and nine-port partition are the separately authenticated programme data.

Per class and stripe, each original donor has48 independent coordinates.
Its16 visible rank-three quotients form an invertible48-by48 matrix. The45
visible planes have three visible port values each:42 private planes and
three shared planes. The exact source boundary matrix from144 original input
coordinates to135 visible port coordinates is surjective. The five classes
are independent, so all675 port coordinates per stripe range freely.

The target is the sum of the three original240-coordinate donor banks. For
each plane, invert the relevant donor's48-by48 source stack and its actual
three-by-three Vandermonde port minor. This gives its48-by3 output decoder.
At each shared plane the two donor formulas agree. Multiplication with the
source maps gives identity on every donor and class, so these port decoders
compute the target. Surjectivity makes this decoder unique as a function of
the visible boundary, including among nonlinear functions.

Embed each class decoder in its actual48-coordinate block of the240-dimensional
output. Group its columns by their actual middle D. This defines C_D and R_D
without inventing new independently varying plane inputs. The new checker
reconstructs these matrices from immutable source data without importing or
executing the predecessor's algebra or verifier.

## 3. A three-middle witness and a stronger33-middle witness

For D=640,726,845 the three required image spaces have dimension9 each and
their sum has dimension27. Each D has exactly four actual outgoing right-plane
flags through which it can reach receiver10. Their total capacity is12 symbols
per stripe. Equation(1) therefore requires

    r >= 15 rho.                                    (2)

The separately published witness uses these33 actual middles:

    640,726,845,81,88,93,118,123,138,395,442,443,473,
    558,564,605,663,672,693,696,706,708,717,771,774,
    803,835,849,865,937,974,991,1053.

The first three images have dimension9 and the other30 have dimension7.
Their union rank is237, equal to the sum of those dimensions. The spaces
are therefore in direct sum. The original outgoing alphabet has132 symbols,
and the exact stronger bound is

    r >= 105 rho = (7/16)b,      b=240rho.            (3)

No optimality over all possible subsets or all receiver cuts is claimed.
The33-middle cut relaxation itself has exact helper requirement105rho; a
matching abstract basis split is verified. The rest of the physical network
may require more. Repeating one of the first three middles reduces the union
rank to18, demonstrating why simple addition of cut dimensions is invalid
without the checked direct-sum property.

## 4. Canonical information and movement scope

The native canonical row space H=row(I+O) has rank9. Its restriction to donors
outside receiver10's foreign set still has rank9. Thus arbitrary values of the
three active foreign donors can be extended by outside inputs so Hx=0, while
all other foreign donors are fixed to zero. No outside donor can reach the
receiver through the retained nested proper routes. Set original Y=0 as well.
The retained canonical preload is zero, and the required native output becomes
the sum of the three active banks. This is the slice used in sections1-3.

Consequently a repair that retains these source port functions, the original
proper routes, and the canonical bank must supply at least105rho additional
field symbols. A helper can depend on all original inputs; it is not restricted
to one donor or to a linear function. It may be made freely available at every
downstream location for this lower bound, a relaxation favorable to the repair.

At b1920 (rho8) and b5760 (rho24), the respective floors are840 and2520,
far above the admitted limiting gap-eight return allowances67 and202. The
formal b480 scaling gives210 versus16; it is a fixed-port cut calculation,
not a claimed early source realization on the changed480 atlas.

The normalized floor7/16 also exceeds the original atlas's entire limiting
movement room0.278106915125... even if every additional informative crossing
could be bought at the minimal unit charge. This comparison applies only when
the original invoice is retained and the extra crossings are additional.
It does not forbid reallocating already paid owners or changing route endpoints.
Actual Hub-to-ground returns have gap-eight charge and are more expensive.

For a replacement return bank with fitting A=I+B, distinguish

    h=rank(A)-9b,
    r=rank([H;A])-9b,
    r-h=9b-dim(row(H) intersect row(A)).

Our fixed-canonical repair obstruction constrains r, and does not justify
substituting h unless canonical containment has been established. A tilted
replacement bank, source recoding, changed D/K routes, or a source that mixes
classes before the frozen ports lies outside the exclusion. No unrestricted
low-excess fitting impossibility, full supplier bound or foundational discharge
is asserted.

## 5. Evidence, review and next construction

Run reconstruct.py with --repo, --source (the frozen triangle author directory)
and --out. It checks both orders of every source/local inverse, all675 independent
visible coordinates, every active donor identity, all33 actual four-flag cuts,
the237-dimensional direct sum, and the canonical restriction. WITNESS.json.gz
contains the actual columns and source labels. A duplicate-middle control fails
the asserted rank27. The abstract matching split has132 local and105 helper
dimensions; deleting one helper leaves rank236 instead of237.

The separate pack.py initially found the witness using Worker B's extracted
spaces. That search is not called independent source verification and is not
an optimality certificate. reconstruct.py supplies the fresh source binding.

The constructive next step is to change the source/port maps together with
the D/K decoder, or to reallocate the actual paid routes. This result prevents
spending further effort on a small auxiliary repair of the frozen triangle.
Credit @CubeJerry, the retained native and atlas authors, S026 Worker A's source
certificate, S026 Worker B's one-middle obstruction, and S027 Worker B's space
extraction. S027 root supplied this joint-cut theorem, witness and fresh
reconstruction with substantial OpenAI assistance. All five foundations remain.
