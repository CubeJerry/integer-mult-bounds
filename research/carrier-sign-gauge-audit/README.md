# Independent audit of the P104 carrier search's sign pruning

**No defect found in this pruning step. No new κ.** An independent orbit oracle
and a written stabilizer proof corroborate the sign normalization and component
merging in Matarener's [PR6166](https://github.com/CrocSwap/integer-mult-bounds/pull/6166).
Every residual sign orbit has exactly one retained representative, and the
normalizing transformation preserves the earlier coefficient choices and the
decoding equations. This supports one dependency of the proposed exclusion;
it does not independently establish code uniqueness or the descent-cost bound.

The frozen subject is `code8.py` at
`f7d6431080b375914216d76a8a6426f50c524471`. The source and its original proof
are retained byte for byte in [inputs](inputs), with attribution, commit,
Git-blob and SHA256 pins in [UPSTREAM.json](UPSTREAM.json). The new checker
does not run the predecessor's Gaussian elimination or search certificate.
Its independent engines are breadth-first traversal of raw sign orbits and
hypergraph connectivity, compared with the actual source routines.

## Exact result and coverage

[PROOF.md](PROOF.md) proves the history/stabilizer and completeness implications
for any finite history assigning each port at most once. [RESULT.json](RESULT.json) records the
separate exhaustive finite evidence:

- 4,140 partitions of eight pivots times 70 four-subsets: **289,800 states**.
- **11,592,000** source canonicalization checks and the same number of merge
  checks, including zeros and every normalized ternary sign pattern.
- **670,680** independently computed support-connectivity updates and
  **1,059,840** sign assignments on representative coefficient histories.
- **30,720** transformations of the actual source equation systems, comparing
  **1,255,168** encoded rows, including each diagonal right hand side.
- Five semantic controls detect over-pruning, duplicate representatives,
  omitted merging, merging untouched components, and a missing column sign.

This domain includes all 14 actual P104 support blocks and also abstract states
that may never occur in its search. It is a complete finite audit of the stated
routine domain, not a larger decoder search or a formal proof of the full theorem.
The written all-history proof is distinguished from the representative-history
tests. Normal and optimized replay must produce exactly the committed receipt.

## Reproduce

From the repository root with Python 3.12 and only its standard library:

```sh
python3.12 -I -B research/carrier-sign-gauge-audit/verify.py
```

Expected: `PASS_CARRIER_SIGN_GAUGE_AUDIT states=289800 merges=11592000 controls=5 no_new_kappa`.
The complete run took about 47 seconds on the session host; this is a runtime
estimate, not a performance comparison. The registered command also runs the
same audit with `-O`, using explicit checks that survive disabled assertions:

```sh
python3.12 -B scripts/research_package.py --package research/carrier-sign-gauge-audit
```

`--write-result` is an explicit receipt-generation option, never needed to
verify. No network, solver, native compiler or Lean installation is needed.
See [VALIDATION.md](VALIDATION.md) for checks actually executed and their limits.

## Pins, novelty and limitations

Base main: `3f0152a32eeebac0df11946dbd50cabe5a7f7839`; priority revision 8;
accepted κ remains `781451/250000000` (PR6030). [SOURCES.json](SOURCES.json)
pins the selected word, whose only role here is supplying the 104 initial live
frames. No endpoint, native operator, caller, pricing or outer-bound replay is
claimed. The five selected framework assumptions are unchanged.

PR6166 already supplies the pruning argument and its certificate replay. This
package adds an independently implemented exhaustive symmetry audit and explicit
failure witnesses, not a new discovery of the code or its cost floor. Brett
Halligan's PR1212 concerns characteristic-zero rank-eight rigidity on specified
root sets; this audit concerns the later finite-field search's pruning machinery.
PR6167's cache chronology and PR6168's projector/finite-period identities are
distinct concurrent work. The prior F7 parity audits, P104 scalar sign propagation
and signed-sparse degree prune concern other predicates and are not re-opened.

The source commit association was checked against the fetched PR head during
this session. Standalone replay checks retained bytes by SHA256 and Git-blob
hash; it does not authenticate remote Git history. The pending PR is not a
publication-ancestry dependency. Its two retained source files allow offline
review without fetching that unmerged commit.

Still unreviewed here: equation-model completeness, elimination, certificate
traversal, the unique-code count and weight distribution, rational reduction,
delivery decomposition, frame-capacity and descent-cost arguments. No human
review, formal proof-kernel certification, CI pass or full selected cold replay
is claimed. Nothing outside this isolated package is changed.

## Open next questions

Independently check PR6166's equation encoding and consistency decisions before
replaying its certificates: build a separate dense F3 model at the same frozen
head and compare constraints and rejection witnesses. This matters because
symmetry completeness alone does not certify uniqueness. It requires a separate
review scope and the complete certificate inputs; no mathematical blocker is
known. The structured handoff is in [TASK.json](TASK.json).

## Attribution

Prepared for **Jerry Chen (@CubeJerry)** with substantial **OpenAI Codex**
assistance in reasoning, implementation, verification and writing. Credit
**Matarener**, with Claude (Anthropic) via Claude Code, for PR6166's proof and
retained implementation; **DreamingOfClouds** for PR6030/5907; **Ali Romman** for
the P104 word/checker lineage; and **Brett Halligan (@burntout76)** for PR1212.
New material and retained subject sources are Apache-2.0. Original notices are
preserved. [CLAIM.md](CLAIM.md) records the OS draw 66, candidate selection,
coordination limits and checkpoint outcome.
