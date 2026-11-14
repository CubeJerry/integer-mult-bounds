# Scope clarification for varying chain length

This note supplements, without altering, frozen PROOF.md SHA2568878de72284ec4a02d928480f38e68a66e7768306885d2b86b557e11d6490937.

The exact rank formula8m−r+2p and exact alternating operator identities hold for every finite choice of distinct stages. The asymptotic support exclusion for a nonalternating odd chain in Section2 must also retain its path-count factor4^r. With L_V additional binary scalar-ADD branching factors, its row support is at most

2^(2r+L_V+(8m−1)V).

Consequently a full rank8m+1 target is excluded whenever2r+L_V<2V. In particular this holds for fixed r and L_V=o(V), or more generally r=o(V) and L_V=o(V). The proof does not exclude growing chains when2r+L_V reaches2V merely from the per-path rank deficit.

The current two-bank favorable caller budget independently forcesm<=8, hence r<=8, so its application has fixed r and meets the stated condition for sublinear ordinary branching. That separate budget is not needed for the exact rank or operator identities. Credit Worker C's independent review for requesting the explicit varying-length scope.
