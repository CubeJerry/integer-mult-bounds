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
 m=load(here/'check_seven.py','frozen_review');m.REPO=a.repo.resolve();m.PACK=here.parent;m.OUT=a.output.resolve()
 m.BUDGET=here/'inputs/controllers'
 m.BASE=Paths({'worker-review/owned-history/CERTIFICATE.json.gz':here/'inputs/owned-history/CERTIFICATE.json.gz'})
 one=load(results/'eight-packet-one-correction/review/check_composition.py','frozen_one_helpers','a089410089d0c57549379cc51c3dd09829b3cc9f0ee209d3e0ab2d53462aa473');one.REPO=a.repo.resolve()
 channel=load(results/'foreign-history-channel/review/check_channel.py','frozen_channel_helpers','8e625b20883a865ea2e8eb06994e94ad035416a30bbd70ad3e4bc3013ce9e2e3')
 m.own_helpers=lambda:(one,channel)
 m.main()
if __name__=='__main__':main()
