"""Transport an exact entropy witness and audit five actual source cuts."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
CORE=[61,82,83,20,18,71,70,69,74,76,63];ISOLATES=[65,109,107]
PERM=[0,5,1,4,3,6,2,7];SIGN=1
OLD='c5d40e71246008699cb137eaa2badd2674253b0567c87e54fa7fa5809bacc79f'
HELPER='f1da4816d7c0b285271735f53158f180b349798788ee67ed428e37f1f45429fc'
GEOMETRY='983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(p,name):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def normalize(row):
    first=next(x for x in row if x);return tuple(x if first>0 else-x for x in row)
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--geometry',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=a.repo/'research/moonshot-005-program';old_path=base/'sessions/2026-11-17-S020/checkpoint1-evidence/R/entropy54/CERTIFICATE.json';helper=old_path.with_name('check.py')
    assert digest(old_path)==OLD and digest(helper)==HELPER and digest(a.geometry)==GEOMETRY
    g=module(a.geometry,'root_independent_geometry');h=module(helper,'pinned_exact_entropy_verifier')
    native=base/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert digest(native)==g.NATIVE;R=json.loads(native.read_text())['native_roots']
    old=json.loads(old_path.read_text());mapped=copy.deepcopy(old);mapped['roles']=CORE;mapped['isolates']=ISOLATES
    expired=set(range(8))|set(range(22,46))|set(range(88,96));fresh=set(range(111))-expired;assert len(fresh)==71 and set(CORE+ISOLATES)<=fresh
    mapping=[]
    for i,j in zip(old['roles']+old['isolates'],CORE+ISOLATES):
        row=[0]*8
        for k,x in enumerate(R[i]):row[PERM[k]]=x*(-1 if SIGN>>k&1 else 1)
        assert normalize(row)==normalize(R[j]);mapping.append({'old_role':i,'new_role':j})
    old_all=old['roles']+old['isolates'];new_all=CORE+ISOLATES
    assert all((sum(x*y for x,y in zip(R[i],R[j]))==0)==(sum(x*y for x,y in zip(R[u],R[v]))==0)for i,u in zip(old_all,new_all)for j,v in zip(old_all,new_all))
    mapped.pop('discovery',None);mapped['transport']={'source_certificate_sha256':OLD,'coordinate_permutation':PERM,'old_coordinate_sign_mask':SIGN,'role_map':mapping}
    exact=h.verify(mapped,R,fresh);cases=[];xmask=sum(1<<i for i in fresh)
    canonical_basis={}
    for i in sorted(fresh):
        row=(1<<i)|sum(1<<j for j in fresh if sum(x*y for x,y in zip(R[i],R[j]))==0)
        while row:
            b=row.bit_length()-1
            if b in canonical_basis:row^=canonical_basis[b]
            else:canonical_basis[b]=row;break
    assert len(canonical_basis)==9
    exact['canonical_scalar_upper_rank']=9
    exact['canonical_independent_rows_hex']=[hex(canonical_basis[b])for b in sorted(canonical_basis,reverse=True)]
    for name,pin in g.PINS.items():
        path=a.inputs/name/'WORD.json';assert digest(path)==pin;word=json.loads(path.read_text());charts,V,P=g.replay_cut(word)
        assert all(P[f'X{i}']==P[f'NATIVE_{i}']==f'L{i}'and V[f'X{i}']==V[f'NATIVE_{i}']==1<<i for i in fresh)
        checks=[]
        for i in sorted(fresh):
            neighbours=sum(1<<j for j in fresh if sum(x*y for x,y in zip(R[i],R[j]))==0);inside=[]
            for n in V:
                if all(sum(x*y for x,y in zip(row,R[i]))==0 for row in charts[P[n]]):
                    assert not(V[n]&xmask&~neighbours),(name,i,n);inside.append(n)
            assert not((1<<i)&neighbours)and 'Y'+str(i)in inside
            checks.append({'receiver':i,'inside_fields':len(inside)})
        cases.append({'source':name,'word_sha256':pin,'cut':word['carrier_interface_before_operation'],'live_fields':len(V),'untouched_roles':71,'receiver_locality_checks':checks,'nonlocal_leaks':[],'minimum_future_whole_record_descents':9})
    bad=copy.deepcopy(mapped);bad['terms'].pop()
    try:h.verify(bad,R,fresh)
    except ValueError as ex:control=str(ex)
    else:raise AssertionError('omitted dual term escaped')
    result={'status':'PASS_MAPPED_17_OVER_2_WITNESS_AND_FIVE_ACTUAL_CUTS','native_sha256':digest(native),'prior_dual_sha256':OLD,'prior_verifier_sha256':HELPER,'geometry_sha256':GEOMETRY,'mapped_core':CORE,'mapped_isolates':ISOLATES,'coordinate_permutation':PERM,'old_coordinate_sign_mask':SIGN,'exact_dual':exact,'cases':cases,'omitted_dual_term_rejected':control,'scope':'Fixed-schedule monotone-public, arbitrary nested-owned continuation; at least9 future whole-record downward transfers. All-field linear or zero-error deterministic finite-alphabet nonlinear scope as proved. No9-lifetime or9-Hub-ground assertion.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True)
    for name,value in [('CERTIFICATE.json',result),('MAPPED-DUAL.json',mapped)]:(a.out/name).write_text(json.dumps(value,indent=2)+'\n')
    print(result['status'],exact['witness_bound'],len(cases),'cuts')
if __name__=='__main__':main()
