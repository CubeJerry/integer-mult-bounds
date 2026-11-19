#!/usr/bin/env python3
"""Separate whole-owner engine reused and generalized from B's tile/row reviews."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from hashlib import sha256
import gzip,json
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'}
STAGES=['X_NATIVE','X_H','X_D','X_K','X_F','HUB_RESTORE','GROUND_PRELOAD','Y_LINE','Y_H','Y_D','Y_K','Y_F']
CHARTS=['L','H','D','K','F','Hub','Ground','L','H','D','K','F']
F=5;BANK=480;N=111;PF=2*N*BANK;XB=N*BANK*F;PB=PF*F

def load(path,key,jsonl=False):
    raw=gzip.decompress(path.read_bytes());assert sha256(raw).hexdigest()==PINS[key]
    return[json.loads(x)for x in raw.splitlines()]if jsonl else json.loads(raw)

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--word-pin',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results';L=load(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout');routes=load(base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','routes',True)
    raw=gzip.decompress(a.word.read_bytes());assert sha256(raw).hexdigest()==a.word_pin;W=json.loads(raw)
    assert W['bank_fields']==BANK and W['field_bits']==F and W['public_route_pin']==PINS['routes']and W['field_modulus']==0x25
    roots=L['root_table'];H=list(map(set,L['A2']));D=list(map(set,L['D4']));orth=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots]
    route={};movement=Counter();perx=Counter();pery=Counter()
    for r in routes:
        kind,j,c,h,d,k,left,right=r
        assert kind in ['X','Y']and 0<=j<N and 0<=c<BANK and 0<=d<len(D)
        f=(0 if kind=='X'else N*BANK)+j*BANK+c;assert f not in route;route[f]=r
        if h is not None:assert H[h]<=D[d]
        if k is not None:assert all(y in orth[x]for x in D[d]for y in H[k])
        if left is not None:assert h is not None and left in H[h]
        if right is not None:assert k is not None and right in H[k]
        if kind=='X':
            assert left==j and h is not None;perx[j]+=1
            ranks=[1,2,4]+([6]if k is not None else[])+([7]if right is not None else[])+[8]
        else:
            assert right==j and k is not None;pery[j]+=1
            ranks=[0]+([1]if left is not None else[])+([2]if h is not None else[])+[4,6,7]
        assert all(t>s for s,t in zip(ranks,ranks[1:]));movement.update(t-s for s,t in zip(ranks,ranks[1:]))
    assert len(route)==PF and set(perx.values())==set(pery.values())=={BANK}and len(perx)==len(pery)==N
    assert dict(movement)=={1:267060,2:216390,4:11520}
    cache={z['field']:tuple(z['chart'])for z in W['caches']};assert len(cache)==len(W['caches'])and set(cache)==set(range(PF,PF+len(cache)))
    acts=W['actions'];assert len({x['tag']for x in acts})==len(acts)
    assert [STAGES.index(x['stage'])for x in acts]==sorted(STAGES.index(x['stage'])for x in acts)
    public=sorted({z for x in acts for op in x['word']for z in op[1:]if z<PB});col={z:i for i,z in enumerate(public)}
    ym=sum(1<<i for z,i in col.items()if z>=XB)
    def location(stage,z):
        f=z//5
        if f>=PF:return cache[f]
        kind,j,c,h,d,k,left,right=route[f]
        if kind=='X':
            if stage==0:return('L',j)
            if stage==1:return('H',h)
            if stage==2:return('D',d)
            if stage==3:return('K',k)if k is not None else('Hub',)
            if stage==4:return('F',right)if right is not None else('Hub',)
            return('Hub',)
        if stage<=6:return('Ground',)
        if stage==7:return('L',left)if left is not None else None
        if stage==8:return('H',h)if h is not None else None
        if stage==9:return('D',d)
        if stage==10:return('K',k)
        return('F',j)
    donors=W['source_donors'];assert donors==sorted(set(donors))and set(W['receivers'])=={1,80}and W['selected_rows']==list(range(4))
    assert all(j in orth[80]and j in orth[1]for j in donors)
    neighbors=sorted(orth[80]&set(range(N)));expected={}
    for i in [80,1]:
        for t in range(4):
            fs=[]
            for j in donors:
                cc=[t];pos=neighbors.index(j)
                if i==80 and pos==0:cc.append(t+1)
                elif i==80 and 2<=pos<=60:cc.append(8*(pos-1)+t)
                fs.extend(j*BANK+c for c in cc)
            for bit in range(5):
                z=5*(N*BANK+i*BANK+t)+bit;assert z in col
                expected[z]=(1<<col[z])^sum(1<<col[5*f+bit]for f in fs)
    first_H=next(x['tag']for x in acts if x['stage']=='X_H');first_L=next(x['tag']for x in acts if x['stage']=='Y_LINE');first_F=next(x['tag']for x in acts if x['stage']=='X_F')
    hub=next(x['tag']for x in acts if x['stage']=='HUB_RESTORE');ground=next(x['tag']for x in acts if x['stage']=='GROUND_PRELOAD')
    def replay(skip=None,omit_add=None,wrong_chart=False,late_X_read=False,dead_cache=False):
        value={z:1<<i for z,i in col.items()};live=set();ever=set();counts=Counter();peak=dirty=checks=0;at_hub=None
        for idx,act in enumerate(acts):
            if act['tag']==skip:continue
            stage=STAGES.index(act['stage']);chart=tuple(act['chart']);assert chart[0]==CHARTS[stage]
            if wrong_chart and act['tag']==first_H:chart=('H',chart[1]+1)
            word=act['word']
            if act['tag']==omit_add:word=[op for op in word if op[0]!='ADD']
            if late_X_read and act['tag']==first_L:
                word=[list(op)for op in word];op=next(op for op in word if op[0]=='ADD');op[2]=0
            if dead_cache and act['tag']==first_L:word=[op for op in word if op[0]=='CLEAR']+[op for op in word if op[0]!='CLEAR']
            for op in word:
                kind=op[0];assert kind in ['ADD','INIT','CLEAR']
                for z in op[1:]:
                    assert isinstance(z,int)and z>=0
                    if location(stage,z)!=chart:raise ValueError('nonlocal original or stationary-cache operand')
                    if z>=PB and kind!='INIT'and z not in live:raise ValueError('owned operand used outside lifetime')
                    checks+=1
                counts[kind]+=1
                if kind=='INIT':
                    z=op[1];assert z>=PB and z not in ever;ever.add(z);live.add(z);value[z]=0;peak=max(peak,len(live))
                elif kind=='ADD':
                    dst,src=op[1:];assert dst!=src;value[dst]^=value[src]
                else:
                    z=op[1];assert z in live;dirty+=bool(value[z]);live.remove(z);del value[z]
            if stage==5:at_hub=all(value[z]==1<<i for z,i in col.items()if z<XB)
        assert not live and ever=={5*f+r for f in cache for r in range(5)}
        return {'all_X_before_Y':bool(at_hub),'all_X_final':all(value[z]==1<<i for z,i in col.items()if z<XB),
                'all_Y_identity':all(value[z]&ym==1<<i for z,i in col.items()if z>=XB),
                'selected_targets':all(value[z]==v for z,v in expected.items()),'counts':dict(counts),
                'dirty_CLEAR':dirty,'extra_peak':peak,'operand_locality_checks':checks}
    r=replay();assert all(r[k]for k in ['all_X_before_Y','all_X_final','all_Y_identity','selected_targets'])
    invoice={'ADD':r['counts']['ADD'],'INIT':r['counts']['INIT'],'dirty_CLEAR':r['dirty_CLEAR'],'extra_peak_binary_owners':r['extra_peak'],
             'public_binary_owners':PB,'peak_total_binary_owners':PB+r['extra_peak'],'proper_MOVE_binary_counts':{str(k):5*v for k,v in movement.items()},'added_MOVE':0,'canonical_return_included':False}
    assert invoice==W['invoice']and r['counts']['CLEAR']==r['counts']['INIT']==5*len(cache)
    faults={}
    for tag,key in [(hub,'all_X_final'),(ground,'all_Y_identity')]:
        f=replay(skip=tag);assert not f[key];faults[tag]=key
    for tag in [first_L,first_F]:
        f=replay(omit_add=tag);assert not f['selected_targets'];faults['omit_add:'+tag]='selected_targets'
    for name,kw in [('wrong_chart',{'wrong_chart':True}),('late_original_X_read',{'late_X_read':True}),('cache_use_after_clear',{'dead_cache':True})]:
        try:replay(**kw)
        except ValueError as err:faults[name]=str(err)
        else:raise AssertionError(name)
    out={'status':'PASS_INDEPENDENT_FULL_NATIVE_OWNER_WORD_REVIEW','word_pin':a.word_pin,'source_pins':PINS,
         'actual_public_field_paths':PF,'all_independent_original_binary_columns':PB,'touched_public_binary_columns':len(col),
         'untouched_X_columns':XB-sum(z<XB for z in col),'untouched_Y_columns':XB-sum(z>=XB for z in col),
         'active_donors':len(donors),'selected_receivers':[80,1],'target_binary_rows':len(expected),'actions':len(acts),'cache_fields':len(cache),
         'verification':r,'invoice':invoice,'negative_controls':faults,'author_code_imported_or_executed':False,
         'same_B_owner_engine_as_predecessor':True,'all_unselected_proper_targets_prescribed':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print('donors',len(donors),'ADD',invoice['ADD'],'all532800 columns; operand checks',r['operand_locality_checks'])
if __name__=='__main__':main()
