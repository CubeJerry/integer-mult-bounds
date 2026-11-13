# Target bridge audit: movement (k), covered (C), completed (B)

This is an exact arithmetic/provenance note only. It supplies no new BIT construction, covered saving, ordinary saving, or supplier.

## Conditional arithmetic

The retained ordinary seed is (b_0=12039/3125000=0.00385248). The target-bootstrap theorem takes as input a *covered* BIT saving (C), already after finite compilation and paid cover loss, and a completed arbitrary-width ordinary saving (b). It does not take a MOVE exponent (k) as either input.

The exact one-stage condition for (B>1/200) is

\[
C>3112961/621875000=0.005005766432160804\ldots.
\]

For two stages, the exact strict reachability condition from (b_0) is

\[
\frac{C^2(C-b_0)}{1-b_0}<\frac{C-B}{1-B}.
\]

The retained sufficient witness is (C=50001/10000000=0.0050001), changed atom exponent (\rho=51/10000=0.0051), (b_1=15607/3125000=0.00499424), and completed (B=500007/100000000=0.00500007). All eight stage gaps were independently recomputed as exact rationals in `RESULT.json`; in particular, the relaxation gaps are (3569/500000000000) and (57/500000000000). Thus this witness strictly clears (1/200), conditional on its inputs and stock contracts being supplied.

The q8 strict-price receipt tests movement exponent (k\in[1/200,2503/500000]=[.005,.005006]) for a hypothetical **MOVE-only** profile (Q=\{1:1618\}). It proves positive per-rail movement margin at (m=6) throughout the interval, with one additional unit-rank MOVE affordable and two unaffordable; the all-finite-(m) limit permits at most three. The q8 target records that the complete source is not constructed. It also explicitly excludes ADD/COPY/SCALE/INIT/CLEAR costs from (Q), and requires a causal word with all 222 endpoints, histories, chart maps, and ownership/erasure.

For scale only, if one *assumed* (k_{max}=0.005006) were a pre-loss raw saving, then to get the one-stage covered threshold the total conversion loss would have to be less than

\[
2503/500000-3112961/621875000=581/2487500000\approx2.33568\cdot10^{-7}.
\]

To reach the retained two-stage sufficient (C=0.0050001), that hypothetical loss could be at most (59/10000000=5.9\cdot10^{-6}). These are conditional differences, **not** a proved relation (C\ge k-L); the current receipts give no (k\to C) conversion theorem. The exact checker rejects any interpretation that treats these gaps as supplier credit.

## Required source-to-admission obligations

1. Construct and replay one causal word that acquires all eight packet forms from available source histories, restores every X row, and computes every (Y_i=y_i+x_i) on all 222 arbitrary inputs. The B8 reference is an explicit failure (Y=y+Bx); cut saturation alone is not completion.
2. Verify scalar historical fitting/mode constraints, all actual chart maps and lifetime/clear behavior. Current q8 analysis gives a scalar historical fitting rank requirement of at least 10 and at least two independent historical directions beyond eight full-rank ground modes; for arbitrary blocks it does not establish a (10V) rank bound.
3. Produce a complete signed paid/target invoice for the *actual* word. (Q=\{1:1618\}) contains only the proposed unit MOVE paths. The positive (M_6) margin cannot silently pay ADDs, compiler operations, covers, strictification, source acquisition, extra routes, or ownership cleanup. At fixed (m=6), it can absorb only one additional unit-rank MOVE.
4. Bind a finite all-width compiler/cover proof to the word, with exact cover and strictification loss, all native columns, and a rational covered (C) satisfying the strict one- or two-stage condition. (k) remains a test exponent until this proof exists.
5. For the two-stage witness, rebind the retained arbitrary-width ordinary primitive, stock formula, spectator/ROW restoration, high-digit exchange and finite threshold constants at changed (\rho=0.0051). The selected (\rho=0.004) does not supply this contract. Complete the two wrappers to an ordinary (B>0.005).
6. Outer target admission separately still needs a compatible uniform complex (U>0.005) and every retained foundation; those are not implied by a completed BIT (B).

The strict-price interval proof is arithmetically sound; the missing step is a complete source and charged compiler/cover contract. No hidden exponent or price substitution was found.

## Pinned provenance

- Target reachability proof: `programme/research/bit-target-bootstrap/PROOF.md`, SHA256 `fff9e71930ceb31c82b3a56c245cd2ae4209451a937f7ccdc24142f74b0eaf2e`.
- Target receipt: `programme/research/bit-target-bootstrap/RESULT.json`, SHA256 `1a9114afbfe9d1eb97e26f5b613014632585ca3584d46db3a324dfaa691cdcf4`.
- q8 target/admission: `programme/research/moonshot-005-program/results/bit-eight-packet-target/author/TARGET.md`, SHA256 `45d27355d3e6f7d88617dd0473a076b20f1a4b2cb3339b58429eaf806b73061e`; `ADMISSION.md`, SHA256 `644b508b78c3237a64a124657e4e171cc78b01daae1103c54b82eb24034ea47e`.
- q8 unit MOVE receipt: `.../bit-eight-packet-target/author/RESULT.json`, SHA256 `f1ec7b16a986c7b7ce7d9a3788bbea2943810cfd70386e554bd14a21759e07e2`.
- Uniform movement proof/receipt: `.../strict-price/author-uniform/PROOF.md`, SHA256 `fb8e8592a7305fd27797047a73807160cffb207fdf5121b438e60dbe1e55a1a7`; `RESULT.json`, SHA256 `8178c76d1a20c39faf11c02bbb1c143eff151c4bb7ad717fd098ba8067137936`.
- Exact two-price MOVE calculation: `.../strict-price/author-two-prices/PROOF.md`, SHA256 `3ad51ec509305fa86e4052c9491f77f53cf3cddf7cff53bd2600d87e8ae4225b`; receipt SHA256 `1ead49806d5bde7e0be794c362ab8abba657dfdaeb1fb5278feb051ab6016397`.
- Independent uniform movement review: `.../strict-price/review/REVIEW.md`, SHA256 `3fcaba51397f532af7b35035b3f658d913c54a0b4cff18db18162b4ca32bcdda`; receipt SHA256 `61d93d95db5460899710f054aa5230fd3569c7911b549f0b3be86494d04f8117`.

Run `python check_rational_bridge.py --bootstrap programme/research/bit-target-bootstrap --strict-price programme/research/moonshot-005-program/results/bit-eight-packet-target/strict-price --output worker-c/target-bridge-audit` for the exact witness and loss-gap arithmetic. The checker verifies conditional identities only and deliberately asserts no (k\to C) implication.
