#!/usr/bin/env python3
"""Actual same-minus two-stage correction, summing every intermediate port."""
import argparse, gzip, hashlib, itertools, json, random
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)
def dot(a,b):return (a&b).bit_count()%2
def apply(cols,x):
    z=0
    while x:
        bit=x&-x;z^=cols[bit.bit_length()-1];x^=bit
    return z
def rank(xs):
    basis={}
    for x in xs:
        while x:
            b=x.bit_length()-1
            if b in basis:x^=basis[b]
            else:basis[b]=x;break
    return len(basis)
def basis(xs):
    out=[]
    for x in xs:
        if rank(out+[x])>len(out):out.append(x)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--routes',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    pins={'source':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336','routes':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a'}
    for k,p in [('source',a.source),('routes',a.routes)]:need(hashlib.sha256(p.read_bytes()).hexdigest()==pins[k],k+' pin')
    w=json.loads(gzip.decompress(a.source.read_bytes()));rr=json.loads(a.routes.read_text())
    m=w['logical_involution'];ports=m['ports'];q={int(h):x for h,x in m['normals'].items()};R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in m['R_rows'].items()};rec={(x['stage'],x['port']):x for x in rr['route_records']}
    def perm(s,h,x):
        out=x
        for k,b in enumerate(rec[s,h]['orthogonal_complement']):
            z=b^(1<<(9+8*(s-1)+k))
            if dot(z,x):out^=z
        return out
    def path(h,k,j,s=1,t=2):
        def f(x):
            x=perm(t,h,x^rec[t,h]['output_translation'])
            x=perm(t,k,x)^rec[t,k]['output_translation']
            x^=q[k]
            x=perm(s,k,x)^rec[s,k]['input_translation']
            return perm(s,j,x^rec[s,j]['input_translation'])
        off=f(0);cols=tuple(f(1<<i)^off for i in range(25))
        need(all(dot(u,v)==int(i==j)for i,u in enumerate(cols)for j,v in enumerate(cols)),'actual core path orthogonal')
        need(all(f((1<<i)^(1<<j))==cols[i]^cols[j]^off for i in range(25)for j in range(i)),'actual affine path')
        return cols,off
    blocks={}
    for h in ports:
        for k,u in R[h].items():
            for j,v in R[k].items():
                key=path(h,k,j);blocks.setdefault((h,j),defaultdict(F))[key]+=u*v
    blocks={ij:{k:c for k,c in data.items()if c}for ij,data in blocks.items()if any(data.values())}
    need(len(blocks)==448 and all(len(v)==4 and all(abs(c)==F(1,4)for c in v.values())for v in blocks.values()),'all actual four paths survive after complete grouping')
    rng=random.Random(12014)
    candidates=[0]+[1<<i for i in range(25)]+[(1<<i)^(1<<j)for i in range(25)for j in range(i)]+[rng.randrange(1<<25)for _ in range(256)]
    certificates=[];codim_hist=defaultdict(int)
    for h in ports:
        def planes(x):
            data=[]
            for (hh,j),terms in blocks.items():
                if hh!=h:continue
                one=[]
                for (cols,off),c in terms.items():
                    base=apply(cols,x)^off;u=apply(cols,q[h]);v=q[j]
                    pp=sorted({base,base^u,base^v,base^u^v})
                    need(len(pp)==4,'independent Gaussian translation pair')
                    one.append((pp,str(c)))
                data.append({'input_port':j,'planes':one})
            return data
        good=None
        for x in candidates:
            data=planes(x)
            if all(len(set(itertools.chain.from_iterable(z[0]for z in d['planes'])))==16 for d in data):good=(x,data);break
        need(good is not None,'certified full-row separator')
        # A collision is an affine condition. Codimension follows from projecting
        # the difference of the two linear maps modulo the two plane directions.
        pairs=[]
        for (hh,j),terms in blocks.items():
            if hh!=h:continue
            tt=list(terms)
            for ii in range(4):
                for jj in range(ii):
                    (f,u),(g,v)=tt[ii],tt[jj]
                    directions=basis([apply(f,q[h]),apply(g,q[h]),q[j]])
                    differences=[x^y for x,y in zip(f,g)]
                    codim=rank(directions+differences)-len(directions)
                    consistent=rank(directions+differences+[u^v])==len(directions)+codim
                    need(codim>=1 or not consistent,'proper or empty collision affine set')
                    codim_hist[str(codim)if consistent else'empty']+=1
                    pairs.append({'input_port':j,'term_pair':[ii,jj],'codimension':codim,'consistent':consistent})
        need(len(pairs)==24,'24 within-port possible path collisions')
        certificates.append({'output_port':h,'spatial_row':good[0],'input_blocks':good[1],'collision_pairs':pairs})
    result={'status':'PASS_ACTUAL_TWO_STAGE_CORRECTION_SUPPORT','operator':'C_st=Q^-1 Rprime_t Q^2 R_s Q, s=1,t=2','source_pins':pins,'nonzero_blocks':len(blocks),'paths_per_block':4,'certificates':certificates,'collision_codimension_histogram':dict(codim_hist),'full_row_support':'16*4^V on a fraction at least max(0,1-24*2^-V) of spatial rows at each output port','entry_magnitude_on_good_rows':'2^(-V-2)','normalized_entropy_lower_bound':'112*b*max(0,1-24*2^-V)*(2V+4)','scope':'Actual distinct-stage route family. Every intermediate path retained. Universal collision-product argument still requires critical proof review. No general nonunitary or different caller impossibility.'}
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in['certificates','source_pins']}))

if __name__=='__main__':main()
