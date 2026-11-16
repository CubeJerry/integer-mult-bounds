# Independent review of root's aligned-component primitive words

**PASS, exact symbolic replay.** Reviewed `R/pure-prefix-review/check.py` and `ORDINARY-WORDS.json`; the separate B checker `check_aligned_selective_component-v1.py` rebuilds the literal source in SymPy and reconstructs every monomial table independently. It does not import root's matrix engine or its assertions.

The shear is valid over the abstract collective involution algebra: scaling x by epsilon/2, adding, applying F, adding, applying F again, and scaling by2epsilon restores x and adds epsilon(I+F)x/2 to y. Three such shears followed by diag(I,-F) yield the controlled swap. The F²=I relation holds for every tensor width. The -1 and dyadic scalars are external, avoiding odd/even phase errors.

All eight words equal their intended exact operators, both inverse directions compose to identity, and every one of48 omitted ADD variants fails. The counts are6 ADD,7 SCALE, and respectively8/9/8/7 MONO for C/Q/output/input, in either direction. The bank row-sum prefix bound is5. No free tensor decoder, auxiliary field, source volume, or supplier has been granted.

The positive component identity is also independently reconstructed: literal K is two controlled flips with phase(-1)^ad, B2 has the supplied rank2 gauges, K commutes with Fhat, B2 and A⁴ intertwine Fback to Fhat, and the collective routes send the entire quartic contribution to the single full-rank block -a⁴. The multiplication identities tensor exactly, followed by collective projector algebra. The pure-prefix theorem, rather than a finite search, excludes independent421 completion of those fixed entries.

Exact input pins and replay receipts are in `ALIGNED-SELECTIVE-COMPONENT-RESULT-v1.json`; the mathematical component proof is `ALIGNED-SELECTIVE-COMPONENT-v1.md`.
