#!/usr/bin/env python3
from pathlib import Path
import argparse,copy,hashlib,json
BASE='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
def build(w):
 out=copy.deepcopy(w);ops=[['INIT','BACK2','M1']];mapping={};oldh=w['m1_retention'][0]['h_hex'];q1=sum(1<<j for j in next(d['roles']for d in w['cache_metadata']if d['name']=='Q1'))
 for step,o in enumerate(w['operations'],1):
  if o==['INIT','ZKEEP2','L0']:ops.append(['INIT','ZKEEP2','L41'])
  elif o==['ADD','X0','ZRAW0']:ops.extend([o,['MOVE','ZRAW0','zero']])
  elif o==['MOVE','P3','L0']:ops.extend([['ADD','P3','BACK2'],['ADD','BACK2','P3'],['ADD','Q1','P3'],['MOVE','BACK2','Jnew2'],['MOVE','P3','L41']])
  elif o==['ADD','ZRAW0','P3']:pass
  elif o==['MOVE','P3','zero']:ops.extend([o,['ADD','ZRAW0','P3']])
  elif o in [['MOVE','Y2','L0'],['ADD','ZKEEP2','Y2']]:pass
  elif o==['MOVE','Y2','Jnew2']:ops.extend([o,['ADD','BACK2','Y2']])
  else:ops.append(o)
  mapping[step]=len(ops)
 ops.append(['CLEAR','BACK2']);out['base_word_sha256']=BASE;out['operations']=ops;out['milestones']={k:mapping[v]for k,v in w['milestones'].items()}
 for n,ch in [('ZRAW0','zero'),('ZKEEP2','L41')]:
  if n in out['source_cut']:out['source_cut'][n]['chart']=ch
 m=out['m1_retention'][0];m['retention_port']=41;m['point_source']=0;m['backup_h_hex']=oldh;m['h_hex']=hex(q1);m['h_recipe']=['Q1']
 out['coded_port_repair']={'packet':3,'old_port':0,'new_port':41,'retention_field':'ZKEEP2','new_payload_hex':hex(q1),'actual_new_payload_source':'Q1','backup':'BACK2','backup_birth':'M1','backup_destination':'Jnew2','backup_row_hex':oldh,'helper':'ZRAW0','helper_owned_MOVE':['MOVE','ZRAW0','zero'],'helper_point_source':0,'decoder':2,'old_decoder_uses_backup_only':True,'new_payload_has_no_old_Y_reader':True}
 out['affine_scope']='Actual34-preservingcodedport41: oldY2 usesactualbackup; principalreadsnewQ1atM1, retainsatL41, terminalraw0unchanged. Fullbank111coverageisnotcompleteoutputproof.'
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw));a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest())
if __name__=='__main__':main()
