#!/usr/bin/env python3
"""Compile overlapping native receiver groups using chronological taps on nested charts."""
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
from importlib.util import module_from_spec,spec_from_file_location
from pathlib import Path
import json

CORE=frozenset((1,3,73,76,77,80))
EXTRA=frozenset((56,100))
NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'


def require(ok,message):
    if not ok:raise ValueError(message)


def order(rows):return sorted(rows,key=lambda s:(-len(s),tuple(sorted(s))))


def chain_cover(rows):
    elems=order(set(rows));match={}
    def augment(u,seen):
        for v in elems:
            if v<u and v not in seen:
                seen.add(v)
                if v not in match or augment(match[v],seen):match[v]=u;return True
        return False
    for u in elems:augment(u,set())
    nxt={u:v for v,u in match.items()};out=[]
    for u in elems:
        if u in match:continue
        path=[u]
        while path[-1] in nxt:path.append(nxt[path[-1]])
        out.append(path)
    require(len({v for path in out for v in path})==len(elems),'chain coverage')
    return out


def compile_word(R,util,extra=EXTRA):
    active=CORE|extra;G=defaultdict(list);orig={};nodes={}
    for j,r in enumerate(R):
        w=frozenset(i for i in active if util.dot(r,R[i])==0);G[w].append(j);orig[j]=w
    require(not any(CORE<w<active for w in G),'old common group admits exactly two parts')
    require(all(w&CORE for w in G),'positive core signatures')
    def site(w):
        if len(w)==1:return 'F'+str(next(iter(w)))
        c='C_'+'_'.join(map(str,sorted(w)));nodes[c]={'kind':'kernel','normals':sorted(w)};return c
    charts={'zero':{'kind':'zero'},'Hub':{'kind':'ambient'}}
    for j in range(len(R)):
        charts[f'L{j}']={'kind':'line','role':j};charts[f'F{j}']={'kind':'kernel','normals':[j]}
    opers=[];tags=[];owners=[];receivers=defaultdict(lambda:defaultdict(list));sites=[];loc={f'X{j}':f'L{j}' for j in range(len(R))}
    def emit(tag,*args):opers.append(list(args));tags.append(tag)
    def xmove(tag,j,c):
        name=f'X{j}'
        if loc[name]!=c:emit(tag,'MOVE',name,c);loc[name]=c
    def cache(tag,name,chart,src):
        emit(tag+'_birth','INIT',name,chart);owners.append(name)
        for q in src:emit(tag+'_capture','ADD',q,name)
    def deliver(tag,name,chart,src,targets):
        cache(tag,name,chart,src)
        for i in targets:receivers[i][chart].append(name)
    common=G[active];old_common_only=G[CORE]
    cover={i:chain_cover(w for w in G if i in w and w!=active) for i in sorted(extra)}
    need=sum(len(ch)-1 for ch in cover.values());require(need<=len(common),'common native physical carrier reservoir')
    h4=site(active);h5=site(CORE)
    for j in common:xmove('deep_common_gather',j,h4)
    deliver('deep_common','COMMON_DEEP',h4,[f'X{j}' for j in common],active)
    masks=iter(common);tracks=[];tap_users=defaultdict(list)
    for i,chains in cover.items():
        # Reserve one actual Y route; each other disjoint track uses a physical original X.
        for k,chain in enumerate(chains):
            q=None if k==0 else next(masks)
            if q is not None:
                deliver('outer_mask',f'MASK_OUTER_{q}',h4,[f'X{q}'],[i])
            tracks.append({'receiver':i,'carrier_role':q,'sites':[sorted(w) for w in chain]})
            for w in chain:tap_users[w].append((i,q))
    used_q={tr['carrier_role'] for tr in tracks if tr['carrier_role'] is not None}
    for j in common:
        if j not in used_q:xmove('deep_raw_release',j,'Hub')
    for w in order(tap_users):
        c=site(w);ds=G[w]
        for j in ds:xmove('overlap_donor_visit',j,c)
        for i,q in tap_users[w]:
            if q is not None:xmove('outer_track_visit',q,c)
        name='TAP_'+c
        deliver('overlap_tap',name,c,[f'X{j}' for j in ds],[i for i,q in tap_users[w] if q is None])
        for i,q in tap_users[w]:
            if q is not None:emit('outer_track_add','ADD',name,f'X{q}')
        sites.append({'signature':sorted(w),'donors':ds,'tap':name,'readers':tap_users[w]})
    for tr in tracks:
        q=tr['carrier_role'];i=tr['receiver']
        if q is not None:
            c=f'F{i}';xmove('outer_terminal_visit',q,c)
            deliver('outer_terminal',f'OUT_{q}_{i}',c,[f'X{q}'],[i]);xmove('outer_release',q,'Hub')
    group=defaultdict(list)
    for j,w in orig.items():
        if w!=active:group[w&CORE].append(j)
    mixed=sorted((tuple(sorted(u)) for u in group if 1<len(u)<len(CORE)))
    anchors={i:frozenset(u) for i,u in util.assignment(mixed,tuple(sorted(CORE))).items()}
    jobs={}; free=iter(old_common_only)
    for u in map(frozenset,mixed):
        pr=[i for i in sorted(u) if anchors[i]!=u]
        for i in pr[1:]:jobs[next(free)]=(u,i)
    require(len(jobs)==5 and len(old_common_only)>=len(jobs),'old common-only relay supply')
    for j in old_common_only:xmove('old_common_gather',j,h5)
    deliver('old_common','COMMON_OLD_ONLY',h5,[f'X{j}' for j in old_common_only],CORE)
    for j in old_common_only:
        if j in jobs:
            u,i=jobs[j];deliver('core_mask',f'MASK_CORE_{j}',h5,[f'X{j}'],[i]);xmove('core_mask_carrier_visit',j,site(u))
        else:xmove('old_common_release',j,'Hub')
    inv=[]
    for u,ds in sorted(group.items(),key=lambda p:tuple(sorted(p[0]))):
        if u==CORE:continue
        c=site(u)
        for j in ds:xmove('core_regroup',j,c)
        if len(u)==1:
            deliver('private','PRIVATE_'+c,c,[f'X{j}' for j in ds],u)
            for j in ds:xmove('core_private_release',j,'Hub')
            continue
        p=ds[0]; A=[i for i in sorted(u) if anchors[i]==u];pr=[i for i in sorted(u) if i not in A]
        rel=[(q,i) for q,(U,i) in jobs.items() if U==u]
        intra=[(j,p) for j in ds[1:]]+[(p,q) for q,i in rel]
        for j,k in intra:emit('core_recode','ADD',f'X{j}',f'X{k}')
        inv.extend(intra[::-1]);selected={p:pr[0],**dict(rel)}
        if A:deliver('core_anchor','CORE_'+c,c,[f'X{p}'],A)
        for j in ds+[q for q,i in rel]:
            if j in selected:
                i=selected[j];z=f'F{i}';xmove('core_terminal_visit',j,z)
                deliver('core_terminal',f'END_{j}_{i}',z,[f'X{j}'],[i])
            xmove('core_release',j,'Hub')
    for j,k in inv:emit('core_inverse','ADD',f'X{j}',f'X{k}')
    for tr in tracks:
        q=tr['carrier_role']
        if q is None:continue
        for w in tr['sites']:
            for j in G[frozenset(w)]:emit('outer_inverse','ADD',f'X{j}',f'X{q}')
    cuts={'source_restored':len(opers)};K,decomp=util.canonical(R)
    for i in util.CANON:
        cache('canonical',f'K{i}','Hub',[f'X{j}' for j in range(len(R)) if K[i]>>j&1]);emit('canonical_descent','MOVE',f'K{i}','zero')
    cuts['canonical_at_ground']=len(opers)
    for i in sorted(active):
        for k in decomp[i]:emit('canonical_preload','ADD',f'K{k}',f'Y{i}')
    for i in range(len(R)):
        route=[]
        if i in CORE:route=[h4,h5,site(anchors[i])]
        elif i in extra:route=[h4]+[site(w) for w in cover[i][0]]
        route.append(f'F{i}')
        require(set(receivers[i])<=set(route),'all required physical cache visits')
        for c in route:
            emit('receiver_route','MOVE',f'Y{i}',c)
            for n in receivers[i][c]:emit('physical_cache_read','ADD',n,f'Y{i}')
    cuts['before_retirement']=len(opers)
    for n in owners:emit('retire','CLEAR',n)
    return {'schema':'two-level-overlapping-signature-network-v1','native_sha256':NATIVE_SHA,
            'all_completed_roles':sorted(active),'core_roles':sorted(CORE),'outer_roles':sorted(extra),
            'common_mask_originals':sorted(used_q),'old_common_mask_originals':sorted(jobs),'tracks':tracks,
            'tap_sites':sites,'charts':charts|nodes,'milestones':cuts,'operations':opers,'operation_tags':tags}


def main():
    p=ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--utility',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--single',action='store_true');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=a.native.read_bytes();require(sha256(raw).hexdigest()==NATIVE_SHA,'native source pin');require(sha256(a.utility.read_bytes()).hexdigest()=='78454a0967439b113a94214831bfa1facbe9f17523a42b0d1a173786c51c771f','utility source pin');R=json.loads(raw)['native_roots'];mod=spec_from_file_location('source_utility',a.utility);u=module_from_spec(mod);mod.loader.exec_module(u)
    ext=frozenset((56,)) if a.single else EXTRA;w=compile_word(R,u,ext);u.write(a.out/'WORD.json',w);g=u.geometry_map(w,R);r=u.replay(w,R,g)
    q=u.price(r['movement_profile']);c={127:37,64:74,1:-74}
    for j in range(1,9):c[1+7*j]=c.get(1+7*j,0)+74;c[7*j]=c.get(7*j,0)-74
    cap=tuple(x/6 for x in u.price(c));room=(cap[0]-q[1],cap[1]-q[0]);require(room[0]>0,'limiting allowance')
    ctr=[]
    for tag in ['deep_common_capture','outer_mask_capture','overlap_donor_visit','outer_track_visit','overlap_tap_capture','outer_track_add','outer_terminal_capture','old_common_capture','core_recode','core_mask_capture','core_inverse','outer_inverse','canonical_capture','canonical_descent','canonical_preload','receiver_route','physical_cache_read','retire']:
        k=w['operation_tags'].index(tag)
        try:u.replay(w,R,g,omit=k)
        except (ValueError,KeyError) as e:ctr.append([tag,k,str(e)])
        else:raise ValueError('missed negative control '+tag)
    ans={'status':'PASS_LAYERED_OVERLAPPING_SOURCE','native_sha256':NATIVE_SHA,'word_sha256':sha256((a.out/'WORD.json').read_bytes()).hexdigest(),
         'all_completed_roles':w['all_completed_roles'],'unused_Y_pure':111-len(w['all_completed_roles']),
         'number_outer_raw_carriers':len(w['common_mask_originals']),'ordinary_counts_and_routes':r,
         'moment_at_199_over_200':u.iv(q),'necessary_limiting_room':u.iv(room),'omission_controls':ctr,'complete_supplier':False,'new_complete_kappa':False}
    u.write(a.out/'RESULT.json',ans);print(ans['status'],ans['word_sha256'],r['counts'],r['movement_profile'],u.iv(q)['decimal'],u.iv(room)['decimal'])

if __name__=='__main__':main()
