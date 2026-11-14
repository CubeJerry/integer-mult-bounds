# Independent review of the complete literal key pass

**Disposition: PASS within the stated fixed thirteen-bit payload ABI.**
No scientific change is requested. The implementation computes destination
keys at all physical record positions, with the claimed exact added bill,
preserved opaque payloads, complete successful returns and explicit
overwrite limitations. This is complementary model-assisted review, not
human or formal-kernel certification.

## 1. Reviewed object and independence

Canonical main is `e54523517d0f03e58352e647c403a5af3e525a57`.
The immediate B6 dependency is CubeJerry commit
`4ccf407db96c7797dc3c83d90b033551f7d52c76`.

Reviewed scientific identities:

- `key_pass.py`: `3df218d812d47c1e935715c87d716a7acf7a2bf2610c752ba409a9e29014d8f3`.
- `PROOF.md`: `ea1a6ffb0f282e8805788d5ae2521b2a9658a3e963f00575c794e6c7080fbcd4`.
- Graph: `8f5ae62b89de8308eb021920185269d884f07f625a5b3ee10b39f27aee5a393b`,
  21135 locations,22 fixed roles, forward/inverse entries0 and444.

The independent checker imports the frozen compiler tables as the object
under review, but imports neither the contributor's verifier nor its
execution engine. It supplies a separate sparse dictionary interpreter for
R/W/M/J/H, separate packet construction, translated negative origins,
opaque exterior sentinels, per-invocation visit windows, older retained
history, and direct integer padded-rotation oracles. All47 retained source
files are checked against their supplied byte/Git-blob pins. Remote ref
verification remains the orchestrator's separate publication gate.

Every one of the two10123-instruction child copies is independently compared
to the exact retained B6 table. Read and jump targets receive only their
fixed offset. Every successful DONE halt becomes exactly one continuation
jump; unsuccessful halts and all port operands remain unchanged. A missing
child-return mutation is detected. The outer portion is889 locations,
independent of h,p,s,a and payload values.

## 2. Independent record and carry argument

The required domain is h>=1, p>=h+1, N=2^h, 1<=s<=N and0<=a<s, together
with the true header/width correspondence, source/owner capabilities and
complete field framing. The local graph does not acquire these premises.

After the literal marker read and width-driven INDEX construction, the
index is exactly an h-bit little-endian zero word. At iteration i, it is
the physical record number i, independent of that record's old key. Copying
it into a newly framed ADDRESS sets the actual B6 input once for that full
route. The retained B6 theorem updates the current address through its
2h-1 child queries and returns the true padded rotation pi(i), or its
inverse. The copied address is not reset inside a point query.

ADDRESS is then scanned to its end and read from most to least significant
digit. Each digit is written as the original thirteen-bit code2 or3, so
the original key-word order is preserved. Validation reads all13 bits of
each old code before rewriting any of that code; it pays the full rewind
before output. The payload pointer advances through exactly h key words
to the next physical record, and the copied address is completely erased.

The explicit carry turns c trailing ones to zero and the next zero to one.
For all i<N-1 the next zero is inside the word. Only i=N-1 reaches R after
all h bits were one, and that unique overflow takes the end branch. Hence
the graph processes exactly N records. No runtime decoded N, address
lookup or host record loop is used. The h=1 case processes two records
through the same instructions.

The increment sequence has exactly N-1 propagated ones in total:
`sum_(j=1)^h floor(N/2^j)=N-1`. This includes the final h-bit wrap. That
identity proves the all-size carry invoice; bounded tests alone do not.

## 3. Payload preservation and paid return

Each record begins with one thirteen-bit payload code4096+t, where the
twelve lower bits are arbitrary and the high tag is1. The graph merely
moves across the lower bits and checks the tag; no payload cell is written.
Its only payload-port writes are the13Nh allocated key bits, exactly once
and in physical record/key order. Repeated and correlated payload values
are allowed; the graph does not use them as identities.

After checking `>`, the graph explicitly returns13 positions to that word's
start. Its leftward scan checks every bit of each aligned code even after
a mismatch. Every candidate therefore has the same scan cost. The only
aligned code5 in a valid frame is the original `<`: neither payload codes
with high bit1, key codes2/3 nor final code6 can equal5. Consequently the
scan returns to the actual entry head, even when the physical origin is
negative or not a global multiple of13. It visits the complete frame and
one right frontier cell, and does not inspect a left exterior word.

The independent interpreter checks the exact full payload dictionary,
including zero,4095 and payloads whose lower bits resemble marker codes.
A new returning mutation inserts an opaque-payload write while retaining
correct alignment and all correct destination keys. It reaches DONE, but
the full-payload oracle detects it. Thus checking only keys would be
insufficient, just as checking only a final head would be insufficient.

## 4. Independent exact invoice

One instruction means one R, W, unit M, J or H. The child DONE-to-J rewrite
preserves its instruction count exactly. Direct counting of the outer
paths gives:

| Surface | Added instructions |
|---|---:|
| Read one complete fixed marker and move past it |26|
| Initialize INDEX from unary h, returning both heads |11h+17|
| Copy INDEX to ADDRESS, returning both heads |11h+15|
| Skip payload bits and check the tag |14|
| Validate, rewind and rewrite one key code |65|
| Complete address scan and h-key emission |72h+5|
| Erase one complete h-bit frame and return |7h+9|
| Nonoverflow increment with c propagated ones |7c+9|
| Final overflow |7h+8|
| Full paid payload rewind |66N(h+1)+119|

For the last row, every mismatching code costs39 read/move/jump instructions
plus27 backward/return instructions. There are N(h+1)+1 mismatches,
including `>`. The matching initial `<` costs53. Thus the exact result is
`66[N(h+1)+1]+53`, not a free symbolic seek.

The complete index-increment bill is16N-8. Entry contributes11h+43;
each record outside the child/carry contributes90h+44; exit contributes
`66N(h+1)+7h+168`. Their sum is exactly

`N(156h+126)+18h+203`.

Separately count only payload-port actions. The payload bit actions are

`N(117h+66)+156`,

and all are already inside the above instruction count. This is an action
subcount, not an extra charge. There are exactly13Nh key writes. The
uniform B6 envelope consequently gives the stated O(N(h^3+hp)) bound;
eliminating the host loop or ROM does not itself give a speedup.

The independent engine executes39 small helper cases at widths1,2,3,7,17,257
to check complete index creation, copy, retirement, nonoverflow carry and
final overflow. It also executes10 complete passes in both directions,
covering h1–3, p up to97, minimum precision, s=1, full s=N, a padded
nontrivial rotation and distinct translated origins. Those complete runs
total430130 literal instructions. All observed added bills and payload
subcounts agree with the formulas, and every current-index/record-position
boundary agrees with its independent direct index.

## 5. Fixed owners and historical union

The old14 private roles have exact stated window lengths

`(p+2), 4*(h+3), 3, (bit_length(h)+3), 7*(h+4)`.

Their sum is `p+11h+bit_length(h)+48`. The four p-bit header/row frames
occupy4p+9 cells; width occupies h+2; INDEX and ADDRESS each occupy h+2.
The21 marker-role envelope is therefore

`5p+14h+bit_length(h)+63`.

These are repeated windows on the same physical roles. Each child returns
its private window blank, and each record retires ADDRESS; the whole pass
retires INDEX. No allocation or owner multiplication occurs at an N or
2h-1 boundary. Larger old retained history must be unioned per role rather
than replaced by this current-size estimate.

The sparse checker distinguishes previous history from the newly visited
interval. It checks all current private/header/index/address grants, all
opaque sentinels and every returned head, while retaining deliberately
larger old extents. The payload visits exactly its frame and right frontier.
Returning omitted-payload-rewind and dirty-index-origin mutations are
detected separately. Physical owner aliasing is rejected by the binder.
No failure rollback or cleanup is inferred for malformed inputs.

## 6. Inverse overwrite and actual-source cost boundary

The inverse entry writes pi^-1(i) at current physical position i. It cannot
recover arbitrary old keys, because forward overwriting did not save them.
For original identity keys, the first correct sort sends original record i
to pi(i), the inverse pass writes i there, and the second sort returns the
record and its identity key. Arbitrary original keys do not follow this
argument. The explicit mathematical permutation control starts with keys
[3,2,1,0] and ends with[0,1,2,3] while restoring original payload positions.
The control's sorts are a mathematical oracle, not a new implementation
of the retained radix provider.

The exact caller AST is unchanged except for `prepare_keys`. The earlier
host `route_address` definition is retained but has no call site after the
replacement. The new seam binds the same private/header/index/address and
original payload objects, selects one fixed entry and checks its status.
Source production, numeric lease/staging/commit, source restoration and
retained radix remain the credited providers with their original costs.

The actual source receipts are cross-checked against the exact B6 receipts
for both#7388 and the current-wire-sensitive modulus-three case. Every
encoded-source, radix, owner-history, point-work and full-route component
agrees. At h=2,N=4 the added outer bill is1991 per leg and the payload
subcount is1356, already inside the new literal key-pass bill. The remaining
external payload charge156 and marker charge382 per leg are retained.
This is a cost-vector/seam audit; I did not rerun the complete external
source/radix providers, and no common cross-model tariff is inferred.

## 7. Reproduction and final limits

Run beside the package, or supply `--package` explicitly:

```sh
python3.12 -I -W error -B independent_check.py --package PATH_TO_PACKAGE
python3.12 -I -O -W error -B independent_check.py --package PATH_TO_PACKAGE
```

Both completed with identical PASS JSON. The default command writes no
files; `--write` explicitly requests a receipt. `RESULT.json` retains the
normal result, and FREEZE.json records the checker/review hashes.

This closes the stated local key-production and return claim. It does not
prove variable payload width, complete CRT-stage source orchestration,
initial ownership acquisition, arbitrary-key rollback, a global stock
theorem, any of the five foundational assumptions, or a new kappa.
