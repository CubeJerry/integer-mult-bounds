#!/usr/bin/env python3
"""Relocate the frozen review's one historical receipt path without editing it."""
import argparse,hashlib,importlib.util,json,shutil,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
review=HERE/'review-c/check.py';manifest=json.loads((HERE/'review-c/MANIFEST.json').read_text())
if hashlib.sha256(review.read_bytes()).hexdigest()!=manifest['files']['check.py']:raise ValueError('frozen independent review changed')
receipt=HERE.parent/'involutive112-caller-budget/review-c/RESULT.json'
if hashlib.sha256(receipt.read_bytes()).hexdigest()!='1d99925bf409efc512849f2f8304b562b33e6b5659e769d1487b6447159cc004':raise ValueError('independent budget receipt changed')
spec=importlib.util.spec_from_file_location('frozen_physical_involution_review',review);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='physical-involution-review-')as tmp:
    base=Path(tmp);target=base/'worker-c/involutive112-budget-review/RESULT.json';target.parent.mkdir(parents=True);shutil.copyfile(receipt,target)
    module.BASE=base
    sys.argv=[str(review),'--author',str(HERE/'author'),'--output',str(args.output.resolve())]
    module.main()
