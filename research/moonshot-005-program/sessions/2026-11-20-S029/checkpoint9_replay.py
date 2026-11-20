"""Replay the exact source, entropy, pricing and native-activity certificates."""
import argparse,json,subprocess,sys
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    repo=a.repo.resolve();out=a.out.resolve();r=repo/'research/moonshot-005-program/results';out.mkdir(parents=True,exist_ok=True)
    c=r/'bit-native-directed-arc-gap';k=r/'bit-covariant-rebalanced-cutoffs/ideal';f=r/'bit-paid-native-middle-feedback'
    h=r/'bit-native-prefix-suffix-stability';w=h/'activity/output/WEIGHTS.json'
    result={}
    for name,script,args,wanted,record in [
        ('native_arc',c/'author/replay.py',[],c/'author/output','RESULT.json'),
        ('dual_independent',c/'review/check.py',['--dual-dir',c/'author/output'],c/'review/output','REVIEW.json'),
        ('ideal_moments',k/'check.py',['--repo',repo],k/'output','RESULT.json'),
        ('weighted_charts',h/'activity/check.py',['--repo',repo],h/'activity/output','RESULT.json'),
        ('original_holders',h/'activity-review/check.py',['--repo',repo,'--weights',w],h/'activity-review/output','RESULT.json'),
        ('physical_feedback',f/'verify.py',['--repo',repo],f/'author/output','RESULT.json')
    ]:
        dst=out/name
        subprocess.run([sys.executable,'-B',script,*args,'--out',dst],check=True,stdout=subprocess.DEVNULL)
        observed=json.loads((dst/record).read_bytes());assert observed==json.loads((wanted/record).read_bytes())
        result[name]=observed
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
