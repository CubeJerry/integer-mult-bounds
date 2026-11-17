"""Independent subset-incidence certificate; no author imports."""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json
WORD='6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980'
GEO='983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc'
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
ROLES=[14,17,19,20,96,99,101,102]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--geometry',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    assert hashlib.sha256(a.geometry.read_bytes()).hexdigest()==GEO and hashlib.sha256(a.word.read_bytes()).hexdigest()==WORD
    spec=importlib.util.spec_from_file_location('frame_geometry',a.geometry);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    path=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(path.read_bytes()).hexdigest()==NATIVE
    roots=json.loads(path.read_text())['native_roots'];r=[roots[i] for i in ROLES]
    assert len(g.rref(r))==8 and all(sum(x*y for x,y in zip(r[i],r[j]))==0 for i in range(8) for j in range(i))
    word=json.loads(a.word.read_text());C,V,at=g.replay_cut(word);assert word['carrier_interface_before_operation']==1893
    fresh=sum(1<<i for i in ROLES)
    for i in ROLES:
        assert V[f'NATIVE_{i}']==1<<i and C[at[f'NATIVE_{i}']]==g.rref([roots[i]])
        assert at[f'Y{i}']=='zero' and V[f'Y{i}']&fresh==0
    permutations=list(itertools.permutations(range(4)));six=eligible=0;cases=[]
    for p2 in permutations:
        for p3 in permutations:
            current=[frozenset([i])for i in range(8)];history=[]
            for p in [tuple(range(4)),p2,p3]:
                nxt=current.copy()
                for i,j in enumerate(p):nxt[i]=nxt[4+j]=current[i]|current[4+j]
                current=nxt;history.append(current)
            if any(len(x)!=6 for x in current):continue
            six+=1
            # Match missing-incidence signatures instead of testing8! seeds.
            missing=[tuple(i for i in range(4)if pos not in current[i])for pos in range(8)]
            if any(len(x)!=1 for x in missing):continue
            groups=[[pos for pos,x in enumerate(missing)if x==(i,)]for i in range(4)]
            if any(len(x)!=2 for x in groups):continue
            eligible+=1
            for choices in itertools.product([0,1],repeat=4):
                seed=[None]*8
                for i,slots in enumerate(groups):
                    labels=[i,4+p3[i]]
                    for k,pos in enumerate(slots):seed[pos]=labels[k^choices[i]]
                assert sorted(seed)==list(range(8))
                for i,j in enumerate(p3):assert {seed[k]for k in current[i]}==set(range(8))-{i,4+j}
                witnesses=[]
                for i,j in enumerate(p3):
                    u={seed[k]for k in history[1][i]};v={seed[k]for k in history[1][4+j]}
                    na=set(range(4))-{i};nb=set(range(4,8))-{4+j};gaps=[na-u,na-v,nb-u,nb-v];assert all(gaps)
                    witnesses.append({'pair':[i,4+j],'incoming':[sorted(u),sorted(v)],'required':[sorted(na),sorted(nb)],'missing':[sorted(x)for x in gaps]})
                cases.append({'round2':p2,'round3':p3,'seed':seed,'witnesses':witnesses})
    assert six==120 and eligible==12 and len(cases)==192
    gl2=[(a,b,c,d)for a,b,c,d in itertools.product([0,1],repeat=4)if(a*d-b*c)%2]
    assert len(gl2)==6 and all(not(a and b and c and d)for a,b,c,d in gl2)
    result={'status':'PASS_INDEPENDENT_THREE_ACTUAL_MEETINGS_GATE','parent_word_sha256':WORD,'geometry_sha256':GEO,'native_sha256':NATIVE,'parent_actual_fields':len(V),'raw_seeds_and_empty_fresh_Y_response_checked':True,'normalized_schedules':576,'six_line_final_schedules':six,'feasible_incidence_signatures':eligible,'bijective_seed_assignments':len(cases),'final_pair_witnesses':4*len(cases),'binary_GL2_matrices':gl2,'cases':cases,'scope':'Three actual cochart cross-frame perfect-matching rounds, all meetings obligatory even for identity maps; eight single native-unit seeds, no extra reads or outside records; binary invertible local maps. No general receiver exclusion.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
