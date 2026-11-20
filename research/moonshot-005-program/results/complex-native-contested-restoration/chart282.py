"""Check the two-replacement experiment on the true chart-282 stock."""
from fractions import Fraction as Q
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'author'))
from graph import Graph,require
from packed import coefficient,PRIME
from rows import original_values

def pivot_columns(A,p):
    A=[row.copy()for row in A];m=len(A);n=len(A[0]);piv=[]
    for j in range(n):
        k=len(piv);i=next((i for i in range(k,m)if A[i][j]%p),None)
        if i is None:continue
        A[k],A[i]=A[i],A[k];v=pow(A[k][j],-1,p);A[k]=[(x*v)%p for x in A[k]]
        for i in range(k+1,m):
            v=A[i][j];A[i]=[(x-v*y)%p for x,y in zip(A[i],A[k])]
        piv.append(j)
        if len(piv)==m:break
    return piv

def det(A):
    if not A:return Q(1)
    return sum((-1)**i*row[0]*det([r[1:]for j,r in enumerate(A)if j!=i])for i,row in enumerate(A))

def run():
    g=Graph();V,_=original_values(g);unknown=[88959,88960,90369];survive=[90605,90604];allin=unknown+survive;tm={e:i for i,e in enumerate(g.schedule)}
    require(set(g.incoming[282])==set(allin),'entire literal receiver stock')
    bank=[[coefficient(V[e],j)for j in range(1289)]for e in allin];piv=pivot_columns(bank,PRIME)
    require(len(piv)==5,'five independent true input rows')
    D=int(det([[r[j]for j in piv]for r in bank]))%PRIME
    require(D,'positive rational rank certificate')
    clocks=sorted(g.outgoing[282],key=tm.get);rows=[[g.forms[e].get(j,Q(0))for j in unknown]for e in clocks]
    require(clocks==[89198,91110,98703,91131,94251] and max(map(tm.get,survive))<tm[clocks[0]],'protected reader order')
    require(det(rows[:3])==1,'three-direction unimodular minor')
    mrows=[[int(x.numerator)*pow(x.denominator,-1,PRIME)%PRIME for x in r]for r in rows]
    ranks=[len(pivot_columns(mrows[:i],PRIME))for i in range(1,6)];require(ranks==[1,2,3,3,3],'chronological quotient ranks')
    return {'status':'PASS_TWO_FUNDED_ARRIVALS_CANNOT_RESTORE_CHART_282','source_sha256':g.receipt['word_sha256'],'receiver':282,'retargeted_paid':90369,'two_changed_funded_legs':[88959,88960],'surviving_arrivals':[[e,tm[e]]for e in survive], 'all_original_stock_rank':5,'independence_minor':{'input_axes':piv,'determinant_mod_prime':D,'prime':PRIME},'quotient_coordinate_order':unknown,'reader_prefixes':[{'event':e,'clock':tm[e],'row':[str(x)for x in r],'rank':rk}for e,r,rk in zip(clocks,rows,ranks)],'first_three_determinant':1,'required_independent_replacements':3,'available_replacements':2,'scope':'Fixed original protected chart-282 readers and the stated two surviving stocks; external and jointly changed reader maps require their own certification.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(exist_ok=True,parents=True);r=run();(a.out/'CHART282.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
