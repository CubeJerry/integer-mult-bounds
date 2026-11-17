"""Independent exact geometry, current-field audit and remapped Shannon dual."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
PINS={'geometry':'983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc','entropy':'f1da4816d7c0b285271735f53158f180b349798788ee67ed428e37f1f45429fc','word':'6256e8349cd6b74e91bcd225141eb84325557eda92fba25cc51ed288dd4a7000','mapped':'37a7dd9def5e961e81f75e14902c73d4cf15d6c10f499afff9ffbaa1aaa6c918','old_dual':'67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e'}
DONE=set(range(8))|{14,17,19,20,96,99,101,102}
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    for k in PINS:p.add_argument('--'+k.replace('_','-'),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    for k,v in PINS.items():assert hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==v,k
    g=module(a.geometry,'independent_16_geometry');h=module(a.entropy,'independent_16_entropy')
    native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    assert hashlib.sha256(native.read_bytes()).hexdigest()==g.NATIVE
    R=json.loads(native.read_text())['native_roots'];word=json.loads(a.word.read_text());C,V,at=g.replay_cut(word)
    assert word['carrier_interface_before_operation']==2091 and len(V)==424
    for i,r in enumerate(R):assert C[f'L{i}']==g.rref([r]) and C[f'F{i}']==g.nullspace([r])
    completed={i for i in range(111) if V[f'Y{i}']==(1<<(111+i))^(1<<i)}
    assert completed==DONE and all(V[f'X{i}']==1<<i and at[f'X{i}']=='Hub' for i in range(111))
    unfinished=set(range(111))-DONE;assert len(unfinished)==95
    nonaxis=((1<<111)-1)^255;checks=[];leaks={}
    for i in range(8,111):
        neighbours=sum(1<<j for j in range(111) if sum(x*y for x,y in zip(R[i],R[j]))==0)
        inside=[n for n in sorted(V) if all(sum(x*y for x,y in zip(row,R[i]))==0 for row in C[at[n]])]
        bad=[n for n in inside if V[n]&nonaxis&~neighbours]
        if i in unfinished:
            assert not bad and at[f'Y{i}']=='zero';checks.append({'receiver':i,'inside_fields':len(inside)})
        else:assert bad;leaks[str(i)]=bad
    cert=json.loads(a.mapped.read_text());old=json.loads(a.old_dual.read_text())
    assert not set(old['roles']+old['isolates'])<=unfinished
    oldroles=old['roles']+old['isolates'];newroles=cert['roles']+cert['isolates']
    perm=cert['transport']['coordinate_permutation'];mask=cert['transport']['old_coordinate_sign_mask']
    def normalized(r):
        s=1 if next(x for x in r if x)>0 else -1;return tuple(s*x for x in r)
    for i,j in zip(oldroles,newroles):
        row=[0]*8
        for k,x in enumerate(R[i]):row[perm[k]]=x*(-1 if mask>>k&1 else 1)
        assert normalized(row)==normalized(R[j])
    assert cert['terms']==old['terms'] and cert['adjacency_masks']==old['adjacency_masks']
    exact=h.verify(cert,R,unfinished);controls=[]
    bad=copy.deepcopy(cert);bad['terms'].pop()
    try:h.verify(bad,R,unfinished)
    except ValueError as e:controls.append(str(e))
    else:raise AssertionError('missing dual row accepted')
    try:h.verify(old,R,unfinished)
    except ValueError as e:controls.append(str(e))
    else:raise AssertionError('completed old role accepted')
    result={'status':'PASS_INDEPENDENT_POST16_NINE_DESCENTS','pins':PINS,'cut':2091,'all_original_columns':222,'actual_fields':424,'completed_roles':sorted(DONE),'all95_strong_native_locality':checks,'completed_facet_leaks':leaks,'core':cert['roles'],'isolates':cert['isolates'],'exact_dual':exact,'negative_controls':controls,'minimum_additional_whole_record_descents':9,'scope':'New actual source and transported witness; fixed schedule, zero-error finite alphabet, monotone public and arbitrary paid nested owned routes. The8 prior clique descents are already charged. No16-global-raw-input grant.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
