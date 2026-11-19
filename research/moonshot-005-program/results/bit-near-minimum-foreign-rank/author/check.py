#!/usr/bin/env python3
"""Verify native seed coverage and exact LR duals without an optimizer."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

def require(ok,reason):
    if not ok:raise ValueError(reason)

def movement_enclosure():
    """Prove the needed price comparison using integer powers only."""
    scale=10**12
    powers={}
    def power(n):
        if n not in powers:
            target=n**199*scale**200
            low,high=0,n*scale+1
            while high-low>1:
                middle=(low+high)//2
                if middle**200<=target:low=middle
                else:high=middle
            require(low**200<=target<(low+1)**200,'integer root enclosure')
            powers[n]=(Q(low,scale),Q(low if low**200==target else low+1,scale))
        return powers[n]
    def interval(profile):
        low=high=Q(0)
        for n,c in profile.items():
            a,b=power(n)
            low+=c*(a if c>=0 else b)
            high+=c*(b if c>=0 else a)
        return low,high
    def add(profile,n,c):profile[n]=profile.get(n,Q(0))+c
    # Native retained limiting budget, after the ordinary n/h profiles cancel.
    limit={127:Q(37,6),64:Q(37,3),1:Q(-37,3)}
    for j in range(1,9):
        add(limit,1+7*j,Q(37,3));add(limit,7*j,Q(-37,3))
    room=dict(limit)
    for n,c in {1:Q(4451,8),2:Q(7213,16),4:Q(24),8:Q(9)}.items():add(room,n,-c)
    room_bounds=interval(room)
    require(0<room_bounds[0]<=room_bounds[1]<Q(279,1000),'limiting room below 0.279')
    eighth=power(8)
    require(8**199>7**200 and Q(7,6)>Q(279,1000),'late-only penalty exceeds room')
    threshold=(5760*room_bounds[0]/eighth[1],5760*room_bounds[1]/eighth[0])
    require(202<threshold[0]<=threshold[1]<203,'exact integer excess ceiling at b5760')
    # The finite paired budget is below its limit: B_m=B_inf+(T_2-P_2)/(36(m-1)).
    n={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10}
    h={2:1,4:25,6:1,8:410}
    difference={}
    for gap,c in h.items():add(difference,gap,36*c)
    for gap,c in n.items():add(difference,gap,-36*c)
    add(difference,127,222);add(difference,1,-444)
    for j in range(1,10):add(difference,1+7*j,444)
    for j in range(1,9):add(difference,7*j,-444)
    finite_numerator=interval(difference)
    require(finite_numerator[1]<0,'every finite paired budget below limit')
    return {'scale':scale,'exponent':'199/200','room_interval':list(map(str,room_bounds)),
            'excess_ceiling_interval_at_b5760':list(map(str,threshold)),
            'finite_budget_offset_numerator_T2_minus_P2':list(map(str,finite_numerator)),
            'postline_cost_lower_bound':'7/6','room_upper_bound':'279/1000',
            'postline_gate_excludes_every_even_m_ge_2':True,
            'verification':'integer 200th powers; no floating point or numerical optimizer'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);pg=a.repo/'research/moonshot-005-program'
    lp=pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';layout_raw=gzip.decompress(lp.read_bytes())
    require(hashlib.sha256(layout_raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    fp=pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json';factor_raw=fp.read_bytes()
    require(hashlib.sha256(factor_raw).hexdigest()=='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7','factor pin')
    np=pg/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';native_raw=np.read_bytes()
    require(hashlib.sha256(native_raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native recovery pin')
    layout=json.loads(layout_raw);factor=dict(json.loads(factor_raw)['factors']);roots=layout['root_table'];planes=[set(H) for H in layout['A2']]
    require(roots[:111]==json.loads(native_raw)['native_roots'],'native indices agree with authenticated recovery')
    full_adj=[{j for j,s in enumerate(roots) if sum(x*y for x,y in zip(r,s))==0} for r in roots]
    native=set(range(111));adj=[S&native for S in full_adj[:111]];all_pairs={(i,j) for i in range(111) for j in range(i+1,111) if j in adj[i]}
    require(len(all_pairs)==3235,'foreign pairs')
    payload=gzip.decompress(Path(__file__).with_name('CERTIFICATE.json.gz').read_bytes());cert=json.loads(payload)
    frame_cache={}
    def seed(frame):
        frame=tuple(frame)
        if frame in frame_cache:return frame_cache[frame]
        require(len(frame)==8 and len(set(frame))==8 and set(frame)<=native,'eight real points')
        require(all(j not in adj[i] for i,j in itertools.combinations(frame,2)),'point noncontacts')
        edge_roles=[]
        for j in range(111):
            e=tuple(i for i,v in enumerate(frame) if v in adj[j])
            if len(e)==2:edge_roles.append((j,e))
        graph={e for _,e in edge_roles};require(len(graph)==len(edge_roles),'unique edge roles')
        for j,e in edge_roles:
            for k,f in edge_roles:
                if j!=k and set(e)&set(f):require(k not in adj[j],'shared endpoint noncontact')
        frame_cache[frame]=edge_roles,graph;return edge_roles,graph
    best={};witness={};counts=Counter()
    for frame in cert['frames']:
        roles,graph=seed(frame)
        for order,constant in [(6,Q(7,2)),(7,Q(3))]:
            cliques=[C for C in itertools.combinations(range(8),order) if all(e in graph for e in itertools.combinations(C,2))]
            good={e for C in cliques for e in itertools.combinations(C,2)}
            for j,e in roles:
                if e not in good:continue
                C=next(C for C in cliques if set(e)<=set(C))
                for k in e:
                    pair=tuple(sorted((frame[k],j)))
                    if constant<best.get(pair,Q(100)):
                        best[pair]=constant;witness[pair]={'frame':frame,'clique':C,'point_role':frame[k],'edge_role':j,'coefficient':str(constant)}
        counts[len(roles)]+=1
    residual=[];bad_dual_rejected=False
    for d in cert['residual_duals']:
        frame=d['frame'];roles,graph=seed(frame);variables=[(e,i) for j,e in roles for i in e]
        target_edge=next(e for j,e in roles if j==d['edge_role']);point_index=frame.index(d['point_role']);require(point_index in target_edge,'target contact')
        other=next(i for i in target_edge if i!=point_index);target=(target_edge,other)
        require(d['target_directed_incidence']==[list(target_edge),other],'opposite-endpoint defect index')
        A=[[int(j==i)-2*int(f==e) for f,j in variables] for e,i in variables]
        objective=[int(v==target) for v in variables];lam=list(map(Q,d['dual_weights']))
        require(len(lam)==len(variables) and min(lam)>=0,'nonnegative dual')
        lhs=[sum(lam[i]*A[i][j] for i in range(len(variables))) for j in range(len(variables))]
        require(all(x>=y for x,y in zip(lhs,objective)),'exact dual feasibility')
        value=sum(lam);require(value==Q(d['bound']) and value<=Q(9,2),'dual objective bound')
        pair=tuple(sorted((d['point_role'],d['edge_role'])));require(list(pair)==d['pair'],'pair identity')
        if value<best.get(pair,Q(100)):
            best[pair]=value;witness[pair]={'residual_dual':d,'coefficient':str(value)}
        residual.append({'pair':pair,'coefficient':str(value),'dual_support':sum(x>0 for x in lam)})
        for i,x in enumerate(lam):
            if x and any(lhs[j]-x*A[i][j]<objective[j] for j in range(len(variables))):bad_dual_rejected=True;break
    require(set(best)==all_pairs,'every native foreign pair certified')
    require(max(best.values())<=Q(9,2),'uniform 9h/2 bound')
    # Exact averaged LR proofs and matching relaxation controls.
    # K6 variables x,y,a,b,c,d,e; rows A,B,C,D in the written proof.
    rows6=[(1,0,2,-2,0,0,0),(0,0,0,1,0,1,-1),(0,0,0,1,-2,-1,3),(0,1,0,0,2,-2,0)]
    dual6=[Q(1),Q(3,2),Q(1,2),Q(1,2)]
    require([sum(w*r[j] for w,r in zip(dual6,rows6)) for j in range(7)]==[1,Q(1,2),2,0,0,0,0],'K6 averaged dual')
    require(sum(dual6)==Q(7,2),'K6 objective')
    sharp6=[Q(7,2),Q(0),Q(0),Q(5,4),Q(1,2),Q(0),Q(1,4)]
    require(all(sum(x*y for x,y in zip(row,sharp6))==1 for row in rows6),'K6 relaxation sharpness')
    # K7: x+3a-2b<=h and b+d<=h imply x+3a+2d<=3h.
    rows7=[(1,3,-2,0),(0,0,1,1)];dual7=[Q(1),Q(2)]
    require([sum(w*r[j] for w,r in zip(dual7,rows7)) for j in range(4)]==[1,3,0,2] and sum(dual7)==3,'K7 averaged dual')
    for n,values in [(6,sharp6),(7,[Q(3),Q(0),Q(0),Q(1),Q(0),Q(0),Q(0)])]:
        x,y,av,bv,cv,dv,ev=values;edges=list(itertools.combinations(range(n),2));g={}
        for u,v in edges:
            if (u,v)==(0,1):g[u,v,u],g[u,v,v]=x,y
            elif u==0:g[u,v,u],g[u,v,v]=av,bv
            elif u==1:g[u,v,u],g[u,v,v]=cv,dv
            else:g[u,v,u]=g[u,v,v]=ev
        G={i:sum(z for (u,v,j),z in g.items() if j==i) for i in range(n)}
        require(all(G[i]<=1+2*(g[u,v,u]+g[u,v,v]) for u,v in edges for i in (u,v)),'full LR relaxation sharpness')
    critical_frame=cert['critical_frame'];roles,graph=seed(critical_frame);C=cert['critical_seven_clique']
    require(len(C)==7 and all(e in graph for e in itertools.combinations(C,2)),'critical complete K7')
    require(any(j==5 and critical_frame[k]==77 and set(e)<=set(C) for j,e in roles for k in e),'critical5,77 block')
    source_x=[]
    for h,H in enumerate(planes):
        m=len(H&native);source_x.append(12//m+factor.get(h,0) if m else 0)
    cut_rows=[]
    for i in range(111):
        for j in sorted(adj[i]):
            E=45*sum(source_x[h] for h,H in enumerate(planes) if j in H and H<=full_adj[i]);c=best[tuple(sorted((i,j)))];floor=(c*202).__floor__()
            cut_rows.append({'receiver':i,'donor':j,'early_capacity':E,'coefficient':str(c),'foreign_rank_floor_at_h202':5760-floor,'late_dimension_floor_at_h202':5760-floor-E,'minimum_excess_for_postline_gate':(Q(5760-E)/c).__ceil__()})
    require(len(cut_rows)==6470 and min(r['early_capacity'] for r in cut_rows)==2880 and max(r['early_capacity'] for r in cut_rows)==3600,'source cut census')
    critical=next(r for r in cut_rows if r['receiver']==5 and r['donor']==77)
    require(critical['early_capacity']==2880 and Q(critical['coefficient'])<=3,'critical b/2 source cut')
    require(critical['minimum_excess_for_postline_gate']>=960,'critical h>=b/6')
    minlate=min(r['late_dimension_floor_at_h202'] for r in cut_rows)
    require(minlate>0,'late taps necessary for all foreign pairs')
    require(bad_dual_rejected,'corrupted residual dual rejected')
    movement=movement_enclosure()
    result={'status':'PASS_NATIVE_NEAR_MINIMUM_FOREIGN_RANK','certificate_uncompressed_sha256':hashlib.sha256(payload).hexdigest(),'native_pairs':3235,'directed_foreign_blocks':6470,'frames':len(cert['frames']),'frame_edge_count_histogram':dict(sorted(counts.items())),'best_coefficient_histogram':dict(Counter(str(c) for c in best.values())),'uniform_foreign_rank_floor':'b-floor(9h/2)','uniform_floor_at_b5760_h202':4851,'minimum_certified_late_dimensions_at_h202':minlate,'maximum_postline_excess_floor':max(r['minimum_excess_for_postline_gate'] for r in cut_rows),'critical_pair':critical,'critical_frame':critical_frame,'critical_K7':C,'residual_duals':residual,'movement':movement,'negative_controls':{'corrupted_dual_rejected':bad_dual_rejected,'coefficient_below_7_over_2_excluded_by_relaxation_control':True},'scope':'Linear proper transfers and arbitrary-width fitting matrices; nonlinear return-bank messages allowed only through the separate fixed-code rank necessity. No new kappa.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'ALL-PAIR-CUTS.json.gz').write_bytes(gzip.compress((json.dumps(cut_rows,separators=(',',':'))+'\n').encode(),mtime=0))
    (a.out/'RATIONAL-MOVEMENT.json').write_text(json.dumps(movement,indent=2)+'\n')
    pins=[]
    for p in ['results/bit-saturated-star-rigidity/author/PROOF.md','results/bit-native-cycle-and-inlet-gates/author/PROOF.md','results/bit-all111-balanced-causal-atlas/author/BALANCED-PROOF.md']:
        pins.append({'path':'research/moonshot-005-program/'+p,'sha256':hashlib.sha256((pg/p).read_bytes()).hexdigest()})
    (a.out/'SOURCE-PINS.json').write_text(json.dumps({'baseline':cert['source_baseline'],'layout_uncompressed_sha256':hashlib.sha256(layout_raw).hexdigest(),'factor_sha256':hashlib.sha256(factor_raw).hexdigest(),'native_recovery_sha256':hashlib.sha256(native_raw).hexdigest(),'files':pins},indent=2)+'\n')
    print(result['status'], '6470 blocks; post-line-only h>=b/6')

if __name__=='__main__':main()
