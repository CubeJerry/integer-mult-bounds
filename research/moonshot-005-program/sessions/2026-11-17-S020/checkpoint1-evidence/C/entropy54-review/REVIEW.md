# Independent review of the 17/2-record nonlinear transcript bound

**Accepted within the stated finite-alphabet, deterministic, zero-error,
input-independent-schedule, whole-record interface.** The exact entropy
certificate is valid. Both the old 392-field masked source and the new
408-field all54-held source satisfy its separately audited physical source
premise. Every such continuation needs at least nine future strict owned
downward transfers. This is not nine distinct lifetimes, not a universal
nonlinear lower bound over infinite alphabets, and not a complete supplier
or new kappa.

## 1. Exact source and graph binding

The native-root bytes have SHA256
`8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`.
Both actual words have the same 57-known/54-unfinished partition. The
fourteen selected unfinished roles are the eleven-core roles

    18,55,56,105,109,66,69,70,89,93,15

and three isolates

    14,31,35.

The independent checker derives adjacency solely from exact integer root
dot products, with adjacency meaning orthogonality. The isolates have no
neighbors among the other thirteen roles. The eleven-core adjacency masks
match the certificate. No graph supplied by the discovery solver is trusted
without this source reconstruction.

Certificate SHA256:
`c5d40e71246008699cb137eaa2badd2674253b0567c87e54fa7fa5809bacc79f`.

## 2. Shannon rows independently justified

First fix all source inputs outside the fourteen-role witness and all
initial Y inputs. Granting those fixed constants is harmless for a lower
bound. For the eleven-core subproblem, also fix the three isolate inputs.
Let the remaining input records `X_i` be mutually independent and uniform
over the same finite alphabet of size `Q>=2`. This alphabet can be an
entire width-`m` record over a scalar alphabet, so `log Q=m log q`.

Let `Z` be any deterministic zero-error broadcast. With `V` the eleven
core roles, define

    g(S) = H(Z | X_(V\S)) / log Q.

The independent checker rewrites all inequalities in nonnegative `>=`
orientation, using sets of native role IDs instead of the author's integer
entropy-coordinate indexing. Their meanings are:

* `g(empty)=0` because the encoder is deterministic when every input is known.
* For `i` outside `S`, `g(S+i)-g(S)` is a conditional mutual information,
  hence is nonnegative and at most one.
* For distinct `i,j` outside `S`,
  `g(S+i)+g(S+j)-g(S)-g(S+i+j)` equals
  `I(X_i;X_j | Z,X_(V\(S+i+j))) / log Q`. Independence removes the
  corresponding unconditioned mutual information, proving nonnegativity.
* If `S` contains none of receiver `i`'s neighbors, conditioning on
  `X_(V\(S+i))` supplies every side-information input needed to decode
  `X_i` from `Z`. Consequently `g(S+i)-g(S)=1`.

The checked certificate uses 27 monotonicity rows, 43 submodularity rows,
35 decoding equalities, and one deterministic-empty equality. Every
inequality has a nonnegative multiplier after the independent orientation
change. Equality multipliers may have either sign. Exact rational summation
of all 106 rows cancels every entropy variable except `g(V)`, with coefficient
one, and gives right side `11/2`. Thus

    H(Z) >= (11/2) log Q

for the core problem. Floating-point LP discovery does not enter this proof.
`output/EXPANDED-DUAL.json` records the separate native-set reconstruction of
every term and its rational multiplier.

## 3. Why the three isolates add exactly three units to this lower bound

After the inputs outside the fourteen-role witness are fixed, each isolate
has no unknown side information in the witness. Hence the three independent
isolate records are deterministic functions of `Z`:

    H(X_I | Z)=0,     H(X_I)=3 log Q.

It follows that

    H(Z) = 3 log Q + H(Z | X_I).

For each fixed value of `X_I`, the eleven remaining records are still
independent and uniform, and the conditional encoder and decoders solve the
same eleven-core problem. Applying Section 2 in each conditional slice and
averaging proves

    H(Z) >= (17/2) log Q.

This argument does not assume that disjoint index-coding problems have an
unproved general additivity property. The isolated demands are decoded
directly from the broadcast, which supplies the exact chain-rule identity.

## 4. Independent audits of both actual source cuts

The review replays prefix values as sets of the full 222 independent input
columns, with ADD implemented by symmetric difference. It obtains actual
chart locations from the word. Real chart inclusion is reconstructed by
exact rational row reduction from each span/annihilator description. It
does not import the root interpreter, the source builder, their inventories,
or the root entropy verifier.

| Source word | SHA256 | Cut before operation | Live fields |
|---|---|---:|---:|
| Admitted S019 masked Hub | `f21de38f4a8adc1a55920c16b684285f62607829fe512a0088fe5ecb217fcfdd` | 1129 | 392 |
| New direct-known57/all54-held | `74fb050a6afb8d8e1b6895b0f092220f8e6852365a7516ef4db2284c43c1a5ee` | 1269 | 408 |

For every unfinished receiver `i` and every live field lying at a chart
inside its native facet `F_i`, the unknown-coordinate dependency is a
subset of `i`'s native orthogonal-neighbor set. Both audits find zero leaks.
All unfinished Y fields still contain their own arbitrary initial Y
coordinate only at the source cut. The valid operation geometry and full
closed-word invoice of each source remain covered by their separate source
reviews; this review checks the new entropy-application premise directly.

## 5. Nonlinear physical transcript reduction

Consider any finite fixed continuation schedule using arbitrary deterministic
co-chart functions over width-`m` records, ascending originals, and strict
downward owned transfers. Let `D_i` be the downset of all real subspaces of
`F_i`. Grant the value carried by **every** future strict owned downward
transfer to every receiver, in chronological order. If there are `q`
transfers, this globally granted transcript has at most `Q^q` possibilities,
so its entropy is at most `q log Q`. Values can depend on previous transfers
and feedback; the same cardinality bound holds.

Receiver `i` can simulate all computation inside `D_i` from its initial
inside values and this transcript. By the source audit, its native-neighbor
records and conditioned constants determine those initial inside values.
An ascending carrier cannot enter a downset from outside: `H<=H'<=F_i`
implies `H<=F_i`. Local operations, zero births, and erasures add no external
information. Every inward owned entry is among the globally granted
transfers. Deterministic chronological simulation therefore recovers its
final `Y_i+x_i` value; fixing initial Y values reduces this to demand `x_i`.

Thus this transcript is a valid static code for the native-neighbor problem.
Sections 2-3 require `q>=17/2`, and the integer number of whole-record
transfers satisfies `q>=9`. One owner can make several such transfers, so
the proof does not count nine distinct lifetimes. Input-dependent scheduling,
uncharged timing/control channels, wider records, or different initial
source data are outside this reduction. No infinite-alphabet nonlinear
dimension assertion is made.

## 6. Controls and conclusion

The separate verifier rejects deletion of a nonzero dual term by exact
residual failure. A planted initial own-input record at ground invalidates
the physical native-neighbor premise for that receiver, demonstrating why
a changed source cannot inherit the result without a fresh audit. The
earlier scalar/block-factor package also has constructive rank-eight
controls under specified graph changes; those do not weaken this exact
graph's entropy certificate.

The 17/2 bound strengthens the all-width linear exclusion to deterministic
nonlinear finite-alphabet continuations and provides a quantitative
fractional transcript lower bound. It still does not establish the exact
fractional broadcast rate, nor a lower bound of nine full record widths.
Nine characteristic-two canonical records give a static upper bound, so
the integer whole-record static count is nine. Their actual physical
delivery and restoration remain unproved.

Credit root's exact Shannon certificate, Worker C's independently discovered
fourteen-role witness and separate rational/source review, the native,
canonical, initial-chart-transcript, and masked-source predecessors, and
@CubeJerry. Substantial OpenAI assistance; this is independent agent review,
not human or proof-kernel certification. No complete kappa update.
