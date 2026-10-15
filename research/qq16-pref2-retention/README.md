# Retain the first QQ16 cut in final selected outputs

**Conditional logical construction / research note; no new κ.** A paid
rotation immediately before F2 preserves the first bank's record that the
unchanged QQ16 schedule can lose. All four original selected input blocks of
pair 0 can then be reconstructed from final outputs, two initial ordinary
queries and f0. Neither a post-B1 checkpoint nor a separate f2 history is
needed. Other banks' recovery and a favorable native supplier bill remain open.

The result takes the explicit pre-F2 handoff in
[PR2346](https://github.com/CrocSwap/integer-mult-bounds/pull/2346) and supplies
the missing final-record premise of
[PR2174](https://github.com/CrocSwap/integer-mult-bounds/pull/2174)'s decoder.
It preserves those predecessors' scopes: the former excludes this intervention,
and the latter proves the decoder when its cut is recorded. The query captures
are still required and paid; this is not a selected-only repair without records.

## Exact result

At chart 2 let `H=P_(2,A) ell_(2,T)` and `J=H^-1=P_(2,T) ell_(2,A)`.
Immediately before F2, after the positive ordinary bridge, perform

```text
X_A += H X_T;   Y_A -= H X_T;
X_T -= J X_A;   Y_T += J X_A;
X_A += H X_T;   Y_A -= H X_T.
```

This takes arbitrary `(X_A,X_T,Y_A,Y_T)=(a,t,b,d)` to
`(H t,-J a,b+a-H t,d+t+J a)`. It preserves both selected pair sums.
F2 consequently stores `-a` in its A output. Under the retained ordinary-only
tail and the explicitly selected signed terminal `(X,Y)->(Y,-X)`,

```text
final Y_0,A = X_0,A immediately after B1,
Y_0,A immediately after B1 = final X_0,A - 2 final Y_0,A,
f2 = -ell_(2,T) final Y_0,T.
```

The complete decoder uses only `q0=B0 X_0,U^initial`,
`q2=B2 X_0,U^initial`, f0, the four final selected blocks of pair 0,
and its named final Y_0,U (the completed-X descendant).
The [ordered proof and complete cost boundary](PROOF.md) derive every formula.
They apply to arbitrary initial inputs in all four banks, including all
selected dirt; no query operator or cross-chart matrix is inverted.

The adapter is six complete mapped ADDs. A fully expanded dirty-echo
implementation uses **24 additive child calls**, with multiplicities
`8 ell_2T + 8 P_2A + 4 ell_2A + 4 P_2T`, and one borrowed eight-coordinate
query block, restored exactly. These are abstract complete-call counts,
**not native child ranks**. No clean scratch is assumed for that adapter.
Capturing the three retained query blocks, their storage, native frame/cover
conversions, final access, decoder workspace and release remain charged in
the conditional recurrence. No physical saving is inferred from removing a
logical observation.

## Reproduce

From the repository root, Python 3.12, standard library only:

```sh
python3 -I -B scripts/research_package.py --package research/qq16-pref2-retention
```

The registered command runs normal and optimized verification plus isolated
integrity checks. Expected mathematical marker:

```text
PASS_QQ16_PREF2_RETENTION pair=0 columns=240 adapter_children=24 controls=71 no_new_kappa
```

Expected final launcher marker:

```text
PASS_REGISTERED_RESEARCH_PACKAGE research/qq16-pref2-retention outcome=partial
```

`verify.py` is read-only by default. `--write-result NEW_PATH` is an explicit
authoring mode and refuses to overwrite an existing file. A Git-free source
export can run the direct verifier with `--repo /path/to/export`; registered
metadata validation additionally checks the pinned base provenance in Git.

The replay records its mathematical result in [RESULT.json](RESULT.json)
and checks:

- The exact source packet, archive and 19-event recipe binding; actual
  selected scalar Grams and the ordinary Gram `48 I`.
- Free ordered-operator retention and decoder identities, plus a separate
  symbolic ordinary-tail calculation with all bank inputs and call drivers.
- Three rational models, query dimensions 1, 2 and 3: all **240** initial
  basis columns across four dirty bank pairs. The larger models have
  noncommuting selected sections. The B map uses its E/exchange/H
  factorization; the decoder accepts only its explicit observation whitelist.
- The actual eight-coordinate scalar minors: all **40** data/scratch basis
  columns of the 24-child adapter, both inverse orders and agreement with
  the six mapped ADDs. The scalar check is not a native routed replay.
- A literal **35-event decoder** with all temporary admission and clears
  exposed: 10 mapped ADDs, 12 scalar-block ADDs and 13 CLEARs. Its 112
  scratch and 32 output coordinates per owner are **owned** storage;
  the previous values may be discarded, and that is explicitly charged.
  Across the finite models all 54 independent owned-dirt columns are checked.
- **71 rejecting controls:** all 24 adapter-child and 35 decoder-event
  omissions, six decoder/endpoint faults, four adapter faults and two
  schedule faults. A separate rational
  fixture confirms the predecessor's loss and its detection after the repair.
- Relocated optimized replay without Git, no-write acceptance, and rejection
  of a forged invoice receipt, a changed source, an unknown option and an
  attempt to overwrite the committed receipt.

The all-input theorem comes from the written proof. Finite model checks are
regressions, not a formal proof or an enumeration of the enormous owner cover.

## Sources, overlap and limits

Base main: `0fdd7d82de03e43c9e5a1000dfbcd380d1b687d2`, priority revision 4.
The selected conditional κ is unchanged at **0.001672660197076918**.
[SOURCES.json](SOURCES.json) pins every consumed main input by SHA256 and Git
blob. [TASK.json](TASK.json) records OS assignment seed **56**, the three
candidate tasks, exact pending predecessor heads/proof hashes, overlap coverage,
local coordination status and validation.

Direct pending predecessors, inspected but not imported or vendored:

| Work | Exact head | Retained contribution |
| --- | --- | --- |
| commdata2338, PR2174 | `f79470a7931f3943360c10d15b428e0e4e479c22` | Recorded-cut decoder and correct F2 bank/tail |
| alephnan, PR2346 | `653520d7f18f686ea3a274b4963981f5be563477` | Final-only obstruction and changed-pre-F2 handoff |

Nearby PR2216/2252/2328 concern a shear **before B1**, its frame mismatch
and prefix cost. PR2306/2350 address selected-only controls without the added
records; PR2326/2354 address coordinate taps. The dense old-chart/shear claim
in Discussion2205 also keeps a different pre-B1 intervention. This contribution
is a **post-B1, pre-F2 retention identity**, not another hidden-kernel census.
The submission refresh also inspected PR2197's private-field d_A relay,
PR2368/2381's pre-B1 shear/transcript obstructions, PR2384/2389's coordinate
read results and PR2376's observation-contract map. Those results do not
supply this post-B1 retention operation; their native and observation
restrictions remain in force. No global first-discovery claim is made.
Live coverage used targeted public HTML, relevant discussion bodies and Git
refs; the user specified unavailable API/posting access. Full live pagination
was not available, so the overlap check is explicitly incomplete. The scope
and result are recorded locally, with no claimed public reservation.

The native frame mismatch between X and Y is not waived. Availability and
cost of the adapter's P/ell children, physical query capture and retention,
owned decoder and borrowed adapter storage, legal final reads, precision, hosting, all-size
recursion and the intended complete ordinary-data map remain unproved.
The adapter changes f2 and hence may change ordinary endpoints. This is a
recovery lemma for the specified modified program, **not** a substitutable
full supplier. No full selected cold replay, actual routed adapter execution,
proof-assistant formalization, hosted CI or independent human review is claimed.

## Open next questions

1. Can these exact six mapped ADDs be implemented at the actual B1/F2
   native boundary? First emit their phase-correct reads, writes and cover
   sweeps, and price every child and borrowed-block lifetime. The missing
   typed native implementation is the blocker; scalar invertibility is
   insufficient.
2. Can the full intended controller outputs be recovered within a favorable
   bill? First track the changed f2 and all ordinary endpoints, then analyze
   the other three banks and the three retained record lifetimes. Pair-0
   selected recovery alone does not answer that question.

These questions and bounded first steps are also structured in TASK.json.

## Attribution

Prepared for **@CubeJerry** with substantial **OpenAI Codex assistance** in
derivation, implementation, verification and writing. New material is
Apache-2.0. Ali Romman supplies the retained QQ16 maps; commdata2338 supplies
the decoder; alephnan and Philippe Van Velzen supply the preceding final-only
obstruction/failure; Adam Gall, Ross Richardson, Cinna Davis and the adjacent
audit/tap contributors retain their respective credit. The standard four-child
dirty echo is predecessor machinery. The selected suppliers, owner/controller
and compiler lineage retain their unchanged notices. No priority is claimed
for those inherited identities or for generic reversible shears.
