# Independent selector-lift review

**PASS for the stated selector family and literal paid repair. No new κ.**
Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.
The reviewer imports no author scientific code.

## Mechanism and scope

The selector invariant is valid for every fixed m>=2: selected copy plus
shared core executes the original word, while each passive-minus-selected
main vector executes only the main-main operations. It requires no main/core
SWAP and no reset of a main field. Both conditions were independently checked
on the authenticated word. The original endpoint has arbitrary independent
helper inputs, all restored; it is not a zero-helper specialization.

The main-only endpoint is I, while the full main endpoint E has111 Y<-Y+X
shears. Passive outputs are therefore `x_i+(E-I)x_1`. Adding each missing
`X_i+X_1` term gives E independently on each copy. The displayed repair is
legal in the stated normalized grammar: allocate zero scratch in actual full
frame8, gather the two X fields, make the nested rank1 move to actual body
frame7, add to Y, and erase. Clearing nonzero scratch retains the owned-erasure
assumption. This proves neither a free same-frame ADD nor an all-width
physical admission nor optimality of the repair.

I independently checked all636 rational frames: basis ranks, annihilator
ranks and orthogonality; every original and lifted MOVE is nested, every
ADD is in the same exact frame, and every owned activation/erasure and final
frame matches. The full8/body7 repair nesting is proved from actual matrices,
not merely asserted from dimension tags.

## Independent evidence

The Python verifier uses reverse adjoint propagation, while the author uses
forward rows. It verifies all659 original public columns, main-only I, and
all public endpoint columns of repaired m=2,4,6 lifts. Its pre-repair adjoint
bad-column counts are222,444,666; these differ legitimately from the author's
bad-output-row counts111,333,555. All repaired counts are zero. Literal paid
profiles, events and owned lifetimes are independently reconstructed.

The raw caller is independently authenticated and recounted directly from
its J, QUERY, IDLE_ONE events and target masks. It supplies36 actual native
invocations at18 stages,222 rank127 targets,444 targets at each rank1+7j
(j=1..9),444 paid rank1 queries, and444 paid rank7j idles (j=1..8).
Thus every root term in the proposed m-plane assembly is present.

Independent rational fixed-point logarithm/exponential enclosures give
`M2 < -444` and `D=(P_core-H0)_t < 88`, t=199/200. The lost m-1 copies of
productive helper credit are debited. The complete repaired family obeys
`M(m)=(m/2)M2+18(m-1)(D-111)<-222m-414(m-1)<0` for every even m>=2.
This universal conclusion follows from the invariant and exact count formula,
not extrapolation from the three tested m values. Omitting the repair yields
a false positive moment already for m=2; reinstating its full charge rejects it.

## Reproduction, pins and limitations

```sh
python3 -I -B independent.py --word /path/to/native.json.gz --caller /path/to/query_only_6980.json
python3 -I -O -B independent.py --word /path/to/native.json.gz --caller /path/to/query_only_6980.json
```

Expected marker: `PASS_INDEPENDENT_REVERSE_SELECTOR_LIFT`. Normal/-O receipts
are byte-identical; the author Node replay also passed. `arithmetic.py` is
the reviewer's independent exact arithmetic module, using outward rounding
and proved series remainders; the author uses integer-root bounds instead.

Native SHA256: `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`.
Native Git blob: `b718d6b2848215ad785022106dfa9f871a3d1c0c`.
Raw caller SHA256: `3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e`.
Raw caller Git blob: `cf55f4271009a06ad192a070d330a4466b6d44fa`.

Fresh reviewed authored bytes:

- PROOF.md `5c20d631a18d0a975bab8f4b191756f3cf724fabb22f46bc553b1929725fe809`
- verify.js `970f9602e007a89c22093a7f408850008129404f38ebd8cb41ce9e5f8c9fba14`
- RESULT.json `69b06177aa36ee183829ce4d5b6b2fd9728cd266fc9660903d019828d0486105`

The result does not exclude cheaper corrections, different selectors or
shared cores, cross-plane batching, changed sources or different interfaces.
It supplies no finite compiler, precision/tape admission or new multiplication
bound. The failing raw moment already allows all extra ordinary work for free;
charging that work cannot rescue this particular gate. All five foundational
assumptions remain. Prepared by a separate OpenAI Codex reviewer; original
BIT source/caller authors, DreamingOfClouds, zxv and @CubeJerry retain credit.
