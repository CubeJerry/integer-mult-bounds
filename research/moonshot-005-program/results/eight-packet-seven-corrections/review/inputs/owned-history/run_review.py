#!/usr/bin/env python3
from pathlib import Path
import argparse,importlib.util
here=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
s=importlib.util.spec_from_file_location('original_history_review',here/'check_owned_history.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.SOURCE=a.repo/'research/shared-wire-split-composition/data/final.json.gz';m.AUTHOR=here/'AUTHOR-EXTRACT.json';m.OUT=a.output;m.main()
