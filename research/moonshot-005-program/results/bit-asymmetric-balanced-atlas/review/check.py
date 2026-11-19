#!/usr/bin/env python3
"""Independent checks of actual owners, chart incidences and causal capacities."""
import argparse
from collections import Counter
import gzip,hashlib,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--bank',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    bank=a.bank;assert bank in (480,1920);port=bank//240;p=bank//16
    pg=a.repo/'research/moonshot-005-program';lp=pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    raw=gzip.decompress(lp.read_bytes());assert hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    lay=json.loads(raw);R=lay['root_table'];H=[sum(1<<j for j in v) for v in lay['A2']];D=[sum(1<<j for j in v) for v in lay['D4']];dual=lay['dual_D4']
    O=[sum(1<<j for j,y in enumerate(R) if sum(u*v for u,v in zip(x,y))==0) for x in R]
    assert all(dual[dual[d]]==d and all(O[j]&D[dual[d]]==D[dual[d]] for j in range(120) if D[d]>>j&1) for d in range(3150))
    J=[[j for j in range(111) if h>>j&1] for h in H]
    HD=[[d for d,v in enumerate(D) if h&v==h] for h in H];assert all(len(v)==45 for v in HD)
    DH=[[] for _ in D]
    for h,ds in enumerate(HD):
        for d in ds:DH[d].append(h)
    assert all(len(v)==16 for v in DH)
    phase=[];quota=[];early=[]
    if bank==1920:
        fr=(pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json').read_bytes()
        assert hashlib.sha256(fr).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
        factors=dict(json.loads(fr)['factors'])
        for h,js in enumerate(J):
            x=12//len(js)+factors.get(h,0) if js else 0;assert len(js)*x%3==0
            phase.append(len(js)*x//3);quota.append({j:15*max(8,x) for j in js});early.append({j:15*x for j in js})
        phase_hash=hashlib.sha256(fr).hexdigest()
    else:
        fr=(a.author/'PHASE-CERTIFICATE.json').read_bytes();cert=json.loads(fr)
        S=set(cert['full_early_planes']);L={int(h):j for h,j in cert['large_early_donor_at_partial_plane'].items()}
        assert len(S)==65 and all(len(J[h])==3 for h in S)
        assert set(L)=={h for h,js in enumerate(J) if len(js)==2} and all(j in J[h] for h,j in L.items())
        for h,js in enumerate(J):
            phase.append(2 if h in S else int(bool(js)))
            quota.append({j:45 if len(js)==1 else 30 for j in js})
            early.append({j:45 if len(js)==1 else 30 if h in S or L.get(h)==j else 15 for j in js})
        for j in range(111):
            assert sum(j in J[h] for h in S)+sum(v==j for v in L.values())+2*sum(len(js)==1 and j in js for js in J)==4
        assert 111*240<1119*45<=111*480
        phase_hash=hashlib.sha256(fr).hexdigest()
    assert all(sum(v.values())==45*phase[h] for h,v in enumerate(early))
    assert all(sum(v.get(j,0) for v in early)==bank for j in range(111))
    l=[sum(phase[h] for h in hs) for hs in DH];reserve=[l[d]+l[dual[d]]-16*port for d in range(3150)]
    assert min(reserve)>=0 and sum(reserve)==12*bank
    seen={k:[0]*111 for k in ('X','Y')};moves=Counter();flags=Counter();branches=Counter();birth=Counter();close=Counter();digest=hashlib.sha256();total=0
    def route(row,record=True):
        nonlocal total
        kind,j,c,h,d,k,left,right=row
        assert kind in seen and 0<=j<111 and 0<=c<bank and 0<=d<3150
        if record:
            assert not seen[kind][j]>>c&1;seen[kind][j]|=1<<c;total+=1
        if h is not None:
            assert 0<=h<1120 and H[h]&D[d]==H[h]
            if left is not None:assert 0<=left<111 and H[h]>>left&1
        if k is not None:
            assert 0<=k<1120 and H[k]&D[dual[d]]==H[k]
            if right is not None:assert 0<=right<111 and H[k]>>right&1
        if kind=='X':
            assert h is not None and left==j;ranks=[1,2,4]
            if k is None:assert right is None
            else:
                ranks.append(6)
                if right is not None:ranks.append(7)
            ranks.append(8)
            if record and k is None:close[d]+=1
        else:
            assert k is not None and right==j;ranks=[0]
            if h is None:assert left is None
            else:
                if left is not None:ranks.append(1)
                ranks.append(2)
            ranks += [4,6,7]
            if record and h is None:birth[d]+=1
        gaps=[y-x for x,y in zip(ranks,ranks[1:])];assert sum(gaps)==7 and all(v>0 for v in gaps)
        if record:
            moves.update(gaps)
            if h is not None:flags['L',h,d,kind]+=1;branches['L',h,left,kind]+=1
            if k is not None:flags['R',k,dual[d],kind]+=1;branches['R',k,right,kind]+=1
    first=None
    with gzip.open(a.author/'output/ROUTES.jsonl.gz','rb') as stream:
        for line in stream:
            digest.update(line);row=json.loads(line)
            if first is None:first=row
            route(row)
    assert total==2*111*bank and all(v==(1<<bank)-1 for side in seen.values() for v in side)
    assert all(birth[d]==close[d]==reserve[d] for d in range(3150))
    for h,js in enumerate(J):
        for d in HD[h]:
            assert flags['L',h,d,'X']==flags['R',h,d,'Y']==phase[h]
            assert flags['L',h,d,'Y']==flags['R',h,d,'X']==port-phase[h]
        for j in js:
            assert branches['L',h,j,'X']==branches['R',h,j,'Y']==early[h][j]
            assert branches['L',h,j,'Y']==branches['R',h,j,'X']==quota[h][j]-early[h][j]
        direct=45*port-sum(quota[h].values())
        assert branches['L',h,None,'Y']==branches['R',h,None,'X']==direct
    assert moves==Counter({1:bank*4451//8,2:bank*7213//16,4:24*bank})
    pairs=0
    for i in range(111):
        for j in range(111):
            if not(O[i]>>j&1):continue
            hs=[h for h in range(1120) if j in J[h] and H[h]&O[i]==H[h]]
            ks=[k for k in range(1120) if i in J[k] and H[k]&O[j]==H[k]]
            assert len(hs)==len(ks)==16
            left=Counter();right=Counter();lc=Counter();rc=Counter()
            for h in hs:
                assert quota[h][j]>=p and early[h][j]>=15*phase[h]
                ds=[d for d in HD[h] if D[d]&O[i]==D[d]];assert len(ds)==15
                for d in ds:left[d]+=phase[h];lc[d]+=1
            for k in ks:
                assert quota[k][i]>=p and early[k][i]>=15*phase[k]
                ds=[dual[d] for d in HD[k] if D[d]&O[j]==D[d]];assert len(ds)==15
                for d in ds:right[d]+=port-phase[k];rc[d]+=1
            assert set(left)==set(right) and len(left)==60
            assert set(lc.values())==set(rc.values())=={4}
            assert all(left[d]>=right[d] for d in left)
            pairs+=1
    assert pairs==6470
    try:route(first)
    except AssertionError:pass
    else:raise AssertionError('duplicate owner accepted')
    bad=first[:];bad[4]=next(d for d in range(3150) if H[bad[3]]&D[d]!=H[bad[3]])
    try:route(bad,False)
    except AssertionError:pass
    else:raise AssertionError('noncontaining middle accepted')
    result={'status':'PASS_INDEPENDENT_LITERAL_COMPRESSED_ATLAS','bank':bank,'port':port,'ordinary_quotient':p,
            'original_routes':total,'public_movement':dict(moves),'canonical_gap8':9*bank,
            'middle_births_and_closures_each':sum(reserve),'all_foreign_path_checks':pairs,
            'route_sha256':digest.hexdigest(),'phase_sha256':phase_hash,'author_code_imported':False,
            'physical_low_defect_map_constructed':False,'negative_controls':['duplicate original','noncontaining middle'],
            'rank_only_degree_bound':10*(6470+222)*bank}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
