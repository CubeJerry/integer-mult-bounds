# Verification

## Actually performed at checkpoint 1
- Read current remote `AGENTS.md`, `autoresearch.md`, `CONTRIBUTING.md` at canonical main SHA e54523517d0f03e58352e647c403a5af3e525a57.
- Read OpenAI `uniformity.tex` at math SHA 3344da59991ed94f9ba711217b29c1d760badfa6 (blob 5ea562044e8830c8402f2a61caf8729dd2feb086).
- Read prior moonshot STATE.json at legacy branch (blob 411eb5aba139d47ff3d705cb7da51a4d42660d64).
- Verified absent new branch then created at exact canonical commit.
- Mathematical hand derivation: if round s is O(2^s) and successful attempt i requires t steps, s=i+ceil(log_2(t+1)); sum of rounds O(2^i(t+1)). This is the same bound as the cited source and is not independent certification of its implementation.

## S002 first-wave evidence

Three genuine concurrent research workers produced independent routes; the lead read the critical first-wave proofs and replayed isolated copies of their verifiers. This is AI-assisted independent review, not human refereeing or kernel certification.

| Replay | Main finite checks | Failure controls |
| --- | --- | --- |
| A scheduling/chunking | 1,024 rounds; 19,999 indices; 145,636 exhaustive products; 980 larger products; 3,840 cap boundaries; 867 polynomial thresholds; 1,024 slack cases; 5,208 recursion counts | Omitted carry logic rejected. |
| B Newton/division repair | 8,340 rational count cases; 2,559 pair marginals; 1,544 finite repair matrices; 184 arbitrary-support identities | Wrong transpose, zero and nonunit gaps, unbalanced shifts rejected. |
| C count barrier | 33,152 prefix identities; 16,380 small sign patterns; 1,473 exact interpolants; 510 shifted histograms | Characteristic-three counterexample prevents an invalid field extension. |
| Recovered B contraction | Exact modular Walsh repair and finite unrolling on 64/256 rows; 4,096 shifted-frequency checks | Omitted repair creates 16,328 mismatches. |

Replay records under `verification/S002/` contain script hashes, interpreter version, command output and exit status. Exact small-case checks support but do not replace the unbounded-size proofs. The compact predictor and Hermite-table scripts have their own result files; these must not be described as full multiplier tests.

The source manifest checks 103 available primary-source files against the pinned Git blob identities. Integrity coverage is distinct from the proof-reading coverage recorded in SOURCE-AUDIT.md.

## Not performed

No Lean build; no complete re-derivation of all Fourier/tape/lower-bound chapters; no all-size generated multiplier; no new multiplier runtime measurements; no new complete conditional or unconditional H(n); no independent human refereeing; no full scientific cold replay. Literature and live discussion coverage remain partial. All such status remains open until the corresponding work is actually performed.
