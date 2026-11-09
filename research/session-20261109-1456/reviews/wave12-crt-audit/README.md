# Wave 12 read-only CRT/carry interface audit

**Disposition: resolved at the canonical written-construction level;
the unchanged older physical Converter is a superseded port. No new
research PR is proposed.** This checkpoint prevents claiming a new CRT
identity or silently using the wrong existing layout implementation.

Canonical base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.
Current normalized recovery:
`CubeJerry/integer-mult-bounds@1ab10aa78c4b27345c76806d1d32c7b9de481219`.
The wave11 extractor is frozen separately and was not modified here.
All consulted source bytes and exact paths are in SOURCES.json.

## What the source already establishes

Canonical `unconditional-batched-crt/PROOF.md`, “Address isomorphism,”
defines `P_i=product_{j<i}s_j` and sends ordinary coefficient k to
`y_i=k*P_i^-1 mod s_i`. It explicitly fixes axis zero as fastest and
charges three balanced CRT conversions, including the inverse conversion
of the final recovered integer coefficient field. “Recovering the exact
product” applies that inverse before carrying. Therefore compact tensor
coefficient order is not asserted to be ordinary coefficient order.

The new normalized recovery endpoint copies records in its input order
while restoring `S^2*2^(2b+4+3Gamma)` and rounding. Its integer record
width is `W=q+3Gamma+4b+6`, and its record count is exactly S. With the
wave11 extraction contract, these records are in axis-zero-fastest y
order. CRT treats the complete W-bit signed record as opaque: no further
Gaussian restoration or S factor belongs to address conversion.

Canonical `CRT.md` section1 deliberately accommodates physical axis zero
innermost, retaining arbitrary-source controls and avoiding the older
full axis reversal. Its inverse takes the current y coordinates back to
the mixed-radix digits of ordinary k. Section5 explicitly includes plain
dyadic padding and cropping. This is the desired written source join;
it is already present, not a new lemma.

The required padding is the ordinary valid box `j_i<s_i`, not a second
Gaussian `Q_i(j)` insertion. Existing `crt_padding.padded(...,
natural=False)` uses `Shape.bounds` in source-axis order and reads the
packed Address least significant field first; it supplies exactly this
colex padding/cropping operation under its own native source contract.
No full physical balanced CRT caller is executed or inferred here.

## Why the older whole Converter cannot be substituted unchanged

`crt-address-streams/PROOF.md` defines its *natural tensor order* with
the **final** axis contiguous. `Converter.run(...,inverse=True)` calls
`padded(...,natural=True)`, so `reversed_bounds` puts that final axis into
the least significant target field. Its forward/inverse routes explicitly
pay a global reversal of axis fields. This is a different convention from
the current axis-zero-fastest compact field.

For moduli `(3,5)`, current compact ordinal1 is coordinate `(1,0)` and
belongs to ordinary coefficient k=10. The unchanged old inverse instead
interprets ordinal1 as `(0,1)` and sends it to k=3. The mismatch is a
binding failure for this precise attempted substitution, not a defect
in the old Converter's documented interface. Reversing metadata changes
the prefix products as well; it is not permission to silently relabel
one endpoint of an already-fixed caller.

This incompatibility is already anticipated by canonical CRT's explicit
choice to avoid the older reversal. It does not justify a duplicate
publication. The old `run_plan` additionally inherits the old TensorPlan
admission dealt with in public wave7; using standalone `run` avoids that
type gate but does not remove the order or cost differences.

## Optimistic complete-cost stopping test

Let `V=T*W`, with `W=Theta(p0)`, and D source axes. The new extraction,
codec, exact recovery and eventual carry/trim scans do not remove the
CRT conversion. Even assigning an optimistic zero cost to any needed
layout repair, the **literal** old inverse has at least `2*D*T*W` payload
writes in its shears alone:

- `Converter.triangular` invokes `shifted` once for every axis, including
  the axis whose offset is zero; there is no identity-stage elision.
- `shifted` always executes the bucket and merge passes.
- For every prefix, `first+second+invalid = s_i+(t_i-s_i)=t_i`.
- `copy_rows/copy_record` write every bit, so each pass writes T*W bits.

Thus this unchanged implementation costs Omega(DV), before its paid
router, offsets, padding, copies, cleanup, source setup and history.
For the fine family `D=Theta(p0^(1-10^-30))`, it cannot fit a target
`O(V*p0^(1-kappa))` with any fixed `kappa>10^-30`, even allowing fixed
polylogarithms. Canonical CRT.md already explains why the O(VD) route
is insufficient and replaces it with a balanced-switch construction.
This audit confirms that distinction at the literal writes; it is not
a new lower bound for other implementations or an improved multiplier.

The intended balanced route's stated invoice remains
`O(V*p0^(1-a2)*ell^2*polylog(p0))`, with all its native/compiled-control,
source/ownership and uniform cost obligations. This checkpoint does not
replace those obligations with a generic fast permutation oracle.

## Carry width and output length

Canonical recovery bounds true coefficients by `<2^(3b)`. The public W
is more than sufficient; inverse CRT must preserve all W bits and order.
`Sandwich.carries` then reads signed W-bit records, requires nonnegative
values, propagates radix-`2^b` carry, checks excess high digits, and
returns **exactly `2*Ndigits*b` bits**, as its own PROOF states. The
canonical n-bit multiplication output has 2n bits. For
`Ndigits=ceil(n/b)`, a final exact trim of `2*(Ndigits*b-n)` leading zeros
(less than 2b bits), with its read/validation/copy cost paid, gives that
extent. This is a routine wrapper consequence of padded radix input,
not a new carry theorem or a defect in the old wrapper's stated domain.

No old production Catalogue guard is waived, and no two-S or Gamma
restoration is repeated at this stage. The old typed whole Sandwich
remains subject to the previously established fine-family obstruction.

## Reproduce and remaining obligation

```sh
python -B /workspace/scratch/a365d332d434/wave12-crt-audit/audit.py
python -O -B /workspace/scratch/a365d332d434/wave12-crt-audit/audit.py
```

Expected: `PASS_READ_ONLY_CRT_INTERFACE_AUDIT`. The independent direct
CRT oracle checks the layout discriminator, canonical logical inverse
on 1,205 valid coordinates, exact shear write counts, and a 9-bit input
carry/extent case. This is source algebra and bounded logical checking;
there is **no native CRT payload, production transform, scalar service,
or carry execution** in this checkpoint.

The useful remaining task is the actual fast balanced CRT payload caller
and its complete source/primitive/ownership admissions, with current
coefficient fields at the correct source and target epochs. The canonical
`encoded-current-crt` package already implements current-child numerical
offset reconstruction and expressly leaves the physical whole-payload
route external. Its source distinction must be preserved. No additional
abstract CRT identity, projection lemma, naive sort or old triangular
port is recommended.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit the
canonical #4100 balanced construction, Tekalign's #4024 physical CRT
address streams, #5095 tensor/recovery sandwich, encoded-current-CRT
authors and retained native source contributors. This is an audited
restart checkpoint, not a submitted or registered contribution, and
claims no new kappa or discharge of a foundational assumption.
