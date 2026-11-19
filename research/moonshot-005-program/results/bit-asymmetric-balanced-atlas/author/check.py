#!/usr/bin/env python3
"""Literal asymmetric port-two owner routing on the fixed native geometry."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import zip_longest
from pathlib import Path
import gzip,json


def need(ok,why):
    if not ok:raise AssertionError(why)


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();pg=a.repo/'research/moonshot-005-program'
    paths={'layout':pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
           'phase':Path(__file__).with_name('PHASE-CERTIFICATE.json')}
    pins={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
          'phase':'a806cc80a7bc7955fa07e04384707deb38200bac682424682e997f742dc5e278'}
    raw={k:gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes() for k,p in paths.items()}
    for k,v in raw.items():need(sha256(v).hexdigest()==pins[k],k+' pin')
    lay=json.loads(raw['layout']);phase=json.loads(raw['phase']);selected=set(phase['full_early_planes']);large={int(h):j for h,j in phase['large_early_donor_at_partial_plane'].items()}
    roots=lay['root_table'];Hs=list(map(set,lay['A2']));Ds=list(map(set,lay['D4']));dual=lay['dual_D4']
    native=set(range(111));full_adj=[{j for j,v in enumerate(roots) if sum(x*y for x,y in zip(u,v))==0} for u in roots]
    need(all(dual[dual[d]]==d and all(Ds[dual[d]]<=full_adj[j] for j in Ds[d]) for d in range(3150)),'actual dual middle charts')
    hd=[[d for d,D in enumerate(Ds) if H<=D] for H in Hs]
    need(all(len(ds)==45 for ds in hd),'forty-five actual flags per plane')
    dh=[set() for _ in Ds]
    for h,ds in enumerate(hd):
        for d in ds:dh[d].add(h)
    need(all(len(hs)==16 for hs in dh),'sixteen planes per middle')
    leftX=[[] for _ in Ds];leftY=[[] for _ in Ds];rightX=[[] for _ in Ds];rightY=[[] for _ in Ds]
    Xid=Counter();Yid=Counter();params={};inlets={};line_origin_variation=False
    need(len(selected)==65 and all(len(Hs[h]&native)==3 for h in selected),'sixty-five actual full early planes')
    need(set(large)=={h for h,H in enumerate(Hs) if len(H&native)==2},'every two-native plane has exactly one designated donor')
    need(all(j in Hs[h]&native for h,j in large.items()),'large early donor is an actual owner on its plane')
    for h,H in enumerate(Hs):
        donors=sorted(H&native);m=len(donors)
        early=2 if h in selected else 1 if m else 0;late=2-early
        p=45 if m==1 else 30
        quotas={j:45 if m==1 else 30 if h in selected or large.get(h)==j else 15 for j in donors}
        need(sum(quotas.values())==45*early,'local genuine early source margin')
        need(all(15*early<=v<=p for v in quotas.values()),'each donor can fill the visible early target')
        params[h]={'m':m,'early':early,'late':late,'source_quota':p,'donor_early':quotas}
        xe=[];ye=[];xx=[];yy=[]
        for j in donors:
            for _ in range(quotas[j]):
                xe.append((j,Xid[j]));Xid[j]+=1
                yy.append((j,Yid[j]));Yid[j]+=1
            ye.extend([j]*(p-quotas[j]));xx.extend([j]*(p-quotas[j]))
        direct=90-m*p
        need(direct>=0,'nonnegative actual direct birth/closure')
        ye.extend([None]*direct);xx.extend([None]*direct)
        need(len(xe)==len(yy)==45*early and len(ye)==len(xx)==45*late,'integral local ownership margins')
        for at,d in enumerate(hd[h]):
            for owner in xe[at*early:(at+1)*early]:leftX[d].append((owner,h))
            for j in ye[at*late:(at+1)*late]:leftY[d].append((j,h))
        rd=sorted(dual[d] for d in hd[h])
        for at,d in enumerate(rd):
            for owner in yy[at*early:(at+1)*early]:rightY[d].append((owner,h))
            for j in xx[at*late:(at+1)*late]:rightX[d].append((j,h))
        inlets[h]={'donors':donors,'early_quotas':quotas,'full_source_quota':p,'direct_late':direct}
        if m==2:line_origin_variation|=len(set(quotas.values()))==2
    need(set(Xid)==native and set(Xid.values())=={480} and Xid==Yid,'all real original banks')
    need(line_origin_variation,'nonuniform owner assignment is actually required')
    a.out.mkdir(parents=True,exist_ok=True)
    route_hash=sha256();moves=Counter();starts=Counter();ends=Counter();seenX=set();seenY=set()
    left_flags=Counter();right_flags=Counter();middle_birth=middle_close=0
    route_count=0
    # Each row stores [kind,native_owner,owner_coordinate,left_H,D,right_K,left_native,right_native].
    # Null left_H means Y begins at D. Null right_K means X closes from D.
    with gzip.GzipFile(filename=str(a.out/'ROUTES.jsonl.gz'),mode='wb',mtime=0) as out:
        def emit(kind,owner,h,d,k,left_native,right_native):
            nonlocal route_count
            native_owner,coordinate=owner
            row=[kind,native_owner,coordinate,h,d,k,left_native,right_native]
            payload=(json.dumps(row,separators=(',',':'))+'\n').encode();out.write(payload);route_hash.update(payload)
            route_count+=1
            if kind=='X':
                need(h is not None and left_native==native_owner,'real X starts at its native line')
                need(owner not in seenX,'X original used exactly once');seenX.add(owner)
                ranks=[1,2,4];starts[native_owner]+=1
                need(left_native in Hs[h] and Hs[h]<=Ds[d],'actual X left chain')
                if k is not None:
                    ranks.append(6);need(Hs[k]<=Ds[dual[d]],'actual X right dual chain')
                    if right_native is not None:
                        ranks.append(7);need(right_native in Hs[k] and right_native<111,'actual X facet visit')
                else:need(right_native is None,'short X closure')
                ranks.append(8)
            else:
                need(k is not None and right_native==native_owner,'real Y ends at its native facet')
                need(owner not in seenY,'Y original used exactly once');seenY.add(owner);ends[native_owner]+=1
                ranks=[0]
                if h is not None:
                    if left_native is not None:
                        ranks.append(1);need(left_native in Hs[h] and left_native<111,'actual late source visit')
                    ranks.append(2);need(Hs[h]<=Ds[d],'actual Y left chain')
                else:need(left_native is None,'middle Y birth has no earlier visit')
                ranks.extend([4,6,7]);need(Hs[k]<=Ds[dual[d]] and right_native in Hs[k],'actual Y right chain')
            need(sum(v-u for u,v in zip(ranks,ranks[1:]))==7,'every real original has total public rank rise seven')
            moves.update(v-u for u,v in zip(ranks,ranks[1:]))
            if h is not None:left_flags[h,d,kind]+=1
            if k is not None:right_flags[d,k,kind]+=1
        for d in range(3150):
            lx,ly,rx,ry=leftX[d],leftY[d],rightX[d],rightY[d]
            need(len(lx)+len(ly)==len(rx)+len(ry)==32,'all sixteen two-lane middle flags')
            surplus=len(lx)-len(rx)
            need(surplus==len(ry)-len(ly)>=0,'integer middle causal reserve')
            middle_close+=surplus;middle_birth+=surplus
            for p,(owner,h) in enumerate(lx):
                i,k=rx[p] if p<len(rx) else (None,None)
                emit('X',owner,h,d,k,owner[0],i)
            for p,(owner,k) in enumerate(ry):
                j,h=ly[p] if p<len(ly) else (None,None)
                emit('Y',owner,h,d,k,j,owner[0])
    need(route_count==106560 and len(seenX)==len(seenY)==53280,'complete unique public owner inventory')
    need(starts==ends==Counter({j:480 for j in range(111)}),'native source/terminal inventories')
    need(middle_birth==middle_close==5760,'all real short middle births and closures')
    for h,ds in enumerate(hd):
        p=params[h]
        for d in ds:
            need(left_flags[h,d,'X']==p['early'] and left_flags[h,d,'Y']==p['late'],'every left phase flag exact')
            dd=dual[d]
            need(right_flags[dd,h,'Y']==p['early'] and right_flags[dd,h,'X']==p['late'],'every right phase flag exact')
    need(moves==Counter({1:267060,2:216390,4:11520}),'literal compressed movement histogram')
    # Symmetric source division at a partial plane would ask for 45/2 originals.
    bad_uniform=min(large)
    need(F(45,2).denominator!=1,'fractional source-owner shortcut rejected')
    # All local inequalities needed by the foreign integral path witness.
    pair_count=0
    for i in range(111):
        for j in sorted(full_adj[i]&native):
            hs=[h for h,H in enumerate(Hs) if j in H and H<=full_adj[i]]
            ks=[k for k,K in enumerate(Hs) if i in K and K<=full_adj[j]]
            need(len(hs)==len(ks)==16,'sixteen real source and terminal branches')
            for h in hs:
                p=params[h];need(p['source_quota']>=30 and p['donor_early'][j]>=15*p['early'],'left integral port/source capacity')
                need(sum(Ds[d]<=full_adj[i] for d in hd[h])==15,'fifteen visible left flags')
            for k in ks:
                p=params[k];need(p['source_quota']>=30 and p['donor_early'][i]>=15*p['early'],'right integral port/source capacity')
            middles={d for h in hs for d in hd[h] if Ds[d]<=full_adj[i]}
            need(len(middles)==60,'sixty actual middle charts')
            for d in middles:
                lh=[h for h in hs if h in dh[d]]
                rk=[k for k in ks if Hs[k]<=Ds[dual[d]]]
                need(len(lh)==len(rk)==4,'four true branches per middle side')
                need(sum(params[h]['early'] for h in lh)>=sum(params[k]['late'] for k in rk),'integral early-to-early middle matching')
            pair_count+=1
    need(pair_count==6470,'every foreign pair path-count certificate')
    degree=10*(6470+2*111)*480
    need(degree==32121600 and degree<2**25,'joint determinant field degree')
    invoice={}
    for w in [4,25,26,28]:
        M=111*480*w;C=9*480*w
        invoice[w]={'field_degree':w,'rank_only_field_existence_proved_here':w>=25,'fixed_GF16_coefficients_embed':w%4==0,
                    'M':M,'C':C,'ADD':17*M*M+50*M+111*C,'INIT':5*M+C,'dirty_CLEAR':5*M+C,
                    'peak_public_and_auxiliary':7*M+C,
                    'MOVE':{str(g):v*w for g,v in {**moves,8:9*480}.items()}}
    result={'status':'PASS_LITERAL_ASYMMETRIC_PORT_TWO_ATLAS','bank':480,'ordinary_quotient':30,
            'port':2,'source_pins':pins,'public_original_routes':route_count,
            'X_originals':len(seenX),'Y_originals':len(seenY),'middle_X_closures':middle_close,'middle_Y_births':middle_birth,
            'public_MOVE_field_counts':dict(moves),'canonical_gap8_field_count':4320,
            'normalized_profile':{'1':'4451/8','2':'7213/16','4':'24','8':'9'},
            'routes_uncompressed_sha256':route_hash.hexdigest(),'all_foreign_path_count_checks':pair_count,
            'rank_only_degree_bound':degree,'rank_only_field_degree':25,'finite_word_invoices':invoice,
            'uniform_fractional_owner_negative_control_plane':bad_uniform,
            'complete_native_map_constructed':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (a.out/'PLANE-PHASES.json').write_text(json.dumps(params,sort_keys=True,separators=(',',':'))+'\n')
    print(result['status']);print(json.dumps({k:v for k,v in result.items() if k not in ['finite_word_invoices','source_pins']}))


if __name__=='__main__':main()
