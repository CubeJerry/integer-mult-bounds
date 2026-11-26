# S007 verification

| Claim | Evidence checked | Scope |
|---|---|---|
| Both directions through real FS1 factors | [Root replay](verify-plane-directory.py), [separate interpolation and idempotent reconstruction](verify-plane-independent.py), [degree 15](plane-directory-b15.json) | All 2,192 factors at degree 15 match ordinary polynomial division, including 32,768 independent inverse bits and a nonterminal coefficient prefix. |
| Short-key sort replaced in both directions | [Marked subspaces](marked-plane-directory.md) and [cyclic-window construction](structured-orbit-directory.md), with independently written checkers | Exact FS1 serial order, two distinct field presentations, duplicate matches, short periods and proper subfields. The marked route checked 68,760 dense addresses. |
| Tape convolution and bounded words | [Native compiler](lane-packed-convolution.md), [first review](compiler-audit.md), [second review](review-lane-packed.md), [jet replay](padded-convolution-receipt.json) | Sixty-nine independent packed products matched direct convolution. Every rank-six binary mask was tested by a separate fixture. The tools use direct arithmetic on finite instances. |
| Ordinary product | [Grid and factor routes](ordinary-binary-product-cases.json) | Both paths matched 36 products through 2,048-bit inputs. |
| Actual first carry and modulo-four product | [Signed monic division](first-witt-carry-receipt.json), [converse](half-square-converse-cases.json), [nonfield jets](mod-four-jets-receipt.json) | 425,222 binary-input factor comparisons, 262,944 modulo-four factor comparisons and 40 unrestricted modulo-four products in the converse fixture. Nilpotents and the inverse normalization were exercised. |
| Precision-independent Pascal word | [Finite coefficient checks](precision-striped-pascal-receipt.json) | Fixed word shape, moduli $2^H$, true positive and inverse subset-sum transforms. |
| Mathematical time and cumulative tape space | [Complete theorem](binary-transform-and-product.md), [modulo-four compiler](mod-four-batch.md) and [ring review](review-mod-four.md) | Written proofs. Python run times are not measurements of a fixed-tape machine. |

A [two-stage triadic implementation](macro-triadic-product-receipt.json) checked 12,960 transform coefficients and 3,388 ordinary product coefficients. Complete integer guard tests at 1,000 and 3,072 bits checked the final carry scan. This route gives a simpler, asymptotically slower integer bound than the retained square-root envelope.

The [fixed-precision evaluation](fixed-witt-precision.md) was checked against 32,512 independent Witt-coordinate Horner evaluations, 16,256 literal modulo-eight factor comparisons and 4,132 arbitrary inverse inputs. A [second implementation](fixed-witt-independent-cases.json) uses literal quotient rings and checks Hensel roots and higher Hasse terms at precisions four, five and six. The [separate macro-transform replay](macro-ck-independent-cases.json) compares 39,204 transform symbols, five complete outer products, and 19,602 coefficient positions. [Independent review](review-macro-and-fixed-witt.md)

## Reproduction

Run `python3 verify-session.py` in this directory for the recorded numeric fixtures. It compares decoded JSON values for every run and reports the SHA-256 of each expected certificate. [Verification driver](verify-session.py)

The [formal checker](../../contributions/explicit-overhead/formal/check.sh) pins Lean 4.34.1, Mathlib and the reused OpenAI source modules. It builds the deposited Lean sources with warnings as errors, kernel-replays each named module, and rejects any designated theorem with axioms outside `propext`, `Classical.choice` and `Quot.sound`. [Kernel transcript](lean-axioms.txt)

Lean verifies individual-factor membership and product, arbitrary low-degree CRT lifting, selected orbit coverage, actual ordinary-product reconstruction, moment and affine-chart identities, the masked tensor identity and the two-Witt-coordinate formula under its literal-root and remainder hypotheses. The October finite word has its own source pin and [kernel receipt](fourier-word-kernel.txt). The exponential design constants, full fixed-tape implementation, cumulative physical complexity of the new algorithms and complete integer theorem remain outside the Lean proof.

## Verified release totals

The complete pinned run built and replayed 23 component modules, auditing 139 named results. The actual scalar specialization of the divided-square product identity and the triadic cyclotomic restriction, lane basis, transform entry and chirp are included. Fresh-environment spot checks include the binary factor inventory, masked tensor, literal Witt carry and trace-fibre join. The [numeric transcript](numerical-replay.txt) records all 28 matching certificates.
