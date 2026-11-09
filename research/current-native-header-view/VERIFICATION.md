# Verification record

Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.

## Completed scientific and source checks

Environment: Python 3.12.14, standard library only. Every scientific replay
uses a fresh private bytecode-cache namespace, including direct standalone
commands, so existing bytecode cannot replace source-authenticated imports.
All new scientific guards remain active under `-O`.

The exact registered package command passed:

```sh
GIT_NO_LAZY_FETCH=1 python3 -B scripts/research_package.py --package research/current-native-header-view
```

It ran all four commands declared in VERIFY.json, in order:

| Command | Result |
|---|---|
| `python3 -I -B research/current-native-header-view/verify.py` | PASS, exact committed descriptor and phase receipts |
| `python3 -I -O -B research/current-native-header-view/verify.py` | PASS, same exact receipts |
| `python3 -I -B research/current-native-header-view/check_review.py` | PASS, independent frozen receipt reproduced |
| `python3 -I -O -B research/current-native-header-view/check_review.py` | PASS, same independent receipt |

The complete output is in checks/REGISTERED.log. Its outcome label was
`partial` while final packaging was in progress. The final TASK metadata was
then marked completed for the stated narrow scope; no executable or scientific
receipt changed. The metadata-only validation was repeated after that update.
This administrative outcome does not discharge a selected assumption.

Author scientific digests, over canonical JSON:

| Evidence | SHA256 |
|---|---|
| Complete descriptor receipt | `ea9ebb691083cc5b70b55da5d4b3304b724c4606b1fb0ff3d3ddb6a477cbc7db` |
| Actual phase-control receipt | `1da57067643e89f2b492474b1cfbd4dee56147f37435243522f3c62e7bf81743` |

RESULT.json is authoritative for those digests and all source pins. The two
independent receipt files are byte-identical, with SHA256
`f3f837aee296fef4b47f9a7432c4842ce4098f9142d881c14a046d8d31149723`.
The literal PREPARE/RELEASE graph hash is
`3e8bdb02323df791291cd7dd002483ebcdd8b02874b4ae53092bcb6860e08b1e`.

The reviewer independently interprets the emitted graphs on sparse local
hardware. It does not import the author's runner, tape model or fixture
encoders. Its mathematical/source review, three compiled mutants, malformed
binary controls and exact typed event/route controls are retained unchanged
in review/. The final review note SHA256 is
`62351225790c1abd365753eef512de2f7ce78f9723743885e5f989e5d702e0d7`.
This review is separate OpenAI-assisted work, not independent human or
proof-kernel acceptance.

The source authenticator checks all 109 retained files against both their
Git blob and SHA256 before import. Both scientific modes also snapshot the
new executable sources and dependency manifest before/after execution.
Canonical provenance metadata and pins passed the standard package validator.

## Scope and unexecuted obligations

Descriptor execution covers every declared field and raw bit, nonzero
ordinary remainders including r>=9, the actual nested caller event/owner,
same-port ordinary-source output consumption, translated origins, private
erasure, current cost and retained-history distinction. The all-size argument
and explicit instruction invoice are in PROOF.md; finite cases do not replace
that argument.

The phase fixture executes real encoded selected phase controls at f=2 through
the new produced view. It has `full_native_invocations=0`,
`complete_parent_packet_executed=false`, `fourier_child_executed=false`, and
`full_global_reservation_admission=false`. Its local H=f-1 geometry is not
presented as a complete root precision/reservation/provider admission. The
full numeric field is astronomical and is not constructed. No synthetic
numeric callback is treated as a native endpoint.

An exploratory phase-control run with the larger H=dG metadata was stopped
without a completed receipt because inherited numerical setup dominated its
cost. The registered bounded fixtures use the explicitly disclosed local
reservations above; no production algorithm or proof premise was weakened.
An initial wrong-residue fixture happened to have equal phases under both
residues; its columns were changed to the discriminating `(1,0)` pair, and the
entire final phase suite was rerun. No production table or native service was
changed in response to that fixture issue.

The source geometry, complete global parent validity, physical segment
disjointness, signed-grid/headroom and native endpoint/cost contracts remain
premises. No full selected caller, atomic MOVE triple, generalized product
occurrence or Fourier-child execution is claimed. All five assumptions remain.

## Publication integrity boundary

Only the scoped package is committed. All predecessor computational bytes
remain unchanged. FILE-MANIFEST.json records every regular package file except
itself; DEPENDENCIES.json separately records immutable source Git blobs and
public commits. The standard committed-byte/mode preflight is used after
commit; it checks publication bytes, not the mathematical theorem.

The optional `--check-source-history` gate is not claimed. This workspace uses
the shared shallow canonical Git object store. No unshallow, clone or network
shell fetch was attempted. Runtime dependencies are self-contained retained
bytes, independently hash checked before import; their public source pins
are explicit rather than relying on an unrelated local branch being reachable.
