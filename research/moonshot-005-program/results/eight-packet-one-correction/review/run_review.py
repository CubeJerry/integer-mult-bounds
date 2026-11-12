#!/usr/bin/env python3
"""Portable path adapter; the frozen independent checker is not edited."""
from pathlib import Path
import argparse,hashlib,importlib.util

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module

def main():
 here=Path(__file__).resolve().parent
 parser=argparse.ArgumentParser()
 parser.add_argument('--repo',type=Path,required=True)
 parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
 module=load(here/'check_composition.py','frozen_independent_review')
 module.REPO=args.repo.resolve();module.PACK=here.parent;module.OUT=args.output.resolve()
 channel=here.parent.parent/'foreign-history-channel/review/check_channel.py'
 if hashlib.sha256(channel.read_bytes()).hexdigest()!='8e625b20883a865ea2e8eb06994e94ad035416a30bbd70ad3e4bc3013ce9e2e3':
  raise ValueError('frozen independent channel checker changed')
 helper=load(channel,'frozen_channel_helpers')
 module.import_own_channel_checker=lambda:helper
 module.main()
if __name__=='__main__':main()
