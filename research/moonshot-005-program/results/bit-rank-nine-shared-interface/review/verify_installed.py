#!/usr/bin/env python3
"""Byte-preserving path adapter for the independently frozen reviewer."""
import argparse,subprocess,sys,tempfile
from pathlib import Path
def main(a):
    here=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='bit-nine-review-') as temporary:
        stage=Path(temporary)
        (stage/'programme').symlink_to(a.repo.resolve(),target_is_directory=True)
        (stage/'bit-nine').symlink_to(here.parent,target_is_directory=True)
        subprocess.run([sys.executable,'-I','-B',str(here/'check_bit_nine.py'),
                        '--repo',str(stage),'--output',str(a.output.resolve())],check=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
