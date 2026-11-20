"""Derive rational linear separating inputs for the 181 exterior cuts."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter,defaultdict
from fractions import Fraction as Q
from math import gcd,lcm
from pathlib import Path

def load(src):
    s=importlib.util.spec_from_file_location('p104_original',src/'7833-construction.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def exterior(g,w,shadow,donor,target):
    ids=[*g.inputs,*g.schedule];ix={e:i for i,e in enumerate(ids)};stock=defaultdict(int);reached=set()
    for e,a in g.inputs.items():stock[a]|=1<<ix[e]
    stock[282]|=1<<ix[shadow]
    for e in g.schedule:
        if e==shadow:continue
        if e==donor:reached.add(w.routes[donor][1]);continue
        a=g.source(e);dirty=a in reached;m=stock[a]if dirty else 1<<ix[e]
        if e==target:
            if not dirty:raise ValueError('target does not causally descend')
            out=[]
            while m:
                b=m&-m;out.append(ids[b.bit_length()-1]);m^=b
            return out
        if e in g.routes:
            b=g.routes[e][1];stock[b]|=m
            if dirty:reached.add(b)
    raise ValueError('absent terminal')

def derive(S,V,axes,fixed,target):
    freq=Counter(axis for i in fixed for axis in V[i][1]);order=sorted(range(axes),key=lambda j:(freq[j],j));priority={j:i for i,j in enumerate(order)};R=S.IntegerElimination(priority)
    for e in sorted(fixed,key=lambda i:(len(V[i][1]),i)):R.add(V[e][1])
    piv=set(R.rows);S.require(R.add(V[target][1]),'outside rational row');free,=set(R.rows)-piv;x={free:Q(1)}
    for i in sorted(piv,key=priority.__getitem__,reverse=True):
        row=R.rows[i];val=-sum(c*x[j] for j,c in row.items() if j in x)/Q(row[i])
        if val:x[i]=val
    den=lcm(*(q.denominator for q in x.values()));z={i:int(den*q)for i,q in x.items()};com=gcd(*z.values());return {i:n//com for i,n in z.items()},len(piv)
def value(V,e,pulse):
    d,row=V[e];return Q(sum(pulse[i]*c for i,c in row.items()if i in pulse),d)
def run(src,data,out):
    S=load(src);w=S.load_word(src/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);shadow,=g.routes.keys()-w.routes.keys();V=S.all_public_rows(g);r=json.loads((data/'support.json').read_text())['excluded']+json.loads((data/'rank.json').read_text())['excluded'];receipts=[]
    for rr in sorted(r,key=lambda x:x['donor']):
        d,t=rr['donor'],rr['terminal'];fix=exterior(g,w,shadow,d,t);S.require(len(fix)==rr['boundary_count'],'unpruned fixed exterior')
        if 'unit_axis'in rr:xi={rr['unit_axis']:1};rank=None
        else:xi,rank=derive(S,V,len(w.inputs),fix,t);S.require(rank==rr['boundary_rank'],'same rank')
        S.require(all(not value(V,e,xi)for e in fix),'zero on the entire exterior');target=value(V,t,xi);S.require(target,'nonzero target')
        receipts.append({'donor':d,'native_clock':w.clock[d],'old_route':list(w.routes[d]),'original_grade':w.grade(w.routes[d]),'terminal':t,'exterior_size':len(fix),'exterior_sha256':hashlib.sha256(json.dumps(sorted(fix),separators=(',',':')).encode()).hexdigest(),'original_input':[[i,v]for i,v in sorted(xi.items())],'terminal_value':str(target)})
    S.require(len(receipts)==len({r['donor']for r in receipts})==181,'complete funding roster');out.write_bytes(gzip.compress((json.dumps(receipts,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0));print('all donors',len(receipts),'max pulse',max(len(r['original_input'])for r in receipts),'bytes',out.stat().st_size)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--rank-data',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.sources,a.rank_data,a.out)
