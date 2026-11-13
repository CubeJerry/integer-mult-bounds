# Cumulative filters for the temporal zero-erasure two-cache bypass

All 16 owned MOVEs that failed the live-source span test also fail both
necessary temporal filters on exact #7481. This rules out the specified
unchanged-history two-cache primitive; it is not an unrestricted cache bound.

Source gzip SHA256:
acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9.
The candidate ranks are {1:6,2:1,3:1,4:5,5:2,6:1}, including eight ranks>=4.
All 1,501 original public inputs remain arbitrary.

At a candidate event E, the owned mover has latent row x and travels A→B.
The proposed bypass needs a B cache formed strictly earlier and an A cache
cleared from a strictly later native A bank. It must clear all extra caches
to zero, preserve the arbitrary-input map and pay every extra operation,
slot and lifetime. No nonzero-cache erasure is granted.

For the earlier-B filter, initialize each cumulative span with its public
entrance rows, then add rows at earlier MOVE arrivals. Coframed arithmetic
adds no direction outside the current historical span. The candidate's own
arrival is excluded by querying before it is observed.

For the later-A filter, initialize with the final native A banks and scan
backwards. Add rows at strictly later MOVE departures and CLEAR positions.
Every native ADD and nonzero SCALE preserves the coframed bank span; COPY
into ideal zero is an ADD on the actual state. INIT contributes only zero.
Therefore the backwards cumulative span contains every strictly later native
A bank. Query before adding the candidate's own departure, excluding its
original x at A from the permitted future information.

The exact sparse-rational interpreter processes all 76,475 instructions and
checks all 16 earlier and all 16 later conditions. Earlier-B hits: 0. Later-A
hits: 0. Survivors: 0. Runtime was 8.48 seconds. FILTER.json retains the exact
generator rows, cuts, target rows and outcomes. Equal-subspace alias
normalization is granted, so the filters enlarge literal equal-frame banks.

A single actual earlier/later provider must lie in these larger cumulative
spans. Since both filters fail, no single-cut sharpening, physical word or
paid-budget gain is justified. The result does not exclude imported/moved
cache information, changes to the native history, other input restrictions,
or a provider allowed to erase a new nonzero cache under a separately proved
contract. The five inherited assumptions remain unchanged.

Reproduce with the standard library:

```
python3 -I -B worker-b/two-cache/filter.py
```

The filter reuses the frozen historical-span and exact row helpers; no source
or sibling file was modified. Related #7308 owned-destination work does not
by itself establish this temporal result. Root owns final related-work
classification and integration. Credit the source/native lineage and root's
temporal two-cache research scope. Substantial OpenAI assistance; Apache-2.0.
No publication, new supplier, new kappa or physical implementation is asserted.
