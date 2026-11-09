"""Replay the unchanged BIT source in a disposable copy and compare receipts.
@CubeJerry, substantial OpenAI assistance, Apache-2.0.
"""
from pathlib import Path
import gzip, json, shutil, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    source=HERE/'retained'
    before=json.loads((source/'bit/FRAGMENT-BIT-ADMISSION.json').read_text())
    caller=gzip.decompress((source/'bit/FRAGMENT-CALLER.json.gz').read_bytes())
    with tempfile.TemporaryDirectory(prefix='integer-mult-bit-source-') as temporary:
        dst=Path(temporary)
        shutil.copytree(source/'bit',dst/'bit')
        shutil.copytree(source/'two-fragment',dst/'two-fragment')
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+['-B',str(dst/'bit/verify_fragment.py')]
        run=subprocess.run(command,capture_output=True,text=True)
        need(run.returncode==0,'retained source failed: '+run.stdout+run.stderr)
        after=json.loads((dst/'bit/FRAGMENT-BIT-ADMISSION.json').read_text())
        need(gzip.decompress((dst/'bit/FRAGMENT-CALLER.json.gz').read_bytes())==caller,
             'literal decompressed caller differs')
        need(set(before)==set(after),'source receipt schema differs')
        omitted={'seconds','caller_sha256'}
        need({k:v for k,v in before.items() if k not in omitted}==
             {k:v for k,v in after.items() if k not in omitted},
             'source mathematical receipt differs')
    print('PASS_FROZEN_BIT_SOURCE_REPLAY')

if __name__=='__main__':main()
