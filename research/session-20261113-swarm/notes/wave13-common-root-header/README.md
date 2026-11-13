# Selected common-root header compatibility gate

Read GATE.md. The actual input's descriptor is separate from DATA. Keeping
DATA alone in a HOME and a private native HEADER avoids any requirement
that native Gamma6 headers have equal length. The source-specific runtime
header/view producer and fully restored wrapper remain missing. This is
a bounded dependency gate, not a standalone PR or new precision theorem.

The common root format simplifies to fractional bits p0+D_total and signed
width p0+2D_total+4, independently of Q0. Native P/S geometry must preserve
the complete root factor and every unselected/compact coordinate. These are
exact substitutions into the pinned selected source, not new suppliers.

```sh
python3 -I -W error -B check.py --source-repo /path/to/read-only/repo
python3 -I -O -W error -B check.py --source-repo /path/to/read-only/repo
sha256sum -c CHECKSUMS
```

The check performs compact exact extraction and geometry corroboration. It
does not run a literal tape wrapper or an exponentially large payload.
Earlier frozen packages remain unchanged. No remote mutation was performed.
