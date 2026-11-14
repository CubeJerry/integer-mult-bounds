# Matched D5 cubic reservoir gate

For the exact common rank-three chart I, A3-normal D5 banks with disjoint native source cohorts outside I correspond to matchings in K6. There are15 banks and15 maximal triples.

Even granting all five cubic modes at every chosen bank and arbitrary shared-I coordinates e23,e61, every fitting over every characteristic-two field and every block width has chi>=197. This misses the retained coarse target chi<=194. The theorem does not cover arbitrary raw cohort modes or overlapping bank acquisitions.

Read PROOF.md for the precise code/geometry scope. CERTIFICATE.json records all1,665 forced-support checks. Reproduce with:
```sh
node reproduce.cjs
```
Expected PASS,15 banks,15 triples,code dimension26,chi lower bound197. Controls for overlapping banks and arbitrary raw modes deliberately escape this bound; they do not establish feasible sources.

The author ran these pure-JavaScript functions in the cloud environment. The provided Node wrapper was not run in the unavailable local environment. Source recovery and exact prior pins are retained in SOURCES.json. No new kappa.
