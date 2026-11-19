#!/usr/bin/env python3
"""Independent native-frame and dual review; executes no author code."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip, json


def need(ok, why):
    if not ok: raise AssertionError(why)


def roots_movement():
    scale=10**9;cache={}
    def bracket(n):
        if n not in cache:
            v=n**199*scale**200;lo=0;hi=n*scale+1
            while hi-lo>1:
                m=(lo+hi)//2
                if m**200<=v:lo=m
                else:hi=m
            need(lo**200<=v<hi**200,'exact radical interval')
            cache[n]=(F(lo,scale),F(lo if lo**200==v else hi,scale))
        return cache[n]
    def value(profile):
        l=h=F(0)
        for n,c in profile.items():
            p,q=bracket(n);l+=c*(p if c>=0 else q);h+=c*(q if c>=0 else p)
        return [l,h]
    def combine(*terms):
        d=defaultdict(F)
        for coefficient,profile in terms:
            for n,c in profile.items():d[n]+=coefficient*c
        return d
    Q={1:F(4451,8),2:F(7213,16),4:F(24),8:F(9)}
    N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
    P2=combine((36,N),(1,{1:444}),*( (1,{7*j:444}) for j in range(1,9)))
    T2=combine((36,H),(1,{127:222}),*( (1,{1+7*j:444}) for j in range(1,10)))
    difference=combine((1,T2),(-1,P2))
    limit=combine((F(1,36),difference),(1,N),(-1,H))
    room=value(combine((1,limit),(-1,Q)));finite=value(difference)
    need(0<room[0]<=room[1]<F(279,1000),'room below .279')
    need(finite[1]<0,'finite paired allowance below limit')
    need(8**199>7**200 and F(7,6)>room[1],'early-only surcharge exceeds limit')
    b8=bracket(8);threshold=[5760*room[0]/b8[1],5760*room[1]/b8[0]]
    need(202<threshold[0]<=threshold[1]<203,'scaled excess threshold at base bank')
    return {'root_interval_scale':scale,'room':list(map(str,room)),
            'T2_minus_P2':list(map(str,finite)), 'base_excess_threshold':list(map(str,threshold)),
            'extra_movement_lower_bound':'7/6','excludes_all_even_m_ge_2':True}


def relaxation_control(n):
    edges=list(combinations(range(n),2));v={}
    vals=(F(7,2),F(0),F(0),F(5,4),F(1,2),F(0),F(1,4)) if n==6 else (F(3),F(0),F(0),F(1),F(0),F(0),F(0))
    x,y,a,b,c,d,e=vals
    for u,w in edges:
        p,q=(x,y) if u==0 and w==1 else (a,b) if u==0 else (c,d) if u==1 else (e,e)
        v[(u,w),u]=p;v[(u,w),w]=q
    sums={i:sum(z for (edge,j),z in v.items() if j==i) for i in range(n)}
    need(all(sums[i]<=1+2*(v[edge,edge[0]]+v[edge,edge[1]]) for edge,i in v),'every sharp-fixture LR inequality')
    need(v[((0,1),0)]== (F(7,2) if n==6 else F(3)),'sharp objective')
    # A smaller claimed coefficient fails this exact nonnegative relaxation point.
    need(v[((0,1),0)]> (F(17,5) if n==6 else F(29,10)),'coefficient corruption rejected')
    return {'order':n,'incidences':len(v),'objective':str(v[((0,1),0)])}


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();pg=a.repo/'research/moonshot-005-program'
    paths={'native':pg/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json',
           'layout':pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
           'factor':pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json'}
    pins={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
          'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
          'factor':'346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'}
    raw={k:gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes() for k,p in paths.items()}
    for k,v in raw.items():need(sha256(v).hexdigest()==pins[k],k+' source hash')
    native=json.loads(raw['native'])['native_roots'];layout=json.loads(raw['layout']);roots=layout['root_table']
    need(roots[:111]==native,'native role order agrees with direct source')
    def contact(u,v):return sum(x*y for x,y in zip(u,v))==0
    adj=[{j for j,v in enumerate(native) if contact(u,v)} for u in native]
    full_adj=[{j for j,v in enumerate(roots) if contact(u,v)} for u in native]
    pairs={tuple((i,j)) for i,j in combinations(range(111),2) if j in adj[i]}
    need(len(pairs)==3235 and all(i not in adj[i] for i in range(111)),'exact foreign support')
    craw=gzip.decompress((a.author/'CERTIFICATE.json.gz').read_bytes());cert=json.loads(craw)
    need(sha256(craw).hexdigest()=='e7015bd9e1111ec8d4c3ebaa30460d767b66ea1d7e8a33279b9f033c0053dc57','frozen native certificate')
    info={};hist=Counter();best={};covered_by_cliques=set()
    def inspect_frame(frame):
        key=tuple(frame)
        if key in info:return info[key]
        need(len(key)==8 and len(set(key))==8 and all(0<=v<111 for v in key),'eight distinct actual native points')
        need(all(v not in adj[u] for u,v in combinations(key,2)),'frame point noncontacts')
        roles={}
        for v in range(111):
            ends=tuple(k for k,u in enumerate(key) if u in adj[v])
            if len(ends)==2:roles[v]=ends
        need(len(set(roles.values()))==len(roles),'edge roles are unique')
        for u,v in combinations(roles,2):
            if set(roles[u])&set(roles[v]):need(v not in adj[u],'shared point edge roles are true noncontacts')
        info[key]=roles;return roles
    for frame in cert['frames']:
        roles=inspect_frame(frame);graph=set(roles.values());hist[len(roles)]+=1
        for n,c in [(6,F(7,2)),(7,F(3))]:
            for clique in combinations(range(8),n):
                ce=set(combinations(clique,2))
                if not ce<=graph:continue
                for role,ends in roles.items():
                    if ends not in ce:continue
                    for end in ends:
                        pair=tuple(sorted((role,frame[end])));need(pair in pairs,'clique bound applies to true contact')
                        best[pair]=min(best.get(pair,c),c);covered_by_cliques.add(pair)
    dual_checks=[];corrupted_rejected=0
    for d in cert['residual_duals']:
        frame=d['frame'];roles=inspect_frame(frame)
        variables=[(role,point) for role,ends in sorted(roles.items()) for point in ends]
        edge=d['edge_role'];point=frame.index(d['point_role']);ends=roles[edge]
        need(point in ends,'specified point meets specified edge')
        other=ends[0] if point==ends[1] else ends[1]
        need(d['target_directed_incidence']==[list(ends),other],'objective uses opposite endpoint')
        target=(edge,other);weights=list(map(F,d['dual_weights']))
        need(len(weights)==len(variables) and all(w>=0 for w in weights),'correct nonnegative dual dimensions')
        def coefficients(w):
            pointweight=defaultdict(F);edgeweight=defaultdict(F)
            for (role,end),z in zip(variables,w):pointweight[end]+=z;edgeweight[role]+=z
            return {v:pointweight[v[1]]-2*edgeweight[v[0]] for v in variables}
        lhs=coefficients(weights)
        need(all(z>=(1 if v==target else 0) for v,z in lhs.items()),'exact LR dual domination')
        bound=sum(weights);need(bound==F(d['bound']) and bound<=F(9,2),'dual objective')
        pair=tuple(sorted((d['point_role'],edge)));need(list(pair)==d['pair'] and pair in pairs,'native pair identity')
        best[pair]=min(best.get(pair,bound),bound)
        detected=False
        for k,z in enumerate(weights):
            if z==0:continue
            changed=weights.copy();changed[k]=0;bad=coefficients(changed)
            if any(t<(1 if v==target else 0) for v,t in bad.items()):detected=True;break
        need(detected,'removing an essential weight is detected');corrupted_rejected+=1
        dual_checks.append({'pair':list(pair),'opposite_endpoint':other,'bound':str(bound),'nonzero_weights':sum(w>0 for w in weights)})
    need(set(best)==pairs,'every true foreign pair covered')
    need(len(cert['frames'])==621 and max(best.values())==F(9,2),'full finite cover and uniform constant')
    factor=dict(json.loads(raw['factor'])['factors']);planes=list(map(set,layout['A2']));natives=set(range(111))
    x={h:12//len(H&natives)+factor.get(h,0) for h,H in enumerate(planes) if H&natives}
    need(all(45*sum(x[h] for h,H in enumerate(planes) if j in H)==5760 for j in range(111)),'all actual early donor-bank sizes')
    author_rows=json.loads(gzip.decompress((a.author/'output/ALL-PAIR-CUTS.json.gz').read_bytes()))
    author_by_pair={(z['receiver'],z['donor']):z for z in author_rows}
    cuts=[]
    for i in range(111):
        for j in sorted(adj[i]):
            visible=[h for h,H in enumerate(planes) if j in H and H<=full_adj[i]]
            need(len(visible)==16,'sixteen actual early source branches')
            E=45*sum(x[h] for h in visible);c=best[tuple(sorted((i,j)))];f=(202*c).__floor__()
            row={'receiver':i,'donor':j,'early_capacity':E,'coefficient':str(c),
                 'foreign_rank_floor_at_h202':5760-f,'late_dimension_floor_at_h202':5760-f-E,
                 'minimum_excess_for_postline_gate':(F(5760-E)/c).__ceil__()}
            need(author_by_pair[i,j]==row,'every literal directed source-cut row')
            cuts.append(row)
    need(len(cuts)==6470 and min(z['early_capacity'] for z in cuts)==2880 and max(z['early_capacity'] for z in cuts)==3600,'full source-cut range')
    need(min(z['late_dimension_floor_at_h202'] for z in cuts)==1554,'minimum additional late dimension')
    frame=cert['critical_frame'];roles=inspect_frame(frame);clique=cert['critical_seven_clique']
    need(frame==[9,30,37,46,52,77,92,101] and len(set(clique))==7,'critical actual frame')
    need(set(combinations(sorted(clique),2))<=set(roles.values()),'critical complete seven-point edge system')
    need(roles[5]==(0,5) and frame[5]==77,'critical point-edge contact')
    critical=next(z for z in cuts if z['receiver']==5 and z['donor']==77)
    need(critical['early_capacity']==2880 and critical['coefficient']=='3' and critical['minimum_excess_for_postline_gate']==960,'critical b/6 excess')
    result={'status':'PASS_INDEPENDENT_NEAR_MINIMUM_FOREIGN_REVIEW','native_pairs':3235,'directed_blocks':6470,
            'frames':621,'frame_edge_count_histogram':dict(sorted(hist.items())),
            'clique_covered_pairs':len(covered_by_cliques),'coefficient_histogram':dict(Counter(str(v) for v in best.values())),
            'residual_duals':dual_checks,'all_eight_corrupted_duals_rejected':corrupted_rejected==8,
            'relaxation_controls':[relaxation_control(6),relaxation_control(7)],
            'critical_pair':critical,'minimum_additional_late_dimensions':1554,
            'movement':roots_movement(),'source_pins':pins,
            'certificate_uncompressed_sha256':sha256(craw).hexdigest(),
            'author_hashes':{name:sha256((a.author/name).read_bytes()).hexdigest() for name in ['PROOF.md','check.py','output/RESULT.json']},
            'author_code_imported_or_executed':False,'nonlinear_proper_transfer_claim':False,
            'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print('621 frames; 8 exact residual duals; 6470 directed cuts; h >= b/6.')


if __name__=='__main__':main()
