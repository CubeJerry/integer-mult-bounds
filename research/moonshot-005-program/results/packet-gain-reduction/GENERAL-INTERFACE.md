# General decoder criterion when foreign controls create history relations

This supplement prevents overextending the one-receiver220-station theorem to a multi-donor code using other charts. It is a linear-algebra interface reduction, not an additional source construction.

Let a receiver's actual recorded histories be `y=Ou+Rq`, with all original common inputs u arbitrary and independent of q. Grant packet/private records `Cq,Sq`. Let N have rows spanning the full left nullspace of O, and suppose h is a baseline target row with `D0 O=h`. Then a linear decoder for `h u+e q` exists exactly when

`e-D0 R in row(C,S,N R)`.

Indeed all possible baseline-compatible history coefficients are `D=D0+tN`; their gains are `D0R+tNR`. Packet/private coefficients give precisely the displayed row span. This equivalence handles all finite dimensions, and tensor/block versions follow with the corresponding linear maps. It does not price any records.

If an actual stable endpoint-minus-initial representation gives `D0R in row(C)`, the criterion simplifies to

`e in row(C,S,N R)`.

For precompensation `R=OVC+B`, one has `NR=NB` because NO=0. Thus the only additional q information supplied by zero-baseline native history combinations is exactly the row space of NB. The admitted220-station theorem sets NB=0 when all controls are supported at those stations.

For a multi-donor code, the source theorem for the q77 column alone is insufficient to set the entire NB matrix to zero. Other donors may be physically available outside the220 set and create nonzero columns of NB. Those columns can combine with packets to reveal q77. A kernel vector of C usually has several nonzero donor coordinates, so an indistinguishability proof cannot simply fix all foreign q coordinates to zero while retaining Cq=0. The enlarged source design problem is to compute the actual timed NB and stable decoder gain, jointly with endpoint response and physical access, and then verify this exact decoder criterion. A desired low-rank final error matrix alone does not establish it.

If controls are inserted at receiver charts, the claimed endpoint representation itself must be reauthenticated against the actual recorded histories; local additions can otherwise introduce unrecorded information. New carrier observations similarly change O,R,N and must be included explicitly. No source sufficiency, E8 impossibility, or new kappa is claimed here.
