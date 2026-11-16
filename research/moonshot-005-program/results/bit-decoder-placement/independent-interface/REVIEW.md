# Independent review of separated-bank compression and fixed-port information

**Accepted within the stated interfaces. No new complete kappa.** This receipt uses a separately authored high-pivot binary solver and the retained independent rational-chart interpreter. It does not rerun either author's checker.

## Sharp canonical compression

The reviewed author proof is `work-b/four-bank-compression-target/PROOF.md`, SHA256 `f0efc6ed285578f69dd40225b9c7686f89c98640a7669f6b87b976e394141987`; its certificate is `9032709325131c05a50a0474d0213c2ad96f7fb39c124beddba9a9c6ebf7a118`. The native source and previously reviewed private-bank envelope are pinned by the checker.

The independent calculation reconstructs the rank80 side space, its rank88 enlargement after the83 existing recovered points, all four actual filter banks, and the canonical rank9 code. It verifies the eight conditional rank differences: `(3,3,3,4)` before the point announcements and `(2,2,2,3)` after them. All22 cut-dual identity matrices and all222 canonical reconstruction equations hold. Each of22 single-message deletion controls loses canonical recoverability.

The lower-bound proof is valid over every characteristic-two field and all positive block widths: quotienting by the side space and the other three banks kills their messages, so the remaining bank must contribute at least its certified conditional target dimension times the block width. Noncommuting block encoders do not evade this quotient argument. The displayed linear messages attain totals13 and9.

Root's separate `four-bank-compression-review/REVIEW.md` gives a sound finite-field nonlinear extension. On the certified input slice spanned by the cut duals, side information and all other banks are constant while the selected canonical outputs run over all `q^(dV)` values. Exact recovery therefore requires at least that many message values from the remaining bank. This proves the same per-bank bound for arbitrary nonlinear encoders with fixed bounded message alphabets. Summing the four inequalities is legitimate because each is necessary for the same code. The argument does not require the four input slices to coincide.

These are **fixed-side-information, direct-canonical-recovery** results. They do not price one physical packet, rule out arbitrary noncanonical fitting, or grant new decoded-point announcements after the messages. Rank80 and rank88 are different interfaces. Interactions that change what a bank knows can change the bound. Infinite-set nonlinear encoders are outside the finite-field counting statement.

## Fixed-port108 envelope

The independently replayed literal34 word is SHA256 `46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e`. From its actual seed cut, the checker reconstructs the fixed old P6/P7 prevalues and the four generously supplied banks of ranks52,53,7,53. It verifies **2,913 visible pure-X field incidences and6,465 visible actual principal-history incidences** are contained in the receiver's declared bank grant, raw local coordinates and34 globally granted completed points. This check includes every actually paid nonlocal cache; original Y nuisance is not converted into free X information.

Exact membership and iterative point feedback give108 receivers in one additional wave. The three displayed duals are verified against the entire final grant: `e24` for24, and `e42+e69` for42 and69. They annihilate all108 recovered points and separate the missing demand. Consequently the first-outsider argument excludes any further free point-feedback recovery. The dual indistinguishability proof also applies to arbitrary processing of these fixed measurements over any characteristic-two field.

The theorem fixes **source-bank assignments, leaf ports, the point-terminal information span and the actual P6/P7 preload classes**. This is stronger than granting one actual record at each port, so it is a useful obstruction. It does not prohibit changing the coded terminal space or coupling packets from different banks. In particular, the actual P0/P7 meeting at D3 can be used by a new chronology; that would be outside this separated-bank envelope. A port change is one possible escape, not a logically necessary universal remedy.

The72-family review separately establishes that its allowed perturbations stay inside the stated source banks. The current check establishes the complete actual34 stock/history domination. Neither assertion grants all historical rows globally or makes the108 optimistic fits into simultaneous physical deliveries.

## Reproduction

```bash
python3 check.py --repo /path/to/programme \
  --word /path/to/higher-source-thirtyfour/output/WORD.json \
  --envelope /path/to/private-bank-envelope/output/RESULT.json \
  --compression /path/to/four-bank-compression-target/output/RESULT.json \
  --ports /path/to/variable-load-envelope/output/RESULT.json \
  --out /tmp/final-interface-review
```

Expected: exact13/9 optima,22 dual identities,222 reconstruction equations,22 rejected deletions; full222-column replay,2,913 field and6,465 history incidences dominated, closure108 and precisely three exclusion duals.

Credit @CubeJerry; Worker B for the compression construction, root for the nonlinear counting extension, Worker A for the source and separated-port theorem, and retained source/envelope predecessors. Independent review by Worker C with OpenAI assistance. All foundational assumptions remain visible in the programme; no supplier or complete multiplication bound is asserted here.
