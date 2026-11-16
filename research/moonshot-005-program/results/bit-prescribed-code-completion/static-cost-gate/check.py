"""Source heights and rigorous rational budget for the frozen-prefix gate."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
from decimal import Decimal,localcontext
import argparse, hashlib, json, sys

def rr(rows):
    a=[list(map(Fraction,r)) for r in rows];k=0
    for j in range(8):
        q=next((q for q in range(k,len(a)) if a[q][j]),None)
        if q is None:continue
        a[k],a[q]=a[q],a[k];z=a[k][j];a[k]=[x/z for x in a[k]]
        for q in range(len(a)):
            if q!=k and a[q][j]:
                z=a[q][j];a[q]=[x-z*y for x,y in zip(a[q],a[k])]
        k+=1
    return k
def reduce(x,B):
    for p,y in sorted(B.items(),reverse=True):
        if x>>p&1:x^=y
    return x
def basis(rows):
    B={}
    for x in rows:
        x=reduce(x,B)
        if x:B[x.bit_length()-1]=x
    return B

def main():
    p=argparse.ArgumentParser();p.add_argument('--word',type=Path,required=True)
    p.add_argument('--seed',type=Path,required=True);p.add_argument('--engine',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=a.word.read_bytes();assert hashlib.sha256(data).hexdigest()=='a82d3f9283fb770377981b9f20b384639aaf135dbdc0046db4852f7f0df6f46d'
    w=json.loads(data);seed=json.loads(a.seed.read_text());S=[int(x,16) for x in seed['seed_rows']]
    Z=[1,3,4,6,18,21,61,64,65,73,74,75,76,77,78,79,80]
    B=basis(S+[1<<j for j in Z]);qpoints={reduce(1<<j,B) for j in range(111)}
    dims={k:(rr(v['rows']) if v['kind']=='span' else 8-rr(v['rows'])) for k,v in w['charts'].items()}
    val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':0 for j in range(111)}
    at={f'X{j}':f'L{j}' for j in range(111)}|{f'Y{j}':'zero' for j in range(111)}
    owners=set();cut=w['milestones']['seed8_before_Y'];suffix_owned_moves=0;low_nonpoint=[];heights=None
    for step,o in enumerate(w['operations'],1):
        if o[0]=='INIT':_,n,c=o;val[n]=0;at[n]=c;owners.add(n)
        elif o[0]=='ADD':_,s,n=o;val[n]^=val[s]
        elif o[0]=='MOVE':
            _,n,c=o
            if step>cut and n in owners:suffix_owned_moves+=1
            at[n]=c
        elif o[0]=='CLEAR':_,n=o;del val[n];del at[n];owners.remove(n);continue
        if 0<dims[at[n]]<5 and reduce(val[n],B) not in qpoints|{0}:low_nonpoint.append([step,n,at[n]])
        if step==cut:heights=Counter(dims[at[n]] for n in val if dims[at[n]]>0)
    assert suffix_owned_moves==0 and low_nonpoint==[]
    assert dict(heights)=={5:16,6:21,7:21,8:102}
    sys.path.insert(0,str(a.engine));from budget import budget,moment
    profile={1:58,2:56,3:36,4:35,5:69,6:19,7:106,8:1}
    invoice=budget(profile)
    five=moment({5:1});lower=Fraction(4)+five[0];upper=Fraction(4)+five[1]
    room_upper=Fraction(invoice['limiting_room']['upper_fraction'])
    excess=lower-room_upper;assert excess>0
    with localcontext() as ctx:
        ctx.prec=60
        show=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
        displays={'mixed_lower_bound_lower':show(lower),'room_upper':show(room_upper),'excess_lower':show(excess)}
    out={'status':'PASS_FROZEN_PREFIX_SOURCE_HEIGHTS','word_sha256':hashlib.sha256(data).hexdigest(),
         'seed_cut_positive_heights':dict(heights),'owned_moves_after_seed_cut':suffix_owned_moves,
         'low_chart_values_outside_baseline_and_one_point':low_nonpoint,
         'mixed_lower_bound_exact_interval':[str(lower),str(upper)],'excess_lower_fraction':str(excess),
         'decimal_displays':displays,'invoice':invoice,
         'scope':'Static linear whole-record common broadcast; no extra free feedback; frozen routes and values; raw-point or high-origin imports only',
         'new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])
if __name__=='__main__':main()
