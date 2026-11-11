# Sound retirement and the eager delivery rule's paid stopping point

This extends the changed-main prefix construction by a **conditional retirement
interface**. It retains the programme's `owned_erasure` premise: a retired
field may be dirty. No zero-CLEAR implementation or new physical tariff is
asserted. The simple 25,728-event prefix in PROOF.md has no CLEAR and does not
use this extension.

## Exact retirement criterion

At a source checkpoint, for every chart f let V_f be the span of the current
homogeneous difference rows of **all live virtual roles** at f: original mains,
helpers and active source-owned roles. Let O_f be the span of the currently
available physical difference observations at f. The encoded-state invariant
is V_f ⊆ O_f, together with the separately preserved first-copy source state.

A proposed owned observation t at f may be retired whenever

\[
V_f\subseteq\operatorname{span}\{o_j:\ j\ne t,\ \text{current chart}(j)=f\}.
\]

Necessity is not claimed: a different representation or future-demand contract
could allow more retirement. Sufficiency follows directly from the invariant.
All current virtual differences remain cochart-decodable, so every future
same-chart scalar event is a linear combination of available rows. Every
future MOVE is still treated by the charged delivery/main-rebase rules. The
proof does not rely on the retired row being zero or on its original decoder
coefficients continuing to work; decoders are recomputed from the retained span.

Checking only main rows is unsound. For example, if all current main differences
are zero but one live helper difference is q, a single observation q is still
necessary to represent that helper. Deleting it because the main-only span is
zero destroys the interface. All source-owned roles must also be included.

The current implementation performs exact rational span checks after each
MOVE. It reuses an owned label only after the prior actual CLEAR, then INITs
it at the next declared chart. The total peak is the sum of live new observations
and live original source-owned fields, including new snapshot temporaries.
It is not just a count of persistent cache entries.

## Constructed extension and stopping decision

The exact replay with this rule reaches **cut 26226**, immediately before

```
MOVE 296, chart 332 -> chart 341, rank 1.
```

It emits 120 new owned lifetimes, 33 dirty CLEARs and has 87 fields live at the
cut, with peak 87. No original source-owned field has yet been initialized.
This exceeds the old 43-live geometry; that limitation is reported rather
than silently borrowing the old compiler. The additional paid profile already
spent is

\[
P_1+86,\qquad P_2+6,
\]

with exact moment interval

\[
\frac{9795848315393441}{10^{14}}
\le 86+6\,2^{199/200}
\le \frac{6122405197120901}{62500000000000}.
\]

Both endpoints come from integer 200th-root comparisons with denominator
10^15, not floating approximation. The interval is approximately
97.9584831539344. The next required rank-one delivery **under this particular
rule and already chosen history** would make the spent moment exceed
98.9584831539344, which is larger than the unchanged H4 allowance's upper bound
221397923137950577/2250000000000000 ≈ 98.3990769502003.

Consequently, continuing this eager delivery rule cannot finish under the
unchanged H4 target/paid invoice. Expansion stopped before that payment. This
is an exact failure of a specified constructed rule, **not** a lower bound on
all codes, all schedules or all H4 realizations. Retiming deliveries, borrowing
existing transports, changing which main differences ride a paid main MOVE,
changing the virtual observation contract, or changing the complete invoice
remain legitimate directions.

The emitted extension's 27,312 operations are 25,444 ADDs, 1,406 SCALEs,
309 MOVEs, 120 INITs and 33 CLEARs. Of the 120 MOVEs added to its original source
prefix, 28 are already-funded second-main MOVEs and 92 are new deliveries.
All positive scalar/lifecycle work remains to receive a new physical tariff.
No complete κ or compiler admission follows from this prefix.

## Why preserve this diagnostic

The first small prefix is a reusable positive witness for changing intermediate
main information and safely delivering missing differences. This extension
shows exactly why automatic continuation of that witness is inadequate: owned
capacity and accumulated transport both grow. It gives future sessions a
specific stopping event and a literal current state. The next work should
remove actual charged routes or change their cost structure, rather than
merely add more parked observations.
