# Corrected independent review: three canonical rows at M1

## Decision

**PASS**, for the exact word pinned below. The word preserves the 46 completed
outputs, restores all 111 originals, and replaces the three actual retained
M1 fields by independent rows of the canonical binary rank-nine code. Their
simultaneous custody is physical: each field exists at M1 when P5 resets there,
and a legal joint read/unread probe passes. This is a source change, with no new
completed output claimed.

The equal real chart names M1 and C2 are treated as one physical chart.
The actual final-live M1 inventory has rank **13 before and 13 after**. Its
intersection with the canonical code changes from **0 to 3**. Thus three source
directions are replaced; the total M1 rank does not increase by three.

The review imports neither the author builder nor its trace or representation
functions. It uses the pre-existing metadata-free exact rational geometry and
222-column replay engine, an independent operation-alignment and source-reader
analysis, and the separate integer-bisection price engine.

## Exact inputs and reproduction

| Input | SHA256 |
| --- | --- |
| Native roots | `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e` |
| Early-release41 | `509fe171db1fb0f82d9452c52e53166cae41da6f0c1700b10d8ef5db00ad28f2` |
| Early-paid46 base | `27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd` |
| Canonical M1 word | `7d2fea44d7bdf8b3a63807f88371cad28f9303649db66b7d4ccbb56e9c180ada` |

From the workspace root:

```sh
python3 -B workers/audit/semantic-inventory-correction/check.py --repo programme --early-word workers/root/early-release41/WORD.json --base workers/coded/early-paid46/WORD.json --word workers/coded/canonical-masked-M1/WORD.json --author-result workers/coded/canonical-masked-M1/RESULT.json --engine workers/audit/leaf-capacity-gate/check.py --price-engine workers/audit/review-cyclic-imports41/check.py --out workers/audit/semantic-inventory-correction
```

The first ancestry step is checked separately: removing the five new paid raw
return owners from early-paid46 recovers every early-release41 operation in
order. The added native returns are exactly 8, 9, 36, 37, and 50; their movement
increment is exactly `5[1]`. The subsequent mask insertions are reconstructed
at independently located source, meeting, retention, and restoration cuts.
They reproduce the entire reviewed operation list exactly.

## Live source and restoration audit

Let `r` be an old retained row and `c` its intended canonical replacement. Each
auxiliary carries `u = r + c`. Both the packet and its held original receive the
same `u` at their actual facet meeting. Every source donor in the construction
and restoration recipes is checked to be a live **raw original at Hub**, at the
precise read time in the new word. Merely belonging to a historical span is not
used. The restoration donor list excludes the held original itself.

| Packet | Meeting | Held original | Retention | Actual raw originals at source cut | Feasible nonzero canonical rows | Source ADDs | Restoration ADDs |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| P3 | F4 | X6 | ZFIRST3 at M1 | 108 | 63 | 45 | 45 |
| P4 | F74 | X75 | ZFIRST4 at M1 | 109 | 127 | 44 | 44 |
| P5 | F78 | X79 | ZFIRST5 at M1 | 110 | 255 | 45 | 45 |

The feasible counts are recomputed from all 511 nonzero canonical codewords
and both actual source cuts. The new rows and their full donor lists are in
`RESULT.json`; their supports on unfinished coordinates have sizes 32, 31,
and 34. The canonical code is recomputed directly from the pinned native roots
as `K_i = e_i + sum_{j: r_i dot r_j = 0} e_j`, and its rank is verified to be 9.

There are exactly **12 inherited ADDs with a changed source value**, four for
each packet. They are the packet-to-retention write, the retention-to-packet
reset, the retention-to-old-receiver read, and the held-original-to-that-receiver
read. Every other inherited ADD source is unchanged. The retained row acquires
`u`, the packet reset cancels `u`, and the two receiver reads cancel `u`.
All changed intermediate receiver values and the later restoration of X6, X75,
and X79 are tracked explicitly. The restored raw original is available before
the next auxiliary's Hub recipe needs it.

The audit verifies that all other old fields at the final live cut have exactly
their old values and charts. It separately verifies that IMPORT_E8, IMPORT_E9,
and IMPORT_E36 retain their exact raw values at M1. It does not infer any of
these source contracts merely from the final 46 endpoint equations.

## Replay, controls, and scope of the algebra

All 222 independent X/Y columns replay exactly. Every ADD has equal actual
charts, every public movement ascends, every owned movement descends, every
movement has positive rank difference, every owner is uniquely born at zero,
and every owner is explicitly cleared. All originals are restored at Hub and
all receivers finish at their own facets with the advertised increments.

There are 24 independent controls. For each mask, omitting its movement, either
coupling ADD, one construction ADD, one restoration ADD, or its CLEAR is
rejected. Two additional controls per mask deliberately keep the 46 endpoint
equations correct while destroying its canonical source contract: removing both
couplings and the matching restoration, and removing the same raw donor from
both the construction and restoration recipes. The latter still forms a valid
coupled mask, but its retained row lies outside the canonical code. These
controls separate source correctness from endpoint correctness.

The identities and ranks are binary. They extend to every characteristic-two
field and every whole-record width by applying the same maps componentwise.
No claim for arbitrary characteristic, nonlinear source transformations, or
unbilled access to historical rows is made.

## Complete invoice

| Count or statistic | Early-paid46 | Reviewed word | Change |
| --- | ---: | ---: | ---: |
| INIT | 127 | 130 | 3 |
| ADD | 819 | 1093 | 274 |
| MOVE | 481 | 484 | 3 |
| CLEAR, all dirty | 127 | 130 | 3 |
| Peak live owned fields | 127 | 130 | 3 |

The 274 ADDs are 134 raw construction reads, six coupling reads, and 134 raw
restoration reads. The entire movement profile is

```text
{1:188, 2:40, 3:60, 4:9, 5:72, 6:22, 7:93}
```

The exact difference is `3[1]`. Independent integer-root interval arithmetic
gives, at exponent 199/200,

```text
Q in [1615.1226434202980279690483298723712031661529,
      1615.1226434202980279690483298723712031661825]

limiting room in
     [6.62823679085432727719782049462378328172185,
      6.628236790854327277197820494623783281773033333333333333]
```

These bounds lie inside the independently computed author intervals. The
limiting room is not a finite-multiplicity supplier certificate; the ordinary
operation counts and all remaining delivery obligations still matter.

## Fresh delivery diagnostic

The old fixed-bank and fixed-history premises are not inherited. This review
recomputes the complete changed history. M1 is contained in exactly the native
facets `{3,4,74,76,78,80}`, all already completed. For every one of the 65
unfinished receivers, every actual visible historical X row still has zero
coefficient on that receiver's own coordinate. More strongly, its visible
history has rank zero after quotienting by its native raw locals and the 46
completed coordinates. The fresh all-history/raw-point-feedback closure is
therefore still exactly 46, with 65 explicit dual witnesses.

This freshly checked fact restricts extensions that freeze those histories and
only grant raw points. It does not prohibit new coded delivery from the changed
M1 bank, and it is not a lower bound of 65 packets or 65 movements.

As a separate diagnostic, granting the three actual canonical rows globally
without cost raises that generous feedback closure only to **47**, adding
point **34**. The global grant is not an actual delivery construction. The
chosen rows establish a real source mechanism; selecting rows and routes for
joint delivery remains a distinct optimization and proof obligation.

No new multiplication exponent or complete supplier is claimed.
