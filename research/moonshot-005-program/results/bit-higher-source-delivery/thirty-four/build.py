#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json
BASE='73a6c4adb00498a0c33956a3aa1a0525eb143fa0179a4abaeb238b150774da45'
def build(w):
 out=copy.deepcopy(w);ops=[['INIT','HRAW19','L19'],['ADD','X19','HRAW19'],['INIT','HKEEP_E6','Extra6'],['INIT','HKEEP_L19','L19']];mapping={};mask=sum(1<<j for j in[75,77,79]);oldp=int(w['seed_rows_hex'][6],16)
 for step,o in enumerate(w['operations'],1):
  if o==['MOVE','P6','zero']:
   ops +=[['ADD','P6','HKEEP_E6'],['ADD','HKEEP_E6','P6'],['ADD','EXTRA_AFF','P6'],['MOVE','P6','L19'],['ADD','P6','HKEEP_L19'],['ADD','HKEEP_L19','P6'],['ADD','HRAW19','P6'],['MOVE','P6','zero']]
  elif o==['MOVE','Y20','F20']:ops +=[['MOVE','Y20','L19'],['ADD','HKEEP_L19','Y20'],o]
  elif o==['MOVE','Y19','F19']:ops +=[['ADD','P6','Y19']]+[['ADD',f'E{j}','Y19']for j in[75,77,79]]+[o]
  else:ops.append(o)
  mapping[step]=len(ops)
 ops +=[['CLEAR','HRAW19'],['CLEAR','HKEEP_E6'],['CLEAR','HKEEP_L19']]
 out['base_word_sha256']=BASE;out['operations']=ops;out['milestones']={k:mapping[v]for k,v in w['milestones'].items()};out['targets']=sorted(w['targets']+[19,20]);out['seed_rows_hex'][6]=hex((1<<19)^mask)
 out['extra_source_delivery']={'packet':6,'first_chart':'Extra6','actual_acquired_owner':'EXTRA_AFF','actual_acquired_row_hex':hex(1<<20),'first_retention':'HKEEP_E6','first_retention_hex':hex(oldp^mask),'second_chart':'L19','second_retention':'HKEEP_L19','second_retention_hex':hex(1<<20),'actual_raw_owner':'HRAW19','new_targets':[19,20],'ground_mask_points':[75,77,79],'changed_ground_row_hex':out['seed_rows_hex'][6]}
 out['ground_code']='Exactseedrows: P6 nowrawX19+listedEcorrections andP7 rawX27+listedEcorrections. FormerP6prevalue retainedonlyatExtra6; formerP7prevalue retainedonlyatD3_21.'
 out['affine_scope']='Concrete34-outputnativehigher-sourcecontinuation. Bothspareprincipalgroundrowschanged; old32outputs preserved. No complete supplier or newkappa.'
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw));a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
