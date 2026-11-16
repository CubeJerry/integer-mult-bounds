#!/usr/bin/env python3
"""Retimes a real packet and couples its retained row through an existing meeting."""
import argparse,copy,hashlib,json
from pathlib import Path
BASE='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
def build(w):
    out=copy.deepcopy(w);old=w['operations'];start=old.index(['INIT','P7','Hub']);end=w['milestones']['seed8_before_Y'];assert old[end-1]==['ADD','E79','P7'];block=old[start:end]
    assert all(o[1]=='P7'if o[0]in ['INIT','MOVE']else o[0]=='ADD'and'P7'in o for o in block)
    ops=[];mapping={};source=w['milestones']['source_cut'];g=int(w['higher_source_delivery']['first_retention_hex'],16)
    for step,o in enumerate(old,1):
        if step==source+1:ops.extend(block)
        if start<=step-1<end:continue
        ops.append(o)
        if o in [['MOVE','P0','D3_21'],['MOVE','Y3','D3_21'],['MOVE','Y21','D3_21']]:ops.append(['ADD','HKEEP_D7',o[1]])
        mapping[step]=len(ops)
    out['operations']=ops;out['milestones']={key:(max(mapping[s]for s in mapping if s<=step)if key=='seed8_before_Y'else mapping[step])for key,step in w['milestones'].items()}
    out['base_word_sha256']=BASE;out['multi_retention'][0]['first_retention_hex']=hex(int(w['multi_retention'][0]['first_retention_hex'],16)^g)
    out['principal_routes']=[[o[2]for o in ops if o[:2]==['MOVE',f'P{z}']]for z in range(8)]
    out['cross_bank_coupling']={'earlier_packet':7,'coupled_packet':0,'actual_retained_owner':'HKEEP_D7','meeting_chart':'D3_21','transported_row_hex':hex(g),'changed_lower_retention':'KEEP_C0','affected_receivers':[3,21],'extra_ADD':3,'extra_MOVE':0,'extra_owners':0,'old_initial_P7_block_start':start,'old_initial_P7_block_end_exclusive':end,'source_originals_unchanged_between_source_cut_and_old_P7_block':True}
    out['history_claim']='Actual P7 prevalue is retained at D3 before P0 visits; its real cross-bank copy changes only the first C0 retention and is compensated at existing Y3/Y21 D3 visits. All34 endpoints and all terminal seeds are unchanged. No new supplier or kappa.'
    out['affine_scope']='Concrete three-ADD cross-bank source coupling. The separated-bank108 premise no longer directly describes the changed C0 retention; the fixed transferred row does not itself remove its three coarse duals.'
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;w=build(json.loads(raw));a.out.mkdir(parents=True,exist_ok=True);path=a.out/'WORD.json';path.write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':main()
