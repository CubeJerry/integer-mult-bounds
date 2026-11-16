# Reproduce the cheaper41 source

From the repository root, with SymPy for the independent interpreter:

```bash
programme_path=research/moonshot-005-program
package_path=$programme_path/results/bit-proper-birth-reduction
full41=$programme_path/results/bit-common-triple-retention/author/stages/clique41/WORD.json
engine_path=$programme_path/results/bit-leaf-capacity-quotient/author/check.py
price_path=$programme_path/results/bit-common-terminal-reuse/independent-review/check.py
python "$package_path/author/optimize_word.py" --word "$full41" --out /tmp/moonshot-reduced41
python "$package_path/independent-reduction/check.py" --repo . --base "$full41" --word "$package_path/author/reduced41/WORD.json" --author-price "$package_path/author/reduced41/PRICE.json" --engine "$engine_path" --price-engine "$price_path" --out /tmp/moonshot-reduced41-review
python "$package_path/author/proper-birth41/build.py" --repo . --base "$package_path/author/reduced41/WORD.json" --engine "$engine_path" --price-engine "$price_path" --out /tmp/moonshot-proper-birth41
python "$package_path/root-birth-review/check.py" --base "$package_path/author/reduced41/WORD.json" --word "$package_path/author/proper-birth41/WORD.json" --out /tmp/moonshot-proper-birth41-root.json
```

Expected final word SHA2566c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9;118 INIT/798 ADD/450 MOVE/118 dirty CLEAR; all41 endpoints and all222 original columns; Q1616.8469797526895420964..., necessary limiting room4.9039004584628131498.... Intermediate inventory and history are deliberately changed.
