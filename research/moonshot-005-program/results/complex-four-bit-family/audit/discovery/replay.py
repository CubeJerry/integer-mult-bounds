#!/usr/bin/env python3
"""Relocate the frozen exploratory runner without changing its algebra or options."""
from pathlib import Path
import argparse, sys

ap = argparse.ArgumentParser(add_help=False)
ap.add_argument('--repo', type=Path, required=True)
args, rest = ap.parse_known_args()
base = Path(__file__).parent
helper = (base/'nonclifford_sector_search.py').read_text().split("if __name__=='__main__':")[0]
old = "repo=Path('/workspace/scratch/6e036830f982/programme')"
assert helper.count(old) == 1
helper = helper.replace(old, 'repo=Path(' + repr(str(args.repo.resolve())) + ')')
script = (base/'four_bit_caller_search.py').read_text()
loader = "exec(Path(__file__).with_name('nonclifford_sector_search.py').read_text().split(\"if __name__=='__main__':\")[0])"
assert script.count(loader) == 1
script = script.replace(loader, '')
namespace = {'__name__':'__main__', '__file__':str(base/'four_bit_caller_search.py')}
sys.argv = [str(base/'four_bit_caller_search.py')] + rest
exec(compile(helper, str(base/'nonclifford_sector_search.py'), 'exec'), namespace)
exec(compile(script, str(base/'four_bit_caller_search.py'), 'exec'), namespace)
