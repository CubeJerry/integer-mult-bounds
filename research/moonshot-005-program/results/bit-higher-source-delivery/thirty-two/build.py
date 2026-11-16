#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json
BASE='6a1eef8ef1f620914b3f014c9ba129bbe389c6fd5a010872f3e5cca88f5cb52f'
def build(w):
 out=copy.deepcopy(w);ops=[['INIT','HRAW27','L27'],['ADD','X27','HRAW27'],['INIT','HKEEP_D7','D3_21'],['INIT','HKEEP_L27','L27']];mapping={};mask=sum(1<<j for j in[1,73,75,79]);oldp=int(w['seed_rows_hex'][7],16)
 for step,o in enumerate(w['operations'],1):
  if o==['MOVE','P7','zero']:
   ops +=[['MOVE','P7','D3_21'],['ADD','P7','HKEEP_D7'],['ADD','HKEEP_D7','P7'],['ADD','AFF0','P7'],['MOVE','P7','L27'],['ADD','P7','HKEEP_L27'],['ADD','HKEEP_L27','P7'],['ADD','HRAW27','P7'],['MOVE','P7','zero']]
  elif o==['MOVE','Y10','F10']:
   ops +=[['MOVE','Y10','L27'],['ADD','HKEEP_L27','Y10'],o]
  elif o==['MOVE','Y27','F27']:
   ops +=[['ADD','P7','Y27']]+[['ADD',f'E{j}','Y27']for j in[1,73,75,79]]+[o]
  else:ops.append(o)
  mapping[step]=len(ops)
 ops +=[['CLEAR','HRAW27'],['CLEAR','HKEEP_D7'],['CLEAR','HKEEP_L27']]
 out['base_word_sha256']=BASE;out['operations']=ops;out['milestones']={k:mapping[v]for k,v in w['milestones'].items()};out['targets']=sorted(w['targets']+[10,27]);out['seed_rows_hex'][7]=hex((1<<27)^mask)
 out['higher_source_delivery']={'packet':7,'first_chart':'D3_21','actual_acquired_owner':'AFF0','actual_acquired_row_hex':hex(1<<10),'first_retention':'HKEEP_D7','first_retention_hex':hex(oldp^mask),'second_chart':'L27','second_retention':'HKEEP_L27','second_retention_hex':hex(1<<10),'actual_raw_owner':'HRAW27','new_targets':[10,27],'ground_mask_points':[1,73,75,79],'changed_ground_row_hex':out['seed_rows_hex'][7]}
 out['ground_code']='Exactseedrows: P6 carries its actualExtra6perturbation; P7 carries rawX27 pluslistedEcorrections. FormerP7prevalue is retainedonlyatD3_21.'
 out['affine_scope']='Concrete32-outputnativehigher-sourcecontinuation. P7substitutionchangesitsgroundrow, preservingold30endpoints. No complete supplier or newkappa.'
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw));a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
