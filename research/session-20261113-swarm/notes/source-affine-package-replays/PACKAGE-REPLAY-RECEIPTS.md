# Frozen source-affine package replay receipts

Package: `publication/source-affine/research/literal-source-affine-move/`.
Outer freeze SHA-256: `8386424089c82752da129717c93c89af68f1cabc039ae6d6664989c1e7a3f345`.

Seven registered command results:

| Replay | Output/receipt | SHA-256 | Result |
|---|---|---|---|
| Author normal | `package-replays/author.normal.stdout` | `8ed345e3abc86895a0a2866882069d986220d8e0ec08f27482a6fc1017431e8c` | PASS_SOURCE_BOUND_AFFINE_MOVE_HOME |
| Author `-O` | `package-replays/author.optimized.stdout` | `c728a2f732667a0c023839756af1c4c262f8570be9841929ed365049194298e0` | PASS_SOURCE_BOUND_AFFINE_MOVE_HOME |
| Independent kernel normal | `publication/source-affine/research/literal-source-affine-move/review/independent/RESULT.normal.json` | `219c61bfb47f48d9e63012fae2bd0000f37dcb8720db8e9090c5b4b5eb62662e` | 512 basis inputs / 4,096 exact nonzero entries, five mutants rejected |
| Independent kernel `-O` | `publication/source-affine/research/literal-source-affine-move/review/independent/RESULT.optimized.json` | `219c61bfb47f48d9e63012fae2bd0000f37dcb8720db8e9090c5b4b5eb62662e` | Byte-identical to normal |
| Derivative AST normal | `publication/source-affine/research/literal-source-affine-move/review/independent/DERIVATIVE-AST.normal.json` | `87ce0928603b4fc3b463e0494ce1b80eb91fddab1f40f95bd53471ef3c909f1a` | 13 mathematical/negative-control function ASTs identical |
| Derivative AST `-O` | `publication/source-affine/research/literal-source-affine-move/review/independent/DERIVATIVE-AST.optimized.json` | `87ce0928603b4fc3b463e0494ce1b80eb91fddab1f40f95bd53471ef3c909f1a` | Byte-identical to normal |
| Root sparse machine | `publication/source-affine/research/literal-source-affine-move/review/root/RESULT.json` | `508ce98e70e9e0bef11432635f814a793f3165a3f1b9ded2822381ca3e2b87c7` | PASS_ROOT_SOURCE_AFFINE_MOVE; 118,744,836 steps; 20,496 late HOME writes; 35 heads/private/exteriors restored |

The root command was executed on the frozen package copy with explicit `implementation/` argument; it was not repeated after packaging. The copied root receipt is the exact output of that independent run. The author package's `normal.log` and `optimized.log` are preserved unchanged under `implementation/`; the two `package-replays` stdout files separately capture the registered commands run against this staged package.

Schema validation receipt: [`METADATA-CHECK-RECEIPT.txt`](METADATA-CHECK-RECEIPT.txt). It reports `PASS_PACKAGE_METADATA_AND_PINS`; this checks metadata schema and source pins only, not theorem acceptance.
