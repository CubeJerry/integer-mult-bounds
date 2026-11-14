# Exact saving thresholds for the fixed two-patch quotient

This package retires the proposed `V=2,d=3` compression of the two native
scalar patches introduced as the invariant-filtration boundary control.
It proves an all-characteristic-two-field, all-width classification of
arbitrary subspaces inside their tensor quotient, including noncommuting
and singular operator encodings.

For a permitted quotient subspace `E`, the minimum whole-block arrival
proxy is 222 if it contains none of the three named full scalar-line
tensors; 205 if it contains only the first or second; 216 if it contains
only their sum; and 192 if it contains their entire two-width span. Thus
every proper subspace fails the retained `ell<=194` target requirement.

The key native structure is exact receiver availability: 77 receivers
have no available direction, fourteen each have only the first/second,
and six have both. At those six, cancelling enough whole blocks forces
one of three full identity patterns; arbitrary partial operator mixing
does not achieve another saving pattern.

The checker also exhausts all fifteen F2 hyperplanes of the width-two
four-dimensional tensor quotient. It explicitly enumerates every pair
of diagonal-normalized local rows. Its exact minima are 205 in six cases,
216 in three, and 222 in six. Full-space and one-patch controls attain
192 and 205. Result JSON contains every chosen row, local affine nullity,
enumeration size, native availability record and an explicit full-space
scalar fitting.

```bash
python3 -I -B research/moonshot-005-program/results/bit-two-patch-proper-quotient/author/check.py \
  --native research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz \
  --output /tmp/two-patch-proper-quotient
```

Expected status: `PASS_TWO_PATCH_PROPER_QUOTIENT_NATIVE_AND_EXACT_HYPERPLANES`.
Normal and optimized Python results match byte-for-byte. The universal proof
is separate from the finite enumeration. Independent review is pending.
No physical decoder, strict supplier, foundational discharge or new kappa.

Next work must change the receiver-availability geometry or the patch
region structure; further coefficient searches inside this family are
excluded by the theorem. Credit @CubeJerry, the named source/predecessor
results and substantial OpenAI assistance. Apache-2.0.
