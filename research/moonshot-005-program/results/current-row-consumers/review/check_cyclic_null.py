"""Independent exact review of the cyclic null-4/null-8 words."""
import argparse
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--repo',required=True,type=Path,help='root of the pinned programme checkout')
parser.add_argument('--author',required=True,type=Path,help='root of frozen worker-a artifacts')
args=parser.parse_args()
REPO=args.repo
AUTHOR=args.author
SRC=REPO/'research/shared-wire-split-composition/data/final.json.gz'
PARENT=REPO/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz'
CASES={'4':AUTHOR/'cyclic-null-4/WORD.json.gz','8':AUTHOR/'cyclic-null-8/WORD.json.gz'}
PIN_SRC='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PIN_PARENT='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'


def need(ok,msg):
    if not ok: raise AssertionError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(path):
    raw=path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)
def q(value): return Q(str(value))
def rowadd(a,b,c=Q(1)):
    out=a.copy()
    for k,v in b.items():
        value=out.get(k,Q(0))+c*v
        if value: out[k]=value
        else: out.pop(k,None)
    return out
def span(frame):
    out={0}
    for vector in frame: out|={x^vector for x in tuple(out)}
    return frozenset(out)
def frames(source,word):
    return source['frames']+[x['frame'] for x in word.get('additional_charts',[])]
def root9(bits):
    support={i for i in range(9) if bits>>i&1}
    if len(support)==3:
        return [Q(int(i in support))-Q(1,3) for i in range(9)]
    need(len(support)==7,'E8 role root weight')
    a,b=sorted(set(range(9))-support)
    return [Q(int(i==a)-int(i==b)) for i in range(9)]
def rank(A):
    if not A: return 0
    B=[list(row) for row in A];m,n=len(B),len(B[0]);r=0
    for col in range(n):
        pivot=next((i for i in range(r,m) if B[i][col]),None)
        if pivot is None: continue
        B[r],B[pivot]=B[pivot],B[r]
        scale=B[r][col];B[r]=[x/scale for x in B[r]]
        for i in range(m):
            if i!=r and B[i][col]:
                scale=B[i][col];B[i]=[x-scale*y for x,y in zip(B[i],B[r])]
        r+=1
        if r==m: break
    return r
def replay(source,word,stop):
    f=frames(source,word);n=1880
    rows=[{i:Q(1)} for i in range(n)]+[{} for _ in range(word['owned_fields'])]
    loc=list(word['initial'])+[None]*word['owned_fields'];live=set(range(n))
    for t,oprec in enumerate(word['program'][:stop]):
        op,dst=oprec[:2]
        need(0<=dst<len(loc),f'field address event {t}')
        if op=='INIT':
            need(dst>=n and dst not in live and loc[dst] is None,f'fresh owned INIT {t}')
            rows[dst]={};loc[dst]=oprec[2];live.add(dst)
        elif op=='CLEAR':
            need(dst>=n and dst in live and loc[dst]==oprec[2],f'owned CLEAR {t}')
            live.remove(dst);loc[dst]=None;rows[dst]={}
        elif op=='MOVE':
            src_chart,dst_chart,owned=oprec[2:]
            need(dst in live and loc[dst]==src_chart and type(owned)is bool and owned==(dst>=n),f'MOVE source/ownership {t}')
            source_span,target_span=span(f[src_chart]),span(f[dst_chart])
            need(source_span<target_span or (owned and target_span<source_span),f'MOVE nesting {t}')
            loc[dst]=dst_chart
        elif op=='SCALE':
            scale=q(oprec[2]);need(scale and dst in live and loc[dst]==oprec[3],f'SCALE source {t}')
            rows[dst]={i:scale*v for i,v in rows[dst].items() if scale*v}
        else:
            need(op in ('ADD','COPY'),f'unknown opcode {t}')
            src,scale,chart=oprec[2],q(oprec[3]),oprec[4]
            need(dst!=src and dst in live and src in live and loc[dst]==loc[src]==chart,f'cochart source {t}')
            if op=='COPY': need(not rows[dst],f'COPY destination nonzero {t}')
            rows[dst]=rowadd(rows[dst],rows[src],scale)
    return rows,loc,live
def full_type(source,word,raw_fields):
    f=frames(source,word);n=1880
    loc=list(word['initial'])+[None]*word['owned_fields'];live=set(range(n))
    counts=Counter();moves=Counter();rawmoves=Counter();ownedmoves=Counter()
    now=0;peak=0;lifetimes=0
    for t,record in enumerate(word['program']):
        op,dst=record[:2];counts[op]+=1
        if op=='INIT':
            need(dst>=n and dst not in live and loc[dst] is None,f'full INIT {t}')
            loc[dst]=record[2];live.add(dst);now+=1;lifetimes+=1;peak=max(peak,now)
        elif op=='CLEAR':
            need(dst>=n and dst in live and loc[dst]==record[2],f'full CLEAR {t}')
            live.remove(dst);loc[dst]=None;now-=1
        elif op=='MOVE':
            a,b,owned=record[2:]
            need(dst in live and loc[dst]==a and owned==(dst>=n),f'full MOVE source/owner {t}')
            need(span(f[a])<span(f[b]) or (owned and span(f[b])<span(f[a])),f'full MOVE nesting {t}')
            r=abs(len(f[a])-len(f[b]));moves[r]+=1
            (ownedmoves if owned else rawmoves)[r]+=1
            loc[dst]=b
        elif op=='SCALE':
            need(dst in live and loc[dst]==record[3] and q(record[2]),f'full SCALE {t}')
        else:
            need(op in ('ADD','COPY') and dst in live and record[2] in live and loc[dst]==loc[record[2]]==record[4],f'full ADD/COPY {t}')
    need(live==set(range(n)) and now==0 and all(loc[i] is not None for i in range(n)),'full word lifetimes')
    return counts,moves,rawmoves,ownedmoves,peak,lifetimes,loc


source=load(SRC);parent=load(PARENT);parent_result=load(PARENT.parent/'RESULT.json')
need(sha(SRC.read_bytes())==PIN_SRC,'native source pin')
need(sha(PARENT.read_bytes())==PIN_PARENT,'cyclic parent pin')
raw={int(k):v for k,v in parent['private_role_map'].items()}
host={source['live'][k]:(x,y) for k,x,y in zip(source['hosted']['Dports'],source['hosted']['X2'],source['hosted']['Y2'])}
order=list(host);K=[j for g in parent['cyclic_dual']['source_groups'] for kind in ('B','S','T') for j in g[kind]]
need(len(order)==96 and len(K)==22 and len(set(K))==22,'hosted role set')
roots={i:root9(source['frames'][source['initial'][i]][0]) for i in order}
G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2
need(all(G(i,j)==Q(i==j) for i in [5,56,69,100,65,77,96,103] for j in [5,56,69,100,65,77,96,103]),'B8 orthonormality')
parent_at=parent['marks']['common_starts']
parent_rows,parent_loc,parent_live=replay(source,parent,parent_at)
parent_counts,parent_moves,parent_rawmoves,parent_ownedmoves,parent_peak,parent_life,parent_final=full_type(source,parent,set(raw.values()))
C0={i:{j:Q(i==j)+parent_rows[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order} for i in order}
need(rank([[C0[i][j] for j in order] for i in order])==82,'independently reconstructed parent residual rank')
outside=[i for i in order if i not in K]
need(all(C0[i][j]==0 for i in K for j in outside),'parent top-right block is zero')
need(all(C0[i][j]==Q(i==j) for i in outside for j in outside),'parent outside block is I74')

receipts=[]
for label,path in CASES.items():
    word=load(path);result=load(path.parent/'RESULT.json');meta=word['cyclic_null_projector'];J=meta['selected_modes']
    need(word['parent_word_sha256']==PIN_PARENT,'candidate points to exact parent '+label)
    need(sha(path.read_bytes())==result['word_sha256'],'candidate word pin '+label)
    need(sha(SRC.read_bytes())==result['source_sha256'],'candidate source pin '+label)
    need(len(J)==int(label) and len(set(J))==len(J) and set(J)<=set(K),'selected orthogonal modes '+label)
    need(word['program'][word['marks']['common_starts']:] == parent['program'][parent_at:],'literal common suffix '+label)
    obs=meta['observation_boundary']
    before,before_loc,before_live=replay(source,word,obs)
    need(before[:1880]==parent_rows[:1880],'all 1880 original rows unchanged through observations '+label)
    need(before_loc[:1880]==parent_loc[:1880],'all original locations restored at observation boundary '+label)
    live_added={meta['ghost_fields'][str(j)] for j in J}|{meta['return_fields'][str(j)] for j in J}
    need(parent_live<=before_live and before_live-parent_live==live_added,
         'only declared ghost/return records are additionally live at observation '+label)
    ghost_rows={}
    for j in J:
        ghost=meta['ghost_fields'][str(j)];ret=meta['return_fields'][str(j)]
        expected={}
        for k in K: expected=rowadd(expected,before[raw[host[k][1]]],G(j,k))
        need(before[ghost]==expected,f'late-cancelled ghost equals actual Gram row for {j}')
        need(before[ret]==parent_rows[raw[host[j][1]]],f'authentic original d{j} returned')
        need(before_loc[ghost]==127 and before_loc[ret]==127,f'ghost/return at Hub {j}')
        need(parent_loc[raw[host[j][1]]]==source['final'][host[j][1]],f'original d{j} endpoint restored')
        ghost_rows[j]=expected
    after,after_loc,after_live=replay(source,word,word['marks']['common_starts'])
    need(after_live==parent_live and after_loc[:1880]==parent_loc[:1880],'original locations/lifetimes at common entry '+label)
    need(all(after[i]=={i:Q(1)} and after_loc[i]==word['initial'][i] for i in range(1480)),'1480 common identity rows '+label)
    for i in K:
        b=raw[host[i][0]];expected=parent_rows[b].copy()
        for j in J: expected=rowadd(expected,ghost_rows[j],-G(i,j))
        need(after[b]==expected,f'actual full-coordinate Gram correction for B row {i}')
    for i in order:
        b=raw[host[i][0]]
        if i not in K: need(after[b]==parent_rows[b],f'outside-K current B row unchanged {i}')
    C1={i:{j:Q(i==j)+after[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order} for i in order}
    for i in order:
        for j in order:
            projection=sum(G(i,k)*G(k,j) for k in J) if i in K and j in K else Q(0)
            need(C1[i][j]==C0[i][j]-projection,f'actual projected residual matrix entry {i},{j}')
    new_rank=rank([[C1[i][j] for j in order] for i in order])
    need(new_rank==82-len(J),f'full residual rank drops by selected independent modes {label}')
    completed={i for i in order if all(C1[i][j]==0 for j in order)}
    need(completed==set(result['completed_hosted_reverse_ports']),f'actual completed outputs {label}')
    need(len(completed)==(11 if label=='4' else 22),f'completed endpoint count {label}')
    # Changed hosted rows are each consumed only by their original suffix recoupling.
    changed=[]
    suffix=word['program'][word['marks']['common_starts']:]
    for i in order:
        b=raw[host[i][0]]
        if after[b]!=parent_rows[b]:
            changed.append(i)
            uses=[o for o in suffix if o[1]==b or o[0] in ('ADD','COPY') and o[2]==b]
            need(uses==[['ADD',b,host[i][0],'1',source['final'][host[i][0]]]],f'only own final recoupling for changed B{i}')
    counts,moves,rawmoves,ownedmoves,peak,lifetimes,final=full_type(source,word,set(raw.values()))
    need(rawmoves==parent_rawmoves,'all original raw routes retained '+label)
    need(moves==parent_moves+Counter({1:len(J),6:len(J)}),'only expected rank1/rank6 owned MOVEs '+label)
    need(ownedmoves==parent_ownedmoves+Counter({1:len(J),6:len(J)}),'owned MOVE tariff '+label)
    need(peak==parent_peak==43 and lifetimes==parent_life+2*len(J),'peak/lifetime accounting '+label)
    need(final[:len(parent_final)]==parent_final and all(x is None for x in final[len(parent_final):]),'final locations / all temporary fields retired '+label)
    need(counts['ADD']-parent_counts['ADD']==12*len(J),'all projector ADDs billed '+label)
    need(counts['INIT']-parent_counts['INIT']==2*len(J) and counts['CLEAR']-parent_counts['CLEAR']==2*len(J),'all owned lifetimes retired '+label)
    need(counts['MOVE']-parent_counts['MOVE']==2*len(J),'all new owned MOVEs counted '+label)
    need(result['new_owned_move_histogram']=={'1':len(J),'6':len(J)},'result owned rank histogram '+label)
    need(result['hosted_reverse_residual_rank']==new_rank,'reported exact rank '+label)
    receipts.append({'case':label,'word_sha256':sha(path.read_bytes()),'selected_modes':len(J),'completed_hosted_reverse_outputs':len(completed),'parent_residual_rank':82,'actual_residual_rank':new_rank,'ghost_rows_equal_actual_Gram_d_combinations':True,'all1880_preprojection_rows_match_parent':True,'all1480_common_identities':True,'all_original_D_restored':True,'changed_B_rows_used_only_for_own_final_recoupling':True,'raw_move_histogram_unchanged':True,'new_owned_move_histogram':{'1':len(J),'6':len(J)},'owned_peak':peak,'owned_lifetimes_added':2*len(J),'ordinary_increment':{'ADD':counts['ADD']-parent_counts['ADD'],'INIT':2*len(J),'MOVE':2*len(J),'CLEAR':2*len(J)}})

print(json.dumps({'status':'PASS_INDEPENDENT_CYCLIC_NULL_AUDIT','source_sha256':PIN_SRC,'parent_sha256':PIN_PARENT,'parent_residual_rank':82,'cases':receipts,'scope':'Checks exact scalar source algebra, all1880 input rows, chart/lifetime validity, residual rank, selected completions and movement/ordinary counts. It does not complete the full supplier or remaining forward duties.'},indent=2))
