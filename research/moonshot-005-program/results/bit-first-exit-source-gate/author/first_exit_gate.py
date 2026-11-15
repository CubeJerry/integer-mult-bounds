#!/usr/bin/env python3
"""Exact six/seven-facet source-obstruction witnesses and a changed-basis control."""
from pathlib import Path
import hashlib
import json


def dot(x,y):
    return sum(a*b for a,b in zip(x,y))


def rank(rows):
    basis={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p]=row
                break
    return len(basis)


def singleton_witnesses(roots,modes):
    answer=[]
    for j in range(111):
        demanded=[k for k,m in enumerate(modes) if m['word']>>j&1]
        if len(demanded)<2:
            continue
        inside=[l for l,r in enumerate(roots) if all(dot(r,modes[k]['normal'])==0 for k in demanded)]
        if inside==[j]:
            answer.append({'source':j,'demanded_mode_indices':demanded,'only_native_source_in_common_chart':inside})
    return answer


if __name__=='__main__':
    here=Path(__file__).parent
    repo=next(p for p in here.parents if (p/'AGENTS.md').exists())
    source=repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    raw=source.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='8eba43d142c819c206dce5df87ea4571aaead287'
    roots=json.loads(raw)['native_roots']
    b=[0,0,1,1,0,0,1,-1]
    h=[(dot(roots[72],r)//2+dot(b,r)//2)%2 for r in roots]
    hm=sum(v<<j for j,v in enumerate(h));allones=(1<<111)-1
    K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(roots)) for i,r in enumerate(roots)]
    W=[row&(hm if h[i] else allones^hm) for i,row in enumerate(K)]
    initial=[K[i] for i in [1,3,5,10,11,15,30]]+[K[0]&hm]
    assert rank(W)==15 and rank(initial)==8
    pairs=[(1,18),(3,21),(5,15),(10,27),(30,50),(61,73)]
    for a,c in pairs:
        assert (K[a]&hm)^(K[c]&hm)==hm
    assert rank(initial+[hm])==8
    kb=sum(int(dot(r,b)==0)<<j for j,r in enumerate(roots))
    receipts=[]
    six_pass=[]
    for orientation in range(64):
        roles=[pair[(orientation>>k)&1] for k,pair in enumerate(pairs)]
        six=[{'word':K[i]&hm,'normal':roots[i],'native_normal_role':i} for i in roles]
        seven=six+[{'word':kb,'normal':b,'native_normal_role':None}]
        assert rank(initial+[m['word'] for m in seven])==15
        sw=singleton_witnesses(roots,six)
        if not sw:
            six_pass.append(orientation)
        witnesses=singleton_witnesses(roots,seven)
        assert witnesses
        receipts.append({'orientation':orientation,'native_six_normals':roles,
                         'six_only_witnesses':sw,'seven_mode_witnesses':witnesses})
    assert six_pass==[26,28,41,47,53]
    assert receipts[0]['six_only_witnesses'][0]['source']==6
    candidate=json.loads((here/'alternate-basis-candidate.json').read_text())
    alternate=[{'word':int(m['word']),'normal':m['normal']}for m in candidate['modes']]
    for m in alternate:
        assert rank(W+[m['word']])==15
        assert all(not(m['word']>>j&1)or dot(r,m['normal'])==0 for j,r in enumerate(roots))
    assert rank(initial+[m['word']for m in alternate])==15
    assert not singleton_witnesses(roots,alternate)
    result={'status':'PASS_FIRST_EXIT_GATE_64_ORIENTATIONS','source_sha256':hashlib.sha256(raw).hexdigest(),
            'source_git_blob':'8eba43d142c819c206dce5df87ea4571aaead287',
            'initial_seed_dimension':8,'target_code_dimension':15,'orientations':receipts,
            'six_only_passing_orientations':six_pass,
            'all_64_seven_mode_families_have_singleton_source_witness':True,
            'changed_basis_control':{'status':'PASSES_NECESSARY_GATE_ONLY','modes':alternate,'joint_rank_with_seed':15,'actual_source':False},
            'model':'Pre-Hub preparation by monotone original-X carriers and stationary zero-born caches; no original-Y relays, extra ascending carriers, downward preprocessing transport, nonlocal initial data or nonmonotone movement.',
            'new_complete_kappa':False}
    (here/'output/FIRST-EXIT-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seven_families_rejected':64,'six_only_controls':six_pass,'changed_basis_passes':True}))
