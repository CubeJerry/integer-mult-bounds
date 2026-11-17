"""Independent actual-field and Shannon audit after paid upward reuse."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
PINS={'geometry':'983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc','entropy':'f1da4816d7c0b285271735f53158f180b349798788ee67ed428e37f1f45429fc','word':'581266484817956c8f6b1dc279291a362ddf00a4c580f25a35f3fe56670c7729','mapped':'e8cce0c701912e3be111603447ec1b0f95daee1b84a783cce15a5fe730b10e92','old_dual':'67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e'}
EXPORT_ROLES={22,23,26,27,42,43,44,45,73,74,75,76,77,78,79,80}
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    for k in PINS:p.add_argument('--'+k.replace('_','-'),type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    for k,v in PINS.items():assert hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==v,k
    g=module(a.geometry,'independent_half_geometry');h=module(a.entropy,'independent_half_entropy')
    native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(native.read_bytes()).hexdigest()==g.NATIVE
    R=json.loads(native.read_text())['native_roots'];word=json.loads(a.word.read_text());C,V,at=g.replay_cut(word)
    assert word['carrier_interface_before_operation']==2097 and len(V)==420
    for i,r in enumerate(R):assert C[f'L{i}']==g.rref([r]) and C[f'F{i}']==g.nullspace([r])
    complete={i for i in range(111) if V[f'Y{i}']==(1<<(111+i))^(1<<i)};assert complete==set(range(8))
    assert all(V[f'X{i}']==1<<i and at[f'X{i}']=='Hub' for i in range(111))
    mask=0
    for e in word['construction']['proper_half_service']['exports']:
        row=V[e['export_owner']];assert row==int(e['payload_hex'],16);mask|=row
    assert {i for i in range(111) if mask>>i&1}==EXPORT_ROLES
    unknown=set(range(8,111))-EXPORT_ROLES;unknown_mask=sum(1<<i for i in unknown);assert len(unknown)==87
    nonaxis=((1<<111)-1)^255;checks=[];leaks=[]
    for i in range(8,111):
        neighbours=sum(1<<j for j in range(111) if sum(x*y for x,y in zip(R[i],R[j]))==0)
        inside=[n for n in sorted(V) if all(sum(x*y for x,y in zip(row,R[i]))==0 for row in C[at[n]])]
        for n in inside:
            forbidden=V[n]&nonaxis&~neighbours
            if forbidden:leaks.append({'receiver':i,'field':n,'forbidden_mask_hex':hex(forbidden)})
            assert not(V[n]&unknown_mask&~neighbours)
        if i in unknown:checks.append({'receiver':i,'inside_fields':len(inside),'Y_chart_rank':len(C[at[f'Y{i}']])})
    assert len(leaks)==56
    leak_types={'owned_export':sum(x['field'].startswith('HALF_SERVICE_EXPORT_') for x in leaks),'public_Y':sum(x['field'].startswith('Y') for x in leaks)}
    assert sum(leak_types.values())==56
    cert=json.loads(a.mapped.read_text());old=json.loads(a.old_dual.read_text());assert not set(old['roles']+old['isolates'])<=unknown
    perm=cert['transport']['coordinate_permutation'];sign=cert['transport']['old_coordinate_sign_mask']
    def normalize(r):
        s=1 if next(x for x in r if x)>0 else -1;return tuple(s*x for x in r)
    for i,j in zip(old['roles']+old['isolates'],cert['roles']+cert['isolates']):
        row=[0]*8
        for k,x in enumerate(R[i]):row[perm[k]]=x*(-1 if sign>>k&1 else 1)
        assert normalize(row)==normalize(R[j])
    assert cert['terms']==old['terms'];exact=h.verify(cert,R,unknown);controls=[]
    bad=copy.deepcopy(cert);bad['terms'].pop()
    for label,candidate in[('missing_dual_term',bad),('obsolete_conditioned_witness',old)]:
        try:h.verify(candidate,R,unknown)
        except ValueError as e:controls.append({'name':label,'rejected':str(e)})
        else:raise AssertionError('invalid witness accepted')
    result={'status':'PASS_INDEPENDENT_UPWARD_REBASE_FRESH_NINE','pins':PINS,'source_cut':2097,'all_original_columns':222,'actual_fields':420,'actual_completed_roles':sorted(complete),'conditioned_export_inputs':sorted(EXPORT_ROLES),'conditioned_unknown_count':87,'unconditioned_leaks':leaks,'leak_types':leak_types,'all87_receiver_locality_checks':checks,'core':cert['roles'],'isolates':cert['isolates'],'exact_dual':exact,'negative_controls':controls,'minimum_additional_whole_record_descents':9,'scope':'Fixed-schedule zero-error finite-alphabet continuation; arbitrary paid nested owned routes, monotone publics. Conditioning16 source coordinates is a lower-bound relaxation, not a physical global-input grant. All56 leaked incidences are accounted.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
