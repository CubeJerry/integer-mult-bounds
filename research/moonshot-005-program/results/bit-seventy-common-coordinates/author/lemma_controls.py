#!/usr/bin/env python3
"""Exhaustive binary controls for the exact quotient-image lifting lemma."""
from argparse import ArgumentParser
from itertools import product
from pathlib import Path
import json

def need(q,msg):
    if not q:raise ValueError(msg)
def span(columns):
    out={0}
    for c in columns:out|={x^c for x in list(out)}
    return out
def lin(columns,v):
    r=0
    for i,c in enumerate(columns):
        if v>>i&1:r^=c
    return r
def main():
    p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();cases=0;hist={};positive=negative=0
    b=2;GL=[e for e in product(range(1<<b),repeat=b)if len(span(e))==1<<b];need(len(GL)==6,'GL2 count')
    for q,c in[(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),(3,0),(3,1),(3,2)]:
        n=1<<q;count=0
        for Te in product(range(n),repeat=b):
            for Tl in product(range(n),repeat=c):
                iml=span(Tl);normal=lambda x:min(x^z for z in iml);imageA=span([normal(x)for x in Te]);reachable=set()
                for E in GL:
                    ae=tuple(lin(Te,v)for v in E)
                    for additions in product(iml,repeat=b):reachable.add(tuple(x^y for x,y in zip(ae,additions)))
                for R in product(range(n),repeat=b):
                    criterion=imageA==span([normal(x)for x in R]);found=R in reachable;need(criterion==found,'exact quotient image iff invertible lift');cases+=1;count+=1;positive+=found;negative+=not found
        hist[f'q{q}_c{c}']=count
    # Column encodings: Te=I2, Tl=e0, and both rows of R equal the first input coordinate.
    Te=(1,2);Tl=(1,);R=(3,0);E=(3,1);L=(0,1)
    need(len(span(Tl))<4,'positive control late map not surjective');need(len(span(E))==4,'positive source E invertible')
    need(tuple(lin(Te,E[j])^lin(Tl,L[j])for j in range(2))==R,'positive augmented target control')
    badR=(1,0);need(span([min(x^z for z in span(Tl))for x in Te])!=span([min(x^z for z in span(Tl))for x in badR]),'negative quotient image mismatch')
    result={'status':'PASS_EXACT_QUOTIENT_IMAGE_LIFTING_CONTROLS','exhaustive_cases':cases,'positive_cases':positive,'negative_cases':negative,'case_histogram':hist,'positive_control_columns':{'T_e':Te,'T_l':Tl,'R':R,'E':E,'L':L},'negative_control_R_columns':badR,'source80_k71_mixed_input_deficit':61*71-4320,'source80_k70_mixed_input_slack':4320-61*70}
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
