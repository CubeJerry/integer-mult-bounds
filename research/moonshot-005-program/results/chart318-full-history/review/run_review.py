#!/usr/bin/env python3
"""Path-only adapter for the unchanged independent reviewer."""
from pathlib import Path
import argparse,importlib.util
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('frozen_review',here/'check_full_history.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
m.REPO=a.repo.resolve();m.PACK=here.parent;m.OUT=a.output.resolve();m.main()
