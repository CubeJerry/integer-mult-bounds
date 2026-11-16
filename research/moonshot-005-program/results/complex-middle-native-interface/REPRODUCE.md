# Reproduce the middle-native interface controls

From the repository root, with SymPy installed:

```bash
package_path=research/moonshot-005-program/results/complex-middle-native-interface
python "$package_path/author/check.py" --repo . --output /tmp/moonshot-middle-author.json
python "$package_path/root-review/check.py" --repo . --proof "$package_path/author/PROOF.md" --out /tmp/moonshot-middle-root.json
```

Expected: exact free-word identities and independent actual-source Gaussian-rational matrix controls both pass. The finite controls authenticate the equations; the cited finite tensor-separation proof and independent written audit establish the universal projection scope. No profitable caller is produced.
