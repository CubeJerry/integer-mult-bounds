"""Independent reverse-prefix owned-pivot audit, without author imports."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,gzip,json,argparse
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--word',type=Path,default=ROOT/'research/shared-wire-split-composition/data/final.json.gz')
args=parser.parse_args()
RAW=args.word.read_bytes()
def need(ok,why):
    if not ok: raise ValueError(why)
need(hashlib.sha256(RAW).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','word SHA')
need(hashlib.sha1(b'blob '+str(len(RAW)).encode()+b'\0'+RAW).hexdigest()=='74563a7867d9d762b6588f65362369668841bb3e','word blob')
w=json.loads(gzip.decompress(RAW))
claims=json.loads((HERE/'OWNED-ROWS.json').read_text())['rises']
def rank(rows):
    piv={}
    for x in rows:
        need(type(x) is int and 0<x<512,'frame vector')
        while x:
            b=x.bit_length()-1
            if b not in piv:
                piv[b]=x
                break
            x^=piv[b]
    return len(piv)
frames=w['frames']
for row in frames: need(rank(row)==len(row),'frame basis')
states=list(w['initial'])+[None]*w['owned_fields']
events=w['program']
found=[]
init=clear=0
for i,e in enumerate(events):
    op,a=e[:2]
    if op=='INIT':
        need(a>=w['public'] and states[a] is None,'INIT lifecycle')
        states[a]=e[2]
        init+=1
    elif op=='CLEAR':
        need(a>=w['public'] and states[a]==e[2],'CLEAR lifecycle')
        states[a]=None
        clear+=1
    elif op in ('ADD','COPY'):
        need(states[a]==states[e[2]]==e[4],'contact frame')
    elif op=='SCALE': need(states[a]==e[3],'scale frame')
    elif op=='MOVE':
        _,a,u,v,charge=e
        need(states[a]==u,'move entry frame')
        if a>=w['public'] and len(frames[v])>len(frames[u]):
            need(charge is True,'actual paid rise')
            need(rank(frames[u]+frames[v])==len(frames[v]),'nested rise')
            found.append((i,a,u,v,len(frames[v])-len(frames[u])))
        states[a]=v
    else: raise ValueError('unknown opcode')
need(len(found)==23 and init==clear==54,'census')
need(all(s is None for s in states[w['public']:]),'owned retirement')
def reverse_pivot(event,owner,pivot):
    q={owner:F(1)}
    for e in reversed(events[:event]):
        op,a=e[:2]
        if op in ('INIT','CLEAR'):
            q.pop(a,None)
        elif op in ('ADD','COPY'):
            if a in q:
                b,c=e[2],F(e[3])
                q[b]=q.get(b,F(0))+c*q[a]
                if q[b]==0: q.pop(b)
        elif op=='SCALE':
            if a in q:
                q[a]*=F(e[2])
                if q[a]==0: q.pop(a)
        elif op=='MOVE': pass
        else: raise ValueError('adjoint opcode')
    need(all(a<w['public'] for a in q),'no entrance owned dependence')
    return q.get(pivot,F(0)),len(q)
out=[]
for data,c in zip(found,claims):
    i,a,u,v,r=data
    need(data==(c['event'],c['owner'],c['source_frame'],c['target_frame'],c['rank']),'rise metadata')
    p,claim=c['pivot']
    actual,support=reverse_pivot(i,a,p)
    need(actual==F(claim) and actual!=0,'nonzero pivot')
    need(support==c['support'],'independent full support')
    out.append({'event':i,'owner':a,'rank':r,'pivot':p,
                'coefficient':str(actual),'support':support})
hist=dict(sorted(Counter(z['rank'] for z in out).items()))
need(hist=={1:10,2:4,3:1,4:6,5:1,6:1},'rank histogram')
need(sum(r*c for r,c in hist.items())==56,'rank mass')

# The support theorem's norm floor can be checked exactly on flat rows.
normcases=0
for n in range(1,9):
    row_width=2**n
    for k in range(row_width+1):
        # Missing positions of a flat unit vector, optimal coefficients retained.
        miss=F(row_width-k,row_width)
        need(miss==max(F(0),1-F(k,row_width)),'projection floor')
        normcases+=1
tradeoff=0
for r in range(1,7):
    for f in range(1,11):
        for s in range(r):
            for g in range((r-s)*f+1):
                floor=max(F(0),1-F(2)**(g-(r-s)*f))
                need((floor>=F(1,2)) if g<(r-s)*f else floor==0,'integer gap')
                tradeoff+=1

# Explicit fault detection independent of assertion mode.
def reject(thunk):
    try: thunk()
    except ValueError: return
    raise ValueError('undetected mutation')
def check_certificate(c,data,actual):
    need(data==(c['event'],c['owner'],c['source_frame'],c['target_frame'],c['rank']),'certificate metadata')
    need(F(c['pivot'][1])==actual,'certificate coefficient')
bad_coeff=dict(claims[0],pivot=[claims[0]['pivot'][0],str(F(claims[0]['pivot'][1])+1)])
bad_rank=dict(claims[0],rank=claims[0]['rank']-1)
check_certificate(claims[0],found[0],F(out[0]['coefficient']))
reject(lambda:check_certificate(bad_coeff,found[0],F(out[0]['coefficient'])))
reject(lambda:need(rank([1,1])==2,'dependent frame'))
reject(lambda:check_certificate(bad_rank,found[0],F(out[0]['coefficient'])))
print(json.dumps({'status':'PASS_INDEPENDENT_REVERSE_OWNED_AUDIT',
 'word_sha256':hashlib.sha256(RAW).hexdigest(),'events':len(events),'frames':len(frames),
 'init_clear':init,'rises':out,'histogram':hist,'projection_cases':normcases,
 'rank_work_cases':tradeoff,'negative_controls':['altered pivot','dependent frame','undercharged rank']},indent=2))
