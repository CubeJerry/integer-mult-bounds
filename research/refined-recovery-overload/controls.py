"""Actual private-copy semantic corruptions, normal and optimized; Apache-2.0."""
from pathlib import Path
import json,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
MUTANTS=[
 ('source-byte',None,None,'source SHA256'),
 ('odd-coset','return A if v==0 else (D if v&1 else B)','return A if v==0 else B','map domination'),
 ('even-rank','other=[i for i in range(4) if i!=pivot]','other=[i for i in range(4) if i!=pivot][:2]','rank-three kernel'),
 ('kernel-collision','list(range(4,16));maps=[]','[1]*12;maps=[]','no one-coordinate relation'),
 ('skip-Y3','for y in range(4):','for y in range(3):','complete small-Y domain'),
 ('AM-exponent','D**32*B**350','D**32*B**349','AM-GM'),
 ('largest-marginal','k=min(range(15),key=','k=max(range(15),key=','balanced kernels'),
 ('undersized-tag','zero<=upper<2**696','zero<=upper<2**695','696-bit bracket'),
]
def main():
 count=0
 with tempfile.TemporaryDirectory(prefix='recovery-controls-') as td:
  root=Path(td);q=root/'research/refined-recovery-overload';q.mkdir(parents=True)
  for name in ['core.py','verify.py','SOURCES.json']:shutil.copyfile(P/name,q/name)
  for rel in ['research/precision-state-frontier/FIXTURE.json','research/refined-native-recovery/CHAIN_PROOF.md']:
   dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
  original=(P/'core.py').read_text();fixture=root/'research/precision-state-frontier/FIXTURE.json';raw=fixture.read_bytes()
  for label,old,new,expected in MUTANTS:
   if old is not None and original.count(old)!=1:raise ValueError('ambiguous mutation '+label)
   (q/'core.py').write_text(original if old is None else original.replace(old,new))
   fixture.write_bytes(raw+b' ' if old is None else raw)
   proc=subprocess.run([sys.executable,'-I','-B',*(['-O'] if sys.flags.optimize else []),str(q/'verify.py')],capture_output=True,text=True,timeout=30)
   if proc.returncode==0 or expected not in proc.stderr:raise ValueError(label+' wrong failure: '+proc.stdout+proc.stderr)
   count+=1
 print('PASS_RECOVERY_OVERLOAD_MUTATIONS',count,'optimized',bool(sys.flags.optimize))
if __name__=='__main__':main()
