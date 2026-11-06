"""Run both separately authored lower-bound oracles; neither imports primary code."""
from pathlib import Path
import runpy
p=Path(__file__).resolve().parent
for name in ('independent_dp.py','independent_histograms.py'):
    runpy.run_path(str(p/name),run_name='__main__')
