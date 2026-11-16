#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json
BASE='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
def build(w):
 out=copy.deepcopy(w);ops=[];mapping={};capture=0
 for step,o in enumerate(w['operations'],1):
  if o==['INIT','ZRAW0','L0']:ops.append(['INIT','ZRAW0','M1'])
  elif o==['ADD','X0','ZRAW0']:pass
  elif o==['INIT','ZKEEP2','L0']:ops.append(['INIT','ZKEEP2','L29'])
  elif o in [['MOVE','P3','L0'],['MOVE','Y2','L0']]:ops.append([o[0],o[1],'L29'])
  else:ops.append(o)
  if o==['MOVE','X0','C2']:
   ops.extend([['ADD','X0','ZRAW0'],['MOVE','ZRAW0','L29']]);capture+=1
  mapping[step]=len(ops)
 assert capture==1
 out['base_word_sha256']=BASE;out['operations']=ops;out['milestones']={k:mapping[v]for k,v in w['milestones'].items()}
 for n in ['ZRAW0','ZKEEP2']:
  if n in out['source_cut']:out['source_cut'][n]['chart']='L29'
 out['m1_retention'][0]['retention_port']=29;out['m1_retention'][0]['point_source']=0
 out['port_repair']={'packet':3,'old_port':0,'new_port':29,'retention_field':'ZKEEP2','unchanged_retained_row_hex':w['m1_retention'][0]['h_hex'],'raw_helper':'ZRAW0','helper_birth':'M1','helper_raw_source':'X0','source_capture_after_original_move':['MOVE','X0','C2'],'helper_owned_move':['MOVE','ZRAW0','L29'],'point_source_unchanged':0,'decoder':2,'decoder_correction_chart':'Jnew2','old_d_metadata_remains_raw_point_source':True}
 out['affine_scope']='Actualsame34-outputportrepair. Pointsource0 stays0; line-retentionportmoves0to29 withonefullypaidrank4ownedhelperMOVE. Notcomplete111deliveryornewkappa.'
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw));a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
