#!/usr/bin/env python3
"""Independent four-cut geometry, handoff, activity and complete price review."""
import argparse,hashlib,json
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as Q
from functools import lru_cache
import sympy as S

FRAMES=[[0,14,18,30,69,70,107],[2,8,9,14,21,46,88,92],
        [4,11,12,16,36,37,74,78],[4,32,35,55,56,89,93]]
DONORS=[16,19,38,49,50,56,57]

def rank(rows):
    piv={}
    for r in rows:
        while r:
            k=(r&-r).bit_length()-1
            if k in piv:r^=piv[k]
            else:piv[k]=r;break
    return len(piv)

@lru_cache(None)
def basis(kind,rows):
    if kind=='ann':
        columns=S.Matrix(rows).nullspace() if rows else list(S.eye(8).columnspace())
        matrix=S.Matrix([list(v)for v in columns]) if columns else S.zeros(0,8)
    else:matrix=S.Matrix(rows)if rows else S.zeros(0,8)
    r,_=matrix.rref()
    return tuple(tuple(r.row(i))for i in range(r.rows)if any(r.row(i)))

@lru_cache(None)
def root(r):
    den=1<<90;target=r**199*den**200;lo,hi=0,r*den
    if hi**200==target:return Q(hi,den),Q(hi,den)
    while hi-lo>1:
        m=(hi+lo)//2
        if m**200<=target:lo=m
        else:hi=m
    assert lo**200<=target<hi**200
    return Q(lo,den),Q(hi,den)

def moment(p):
    l=h=Q(0)
    for r,c in p.items():
        a,b=root(r)
        if c<0:a,b=b,a
        l+=c*a;h+=c*b
    return l,h

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    p=args.repo/'research/moonshot-005-program'
    geo=p/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    assert hashlib.sha256(geo.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(geo.read_text())['native_roots'];masks=[sum(1<<j for j in f)for f in FRAMES]
    for f in FRAMES:
        assert not(set(f)&{17,34})
        assert all(sum(a*b for a,b in zip(roots[i],roots[j]))!=0 for i in f for j in f)
    result={'status':'PASS_ROOT_FOUR_FRAME_GROUND_EXPORT_REVIEW','variants':{},'new_complete_kappa':False}
    for mode in['COUPLED','UNCOPLED']:
        fn=p/f'results/bit-coupled-singular-delivery/worker-a/two-receiver-output/{mode}-WORD.json';word=json.loads(fn.read_text())
        charts={n:basis(c['kind'],tuple(tuple(r)for r in c['rows']))for n,c in word['charts'].items()}
        rec={f'X{i}':['L'+str(i),1<<i]for i in range(111)}|{f'Y{i}':['zero',1<<(111+i)]for i in range(111)}
        bill=Counter()
        for op in word['operations']:
            k,n,*rest=op
            if k=='INIT':rec[n]=[rest[0],0]
            elif k=='ADD':
                assert charts[rec[n][0]]==charts[rec[rest[0]][0]]
                rec[rest[0]][1]^=rec[n][1]
            elif k=='MOVE':
                bill[abs(len(charts[rec[n][0]])-len(charts[rest[0]]))]+=1;rec[n][0]=rest[0]
            elif k=='CLEAR':del rec[n]
        for i in range(111):
            assert rec[f'X{i}']==['Hub',1<<i]
            assert rec[f'Y{i}'][1]==(1<<(111+i))^((1<<i)if i in[17,34]else 0)
            if i not in[17,34]:bill[7]+=1
        expected={1:142,2:19,3:49,4:66,5:22,6:22,7:112,8:1};assert dict(bill)==expected
        cells=defaultdict(list)
        for n,(c,r)in rec.items():cells[charts[c]].append((n,r&((1<<111)-1)))
        G=[r for n,r in cells[()]]+[1<<j for j in DONORS]
        ranks=[rank([g&m for g in G])for m in masks];assert ranks==[4,5,6,5]
        deficits=[len(f)-r for f,r in zip(FRAMES,ranks)];assert deficits==[3,3,2,2]
        inventory=[]
        for cell,rows in cells.items():
            active=[i for i,m in enumerate(masks)if rank([g&m for g in G]+[v&m for n,v in rows])>ranks[i]]
            assert len(active)<=len(cell)
            inventory.append({'dimension':len(cell),'record_names':[n for n,v in rows],'active':active})
        assert all(c['dimension']!=2 for c in inventory)
        assert all(not c['active']for c in inventory if c['dimension']==3)
        result['variants'][mode]={'word_sha256':hashlib.sha256(fn.read_bytes()).hexdigest(),'ranks':ranks,'deficits':deficits,'cells':inventory,'source_profile':expected}
    assert 8*989**200<1000**200
    n={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};h={2:1,4:25,6:1,8:410}
    def add(*terms):
        d=defaultdict(Q)
        for c,p0 in terms:
            for r,v in p0.items():d[r]+=c*v
        return dict(d)
    P2=add((36,n),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
    T2=add((36,h),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
    diff=add((1,T2),(-1,P2));assert moment(diff)[1]<0
    room=add((1,n),(-1,h),(Q(1,36),diff),(-1,expected))
    interval=moment(room);assert interval[1]<Q(37,4)<Q(989,100)
    result['price']={'limiting_room_interval':[str(v)for v in interval],
                     'T2_minus_P2_interval':[str(v)for v in moment(diff)],
                     'all_even_m_stricter_identity':'B_m-B_inf=(T2-P2)/(36*(m-1))<0',
                     'added_cost_strict_lower':'989/100',
                     'deficit_strict_lower':str(Q(989,100)-interval[1])}
    result['scope']='Direct ground-export grammar only. Every cheapest required receiver ascent remains charged once in Q2; extra decoder acquisition/fragmentation is optimistically free. Independent nullspace geometry merges equivalent charts regardless of span/ann representation.'
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'deficits':[3,3,2,2],'all_cells_pass':True,'price':result['price']}))
if __name__=='__main__':main()
