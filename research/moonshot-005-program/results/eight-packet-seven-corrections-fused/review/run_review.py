#!/usr/bin/env python3
"""Portable paths for unchanged, pinned independent verification code."""
from pathlib import Path
import argparse,hashlib,importlib.util
class Paths:
 def __init__(self,mapping):self.mapping=mapping
 def __truediv__(self,key):
  if key not in self.mapping:raise ValueError('Undeclared staging path '+key)
  return self.mapping[key]
def load(path,name,pin=None):
 if pin and hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('Helper pin '+str(path))
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main():
 here=Path(__file__).resolve().parent;results=here.parent.parent
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 m=load(here/'check_fused.py','frozen_review');m.REPO=a.repo.resolve();m.PACK=here.parent;m.OUT=a.output.resolve()
 m.PARENT=results/'eight-packet-seven-corrections'
 m.BASE=Paths({'worker-review/route-fusion/check_fusion.py':results/'observation-preserving-route-fusion/review/check_fusion.py','worker-review/eight-packet-seven-corrections/REVIEW-RESULT.json':results/'eight-packet-seven-corrections/review/REVIEW-RESULT.json'})
 m.main()
if __name__=='__main__':main()
