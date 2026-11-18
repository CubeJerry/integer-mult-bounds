#!/usr/bin/env python3
"""Distinct exhaustive F2 and F3 controls for invertible source lifting."""
from itertools import product
from pathlib import Path
import argparse, json

def add(x,y,p): return tuple((a+b)%p for a,b in zip(x,y))
def scale(c,x,p): return tuple(c*a%p for a in x)
def span(columns,q,p):
    result={tuple(0 for _ in range(q))}
    for column in columns:
        result={add(x,scale(c,column,p),p) for x in result for c in range(p)}
    return result
def linear(columns,x,q,p):
    y=tuple(0 for _ in range(q))
    for c,v in zip(x,columns): y=add(y,scale(c,v,p),p)
    return y
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();census=[]
    for p in (2,3):
        vectors2=list(product(range(p),repeat=2))
        automorphisms=[E for E in product(vectors2,repeat=2) if len(span(E,2,p))==p*p]
        if len(automorphisms)!=(p*p-1)*(p*p-p): raise ValueError('GL2 census')
        for q in (1,2):
            vectors=list(product(range(p),repeat=q))
            for c in (0,1):
                accepted=rejected=0
                for Te in product(vectors,repeat=2):
                    for Tl in product(vectors,repeat=c):
                        iml=span(Tl,q,p)
                        def coset(v): return min(add(v,u,p) for u in iml)
                        imageA={coset(v) for v in span(Te,q,p)};attainable=set()
                        for E in automorphisms:
                            mapped=[linear(Te,x,q,p) for x in E]
                            for shifts in product(iml,repeat=2):
                                attainable.add(tuple(add(x,y,p) for x,y in zip(mapped,shifts)))
                        for R in product(vectors,repeat=2):
                            criterion=imageA=={coset(v) for v in span(R,q,p)};actual=R in attainable
                            if criterion!=actual: raise ValueError(('quotient-image disagreement',p,q,c,Te,Tl,R))
                            accepted+=actual;rejected+=not actual
                census.append({'field':p,'q':q,'late_columns':c,'accepted':accepted,'rejected':rejected})
    result={'status':'PASS_INDEPENDENT_F2_F3_SOURCE_LIFTING','cases':sum(x['accepted']+x['rejected'] for x in census),'census':census,'universal_proof':'Equal quotient images identify two surjections; match kernel bases and lifts to construct E, then lift each residual column through Tl. Finite controls corroborate rather than replace this argument.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['cases'])
if __name__=='__main__': main()
