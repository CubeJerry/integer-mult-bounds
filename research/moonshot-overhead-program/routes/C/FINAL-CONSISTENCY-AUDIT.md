# Final consistency observations for the lead

Route C, S002, 2026-11-25. Read the current top-level `STATE.json` and
`TARGET-OVERHEAD.md` after the fixed-field gate. No mathematical mismatch
was found in the current Q envelope, definitions L and s, O(n) visited-cell
claim, explicit null benchmark kappa, or the recorded verification limits.
The chronological older target sections are clearly identified as earlier
checkpoints and the final section states the stronger current result.

Two small state-schema clarity fixes are suggested before final publication:

1. The legacy key `best_unconditional` still contains only the published
   qualitative OpenAI baseline. The current explicit theorem is correctly
   recorded in `new_complete_overhead_bound` and `s002_current_result`.
   Label the legacy string as a published baseline, or give the legacy
   key an explicit pointer to the current theorem, to prevent a consumer
   reading only that key from missing the new envelope.
2. The historical entry in `independent_complete_overhead_bounds` says
   its x and y are as in the primary bound. The primary bound now uses s
   and has no y. Make that historical entry self-contained with
   `x=s=log2 L(n), y=log2 log2(x+16)`. Likewise the top-level conditional
   preflight formula using x can state explicitly `x=s=log2 L(n)`.

These are presentation/data-schema observations, not blockers in the
mathematical theorem. The lead owns the top-level files; this route made
no edits to them.

Within C, the formerly conditional IP4 review has a dated update showing
that its premise is now supplied. The early divided-power working notes
have a dated update pointing to the new full-rate compilers and preserving
the separate polynomial-width open question. The route report identifies
the current theorem, finite evidence and remaining gaps without promoting
the optional prime-characteristic backup composition.

The new four-bit witness checks the carry/formula compiler interfaces
together: four affine 8-by-8 factors, every cyclic product formally equal
to f I_8, all Boolean count values, and a non-Boolean F4 point showing why
the formal multilinear barrier does not apply. It is finite evidence for
the algebraic interface, not a full multiplier execution.
