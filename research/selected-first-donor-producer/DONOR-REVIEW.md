# Independent review of the selected first donor producer

**Outcome: PASS within the stated source, admission, and three-contact scope.**
This is an independent mathematical and static linkage review; it does not
rerun the author's full native packet verifier. The review was prepared for
@CubeJerry with substantial OpenAI assistance. The implementation and the
literal kernels it composes remain credited to their authors and exact
predecessors in `SOURCE-PINS.json` and `NOTICE.md`.

## Reviewed freeze and source

The canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`.
The reviewed `producer.py` SHA-256 is
`e183c38866223a8b896c8210f65e6531f89b0836b88541cb45b27e7ebc672c2f`;
the reviewed `PROOF.md` SHA-256 is
`f95e1def41bdd30289161ad8859fbf47bb19f2159a91c60b5405aab7137a8ba4`.
The exact lifetime predecessor is CubeJerry commit
`53e0a6d689d8c3a840a055eedc59f7f2e9c14022`, whose `protocol.py` SHA-256 is
`c324967962e04a125bbdb5f503d3d6c3cff5d7eb69343443bc6ea4338af243bd`.

`check_donor_source.py` freshly reads the complete retained selected archive,
checks its 350,722-byte length and SHA-256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`, and
checks canonical JSON SHA-256
`91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097`.
It independently extracts events 28037 through 28041 and frames 3 and 601,
then checks chronological ownership and frame typing of all 28,039 preceding
events. It confirms public owner 1349 is in frame 3, owned 1526 is in frame
601, frame 3 is empty, and frame 601 is exactly `[137]`. Substituting `[239]`
fails this source authentication. `DONOR-SOURCE-CHECK.json` records the result.
This proves the chronological binding, not numerical donor acquisition.

## Exact mathematical kernel

Independently enumerating the canonical binary span gives basis columns
`(137,1,2,4,8,16,32,64,256)`. Taking the inverse permutation and the indicated
Gram correction gives the implementation's exact `G` and `Q`. The actual
source frame circuit is chronologically `D, P_G^-1, C0, P_G, D`, with
`D|x> = (-1)^(x7(x0+x3))|x>` and no affine phase. The two identities

\[
P_G X_0P_G^{-1}=X_{137},\qquad
q(x)+q(x\mathbin{\mathrm{xor}}137)=x_0+x_3\pmod2
\]

give the absolute, rather than projective, operator

\[
T_{601}=\frac{(1+i)I+(1-i)X_{137}Z_9}{2}.
\]

The sign masks commute because the binary dot product of 137 and 9 is zero.
The checker derives each of the 512 two-term columns independently from the
canonical chart and verifies the 21-CNOT word and its reverse on all 512 binary
vectors. Bit reversal gives packed xor mask 290 and sign mask 288. The tensor
extension applies this same exact one-factor identity independently to each
of the `f` axes; spectator axes, multiplicity, and external columns are left
to the unchanged kernels' proven traversal contracts.

For the common integer-reserve sufficient domain, every `j`-axis C prefix
has denominator dividing `2^ceil(j/2)` and real-component row norm at most
`2^ceil(j/2)`. The initial divisibility `2^ceil(f/2)` therefore covers each
prefix, and the strict margin
`2^ceil(f/2) M <= 2^(w-1)-1` covers both quadratic sign layers, every
permutation, each C prefix, and the following negation into the zero owned
receiver. This is a sufficient admission theorem, not a claim that endpoint
fit implies admission.

### A uniform endpoint obstruction for this circuit

For every integer `w >= 2`, take `f=1` and put real value `-2^(w-1)` at
native address 129 (packed address 258), with every other component zero.
Its first `D` phase is negative, so that first layer requires `+2^(w-1)`,
outside signed width `w`. Nevertheless the complete kernel outputs only
components of magnitude `2^(w-2)` at native addresses 129 and 8, hence all
complete endpoint components fit. The exact checker records `w=2,3,6,31`
representatives; the displayed algebra proves all `w >= 2`. This obstruction
applies to admission of this five-factor same-width circuit. It is not an
impossibility result for different implementations or wider scratch fields.

## Literal linkage, ports, transaction and pruning

The checker compares all 75,326 factor instructions against the unchanged
phase, CNOT and C kernels after independently reconstructing each PC and
port relocation. It checks all 75,391 native-to-adapter state translations,
including every read branch and halt continuation. The native header is
never written, and original native DATA is not written before commit PC
75,357. Comparing the old parser-only adapter with the new stale adapter
gives an injective 155-state graph isomorphism with identical tests, writes,
moves and continuations.

Native ports 0 through 30 become adapter ports 3 through 33 and physical
ports 5 through 35. The guide is physical port 36. The unchanged bank
delivery uses work port 3 and external bank 43. The producer touches exactly
`{3,43} union {5,...,36}`; in particular it does not touch the owned HOME on
port 2. A separate graph closure check establishes that public donor bank
writes begin only after the complete adapter has returned successfully.
The original HOME and public donor contents are therefore preserved on the
documented phase-overflow rejection; failure head return and private cleanup
are not claimed.

An independent fixed graph walk verifies that every rule in the 4,927-state
inherited INIT/SUB closure is unchanged, and that the complete 71,524-state
joined graph is exactly reachable from its three fixed entry ports, without
dropping any outgoing branch. Its digest is
`fec60dd4653c6c06846850b2d318d9eec0b7d9856af6b65bae2d336d5c5f99a0`.
Deleting the retained SUB entry rule is detected. Pruning is entirely
input-independent; it does not specialize on the positive packet.

## Costs and limits

Re-summing the unchanged kernel bills gives
`8687647 fV + 212992 E + 213019`, coefficientwise below
`2^24 (fV+E+1)`. Adapter plus two bank transfers and the return edge cost at
most `150F+161`; including the unchanged first SUB and INIT origin shifts
gives linear subtotal `4265F+4333`, below `8192(F+1)+128`. The stated private
history allowance includes the kernel, adapter, delivery and scalar unions;
it retains the separate OLD-source INIT history and does not retire a live
public source or refund historical stock.

The source's two intervening ADDs, pre-MOVE donor acquisition, and the
external OLD/context setup remain explicit context premises and charges.
The new conclusion is a produced frame-601 donor followed by the unchanged
first SUB, with the receiver still live. It does not execute later lifetime
contacts, CLEAR, a whole selected caller, or a recursive allocation theorem.
In particular `f <= cutoff` for this producer does not imply the later
rank-two admission condition `2f <= cutoff`, and later numerical reserves
remain independent obligations. No new kappa or foundational assumption
discharge is claimed.

## Reproduction

Place this review and the two checkers beside the proposed `producer.py`, or
pass its containing directory explicitly as `--package`. The primary light
checker is read-only unless `--receipt` is supplied:

```sh
python3 -I -W error -B check_donor_producer.py --package PACKAGE
python3 -I -W error -B -O check_donor_producer.py --package PACKAGE
python3 -I -W error -B check_donor_source.py --package PACKAGE --archive SELECTED_NATIVE_JSON_GZ
```

Both light modes pass with byte-identical `DONOR-REVIEW-CHECKS.json` results.
The separate source command passes with `DONOR-SOURCE-CHECK.json`. The archive
is retained by the exact predecessor referenced above and must have the
stated digest. The review does not treat another execution of the author's
full packet machine as independent proof.
