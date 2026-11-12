"""H4-only packet tariff and typed conditional reverse-eight completion."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip,hashlib,json
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
D=10**30

def need(x,m):
    if not x: raise ValueError(m)
def root(n,k=200):
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x: break
        x=y
    while (x+1)**k<=n: x+=1
    while x**k>n: x-=1
    need(x**k<=n<(x+1)**k,'root bracket');return x
def span(f):
    s={0}
    for b in f: s.update(x^b for x in tuple(s))
    return s
def plus(a,b,c=F(1)):
    for k,v in b.items():
        z=a.get(k,F(0))+c*v
        if z: a[k]=z
        else: a.pop(k,None)
def portrow(v):
    S=[j for j in range(9) if v>>j&1]
    if len(S)==3:return [2*int(j in S) if 8 in S else (1 if j in S else -1) for j in range(8)]
    need(len(S)==7,'port weight');i,j=[j for j in range(9) if j not in S]
    return [2*int(k==i)-2*int(k==j) if j<8 else (1 if k==i else -1) for k in range(8)]
def main(a):
    sb=a.source.read_bytes();ib=a.invoice.read_bytes();need(hashlib.sha256(sb).hexdigest()==PIN,'native pin');need(hashlib.sha256(ib).hexdigest()==IPIN,'H4 invoice pin')
    w=json.loads(gzip.decompress(sb));invoice=json.loads(ib);T={int(k):v for k,v in invoice['T4'].items()};P0={int(k):v for k,v in invoice['P4'].items()}
    M=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));q={j:1480+i for i,j in enumerate(M)}
    need(len(M)==400 and sum(e[0]=='MOVE' for e in w['program'])==6310,'native common census')
    need(sum(e[0]=='MOVE' and e[1] in M for e in w['program'])==1710,'raw route census')
    ranks=set(T)|set(P0)|set(range(1,10));bounds={}
    for r in ranks:
        n=r**199*D**200;lo=root(n);bounds[r]=(lo,lo if lo**200==n else lo+1)
    moment=lambda h:tuple(sum(n*bounds[r][i] for r,n in h.items()) for i in (0,1))
    tlo,thi=moment(T);profiles={}
    for name,added in [('H4_no_second_owned',{}),('eight_rank9_packets',{9:8}),('eight_packets_and_reverse_eight',{9:8,1:8}),('two_independent_eight_packet_trips_and_reverse_eight',{9:16,1:8})]:
        paid=Counter(P0);paid.update({r:18*v for r,v in added.items()});plo,phi=moment(paid);lo,hi=tlo-phi,thi-plo;caps={}
        for r in range(1,10):
            if lo<0:caps[r]=None;continue
            cap=lo//(18*bounds[r][1]);need((cap+1)*18*bounds[r][0]>hi,'strict maximum');caps[r]=cap
        profiles[name]={'new_routes_per_native':added,'paid_histogram':dict(sorted(paid.items())),'paid_count':sum(paid.values()),'target_count':sum(T.values()),'rank_surplus':sum(r*n for r,n in T.items())-sum(r*n for r,n in paid.items()),'margin_numerator_bounds':[str(lo),str(hi)],'margin_denominator':str(D),'per_native_headroom_denominator':str(18*D),'max_further_uniform_rank_calls':caps}
    need(int(profiles['eight_packets_and_reverse_eight']['margin_numerator_bounds'][0])>19*18*D,'positive conditional remainder')
    need(int(profiles['two_independent_eight_packet_trips_and_reverse_eight']['margin_numerator_bounds'][1])<0,'independent return trip fails target')
    # Verify a new physical macro, conditional on all forward residuals removed.
    coupled=[(i,x,x+112) for i,x in enumerate(w['live']) if i not in set(w['hosted']['Dports'])]
    need(len(coupled)==8,'coupled eight');loc={j:w['final'][j] for j in range(1480)}
    loc.update({q[j]:w['final'][j] for j in M});rows={j:{j:F(1)} for j in range(1880)}
    for i,x,y in coupled:
        need(loc[q[x]]==127 and len(w['frames'][loc[q[y]]])==8,'reverse endpoint charts')
        rows[q[y]]={q[x]:F(1,2),q[y]:F(1,2)}
    expected={j:dict(r) for j,r in rows.items()}
    for _,x,y in coupled: expected[q[x]]={q[x]:F(1),q[y]:F(-1)}
    frames=list(map(span,w['frames']));program=[];tmp=1931;counts=Counter();peak=active=0
    for _,x,y in coupled:
        ch=w['final'][y];program += [['INIT',tmp,ch],['ADD',tmp,q[y],'1',ch],['MOVE',tmp,ch,127,True],['SCALE',q[x],'2',127],['ADD',q[x],tmp,'-2',127],['CLEAR',tmp,127]]
    for e in program:
        op,j=e[:2];counts[op]+=1
        if op=='INIT':need(j not in loc and 1880<=j<1932,'fresh owned');loc[j]=e[2];rows[j]={};active+=1;peak=max(peak,active)
        elif op=='ADD':need(loc[j]==loc[e[2]]==e[4],'cochart ADD');plus(rows[j],rows[e[2]],F(e[3]))
        elif op=='SCALE':need(loc[j]==e[3],'cochart SCALE');rows[j]={k:F(e[2])*v for k,v in rows[j].items()}
        elif op=='MOVE':
            need(e[4] and j>=1880 and loc[j]==e[2] and frames[e[2]]<=frames[e[3]],'owned nested MOVE')
            need(len(w['frames'][e[3]])-len(w['frames'][e[2]])==1,'rank1');loc[j]=e[3]
        elif op=='CLEAR':need(loc[j]==e[2] and j>=1880,'owned CLEAR');del loc[j];del rows[j];active-=1
    need(rows==expected and active==0 and peak==1,'all1880 macro endpoint rows')
    need(counts==Counter({'INIT':8,'ADD':16,'MOVE':8,'SCALE':8,'CLEAR':8}),'reverse ordinary invoice')
    A=[portrow(v) for v in w['ports']];G=[[sum(x*y for x,y in zip(a,b)) for b in A] for a in A]
    i,x,y=coupled[0];j=next(j for j in range(104) if i!=j and G[i][j]);error=F(-G[i][j],8)
    need(error!=0,'unrepaired prefix is not a valid reverse-macro input')
    macro={'schema':'conditional-reverse-eight/1','source_sha256':PIN,'public':1880,'owned_fields':52,'difference_role_map':q,'coupled_pairs':coupled,'program':program,'entry_contract':'RawX_i=qXi at hub; coupled RawY_i=(qXi+qYi)/2 at its final facet after all residuals are removed. Other public data unchanged. Common recovery and all uses of original qX complete before this macro.'}
    payload=(json.dumps(macro,sort_keys=True,separators=(',',':'))+'\n').encode();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.with_name('REVERSE-EIGHT.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    out={'status':'PASS_H4_ONLY_EXACT_TARIFF_AND_CONDITIONAL_REVERSE_EIGHT','source_sha256':PIN,'invoice_sha256':IPIN,'kappa':'1/200','power':'199/200','target_histogram':T,'native_repetitions':18,'common_native_MOVEs_retained':6310,'raw_main_MOVEs_retained':1710,'second_owned_reservations_retained':0,'power_bounds':{r:list(map(str,b)) for r,b in sorted(bounds.items())},'power_denominator':str(D),'profiles':profiles,'reverse_eight':{'operation_counts':dict(sorted(counts.items())),'public_rows_checked':1880,'peak_live_owned':1,'owned_lifetimes':8,'pairs_and_final_charts':[[x,y,w['final'][y]] for _,x,y in coupled],'payload_sha256':hashlib.sha256(payload).hexdigest(),'reject_unrepaired_prefix':{'target_X':x,'unresolved_donor_X':w['live'][j],'wrong_extra_coefficient':str(error)}},'scope':'H4 T4/P4 inherited conditional census; eight packet prefix has unpaid residual and hosted duties. Reverse macro composes only after residuals and original-qX-dependent restoration finish. Source word, suppliers, precision/ordinary closure and foundational obligations remain. No new kappa.'}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
    for name,p in profiles.items(): print(name,float(F(int(p['margin_numerator_bounds'][0]),18*D)),p['max_further_uniform_rank_calls'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--invoice',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
