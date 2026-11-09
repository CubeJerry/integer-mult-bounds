"""Portable complete BIT audit entry point; standard library only.
@CubeJerry, substantial OpenAI assistance, Apache-2.0.
"""
from pathlib import Path
import subprocess,sys
HERE=Path(__file__).resolve().parent

def main():
    for script in ['check.py','audit_caps.py','tail_review.py','replay_source.py']:
        command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+['-B',str(HERE/script)]
        run=subprocess.run(command,capture_output=True,text=True)
        if run.returncode:
            raise ValueError(script+' failed\n'+run.stdout+'\n'+run.stderr)
        print(run.stdout.strip().splitlines()[-1])
    print('PASS_BIT_ACTUAL_AMBIENT_AND_WRAPPER_AUDIT')

if __name__=='__main__':main()
