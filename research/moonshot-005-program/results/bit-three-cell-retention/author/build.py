#!/usr/bin/env python3
"""Three actual third-cell resets, using original visitors of private correction charts."""
import argparse,copy,hashlib,json
from pathlib import Path
BASE='d28b6ae55b9d3c3cab440c24af971babbe7fb2413180ec1cb3d5e2fa4c77bb71'
CHOICE={0:30,1:38,2:39}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=a.base.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE;old=json.loads(raw);w=copy.deepcopy(old)
    source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots']
    defs=[];ops=[];owners=[]
    for dd in old['multi_retention']:
        z,d,b=dd['packet'],dd['d'],dd['b'];j=CHOICE[z];assert j in dd['unique_roles']and j not in old['targets']
        assert sum(x*y for x,y in zip(R[d],R[j]))==0
        triad=(1<<b)^(1<<5)^(1<<15);assert int(dd['h_hex'],16)^int(dd['unique_hex'],16)==triad
        tr,rr=f'TRIAD{b}',f'RAW_J{j}';owners.extend([tr,rr]);ops +=[['INIT',tr,f'J{b}'],['INIT',rr,f'J{b}']]
        w['source_cut'].update({tr:{'chart':f'J{b}','row_hex':'0x0'},rr:{'chart':f'J{b}','row_hex':hex(1<<j)}})
        defs.append({'packet':z,'donor':d,'old_receiver':b,'new_receiver':j,'intermediate_chart':f'J{b}',
                     'intermediate_owner':tr,'intermediate_value_hex':hex(triad),'actual_raw_owner':rr,
                     'actual_raw_capture_original':f'X{j}','line_owner':f'KEEP_M{b}',
                     'line_chart':f'L{d}','line_value_hex':hex(1<<j)})
    early={dd['old_receiver']for dd in defs};marks={};loaded=[];captured=[];delivered=[];retired=False
    for step,o in enumerate(old['operations'],1):
        packet=next((q for q in defs if o==['MOVE',f"P{q['packet']}",f"M{q['old_receiver']}"]),None)
        capture=next((q for q in defs if o==['ADD',f"X{q['new_receiver']}",f"PRIVATE{q['old_receiver']}"]),None)
        recipient=next((q for q in defs if o==['MOVE',f"Y{q['new_receiver']}",f"F{q['new_receiver']}"]),None)
        earlyop=any(f'Y{i}'in o[1:]for i in early)
        if packet:
            z,b,j=packet['packet'],packet['old_receiver'],packet['new_receiver']
            ops +=[['MOVE',f'P{z}',f'J{b}'],['ADD',f'PRIVATE{b}',f'P{z}'],
                    ['ADD',f'P{z}',f'TRIAD{b}'],['ADD',f'TRIAD{b}',f'P{z}'],['ADD',f'RAW_J{j}',f'P{z}']]
            loaded.append(z)
        elif capture:ops +=[o,['ADD',capture['actual_raw_capture_original'],capture['actual_raw_owner']]];captured.append(capture['new_receiver'])
        elif recipient:
            j,d=recipient['new_receiver'],recipient['donor'];ops +=[['MOVE',f'Y{j}',f'L{d}'],['ADD',recipient['line_owner'],f'Y{j}'],o];marks[f'completed_{j}']=len(ops);delivered.append(j)
        elif earlyop:
            assert step<=old['milestones']['seed8_before_Y']
        else:
            if o[0]=='CLEAR'and not retired:ops +=[['CLEAR',name]for name in owners];retired=True
            ops.append(o)
        for name,index in old['milestones'].items():
            if index==step and name not in [f'completed_{i}'for i in early]:marks[name]=len(ops)
        if step==old['milestones']['seed8_before_Y']:
            for dd in defs:
                b=dd['old_receiver'];ops +=[['MOVE',f'Y{b}','SH2'],['ADD','SHARED',f'Y{b}'],
                    ['MOVE',f'Y{b}',f'J{b}'],['ADD',f'TRIAD{b}',f'Y{b}'],['MOVE',f'Y{b}',f'F{b}']];marks[f'completed_{b}']=len(ops)
    assert loaded==[0,1,2]and sorted(captured)==sorted(CHOICE.values())and sorted(delivered)==sorted(CHOICE.values())
    w.update(schema='actual-third-retention-thirty-v1',base_word_sha256=BASE,operations=ops,milestones=marks,
             targets=sorted(old['targets']+list(CHOICE.values())),early_completed_targets=[],third_retention=defs,
             history_claim='Three actual intermediate capture/reset/load cells at existing J16,J23,J22 preserve all27 old endpoints and deliver actual raw30,38,39 at existing native donor lines. All source originals and terminal seeds are unchanged. No additional owned MOVE.',
             ground_code=old['ground_code'])
    w['principal_routes']=[[o[2]for o in ops if o[0]=='MOVE'and o[1]==f'P{k}']for k in range(8)]
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(w,indent=2)+'\n');print(hashlib.sha256((a.out/'WORD.json').read_bytes()).hexdigest(),len(ops))
if __name__=='__main__':main()
