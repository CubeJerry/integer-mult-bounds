#!/usr/bin/env python3
"""Independent physical-owner and compressed symbolic replay of the b480 tile."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','phase':'a806cc80a7bc7955fa07e04384707deb38200bac682424682e997f742dc5e278','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','word':'42b701dfce05e108dfafc4db5dcf813f92c42d74f0416e6d37a1d7bb301459e1','matrices':'1f345560001ed3c54ece49ab50f4f8a148914738c26e433bac27dd6a74599753'}
STAGES=['X_NATIVE','X_H','X_D','X_K','X_F','HUB_RESTORE','GROUND_PRELOAD','Y_H','Y_D','Y_K','Y_F']
PUBLIC_FIELDS=111*480*2;PUBLIC_BITS=PUBLIC_FIELDS*5;X_BITS=111*480*5

def load(path,key,jsonl=False):
    raw=gzip.decompress(path.read_bytes())if path.suffix=='.gz'else path.read_bytes();assert sha256(raw).hexdigest()==PINS[key]
    return[json.loads(x)for x in raw.splitlines()]if jsonl else json.loads(raw)
def mul(a,b):
    p=0
    for k in range(5):
        if(b>>k)&1:p^=a<<k
    for k in range(8,4,-1):
        if(p>>k)&1:p^=0x25<<(k-5)
    return p
FM=[[mul(a,b)for b in range(32)]for a in range(32)]
def fdot(a,b):
    r=0
    for x,y in zip(a,b):r^=FM[x][y]
    return r
def b_rank(rows):
    ps={}
    for v0 in rows:
        v=v0
        while v:
            p=v.bit_length()-1
            if p in ps:v^=ps[p]
            else:ps[p]=v;break
    return len(ps)
def field_rank(rows):
    return b_rank(sum(([sum(FM[1<<t][x]<<(5*j)for j,x in enumerate(row))for t in range(5)]for row in rows),[]))//5

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results';atlas=base/'bit-asymmetric-balanced-atlas/author'
    L=load(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout');phase=load(atlas/'PHASE-CERTIFICATE.json','phase')
    routes=load(atlas/'output/ROUTES.jsonl.gz','routes',True);W=load(a.author/'output/WORD.json.gz','word');M=load(a.author/'output/MATRICES.json.gz','matrices')
    roots=L['root_table'];H=list(map(set,L['A2']));D=list(map(set,L['D4']));O=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots]
    owners={};movement=Counter();source_counts=Counter();target_counts=Counter();presence={}
    for rr in routes:
        kind,j,c,h,d,k,left,right=rr
        assert kind in ['X','Y'] and 0<=j<111 and 0<=c<480 and 0<=d<3150
        f=(0 if kind=='X' else 111*480)+j*480+c;assert f not in owners;owners[f]=rr
        if h is not None:assert H[h]<=D[d]
        if k is not None:assert all(y in O[x]for x in D[d]for y in H[k])
        if left is not None:assert h is not None and left in H[h]
        if right is not None:assert k is not None and right in H[k]
        if kind=='X':
            assert left==j and h is not None;source_counts[j]+=1
            ranks=[1,2,4]+([6]if k is not None else[])+([7]if right is not None else[])+[8]
            loc=[('L',j),('H',h),('D',d),('K',k)if k is not None else('Hub',),('F',right)if right is not None else('Hub',)]+[('Hub',)]*6
        else:
            assert right==j and k is not None;target_counts[j]+=1
            ranks=[0]+([1]if left is not None else[])+([2]if h is not None else[])+[4,6,7]
            loc=[('Ground',)]*7+[('H',h)if h is not None else('D',d),('D',d),('K',k),('F',j)]
        assert all(y>x for x,y in zip(ranks,ranks[1:]));movement.update(y-x for x,y in zip(ranks,ranks[1:]));presence[f]=loc
    assert len(owners)==PUBLIC_FIELDS and set(source_counts.values())=={480} and set(target_counts.values())=={480}
    assert dict(movement)=={1:267060,2:216390,4:11520}
    assert M['D']==12 and M['dual_D']==116 and D[12]<=O[80]
    hs=[h for h,V in enumerate(H)if V<=D[12]];ks=[k for k,V in enumerate(H)if V<=D[116]]
    assert hs==M['H'] and ks==M['K'] and len(hs)==len(ks)==16
    assert max(D[12]|D[116])<111 and not set(hs+ks)&set(phase['full_early_planes'])
    assert all(max(H[h])<111 for h in hs+ks)
    selected=[k for k in ks if 80 in H[k]];assert selected==[370,371,372,373]
    donors=sorted(D[12]);neighbors=sorted(O[80]&set(range(111)));assert len(neighbors)==62 and donors==W['source_donors']
    A=[[next(z for z in range(1,32)if FM[r^(16+c)][z]==1)for c in range(16)]for r in range(16)]
    assert A==M['Cauchy'] and field_rank(A)==16
    Ri=[ks.index(k)for k in selected];all_source_maps=0
    for entry in M['pair_transfers']:
        j=entry['donor'];C=[h for h in hs if j in H[h]];Ci=[hs.index(h)for h in C]
        minor=[[A[r][c]for c in Ci]for r in Ri];assert field_rank(minor)==4
        S=[row+[0]*4 for row in minor]+[[int(r==c)for c in Ci]+row for r,row in zip(Ri,minor)]
        assert S==entry['transfer'] and field_rank(S)==8
        T=[[int(r==c)for c in range(480)]for r in range(8)];pos=neighbors.index(j)
        if pos==0:
            for r in range(7):T[r][r+1]^=1
        elif pos==1:T[7][0]^=1
        elif pos<=60:
            for r in range(8):T[r][8*(pos-1)+r]^=1
        F=M['source_maps'][str(j)];assert T==entry['target'] and [[fdot(row,col)for col in zip(*F)]for row in S]==T
        assert field_rank([row[:8]for row in F])==8
        slots=M['source_slots'][str(j)];assert len(slots)==len(set(slots))==8
        for t,h in enumerate(C):
            for slot in [slots[t],slots[t+4]]:assert owners[j*480+slot][3]==h
        all_source_maps+=1
    assert all_source_maps==12
    acts=W['actions'];assert [STAGES.index(x['stage'])for x in acts]==sorted(STAGES.index(x['stage'])for x in acts)
    assert len(acts)==245 and all(op[0] in ['ADD','INIT','CLEAR']for x in acts for op in x['word'])
    public=sorted({bit for x in acts for op in x['word']for bit in op[1:]if bit<PUBLIC_BITS});col={bit:k for k,bit in enumerate(public)}
    ymask=sum(1<<col[bit]for bit in public if bit>=X_BITS)
    cache_charts={z['field']:tuple(z['chart'])for z in W['caches']};assert set(cache_charts)==set(range(PUBLIC_FIELDS,PUBLIC_FIELDS+68))
    expect={}
    for r in range(8):
        source=[]
        for j in donors:
            cc=[r];pos=neighbors.index(j)
            if pos==0 and r<7:cc.append(r+1)
            elif pos==1 and r==7:cc.append(0)
            elif 2<=pos<=60:cc.append(8*(pos-1)+r)
            source += [j*480+c for c in cc]
        for bit in range(5):
            target=5*(111*480+80*480+r)+bit
            assert target in col and all(5*f+bit in col for f in source)
            expect[target]=(1<<col[target])^sum(1<<col[5*f+bit]for f in source)
    def replay(skip=None,bad_chart=False,bad_late_read=False):
        values={bit:1<<col[bit]for bit in public};active=set();ever=set();count=Counter();peak=dirty=reads=0;changed=False
        for act in acts:
            if act['tag']==skip:continue
            stage=STAGES.index(act['stage']);chart=tuple(act['chart'])
            if bad_chart and act['tag']=='early-H-86':chart=('H',89)
            word=act['word']
            if bad_late_read and act['tag']=='D-cross-12':word=[['ADD',word[0][1],0]]+word[1:]
            for op in word:
                kind=op[0]
                for bit in op[1:]:
                    f=bit//5
                    actual=cache_charts[f]if f>=PUBLIC_FIELDS else presence[f][stage]
                    if actual!=chart:raise ValueError('nonlocal operand')
                    if f>=PUBLIC_FIELDS and kind!='INIT'and bit not in active:raise ValueError('dead owned operand')
                    reads+=1
                count[kind]+=1
                if kind=='INIT':
                    bit=op[1];assert bit>=PUBLIC_BITS and bit not in ever;ever.add(bit);active.add(bit);values[bit]=0;peak=max(peak,len(active))
                elif kind=='ADD':
                    dst,src=op[1:];assert dst!=src;values[dst]^=values[src]
                else:
                    bit=op[1];assert bit in active;dirty+=bool(values[bit]);active.remove(bit);del values[bit]
        assert not active
        xok=all(values[bit]==1<<col[bit]for bit in public if bit<X_BITS)
        yok=all(values[bit]&ymask==1<<col[bit]for bit in public if bit>=X_BITS)
        targetok=all(values[bit]==v for bit,v in expect.items())
        return {'X':xok,'Y':yok,'target':targetok,'counts':dict(count),'peak':peak,'dirty':dirty,'operand_checks':reads},values
    result,endpoint=replay();assert result['X']and result['Y']and result['target']
    assert result['counts']=={'ADD':32190,'INIT':340,'CLEAR':340}and result['peak']==result['dirty']==340
    faults={}
    for tag,key in [('restore-all-X','X'),('inverse-arbitrary-Y-baseline','Y'),('late-H-101-0','target'),('D-cross-12','target'),('final-early-add-0','target')]:
        fault,_=replay(skip=tag);assert not fault[key];faults[tag]={'failed_condition':key}
    for name,opts in [('wrong_chart',{'bad_chart':True}),('late_original_X_read',{'bad_late_read':True})]:
        try:replay(**opts)
        except ValueError as e:faults[name]={'rejected':str(e)}
        else:raise AssertionError(name)
    invoice={'ADD':32190,'INIT':340,'dirty_CLEAR':340,'extra_peak_binary_owners':340,'public_binary_owners':PUBLIC_BITS,'peak_total_binary_owners':PUBLIC_BITS+340,'proper_MOVE_binary_counts':{str(k):5*v for k,v in movement.items()},'added_MOVE':0,'canonical_return_included':False}
    assert invoice==W['invoice']
    all_x_untouched=X_BITS-sum(x<X_BITS for x in public);all_y_untouched=X_BITS-sum(x>=X_BITS for x in public)
    out={'status':'PASS_INDEPENDENT_LITERAL_NATIVE_TARGET_TILE_REVIEW','pins':PINS,
      'physical_routes':len(routes),'all_original_columns_covered':PUBLIC_BITS,'compressed_touched_columns':len(public),
      'untouched_X_identity_columns':all_x_untouched,'untouched_Y_identity_columns':all_y_untouched,
      'all_source_matrices_checked':all_source_maps,'local_Cauchy_minors':12,'target_field_rows':8,'target_binary_rows':40,
      'all_original_X_restored':result['X'],'arbitrary_Y_identity':result['Y'],'selected_target_exact':result['target'],
      'literal_operand_locality_checks':result['operand_checks'],'invoice':invoice,'faults':faults,
      'author_code_imported_or_executed':False,'author_symbolic_engine_used':False,
      'unserved_foreign_donors':len(neighbors)-len(donors),'full_target_constructed':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status']);print('routes',len(routes),'binary columns',PUBLIC_BITS,'selected rows',40,'ADD',invoice['ADD'])
if __name__=='__main__':main()
