# Reproduce the source-aware41 construction

Run from the repository root, using Python with SymPy for the independent interpreter.

```bash
programme_path=research/moonshot-005-program
package_path=$programme_path/results/bit-common-triple-retention
python "$package_path/author/reproduce_clique_chain.py" --repo . --base36 "$package_path/author/stages/reprogram36/WORD.json" --expected41 "$package_path/author/stages/clique41/WORD.json" --out /tmp/moonshot-triple41-reproduction.json
python "$package_path/independent-review/check.py" --repo . --stages "$package_path/author/stages" --engine "$programme_path/results/bit-leaf-capacity-quotient/author/check.py" --price-engine "$programme_path/results/bit-common-terminal-reuse/independent-review/check.py" --out /tmp/moonshot-triple41-review
```

Expected: byte-identical four-stage reconstruction and independent all222-column replay,129/948/460/129, common rank17,70 closure duals and20 rejected semantic controls. Individual build scripts accept --repo, --base and --out to regenerate each stage's complete receipts. The general lemma is a written proof with a separate root audit; finite replay authenticates its concrete source instances.
