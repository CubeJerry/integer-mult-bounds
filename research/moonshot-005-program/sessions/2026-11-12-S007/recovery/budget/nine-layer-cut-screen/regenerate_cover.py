# Reconstructed recovery helper, not a pre-outage hashed artifact.
# Run dual-facet-cuts/screen.py and full_screen.py first, then this script.
import json,math
from pathlib import Path
H=Path(__file__).resolve().parent
v=json.loads((H.parent/'dual-facet-cuts/FULL-SCREEN.json').read_text())
out={'source_sha256':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','denominator':1000000,'edges':[{'from_frame':e['from_frame'],'to_frame':e['to_frame'],'rank':e['rank'],'coefficient_numerator':math.ceil(e['cover_multiplicity']*1000000)} for e in v['dual_edge_cover']]}
(H/'COVER.json').write_text(json.dumps(out,indent=2)+'\n')
# The regenerated cover must be checked with check.py; its frozen hash may differ
# if the numerical LP chooses another optimal basis.
