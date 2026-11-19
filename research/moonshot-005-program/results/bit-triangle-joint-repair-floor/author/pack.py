#!/usr/bin/env python3
"""Exact cut-witness selection; this consumes separately extracted spaces."""
import argparse, gzip, json
from pathlib import Path

def mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        b>>=1;a<<=1
        if a&32:a^=0x25
    return out
T=[[mul(a,b) for b in range(32)] for a in range(32)]
INV=[0]+[next(b for b in range(1,32) if mul(a,b)==1) for a in range(1,32)]
def add(basis,vector):
    row=vector[:]
    for p,old in sorted(basis.items()):
        if row[p]:
            tab=T[row[p]];row=[x^tab[y] for x,y in zip(row,old)]
    p=next((i for i,x in enumerate(row) if x),None)
    if p is None:return False
    tab=T[INV[row[p]]];basis[p]=[tab[x] for x in row];return True
def rank(rows):
    basis={}
    for row in rows:add(basis,row)
    return len(basis)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('spaces',type=Path);ap.add_argument('out',type=Path);a=ap.parse_args()
    data=json.load(gzip.open(a.spaces,'rt'))
    if isinstance(data,dict):
        print('keys',list(data),flush=True)
        data=data.get('spaces',data.get('D_spaces',data.get('entries')))
    spaces={}
    for e in data:
        columns=[]
        for c,cols in e['class_columns'].items():
            for col in cols:
                v=[0]*240;v[48*int(c):48*(int(c)+1)]=col;columns.append(v)
        spaces[e['receiver'],e['middle']]=columns
    witnesses=[]
    for i in sorted({i for i,d in spaces}):
        remaining={d:v for (j,d),v in spaces.items() if j==i};basis={};chosen=[];steps=[]
        while remaining:
            best=None
            for d,cols in remaining.items():
                trial={p:r[:] for p,r in basis.items()}
                for col in cols:add(trial,col)
                key=(len(trial)-len(basis)-4,-d)
                if best is None or key>best[0]:best=(key,d,trial)
            if best[0][0]<=0:break
            _,d,basis=best;del remaining[d];chosen.append(d)
            steps.append([d,len(basis),4*len(chosen),len(basis)-4*len(chosen)])
        assert rank([col for d in chosen for col in spaces[i,d]])==len(basis)
        row={'receiver':i,'middles':chosen,'rank':len(basis),'capacity':4*len(chosen),'extra_symbols_per_stripe':len(basis)-4*len(chosen),'steps':steps}
        witnesses.append(row);print(json.dumps(row),flush=True)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'PACKING.json').write_text(json.dumps({'witnesses':witnesses,'optimality_claimed':False},indent=2)+'\n')
if __name__=='__main__':main()
