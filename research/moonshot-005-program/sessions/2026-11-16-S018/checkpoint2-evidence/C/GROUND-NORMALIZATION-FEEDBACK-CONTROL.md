# Positive physical control with Y-to-X feedback

This supplements `GROUND-OUTPUT-NORMALIZATION.md` without changing its
original proof or control word. The general theorem permits temporary
arbitrary-y content in X or owned records when the final X-from-Y block is
zero and the final Y-from-Y block is invertible. The first physical control
uses only Y-to-Y forwarding; this second control exercises that wider case.

At actual native line L0, immediately after X0 adds into Y2, insert

    ADD Y2 X0
    ADD X0 Y3
    ADD Y2 X0

All three fields are physically cocharted. Y2 is unchanged during these
three operations. X0 therefore returns to its raw value before departing,
while Y3 receives the real mixed X0/y value from the middle operation.
This is not merely an adjacent canceling pair: its middle read changes the
later Y transfer.

In the unnormalized reference continuation X0 temporarily equals y2. In
the actually normalized word it temporarily equals

    x0+x2+x3+y2+y3,

then returns to x0. Both statements are checked on the full independent
column trace. The original Y transfer on roles2,3,4 becomes

    (y2,y3,y4) -> (y2+y3, y3, y3+y4).

The actual known-column errors are still ground supplied. The new ground
inverse uses two ADDs, instead of five in the first control. With the three
new feedback operations the complete ledger is therefore unchanged:
46 INIT,106 ADD,274 MOVE,46 dirty CLEAR; profile52[1]+2[5]+2[6]+218[7].
All111 X endpoints and all111 arbitrary Y columns pass. Deleting either of
the two Y2-to-X0 feedback operations leaves an incorrect original-X
endpoint and is rejected before normalization is allowed.

The independently pinned native source and target set are unchanged. The
new word SHA256 is
`0c04328feaa1ba5c561294a301059be0e7402f8f932a8645cda09d0b20d839f9`.
Files are `ground_output_feedback_control.py` and
`normalization-feedback-control/{WORD,UNNORMALIZED-WORD,RESULT}.json`.
This is an author-created positive interface control, not an independent
review of the theorem. It adds no completed output or supplier claim. All
five foundations and all remaining source/completion obligations remain.
