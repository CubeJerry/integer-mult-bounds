# Final ledger consistency audit

Audit snapshot: **2026-11-13 21:20:03 UTC**. This is a read-only local consistency audit of STATE.json, FINAL-HANDOFF.md, nine current review-link receipts and the three newer separate remote-verification receipts. No remote requests, scientific reruns or package-worktree edits were made. Recorded remote verification is checked for internal consistency, not newly performed here.

**Result: nine current publication entries agree exactly on head, branch, title and compare URL.** Each current review-link receipt records HTTP 200 and the expected branch. The three separate newer remote receipts also agree on commit, tree, parent and checked-blob count. STATE and the handoff both count nine contributions. The tenth, carrier943, remains pending in this snapshot; it is not counted as published.

| Receipt | Exact branch | Exact head | STATE comparison |
| --- | --- | --- | --- |
| bit | `research/bit-alternate-carrier-zero-pairing-20261113` | `34016136b3aadfcace5116aac0da70e7bc4637ff` | match |
| mixed | `research/complex-contact-recharting-bound-20261113` | `88665d52c614eb1b33c8b78aa7e35f90d68e4ff5` | match |
| cold | `research/p104-all-helper-zeroing-bound-20261113` | `4f83ab5c0a9c505159031c1f86d2f428b0ea9583` | match |
| cache | `research/p104-earlier-destination-cache-bound-20261113` | `fdbb41450a98594bdf1f5fe4535e77d2466adb4f` | match |
| joint | `research/p104-joint-helper-cache-funding-bound-20261113` | `509baf4514966e4202cfdde379d7adf3085b1cc7` | match |
| native-interface | `research/selected-move-packed-grid-interface-20261113` | `e9b6d75397e3553af77bab81d5816e4b8708a501` | match |
| public-price | `research/p104-public-cache-price-screen-20261113` | `732ed51e1f05457c2d14c90b9d766321e48ed14c` | match |
| relation-family | `research/p104-public-relation-family-bound-20261113` | `2a7f914f530cf357db296ee7951eb9ba053c014f` | match |
| rank1-zero | `research/p104-rank1-zero-cache-bound-20261113` | `c617da336e15f9a15311500d46e724dbf7e8ad69` | match |

## Claim and pending-scope checks

The selected conditional value remains `363005817/100000000000 = 0.00363005817` at canonical base `e54523517d0f03e58352e647c403a5af3e525a57`. No inspected handoff or current receipt asserts a new attained exponent, unconditional multiplication theorem, source/supplier admission of unselected #7481, or discharge of any of the five foundations. The joint package's numerical crossing is expressly an exclusion ceiling. Public-cache prices are per-target optimistic allowances rather than a summable physical gain. The selected packed-grid result expressly requires a faithful **paid** packed bridge.

Carrier943 is correctly separated from those nine publications. The pending handoff limits it to the nominated MOVE40710 replacement, with all other original jobs/target credits retained, fixed invocation dataflow, charged information-bearing cross-frame edges, no unpriced routing/control, no existing-payload piggybacking and no cross-call amortization. Its negative budget is not physical source admission. The completed worker numeric certificate proves only `M + 17*(f(8)-f(1)-f(4)) < 0` at `kappa=19/5000`; commit `509baf...` is inherited **invoice verification**, not admission. The handoff's “last numerical/publication gates in progress” is therefore a publication-stage status, not a new scientific claim. After the tenth package is actually published and remotely checked, all counts/heads/statuses should be refreshed together. No upstream PR submission is claimed in STATE.

## Metadata discrepancies to resolve or label historical

1. `evidence/publication-receipts/cache-review-link.json` is an older mirror at `796b03407d4d05da0390ebc6b28ab98a98c4fa6d`; the current root receipt and STATE correctly name `fdbb41450a98594bdf1f5fe4535e77d2466adb4f`. Refresh that mirror or label it superseded.
2. `evidence/publication-receipts/cold-review-link.json` still names scientific-extension head `70d3eda833dde704522efad3ca155bc5aeb959b3`; the current root receipt and STATE correctly name metadata-followup head `4f83ab5c0a9c505159031c1f86d2f428b0ea9583`. Preserve its historical scientific role while disambiguating the current branch head. The current cold receipt intentionally links the earlier scientific PR description; its commit field is current.
3. `STATE.active.root.scope` says “Six published packages” while the current root status, contribution list and handoff say nine. `STATE.artifacts.joint_funding` still says “UNPUBLISHED” although `joint_published` and the contribution list record `509baf...`. These are stale labels, not mismatches in current heads. The timestamped six-package local checkpoint note is historical and is not itself inconsistent.
4. `STATE.active.bit_gain.status/next_action` still describes the integer-power checker as active/to freeze, although it is frozen. Refresh this progress label during the tenth-package update.

The publication-receipts evidence directory currently contains four older review-link mirrors, whereas all nine current review links and the three newer remote receipts were inspected at workspace root. If the final repository export is intended to carry the complete receipt set, copy or explicitly reference the current set there rather than relying on those two stale mirrors. This audit does not alter or validate durability of unbundled workspace files.

## Exact audit inputs

| Ledger file | Bytes | SHA256 |
| --- | ---: | --- |
| STATE.json | 30368 | `3aa70869e7ebff6aa28d9c588c7ac426f32c15ab0b190d354e15e6913dca00ed` |
| FINAL-HANDOFF.md | 7149 | `4595077bf5988163b581d48ce2eab9b848e5c268c33538ed758b267559a3f3bf` |

Current receipt content hashes, including the newer independent remote receipts:

| Receipt | SHA256 |
| --- | --- |
| bit-review-link.json | `a7ec81f27c7dc43968e0b68ff3d47e955f53ddeb7b15039dd66777ebbc47533c` |
| mixed-review-link.json | `af0029dd7e54e6a1d33e6875a92b8a5c6447a814e8d8f4b6332e983c5116f3db` |
| cold-review-link.json | `7e4fa2a5ea262ed61f38146988e67013867de0c2ba00dc92ee027b12045ce442` |
| cache-review-link.json | `5c330be45e4c604bd92174f4a725f442400e7d77fadd72167c2b5692d8fa7a42` |
| joint-review-link.json | `ac1a04df1d5f91e30add0b9971df764fe11ba366ae25259f432767254e7ddae2` |
| native-interface-review-link.json | `4de1deb2d0fa6c8c65b6fd6f339b14c0c24fd4883ab5c4902c33298c2fa678e4` |
| public-price-review-link.json | `4496d4ad73b189ce06435e5ca8dbbfa94fa56144eb5bda83a38eb66a0a08c712` |
| relation-family-review-link.json | `89590c6efae2fdb70ee303004f904f6e6fc83d3d12a549c87815de546bd6776e` |
| rank1-zero-review-link.json | `717632efdb2765ff614669227ffcf7396034645c7646dd9d15d5479889e652d1` |
| public-price-remote-verification.json | `11dac6d2a7c1c861d1c026f769b17bac0f92c4a7b7570c07a5b7f382e706d402` |
| rank1-zero-remote-verification.json | `a96c1f825330c30a2cec67070eb007002807779b724afaf3a9020ef50d6b70ad` |
| relation-family-remote-verification.json | `166a718c7a978ff370ce618cd1ae78b6a8293f23511942e81804f22dc17006a5` |

Both ledger files were re-read immediately before writing; bytes still matched this snapshot. Findings concern the nine-package snapshot only; a concurrent later tenth-package update supersedes its count.
