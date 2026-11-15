#!/usr/bin/env python3
import argparse,hashlib,itertools,json
from pathlib import Path

def basis(vs):
 d={}
 for v in vs:
  while v:
   k=v.bit_length()-1
   if k in d:v^=d[k]
   else:d[k]=v;break
 return list(d.values())
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in list(s)}
 return s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();cases=[]
 for n in range(1,5):
  spaces={frozenset({0})}
  for v in range(1,1<<n):
   for s in list(spaces):spaces.add(frozenset(set(s)|{x^v for x in s}))
  for P in sorted(spaces,key=lambda s:(len(s),sorted(s))):
   for cut in range(n+1):
    masks=[(1<<cut)-1,((1<<n)-1)^((1<<cut)-1)];B=[]
    for mask in masks:B+=basis(v&mask for v in P)
    p=len(basis(P));t=len(B);E=[];Q=set(P)
    for b in B:
     if b not in Q:E.append(b);Q|={x^b for x in list(Q)}
    assert len(E)==t-p and Q==span(B);Es=span(E);Bs=[b for b in B if b not in E];pairs=[]
    for b in Bs:
     decomps=[(v,b^v)for v in P if b^v in Es];assert len(decomps)==1;pairs.append(decomps[0])
    assert span(v for v,e in pairs)==set(P)
    # Give every p-vector its actual arbitrary injective Hub lift (the same bits in a disjoint block), plus one independent Hub-kernel row.
    ker=1<<(2*n);principals=[(v<<n)^b for b,(v,e)in zip(Bs,pairs)]+[ker];helpers=E[:];first=principals+helpers;corrected=[x^e for x,(v,e)in zip(principals[:-1],pairs)]+[ker];K=basis([(v<<n)^v for v in P]+[ker]);c=p+1
    assert len(basis(first))==c+t-p and span(corrected)==span(K)
    cases.append({'held_dimension':n,'cut':cut,'projection_rank':p,'marginal_sum':t,'canonical_dimension':c,'helpers':len(E),'first_arrival_rank':len(basis(first))})
 out={'status':'PASS_EXACT_CHARTWISE_HELPER_REPAIR_CONTROLS','cases':cases,'case_count':len(cases),'nonseparable_cases':sum(x['helpers']>0 for x in cases),'scope':'Finite binary controls supplement general first-arrival-span theorem; source assembly not supplied.','hypothetical_five_receiver_interface':{'c':36,'p':36,'t':40,'Delta':4,'canonical_movement_coefficients_normalized':{'2':9,'6':10}},'new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(cases),'nonseparable':out['nonseparable_cases']}))
if __name__=='__main__':main()
