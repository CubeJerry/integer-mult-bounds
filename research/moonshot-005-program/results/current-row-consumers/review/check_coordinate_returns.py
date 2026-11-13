"""Independent exact audit of Worker A's 22/31 whole-column returns.
Uses stdlib, pinned payloads, and a fresh sparse-Q source interpreter.
"""
from collections import Counter
from fractions import Fraction as Q
import argparse
import gzip, hashlib, json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--repo',required=True,type=Path,help='root of the pinned programme checkout')
parser.add_argument('--author',required=True,type=Path,help='root of frozen worker-a artifacts')
args=parser.parse_args()
REPO=args.repo
AUTHOR=args.author
SRC=REPO/'research/shared-wire-split-composition/data/final.json.gz'
PARENT=REPO/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz'
CASES={'22':AUTHOR/'cyclic-column-22/WORD.json.gz','31':AUTHOR/'cyclic-column-31/WORD.json.gz','58':AUTHOR/'cyclic-column-rank58/WORD.json.gz'}
PIN_SRC='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PIN_PARENT='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'

def need(ok,msg):
    if not ok: raise AssertionError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def load(path):
    b=path.read_bytes()
    return json.loads(gzip.decompress(b) if path.suffix=='.gz' else b)
def q(v): return Q(str(v))
def rowadd(a,b,c=Q(1)):
    z=a.copy()
    for k,v in b.items():
        x=z.get(k,Q(0))+c*v
        if x: z[k]=x
        else: z.pop(k,None)
    return z
def span(frame):
    s={0}
    for v in frame: s |= {x^v for x in tuple(s)}
    return frozenset(s)
def power_interval(rank):
    # Exact dyadic floor/ceiling for rank^(199/200), denominator 2^120.
    D=2**120
    N=rank**199 * D**200
    lo,hi=0,rank*D+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=N: lo=mid
        else: hi=mid
    lower=Q(lo,D)
    upper=Q(lo if lo**200==N else hi,D)
    need(lo**200<=N<hi**200,'exact root bracket')
    return lower,upper

def root9(bits):
    support={i for i in range(9) if bits>>i&1}
    if len(support)==3: return [Q(int(i in support))-Q(1,3) for i in range(9)]
    need(len(support)==7,'nine-coordinate E8 root weight')
    a,b=sorted(set(range(9))-support)
    return [Q(int(i==a)-int(i==b)) for i in range(9)]

def exact_rank(A):
    B=[list(row) for row in A]
    if not B: return 0
    m,n=len(B),len(B[0]);r=0
    for c in range(n):
        p=next((i for i in range(r,m) if B[i][c]),None)
        if p is None: continue
        B[r],B[p]=B[p],B[r]
        v=B[r][c];B[r]=[x/v for x in B[r]]
        for i in range(m):
            if i!=r and B[i][c]:
                v=B[i][c];B[i]=[x-v*y for x,y in zip(B[i],B[r])]
        r+=1
        if r==m: break
    return r

def get_frames(s,w):
    return s['frames']+[x['frame'] for x in w.get('additional_charts',[])]

def replay_prefix(s,w,stop):
    frames=get_frames(s,w)
    n=1880
    rows=[{i:Q(1)} for i in range(n)]+[{} for _ in range(w['owned_fields'])]
    loc=list(w['initial'])+[None]*w['owned_fields']
    live=set(range(n))
    for t,o in enumerate(w['program'][:stop]):
        op,r=o[:2]
        need(0<=r<len(loc),f'field id {t}')
        if op=='INIT':
            need(r>=n and r not in live and loc[r] is None,f'fresh INIT {t}')
            rows[r]={};loc[r]=o[2];live.add(r)
        elif op=='CLEAR':
            need(r>=n and r in live and loc[r]==o[2],f'owned CLEAR {t}')
            live.remove(r);loc[r]=None;rows[r]={}
        elif op=='MOVE':
            a,b,owned=o[2:]
            need(r in live and loc[r]==a and type(owned)is bool and owned==(r>=n),f'MOVE source/ownership {t}')
            sa,sb=span(frames[a]),span(frames[b])
            need(sa<sb or (owned and sb<sa),f'nested MOVE {t}')
            loc[r]=b
        elif op=='SCALE':
            c=q(o[2]);need(c and r in live and loc[r]==o[3],f'SCALE {t}')
            rows[r]={i:c*v for i,v in rows[r].items() if c*v}
        else:
            need(op in ('ADD','COPY'),f'opcode {t}')
            src,c,chart=o[2],q(o[3]),o[4]
            need(r!=src and r in live and src in live and loc[r]==loc[src]==chart,f'cochart {t}')
            if op=='COPY': need(not rows[r],f'COPY_ZERO {t}')
            rows[r]=rowadd(rows[r],rows[src],c)
    return rows,loc,live

def full_type(s,w):
    frames=get_frames(s,w)
    loc=list(w['initial'])+[None]*w['owned_fields'];live=set(range(1880))
    owned_now=0;owned_peak=0;life=0;ops=Counter();moves=Counter();rawmoves=Counter();raw=set(w['private_role_map'].values())
    for t,o in enumerate(w['program']):
        op,r=o[:2];ops[op]+=1
        if op=='INIT':
            need(r>=1880 and r not in live and loc[r] is None,f'full INIT {t}')
            loc[r]=o[2];live.add(r);owned_now+=1;life+=1;owned_peak=max(owned_peak,owned_now)
        elif op=='CLEAR':
            need(r>=1880 and r in live and loc[r]==o[2],f'full CLEAR {t}')
            live.remove(r);loc[r]=None;owned_now-=1
        elif op=='MOVE':
            a,b,own=o[2:]
            need(r in live and loc[r]==a and own==(r>=1880),f'full MOVE source/owner {t}')
            need(span(frames[a])<span(frames[b]) or own and span(frames[b])<span(frames[a]),f'full MOVE nesting {t}')
            rk=abs(len(frames[a])-len(frames[b]));moves[rk]+=1
            if r in raw: rawmoves[rk]+=1
            loc[r]=b
        elif op=='SCALE':
            need(r in live and loc[r]==o[3] and q(o[2]),f'full SCALE {t}')
        else:
            need(op in ('ADD','COPY') and r in live and o[2] in live and loc[r]==loc[o[2]]==o[4],f'full ADD/COPY {t}')
    need(live==set(range(1880)) and owned_now==0 and all(loc[i] is not None for i in range(1880)),'all originals retained, owned retired')
    return ops,moves,rawmoves,owned_peak,life,loc

s=load(SRC);p=load(PARENT);parent_result=load(PARENT.parent/'RESULT.json')
need(sha(SRC.read_bytes())==PIN_SRC,'native pin')
need(sha(PARENT.read_bytes())==PIN_PARENT,'parent pin')
raw={int(k):v for k,v in p['private_role_map'].items()}
host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
order=list(host);K=[j for g in p['cyclic_dual']['source_groups'] for kind in ('B','S','T') for j in g[kind]]
need(len(order)==96 and len(K)==22 and len(set(K))==22,'96 roles / 22 closed ports')
at=p['marks']['common_starts']
rows,loc,live=replay_prefix(s,p,at)
C={i:{j:Q(i==j)+rows[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order} for i in order}
M=[[C[i][j] for j in order] for i in order]
need(exact_rank(M)==82,'actual parent residual rank 82')
outside=[i for i in order if i not in K]
need(len(outside)==74,'74 complement roots')
need(all(C[i][j]==0 for i in K for j in outside),'actual M[K,Kc]=0')
need(all(C[i][j]==Q(i==j) for i in outside for j in outside),'actual M[Kc,Kc]=I74')
need(exact_rank([[C[i][j] for j in K] for i in K])==8,'actual M[K,K] rank8')
roots={i:root9(s['frames'][s['initial'][i]][0]) for i in order}
G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2
need(all(C[i][j]==G(i,j) for i in K for j in K),'current M[K,K] equals independently rebuilt real-root Gram block')
for j in order:
    d=host[j][1];F=s['final'][d];rd=raw[d]
    need(loc[rd]==F and rows[rd]=={rd:Q(1),d:Q(-1)},f'all96 authentic D endpoints at cyclic boundary: {j}')
for i in order: need(loc[raw[host[i][0]]]==127,f'all96 current B rows at Hub: {i}')

# Parent lifetime and raw route invoice, independently counted.
p_ops,p_moves,p_raw,p_peak,p_life,p_final=full_type(s,p)
receipts=[]
for label,path in CASES.items():
    w=load(path);res=load(path.parent/'RESULT.json')
    need(w['parent_word_sha256']==PIN_PARENT,'candidate parent id '+label)
    need(sha(path.read_bytes())==res['word_sha256'],'candidate gzip checksum '+label)
    cand_at=w['marks']['common_starts'];patch=w['program'][at:cand_at]
    need(w['program'][:at]==p['program'][:at],'literal old prefix '+label)
    need(w['program'][cand_at:]==p['program'][at:],'literal old suffix '+label)
    J=w['cyclic_direct_returns']['selected_return_ports']
    expected_returns={'22':22,'31':31,'58':31}[label]
    need(len(J)==expected_returns and len(set(J))==len(J) and set(J)<=set(order),'selected indices '+label)
    if label in ('22','31'): need(set(K)<=set(J),'all K columns returned '+label)
    if label=='58': need(len(set(K)&set(J))==7 and len(set(J)-set(K))==24,'B7 plus 24 outside returns')
    # Check exact emitted sequence against actual, independently computed M columns.
    slot=1880+p['owned_fields'];cursor=0;nonzero=0;new_moves=[]
    for j in J:
        d=host[j][1];F=s['final'][d];rd=raw[d]
        need(loc[rd]==F and rows[rd]=={rd:Q(1),d:Q(-1)},f'original d{j} at exact facet')
        expected=[['INIT',slot,F],['ADD',slot,rd,'1',F],['MOVE',slot,F,127,True]]
        col=[i for i in order if C[i][j]];nonzero+=len(col)
        for i in col: expected.append(['ADD',raw[host[i][0]],slot,str(-C[i][j]),127])
        expected.append(['CLEAR',slot,127])
        new_moves.append((F,127))
        actual=patch[cursor:cursor+len(expected)]
        need(actual==expected,f'full actual M[:,{j}] correction sequence')
        cursor+=len(expected)
    need(cursor==len(patch),'no omitted or extra patch operations')
    parent_move_pairs={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'}
    need(all(pair in parent_move_pairs for pair in new_moves),'every charged return uses an inherited actual chart pair')
    # Fresh full input-coordinate replay to the new boundary.
    after,loc2,live2=replay_prefix(s,w,cand_at)
    need(loc2[:len(loc)]==loc and live2==live,'restored old locations/lifetimes at boundary')
    need(all(after[i]=={i:Q(1)} and loc2[i]==w['initial'][i] for i in range(1480)),'1480 common input identities')
    for j in J:
        d=host[j][1];rd=raw[d]
        need(loc2[rd]==s['final'][d] and after[rd]=={rd:Q(1),d:Q(-1)},f'd{j} preserved at facet')
    M2=[[Q(i==j)+after[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order] for i in order]
    E=[[Q(0) if j in J else C[i][j] for j in order] for i in order]
    need(M2==E,'candidate residual equals M with selected columns zeroed '+label)
    completed=[i for i,row in zip(order,M2) if not any(row)]
    expected_completed=set(res['completed_hosted_reverse_ports'])
    need(set(completed)==expected_completed,'actual zero rows equal receipt completion list '+label)
    need(exact_rank(M2)==res['hosted_reverse_residual_rank'],'exact residual rank '+label)
    if label in ('22','31'): need(set(completed)==set(J),'K-containing row completion control '+label)
    if label=='58':
        need(len(completed)==24 and set(completed)==set(J)-set(K),'rank58 B7+24 completion pattern')
        remK=[j for j in K if j not in J]
        need(exact_rank([[C[i][j] for j in remK] for i in K])==8,'remaining K columns retain rank8')
    # Each changed B port is consumed only at its own existing common recoupling.
    for i in order:
        if any(C[i][j] for j in J):
            b=raw[host[i][0]]
            uses=[o for o in w['program'][cand_at:] if o[1]==b or o[0] in ('ADD','COPY') and o[2]==b]
            need(uses==[['ADD',b,host[i][0],'1',s['final'][host[i][0]]]],f'only own final B recoupling for {i}')
    ops,moves,rawmoves,peak,life,final=full_type(s,w)
    need(rawmoves==p_raw,'no raw transport changed '+label)
    need(final[:len(p_final)]==p_final and all(x is None for x in final[len(p_final):]),'all final locations restored; only added slot is retired '+label)
    need(peak==p_peak==43,'peak ownership unchanged '+label)
    need(life==p_life+len(J),'one reused slot, |J| real lifetimes '+label)
    need(moves==p_moves+Counter({1:len(J)}),'only |J| new rank-one moves '+label)
    need(ops['ADD']-p_ops['ADD']==len(J)+nonzero,'all coefficient ADDs billed '+label)
    need(ops['INIT']-p_ops['INIT']==len(J) and ops['CLEAR']-p_ops['CLEAR']==len(J),'all owned copies retired '+label)
    # A source-facing control: incomplete K-only correction leaves external L terms.
    if label=='31':
        Jextra=[j for j in J if j not in K]
        need(len(Jextra)==9 and Jextra==outside[:9],'the nine extras are first 9 complement coordinates')
        need(any(C[i][j] for i in Jextra for j in K),'some added rows have nonzero inherited L entries')
    if label=='58':
        Jextra=[j for j in J if j not in K]
        Bframe=[5,56,69,100,65,77,96,103]
        need(set(J).intersection(K)==set(Bframe)-{5},'rank58 choice is B7 (the eight B roots except port5)')
        need(len(Jextra)==24 and all(C[i][j]==Q(i==j) for i in order for j in Jextra),'24 outside returns are exact identity columns')
        restK=set(K)-set(J)
        need(all(C[i][j]==0 for i in Jextra for j in restK),'all 24 completed outside rows have zero residual on unrecovered K columns')
        need(all(C[i][j]==0 for i in order if i not in K for j in set(K)-set(Bframe)),'external L block is supported only on the 8 B-frame columns')
        need(all(C[i][5]==0 for i in Jextra),'selected outside endpoints have zero L coefficient at missing B port5')
    # Exact tariff/premium arithmetic from the pinned full profiles.
    P={int(k):v for k,v in parent_result['conditional_caller']['P_partial'].items()}
    T={int(k):v for k,v in parent_result['conditional_caller']['T4'].items()}
    P[1]=P.get(1,0)+18*len(J)
    lower=upper=Q(0)
    surplus=0
    for rk in set(P)|set(T):
        c=T.get(rk,0)-P.get(rk,0);surplus+=rk*c
        a,b=power_interval(rk)
        if c>=0: lower+=c*a;upper+=c*b
        else: lower+=c*b;upper+=c*a
    lower/=18;upper/=18
    authored=res['conditional_caller']
    need(str(lower)==authored['remaining_moment_per_native_lower'] and str(upper)==authored['remaining_moment_per_native_upper'],f'exact full rank-199/200 tariff interval {label}')
    need(surplus==authored['rank_surplus'],f'exact rank surplus {label}')
    need(lower>0,'positive partial margin remains '+label)
    receipts.append({'case':label,'candidate_sha256':sha(path.read_bytes()),'selected_returns':len(J),'completed_rows':len(completed),'parent_residual_rank':82,'new_residual_rank':exact_rank(M2),'nonzero_full_column_terms':nonzero,'new_ADD':len(J)+nonzero,'all_new_facet_to_Hub_chart_pairs_inherited':True,'new_INIT_CLEAR_each':len(J),'new_rank1_MOVEs':len(J),'new_owned_move_price':len(J),'peak_owned':peak,'all_D_restored':True,'all1480_common_identity_rows':True,'suffix_literal':True,'all_old_raw_move_counts_retained':True,'added_paid_positions':18*len(J),'rank_surplus_after':surplus,'remaining_moment_per_native_lower':str(lower),'remaining_moment_per_native_upper':str(upper)})

print(json.dumps({'status':'PASS_INDEPENDENT_FULL_COLUMN_RETURN_AUDIT','source_sha256':PIN_SRC,'parent_sha256':PIN_PARENT,'parent_residual_rank':exact_rank(M),'K':K,'K_principal_rank':8,'M_K_Kc_is_zero':True,'M_Kc_Kc_is_identity':True,'cases':receipts},indent=2))
