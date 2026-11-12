#!/usr/bin/env python3
"""Resolve paths for the unchanged exact dual checker."""
from pathlib import Path
import argparse,importlib.util
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
f=Path(__file__).resolve().parent/'check_dual.py';s=importlib.util.spec_from_file_location('chart318_dual',f);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.SOURCE=a.repo/'research/shared-wire-split-composition/data/final.json.gz';m.HISTORY=a.repo/'research/moonshot-005-program/results/joint-additive-history-obstruction/CERTIFICATE.json';m.OUT=a.output;m.main()
